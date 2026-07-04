# Posting Automation Plan — Cross-Platform Distribution

**Created**: 2026-07-04
**Context**: User noted that if we test clip-farming / GTA6 / gaming content, we need automated posting to platforms, including YouTube.
**Assumption**: "conforms" in the note means "platforms."

## Strategy

Build a **publishing adapter layer** rather than hard-coding one platform:

```
Creative → Compliance Gate → Platform Render Profile → Publish Queue → Platform Adapter → Result Capture
```

Each platform adapter should support:

- draft/private upload first,
- metadata/caption/hashtag templating,
- compliance/disclosure injection,
- scheduled/manual approval mode,
- post URL/status capture,
- analytics pullback into `results`,
- economics ledger entries for operator time and platform-specific costs.

## Platform priority

### 1. YouTube Shorts

Why first-class:

- Stronger long-term channel asset than pure TikTok.
- Better archive/search/discovery surface.
- Shorts can compound into long-form gaming channel strategy later.
- GTA6/gaming hype is naturally YouTube-native.

Monetization economics (why YouTube-first):

- YouTube long-form ad revenue (55% creator share) pays far more per view than TikTok — commonly ~$2,000-5,000+ per million views for gaming long-form, and much higher in premium niches. This is the primary money surface.
- YouTube Shorts pays from the Shorts ad pool — modest (~$50-150 per million views) but still generally beats TikTok and funnels viewers into long-form + affiliate.
- TikTok Creator Rewards pays ~$20-40 per million and only on 60s+ videos; sub-minute clips earn nothing directly.
- Strategic implication: the highest-paying surface is long-form, which pure clip farming does NOT produce. Use Shorts as top-of-funnel attention, long-form as the revenue capture, affiliate + brand deals stacked on top.
- Funnel shape for GTA6/gaming: AI-persona Shorts (attention) -> long-form GTA6 content (high RPM) -> gaming-adjacent affiliate + brand deals.

Official automation notes:

- YouTube Data API supports uploading videos via `videos.insert` and setting metadata.
- The upload guide uses OAuth 2.0 (`client_secrets.json`) for authorized channel access.
- Current YouTube docs note that API projects created after July 28, 2020 that are not verified/audited have videos uploaded via `videos.insert` restricted to private viewing mode until the project passes a YouTube API Services audit.
- Default quota is enough for our target scale in theory (100 `videos.insert` calls/day), but quota and hidden daily upload limits should be treated as operational constraints.

Recommended v1:

1. Build a YouTube adapter that can upload as **private/draft** first.
2. Keep human approval/publish step until API verification/audit is resolved.
3. Use Aside browser automation as a fallback for logged-in composer flows if official API gating blocks public posts.
4. Store YouTube video ID, privacy state, publish URL, title, description, tags, thumbnail, and analytics pulls.

### 2. TikTok

Official automation notes:

- TikTok Content Posting API Direct Post initializes a video export, returns an `upload_url`, and requires uploading the file to TikTok for processing.
- Direct posting requires app/creator authorization and platform constraints; real-world direct public posting can require review/audit.

Recommended v1:

1. Prefer official Content Posting API if feasible.
2. Otherwise use Aside for logged-in manual/composer automation.
3. Keep manual review before public publish.

### 3. Instagram Reels / Facebook Reels / X

Treat as adapters after YouTube/TikTok. Do not block week 1 on them.

## GTA6 / clip farming-specific rule

If we run a GTA6 content branch, the publishing layer should default to **original AI-persona gaming content** and avoid pure reused clip farming as the core. If any third-party footage is used:

- Use only short, transformed, commentary-led excerpts.
- Keep original voice/persona commentary central.
- Track source provenance.
- Avoid mass duplicate templates.
- Expect monetization and IP risk.

## Data model additions

Add/extend:

- `publish_queue`
  - creative_id
  - channel_id
  - platform
  - target_format
  - title
  - description
  - hashtags
  - disclosure_text
  - status (`draft`, `queued`, `uploaded_private`, `needs_manual_publish`, `published`, `failed`)
  - scheduled_at
  - published_at
  - platform_post_id
  - platform_url
  - error

- `platform_credentials`
  - platform
  - auth_mode (`oauth`, `aside_session`, `manual`)
  - status
  - notes

Credentials/tokens must stay outside git (`.env`, OS keychain, or platform credential store).

## Safety defaults

- Never publish public automatically until the compliance gate passes.
- For YouTube, prefer private upload + human publish until API verification/audit is known.
- For TikTok, prefer draft/inbox/manual approval where possible.
- Record all disclosures in `disclosures`.
- Record all source/provenance for clips in the event store.

## Recommended next build step

Add the `publish_queue` schema and a no-op `YouTubePublisher` adapter that can prepare metadata and mark an item as `needs_auth` / `needs_manual_publish`. Wire actual OAuth/API upload only after we create a Google Cloud project and confirm verification/audit path.
