# ADR-0008: Draft Ramp and Analytics Aggregation

**Date**: 2026-07-04  
**Status**: Accepted  
**Decision Owner**: Operator

## Context

The operator approved moving past the previous zero-cap boundary: generate Shorts under an adaptive credit-learning policy, approve the first 100 Postiz drafts, and capture all video analytics in one aggregated place. Postiz appears to expose platform/post analytics through its public/agent API surface, but the content factory needs metrics joined to packages, creatives, costs, funnels, and lessons.

## Decision

1. Treat Postiz as a scheduler plus analytics ingestion source, not the system of record for learning.
2. Store normalized time-series metrics in local Postgres `analytics_snapshots`.
3. Keep `results` as a compact rollup/output table, with `analytics_snapshots` as the raw learning layer.
4. Approve the first 100 Postiz submissions as drafts only when tied to validated packages and clear target integrations.
5. Approve Higgsfield generation as measured batches for validated packages, with cost capture and stop conditions; do not interpret this as unlimited spend.
6. Keep public publishing blocked until the first draft ramp produces a learned publish-quality policy and analytics capture is working.

## Consequences

- We can ingest metrics from Postiz, YouTube, TikTok, Instagram, manual entry, or later API jobs into one schema.
- The daemon can learn from source-normalized outcomes without depending on a single vendor dashboard.
- Draft generation and scheduling can move forward while public publishing automation remains controlled.
- Construction now has a concrete analytics implementation target before broader daemon autonomy.

## Verification

- Migration: `db/migrations/005_analytics_snapshots.sql`
- Runtime: `aflack analytics-record-manual`, `aflack analytics-status`
- Tests: `tests/test_analytics.py`
- Loop policy: `.aiwg/loops/content-factory/{budget.yaml,constraints.yaml,state.yaml}`
