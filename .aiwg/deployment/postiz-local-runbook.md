# Postiz Local Runbook

**Created**: 2026-07-04
**Location**: `.aiwg/working/postiz/docker-compose.yaml` (gitignored — contains generated JWT secret)
**UI**: http://localhost:4007  (redirects to /auth)
**Temporal UI**: http://localhost:8080

## Security binding requirement

All published ports must be bound to `127.0.0.1`, not `0.0.0.0` / `*`.

The local compose in `.aiwg/working/postiz/docker-compose.yaml` has been patched to use localhost-only bindings. This file is gitignored because it contains the generated JWT secret.

## Lifecycle

```bash
cd .aiwg/working/postiz
docker compose up -d       # start
docker compose ps          # status
docker compose logs -f postiz   # logs
docker compose down        # stop (keeps volumes)
```

## Known local issue: zombie Spotlight container

During hardening, Docker reported:

```text
cannot stop container ... spotlight ... PID ... is zombie and can not be killed
```

Because of that, Docker could not recreate the stack with the patched localhost-only port bindings. Do **not** force-kill arbitrary raw PIDs. Recovery is an operator action:

1. Restart Docker Desktop from the macOS menu bar.
2. Return to this project directory.
3. Run:

```bash
cd .aiwg/working/postiz
docker compose up -d
```

4. Verify:

```bash
for p in 4007 7233 8080 8969; do
  echo --$p
  lsof -nP -iTCP:$p -sTCP:LISTEN
done
```

Expected: localhost-only listeners (`127.0.0.1:<port>`) and no `*:<port>` exposure.

## First-run setup (HUMAN GATE)

1. Open http://localhost:4007 → you are redirected to /auth.
2. Register the first (admin) account. Registration is currently enabled
   (`DISABLE_REGISTRATION=false`). After creating your account, consider setting
   it to `true` and recreating the container to lock signups.
3. In the Postiz UI, connect channels (YouTube first). This requires platform
   OAuth apps / client credentials set in the compose `environment` block
   (e.g. `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, `TIKTOK_CLIENT_ID`, ...).
4. Generate a Postiz Public API key from the UI settings for programmatic use
   by our `PostizPublisher`.

## Why these are human gates

- Account creation establishes ownership/credentials.
- Channel OAuth requires logging into real social accounts and creating
  developer apps — must be done by the operator.
- API key issuance is an account-owner action.

## Notes

- Stack: postiz + postiz-postgres + postiz-redis + temporal (+ es/ui) + spotlight.
- Postiz has its OWN Postgres; do not point it at our pgGraph event store.
- AGPL: run as separate service; integrate over API only.
- Avatars/media storage: local by default; Cloudflare R2 optional.
