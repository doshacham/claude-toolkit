#!/usr/bin/env bash
# Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
# SPDX-License-Identifier: Proprietary

# Guard: enforces agent policy from CLAUDE.md.
# PreToolUse hook for Agent tool.
# Blocks: background agents, haiku/sonnet models.
# Exit 2 = block the tool call. Exit 0 = allow.

set -euo pipefail

command -v jq >/dev/null 2>&1 || exit 0

INPUT=$(cat)

BACKGROUND=$(echo "$INPUT" | jq -r '.tool_input.run_in_background // false')
MODEL=$(echo "$INPUT" | jq -r '.tool_input.model // empty')

if [[ "$BACKGROUND" == "true" ]]; then
  echo "Blocked: background agents are disabled. CLAUDE.md requires all agents to run in foreground." >&2
  exit 2
fi

if [[ "$MODEL" == "haiku" || "$MODEL" == "sonnet" ]]; then
  echo "Blocked: model '$MODEL' is not allowed for subagents. CLAUDE.md requires opus only." >&2
  exit 2
fi

exit 0
