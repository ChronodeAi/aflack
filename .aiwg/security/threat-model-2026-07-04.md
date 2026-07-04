# Threat Model — Local Postiz + Content Pipeline

**Date**: 2026-07-04
**Scope**: Local Aflack pipeline, pgGraph DB, Postiz stack, Claude/Higgsfield/Aside/Firecrawl CLIs.
**Method**: STRIDE lightweight review.

## Assets

- YouTube/TikTok/Postiz credentials and OAuth tokens.
- Postiz admin account and API key.
- Local event store (Postgres + pgGraph + pgvector).
- Generated videos, scripts, personas, prompts, cost/revenue data.
- Agentmemory / project memory.
- Higgsfield account and credits.

## Trust boundaries

- Local machine ↔ Docker containers.
- Pipeline ↔ Postiz Public API.
- Postiz ↔ social media OAuth providers.
- Pipeline ↔ external research sources (Firecrawl, Aside, YouTube).
- Human operator ↔ Postiz UI and social accounts.

## STRIDE threats

| STRIDE | Threat | Control |
|---|---|---|
| Spoofing | Unauthorized user reaches Postiz UI/API over LAN or internet | Bind Postiz to `127.0.0.1`; strong admin password; disable registration after first account |
| Spoofing | Stolen Postiz API key submits posts | Store API key only in `.env`/keychain; rotate if exposed |
| Tampering | Malicious edit to generated content before publish | Compliance gate + provenance + human approval |
| Tampering | Untrusted container image updates | Pin images where possible; document digest/version; avoid `latest` for production |
| Repudiation | No audit of what was generated/submitted | Event store rows for creatives, publish_queue, disclosures, cost_ledger |
| Information disclosure | Tokens/secrets committed to git | `.env` gitignored; Postiz compose with JWT in `.aiwg/working` gitignored |
| Information disclosure | Postiz exposed publicly | Localhost-only port binding required; no public tunnel except explicit timeboxed OAuth |
| Denial of service | Zombie Docker container prevents security changes | Manual Docker Desktop restart required; document recovery |
| Elevation of privilege | Postiz account remains open registration | Disable registration after admin account creation |

## Show-stoppers

1. Postiz/Temporal ports currently exposed on all interfaces (`*:4007`, `*:7233`) due failed Docker recreate.
2. Docker zombie `spotlight` container prevents clean port-binding remediation until Docker Desktop is restarted.

## Required controls before public posting

- Postiz bound to `127.0.0.1` only.
- Temporal UI/ports bound to `127.0.0.1` only or not published.
- Postiz admin created; registration disabled.
- Social OAuth configured by operator.
- Postiz API key stored outside git.
- Public publishing remains human-approved.
