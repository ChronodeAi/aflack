# Test Strategy — Affiliate Content Pipeline MVP

**Created**: 2026-07-04
**Status**: Elaboration baseline

## Test levels

### Unit tests

- DB config loads.
- `MemoryStore.capture_lesson` / `recent_lessons`.
- `PostizPublisher.enqueue` writes correct queue rows.
- Economics ledger helpers (to build).
- Compliance classifier helpers (to build).

### Integration tests

- Migrations apply on fresh pgGraph+pgvector DB.
- Graph traversal: Product → Script → Creative → Result.
- `publish_smoke` creates YouTube/Postiz `needs_auth` queue row.
- Postiz cloud API health (`aflack postiz-integrations` returns connected channels).
- Higgsfield CLI auth status.

### Compliance tests

- Reject source marked `rockstar_pre_release_footage`.
- Reject "same-seed regenerate from official trailer footage."
- Reject missing affiliate disclosure.
- Reject false firsthand claims ("I played the leaked build").
- Allow original Vice-City-inspired visuals + commentary.

### Manual/human acceptance tests

- Create Postiz admin user.
- Connect YouTube account in Postiz.
- Confirm a draft/private YouTube post can be created.
- Approve first public publish.

## Test data

- Smoke niche: `gta6-ai-persona-gaming`.
- Smoke personas: Vice Signal, Loadout Lab.
- Reference videos: official Rockstar GTA6 trailers as metadata only (no media download).

## Current verification status

- [x] Docker available.
- [x] pgGraph + pgvector custom image built.
- [x] DB migrations pass.
- [x] Graph traversal passes.
- [x] Higgsfield auth passes.
- [x] Postiz images pulled.
- [x] Postiz stack starts locally when needed, bound to localhost.
- [x] Cloud Postiz API key configured.
- [x] YouTube connected in cloud Postiz.
- [x] TikTok connected in cloud Postiz.
- [x] `aflack postiz-integrations` verified against cloud Postiz.
- [ ] Real Postiz draft submit verified.
- [x] Postiz payload preview verified for queue `2` without submitting.
- [ ] First generated creative scored by Virality Predictor.

## CI posture

No remote CI required for solo direct-to-main MVP. Use local test commands and committed reports.


## Construction Iteration 1 test additions

- [x] Unit-test Postiz URL normalization for:
  - `http://localhost:4007`,
  - `http://localhost:4007/api/public/v1`,
  - `https://api.postiz.com`,
  - `https://api.postiz.com/public/v1`.
- [x] Add payload preview/dry-run coverage before cloud draft submission.
