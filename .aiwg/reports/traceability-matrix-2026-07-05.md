# Requirements Traceability Matrix — 2026-07-05

**Scope**: Functional requirements FR-001 through FR-021 (mvp-requirements.md)
**Generated**: 2026-07-05
**Status**: Controlled Construction baseline — closes IOC gap from traceability-2026-07-05.md

## How to read this matrix

| Column | Meaning |
|---|---|
| ID | Requirement identifier from mvp-requirements.md |
| Requirement (summary) | Short description |
| Source file(s) | Primary implementation module(s) in `src/aflack/` |
| Test file(s) | Unit/integration test file(s) that cover this requirement |
| Status | **covered** = direct tests exist; **partial** = some coverage, gaps remain; **gap** = no automated tests |

---

## Functional Requirements

| ID | Requirement (summary) | Source file(s) | Test file(s) | Status |
|---|---|---|---|---|
| FR-001 | Store core pipeline entities in local event store | `db.py`, `cli.py` (migrate) | `tests/test_integration.py` | partial |
| FR-002 | Track costs for generation, tokens, tools, operator time | `economics.py`, `cli.py` (cost_record) | `tests/test_economics.py` | covered |
| FR-003 | Maintain episodic/semantic/procedural lessons | `memory.py`, `learning.py`, `cli.py` (memory_consolidate, insight_add) | `tests/test_memory.py`, `tests/test_learning.py` | covered |
| FR-004 | Lock Beachhead A: GTA6 AI-persona gaming, YouTube-first | `cli.py` (set_beachhead) | `tests/test_cli_requirements.py` (set_beachhead) | covered |
| FR-005 | Maintain two active public personas (Vice Signal, Loadout Lab) | `cli.py` (creator_add, creator_proof) | `tests/test_cli_requirements.py` (creator_add, creator_proof) | covered |
| FR-006 | Preserve official GTA6 trailer provenance as references only | `compliance.py` | `tests/test_compliance.py` | partial |
| FR-007 | Block use of Rockstar pre-release footage / same-seed remixes | `compliance.py` | `tests/test_compliance.py`, `tests/test_cli.py` (compliance_smoke_json), `tests/test_cli_requirements.py` (compliance_smoke_text) | covered |
| FR-008 | Queue compliance-approved creatives for Postiz scheduling | `publishing.py`, `cli.py` (publish_smoke, publish_queue_status) | `tests/test_publishing.py`, `tests/test_cli.py` (publish_queue_status_json), `tests/test_cli_requirements.py` (publish_queue_text) | covered |
| FR-009 | Run the video director via Claude Code CLI `claude-fable-5` | ADR-0005 (architecture decision only) | — | gap |
| FR-010 | Generate original visuals via Higgsfield, not Rockstar footage | `publishing.py`, `economics.py` | `tests/test_economics.py` (cost tracking) | partial |
| FR-011 | Score generated videos before publishing (prompt quality + human review) | `prompt_quality.py`, `draft_review.py`, `cli.py` (prompt_quality) | `tests/test_prompt_quality.py`, `tests/test_draft_review.py`, `tests/test_cli.py` (prompt_quality_json_fail), `tests/test_cli_requirements.py` (prompt_quality_json_pass, prompt_quality_text_pass) | covered |
| FR-012 | Publish via Postiz after compliance approval (draft path only) | `publishing.py`, `cli.py` (postiz_submit, postiz_preview) | `tests/test_publishing.py`, `tests/test_cli.py` (publish_queue_status_json), `tests/test_cli_requirements.py` (publish_queue_text_with_item) | covered |
| FR-013 | Capture post-publish metrics into analytics_snapshots | `analytics.py`, `cli.py` (analytics_record_manual, analytics_status) | `tests/test_analytics.py`, `tests/test_integration.py`, `tests/test_cli.py` (analytics_status_json), `tests/test_cli_requirements.py` (analytics_status_text) | covered |
| FR-014 | Maintain lead magnets + one-word funnel keywords | `db.py` (schema: funnel_keywords table via migration) | — | gap |
| FR-015 | YouTube-native funnel delivery before IG/DM automation | ADR accepted; no code gate yet | — | gap |
| FR-016 | Maintain Jarvis data products: hook library, cost ledger, compliance record, etc. | `db.py`, `economics.py`, `learning.py`, `analytics.py` | `tests/test_economics.py`, `tests/test_learning.py`, `tests/test_analytics.py` | partial |
| FR-017 | Run content-agent loop as human-gated orchestration | `daemon.py`, `cli.py` (daemon_status, improve_cycle) | `tests/test_daemon.py`, `tests/test_cli.py` (daemon_status_json), `tests/test_cli_requirements.py` (daemon_status_text_never_run, daemon_status_text_with_run) | covered |
| FR-018 | Allow persona-free formats when benchmark evidence warrants | ADR accepted; no automated gate | — | gap |
| FR-019 | Keep publish, DM, follow, paid actions behind explicit human approval | `daemon.py` (blocked_actions), `draft_review.py`, `cli.py` (draft_review_record) | `tests/test_cli.py` (draft_review_record_never_authorizes_publish, draft_review_status_json) | covered |
| FR-020 | Expose machine-readable local status for Cockpit/control-plane | `cli.py` (daemon_status --json, analytics_status --json, publish_queue_status --json, compliance_smoke --json, prompt_quality --json, loop_status --json) | `tests/test_cli.py` (all *_json tests), `tests/test_cli_requirements.py` (all text-mode tests) | covered |
| FR-021 | Block safe-but-boring paid generation prompts before spend | `prompt_quality.py`, `cli.py` (prompt_quality) | `tests/test_prompt_quality.py`, `tests/test_integration.py`, `tests/test_cli.py` (prompt_quality_json_fail), `tests/test_cli_requirements.py` (prompt_quality_json_pass, prompt_quality_text_pass) | covered |

---

## Non-Functional Requirements (summary)

| ID | Requirement | Source evidence | Status |
|---|---|---|---|
| NFR-001 | Local-first | Postgres on localhost; no cloud data store required | covered |
| NFR-002 | Throughput toward 20 videos/day | Architecture + analytics loop; not load-tested yet | gap |
| NFR-003 | 100% pre-publish gate pass required | `compliance.py` gate enforced in publish path | partial |
| NFR-004 | Cost visibility: every spend written to cost_ledger | `economics.py`, `cli.py` (cost_record) | covered |
| NFR-005 | Memory anti-rot (dedup + validity windows) | `learning.py`, `memory.py` | covered |
| NFR-006 | Source-of-truth ownership in local DB | `db.py` schema; analytics_snapshots design | covered |
| NFR-007 | Lean role scope | ADR, AIWG persona config | partial |
| NFR-008 | Platform safety via Postiz + human approval | `publishing.py`, daemon blocked_actions | covered |
| NFR-009 | Portability of audience/data | Schema design; no export tooling yet | gap |
| NFR-010 | Virality-first learning | `analytics.py`, `draft_review.py`, learning layer | partial |

---

## Coverage Summary

| Status | Functional | Non-functional |
|---|---|---|
| covered | 13 | 5 |
| partial | 4 | 4 |
| gap | 4 | 1 |
| **Total** | **21** | **10** |

### Covered FR-IDs (13)
FR-002, FR-003, FR-004, FR-005, FR-007, FR-008, FR-011, FR-012, FR-013, FR-017, FR-019, FR-020, FR-021

### Partial FR-IDs (4)
FR-001, FR-006, FR-010, FR-016

### Gap FR-IDs (4)
FR-009, FR-014, FR-015, FR-018

---

## Accepted Exceptions for Construction Phase

The following gaps are accepted for Controlled Construction continuation and do NOT block the current iteration:

| ID | Gap reason | Accepted because |
|---|---|---|
| FR-009 | No automated test for `claude-fable-5` director | External CLI invocation; tested manually via session runs |
| FR-014 | Funnel keyword schema not directly tested | Schema exists; no runtime logic gate to verify automatically |
| FR-015 | YouTube-native funnel delivery has no code gate | Architecture-only decision; operator executes manually |
| FR-018 | Persona-free format switch has no automated gate | Policy decision recorded in ADR; no conditional code path to test |

---

## New Tests Added to Close IOC Gap (2026-07-05)

File: `tests/test_cli_requirements.py`

| Test method | FR-IDs covered | Coverage type |
|---|---|---|
| `test_daemon_status_text_never_run` | FR-020 | CLI text-mode output, never-run daemon state |
| `test_daemon_status_text_with_run` | FR-020 | CLI text-mode output, daemon with latest run |
| `test_analytics_status_text_output` | FR-013, FR-020 | CLI text-mode output, analytics rollup |
| `test_publish_queue_status_empty_text_output` | FR-008, FR-020 | CLI text-mode output, empty queue |
| `test_publish_queue_status_text_with_item` | FR-008, FR-012, FR-020 | CLI text-mode output, queue item |
| `test_prompt_quality_json_pass` | FR-011, FR-021 | CLI JSON output, passing prompt |
| `test_prompt_quality_text_pass` | FR-011, FR-021 | CLI text-mode output, passing prompt |
| `test_compliance_smoke_text_output` | FR-007, FR-020 | CLI text-mode output, allow/block samples |
| `test_set_beachhead_locks_gta6_youtube_first_niche` | FR-004 | CLI setup command, DB write mocked |
| `test_creator_add_normalizes_empty_optional_fields` | FR-005 | CLI creator registration command, DB helper mocked |
| `test_creator_proof_reports_computed_credibility` | FR-005 | CLI creator proof command, credibility helper mocked |

---

## Next steps to reach strict IOC traceability

1. Add `# FR-xxx` inline comments to critical source functions (e.g., `check_publish_item`, `check_short_asset_prompt`).
2. Add FR-014 funnel keyword CRUD tests once runtime logic is added.
3. Adopt a behavioral specification layer (Layer 2/3) for the most complex gates before Transition.
