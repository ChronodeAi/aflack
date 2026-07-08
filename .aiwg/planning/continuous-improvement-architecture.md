# Continuous-Improvement Architecture — Aflack Content Pipeline

**Created**: 2026-07-04
**Author role**: candidate-solution agent (SDLC Construction)
**Status**: Implemented v1 (learning layer + daemon loop); scanning delegated to agent/Aside

## SDLC position

We are in **Construction**, Iteration 3 (continuous-improvement engine). Iterations 1-2
delivered the Postiz cloud draft loop, the Claude Code video director, and the first
pre-generation package. This iteration adds the *learning system* that turns competitor
intelligence into reproducible skills/rules/workflows.

## The loop (Damon SDLC)

```
scan (Aside, logged-in IG/TikTok)  ->  distill (insights, deduped)  ->
propose (skill/rule/workflow edits)  ->  [HUMAN GATE] apply  ->
produce (Claude Code director)  ->  validate (compliance + benchmark)  ->
[HUMAN GATE] publish (Postiz)  ->  results  ->  learn (memory) -> repeat
```

The daemon owns the **scan -> distill -> propose -> learn** arc autonomously.
The **apply**, **produce-paid**, and **publish** arcs stay human-gated.

## Components built

| Layer | Artifact | Purpose |
|---|---|---|
| DB | `db/migrations/004_learning_layer.sql` | benchmark_creators, benchmark_videos, insights, improvement_proposals, pipeline_events, daemon_runs |
| Tracing | `src/aflack/tracing.py` | every-bullet-tracer event capture + replay |
| Learning | `src/aflack/learning.py` | dedup + temporal-validity insights; proof-of-real-success creator grading |
| Daemon | `src/aflack/daemon.py` | autonomous scan/distill/propose cycle with hard safety blocks |
| CLI | `src/aflack/cli.py` | improve-cycle, insights-list, proposals-list, creator-add/proof, trace-show |
| Scheduler | `scripts/aflack-improve-daemon.sh`, `scripts/com.aflack.improve-daemon.plist` | cron/launchd background execution |

## Anti-rot memory design (directly answers the ask)

- **Dedup**: insights key on `content_hash = sha256(scope + normalized(statement))`.
  Re-observation reinforces (support_count++, confidence += 0.1 capped) instead of duplicating.
- **Temporal validity**: `valid_at`/`invalid_at` + `status` let stale patterns be retired,
  so they stop feeding the active context. This is the "never forgets, doesn't rot" property.
- **Relevance-gated retrieval**: `active_insights(scope, min_confidence)` returns only what's
  relevant and confident, so we do not jam everything into the window.
- **Three memory tiers / ADR-0007**: local Postgres + pgGraph + pgvector is the
  organization system of record; agentmemory (`:3111`, episodic) is each
  role/agent's notebook; the semantic-memory MCP (`:3113`, fortemi) is the
  semantic library. agentmemory and fortemi are derived indexes populated from
  the local SoR, never sources of truth. "Polygres" is an external company/product
  name and remains internal shorthand only when discussing the component pattern.

## Proof-of-real-success (not vanity flexing)

`benchmark_creators` cannot reach `verified` on followers alone. `score_creator_credibility`
requires 3 signals: real engagement rate (>=2%), observed monetization, and sustained cadence
(>=14 days). Follower count and wealth-flexing are ignored by the grader.

## Hard safety blocks (enforced in code, recorded every run)

The daemon records and refuses: `higgsfield_generation`, `public_publish`,
`account_settings_change`, `dm_or_comment_automation`, `auto_edit_skill_or_rule_files`.

## How scanning connects (agent + Aside handoff)

The daemon accepts an injected `scan_fn(niche) -> list[video dicts]`. The agent layer runs the
Aside browser skill against the operator's logged-in Instagram/TikTok, extracts the fields in
`benchmark_videos`, and passes them in. The daemon dedups + persists them. This keeps scraping
inside a human-authenticated browser session (no private API abuse) while the daemon stays the
durable, auditable orchestrator.

## Verified behavior (2026-07-04)

- `aflack improve-cycle` run twice: cycle 1 distilled 4 insights + 1 proposal; cycle 2
  reinforced all 4 (confidence 0.50 -> 0.60) with zero duplicates.
- `aflack trace-show <trace_id>` replays the full event trace.
- DB integrity: `count(insights) == count(distinct content_hash)`.

## Next (Iteration 4 candidates)

1. Implement the Aside `scan_fn` adapter for IG/TikTok top-creator surfing.
2. Add ROI Sentinel daemon (warn on negative contribution margin).
3. Add memory-consolidation job that promotes high-confidence insights into semantic MCP.
4. Auto-open PR-style proposals into real `.claude/skills` files (still human-approved).
5. Frameworkize into `creator-commerce-ops` once economics gate passes.
