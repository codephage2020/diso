#!/usr/bin/env python3
"""diso page validator — the machine-checkable half of SKILL.md §5.

    python3 scripts/check.py diso-<topic>.html

Exit 0 = clean. ERROR = a stated ban was broken, fix before shipping.
WARN  = a budget or a threshold was crossed; look, then justify or fix.

Judgment items (substance after deleting analogies, one-concept-one-name,
the "oh, I see" moment, tone, the smallest-view test) are NOT checked here.
No dependencies, stdlib only.
"""
import re
import sys
from collections import Counter

# ---------------------------------------------------------------- palette ---
# The closed set from references/design-tokens.md. Anything else is a leak.
PALETTE = {
    # celadon / terracotta
    "#78c2c4", "#267072", "#9ad8da", "#c47a78", "#8c4644", "#d89d9b",
    # surfaces
    "#f5f4ed", "#faf9f5", "#f0eee6", "#e8e6dc", "#30302e", "#1b2e2e",
    # text levels
    "#141413", "#3d3d3a", "#504e49", "#6b6a64",
    # strokes
    "#e8e6dc", "#e5e3d8",
    # premixed tints
    "#ddefef", "#e9f4f4", "#cde9e9", "#f4e8e7",
    # svg-only surfaces
    "#eae9e2", "#e9e8e1", "#edece3", "#d4e7e7",
}
WASH = {"#78c2c4", "#c47a78"}          # fills only, never text or thin lines
ACCENT_SOLID = WASH                     # counts against the 5% area budget

SVG_NS = "http://www.w3.org/2000/svg"

errors, warns = [], []


def err(line, msg):
    errors.append((line, msg))


def warn(line, msg):
    warns.append((line, msg))


def lineno(text, pos):
    return text.count("\n", 0, pos) + 1


def strip_comments(t):
    """Blank out HTML comments, preserving offsets so line numbers stay true."""
    return re.sub(r"<!--.*?-->", lambda m: re.sub(r"[^\n]", " ", m.group(0)), t, flags=re.S)


# ------------------------------------------------------------ self-contained ---
def check_self_contained(t):
    for m in re.finditer(r"<script\b", t, re.I):
        err(lineno(t, m.start()), "<script> — the page must be zero-JS")
    for m in re.finditer(r"@import|<link\b[^>]*stylesheet", t, re.I):
        err(lineno(t, m.start()), "external stylesheet — everything must be inline")
    for m in re.finditer(r"https?://[^\s\"'<>)]+", t):
        if m.group(0).rstrip("/") != SVG_NS:
            err(lineno(t, m.start()), f"external URL {m.group(0)[:60]} — no links, no CDN")
    # url(#frag) is an internal SVG reference; url(data:) is inline
    for m in re.finditer(r"url\(\s*['\"]?(?![#]|data:)([^)'\"]+)", t, re.I):
        err(lineno(t, m.start()), f"external asset url({m.group(1)[:40]})")


# -------------------------------------------------------------- banned CSS ---
def check_banned_css(t):
    bans = [
        (r"box-shadow", "box-shadow — elevation comes from fill"),
        (r"\b(?:linear|radial|conic)-gradient\(", "gradient"),
        (r"rgba\(", "rgba() — label backgrounds must be plain hex"),
        (r"hsla?\(", "hsl()/hsla() — palette is hex only"),
        (r"font-style:\s*italic", "italics are banned"),
        (r"text-shadow", "text-shadow"),
        (r"backdrop-filter", "backdrop-filter / glassmorphism"),
    ]
    for pat, msg in bans:
        for m in re.finditer(pat, t, re.I):
            err(lineno(t, m.start()), msg)

    for m in re.finditer(r"border-radius:\s*([\d.]+)px", t, re.I):
        if float(m.group(1)) > 10:
            err(lineno(t, m.start()), f"border-radius {m.group(1)}px > 10px")
    for m in re.finditer(r"\br[xy]=\"([\d.]+)\"", t):
        if float(m.group(1)) > 10:
            err(lineno(t, m.start()), f"svg r{m.group(0)[1]} {m.group(1)} > 10")
    for m in re.finditer(r"font-weight:\s*(\d+)", t, re.I):
        if int(m.group(1)) > 500:
            err(lineno(t, m.start()), f"font-weight {m.group(1)} — locked to 400/500")
    for m in re.finditer(r"font-weight:\s*bold|<(?:b|strong)\b(?![^>]*font-weight)", t, re.I):
        if m.group(0).lower().startswith("font-weight"):
            err(lineno(t, m.start()), "font-weight:bold — locked to 400/500")


# ------------------------------------------------------------------ colors ---
def check_colors(t):
    seen = Counter()
    for m in re.finditer(r"#[0-9a-fA-F]{6}\b", t):
        h = m.group(0).lower()
        seen[h] += 1
        if h not in PALETTE:
            r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
            cold = " (cold gray: B ≥ R)" if b >= r else ""
            err(lineno(t, m.start()), f"{h} is outside the palette{cold}")
    # wash used where only ink is legible
    for m in re.finditer(r"<text\b[^>]*fill=\"(#[0-9a-fA-F]{6})\"", t):
        if m.group(1).lower() in WASH:
            err(lineno(t, m.start()), f"{m.group(1)} as text fill — illegible, use its ink density")
    for m in re.finditer(r"stroke=\"(#[0-9a-fA-F]{6})\"([^>]*)", t):
        if m.group(1).lower() not in WASH:
            continue
        w = re.search(r"stroke-width=\"([\d.]+)\"", m.group(2))
        if not w or float(w.group(1)) < 2:
            err(lineno(t, m.start()),
                f"{m.group(1)} as a thin stroke — wash is for fills; the only exception "
                f"is the 2.5px focus path")
    if "#ffffff" in t.lower() or re.search(r"background:\s*#fff\b", t, re.I):
        err(0, "pure white surface — the canvas is parchment #f5f4ed")
    return seen


# -------------------------------------------------------------------- svgs ---
def iter_svgs(t):
    for m in re.finditer(r"<svg\b.*?</svg>", t, re.S):
        yield m.start(), m.group(0)


def check_svgs(t):
    svgs = list(iter_svgs(t))
    if not svgs:
        warn(0, "no <svg> — the intuition journey is built on figures")
    for pos, s in svgs:
        ln = lineno(t, pos)
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
        if not vb:
            err(ln, "svg has no viewBox=\"0 0 960 H\"")
        elif vb.group(1) != "960":
            err(ln, f"viewBox width {vb.group(1)} — always 960")
        if "<title>" not in s:
            err(ln, "svg missing <title> (accessibility)")
        if "<desc>" not in s:
            warn(ln, "svg missing <desc>")
        if "<marker" in s:
            err(ln, "<marker> — arrowheads are hand-drawn chevrons")

        # one accent hue per figure
        focus = len(re.findall(r'<rect[^>]*fill="#78C2C4"', s, re.I))
        warnn = len(re.findall(r'<rect[^>]*fill="#C47A78"', s, re.I))
        if focus and warnn:
            err(ln, "celadon focus and terracotta warning in the same figure — one hue per diagram")
        if focus > 2:
            err(ln, f"{focus} focus nodes — at most 2")
        if warnn > 1:
            err(ln, f"{warnn} warning nodes — at most 1")

        dots = len(re.findall(r'<circle[^>]*r="12"[^>]*fill="#267072"', s, re.I))
        if dots > 6:
            err(ln, f"{dots} sequence dots — at most 6, split the figure")
        groups = len(re.findall(r'<rect[^>]*fill="#EDECE3"', s, re.I))
        if groups > 2:
            err(ln, f"{groups} group containers — at most 2")

        # orthogonal edges only (3-point chevrons exempt)
        for pm in re.finditer(r'<path[^>]*\sd="([^"]+)"', s):
            d = pm.group(1)
            pts = re.findall(r"([MLl])\s*(-?[\d.]+)[ ,](-?[\d.]+)", d)
            if len(pts) == 3 and d.count("L") == 2:
                continue                                  # arrowhead
            for (_, x1, y1), (_, x2, y2) in zip(pts, pts[1:]):
                if float(x1) != float(x2) and float(y1) != float(y2):
                    err(lineno(t, pos + pm.start()),
                        f"diagonal segment {x1},{y1}→{x2},{y2} — edges are 0°/90° only")
                    break

        # layout coordinates land on the 4px grid (rects only; baselines derive)
        off = []
        for rm in re.finditer(r"<rect\b[^>]*>", s):
            for a in ("x", "y", "width", "height"):
                v = re.search(rf'\b{a}="(-?\d+)"', rm.group(0))
                if v and int(v.group(1)) % 4:
                    off.append(f"{a}={v.group(1)}")
        if off:
            err(ln, f"rect coords off the 4px grid: {', '.join(off[:6])}")

        # text baselines must clear their own cap height
        for tm in re.finditer(r'<text\b[^>]*\by="([\d.]+)"[^>]*font-size="([\d.]+)"|'
                              r'<text\b[^>]*font-size="([\d.]+)"[^>]*\by="([\d.]+)"', s):
            y = float(tm.group(1) or tm.group(4))
            fs = float(tm.group(2) or tm.group(3))
            if y < fs * 1.2:
                err(lineno(t, pos + tm.start()),
                    f"text baseline y={y:g} < font-size {fs:g} × 1.2 — top will clip")

    # accent area budget: solid wash fills as a share of drawn canvas
    total = accent = 0
    for _, s in svgs:
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', s)
        if vb:
            total += int(vb.group(1)) * int(vb.group(2))
        for rm in re.finditer(r"<rect\b[^>]*>", s):
            tag = rm.group(0)
            f = re.search(r'fill="(#[0-9a-fA-F]{6})"', tag)
            w = re.search(r'width="(\d+)"', tag)
            h = re.search(r'height="(\d+)"', tag)
            if f and w and h and f.group(1).lower() in ACCENT_SOLID:
                accent += int(w.group(1)) * int(h.group(1))
    if total:
        pct = 100 * accent / total
        if pct > 5:
            warn(0, f"solid accent fills ≈{pct:.1f}% of figure area — budget is 5%")


# ------------------------------------------------------------------ layout ---
def check_structure(t):
    ids = set(re.findall(r'\bid="([^"]+)"', t))
    for m in re.finditer(r'<a\b[^>]*href="#([^"]+)"', t):
        if m.group(1) not in ids:
            err(lineno(t, m.start()), f'TOC anchor #{m.group(1)} resolves to nothing')
    for m in re.finditer(r'<section\b[^>]*class="[^"]*\bpart\b[^"]*"[^>]*>', t):
        if "id=" not in m.group(0):
            err(lineno(t, m.start()), "section.part without an id — the TOC cannot reach it")

    if not re.search(r"<html[^>]*\blang=", t, re.I):
        err(1, "<html> missing lang=")
    zh = bool(re.search(r'<html[^>]*lang="zh', t, re.I))
    if zh and "letter-spacing:0.3px" not in t.replace(" ", ""):
        warn(0, "Chinese page without body letter-spacing:0.3px")
    if not zh and re.search(r"text-justify:\s*inter-ideograph", t, re.I):
        warn(0, "English page using inter-ideograph justification — use text-align:start")

    for pat, msg in [
        (r'class="takeaway"', "no .takeaway closing block"),
        (r'class="colophon"', "no .colophon line"),
        (r"@media\s+print", "no print styles"),
        (r"scroll-margin-top", "no scroll-margin-top — anchor jumps will glue to the top"),
    ]:
        if not re.search(pat, t, re.I):
            err(0, msg)

    if len(re.findall(r'class="takeaway"', t)) > 1 or \
       len(re.findall(r"var\(--deep-dark\)|#1B2E2E", t, re.I)) > 3:
        warn(0, "more than one dark block — the closing block should be the only one")

    # step numerals live only in the intuition journey
    nums = [m.start() for m in re.finditer(r'class="step-num"', t)]
    parts = [m.start() for m in re.finditer(r'<section\b[^>]*class="[^"]*\bpart\b', t)]
    if nums and len(parts) > 1 and max(nums) > parts[1]:
        err(lineno(t, max(nums)), "step numerals outside Part 1 — scarcity is the point")
    labels = re.findall(r'class="step-num">\s*(\d+)', t)
    if labels and labels != [f"{i:02d}" for i in range(1, len(labels) + 1)]:
        warn(0, f"step numerals not zero-padded and sequential: {labels}")
    if labels and not 4 <= len(labels) <= 6:
        warn(0, f"{len(labels)} intuition steps — the skeleton asks for 4–6")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    raw = open(path, encoding="utf-8").read()
    t = strip_comments(raw)

    check_self_contained(t)
    check_banned_css(t)
    check_colors(t)
    check_svgs(t)
    check_structure(t)

    for label, items in (("ERROR", errors), ("WARN", warns)):
        for ln, msg in sorted(items):
            where = f"{path}:{ln}" if ln else path
            print(f"{label:5} {where}: {msg}")

    kb = len(raw.encode()) / 1024
    print(f"\n{len(errors)} error(s), {len(warns)} warning(s) — {kb:.1f} KB")
    if not errors and not warns:
        print("clean.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
