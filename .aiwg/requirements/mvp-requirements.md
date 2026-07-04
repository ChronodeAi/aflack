# MVP Requirements — Affiliate Content Pipeline

**Created**: 2026-07-04
**Status**: Elaboration baseline

## Functional requirements

| ID | Requirement | Status |
|---|---|---|
| FR-001 | Store all core pipeline entities in the local event store. | Implemented v1 schema |
| FR-002 | Track costs for Higgsfield, tokens, tools, operator time. | Implemented v1 `cost_ledger` |
| FR-003 | Maintain episodic/semantic/procedural lessons. | Implemented thin `MemoryStore` |
| FR-004 | Lock Beachhead A: GTA6 AI-persona gaming, YouTube-first. | Implemented |
| FR-005 | Maintain two active public personas (Vice Signal, Loadout Lab). | Implemented/recorded |
| FR-006 | Preserve official GTA6 trailer provenance as references only. | Implemented |
| FR-007 | Block use of Rockstar pre-release footage / same-seed remixes. | Implemented policy; gate code pending |
| FR-008 | Queue compliance-approved creatives for Postiz scheduling. | Implemented stub + DB |
| FR-009 | Run the video director via Claude Code CLI `claude-fable-5`. | ADR accepted; command ready |
| FR-010 | Generate original visuals via Higgsfield, not Rockstar footage. | Pending generation wrapper |
| FR-011 | Score generated videos before publishing. | Pending Virality Predictor wrapper |
| FR-012 | Publish via Postiz after compliance approval. | Postiz UI up; API adapter pending |
| FR-013 | Capture post-publish metrics into results table. | Pending |

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

## User stories

- US-001: As the operator, I can run a local DB migration and know the schema is ready.
- US-002: As the operator, I can queue a creative for Postiz without public publishing.
- US-003: As the director, I can read official GTA6 references and produce original script/shot direction.
- US-004: As the compliance gate, I can reject footage derived from Rockstar pre-release material.
- US-005: As the memory system, I can store a lesson and later retrieve only relevant context.
- US-006: As the operator, I can see whether the system is profitable per video/platform.

## Acceptance criteria for Elaboration complete

- [x] Intake complete.
- [x] Architecture decisions recorded as ADRs.
- [x] SAD baseline written.
- [x] Requirements/NFRs written.
- [x] Risk register written.
- [x] Test strategy written.
- [x] Local DB substrate validated.
- [x] Postiz local UI reachable.
- [ ] Human creates Postiz admin + social OAuth connections (explicit human gate).
