# Security Controls Validation

**Date**: 2026-07-04
**Scope**: Local MVP infrastructure and posting pipeline

## Controls

| Control | Status | Evidence / Notes |
|---|---|---|
| Secrets excluded from git | PASS | `.env` ignored; `.aiwg/working/` ignored; Postiz JWT compose not committed |
| Postiz separate service / AGPL boundary | PASS | ADR-0001; Postiz stack in `.aiwg/working/postiz`, not vendored |
| Event store localhost-only | PASS | pgGraph DB bound to `127.0.0.1:55432` |
| Compliance gate blocks high-risk footage | PASS | `aflack compliance-smoke` blocks same-seed official footage + missing disclosure |
| Economics/cost tracking | PASS | `cost_ledger` + `aflack economics-status` |
| Postiz UI reachable | PARTIAL | UI stack exists, but current Docker port state not secure |
| Postiz localhost-only | FAIL | Current host lsof shows `*:4007` |
| Temporal localhost-only | FAIL | Current host lsof shows `*:7233` |
| Postiz registration disabled after admin | NOT TESTED | Human must create admin first, then disable |
| YouTube OAuth connected | NOT TESTED | Human OAuth gate |
| Postiz API key generated | NOT TESTED | Human/account-owner gate |

## Immediate required remediation

The compose file has been patched to use localhost-only bindings, but Docker could not apply it because `spotlight` is a zombie container. The operator must restart Docker Desktop, then re-run the Postiz stack from the patched compose.

## Verification command after remediation

```bash
for p in 4007 7233 8080 8969; do
  echo --$p
  lsof -nP -iTCP:$p -sTCP:LISTEN
done
```

Expected: `127.0.0.1:4007`, `127.0.0.1:7233` if Temporal is published, `127.0.0.1:8080` if UI is published, no `*:<port>`.
