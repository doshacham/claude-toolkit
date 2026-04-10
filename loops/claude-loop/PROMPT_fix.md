0a. Study `specs/*` by dispatching up to 10 parallel Opus subagents to learn the application specifications in batches per logical area.
0b. Study `IMPLEMENTATION_PLAN.md`.
0c. For reference, the application source code is in `src/*`.

1. Your task is to fix bugs per the audit findings and specifications. Follow `IMPLEMENTATION_PLAN.md` and choose the highest severity item to address. Before making changes, dispatch up to 20 parallel Opus subagents to search the codebase and confirm the bug still exists. Use only 1 Opus subagent for build/tests. Dispatch Opus subagents when complex reasoning is needed (debugging, architectural decisions).
2. After fixing the bug, run all tests. The fix must not break existing tests or introduce regressions. If the bug has no test coverage, write a test that reproduces the bug before fixing it, then verify the test passes after fixing.
3. When you discover additional issues, immediately update `IMPLEMENTATION_PLAN.md` with your findings using a subagent. When resolved, update and remove the item.
4. When the tests pass, update `IMPLEMENTATION_PLAN.md`, then `git add -A` then `git commit` with a message describing the fix. After the commit, `git push`. Do not pick up another item — you are running inside an automated loop and the loop script will start a fresh iteration for the next item.

*** MANDATORY RULES: ***

999. Every fix must have a test that would have caught the bug. Tests are part of fix scope, not optional.
9999. Verify the fix against the specification in `specs/*` — the spec defines correct behavior, not the previous code.
99999. Important: Single sources of truth, no migrations/adapters. If tests unrelated to your work fail, resolve them as part of the increment.
999999. Important: Fix one bug per iteration. Keep fixes focused and minimal
9999999. You may add extra logging if required to debug issues.
99999999. Keep `IMPLEMENTATION_PLAN.md` current with learnings using a subagent — future work depends on this to avoid duplicating efforts. Update especially after finishing your turn.
999999999. When you learn something new about how to run the application, update `AGENTS.md` using a subagent but keep it brief.
9999999999. When `IMPLEMENTATION_PLAN.md` becomes large periodically clean out the items that are completed from the file using a subagent.
99999999999. If you find inconsistencies in the specs/* then use an Opus subagent with 'ultrathink' requested to update the specs.
999999999999. IMPORTANT: Keep `AGENTS.md` operational only — status updates and progress notes belong in `IMPLEMENTATION_PLAN.md`. A bloated AGENTS.md pollutes every future loop's context.
9999999999999. MANDATORY: After commit+push, do not pick up another item — the loop handles the next iteration.
