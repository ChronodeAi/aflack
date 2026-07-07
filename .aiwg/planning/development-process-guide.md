# Development Process Guide — Aflack MVP Construction

**Date**: 2026-07-04  
**Mode**: solo operator, direct commit to `main`  
**Phase**: Construction handoff after Elaboration baseline

## Operating principles

1. Ship the smallest measurable loop before scaling volume.
2. Human approval remains mandatory for public publishing, paid generation spend, channel/account changes, and DM/comment automation.
3. Compliance gates run before generation and before publish.
4. Every cost and result should land in the event store.
5. Official GTA6/Rockstar trailers are reference/provenance only; generated content must be original and non-impersonating.
6. Prefer Postiz cloud for scheduling/publishing; keep local Postiz isolated or stopped.
7. Follow ADR-0005 for Jarvis-style orchestration and ADR-0006 for virality-first, persona-optional lane selection.

## Iteration cadence

- Iteration length: 2-3 days for the week-1 MVP sprint.
- Daily loop:
  1. Pick one work item from the iteration plan.
  2. Write or update the smallest safety/test artifact first.
  3. Implement.
  4. Run smoke commands.
  5. Update `.aiwg/` status artifacts.
  6. Stop at human gates instead of bypassing approval.

## Definition of Ready

A work item is ready when it has:

- clear acceptance criteria,
- affected files/components identified,
- compliance implications understood,
- no unresolved secret/account dependency, or the dependency is explicitly marked as a human gate.

## Definition of Done

A work item is done when:

- code/docs are updated,
- smoke commands pass,
- security/compliance implications are recorded,
- no secrets are committed,
- public actions remain gated unless explicitly approved.

## Standard local verification

```bash
source .venv/bin/activate
python3 -m compileall -q src
aflack db-status
aflack compliance-smoke
aflack economics-status
aflack postiz-integrations
```

## Human-gated commands / actions

Do not run these without explicit confirmation for the specific item:

- paid Higgsfield generation,
- public YouTube/TikTok/Instagram publishing,
- comment/DM automation,
- follow/unfollow automation,
- paid promotion or ad spend,
- OAuth app or channel setting changes,
- deleting or force-stopping unknown processes.

Draft creation in Postiz is allowed only when the queue item and integration target are clear; public publish is still blocked until approved.
