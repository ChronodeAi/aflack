# Risk Register — Affiliate Content Pipeline

**Created**: 2026-07-04
**Status**: Elaboration baseline

| ID | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---:|---:|---|---|
| R-001 | Rockstar/Take-Two IP strike from reused/pre-release footage | High | Critical | Block footage/same-seed remix; original visuals only; provenance gate | Compliance |
| R-002 | YouTube/TikTok reused-content demonetization | High | High | Original AI-persona content; commentary dominant; avoid reposts | Director |
| R-003 | Postiz platform OAuth/API blocks posting | Medium | High | Human OAuth setup; draft/private/manual gate; Aside fallback | Operator |
| R-004 | YouTube API project/audit forces private uploads | Medium | Medium | Treat private/draft upload as normal; human publish until verified | Operator |
| R-005 | Higgsfield credit burn before ROI | Medium | High | Daily credit cap; cost ledger; validate cheaply before final | Operator |
| R-006 | Role/persona sprawl slows MVP | Medium | Medium | V1 role budget: director + operator + Vice Signal + Loadout Lab | Operator |
| R-007 | pgGraph alpha rough edge breaks migrations | Medium | Medium | Keep behind abstraction; clean graph state before schema drops | Engineering |
| R-008 | Postiz AGPL boundary misunderstood | Low | High | API-only separate service; no vendoring/modifying Postiz | Architecture |
| R-009 | Claude director over-produces non-actionable ideas | Medium | Medium | Fixed prompt, cost/time limits, output schema, event capture | Operator |
| R-010 | No direct affiliate fit in GTA6 | Medium | Medium | Loadout Lab focuses gaming-adjacent affiliate; YouTube long-form RPM | Strategy |
| R-011 | Over-reliance on Higgsfield (bans/throttling/payment issues per Forbes/Reddit/X-suspension) | Medium | High | Keep generation behind swappable interface; evaluate alt generators; own audience/lead magnet/posting infra | Architecture |
| R-012 | Scaling volume before funnel works burns credits | High | High | Prove one hook->CTA->lead-magnet->conversion loop before 20/day; gate on cost-per-winning-video | Operator |
| R-013 | Comment-to-DM automation compliance (opt-in, disclosure, no scraping) | Medium | High | YouTube-native funnel (pinned comment + description) first; opt-in + disclosure if DM automation later | Compliance |

## Top show-stoppers

1. Any plan requiring direct reuse/same-seed remix of Rockstar pre-release footage.
2. Public publishing before Postiz/social OAuth and compliance approval.
3. Large paid generation batch before economics caps are implemented.
