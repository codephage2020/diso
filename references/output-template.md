# Authoring diso pages

The generator writes JSON content; `scripts/build.py` owns the shell, CSS, escaping, depth selection and TOC. `assets/base.html` is the single CSS source. The final HTML has no runtime dependencies. Do not paste the stylesheet into the JSON, add `style` attributes, or edit it in the output.

## Input schema

See `examples/btree-index.json` for a complete input that can be built in all three modes. All fields below contain plain text unless named `_html` or `svg`. Plain text is automatically escaped, including titles, table cells, source titles and URLs; HTML-looking text remains visible text.

| Field | Type / use |
|---|---|
| `title`, `essence`, `takeaway` | Required nonempty strings; the essence and takeaway state the mechanism |
| `lang` | Language tag, e.g. `zh-CN` or `en` |
| `mode` | `standard` (default), `kid` or `deep`; CLI `--mode` overrides it |
| `date` | Optional `YYYY-MM-DD`, defaults to the build date; set it for reproducible output |
| `steps` | 4–6 objects: `title`, `label`, `text`; optionally `svg` plus `caption` |
| `mapping` | At least three rows, each an array of three strings: analogy role, real component, note |
| `mechanism_html` | Required in standard/deep: real flow, definitions, actual structures |
| `tradeoffs_html` | Required in standard/deep: gains/costs and a supported counterintuitive insight |
| `misconceptions` | Required in standard/deep: objects with `belief`, `truth`, `reason` |
| `kid_mechanism`, `kid_boundary` | Required in kid: compact real mechanism and one specific analogy limit |
| `deep_title`, `deep_html` | Required in deep: collapsible formal description, assumptions and boundary conditions |
| `cheatsheet_html` | Optional, emitted only in deep; compact tables/code, no new concepts |
| `sources` | Required nonempty array of `title`, `note` (claim supported), optional absolute HTTP(S) `url`; books/papers may omit URL |
| `headings` | Optional `p1`/`p2`/`p3`/`p4` section-title overrides |
| `labels` | Optional UI string overrides; see keys below; complete translations required for languages other than en/zh |

The builder ignores depth-specific content in modes that omit it. A standard page has all five layers and no deep details. Kid keeps the journey, compact mapping/mechanism and a short limit; it omits full trade-offs. All modes retain sources and a takeaway. Source checking remains the author's responsibility; the builder does not browse or execute input.

`labels` keys: `site`, `contents`, `figure`, `p1`, `p2`, `p3`, `p4`, `analogy`, `component`, `note`, `misconception`, `reason`, `sources`, `takeaway`, `cheatsheet`.

## Markup fields

Use the bundled component classes: paragraphs, lists, tables, `.term`, `.alert`, `.card`, `.stats`, `.versus`, `.diff`, `.callout`, `pre` and `code`. Do not include document wrappers, navigation, styles or `details` in a fragment; the builder adds those. Put formal material in `deep_html`. Write escaped examples inside markup fields, e.g. `<pre><code>&lt;script&gt;alert(1)&lt;/script&gt;</code></pre>`; the validator does not scan this displayed text for CSS or JavaScript.

Citation links in body fragments may point to `#sources` or an absolute HTTP(S) URL. Relative images, fonts, stylesheets, embeds and external SVG resources are rejected. Inline raster images, if necessary, need an `alt` and base64 PNG/JPEG/GIF/WebP `src`; SVG data URLs are unsupported. Prefer inline SVG diagrams.

SVG uses explicit six-digit palette colors (case-insensitive), `none`, or `url(#pattern-id)` referencing a pattern in the same SVG. CSS variables, named colors, computed colors, style attributes, transforms, animation, `<use>`, `<marker>` and foreign content are unsupported. Use explicit closing tags in HTML, standard self-closing tags in SVG, unique IDs and the supplied classes. Do not treat the validator as a general-purpose HTML sanitizer.

## Commands

From any working directory, replace `/absolute/path/to/diso` with the installed skill directory:

```bash
python3 /absolute/path/to/diso/scripts/build.py diso-topic.json -o diso-topic.html
python3 /absolute/path/to/diso/scripts/check.py diso-topic.html
```

Any error or warning fails the build before output replacement. Rebuild after fixing the JSON; generated HTML is not the editable source. Exit 2 means an input/usage error (e.g. unreadable file, invalid JSON or missing mode fields).

## String localization map

The author must translate every visible content string and SVG label into the request language. The builder supplies en/zh UI labels. Canonical mappings (anything not listed is translated on the fly in the same register):

| English (reference) | Chinese |
|---|---|
| diso / Plain, Not Shallow (site eyebrow) | 深入浅出 |
| Part 1 · Build the intuition | Part 1 · 先建立直觉 |
| Part 2 · The real mechanism | Part 2 · 拆开看真实机制 |
| Part 3 · Why designed this way | Part 3 · 为什么这样设计 |
| Part 4 · Where the analogy breaks | Part 4 · 这个类比在哪里失效 |
| Fig. 1 · | 图 1 · |
| Role in the analogy / What it really is / Note | 类比里的角色 / 真实系统里是什么 / 说明 |
| One layer deeper: … | 再深一层：… |
| Gained / Cost | 得到 / 代价 |
| Misconception 1 | 误解 1 |
| One-sentence summary (takeaway eyebrow) | 一句话总结 |
| Cheat sheet (`--deep`, optional) | 速查卡 |
| Sources / Contents | 来源 / 目录 |
| TOC labels | short forms of the section names, localized |

The colophon (`YYYY-MM-DD · Generated by diso`) stays identical in every language. Part numbers are sequential for the sections actually rendered. A deep cheat sheet precedes sources and the takeaway; the builder generates its ID and TOC entry.

---

## Ready-made diagram snippets

**Focus node** (solid celadon fill + ink stroke + dark text, 1–2 per diagram):

```html
<rect x="400" y="80" width="160" height="64" rx="4" fill="#78C2C4" stroke="#267072" stroke-width="1.5"/>
<text x="480" y="120" font-size="26" font-weight="500" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">root</text>
```

**Warning node** (solid terracotta fill + terracotta-ink stroke; only where something fails, never alongside a celadon focus in the same figure):

```html
<rect x="400" y="80" width="160" height="64" rx="4" fill="#C47A78" stroke="#8C4644" stroke-width="1.5"/>
<text x="480" y="120" font-size="26" font-weight="500" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">dropped</text>
```

**Standard node**:

```html
<rect x="100" y="216" width="160" height="64" rx="4" fill="#faf9f5" stroke="#141413" stroke-width="1.2"/>
<text x="180" y="256" font-size="26" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">10 | 20</text>
```

**Orthogonal edge + chevron** (main edge celadon ink, secondary warm gray; 4px clearance, ends snapped to node edges):

```html
<!-- main edge (#267072): from (480,148) to (480,212), downward chevron -->
<path d="M480 148 L480 212" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M475 205 L480 212 L485 205" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<!-- secondary edge (#504e49): down → across → down -->
<path d="M480 148 L480 180 L180 180 L180 212" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M175 205 L180 212 L185 205" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Failure path** (terracotta ink, 1.5px, chevron same color; mutually exclusive with a celadon focus path in the same figure):

```html
<path d="M480 148 L480 212" stroke="#8C4644" stroke-width="1.5" fill="none"/>
<path d="M475 205 L480 212 L485 205" fill="none" stroke="#8C4644"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Fan-out bus** (one source to many targets — exit the source sideways, ride a horizontal bus, drop into each target; never draw diagonals):

```html
<!-- source node bottom-center is busy, so exit its left edge at (396,112);
     bus at y=112, then down into each target's top edge -->
<path d="M396 112 L160 112 L160 236" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M155 229 L160 236 L165 229" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M564 112 L800 112 L800 236" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M795 229 L800 236 L805 229" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Mid-line tap** (a listener/observer node hanging off the middle of a channel — drop a vertical stub from the channel's midpoint into the node; never attach the observer to one endpoint):

```html
<!-- channel: A(240,152) → B(716,152); observer node top edge at y=280, center x=480 -->
<path d="M244 152 L716 152" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M709 147 L716 152 L709 157" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M480 156 L480 276" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M475 269 L480 276 L485 269" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Timeline with stubs** (sequence dots on a horizontal line: line first, stubs second, dots last so they sit on top; every node below connects to the line by a stub — no floating nodes, no arrowhead on the timeline):

```html
<path d="M160 120 L800 120" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M160 132 L160 156" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M480 132 L480 156" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M800 132 L800 156" stroke="#504e49" stroke-width="1.5" fill="none"/>
<circle cx="160" cy="120" r="12" fill="#267072"/>
<text x="160" y="125" font-size="16" font-weight="500" fill="#f5f4ed"
      text-anchor="middle" font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">1</text>
```

**Edge-label backing** (on-edge text sits on a canvas-colored pad, 8px padding all around):

```html
<rect x="448" y="164" width="64" height="24" rx="4" fill="#f5f4ed"/>
<text x="480" y="181" font-size="20" fill="#504e49" text-anchor="middle"
      font-family="'JetBrains Mono', Consolas, monospace">RTT</text>
```

**Sequence dot** (execution order, ≤ 6 per figure):

```html
<circle cx="436" cy="148" r="12" fill="#267072"/>
<text x="436" y="153" font-size="16" font-weight="500" fill="#f5f4ed"
      text-anchor="middle" font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">1</text>
```

**Group container** (covers nodes of one subsystem, drawn beneath them, ≤ 2 per figure):

```html
<rect x="64" y="192" width="420" height="180" rx="8" fill="#EDECE3"/>
<text x="88" y="224" font-size="20" fill="#504e49"
      font-family="'JetBrains Mono', Consolas, monospace">storage engine</text>
```

**Note**: `<text>` `y` is the baseline. To vertically center text in a box at `y=80, height=64`, use baseline `y = 80 + 40 = 120`. To highlight a focus path use `stroke="#78C2C4" stroke-width="2.5"` — once per figure. Chevron directions: right is `Mx,y Lx+7,y+5 Lx,y+10`; up and left are mirrors; arms stay 5×7.
