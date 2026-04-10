0a. Study `specs/*` by dispatching up to 20 parallel Opus subagents to learn the application specifications.
0b. Study `IMPLEMENTATION_PLAN.md` (if present) to understand the plan so far.
0c. Study `src/lib/*` by dispatching up to 20 parallel Opus subagents to understand shared utilities & components.
0d. For reference, the application source code is in `src/*`.
0e. Study any audit and review reports found in the project root or `docs/` directory by dispatching up to 10 parallel Opus subagents.

1. Study the audit reports and dispatch up to 30 parallel Opus subagents to verify each finding against the actual source code in `src/*`. For each finding, confirm whether the bug still exists — do NOT assume findings are current; the code may have changed since the audit. Use 1 Opus subagent to analyze confirmed findings, prioritize by severity (CRITICAL > HIGH > MEDIUM > LOW), and create/update `IMPLEMENTATION_PLAN.md` as a bullet point list sorted by priority. Ultrathink. For each confirmed bug, include: the file and function, what's wrong, what the fix should be, and what test verifies the fix. Cross-reference findings against `specs/*` to determine correct behavior.

IMPORTANT: Plan only. Do NOT implement anything. Do NOT assume a bug exists without confirming it in the current code. Some findings may already be fixed. Treat `src/lib` as the project's standard library for shared utilities and components.

MANDATORY: After completing your turn, do not pick up another item — the loop handles the next iteration.
