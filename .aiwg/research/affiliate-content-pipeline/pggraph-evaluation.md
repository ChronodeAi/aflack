# pgGraph Evaluation Note

**Created**: 2026-07-03
**Candidate**: <https://github.com/Evokoa/pgGraph>
**Purpose**: Evaluate pgGraph as the local graph layer for the affiliate/content pipeline memory/event store.

## Summary

pgGraph is a PostgreSQL extension that adds graph search, traversal, shortest-path, and relationship queries directly over ordinary PostgreSQL tables.

The key fit for this project:

> Our tables stay the source of truth; pgGraph builds a derived graph index and queries it from SQL.

That matches the architecture decision to own the raw event store and treat graph/memory systems as derived indexes. It also keeps the system local and simple for a solo operator.

## Observed facts from repo/docs

- Repo: `Evokoa/pgGraph`
- Language: Rust (`pgrx` extension)
- Version shown in README: `0.1.8`
- License badge: Apache-2.0
- PostgreSQL support: 14–18
- Docker image: `ghcr.io/evokoa/pggraph:0.1.8`
- Homebrew tap: `Evokoa/tap/pggraph`
- Includes `pg_cron` in Docker quickstart with maintenance preconfigured.
- Maintainers mark it **early alpha** and recommend Docker or a dedicated development DB; avoid production use for now.

## Why it may be better than a separate graph DB for v1

- Keeps relational source-of-truth, graph traversal, and (with `pgvector`) embeddings inside one local Postgres instance.
- No separate Neo4j/Kuzu/Graphiti service required for week 1.
- Graph queries can be built directly over the marketing data model:
  - Product → Script → Creative → Result
  - Niche → Hook → Creative → Lesson
  - Persona → Creative → Result
  - Claim → ComplianceDecision → Creative
- `pg_cron` can support periodic graph refresh / memory consolidation jobs.

## Risks

- Early alpha; extension APIs and stability may change.
- Must not treat it as production-grade yet.
- We still need temporal validity semantics for stale facts; pgGraph provides graph traversal, not a full temporal knowledge-graph memory framework by itself.
- Need to test ergonomics: table registration, graph refresh, query complexity, and migration compatibility.

## Recommended v1 approach

Use pgGraph in local/dev only:

1. Start the pgGraph Docker image.
2. Create the v1 tables (`Product`, `Creative`, `Result`, `Lesson`, etc.).
3. Register relationships and build the graph index.
4. Run sample traversals:
   - Given a product, find related winning hooks within 2 hops.
   - Given a persona, find creatives with positive contribution margin.
   - Given a claim pattern, find all rejected scripts/creatives and their lessons.
5. Pair with `pgvector` for semantic retrieval over scripts, lessons, and benchmark notes.
6. Compare against Mem0/Zep/Graphiti/Cognee in week 2.

## Decision

Add pgGraph to the week-1 local database plan as the preferred first graph candidate, with the explicit caveat that it is alpha and must be kept behind a swappable memory/query interface.
