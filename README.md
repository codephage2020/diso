# diso — 深入浅出

A Claude skill that turns a topic into an illustrated, self-contained HTML page. Start with an analogy, understand the real mechanism, and learn where the analogy breaks.

Hand-drawn SVG diagrams. No JavaScript or external dependencies. Open in any browser.

<details>
<summary>View full preview</summary>

![B+ tree explanation preview](examples/preview.png)

</details>

## Install

Requires Python 3.10+ to generate pages.

```bash
git clone https://github.com/codephage2020/diso.git ~/.claude/skills/diso
```

For a project-only installation, clone into `.claude/skills/diso` inside your project.

## Use

```text
/diso B-tree 索引
/diso TCP congestion control --deep
/diso 为什么飞机能飞 --kid
```

| Mode | Output |
|---|---|
| Default | Essence → illustrated intuition → real mechanism → design rationale → analogy limits |
| `--kid` | A shorter explanation with a simple mechanism and analogy limit |
| `--deep` | All five layers plus formal details, assumptions and boundary conditions |

Every mode includes sources and follows the input language. The skill writes `diso-<topic>.json` and `diso-<topic>.html` to your working directory. Open the HTML directly; no server is needed.

## Development

Run from the repository root:

```bash
python3 scripts/build.py examples/btree-index.json -o diso-btree-index.html
python3 scripts/check.py diso-btree-index.html
python3 -m unittest discover -s tests -v
```

The builder validates before replacing output. Errors and warnings fail validation. Citation links are allowed; external rendering dependencies are not. Validation checks the supported format, not factual accuracy or visual quality, and is not a sanitizer for arbitrary HTML.

See [SKILL.md](SKILL.md) for the workflow, [output-template.md](references/output-template.md) for the content schema and SVG snippets, and [design-tokens.md](references/design-tokens.md) for visual rules. The shared HTML and CSS live in [assets/base.html](assets/base.html).
