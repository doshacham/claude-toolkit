#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Pre-flight checks for triagger.
# Verifies the environment is ready for triage.
# Exit 0 = all clear, exit 1 = something's wrong.

set -euo pipefail

ERRORS=0

check() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $label"
  else
    echo "FAIL: $label"
    ERRORS=$((ERRORS + 1))
  fi
}

# --- Git ---
check "git installed" command -v git
check "inside git repo" git rev-parse --is-inside-work-tree
check "repo has commits" git rev-list -1 HEAD
check "origin remote exists" git remote get-url origin

# --- GitHub CLI ---
check "gh installed" command -v gh
check "gh authenticated" gh auth status
check "gh can reach repo" gh repo view --json name

# --- Network ---
check "GitHub API reachable" curl -s --max-time 5 https://api.github.com/zen

# --- Issues enabled ---
ISSUES_ENABLED=$(gh repo view --json hasIssuesEnabled -q '.hasIssuesEnabled' 2>/dev/null || echo "false")
if [ "$ISSUES_ENABLED" = "true" ]; then
  echo "PASS: issues enabled on repo"
else
  echo "FAIL: issues disabled on repo"
  ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -gt 0 ]; then
  echo "PREFLIGHT FAILED: $ERRORS check(s) failed"
  exit 1
fi
echo "PREFLIGHT PASSED: all checks green"
