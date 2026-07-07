# ADR-0007: Memory system of record and week-2 bakeoff

**Status**: Accepted for MVP; bakeoff pending after first result loop  
**Date**: 2026-07-04  
**Decision owner**: Solo operator

## Context

The project currently uses several memory surfaces:

- agentmemory for coding-agent session memory and handoff/recall,
- local Postgres event-store tables for the content pipeline,
- pgGraph as a derived relationship/traversal index over those tables,
- pgvector columns reserved for semantic retrieval,
- project-local `.aiwg/` artifacts for human-ratified decisions, requirements, runbooks, and framework materials.

Open-source memory systems worth evaluating include Mem0, Zep/Graphiti, Letta/MemGPT, Cognee, GraphZep, and Postgres-native graph/vector projects. Polygres is relevant because it productizes the same direction we are already taking: Postgres plus graph traversal plus vector search plus hybrid retrieval APIs.

## Decision

Keep **Postgres as the pipeline memory system of record** for MVP Construction. Treat agentmemory, pgGraph, pgvector, and any future Mem0/Zep/Graphiti/Cognee/Letta integration as derived retrieval or orchestration layers.

The current implementation is:

- **Raw episodic trace**: `pipeline_events` keyed by `trace_id`.
- **Daemon run memory**: `daemon_runs`.
- **Benchmark memory**: `benchmark_creators`, `benchmark_videos`.
- **Semantic/procedural lesson memory**: `lessons` and `insights`.
- **Change memory**: `improvement_proposals` linking insights to skill/rule/workflow changes.
- **Relational source of truth**: core pipeline tables such as niches, hooks, scripts, creatives, claims, results, and cost ledger.
- **Graph memory**: pgGraph auto-discovers table relationships and provides traversal over the relational model.
- **Vector memory**: pgvector is installed; embedding columns exist but production embedding ingestion is not yet implemented.

## Memory taxonomy for this pipeline

| Memory type | Source of truth | Examples |
|---|---|---|
| Episodic | `pipeline_events`, `daemon_runs`, `benchmark_videos`, content-package artifacts | What happened in a scan, import, package build, compliance preflight, or publish attempt. |
| Semantic | `insights`, `lessons(scope='semantic')`, `.aiwg/research/` | Stable facts and distilled patterns: GTA6 rules, Postiz boundary, proven funnel patterns. |
| Procedural | `lessons(scope='procedural')`, `.aiwg/creator-commerce-ops/skills/`, `.aiwg/planning/` | How to author hooks, run the director loop, review virality, enforce compliance. |
| Strategic / ratified | ADRs, requirements, risk register, readiness reports | Human-approved decisions that should not be overwritten by transient agent memory. |

## Bakeoff candidates

| Candidate | Why evaluate | Likely role |
|---|---|---|
| Mem0 | Mature standalone memory layer for assistants/agents. | Optional derived memory API if we need cross-agent personalization. |
| Zep/Graphiti | Temporal knowledge graph with fact invalidation and hybrid retrieval. | Strong candidate for temporal fact/relationship extraction from transcripts and results. |
| Letta/MemGPT | Agent runtime with managed memory/context. | Evaluate only if we want agents to live inside Letta instead of our CLI/AIWG runtime. |
| Cognee | GraphRAG/data-ingestion memory platform. | Candidate for document/source corpus memory and ontology extraction. |
| GraphZep | TypeScript implementation of Zep-like temporal memory. | Candidate only if we shift orchestration toward Node/TS. |
| Polygres | Hosted Postgres + pgGraph + pgvector + retrieval APIs. | Future managed replacement for self-hosted local Postgres/pgGraph if operational burden grows. |

## Non-decisions

- Do not move the system of record into agentmemory.
- Do not adopt a second graph database before one complete publish/result/economics loop.
- Do not promote transient chat summaries into strategic memory without human-ratified artifacts.
- Do not rely on pgGraph alone as "memory"; it is a traversal/index layer over memory-bearing tables.

## Construction requirements

- Add embedding population and hybrid retrieval only after the current relational/trace loop is stable.
- Add a memory-consolidation job that promotes raw traces into semantic/procedural lessons.
- Add a memory bakeoff report after real publish/result/economics data exists.
- Preserve re-ingestability: every external memory engine must be rebuildable from Postgres rows and `.aiwg/` artifacts.

## Related

- ADR-0002 Own the raw event store
- ADR-0003 Local Postgres + pgGraph + pgvector memory substrate
- ADR-0005 Human-gated Jarvis content-agent orchestration
- `.aiwg/planning/daemon-runtime-architecture.md`
- `.aiwg/planning/continuous-improvement-architecture.md`
