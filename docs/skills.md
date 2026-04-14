# 🧠 Skills — Technical Reference

> Skills are markdown files in `skills/<name>/SKILL.md` that auto-trigger when their `description` matches the user's request.

---

## How Skills Work

```
User: "debug this test failure"
         |
Claude scans all skill descriptions
         |
Matches: "Use when encountering any bug, test failure..."
         |
Loads: skills/systematic-debugging/SKILL.md
         |
Follows the skill instructions
```

## Skill Anatomy

```yaml
---
name: my-skill
description: What this does...    # Claude matches against this
allowed-tools: Read Grep Bash     # optional tool restrictions
---

Instructions Claude follows when the skill is active.
```

---

## 🔍 Debugging & Quality

### systematic-debugging
**Triggers:** bug, test failure, unexpected behavior

Iron law: **no fixes without root cause investigation first.**

| Phase | What Happens |
|-------|-------------|
| 1. Root Cause Investigation | Full stack traces, reproduce, trace data flow backward |
| 2. Pattern Analysis | Find working examples, compare, list every difference |
| 3. Hypothesis & Testing | "I think X because Y", smallest change, one variable at a time |
| 4. Implementation | Failing test FIRST, single fix, verify, guard with regression test |

Red flags (restart Phase 1): "Quick fix for now" / "Just try X" / 2+ failed attempts

### debugging-and-error-recovery
**Triggers:** tests fail, builds break

Stop-the-line: triage, reproduce, localize, reduce, fix, guard.

### defense-in-depth
**Triggers:** after fixing data bugs

4 validation layers: Entry Point, Business Logic, Environment Guards, Debug Instrumentation.

### code-review-and-quality
**Triggers:** before merging, review code

Multi-axis review with checklists: `security-checklist.md`, `performance-checklist.md`, `testing-patterns.md`, `accessibility-checklist.md`

---

## 🏗️ Architecture & Design

### improve-codebase-architecture
**Triggers:** improve architecture, refactoring opportunities

Based on Ousterhout. Explore organically, present candidates, spawn 3+ parallel sub-agents for interface design, file GitHub RFC.

**Files:** `REFERENCE.md` (dependency categories, testing strategy, issue template)

### design-an-interface
**Triggers:** design an API, "design it twice"

3+ parallel agents with different constraints. Compare on simplicity, depth, efficiency.

### improve-claude-md
**Triggers:** "improve my CLAUDE.md", "Claude keeps ignoring rules"

Rewrite with `<important if>` blocks. Foundational context bare, domain guidance wrapped.

### context-engineering
**Triggers:** output quality degrading, switching tasks

Optimize loaded context: hierarchy, selective includes, confusion management.

---

## 📋 Planning & Execution

| Skill | What It Does |
|-------|-------------|
| **planning-and-task-breakdown** | Ordered tasks + acceptance criteria + parallelization |
| **spec-driven-development** | SPECIFY, PLAN, TASKS, IMPLEMENT |
| **incremental-implementation** | Thin vertical slices: implement, test, verify, commit |
| **source-driven-development** | Detect stack, fetch docs, implement, cite sources |

---

## 🧪 Testing

| Skill | What It Does |
|-------|-------------|
| **test-driven-development** | Full TDD + prove-it pattern. Ref: `testing-patterns.md` |
| **tdd** | Lightweight TDD. Refs: `deep-modules.md`, `mocking.md`, `refactoring.md`, `tests.md` |

---

## 🔬 Analysis & Research

### synthesizer
**Triggers:** "synthesize", "analyze codebase deeply"

6-phase analysis inspired by InfoSeek (arXiv:2509.00375):

```
RECON -> DEEP-DIVE -> REFINE -> SYNTHESIZE -> VALIDATE -> REPORT
```

10 Python scripts in `scripts/`. Quality scoring: Coverage 30% + Completeness 30% + Consistency 40%. Grades A-F.

Refs: `infoseek-mapping.md`, `agent-dump.xml` template.

### read-arxiv
**Triggers:** arxiv URL. Downloads TeX sources, produces structured summary.

### ingest
**Triggers:** "ingest", "process raw". LLM Wiki pattern: raw sources to interlinked wiki pages.

---

## 🧭 Behavioral

### karpathy-guidelines
**Triggers:** writing/reviewing/refactoring code

4 Karpathy principles: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven Execution.

### grill-me
**Triggers:** stress-test a plan, "grill me"

Relentless interview walking every branch of the decision tree.

### request-refactor-plan
**Triggers:** plan a refactor, refactoring RFC

8-step process: problem, explore repo, alternatives, interview, scope, test coverage, tiny commits, GitHub issue.

---

## 🔧 Domain-Specific

### obsidian
**Triggers:** Obsidian, vault, notes, Dataview, Templater, PKM

15 reference docs, 10 templates. Covers CLI, REST API, Dataview, Templater, Tasks, Canvas, CSS, plugins, PKM workflows.

### marp-presentation
**Triggers:** presentation, slide deck, talk, pitch

15 CSS themes, 5 templates, 14 Python scripts, 6 reference docs, Playwright QA loop.

### ci-cd-and-automation
**Triggers:** CI/CD setup, quality gates, deployment strategies.
