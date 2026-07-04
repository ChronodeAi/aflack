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
- Postiz UI health (`http://localhost:4007` returns auth redirect).
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
- [x] Postiz stack starts.
- [x] Postiz UI reachable (307 auth redirect).
- [ ] Postiz admin account created (human gate).
- [ ] YouTube connected in Postiz (human/OAuth gate).
- [ ] Real Postiz API submit verified.
- [ ] First generated creative scored by Virality Predictor.

## CI posture

No remote CI required for solo direct-to-main MVP. Use local test commands and committed reports.
