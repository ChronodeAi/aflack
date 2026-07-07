# Project Intake Form

**Document Type**: Greenfield Project
**Generated**: 2026-07-03
**Source**: User description + interactive intake responses + research briefs under `.aiwg/research/affiliate-content-pipeline/`

## Metadata

- **Project name**: Automated Affiliate Content Pipeline (working name: "aflack")
- **Requestor/owner**: Solo operator (project owner)
- **Date**: 2026-07-03
- **Stakeholders**: Solo operator (owner/engineer/creative/reviewer). External dependencies: TikTok Shop/affiliate platforms, Higgsfield AI, Firecrawl, Aside browser, market-intelligence tools (Kalodata/FastMoss/EchoTik), memory engines.

## System Overview

**Purpose**: A locally-run, single-operator pipeline that researches trending affiliate products, generates lifelike AI personas and short-form UGC-style videos (via Higgsfield), benchmarks them against top-performing creator content, applies compliance gating, and publishes/tests them for affiliate revenue — starting narrow (one niche) and repeating the proven system across niches. Long-term: repurpose the pipeline to power an owned e-commerce store.

**Current Status**: Planning → early build (target: operational MVP within 1 week)
**Users**: 1 (solo operator on this local machine)
**Target throughput**: ~20 videos/day

**Tech Stack** (proposed / inferred):
- **Runtime**: Local on operator's macOS machine (local-first, self-hosted)
- **Languages**: Python (pipeline/orchestration + data), TypeScript/Node (tooling/CLIs already present)
- **Content generation**: Higgsfield CLI (personas, images, video, Marketing Studio, Virality Predictor)
- **Research/ingestion**: Firecrawl (broad web research), Aside browser (logged-in/human-web surfaces), TikTok Creative Center (first-party trend/product data)
- **Memory/knowledge**: agentmemory (reference + coding-side); marketing-domain memory engine TBD via bake-off (Mem0 / Zep-Graphiti / Cognee)
- **Source-of-truth store**: Local Postgres + local object storage (own the raw event stream; treat memory engines as swappable indexes)
- **Orchestration**: Local scripts/agents; scheduler for the daily content loop

## Problem and Outcomes

**Problem Statement**: Producing consistent, high-performing affiliate content by hand does not scale — a solo operator cannot manually research products, script, film, edit, benchmark, and publish enough short-form video to compete with content "factories." Today there is no repeatable, measurable system that turns trend signals into validated, compliant, revenue-generating content.

**Target Personas / Scenarios**:
- Primary: The solo operator running the pipeline daily to produce and publish ~20 videos across a chosen niche.
- Secondary (audience of the content): short-form social commerce viewers in the starting niche (e.g., beauty/wellness) who buy through affiliate links.

**Success Metrics (KPIs)**:
- **Throughput**: ~20 publishable videos/day generated locally.
- **Operational**: End-to-end pipeline (research → generate → benchmark → compliance gate → publish/test) running within 1 week.
- **Quality/validation**: ≥X% of generated videos clear the Virality Predictor pre-publish threshold (threshold to be calibrated) and match benchmark structure of top niche creators.
- **Compliance**: 100% of published videos pass the affiliate-disclosure + claim-safety gate before publishing.
- **Business (leading)**: measurable affiliate clicks/conversions per niche; a niche is "proven" when it clears a defined ROI/hit-rate bar, at which point the system is cloned to the next niche.
- **Economics gate**: content production must show positive return on Higgsfield credits, LLM/token spend, tool subscriptions, and operator time before scaling. Track cost per generated video, cost per publishable video, cost per validated/winning video, gross affiliate revenue, contribution margin, and MMR/MRR (working definition: monetized monthly revenue until formal accounting is chosen).
- **Frameworkization gate**: do not graduate this into an AIWG framework until the local MVP has repeatable economics, a proven niche loop, and reusable rules/skills/workflows worth formalizing.

## Current Scope and Features

**Core Features (in-scope for MVP, week 1)**:
- Niche selection + product shortlisting from trend/intelligence sources (Creative Center first, one third-party research tool).
- Benchmark "gold set" builder: pull + tag top niche videos/products for comparison.
- AI persona creation (Higgsfield) — a small set of reusable, non-impersonating personas.
- Script generation conditioned on winning hooks + compliance rules.
- Video generation via Higgsfield (Marketing Studio / Seedance) at volume.
- Pre-publish validation: Higgsfield Virality Predictor scoring + benchmark comparison.
- Compliance gate: affiliate disclosure insertion + medical/claim-safety check (human-approved).
- Publish/test path for the starting niche + result capture.
- Local marketing-domain memory capturing what worked/failed and why.

**Out-of-Scope (for now)**:
- Owned e-commerce store / private label (explicitly a future phase).
- Multi-operator/team features, multi-tenant, or cloud SaaS.
- Fully hands-off auto-publishing without human compliance approval.
- Simultaneous multi-niche scaling (start with ONE niche).
- Paid ad-spend management (organic/affiliate content first).

**Future Considerations (post-MVP)**:
- Clone the proven pipeline across additional niches ("wrap and repeat").
- Repurpose pipeline for an owned e-commerce store.
- Broader platform coverage beyond TikTok (Instagram, YouTube Shorts).
- Autonomous operator agent (Letta/MemGPT-style) once guardrails are proven.
- Graduate into an AIWG framework inside the AIWG fork, carrying its own rules, skills, workflows, behaviors, and specialist/daemon-like agents once the pipeline proves sustained return on credits/tokens and monetized monthly revenue.

## Architecture (Proposed)

**Architecture Style**: Local modular monolith / pipeline of stages, single operator, no distributed infra. Stages are swappable adapters (research source, memory engine, generation model, publish target) so any component can be replaced without a rewrite. Raw event store (Postgres + object storage) is the durable source of truth; memory engines index over it.

**Pipeline stages**:
1. Discover (trend/product signals) → 2. Select niche/product → 3. Build benchmark gold set → 4. Persona select → 5. Script → 6. Generate video → 7. Validate (Virality Predictor + benchmark) → 8. Compliance gate (human) → 9. Publish/test → 10. Capture results → 11. Learn (memory) → loop.

## Constraints

- **Local-only**: Runs on the operator's machine; no cloud dependency for core loop (external SaaS APIs excepted).
- **Timeline**: Operational MVP within 1 week.
- **Solo**: One person owns all roles; automation must minimize manual toil to hit 20 videos/day.
- **Delivery**: Solo, direct commit to `main` (no PR required).
- **Third-party fragility**: Market-intelligence tools are scraped/unofficial; must degrade gracefully (Aside fallback; ask operator to log in when needed).
- **Compliance is a hard gate**: FTC affiliate disclosure + TikTok medical/claim rules + AI-persona honesty are non-negotiable before publish.

## Compliance & Legal (starting posture)

- **FTC**: Clear, conspicuous affiliate disclosure on every published video (text + on-screen + spoken as appropriate). AI/virtual personas are held to the same disclosure standard as human creators.
- **TikTok Shop**: No medical/wellness/weight-management/GLP-1 claims; OTC claims must match labels; general-wellness framing only.
- **Persona ethics**: No impersonation of real people; no false firsthand experience claims; disclose AI where required/appropriate.

## Delivery Policy

- **Mode**: `direct` (solo commit to `main`)
- **Default branch**: `main`
- **CI green required**: no
- **Force-push**: never
- Persisted in `.aiwg/aiwg.config` under `delivery`.

## Next Steps

1. Review `solution-profile.md` and `option-matrix.md` (generated alongside this form).
2. Draft the marketing-domain memory schema + capture-hook triggers.
3. Run the memory-engine bake-off (Mem0 / Zep-Graphiti / Cognee) on sample data.
4. Choose the week-1 beachhead niche via the niche-diagnostic scorecard.
5. Stand up the local event store + first pipeline stages.
6. Define the economics dashboard and scale/frameworkization gates: credit spend, token spend, tool spend, operator time, affiliate revenue, margin, MMR/MRR, and per-video ROI.

## Controlled Construction Addendum — 2026-07-05

The original intake captured the broad affiliate content pipeline concept before the beachhead narrowed. Current Aflack construction state is:

- Beachhead: GTA6-adjacent gaming content, YouTube-first.
- Active lanes: Vice Signal and Loadout Lab.
- Current phase: Controlled Construction through the draft-ramp boundary, not Transition or Production.
- Current approval bounds: measured Higgsfield generation for validated packages and first-100 Postiz draft submissions with explicit targets.
- Current hard blocks: public publishing, account/channel settings, comments/DM/follows, paid promotion/ad spend, and broader daemon autonomy.
- Current proof target: move from locally constructed loop to IOC readiness by adding Cockpit visibility, render-review learning, analytics refresh, publish-quality policy, and stronger traceability.

This addendum supersedes early beauty/TikTok examples as the active MVP scope while preserving the original intake history.
