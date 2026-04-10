#!/bin/bash
# Usage:
#   ./loop-fix.sh plan [max_iterations]    # Create fix plan from audit reports
#   ./loop-fix.sh [max_iterations]         # Fix bugs from plan
# Examples:
#   ./loop-fix.sh plan          # Plan mode, unlimited iterations
#   ./loop-fix.sh plan 3        # Plan mode, max 3 iterations
#   ./loop-fix.sh               # Fix mode, unlimited iterations
#   ./loop-fix.sh 20            # Fix mode, max 20 iterations

# Parse arguments
MODE="fix"
PROMPT_FILE="PROMPT_fix.md"
MAX_ITERATIONS=0

if [ "${1:-}" = "plan" ]; then
    MODE="fix-plan"
    PROMPT_FILE="PROMPT_fix_plan.md"
    MAX_ITERATIONS=${2:-0}
elif [[ "${1:-}" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=$1
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)
export CLAUDE_LOOP_MODE=1

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   $MODE"
echo "Prompt: $PROMPT_FILE"
echo "Branch: $CURRENT_BRANCH"
[ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: $PROMPT_FILE not found"
    exit 1
fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"
        if [ "$MODE" = "fix-plan" ]; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Fix plan created. To start fixing, run:"
            echo "  ./loop-fix.sh 20"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
        break
    fi

    ITERATION=$((ITERATION + 1))
    echo -e "\n======================== ITERATION $ITERATION ========================\n"

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

    claude --dangerously-skip-permissions \
        --model claude-opus-4-6 \
        "$(cat "$PROMPT_FILE")" || true

    # Clean up watcher if claude exited on its own
    kill $WATCHER_PID 2>/dev/null || true
    wait $WATCHER_PID 2>/dev/null || true
    rm -f /tmp/claude-loop-done

    git push origin "$CURRENT_BRANCH" 2>/dev/null || git push -u origin "$CURRENT_BRANCH"

    echo -e "\n======================== ITERATION $ITERATION COMPLETE ========================\n"
done
