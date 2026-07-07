# Traceability Report — 2026-07-04

**Skill**: `traceability-check`  
**Scope**: `.aiwg/requirements`, `.aiwg/architecture`, `src/aflack`, `tests`  
**Status**: CONDITIONAL PASS

## Executive summary

The project has strong artifact-level traceability for architecture and construction readiness, but requirement-row-to-code/test traceability is still coarse. Requirement IDs are defined in one table in `.aiwg/requirements/mvp-requirements.md`; they are not yet split into individually indexed requirement artifacts or referenced directly in code/tests.

## Index status

| Metric | Value |
|---|---:|
| Project artifacts indexed | 104 |
| ADRs indexed | 7 |
| Requirement artifacts indexed by AIWG type | 0 |
| Requirements discovered by direct scan | 19 FR, 10 NFR, 11 US |

## Requirements-to-implementation matrix

| Requirement group | Implementation evidence | Test evidence | Status |
|---|---|---|---|
| FR-001 local event store | `db/migrations/001_init.sql`, `aflack db-status` | DB status smoke | Covered |
| FR-002 cost ledger | `cost_ledger`, `aflack economics-status` | CLI smoke | Partial |
| FR-003 lessons memory | `src/aflack/memory.py`, ADR-0007 | No direct tests | Partial |
| FR-004 beachhead niche | `aflack set-beachhead`, planning artifacts | Manual/DB | Partial |
| FR-005 personas | `.aiwg/marketing/strategy/gta6-personas.md` | Documented only | Partial |
| FR-006 official reference provenance | reference packs and compliance docs | Content package preflight | Covered |
| FR-007 footage/same-seed block | `src/aflack/compliance.py`, security docs | `aflack compliance-smoke` | Covered by smoke; add unit tests |
| FR-008 publish queue | `db/migrations/002_publish_queue.sql`, `PostizPublisher.enqueue` | Publishing payload test covers preview; enqueue untested | Partial |
| FR-009 Claude director runtime | ADR-0004, runbook, packages | Manual run reports | Covered by artifact |
| FR-010 Higgsfield wrapper | Not implemented | None | Gap |
| FR-011 Virality Predictor wrapper | Not implemented | None | Gap |
| FR-012 Postiz publish after approval | `PostizPublisher`, preview command, integrations | URL/payload tests; no real draft submit test | Partial |
| FR-013 results capture | `results` table exists | No real ingestion tests | Gap |
| FR-014 lead magnets/funnel keywords | `db/migrations/003_funnel_layer.sql` | DB status smoke | Partial |
| FR-015 YouTube-native funnel delivery | content packages and strategy docs | Manual review | Partial |
| FR-016 Jarvis data products | ADR-0005, ADR-0007, learning layer | Learning tests partial | Partial |
| FR-017 human-gated loop | ADR-0005, daemon hard blocks | Unit/smoke partial | Partial |
| FR-018 persona-free formats | ADR-0006, director routine | Documented only | Partial |
| FR-019 human approval for actions | ADR-0005, daemon/runtime docs | Smoke via daemon blocked-actions trace; no direct unit | Partial |

## Code-to-test matrix

| Source module | Direct tests | Status |
|---|---|---|
| `aside_scan.py` | `tests/test_aside_scan.py` | Covered for pure logic |
| `learning.py` | `tests/test_learning.py` | Covered for pure logic |
| `publishing.py` | `tests/test_publishing.py` | Covered for URL/payload behavior |
| `compliance.py` | CLI smoke only | Add unit tests |
| `memory.py` | None | Add DB/mocked tests |
| `economics.py` | CLI smoke only | Add DB/mocked tests |
| `daemon.py` | Improvement cycles exercised manually; no unit tests | Add daemon-cycle tests before autonomy expansion |
| `tracing.py` | Used by scan/daemon; no direct tests | Add trace write/read test |
| `cli.py` | Manual/command smoke only | Add Typer runner tests for new commands |

## Gaps

1. Requirement IDs are not embedded in source/test comments or metadata.
2. AIWG index does not classify rows inside `mvp-requirements.md` as separate requirement artifacts.
3. Higgsfield generation, Virality Predictor, real result ingestion, and real Postiz draft submit remain construction gaps.
4. Several runtime modules are smoke-tested but lack direct unit tests.

## Recommendations

1. Add a `requirements-traceability-matrix.md` or split major FR/NFR/US items into individual artifacts before IOC.
2. Add direct unit tests for compliance, memory, economics, daemon, and tracing before expanding daemon autonomy.
3. Add requirement IDs to tests where useful, for example `FR-007` in compliance tests and `FR-012` in publishing tests.
4. Treat current traceability as sufficient for controlled Construction, not for Transition/IOC.

## References

- @.aiwg/requirements/mvp-requirements.md
- @.aiwg/architecture/software-architecture-document.md
- @.aiwg/architecture/adr-0005-human-gated-jarvis-content-agent-orchestration.md
- @.aiwg/architecture/adr-0007-memory-system-of-record-and-bakeoff.md
- @src/aflack/compliance.py
- @src/aflack/publishing.py
- @src/aflack/daemon.py
- @tests/test_publishing.py
