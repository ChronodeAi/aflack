# Security Gate — 2026-07-04

**Initial decision**: FAIL / BLOCKED (ports exposed on all interfaces).
**Updated decision (post Docker restart)**: **CONDITIONAL PASS** — network binding remediated; remaining items are human account/OAuth gates.

## Network exposure — RESOLVED

After the operator restarted Docker Desktop, the stack was recreated from the patched localhost-only compose. Verified bindings (host `lsof`):

- `127.0.0.1:4007` Postiz UI
- `127.0.0.1:7233` Temporal
- `127.0.0.1:8080` Temporal UI
- `127.0.0.1:8969` Spotlight
- `127.0.0.1:55432` pgGraph DB

No `*:<port>` / `0.0.0.0` exposure remains. Postiz backend healthy (API returns 401 auth-required, UI 307 to /auth).

## Root cause

The official Postiz compose initially exposed ports on all interfaces. We patched the local ignored compose to bind ports to `127.0.0.1`, but Docker could not recreate the stack because the optional `spotlight` container became a zombie and cannot be stopped by Docker.

## Gate conditions to pass

- [x] Operator restarts Docker Desktop (or otherwise clears the zombie container).
- [x] Run patched Postiz compose.
- [x] Verify `lsof` shows localhost-only bindings.
- [ ] Create Postiz admin account.
- [ ] Disable public registration after admin account is created.
- [ ] Connect YouTube and generate API key.
- [ ] Store API key outside git.

## Allowed while gate is failed

- Local code development.
- Research.
- Script generation without paid video creation.
- No public posting.
- No public tunnels.

## Not allowed while gate is failed

- Connecting real social accounts through an exposed Postiz instance.
- Public publishing.
- Sharing/forwarding the Postiz URL outside localhost.
