# Security Gate — 2026-07-04

**Decision**: **FAIL / BLOCKED FOR PUBLIC POSTING**

## Reason

Postiz and Temporal are currently exposed on all host interfaces:

- `*:4007`
- `*:7233`

This violates the user requirement: do not expose Postiz to the greater internet unless explicitly required for posting content.

## Root cause

The official Postiz compose initially exposed ports on all interfaces. We patched the local ignored compose to bind ports to `127.0.0.1`, but Docker could not recreate the stack because the optional `spotlight` container became a zombie and cannot be stopped by Docker.

## Gate conditions to pass

- [ ] Operator restarts Docker Desktop (or otherwise clears the zombie container).
- [ ] Run patched Postiz compose.
- [ ] Verify `lsof` shows localhost-only bindings.
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
