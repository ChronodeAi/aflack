# Incident Response Runbook

## Overview

This runbook covers incident response procedures for the aflack content pipeline.

## Incident Severity Levels

| Level | Description | Response Time |
|-------|-------------|---------------|
| P0 | Pipeline down, data loss, security breach | Immediate |
| P1 | Major feature broken, generation/publishing blocked | < 1 hour |
| P2 | Minor feature degraded, workarounds available | < 4 hours |
| P3 | Cosmetic issues, non-urgent improvements | Next business day |

## Response Steps

### 1. Triage
- Identify the alert source (error tracking, monitoring, user report)
- Classify severity using the table above
- Create an issue with the appropriate priority label (P0-P3)

### 2. Investigate
- Check `aflack daemon-status` for recent daemon runs and blocked actions
- Check `aflack trace-show <trace_id>` for full event traces
- Review error tracking output in `pipeline_events` table
- Check `aflack economics-status` for cost/revenue anomalies
- Check `aflack analytics-status` for traffic anomalies

### 3. Mitigate
- If generation is runaway: stop the daemon, check cost ledger
- If publishing is broken: pause all publish queue items
- If compliance gate is bypassed: block all submissions immediately
- If database is corrupted: restore from Docker volume backup

### 4. Resolve
- Apply fix following the development workflow (lint, typecheck, test)
- Verify fix with `aflack compliance-smoke` and relevant CLI commands
- Monitor for 30 minutes after resolution

### 5. Post-Mortem
- Document timeline, root cause, and resolution
- Create improvement proposals using `aflack insights-list` and `aflack proposals-list`
- Update this runbook if procedures need adjustment

## Key Commands

```bash
aflack daemon-status          # Check daemon health
aflack trace-show <trace_id>  # Replay event trace
aflack economics-status       # Check costs/revenue
aflack analytics-status       # Check traffic metrics
aflack compliance-smoke       # Verify compliance gates
aflack proposals-list         # Check open improvement proposals
```

## Escalation

- Security incidents: notify operator immediately, preserve evidence
- Cost overruns: check `cost_ledger` table, enforce daily caps from `.env`
- Data integrity: check pgGraph registration and migration status
