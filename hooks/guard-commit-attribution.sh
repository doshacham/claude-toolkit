#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Guard: blocks git commit commands containing AI attribution.
# PreToolUse hook for Bash tool, filtered by "if": "Bash(git commit*)".
# Exit 2 = block the tool call. Exit 0 = allow.

set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

[[ -z "$CMD" ]] && exit 0

if echo "$CMD" | grep -qiE 'Co-Authored-By.*Claude|Generated with.*Claude Code'; then
  echo "Blocked: commit contains AI attribution. CLAUDE.md forbids Co-Authored-By and 'Generated with Claude Code' lines. Remove them and retry." >&2
  exit 2
fi

exit 0
