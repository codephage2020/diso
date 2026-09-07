# diso — 深入浅出

A Claude skill that explains a topic **plainly without making it shallow**, and delivers the explanation as one self-contained HTML page: hand-drawn SVG diagrams, print-quality typesetting, zero JavaScript, opens on double-click.

The name is the stance. `diso` = 深入浅出 — go deep, come out plain.

![preview](examples/preview.png)

## The bet

Most "explain simply" output stops at the analogy: a warm metaphor, a satisfied reader, and nothing that survives the walk to the whiteboard. diso treats the analogy as **the entrance, not the destination**, and enforces that with one rule:

> Delete every analogy from the finished piece. The real mechanism that remains must still stand on its own.

So every page carries two layers that must both hold: an intuition journey that gets you in the door, and a real-mechanism section with real terminology, a mapping table from each analogy role to the thing it stands for, and an honest account of where the analogy breaks.

## Install

```bash
git clone https://github.com/codephage2020/diso.git ~/.claude/skills/diso
```

Project-scoped instead of personal: clone into `.claude/skills/diso` inside the repo you're working in.

## Use

```
/diso B-tree 索引
/diso TCP congestion control --deep
/diso 为什么飞机能飞 --kid
```

| Flag | Mode | What you get |
|---|---|---|
| `--kid` | intuition only | the journey and the pictures, layers 1–2 |
| *(none)* | standard | layers 1–4 — intuition, mechanism, trade-offs |
| `--deep` | deep dive | all five layers, plus formulas / pseudocode, orders of magnitude, boundary conditions, and an optional cheat sheet |

Chinese in, Chinese out; English likewise. The page is written to `diso-<topic>.html` in the working directory.

## What the page is made of

**Five layers.** One-sentence essence → intuition journey (4–6 illustrated steps) → the real mechanism → why it was designed this way → where the analogy breaks.

**A closed visual system.** Parchment `#f5f4ed`, never pure white. Two accent hues with divided semantics: celadon owns focus and gains, terracotta owns cost and failure — never swapped. Each ships in a wash for fills and an ink for text and lines, because the washes measure 1.85:1 and 2.97:1 on parchment and would be illegible as type. One serif family, weights locked to 400/500. Elevation by fill, never shadow.

**A subtraction principle.** A line earns its existence only when it separates regions, encodes state, or carries a data relationship. Hide it; if meaning, state, grouping, and navigation are unchanged, it goes.

**Diagrams with rules.** Orthogonal edges only — no diagonals. Every edge endpoint lands on a node-edge midpoint, a bus, or a timeline. Arrowheads are hand-drawn chevrons, never `<marker>` (which doesn't rotate under WeasyPrint). At most two focus nodes per figure, one accent hue per figure, six sequence dots, two group containers.

## Repo layout

| Path | What it is |
|---|---|
| `SKILL.md` | The skill: stance, depth modes, the five-layer skeleton, workflow, quality gates |
| `references/design-tokens.md` | The law — palette semantics, component rules of use, the full SVG rulebook |
| `references/output-template.md` | The implementation — complete stylesheet, HTML skeleton, diagram snippets, string map |
| `scripts/check.py` | The validator |
| `examples/` | A finished page (B-tree indexes) and its preview |

`design-tokens.md` states rules and `output-template.md` implements them; CSS is copied from the template only, so the two never drift.

## The validator

The visual contract is mechanical, so it's checked mechanically rather than hoped for:

```bash
python3 scripts/check.py diso-btree-index.html
```

Stdlib only, no dependencies. Exit 0 means the page holds. It enforces self-containment (no script, no CDN, no external fonts), the closed 25-colour palette, banned CSS (`box-shadow`, gradients, `rgba()`, italics, radius > 10px, weight > 500), wash-vs-ink density, orthogonal-only SVG edges, the 4px layout grid, text baselines that don't clip, focus/warning-node budgets, one accent hue per figure, resolvable TOC anchors, step-numeral scarcity, and print styles.

What it deliberately does not check is whether the page is any *good* — whether substance survives deleting the analogies, whether the "oh, I see" moment is true, whether one concept keeps one name. `SKILL.md` §7 keeps those as a human checklist.

## Design notes

Two decisions worth stating, because they cost something:

**Zero JavaScript** means the right-edge table of contents has no scroll-spy — hover state only. That is the explicit price of a file that opens from disk in ten years, and the rulebook forbids sneaking a `<script>` in to fix it.

**No external fonts** means the preferred Chinese serif (TsangerJinKai02) can't be linked, so the stack falls back through Source Han Serif / Noto Serif SC / Songti, with Latin families first so mixed CJK/Latin text shares a baseline, and every family written under both its English and localized name because Windows often registers only the latter.
