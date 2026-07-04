# Software Architecture Document (SAD) — Affiliate Content Pipeline (MVP)

**Created**: 2026-07-04
**Status**: Elaboration baseline
**Scope**: Local, solo-operated GTA6 AI-persona gaming content pipeline (Beachhead A), YouTube-first.

## 1. Architectural goals & constraints

- Local-first, single operator, runs on one macOS machine.
- Research-first; compounding memory without context rot.
- Compliance is a hard pre-publish gate (FTC + platform + AI-persona + IP).
- ROI-aware from day one (cost ledger).
- Swappable adapters (research source, memory engine, generation model, publisher).
- Lean roles: 1 director runtime + 1 operator + 2 active personas.
- Do not vendor AGPL Postiz; integrate over its API as a separate service.

## 2. System context

```
          +-------------------- operator (human) --------------------+
          |                                                          |
   research sources          director runtime            publishing/scheduling
  (Firecrawl, Aside,   ->   (Claude Code CLI,     ->    (Postiz self-hosted) -> platforms
   Creative Center)          claude-fable-5)                                    (YouTube-first)
          |                        |                                            |
          v                        v                                            v
        event store (Postgres + pgGraph + pgvector)  <----- results/analytics ---+
                      ^  generation: Higgsfield  ^
                      +----- memory/lessons ------+
```

## 3. Components

| Component | Responsibility | Tech |
|---|---|---|
| Event store | Source of truth: entities, costs, results | Postgres 17 |
| Graph index | Relationship traversal over tables | pgGraph 0.1.8 |
| Vector index | Semantic retrieval | pgvector 0.8.4 |
| Memory interface | Episodic/semantic/procedural lessons | `src/aflack/memory.py` |
| Research adapter | Ingest trends/benchmarks | Firecrawl + Aside (CLI fallback) |
| Director runtime | Plans scripts/shots/prompts, enforces gates | Claude Code CLI `claude-fable-5` |
| Generation | Original AI persona video/images | Higgsfield CLI |
| Validation | Virality Predictor + benchmark compare | Higgsfield `brain_activity` + gold set |
| Compliance gate | FTC/platform/IP/persona checks | `src/aflack` (to build) + human approve |
| Publisher | Queue → Postiz scheduling | `src/aflack/publishing.py` + Postiz API |
| Economics | Cost/revenue rollups | `cost_ledger` + queries |

## 4. Key decisions (ADRs)

- ADR-0001 Postiz for scheduling/posting (AGPL boundary: API-only).
- ADR-0002 Own the raw event store; engines are derived indexes.
- ADR-0003 Local Postgres + pgGraph + pgvector v1 memory substrate.
- ADR-0004 Claude Code CLI (`claude-fable-5`) as director runtime.
- ADR-0005 Human-gated Jarvis content-agent orchestration.
- ADR-0006 Virality-first lane selection and persona-optional form.

## 5. Data architecture

Core entities: niches, products, personas, hooks, scripts, creatives, creative_variants, channels, disclosures, claims, results, lessons, cost_ledger, publish_queue, platform_credentials. The Jarvis/content-factory data products are hook library, source/reference library, asset library, funnel map, performance log, compliance/provenance record, and memory lessons. Graph derived via `graph.auto_discover`. Embeddings on hooks/scripts/lessons (`vector(384)`).

## 6. Runtime flows

1. Research → benchmark gold set → niche/product selection.
2. Director plans persona + hook + script (compliance-aware).
3. Higgsfield generates ORIGINAL visuals (no Rockstar footage).
4. Validation: Virality Predictor score + benchmark compare; iterate.
5. Compliance gate (auto checklist + human approve).
6. Publisher enqueues → Postiz schedules/posts (YouTube-first).
7. Results captured → memory lessons → economics rollup → scale/kill.

### Jarvis/director loop

The director loop is human-gated: Trend Scout → Source/Reference → Hook Author → Creative Producer → Editor/Packager → Compliance Reviewer → Publisher → Analytics/Memory Curator. These roles start as thin commands/runbooks over the event store and may become agents or daemons only after the manual loop proves repeatable economics.

## 7. Cross-cutting concerns

- Security: secrets in `.env`/Postiz config, never git; DB bound to localhost.
- Compliance: pre-publish blocking gate; provenance recorded.
- Cost control: every generation/publish writes `cost_ledger`; daily caps.
- Observability: agentmemory for build; event store for pipeline; Postiz for posting status.
- Resilience: adapters swappable; Aside fallback when APIs break.

## 8. Deployment (local)

- `pggraph` container (127.0.0.1:55432) — event store + memory.
- `postiz` stack (localhost:4007) — separate compose in `.aiwg/working/postiz/`.
- Python package `aflack` in `.venv`.
- Higgsfield + Claude + Aside via local CLIs.

## 9. Out of scope (MVP)

- Cloud deployment, multi-operator, owned e-commerce store, full AIWG framework, autonomous publishing, daemon roster.

## 10. Human-gated boundaries

- Postiz admin account creation + social OAuth connections.
- YouTube channel connection + API audit path.
- Real paid Higgsfield generation batches (credit spend).
- Actual public publishing.
- Comment, DM, follow, channel setting, account setting, paid promotion, or ad-spend actions.
