#!/usr/bin/env python3
"""Build and strictly validate one self-contained diso page from JSON."""
from html import escape
import os
import re
import sys

from markup import ROOT, valid_link

LANG_RE = re.compile(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*")
PLACEHOLDER_RE = re.compile(r"\{\{([a-z_]+)\}\}")

LABELS = {
    "en": {
        "site": "diso / Plain, Not Shallow", "contents": "Contents", "figure": "Fig.",
        "p1": "Build the intuition", "p2": "The real mechanism",
        "p3": "Why designed this way",
        "analogy": "Role in the analogy", "component": "Real component", "note": "Note",
        "sources": "Sources", "takeaway": "One-sentence summary", "cheatsheet": "Cheat sheet",
    },
    "zh": {
        "site": "深入浅出", "contents": "目录", "figure": "图",
        "p1": "先建立直觉", "p2": "拆开看真实机制", "p3": "为什么这样设计",
        "analogy": "类比里的角色", "component": "真实系统里是什么", "note": "说明",
        "sources": "来源", "takeaway": "一句话总结", "cheatsheet": "速查卡",
    },
}
# Accept retired section fields so existing JSON remains rebuildable.
FIELDS = {"title", "lang", "mode", "date", "essence", "takeaway", "steps", "mapping",
          "mechanism_html", "tradeoffs_html", "misconceptions", "kid_mechanism", "kid_boundary",
          "deep_html", "deep_title", "cheatsheet_html", "sources", "labels", "headings"}


def object_fields(value, allowed, context):
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    unknown = value.keys() - allowed
    if unknown:
        raise ValueError(f"unknown {context} fields: {', '.join(sorted(unknown))}")


def string(value, context):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{context} must be a nonempty string")
    return value


def text_field(obj, key):
    return escape(string(obj.get(key), key), quote=True)


def list_field(obj, key, minimum=1, maximum=None):
    value = obj.get(key)
    if not isinstance(value, list) or len(value) < minimum or (maximum and len(value) > maximum):
        raise ValueError(f"{key} must be an array with {minimum}–{maximum or 'many'} items")
    return value


def render(data, mode=None):
    """Escape ordinary strings; explicit *_html and svg fields are validated markup.

    Never execute or fetch anything from the input. The caller must run validate
    before persisting the returned HTML; the CLI does so before touching output.
    """
    object_fields(data, FIELDS, "page")
    lang = string(data.get("lang"), "lang")
    if not LANG_RE.fullmatch(lang):
        raise ValueError("lang must be a language tag such as zh-CN or en")
    mode = mode or data.get("mode", "standard")
    if mode not in {"kid", "standard", "deep"}:
        raise ValueError("mode must be kid, standard or deep")
    language = lang.lower().split("-")[0]
    overrides = data.get("labels", {})
    object_fields(overrides, LABELS["en"].keys() | {"p4", "misconception", "reason"}, "labels")
    overrides = {key: value for key, value in overrides.items() if key in LABELS["en"]}
    if language not in LABELS and overrides.keys() != LABELS["en"].keys():
        raise ValueError("languages other than en/zh need a complete localized labels object")
    labels = {**LABELS.get(language, LABELS["en"]), **overrides}
    labels = {key: escape(string(value, f"labels.{key}")) for key, value in labels.items()}
    headings = data.get("headings", {})
    object_fields(headings, {"p1", "p2", "p3", "p4"}, "headings")
    headings = {key: value for key, value in headings.items() if key != "p4"}
    for key, value in headings.items():
        string(value, f"headings.{key}")
    from datetime import date
    generated = data.get("date", date.today().isoformat())
    if not isinstance(generated, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", generated):
        raise ValueError("date must be YYYY-MM-DD")
    date.fromisoformat(generated)

    content, toc = [], []

    def section(key, body):
        label = labels[key]
        title = escape(headings[key]) if key in headings else label
        toc.append(f'<a href="#{key}"><span>{label}</span></a>')
        part = f"Part {len(toc)} · " if key.startswith("p") and key[1:].isdigit() else ""
        content.append(f'<section class="part" id="{key}">\n<div class="part-eyebrow">{part}{label}</div>\n<h2>{title}</h2>\n{body}\n</section>')

    content.append(f'<header class="hero"><div class="eyebrow">{labels["site"]}</div>\n<h1>{text_field(data, "title")}</h1>\n<p class="essence">{text_field(data, "essence")}</p><div class="rule"></div></header>')
    steps = []
    figure_count = 0
    for i, step in enumerate(list_field(data, "steps", 4, 6), 1):
        object_fields(step, {"title", "label", "text", "svg", "caption"}, f"step {i}")
        figure = ""
        if "svg" in step:
            figure_count += 1
            svg = string(step["svg"], f"step {i} svg")
            figure = f'<figure>\n{svg}\n<figcaption><span class="fig-label">{labels["figure"]} {figure_count} ·</span>{text_field(step, "caption")}</figcaption></figure>'
        elif "caption" in step:
            raise ValueError(f"step {i} has a caption but no svg")
        steps.append(f'<div class="step">{figure}\n<div class="step-head"><span class="step-num">{i:02d}</span><span class="step-label">{text_field(step, "label")}</span></div>\n<h3>{text_field(step, "title")}</h3><p class="step-txt">{text_field(step, "text")}</p></div>')
    section("p1", "\n".join(steps))

    rows = []
    for row in list_field(data, "mapping", 3):
        if not isinstance(row, list) or len(row) != 3:
            raise ValueError("each mapping row needs three strings")
        rows.append("<tr>" + "".join(f"<td>{escape(string(v, 'mapping cell'))}</td>" for v in row) + "</tr>")
    mapping = '<table><thead><tr>' + "".join(f"<th>{labels[k]}</th>" for k in ("analogy", "component", "note")) + '</tr></thead><tbody>' + "".join(rows) + '</tbody></table>'
    mechanism = f'<p>{text_field(data, "kid_mechanism")}</p>' if mode == "kid" else string(data.get("mechanism_html"), "mechanism_html")
    if mode == "deep":
        mechanism += f'<details><summary>{text_field(data, "deep_title")}</summary><div class="dbody">{string(data.get("deep_html"), "deep_html")}</div></details>'
    section("p2", mapping + "\n" + mechanism)

    if mode != "kid":
        section("p3", string(data.get("tradeoffs_html"), "tradeoffs_html"))
    if mode == "deep" and data.get("cheatsheet_html"):
        section("cheatsheet", string(data["cheatsheet_html"], "cheatsheet_html"))

    sources = []
    for item in list_field(data, "sources"):
        object_fields(item, {"title", "url", "note"}, "source")
        title = text_field(item, "title")
        if "url" in item:
            url = string(item["url"], "source URL")
            if not valid_link(url) or url.startswith("#"):
                raise ValueError("source URLs must be absolute HTTP(S) links")
            title = f'<a href="{escape(url, quote=True)}">{title}</a>'
        sources.append(f'<li>{title} — {text_field(item, "note")}</li>')
    section("sources", '<ol class="sources">' + "\n".join(sources) + '</ol>')
    toc.append(f'<a href="#takeaway"><span>{labels["takeaway"]}</span></a>')
    content.append(f'<div class="takeaway" id="takeaway"><div class="eyebrow">{labels["takeaway"]}</div><p>{text_field(data, "takeaway")}</p></div>\n<div class="colophon">{generated} · Generated by diso</div>')
    values = {"lang": escape(lang), "mode": mode, "title": text_field(data, "title"),
              "contents_label": labels["contents"], "toc": "\n".join(toc), "content": "\n".join(content)}
    template = open(os.path.join(ROOT, "assets", "base.html"), encoding="utf-8").read()
    # One substitution pass: user text containing {{title}} stays literal text.
    def substitute(match):
        if match[1] not in values:
            raise ValueError(f"unknown placeholder {{{{{match[1]}}}}} in assets/base.html")
        return values[match[1]]
    return PLACEHOLDER_RE.sub(substitute, template)


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key {key!r}")
        obj[key] = value
    return obj


def main(argv=None):
    # Hand-rolled parsing: the CLI has one fixed shape and argparse costs
    # more import time than the whole render.
    argv = sys.argv[1:] if argv is None else argv
    usage = __doc__ + "\nusage: build.py input.json -o output.html [--mode kid|standard|deep]"
    input_path = output = mode = None
    it = iter(argv)
    for arg in it:
        if arg in ("-o", "--output") and output is None:
            output = next(it, None)
        elif arg == "--mode" and mode is None:
            mode = next(it, None)
        elif not isinstance(arg, str) or arg.startswith("-") or input_path is not None:
            print(usage, file=sys.stderr)
            return 2
        else:
            input_path = arg
    if input_path is None or output is None:
        print(usage, file=sys.stderr)
        return 2
    if mode not in (None, "kid", "standard", "deep"):
        print("ERROR: --mode must be kid, standard or deep", file=sys.stderr)
        return 2
    # Imported here, not at module top: tests import render() directly, and the
    # CLI is the only caller that needs the validator and JSON machinery.
    from check import report, validate
    from json import loads
    from pathlib import Path
    input_path, output = Path(input_path), Path(output)
    temporary = output.with_name(output.name + ".tmp")
    try:
        if input_path.resolve() == output.resolve():
            raise ValueError("output must not overwrite the input JSON")
        data = loads(input_path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
        raw = render(data, mode)
        result = validate(raw)
        report(result, output)
        if not result.ok:
            return 1
        # Validate first; atomically replace only once a complete page is ready.
        temporary.write_text(raw, encoding="utf-8", newline="\n")
        os.replace(temporary, output)
        print(f"wrote {output}")
        return 0
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    finally:
        temporary.unlink(missing_ok=True)


if __name__ == "__main__":
    sys.exit(main())
