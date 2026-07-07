# Software Architecture Document (SAD) — Affiliate Content Pipeline (MVP)

**Created**: 2026-07-04
**Status**: Elaboration baseline with Controlled Construction addendum
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
| Memory interface | Episodic/semantic/procedural lessons; swappable backing engines | `src/aflack/memory.py` |
| Learning layer | Benchmark observations, insights, proposals, daemon runs | `src/aflack/learning.py`, `src/aflack/daemon.py` |
| Research adapter | Ingest trends/benchmarks | Firecrawl + Aside (CLI fallback) |
| Director runtime | Plans scripts/shots/prompts, enforces gates | Claude Code CLI `claude-fable-5` |
| Generation | Original AI persona video/images | Higgsfield CLI |
| Validation | Virality Predictor + benchmark compare | Higgsfield `brain_activity` + gold set |
| Compliance gate | FTC/platform/IP/persona checks | `src/aflack` (to build) + human approve |
| Publisher | Queue → Postiz scheduling | `src/aflack/publishing.py` + Postiz API |
| Economics | Cost/revenue rollups | `cost_ledger` + queries |
| Cockpit surface | Operator console integration via machine-readable CLI status/actions | AIWG Cockpit + `aflack * --json` commands |

## 4. Key decisions (ADRs)

- ADR-0001 Postiz for scheduling/posting (AGPL boundary: API-only).
- ADR-0002 Own the raw event store; engines are derived indexes.
- ADR-0003 Local Postgres + pgGraph + pgvector v1 memory substrate.
- ADR-0004 Claude Code CLI (`claude-fable-5`) as director runtime.
- ADR-0005 Human-gated Jarvis content-agent orchestration.
- ADR-0006 Virality-first lane selection and persona-optional form.
- ADR-0007 Memory system of record and week-2 bakeoff.
- ADR-0008 Draft ramp and analytics aggregation.

## 5. Data architecture

Core entities: niches, products, personas, hooks, scripts, creatives, creative_variants, channels, disclosures, claims, results, lessons, cost_ledger, publish_queue, platform_credentials. The Jarvis/content-factory data products are hook library, source/reference library, asset library, funnel map, performance log, compliance/provenance record, and memory lessons. Raw episodic traces live in `pipeline_events`; daemon run state lives in `daemon_runs`; distilled semantic/procedural patterns live in `insights`, `lessons`, and `.aiwg/` skills/rules/workflows. Graph derived via `graph.auto_discover`. Embeddings on hooks/scripts/lessons/insights are planned through `vector(384)`.

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

### Daemon runtime

The implemented daemon surface is the `improvement-daemon`: it ingests benchmark observations, distills deduped insights, creates improvement proposals, and records every run through `daemon_runs` and `pipeline_events`. It does not generate paid media, publish, change accounts, automate comments/DMs/follows, or edit framework files. The full daemon roster is deferred and documented in `.aiwg/planning/daemon-runtime-architecture.md`.

### Cockpit/control-plane addendum

AIWG Cockpit is the operator console for observing and steering Aflack sessions; it is not the Aflack domain brain and does not replace Postgres, the daemon safety model, Postiz, or AIWG CLI. Aflack exposes machine-readable status for Cockpit and future automation through JSON-capable CLI commands:

- `aflack daemon-status --json`
- `aflack analytics-status --json`
- `aflack publish-queue-status --json`
- `aflack compliance-smoke --json`
- `aflack prompt-quality --json`

The Cockpit layer may register these as actions and approval views. It must preserve the same human gates: public publish, account/channel settings, comments/DM/follows, ad spend, and broader daemon autonomy.

### Memory addendum

Postgres remains the content-pipeline system of record. `agentmemory` remains the coding-agent/session recall layer. pgGraph/pgvector remain local graph/vector substrates over Aflack-owned data. Memory engines are indexes or assistants, not authorities. Transcript and agentmemory lessons must be promoted into ADRs, rules, skills, tests, or explicit non-actions before they influence automation.

## 7. Cross-cutting concerns

- Security: secrets in `.env`/Postiz config, never git; DB bound to localhost.
- Compliance: pre-publish blocking gate; provenance recorded.
- Cost control: every generation/publish writes `cost_ledger`; daily caps.
- Observability: agentmemory for build; event store for pipeline; Postiz for posting status.
- Resilience: adapters swappable; Aside fallback when APIs break.
- Agent reliability: important skills, rules, daemon behaviors, and prompt contracts require deterministic checks or explicit no-check rationale; prose alone is not sufficient for automation.

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

## 11. Controlled Construction status

As of 2026-07-05, the MVP loop is constructed through the draft-ramp boundary: one measured Higgsfield batch is cost-captured, one private Postiz draft exists, analytics snapshots are wired, 67 unit/integration tests pass, draft-review learning is implemented, and prompt-quality hardening blocks safe-but-boring prompts. The project is not Transition/Production ready until render review, non-zero or explicit no-signal analytics, publish-quality learning, real Cockpit executor availability, and IOC traceability gates are satisfied.
