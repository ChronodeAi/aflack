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
| I2-003 | Loadout Lab script + affiliate angle | Should | Gear/checklist angle with no false claims and clear affiliate disclosure. | Pending |
| I2-004 | Compliance preflight record | Must | `aflack compliance-smoke` pattern applied to each script/package. | Complete |
| I2-005 | Higgsfield generation approval gate | Human-gated | Operator approves cost cap and prompt before spend. | Pending |
| I2-006 | Virality/benchmark validation | Should | Score or qualitative benchmark comparison captured before publish. | Complete |
| I2-007 | Postiz draft scheduling | Human-gated | Draft only; public publish requires separate approval. | Pending |

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


## Claude Code builder update — 2026-07-04

Completed before generation:

- Created Claude Code video builder runbook: `.aiwg/planning/claude-code-video-builder-runbook.md`.
- Created Claude Code prompt: `.aiwg/prompts/claude-code/vice-signal-ep001-builder.md`.
- Ran Claude Code as the video director to produce: `.aiwg/marketing/vice-signal/episode-001-claude-code-package.md`.
- Stopped before Higgsfield generation, Postiz submission, and public publishing.
- Created run report: `.aiwg/reports/claude-code-video-builder-run-2026-07-04.md`.

Next gate: operator approval/revision of the pre-generation package and explicit Higgsfield credit cap.

## Episode 002 builder update - 2026-07-04

Completed before generation:

- Imported the AI-video automation monetization scan from the Aside/Fugu artifact into `.aiwg/working/aside-scans/live-ai-video-automation-money-2026-07-04.json`.
- Distilled active benchmark insights for tool referrals, free workflow education, prompt packs, and paid community/software funnels.
- Applied the resulting guidance into `.aiwg/creator-commerce-ops/skills/hook-authoring.md`, `.aiwg/creator-commerce-ops/skills/claude-video-builder.md`, and `.aiwg/creator-commerce-ops/rules/compliance-before-publish.md`.
- Produced `.aiwg/marketing/vice-signal/episode-002-claude-code-package.md`.
- Created `.aiwg/research/sources/gta6-official-reference-package-2026-07-04.md` using official URLs as metadata only.
- Ran deterministic compliance preflight against Episode 002 script/disclosure: `passed=True`, `blocks=[]`, `warnings=[]`.
- Stopped before Higgsfield generation, Postiz submission, and public publishing.

Next gate remains unchanged: operator approval/revision of a pre-generation
package and explicit Higgsfield credit cap.
