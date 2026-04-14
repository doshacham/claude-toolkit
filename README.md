<p align="center">
  <h1 align="center">🧰 Claude Toolkit</h1>
  <p align="center">
    <strong>Make Claude Code unreasonably good at engineering.</strong>
    <br />
    <em>23 skills · 15 commands · 7 agents · 4 plugins · 4 autonomous loops</em>
  </p>
  <p align="center">
    <a href="#-quick-start">Quick Start</a> · <a href="#-skills">Skills</a> · <a href="#-commands">Commands</a> · <a href="#-agents">Agents</a> · <a href="#-plugins">Plugins</a> · <a href="#-autonomous-loops">Loops</a> · <a href="docs/">Docs</a>
  </p>
</p>

---

Drop markdown files into `~/.claude/` and Claude Code gains superpowers. No build step. No config. No registration. It just works.

Skills auto-trigger when you need them. Agents think before they code. Loops build while you sleep.

```bash
git clone https://github.com/doshacham/claude-toolkit.git
cp -r claude-toolkit/{skills,commands,agents} ~/.claude/
```

That's it. Next time Claude Code starts, everything is live.

---

## 📑 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🧠 Skills](#-skills) — 23 auto-triggered capabilities
- [⌘ Commands](#-commands) — 15 slash commands
- [🤖 Agents](#-agents) — 7 specialized sub-agents
- [🔌 Plugins](#-plugins) — 4 bundled packages
- [🔄 Autonomous Loops](#-autonomous-loops) — build on autopilot
- [🛡️ Infrastructure](#️-infrastructure) — hooks, scripts, rules
- [📐 Architecture](#-architecture) — how it all connects
- [📁 Repo Structure](#-repo-structure)
- [🗺️ Cheat Sheet](#️-cheat-sheet)

---

## 🚀 Quick Start

**Everything:**

```bash
cp -r skills/ commands/ agents/ ~/.claude/
```

**Cherry-pick what you need:**

```bash
# just the Karpathy discipline skill
cp -r skills/karpathy-guidelines/ ~/.claude/skills/

# just the deep codebase analyzer
cp -r skills/synthesizer/ ~/.claude/skills/

# just the slash commands
cp -r commands/ ~/.claude/
```

Claude auto-discovers everything from `~/.claude/`. Zero configuration.

---

## 🧠 Skills

> Skills are the core of the toolkit. They auto-trigger based on what you're doing — you don't type a command, Claude just *knows* when to use them.
>
> Say *"debug this test failure"* and `systematic-debugging` activates. Say *"improve the architecture"* and `improve-codebase-architecture` kicks in.

### 🔍 Debugging & Quality

| Skill | What Happens |
|-------|-------------|
| 🔬 **[systematic-debugging](skills/systematic-debugging/)** | 4-phase root-cause investigation. No fixes until you have evidence. |
| 🩺 **[debugging-and-error-recovery](skills/debugging-and-error-recovery/)** | Stop-the-line triage — when builds break, this is your ER. |
| 🛡️ **[defense-in-depth](skills/defense-in-depth/)** | After fixing a bug: validate at 4 layers so it *can't come back*. |
| 🔍 **[code-review-and-quality](skills/code-review-and-quality/)** | Multi-axis review with security, performance, and accessibility checklists. |

### 🏗️ Architecture & Design

| Skill | What Happens |
|-------|-------------|
| 🏗️ **[improve-codebase-architecture](skills/improve-codebase-architecture/)** | Find shallow modules → design deep-module interfaces → file GitHub RFC. |
| 🎨 **[design-an-interface](skills/design-an-interface/)** | Spawn 3+ parallel agents, each with a *radically* different design. |
| 📐 **[improve-claude-md](skills/improve-claude-md/)** | Rewrite your CLAUDE.md so Claude actually follows the rules. |
| 🧠 **[context-engineering](skills/context-engineering/)** | When Claude's output quality drops, this fixes what context it loads. |

### 📋 Planning & Execution

| Skill | What Happens |
|-------|-------------|
| 📋 **[planning-and-task-breakdown](skills/planning-and-task-breakdown/)** | Big task? Break it into ordered tasks with acceptance criteria. |
| 📝 **[spec-driven-development](skills/spec-driven-development/)** | Spec first, code second. SPECIFY → PLAN → TASKS → IMPLEMENT. |
| 🧱 **[incremental-implementation](skills/incremental-implementation/)** | Thin vertical slices — implement, test, verify, commit. Repeat. |
| 📖 **[source-driven-development](skills/source-driven-development/)** | Every decision grounded in official docs. No guessing at APIs. |

### 🧪 Testing

| Skill | What Happens |
|-------|-------------|
| 🧪 **[test-driven-development](skills/test-driven-development/)** | Full TDD — red/green/refactor + prove-it pattern for bugs. |
| 🧪 **[tdd](skills/tdd/)** | Quick lightweight TDD invocation. |

### 🔬 Analysis & Research

| Skill | What Happens |
|-------|-------------|
| 🧬 **[synthesizer](skills/synthesizer/)** | 6-phase deep codebase analysis. 10 Python scripts. Parallel agents. Quality grade A-F. |
| 📄 **[read-arxiv](skills/read-arxiv/)** | Paste an arxiv link → get a structured summary from the TeX source. |
| 📥 **[ingest](skills/ingest/)** | Karpathy's LLM Wiki pattern — raw sources → interlinked wiki pages. |

### 🧭 Behavioral

| Skill | What Happens |
|-------|-------------|
| 🧭 **[karpathy-guidelines](skills/karpathy-guidelines/)** | Think Before Coding · Simplicity First · Surgical Changes · Goal-Driven. |
| 🔥 **[grill-me](skills/grill-me/)** | Ruthless interview about your plan until every assumption is exposed. |
| 🔧 **[request-refactor-plan](skills/request-refactor-plan/)** | Interview → tiny-commit plan → GitHub issue RFC. |

### 💎 Domain-Specific

| Skill | What Happens |
|-------|-------------|
| 💎 **[obsidian](skills/obsidian/)** | Full Obsidian mastery — CLI, Dataview, Templater, 15 reference docs, 10 templates. |
| 📊 **[marp-presentation](skills/marp-presentation/)** | Slide decks with 15 themes, 14 scripts, Playwright QA verification. |
| 🔄 **[ci-cd-and-automation](skills/ci-cd-and-automation/)** | CI/CD pipelines — quality gates, test runners, deployment strategies. |

> 📖 **Deep dive →** [docs/skills.md](docs/skills.md) — trigger phrases, internals, reference files, every script documented.

---

## ⌘ Commands

> Type `/command-name` and go. Each command wires into a skill and passes your arguments through.

| Command | What It Does |
|---------|-------------|
| 🧭 `/karpathy` | Apply the 4 Karpathy principles |
| 🔍 `/debug` | Investigate before fixing — 4-phase root-cause debugging |
| 🩺 `/debug-recover` | Stop-the-line error recovery |
| 🛡️ `/defense-in-depth` | Validate at every layer after a bug fix |
| 🧪 `/tdd` | Red → Green → Refactor |
| 📝 `/spec` | Write a spec before coding |
| 📋 `/plan` | Break work into ordered tasks |
| 🧱 `/incremental` | Build in thin vertical slices |
| 🏗️ `/improve-architecture` | Find deep-module refactoring opportunities |
| 📐 `/improve-claude-md` | Optimize your CLAUDE.md |
| 🔧 `/request-refactor-plan` | Interview → tiny commits → GitHub issue |
| 🧬 `/synthesize` | Deep 6-phase codebase analysis |
| 📖 `/source-check` | Verify against official docs |
| 🔄 `/ci-cd` | Set up CI/CD pipelines |
| 🧠 `/context` | Optimize agent context |

> 📖 **Deep dive →** [docs/commands.md](docs/commands.md)

---

## 🤖 Agents

> Agents are like coworkers Claude can call in. Each one has its own personality, tool set, and area of expertise.

| Agent | What It Does |
|-------|-------------|
| 🟦 **karpathy-engineer** | The disciplined one — won't overcomplicate, won't assume, won't skip verification. |
| 🟨 **architecture-improver** | Explores your codebase, surfaces friction, designs interfaces, files GitHub RFCs. |
| 🟦 **synthesizer** | Dispatches parallel documenter agents, runs validation scripts, grades your codebase A-F. |
| 🟩 **claude-md-improver** | Makes your CLAUDE.md actually work with `<important if>` conditional blocks. |
| 🔵 **refactor-planner** | Interviews you, explores the code, produces a tiny-commit plan as a GitHub issue. |
| 🟣 **obsidian** | The Obsidian vault expert — CLI, Dataview, Templater, PKM, everything. |
| 🟤 **presenter** | Creates Marp slide decks, picks themes, runs Playwright QA on every slide. |

> 📖 **Deep dive →** [docs/agents.md](docs/agents.md) — tools, models, skill preloads, behaviors.

---

## 🔌 Plugins

> Self-contained packages that bundle commands + skills + agents + scripts together.

| Plugin | What It Does |
|--------|-------------|
| 📚 **[learn](plugins/learn/)** | Explain any concept — definition, analogy, examples, takeaways. Adapts to your level. |
| 📰 **[paper](plugins/paper/)** | Turn any codebase into a newspaper-style dev-blog article. 1,500-3,000 words. |
| 🐛 **[triagger](plugins/triagger/)** | Bug report → root cause → TDD fix plan → GitHub issue. Fully autonomous. |
| ✏️ **[write-a-skill](plugins/write-a-skill/)** | Interactive wizard for creating new Claude Code skills from scratch. |

> 📖 **Deep dive →** [docs/plugins.md](docs/plugins.md)

---

## 🔄 Autonomous Loops

> Based on the [Ralph methodology](https://ghuntley.com/ralph/). Bash loops that drive Claude through plan → build → test → commit cycles. Each iteration starts with a fresh context — `IMPLEMENTATION_PLAN.md` is the shared memory.

| Loop | Best For |
|------|---------|
| 📘 **[how-to-ralph-wiggum](loops/how-to-ralph-wiggum/)** | Learning the methodology — start here |
| 🪟 **[ralph-loop](loops/ralph-loop/)** | Windows + Max plan — no API credits needed |
| 🔧 **[claude-loop](loops/claude-loop/)** | Power users — adds fix, audit, and specs modes |
| ⚡ **[ralph-wiggum-files](loops/ralph-wiggum-files/)** | API mode — Sonnet reads, Opus reasons, Ultrathink plans |

**The three phases:**

```
📋 Phase 1: Specs     →  Interview you about requirements
📝 Phase 2: Plan      →  Generate IMPLEMENTATION_PLAN.md from gap analysis
🔨 Phase 3: Build     →  Pick task → TDD → commit → push → repeat
```

> 📖 **Deep dive →** [docs/loops.md](docs/loops.md) — phases, file-based state, sentinel watcher.

---

## 🛡️ Infrastructure

| Component | What It Does |
|-----------|-------------|
| 🚫 [`hooks/guard-commit-attribution.sh`](hooks/guard-commit-attribution.sh) | Blocks AI attribution lines in commits |
| 🔒 [`hooks/guard-agent-policy.sh`](hooks/guard-agent-policy.sh) | Enforces agent spawning policies |
| 📄 [`hooks/add-license-header.sh`](hooks/add-license-header.sh) | Auto-adds copyright headers to new files |
| ✨ [`scripts/show-skills.sh`](scripts/show-skills.sh) | Session startup banner — your toolkit at a glance |
| 📊 [`status_lines/status_line.sh`](status_lines/status_line.sh) | Status bar display |
| 📜 [`rules/license-header.md`](rules/license-header.md) | License header rule |

---

## 📐 Architecture

> How the pieces connect when you type something in Claude Code.

```
                  ┌─────────────────────────────┐
                  │        You type...          │
                  │                             │
                  │   "/debug this failure"     │
                  │   "improve architecture"    │
                  │   "/synthesize my-repo"     │
                  └──────────────┬──────────────┘
                                 │
                  ┌──────────────▼──────────────┐
                  │        Claude Code          │
                  │     reads ~/.claude/        │
                  └──────┬──────────────┬───────┘
                         │              │
               ┌─────────▼───┐   ┌──────▼─────────┐
               │  ⌘ Command  │   │  🧠 Skill      │
               │   (manual)  │   │   (auto)       │
               └─────┬───────┘   └──────┬─────────┘
                     │                  │
               ┌─────▼──────────────────▼──────┐
               │         🤖 Agent              │
               │    (spawned if needed)        │
               │                               │
               │    Can launch parallel        │
               │    sub-agents for interface   │
               │    design, codebase analysis  │
               └─────┬────────────────┬────────┘
                     │                │
               ┌─────▼─────┐   ┌─────▼─────┐
               │ 🐍 Scripts │   │ 🛡️ Hooks  │
               │  (Python)  │   │  (Bash)   │
               └────────────┘   └───────────┘
```

---

## 📁 Repo Structure

```
claude-toolkit/
│
├── 🧠 skills/               23 auto-triggered skills
│   ├── synthesizer/          ├── 10 Python scripts + XML template
│   ├── obsidian/             ├── 15 reference docs + 10 templates
│   ├── marp-presentation/    ├── 15 themes + 14 scripts + 5 templates
│   ├── karpathy-guidelines/  ├── the 4 principles
│   └── ...                   └── each has SKILL.md + optional refs
│
├── ⌘ commands/               15 slash commands
├── 🤖 agents/                7 specialized agents
│
├── 🔌 plugins/               4 self-contained packages
│   ├── learn/                ├── concept explainer
│   ├── paper/                ├── dev-blog generator
│   ├── triagger/             ├── bug triage → GitHub issue
│   └── write-a-skill/        └── skill creation wizard
│
├── 🔄 loops/                 4 autonomous loop variants
│   ├── how-to-ralph-wiggum/  ├── the reference guide
│   ├── ralph-loop/           ├── Windows + Max plan
│   ├── claude-loop/          ├── extended (fix/audit modes)
│   └── ralph-wiggum-files/   └── API mode templates
│
├── 🛡️ hooks/                 4 policy hooks
├── 📜 rules/                 1 rule
├── ✨ scripts/               1 session startup script
├── 📊 status_lines/          1 status bar script
│
├── 📖 docs/                  technical reference
│   ├── skills.md
│   ├── agents.md
│   ├── commands.md
│   ├── plugins.md
│   └── loops.md
│
└── 📋 llms.txt               LLM-friendly description
```

---

## 🗺️ Cheat Sheet

> *"I want to..."*

| Goal | What to use |
|------|------------|
| 🐛 Debug a bug properly | `/debug` or say *"debug this"* |
| 📋 Plan a feature | `/plan` or `/spec` |
| 🧪 Build with tests first | `/tdd` |
| 🔬 Analyze a codebase deeply | `/synthesize` |
| 🎨 Design a module interface | Say *"design an interface for..."* |
| 🏗️ Improve architecture | `/improve-architecture` |
| 🔧 Refactor safely | `/request-refactor-plan` |
| 📊 Make a presentation | Say *"create a slide deck"* |
| 💎 Work with Obsidian vaults | Say *"Obsidian..."* |
| 🧭 Code with Karpathy discipline | `/karpathy` |
| 🔥 Stress-test my design | Say *"grill me"* |
| 🔄 Run autonomous builds | Check out `loops/` |
| ✏️ Create a new skill | `/write-a-skill` |
| 📚 Explain a concept | `/learn` (plugin) |
| 📰 Write a dev-blog article | `/paper` (plugin) |

---

<p align="center">
  <strong>Built by <a href="https://github.com/doshacham">Dor Shacham</a></strong> — making Claude Code unreasonably effective, one skill at a time.
</p>
