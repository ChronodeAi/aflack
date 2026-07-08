# Polygres-style Local Stack — Internal Positioning Boundary

**Date**: 2026-07-07  
**Source**: operator-provided positioning diagram  
**Status**: internal reference only — not public marketing copy
**Architecture decision**: ADR-0007 defines the local Postgres + pgGraph +
pgvector stack as the organization system of record; agentmemory and fortemi are
derived indexes.
**Naming boundary**: "Polygres" is an external company's brand/product name for
this combined Postgres-component pattern. Do not claim it as our product or
external brand. We are running the pattern locally.

## One-line

Internal shorthand: local Postgres + pgGraph + pgvector = one local substrate
for facts, relationships, and meaning.

## The story arc (from the diagram)

The diagram tells a three-stage narrative:

1. **Inputs → Postgres source of truth**
   - Rows
   - Documents
   - Events
2. **Local Postgres + pgGraph + pgvector stack** — one local substrate combining three capabilities inside Postgres:
   - **Postgres → truth** (the source-of-truth tables)
   - **pgGraph → relationships** (how records connect)
   - **pgVector → meaning** (semantic similarity/embeddings)
   - Tagline: "One platform for facts, relationships, and meaning."
3. **Agents & Apps** consume it:
   - **Ask what happened** (query facts/events)
   - **Follow what connects** (traverse relationships)
   - **Search what it resembles** (semantic/vector search)

## Message architecture

| Layer | Capability word | What it means | Buyer benefit |
|---|---|---|---|
| Postgres | Truth | Durable, relational source of record | "Your data stays owned and consistent." |
| pgGraph | Relationships | Graph traversal over your own tables | "See how everything connects without a second database." |
| pgVector | Meaning | Embeddings + semantic search | "Find what's relevant, not just exact matches." |
| Agents & Apps | Action | Facts + relationships + meaning in one query surface | "Agents reason over one substrate instead of stitching systems." |

## Internal claims (safe wording)

- One local Postgres-based substrate for facts, relationships, and meaning.
- Postgres is the source of truth; graph and vector are derived views over the same data.
- Agents ask what happened, follow what connects, and search what resembles — from one local source-of-truth pattern.

## Proof anchors in this project

This positioning is not aspirational for `aflack` — the pipeline already runs on this substrate:

- Architecture: `.aiwg/architecture/software-architecture-document.md` (§3, §5).
- Decision: `.aiwg/architecture/adr-0003-local-postgres-pggraph-pgvector-memory.md`.
- Local image: `docker/pggraph-pgvector/` (Postgres 17 + pgGraph 0.1.8 + pgvector 0.8.4).
- Verified extensions via `aflack db-status`: `graph`, `pg_cron`, `vector`.
- "Source of truth" principle: raw events in Postgres; graph/vector are derived indexes (NFR-006).
- Org-memory decision: `.aiwg/architecture/adr-0007-polygres-system-of-record-memory-tiers.md`.

## Naming decision

- Treat **Polygres** as an external company's brand/product name.
- Do **not** adopt Polygres as our public product name.
- Keep internal implementation names concrete: Postgres, pgGraph, pgvector,
  agentmemory, fortemi.
- If referencing the external cloud product/company, be explicit that it is
  external and likely cloud-facing; our implementation remains local.

## Org-role positioning

The local Postgres + pgGraph + pgvector stack is the **company memory**, not just
the marketing team database:

- CEO asks: what happened, what changed, what is blocked?
- CFO asks: what did it cost, what returned, should we scale?
- CMO asks: which campaign/creative/funnel produced the signal?
- Compliance asks: which claims, disclosures, and approvals exist?
- Agents ask: what should I do next, what connects, what resembles this?

agentmemory is each role's notebook; fortemi is the semantic library; the local
Postgres/pgGraph/pgvector stack is the authoritative company ledger.

## Internal copy blocks the team can reuse in architecture discussions

**Headline options**

1. "Facts, relationships, and meaning in one local Postgres substrate."
2. "One source of truth. Three ways to reason over it."
3. "Postgres for truth. pgGraph for relationships. pgVector for meaning."

**Subhead**

> Agents ask what happened, follow what connects, and search what it resembles —
> all from one local Postgres-based substrate we own.

**Three-icon feature row**

- **Ask what happened** — query facts and events.
- **Follow what connects** — traverse relationships in the graph.
- **Search what it resembles** — semantic vector search over meaning.

## Compliance / accuracy guardrails

- Do not market "Polygres" as ours. It is an external brand/product name.
- pgGraph is early alpha; for external claims, describe it as "graph relationships over
  your Postgres tables," not as a hardened production graph database.
- Do not claim performance/scale numbers without a benchmark artifact.
- Keep "you own your data" claims consistent with the local-first architecture.

## Open items for the marketing team

1. Decide if this stays as architecture enablement copy only or becomes a
   background explainer for internal operator/team onboarding.
2. If external content references the stack, use component names rather than
   Polygres unless explicitly discussing the external company/product.
3. Decide whether to produce a branded **internal** diagram using our own naming.
