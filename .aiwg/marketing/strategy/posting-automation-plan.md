# Posting Automation Plan — Postiz-backed Distribution

**Created**: 2026-07-04
**Updated**: 2026-07-04
**Decision**: Use Postiz (`gitroomhq/postiz-app`) as the open-source scheduling/posting app.
**ADR**: `.aiwg/architecture/adr-0001-postiz-posting-scheduler.md`

## Strategy

Use **Postiz** as the publishing/scheduling backbone instead of hand-rolling platform adapters.

```
Creative → Compliance Gate → Platform Render Profile → Publish Queue → Postiz API/SDK/agent → Platforms → Result Capture
```

Our pipeline owns:

- research,
- generation,
- validation,
- compliance approval,
- economics ledger,
- memory/event store.

Postiz owns:

- calendar/scheduling,
- platform OAuth/connection management,
- posting execution,
- multi-platform support,
- retries/platform-specific mechanics where available.

## Why Postiz

Verified 2026-07-04:

- OSS, active, mature: `gitroomhq/postiz-app`, ~32.7k stars, TypeScript/Next.js, pushed 2026-07-03.
- License: **AGPL-3.0**.
- Native platforms include YouTube, TikTok, Instagram, Facebook, X, Reddit, LinkedIn, Pinterest, Threads, Bluesky, Mastodon, Discord, Slack.
- Has Public API, Node SDK (`@postiz/node`), n8n node, Make integration, and a new `postiz-agent` CLI for agents.

## Licensing boundary

For our use:

- Solo self-hosted internal use is fine.
- Integrate over Postiz's Public API / SDK / CLI as a separate service.
- Do **not** vendor, fork, or modify Postiz inside our AIWG framework unless we accept AGPL obligations.
- When/if this becomes an AIWG framework, Postiz should be documented as an external optional dependency, not bundled source.

## Data model impact

We still keep a local `publish_queue`, but it becomes a queue of **Postiz scheduling intents**, not direct platform API calls.

Add/extend:

- `publish_queue`
  - creative_id
  - channel_id
  - platform
  - target_format (`short`, `longform`, `reel`, etc.)
  - title
  - description
  - hashtags
  - disclosure_text
  - status (`draft`, `queued`, `submitted_to_postiz`, `scheduled`, `published`, `failed`, `needs_manual_review`)
  - scheduled_at
  - published_at
  - postiz_post_id
  - platform_post_id
  - platform_url
  - error

- `platform_credentials`
  - platform
  - auth_mode (`postiz_oauth`, `postiz_api_key`, `aside_session`, `manual`)
  - status
  - notes

Credentials/tokens stay in Postiz / `.env` / secure store, never git.

## YouTube-first economics

YouTube should be first-class:

- YouTube long-form = primary RPM/revenue surface (~$2,000-5,000+ per million views for gaming long-form, varies by geography/audience/ad inventory).
- YouTube Shorts = top-of-funnel (~$50-150 per million views).
- TikTok = reach, trend discovery, lower direct payout (~$20-40 per million, 60s+ only).

For GTA6/gaming:

```
AI-persona Shorts → YouTube long-form → gaming-adjacent affiliate + brand deals
```

## Safe publishing defaults

- Compliance gate must pass before submitting anything to Postiz.
- Use draft/private/manual-review modes where possible.
- For YouTube, expect API audit/private-upload constraints under the hood; Postiz may make the UI flow easier but cannot bypass YouTube policy.
- For TikTok, expect posting authorization/review constraints; use Aside fallback if needed.
- Store all disclosures and source provenance.

## Immediate implementation plan

1. Read Postiz self-host + Public API docs.
2. Decide local deployment strategy:
   - separate `docker compose` stack for Postiz,
   - keep our pgGraph DB separate from Postiz's internal Postgres unless docs prove sharing is safe.
3. Add `publish_queue` and `platform_credentials` migration.
4. Add `PostizPublisher` adapter:
   - create/schedule post via API/SDK/CLI,
   - record `postiz_post_id`,
   - poll/status update,
   - record final platform URL.
5. Keep Aside fallback for platform login/composer work.

## Open verification items

- Public API endpoints and auth for self-hosted deployments.
- Media upload/schedule support per platform, especially YouTube video and TikTok video.
- Whether Node SDK or `postiz-agent` CLI is better for our Python pipeline.
- Required env vars and resource footprint for local Postiz.
