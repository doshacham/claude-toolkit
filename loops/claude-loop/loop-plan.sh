#!/bin/bash
# Usage: ./loop-plan.sh [max_iterations]
# Examples:
#   ./loop-plan.sh          # Unlimited iterations
#   ./loop-plan.sh 5        # Max 5 iterations

MAX_ITERATIONS=${1:-0}
ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)
export CLAUDE_LOOP_MODE=1
PROMPT_FILE="PROMPT_plan.md"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Mode:   plan"
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
