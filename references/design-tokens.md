# Design Tokens (diso · Celadon Edition)

One line: **a parchment canvas, two accent hues with divided semantics (celadon & terracotta, each in two densities), serif for hierarchy, numerals for rhythm — no cold grays, no hard shadows.**
This is not a UI framework; it is a constraint system for print. The page must read as a typeset sheet of paper, not a dashboard.

> Language: this document is written in English for the generator. All visible copy in the produced HTML must match the user's request language (see the string map in `output-template.md`).

---

## 1. Eleven invariants (think about the cost before overriding any)

1. Page background is parchment `#f5f4ed` — **never pure white**
2. Two accent hues with **semantic division**: **celadon** `#78C2C4` owns focus, structure, and the positive (gains, paths, navigation); **terracotta** `#C47A78` owns warning, cost, and failure. They are complementary hues — never swap their semantics ("gained" is never red, "cost" is never celadon). Each hue ships in a wash (fills only) and an ink (text and thin lines). **No third hue**
3. Combined solid accent fills ≤ **5%** of page area (celadon + terracotta share this budget); text and thin lines don't count. Beyond that it's decoration, not restraint
4. All grays are warm (yellow-brown base); no cold blue-grays
5. One serif family carries both headings and body
6. Serif weights locked to **400 / 500** — no bold (900/100 banned, `strong` locked to 500)
7. Line heights: headings 1.10–1.30, reading text 1.50–1.55, CJK screen body 1.55–1.65
8. Chinese body `letter-spacing: 0.3px`; English body 0; only short labels and overlines get tracking
9. Label backgrounds must be **plain hex** — never `rgba()`
10. Surfaces are flat by default; whisper shadow is reserved for genuinely floating screenshots/overlays
11. **No italics** (`font-style: italic`)

**Why two densities**: `#78C2C4` measures ≈1.9:1 and `#C47A78` ≈3.0:1 on parchment — both illegible as body text or 1.5px rules; `#267072` ≈5.2:1 and `#8C4644` ≈6.2:1 safely carry text and lines. This is the print division of labor — "wash lays the surface, ink draws the line" — and both hues obey the same density discipline.

---

## 2. Palette (complete)

```css
:root{
  /* Brand: celadon, one hue two densities — focus, structure, positive */
  --brand:        #78C2C4;   /* celadon wash — focus fills, tints, accents on dark */
  --brand-ink:    #267072;   /* celadon ink — text emphasis, hairlines, small glyphs (≈5.2:1) */
  --brand-light:  #9AD8DA;   /* label & keyword variant on dark surfaces */

  /* Accent: terracotta, one hue two densities — warning, cost, failure */
  --accent:       #C47A78;   /* terracotta wash — warning fills, failure paths (≈3.0:1, never text) */
  --accent-ink:   #8C4644;   /* terracotta ink — cost/misconception labels, risk emphasis (≈6.2:1) */
  --accent-light: #D89D9B;   /* warning-word variant on dark (≈6.2:1 on #1B2E2E) */

  /* Surfaces */
  --parchment:      #f5f4ed;   /* page background — warm cream, the emotional base */
  --ivory:          #faf9f5;   /* quiet filled container, one step lighter than parchment */
  --inline-code-bg: #f0eee6;   /* inline code, one step darker than parchment */
  --warm-sand:      #e8e6dc;   /* default button face */
  --dark-surface:   #30302e;   /* dark container, warm charcoal */
  --deep-dark:      #1B2E2E;   /* closing dark block: near-black celadon density (only cool-leaning surface allowed) */

  /* Four text levels — there is no fifth */
  --near-black:     #141413;   /* primary text */
  --dark-warm:      #3d3d3a;   /* secondary, table headers */
  --olive:          #504e49;   /* captions, notes */
  --stone:          #6b6a64;   /* dates, metadata */

  /* Strokes */
  --border:         #e8e6dc;
  --border-soft:    #e5e3d8;

  /* Premixed solid celadon/terracotta tones (replace rgba) */
  --tag-bg:         #DDEFEF;   /* chip label background */
  --brand-tint:     #E9F4F4;   /* faintest celadon wash */
  --selection-bg:   #CDE9E9;   /* text selection */
  --accent-tint:    #F4E8E7;   /* faintest terracotta wash: misconception callout background */
}
```

**Banned**: `#ffffff` as page background; `#f8f9fa` / `#f3f4f6` and every other cold gray surface; any color outside the celadon and terracotta families.
**Warm-gray test**: in `rgb()`, R ≈ G > B (or R > G > B with small deltas). A cold gray is R < G < B or R = G = B.

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

```css
/* Latin-first Chinese serif stack (robust fallback when no external font files) */
--serif: Charter, "Bitstream Charter", Georgia,
         "TsangerJinKai02", "Source Han Serif SC", "Noto Serif SC",
         "Source Han Serif CN", "Noto Serif CJK SC", "思源宋体",
         "Songti SC", "STSong", SimSun, "宋体", serif;
--sans:  var(--serif);          /* one family per page */
--mono:  "JetBrains Mono", "SF Mono", "Cascadia Code", "Fira Code",
         Consolas, Monaco, "Courier New",
         "TsangerJinKai02", "Noto Serif SC", Georgia, serif;   /* mono must carry a CJK fallback */
```

The preferred Chinese serif is TsangerJinKai02, but it requires a local font file; a self-contained HTML cannot link external fonts, so we rely on this fallback chain. **Latin families come first** so mixed CJK/Latin text shares a baseline. Families are written under both their English and localized names (`"Source Han Serif SC"` / `"思源宋体"`, `SimSun` / `"宋体"`): Windows often registers fonts under localized names, and dual naming hits more often. The mono stack includes `"Cascadia Code"` (ships with Windows 11), and its CJK fallback lands on serif so Chinese inside code blocks never jumps to a gothic.

**Body typesetting trio** (declared on body; unsupported browsers ignore them, zero cost):
```css
font-kerning: normal;                  /* use the font's built-in kerning (evens out mixed Latin) */
text-rendering: optimizeLegibility;    /* finer glyph rendering and ligatures */
hanging-punctuation: first allow-end;  /* CJK punctuation overhang: opening quotes lead out, closing punctuation hangs — cleaner justified edges */
```

**Weights**: body 400, headings 500. `strong { font-weight: 500 }` is locked to prevent browsers from synthesizing 700.

**Figures**: stats and numerals always use `font-variant-numeric: lining-nums tabular-nums` for vertical alignment.

**Screen size scale** (px):

| Role | Size | Weight | Line height |
|---|---|---|---|
| H1 / hero title | 48px | 500 | 1.18 |
| Stat figure | 34px | 500 | 1.10 |
| H2 section title | 30px | 500 | 1.25 |
| Step numeral | 30px | 400 | 1.00 |
| H3 step title | 21px | 500 | 1.30 |
| Lede / essence | 20–22px | 400 | 1.60 |
| Reading body | 18px | 400 | 1.65 |
| Caption / note | 15px | 400 | 1.50 |
| Overline label | 12px | 500 | 1.35 |

Scale discipline: **land on the rungs, never between them**. Body floor is 14px — nothing smaller.

**CJK justification**: body paragraphs use `text-align: justify; text-justify: inter-ideograph;` — flush right edges, closer to a printed book. English pages revert to `text-align: start`.

---

## 4. Components

### Cards
```css
.card{ background:var(--ivory); border-radius:8px; padding:22px 26px; }
```
Elevation is carried by **fill**, not strokes. **No closed hairline borders** (a sub-1px closed border plus radius renders as a double ring). When more weight is needed, strengthen the label or the first sentence — never add a four-sided accent line.

### Step numerals
Each intuition-journey step opens with a two-line header — large serif numeral + mono tag:
```css
.step-head{display:flex;align-items:baseline;gap:16px;margin:0 0 10px;}
.step-num{font-size:30px;font-weight:400;line-height:1;color:var(--brand-ink);
          font-variant-numeric:lining-nums tabular-nums;}
.step-label{font-family:var(--mono);font-size:12px;font-weight:500;
            letter-spacing:2px;color:var(--brand-ink);}
```
Numerals are zero-padded (`01 02 03`). They are the page's only large decorative element, so they appear **only in the intuition journey** — nowhere else. Scarcity is the point.

### Stats (big-number cards)
Order-of-magnitude "oh, I see" facts become big-number cards instead of buried clauses:
```css
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
       gap:16px;margin:28px 0;}
.stat{background:var(--ivory);border-radius:8px;padding:20px 24px;}
.stat b{display:block;font-size:34px;font-weight:500;line-height:1.1;
        color:var(--brand-ink);font-variant-numeric:lining-nums tabular-nums;}
.stat span{display:block;font-size:14px;line-height:1.50;color:var(--olive);margin-top:8px;}
```
2–4 per row; each = one big number + one note of ≤15 characters (CJK) / ≤8 words (English). Units go inside `<b>` (e.g. `5ms`); the note states the comparison baseline.

### Versus (paired trade-off cards)
When "gained vs cost" appears as a pair, twin cards beat a table:
```css
.versus{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:24px 0;}
.vs-card{background:var(--ivory);border-radius:8px;padding:22px 26px;}
.vs-label{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:2px;
          text-transform:uppercase;display:block;margin-bottom:10px;}
.vs-card.gain .vs-label{color:var(--brand-ink);}
.vs-card.cost .vs-label{color:var(--accent-ink);}
.vs-card p{margin:0;font-size:17px;line-height:1.60;color:var(--dark-warm);}
```
"Gained" takes a celadon-ink label, "cost" a terracotta-ink label — **distinguished by text color, not fill**, so the area budget holds. This is also the most visible application of the two-hue semantic division. Trade-offs with more than two columns still use a table.

### Misconception callout
```css
.callout{ background:var(--accent-tint); border-radius:8px; padding:22px 26px; }
.callout-label{ color:var(--accent-ink); }
```
The faint terracotta wash is the exclusive surface for "where the analogy breaks": a complementary signal to the celadon focus in the body — a reader who spots a red block knows "this is where the analogy fails". The celadon wash (`--brand-tint`) is reserved for neutral/positive asides. The two colored surfaces each do their own job — **never tint an ordinary note red**.

### Blockquote
```css
blockquote{margin:28px 0;padding:0;font-size:20px;line-height:1.60;
           color:var(--dark-warm);}
blockquote strong{color:var(--brand-ink);font-weight:500;}
```
For the one sentence worth quoting verbatim. **No side bar** — size and gray level set it apart from body text.

### Tables
```css
table{ width:100%; border-collapse:collapse; font-size:17px; margin:16px 0; }
th{ text-align:left; font-weight:500; color:var(--dark-warm);
    padding:9px 12px; border-bottom:0.6px solid var(--border); }
td{ padding:8px 12px; border-bottom:0.25px solid var(--border); vertical-align:top; }
tr.total td{ font-weight:500; border-top:0.6px solid var(--border); border-bottom:none; }
```
Rows separate **by whitespace first, line weight second**. No vertical rules, no boxed frame, no tinted header, no zebra striping (only add a `var(--ivory)` even-row fill when there are ≥ 8 rows and tracking is genuinely hard). Numeric columns take `.num` (tabular-nums + celadon ink).

### Code
```css
pre{ background:var(--ivory); border-radius:8px; padding:14px 18px;
     font-family:var(--mono); font-size:15px; line-height:1.55; overflow-x:auto; }
code{ font-family:var(--mono); background:var(--inline-code-bg);
      color:var(--dark-warm); padding:1px 4px; border-radius:3px; font-size:0.9em; }
```

### Diff blocks (before → after)
When the point is "what changed" and the surrounding shape already exists, a diff beats redrawing the whole:
```css
.diff{ background:var(--ivory); border-radius:8px; padding:14px 18px; margin:20px 0;
       font-family:var(--mono); font-size:15px; line-height:1.60; overflow-x:auto; }
.diff .hunk{ color:var(--stone); }        /* context header, e.g. @@ or section name */
.diff .ctx{ color:var(--dark-warm); }     /* unchanged context */
.diff .add{ color:var(--brand-ink); }     /* + gained — celadon */
.diff .del{ color:var(--accent-ink); }    /* − given up — terracotta */
```
- `+` / `-` prefixes are written literally as text, so the block stays copyable
- Semantics follow the two-hue division: addition = celadon ink, removal = terracotta ink. **No per-line background tints** — color carries meaning through text alone, keeping the area budget intact
- A diff shows the change, not the file: keep context lines to the minimum that orients the reader
- The block is shaped text, not only code — file-tree, call-tree, control-flow, and pseudocode diffs are all valid; match the diff's shape to the topic

### Tags / term highlights
- Chip label: `background:var(--tag-bg); color:var(--brand-ink); font-weight:500; padding:1px 6px; border-radius:4px; font-size:12px;`
- **Inline term**: `color:var(--brand-ink); font-weight:500`, **no background block** (stacked color chips in prose blow the area budget)
- **Inline warning** (`.alert`): `color:var(--accent-ink); font-weight:500`, for same-sentence emphasis of cost/risk/boundary phrases. Same spec as `.term`, different semantics; at most one red per sentence, never two reds in one paragraph

### Text selection
```css
::selection{ background:var(--selection-bg); color:var(--near-black); }
```
The only permitted "non-structural color block", because it encodes state (selected), not decoration.

### Lists
Native markers in brand color: `ul li::marker{ color:var(--brand-ink) }`. **Never fake dashes with `::before`** — that's default AI output, not editorial typesetting.

### Colophon
```css
.colophon{margin:72px 0 0;font-family:var(--mono);font-size:12px;
          letter-spacing:1px;color:var(--stone);}
```
Placed after the takeaway: generation date + "Generated by diso". One line, no links.

### Right-edge line TOC
```css
.toc{position:fixed;right:28px;top:50%;transform:translateY(-50%);
     display:flex;flex-direction:column;gap:16px;z-index:10;}
.toc a{display:flex;align-items:center;justify-content:flex-end;text-decoration:none;}
.toc a span{font-family:var(--mono);font-size:12px;letter-spacing:1px;
            color:var(--brand-ink);margin-right:12px;
            opacity:0;transform:translateX(6px);
            transition:opacity .18s ease,transform .18s ease;}
.toc a::after{content:"";display:block;width:22px;height:2px;border-radius:1px;
              background:var(--stone);opacity:.45;
              transition:width .18s ease,background .18s ease,opacity .18s ease;}
.toc a:hover span,.toc a:focus-visible span{opacity:1;transform:none;}
.toc a:hover::after,.toc a:focus-visible::after{width:36px;background:var(--brand-ink);opacity:1;}
```
One 22px warm-gray dash per section; on hover/keyboard focus the dash extends to 36px in celadon ink while the section name slides in from the left. Clicking uses native anchors (`scroll-behavior:smooth`).
- Hidden entirely at viewport ≤ 1240px (`.toc{display:none}`) — never compete with the column
- Every section and the takeaway need an `id`, plus `scroll-margin-top:32px` so jumps don't glue to the top
- **The cost of zero JS**: no scroll-spy active highlight, hover state only. That is the explicit price of "no scripts" — do not sneak in a `<script>` to fix it
- The dashes carry navigational meaning, so they don't violate the subtraction principle; but every anchor must resolve to a real section — orphan links banned

### Accessible focus
The page's interactive elements are `<summary>` and the TOC anchors:
```css
summary:focus-visible{outline:2px solid var(--brand-ink);outline-offset:2px;border-radius:4px;}
```

### Print styles
```css
@media print{
  body{background:#f5f4ed;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  .wrap{max-width:100%;padding:0;}
  .takeaway{break-inside:avoid;}
  figure,.stat,.vs-card,.callout,.diff{break-inside:avoid;}
}
```
Print keeps the parchment background (needs `print-color-adjust:exact`); figures and cards never break across pages.

### The subtraction principle (critical)
A line earns its existence only when it **separates regions, encodes state, or carries a data relationship**.
**Banned**: decorative eyebrow bars, vertical rules beside headings, quote side bars, callout accent edges, cover flourishes (the short celadon segment on the hero rule is the single exception).
Test: hide the line — if meaning, state, grouping, and navigation are all unchanged, delete it and buy the pause back with spacing.

---

## 5. SVG diagram rules

### Canvas
- Background must be `#f5f4ed` — **never pure white**
- **All layout coordinates, widths, heights, and gaps must be divisible by 4**
- `viewBox` width is always `960`; height follows content
- Text baseline `y ≥ font-size × 1.2` (otherwise the top clips)
- Dot texture: pattern 24×24, `circle r="0.8"` fill `#D4E7E7`, layer `opacity="0.55"` — a faint celadon lean so every diagram shares the page's color temperature

### Nodes
| Role | Fill | Stroke | Text |
|---|---|---|---|
| Standard node | `#faf9f5` | `#141413` | `#141413` |
| Storage node | `#EAE9E2` | `#504e49` | `#141413` |
| External node | `#E9E8E1` | `#6b6a64` | `#141413` |
| **Focus node** | `#78C2C4` (solid) | `#267072` (1.5px) | `#141413`, `font-weight 500` |
| **Warning node** | `#C47A78` (solid) | `#8C4644` (1.5px) | `#141413`, `font-weight 500` |

The focus node is the page's heaviest stroke of celadon: **solid celadon fill + ink stroke + dark text**, 1–2 per diagram at most. White text banned (2:1 on celadon).
Warning nodes use the same spec in the terracotta family: only for "this fails / this gets eliminated / this pays the price". **One accent hue per diagram** — a focus diagram is all celadon, a warning diagram all terracotta; never mix red and celadon in one figure.
Node widths come in three sizes only: `128 / 144 / 160`; heights in two: `32 / 64` (pill / standard). Never per-node custom widths within one diagram.

### Group containers
When several nodes belong to one subsystem, cover them with a large rounded rect, **fill `#EDECE3`, no stroke**, with a small mono group name (`#504e49`) at the top-left. Draw containers before nodes (bottom layer). At most 2 group containers per diagram; a single group gets none.

### Edges
- **Orthogonal lines only — 0° or 90°, diagonals explicitly banned.** No curves, no crossing modules, no text overruns, no decorative joints. If a line needs to change direction, it turns at a right angle (see the routing patterns in `output-template.md`)
- **Every edge attaches**: both endpoints land on a node edge (at its midpoint), on a bus, or on a timeline. Dangling arrows pointing into empty space are banned; so are lines ending at node corners
- Main edges `#267072` (celadon ink), secondary edges `#504e49`
- The diagram's single **focus path** may use `#78C2C4` thickened to `stroke-width 2.5`; a **failure/rollback path** uses `#8C4644` (terracotta ink, 1.5px, matching chevron). Pick one per diagram — never both
- **4px clearance**: an edge starts 4px off the source edge, the arrowhead lands 4px off the target edge, snapped exactly to node boundaries
- **Never run an edge along a module's top edge** (reads as a broken frame)
- Focus means **1–2 nodes**, not painting every "important" node celadon; warning nodes likewise at most 1
- **Timeline rule**: when sequence dots sit on a horizontal line, draw the line and the vertical stubs first, dots on top, and give every node below a stub connecting it to the line — no floating nodes under a timeline

### Edge-label backing
On-edge text labels (e.g. `RTT`, `ACK`) must sit on a backing rect so they don't fight the dot texture:
```html
<rect x="448" y="164" width="64" height="24" rx="4" fill="#f5f4ed"/>
<text x="480" y="181" font-size="20" fill="#504e49" text-anchor="middle"
      font-family="'JetBrains Mono', Consolas, monospace">RTT</text>
```
The backing uses the canvas color `#f5f4ed` (not ivory), 4px radius, 8px of padding around the text on all sides.

### Arrowheads: hand-drawn chevrons, never `<marker>`, colored like their edge
```html
<!-- main edge (celadon ink 1.5px), downward chevron -->
<path d="M475 206 L480 213 L485 206" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<!-- secondary edge (warm gray 1.5px), downward chevron -->
<path d="M175 206 L180 213 L185 206" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```
Open two-stroke marks read as "editorial diagram", not technical UI. `<marker orient="auto">` doesn't rotate under WeasyPrint — banned.
Other directions: down is `Mx,y Lx+5,y+7 Lx+10,y`; right is `Mx,y Lx+7,y+5 Lx,y+10`; up and left are mirrors. Arms stay 5×7, line caps and joins always round.

### Sequence dots
To show execution order (① then ②), place numbered dots beside nodes or edges:
```html
<circle cx="436" cy="148" r="12" fill="#267072"/>
<text x="436" y="153" font-size="16" font-weight="500" fill="#f5f4ed"
      text-anchor="middle" font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">1</text>
```
Celadon-ink solid circle + parchment numeral (contrast ≈4.9:1). At most 6 sequence dots per diagram; beyond that, split the figure.

### SVG text
| Role | Color |
|---|---|
| Primary | `#141413` |
| Secondary | `#504e49` |
| Tertiary / small mono labels | `#6b6a64` |
| Text inside focus/warning nodes | `#141413` |
| Numerals inside sequence dots | `#f5f4ed` |

**Never use `#78C2C4` / `#C47A78` as SVG text or thin strokes** — both washes are illegible on parchment (≈1.9:1 / ≈3.0:1); text and lines always use their ink densities.
The `font-family` attribute of SVG `<text>` must match the page chain; if the full chain won't fit, write at least `Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif` so CJK falls back to a serif instead of the browser's default gothic.
Scale-compensate font sizes: rendered width ÷ viewBox width ≈ 0.74, so to render 18px you write `font-size="24"`.
→ **Node primary text 26, secondary text 24, small mono labels 20, sequence-dot numerals 16.**

### SVG bans
- `fill` / `stroke` must never use `rgba()`
- No gradients, no `box-shadow`, no 3D, no glassmorphism
- No emoji faces, mascots, or anthropomorphic characters
- No imported icon fonts, no SVG sprites
- Radius ≤ 10px
- Legends never float over the drawing area; text on arrows needs a backing rect

---

## 6. Light/dark alternation

Long pieces may alternate **at the block level** between parchment `#f5f4ed` and near-black celadon `#1B2E2E`. It is the strongest contrast device (diso's closing block uses it).
Text on dark: body in parchment, labels and keywords in `--brand-light`, warning words in `--accent-light` (≈6.2:1). `box-shadow: 0 2px 8px rgba(0,0,0,0.3)` and its kin are banned.
**At most one** dark block per page (the takeaway); Part sections stay parchment so the closing black remains the only accent of weight.

---

## 7. Quick decision table

| Need | Use |
|---|---|
| Display heading | Serif 500, size by level, line height 1.10–1.30 |
| Emphasize a figure / term | `color:var(--brand-ink)`, `font-weight:500`, no background block |
| Emphasize cost / risk / failure inline | `.alert` (`--accent-ink`, 500), at most one per sentence |
| An order-of-magnitude "oh" moment | stats cards (big number + small note), 2–4 per row |
| Step guidance in the intuition journey | Large serif numeral `01` + mono tag (this section only) |
| Paired gained-vs-cost trade-off | versus twin cards (gain = celadon / cost = terracotta); more than two items → table |
| An evolution: old design → new design | diff block (add = celadon ink, remove = terracotta ink); match the diff's shape to the topic |
| Lift a block above body text | ivory fill + 8px radius, no accent edge |
| A sentence worth quoting verbatim | blockquote (one size up, no side bar) |
| Where the analogy breaks / misconceptions | terracotta-wash callout + terracotta-ink label |
| Key node in a diagram | `#78C2C4` solid + `#267072` stroke, 1–2 per page |
| A node that fails / gets eliminated | `#C47A78` solid + `#8C4644` stroke, ≤ 1 per diagram, never alongside a celadon focus |
| Execution order in a diagram | celadon-ink sequence dots, ≤ 6 per figure |
| Subsystem grouping in a diagram | `#EDECE3` unstroked large-radius cover, ≤ 2 per figure |
| Showing code | ivory fill, no border |
| Opening a section | serif scale and margins; overline in celadon ink |
| Marking one item in a list | ivory fill, a stronger label, or a lead-in sentence; no accent edge |

Fallback principle: **serif carries authority, warm gray carries rhythm, celadon carries focus, terracotta carries cost, numerals carry evidence.** Then add the smallest thing that works.
