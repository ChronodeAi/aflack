# Daemon Runtime Architecture

**Date**: 2026-07-04  
**Status**: v1 improvement daemon implemented; full daemon roster deferred

## Purpose

The daemon system exists to make the content factory improve without requiring the operator to manually prompt every learning step. It is not an autonomous publishing system.

## Current implemented daemon

`improvement-daemon` is implemented in `src/aflack/daemon.py` and exposed through:

- `aflack improve-cycle`
- `scripts/aflack-improve-daemon.sh`
- `scripts/com.aflack.improve-daemon.plist`

The cycle is:

```text
scan input or existing benchmark rows
  -> ingest benchmark videos
  -> distill deduped insights
  -> propose skill/rule/workflow changes
  -> record trace
  -> stop before human-gated actions
```

## Runtime contract

Every daemon run must:

1. create a `daemon_runs` row,
2. create a `trace_id`,
3. append stage events to `pipeline_events`,
4. be idempotent or deduped,
5. declare blocked actions in the trace,
6. finish as `succeeded`, `failed`, `skipped`, or `blocked`,
7. write proposals instead of directly mutating framework files unless a human-approved apply workflow is explicitly invoked.

## Hard blocked actions

The daemon must not perform:

- paid Higgsfield generation,
- public publishing,
- Postiz draft submission when target/content ambiguity exists,
- account or channel setting changes,
- comment, DM, follow, or unfollow automation,
- paid promotion or ad spend,
- direct skill/rule/workflow edits without human approval,
- private API scraping.

## Planned daemon roster

| Daemon | Status | Responsibility | First trigger |
|---|---|---|---|
| Improvement Daemon | Implemented v1 | Distill benchmark observations into insights and proposals. | Manual CLI or launchd tick. |
| Trend Watcher | Deferred | Monitor trend sources and create candidate briefs. | After one results loop. |
| Gold-Set Refresher | Deferred | Refresh benchmark creators/videos and retire stale patterns. | After stable Aside scan adapter. |
| Memory Consolidator | Deferred | Promote raw traces into semantic/procedural lessons and derived memory indexes. | After embedding/hybrid retrieval decision. |
| ROI Sentinel | Deferred | Warn or block scale-up when contribution margin is negative. | After results/economics ingestion. |
| Publisher Sentinel | Deferred | Detect queued/draft items needing operator approval. | After Postiz draft loop is used. |

## Orchestration model

The current orchestration model is **single-process CLI plus scheduled ticks**:

- Python/Typer commands perform deterministic local operations.
- launchd/cron may call safe daemon ticks.
- Aside/Fugu or browser agents supply logged-in scan observations when needed.
- Claude Code/Codex acts as the human-facing director and applies approved framework changes.
- Postiz remains the external scheduling/posting boundary.

This can evolve into AIWG agents/behaviors later, but the MVP should keep daemon execution local, inspectable, and reversible.

## PSI-derived control plane target

The PSI project's RBI control-plane pattern is the right future shape for this daemon system once construction begins. The transferable model is explicit loop state, budget caps, constraints, append-only run logs, and verifier routing rather than hidden agent state.

Proposed construction layout:

```text
.aiwg/loops/content-factory/
  LOOP.md
  state.yaml
  budget.yaml
  constraints.yaml
  run-log.jsonl
```

The control plane should enforce:

- one active lock per loop run,
- explicit budget and spend caps,
- append-only run logging,
- deterministic verifier checks before gate decisions,
- no self-verification for high-risk actions,
- stop conditions for failed contracts, exhausted budget, unsafe actions, or missing operator approval.

This does not change the v1 daemon's current scope. It defines the construction target for making daemon behavior visible and auditable.

## Memory flow

```text
raw event or scan
  -> pipeline_events / benchmark_* tables
  -> insights / lessons
  -> improvement_proposals
  -> human-approved skill/rule/workflow change
  -> future production package
  -> result/economics data
  -> next learning cycle
```

agentmemory remains useful for agent-session recall. It is not the content-pipeline system of record.

## Construction gaps

- Add a visible `aflack daemon-status` command.
- Add a memory-consolidation command.
- Add embedding population for hooks/scripts/lessons/insights.
- Add a bakeoff report comparing Postgres/pgGraph/pgvector with Mem0, Zep/Graphiti, Cognee, and Letta after real result data exists.
- Add an approved proposal-apply command or PR-style workflow.
- Add the PSI-style `.aiwg/loops/content-factory/` control-plane files before enabling broader daemon autonomy.
- Add deterministic contract checks for new or changed skills, rules, workflows, agents, and daemon behaviors.
