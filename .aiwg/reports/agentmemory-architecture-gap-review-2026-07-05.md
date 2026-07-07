# Agentmemory Architecture Gap Review

**Date**: 2026-07-05  
**Scope**: agentmemory recall, Aflack architecture, construction readiness  
**Status**: reviewed

## Memory Findings

Agentmemory returned these high-signal Aflack lessons:

| Lesson | Architectural impact |
|---|---|
| Bounded automation lanes: measured generation, draft-only Postiz ramp, public publishing blocked until criteria exist. | Already captured in ADR-0008, loop constraints, budget, and construction gates; reinforced in this review. |
| Testable contracts over prose for skills/rules/workflows/daemon behavior. | Present as a rule; now also reflected in SAD and test strategy. |
| Prefer AIWG SkillSmith/AgentSmith for reusable content-pipeline skills/agents. | Present in frameworkization plan; should remain a promotion gate before creating new reusable skills/agents. |
| Loadout Lab v1 prompts were compliant but not viral/generation-worthy. | Present in prompt-quality rule and tests; reinforced as a publish-quality gate. |
| PSI transition lesson: do not claim transition readiness without real proof. | Applied to Aflack: no Transition/Production claim until real render/analytics/traceability gates pass. |

## Architecture Gap Assessment

No new core memory engine should be added before IOC. The current architecture is intentionally split:

- Postgres/pgGraph/pgvector: content-pipeline source of truth and retrieval substrate.
- agentmemory: agent/session recall and learned development context.
- `.aiwg` artifacts: durable SDLC decisions, gates, and policies.
- Cockpit: operator surface over sessions/actions/approvals.

The missing piece was not another memory product; it was a clearer contract for how Cockpit consumes Aflack state and how memories become executable policy. This review added that contract to the SAD, Cockpit plan, and publish-quality policy draft.

## Recommendation

Defer external memory-system bakeoff until real draft/publish outcomes exist. Prioritize structured review records and analytics snapshots so future memory evaluation uses real Aflack evidence instead of synthetic examples.
