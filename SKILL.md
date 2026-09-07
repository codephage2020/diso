---
name: diso
description: Create a self-contained HTML explainer with an analogy, its mapping to the real mechanism, its limits, source citations, and inline SVG diagrams. Use for /diso followed by a topic, or requests for an illustrated HTML explainer. Ordinary conversational explanations do not need this skill.
---

# diso — plain, not shallow

Explain like I'm an intelligent adult with zero background in this topic.

Topic: $ARGUMENTS — or, if that is empty, whatever the user asked to have explained.

## 1. Core stance: the analogy is the entrance, not the destination

> Delete every analogy from the finished piece. The real mechanism that remains must still stand on its own.

1. **Every analogy ships with a mapping** — a table mapping each analogy role to the real component it stands for.
2. **Every analogy ships with its failure points** — state where it stops holding.
3. **Never avoid real terminology** — define on first use, then keep using the real term. One concept gets exactly one name across the whole page: never alternate between the analogy name and the real name for the same thing.
4. **Never trust parametric memory for facts.** Every factual number, date, version, standard clause or named source must be verified before it lands on the page. Drop unverifiable claims; label teaching assumptions and estimates derived from them explicitly. One invented "oh, I see" figure destroys the page's credibility.

Tone: adult to adult. The reader is smart, just lacks background. Banned: baby talk, mascots, coaxing exclamations, emoji as punctuation. **What drops is the barrier to entry, not the information density.**

## 2. Depth modes

| Flag | Mode | Layers |
|---|---|---|
| `--kid` | concise intuition | 1–2 + compact mapping and real mechanism + one plain-language analogy limit |
| (default) | standard | All five layers, including analogy limits |
| `--deep` | deep dive | Standard + formal description (formula / pseudocode / data structure), explicit assumptions and boundary conditions; optional **cheat sheet** |

Every mode includes sources and a mechanism-based takeaway. `--kid` changes depth, not the adult tone. The builder selects the sections and TOC; never manually hide deep content with CSS.

## 3. Choosing the analogy (do this before writing anything)

The whole page rests on this choice, so spend real effort on it. A usable analogy:

- comes from a domain the reader already inhabits physically or socially — not from another technical field;
- has **at least three roles** that map onto real components, so the mapping table isn't padding;
- has a **native failure mode** — it must be able to carry the topic's bottleneck, cost, or trade-off. If the analogy can only show the happy path, it will collapse exactly where Layer 4 needs it. Pick another;
- breaks somewhere *interesting*, giving Layer 5 something real to say.

Generate two or three candidates, test each against the bottleneck, then commit to one and carry it start to finish. **When the topic has no mechanism** — a historical episode, a policy, a contested idea — replace Layer 3 with "what actually happened / what the rule actually says" and keep everything else: the mapping table becomes a claim-to-evidence table.

## 4. Five-layer skeleton

**Layer 1 — one-sentence essence**: holds with zero background, ≤ 30 characters (Chinese) / ≤ 20 words (English), states the working mechanism, no metaphor.

**Layer 2 — intuition journey (4–6 steps)**: one analogy carried start to finish, telling "how people managed before it existed → what happened, step by step". Each step gets 1–2 sentences; add an SVG when it communicates a relationship the prose cannot. Keep at least one substantive figure in the journey.

**Layer 3 — the real mechanism**: first the analogy→component mapping table, then the real flow with real terms and structures. Target: the reader can retell "what goes in → what happens inside → what comes out".

**Layer 4 — why designed this way**: a trade-off table (gained / cost) plus at least one "oh, I see" moment: a counterintuitive fact, an order-of-magnitude gap, or a deliberate sacrifice. When the story is an evolution (old design → new design), show it as a diff block — before/after with `+` / `-` lines — instead of versus cards.

**Layer 5 — where the analogy breaks & misconceptions**: ~3 items, each: the misconception → the truth → why people think this way. In `--kid`, keep one specific limit in plain language instead.

**Smallest-view test**: every block earns its size. If a sentence or a small table makes the point, do not inflate it into a stats row, a versus pair, or a full-width SVG. A step whose figure would only re-draw the sentence above it keeps the sentence and drops the figure.

**Ending — one-sentence summary**: repeatable verbatim, contains the mechanism, not the metaphor. In Chinese pages the takeaway block's eyebrow reads 「一句话总结」.

**Cheat sheet** (`--deep` only, optional): a compact final section for later reference — the term mapping and the formal description, restated tightly using tables and code blocks. No new prose, no new diagrams; it is the page's distillate.

## 5. HTML output

Use `scripts/build.py` to assemble content into `assets/base.html`. That asset is the only stylesheet and document shell; do not copy or edit CSS in generated pages. Read `references/output-template.md` for the JSON schema, localization and SVG snippets, and `references/design-tokens.md` for visual semantics.

The delivered HTML is self-contained: inline SVG, no external dependencies, CDN, JavaScript or runtime build step. It opens on double-click. Passive HTTP(S) citation links are allowed; fetching images, fonts, stylesheets or embedded documents is not. Use the bundled classes; inline styles and extra stylesheets are rejected. Write SVG presentation attributes explicitly, not CSS variables or transforms.

The visual system: parchment `#f5f4ed`, celadon for focus and gains, terracotta for cost and failure, serif weights 400/500, flat surfaces and orthogonal diagrams. The page should read as typeset paper.

## 6. Workflow

1. **Parse** `$ARGUMENTS` for the topic and `--kid` / `--deep`. No topic → ask. No flag → standard. Do not pass the raw topic or arguments to a shell.
2. **Verify facts.** Check numbers, dates, versions and named sources before writing. Keep a source list with the claim each source supports. Mark teaching assumptions and derived estimates explicitly. Drop unsupported factual claims; do not turn them into “approximate” facts.
3. **Choose the analogy** by §3 and sketch its mapping. If the mapping is thin, choose another.
4. **Outline the requested depth**, retaining a real mechanism and an analogy limit in every mode. Apply the smallest-view test before generating figures.
5. **Read the authoring and design references**, then write `diso-<topic-slug>.json` in the current workspace. Use a simple filename slug. Plain string fields are escaped by the builder; only fields ending in `_html` and `svg` are markup. Escape code examples inside those markup fields. Localize visible copy and SVG text to the request language.
6. **Build and validate from the current workspace**, using the installed skill's absolute path:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build.py" \
  "diso-<topic-slug>.json" -o "diso-<topic-slug>.html"
python3 "${CLAUDE_SKILL_DIR}/scripts/check.py" "diso-<topic-slug>.html"
```

Claude Code substitutes `${CLAUDE_SKILL_DIR}` in this skill body; it is not a shell environment variable you should assume exists in other agents. In another host, resolve the directory containing the loaded `SKILL.md` and substitute that absolute directory in both commands. Keep input/output paths in the user's workspace. The scripts resolve their own assets relative to `__file__`, so installation location and shell working directory can differ.

Python 3.10+ is required; there are no third-party dependencies. The JSON `mode` defaults to `standard`; use `kid` or `deep` when requested. A build with any error or warning fails before writing the output. Fix every finding and rebuild; never bypass validation or replace the trusted stylesheet to make a generated page pass.
7. **Review §7** and inspect the rendered page when a renderer is available. The validator cannot judge factual support, readability, clipping in every font, or whether an arrow conveys the right relationship.

## 7. Quality checklist

`scripts/check.py` checks the supported HTML/SVG vocabulary, exact bundled CSS, resource attributes, palette, orthogonal geometry, marked/rounded node sizes, rectangle/edge grid, accent budgets, accessibility text, TOC and depth structure. Exit 0 means no mechanical findings, not proof of safety or visual correctness. It is a format validator, not a sanitizer for arbitrary untrusted HTML.

It cannot see whether the page is any good. Check these yourself:

- [ ] Delete every analogy in your head — does the remaining substance still teach the mechanism? In standard/deep mode, it must be more than half the substance; in kid mode the compact real mechanism must still stand alone.
- [ ] Every factual number, date and named source was verified in step 2. The sources section identifies supporting claims; numerical teaching assumptions are labeled.
- [ ] Diagram ranges, labels, arrow endpoints and the prose agree; check these visually.
- [ ] One concept = one name throughout. No sentence alternates between the analogy's word and the real term.
- [ ] The analogy's failure points are written down, and they are specific to this analogy.
- [ ] In standard/deep mode, at least one genuine "oh, I see" moment — true, not just surprising.
- [ ] Smallest-view test: no block is larger than its point requires. Every figure adds something its caption doesn't.
- [ ] Captions add a fact rather than restating the prose.
- [ ] Tone is colleague-to-colleague throughout — no baby talk, no cheerleading.
- [ ] The closing sentence is repeatable verbatim and contains the mechanism, not the metaphor.

## Reference files

| File | When to use |
|---|---|
| `references/design-tokens.md` | Before generating: palette semantics, component use and SVG rules |
| `references/output-template.md` | When authoring JSON: schema, mode fields, localization and diagram snippets |
| `assets/base.html` | Builder-owned stylesheet and shell; no need to copy it into model context |
| `scripts/build.py` | Assemble and strictly validate a page from JSON |
| `scripts/check.py` | Validate the final HTML; any finding returns nonzero |
| `examples/btree-index.json` | A complete, reproducible input supporting all three modes |
| `examples/diso-btree-index.html` | Finished standard-mode example |
