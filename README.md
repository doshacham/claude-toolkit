# Claude Toolkit

A personal collection of Claude Code slash commands, skills, and plugins for software engineering workflows. Covers everything from systematic debugging to PRD breakdowns, codebase synthesis, dev-blog generation, and team orchestration.

## Repository Structure

```
claude-toolkit/
├── commands/          # Slash commands (invoked via /command-name)
│   └── references/    # Shared reference docs used by commands
├── skills/            # Skills (auto-loaded by matching description triggers)
│   ├── systematic-debugging/
│   ├── clean-coder/
│   ├── design-an-interface/
│   ├── github-setup/
│   ├── improve-claude-md/
│   ├── improve-codebase-architecture/
│   ├── learn-gh-repo/
│   ├── prd-to-issues/
│   ├── prd-to-plan/
│   ├── read-article/
│   ├── request-refactor-plan/
│   └── synthesizer/
└── plugins/           # Full plugins (commands + skills + agents + scripts)
    ├── learn/
    ├── paper/
    ├── triagger/
    └── write-a-skill/
```

---

## Commands

Slash commands are invoked directly in Claude Code via `/command-name [arguments]`.

| Command | File | Description | Arguments |
|---|---|---|---|
| `/build` | [`commands/build.md`](commands/build.md) | Implement a plan file into the codebase | `[path-to-plan]` |
| `/build-with-orch` | [`commands/build-with-orch.md`](commands/build-with-orch.md) | Execute a plan using agent teams orchestration (TeamCreate, SendMessage, Agent) | `[path-to-plan]` |
| `/clean-coder` | [`commands/clean-coder.md`](commands/clean-coder.md) | Invoke the clean coder skill for professional, principled coding assistance | — |
| `/design-interface` | [`commands/design-interface.md`](commands/design-interface.md) | Generate multiple radically different interface designs for a module | `[module or component]` |
| `/gh-setup` | [`commands/gh-setup.md`](commands/gh-setup.md) | Set up and configure a GitHub repository from A-Z (secrets, CI, Dependabot, Claude integration, branch protection) | `[repo name or path]` |
| `/grill-me` | [`commands/grill-me.md`](commands/grill-me.md) | Interview the user relentlessly about a plan or design until reaching shared understanding | — |
| `/improve-architecture` | [`commands/improve-architecture.md`](commands/improve-architecture.md) | Find architectural improvement opportunities and propose deep-module refactors | — |
| `/improve-claude-md` | [`commands/improve-claude-md.md`](commands/improve-claude-md.md) | Improve a CLAUDE.md file using `<important if>` conditional blocks for better instruction adherence | — |
| `/learn-repo` | [`commands/learn-repo.md`](commands/learn-repo.md) | Learn and analyze a GitHub repository's architecture, produce a report | `<github-url>` (required) |
| `/plan-for-orch` | [`commands/plan-for-orch.md`](commands/plan-for-orch.md) | Create a detailed implementation plan for agent teams orchestration (TeamCreate + Agent + SendMessage) | `[user prompt] [orchestration prompt]` |
| `/plan-w-team` | [`commands/plan-w-team.md`](commands/plan-w-team.md) | Create a detailed implementation plan for team-based execution (Task tool + resume pattern) | `[user prompt] [orchestration prompt]` |
| `/prd-to-issues` | [`commands/prd-to-issues.md`](commands/prd-to-issues.md) | Break a PRD into GitHub issues using vertical slices | `<issue number or URL>` (required) |
| `/prd-to-plan` | [`commands/prd-to-plan.md`](commands/prd-to-plan.md) | Turn a PRD into a phased implementation plan using vertical slices | — |
| `/ralph-issues-build` | [`commands/ralph-issues-build.md`](commands/ralph-issues-build.md) | Autonomous issue-driven builder: picks next task from GitHub issues, implements with TDD, commits, and closes | — |
| `/read-article` | [`commands/read-article.md`](commands/read-article.md) | Read a web article or paper and produce a project-aware or standalone summary | `<url>` (required) |
| `/request-refactor-plan` | [`commands/request-refactor-plan.md`](commands/request-refactor-plan.md) | Create a detailed refactor plan with tiny commits via user interview, file as GitHub issue | — |
| `/synthesize` | [`commands/synthesize.md`](commands/synthesize.md) | Deep codebase analysis and synthesis producing exhaustive architecture reports | `[target]` |
| `/tdd` | [`commands/tdd-skill.md`](commands/tdd-skill.md) | TDD development process: red-green-refactor loop for building applications iteratively | `[project-name-or-path]` |
| `/write-a-prd` | [`commands/write-a-prd.md`](commands/write-a-prd.md) | Create a PRD through user interview and submit as a GitHub issue | — |

### Command References

| File | Used By | Purpose |
|---|---|---|
| [`commands/references/plan-format.md`](commands/references/plan-format.md) | `/plan-for-orch`, `/plan-w-team` | Shared plan format template, task management tools, dependency patterns, and workflow instructions |

---

## Skills

Skills are auto-loaded when their description triggers match the user's request. Each skill lives in its own directory with a `SKILL.md` and optional reference/script files.

| Skill | Directory | Trigger Phrases | What It Does |
|---|---|---|---|
| **Systematic Debugging** | [`skills/systematic-debugging/`](skills/systematic-debugging/) | Bug, test failure, unexpected behavior, "before proposing fixes" | Four-phase debugging process: Root Cause Investigation → Pattern Analysis → Hypothesis Testing → Implementation. Enforces "no fixes without root cause" iron law. |
| **Clean Coder** | [`skills/clean-coder/`](skills/clean-coder/) | "Be more careful", "slow down", "stop guessing", frustration with quality | Professional conduct principles using `<important if>` blocks: say no when appropriate, surface mistakes early, prefer correctness over speed, pause when thrashing. |
| **Design an Interface** | [`skills/design-an-interface/`](skills/design-an-interface/) | "Design an API", "explore interface options", "design it twice" | Generates 3+ radically different interface designs via parallel sub-agents, then compares on simplicity, depth, efficiency, and ease of correct use. Based on Ousterhout's "Design It Twice". |
| **GitHub Setup** | [`skills/github-setup/`](skills/github-setup/) | "Set up my GitHub repo", "configure GitHub", "add Dependabot", "harden CI" | A-Z GitHub repository setup: secrets, CI workflows (hardened with SHA pinning), Dependabot, auto-merge, Claude integration, security scanning, branch protection. |
| **Improve CLAUDE.md** | [`skills/improve-claude-md/`](skills/improve-claude-md/) | "Improve my CLAUDE.md", "Claude keeps ignoring my rules" | Rewrites CLAUDE.md files using `<important if="condition">` conditional blocks. Splits broad rules into targeted triggers, removes linter territory, keeps commands intact. |
| **Improve Codebase Architecture** | [`skills/improve-codebase-architecture/`](skills/improve-codebase-architecture/) | "Improve architecture", "find refactoring opportunities", "make codebase more AI-navigable" | Explores codebase for architectural friction, identifies shallow/coupled modules, designs multiple deepening interfaces via parallel sub-agents, files refactor RFC as GitHub issue. |
| **Learn GitHub Repo** | [`skills/learn-gh-repo/`](skills/learn-gh-repo/) | "Learn this repo", "study this codebase", "analyze this GitHub project" | Clones and deeply analyzes a GitHub repo: structure, entry points, core abstractions, data flow, design patterns. Produces a `knowledge/summary_*.md` report (project-aware or standalone). |
| **PRD to Issues** | [`skills/prd-to-issues/`](skills/prd-to-issues/) | "Convert PRD to issues", "create implementation tickets", "break down PRD" | Breaks a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices. Each issue is HITL or AFK, with dependency tracking and acceptance criteria. |
| **PRD to Plan** | [`skills/prd-to-plan/`](skills/prd-to-plan/) | "Break down PRD", "implementation plan", "tracer bullets", "vertical slices" | Turns a PRD into a phased implementation plan saved as `./plans/*.md`. Identifies durable architectural decisions, quizzes user on granularity, outputs phase-by-phase acceptance criteria. |
| **Read Article** | [`skills/read-article/`](skills/read-article/) | "Read this article", "summarize this blog post", "what does this page say" | Fetches and summarizes web articles/papers from a URL. Handles PDFs, multi-page articles, login walls. Produces `knowledge/summary_*.md` (project-aware or standalone). |
| **Request Refactor Plan** | [`skills/request-refactor-plan/`](skills/request-refactor-plan/) | "Plan a refactor", "create a refactoring RFC", "break refactor into steps" | Interactive refactor planning: interviews user about the problem, explores codebase, examines test coverage, breaks into tiny commits (Martin Fowler style), files as GitHub issue. |
| **Synthesizer** | [`skills/synthesizer/`](skills/synthesizer/) | "Synthesize", "analyze codebase deeply", "create architecture report" | Six-phase deep codebase analysis inspired by InfoSeek (arXiv:2509.00375). RECON → DEEP-DIVE → REFINE → SYNTHESIZE → VALIDATE → REPORT. Uses parallel documenter agents, deterministic validation scripts, and produces graded architecture reports. |

### Skill Reference Files

| File | Parent Skill | Purpose |
|---|---|---|
| [`skills/systematic-debugging/root-cause-tracing.md`](skills/systematic-debugging/root-cause-tracing.md) | Systematic Debugging | Backward call-chain tracing technique: observe symptom → find immediate cause → trace up → fix at source. Includes stack trace instrumentation and test pollution bisection. |
| [`skills/github-setup/references/config-reference.md`](skills/github-setup/references/config-reference.md) | GitHub Setup | Detailed config reference for secrets, Actions security, Dependabot YAML, auto-merge workflows, Claude integration, scanning, auth token types, branch protection, and free-tier boundaries. |
| [`skills/improve-codebase-architecture/REFERENCE.md`](skills/improve-codebase-architecture/REFERENCE.md) | Improve Codebase Architecture | Dependency categories (in-process, local-substitutable, ports & adapters, true external), testing strategy ("replace, don't layer"), and GitHub issue template for refactor RFCs. |
| [`skills/synthesizer/references/infoseek-mapping.md`](skills/synthesizer/references/infoseek-mapping.md) | Synthesizer | Concept mapping from InfoSeek paper to Synthesizer implementation. Quality score design rationale (coverage 30%, completeness 30%, consistency 40%). |
| [`skills/synthesizer/templates/agent-dump.xml`](skills/synthesizer/templates/agent-dump.xml) | Synthesizer | XML template for deep-dive agent output: `<think>`, `<types>`, `<functions>`, `<constants>`, `<sql-queries>`, `<information>`, `<data-flows>`, `<design-patterns>`, `<borrowable-ideas>`. |

### Synthesizer Scripts

All scripts live in [`skills/synthesizer/scripts/`](skills/synthesizer/scripts/) and form the deterministic validation pipeline.

| Script | Phase | What It Does |
|---|---|---|
| `detect_project.py` | 1 (RECON) | Detects project language, manifest, entry points, and source directories. Supports Go, Python, TS/JS, Rust, Java, C#, Ruby, PHP. |
| `build_exploration_tree.py` | 1 (RECON) | Builds an exploration tree from the import/dependency graph (not directory layout). Language-specific parsers for Go, Python, TS/JS, Rust. Falls back to directory-based tree. |
| `plan_dispatch.py` | 1 (RECON) | Partitions exploration tree into balanced agent assignments. Optimizes for balanced complexity, package cohesion, and full coverage. |
| `validate_dumps.py` | 3 (REFINE) | Validates raw agent dumps: checks XML well-formedness, minimum size thresholds, paired XML/MD files. |
| `merge_xml.py` | 3 (REFINE) | Merges multiple XML dumps: deduplicates entities, resolves cross-references, builds unified entity index. Outputs merged XML + JSON. |
| `build_entity_index.py` | 3 (REFINE) | Builds flat entity index from merged XML/JSON: categorizes types, functions, interfaces, constants, commands, patterns. Used by completeness validator. |
| `validate_coverage.py` | 5 (VALIDATE) | File coverage check: lists all source files in repo, fuzzy-matches against file paths mentioned in dumps. PASS threshold: >= 70%. |
| `validate_completeness.py` | 5 (VALIDATE) | Symbol documentation check: extracts public symbols from source code, cross-references against entity index. PASS threshold: >= 60%. |
| `validate_consistency.py` | 5 (VALIDATE) | Cross-reference consistency check: detects type contradictions and orphan references across agent dumps. PASS threshold: 0 contradictions. |
| `score_report.py` | 5 (VALIDATE) | Aggregates validation results into weighted quality score. Grades A-F. Produces actionable recommendations for gaps. |

---

## Plugins

Plugins are self-contained packages that bundle commands, skills, agents, and scripts together.

### Learn Plugin

**Directory:** [`plugins/learn/`](plugins/learn/)

Educational explanation plugin. Explains concepts with structured methodology: one-line definition, analogy, core explanation, practical example, key takeaways, related concepts.

| Component | File | Type | Description |
|---|---|---|---|
| `/learn` command | [`plugins/learn/commands/learn.md`](plugins/learn/commands/learn.md) | Command | Explain a concept or answer a question using the explanation methodology |
| Explainer agent | [`plugins/learn/agents/explainer.md`](plugins/learn/agents/explainer.md) | Agent | Proactive agent for structured explanations. Adapts for programming, comparisons, procedural, and abstract concepts. |
| Explanation Methodology | [`plugins/learn/skills/explanation-methodology/SKILL.md`](plugins/learn/skills/explanation-methodology/SKILL.md) | Skill | Core methodology: template, writing guidelines, quality checklist |
| Advanced Patterns | [`plugins/learn/skills/explanation-methodology/references/advanced-patterns.md`](plugins/learn/skills/explanation-methodology/references/advanced-patterns.md) | Reference | Audience adaptation (beginner/intermediate/expert), domain-specific adjustments, handling "vs" and "how to" and abstract concept questions |

### Paper Plugin

**Directory:** [`plugins/paper/`](plugins/paper/)

Newspaper-style dev-blog article generator. Reads a project's codebase and produces a compelling article with a punchy headline, strong lead, and technical depth woven into narrative.

| Component | File | Type | Description |
|---|---|---|---|
| `/paper` command | [`plugins/paper/commands/paper.md`](plugins/paper/commands/paper.md) | Command | Generate a dev-blog article from the current project, output to `docs/paper.md` |
| Paper skill | [`plugins/paper/skills/paper/SKILL.md`](plugins/paper/skills/paper/SKILL.md) | Skill | Full process: gather raw material → find the story → write the article → save to disk. 1,500-3,000 words. |
| Article Structure | [`plugins/paper/skills/paper/references/article-structure.md`](plugins/paper/skills/paper/references/article-structure.md) | Reference | Structural templates for different project types: Tool Story, Abstraction Story, Architecture Story, Itch Story, Migration Story. Section flow principles and length guidance. |
| Writing Guide | [`plugins/paper/skills/paper/references/writing-guide.md`](plugins/paper/skills/paper/references/writing-guide.md) | Reference | Newspaper writing techniques: inverted pyramid, headline craft, lead patterns, sandwich technique for code snippets, tone calibration, words/phrases to avoid. |

### Triagger Plugin

**Directory:** [`plugins/triagger/`](plugins/triagger/)

Bug triage and issue creation plugin. Investigates reported problems, finds root causes, and creates GitHub issues with TDD-based fix plans.

| Component | File | Type | Description |
|---|---|---|---|
| `/triage-issue` command | [`plugins/triagger/commands/triage-issue.md`](plugins/triagger/commands/triage-issue.md) | Command | Triage a bug: explore codebase, find root cause, create GitHub issue with TDD fix plan |
| `/write-a-skill` command | [`plugins/triagger/commands/write-a-skill.md`](plugins/triagger/commands/write-a-skill.md) | Command | Write a Claude Code skill from scratch with proper structure, scripts, and review |
| Triagger agent | [`plugins/triagger/agents/triagger.md`](plugins/triagger/agents/triagger.md) | Agent | Autonomous triage agent: pre-flight → capture → explore/diagnose → identify fix → design TDD plan → create issue → landing |
| `preflight.sh` | [`plugins/triagger/scripts/preflight.sh`](plugins/triagger/scripts/preflight.sh) | Script | Environment check: git, gh CLI, authentication, repo access, issues enabled, network |
| `postflight.sh` | [`plugins/triagger/scripts/postflight.sh`](plugins/triagger/scripts/postflight.sh) | Script | Issue validation: required sections (Problem, Root Cause Analysis, TDD Fix Plan, Acceptance Criteria), RED/GREEN balance, durability check |
| `landing.sh` | [`plugins/triagger/scripts/landing.sh`](plugins/triagger/scripts/landing.sh) | Script | Final protocol: runs post-flight, prints issue summary, cleans up temp files |
| `doctor.sh` | [`plugins/triagger/scripts/doctor.sh`](plugins/triagger/scripts/doctor.sh) | Script | Full environment diagnostic (like `flutter doctor`): git, gh, repo access, network, shell tools, plugin scripts |
| `validate-issue.sh` | [`plugins/triagger/scripts/validate-issue.sh`](plugins/triagger/scripts/validate-issue.sh) | Script | Deep CI-grade validation: title length, required sections, TDD plan quality, durability (no file:line refs, no hardcoded paths), acceptance criteria completeness. Mockable via `GH_CMD`. |

### Write-a-Skill Plugin

**Directory:** [`plugins/write-a-skill/`](plugins/write-a-skill/)

| Component | File | Type | Description |
|---|---|---|---|
| `/write-a-skill` command | [`plugins/write-a-skill/commands/write-a-skill.md`](plugins/write-a-skill/commands/write-a-skill.md) | Command | Interactive skill creation: gather requirements → draft SKILL.md + references + scripts → review with user. Includes description requirements, file splitting guidance, and review checklist. |

---

## Quick Reference

### By Workflow

| I want to... | Use |
|---|---|
| Debug a bug systematically | `systematic-debugging` skill |
| Triage and file a bug | `/triage-issue` |
| Plan a feature from a PRD | `/prd-to-plan` or `/prd-to-issues` |
| Write a PRD from scratch | `/write-a-prd` |
| Stress-test my design | `/grill-me` |
| Build from a plan (solo) | `/build` |
| Build from a plan (team) | `/build-with-orch` or `/plan-w-team` |
| Develop with TDD | `/tdd` |
| Analyze a GitHub repo | `/learn-repo` or `/synthesize` |
| Read and summarize an article | `/read-article` |
| Design a module interface | `/design-interface` |
| Find architecture improvements | `/improve-architecture` |
| Plan a refactor with tiny commits | `/request-refactor-plan` |
| Set up a GitHub repo from scratch | `/gh-setup` |
| Improve a CLAUDE.md file | `/improve-claude-md` |
| Explain a concept clearly | `/learn` |
| Generate a dev-blog article | `/paper` |
| Create a new Claude skill | `/write-a-skill` |
| Code with professional principles | `/clean-coder` |

### By Category

| Category | Commands / Skills |
|---|---|
| **Debugging & Triage** | `systematic-debugging`, `/triage-issue`, `root-cause-tracing` |
| **Planning & Design** | `/write-a-prd`, `/grill-me`, `/prd-to-plan`, `/prd-to-issues`, `/design-interface`, `/request-refactor-plan` |
| **Building & Execution** | `/build`, `/build-with-orch`, `/plan-w-team`, `/tdd`, `/ralph-issues-build` |
| **Codebase Analysis** | `/learn-repo`, `/synthesize`, `/improve-architecture` |
| **Reading & Learning** | `/read-article`, `/learn` |
| **GitHub & DevOps** | `/gh-setup` |
| **Writing & Documentation** | `/paper`, `/improve-claude-md` |
| **Meta (Skill/Agent Creation)** | `/write-a-skill`, `clean-coder` |
