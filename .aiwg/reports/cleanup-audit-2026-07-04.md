# Cleanup Audit — 2026-07-04

**Skill**: `cleanup-audit`  
**Scope**: `src/`, `tests/`, `db/migrations/`, `scripts/`, `.aiwg/creator-commerce-ops`  
**Mode**: dry-run audit; no deletions performed  
**Status**: PASS WITH REVIEW ITEMS

## Summary

| Metric | Count | Status |
|---|---:|---|
| Python source modules scanned | 11 | PASS |
| Test files scanned | 3 | PASS |
| SQL migrations scanned | 4 | PASS |
| Project-local manifest files | 1 | PASS |
| High-confidence removable files | 0 | PASS |
| Stale manifest entries | 0 | PASS |
| Unused dependencies | 0 found | PASS |
| Review-only possible cleanup items | 4 | TRACK |

## Dependency audit

| Dependency | Evidence |
|---|---|
| `psycopg[binary]` | Used by `aflack.db`. |
| `python-dotenv` | Used by `aflack.config`. |
| `typer` | Used by `aflack.cli`. |

No unused `pyproject.toml` dependencies were found.

## Manifest audit

`.aiwg/creator-commerce-ops/manifest.json` matches the project-local bundle on disk:

| Component | Manifest count | Actual files | Status |
|---|---:|---:|---|
| agents | 5 | 5 | PASS |
| rules | 5 | 5 | PASS |
| skills | 6 | 6 | PASS |
| workflows | 4 | 4 | PASS |

## Dead-code / orphan-file assessment

No high-confidence dead Python module was identified. Several modules are not directly unit-tested, but they are documented architectural surfaces or CLI-backed runtime modules and should not be removed:

| File | Reason to keep |
|---|---|
| `src/aflack/memory.py` | ADR-0003/ADR-0007 memory interface; upcoming memory-consolidation work. |
| `src/aflack/economics.py` | CLI economics rollup and future results ingestion. |
| `src/aflack/compliance.py` | Deterministic compliance gate used by CLI and content preflight. |
| `scripts/com.aflack.improve-daemon.plist` | launchd scheduler candidate for safe improvement-daemon ticks. |

## Review items

| ID | Item | Action |
|---|---|---|
| CLEAN-001 | `.aiwg/marketing/vice-final/reference-footage/frames/` contains many real-event frame files. | Keep only if the operator accepts the Tier 3 override risk record; otherwise quarantine/remove in a separate explicit cleanup. |
| CLEAN-002 | `.aiwg/working/postiz/` contains local Postiz working config while cloud Postiz is active. | Decide whether to keep as fallback or archive after cloud draft path is proven. |
| CLEAN-003 | `.aiwg/working/aside-scans/sample-scan.json` is sample input. | Keep as fixture if tests will use it; otherwise archive later. |
| CLEAN-004 | No root README/operator quickstart exists. | Optional documentation cleanup after Construction command surface stabilizes. |

## Safety decision

No files were deleted. Cleanup removals require explicit `--fix`-style approval and should run after the operator decides whether local Postiz fallback and Tier 3 reference frames remain in scope.

## References

- @pyproject.toml
- @.aiwg/creator-commerce-ops/manifest.json
- @src/aflack/memory.py
- @src/aflack/economics.py
- @src/aflack/compliance.py
- @scripts/com.aflack.improve-daemon.plist
- @.aiwg/security/decision-memo-event-reference-policy.md
