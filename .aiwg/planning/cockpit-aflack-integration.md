# Cockpit / Aflack Integration Plan

**Date**: 2026-07-05  
**Phase**: Controlled Construction  
**Status**: local contribution manifest and Bridge API contract verified; real executor launch pending

## Decision

AIWG Cockpit is the operator console for Aflack. It observes and directs local sessions, status, actions, telemetry, and approvals. It does not replace Aflack's Postgres source of truth, daemon safety model, Postiz adapter, or AIWG CLI.

## Machine-Readable Status Surface

| Command | Purpose | Status |
|---|---|---|
| `aflack loop-status --json` | Content-factory loop phase, gates, validation, and safe next actions. | Implemented and CLI-tested |
| `aflack daemon-status --json` | Daemon run/backlog/blocked-action status. | Implemented and CLI-tested |
| `aflack analytics-status --json` | Aggregated local analytics snapshot status. | Implemented and CLI-tested |
| `aflack publish-queue-status --json` | Draft/public queue posture and external IDs. | Implemented and CLI-tested |
| `aflack draft-review-status --json` | First-100 draft review counts, verdicts, and score rollups. | Implemented and CLI-tested |
| `aflack compliance-smoke --json` | Deterministic compliance gate smoke result. | Implemented and CLI-tested |
| `aflack prompt-quality --json` | Prompt-quality gate result. | Implemented and CLI-tested |

## Suggested Cockpit Actions

| Action | Command | Safety |
|---|---|---|
| Check daemon | `aflack daemon-status --json` | Read-only |
| Check loop | `aflack loop-status --json` | Read-only |
| Check analytics | `aflack analytics-status --json` | Read-only |
| Check publish queue | `aflack publish-queue-status --json` | Read-only |
| Check draft reviews | `aflack draft-review-status --json` | Read-only |
| Run compliance smoke | `aflack compliance-smoke --json` | Local deterministic |
| Check prompt | `aflack prompt-quality --text "<prompt>" --json` | Local deterministic |
| Run improvement cycle | `aflack improve-cycle` | Proposal-only; no spend/publish |
| Consolidate memory | `aflack memory-consolidate --min-confidence 0.95 --limit 5` | Local dedupe/promotion |

## Approval Inbox Candidates

Cockpit approvals should be used for:

- measured Higgsfield generation batch,
- Postiz draft submission when package/target is ambiguous,
- public publish,
- account/channel setting change,
- comment/DM/follow/unfollow automation,
- paid promotion/ad spend,
- broader daemon autonomy,
- skill/rule/workflow edits proposed by daemons.

## Gate Rule

A green Cockpit action means local status or deterministic validation passed. It is not public-publish approval, spend approval, or Transition readiness.

## Contribution Manifest

The local contribution manifest is:

`@.aiwg/cockpit/contrib/aflack-control-plane.json`

Launch Cockpit with this project-local contribution directory:

```bash
AIWG_COCKPIT_CONTRIB=/Users/ace/aflack/.aiwg/cockpit/contrib aiwg cockpit
```

Cockpit actions inject commands into an attached agentic session. They do not run the Aflack CLI directly from the Bridge.

## Verification

Harness verification passed with the AIWG source mock executor and installed Cockpit Bridge:

```bash
PORT=8123 node /Users/ace/my-aiwg/apps/cockpit/mock-executor/src/server.mjs
AIWG_COCKPIT_CONTRIB=/Users/ace/aflack/.aiwg/cockpit/contrib \
  AIWG_COCKPIT_EXECUTOR_URL=http://127.0.0.1:8123 \
  AIWG_COCKPIT_ALLOW_MOCK_EXECUTOR=1 \
  AIWG_COCKPIT_AUTOSTART_EXECUTOR=0 \
  AIWG_COCKPIT_BRIDGE_PORT=8141 \
  node /Users/ace/.aiwg/cockpit/package/node_modules/@aiwg/cockpit/bridge/src/server.mjs
```

`/api/contributions` returned the `aflack-control-plane` source, seven Aflack actions, and the `aflack-construction-check` workflow.

For human/operator Cockpit use, a real `agentic-sandbox` executor is still required. Without an executor reachable at `AIWG_COCKPIT_EXECUTOR_URL`, Bridge attempts to autostart `agentic-mgmt`; that binary is not installed on this workstation.
