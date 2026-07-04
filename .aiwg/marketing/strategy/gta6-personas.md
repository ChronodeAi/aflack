# GTA6 Gaming Channel — AI Persona Roster (v1)

**Created**: 2026-07-04
**Niche**: gta6-ai-persona-gaming (Beachhead A)
**Rule**: Personas are synthetic, non-impersonating, and disclosed. They present ORIGINAL commentary/analysis over ORIGINAL or clearly-licensed visuals — never wholesale reposts of Rockstar pre-release footage.

## Ethics/disclosure policy (applies to ALL personas)

- Synthetic/AI-assisted persona; not a real person; no impersonation of any real individual.
- No false firsthand claims ("I played the leaked build"), no leaked/pre-release footage.
- Affiliate relationship disclosed; AI-assisted content disclosed where required by platform/FTC.
- Commentary is transformative: original scripts, original or licensed visuals, minimal defensible third-party excerpts only.
- No medical/financial/again-illegal claims; gaming context only.

## Role/persona scope rule

Do not overbuild roles. V1 uses:

- **One internal director runtime**: Claude Code CLI `claude-fable-5` (ADR-0004)
- **Two active public personas**:
  - Vice Signal (attention/news/Shorts)
  - Loadout Lab (affiliate/gear/monetization)

Everything else is backlog until metrics prove the need.

## Personas

| Handle | Archetype | Voice | Content lane |
|---|---|---|---|
| **Vice Signal** | Hype analyst | Fast, punchy, hype-but-credible | Countdown, trailers breakdown (commentary), "days until" |
| **Lore Vault** | Lore/theory | Calm, deep, narrative | Vice City lore, story theories, map/character analysis |
| **Patch Notes** | News/leaks-debunk | Skeptical, factual | What's confirmed vs rumor, debunking fake leaks (no leaked footage shown) |
| **Rng Goblin** | Comedy/reaction | Chaotic, meme-native | Reaction-style takes, community memes, hot takes |
| **Loadout Lab** | Gear/affiliate | Practical, helpful | Best setup to play GTA6 (controllers, headsets, capture cards, monitors) — affiliate lane |

## Notes

- Loadout Lab is the primary affiliate monetization persona (gaming-adjacent gear).
- Vice Signal + Patch Notes drive Shorts velocity (top-of-funnel).
- Lore Vault anchors long-form YouTube (high RPM).
- Rng Goblin farms shareability/comments.
- Higgsfield reference/identity assets to be generated per persona; store `higgsfield_ref` in `personas`.

## V1 activation

| Persona | V1 status | Why |
|---|---|---|
| Vice Signal | Active | Fastest path to GTA6 Shorts/news/commentary velocity. |
| Loadout Lab | Active | Direct monetization lane: gaming-adjacent affiliate. |
| Lore Vault | Backlog | Useful for long-form later, but not needed for first batch. |
| Patch Notes | Backlog | Can merge into Vice Signal initially. |
| Rng Goblin | Backlog | Fun, but avoid persona sprawl until we see traction. |
