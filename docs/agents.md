# 🤖 Agents — Technical Reference

> Agents live in `agents/<name>.md`. Claude spawns them when a task matches their `description`. Each gets its own context window, tool set, and skill preloads.

---

## How Agents Work

```
User request -> Claude matches agent description -> Spawns agent
                                                      |
                                            Own context window
                                            Own tool set
                                            Preloaded skills
                                                      |
                                            Returns results
```

## Agent Frontmatter

```yaml
---
name: my-agent
description: "When to invoke..."
model: opus
color: cyan
tools: Read, Write, Edit, Glob, Grep, Bash
skills:
  - my-skill
---

System prompt defining agent personality.
```

---

## Primary Agents

### karpathy-engineer
🧭 cyan | opus | Tools: Read, Write, Edit, Glob, Grep, Bash | Skills: karpathy-guidelines

Disciplined implementer. 4 Karpathy principles + systematic debugging + defense-in-depth. Won't overcomplicate, won't assume, won't skip verification.

Stops and resets after 2+ failed fix attempts. Invokes test-driven-development, systematic-debugging, incremental-implementation, defense-in-depth, source-driven-development as needed.

### architecture-improver
🏗️ yellow | opus | Tools: Read, Glob, Grep, Bash, WebFetch, WebSearch, AskUserQuestion, Agent | Skills: improve-codebase-architecture

Explores codebases for architectural friction. Spawns 3+ parallel sub-agents for interface design. Files refactor RFCs as GitHub issues.

### synthesizer
🧬 cyan | opus | Tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, AskUserQuestion, Agent | Skills: synthesizer

6-phase deep codebase analysis. Dispatches parallel documenter agents. 10 Python validation scripts. Graded architecture reports (A-F).

### claude-md-improver
📐 green | opus | Tools: Read, Glob, Grep, Write, Edit, AskUserQuestion | Skills: improve-claude-md

Rewrites CLAUDE.md files with `<important if>` conditional blocks.

### refactor-planner
🔧 blue | opus | Tools: Read, Glob, Grep, Bash, AskUserQuestion | Skills: request-refactor-plan

Structured interview -> tiny-commit plan -> GitHub issue RFC. Martin Fowler's advice: smallest possible steps.

### obsidian
💎 purple | opus | Tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, WebSearch

Full Obsidian vault expert. CLI, REST API, Dataview, Templater, Tasks, CSS, PKM. Never edits workspace.json while running. Never renames with OS tools.

### presenter
📊 magenta | opus | Tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch, AskUserQuestion | Skills: marp-presentation | MCP: playwright

Marp slide decks. Design thinking, theme auto-selection, Playwright QA screenshots, multi-format export.

---

## Plugin Agents

### prd-writer
📋 blue | inherit | Tools: Glob, Grep, LS, Read, WebFetch, WebSearch, BashOutput

Researches codebase to draft technically grounded PRDs. Explores existing patterns, models, APIs, and integration points. Returns structured draft with codebase context, user stories, requirements, and open questions.

### prd-issue-breaker
🗂️ yellow | inherit | Tools: Glob, Grep, LS, Read, WebFetch, BashOutput

Breaks PRDs into thin vertical slices (tracer bullets). Each slice cuts through ALL integration layers end-to-end. Classifies as HITL (needs human input) or AFK (can be built independently). Returns dependency graph and implementation order.

### prd-planner
🗺️ green | inherit | Tools: Glob, Grep, LS, Read, WebFetch, BashOutput

Creates phased implementation plans from PRDs. Identifies durable architectural decisions (routes, schema, models) that apply across all phases. Designs tracer-bullet phases with acceptance criteria. Output feeds into `./plans/*.md` files.
