#!/usr/bin/env python3
"""Validate diso HTML/SVG (Python 3.10+, stdlib only).

Exit 0 = no findings; 1 = errors OR warnings; 2 = input/usage error.
CSS must match assets/base.html. This is a format validator, not a sanitizer
or browser security sandbox. Editorial quality still needs human review.
"""
import re
import sys
from collections import Counter

from markup import Result, check_markup, parse_html
from svg import check_svgs

LANG_RE = re.compile(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*")


def check_structure(document, nodes, ids, result):
    counts = Counter(n.tag for n in nodes if not n.svg)
    for tag in ("html", "head", "body", "title"):
        if counts[tag] != 1:
            result.error(1, f"expected exactly one HTML <{tag}>")
    if document.doctypes != 1:
        result.error(1, "expected one <!DOCTYPE html>")
    html = next((n for n in nodes if n.tag == "html"), None)
    if not html or not LANG_RE.fullmatch(html.attrs.get("lang", "")):
        result.error(1, "HTML needs a valid lang attribute")
    mode = html.attrs.get("data-mode", "") if html else ""
    if mode not in {"kid", "standard", "deep"}:
        result.error(1, "HTML data-mode must be kid, standard or deep")
    expected = {"p1", "p2", "takeaway", "sources"} | ({"p3"} if mode != "kid" else set())
    for name in expected:
        if name not in ids:
            result.error(0, f"missing required section #{name}")
    for node in nodes:
        if node.tag == "section" and node.has_class("part") and not node.attrs.get("id"):
            result.error(node.line, "section.part needs an id")
        if node.has_class("step-num") and node.ancestor("section") is not ids.get("p1"):
            result.error(node.line, "step numerals belong only in the intuition journey")
    for name in ("takeaway", "colophon", "toc"):
        if sum(n.has_class(name) for n in nodes) != 1:
            result.error(0, f"expected exactly one .{name}")
    labels = [n.text().strip() for n in nodes if n.has_class("step-num")]
    if labels != [f"{i:02d}" for i in range(1, len(labels) + 1)]:
        result.warn(0, "intuition step numerals must be sequential and zero-padded")
    if not 4 <= len(labels) <= 6:
        result.warn(0, "the intuition journey needs 4–6 steps")
    toc = next((n for n in nodes if n.has_class("toc")), None)
    if toc:
        targets = [n.attrs.get("href", "")[1:] for n in toc.walk() if n.tag == "a"]
        sections = [n.attrs.get("id") for n in nodes if n.has_class("part") or n.has_class("takeaway")]
        if targets != sections:
            result.error(toc.line, "TOC must match the rendered sections in order")
    if mode != "deep" and any(n.tag == "details" for n in nodes):
        result.error(0, "formal deep-dive details belong only in deep mode")
    if mode == "kid" and "p3" in ids:
        result.error(0, "kid mode omits the full trade-off section")
    if mode == "deep" and not any(n.tag == "details" for n in nodes):
        result.error(0, "deep mode needs a formal description in <details>")
    for name in ("p2", "sources"):
        if name in ids and not ids[name].text().strip():
            result.error(ids[name].line, f"#{name} must not be empty")


def validate(raw):
    result = Result()
    if "\x00" in raw:
        result.error(0, "NUL characters are unsupported")
    try:
        document = parse_html(raw, result)
        nodes, ids = check_markup(document, result)
        check_svgs(nodes, ids, result)
        check_structure(document, nodes, ids, result)
    except (ValueError, RecursionError) as exc:
        result.error(0, f"invalid document: {exc}")
    return result


def report(result, path):
    for label, items in (("ERROR", result.errors), ("WARN", result.warnings)):
        for line, message in sorted(items):
            print(f"{label:5} {path}{':' + str(line) if line else ''}: {message}")
    print(f"{len(result.errors)} error(s), {len(result.warnings)} warning(s)")
    if result.ok:
        print("clean.")


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or argv[0].startswith("-"):
        print(__doc__ + "\nusage: check.py page.html", file=sys.stderr)
        return 2
    from pathlib import Path
    path = Path(argv[0])
    try:
        raw = path.read_text(encoding="utf-8")
        result = validate(raw)
    except (OSError, UnicodeError) as exc:
        print(f"ERROR {path}: {exc}", file=sys.stderr)
        return 2
    report(result, path)
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
