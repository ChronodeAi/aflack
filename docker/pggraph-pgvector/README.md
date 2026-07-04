# Local Postgres memory substrate (pgGraph + pgvector)

Local/dev-only image combining:

- **PostgreSQL 17.10**
- **pgGraph 0.1.8** (`graph` schema) — graph traversal over our own tables
- **pg_cron 1.6** — scheduled maintenance / consolidation jobs
- **pgvector 0.8.4** (`vector`) — embeddings for semantic retrieval

> pgGraph is early alpha. Use locally only, never in production.

## Build

```bash
docker build -t aflack/pggraph-pgvector:0.1.8-pgvector0.8.4 docker/pggraph-pgvector
```

## Run (localhost-only, persistent volume)

```bash
docker volume create aflack_pggraph_data
docker run -d --name pggraph \
  -e POSTGRES_PASSWORD=aflack_local_dev \
  -p 127.0.0.1:55432:5432 \
  -v aflack_pggraph_data:/var/lib/postgresql/data \
  aflack/pggraph-pgvector:0.1.8-pgvector0.8.4
```

Default DB: `graph`. Connection (local dev): `postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph`.

On a **fresh** volume the `vector` extension is auto-created by `docker-entrypoint-initdb.d/20-pgvector.sql`.
On an **existing** volume, run `CREATE EXTENSION IF NOT EXISTS vector;` once.

## Notes

- Bound to `127.0.0.1` only — not exposed to the network.
- Credentials here are local-dev throwaway values; real secrets go in `.env` (gitignored).
- Dropping a registered table leaves dangling pgGraph registration; clean graph state before schema teardown.
