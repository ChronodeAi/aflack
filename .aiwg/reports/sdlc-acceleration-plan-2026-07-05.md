# SDLC Acceleration Plan

**Date**: 2026-07-05  
**Skill**: `sdlc-accelerate`  
**Mode**: Construction -> IOC acceleration  
**Phase**: Controlled Construction  
**Decision**: Accelerate the remaining evidence, integration, and traceability work; do not regenerate completed Inception/Elaboration artifacts.

## Acceleration Summary

The normal `sdlc-accelerate` path moves a raw idea or codebase through Intake, LOM, Elaboration, ABM, Construction Prep, and a Construction Ready Brief. Aflack has already passed that boundary. The correct acceleration target is now Initial Operational Capability readiness: make the live content-factory loop observable, reviewable, measurable, and traceable enough to evaluate Construction -> Transition later.

Current state:

- Construction-ready brief exists and remains valid with updated caveats.
- Controlled Construction is 90%+ complete through the draft-ramp boundary.
- EP001 measured generation and private Postiz draft are complete.
- Analytics aggregation is wired but has zero real metrics.
- Prompt-quality hardening now blocks compliant-but-boring assets.
- 53 unit/integration tests pass.
- AIWG index contains 149 project artifacts after the draft-review, Loadout Lab regression, config-loader hardening, and setup-command traceability rebuild.
- Public publishing and broader autonomy remain blocked.

## Accelerated Path

| Lane | Goal | Acceptance criteria | Gate |
|---|---|---|---|
| A3-001 Cockpit visibility | Make Aflack legible in AIWG Cockpit. | JSON status commands, loop status, and action manifest documented; approval gates mapped to Cockpit inbox/action model. | No account, publish, spend, or daemon autonomy changes. |
| A3-002 Render review | Turn EP001 final render review into structured learning. | Review rubric captures hook, retention, compliance, asset quality, CTA, and kill/keep decision. | Public publish remains blocked. |
| A3-003 Analytics refresh | Capture real Postiz/platform metrics when available. | Post/post platform snapshots refreshed; no-signal state recorded if metrics remain zero. | Do not infer success from views alone or zero metrics. |
| A3-004 Draft-ramp policy | Learn publish-quality criteria from first drafts. | Draft review records roll up into a deterministic policy with thresholds and examples. | No publish automation until policy is encoded and approved. |
| A3-005 IOC hardening | Close technical gates for Construction -> Transition. | CLI runner tests, requirement-code-test matrix, and live adapter contract tests exist for critical paths. | IOC gate remains conditional until traceability improves. |

## Dual-Track Iteration 3

Delivery track:

1. Keep Cockpit contribution manifest current with Aflack status/action surfaces.
2. Add CLI runner tests for high-value commands: `daemon-status`, `analytics-status`, `publish-queue-status`, `prompt-quality`, and `compliance-smoke`.
3. Refresh traceability so requirements link to code/tests after the 47-test suite.

Discovery track:

1. Record EP001 final-render review through the implemented draft-review data model.
2. Define publish-quality policy fields before the first-100 draft ramp grows.
3. Decide whether Cockpit install belongs in this repo session now or after the current construction report is reviewed.

## IOC Gate Forecast

| IOC criterion | Current status | Acceleration action |
|---|---|---|
| Critical tests passing | PASS | Keep 47-test suite green; add CLI runner coverage. |
| Security/compliance gates | PASS WITH HUMAN GATES | Preserve public-publish/account/ad/DM/follow blocks. |
| Operational visibility | PARTIAL | JSON status and contribution manifest exist; Cockpit Bridge launch verification remains. |
| Analytics/economics loop | WIRED / NO REAL SIGNAL | Postiz refresh captured snapshot 3; record no-signal explicitly. |
| Traceability | CONDITIONAL | Create requirement-code-test matrix before IOC. |
| Release/publish readiness | BLOCKED BY DESIGN | Requires render review, draft learning, and operator approval. |

## Operator Gates Preserved

- Public publishing.
- Account or channel setting changes.
- Comment, DM, follow, unfollow automation.
- Paid promotion or ad spend.
- Broader daemon autonomy.

Measured generation remains approved only for validated packages under adaptive credit tracking. The first 100 Postiz submissions remain draft-only and require explicit package/target integration.

## Next Safe Actions

1. Implement Cockpit-readable status/action mapping for Aflack.
2. Add CLI runner tests for critical commands.
3. Create the EP001 render-review rubric and record the first review.
4. Refresh analytics after real metrics exist.
5. Update traceability from requirements to code/tests before running Construction -> Transition gate.

## References

- @.aiwg/reports/status-assessment.md
- @.aiwg/reports/construction-90pct-status-2026-07-04.md
- @.aiwg/reports/construction-completion-report-2026-07-04.md
- @.aiwg/reports/higgsfield-prompt-audit-2026-07-04.md
- @.aiwg/reports/traceability-2026-07-04.md
- @.aiwg/loops/content-factory/LOOP.md
- @.aiwg/loops/content-factory/state.yaml
- @.aiwg/planning/video-analytics-aggregation-plan.md
- @.aiwg/planning/daemon-runtime-architecture.md
- @.aiwg/creator-commerce-ops/rules/no-safe-boring-generation.md
- @.aiwg/creator-commerce-ops/rules/testable-contracts-over-prose.md
