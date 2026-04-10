---
description: Execute a plan using agent teams orchestration
argument-hint: [path-to-plan]
---

# Build With Orchestration

Follow the `Workflow` to execute the `PATH_TO_PLAN` using agent teams orchestration, then `Report` the completed work.

## Variables

PATH_TO_PLAN: $ARGUMENTS

## Workflow

- If no `PATH_TO_PLAN` is provided, STOP immediately and ask the user to provide it (AskUserQuestion).
- Read the plan at `PATH_TO_PLAN`. Think hard about the plan and execute it using agent teams.
- Follow the Team Orchestration section in the plan to:
  1. **Create team** with `TeamCreate` using a descriptive team name
  2. **Create all tasks** with `TaskCreate` for each step, then set dependencies with `TaskUpdate` + `addBlockedBy`
  3. **Spawn ALL teammates** listed in the plan with `Agent` using `team_name` — pre-spawn everyone upfront since teammates cannot spawn their own workers
  4. **Assign tasks** to teammates with `TaskUpdate` + `owner`
  5. **Monitor progress** — messages from teammates arrive automatically, use `TaskList` to check status
  6. **Coordinate** with `SendMessage` when teammates need guidance, re-assignment, or unblocking
  7. **Shutdown all teammates** with `SendMessage` type `shutdown_request` when all tasks are complete

## Report

- Present the `## Report` section of the plan.
