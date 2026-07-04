# Option Matrix

**Project**: Automated Affiliate Content Pipeline
**Generated**: 2026-07-03
**Decision**: Week-1 architecture + memory strategy + market-intelligence approach

## Decision Criteria

| Criterion | Weight | Notes |
|---|---:|---|
| Speed to operational MVP | 0.30 | Must run within 1 week. |
| Compounding learning / memory quality | 0.25 | Core differentiator: never forget, no context rot. |
| Content quality / benchmarkability | 0.20 | Must compare to top creators and improve. |
| Compliance/risk control | 0.15 | FTC/TikTok/AI-persona rules. |
| Cost/complexity | 0.10 | Solo local operator. |

Total: 1.00

Scoring: 1 = poor, 5 = excellent.

## Option A — Local MVP modular pipeline + owned event store + memory bake-off

**Summary**: Build locally on this computer. Use modular adapters, Postgres/object storage as source-of-truth, agentmemory for coding memory, and a lightweight bake-off for marketing memory (Mem0 / Zep-Graphiti / Cognee). Use Creative Center + one paid/free research tool + Aside fallback.

| Criterion | Weight | Score | Weighted |
|---|---:|---:|---:|
| Speed | 0.30 | 4 | 1.20 |
| Memory quality | 0.25 | 5 | 1.25 |
| Content quality | 0.20 | 4 | 0.80 |
| Compliance | 0.15 | 4 | 0.60 |
| Cost/complexity | 0.10 | 3 | 0.30 |

**Total**: **4.15 / 5**

**Pros**:
- Best balance of speed and long-term architecture.
- Avoids lock-in by owning raw events.
- Allows memory-engine choice to be evidence-based.
- Fits solo local operation.

**Cons**:
- More setup than a pure no-code workflow.
- Memory bake-off adds early complexity.

## Option B — No-code/manual stack first, memory later

**Summary**: Use spreadsheets/Notion/Airtable, Higgsfield manually, and manual research tooling. Add memory/event store after product-market evidence.

| Criterion | Weight | Score | Weighted |
|---|---:|---:|---:|
| Speed | 0.30 | 5 | 1.50 |
| Memory quality | 0.25 | 1 | 0.25 |
| Content quality | 0.20 | 3 | 0.60 |
| Compliance | 0.15 | 2 | 0.30 |
| Cost/complexity | 0.10 | 5 | 0.50 |

**Total**: **3.15 / 5**

**Pros**:
- Fastest possible start.
- Lowest technical risk.

**Cons**:
- Recreates the exact "forgetting/context rot" problem.
- Hard to scale to 20 videos/day with learning loops.
- Later migration is painful because raw events are poorly structured.

## Option C — Cloud/SaaS-first automation platform

**Summary**: Build a cloud-hosted orchestrator with managed DB/object storage, full dashboards, team-ready deployment, and cloud workers.

| Criterion | Weight | Score | Weighted |
|---|---:|---:|---:|
| Speed | 0.30 | 2 | 0.60 |
| Memory quality | 0.25 | 4 | 1.00 |
| Content quality | 0.20 | 4 | 0.80 |
| Compliance | 0.15 | 4 | 0.60 |
| Cost/complexity | 0.10 | 2 | 0.20 |

**Total**: **3.20 / 5**

**Pros**:
- More production-ready if team grows.
- Easier scheduled/background generation at scale.

**Cons**:
- Overbuilt for solo/local week-1 MVP.
- Slower and more expensive.
- Requires more security/secrets/deployment work before proving niche.

## Option D — Autonomous-agent-first system (Letta/MemGPT-style)

**Summary**: Start by building a long-running autonomous content operator agent with self-managed memory, then connect tools.

| Criterion | Weight | Score | Weighted |
|---|---:|---:|---:|
| Speed | 0.30 | 2 | 0.60 |
| Memory quality | 0.25 | 4 | 1.00 |
| Content quality | 0.20 | 3 | 0.60 |
| Compliance | 0.15 | 2 | 0.30 |
| Cost/complexity | 0.10 | 2 | 0.20 |

**Total**: **2.70 / 5**

**Pros**:
- Attractive long-term vision.
- Agent can become an operator persona later.

**Cons**:
- Too much autonomy before guardrails.
- Compliance risk.
- Slower than week-1 MVP.

## Recommendation

Choose **Option A: Local MVP modular pipeline + owned event store + memory bake-off**.

## Immediate Build Sequence

1. Initialize repo and delivery policy (done: direct to `main`).
2. Draft local data model:
   - Product
   - Niche
   - Persona
   - Hook
   - Script
   - Creative
   - Variant
   - Channel
   - Disclosure
   - Claim
   - Result
   - Lesson
3. Build the first research adapter:
   - TikTok Creative Center / Firecrawl / Aside fallback.
4. Build benchmark gold-set artifact for one narrow niche.
5. Build Higgsfield generation wrapper:
   - 3 personas
   - 3 products
   - 5 scripts/product
6. Add validation:
   - Virality Predictor
   - benchmark comparison
   - compliance checklist
7. Publish/test manually at first.
8. Capture results into event store and memory.

## Decision Notes

- Starting niche remains to be chosen, but beauty/wellness is a plausible beachhead if framed carefully to avoid medical claims.
- Use "niche-diagnostic" as a repeatable pre-build phase for each new niche.
- Do not depend on a single market-intelligence vendor; all scraped sources must be adapters.
