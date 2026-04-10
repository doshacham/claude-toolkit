#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Deep validation of a triagger issue.
# Stricter than postflight - use for CI or manual review.
# Usage: validate-issue.sh <issue-number>
# Mockable: override GH_CMD env var to mock gh (default: gh)

set -euo pipefail

GH="${GH_CMD:-gh}"
ISSUE_NUM="${1:-}"

if [ -z "$ISSUE_NUM" ]; then
  echo "Usage: validate-issue.sh <issue-number>"
  echo "  Set GH_CMD to mock the gh CLI"
  exit 1
fi

BODY=$($GH issue view "$ISSUE_NUM" --json body -q '.body')
TITLE=$($GH issue view "$ISSUE_NUM" --json title -q '.title')
LABELS=$($GH issue view "$ISSUE_NUM" --json labels -q '[.labels[].name] | join(",")')

ERRORS=0
WARNINGS=0

err()  { echo "ERROR: $1"; ERRORS=$((ERRORS + 1)); }
warn() { echo "WARN:  $1"; WARNINGS=$((WARNINGS + 1)); }
pass() { echo "PASS:  $1"; }

# --- Title ---
if [ ${#TITLE} -gt 100 ]; then
  warn "title exceeds 100 chars (${#TITLE})"
else
  pass "title length OK (${#TITLE})"
fi

if [ -z "$TITLE" ]; then
  err "title is empty"
fi

# --- Required sections ---
for section in "## Problem" "## Root Cause Analysis" "## TDD Fix Plan" "## Acceptance Criteria"; do
  if echo "$BODY" | grep -q "$section"; then
    pass "section: $section"
  else
    err "missing section: $section"
  fi
done

# --- TDD plan quality ---
RED_COUNT=$(echo "$BODY" | grep -c '\*\*RED\*\*' || true)
GREEN_COUNT=$(echo "$BODY" | grep -c '\*\*GREEN\*\*' || true)
REFACTOR=$(echo "$BODY" | grep -c '\*\*REFACTOR\*\*' || true)

if [ "$RED_COUNT" -eq 0 ]; then
  err "no RED steps in TDD plan"
else
  pass "$RED_COUNT RED step(s)"
fi

if [ "$GREEN_COUNT" -eq 0 ]; then
  err "no GREEN steps in TDD plan"
else
  pass "$GREEN_COUNT GREEN step(s)"
fi

if [ "$RED_COUNT" -ne "$GREEN_COUNT" ]; then
  warn "RED/GREEN count mismatch (RED=$RED_COUNT, GREEN=$GREEN_COUNT)"
fi

if [ "$REFACTOR" -eq 0 ]; then
  warn "no REFACTOR step (optional but recommended)"
fi

# --- Durability ---
if echo "$BODY" | grep -qE '[a-zA-Z0-9_/]+\.[a-z]{2,4}:[0-9]+'; then
  warn "contains file:line references (breaks durability)"
else
  pass "no file:line references"
fi

if echo "$BODY" | grep -qE '(src|lib|app|pages|components)/[a-zA-Z0-9_/]+\.[a-z]+'; then
  warn "contains specific file paths (consider using module/behavior names)"
else
  pass "no hardcoded file paths"
fi

# --- Acceptance criteria ---
CRITERIA_COUNT=$(echo "$BODY" | grep -c '\- \[ \]' || true)
if [ "$CRITERIA_COUNT" -lt 2 ]; then
  warn "fewer than 2 acceptance criteria ($CRITERIA_COUNT)"
else
  pass "$CRITERIA_COUNT acceptance criteria"
fi

# Must include "All new tests pass" and "Existing tests still pass"
if ! echo "$BODY" | grep -qi 'new tests pass'; then
  warn "missing 'all new tests pass' criterion"
fi
if ! echo "$BODY" | grep -qi 'existing tests.*pass'; then
  warn "missing 'existing tests still pass' criterion"
fi

# --- Summary ---
echo ""
echo "=== Validation: $ERRORS error(s), $WARNINGS warning(s) ==="
echo "TDD: $RED_COUNT RED / $GREEN_COUNT GREEN / $REFACTOR REFACTOR"
echo "Criteria: $CRITERIA_COUNT"
echo "Labels: ${LABELS:-none}"

if [ $ERRORS -gt 0 ]; then
  exit 1
fi
exit 0
