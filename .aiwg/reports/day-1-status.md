# Day-1 Status — Local Event Store + Memory Substrate

**Date**: 2026-07-04
**Status**: Core database substrate validated

## Completed

- Built custom local Docker image:
  - `aflack/pggraph-pgvector:0.1.8-pgvector0.8.4`
  - base: `ghcr.io/evokoa/pggraph:0.1.8`
  - added: `postgresql-17-pgvector` 0.8.4
- Recreated local dev volume and container:
  - container: `pggraph`
  - host binding: `127.0.0.1:55432`
  - volume: `aflack_pggraph_data`
- Verified extensions:
  - `graph` 0.1.8
  - `pg_cron` 1.6
  - `vector` 0.8.4
- Added project scaffold:
  - `pyproject.toml`
  - `.env.example`
  - `src/aflack/`
  - `db/migrations/001_init.sql`
  - `docker/pggraph-pgvector/`
- Created v1 event-store schema:
  - `niches`
  - `products`
  - `personas`
  - `hooks`
  - `scripts`
  - `creatives`
  - `creative_variants`
  - `channels`
  - `disclosures`
  - `claims`
  - `results`
  - `lessons`
  - `cost_ledger`
- Created thin swappable memory interface:
  - `src/aflack/memory.py`
- Validated graph traversal on the real v1 schema:
  - Product → Script → Creative → Result
  - Product → Niche → Hook
  - Script → Persona
- Verified Higgsfield CLI authentication:
  - account: `tech@chronode.ai`
  - plan: ultra
  - credits at check: 5010

## Notes

- `CostLedger` exists from day one and is ready to track Higgsfield credits, token spend, tool spend, operator time, and other costs.
- pgGraph remains alpha. It is validated locally, but all callers should go through the project abstraction layer rather than depending on pgGraph directly.
- The first manual smoke row set is placeholder data and can be cleared before real production testing if desired.

## Next Day-1/Day-2 tasks

1. Add migration history table (optional but recommended before many migrations).
2. Add economics rollup query/command.
3. Run niche-diagnostic scorecard and pick the first beachhead niche.
4. Build first research ingestion adapter.
5. Define daily credit/token/operator-time caps in the economics ledger.
