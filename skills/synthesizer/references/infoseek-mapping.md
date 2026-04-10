# InfoSeek → Synthesizer Mapping

How the Synthesizer skill maps concepts from the InfoSeek paper
(arXiv:2509.00375) to codebase analysis.

## Concept Mapping

| InfoSeek Concept | Synthesizer Analog | Implementation |
|---|---|---|
| Research Tree | Exploration Tree | `build_exploration_tree.py` — import graph |
| Planner Agent | Phase 1 RECON | Skill instructions + `plan_dispatch.py` |
| Browser Agent | Documenter subagents | Agent prompts in SKILL.md Phase 2 |
| Refiner Agent | Phase 3 REFINE | `merge_xml.py` + `build_entity_index.py` |
| `<think>` phase | Think-Read-Refine cycle | XML template `<think>` blocks |
| `<search>` action | File reads (Glob/Read) | Agent Read tool calls |
| `<information>` output | `<information>` blocks | XML template post-read reflection |
| Difficulty validation | Coverage check | `validate_coverage.py` |
| Verifiability validation | Completeness check | `validate_completeness.py` |
| Underdetermination check | Consistency check | `validate_consistency.py` |
| HCSP formalization | Not applicable | Codebase analysis is graph traversal, not constraint satisfaction |
| Blur action | Not applicable | We extract facts, not generate questions |
| GRPO training | Not applicable | We're orchestrating agents, not training models |

## Quality Score Design

Weights inspired by InfoSeek's dual validation criteria:

- **Coverage (30%)** — Did we look at the code? (InfoSeek: "verifiability")
- **Completeness (30%)** — Did we document what matters? (InfoSeek: "difficulty")
- **Consistency (40%)** — Is the analysis coherent? (InfoSeek: "underdetermination")

## Key Differences

1. **All information is local** — no search engine needed, just file reads
2. **Deterministic validation** — we can programmatically check coverage/completeness
3. **No training step** — the output is a report, not a trained model
4. **Adaptive dispatch** — agents are re-dispatched based on gaps (InfoSeek doesn't do this)
