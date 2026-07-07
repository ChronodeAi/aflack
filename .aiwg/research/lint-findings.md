# Research Corpus Lint Report

**Date**: 2026-07-05
**Command**: `aiwg lint .aiwg/research/ --ruleset research --format full`
**Result**: PASS (0 errors, 0 warnings)

## Summary

All 8 research files pass the research ruleset lint after frontmatter alignment and file renames.

## Fixes applied

| Issue | Count before | Fix |
|---|---|---|
| citation-resolves (filename mismatch) | 5 errors | Renamed findings to bare REF-NNN.md (REF-001-memory-system-research.md to REF-001.md, etc.) |
| grade-present (missing flat field) | 4 errors | Added `grade_rating` field matching `quality_assessment.grade` |
| provenance-present (missing fields) | 8 errors | Added `documented_date` and `acquisition_method` to all findings |
| ref-frontmatter (missing fields) | 16 errors | Added `authors` (string), `publication_type`, `tags`, `status` to all findings |
| ref-id-format (descriptive filenames) | 4 warnings | Resolved by rename to bare REF-NNN.md |
| grade_rating format (REF-004) | 1 warning | Changed `low-to-moderate` to `low` (closest allowed value) |
| status format | 4 warnings | Changed `active` to `quality-assessed` (allowed pattern) |
| publication_type format | 4 warnings | Changed `technical_report` to `technical-report` (hyphenated) |

## Corpus state after fixes

| Dimension | Status |
|---|---|
| Findings | 4 (REF-001 through REF-004) |
| Sources | 2 (GTA6 reference packs) |
| Syntheses | 1 (affiliate-content-pipeline-brief) |
| GRADE distribution | 0 high, 3 moderate, 1 low, 0 unrated |
| Cross-citations | 6 edges (REF-001 to REF-002/REF-003, REF-002 to REF-001, REF-003 to REF-001/REF-004, REF-004 to REF-003) |
| Source integration | 2 sources referenced by REF-004 |
| Lint | PASS (0 errors, 0 warnings) |
| Citation graph index | Not built (tooling expects different corpus layout) |

## Remaining follow-ups

1. Build citation graph index when tooling supports this corpus layout.
2. Add more findings as research expands beyond the initial 4.
3. Consider promoting `grade_rating` values to `high` as research quality improves.
