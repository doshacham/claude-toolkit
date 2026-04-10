#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Post-flight validation for a created GitHub issue.
# Checks that the issue has the required structure.
# Usage: postflight.sh <issue-url>

set -euo pipefail

ISSUE_URL="${1:-}"
if [ -z "$ISSUE_URL" ]; then
  echo "FAIL: no issue URL provided"
  echo "Usage: postflight.sh <issue-url>"
  exit 1
fi

# Extract issue number from URL
ISSUE_NUM=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')
if [ -z "$ISSUE_NUM" ]; then
  echo "FAIL: could not extract issue number from URL: $ISSUE_URL"
  exit 1
fi

# Fetch issue body
BODY=$(gh issue view "$ISSUE_NUM" --json body -q '.body' 2>/dev/null)
if [ -z "$BODY" ]; then
  echo "FAIL: could not fetch issue #$ISSUE_NUM body"
  exit 1
fi

ERRORS=0
WARNINGS=0

# --- Required sections ---
for section in "## Problem" "## Root Cause Analysis" "## TDD Fix Plan" "## Acceptance Criteria"; do
  if echo "$BODY" | grep -q "$section"; then
    echo "PASS: has '$section'"
  else
    echo "FAIL: missing '$section'"
    ERRORS=$((ERRORS + 1))
  fi
done

# --- TDD structure ---
RED_COUNT=$(echo "$BODY" | grep -c '\*\*RED\*\*' || true)
GREEN_COUNT=$(echo "$BODY" | grep -c '\*\*GREEN\*\*' || true)

if [ "$RED_COUNT" -eq 0 ]; then
  echo "FAIL: no RED steps in TDD plan"
  ERRORS=$((ERRORS + 1))
else
  echo "PASS: $RED_COUNT RED step(s)"
fi

if [ "$GREEN_COUNT" -eq 0 ]; then
  echo "FAIL: no GREEN steps in TDD plan"
  ERRORS=$((ERRORS + 1))
else
  echo "PASS: $GREEN_COUNT GREEN step(s)"
fi

if [ "$RED_COUNT" -ne "$GREEN_COUNT" ]; then
  echo "WARN: RED/GREEN mismatch ($RED_COUNT RED, $GREEN_COUNT GREEN)"
  WARNINGS=$((WARNINGS + 1))
fi

# --- Acceptance criteria checkboxes ---
CRITERIA_COUNT=$(echo "$BODY" | grep -c '\- \[ \]' || true)
if [ "$CRITERIA_COUNT" -lt 2 ]; then
  echo "WARN: fewer than 2 acceptance criteria ($CRITERIA_COUNT found)"
  WARNINGS=$((WARNINGS + 1))
else
  echo "PASS: $CRITERIA_COUNT acceptance criteria"
fi

# --- Durability: no file:line references ---
if echo "$BODY" | grep -qE '[a-zA-Z0-9_/]+\.[a-z]{2,4}:[0-9]+'; then
  echo "WARN: issue contains file:line references (durability concern)"
  WARNINGS=$((WARNINGS + 1))
else
  echo "PASS: no file:line references (durable)"
fi

# --- Summary ---
echo ""
echo "POSTFLIGHT: $ERRORS error(s), $WARNINGS warning(s)"
if [ $ERRORS -gt 0 ]; then
  exit 1
fi
exit 0
