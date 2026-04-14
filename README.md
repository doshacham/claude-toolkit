# Claude Toolkit

> **23 skills · 15 commands · 7 agents · 4 plugins · 4 autonomous loops**
>
> A batteries-included toolkit for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — drop it into `~/.claude/` and get superpowers.

---

## What This Is

A personal collection of everything that makes Claude Code actually useful for real engineering work. Skills that auto-trigger when you need them. Slash commands for common workflows. Specialized agents that think before they code. Autonomous loops that build while you sleep.

**Not a framework.** Not a library. Just markdown files and Python scripts that Claude Code reads and follows. Copy what you want into `~/.claude/` and it works.

---

## 🚀 Quick Start

```bash
# clone it
git clone https://github.com/doshacham/claude-toolkit.git

# copy everything into your Claude Code config
cp -r claude-toolkit/skills/ ~/.claude/
cp -r claude-toolkit/commands/ ~/.claude/
cp -r claude-toolkit/agents/ ~/.claude/

# or cherry-pick what you need
cp -r claude-toolkit/skills/synthesizer/ ~/.claude/skills/
cp -r claude-toolkit/skills/karpathy-guidelines/ ~/.claude/skills/
```

No registration, no config files, no build step. Claude auto-discovers everything from `~/.claude/`.

---

## 🧠 Skills

Skills auto-trigger based on what you're doing — no slash command needed. Ask Claude to "debug this test failure" and the `systematic-debugging` skill kicks in automatically.

### 🔍 Debugging & Quality

| Skill | What It Does |
|-------|-------------|
| **systematic-debugging** | 4-phase root-cause investigation — no fixes without evidence first |
| **debugging-and-error-recovery** | Stop-the-line triage when builds break or tests fail |
| **defense-in-depth** | Multi-layer validation after bug fixes — make the bug *structurally impossible* |
| **code-review-and-quality** | Multi-axis code review (correctness, security, performance, maintainability) |

### 🏗️ Architecture & Design

| Skill | What It Does |
|-------|-------------|
| **improve-codebase-architecture** | Find shallow modules, design deep-module refactors, file GitHub RFCs |
| **design-an-interface** | Spawn 3+ parallel agents with radically different interface designs |
| **improve-claude-md** | Rewrite CLAUDE.md with `<important if>` conditional blocks |
| **context-engineering** | Optimize what context Claude loads — hierarchy, selective includes |

### 📋 Planning & Execution

| Skill | What It Does |
|-------|-------------|
| **planning-and-task-breakdown** | Break work into ordered tasks with acceptance criteria |
| **spec-driven-development** | Write a spec before coding — SPECIFY → PLAN → TASKS → IMPLEMENT |
| **incremental-implementation** | Deliver in thin vertical slices — implement, test, verify, commit |
| **source-driven-development** | Ground every decision in official docs — fetch, implement, cite |

### 🧪 Testing

| Skill | What It Does |
|-------|-------------|
| **test-driven-development** | Full TDD with red-green-refactor, prove-it pattern for bugs |
| **tdd** | Lightweight TDD — quick red-green-refactor invocation |

### 🔬 Analysis & Research

| Skill | What It Does |
|-------|-------------|
| **synthesizer** | 6-phase deep codebase analysis with parallel agents and quality scoring |
| **read-arxiv** | Download arxiv paper TeX sources → structured summary |
| **ingest** | LLM Wiki pattern — process raw sources into interlinked wiki pages |

### 🧭 Behavioral

| Skill | What It Does |
|-------|-------------|
| **karpathy-guidelines** | 4 principles: Think Before Coding, Simplicity First, Surgical Changes, Goal-Driven |
| **grill-me** | Relentless interview about your plan until every assumption is surfaced |
| **request-refactor-plan** | Interactive interview → tiny-commit plan → GitHub issue RFC |

### 🔧 Domain-Specific

| Skill | What It Does |
|-------|-------------|
| **obsidian** | Full Obsidian vault operations — CLI, Dataview, Templater, PKM workflows |
| **marp-presentation** | Slide decks with 15 themes, Playwright QA, multi-format export |
| **ci-cd-and-automation** | CI/CD pipeline setup — quality gates, test runners, deployment |

> 📖 **[Full skill documentation →](docs/skills.md)** — trigger phrases, internals, reference files, scripts

---

## ⌘ Commands

Slash commands you type directly. Each one wires into a skill.

| Command | What It Does |
|---------|-------------|
| `/karpathy` | Apply the 4 Karpathy principles to current work |
| `/debug` | Systematic root-cause debugging — investigate before fixing |
| `/debug-recover` | Stop-the-line error recovery — triage → reproduce → fix → guard |
| `/defense-in-depth` | Add validation at every layer after a bug fix |
| `/tdd` | Red → Green → Refactor development loop |
| `/spec` | Write a structured spec before coding |
| `/plan` | Break work into ordered tasks with acceptance criteria |
| `/incremental` | Build in thin vertical slices |
| `/improve-architecture` | Find deep-module refactoring opportunities |
| `/improve-claude-md` | Optimize a CLAUDE.md with conditional blocks |
| `/request-refactor-plan` | Interview → tiny-commit plan → GitHub issue |
| `/synthesize` | Deep 6-phase codebase analysis with quality scorecard |
| `/source-check` | Verify implementation against official documentation |
| `/ci-cd` | Set up or modify CI/CD pipelines |
| `/context` | Optimize agent context for better output quality |

> 📖 **[Full command reference →](docs/commands.md)**

---

## 🤖 Agents

Specialized sub-agents that Claude spawns for focused work. Each has its own tools, model, and personality.

| Agent | Purpose |
|-------|---------|
| 🟦 **karpathy-engineer** | Disciplined implementer — won't overcomplicate, won't assume, won't skip verification |
| 🟨 **architecture-improver** | Explore → surface friction → design interfaces → file GitHub RFC |
| 🟦 **synthesizer** | 6-phase codebase analysis with parallel documenter agents |
| 🟩 **claude-md-improver** | Rewrite CLAUDE.md with `<important if>` blocks |
| 🔵 **refactor-planner** | Structured interview → tiny-commit plan → GitHub issue |
| 🟣 **obsidian** | Full Obsidian vault expert — CLI, Dataview, Templater, PKM |
| 🟤 **presenter** | Marp slide decks with design thinking and Playwright QA |

> 📖 **[Full agent documentation →](docs/agents.md)** — tools, models, colors, skill preloads

---

## 🔌 Plugins

Self-contained packages with commands + skills + agents + scripts.

| Plugin | What It Does |
|--------|-------------|
| 📚 **learn** | Structured concept explanations — definition, analogy, examples, takeaways |
| 📰 **paper** | Generate newspaper-style dev-blog articles from any codebase |
| 🐛 **triagger** | Bug triage → root cause → TDD fix plan → GitHub issue |
| ✏️ **write-a-skill** | Interactive Claude Code skill creation wizard |

> 📖 **[Full plugin documentation →](docs/plugins.md)** — directory structures, components, usage

---

## 🔄 Autonomous Loops

Continuous bash loops that drive Claude through plan → build → test → commit cycles. Based on the [Ralph methodology](https://ghuntley.com/ralph/).

| Loop | What's Different |
|------|-----------------|
| 📘 **[how-to-ralph-wiggum](loops/how-to-ralph-wiggum/)** | The reference guide — start here |
| 🪟 **[ralph-loop](loops/ralph-loop/)** | Windows + Max plan — sentinel watcher, no API credits needed |
| 🔧 **[claude-loop](loops/claude-loop/)** | Extended — adds fix, audit, and specs interview modes |
| ⚡ **[ralph-wiggum-files](loops/ralph-wiggum-files/)** | Refined API-mode templates — Sonnet/Opus subagents, Ultrathink |

> 📖 **[Full loop documentation →](docs/loops.md)** — phases, file-based state, sentinel watcher

---

## 🛡️ Infrastructure

Hooks, scripts, and rules that run automatically.

| Component | What It Does |
|-----------|-------------|
| `hooks/guard-commit-attribution.sh` | Blocks AI attribution lines in git commits |
| `hooks/guard-agent-policy.sh` | Enforces agent spawning policies |
| `hooks/add-license-header.sh` | Auto-adds copyright headers to new files |
| `scripts/show-skills.sh` | Session startup banner — lists all available skills and commands |
| `status_lines/status_line.sh` | Status bar display script |
| `rules/license-header.md` | License header rule for new file creation |

---

## 📐 How It All Fits Together

```
              ┌─────────────────────────┐
              │      You type...        │
              │                         │
              │  "/debug this failure"  │
              │  "improve architecture" │
              │  "/synthesize repo"     │
              └───────────┬─────────────┘
                          │
                ┌─────────▼─────────┐
                │   Claude Code     │
                │   reads ~/.claude │
                └────┬─────────┬────┘
                     │         │
            ┌────────▼──┐  ┌───▼────────┐
            │  Command  │  │   Skill    │
            │  (manual) │  │  (auto)    │
            └────┬──────┘  └───┬────────┘
                 │             │
            ┌────▼─────────────▼────┐
            │       Agent           │
            │  (if complex work)    │
            │                       │
            │  Can spawn parallel   │
            │  sub-agents for       │
            │  interface design,    │
            │  codebase analysis,   │
            │  etc.                 │
            └────┬─────────────┬────┘
                 │             │
            ┌────▼─────┐ ┌────▼─────┐
            │ Scripts  │ │  Hooks   │
            │ (Python) │ │  (Bash)  │
            └──────────┘ └──────────┘
```

---

## 📁 Repository Structure

```
claude-toolkit/
├── skills/            # 23 auto-triggered skills
│   ├── synthesizer/   #   └── 10 Python scripts, XML template, references
│   ├── obsidian/      #   └── 15 reference docs, 10 templates
│   ├── marp-presentation/ # └── 15 themes, 14 scripts, 5 templates
│   └── ...            #   └── each has SKILL.md + optional refs
├── commands/          # 15 slash commands
├── agents/            # 7 specialized agents
├── plugins/           # 4 bundled plugins
│   ├── learn/         #   └── command + agent + skill + references
│   ├── paper/         #   └── command + skill + writing guides
│   ├── triagger/      #   └── command + agent + 5 bash scripts
│   └── write-a-skill/ #   └── interactive skill creation wizard
├── loops/             # 4 autonomous loop variants
├── hooks/             # 4 policy enforcement hooks
├── rules/             # 1 rule (license headers)
├── scripts/           # 1 session startup script
├── status_lines/      # 1 status bar script
└── docs/              # detailed technical documentation
    ├── skills.md
    ├── agents.md
    ├── commands.md
    ├── plugins.md
    └── loops.md
```

---

## 🗺️ "I want to..."

| I want to... | Use this |
|--------------|----------|
| Debug a bug properly | `/debug` or `systematic-debugging` skill |
| Plan a feature | `/plan` or `/spec` |
| Build with tests first | `/tdd` |
| Analyze a codebase deeply | `/synthesize` |
| Design a module interface | `design-an-interface` skill |
| Improve my architecture | `/improve-architecture` |
| Refactor safely | `/request-refactor-plan` |
| Make a presentation | `marp-presentation` skill |
| Work with Obsidian | `obsidian` skill |
| Code with discipline | `/karpathy` |
| Stress-test my design | `grill-me` skill |
| Run autonomous builds | See `loops/` directory |
| Create a new skill | `/write-a-skill` (plugin) |

---

## Author

**Dor Shacham** — [github.com/doshacham](https://github.com/doshacham)
