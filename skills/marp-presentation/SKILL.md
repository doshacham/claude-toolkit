---
name: marp-presentation
description: Build Marp slide decks (pptx/pdf/html). Use when making a presentation, talk, pitch, or briefing, or converting a codebase, paper, data, or architecture doc into slides. Bundles 5 templates, 15 themes, 14 scripts, Playwright QA loop.
argument-hint: "[mode] [topic or source path]"
allowed-tools: Read Write Edit Bash Glob Grep AskUserQuestion
hooks:
  PostToolUse:
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: "python C:/Users/User/.claude/skills/marp-presentation/scripts/_hook_lint.py"
          timeout: 30
---

# Marp Presentation

Build slide decks with [Marp](https://marp.app/) — Markdown-based slides that compile to .pptx, .pdf, and .html via a single CLI. Version-controllable, grep-able, diff-able. No design tool required.

## Non-negotiables

1. **Nothing on a slide may overlap anything else.** See `references/qa_playbook.md` — the QA loop enforces this.
2. **The QA loop (lint → render → Playwright audit → fix → repeat) runs until clean.** No "ship with one known warning" unless the user accepts it explicitly.
3. **Typography is baseline in `references/typography.md`.** Deviate only for documented reasons.
4. **Emojis and visuals are encouraged** when they match the theme's environment; **never** when they fight it. Re-audit styling after adding many visuals — visual density is the #1 cause of overflow.

## When to use this skill

Trigger on any of:

- Make / create / build / draft / design a presentation, slide deck, talk, pitch, briefing, keynote, or all-hands
- Convert content (repo, paper, data, incident report, architecture doc, ADR, readme) into slides
- Update, restyle, or re-theme an existing Marp deck
- Render or re-render an existing .md deck to pptx/pdf/html

## The six modes

Identify which mode fits the task. Detailed slide archetypes per mode live in `references/modes.md`.

1. **Technical codebase deep-dive** — explain a feature/subsystem. Code-heavy. Budget: 12-25 slides.
2. **Research paper to conference talk** — 10-20 slide paper talk. Integrates with `read-arxiv` summaries in `./knowledge/`.
3. **Narrative storytelling deck** — pitch, vision, launch. Big-type, emotional arc. Budget: 6-15 slides.
4. **Data to insight briefing** — executive summary from metrics. Charts + headlines. Budget: 5-12 slides.
5. **Onboarding deck from repo** — day-one new-hire deck. Budget: 8-18 slides.
6. **Architecture showcase** — system visualization with C4/sequence diagrams. Budget: 8-18 slides.

## The fifteen themes

Full catalog with reasoning and mode fit in `references/themes.md`. Summary:

| Theme | Vibe | Modes |
|---|---|---|
| midnight | deep navy, cyan/magenta accents | technical, architecture |
| paper | warm cream, editorial serif | research, onboarding |
| terminal | black + green mono, CRT feel | technical, architecture |
| corporate | white, navy, Inter grid | narrative, data, onboarding |
| brutalist | stark B/W, heavy Helvetica | narrative |
| neon | black, pink/cyan glow | narrative |
| academic | cream, EB Garamond, footnotes | research |
| dashboard | slate, huge numerics | data |
| minimal | white, thin rules, whitespace | research, onboarding, data |
| gradient | sunset gradients, glassmorphism | narrative, onboarding |
| blueprint | cyan grid on navy, drafting | architecture, technical |
| monochrome | grayscale Swiss grid | research, technical, data |
| kraft | brown paper, handwritten feel | onboarding |
| high_contrast | WCAG-AAA, max legibility | any |
| pastel | soft tones, rounded | onboarding, narrative |

Pick the best theme for the content and tell the user what you chose with one line of reasoning. If the user wants to change it, they'll say so. Consult `references/themes.md` for the full catalog and mode mappings.

## Authoring workflow

Do not skip or reorder.

### Step 0a — Detect the mode (optional)

If the user points you at source material but doesn't name a mode, you can get a ranked suggestion:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/detect_mode.py" --input ./my-repo --format text
```

Use it as a hint, then confirm with the user.

### Step 0b — Scaffold from a repo (onboarding mode only)

For an onboarding deck, skip Step 1 and use `from_repo.py` instead:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/from_repo.py" --repo ./my-project --out ./onboarding.md --theme paper
```

It walks the repo (README, package.json, pyproject.toml, top-level dirs, .env.example, CONTRIBUTING.md) and produces a scaffolded deck with placeholders you fill in. Jump to Step 4 after that.

### Step 0c — Read the golden example for your mode

Before writing anything, read one exemplar deck from `references/examples/`:

- `technical_codebase.md` — for technical and architecture modes
- `narrative_pitch.md` — for narrative mode
- `data_briefing.md` — for data mode

They're the target. Aim for that quality bar.

### Step 1 — Pick template and theme

Templates live in `templates/`:

- `default.md` — neutral, works for anything
- `technical.md` — monospace-forward, code-heavy
- `narrative.md` — big-type pitch
- `academic.md` — research talk with math and citations
- `data.md` — dashboard-style with big numerics

Pick the best theme for the content type. Tell the user your choice with one line of reasoning. Read `references/themes.md` for the full catalog.

### Step 2 — Scaffold the deck

```bash
python "${CLAUDE_SKILL_DIR}/scripts/new_deck.py" \
  --template technical \
  --theme midnight \
  --out ./deck.md \
  --title "Auth Rewrite" \
  --subtitle "Design review"
```

### Step 3 — Draft the outline FIRST

Before filling any slide body, list slide titles plus one-line intents as Markdown comments at the top of the deck file. Present this skeleton to the user for approval. Iterate on structure before writing any content. **Non-negotiable.**

### Step 4 — Fill slides

Rules:

- One idea per slide
- Titles are sentences / assertions, not topics ("We lost 12% of sessions after the rewrite", not "Session metrics")
- No more than five bullets per slide; prefer prose + visual
- Code blocks: fenced triple-backticks with a language hint
- Diagrams: Mermaid (native) or images. See `references/diagrams.md` for 18 Mermaid types + HTML-embed charts + external imports
- Speaker notes: HTML comments (`<!-- ... -->`)

When Marp syntax is unclear, read `references/marp-cheatsheet.md`.

### Step 4.5 — Generate diagrams and charts (as needed)

For data-driven charts from CSV:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/make_chart.py" \
  --csv data.csv --type bar --x quarter --y revenue \
  --theme midnight --out charts/revenue.png
```

For a Mermaid flowchart of a Python file's internal call graph:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/code_to_mermaid.py" \
  --input src/pipeline.py --fence --out pipeline.mmd
```

For ASCII boxes (terminal/brutalist themes):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/ascii_box.py" \
  --mode boxes --labels "Client,API,Service,DB" --fence
```

### Step 5 — Lint (mandatory)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/lint.py" --input ./deck.md --mode technical --format text
```

The lint script checks:

- Marp frontmatter validity (`marp: true`)
- Per-mode slide budget (e.g. technical decks 12-25 slides)
- Slide length warnings (text overflow heuristic)
- Title-as-assertion heuristic (flags topic-only titles)
- No slide has more than 5 bullets
- Balanced code fences
- HTTP link health (HEAD every link; warn on 4xx/5xx)
- Markdown hygiene (via `markdownlint-cli2` if available)
- Spelling (via `cspell` if available)

Fix every **error**. Acknowledge **warnings** consciously.

The lint passes `scripts/markdownlint.jsonc` (which disables Marp-incompatible rules: MD013 line-length, MD025 multiple-h1, MD033 inline-HTML, MD041 first-line-h1, MD046 code-block-style) to `markdownlint-cli2` automatically when the tool is installed. To tune markdownlint further, edit that config file.

A PostToolUse hook auto-runs a lightweight version of this lint whenever the agent writes or edits a Marp file — so slips get caught even if you forget.

### Step 5.5 — Optional: insert a TOC slide

For decks with 10+ slides, auto-generate a table-of-contents slide:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/insert_toc.py" --input ./deck.md --at 2 --title "Outline"
```

Detects an existing TOC and replaces it; otherwise inserts at the given position.

### Step 5.6 — Optional: deck stats

Quick health check of the deck before rendering:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/deck_stats.py" --input ./deck.md
# 14 slides · 842 words · 6 visuals · 2 code blocks · ~9.2 min
```

Use `--verbose` for a full breakdown.

### Step 5.7 — Optional: duration estimate

For talks with a target length:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/estimate_duration.py" --input ./deck.md --target-minutes 15
```

Reports total, flags long slides, and validates against the target.

### Step 6 — Render

Single format:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format html
```

Bundle all three formats in one call:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format bundle
```

Handout PDF with speaker notes:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format handout
```

Watch mode (re-render on save):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format html --watch
```

Live preview server (serves a directory at localhost:8080):

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --server --input-dir ./decks/
```

Always render `html` first — it is the input for Playwright QA.

**Skip unchanged renders:** pass `--skip-unchanged` to avoid re-rendering when the input hash matches the cached hash and the output still exists. Cache lives in `.marp_render_cache.json` next to the deck.

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format bundle --skip-unchanged
```

### Step 6.5 — Optional: diff screenshots against a previous render

For iterative review, save QA screenshots to versioned dirs (e.g. `docs/qa/v1/`, `docs/qa/v2/`) and run:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/diff_screenshots.py" --before docs/qa/v1 --after docs/qa/v2
```

Reports added/removed/changed/unchanged slides by SHA hash. No Pillow required. Open changed slides in Playwright MCP to inspect visually.

### Step 7 — QA with Playwright (mandatory)

Read `references/qa_playbook.md` and execute it. Short version:

1. Use Playwright MCP to open the rendered `.html` file (`file://` URL)
2. Count slides, screenshot each one
3. Per slide: JS eval comparing `scrollHeight` vs `clientHeight` to detect overflow
4. Accessibility checks (alt text, heading order, color contrast)
5. Broken image check, font load check
6. Produce a report. Fix errors. Re-render. Re-QA.

Never declare the deck done until QA is clean.

### Step 8 — Extract speaker notes (optional)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/notes.py" \
  --input ./deck.md --out ./deck_notes.md
```

Produces a standalone presenter script with every `<!-- ... -->` comment grouped by slide.

## Integration with read-arxiv

When the user provides an arxiv URL (e.g. `https://arxiv.org/abs/2601.07372`), the agent chains:

1. Invoke the `read-arxiv` skill first — it downloads the paper, reads it, and writes `./knowledge/summary_<tag>.md`
2. Read that summary
3. Enter research-paper mode using the `academic` template + theme
4. Proceed from Step 1 above

This chain is zero-cost and turns "make a deck from this paper" into one command.

## Files in this skill

```
marp-presentation/
├── SKILL.md                          (this file)
├── scripts/
│   ├── new_deck.py                   (scaffold from template + theme)
│   ├── render.py                     (bundle / handout / watch / server / skip-unchanged)
│   ├── lint.py                       (mode-aware lint, slide + time budgets, link check)
│   ├── deck_stats.py                 (one-line health summary)
│   ├── estimate_duration.py          (speaking-time estimator)
│   ├── insert_toc.py                 (auto-TOC slide)
│   ├── detect_mode.py                (suggest mode from source material)
│   ├── from_repo.py                  (scaffold onboarding deck from a repo)
│   ├── diff_screenshots.py           (compare two dirs of QA screenshots, no deps)
│   ├── make_chart.py                 (CSV → themed matplotlib PNG)
│   ├── code_to_mermaid.py            (Python source → Mermaid flowchart)
│   ├── ascii_box.py                  (ASCII box / tree / grid diagrams)
│   ├── notes.py                      (extract speaker notes to standalone md)
│   ├── _hook_lint.py                 (PostToolUse hook wrapper, internal)
│   └── markdownlint.jsonc            (shared config, disables Marp-incompatible rules)
├── templates/
│   ├── default.md
│   ├── technical.md
│   ├── narrative.md
│   ├── academic.md
│   └── data.md
├── themes/
│   ├── midnight.css
│   ├── paper.css
│   ├── terminal.css
│   ├── corporate.css
│   ├── brutalist.css
│   ├── neon.css
│   ├── academic.css
│   ├── dashboard.css
│   ├── minimal.css
│   ├── gradient.css
│   ├── blueprint.css
│   ├── monochrome.css
│   ├── kraft.css
│   ├── high_contrast.css
│   └── pastel.css
└── references/
    ├── modes.md                      (slide archetypes per mode)
    ├── themes.md                     (theme catalog with reasoning)
    ├── typography.md                 (typography baseline + rules)
    ├── marp-cheatsheet.md            (Marp syntax quick-ref)
    ├── diagrams.md                   (Mermaid + HTML charts + externals)
    ├── qa_playbook.md                (Playwright QA loop, the enforcer)
    └── examples/
        ├── technical_codebase.md     (golden example: technical mode)
        ├── narrative_pitch.md        (golden example: narrative mode)
        └── data_briefing.md          (golden example: data mode)
```

## Requirements

- **Node.js + npx** — required for Marp CLI (fetched on demand via npx, no global install)
- **Python 3** — standard library only for new_deck, render, lint, code_to_mermaid, ascii_box, notes, _hook_lint
- **matplotlib** — required only if you use `scripts/make_chart.py` (`pip install matplotlib`)
- **Playwright MCP** — the presenter agent attaches `@playwright/mcp@latest` inline; no user install needed
- **Optional lint tools** — `markdownlint-cli2` and `cspell` via npx; lint skips gracefully if missing
