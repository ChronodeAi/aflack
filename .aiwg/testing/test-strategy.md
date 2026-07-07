# Test Strategy — Affiliate Content Pipeline MVP

**Created**: 2026-07-04
**Status**: Elaboration baseline with Controlled Construction updates

## Test levels

### Unit tests

- `PostizPublisher` URL normalization and payload preview.
- Aside scan pure logic: platform normalization, social metric parsing, engagement rate, observation hash stability.
- Learning pure logic: insight hash stability and proof-of-real-success creator credibility.
- Compliance gate logic: blocked provenance, disclosure, false access, medical claim markers, and AI disclosure warnings.
- Daemon status, memory consolidation, economics rollup, and trace capture/replay.
- DB config loading remains a candidate for expansion.
- CLI runner tests cover JSON status/action surfaces for Cockpit integration.

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

- [x] Local unit/integration suite passes: 73 tests.
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
- [x] Real Postiz private/draft submit verified for queue `2`.
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

## Construction Iteration 2 test additions

- [x] Add direct compliance gate coverage.
- [x] Add daemon status coverage.
- [x] Add memory consolidation coverage.
- [x] Add economics rollup coverage.
- [x] Add trace capture/replay coverage.

## Construction acceleration test additions

- [x] Add CLI runner coverage for:
  - `daemon-status --json`,
  - `loop-status --json`,
  - `analytics-status --json`,
  - `publish-queue-status --json`,
  - `prompt-quality --json`,
  - `compliance-smoke --json`.
- [x] Validate that failed prompt-quality JSON exits non-zero while remaining parseable.
- [x] Add DB config loader tests.
- [ ] Add live adapter contract tests for Postiz analytics once stable real metrics exist.
- [ ] Add requirement ID references in high-value tests before IOC gate.
