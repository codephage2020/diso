# diso — 深入浅出

A skill that turns a topic into an illustrated, self-contained HTML page. Start with an analogy, understand the real mechanism, and explore its design trade-offs.

Hand-drawn inline SVG. No JavaScript, no external dependencies. Open in any browser.

## Install

Requires nothing but the agent runtime — pages are written directly as HTML.

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
| Default | Essence → illustrated intuition → real mechanism → design rationale |
| `--kid` | A shorter explanation with an illustrated intuition and compact mechanism |
| `--deep` | Standard plus formal details, assumptions and boundary conditions |

Every mode includes sources and follows the input language. The skill writes `diso-<topic>.html` to your working directory. Open it directly; no server is needed.

## How it works

The skill reads [SKILL.md](SKILL.md) for the content contract and copies the shell and stylesheet from [base.html](base.html) verbatim, then writes the finished page in one pass. There is no build step, no intermediate format, and nothing to validate — visual quality is the agent's job, checked in a browser.