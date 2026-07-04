# Iteration Plan 001 — Cloud Postiz Draft Loop + Safety Tests

**Date**: 2026-07-04  
**Phase**: Construction  
**Goal**: Make the first safe cloud Postiz draft path reliable without public publishing.

## Objectives

1. Normalize the Postiz adapter for cloud and local self-hosted modes.
2. Verify connected cloud integrations from the CLI.
3. Add safeguards/tests around API URL construction and draft payloads.
4. Prepare one safe draft publish package for YouTube.
5. Update security/status artifacts to reflect the cloud Postiz pivot.

## Work items

| ID | Item | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| I1-001 | Cloud Postiz base URL support | Must | `POSTIZ_BASE_URL=https://api.postiz.com` lists integrations; local base remains supported. | Done |
| I1-002 | Document cloud vs local Postiz config | Must | `.env.example` and SDLC reports explain cloud/local values. | Done |
| I1-003 | Add URL normalization tests | Must | Unit tests cover cloud root, cloud API base, local root, and local API base. | Done |
| I1-004 | Add Postiz payload preview/dry-run | Should | Operator can inspect payload before draft submission. | Done |
| I1-005 | Submit first Postiz draft | Human-gated | Queue item and target integration confirmed; draft created, not public. | Pending |
| I1-006 | Security gate refresh | Must | Gate reflects cloud Postiz connected and local-only posture. | Done |

## Verification commands

```bash
source .venv/bin/activate
python3 -m compileall -q src
aflack postiz-integrations
aflack compliance-smoke
aflack economics-status
```

## Risks

- Cloud API behavior may differ from local Postiz. Mitigation: use draft mode, payload preview, and small smoke submissions only.
- Draft payload could lack media or platform-specific settings. Mitigation: first draft is text-only/package validation, not public content.
- API key leakage. Mitigation: never print key; keep `.env` untracked.


## Execution update — 2026-07-04

Completed in this pass:

- Added `PostizPublisher.build_queue_payload(...)` for non-mutating preview.
- Added `aflack postiz-preview <queue_id> <integration_id>`.
- Added `tests/test_publishing.py` with five unit tests for cloud/local URL normalization and payload construction.
- Created safe publish intent `queue_id=2` and previewed its YouTube draft payload without submitting it to Postiz.

Validation:

```bash
source .venv/bin/activate
python3 -m unittest discover -s tests -v
python3 -m compileall -q src
aflack compliance-smoke
aflack economics-status
aflack postiz-integrations
```
