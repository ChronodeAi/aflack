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

## Hands-on validation (2026-07-04, local Docker)

Ran the pinned image `ghcr.io/evokoa/pggraph:0.1.8` locally via Docker Desktop, bound to `127.0.0.1:55432`, persistent volume `aflack_pggraph_data`.

Confirmed:

- Extensions in image: `graph` 0.1.8 + `pg_cron` 1.6 on PostgreSQL 17.10.
- **pgvector is NOT in this image** — `vector` is not in `pg_available_extensions`. All-in-Postgres embeddings would need a custom image (add `pgvector`) or a separate vector store.
- `graph.auto_discover('public')` auto-registered 3 tables + 2 FK edges and built the graph (5 nodes / 8 edges) in one call — matches the README's FK-discovery claim.
- Domain-shaped 2-hop traversal validated: `graph.expand(product, id, 2)` returned Product → Creative → Result with readable paths; `graph.find_related(...)` returned results ranked by `revenue`. This is exactly our Product→Creative→Result / Persona→Creative→Result access pattern.
- Default `sync_mode=trigger`: pgGraph installs INSERT/UPDATE/DELETE/TRUNCATE triggers on registered tables to keep the derived graph fresh (can opt out with `graph.sync_mode='manual'`). Good for a live pipeline; note the trigger overhead on high-write tables.

Caveats found:

- **Alpha rough edge**: dropping a registered table leaves dangling graph registration — a subsequent `graph.build()` errors with `relation not found`. Deregister/clean graph state before dropping tables. Reinforces keeping pgGraph behind a swappable interface and treating schema changes carefully.
- API is function-based in the `graph` schema (`add_table`, `add_edge`, `auto_discover`, `build`, `expand`, `find`, `find_related`, sync-policy funcs) — usable directly from SQL, no new query language.

Verdict: **validated for Week-1 local use** as the graph layer over our own tables. Pair with a separate vector approach (custom image with pgvector, or external) until/unless pgvector is added to the image.

## Custom pgGraph + pgvector image validation (2026-07-04)

Built local image `aflack/pggraph-pgvector:0.1.8-pgvector0.8.4` from `ghcr.io/evokoa/pggraph:0.1.8` by installing `postgresql-17-pgvector`.

Confirmed on a fresh persistent volume:

- `graph` 0.1.8
- `pg_cron` 1.6
- `vector` 0.8.4
- v1 migration applied successfully.
- v1 tables created: `niches`, `products`, `personas`, `hooks`, `scripts`, `creatives`, `creative_variants`, `channels`, `disclosures`, `claims`, `results`, `lessons`, `cost_ledger`.
- Domain smoke seed passed: Product → Script → Creative → Result traversal works over the real v1 schema, and graph traversal also connects Product→Niche→Hook and Script→Persona.

Verdict update: **all-in-Postgres substrate validated locally** (relational + graph + vector). Continue to keep pgGraph behind the swappable memory/query interface because it is alpha.
