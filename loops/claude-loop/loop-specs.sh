#!/bin/bash
# Usage: ./loop-specs.sh
# Phase 1: Requirements interview — runs once (interactive, not a loop)

PROMPT_FILE="PROMPT_specs.md"
CURRENT_BRANCH=$(git branch --show-current)

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   specs (Phase 1 interview)"
echo "Prompt: $PROMPT_FILE"
echo "Branch: $CURRENT_BRANCH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: $PROMPT_FILE not found"
    exit 1
fi

rm -f /tmp/claude-loop-done

# Background watcher: polls for sentinel file, then kills the newest claude.exe
powershell.exe -NoProfile -Command "
    \$sentinel = Join-Path \$env:TEMP 'claude-loop-done'
    while (\$true) {
        if (Test-Path \$sentinel) {
            Remove-Item \$sentinel -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 3
            Get-Process -Name claude -ErrorAction SilentlyContinue |
                Sort-Object StartTime -Descending |
                Select-Object -First 1 |
                Stop-Process -Force -ErrorAction SilentlyContinue
            break
        }
        Start-Sleep -Seconds 2
    }
" &
WATCHER_PID=$!

claude --model claude-opus-4-6 \
    "$(cat "$PROMPT_FILE")" || true

# Clean up watcher if claude exited on its own
kill $WATCHER_PID 2>/dev/null || true
wait $WATCHER_PID 2>/dev/null || true
rm -f /tmp/claude-loop-done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Phase 1 complete. Review artifacts:"
echo "  - AUDIENCE_JTBD.md"
echo "  - specs/*.md"
echo "  - PROMPT_plan.md (goal updated)"
echo ""
echo "Next: ./loop-plan.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
