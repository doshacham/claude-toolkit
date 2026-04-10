---
description: Creates a concise engineering implementation plan for agent teams orchestration and saves it to specs directory
argument-hint: [user prompt] [orchestration prompt]
model: opus
disallowed-tools: TeamCreate, SendMessage, EnterPlanMode
hooks:
  Stop:
    - hooks:
        - type: command
          command: >-
            uv run $HOME/.claude/hooks/validators/validate_new_file.py
            --directory specs
            --extension .md
        - type: command
          command: >-
            uv run $HOME/.claude/hooks/validators/validate_file_contains.py
            --directory specs
            --extension .md
            --contains '## Task Description'
            --contains '## Objective'
            --contains '## Relevant Files'
            --contains '## Step by Step Tasks'
            --contains '## Acceptance Criteria'
            --contains '## Team Orchestration'
            --contains '### Team Members'
---

# Plan For Orchestration

Create a detailed implementation plan based on the user's requirements provided through the `USER_PROMPT` variable. Analyze the request, think through the implementation approach, and save a comprehensive specification document to `PLAN_OUTPUT_DIRECTORY/<name-of-plan>.md` that can be used as a blueprint for agent teams orchestration.

## Variables

USER_PROMPT: $1
ORCHESTRATION_PROMPT: $2 - (Optional) Guidance for team assembly, task structure, and execution strategy
PLAN_OUTPUT_DIRECTORY: `specs/`
TEAM_MEMBERS: `.claude/agents/orch/*.md`
GENERAL_PURPOSE_AGENT: `general-purpose`

## Shared Reference

Read the shared plan format at `references/plan-format.md` for: Instructions, Task Management Tools, Task Dependencies, Owner Assignment, Workflow, and Plan Format template.

## Orchestration Tools (Orch-Specific)

### Team Creation with TeamCreate

**TeamCreate** - Create an agent team with a shared task list:
```typescript
TeamCreate({
  team_name: "feature-build",
  description: "Building feature X as specified in specs/feature-x.md"
})
// Creates: team config at ~/.claude/teams/feature-build.json
// Creates: shared task list at ~/.claude/tasks/feature-build/
```

### Spawning Teammates with Agent Tool

**Agent** - Spawn a teammate that joins the team:
```typescript
Agent({
  name: "builder-api",
  prompt: "You are a builder focused on API endpoints. Check TaskList for your assigned tasks and execute them.",
  subagent_type: "builder",  // from TEAM_MEMBERS or GENERAL_PURPOSE_AGENT
  team_name: "feature-build"  // joins the team created by TeamCreate
})
```

Key constraints and differences from subagents:
- Teammates have their OWN full context window and work independently
- Teammates can message each other directly (peer-to-peer via SendMessage)
- Teammates claim and complete tasks from the shared task list
- Teammates CANNOT spawn their own subagents or teams — all teammates must be pre-spawned by the lead
- Messages from teammates are delivered automatically — no need to poll

### Communication with SendMessage

**SendMessage (direct message)** - Send a message to a specific teammate:
```typescript
SendMessage({
  type: "message",
  recipient: "builder-api",
  content: "Task 1 is ready for you. Start with the database schema.",
  summary: "Task 1 assignment notification"
})
```

**SendMessage (broadcast)** - Send a message to ALL teammates (use sparingly — costs scale with team size):
```typescript
SendMessage({
  type: "broadcast",
  content: "Blocking issue found in shared config. Hold off on config changes.",
  summary: "Critical blocking issue found"
})
```

**SendMessage (shutdown)** - Request a teammate to gracefully shut down:
```typescript
SendMessage({
  type: "shutdown_request",
  recipient: "builder-api",
  content: "All tasks complete. Wrapping up the session."
})
```

### Teammate Idle State

Teammates go idle after every turn — this is normal. An idle teammate is simply waiting for input. Sending a message to an idle teammate wakes them up. Do not treat idle as an error or assume the teammate is done.

### Orchestration Workflow (Orch-Specific)

1. **Create team** with `TeamCreate` for the project
2. **Create tasks** with `TaskCreate` for each step in the plan
3. **Set dependencies** with `TaskUpdate` + `addBlockedBy`
4. **Spawn ALL teammates** with `Agent` + `team_name` (pre-spawn everyone upfront — they cannot spawn their own workers)
5. **Assign tasks** with `TaskUpdate` + `owner` to teammates
6. **Monitor progress** via automatic message delivery and `TaskList`
7. **Coordinate** with `SendMessage` when teammates need guidance or re-assignment
8. **Shutdown teammates** with `SendMessage` + `type: "shutdown_request"` when all work is done

## Team Orchestration Blurb (for Plan Format)

When writing the `## Team Orchestration` section in the plan, use this content:

- You operate as the team lead and orchestrate the team using **agent teams** to execute the plan.
- You are responsible for creating the team, spawning the right teammates, and coordinating via messaging.
- IMPORTANT: You NEVER operate directly on the codebase. You use `TeamCreate` to create the team, `Agent` with `team_name` to spawn teammates, `SendMessage` to coordinate, and `Task*` tools to manage the shared task list.
  - This is critical. Your job is to act as a high level director of the team, not a builder.
  - Your role is to validate all work is going well and make sure the team is on track to complete the plan.
  - You'll orchestrate by using the shared task list for coordination and `SendMessage` for direct communication with teammates.
  - Communication is paramount. Teammates can message each other directly, but you coordinate the overall effort.
  - Teammates CANNOT spawn subagents or other teams. All teammates must be pre-spawned by you.
- Take note of the name of each teammate. This is how you'll reference them via `SendMessage`.

### Team Members Template

```md
- Teammate
  - Name: <unique name for this teammate - used for SendMessage recipient and task owner>
  - Role: <the single role and focus this teammate will play>
  - Agent Type: <the subagent type, from TEAM_MEMBERS file or GENERAL_PURPOSE_AGENT>
- <continue with additional teammates as needed in the same format as above>
```

## Report

After creating and saving the implementation plan, provide a concise report with the following format:

```
Implementation Plan Created (Agent Teams)

File: PLAN_OUTPUT_DIRECTORY/<filename>.md
Topic: <brief description of what the plan covers>
Key Components:
- <main component 1>
- <main component 2>
- <main component 3>

Team Task List:
- <list of tasks, and owner (concise)>

Teammates:
- <list of teammates and their roles (concise)>

When you're ready, you can execute the plan in a new agent by running:
/build-with-orch <replace with path to plan>
```
