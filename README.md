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
| `--kid` | concise intuition | journey + compact mapping/mechanism + one plain-language analogy limit |
| *(none)* | standard | all five layers, including where the analogy breaks |
| `--deep` | deep dive | standard + formal description, explicit assumptions, boundary conditions, optional cheat sheet |

Chinese in, Chinese out; English likewise. Every mode includes sources and a mechanism-based takeaway. Ordinary chat explanations do not automatically trigger HTML generation. The skill writes `diso-<topic>.json`, then builds `diso-<topic>.html` in the working directory. Python 3.10+ is required; the delivered HTML needs only a browser.

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
| `references/output-template.md` | JSON schema, markup guidance, diagram snippets, string map |
| `assets/base.html` | The single stylesheet and HTML shell |
| `scripts/build.py` | Escaping, mode selection, TOC generation, strict validation and atomic output |
| `scripts/check.py` | Validator CLI and page structure checks |
| `scripts/markup.py`, `scripts/svg.py` | HTML parsing, static vocabulary and SVG geometry/paint checks |
| `tests/` | Positive/negative fixtures and regression tests, run in CI |
| `examples/` | Reproducible B+ tree JSON, generated standard page and preview |

`design-tokens.md` states the visual rules. The builder copies CSS from `assets/base.html` unchanged; generated pages cannot add inline styles or extra stylesheets. When changing the asset, rebuild the example and run the tests.

## Build and validate

Inside this repository:

```bash
python3 scripts/build.py examples/btree-index.json -o diso-btree-index.html
python3 scripts/check.py diso-btree-index.html
python3 scripts/build.py examples/btree-index.json --mode deep -o diso-btree-deep.html
python3 -m unittest discover -s tests -v
```

After installation, commands work from another project's directory by using the installed path:

```bash
python3 "$HOME/.claude/skills/diso/scripts/build.py" diso-topic.json -o diso-topic.html
python3 "$HOME/.claude/skills/diso/scripts/check.py" diso-topic.html
```

For a project-scoped install, use that installation's absolute path instead. Claude Code skill instructions use its `${CLAUDE_SKILL_DIR}` substitution; the Python scripts resolve assets relative to themselves, never to the caller's working directory.

Both scripts use only the standard library. Exit **0** means no mechanical findings, **1** means an error or warning, **2** means invalid input/usage or an I/O failure. The builder validates before replacing output, so a failed build preserves an existing page.

The supported format is deliberately bounded: one exact bundled stylesheet; no JS, event handlers, embeds or external resource dependencies; six-digit palette colors and local SVG patterns; orthogonal M/L/H/V/Z paths (including relative commands), lines and polylines; geometrically checked 5×7 chevrons; rectangle/edge grids; node dimensions; accent budgets; title/description accessibility text; depth sections and matching TOC anchors. Unsupported tags, attributes, CSS, curves and transforms fail closed. Prose and escaped code are not scanned as executable markup, styles or resource URLs.

**Citation links are allowed.** “Self-contained” means the page renders without external dependencies; it does not forbid links to evidence. Sources appear in every mode, with notes about the claims they support.

A clean exit is **not** proof of factual accuracy, font/layout quality or safety of arbitrary untrusted HTML. This is a format validator, not a sanitizer. Human/rendered review still checks analogy quality, label/range consistency, actual arrow attachment, crossings and clipping. `SKILL.md` §7 records those checks.

## Design notes

Two decisions worth stating, because they cost something:

**Zero JavaScript** means the right-edge table of contents has no scroll-spy — hover state only. That is the explicit price of a file that opens from disk in ten years, and the rulebook forbids sneaking a `<script>` in to fix it.

**No external fonts** means the preferred Chinese serif (TsangerJinKai02) can't be linked, so the stack falls back through Source Han Serif / Noto Serif SC / Songti, with Latin families first so mixed CJK/Latin text shares a baseline, and every family written under both its English and localized name because Windows often registers only the latter.
