# Security Gate — 2026-07-04

**Current decision**: **PASS FOR CONSTRUCTION ITERATION 1**

## Summary

The earlier local Postiz network exposure was remediated by binding local services to `127.0.0.1`. The operator has now switched the active publisher to paid cloud Postiz, configured a cloud API key, and connected YouTube/TikTok integrations.

## Verified controls

| Gate item | Status | Evidence |
|---|---|---|
| Local network exposure remediated | PASS | Host `lsof` shows Postiz/Temporal/Spotlight/DB ports on `127.0.0.1` only. |
| Cloud Postiz API configured | PASS | `.env` uses `POSTIZ_BASE_URL=https://api.postiz.com`. |
| Cloud integrations connected | PASS | `aflack postiz-integrations` returns YouTube `Memetics Sa` and TikTok `memetics365`. |
| Secrets not committed | PASS | `.env` remains untracked/gitignored; `.env.example` has no secret. |
| Public publishing blocked | PASS | Draft mode is default; public publish remains human-gated. |
| High-risk GTA6 footage blocked | PASS | Compliance smoke blocks same-seed official footage and missing disclosures. |

## Conditions that remain active

- Public publishing requires explicit operator approval.
- Paid Higgsfield generation requires explicit operator approval or an approved cap.
- Comment/DM automation requires explicit operator approval.
- Official Rockstar/GTA6 footage cannot be downloaded, clipped, reuploaded, or same-seed remixed.
- If local Postiz is not needed, prefer stopping it later to reduce local attack surface; do not expose it beyond localhost.

## Allowed now

- Local Construction Iteration 1 coding.
- Cloud Postiz integration listing.
- Creating a Postiz **draft** after confirming the queue item and integration target.
- Research, scripting, prompt-writing, and compliance checks.

## Not allowed without a fresh human approval

- Public posts.
- Paid Higgsfield jobs.
- OAuth/channel setting changes.
- DM/comment automation.
