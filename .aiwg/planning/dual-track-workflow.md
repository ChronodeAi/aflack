# Dual-Track Workflow

**Date**: 2026-07-05  
**Phase**: Controlled Construction  
**Mode**: Lightweight solo-operator dual track

## Purpose

Construction should keep discovery and delivery separate even though one operator may perform both roles. Discovery prepares the next package or runtime slice; delivery builds and validates the current slice.

## Tracks

| Track | Scope | Current focus | Output |
|---|---|---|---|
| Discovery | Prepare next work item before implementation. | EP001 render-review rubric, publish-quality policy shape, Cockpit install/action mapping. | Ready item with acceptance criteria and validation path. |
| Delivery | Implement and validate current work item. | Construction -> IOC acceleration lane. | Code/doc/content artifact with deterministic checks recorded. |

## Definition of Ready

A work item may enter Delivery when it has:

- clear acceptance criteria,
- affected components or artifacts identified,
- compliance and human-gate implications listed,
- deterministic checks named or an explicit no-check rationale,
- no hidden dependency on paid generation or public publishing.

## Definition of Done

A work item is complete when:

- code/docs/content are updated,
- relevant tests or smoke checks pass,
- AIWG index is rebuilt after artifact changes,
- status/report artifact records the result,
- public/publish/spend actions remain gated unless explicitly approved.

## Current Discovery Queue

1. EP001 final-render review rubric and first review record.
2. First-100 Postiz draft publish-quality policy fields.
3. Cockpit status/action/approval mapping for Aflack.
4. Analytics refresh policy for zero-signal and real-signal snapshots.
5. IOC requirement-code-test traceability shape.

## Current Delivery Queue

1. Add Cockpit-facing machine-readable status for daemon/loop/publish queue/analytics.
2. Add CLI runner tests for high-value commands.
3. Refresh traceability matrix after the 47-test suite.
4. Keep analytics/economics refresh ready for when real metrics exist.
5. Preserve public publish, account action, DM/comment/follow, ad-spend, and broader daemon-autonomy gates.

## Synchronization

At the start of each work slice:

1. Read @.aiwg/reports/status-assessment.md.
2. Pick one item from Discovery or Delivery.
3. Confirm its validation path.
4. Build the smallest useful slice.
5. Run deterministic checks.
6. Update the relevant `.aiwg/` artifact.
