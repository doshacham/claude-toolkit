#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Doctor protocol for triagger.
# Full environment diagnostic - like `flutter doctor`.
# Exit 0 = healthy, exit 1 = problems found.

set -uo pipefail

STATUS=0

section() { echo ""; echo "--- $1 ---"; }
pass()    { echo "  PASS: $1"; }
fail()    { echo "  FAIL: $1"; STATUS=1; }
warn()    { echo "  WARN: $1"; }
info()    { echo "  INFO: $1"; }

echo "=== Triagger Doctor ==="

# --- Git ---
section "Git"
if command -v git >/dev/null 2>&1; then
  pass "git $(git --version 2>/dev/null | cut -d' ' -f3)"
else
  fail "git not found"
fi

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  pass "inside git repo"
  REMOTE=$(git remote get-url origin 2>/dev/null || echo "none")
  BRANCH=$(git branch --show-current 2>/dev/null || echo "detached")
  COMMITS=$(git rev-list --count HEAD 2>/dev/null || echo "0")
  info "remote: $REMOTE"
  info "branch: $BRANCH"
  info "commits: $COMMITS"
else
  warn "not inside a git repo (triagger needs a repo to work)"
fi

# --- GitHub CLI ---
section "GitHub CLI"
if command -v gh >/dev/null 2>&1; then
  GH_VER=$(gh --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' || echo "unknown")
  pass "gh $GH_VER"
else
  fail "gh not found (install: https://cli.github.com)"
fi

if gh auth status >/dev/null 2>&1; then
  pass "gh authenticated"
  GH_USER=$(gh api user -q '.login' 2>/dev/null || echo "unknown")
  info "logged in as: $GH_USER"
else
  fail "gh not authenticated (run: gh auth login)"
fi

# --- Repo access ---
section "Repository"
if gh repo view --json name >/dev/null 2>&1; then
  REPO_NAME=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null)
  pass "repo accessible: $REPO_NAME"

  ISSUES=$(gh repo view --json hasIssuesEnabled -q '.hasIssuesEnabled' 2>/dev/null)
  if [ "$ISSUES" = "true" ]; then
    pass "issues enabled"
  else
    fail "issues disabled on this repo"
  fi

  ISSUE_COUNT=$(gh issue list --limit 1 --json number -q 'length' 2>/dev/null || echo "?")
  info "open issues: $ISSUE_COUNT+"
else
  warn "cannot access repo via gh (may not be in a repo)"
fi

# --- Network ---
section "Network"
if curl -s --max-time 5 https://api.github.com/zen >/dev/null 2>&1; then
  pass "GitHub API reachable"
else
  fail "cannot reach GitHub API"
fi

# --- Shell tools ---
section "Shell Tools"
for tool in curl grep sed bash; do
  if command -v "$tool" >/dev/null 2>&1; then
    pass "$tool available"
  else
    fail "$tool not found"
  fi
done

# --- Plugin scripts ---
section "Plugin Scripts"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
for script in preflight.sh postflight.sh validate-issue.sh landing.sh; do
  if [ -x "$SCRIPT_DIR/$script" ]; then
    pass "$script (executable)"
  elif [ -f "$SCRIPT_DIR/$script" ]; then
    warn "$script exists but not executable (run: chmod +x $SCRIPT_DIR/$script)"
  else
    fail "$script missing"
  fi
done

# --- Summary ---
echo ""
echo "=== Doctor complete (status: $STATUS) ==="
if [ $STATUS -eq 0 ]; then
  echo "Environment is healthy."
else
  echo "Fix the FAIL items above before running triagger."
fi
exit $STATUS
