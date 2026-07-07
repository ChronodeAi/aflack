# Team Onboarding Guide

**Date**: 2026-07-04  
**Phase**: Controlled Construction  
**Mode**: Solo operator now; future collaborators use this as the starter map

## First Hour

1. Read @.aiwg/reports/status-assessment.md.
2. Read @.aiwg/gates/pre-construction-gate-2026-07-04.md.
3. Read @.aiwg/planning/development-process-guide.md.
4. Read @.aiwg/planning/iteration-plan-002.md.
5. Confirm the human gates before touching generation, publishing, account actions, comments, DMs, follows, or ad spend.

## Project Map

| Area | Start here |
|---|---|
| Requirements | @.aiwg/requirements/mvp-requirements.md |
| Architecture | @.aiwg/architecture/software-architecture-document.md |
| Decisions | @.aiwg/architecture/adr-0005-human-gated-jarvis-content-agent-orchestration.md |
| Current iteration | @.aiwg/planning/iteration-plan-002.md |
| Daemon runtime | @.aiwg/planning/daemon-runtime-architecture.md |
| Testing | @.aiwg/testing/test-strategy.md |
| Compliance | @.aiwg/creator-commerce-ops/rules/compliance-before-publish.md |
| Deterministic agent rules | @.aiwg/creator-commerce-ops/rules/testable-contracts-over-prose.md |

## Local Verification

Run these before claiming a construction slice is complete:

```bash
.venv/bin/python -m compileall -q src
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/aflack compliance-smoke
.venv/bin/aflack proposals-list
aiwg index build
```

## Human Gates

Do not perform these actions without explicit approval for the specific item:

- paid Higgsfield generation,
- public publishing,
- channel/account setting changes,
- comments, DMs, follows, or unfollows,
- ad spend or paid promotion,
- deleting or force-stopping unknown services,
- expanding autonomous daemon actions.

## First Starter Tasks

1. Finish the Loadout Lab affiliate package with disclosure and no guaranteed-results claims.
2. Add direct compliance unit tests.
3. Add `aflack daemon-status`.
4. Add daemon/status tests.
5. Add the PSI-style `.aiwg/loops/content-factory/` control-plane files.

