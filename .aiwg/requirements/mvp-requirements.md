# MVP Requirements — Affiliate Content Pipeline

**Created**: 2026-07-04
**Status**: Elaboration baseline with Controlled Construction updates

## Functional requirements

| ID | Requirement | Status |
|---|---|---|
| FR-001 | Store all core pipeline entities in the local event store. | Implemented v1 schema |
| FR-002 | Track costs for Higgsfield, tokens, tools, operator time. | Implemented v1 `cost_ledger` |
| FR-003 | Maintain episodic/semantic/procedural lessons. | Implemented thin `MemoryStore` |
| FR-004 | Lock Beachhead A: GTA6 AI-persona gaming, YouTube-first. | Implemented |
| FR-005 | Maintain two active public personas (Vice Signal, Loadout Lab). | Implemented/recorded |
| FR-006 | Preserve official GTA6 trailer provenance as references only. | Implemented |
| FR-007 | Block use of Rockstar pre-release footage / same-seed remixes. | Implemented and directly tested |
| FR-008 | Queue compliance-approved creatives for Postiz scheduling. | Implemented stub + DB |
| FR-009 | Run the video director via Claude Code CLI `claude-fable-5`. | ADR accepted; command ready |
| FR-010 | Generate original visuals via Higgsfield, not Rockstar footage. | Implemented as measured, human-gated batch path for validated packages |
| FR-011 | Score generated videos before publishing. | Reframed: prompt-quality + human render review + analytics learning before public publish; Virality Predictor remains optional adapter |
| FR-012 | Publish via Postiz after compliance approval. | Private/draft Postiz submission implemented; public publish blocked |
| FR-013 | Capture post-publish metrics into results table. | Implemented as `analytics_snapshots`; waiting on real public metrics |
| FR-014 | Maintain lead magnets + one-word funnel keywords. | Implemented v1 schema |
| FR-015 | Use YouTube-native funnel delivery (pinned comment + description) before IG/DM automation. | Accepted |
| FR-016 | Maintain Jarvis/content-factory data products: hook library, source/reference library, asset library, funnel map, performance log, cost ledger, compliance record, and memory lessons. | Partially implemented; extend during Construction |
| FR-017 | Run the content-agent loop as human-gated orchestration, not autonomous publishing. | Accepted |
| FR-018 | Allow persona-free formats when trend fit and benchmark evidence beat persona continuity. | Accepted |
| FR-019 | Keep all comment, DM, follow, paid promotion, account-setting, and public-publish actions behind explicit human approval. | Accepted |
| FR-020 | Expose machine-readable local status for Cockpit/control-plane inspection. | Implemented for daemon, analytics, publish queue, compliance smoke, and prompt quality |
| FR-021 | Block safe-but-boring paid generation prompts before spend. | Implemented and tested |

## Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR-001 | Local-first | Core loop runs on operator's machine |
| NFR-002 | Throughput | Toward 20 videos/day after MVP loop works |
| NFR-003 | Compliance | 100% pre-publish gate pass required |
| NFR-004 | Cost visibility | Every spend event written to `cost_ledger` |
| NFR-005 | Memory anti-rot | Dedup + validity windows + retrieve-then-inject |
| NFR-006 | Source-of-truth ownership | Raw events in our DB; engines are indexes |
| NFR-007 | Lean role scope | One director + operator + two active personas |
| NFR-008 | Platform safety | Postiz handles posting; human approval before public publish |
| NFR-009 | Portability | Audience, lead magnets, source logs, and performance data must survive tool/account/provider changes |
| NFR-010 | Virality-first learning | Lane choices are measured by shares, retention, speed-to-trend, CTA response, and contribution margin |

## User stories

- US-001: As the operator, I can run a local DB migration and know the schema is ready.
- US-002: As the operator, I can queue a creative for Postiz without public publishing.
- US-003: As the director, I can read official GTA6 references and produce original script/shot direction.
- US-004: As the compliance gate, I can reject footage derived from Rockstar pre-release material.
- US-005: As the memory system, I can store a lesson and later retrieve only relevant context.
- US-006: As the operator, I can see whether the system is profitable per video/platform.
- US-007: As the operator, I can map a one-word CTA keyword to a lead magnet without relying on Instagram DM automation.
- US-008: As the director, I can run a lean weekly/daily routine without spawning a large agent org chart.
- US-009: As the operator, I can run a Jarvis-style loop that prepares drafts and recommendations while stopping before spend, publish, DM/comment, follow, or account actions.
- US-010: As the director, I can choose persona-free content when benchmark evidence says it should outperform a persona-led format.
- US-011: As the memory system, I can preserve transcript-derived lessons as ADRs, requirements, backlog items, or explicit non-actions.
- US-012: As the operator, I can inspect Aflack control-plane state as JSON so Cockpit or another console can observe the loop.
- US-013: As the creative director, I can reject compliant but weak asset prompts before paying for generation.
- US-014: As the operator, I can review private drafts and convert review outcomes into a learned publish-quality policy before public automation.

## Controlled Construction addendum — 2026-07-05

Optimization decisions made during Elaboration/Construction:

- Beachhead narrowed from generic affiliate/beauty assumptions to GTA6-adjacent YouTube-first content with Vice Signal and Loadout Lab lanes.
- Postiz submissions are approved only as drafts for the first-100 ramp; public publishing remains blocked.
- Higgsfield spend is approved only as measured generation batches for validated packages with cost capture.
- Analytics source of truth moved from the original `results` table idea to normalized `analytics_snapshots` so Postiz, platform exports, manual entries, and future Aside captures can converge.
- Virality validation is not a single predictor dependency; the current contract combines prompt-quality, compliance, render review, analytics/economics, and learned draft policy.
- Cockpit is the operator console layer; Aflack’s Postgres/domain services remain source of truth.

## Acceptance criteria for Elaboration complete

- [x] Intake complete.
- [x] Architecture decisions recorded as ADRs.
- [x] SAD baseline written.
- [x] Requirements/NFRs written.
- [x] Risk register written.
- [x] Test strategy written.
- [x] Local DB substrate validated.
- [x] Postiz cloud API reachable.
- [x] YouTube/TikTok connected in cloud Postiz.
- [x] Human generated cloud Postiz API key and stored it in `.env`.
- [x] Transcript-derived lessons mined and routed into SDLC artifacts.
- [x] Jarvis/content-agent orchestration ADR accepted.
- [x] Virality-first/persona-optional ADR accepted.
