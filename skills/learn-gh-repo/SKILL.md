---
name: learn-gh-repo
description: This skill clones and deeply analyzes a GitHub repository, producing a comprehensive architecture report. Use when the user asks to "learn this repo", "study this codebase", "analyze this GitHub project", "what does this repo do", "break down this codebase", or provides a GitHub URL to understand.
---

You will be given a URL of a GitHub repository, for example:

https://github.com/karpathy/nanochat

### Part 1: Normalize the URL

Extract the `owner/repo` from the URL. Accept any of these formats:

- `https://github.com/owner/repo`
- `github.com/owner/repo`
- `owner/repo`

Strip any trailing slashes, `.git` suffix, or subpaths (e.g. `/tree/main/src`).

### Part 2: Clone the repository

Clone the repository into a temporary directory. A good location is `/tmp/claude-repos/{repo}`. On Windows, use the system temp directory instead (e.g. `$TEMP/claude-repos/{repo}`).

(If the directory already exists from a previous run, remove it first to ensure a fresh clone).

### Part 3: Explore the structure

Get oriented in the codebase:

1. List the top-level files and directories
2. Read the README if one exists
3. Read the project manifest (e.g. `package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `pom.xml`, `Makefile`, etc.) to identify the tech stack, dependencies, and build system
4. Note the high-level directory layout and what each top-level directory likely contains

### Part 4: Identify entry points

Find the main entry points of the project:

- Application entry points (e.g. `main.py`, `index.ts`, `cmd/`, `src/main.rs`)
- Configuration files that reveal how the project is wired together
- If it's a library, find the public API surface (exports, public modules)

### Part 5: Deep read of core source files

Read the most important source files — focus on core logic, not tests, docs, or generated code. Prioritize:

1. Entry points and their immediate dependencies
2. Core abstractions (base classes, traits, interfaces, key types)
3. The main data flow path (request → processing → response, or input → transform → output)
4. Any architectural patterns (plugin systems, middleware chains, event buses, etc.)

Read broadly enough to understand how the pieces connect. For large repos, focus on the most important 15-20 files rather than trying to read everything.

### Part 6: Ask about report style

Before writing the report, ask the user:

> Should this summary be **project-aware** (tied to the current project with borrowable ideas) or **standalone** (general-purpose summary)?

Use AskUserQuestion to let the user choose.

### Part 7: Report

Once you've studied the codebase, produce an architecture report into a markdown file at `./knowledge/summary_{tag}.md`. Generate a reasonable `tag` based on the repo's purpose, like e.g. `nanochat_architecture` or `llm_inference_engine` — whatever fits. Make sure the tag doesn't already exist so you're not overwriting files.

The report should cover:

1. **Overview** — what the project is, what problem it solves, tech stack
2. **Architecture** — how the codebase is organized, key directories and their roles
3. **Core Abstractions** — the main types, interfaces, and patterns that hold the system together
4. **Data Flow** — how data moves through the system from input to output
5. **Design Patterns** — notable architectural choices, patterns, or idioms used

If the user chose **project-aware**, also include:

6. **Borrowable Ideas** — what patterns, techniques, or design decisions from this repo could be applied to the current project. Feel free to "remind yourself" of the related project code by reading the relevant parts, and then explicitly make the connection of how this repo's ideas might apply or what we might be inspired to try.

### Part 8: Clean up

Delete the cloned repository from the temporary directory to free disk space. The report in `./knowledge/` is the permanent artifact.
