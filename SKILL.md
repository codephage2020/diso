---
name: diso
description: Create an illustrated, self-contained HTML explainer for /diso followed by a topic. Ordinary conversational explanations stay in chat.
---

# diso — 深入浅出

Explain the topic in `$ARGUMENTS` using the Feynman technique and a concrete analogy. Write for an intelligent adult new to the subject, in the request language.

## Output contract

- Essence → illustrated intuition → analogy-to-component mapping → real mechanism → design trade-offs → sources → mechanism-based takeaway.
- `--kid`: compact mechanism; omit trade-offs. `--deep`: add formal details with assumptions and optional cheat sheet. Default: standard.
- The intuition journey has 4–6 steps, at least one substantive inline SVG, and a mapping with at least three rows. Add figures when they explain a relationship.
- Cite supporting sources for factual claims; label teaching assumptions and derived estimates.

## Build

Read [output-template.md](references/output-template.md) for the JSON schema and supported markup. Use [design-tokens.md](references/design-tokens.md) for project-specific styling and diagram geometry; consult SVG snippets as needed.

Write `diso-<topic-slug>.json` in the user's workspace with only the requested mode's content. Plain fields are escaped; `_html` and `svg` fields contain markup. The builder owns the document shell, stylesheet and TOC.

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/build.py" \
  "diso-<topic-slug>.json" -o "diso-<topic-slug>.html"
```

Python 3.10+, standard library only. Claude Code substitutes `${CLAUDE_SKILL_DIR}`; other hosts use the absolute directory containing this skill. Input and output stay in the user's workspace.

The build validates before atomically replacing output; errors and warnings fail the build. Fix the reported JSON fields and rebuild. Standalone `scripts/check.py` checks existing HTML.

Inspect the rendered page for readability and diagram correctness when a browser is available, then return the HTML link. The validator checks format; factual and visual quality require review.
