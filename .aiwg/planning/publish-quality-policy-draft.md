# Publish Quality Policy Draft

**Date**: 2026-07-05  
**Phase**: Controlled Construction  
**Status**: policy data model implemented; first human review pending; not approved for automation

## Decision

Public publishing remains blocked until draft review and analytics evidence produce deterministic publish criteria. This policy is the target schema for learning from the first-100 Postiz drafts.

## Candidate Criteria

| Criterion | Required before public publish automation |
|---|---|
| Compliance | Zero blocking compliance issues. |
| Prompt quality | Prompt passes story-native gate and includes complete compliance negatives. |
| Render review | Human review verdict is `publish_candidate`. |
| Analytics | Real metrics exist or no-signal state is explicitly recorded and accepted. |
| Economics | Cost ledger entry exists and cost-per-generated is known. |
| CTA | CTA keyword, lead magnet, description, and disclosure are present. |
| Provenance | Official/Rockstar assets are reference metadata only; no reused media. |
| Platform fit | Format/platform settings are explicit; YouTube drafts stay private until approval. |

## Draft Review Data Model

Each draft review should capture:

- `queue_id`
- `creative_id`
- `reviewed_at`
- `reviewer`
- `verdict`
- `scores`: hook, retention, payoff, compliance, CTA, asset quality
- `blocks`
- `warnings`
- `lessons`
- `policy_update_candidate`

Implemented locally as:

- migration: `db/migrations/007_draft_reviews.sql`
- domain module: `src/aflack/draft_review.py`
- record command: `aflack draft-review-record`
- rollup command: `aflack draft-review-status --json`

The command output always reports `public_publish_authorized=false` or `public_publish_automation_ready=false`; a review record is learning evidence, not a publish approval.

## Automation Gate

Automation can only be proposed after enough reviewed drafts show stable criteria. Until then, the daemon may summarize and propose; it may not publish.
