---
name: diso
description: Explain any topic in plain language without dumbing it down — a visual intuition layer plus a real mechanism layer, delivered as a self-contained HTML page. Use when the user types /diso <topic> or asks for an explainer that is simple but not shallow.
---

# diso — plain, not shallow

Explain like I'm an intelligent adult with zero background in this topic.

Topic: $ARGUMENTS

## 1. Core stance: the analogy is the entrance, not the destination

> Delete every analogy from the finished piece. The real mechanism that remains must still stand on its own.

1. **Every analogy ships with a mapping** — a table mapping each analogy role to the real component it stands for.
2. **Every analogy ships with its failure points** — state where it stops holding.
3. **Never avoid real terminology** — define on first use, then keep using the real term.

Tone: adult to adult. The reader is smart, just lacks background. Banned: baby talk, mascots, coaxing exclamations, emoji as punctuation. **What drops is the barrier to entry, not the information density.**

## 2. Depth modes

| Flag | Mode | Layers |
|---|---|---|
| `--kid` | intuition only | 1–2 |
| (default) | standard | 1–4 |
| `--deep` | deep dive | 1–5 + formal description (formula / pseudocode / data structure), order-of-magnitude estimates, boundary conditions |

## 3. Five-layer skeleton

**Layer 1 — one-sentence essence**: holds with zero background, ≤ 30 characters (Chinese) / ≤ 20 words (English), states the working mechanism, no metaphor.

**Layer 2 — intuition journey (4–6 steps)**: one analogy carried start to finish, telling "how people managed before it existed → what happened, step by step". Each step gets a large SVG + 1–2 sentences. The analogy must be able to carry bottleneck / failure / trade-off; if it can't, pick another.

**Layer 3 — the real mechanism**: first an analogy→component mapping table, then the real flow with real terms and structures. Target: the reader can retell "what goes in → what happens inside → what comes out".

**Layer 4 — why designed this way**: a trade-off table (gained / cost) plus at least one "oh, I see" moment: a counterintuitive fact, an order-of-magnitude gap, or a deliberate sacrifice.

**Layer 5 — where the analogy breaks & misconceptions** (skip in `--kid`): ~3 items, each: the misconception → the truth → why people think this way.

**Ending — one-sentence summary**: repeatable verbatim, contains the mechanism, not the metaphor. In Chinese pages the takeaway block's eyebrow reads 「一句话总结」.

## 4. HTML output

Read `references/design-tokens.md` before every generation; build the page on `references/output-template.md`. The reference files are written in English; **every visible string in the produced HTML must be localized to the request language** using the string map at the bottom of `output-template.md`.

Produce **one self-contained HTML file**: inline SVG, no external links, no CDN, no JS, no build step, opens on double-click. The page must read as typeset paper, not a dashboard.

Five non-negotiables:

1. **Parchment `#f5f4ed` canvas, never pure white.** All grays warm (R ≈ G > B); cold grays banned.
2. **Two accent hues with semantic division: celadon and terracotta.** Celadon `#78C2C4` owns focus, structure, and the positive; terracotta `#C47A78` owns warning, cost, and failure — never swap their meanings. Each hue has a wash (fills only) and an ink depth for text and thin lines: `#267072` (≈5.2:1) and `#8C4644` (≈6.2:1); the washes alone (≈1.9:1 / ≈3.0:1) are illegible as text. Combined solid accent fills ≤ 5% of page area.
3. **One serif family, weights 400/500 only.** `strong` locked to 500, no synthetic bold.
4. **Flat surfaces.** Elevation comes from ivory `#faf9f5` fill, never borders or shadows.
5. **Subtraction principle.** A line must separate regions, encode state, or carry a data relationship; otherwise delete it.

Signature components: intuition steps open with a large serif numeral (`01`, celadon ink) + mono tag; order-of-magnitude "oh, I see" facts go into `.stats` big-number cards, not buried in prose; paired gained/cost trade-offs use `.versus` twin cards; the page ends with the dark takeaway block followed by a one-line `.colophon`. Print stylesheet included; details blocks expand when printed.

## 5. Quality checklist (verify after generation; fix anything failing)

- [ ] Reader can state the mechanism, not just "it's like a X"; substance > 50% after deleting all analogies
- [ ] At least one "oh, I see" moment, rendered as a `.stats` card when it involves magnitude; analogy failure points written; tone is colleague-to-colleague
- [ ] Intuition steps use the `01` serif numeral + mono tag header; numerals used nowhere else on the page
- [ ] Background `#f5f4ed`; grays warm; no hue besides celadon (focus/positive) and terracotta (cost/failure); combined solid accent fills ≤ 5%
- [ ] No text or thin lines in `#78C2C4` / `#C47A78` (must be `#267072` / `#8C4644` on light surfaces); misconception callouts use the rose tint, not the celadon one
- [ ] No `box-shadow`, gradients, `rgba()`, radii > 10px, italics, weight > 500
- [ ] SVG coordinates divisible by 4; focus nodes 1–2 per diagram; arrows are hand-drawn chevrons, not `<marker>`; text baseline `y ≥ font-size × 1.2`; on-line labels sit on a `#f5f4ed` backing rect
- [ ] **Edges are 0°/90° only (no diagonals)**; every edge endpoint lands on a node-edge midpoint, a bus, or a timeline — no dangling arrows, no corner attachments; timeline dots drawn above the line with stubs connecting every node below
- [ ] Ends with dark takeaway block + one-line `.colophon`; print styles present
- [ ] Right-edge line TOC present (pure CSS, hover reveals label, anchors wired to section ids, hidden ≤ 1240px, no scroll-spy script)
- [ ] No external links, no `<script>`, no external fonts — verify:

```
grep -nE 'https?://|box-shadow|rgba\(|font-style:\s*italic|<script' <file>
```

The only allowed hit is the SVG namespace `http://www.w3.org/2000/svg`.

## 6. Workflow

- `$ARGUMENTS` is the topic, optionally with `--kid` / `--deep`; no topic → ask first, never generate from nothing.
- Write `diso-<topic-slug>.html` into the current workspace.
- Language matches the request: Chinese in, Chinese out; English likewise.
- Unsure of depth → standard mode, end with "tell me if you want it deeper or simpler".

## Reference files

| File | When to read |
|---|---|
| `references/design-tokens.md` | **Before every generation**. Palette, fonts, components, SVG rules and bans |
| `references/output-template.md` | At generation time. HTML skeleton + ready-made diagram snippets |