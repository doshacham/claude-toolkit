---
description: Set up and configure a GitHub repository from A-Z
argument-hint: [repo name or path (optional)]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

# GitHub Repository Setup

Set up and configure a GitHub repository following security best practices.

## Instructions

Follow the A-Z workflow from the `github-setup` skill. Execute each step sequentially:

1. **Preflight** — verify `gh auth status`, detect repo, check visibility
2. **Secrets** — ask the user which secrets to configure, set via `gh secret set`
3. **Dependabot** — detect ecosystems from manifest files, generate `.github/dependabot.yml`
4. **CI Workflow** — generate hardened `.github/workflows/ci.yml` (pinned SHAs, `permissions: {}`, env var injection)
5. **Auto-merge** — generate `.github/workflows/dependabot-auto-merge.yml` (patch+minor only)
6. **Claude Integration** — generate `.github/workflows/claude-review.yml` + `CLAUDE.md` if requested
7. **Scanning** — enable Dependabot alerts, verify push protection
8. **Branch Protection** — configure via `gh api` if available (free tier aware)
9. **Verify** — confirm everything landed, print summary

## Behavior

- Check existing config before each step — never duplicate
- Ask before setting secrets — never assume values
- Pin all actions to full SHA in generated workflows
- Warn if a feature requires a paid plan
- If `$ARGUMENTS` specifies a repo, `cd` to it or `gh repo clone` it first
- If `$ARGUMENTS` is empty, use the current working directory
- If not in a git repo, ask the user what to do
