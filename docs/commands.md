# ⌘ Commands — Technical Reference

> Commands live in `commands/<name>.md`. Invoked via `/command-name [arguments]`. Each wires into a skill.

---

## Command Anatomy

```yaml
---
description: What this does (shown in autocomplete)
argument-hint: [optional placeholder]
---

Instructions. Usually: "Use the X skill to..."
$ARGUMENTS captures user input after the command name.
```

---

## All Commands

| Command | Skill | Args | What It Does |
|---------|-------|------|-------------|
| `/karpathy` | karpathy-guidelines | — | Apply the 4 Karpathy principles |
| `/debug` | systematic-debugging | `[bug]` | 4-phase root-cause debugging |
| `/debug-recover` | debugging-and-error-recovery | `[error]` | Stop-the-line triage and recovery |
| `/defense-in-depth` | defense-in-depth | `[fixed bug]` | Multi-layer validation |
| `/tdd` | test-driven-development | `[task]` | Red, Green, Refactor |
| `/spec` | spec-driven-development | `[feature]` | Spec before coding |
| `/plan` | planning-and-task-breakdown | `[requirements]` | Ordered tasks + acceptance criteria |
| `/incremental` | incremental-implementation | `[feature]` | Thin vertical slices |
| `/improve-architecture` | improve-codebase-architecture | — | Deep-module refactoring |
| `/improve-claude-md` | improve-claude-md | — | Conditional `<important if>` blocks |
| `/request-refactor-plan` | request-refactor-plan | — | Interview, plan, GitHub issue |
| `/synthesize` | synthesizer | `[target]` | 6-phase codebase analysis |
| `/source-check` | source-driven-development | `[framework]` | Verify against official docs |
| `/ci-cd` | ci-cd-and-automation | `[target]` | CI/CD pipeline setup |
| `/context` | context-engineering | `[target]` | Optimize agent context |
| `/write-a-prd` | write-a-prd | — | Interview → PRD → GitHub issue |
| `/prd-to-issues` | prd-to-issues | `[issue #]` | PRD → vertical-slice GitHub issues |
| `/prd-to-plan` | prd-to-plan | `[PRD ref]` | PRD → phased plan in `./plans/` |
