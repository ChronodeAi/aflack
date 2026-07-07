# Publish-Quality Policy Schema

**Date**: 2026-07-05
**Phase**: Controlled Construction
**Status**: schema definition; policy thresholds in `draft` status (not approved for automation)
**Source draft**: `.aiwg/planning/publish-quality-policy-draft.md`
**Review data model**: `.aiwg/marketing/vice-signal/episode-001-render-review-rubric.md` (Structured Data Model section)
**Related**: ADR-0008 (draft ramp + analytics aggregation); content-factory loop (`LOOP.md`, `state.yaml`, `budget.yaml`, `constraints.yaml`); `src/aflack/prompt_quality.py`; `src/aflack/draft_review.py`; `db/migrations/007_draft_reviews.sql`; no-safe-boring-generation rule.

## Purpose

Define the deterministic publish-quality policy that the draft-ramp learning loop produces from reviewed Postiz drafts. Public publishing stays blocked (`constraints.yaml`: `no_public_publish_without_approval`; `budget.yaml`: `public_posts.cap = 0`) until this policy reaches `learned` status AND the operator explicitly lifts the publish cap per-publish. This document is the schema and the learning mechanism, not automation code, and it creates no publish automation.

## Schema: `aflack.publish-quality-policy.v1`

The active policy is a single versioned document. Reviews produce candidates that tune it; the operator approves material changes.

```yaml
schema: aflack.publish-quality-policy.v1
version: 1
status: draft          # draft -> learned -> approved_for_automation_proposal
updated_at: "2026-07-05T00:00:00Z"
updated_by: operator
evidence_base:
  reviewed_drafts_count: 0
  reviewed_draft_ids: []
  min_drafts_for_automation_proposal: 100   # ties to the first-100 Postiz ramp (ADR-0008)
  convergence_min_reviews: 3                # reviews that must reinforce a candidate before auto-accept
  stable_criteria_observed: false
gates:
  compliance:
    required: true
    rule: zero blocking compliance issues AND complete compliance negatives + disclosure
    threshold: compliance_score == 5
    source: draft_reviews.compliance_score + blocks
  prompt_quality:
    required: true
    rule: passes story-native gate and includes complete compliance negatives
    threshold: check_short_asset_prompt(prompt).passed == true AND warnings == []
    source: src/aflack/prompt_quality.py (pre-generation gate)
  render_review:
    required: true
    rule: human review verdict is publish_candidate
    threshold: verdict == publish_candidate AND min(score) >= 3
    source: draft_reviews.verdict + scores
  analytics:
    required: true
    rule: real metrics exist OR no-signal state explicitly recorded and accepted
    threshold: analytics_ref != null OR analytics_no_signal_accepted == true
    source: analytics_snapshots + draft_reviews.metadata
  economics:
    required: true
    rule: cost ledger entry exists AND cost-per-generated is known
    threshold: economics_verified == true AND cost_per_generated_known == true
    source: cost_ledger + draft_reviews.metadata
  cta:
    required: true
    rule: CTA keyword, lead magnet, description, and disclosure present
    threshold: cta_score >= 3 AND cta_components_present == true
    source: draft_reviews.cta_score + metadata
  provenance:
    required: true
    rule: official/Rockstar assets are reference metadata only; no reused media
    threshold: no_reused_media == true
    source: compliance blocks + metadata
  platform_fit:
    required: true
    rule: format/platform settings explicit; YouTube drafts private until approval
    threshold: platform_explicit == true AND visibility == private_until_approved
    source: publish_queue + metadata
decision_rule:
  publish_candidate_gate: ALL required gates pass
  publish_authorized: publish_candidate_gate == true AND explicit_operator_approval == true
  notes: >
    The daemon computes publish_candidate_gate; only the operator sets
    explicit_operator_approval. No autonomous publish.
automation_gate:
  may_propose_after: reviewed_drafts_count >= 100 AND stable_criteria_observed == true
  may_publish: never_autonomous
  proposal_action: daemon may summarize and propose; operator approves per-publish
learning_update:
  trigger: each completed render review (draft_reviews row)
  produces_one_of:
    - prompt_rule_update
    - content_package_update
    - compliance_lesson
    - publish_quality_threshold
    - explicit_non_action_with_reason
  threshold_candidate: metadata.policy_update_candidate_structured
  accept_rule: operator approves OR (converged across >= convergence_min_reviews AND status == draft)
  contradict_rule: a contradicting observation reopens an accepted candidate as proposed
human_gates_preserved:
  - public_publish
  - account_or_channel_settings
  - comment_dm_follow_automation
  - paid_promotion_or_ad_spend
  - broader_daemon_autonomy
```

## Gates

Eight required gates; all must pass for `publish_candidate_gate`. Each gate names its threshold, its data source, and whether it is pre-generation or post-generation.

| Gate | Required | Threshold | Source | Layer |
|---|---|---|---|---|
| compliance | yes | `compliance_score == 5` (zero blocks + complete negatives + disclosure) | `draft_reviews` + `blocks` | post-generation |
| prompt_quality | yes | `check_short_asset_prompt().passed == true AND warnings == []` | `src/aflack/prompt_quality.py` | pre-generation |
| render_review | yes | `verdict == publish_candidate AND min(score) >= 3` | `draft_reviews` | post-generation |
| analytics | yes | `analytics_ref != null OR analytics_no_signal_accepted == true` | `analytics_snapshots` + `metadata` | post-publish-draft |
| economics | yes | `economics_verified AND cost_per_generated_known` | `cost_ledger` + `metadata` | post-generation |
| cta | yes | `cta_score >= 3 AND cta_components_present` | `draft_reviews.cta_score` + `metadata` | post-generation |
| provenance | yes | `no_reused_media == true` | `blocks` + `metadata` | post-generation |
| platform_fit | yes | `platform_explicit AND visibility == private_until_approved` | `publish_queue` + `metadata` | pre-publish |

### Two-layer quality check

The policy enforces the no-safe-boring-generation rule at two layers:

1. **Pre-generation** (`prompt_quality` gate): `check_short_asset_prompt` rejects prompts missing positive GTA6 anchors, narrative tension, payoff, or motion markers, and warns on incomplete compliance negatives. This is the existing `src/aflack/prompt_quality.py` contract, referenced by name, not redefined here.
2. **Post-generation** (`render_review` + `compliance` gates): the render review scores verify the prompt's promises actually delivered in the asset (hook, retention, payoff, story-native, asset quality) and that compliance held after generation.

A prompt can pass pre-generation and still fail post-generation; both layers must pass for `publish_candidate_gate`.

## Decision (rollup) rule

`publish_candidate_gate = (compliance AND prompt_quality AND render_review AND analytics AND economics AND cta AND provenance AND platform_fit)`

`publish_authorized = publish_candidate_gate AND explicit_operator_approval`

The daemon may compute `publish_candidate_gate` and surface it via `aflack review status` and proposals. Only the operator sets `explicit_operator_approval`. There is no path to autonomous publish in this schema.

## Automation gate

- The daemon MAY summarize reviews and propose threshold updates once `reviewed_drafts_count >= 100` AND `stable_criteria_observed == true`.
- The daemon MAY propose a publish once `publish_candidate_gate` passes, but each publish requires explicit per-publish operator approval.
- The daemon MUST NOT publish, change account/channel settings, automate comments/DMs/follows, spend on ads, or edit framework artifacts autonomously (`constraints.yaml` hard blocks).

## Learning loop: review -> lesson -> threshold update

1. **Capture**: operator completes a render review, a `draft_reviews` row is written (`aflack review record`) carrying the six core scores, with `story_native_score` and structured detail in `metadata`. A YAML mirror is written under `.aiwg/marketing/<show>/reviews/`.

2. **Lesson extraction**: each review produces at least one lesson (`metadata.lessons_structured`) of one of five types: `prompt_rule`, `content_package`, `compliance`, `publish_quality_threshold`, `explicit_non_action`. Each lesson carries `scope`, `finding`, `action`, `evidence`, `confidence`.

3. **Threshold candidate**: a `publish_quality_threshold` lesson produces a `PolicyUpdateCandidate` (`metadata.policy_update_candidate_structured`) naming the `gate`, `current_threshold`, `proposed_threshold`, `direction`, `evidence_reviews`, `rationale`, and `status = proposed`.

4. **Stability and convergence**: a candidate becomes `accepted` (applied to the active policy) when:
   - the operator explicitly approves it, OR
   - it is reinforced by at least `convergence_min_reviews` (default 3) consecutive reviews without a contradicting observation, AND the policy `status == draft`.
   A contradicting observation reopens an `accepted` candidate as `proposed` with both evidence sets recorded.

5. **Policy status transitions**:
   - `draft`: initial thresholds from the rubric pass signals; tunable from reviews and candidates.
   - `learned`: `reviewed_drafts_count >= min_drafts_for_automation_proposal` (100) AND `stable_criteria_observed` (no open or rejected candidates on the core gates) AND operator marks it learned.
   - `approved_for_automation_proposal`: operator approves; the daemon MAY propose publishes against the policy, each still gated by explicit per-publish operator approval.

6. **Rollup vs single review**: no single review authorizes publish. The policy is the aggregated threshold; each publish is a separate gated approval. `publish_candidate` verdicts feed `publish_candidate_gate`, but `publish_authorized` always requires the operator.

## Loop integration

This policy is the gating artifact referenced by the content-factory loop. The integration is by reference; this document does not edit loop files:

- `constraints.yaml` hard block `no_public_publish_without_approval` resolves to "this policy status is at least `learned` AND the operator lifts `budget.yaml.public_posts.cap` per-publish".
- `budget.yaml.public_posts.cap` stays `0` until policy `status >= learned`; lifting it is a separate explicit operator action recorded in `.aiwg/activity.log`.
- `budget.yaml.postiz_drafts` (cap 100, submitted 1) counts review inputs; `reviewed_drafts_count` in the policy's `evidence_base` tracks how many of those have a completed `draft_reviews` row.
- `state.yaml.next_safe_actions` carries `learn_publish_quality_policy_from_first_100_drafts`; on each review, `state.yaml.latest_validation` can add `render_reviews: pass_N` and `publish_quality_policy: draft_v1`.
- `state.yaml.current_human_gates` is unchanged; this policy does not remove any human gate.

No loop file is modified by this schema document. Status transitions are operator actions recorded in `.aiwg/activity.log`.

## Reconciliation with existing contracts

- `src/aflack/draft_review.py` / `db/migrations/007_draft_reviews.sql`: the six core scores (1-5), verdict CHECK, `blocks`/`warnings`/`lessons` JSONB, `policy_update_candidate` TEXT, and `metadata` JSONB are the storage. Structured lessons, structured candidates, `story_native_score`, and economics/analytics facts ride in `metadata`. No source change is required to start the learning loop; a future migration may promote high-value `metadata` fields to columns once the first-100 ramp confirms which are load-bearing.
- `src/aflack/prompt_quality.py`: the `prompt_quality` gate references `check_short_asset_prompt` / `PromptQualityResult` by name. The post-generation `render_review` scores verify what the pre-generation prompt gate promised.
- no-safe-boring-generation rule: enforced at the two layers above (pre-generation prompt gate plus post-generation render review).
- ADR-0008: the first-100 Postiz draft ramp and analytics aggregation are the evidence source for this policy; `min_drafts_for_automation_proposal = 100` mirrors the ramp cap.

## Worked example (EP001)

When the operator completes the EP001 final render review:

1. Operator runs `aflack review record` with the six core scores, `verdict`, `blocks`, `warnings`, `lessons`, and `metadata` carrying `story_native_score`, `economics_verified`, `cost_per_generated_known`, `cost_ledger_ref`, `analytics_ref` (or `analytics_no_signal_accepted = true`), and any `lessons_structured` / `policy_update_candidate_structured`.
2. A YAML mirror is written to `.aiwg/marketing/vice-signal/reviews/vice-signal-ep001-review-2026-07-05.yaml`.
3. The review's `publish_candidate` verdict (if any) feeds `publish_candidate_gate`, but EP001 is NOT published: `budget.yaml.public_posts.cap == 0` and policy `status == draft`.
4. Any `publish_quality_threshold` lesson becomes a `proposed` candidate; with only one review it stays `proposed` (needs `convergence_min_reviews = 3` or operator approval).
5. `reviewed_drafts_count` increments to 1; `learned` status requires 100 reviewed drafts.

## Evidence base tracking

`evidence_base` in the policy document tracks:

- `reviewed_drafts_count` and `reviewed_draft_ids`: which `draft_reviews` rows informed the current thresholds.
- `min_drafts_for_automation_proposal`: 100 (first-100 ramp).
- `convergence_min_reviews`: 3 (default; operator-tunable).
- `stable_criteria_observed`: true only when no core gate has an open or rejected candidate.

The `aflack review status` rollup (`draft_review_rollup`) already exposes counts and score averages; the policy document layers threshold state and candidate status on top of that rollup.
