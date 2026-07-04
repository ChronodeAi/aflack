# ADR-0002: Own the raw event store; treat memory engines as derived indexes

**Status**: Accepted
**Date**: 2026-07-04

## Context

The pipeline's long-term value is compounding learning across experiments. Memory frameworks (Mem0, Zep/Graphiti, Cognee, pgGraph) each have their own storage models; committing our source of truth to any one of them creates lock-in and makes migration a salvage job.

## Decision

Own the **raw event store** as the single source of truth: local **Postgres** (relational rows) + local **object storage/filesystem** (media, screenshots, transcripts, product pages, generated assets). All memory/graph/vector engines are **derived indexes** built over these tables. Switching engines becomes a re-ingest, not a rescue.

## Consequences

- Positive: no lock-in; engines are swappable; provenance and cost data live in our schema; deterministic backups.
- Positive: pgGraph/pgvector build indexes over the same tables (validated in ADR-0003).
- Negative: we maintain the schema + migrations ourselves.
- Rule: any new memory engine must be populated FROM the event store, never become the primary store.

## Related

- ADR-0003 (memory engine), `.aiwg/research/affiliate-content-pipeline/memory-system-research.md`
