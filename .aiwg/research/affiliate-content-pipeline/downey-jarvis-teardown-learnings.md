# Learnings Digest — Downey.ai / Jarvis / Higgsfield MCP Blueprint

**Created**: 2026-07-04
**Source**: User-provided evidence-bounded teardown of @downey.ai, LukeBuildsAI "Jarvis", and Higgsfield MCP.
**Discipline adopted**: keep OBSERVED vs INFERRED separate (their addendum does this well; we mirror it).

## The one-line pattern worth internalizing

Visual spectacle (Higgsfield) → curiosity/business hook → ONE-WORD comment CTA → DM delivers a guide/lead magnet (with affiliate link) → capture audience → iterate. The post's job is to trigger the keyword comment; the DM/lead magnet is the real conversion asset.

## What is actually verified (high confidence)

- Higgsfield-generated short videos + Iron Man/Jarvis persona.
- One-word comment CTA on posts (e.g., Jarvis, Higgs, football).
- The DM "guide" is literally a Higgsfield MCP + Claude connector setup walkthrough (often with an affiliate/referral link).
- Higgsfield MCP connector into Claude (Settings > Connectors), "Content Factory" Claude skill: research → plan → batch-generate → schedule.
- Consistent character via Soul/avatar; Seedance 2.0 video + GPT Image 2 / Nano Banana images.
- Google Sheets as creative DB + Claude "routines" for scheduled recurring generation (e.g., weekly: append 50 idea rows; daily: generate all blank-status rows).
- Comment-to-DM automation (ManyChat / Meta-native) is a separate, genre-standard layer.
- Cadence is low (~2 posts/week) — manual-scale. Success is from funnel mechanic + spectacle, NOT raw volume.
- Monetization most plausibly Higgsfield Earn payouts + affiliate, not a real "$1B ARR". The "43 pages" line is fiction inside the video.

## Verified risk context (important)

- Forbes exposé on Higgsfield; Higgsfield X account suspended for inauthentic behavior; Reddit reports of throttled "unlimited" plans + a mass account-ban wave.
- Implication: do NOT build the whole business on Higgsfield credits/Earn. Keep funnel + audience portable (own lead magnet, email list, posting infra).

## What we ADOPT into our setup

1. **Funnel-first mindset**: treat the post as a trigger and the lead magnet as the conversion asset. Add an explicit funnel/lead-magnet layer to our model (we already stubbed this in the posting plan; formalize it).
2. **Batch "routine" generation pattern**: our event store already beats Google Sheets. Adopt the status-driven batch loop — the director appends idea/brief rows, then batch-generates everything in `status='blank'/'draft'`. Maps cleanly to our `scripts`/`creatives`/`publish_queue` status columns.
3. **Consistent character (Soul/avatar)**: reinforces our persona approach (Vice Signal, Loadout Lab). Store a stable Higgsfield Soul/reference per persona.
4. **Virality Prediction pre-publish gate**: already in our plan (Higgsfield `brain_activity`). Keep it.
5. **Own-the-audience**: add email/lead capture as a first-class, portable asset — not just platform followers. Anti-platform-risk.
6. **Evidence discipline**: every research artifact separates observed vs inferred (already our norm; keep enforcing).

## What we DO DIFFERENTLY / already ahead

- **We already have a stronger substrate than Sheets**: Postgres + pgGraph + pgvector event store vs Google Sheets.
- **We already chose Postiz** for scheduling/posting (portable, multi-platform) instead of Meta Ads scheduling or Higgsfield Social Connectors — this is the "own posting infra" lesson, already done.
- **We are YouTube-first**, not Instagram-first. The comment-to-DM/ManyChat mechanic is IG-centric; on YouTube the equivalent is pinned comment + description link + community tab + (optionally) a lead-magnet link. Adapt, don't copy.
- **Compliance is stricter for us**: no false income claims, affiliate disclosure, no Rockstar footage. Their "$1B ARR / 43 pages" bait is exactly what our compliance gate forbids.
- **Do not over-rely on Higgsfield**: keep generation behind a swappable interface; consider alternate generators so a Higgsfield ban/throttle doesn't kill the pipeline.

## Tension to flag: volume vs funnel

Their result comes from ~2 high-quality funnel posts/week, not volume. Our target is ~20 videos/day. Lesson: **volume without a working hook+funnel just burns Higgsfield credits**. Recommendation: prove ONE hook→CTA→lead-magnet→conversion loop works before scaling to 20/day. Fold this into the economics/scale gate (don't scale volume until cost-per-winning-video and funnel conversion are positive).

## Concrete backlog items produced

- Formalize funnel entities: `lead_magnets`, `funnel_keywords`, and link them to `publish_queue`.
- Add `soul_ref` per persona (stable Higgsfield character).
- Add director "routine" spec: weekly brief append + daily batch-generate blank-status rows.
- Add YouTube-native funnel (pinned comment + description link) instead of IG comment-to-DM for v1.
- Add generator-portability note (don't single-source Higgsfield).
- Add "prove funnel before volume" to the scale gate.

## Compliance reminders reinforced

- Comment-to-DM automation, if ever used, must be opt-in and disclosed; use official platform paths only; no scraping/private APIs.
- No false income/ARR claims; use "workflow/demo/template" framing.
- Affiliate disclosure everywhere.
