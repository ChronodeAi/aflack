# Video Analytics Aggregation Plan

**Date**: 2026-07-04  
**Phase**: Controlled Construction  
**Status**: active construction slice

## Goal

Capture all video/post performance metrics into one local source of truth so the content factory can learn which packages, scripts, hooks, personas, offers, and platforms actually perform.

## Source Model

Postgres `analytics_snapshots` is the canonical time-series store. Ingestion sources may include:

- Postiz platform analytics.
- Postiz post analytics.
- YouTube Studio/API exports.
- TikTok/Instagram platform exports.
- Manual operator entry.
- Future Aside/browser capture when APIs are incomplete.

## Normalized Metrics

Minimum snapshot fields:

- linkage: `publish_queue_id`, `creative_id`, `channel_id`, `platform`, `source`, `source_post_id`, `platform_url`
- reach: `views`
- engagement: `likes`, `comments`, `shares`, `saves`
- traffic/revenue: `clicks`, `ctr`, `conversions`, `revenue`
- video quality: `watch_time_seconds`, `average_view_duration_seconds`, `average_percentage_viewed`, `retention`
- provenance: `raw`, `captured_at`

## Learning Rules

1. Do not scale generation volume from views alone.
2. Prefer signals that combine retention, clicks, conversions, revenue, and cost.
3. Learn publish automation criteria from the first 100 reviewed Postiz drafts before public publishing is automated.
4. Keep raw source payloads so later schema improvements can reprocess old observations.
5. Record generation cost in `cost_ledger` before comparing performance.

## Construction Tasks

1. Apply migration `005_analytics_snapshots.sql`.
2. Use `aflack analytics-record-manual` for manual snapshots while API ingestion is incomplete.
3. Use `aflack analytics-status` for aggregate inspection.
4. Add Postiz analytics API ingestion once connected account IDs and post IDs are available.
5. Add platform-specific ingestion jobs only after draft/publish identifiers are stable.
