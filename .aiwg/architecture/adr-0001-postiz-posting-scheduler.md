# ADR-0001: Adopt Postiz as the scheduling + posting layer

**Status**: Accepted
**Date**: 2026-07-04
**Decision owner**: Solo operator

## Context

The pipeline needs cross-platform publishing + scheduling (YouTube first-class, plus TikTok, Instagram, X, Reddit, etc.). We had planned to hand-roll per-platform adapters (OAuth, upload flows, quotas, retries) — significant, brittle, per-platform work that fights platform API gating and changes constantly.

Postiz (`gitroomhq/postiz-app`) is a mature open-source social scheduling tool that already solves this.

## Decision

Use **Postiz** as our scheduling + posting layer instead of building platform adapters ourselves. Our pipeline integrates with Postiz over its **Public API** (optionally the Node SDK or the `postiz-agent` CLI), treating Postiz as a separate self-hosted service.

## Facts (verified 2026-07-04)

- Repo: `gitroomhq/postiz-app`, TypeScript/Next.js, ~32.7k stars, actively maintained (pushed 2026-07-03).
- License: **AGPL-3.0**.
- Supported channels include: YouTube, TikTok, Instagram, Facebook, X, Reddit, LinkedIn, Pinterest, Threads, Bluesky, Mastodon, Discord, Slack.
- Surfaces: Public API (`docs.postiz.com/public-api`), Node SDK (`@postiz/node`), n8n node, Make.com integration, and a new agent CLI (`gitroomhq/postiz-agent`).
- Self-hostable (Docker); stack uses Next.js + Redis + Postgres.

## Why

- Removes the largest, most brittle part of our build (per-platform OAuth + upload + scheduling + retries).
- YouTube + TikTok + the rest are already integrated and maintained by an active project.
- API/SDK/agent-CLI surfaces fit our agentic pipeline.
- Self-hostable → aligns with our local-first, own-the-stack posture.

## Consequences

### Positive
- We keep OUR code focused on: research → generation → validation → compliance → memory/economics. Postiz owns distribution.
- Faster path to actually posting (YouTube-first funnel).
- Scheduling, calendar, multi-account, retries handled for us.

### Negative / risks
- **AGPL-3.0 copyleft.** Safe for solo self-hosted internal use. Integrate ONLY over the Public API / SDK / CLI (separate process) so our code is not a derivative work. Do NOT fork/modify-and-redistribute Postiz, or offer a modified Postiz as a network service to third parties, without meeting AGPL source-release obligations. Revisit at the frameworkization stage (our AIWG framework should reference Postiz as an external dependency, not vendor its source).
- Platform API gating still applies underneath (e.g., YouTube unaudited-project private-upload restriction, TikTok posting review). Postiz manages the mechanics but cannot bypass platform policy.
- Adds an operational service to run/monitor (Docker: app + Redis + Postgres).
- Another data surface for tokens/credentials — keep secrets in Postiz's own secured config, not our git.

## Alternatives considered

- **Hand-rolled adapters**: maximal control, but slow, brittle, and duplicative of Postiz. Rejected.
- **Aside browser automation only**: good fallback for logged-in composers, but not a durable scheduling backbone. Keep as fallback, not primary.
- **Commercial schedulers (Buffer/Hypefury)**: closed, recurring cost, weaker automation/API fit. Rejected.

## Integration shape

```
aflack pipeline  --(Public API / SDK / postiz-agent)-->  Postiz (self-hosted)  -->  YouTube / TikTok / IG / X / ...
```

- Our `publish_queue` holds intent + compliance-approved metadata; a Postiz publisher submits/schedules to Postiz and records the returned post id/status back into our event store + `results`.
- Compliance gate stays on OUR side and must pass before anything is handed to Postiz.

## Open items to verify against Postiz docs

- Public API coverage for programmatic upload + schedule per channel (esp. YouTube video + TikTok video), on the **self-hosted** deployment (not just cloud).
- Auth model for the self-hosted Public API (API keys) and per-channel OAuth connection flow.
- Whether the `postiz-agent` CLI or Node SDK is the cleaner integration for our pipeline.
- Media upload constraints (size/length/format) and rate limits.
