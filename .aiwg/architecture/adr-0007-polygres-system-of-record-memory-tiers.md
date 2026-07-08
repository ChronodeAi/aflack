# ADR-0007: Local Postgres/pgGraph/pgvector as the organization system of record; agentmemory and fortemi as derived per-role and semantic indexes

**Status**: Accepted for local MVP; revisit when multi-agent org roles are introduced
**Date**: 2026-07-07

## Context

The project already runs three memory-related systems:

- **Local Postgres + pgGraph + pgvector** (internal shorthand: "Polygres-style
  local stack") — the architecture pattern from ADR-0002 and ADR-0003. Postgres
  is the relational source of truth; pgGraph adds relationship traversal;
  pgvector adds semantic retrieval. All three operate over the **same** rows.
- **agentmemory** (`:3111`) — episodic/working memory for the building/coding agents.
- **fortemi** (`:3113`) — semantic-memory MCP used for knowledge/capability recall
  and AIWG indexing.

As the system grows from a solo-operated content pipeline toward an agentic
**marketing team**, and eventually a brand/ecommerce **company** with traditional
roles (CEO, CFO, CMO, and functional agents), a recurring risk appears: each new
role/agent could invent its own memory or treat a derived index as truth. That
would fracture the source of truth, create lock-in, and make company-level
questions (revenue, cost, margin, provenance, accountability) unanswerable.

ADR-0002 already established that Postgres is the single source of truth and that
memory engines are derived indexes populated **from** the event store. This ADR
extends that principle explicitly to the **organizational/role model**.

Naming boundary: **Polygres is the name of an external company's brand/product
for a cloud-facing combination of these Postgres components.** In this project,
do not present Polygres as our product, brand, or public marketing name. Use it
only as an internal shorthand/category reference for the local pattern, while
code and architecture documents should continue to name the concrete local
components: Postgres, pgGraph, and pgvector.

## Decision

Adopt a three-tier memory model with strict roles:

1. **Local Postgres + pgGraph + pgvector = system of record (SoR).**
   - The authoritative operating ledger for the organization: facts
     (`niches`, `personas`, `products`, `creatives`, `publish_queue`, `results`,
     `cost_ledger`, `funnel_keywords`, `lead_magnets`, `analytics_snapshots`,
     `benchmark_creators`, `benchmark_videos`, `insights`,
     `improvement_proposals`, `pipeline_events`, `daemon_runs`).
   - Relationships are served by **pgGraph** over these tables.
   - Meaning/similarity is served by **pgvector** embedding columns over these
     tables.
   - Consumer verbs (from the internal Polygres-style positioning): **ask what happened**
     (facts/events), **follow what connects** (graph), **search what it
     resembles** (vector).

2. **agentmemory = per-role episodic/working memory (derived).**
   - How an individual agent/role did its work: session continuity, working
     notes, in-flight context.
   - Never the authoritative store for business facts.

3. **fortemi = semantic recall index (derived).**
   - Knowledge/capability retrieval and "resembles this" search across distilled
     knowledge.
   - Populated from the local SoR content (e.g., promoted high-confidence insights),
     never the authoritative store.

### Invariants (enforced going forward)

- **I1 — Truth lands in the local SoR first.** Any business fact, decision, cost,
  result, or artifact reference is written to local Postgres before it is
  projected into agentmemory or fortemi.
- **I2 — Derived indexes are rebuildable.** agentmemory and fortemi content must
  be reconstructable from the local SoR via re-ingest. Losing a derived index is a
  re-index, not data loss.
- **I3 — No role owns private truth.** A new role/agent may keep episodic state
  in agentmemory, but its authoritative outputs (spend, results, approvals,
  provenance) must be written to the local SoR.
- **I4 — Swappable engines.** pgGraph/pgvector/agentmemory/fortemi sit behind an
  abstraction; replacing any of them is a re-ingest from the local SoR (per
  ADR-0002).
- **I5 — Human gates are recorded in the local SoR.** Public publish, paid
  generation, account changes, and DM/comment automation approvals are recorded
  as events in the SoR, not only in agent memory.
- **I6 — Polygres name stays internal.** Do not use "Polygres" as an outward
  product/brand claim for this project. The external company/product may serve
  cloud users later; this project remains a local implementation of the
  component pattern.

## Organizational role → memory-layer mapping

This mapping is the contract new agent roles inherit by design.

| Role (agent) | Primary need | Local SoR (Postgres + pgGraph + pgvector) | agentmemory (episodic) | fortemi (semantic) |
|---|---|---|---|---|
| CEO | Cross-functional truth: what happened, what it costs, what's blocked | Read (facts, results, cost, gates) | — | Optional recall |
| CFO / economics | Cost, revenue, contribution margin, ROI scale gate | Read/write (`cost_ledger`, `results`, `analytics_snapshots`) | — | — |
| CMO / marketing lead | Campaign/creative/funnel performance and connections | Read/write + pgGraph traversal | Light planning notes | Recall similar plays |
| Content/creative agents | Produce packages and creatives | Write outputs + provenance | Working state/session continuity | Recall similar hooks/formats |
| Research/insights agents | Find and distill patterns | Write `insights`, `benchmark_*` | Scan session state | Primary: "resembles this" search |
| Compliance/legal | Enforce disclosures, claims, provenance, gates | Read disclosures/claims/provenance; record gate decisions | — | — |
| Ops/daemon | Autonomous scan→distill→propose loop | Write `pipeline_events`, `daemon_runs`, proposals | — | Reinforce/promote insights |

## Why not collapse into agentmemory or fortemi

- agentmemory is per-agent and episodic; it cannot serve as the accountable,
  org-wide ledger a CEO/CFO needs.
- fortemi is semantic search; it answers "resembles this," not "what is true and
  what did it cost."
- Only a relational SoR with graph + vector projections answers facts,
  relationships, and meaning over the same authoritative rows — which is exactly
  the local component composition we run.

## Consequences

- Positive: clean separation of concerns; no lock-in; company-level questions
  remain answerable; new roles inherit the correct substrate.
- Positive: agentmemory/fortemi stay cheap, disposable, and rebuildable.
- Negative: we own the local SoR schema, migrations, and (as roles grow) role
  access and audit.
- Negative: pgGraph is early alpha (ADR-0003); multi-writer/role scale is a
  revisit trigger.

## Revisit triggers

Re-open this ADR when any of the following occur:

1. Introducing concurrent multi-agent org roles (CEO/CFO/CMO agents) that write
   to the local SoR simultaneously → add role-scoped access + audit trail, and confirm
   or replace pgGraph for concurrent production use.
2. Moving beyond single-machine/local deployment.
3. Adding a second brand/tenant → decide single-tenant vs multi-tenant SoR.
4. External Polygres product changes the integration landscape → decide whether
   to remain fully local, integrate, or migrate any derived/index layer. The
   source-of-truth rule still applies unless superseded by a new ADR.

## Related

- ADR-0002 (own the raw event store; engines are derived indexes)
- ADR-0003 (Postgres + pgGraph + pgvector memory substrate)
- ADR-0005 (human-gated content-agent orchestration)
- `.aiwg/architecture/software-architecture-document.md` (§3, §5, §7)
- `.aiwg/marketing/strategy/polygres-positioning.md`
- `.aiwg/planning/continuous-improvement-architecture.md`
