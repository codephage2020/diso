# diso HTML Output Skeleton

Apply directly, replacing `{{...}}`. Self-contained, no external links, no JS, parchment canvas.
Full tokens and bans live in `design-tokens.md`.

**Language**: the skeleton below uses English reference copy. **All visible strings must be localized into the user's request language at generation time** — use the string map at the bottom of this file. For Chinese pages: `lang="zh-CN"`, keep body `letter-spacing: 0.3px` and `text-align: justify`. For English pages: `lang="en"`, set body `letter-spacing: 0` and `text-align: start`.

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{topic}} · diso</title>
<style>
  :root{
    --brand:#78C2C4; --brand-ink:#267072; --brand-light:#9AD8DA;
    --accent:#C47A78; --accent-ink:#8C4644; --accent-light:#D89D9B; --accent-tint:#F4E8E7;
    --parchment:#f5f4ed; --ivory:#faf9f5; --inline-code-bg:#f0eee6; --warm-sand:#e8e6dc;
    --dark-surface:#30302e; --deep-dark:#1B2E2E;
    --near-black:#141413; --dark-warm:#3d3d3a; --olive:#504e49; --stone:#6b6a64;
    --border:#e8e6dc; --border-soft:#e5e3d8;
    --tag-bg:#DDEFEF; --brand-tint:#E9F4F4; --selection-bg:#CDE9E9;
    --serif: Charter, "Bitstream Charter", Georgia,
             "TsangerJinKai02", "Source Han Serif SC", "Noto Serif SC",
             "Source Han Serif CN", "Noto Serif CJK SC", "思源宋体",
             "Songti SC", "STSong", SimSun, "宋体", serif;
    --sans: var(--serif);
    --mono: "JetBrains Mono", "SF Mono", "Cascadia Code", "Fira Code",
            Consolas, Monaco, "Courier New",
            "TsangerJinKai02", "Noto Serif SC", Georgia, serif;
  }
  *{box-sizing:border-box;}
  html{background:var(--parchment);scroll-behavior:smooth;}
  section.part,.takeaway{scroll-margin-top:32px;} /* breathing room after anchor jumps */
  body{margin:0;background:var(--parchment);color:var(--near-black);
       font-family:var(--serif);font-weight:400;
       font-size:18px;line-height:1.65;letter-spacing:0.3px;
       font-kerning:normal;text-rendering:optimizeLegibility;
       hanging-punctuation:first allow-end;
       font-synthesis:none;-webkit-font-smoothing:antialiased;}
  ::selection{background:var(--selection-bg);color:var(--near-black);}
  .wrap{max-width:760px;margin:0 auto;padding:0 32px 120px;}
  p,li{text-align:justify;text-justify:inter-ideograph;}

  /* ---------- Hero ---------- */
  .hero{padding:112px 0 44px;}
  .eyebrow{font-family:var(--mono);font-size:12px;font-weight:500;
           letter-spacing:2px;text-transform:uppercase;color:var(--stone);}
  h1{font-size:48px;font-weight:500;line-height:1.18;letter-spacing:0.5px;
     margin:20px 0 24px;color:var(--near-black);}
  .essence{font-size:22px;line-height:1.60;font-weight:400;color:var(--dark-warm);
           margin:0;max-width:640px;text-align:justify;}
  .essence strong{color:var(--brand-ink);font-weight:500;}
  .rule{position:relative;height:1px;background:var(--border);border:0;margin:44px 0 0;}
  .rule::before{content:"";position:absolute;left:0;top:-1px;width:72px;height:3px;
                background:var(--brand);border-radius:2px;} /* the page's only decoration */

  /* ---------- Sections ---------- */
  section.part{margin-top:96px;}
  .part-eyebrow{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:2px;
                text-transform:uppercase;color:var(--brand-ink);margin-bottom:16px;}
  h2{font-size:30px;font-weight:500;line-height:1.25;letter-spacing:0.3px;
     margin:0 0 24px;color:var(--near-black);}
  .lede{font-size:20px;line-height:1.60;color:var(--olive);margin:0 0 44px;max-width:620px;}
  h3{font-size:21px;font-weight:500;line-height:1.30;margin:0 0 10px;color:var(--near-black);}
  p{margin:0 0 20px;}
  ul{padding-left:24px;margin:0 0 20px;}
  li{margin:0 0 8px;}
  ul li::marker{color:var(--brand-ink);}

  /* ---------- Intuition steps (large numeral + mono tag) ---------- */
  .step{margin:0 0 72px;}
  .step:last-child{margin-bottom:0;}
  figure{margin:0 0 22px;}
  figure svg{display:block;width:100%;height:auto;border-radius:8px;}
  figcaption{font-size:15px;line-height:1.50;color:var(--olive);margin-top:12px;}
  .fig-label{font-family:var(--mono);font-size:12px;font-weight:500;
             letter-spacing:1px;color:var(--brand-ink);margin-right:8px;}
  .step-head{display:flex;align-items:baseline;gap:16px;margin:0 0 10px;}
  .step-num{font-size:30px;font-weight:400;line-height:1;color:var(--brand-ink);
            font-variant-numeric:lining-nums tabular-nums;}
  .step-label{font-family:var(--mono);font-size:12px;font-weight:500;
              letter-spacing:2px;color:var(--brand-ink);}
  .step-txt{font-size:19px;line-height:1.65;color:var(--near-black);}

  /* ---------- Stats ---------- */
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));
         gap:16px;margin:28px 0;}
  .stat{background:var(--ivory);border-radius:8px;padding:20px 24px;}
  .stat b{display:block;font-size:34px;font-weight:500;line-height:1.1;
          color:var(--brand-ink);font-variant-numeric:lining-nums tabular-nums;}
  .stat span{display:block;font-size:14px;line-height:1.50;color:var(--olive);margin-top:8px;}

  /* ---------- Versus (paired trade-off cards) ---------- */
  .versus{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:24px 0;}
  .vs-card{background:var(--ivory);border-radius:8px;padding:22px 26px;}
  .vs-label{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:2px;
            text-transform:uppercase;display:block;margin-bottom:10px;}
  .vs-card.gain .vs-label{color:var(--brand-ink);}
  .vs-card.cost .vs-label{color:var(--accent-ink);}
  .vs-card p{margin:0;font-size:17px;line-height:1.60;color:var(--dark-warm);}

  /* ---------- Blockquote ---------- */
  blockquote{margin:28px 0;padding:0;font-size:20px;line-height:1.60;color:var(--dark-warm);}
  blockquote strong{color:var(--brand-ink);font-weight:500;}

  /* ---------- Tables ---------- */
  table{width:100%;border-collapse:collapse;font-size:17px;margin:24px 0;}
  th{text-align:left;font-weight:500;color:var(--dark-warm);
     padding:9px 12px;border-bottom:0.6px solid var(--border);}
  td{padding:8px 12px;border-bottom:0.25px solid var(--border);
     vertical-align:top;color:var(--near-black);}
  td:first-child{color:var(--near-black);font-weight:500;white-space:nowrap;}
  tr:last-child td{border-bottom:none;}
  .num{font-variant-numeric:lining-nums tabular-nums;color:var(--brand-ink);font-weight:500;}

  /* ---------- Inline ---------- */
  .term{color:var(--brand-ink);font-weight:500;}      /* no background block */
  .alert{color:var(--accent-ink);font-weight:500;}    /* cost/risk/failure, max one per sentence */
  strong{font-weight:500;}
  code{font-family:var(--mono);background:var(--inline-code-bg);color:var(--dark-warm);
       padding:1px 5px;border-radius:3px;font-size:0.88em;}
  pre{background:var(--ivory);border-radius:8px;padding:16px 20px;margin:20px 0;
      font-family:var(--mono);font-size:15px;line-height:1.55;
      color:var(--near-black);overflow-x:auto;}
  pre code{background:none;padding:0;font-size:inherit;color:inherit;}

  /* ---------- Collapsible deep-dive ---------- */
  details{background:var(--ivory);border-radius:8px;padding:0;margin:24px 0;}
  summary{cursor:pointer;padding:16px 22px;font-size:18px;font-weight:500;
          color:var(--brand-ink);list-style:none;user-select:none;letter-spacing:0.3px;}
  summary::-webkit-details-marker{display:none;}
  summary::before{content:"+ ";font-family:var(--mono);}
  details[open] summary::before{content:"\2212  ";}
  summary:focus-visible{outline:2px solid var(--brand-ink);outline-offset:2px;border-radius:4px;}
  .dbody{padding:0 22px 20px;font-size:17px;line-height:1.60;color:var(--dark-warm);}
  .dbody p:last-child{margin-bottom:0;}

  /* ---------- Misconception callout: terracotta wash, warning semantics ---------- */
  .callout{background:var(--accent-tint);border-radius:8px;padding:22px 26px;margin:0 0 16px;}
  .callout-label{font-family:var(--mono);font-size:12px;font-weight:500;letter-spacing:2px;
                 text-transform:uppercase;color:var(--accent-ink);display:block;margin-bottom:10px;}
  .callout h3{font-size:19px;margin:0 0 8px;}
  .callout p{margin:0;font-size:17px;line-height:1.60;color:var(--dark-warm);}

  /* ---------- Closing: block-level light/dark alternation ---------- */
  .takeaway{margin-top:104px;padding:56px 48px;border-radius:8px;
            background:var(--deep-dark);color:var(--parchment);}
  .takeaway .eyebrow{color:var(--brand-light);}
  .takeaway p{font-size:21px;line-height:1.65;color:var(--parchment);
              margin:16px 0 0;font-weight:400;}
  .takeaway strong{color:var(--brand-light);font-weight:500;}

  /* ---------- Colophon ---------- */
  .colophon{margin:72px 0 0;font-family:var(--mono);font-size:12px;
            letter-spacing:1px;color:var(--stone);}

  /* ---------- Right-edge line TOC: pure CSS, hover reveals the label ---------- */
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
  @media (max-width:1240px){ .toc{display:none;} } /* narrow screens: never fight the column */

  @media (max-width:680px){
    body{font-size:17px;}
    .wrap{padding:0 20px 100px;}
    h1{font-size:32px;}
    h2{font-size:24px;}
    .hero{padding:64px 0 32px;}
    .essence{font-size:19px;}
    .stat b{font-size:28px;}
    .versus{grid-template-columns:1fr;}
    .takeaway{padding:36px 24px;}
    td:first-child{white-space:normal;}
  }
  @media print{
    body{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
    .wrap{max-width:100%;padding:0;}
    figure,.stat,.vs-card,.callout,.takeaway,details{break-inside:avoid;}
    details:not([open]) .dbody{display:block;} /* expand deep-dives when printing */
  }
</style>
</head>
<body>
<nav class="toc" aria-label="Contents">
  <a href="#p1"><span>{{section 1 short name}}</span></a>
  <a href="#p2"><span>{{section 2 short name}}</span></a>
  <a href="#p3"><span>{{section 3 short name}}</span></a>
  <a href="#p4"><span>{{section 4 short name}}</span></a>
  <a href="#takeaway"><span>{{takeaway short name}}</span></a>
</nav>
<div class="wrap">

  <header class="hero">
    <div class="eyebrow">{{site eyebrow}}</div>
    <h1>{{topic}}</h1>
    <p class="essence">{{one-sentence essence: ≤20 words EN / ≤30 chars ZH; states the working mechanism, no metaphor; wrap keywords in <strong>}}</p>
    <div class="rule"></div>
  </header>

  <!-- Layer 2: intuition journey, 4-6 steps -->
  <section class="part" id="p1">
    <div class="part-eyebrow">Part 1 · {{eyebrow: build the intuition}}</div>
    <h2>{{section title}}</h2>
    <p class="lede">{{one-sentence setup of the analogy}}</p>

    <div class="step">
      <figure>
        <svg viewBox="0 0 960 400" xmlns="http://www.w3.org/2000/svg" role="img">
          <title>{{accessible figure title}}</title>
          <desc>{{one-sentence description of the figure}}</desc>
          <defs>
            <pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">
              <circle cx="1" cy="1" r="0.8" fill="#D4E7E7"/>
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="#f5f4ed"/>
          <rect width="100%" height="100%" fill="url(#dots)" opacity="0.55"/>
          <!-- content: every coordinate divisible by 4; at most 1-2 focus nodes -->
        </svg>
        <figcaption><span class="fig-label">{{Fig. 1 ·}}</span>{{caption: add a fact, never restate the prose}}</figcaption>
      </figure>
      <div class="step-head">
        <span class="step-num">01</span>
        <span class="step-label">{{short tag}}</span>
      </div>
      <h3>{{step title}}</h3>
      <p class="step-txt">{{1-2 sentences, adult tone}}</p>
    </div>
    <!-- repeat .step up to 4-6 total; numerals zero-padded 01 02 03… -->
  </section>

  <!-- Layer 3: the real mechanism -->
  <section class="part" id="p2">
    <div class="part-eyebrow">Part 2 · {{eyebrow: the real mechanism}}</div>
    <h2>{{one-sentence summary of the real mechanism}}</h2>

    <p>{{transition: the analogy ends here; below is the mapping to the real system}}</p>
    <table>
      <thead><tr><th>{{header: role in the analogy}}</th><th>{{header: what it really is}}</th><th>{{header: note}}</th></tr></thead>
      <tbody>
        <tr><td>{{A}}</td><td>{{real component}}</td><td>{{one sentence}}</td></tr>
      </tbody>
    </table>

    <p>{{the real flow; highlight terms with <span class="term">term</span> and define them in the same sentence; cost/risk phrases take <span class="alert">…</span>}}</p>

    <details>
      <summary>{{One layer deeper: what exactly}}</summary>
      <div class="dbody">{{pseudocode / formula / data structure / orders of magnitude}}</div>
    </details>
  </section>

  <!-- Layer 4: design trade-offs -->
  <section class="part" id="p3">
    <div class="part-eyebrow">Part 3 · {{eyebrow: why designed this way}}</div>
    <h2>{{the core constraint}}</h2>

    <!-- order-of-magnitude "oh" moment: stats cards, 2-4 -->
    <div class="stats">
      <div class="stat"><b>{{5ms}}</b><span>{{comparison baseline, ≤15 chars ZH / ≤8 words EN}}</span></div>
      <div class="stat"><b>{{100×}}</b><span>{{comparison baseline}}</span></div>
    </div>

    <!-- paired trade-off: versus twin cards; more than two items → table -->
    <div class="versus">
      <div class="vs-card gain">
        <span class="vs-label">{{Gained}}</span>
        <p>{{the capability bought}}</p>
      </div>
      <div class="vs-card cost">
        <span class="vs-label">{{Cost}}</span>
        <p>{{what was given up}}</p>
      </div>
    </div>

    <blockquote>{{a judgment worth quoting verbatim; wrap keywords in <strong>}}</blockquote>
  </section>

  <!-- Layer 5: failure points & misconceptions -->
  <section class="part" id="p4">
    <div class="part-eyebrow">Part 4 · {{eyebrow: where the analogy breaks}}</div>
    <h2>{{overview}}</h2>
    <div class="callout">
      <span class="callout-label">{{Misconception}} {{n}}</span>
      <h3>{{the wrong belief}}</h3>
      <p>{{the actual mechanism}}. {{People believe this because}} {{root cause}}.</p>
    </div>
  </section>

  <!-- Closing -->
  <div class="takeaway" id="takeaway">
    <div class="eyebrow">{{takeaway eyebrow}}</div>
    <p>{{mechanism, not metaphor; repeatable verbatim; wrap keywords in <strong>}}</p>
  </div>

  <div class="colophon">{{YYYY-MM-DD}} · Generated by diso</div>

</div>
</body>
</html>
```

---

## String localization map

The generator must translate every visible string into the request language. Canonical mappings (anything not listed is translated on the fly in the same register):

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
| TOC labels | short forms of the section names, localized |

The colophon (`YYYY-MM-DD · Generated by diso`) and Part numbering stay identical in every language. A `--deep` cheat sheet is a compact final `section.part` (tables + code blocks only, no new prose or diagrams); it gets its own `id` and one extra TOC dash, placed before the takeaway.

---

## Ready-made diagram snippets

**Focus node** (solid celadon fill + ink stroke + dark text, 1–2 per diagram):

```html
<rect x="360" y="80" width="240" height="64" rx="4" fill="#78C2C4" stroke="#267072" stroke-width="1.5"/>
<text x="480" y="120" font-size="26" font-weight="500" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">root</text>
```

**Warning node** (solid terracotta fill + terracotta-ink stroke; only where something fails, never alongside a celadon focus in the same figure):

```html
<rect x="360" y="80" width="240" height="64" rx="4" fill="#C47A78" stroke="#8C4644" stroke-width="1.5"/>
<text x="480" y="120" font-size="26" font-weight="500" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">dropped</text>
```

**Standard node**:

```html
<rect x="80" y="216" width="200" height="64" rx="4" fill="#faf9f5" stroke="#141413" stroke-width="1.2"/>
<text x="180" y="256" font-size="26" fill="#141413" text-anchor="middle"
      font-family="Charter, Georgia, 'Noto Serif SC', 'Songti SC', serif">10 | 20</text>
```

**Orthogonal edge + chevron** (main edge celadon ink, secondary warm gray; 4px clearance, ends snapped to node edges):

```html
<!-- main edge (#267072): from (480,148) to (480,212), downward chevron -->
<path d="M480 148 L480 212" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M475 206 L480 213 L485 206" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<!-- secondary edge (#504e49): down → across → down -->
<path d="M480 148 L480 180 L180 180 L180 212" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M175 206 L180 213 L185 206" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Failure path** (terracotta ink, 1.5px, chevron same color; mutually exclusive with a celadon focus path in the same figure):

```html
<path d="M480 148 L480 212" stroke="#8C4644" stroke-width="1.5" fill="none"/>
<path d="M475 206 L480 213 L485 206" fill="none" stroke="#8C4644"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Fan-out bus** (one source to many targets — exit the source sideways, ride a horizontal bus, drop into each target; never draw diagonals):

```html
<!-- source node bottom-center is busy, so exit its left edge at (396,112);
     bus at y=112, then down into each target's top edge -->
<path d="M396 112 L160 112 L160 236" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M155 230 L160 237 L165 230" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M564 112 L800 112 L800 236" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M795 230 L800 237 L805 230" fill="none" stroke="#504e49"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
```

**Mid-line tap** (a listener/observer node hanging off the middle of a channel — drop a vertical stub from the channel's midpoint into the node; never attach the observer to one endpoint):

```html
<!-- channel: A(240,152) → B(716,152); observer node top edge at y=280, center x=480 -->
<path d="M244 152 L716 152" stroke="#267072" stroke-width="1.5" fill="none"/>
<path d="M710 147 L717 152 L710 157" fill="none" stroke="#267072"
      stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M480 156 L480 276" stroke="#504e49" stroke-width="1.5" fill="none"/>
<path d="M475 270 L480 277 L485 270" fill="none" stroke="#504e49"
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
