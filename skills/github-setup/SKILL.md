---
name: GitHub Setup
description: This skill should be used when the user asks to "set up my GitHub repo", "configure GitHub", "add Dependabot", "harden my GitHub Actions", "add Claude to my repo", "configure GitHub secrets", "set up CI/CD", or wants end-to-end GitHub repository configuration. Provides an A-Z setup workflow covering secrets, CI, Dependabot, Claude integration, and security.
version: 0.1.0
---

# GitHub Repository Setup — A-Z Workflow

Follow these steps sequentially. Skip steps the user explicitly opts out of. Check existing state before each step to avoid duplicating config.

## Step 1: Preflight

```bash
gh auth status
gh repo view --json name,owner,visibility,defaultBranchRef
```

- Confirm `gh` is authenticated and has the required scopes
- Detect repo name, owner, visibility (public/private), default branch
- If private repo: warn that branch protection and secret scanning require Pro ($4/mo)

## Step 2: Secrets

Ask the user which secrets to configure. Common ones by project type:

- **API projects**: `API_KEY`, `DATABASE_URL`, `JWT_SECRET`
- **Cloud deploy**: configure OIDC instead of static keys (see reference)
- **Claude integration**: `ANTHROPIC_API_KEY`
- **Docker**: `DOCKER_USERNAME`, `DOCKER_PASSWORD`

```bash
gh secret set SECRET_NAME --body "value"
gh secret list  # verify
```

Never assume secret values — always ask. Use `SCREAMING_SNAKE_CASE`, prefix by provider (`AWS_`, `GCP_`).

## Step 3: Dependabot

Generate `.github/dependabot.yml`. Detect ecosystems by scanning for manifest files:

| File | Ecosystem |
|---|---|
| `package.json` | `npm` |
| `requirements.txt` / `pyproject.toml` | `pip` |
| `go.mod` | `gomod` |
| `Cargo.toml` | `cargo` |
| `Dockerfile` | `docker` |
| `.github/workflows/*.yml` | `github-actions` |

Apply grouping for patch+minor, weekly schedule, limit 10 open PRs. See `references/config-reference.md` `<dependabot>` for full config options.

## Step 4: CI Workflow

Generate `.github/workflows/ci.yml` with hardening:

- `permissions: {}` at workflow level — grant per-job
- Pin ALL actions to full SHA (not tags)
- Pass untrusted input as env vars, never interpolate in `run:`
- Include the repo's actual build/test commands

Detect project type from manifest files and generate appropriate build+test steps.

## Step 5: Dependabot Auto-Merge

Generate `.github/workflows/dependabot-auto-merge.yml`:

- Trigger on `pull_request` where `github.actor == 'dependabot[bot]'`
- Use `dependabot/fetch-metadata` to extract semver type
- Auto-approve + auto-merge for patch and minor only
- Block major updates — require human review

See `references/config-reference.md` `<auto-merge>` for the workflow template.

## Step 6: Claude Code Integration

If user wants Claude on the repo:

1. Generate `.github/workflows/claude-review.yml` — triggers on `@claude` mentions
2. Generate `CLAUDE.md` at repo root with project conventions
3. Verify `ANTHROPIC_API_KEY` is set as a repo secret

See `references/config-reference.md` `<claude-integration>` for templates.

## Step 7: Security

```bash
# Enable vulnerability alerts
gh api repos/{owner}/{repo}/vulnerability-alerts --method PUT

# Check security settings
gh api /repos/{owner}/{repo} --jq '.security_and_analysis'
```

- Enable Dependabot alerts if not already on
- Verify push protection status
- For public repos: secret scanning is automatic
- For private repos: warn about paid requirements

## Step 8: Branch Protection (Free Tier)

On public repos or Pro+ plans:

```bash
gh api repos/{owner}/{repo}/branches/{branch}/protection --method PUT \
  --input protection.json
```

Minimum recommended protection:
- Require PR reviews (1 reviewer)
- Require status checks (CI must pass)
- Block force pushes
- Block branch deletion

On free private repos: skip and warn user.

## Step 9: Verify

```bash
gh secret list
gh api repos/{owner}/{repo}/contents/.github/dependabot.yml --jq '.name'
gh api repos/{owner}/{repo}/actions/workflows --jq '.workflows[].name'
gh api repos/{owner}/{repo}/vulnerability-alerts --method GET
```

Print a summary table of everything configured.

## Reference

For detailed configuration options, templates, and YAML snippets, consult `references/config-reference.md`.
