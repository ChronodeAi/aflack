# Iteration Plan 003 — Stabilize, Measure, Gate

**Date**: 2026-07-07  
**Phase**: Construction  
**Goal**: Restore green validation, reconcile stale status, close the first
measurable content loop, and prepare IOC gate inputs before any
Construction → Transition orchestration.

This is the promoted, tracked version of the working handoff at
`.aiwg/working/construction-orchestration/iteration-003-stabilize-measure-gate.md`.

## Objectives

1. Make the documented pytest command pass, including coverage.
2. Keep `.aiwg/` status artifacts consistent with actual EP001/Postiz state.
3. Finalize EP001 render/QC/approval state without public publishing.
4. Implement analytics/results ingestion before scale.
5. Implement a minimum ROI sentinel gate before scale.
6. Prepare the Loadout Lab affiliate package and IOC gate checklist.

## Work items

| ID | Item | Track | Priority | Acceptance criteria | Status |
|---|---|---|---|---|---|
| D3-001 | Recover validation/coverage gate | Delivery | Must | pytest passes at `--cov-fail-under=40` without weakening thresholds | Done — latest reconciliation: 189 tests pass, coverage 82.85% |
| D3-002 | Reconcile SDLC status artifacts | Delivery | Must | Iteration 1/2 plans, test strategy, and readiness match actual EP001/Postiz state | Done |
| D3-003 | Close EP001 package state | Delivery | Must | Explicit final-render/QC/approval/publish checklist recorded; no public publish | Done (status recorded) |
| D3-004 | Analytics/results ingestion slice | Delivery | Must before scale | Post metrics link to queue row, post ID, package, CTA keyword, cost ledger; tested path | Done — migration and CLI ingestion path verified by tests |
| D3-005 | ROI sentinel minimum gate | Delivery | Must before scale | Scale blocked until a hook->CTA->lead-magnet->conversion loop is measured positive; tested | Done — `roi-scale-gate` blocks unmeasured/non-positive margin |
| X3-001 | Loadout Lab affiliate package | Discovery | Should | Script/shot list/CTA/lead magnet, affiliate disclosure, no guaranteed-results claims, compliance checklist, economics estimate | Done |
| X3-002 | Proposal-to-file approval workflow | Discovery | Should | Human approval marker + safe patch path + trace event; no autonomous skill/rule edits | Done |
| X3-003 | Live Aside extraction loop | Discovery | Should | Logged-in extraction artifact imported, dedupe/proof validated, insight/proposal loop confirmed | Done |

## Verification commands

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src
uv run python -m compileall -q src
uv run python -m pytest tests/ --tb=short -q
```

## Exit criteria

- [x] Coverage/test gate passes.
- [x] Lint, format, mypy, compile pass.
- [x] SDLC status artifacts reconciled.
- [x] EP001 package state explicit; human gates preserved.
- [x] Analytics/results ingestion implemented or explicitly deferred with blocker.
- [x] ROI sentinel minimum gate implemented or explicitly deferred with blocker.
- [x] Public publish remains unexecuted unless separately approved.

## After this iteration

Run an SDLC gate check for delivery, test-coverage, security, and
construction/IOC. Only if IOC passes should `flow-construction-to-transition`
be started.

## Implementation update — 2026-07-07

Implemented during this orchestration pass:

- Added `db/migrations/005_analytics_snapshots.sql`, creating the
  `analytics_snapshots` table used by existing Postiz/manual analytics
  ingestion commands.
- Added `scale_gate_decision(...)` in `src/aflack/economics.py`.
- Added CLI command `aflack roi-scale-gate`.
- Added economics tests for unmeasured, zero-margin, positive-margin, and
  invalid-threshold cases.
- Updated README command list.

Validation:

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src
uv run python -m compileall -q src
uv run python -m pytest tests/ --tb=short -q
```

Result: **PASS** — latest reconciliation PASS: 189 tests, 82.85% coverage.

## Discovery update — 2026-07-07

Completed during this orchestration pass:

- Created `.aiwg/marketing/loadout-lab/episode-001-affiliate-package.md`
  with script, shot list, CTA keyword `LOADOUT`, affiliate disclosure, no
  guaranteed-results claims, compliance checklist, and economics estimate.
- Created `.aiwg/creator-commerce-ops/workflows/proposal-to-file-approval.md`
  so daemon proposals require an explicit human approval marker before file
  edits.
- Created `.aiwg/reports/aside-live-extraction-status-2026-07-07.md`, recording
  the live Aside extraction/import/proposal loop as complete for this
  iteration and preserving read-only account boundaries.

Remaining gate before Transition consideration:

- EP001 final render/QC/operator approval.
- Explicit public publish decision if the operator wants to proceed.
- Delivery/test/security/construction IOC gate check completed:
  - Delivery: PASS.
  - Test coverage: PASS.
  - Security/compliance: PASS WITH ACTIVE HUMAN GATES.
  - IOC: CONDITIONAL PASS for continued Construction; NO-GO for Transition.
