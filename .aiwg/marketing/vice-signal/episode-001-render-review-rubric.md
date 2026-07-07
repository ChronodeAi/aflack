# EP001 Render Review Rubric

**Date**: 2026-07-05  
**Phase**: Controlled Construction  
**Status**: rubric ready; final human render review pending  
**Applies to**: Vice Signal EP001 private Postiz draft / measured Higgsfield generation batch

## Purpose

Capture the first private draft review as structured learning before any public publish decision. This is the local completion of the render-review lane; the actual verdict requires the operator to inspect the final assembled render.

## Required Review Fields

| Field | Question | Pass signal |
|---|---|---|
| First-frame hook | Would a GTA6/gaming viewer understand the reason to watch in the first second? | Clear visual tension or promise |
| Story-native relevance | Does the asset visibly belong to the GTA6/day-one setup context? | GTA6/day-one/Vice anchor appears positively, not only in negatives |
| Retention mechanics | Is there motion, escalation, or curiosity across the short? | Visible progression rather than static B-roll |
| Final payoff | Does the last frame reveal a checklist, result, twist, or decision? | Viewer gets a reason to finish |
| Compliance | No official/leaked footage, logos, false access, affiliation, or missing disclosure. | No blocking issues |
| CTA clarity | CTA keyword/lead magnet is understandable and not spammy. | CTA can be used in title/description/pinned comment |
| Asset quality | No unusable artifacts, unreadable text, broken continuity, or brand marks. | Acceptable for private draft review |
| Economics | Cost and asset count are recorded. | Cost ledger present |

## Verdict Values

- `keep_private`: good enough to preserve as draft, not publish.
- `revise_prompt`: prompt concept is viable but needs regeneration or edit.
- `revise_script`: content/story is wrong before asset generation.
- `publish_candidate`: can be considered for public publish after explicit operator approval.
- `kill`: do not reuse except as negative training data.

## Current EP001 Status

- Measured generation: complete.
- Cost capture: complete.
- Private Postiz draft: complete.
- Public publish: blocked.
- Final operator review: pending.

## Learning Rule

Every reviewed draft must produce one of:

1. prompt rule update,
2. content package update,
3. compliance lesson,
4. publish-quality threshold,
5. explicit non-action with reason.

## Structured Data Model

**Schema**: `aflack.render-review.v1`
**Storage**: `draft_reviews` table (migration `007_draft_reviews.sql`) plus a YAML mirror per review.
**Companion policy**: `.aiwg/planning/publish-quality-policy-schema.md`

EP001 is the first instance of this schema; it generalizes to any Vice Signal or Loadout Lab creative. The model is aligned with the existing `draft_reviews` table so reviews captured through `aflack review record` feed the learning loop without a schema change. The six numeric scores below are first-class columns; `story_native`, structured lessons, and analytics/economics facts ride in the `metadata` JSONB extension point until a future migration promotes them.

### Review record

| Field | Type | Storage | Required | Description |
|---|---|---|---|---|
| `review_id` | int | `draft_reviews.id` | yes | DB-generated id. |
| `publish_queue_id` | int | column | one of two | Postiz queue id. |
| `creative_id` | int | column | one of two | Creative id. |
| `reviewer` | string | column | yes | Operator handle. |
| `verdict` | enum | column (CHECK) | yes | `keep_private` \| `revise_prompt` \| `revise_script` \| `publish_candidate` \| `kill`. |
| `recommended_verdict` | enum | `metadata.recommended_verdict` | yes | Verdict computed from scores; human `verdict` confirms or overrides (reason in `metadata.verdict_override_reason`). |
| `hook_score` | int 1-5 | column | yes | First-frame hook. |
| `retention_score` | int 1-5 | column | yes | Retention mechanics. |
| `payoff_score` | int 1-5 | column | yes | Final payoff. |
| `compliance_score` | int 1-5 | column | yes | Compliance. |
| `cta_score` | int 1-5 | column | yes | CTA clarity. |
| `asset_quality_score` | int 1-5 | column | yes | Asset quality. |
| `story_native_score` | int 1-5 | `metadata.story_native_score` | yes | Story-native relevance (target for column promotion). |
| `blocks` | list[string] | column (JSONB) | yes | Blocking compliance/quality issues. |
| `warnings` | list[string] | column (JSONB) | yes | Non-blocking concerns. |
| `lessons` | list[string] | column (JSONB) | yes | Short lesson labels (at least one per Learning Rule). |
| `lessons_structured` | list[Lesson] | `metadata.lessons_structured` | yes | Structured lesson detail (see below). |
| `policy_update_candidate` | string | column | no | Short summary of any threshold proposal. |
| `policy_update_candidate_structured` | PolicyUpdateCandidate \| null | `metadata.policy_update_candidate_structured` | no | Structured threshold proposal. |
| `economics_verified` | bool | `metadata.economics_verified` | yes | Cost ledger entry present. |
| `cost_per_generated_known` | bool | `metadata.cost_per_generated_known` | yes | Cost-per-generated is known. |
| `cost_ledger_ref` | string | `metadata.cost_ledger_ref` | yes | Postgres cost_ledger entry reference. |
| `analytics_ref` | string \| null | `metadata.analytics_ref` | yes | Analytics snapshot ref, or null. |
| `analytics_no_signal_accepted` | bool | `metadata.analytics_no_signal_accepted` | yes | True when no-signal state is explicitly accepted. |
| `notes` | string | `metadata.notes` | no | Free-text operator notes. |
| `reviewed_at` | datetime | column | yes | Review timestamp. |

### Score scale (1-5 ordinal, matches `draft_reviews` CHECK constraints)

| Value | Meaning |
|---|---|
| 1 | Blocking fail. |
| 2 | Weak; warning. |
| 3 | Acceptable; meets the rubric pass signal. |
| 4 | Strong. |
| 5 | Publish-quality / complete. |

### Score anchors

| Score | 1 (block) | 2 (weak) | 3 (pass) | 4 (strong) | 5 (publish-quality) |
|---|---|---|---|---|---|
| `hook_score` | No reason to watch in first second | Unclear tension | Clear visual tension or promise | Immediate hook | Unavoidable, scroll-stopping hook |
| `story_native_score` | No GTA6/Vice anchor, or only in negatives | Anchor present but superficial | Anchor appears positively | Anchor drives the beat | Anchor is load-bearing to the story |
| `retention_score` | Static B-roll | Minor motion only | Visible progression | Sustained escalation | Escalation or curiosity throughout |
| `payoff_score` | No end state | Weak / ambiguous reveal | Clear checklist, result, twist, or decision | Reveal earns the watch | Reveal earns the rewatch |
| `compliance_score` | Blocking issue (footage, logo, affiliation, false access, missing disclosure) | Incomplete negatives or disclosure warning | No blocking issues | Clean, minor polish left | No blocking issues AND complete compliance negatives + disclosure |
| `cta_score` | Missing or spammy | Unclear | Understandable, usable in title/description/pinned comment | Strong, non-spammy | Strong, non-spammy CTA with lead magnet |
| `asset_quality_score` | Unusable artifacts, unreadable text, broken continuity, or brand marks | Major flaws | Acceptable for private draft review | Clean | Clean and publish-ready |
| `economics` (verified, not scored) | Cost ledger missing | Cost recorded, cost-per-generated unknown | Cost ledger present | Cost ledger + cost-per-generated known | n/a (boolean gate, see policy schema) |

> `compliance_score == 1` is always blocking regardless of other scores. The render-review `publish_candidate` floor is `compliance_score >= 3`; the publish-quality policy publish gate requires `compliance_score == 5` (complete negatives) for actual public publish. `economics` is a verification gate, not an aesthetic score.

### Recommended verdict decision rules

Evaluated in order; first match wins. `recommended_verdict` is computed from the scores and stored in `metadata`; the human `verdict` may override it with a reason in `metadata.verdict_override_reason`.

```text
if compliance_score == 1                                          -> kill
elif asset_quality_score == 1                                     -> kill
elif hook_score == 1 and payoff_score == 1                        -> kill
elif story_native_score <= 2 or payoff_score <= 2                 -> revise_script
elif hook_score <= 2 or retention_score <= 2 or asset_quality_score <= 2 -> revise_prompt
elif min(hook, retention, payoff, compliance, cta, asset_quality, story_native) >= 3
     and compliance_score >= 3
     and economics_verified == true
     and (analytics_ref != null or analytics_no_signal_accepted)  -> publish_candidate
else                                                              -> keep_private
```

### Lesson record (`metadata.lessons_structured`)

Each review produces at least one lesson (Learning Rule). The `lessons` column holds short labels; structured detail rides in `metadata.lessons_structured`:

| Field | Type | Description |
|---|---|---|
| `type` | enum | `prompt_rule` \| `content_package` \| `compliance` \| `publish_quality_threshold` \| `explicit_non_action` |
| `scope` | string | Field, gate, or artifact the lesson affects. |
| `finding` | string | What was observed. |
| `action` | string | What should change. |
| `evidence` | list[string] | Review id, score fields, frame/timecode refs. |
| `confidence` | float | 0.0-1.0. Single review starts at 0.3; reinforced across reviews rises toward 1.0. |

### Policy update candidate (`metadata.policy_update_candidate_structured`)

When a lesson is `publish_quality_threshold`, the review attaches a candidate (the `policy_update_candidate` column holds the short summary):

| Field | Type | Description |
|---|---|---|
| `gate` | string | Policy gate name (see publish-quality policy schema). |
| `current_threshold` | string | Current threshold expression. |
| `proposed_threshold` | string | Proposed threshold expression. |
| `direction` | enum | `raise` \| `lower` \| `add` \| `remove` |
| `evidence_reviews` | list[int] | Review ids supporting the change. |
| `rationale` | string | Why. |
| `status` | enum | `proposed` \| `accepted` \| `rejected` \| `superseded` |

### Storage

Primary: `draft_reviews` row written by `aflack review record`.
YAML mirror: `.aiwg/marketing/<show>/reviews/<creative-id>-review-<reviewed-at-date>.yaml`.

EP001 mirror (to be created when the operator completes the final render review): `.aiwg/marketing/vice-signal/reviews/vice-signal-ep001-review-2026-07-05.yaml`.

The aggregated publish-quality policy lives at `.aiwg/planning/publish-quality-policy-schema.md`.

### Reconciliation notes

- The six first-class scores match the `draft_reviews` columns and the `aflack review record` CLI exactly; no source change is needed to start capturing EP001.
- `story_native_score` and the structured lesson/candidate detail use the `metadata` JSONB extension point so the learning loop can start now; a future migration may promote high-value metadata fields to columns once the first-100 ramp confirms which are load-bearing.
- This data model captures reviews only; it does not authorize public publishing (see `constraints.yaml` `no_public_publish_without_approval`).
