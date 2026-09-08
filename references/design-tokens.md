# Design Tokens (diso · Celadon Edition)

One line: **a parchment canvas, two accent hues with divided semantics (celadon & terracotta, each in two densities), serif for hierarchy, numerals for rhythm — no cold grays, no hard shadows.**
This is not a UI framework; it is a constraint system for print. The page must read as a typeset sheet of paper, not a dashboard.

> **This file is the law; `assets/base.html` is the CSS implementation.** Every rule here is already encoded in the bundled stylesheet — let `build.py` copy it, never retype it. This file exists to tell you *which* class to reach for and *why*, and to carry the rules (SVG, above all) that no stylesheet can express.
> **Language**: written in English for the generator. All visible copy in the produced HTML must match the user's request language (see the string map in `output-template.md`).

---

## 1. Eleven invariants (think about the cost before overriding any)

1. Page background is parchment `#f5f4ed` — **never pure white**
2. Two accent hues with **semantic division**: **celadon** `#78C2C4` owns focus, structure, and the positive (gains, paths, navigation); **terracotta** `#C47A78` owns warning, cost, and failure. They are complementary hues — never swap their semantics ("gained" is never red, "cost" is never celadon). Each hue ships in a wash (fills only) and an ink (text and thin lines). **No third hue**
3. Combined solid accent rectangle fills ≤ **5%** of total SVG canvas area (the mechanical proxy); text and thin lines do not count. Also review the whole page visually for excessive accent area
4. All grays are warm (yellow-brown base); no cold blue-grays
5. One serif family carries both headings and body
6. Serif weights locked to **400 / 500** — no bold (900/100 banned, `strong` locked to 500)
7. Line heights: headings 1.10–1.30, reading text 1.50–1.55, CJK screen body 1.55–1.65
8. Chinese body `letter-spacing: 0.3px`; English body 0; only short labels and overlines get tracking
9. Label backgrounds must be **plain hex** — never `rgba()`
10. Surfaces are flat; shadows are banned in generated pages
11. **No italics** (`font-style: italic`)

---

## 2. Palette

The full `:root` block lives in `assets/base.html`; the builder copies it unchanged. This table says what each token is *for*; the closed set below is enforced on SVG paint attributes, while HTML CSS must match the bundled asset. Only six-digit hex, `none`, and local pattern references are supported in SVG paint attributes; named/computed colors and CSS variables are rejected.

| Token | Hex | Owns |
|---|---|---|
| `--brand` | `#78C2C4` | celadon wash — focus fills, tints, accents on dark |
| `--brand-ink` | `#267072` | celadon ink — text emphasis, hairlines, small glyphs |
| `--brand-light` | `#9AD8DA` | labels & keywords on dark surfaces |
| `--accent` | `#C47A78` | terracotta wash — warning fills, failure paths (never text) |
| `--accent-ink` | `#8C4644` | terracotta ink — cost/misconception labels, risk emphasis |
| `--accent-light` | `#D89D9B` | warning words on dark |
| `--parchment` | `#f5f4ed` | page background — the emotional base |
| `--ivory` | `#faf9f5` | quiet filled container, one step lighter |
| `--inline-code-bg` | `#f0eee6` | inline code, one step darker |
| `--warm-sand` | `#e8e6dc` | default button face |
| `--dark-surface` | `#30302e` | dark container, warm charcoal |
| `--deep-dark` | `#1B2E2E` | closing block (the only cool-leaning surface allowed) |
| `--near-black` | `#141413` | primary text |
| `--dark-warm` | `#3d3d3a` | secondary text, table headers |
| `--olive` | `#504e49` | captions, notes |
| `--stone` | `#6b6a64` | dates, metadata |
| `--border` / `--border-soft` | `#e8e6dc` / `#e5e3d8` | structural hairlines |
| `--tag-bg` | `#DDEFEF` | chip label background |
| `--brand-tint` | `#E9F4F4` | faintest celadon wash — neutral/positive asides |
| `--selection-bg` | `#CDE9E9` | text selection |
| `--accent-tint` | `#F4E8E7` | faintest terracotta wash — misconception callouts |

SVG-only surfaces, not in `:root`: `#EAE9E2` storage node · `#E9E8E1` external node · `#EDECE3` group container · `#D4E7E7` dot texture.

**Four text levels — there is no fifth.** **Banned**: `#ffffff` as page background; `#f8f9fa` / `#f3f4f6` and every other cold gray surface; any color outside the families above.
**Warm-gray test**: in `rgb()`, R ≈ G > B (or R > G > B with small deltas). A cold gray is R < G < B or R = G = B.

### Why two densities (measured, not estimated)

| Pair | Contrast | Verdict |
|---|---|---|
| `#78C2C4` on parchment | 1.85:1 | fills only |
| `#C47A78` on parchment | 2.97:1 | fills only |
| `#267072` on parchment | 5.23:1 | text & lines |
| `#8C4644` on parchment | 6.19:1 | text & lines |
| `#f5f4ed` on `#267072` | 5.23:1 | sequence-dot numerals |
| `#141413` on `#78C2C4` | 9.05:1 | focus-node text (white would be 2:1 — banned) |
| `#D89D9B` on `#1B2E2E` | 6.24:1 | warning words on dark |

Both washes are illegible as body text or 1.5px rules; both inks carry them safely. This is the print division of labor — **"wash lays the surface, ink draws the line"** — and both hues obey the same discipline.

### Which density? Quick reference

| Use | Density |
|---|---|
| Inline term emphasis, overline labels, figure emphasis, list markers, step numerals | `--brand-ink` |
| Inline emphasis for cost / risk / failure (`.alert`) | `--accent-ink` |
| Structural hairlines (table rules, dividers, hero rule) | still `--border` — accents never take over gray's job |
| SVG main edges, focus-node strokes, sequence-dot fills | `--brand-ink` |
| SVG focus-node fills, dot texture, large tint areas | `--brand` / `--brand-tint` |
| SVG failure/rollback paths, warning nodes | `--accent-ink` strokes / `--accent` fills |
| Misconception callout background & label | `--accent-tint` / `--accent-ink` |
| Versus "cost" card label | `--accent-ink` |
| Labels & keywords inside the dark closing block | `--brand-light` |
| Warning words inside the dark closing block | `--accent-light` |
| Text-selection highlight | `--selection-bg` |

---

## 3. Type

The `--serif` / `--mono` stacks are in `assets/base.html`'s `:root`. What they encode:

- The preferred Chinese serif is TsangerJinKai02, but it needs a local font file and a self-contained page cannot link fonts — hence the fallback chain. **Latin families come first** so mixed CJK/Latin text shares a baseline.
- Families are written under both English and localized names (`"Source Han Serif SC"` / `"思源宋体"`, `SimSun` / `"宋体"`): Windows often registers fonts under localized names, and dual naming hits more often.
- The mono stack includes `"Cascadia Code"` (ships with Windows 11), and its CJK fallback lands on **serif** so Chinese inside code blocks never jumps to a gothic.
- Body carries `font-kerning`, `text-rendering:optimizeLegibility`, and `hanging-punctuation:first allow-end` (CJK punctuation overhang — cleaner justified edges). Unsupported browsers ignore them; zero cost.
- **Weights**: body 400, headings 500. `strong{font-weight:500}` is locked so browsers can't synthesize 700.
- **Figures**: stats and numerals always take `font-variant-numeric: lining-nums tabular-nums`.
- **CJK justification**: body paragraphs use `text-align:justify; text-justify:inter-ideograph`. English pages revert to `text-align:start`.

**Screen size scale** (px) — land on the rungs, never between them. Body floor is 14px.

| Role | Size | Weight | Line height |
|---|---|---|---|
| H1 / hero title | 48 | 500 | 1.18 |
| Stat figure | 34 | 500 | 1.10 |
| H2 section title | 30 | 500 | 1.25 |
| Step numeral | 30 | 400 | 1.00 |
| H3 step title | 21 | 500 | 1.30 |
| Lede / essence | 20–22 | 400 | 1.60 |
| Reading body | 18 | 400 | 1.65 |
| Caption / note | 15 | 400 | 1.50 |
| Overline label | 12 | 500 | 1.35 |

---

## 4. Components — which class, and the rule that governs it

Every class below is already styled in `assets/base.html`. Use the authoring reference for markup and obey the rule here.

| Class | Rule of use |
|---|---|
| `.card` | Elevation by **fill**, never strokes. **No closed hairline borders** (sub-1px border + radius renders as a double ring). Need more weight? Strengthen the label or the first sentence — never add a four-sided accent line |
| `.step-num` + `.step-label` | Zero-padded `01 02 03`. The page's only large decorative element, so it appears **only in the intuition journey**. Scarcity is the point |
| `.stats` / `.stat` | Order-of-magnitude "oh, I see" facts only. 2–4 per row; one big number + a note ≤15 chars (CJK) / ≤8 words (EN). Units go inside `<b>` (`5ms`); the note states the comparison baseline |
| `.versus` | Only for a **two-item** gained-vs-cost pair. Gain = celadon-ink label, cost = terracotta-ink label — distinguished by **text color, not fill**, so the area budget holds. Three or more columns → a table |
| `.callout` | The exclusive surface for "where the analogy breaks". A reader who sees the terracotta wash knows the analogy just failed. `--brand-tint` is for neutral/positive asides — **never tint an ordinary note red** |
| `.diff` | For an evolution (old design → new design). `+` / `-` are literal text so the block stays copyable; add = celadon ink, remove = terracotta ink; **no per-line background tints**. Keep context lines to the minimum that orients the reader. Shape matches the topic — file tree, call tree, control flow, pseudocode all valid |
| `blockquote` | One sentence worth quoting verbatim. **No side bar** — size and gray level do the separating |
| `table` | Rows separate by **whitespace first, line weight second**. No vertical rules, no boxed frame, no tinted header, no zebra striping (an `--ivory` even-row fill is allowed only at ≥8 rows). Numeric columns take `.num` |
| `pre` / `code` | Ivory fill, no border |
| `.term` | Inline term emphasis: brand ink + 500, **no background block** (stacked chips in prose blow the budget) |
| `.alert` | Same spec, terracotta ink, for cost/risk/boundary phrases. **At most one per sentence, never two in a paragraph** |
| chip label | `--tag-bg` background + brand ink, for short labels only |
| `::selection` | The only permitted non-structural color block — it encodes state, not decoration |
| `ul li::marker` | Native markers in brand ink. **Never fake dashes with `::before`** — that's default AI output, not editorial typesetting |
| `.colophon` | After the takeaway: generation date + "Generated by diso". One line, no links |
| `.toc` | One 22px warm-gray dash per section, hover extends to 36px celadon ink and slides the label in. Hidden ≤1240px. Every section needs an `id` + `scroll-margin-top`. **The cost of zero JS**: no scroll-spy active state — do not sneak in a `<script>` to fix it. Every anchor must resolve to a real section |
| `summary:focus-visible` | Interactive elements are `<summary>`, TOC anchors and citation links; all keep a visible focus ring |
| `@media print` | Parchment survives via `print-color-adjust:exact`; figures and cards never break across pages |

### The subtraction principle (critical)

A line earns its existence only when it **separates regions, encodes state, or carries a data relationship**.
**Banned**: decorative eyebrow bars, vertical rules beside headings, quote side bars, callout accent edges, cover flourishes (the short celadon segment on the hero rule is the single exception).
Test: hide the line — if meaning, state, grouping, and navigation are all unchanged, delete it and buy the pause back with spacing.

---

## 5. SVG diagram rules

SVG geometry is authored with attributes; custom CSS and transforms are unsupported. Ready-made snippets are in `output-template.md`.

### Canvas
- Background must be `#f5f4ed` — **never pure white**
- **Layout coordinates land on a 4px grid**: every `<rect>` `x/y/width/height`, every edge endpoint, every group-container bound. Derived values — text baselines, chevron arms, dot centers — follow from those and are exempt
- `viewBox` width is always `960`; height follows content
- Text baseline `y ≥ font-size × 1.2` (otherwise the top clips)
- Dot texture: pattern 24×24, `circle r="0.8"` fill `#D4E7E7`, layer `opacity="0.55"` — a faint celadon lean so every diagram shares the page's color temperature
- Every `<svg>` carries `<title>` and `<desc>` — figures are content, not decoration

### Nodes
| Role | Fill | Stroke | Text |
|---|---|---|---|
| Standard node | `#faf9f5` | `#141413` | `#141413` |
| Storage node | `#EAE9E2` | `#504e49` | `#141413` |
| External node | `#E9E8E1` | `#6b6a64` | `#141413` |
| **Focus node** | `#78C2C4` (solid) | `#267072` (1.5px) | `#141413`, `font-weight 500` |
| **Warning node** | `#C47A78` (solid) | `#8C4644` (1.5px) | `#141413`, `font-weight 500` |

The focus node is the page's heaviest stroke of celadon: **solid fill + ink stroke + dark text**, 1–2 per diagram at most. White text banned (2:1 on celadon).
Warning nodes use the same spec in terracotta: only for "this fails / this gets eliminated / this pays the price". **One accent hue per diagram** — a focus diagram is all celadon, a warning diagram all terracotta; never both in one figure.
Node widths come in three sizes only: `128 / 144 / 160`; heights in two: `32 / 64` (pill / standard). Mark system nodes with `data-node="true"`; rounded stroked rectangles are also checked as nodes automatically. Canvas/texture fills, canvas-colored label pads, unstroked group/illustration shapes and square-corner book bars are not system nodes. They still obey the 4px rectangle grid. Never relabel a node as an illustration to evade its size constraint.

### Group containers
When several nodes belong to one subsystem, cover them with a large rounded rect, **fill `#EDECE3`, no stroke**, with a small mono group name (`#504e49`) at the top-left. Draw containers before nodes (bottom layer). At most 2 per diagram; a single group gets none.

### Edges
- **Orthogonal only — 0° or 90°, diagonals explicitly banned.** No curves, no crossing modules, no text overruns, no decorative joints. Direction changes at a right angle (routing patterns in `output-template.md`)
- **Every edge attaches**: both endpoints land on a node edge *at its midpoint*, on a bus, or on a timeline. Dangling arrows into empty space are banned; so are lines ending at node corners
- Main edges `#267072`, secondary edges `#504e49`
- The diagram's single **focus path** may use `#78C2C4` thickened to `stroke-width 2.5`; a **failure/rollback path** uses `#8C4644` (1.5px, matching chevron). Pick one per diagram — never both
- **4px clearance**: an edge starts 4px off the source edge, the arrowhead lands 4px off the target edge, snapped to node boundaries
- **Never run an edge along a module's top edge** (reads as a broken frame)
- Focus means **1–2 nodes**, not painting every "important" node celadon; warning nodes at most 1
- **Timeline rule**: line and vertical stubs first, dots on top; every node below a timeline gets a stub connecting it to the line — no floating nodes

### Arrowheads: hand-drawn chevrons, never `<marker>`
Open two-stroke marks read as "editorial diagram", not technical UI. `<marker orient="auto">` doesn't rotate under WeasyPrint — banned. Chevrons are colored like their edge, arms stay 5×7, caps and joins always round. Down is `Mx,y Lx+5,y+7 Lx+10,y`; right is `Mx,y Lx+7,y+5 Lx,y+10`; up and left are mirrors.

### Edge labels
On-edge text (`RTT`, `ACK`) sits on a backing rect in the canvas color `#f5f4ed` (not ivory), 4px radius, 8px padding all round, so it doesn't fight the dot texture.

### Sequence dots
Celadon-ink solid circle (`r=12`) + parchment numeral, to show execution order. At most 6 per diagram; beyond that, split the figure.

### SVG text
| Role | Color |
|---|---|
| Primary | `#141413` |
| Secondary | `#504e49` |
| Tertiary / small mono labels | `#6b6a64` |
| Text inside focus/warning nodes | `#141413` |
| Numerals inside sequence dots | `#f5f4ed` |

**Never use `#78C2C4` / `#C47A78` as SVG text or thin strokes** — see the contrast table in §2.
The `font-family` attribute of SVG `<text>` must match the page chain; if the full chain won't fit, write at least `Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif` so CJK falls back to a serif instead of the browser's default gothic.
Scale-compensate font sizes: rendered width ÷ viewBox width ≈ 0.74, so to render 18px you write `font-size="24"`.
→ **Node primary text 26, secondary 24, small mono labels 20, sequence-dot numerals 16.**

### SVG bans
`rgba()` in `fill`/`stroke` · gradients · `box-shadow` · 3D · glassmorphism · emoji faces, mascots, anthropomorphic characters · imported icon fonts · SVG sprites · radius > 10px · legends floating over the drawing area · unbacked text on arrows.

---

## 6. Light/dark alternation

Use near-black celadon `#1B2E2E` only for the closing takeaway against the parchment `#f5f4ed` page.
Text on dark: body in parchment, labels and keywords in `--brand-light`, warning words in `--accent-light`. `box-shadow: 0 2px 8px rgba(0,0,0,0.3)` and its kin stay banned.
**At most one** dark block per page (the takeaway); Part sections stay parchment so the closing black remains the only accent of weight.

---

## 7. Quick decision table

| Need | Use |
|---|---|
| Display heading | Serif 500, size by level, line height 1.10–1.30 |
| Emphasize a figure / term | `.term` — brand ink, 500, no background block |
| Emphasize cost / risk / failure inline | `.alert` — accent ink, 500, at most one per sentence |
| An order-of-magnitude "oh" moment | `.stats` cards, 2–4 per row |
| Step guidance in the intuition journey | `.step-num` + `.step-label` (this section only) |
| Paired gained-vs-cost trade-off | `.versus` twin cards; more than two items → table |
| An evolution: old design → new design | `.diff` (add = celadon ink, remove = terracotta ink) |
| Lift a block above body text | ivory fill + 8px radius, no accent edge |
| A sentence worth quoting verbatim | `blockquote`, one size up, no side bar |
| Cost or risk callouts | `.callout` — terracotta wash + terracotta-ink label |
| Key node in a diagram | `#78C2C4` solid + `#267072` stroke, 1–2 per figure |
| A node that fails / gets eliminated | `#C47A78` solid + `#8C4644` stroke, ≤1, never beside a celadon focus |
| Execution order in a diagram | celadon-ink sequence dots, ≤6 per figure |
| Subsystem grouping in a diagram | `#EDECE3` unstroked cover, ≤2 per figure |
| Showing code | ivory fill, no border |
| Opening a section | serif scale and margins; overline in celadon ink |
| Marking one item in a list | ivory fill, a stronger label, or a lead-in sentence; no accent edge |

Fallback principle: **serif carries authority, warm gray carries rhythm, celadon carries focus, terracotta carries cost, numerals carry evidence.** Then add the smallest thing that works.

## 8. Mechanical limits

The validator enforces the bundled CSS, supported static markup/resource vocabulary, paint values, rectangle/edge grid, node sizes, geometric chevrons, budgets and navigation structure. It cannot establish semantic node roles, actual font metrics, the correctness of labels/ranges, edge attachment to the intended node, absence of crossings, or factual accuracy. Inspect those in the final rendering; a clean exit is not a claim that arbitrary HTML is safe.
