# Content Factory Loop

**Status**: active for controlled Construction  
**Owner**: solo operator  
**Runtime**: local CLI + human-gated agent direction  
**Purpose**: make content production, validation, draft preparation, results capture, and learning inspectable before any broader daemon autonomy.

## Loop Boundary

The loop may perform safe local work:

- read active gates and backlog,
- create/revise pre-generation packages,
- run deterministic compliance/test checks,
- consolidate memory from existing insights,
- preview Postiz payloads when target/content are explicit,
- record status in `.aiwg/` artifacts and Postgres.

The loop must stop before:

- public publishing,
- account or channel setting changes,
- comment, DM, follow, or unfollow automation,
- paid promotion or ad spend,
- broader daemon autonomy.

Measured Higgsfield generation is approved for validated packages under the
adaptive credit policy in `budget.yaml`. The first 100 Postiz submissions are
approved as drafts only when the package and target integration are explicit.

## Current Construction Target

```text
content package
  -> compliance check
  -> operator review
  -> measured generation with credit/cost capture
  -> generated asset compliance check
  -> Postiz payload preview
  -> Postiz draft submission within first-100 ramp
  -> analytics/results/economics capture
  -> learned publish-quality policy
  -> operator publish automation decision
  -> memory consolidation
```

## Deterministic Checks

Minimum checks for a safe construction slice:

```bash
.venv/bin/python -m compileall -q src
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/aflack daemon-status
.venv/bin/aflack compliance-smoke
.venv/bin/aflack proposals-list
aiwg index build
```

## Gate Policy

This control plane does not override human authorization. A green check means
the artifact is locally consistent. Current operator approval covers measured
generation for validated packages and the first 100 Postiz drafts; it does not
cover public publishing, account action, comment/DM/follow automation, ad spend,
or broader daemon autonomy.

## Related Artifacts

- @.aiwg/reports/construction-ready-brief.md
- @.aiwg/reports/status-assessment.md
- @.aiwg/planning/iteration-plan-002.md
- @.aiwg/planning/daemon-runtime-architecture.md
- @.aiwg/creator-commerce-ops/rules/testable-contracts-over-prose.md
- @.aiwg/architecture/adr-0008-draft-ramp-and-analytics-aggregation.md
- @.aiwg/planning/video-analytics-aggregation-plan.md
