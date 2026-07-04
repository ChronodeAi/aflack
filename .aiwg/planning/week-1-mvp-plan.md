# Week-1 MVP Execution Plan — Affiliate Content Pipeline

**Created**: 2026-07-03
**Owner**: Solo operator
**Goal**: An end-to-end local pipeline that can research → generate → validate → compliance-gate → publish/test → capture results, producing toward ~20 videos/day, operational within 7 days — and ROI-aware from day one.
**Runtime**: Local macOS. Delivery: direct commit to `main`.

## Guiding constraints

- Local-first, solo, no cloud dependency for the core loop.
- Research-first: Firecrawl for broad web, Aside for logged-in surfaces; prompt operator to log in when needed.
- Compliance is a hard pre-publish gate (FTC disclosure, no medical/weight-loss claims, AI-persona honesty, no impersonation).
- Every stage writes to the local event store so nothing is forgotten.
- Track economics from the first generated video (credits, tokens, tool spend, operator minutes).
- Swappable adapters: research source, memory engine, generation model, publish target.

## Success criteria (end of week 1)

- [ ] One narrow beachhead niche selected via the scorecard.
- [ ] Benchmark gold set built (15–50 top videos/products) for that niche.
- [ ] 3–5 reusable AI personas created (non-impersonating, disclosed).
- [ ] Generation wrapper producing batches via Higgsfield.
- [ ] Validation gate wired: Virality Predictor score + benchmark comparison.
- [ ] Compliance checklist enforced before any publish.
- [ ] First batch published/tested for the niche.
- [ ] Results + costs captured to the event store and memory.
- [ ] Economics dashboard shows cost per generated / publishable / winning video.

## Tech decisions to lock on Day 1

- **Language**: Python for pipeline + data; reuse existing Node CLIs (Higgsfield, aiwg, aside) via subprocess.
- **Event store**: local Postgres (source of truth) + local filesystem/object storage for media/evidence.
- **Coding memory**: agentmemory (already running).
- **Marketing memory**: defer engine choice; write a thin `memory` interface now, run the Mem0/Zep-Graphiti/Cognee bake-off in week 2. Do not block week-1 on it.

## Day-by-day plan

### Day 1 — Foundations + economics schema
- Create repo structure: `src/`, `src/pipeline/`, `src/adapters/`, `src/memory/`, `data/`, `artifacts/` (gitignored media).
- Stand up local Postgres; define the data model (below).
- Implement the **economics ledger** table first — every generation/publish writes cost rows.
- Wire config/secrets loading (`.env`, gitignored).
- Smoke-test Higgsfield CLI auth (`higgsfield account status`).

### Day 2 — Research + niche diagnostic
- Build `research_ingest` adapter: Firecrawl + TikTok Creative Center; Aside fallback for logged-in.
- Run the niche-diagnostic scorecard (`.aiwg/marketing/strategy/niche-diagnostic-plan.md`) on candidate niches.
- Select the ONE beachhead niche. Record decision + rationale to memory.

### Day 3 — Benchmark gold set + product shortlist
- Build `benchmarking` module: pull + tag 15–50 top videos/products for the niche (hook, retention proxy, format, duration, persona, proof, CTA, disclosure, claim-risk).
- Produce a product shortlist (3–10) with affiliate availability + margin notes.
- Define numeric benchmark thresholds (e.g., hook target = retain 55%+ at sec 3).

### Day 4 — Personas + scripts
- Build `persona` module: 3–5 personas via Higgsfield (identity/reference), with an ethics/disclosure policy per persona.
- Build `script` module: hook/template/script generation conditioned on the gold set + claim-safety rules.
- Generate 5 scripts/product for the shortlist.

### Day 5 — Generation + validation
- Build `generation` module: Higgsfield batch (Marketing Studio / Seedance), 9:16, target volume.
- Build `validation` module: Higgsfield Virality Predictor (`brain_activity`) scoring + benchmark comparison; set a pass/fail threshold.
- Iterate creatives until they clear the gate; log all costs.

### Day 6 — Compliance + publish/test
- Build `compliance` module: automated checklist (disclosure present, no medical/weight-loss claims, no false firsthand claims, no impersonation, claims match source) + human approval gate.
- Publish/test the first approved batch (manual/semi-automated).
- Capture publish metadata + disclosures used.

### Day 7 — Results, memory, retrospective
- Build `results` capture: pull post-publish metrics; write to event store.
- Run memory capture hooks: episodic (this batch), semantic (niche facts), procedural (what worked).
- Compute economics: cost per generated / publishable / winning video; affiliate outcomes if any.
- Retrospective: scale / iterate / kill decision for the niche; record next-week plan.

## Data model (v1)

Core entities (each also links back to raw evidence in the event store):

| Entity | Key fields |
|---|---|
| Product | id, niche, title, source_url, affiliate_program, commission, margin_notes |
| Niche | id, name, scorecard, status (diagnostic/active/killed) |
| Persona | id, name, higgsfield_ref, ethics_policy, disclosure_mode |
| Hook | id, niche, text, source_ref, benchmark_metrics |
| Script | id, product_id, persona_id, hook_id, body, claim_flags |
| Creative | id, script_id, higgsfield_job_id, media_path, duration, cost_credits |
| Variant | id, creative_id, change_note |
| Channel | id, platform, account_ref |
| Disclosure | id, creative_id, type (text/onscreen/spoken), content |
| Claim | id, script_id/creative_id, text, risk_level, decision |
| Result | id, creative_id, channel_id, views, retention, ctr, conversions, revenue |
| Lesson | id, scope (episodic/semantic/procedural), content, links |
| CostLedger | id, ref_type, ref_id, cost_type (higgsfield/token/tool/operator), amount, ts |

## Economics tracking (from Day 1)

Every generation and publish writes to `CostLedger`. Daily rollup computes:
- cost per generated video,
- cost per publishable (compliance-approved) video,
- cost per validated/winning video (cleared gate + positive signal),
- gross affiliate revenue, contribution margin, MMR/MRR by niche.

## Risks this week + mitigations

| Risk | Mitigation |
|---|---|
| Higgsfield credit burn during iteration | Set a daily credit cap; validate cheaply (lower res) before final renders; log every job cost. |
| Compliance slip on health/beauty | Hard gate + human approval; claim classifier before generation, not just after. |
| Scope creep past 7 days | One niche, 3–5 personas, one generation path, one publish path. Defer memory bake-off to week 2. |
| Logged-in source blocked | Prompt operator to sign into Aside; build a reusable Aside skill for that site. |
| Data source breaks mid-week | Adapter interface + Aside fallback. |

## Out of scope this week

- Owned e-commerce store / private label.
- Multi-niche scaling.
- Full AIWG framework scaffolding (gated on ROI — see `frameworkization-roadmap.md`).
- Fully autonomous publishing without human approval.
- Marketing-memory engine selection (thin interface now, bake-off week 2).

## Immediate next actions (Day 1 kickoff)

1. Confirm Postgres availability locally (or choose SQLite fallback for week 1).
2. Create `src/` skeleton + `CostLedger` + data model migrations.
3. Verify Higgsfield auth + a 1-credit smoke generation.
4. Confirm which niches to run through the scorecard on Day 2.
