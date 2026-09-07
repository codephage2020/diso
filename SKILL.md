---
name: diso
description: Explain any topic plainly without dumbing it down — an intuition layer plus a real-mechanism layer, delivered as one self-contained HTML page with hand-drawn SVG diagrams. Use for /diso <topic>, or when the user wants something explained 深入浅出 / 讲清楚 / 讲透 / 科普, asks for an explainer, a primer, an ELI5 that is still rigorous, or says they want to actually understand how something works rather than get a summary.
---

# diso — plain, not shallow

Explain like I'm an intelligent adult with zero background in this topic.

Topic: $ARGUMENTS — or, if that is empty, whatever the user asked to have explained.

## 1. Core stance: the analogy is the entrance, not the destination

> Delete every analogy from the finished piece. The real mechanism that remains must still stand on its own.

1. **Every analogy ships with a mapping** — a table mapping each analogy role to the real component it stands for.
2. **Every analogy ships with its failure points** — state where it stops holding.
3. **Never avoid real terminology** — define on first use, then keep using the real term. One concept gets exactly one name across the whole page: never alternate between the analogy name and the real name for the same thing.
4. **Never trust parametric memory for facts.** Every number, date, version, standard clause, or named source must be verified against a source before it lands on the page; what cannot be verified is dropped or explicitly marked as approximate. One invented "oh, I see" figure destroys the page's credibility.

Tone: adult to adult. The reader is smart, just lacks background. Banned: baby talk, mascots, coaxing exclamations, emoji as punctuation. **What drops is the barrier to entry, not the information density.**

## 2. Depth modes

| Flag | Mode | Layers |
|---|---|---|
| `--kid` | intuition only | 1–2 |
| (default) | standard | 1–4 |
| `--deep` | deep dive | 1–5 + formal description (formula / pseudocode / data structure), order-of-magnitude estimates, boundary conditions; may close with a **cheat sheet** |

## 3. Choosing the analogy (do this before writing anything)

The whole page rests on this choice, so spend real effort on it. A usable analogy:

- comes from a domain the reader already inhabits physically or socially — not from another technical field;
- has **at least three roles** that map onto real components, so the mapping table isn't padding;
- has a **native failure mode** — it must be able to carry the topic's bottleneck, cost, or trade-off. If the analogy can only show the happy path, it will collapse exactly where Layer 4 needs it. Pick another;
- breaks somewhere *interesting*, giving Layer 5 something real to say.

Generate two or three candidates, test each against the bottleneck, then commit to one and carry it start to finish. **When the topic has no mechanism** — a historical episode, a policy, a contested idea — replace Layer 3 with "what actually happened / what the rule actually says" and keep everything else: the mapping table becomes a claim-to-evidence table.

## 4. Five-layer skeleton

**Layer 1 — one-sentence essence**: holds with zero background, ≤ 30 characters (Chinese) / ≤ 20 words (English), states the working mechanism, no metaphor.

**Layer 2 — intuition journey (4–6 steps)**: one analogy carried start to finish, telling "how people managed before it existed → what happened, step by step". Each step gets a large SVG + 1–2 sentences.

**Layer 3 — the real mechanism**: first the analogy→component mapping table, then the real flow with real terms and structures. Target: the reader can retell "what goes in → what happens inside → what comes out".

**Layer 4 — why designed this way**: a trade-off table (gained / cost) plus at least one "oh, I see" moment: a counterintuitive fact, an order-of-magnitude gap, or a deliberate sacrifice. When the story is an evolution (old design → new design), show it as a diff block — before/after with `+` / `-` lines — instead of versus cards.

**Layer 5 — where the analogy breaks & misconceptions** (skip in `--kid`): ~3 items, each: the misconception → the truth → why people think this way.

**Smallest-view test**: every block earns its size. If a sentence or a small table makes the point, do not inflate it into a stats row, a versus pair, or a full-width SVG. A step whose figure would only re-draw the sentence above it keeps the sentence and drops the figure.

**Ending — one-sentence summary**: repeatable verbatim, contains the mechanism, not the metaphor. In Chinese pages the takeaway block's eyebrow reads 「一句话总结」.

**Cheat sheet** (`--deep` only, optional): a compact final section for later reference — the term mapping and the formal description, restated tightly using tables and code blocks. No new prose, no new diagrams; it is the page's distillate.

## 5. HTML output

Build the page on `references/output-template.md` — it holds the complete stylesheet and the ready-made diagram snippets, and it is the **only** place CSS should be copied from. `references/design-tokens.md` is the law behind it: read it for which class to reach for, the palette semantics, and the SVG rules, which no stylesheet can express. The reference files are written in English; **every visible string in the produced HTML must be localized to the request language** using the string map at the bottom of `output-template.md`.

Produce **one self-contained HTML file**: inline SVG, no external links, no CDN, no JS, no build step, opens on double-click. The page must read as typeset paper, not a dashboard.

The visual system in one breath: parchment `#f5f4ed` canvas, never pure white; two accent hues with divided semantics — celadon owns focus and the positive, terracotta owns cost and failure; one serif family at weights 400/500; flat surfaces, elevation by fill; a line must separate regions, encode state, or carry a data relationship, otherwise delete it.

## 6. Workflow

1. **Parse** `$ARGUMENTS` for the topic and any `--kid` / `--deep` flag. No topic → ask; never generate from nothing. Unsure of depth → standard mode, and close by offering to go deeper or simpler.
2. **Verify the facts first.** List the numbers, dates, versions, and named sources the page will assert, then check them against real sources before writing. This is §1.4 as a procedure, not a wish — do it here, while the page is still cheap to change. Anything unverifiable is dropped or marked approximate.
3. **Choose the analogy** by §3, and sketch the mapping table. If the mapping is thin, the analogy is wrong — go back.
4. **Outline all five layers** as one-liners, including which blocks each layer needs. Apply the smallest-view test to the outline, before the blocks exist.
5. **Read `design-tokens.md` and `output-template.md`**, then generate `diso-<topic-slug>.html` into the current workspace. Language matches the request: Chinese in, Chinese out; English likewise.
6. **Validate**, then fix everything the run reports:

```bash
python3 scripts/check.py diso-<topic-slug>.html
```

7. **Read the judgment checklist in §7** — the half no script can see — and fix what fails.

## 7. Quality checklist

`scripts/check.py` mechanically enforces the visual contract: self-containment, the closed palette, banned CSS, wash-vs-ink density, orthogonal edges, the 4px grid, focus/warning node budgets, resolvable TOC anchors, step-numeral scarcity, print styles. Run it; a clean exit means the *rendering* rules hold.

It cannot see whether the page is any good. Check these yourself:

- [ ] Delete every analogy in your head — does the remaining substance still teach the mechanism? It must be more than half the page.
- [ ] Every number, date, and named source actually verified in step 2 — not recalled.
- [ ] One concept = one name throughout. No sentence alternates between the analogy's word and the real term.
- [ ] The analogy's failure points are written down, and they are specific to this analogy.
- [ ] At least one genuine "oh, I see" moment — and it is true, not just surprising.
- [ ] Smallest-view test: no block is larger than its point requires. Every figure adds something its caption doesn't.
- [ ] Captions add a fact rather than restating the prose.
- [ ] Tone is colleague-to-colleague throughout — no baby talk, no cheerleading.
- [ ] The closing sentence is repeatable verbatim and contains the mechanism, not the metaphor.

## Reference files

| File | When to read |
|---|---|
| `references/design-tokens.md` | Before generating. Palette semantics, component rules of use, SVG rules and bans |
| `references/output-template.md` | At generation time. The complete stylesheet, HTML skeleton, diagram snippets, string map |
| `scripts/check.py` | After generating. `python3 scripts/check.py <file>` — exit 0 means the visual contract holds |
| `examples/diso-btree-index.html` | Optional. A finished page (B-tree indexes) showing how the rules combine; it passes `check.py` clean |
