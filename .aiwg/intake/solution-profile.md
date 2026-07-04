# Solution Profile

**Project**: Automated Affiliate Content Pipeline
**Generated**: 2026-07-03
**Profile recommendation**: **Prototype / MVP**

## Recommended Profile

**Selected profile**: MVP (local-first, fast validation)

**Why**:
- Target is operational within **1 week**, not enterprise rollout.
- Single operator, local machine, no team coordination overhead.
- High uncertainty around niche/product/content fit; the system must learn quickly.
- Long-term architecture should remain clean enough to evolve into an owned e-commerce content engine.

## Priority Weights

| Dimension | Weight | Rationale |
|---|---:|---|
| Speed | 0.40 | One-week operational target; learn from real outputs quickly. |
| Quality | 0.25 | Generated personas/videos must be realistic enough to benchmark against top creators. |
| Compliance/Risk | 0.20 | Beauty/health content can easily cross into medical/FTC issues; publish gate is mandatory. |
| Cost | 0.15 | Local-first reduces infra cost, but Higgsfield/API usage will be variable. |

Total: 1.00

## Economics / MMR Gate

The system should not scale — and should not be promoted into a formal AIWG framework — until it demonstrates real economics. For this project, **MMR/MRR** is a working shorthand for monetized monthly revenue until a formal accounting model is chosen.

Track at minimum:

- Higgsfield credits spent per generated video.
- LLM/token spend per generated script, persona, review, and research run.
- Market-intelligence/tool subscription spend.
- Operator time per publishable video.
- Cost per generated video.
- Cost per publishable/compliance-approved video.
- Cost per validated/winning video.
- Affiliate clicks, conversions, commission revenue, refunds/chargebacks where visible.
- Contribution margin after credits/tokens/tool spend.
- MMR/MRR and trend by niche.
- Per-platform RPM/revenue: YouTube long-form (highest RPM), YouTube Shorts, TikTok Creator Rewards, affiliate commission, brand deals. Track revenue per platform per million views so distribution effort follows the money (YouTube long-form is the strongest monetization surface).

**Scale gate**: a niche can move from diagnostic to repeatable production only when contribution margin is positive and the creative loop produces repeatable winners without uncontrolled credit/token burn.

**Frameworkization gate**: graduate into an AIWG framework only after at least one niche shows repeatable positive economics and the pipeline has reusable rules, skills, workflows, behaviors, and agent roles that are stable enough to package.

## Scale Assumptions

- **Operators**: 1
- **Video generation target**: ~20 videos/day
- **Niches at MVP**: 1 narrow beachhead niche
- **Products under active test**: 3–10 at a time
- **Personas**: 3–5 reusable AI personas initially
- **Benchmark set**: 15–50 winning videos/products per niche
- **Memory/event volume**: low-to-moderate, but must be structured from day one to prevent context rot.

## Recommended Technical Shape

### Local modular pipeline

Run as local scripts/services with clearly separated modules:

- `research_ingest`: Firecrawl, Creative Center, third-party tools, Aside workflows
- `benchmarking`: gold-set builder + video/product tagging
- `persona`: persona briefs + Higgsfield identity/reference workflow
- `script`: hook/template/script generation + claim-safety hints
- `generation`: Higgsfield image/video/Marketing Studio integration
- `validation`: Virality Predictor + benchmark comparison
- `compliance`: FTC/TikTok/AI-persona checks + human approval
- `publishing`: submit compliance-approved creatives to **Postiz** (`gitroomhq/postiz-app`) for scheduling/posting via its Public API / SDK / agent CLI; Aside fallback for blocked flows
- `memory`: capture hooks + retrieval over event store

### Source of truth

- **Local Postgres** for structured events/results; confirmed local-first. Evaluate **pgGraph** as the in-Postgres graph layer and **pgvector** for embeddings so the v1 memory substrate can be relational + graph + vector without a separate graph DB.
- **Local object storage / filesystem** for videos, screenshots, transcripts, product pages, and generated assets.
- **Memory engines as indexes**, not the source of truth.

### Posting / scheduling profile

Use **Postiz** (`gitroomhq/postiz-app`) as the open-source social scheduling/posting layer. Keep Postiz as a separate self-hosted service and integrate over its Public API / Node SDK / `postiz-agent` CLI. This prevents the MVP from spending a week hand-rolling YouTube/TikTok/Instagram/X posting adapters.

License boundary: Postiz is **AGPL-3.0**. Internal self-hosted use is fine for this MVP. If/when this project becomes an AIWG framework, Postiz should be documented as an external optional dependency; do not vendor or modify/distribute Postiz source unless we accept AGPL obligations.

### Memory profile

- **Coding/build memory**: agentmemory remains active for engineering session memory.
- **Marketing-domain memory**: evaluate Mem0, Zep/Graphiti, and Cognee.
- **Minimum v1 requirement**: capture episodic events, semantic facts, and procedural rules without dumping full history into context.

## Security / Compliance Posture

**Selected posture**: Baseline + marketing/compliance hard gates.

### Required controls

- Store credentials/tokens outside committed files.
- Separate raw evidence (screenshots/pages/videos) from distilled memory.
- Maintain source links/provenance for market research and claims.
- Apply a pre-publish compliance checklist to every video:
  - Affiliate disclosure present and clear.
  - No prohibited medical/weight-loss/diagnostic claims.
  - No false firsthand claims by AI personas.
  - No impersonation of real people.
  - Product claims align with source/label.

## Operational Profile

**MVP cadence**:

- Daily: generate and validate ~20 videos.
- Daily: record results and learnings.
- Weekly: kill/iterate/scale the current niche.
- Per niche: maintain a benchmark gold set and a niche scorecard.

**Human gates**:

- Product shortlist approval.
- Persona approval.
- Compliance approval before publishing.
- Niche pivot / scale decision.

## Key Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---:|---|
| AI content looks generic / not competitive | High | High | Benchmark against top creators + Virality Predictor gate before publish. |
| Health/beauty claims violate platform/FTC rules | Medium | High | Claim classifier + human compliance gate. |
| Third-party intelligence source breaks | High | Medium | Swappable adapters + Aside logged-in fallback. |
| Context/memory rot from too much experiment data | Medium | High | Own raw event store; dedup-on-write; relevance-gated retrieval; temporal invalidation. |
| One-week scope creep | High | High | MVP = one niche, 3–5 personas, one generation path, one validation path. |

## Profile Overrides

- Although MVP profile normally minimizes architecture, the memory/event-store decision is intentionally stronger because the project depends on compounding learning.
- Direct-to-main delivery is acceptable because this is a solo local project.

## Recommended Phase Entry

Proceed to **Inception** after intake review, but keep the first week as an MVP construction sprint:

1. Confirm beachhead niche.
2. Define MVP schema + capture hooks.
3. Build first pipeline loop.
4. Generate and validate first batch.
5. Retrospective into memory.

## Long-Term AIWG Framework Direction

The local MVP is the proving ground. The desired end state is an AIWG framework inside the user's AIWG fork with:

- **Rules**: compliance, disclosure, no-medical-claims, ROI gating, memory capture, benchmark-before-publish.
- **Skills**: niche diagnostics, product research, benchmark gold-set creation, persona design, Higgsfield generation, Virality Predictor scoring, compliance review, performance digest.
- **Workflows/flows**: discover → select → generate → validate → publish → analyze → learn → scale/kill.
- **Behaviors**: background monitoring of trends, daily generation loop, result capture, memory consolidation, and alerting when a niche crosses a scale/kill gate.
- **Agents/daemon-like roles**: market researcher, product scout, persona director, scriptwriter, creative producer, compliance reviewer, benchmark analyst, performance analyst, memory curator, orchestration daemon.

Do not scaffold the full framework prematurely. Pilot the pieces as local project artifacts first; promote only proven, repeatable components.
