# Affiliate Content Pipeline — Research Brief

**Created**: 2026-07-03
**Purpose**: Research-first planning brief for an automated content creation pipeline for affiliate marketing, beginning with narrow niche diagnostics and repeatable AI persona/video workflows.

## Working thesis

Build a repeatable affiliate/content engine that can:

1. Discover product/niche opportunities from social commerce signals.
2. Select a narrow beachhead niche.
3. Generate lifelike AI personas and short-form UGC-style content using Higgsfield.
4. Publish/test variants across affiliate channels.
5. Measure creative/product performance.
6. Convert the proven system into an owned e-commerce content engine later.

## User preferences captured

- Do not reinvent the wheel; research successful existing creator/content-factory patterns continuously.
- Use Firecrawl for broad web research and source gathering.
- Use Aside for logged-in/human-web browsing when sites require accounts or interactive access.
- If a needed website is not logged in within Aside, ask the user to sign in through Aside.
- Build website-specific Aside skills/workflows on the fly when important sources do not have existing skills.
- Start niche-diagnostic: perfect the system in one or a few narrow niches, then package and repeat it for other niches.

## Initial beachhead hypothesis

Candidate beachhead: TikTok Shop/social commerce, with beauty + wellness as a starting surface, but not permanently limited to TikTok or TikTok products.

Reasoning to validate:

- TikTok Shop has native affiliate collaboration mechanics.
- Beauty/wellness is highly visual and suitable for UGC/persona-led content.
- Health/wellness introduces high compliance risk, so the pipeline needs claim-safety controls from day one.

## Research workstreams

### 1. Market and niche diagnostics

Questions:

- Which narrow product categories have high short-form content velocity, strong affiliate availability, and acceptable compliance risk?
- Which niches are oversaturated versus under-exploited?
- Which offers support repeat content angles without dangerous claims?

Candidate narrow niches to compare:

- Beauty tools and devices with visual demos.
- Skincare routine accessories and non-medical beauty products.
- Hair styling tools/accessories.
- Sleep/relaxation lifestyle products that avoid medical claims.
- Fitness accessories framed as lifestyle/comfort rather than body-transformation.

### 2. Creator/content-factory pattern research

Questions:

- What hooks, formats, posting cadence, persona archetypes, and product demo patterns appear in high-performing affiliate/UGC operations?
- Which content factories rely on volume, which rely on creator fit, and which rely on product selection?
- What can be reproduced with AI personas without impersonation or deceptive claims?

### 3. Platform and compliance research

Questions:

- What TikTok Shop affiliate features, eligibility rules, and creator/product qualification rules constrain the system?
- What FTC disclosure requirements apply to affiliate content and AI personas?
- What health/beauty claim restrictions must be built into the script and review pipeline?

### 4. Pipeline architecture research

Questions:

- What is the minimum viable pipeline: research → product shortlist → persona selection → script generation → Higgsfield creative generation → compliance check → publish/test → analytics loop?
- Which steps can be automated now and which require human approval?
- What data model should capture products, personas, scripts, variants, channels, disclosures, claims, results, and learnings?

## Immediate research sources to use

- Official TikTok Shop Affiliate and Seller Center policy pages.
- FTC endorsement/disclosure guidance.
- TikTok/Instagram/Amazon/Shopify/TikTok Shop logged-in surfaces through Aside when required.
- Public case studies, interviews, Reddit/operator forums, YouTube breakdowns, and marketplace trend tools.

## Early risk register

| Risk | Why it matters | Mitigation |
|---|---|---|
| Medical/weight-loss claim violations | Beauty/health content can easily cross into prohibited claims | Script claim classifier + compliance checklist + human gate before publishing |
| Affiliate disclosure failures | Affiliate relationships must be clear | Auto-insert visual/audio/text disclosures and verify before export |
| AI persona deception/impersonation | Synthetic creators can mislead if presented as real users with false experiences | Persona policy: no impersonation, no false firsthand claims unless controlled/true, disclose AI where required/appropriate |
| Platform access/eligibility | TikTok Shop affiliate features have eligibility rules | Research eligibility before depending on a workflow |
| Content volume without learning loop | Volume alone can waste spend/time | Require performance tags and post-test analysis before scaling |

## Next artifacts

- `.aiwg/intake/project-intake.md`
- `.aiwg/intake/solution-profile.md`
- `.aiwg/intake/option-matrix.md`
- `.aiwg/marketing/strategy/niche-diagnostic-plan.md`
- `.aiwg/marketing/compliance/affiliate-ai-content-guardrails.md`
