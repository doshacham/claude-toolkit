# 🔌 Plugins — Technical Reference

> Plugins are self-contained packages in `plugins/<name>/` bundling commands + skills + agents + scripts. Each has a `.claude-plugin/plugin.json` manifest.

---

## 📚 learn

Structured concept explanations: definition, analogy, core explanation, practical example, takeaways, related concepts.

**Components:** `/learn` command, `explainer` agent, `explanation-methodology` skill + `advanced-patterns.md` reference

Adapts by concept type: programming (code examples), comparisons (side-by-side tables), procedural (step-by-step), abstract (progressive analogies).

---

## 📰 paper

Newspaper-style dev-blog articles from any codebase. 1,500-3,000 words.

**Components:** `/paper` command, `paper` skill + `article-structure.md` (5 story templates) + `writing-guide.md` (journalism techniques)

Story templates: Tool Story, Abstraction Story, Architecture Story, Itch Story, Migration Story.

---

## 🐛 triagger

Bug triage to GitHub issue with TDD fix plan.

**Components:** `/triage-issue` command, `triagger` agent, 5 bash scripts (preflight, postflight, landing, doctor, validate-issue)

Workflow: preflight (check env) -> capture -> explore/diagnose -> TDD fix plan -> `gh issue create` -> postflight (validate issue quality) -> landing (summarize, cleanup)

---

## ✏️ write-a-skill

Interactive Claude Code skill creation wizard.

**Components:** `/write-a-skill` command

Process: interview -> draft SKILL.md + references + scripts -> review -> iterate.
