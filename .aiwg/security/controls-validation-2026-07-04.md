# Security Controls Validation

**Date**: 2026-07-04  
**Scope**: MVP infrastructure and posting pipeline after cloud Postiz pivot

## Controls

| Control | Status | Evidence / Notes |
|---|---|---|
| Secrets excluded from git | PASS | `.env` ignored; `.aiwg/working/` ignored; API key redacted from outputs |
| Postiz separate service / AGPL boundary | PASS | ADR-0001; integration via public API only |
| Cloud Postiz API key configured outside git | PASS | `.env` contains the active key; `.env.example` contains no secret |
| Cloud Postiz integrations reachable | PASS | `aflack postiz-integrations` returns YouTube and TikTok integrations |
| Event store localhost-only | PASS | pgGraph DB bound to `127.0.0.1:55432` |
| Local Postiz localhost-only if running | PASS | Host `lsof` shows Postiz/Temporal ports bound to `127.0.0.1` |
| Compliance gate blocks high-risk footage | PASS | `aflack compliance-smoke` blocks same-seed official footage + missing disclosure |
| Economics/cost tracking | PASS | `cost_ledger` + `aflack economics-status` |
| Public publishing blocked by process | PASS | `postiz-submit` defaults to draft; public publish requires operator approval |
| Paid generation blocked by process | PASS | Higgsfield spend remains human-gated |
| Postiz local registration disabled | N/A FOR ACTIVE PATH | Active publishing is cloud Postiz. If local Postiz remains running for testing, keep it localhost-only or stop it when not needed. |

## Current risk posture

**PASS for Construction Iteration 1** with these constraints:

- no public publish without explicit operator approval,
- no paid generation without explicit operator approval,
- no use of official Rockstar/GTA6 footage as source media,
- no exposure of local Postiz/DB to LAN or internet,
- no secrets printed or committed.

## Standard verification

```bash
source .venv/bin/activate
python3 -m compileall -q src
aflack db-status
aflack compliance-smoke
aflack economics-status
aflack postiz-integrations
```
