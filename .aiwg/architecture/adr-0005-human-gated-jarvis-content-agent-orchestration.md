# ADR-0005: Human-gated Jarvis content-agent orchestration

**Status**: Accepted  
**Date**: 2026-07-04  
**Decision owner**: Solo operator

## Context

The Codex, Aside/Fugu, and Claude Code sessions repeatedly converged on the same operating model: a Jarvis-style content factory that can research trends, synthesize hooks, generate original assets, prepare posts, and learn from results. The useful parts of that model are not full autonomy; they are repeatable orchestration, persistent memory, and disciplined gates around spending, publishing, account actions, and claims.

The current MVP already has the substrate for this: a local event store, benchmark ingestion, memory lessons, Postiz publishing integration, compliance checks, Claude Code video-builder packages, and a project-local creator-commerce-ops bundle.

## Decision

Implement the content factory as a **human-gated director-and-agent pipeline**, not as an autonomous posting bot.

The pipeline roles are:

- **Director / Jarvis**: coordinates the daily loop, reads current memory, chooses the next production action, and records decisions.
- **Trend Scout**: finds trend, platform, and benchmark signals.
- **Source / Reference Agent**: records provenance and separates fact references from reusable media.
- **Hook Author**: produces hook batches from benchmark patterns and active memory.
- **Creative Producer**: prepares Higgsfield prompts, asset plans, and generation batches.
- **Editor / Packager**: assembles scripts, captions, storyboards, disclosures, CTAs, and Postiz payload previews.
- **Compliance Reviewer**: blocks risky footage, false claims, unsafe likeness use, missing disclosures, and platform-policy violations.
- **Publisher**: submits approved draft payloads to Postiz only after the relevant gate passes.
- **Analytics / Memory Curator**: ingests results, economics, and lessons into the event store and improvement loop.

The roles may be implemented as CLI commands, skills, agents, daemons, or manual runbooks over time, but the source of truth remains the local event store from ADR-0002.

## Hard gates

The following actions require explicit human approval:

- public publishing,
- Postiz draft submission when content/account/channel ambiguity exists,
- Higgsfield or other paid generation spend,
- comment, DM, follow, account-setting, or channel-setting actions,
- any paid promotion or ad spend,
- Tier 3 real-event media ingestion override,
- any claim that implies personal earnings, guaranteed results, medical outcomes, financial outcomes, or false firsthand experience.

## Data products

The orchestration loop must maintain:

- hook library,
- source/reference library,
- generated asset library,
- funnel map and lead magnets,
- performance log,
- cost ledger,
- compliance/provenance record,
- memory lessons with validity and disposition.

## Consequences

### Positive

- Gives the operator a practical Jarvis-style system without risking unsupervised channel actions.
- Converts transcript ideas into buildable roles and artifacts.
- Keeps frameworkization possible once repeatable economics are proven.
- Preserves portability if Higgsfield, Postiz, or a platform account becomes unavailable.

### Negative / risks

- More orchestration surface area than a single manual workflow.
- Requires disciplined logging or memory will rot.
- Some roles remain manual until enough data proves they should be automated.

## Implementation notes

- MVP Construction should implement the roles as thin commands/runbooks first.
- Daemons are deferred until the manual loop proves repeatable contribution margin.
- All agent outputs should write durable artifacts or database rows, not only chat transcript context.

## Related

- ADR-0001 Postiz scheduler
- ADR-0002 Own event store
- ADR-0003 Local Postgres + pgGraph + pgvector memory
- ADR-0006 Virality-first lane selection and persona-optional form
- `.aiwg/planning/frameworkization-roadmap.md`
- `.aiwg/marketing/viral-factory-spec.md`
- `.aiwg/reports/transcript-mining-synthesis-2026-07-04.md`
