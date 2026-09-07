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
3. **Never avoid real terminology** — define on first use, then keep using the real term. One concept gets exactly one name across the whole page: never alternate between the analogy name and the real name for the same thing.
4. **Never trust parametric memory for facts.** Every number, date, version, standard clause, or named source must be verified (search / read the source) before it lands on the page; what cannot be verified is dropped or explicitly marked as approximate. One invented "oh, I see" figure destroys the page's credibility.

Tone: adult to adult. The reader is smart, just lacks background. Banned: baby talk, mascots, coaxing exclamations, emoji as punctuation. **What drops is the barrier to entry, not the information density.**

## 2. Depth modes

| Flag | Mode | Layers |
|---|---|---|
| `--kid` | intuition only | 1–2 |
| (default) | standard | 1–4 |
| `--deep` | deep dive | 1–5 + formal description (formula / pseudocode / data structure), order-of-magnitude estimates, boundary conditions; may close with a **cheat sheet** |

## 3. Five-layer skeleton

**Layer 1 — one-sentence essence**: holds with zero background, ≤ 30 characters (Chinese) / ≤ 20 words (English), states the working mechanism, no metaphor.

**Layer 2 — intuition journey (4–6 steps)**: one analogy carried start to finish, telling "how people managed before it existed → what happened, step by step". Each step gets a large SVG + 1–2 sentences. The analogy must be able to carry bottleneck / failure / trade-off; if it can't, pick another.

**Layer 3 — the real mechanism**: first an analogy→component mapping table, then the real flow with real terms and structures. Target: the reader can retell "what goes in → what happens inside → what comes out".

**Layer 4 — why designed this way**: a trade-off table (gained / cost) plus at least one "oh, I see" moment: a counterintuitive fact, an order-of-magnitude gap, or a deliberate sacrifice. When the story is an evolution (old design → new design), show it as a diff block — before/after with `+` / `-` lines — instead of versus cards.

**Layer 5 — where the analogy breaks & misconceptions** (skip in `--kid`): ~3 items, each: the misconception → the truth → why people think this way.

**Smallest-view test**: every block earns its size. If a sentence or a small table makes the point, do not inflate it into a stats row, a versus pair, or a full-width SVG.

**Ending — one-sentence summary**: repeatable verbatim, contains the mechanism, not the metaphor. In Chinese pages the takeaway block's eyebrow reads 「一句话总结」.

**Cheat sheet** (`--deep` only, optional): a compact final section for later reference — the term mapping and the formal description, restated tightly using tables and code blocks. No new prose, no new diagrams; it is the page's distillate.

## 4. HTML output

Read `references/design-tokens.md` before every generation; build the page on `references/output-template.md`. The reference files are written in English; **every visible string in the produced HTML must be localized to the request language** using the string map at the bottom of `output-template.md`.

Produce **one self-contained HTML file**: inline SVG, no external links, no CDN, no JS, no build step, opens on double-click. The page must read as typeset paper, not a dashboard.

The visual system in one breath: parchment `#f5f4ed` canvas, never pure white; two accent hues with divided semantics — celadon owns focus and the positive, terracotta owns cost and failure; one serif family at weights 400/500; flat surfaces, elevation by fill; a line must separate regions, encode state, or carry a data relationship, otherwise delete it. Full palette, components, and SVG rules live in `references/design-tokens.md` — follow it exactly.

## 5. Quality checklist (verify after generation; fix anything failing)

Content:

- [ ] Reader can state the mechanism, not just "it's like a X"; substance > 50% after deleting all analogies
- [ ] Every number, date, and named source verified; unverifiable claims dropped or marked approximate
- [ ] One concept = one name throughout the page; analogy failure points written; tone is colleague-to-colleague
- [ ] At least one "oh, I see" moment, rendered as a `.stats` card when it involves magnitude
- [ ] Smallest-view test passed: no block is bigger than its point requires; evolutions shown as diff blocks where applicable

Visual (full rules in `design-tokens.md`):

- [ ] Intuition steps use the `01` serif numeral + mono tag header; numerals used nowhere else on the page
- [ ] Background `#f5f4ed`; grays warm; no hue besides celadon (focus/positive) and terracotta (cost/failure); combined solid accent fills ≤ 5%
- [ ] No text or thin lines in `#78C2C4` / `#C47A78` (ink depths `#267072` / `#8C4644` on light surfaces); misconception callouts use the rose tint
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
