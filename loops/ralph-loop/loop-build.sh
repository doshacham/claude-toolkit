#!/bin/bash
# Usage:
#   ./loop-build.sh [max_iterations]              # Build mode
#   ./loop-build.sh plan-work "work description"  # Scoped planning on work branch
# Examples:
#   ./loop-build.sh              # Build mode, unlimited iterations
#   ./loop-build.sh 20           # Build mode, max 20 iterations
#   ./loop-build.sh plan-work "user auth with OAuth"  # Scoped planning

# Parse arguments
MODE="build"
PROMPT_FILE="PROMPT_build.md"
MAX_ITERATIONS=0

if [ "${1:-}" = "plan-work" ]; then
    if [ -z "${2:-}" ]; then
        echo "Error: plan-work requires a work description"
        echo "Usage: ./loop-build.sh plan-work \"description of the work\""
        exit 1
    fi
    MODE="plan-work"
    WORK_DESCRIPTION="$2"
    PROMPT_FILE="PROMPT_plan_work.md"
    MAX_ITERATIONS=${3:-5}
elif [[ "${1:-}" =~ ^[0-9]+$ ]]; then
    MAX_ITERATIONS=$1
fi

ITERATION=0
CURRENT_BRANCH=$(git branch --show-current)
export CLAUDE_LOOP_MODE=1

# Validate branch for plan-work mode
if [ "$MODE" = "plan-work" ]; then
    if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
        echo "Error: plan-work should be run on a work branch, not main/master"
        echo "Create a work branch first: git checkout -b ralph/your-work"
        exit 1
    fi

    export WORK_SCOPE="$WORK_DESCRIPTION"

    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Mode:    plan-work"
    echo "Branch:  $CURRENT_BRANCH"
    echo "Work:    $WORK_DESCRIPTION"
    echo "Prompt:  $PROMPT_FILE"
    [ $MAX_ITERATIONS -gt 0 ] && echo "Max:     $MAX_ITERATIONS iterations"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Mode:   $MODE"
    echo "Prompt: $PROMPT_FILE"
    echo "Branch: $CURRENT_BRANCH"
    [ $MAX_ITERATIONS -gt 0 ] && echo "Max:    $MAX_ITERATIONS iterations"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: $PROMPT_FILE not found"
    exit 1
fi

while true; do
    if [ $MAX_ITERATIONS -gt 0 ] && [ $ITERATION -ge $MAX_ITERATIONS ]; then
        echo "Reached max iterations: $MAX_ITERATIONS"
        if [ "$MODE" = "plan-work" ]; then
            echo ""
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            echo "Scoped plan created: $WORK_DESCRIPTION"
            echo "To build, run:"
            echo "  ./loop-build.sh 20"
            echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        fi
        break
    fi

    ITERATION=$((ITERATION + 1))
    echo -e "\n======================== ITERATION $ITERATION ========================\n"

    rm -f /tmp/claude-loop-done

    # Background watcher: polls for sentinel file, then kills the newest claude.exe
    powershell.exe -NoProfile -Command "
        while (\$true) {
            if (Test-Path 'C:/Users/User/AppData/Local/Temp/claude-loop-done') {
                Remove-Item 'C:/Users/User/AppData/Local/Temp/claude-loop-done' -Force -ErrorAction SilentlyContinue
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

    if [ "$MODE" = "plan-work" ]; then
        claude --dangerously-skip-permissions \
            --model claude-opus-4-6 \
            "$(envsubst < "$PROMPT_FILE")" || true
    else
        claude --dangerously-skip-permissions \
            --model claude-opus-4-6 \
            "$(cat "$PROMPT_FILE")" || true
    fi

    # Clean up watcher if claude exited on its own
    kill $WATCHER_PID 2>/dev/null || true
    wait $WATCHER_PID 2>/dev/null || true
    rm -f /tmp/claude-loop-done

    git push origin "$CURRENT_BRANCH" 2>/dev/null || git push -u origin "$CURRENT_BRANCH"

    echo -e "\n======================== ITERATION $ITERATION COMPLETE ========================\n"
done
