# Iteration Plan 004 — Commit, Prune, Measure, Close the Loop

**Date**: 2026-07-07  
**Phase**: Construction  
**Mode**: dual-track construction stabilization and transition-readiness preparation  
**Decision target**: keep Construction moving; do **not** start Construction → Transition until IOC blockers close.

## Why this iteration exists

Iteration 003 completed the minimum technical gates for continued Construction,
but the project is still not Transition-ready. The remaining risk is no longer
basic code validation; it is operational closure:

- the workspace has many real changes plus generated/cache artifacts that need a
  clean checkpoint policy;
- status artifacts must match actual code, tests, CLI commands, and migrations;
- EP001 is generated and privately drafted, but final render/QC/operator
  approval is still open;
- analytics snapshots are still zero, so the ROI scale gate correctly blocks
  scale-up;
- Construction → Transition requires production/handover/hypercare artifacts
  that are intentionally not present yet.

## Objectives

1. **Workspace checkpoint discipline** — classify dirty/untracked files as commit,
   generated, or operator-review before any handoff to another session.
2. **Docs/code/test/CLI/migration reconciliation** — no gate claim may remain
   doc-only; each claimed control must exist in code, tests, CLI help, or SQL.
3. **Validation proof** — rerun lint, format, typecheck, compile, and full pytest.
4. **Operational smoke proof** — verify local DB status, compliance smoke,
   analytics status, economics status, and ROI scale gate behavior.
5. **EP001 closure plan** — keep public publishing blocked, but define the exact
   final-render/QC/approval path.
6. **Analytics/ROI closure plan** — define what must be recorded before scale or
   transition reconsideration.
7. **Parallel Claude handoff** — provide a safe prompt that lets another Claude
   Code session work in parallel without overwriting this session.
8. **Index refresh** — rebuild/sync AIWG indexes after artifact updates.

## Work items

| ID | Item | Track | Priority | Acceptance criteria | Status |
|---|---|---|---|---|---|
| D4-001 | Deep status sweep | Delivery | Must | Current git state, AIWG status, gate docs, CLI, and DB status captured | Done |
| D4-002 | Reconcile stale validation counts | Delivery | Must | Gate/status docs reflect latest 189-test validation, not older 95/110-test intermediate runs | Done |
| D4-003 | Workspace hygiene policy | Delivery | Must | Commit/generated/prune/operator-review categories documented | Done |
| D4-004 | Full validation suite | Delivery | Must | Ruff, format, mypy, compile, pytest pass | Done — 189 tests pass, 82.85% coverage |
| D4-005 | Operational smoke checks | Delivery | Must | DB, compliance, analytics, economics, ROI gate outputs recorded | Done — ROI gate blocks scale because snapshots=0 |
| X4-001 | EP001 close-loop runbook | Discovery | Must before Transition | Final render/QC/approval/publish boundaries explicit | Done |
| X4-002 | Analytics evidence plan | Discovery | Must before scale | Manual/Postiz analytics ingestion path and minimum evidence defined | Done |
| X4-003 | Claude parallel prompt | Discovery | Should | Prompt limits file ownership and requires verification before claims | Done |

## Current proof from this session

Validation command:

```bash
uv run ruff check src tests scripts && \
uv run ruff format --check src tests scripts && \
uv run mypy src && \
uv run python -m compileall -q src scripts && \
uv run python -m pytest tests/ --tb=short -q
```

Result:

- Ruff: PASS
- Format check: PASS — 48 files already formatted
- Mypy: PASS — 22 source files checked
- Compile: PASS — src and scripts
- Pytest: PASS — 189 passed
- Coverage: 82.85% actual vs 40% required

Operational smoke result:

- `docker ps --filter name=pggraph`: `pggraph` is up and bound to `127.0.0.1:55432`.
- `uv run aflack db-status`: `graph`, `pg_cron`, and `vector` extensions present; `analytics_snapshots` table present.
- `uv run aflack compliance-smoke`: safe sample allowed; unsafe sample blocked.
- `uv run aflack analytics-status`: `snapshots=0`, revenue/conversions/views all zero.
- `uv run aflack economics-status`: cost/revenue/margin all zero.
- `uv run aflack roi-scale-gate`: `scale_allowed=False`; reason is ROI unmeasured/no analytics snapshots.

## Workspace hygiene categories

### Commit candidates

These represent product/code/test/docs work and should be reviewed together as a
single green checkpoint or split into coherent commits:

- `src/aflack/cli.py`
- `src/aflack/economics.py`
- `src/aflack/feature_flags.py`
- `tests/test_economics.py`
- new test files for CLI, resilience, metrics, feature flags, dead flags,
  product analytics, build performance, daemon cycle, learning unit, logging,
  PII, N+1, and error tracking
- `db/migrations/005_analytics_snapshots.sql`
- `.github/workflows/ci.yml`
- `.github/workflows/deploy-staging.yml`
- `scripts/detect_dead_flags.py`
- `scripts/track_build_performance.py`
- `README.md`
- `docs/monitoring.md`
- `.aiwg/architecture/adr-0007-polygres-system-of-record-memory-tiers.md`
- `.aiwg/creator-commerce-ops/workflows/proposal-to-file-approval.md`
- Iteration 003/004 status, gate, and report artifacts
- marketing/loadout-lab and vice-signal package status artifacts

### Generated / usually do not commit unless policy says otherwise

- `.coverage`
- `.aiwg/.index/` if AIWG indexes are treated as regenerable local artifacts

### Policy decision needed

- `uv.lock`: commit if this project standardizes on reproducible `uv`-based
  application/tooling installs; otherwise document why it remains untracked.
  Recommendation: **commit `uv.lock`** because CI and local operator sessions use
  `uv run` and deterministic dependency resolution matters.

### Operator-review before public action

- final render approval
- public publish/scheduling approval
- paid generation or additional credit spend
- account/channel/OAuth settings
- comment/DM/follow automation
- any scale-up decision

## EP001 close-loop plan

1. Assemble final EP001 render with VO, captions, music/audio rights, unified
   grade, and required disclosure.
2. Run final render compliance/QC against the package and platform policy.
3. Record the QC result in `.aiwg/marketing/vice-signal/`.
4. Ask the operator for final-render approval.
5. Only after final-render approval, ask separately for public publish or
   scheduling approval.
6. Do not publish from an agent session without explicit approval in that turn.

## Analytics and ROI closure plan

Minimum evidence before scale-up:

1. At least one analytics snapshot linked to the queue/post/package.
2. CTA/conversion/revenue fields captured or explicitly zero.
3. Cost ledger updated for generated media/operator/tool spend.
4. `uv run aflack economics-status` shows current margin.
5. `uv run aflack roi-scale-gate` passes with the configured thresholds.

Example commands after approved publish/private-test signal:

```bash
uv run aflack analytics-record-manual youtube \
  --views <views> \
  --likes <likes> \
  --comments <comments> \
  --shares <shares> \
  --saves <saves> \
  --clicks <clicks> \
  --conversions <conversions> \
  --revenue <revenue>

uv run aflack analytics-status
uv run aflack economics-status
uv run aflack roi-scale-gate
```

## Construction → Transition decision

Do **not** start `flow-construction-to-transition` yet. The flow requires
Construction exit / OCM criteria and later production deployment, support
handover, operations handover, hypercare, and PRM artifacts. The correct next
step is still Construction Iteration 004 close-loop work.

Transition can be reconsidered only after:

- final render/QC/operator approval is closed;
- public publish or approved private-test signal is closed;
- analytics snapshots exist;
- ROI gate allows scale or an explicit waiver is recorded;
- IOC is rerun and changed from NO-GO to GO/conditional GO for Transition.

## Exit criteria

- [x] Full validation suite passes.
- [x] Operational smoke checks completed.
- [x] ROI gate verified to block unmeasured scale.
- [x] AIWG engagement/status verified.
- [x] Stale gate/status artifact counts reconciled.
- [x] Deep sweep report written.
- [x] Claude parallel prompt written.
- [x] AIWG index rebuilt/synced after this iteration's artifact updates.
- [ ] Workspace commit/prune policy confirmed or executed.
