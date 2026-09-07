#!/usr/bin/env python3
"""Build and strictly validate one self-contained diso page from JSON."""
import argparse
from datetime import date
from html import escape
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from check import report, validate
from markup import ROOT, valid_link

LABELS = {
    "en": {
        "site": "diso / Plain, Not Shallow", "contents": "Contents", "figure": "Fig.",
        "p1": "Build the intuition", "p2": "The real mechanism",
        "p3": "Why designed this way", "p4": "Where the analogy breaks",
        "analogy": "Role in the analogy", "component": "Real component", "note": "Note",
        "misconception": "Misconception", "reason": "Why this seems plausible",
        "sources": "Sources", "takeaway": "One-sentence summary", "cheatsheet": "Cheat sheet",
    },
    "zh": {
        "site": "深入浅出", "contents": "目录", "figure": "图",
        "p1": "先建立直觉", "p2": "拆开看真实机制", "p3": "为什么这样设计", "p4": "这个类比在哪里失效",
        "analogy": "类比里的角色", "component": "真实系统里是什么", "note": "说明",
        "misconception": "误解", "reason": "为什么容易这样想",
        "sources": "来源", "takeaway": "一句话总结", "cheatsheet": "速查卡",
    },
}
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
    if not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", lang):
        raise ValueError("lang must be a language tag such as zh-CN or en")
    mode = mode or data.get("mode", "standard")
    if mode not in {"kid", "standard", "deep"}:
        raise ValueError("mode must be kid, standard or deep")
    language = lang.lower().split("-")[0]
    overrides = data.get("labels", {})
    object_fields(overrides, LABELS["en"].keys(), "labels")
    if language not in LABELS and overrides.keys() != LABELS["en"].keys():
        raise ValueError("languages other than en/zh need a complete localized labels object")
    labels = {**LABELS.get(language, LABELS["en"]), **overrides}
    labels = {key: escape(string(value, f"labels.{key}")) for key, value in labels.items()}
    headings = data.get("headings", {})
    object_fields(headings, {"p1", "p2", "p3", "p4"}, "headings")
    for key, value in headings.items():
        string(value, f"headings.{key}")
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
        reason_sep = "：" if language == "zh" else ": "
        boundaries = []
        for i, item in enumerate(list_field(data, "misconceptions"), 1):
            object_fields(item, {"belief", "truth", "reason"}, "misconception")
            boundaries.append(f'<div class="callout"><span class="callout-label">{labels["misconception"]} {i}</span><h3>{text_field(item, "belief")}</h3><p>{text_field(item, "truth")} {labels["reason"]}{reason_sep}{text_field(item, "reason")}</p></div>')
        section("p4", "\n".join(boundaries))
    else:
        section("p4", f'<div class="callout"><p>{text_field(data, "kid_boundary")}</p></div>')
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
    template = (ROOT / "assets/base.html").read_text(encoding="utf-8")
    # One substitution pass: user text containing {{title}} stays literal text.
    return re.sub(r"\{\{([a-z_]+)\}\}", lambda m: values[m[1]], template)


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key {key!r}")
        obj[key] = value
    return obj


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="page JSON (see references/output-template.md)")
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--mode", choices=("kid", "standard", "deep"))
    args = parser.parse_args(argv)
    temporary = None
    try:
        if args.input.resolve() == args.output.resolve():
            raise ValueError("output must not overwrite the input JSON")
        data = json.loads(args.input.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicate_keys)
        raw = render(data, args.mode)
        result = validate(raw)
        report(result, args.output)
        if not result.ok:
            return 1
        # Validate first; atomically replace only once a complete page is ready.
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n", dir=args.output.parent, suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(raw)
        os.replace(temporary, args.output)
        print(f"wrote {args.output}")
        return 0
    except (OSError, UnicodeError, ValueError, TypeError, RecursionError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    finally:
        if temporary and temporary.exists():
            temporary.unlink()


if __name__ == "__main__":
    sys.exit(main())
