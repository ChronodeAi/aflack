# ADR-0003: Use local Postgres + pgGraph + pgvector as the v1 memory substrate

**Status**: Accepted for local MVP; revisit after week-2 bake-off
**Date**: 2026-07-04

## Context

The project needs episodic, semantic, and procedural memory without context rot. We evaluated agentmemory as the reference pattern and considered Mem0, Zep/Graphiti, Cognee, Letta/MemGPT, and pgGraph.

For week 1, the system is local, solo-operated, and needs a simple, inspectable substrate. We already own Postgres as the raw event store.

## Decision

Use **local Postgres + pgGraph + pgvector** as the v1 memory substrate:

- Postgres = relational source of truth.
- pgGraph = graph traversal over the relational model.
- pgvector = embedding columns for semantic retrieval.
- `lessons` table = episodic/semantic/procedural distilled memories with validity windows (`valid_at`, `invalid_at`).

Keep the memory/query interface swappable. Compare Mem0, Zep/Graphiti, and Cognee in week 2 only after real data exists.

## Validation

On 2026-07-04:

- Built image `aflack/pggraph-pgvector:0.1.8-pgvector0.8.4`.
- Verified extensions: `graph` 0.1.8, `pg_cron` 1.6, `vector` 0.8.4.
- Migrated v1 schema.
- Traversal smoke passed on real domain model: Product → Script → Creative → Result.

## Risks

- pgGraph is early alpha. Use locally only; keep behind abstraction.
- pgGraph is traversal, not a full temporal KG; stale-fact controls are implemented in our schema (`valid_at`, `invalid_at`) and consolidation logic.
- Schema teardown needs care: dropping registered tables can leave dangling pgGraph registrations.

## Related

- ADR-0002 (own event store)
- `.aiwg/research/affiliate-content-pipeline/pggraph-evaluation.md`
