---
name: Paper
description: >
  This skill should be used when the user asks to "write a paper", "generate a paper",
  "create a dev-blog post", "write a blog post about this project", "write an article
  about this project", "paper this project", "turn this project into an article",
  "write up this project", or invokes /paper. Synthesizes codebase analysis, README,
  and project docs into a newspaper-style dev-blog article with a punchy headline,
  strong lead, and technical depth woven into narrative — not an architecture dump.
  Not for generating README files, changelogs, or architecture documentation.
version: 1.0.0
---

# Paper — Newspaper-Style Dev-Blog Generator

Generate a compelling dev-blog article from a software project. The output reads like a
newspaper feature — headline that hooks, lead that sells, story that delivers — with
technical details woven in where they matter. No architecture dumps. No bullet-point
summaries. A story.

## When to Use

Invoke when the user wants to turn a project into a written piece for a dev-blog,
portfolio showcase, or sharing with collaborators. The skill is fully autonomous — no
interview required. It reads the project and finds the story.

## Output

- **Format:** Markdown
- **Location:** `docs/paper.md` in the project root
- **Length:** 1,500–3,000 words (scales with project complexity)
- **One-shot:** Generated in a single pass; re-run to regenerate

## Process

### Phase 1: Gather Raw Material

Read the project systematically to build a mental model. Prioritize in this order:

1. **README.md** — The author's own pitch. This is the richest signal for what the project
   is about and why it exists. Extract the problem statement, motivation, and key claims.
2. **CLAUDE.md / .claude/ rules** — Project conventions, architecture notes, constraints.
   These reveal decisions and tradeoffs the author cared enough to codify.
3. **docs/ directory** — Specs, design docs, ADRs. These contain the "why" behind decisions.
4. **Package manifest** — `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, etc.
   Extract dependencies, project name, description. Dependencies reveal the tech story.
5. **Directory structure** — Run `ls` or Glob on the top two levels. The shape of the
   project tells you what it is (monorepo? CLI? API? library?).
6. **Key source files** — Read 3–5 core files that represent the project's main logic.
   Identify patterns, abstractions, and anything clever or unusual.
7. **Git log (recent)** — `git log --oneline -20` to sense the pace, focus areas, and
   evolution of the project.

### Edge Cases

- **No README found:** Lean harder on the package manifest, CLAUDE.md, and code analysis.
  The headline and lead will require more inference from the codebase itself.
- **Very small project (< 5 files):** Produce a shorter article (1,200–1,500 words). Default
  to "The Itch Story" template from `references/article-structure.md`.
- **Monorepo with multiple projects:** Focus on the subproject in the current working
  directory. If at the repo root, ask the user which subproject to cover.
- **No docs, no README, minimal code:** Produce what's possible from the code and manifest.
  Acknowledge the project is early-stage — frame the article around the ambition and
  initial approach rather than results.

### Phase 2: Find the Story

This is the critical step. Do NOT skip it. Do NOT default to "this project has a clean
architecture." Ask these questions internally:

- **What problem was painful enough to build this?** The README usually says. If not,
  infer from the code — what does the main entry point do? What pain does it relieve?
- **What is the one surprising decision?** Every project has one. An unusual dependency,
  an unconventional architecture, a constraint that shaped everything. Find it.
- **What would a developer learn by reading this code?** Identify the transferable insight —
  a pattern, a technique, a tradeoff that generalizes beyond this project.
- **What is the thesis?** Distill into one sentence: "This project proves that [X] by
  doing [Y] instead of [Z]." If the thesis is bland ("this project is well-structured"),
  dig deeper.

Capture the story angle in a single paragraph before writing. This paragraph is NOT
included in the output — it's the internal compass that keeps the article focused.

### Phase 3: Write the Article

Follow newspaper writing conventions. Consult `references/writing-guide.md` for detailed
style guidance and `references/article-structure.md` for structural templates.

#### Headline

- Short, active, specific
- Names the technology or domain
- Makes a claim or poses a tension
- Examples: "How One CLI Replaced a Team's Entire Deploy Pipeline" /
  "The Case for Throwing Away Your ORM" / "Building a Type-Safe API Without Code Generation"

#### Lead Paragraph

The first 2–3 sentences must hook the reader. State the core tension or insight
immediately. Do NOT open with "In this article, we will..." or "This project is a..."

Use one of these lead patterns:
- **Anecdotal:** Start with the pain point as a scene
- **Declarative:** State the thesis directly
- **Contrarian:** Challenge a common assumption

#### Body

Structure the body around the story, NOT around the codebase structure. Typical flow:

1. **The Problem** (1–2 paragraphs) — What was broken, slow, painful, or missing?
2. **The Approach** (2–3 paragraphs) — What decisions shaped the solution? Focus on the
   surprising or non-obvious ones. Include code snippets (real, from the codebase) where
   they illustrate a point — not as filler.
3. **The Interesting Bits** (2–3 paragraphs) — The technical meat. The clever abstraction,
   the performance trick, the elegant constraint. This is where developer readers get value.
4. **The Tradeoffs** (1–2 paragraphs) — What was sacrificed? What would change with more
   time? Honest reflection builds credibility.
5. **The Takeaway** (1 paragraph) — What generalizable lesson does this project teach?

#### Code Snippets

- Pull REAL code from the project — never fabricate examples
- Keep snippets short (10–25 lines). Trim imports and boilerplate
- Always introduce a snippet with context: what it does and why it matters
- Use the snippet to prove a claim, not to fill space

#### Closing

End with the takeaway, not a summary. No "in conclusion" or "to summarize." The last
sentence should land like the last line of a good article — something the reader remembers.

### Phase 4: Write to Disk

1. Create `docs/` directory if it doesn't exist
2. Write the article to `docs/paper.md`
3. Report the file path and a one-line summary of the angle taken

## Style Rules

- **Voice:** Third-person journalistic OR first-person dev narrative (infer from README tone).
  Default to third-person journalistic when the README tone is neutral or unclear.
- **Tone:** Confident, clear, technical but accessible. No jargon without context.
- **No fluff:** Every sentence must earn its place. Cut "it is worth noting that" and
  similar padding.
- **No AI tells:** Never write "delves into", "it's important to note", "in the
  ever-evolving landscape of." Write like a human journalist.
- **Technical precision:** Name technologies, patterns, and tradeoffs correctly. If
  referencing a library, name the version from the manifest.

## What NOT to Produce

- Architecture documentation disguised as an article
- A bullet-point feature list
- A tutorial or how-to guide
- A README rewrite
- Anything that opens with "In today's fast-paced world of software development..."

## Additional Resources

### Reference Files

For detailed guidance on writing craft and article structure, consult:

- **`references/writing-guide.md`** — Newspaper writing techniques: headline craft, lead
  patterns, inverted pyramid, weaving technical detail into narrative, tone calibration
- **`references/article-structure.md`** — Structural templates for different project types,
  section flow patterns, example outlines, and length guidance
