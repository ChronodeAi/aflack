# Iteration Plan 002 — First Content Package + Validation Loop

**Date**: 2026-07-04  
**Phase**: Construction  
**Goal**: Produce the first original GTA6-adjacent content package and validate it before any public publishing.

## Objectives

1. Create one Vice Signal Shorts package and one Loadout Lab affiliate package.
2. Keep visuals original and non-Rockstar-derived.
3. Add a validation record for hook, CTA, compliance, and expected economics.
4. Optionally run Higgsfield generation only after operator spend approval.
5. Queue approved package to Postiz draft.

## Work items

| ID | Item | Priority | Acceptance criteria | Status |
|---|---|---|---|---|
| I2-001 | Source/reference package | Must | Uses official trailer URLs as metadata only; no downloading/clipping. | Complete |
| I2-002 | Vice Signal script + shot list | Must | Hook, 30-45s script, prompt, CTA keyword, pinned comment, disclosure. | Complete |
| I2-003 | Loadout Lab script + affiliate angle | Should | Gear/checklist angle with no false claims and clear affiliate disclosure. | Complete |
| I2-004 | Compliance preflight record | Must | `aflack compliance-smoke` pattern applied to each script/package. | Complete |
| I2-005 | Higgsfield generation approval gate | Human-gated | Operator approves cost cap and prompt before spend. | Complete for EP001 |
| I2-006 | Virality/benchmark validation | Should | Score or qualitative benchmark comparison captured before publish. | Complete |
| I2-007 | Postiz draft scheduling | Human-gated | Draft only; public publish requires separate approval. | Complete for queue_id=2 |
| I2-008 | Daemon status visibility | Must | `aflack daemon-status` reports latest run, insights, proposals, events, and blocked actions with tests. | Complete |
| I2-009 | Direct deterministic coverage expansion | Must | Direct tests for compliance, memory consolidation, economics, and tracing pass. | Complete |
| I2-010 | Content-factory loop control plane | Must | `.aiwg/loops/content-factory/` contains loop, state, budget, constraints, and run log. | Complete |

## First draft content direction

- Persona: Vice Signal
- Format: YouTube Short
- Theme: “GTA6 hype is becoming an AI content factory — but here’s the safe way to do it.”
- CTA keyword: `JARVIS`
- Lead magnet: GTA6 AI Content Workflow
- Disclosure: “AI-assisted original visuals/commentary. No Rockstar footage used.”

## Exit criteria

Iteration 002 exits when at least one publish-ready package exists with:

- script,
- shot list/Higgsfield prompt,
- disclosure,
- compliance checklist,
- economics estimate,
- Postiz draft or explicit operator decision not to draft.

## SDLC elaboration addendum — 2026-07-04

Transcript mining across Codex, Aside/Fugu, and Claude Code is complete for the current handoff. The durable decisions were recorded in ADR-0005 and ADR-0006, the synthesis is preserved at `.aiwg/reports/transcript-mining-synthesis-2026-07-04.md`, and the framework deliverance handoff is preserved at `.aiwg/reports/framework-deliverance-handoff-2026-07-04.md`.

Construction may continue without reopening strategy: harden the Jarvis/director loop, keep Loadout Lab as the next optional package, refresh analytics after draft metrics exist, and stop at public publish/account/action/ad-spend gates.


## Claude Code builder update — 2026-07-04

Completed before generation:

- Created Claude Code video builder runbook: `.aiwg/planning/claude-code-video-builder-runbook.md`.
- Created Claude Code prompt: `.aiwg/prompts/claude-code/vice-signal-ep001-builder.md`.
- Ran Claude Code as the video director to produce: `.aiwg/marketing/vice-signal/episode-001-claude-code-package.md`.
- Stopped before Higgsfield generation, Postiz submission, and public publishing.
- Created run report: `.aiwg/reports/claude-code-video-builder-run-2026-07-04.md`.

Gate update: EP001 was later approved for one measured generation batch, generated, and submitted as a private Postiz draft. Public publishing remains blocked.

## Episode 002 builder update - 2026-07-04

Completed before generation:

- Imported the AI-video automation monetization scan from the Aside/Fugu artifact into `.aiwg/working/aside-scans/live-ai-video-automation-money-2026-07-04.json`.
- Distilled active benchmark insights for tool referrals, free workflow education, prompt packs, and paid community/software funnels.
- Applied the resulting guidance into `.aiwg/creator-commerce-ops/skills/hook-authoring.md`, `.aiwg/creator-commerce-ops/skills/claude-video-builder.md`, and `.aiwg/creator-commerce-ops/rules/compliance-before-publish.md`.
- Produced `.aiwg/marketing/vice-signal/episode-002-claude-code-package.md`.
- Created `.aiwg/research/sources/gta6-official-reference-package-2026-07-04.md` using official URLs as metadata only.
- Ran deterministic compliance preflight against Episode 002 script/disclosure: `passed=True`, `blocks=[]`, `warnings=[]`.
- Stopped before Higgsfield generation, Postiz submission, and public publishing.

Next gate: optional measured generation/draft ramp for Episode 002, or hold it as a package backlog item while EP001 final render/analytics are reviewed.

## Loadout Lab package update - 2026-07-04

Completed before generation:

- Produced `.aiwg/marketing/loadout-lab/episode-001-affiliate-package.md`.
- Used category-level setup audit guidance instead of unverified SKU/price recommendations.
- Included `LOADOUT` CTA, free GTA6 Day-One Loadout Checklist lead magnet, affiliate disclosure, AI disclosure, non-affiliation language, and no guaranteed-results claims.
- Stopped before Higgsfield generation, affiliate link publication, Postiz submission, and public publishing.

Next gate: operator approval/revision of the Loadout Lab package and explicit
Higgsfield credit cap if generation is desired.

## Daemon status update - 2026-07-04

Completed:

- Added `aflack daemon-status`.
- Added read-only daemon status helper in `src/aflack/daemon.py`.
- Added `tests/test_daemon.py`.
- Verified live status for `improvement-daemon`: latest run succeeded, 19 active insights, 0 open proposals, 98 recent events, and blocked actions preserved.

Next construction item: add direct compliance unit tests, then create the
PSI-style `.aiwg/loops/content-factory/` control-plane files before broader
daemon autonomy.

## Safe construction completion update - 2026-07-04

Completed:

- Added direct compliance unit tests.
- Added memory consolidation command and tests.
- Added economics rollup tests.
- Added trace event tests.
- Created `.aiwg/loops/content-factory/LOOP.md`, `state.yaml`, `budget.yaml`, `constraints.yaml`, and `run-log.jsonl`.
- Verified memory consolidation dedupe by rerunning `aflack memory-consolidate --min-confidence 0.95 --limit 5`: five scanned, zero new, five existing.

Remaining items are final public-publish gated or require real external outcomes:
final render review, public publish decision, post-draft/post-publish analytics,
and broader draft-ramp learning.

## Draft ramp and analytics update - 2026-07-04

Completed:

- EP001 measured generation batch recorded: 7 Seedance clips, 360 credits, zero rerolls.
- Postiz queue `2` is submitted as a private YouTube draft with Postiz post id `cmr6wm4p50eiwnt0ytbyx0pqx`.
- Cost ledger now records the 360-credit generation batch against `creative_id=1`.
- Postiz post analytics ingestion created `analytics_snapshot_id=1`; current metrics are zero.
- Postiz analytics ingestion commands and tests are implemented.
