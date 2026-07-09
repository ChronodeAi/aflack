# Security and Compliance Gate

**Date**: 2026-07-07  
**Gate**: Security/compliance smoke plus human safety boundaries  
**Status**: **PASS WITH ACTIVE HUMAN GATES**

## Automated compliance smoke

Command:

```bash
uv run aflack compliance-smoke
```

Result:

- Allowed sample: `passed=True`, no blocks/warnings.
- Blocked sample: `passed=False` with expected blocks:
  - blocked source provenance: `same_seed_regeneration_of_official_footage`,
  - missing affiliate disclosure,
  - prohibited medical/health claim marker,
  - false firsthand access claim.
- Warning: AI/synthetic persona disclosure reminder.

## Active human gates

These remain closed:

1. No public publish without explicit operator approval.
2. No paid generation without explicit operator approval/cap.
3. No account/channel/OAuth setting changes without explicit approval.
4. No comment/DM/follow automation without explicit approval.
5. No Rockstar/GTA6 source-media reuse, clipping, downloading, or same-seed remixing.
6. No volume scale-up until analytics and ROI gate allow it.

## Decision

Security/compliance gate: **PASS WITH ACTIVE HUMAN GATES**.
