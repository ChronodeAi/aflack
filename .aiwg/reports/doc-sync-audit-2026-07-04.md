# Doc Sync Audit — 2026-07-04

**Skill**: `doc-sync`  
**Direction**: code-to-docs  
**Scope**: `.aiwg/`, `src/`, `tests/`, `db/migrations/`, `scripts/`  
**Status**: PASS WITH MINOR FIXES APPLIED

## Executive summary

| Category | Count | Status |
|---|---:|---|
| Critical drift | 0 | PASS |
| High drift | 0 | PASS |
| Medium drift | 3 | FIXED |
| Low drift / follow-up | 3 | TRACK |

The main documentation drift was stale construction-readiness language from earlier in the day. Reports still referenced ADR-0001 through ADR-0004 or ADR-0006 after ADR-0007 had been added, and one ABM report still said no automated tests existed after the suite had grown to 14 unit tests.

## Fixes applied

| ID | File | Drift | Fix |
|---|---|---|---|
| DOC-DRIFT-001 | `.aiwg/reports/abm-validation-report.md` | Architecture baseline said ADR-0001 through ADR-0004. | Updated to ADR-0001 through ADR-0007 and described the current seven-decision baseline. |
| DOC-DRIFT-002 | `.aiwg/reports/abm-validation-report.md` | Test approach said no automated suite existed. | Updated to reflect the current unit coverage areas and compliance smoke posture. |
| DOC-DRIFT-003 | `.aiwg/reports/framework-deliverance-handoff-2026-07-04.md` | Framework surface said ADR-0001 through ADR-0006. | Updated to ADR-0001 through ADR-0007. |
| DOC-DRIFT-004 | `.aiwg/reports/iteration-0-completion.md` | Listed Postiz URL tests and payload preview as remaining work. | Moved those items to completed-after-report and left remaining infrastructure work. |
| DOC-DRIFT-005 | `.aiwg/testing/test-strategy.md` | Unit-test section was still aspirational and missed current suite. | Updated to reflect current 14-test suite and remaining candidates. |

## Remaining follow-ups

| ID | Area | Finding | Recommendation |
|---|---|---|---|
| DOC-FOLLOW-001 | Traceability metadata | Requirement IDs live inside `.aiwg/requirements/mvp-requirements.md`; the AIWG index does not type each FR/NFR/US row as separate requirement artifacts. | Add a traceability matrix or split high-priority requirements into individual artifacts if stricter index-level traceability is needed. |
| DOC-FOLLOW-002 | Reports | Older milestone reports are snapshots and may intentionally preserve earlier state. | Keep snapshot reports but add addenda instead of rewriting historical evidence unless the report is used as current status. |
| DOC-FOLLOW-003 | README/root docs | No root README exists for the Python CLI. | Optional: add a concise operator README once Construction commands stabilize. |

## Validation run

- `aiwg index build`: 104 project artifacts indexed.
- `aiwg index query --type adr --json`: 7 ADRs found.
- `.venv/bin/python -m compileall -q src`: pass.
- `.venv/bin/python -m unittest discover -s tests -v`: 14 tests pass.
- `.venv/bin/aflack db-status`: graph/vector/cron extensions and pipeline tables present.
- `.venv/bin/aflack compliance-smoke`: allowed sample passes, prohibited sample blocks.

## Decision

Documentation is synchronized enough to continue controlled Construction. Remaining drift is traceability granularity, not blocking correctness.

## References

- @.aiwg/reports/abm-validation-report.md
- @.aiwg/reports/framework-deliverance-handoff-2026-07-04.md
- @.aiwg/reports/iteration-0-completion.md
- @.aiwg/testing/test-strategy.md
- @.aiwg/architecture/software-architecture-document.md
