# Independent Verification — Creator Commerce Ops Framework

**Date**: 2026-07-04  
**SDLC phase**: Construction  
**Iteration**: Continuous-improvement / Damon SDLC framework buildout

## Re-derived requirements

The operator asked for more than one-off video generation. The required system is a reusable content-creation framework that:

1. Uses Claude Code as the video builder/director for pre-generation packages.
2. Uses Aside Browser against logged-in Instagram/TikTok/YouTube surfaces for read-only creator research.
3. Verifies creator success using real proof, not vanity metrics or wealth flexing.
4. Captures observations, inputs, outputs, decisions, and traces continuously.
5. Distills repeatable insights into skills, rules, workflows, and agents.
6. Runs on a background daemon/cron cadence without manual prompting.
7. Learns from past attempts through local Postgres, agentmemory, and semantic memory.
8. Prevents unsafe autonomy: no paid generation, no public publishing, no account changes, no DM/comment automation without explicit approval.

## Gap review of the candidate solution

The candidate solution correctly implemented the DB learning layer, event tracing, daemon cycle, and insight/proposal dedup. Two important gaps remained:

1. **Aside ingestion was only conceptual.** There was no concrete JSON contract or importer connecting Aside research to `benchmark_creators` / `benchmark_videos`.
2. **Framework components were not codified.** The loop produced proposals, but the project-local rules/skills/workflows/agents surface did not yet exist.

## Missing components implemented

### Aside scan ingestion adapter

Added:

- `src/aflack/aside_scan.py`
- CLI: `aflack aside-scan-import <scan.json>`
- Tests: `tests/test_aside_scan.py`
- JSON schema: `.aiwg/creator-commerce-ops/templates/aside-scan.schema.json`
- Aside scan prompt: `.aiwg/creator-commerce-ops/templates/aside-scan-prompt.md`

The importer:

- parses social shorthand metrics (`1.2M`, `45k`, etc.),
- computes engagement rate,
- upserts benchmark creators,
- assigns proof-of-real-success credibility,
- ingests benchmark videos,
- dedups repeated video observations,
- records a trace for the import.

### Project-local framework surface

Added `.aiwg/creator-commerce-ops/` with:

- manifest,
- 5 rules,
- 5 skills,
- 4 workflows,
- 5 agents,
- 1 daemon behavior,
- schema/prompt templates,
- 50% framework status report.

### Proposal dedup hardening

The daemon originally re-created identical open proposals on repeated cycles. Fixed by:

- reusing identical open proposals in `propose_improvement`,
- adding `dedupe_open_proposals`,
- adding CLI `aflack proposals-dedupe`,
- cleaning the current DB down to one open hook-authoring proposal.

## Verification results

Commands run:

```bash
source .venv/bin/activate
python3 -m compileall -q src
python3 -m unittest discover -s tests -v
aflack aside-scan-import .aiwg/working/aside-scans/sample-scan.json
aflack improve-cycle
aflack proposals-dedupe
aflack db-status
aflack postiz-integrations
```

Results:

- 13/13 tests pass.
- Aside scan duplicate import is detected (`videos_duplicate=1`) and does not create another row.
- Insight dedup is clean (`insights == distinct content_hash`).
- Open hook-authoring proposal duplicate count is 1.
- Re-running `aflack improve-cycle` keeps open proposals stable (`before=1`, `after=1`).
- DB tables include the learning layer: `benchmark_creators`, `benchmark_videos`, `insights`, `improvement_proposals`, `pipeline_events`, `daemon_runs`.
- Postiz Cloud integrations still work: YouTube and TikTok are visible.

## Current SDLC status

Construction is active. The project has crossed from "building videos with Claude Code" into a project-local framework stage:

- Video builder: available.
- Learning daemon: available.
- Aside ingestion contract: available.
- Framework rules/skills/workflows/agents: available locally.
- Real live Aside scan execution: next step.
- Real analytics ingest and ROI sentinel automation: still pending.

## Remaining to reach 100%

1. Execute live Aside Browser scans against logged-in Instagram/TikTok.
2. Implement platform analytics/results import after publishing.
3. Add ROI Sentinel automation that blocks scale-up when margins are poor.
4. Add human-approved proposal-to-file application workflow.
5. Promote the project-local framework to the AIWG fork only after economics prove repeatability.
