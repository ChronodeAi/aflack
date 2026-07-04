# Compliance Decision — GTA6 Footage Handling

**Created**: 2026-07-04
**Status**: BLOCKING RULE for the gta6-ai-persona-gaming niche

## Requested (rejected as designed)

"Take official GTA6 pre-release video footage, clip it, and remix/regenerate new content from the same seed as the pre-release gameplay."

## Decision: DO NOT implement as described

Grounds:

1. **Pre-release footage is the hardest red line.** Rockstar/Take-Two policy: postings of in-game footage before official release are removed regardless of how obtained. GTA6 is unreleased (launch 2026-11-19).
2. **Copyright / derivative work.** Their trailer/gameplay is copyrighted. Clipping + "same-seed" video-to-video regeneration produces derivative works of protected, pre-release material.
3. **Non-commercial policy.** Take-Two's fan-content tolerance is non-commercial; our use is explicitly monetized (affiliate/creator revenue).
4. **Platform demonetization.** Reused/inauthentic content is demonetized/removed (YouTube, TikTok), risking channel termination.
5. **Litigation history.** Take-Two has sued over IP (e.g., Red Dead modding project, 2019).

Net: high risk of DMCA strikes, channel/account termination, and legal exposure — which destroys the audience asset we are building.

## Allowed alternatives (compliant, same funnel)

- Original AI-generated Vice-City-INSPIRED visuals (our own scenes/personas), NOT Rockstar frames.
- Transformative commentary/analysis/countdown/lore/predictions as the dominant content.
- Minimal, defensible third-party excerpts only where fair-use commentary genuinely applies, dominated by original voice/visuals.
- After public release: our OWN gameplay capture becomes usable under normal (non-pre-release) policy.

## Enforcement

- The compliance gate MUST block any publish item whose source is Rockstar pre-release footage or a same-seed regeneration of it.
- `claims`/`disclosures` and source provenance must record footage origin; pre-release third-party origin = auto-reject.
