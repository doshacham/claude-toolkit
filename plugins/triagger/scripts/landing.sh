#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Landing protocol - final steps after issue creation.
# Runs post-flight validation, prints summary, cleans up.
# Usage: landing.sh <issue-url>

set -uo pipefail

ISSUE_URL="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -z "$ISSUE_URL" ]; then
  echo "FAIL: no issue URL provided"
  echo "Usage: landing.sh <issue-url>"
  exit 1
fi

echo "=== Landing Protocol ==="

# --- 1. Post-flight validation ---
echo ""
echo "--- Post-flight validation ---"
bash "$SCRIPT_DIR/postflight.sh" "$ISSUE_URL"
POSTFLIGHT_STATUS=$?

if [ $POSTFLIGHT_STATUS -ne 0 ]; then
  echo ""
  echo "WARN: post-flight had failures (see above)"
fi

# --- 2. Issue summary ---
echo ""
echo "--- Issue Summary ---"
ISSUE_NUM=$(echo "$ISSUE_URL" | grep -oE '[0-9]+$')

if [ -n "$ISSUE_NUM" ]; then
  TITLE=$(gh issue view "$ISSUE_NUM" --json title -q '.title' 2>/dev/null || echo "unknown")
  LABELS=$(gh issue view "$ISSUE_NUM" --json labels -q '[.labels[].name] | join(", ")' 2>/dev/null || echo "none")
  ASSIGNEES=$(gh issue view "$ISSUE_NUM" --json assignees -q '[.assignees[].login] | join(", ")' 2>/dev/null || echo "none")
  STATE=$(gh issue view "$ISSUE_NUM" --json state -q '.state' 2>/dev/null || echo "unknown")

  echo "  URL:       $ISSUE_URL"
  echo "  Title:     $TITLE"
  echo "  State:     $STATE"
  echo "  Labels:    ${LABELS:-none}"
  echo "  Assignees: ${ASSIGNEES:-none}"
fi

# --- 3. Cleanup ---
echo ""
echo "--- Cleanup ---"
TEMP_COUNT=0
for f in /tmp/triagger-*; do
  if [ -f "$f" ] 2>/dev/null; then
    rm -f "$f"
    TEMP_COUNT=$((TEMP_COUNT + 1))
  fi
done
echo "Cleaned $TEMP_COUNT temp file(s)"

# --- Done ---
echo ""
echo "=== Landing complete ==="
echo "Issue: $ISSUE_URL"
exit $POSTFLIGHT_STATUS
