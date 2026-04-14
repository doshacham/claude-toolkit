# 🔄 Autonomous Loops — Technical Reference

> Bash scripts that run Claude in continuous cycles. Each iteration starts with a fresh context. Only the filesystem persists between iterations.

---

## How Loops Work

```
loop-build.sh
  |
  while true; do
  |   claude -p PROMPT_build.md
  |     |
  |     Reads IMPLEMENTATION_PLAN.md
  |     Picks next unchecked task
  |     Implements with TDD
  |     Commits + pushes
  |     Checks off task
  |     Exits
  |     |
  |   Loop restarts (fresh context)
  done
```

**Key insight:** `IMPLEMENTATION_PLAN.md` is the shared memory. Claude reads it, picks work, does work, updates it, exits.

---

## Three Phases

| Phase | Script | What Happens | Output |
|-------|--------|-------------|--------|
| 1. Specs | `loop-specs.sh` | Interactive interview (runs once) | `AUDIENCE_JTBD.md` + `specs/*.md` |
| 2. Plan | `loop-plan.sh` | Gap analysis: specs vs code (loops) | `IMPLEMENTATION_PLAN.md` |
| 3. Build | `loop-build.sh` | Pick task, TDD, commit, push (loops) | Checked-off tasks in plan |

---

## Variants

### 📘 how-to-ralph-wiggum
ClaytonFarr's reference guide. Start here. Full playbook with phases, principles, mechanics.

### 🪟 ralph-loop
Windows + Max plan. Sentinel file + PowerShell watcher instead of `-p` API flag. No API credits needed.

### 🔧 claude-loop
Extended variant. Adds fix mode, audit mode, specs interview, fix-plan mode.

### ⚡ ralph-wiggum-files
Refined API-mode templates. Up to 500 Sonnet subagents for reads. Opus for reasoning. Ultrathink for specs fixes.

---

## File-Based State

| File | Purpose | Changes When |
|------|---------|-------------|
| `IMPLEMENTATION_PLAN.md` | Checkboxed task list | Every build iteration |
| `AGENTS.md` | Build/validation commands | Set during Phase 1 |
| `AUDIENCE_JTBD.md` | Audience and jobs-to-be-done | Created in Phase 1 |
| `specs/*.md` | Feature specifications | Created in Phase 1 |
| `PROMPT_*.md` | System prompts | Static |
