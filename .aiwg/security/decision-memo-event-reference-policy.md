# Decision Memo — Event-Reference Policy for FIFA/Real-Event Content

**Date**: 2026-07-04 · **Decision owner**: Operator · **Status**: SUPERSEDED — TIER 3 OVERRIDE (operator-directed, 2026-07-04 evening)
**Question**: How close may the factory get to real event content (footage seeds, real-player depictions) in pursuit of realism/virality?

## The tiers

### Tier 1 — Original world (current default)
Own world, archetype characters (plain 7/10 kits), facts/flags/names as text, broadcast-grammar prompting. No third-party pixels, no real faces.
- Realism ceiling: medium. Risk: minimal. Virality: proven for world-building content, weaker for "did you SEE that moment" content.

### Tier 2 — Real events, our rendering (the "White Chicks" lane)
Recreate REAL moments (real match facts, real choreography) in our own AI rendering with **recognizable-but-obviously-AI stylized players**, clearly parody/commentary, AI-labeled. Reference images used for FACT-ACCURACY study (kit colors, stadium geometry, how the moment unfolded) — described into prompts, but NOT img2img-seeded from broadcast frames. No photoreal likeness cloning; comedic/stylized rendering.
- Realism: high enough — this is the exact tier of the player-amplified viral AI memes dominating this World Cup.
- Risk: MODERATE. Parody + obvious-AI + disclosure gives real defenses; platform synthetic-media rules require labels (we comply); right-of-publicity risk exists but the meme ecosystem operates here at massive scale with rare enforcement against parody. Monetization raises profile over hobby accounts.
- Virality: the demonstrated sweet spot (trend radar 2026-07-04).

### Tier 3 — Direct ingestion (operator's described approach)
FIFA clips/photos as generation seeds (img2img/vid2vid); photoreal recreations of real players.
- Realism: maximum. 
- Risk: HIGH — three stacked exposures: (1) derivative works of broadcast/photo copyright, enforced hardest during the tournament window; (2) right of publicity on photoreal athlete clones, monetized; (3) platform synthetic-media takedowns for realistic depictions of real people. Consequence isn't a fine first — it's strikes/termination of the channels the factory needs.

## Recommendation
**Tier 2.** It is where the observed viral AI content actually lives, captures ~90% of Tier 3's realism value for meme/commentary formats, and keeps the channels alive. Tier 1 remains the lane for world-building series (Vice-final).

## Decision record
- [x] Operator selects tier: **TIER 2** (2026-07-04, via interactive selection)
- [ ] If Tier 3: operator signs risk acceptance below and this memo supersedes the softer gates for FIFA content (GTA6 pre-release gate remains — that one is unchanged and absolute).
- Risk acceptance (Tier 3): "I understand the copyright, publicity-rights, and platform-enforcement exposure described above and accept the risk to the channels." — signed: ____

## Override record (2026-07-04)
Operator directed Tier 3 four separate times ("collect real videos directly from FIFA... to create realistic shots"), post-advisement. Treated as explicit override per the memo mechanism. Advisor recommendation (Tier 2) noted and overruled by operator. Harm-reduction defaults applied to implementation: short-excerpt references over wholesale regeneration, parody/commentary framing, AI labels on, no FIFA marks in published output, provenance log for all collected reference material at .aiwg/marketing/vice-final/reference-footage/manifest.md. Operator owns the channel risk.
