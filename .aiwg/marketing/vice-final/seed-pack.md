# Seed Pack — "Vice Hosts the Final" (Episode 01+)

**Purpose**: everything needed to seed the scene — verified facts for the commentary layer, aesthetic references for the world, and the asset manifest. Reference links are cite/inspiration ONLY — we never ingest or regenerate third-party footage (compliance gate).

## Verified facts (commentary layer) — as of 2026-07-04

| Fact | Detail | Source |
|---|---|---|
| Portugal R32 | Beat Croatia 2-1 (Jul 2); Ronaldo scored the equalizer, Gonçalo Ramos winner | ESPN MD16 recap |
| Portugal R16 | vs Spain, Monday Jul 6, Dallas | ESPN |
| Argentina R32 | Beat Cape Verde 3-2 (Jul 3); 111' own goal settled it | ESPN Jul 3 blog |
| Argentina R16 | vs Egypt, Tuesday Jul 7, Atlanta | ESPN |
| Real final | Jul 19, 2026, MetLife Stadium NJ | tournament schedule |
| Dream-final math | Each side needs 3 wins (R16→QF→SF) to reach the final | bracket |
| GTA6 tie-in | Launch Nov 19 2026 = 138 days from Jul 4 (recompute per episode) | sources/gta6-reference-pack.md |

**Re-verify before every episode** — live sports; scores/fixtures are the one thing we must never get wrong.

## Aesthetic references (style/theme inspiration ONLY — link, never ingest)

- GTA6 official trailers (Rockstar) — neon-Miami palette, humid-noir mood: see `.aiwg/research/sources/gta6-reference-pack.md` (provenance table; do NOT download/clip/regenerate — blocking rule in `.aiwg/security/compliance-gta6-footage.md`)
- Miami real-world texture (public context, not to copy): Hard Rock Stadium is a real WC-2026 venue — grounding for the "Miami deserved the final" joke; our stadium design is ORIGINAL retro-futurist, not a replica
- Style vocabulary for prompts: synthwave / Miami-noir / magenta-teal rim light / wet asphalt reflections / palm silhouettes / volumetric haze / anamorphic cinematic grade

## World bible (v0 — locks consistency across episodes)

- **The city**: unnamed neon-Miami-inspired metropolis; we call it "Vice" in-voice, never "Vice City, the GTA6 location" in claims
- **The stadium**: original retro-futurist waterfront bowl, 80k teal seats, holographic scoreboard, marquee "JULY 19"
- **The 7**: crimson/emerald kit, "V7" mark, no face shown in Ep01
- **The 10**: azure/ivory SOLID kit (no stripes), "X10" mark, no face shown in Ep01
- **Diegetic tickers**: "3 WINS AWAY" / "FINAL · JULY 19" — the countdown lives inside the world
- **Recurring mystery**: the lone silhouette in the stands (seeded Ep01; identity = long-arc hook)

## Asset manifest — Episode 01

| Asset | Status | Tool |
|---|---|---|
| SEED-A..D v1 | done — `assets/seed-*-v1.png` (URLs in `assets/seed-urls.txt`). v1 issues: A has full stands (want empty), B rendered an American-football field (blocker). C/D excellent. GPT Image 2 nailed ALL text renders — keep v1 as text-shot fallback | GPT Image 2 |
| SEED-A/B/D v2 | generating — Soul Location (photoreal environments), soccer-pitch + empty-stands fixes in prompts | soul_location |
| SEED-C v2 | generating — Soul Cinematic 2k | soul_cinematic |
| **CANON SET (locked 2026-07-04)** | SEED-A=`seed-a-v2.png` (marquee text garbled — S2 gate shot needs text fix or v1 fallback) · SEED-B=`seed-b-v2.png` · SEED-C=`seed-c-v5.png` (9:16, V7/X10 marks, logo-free) · SEED-D=`seed-d-v3.png` (billboard text clean) | — |
| Text-render rule | If Soul v2 text (marquee/scoreboard/billboard) degrades, hybrid: Soul environment + text-insert edit pass (nano banana / Seedream edit), or v1 GPT frame for text-bearing shots | — |
| Reference policy | GTA6 trailers are LINK-ONLY style vocabulary — never passed as --image/--video references (blocking rule, compliance doc). World consistency via our OWN generations as references | — |
| S1-S7 video shots | pending seeds | Seedance 2.0 image-to-video |
| Vice Signal VO (24s) | pending script lock | seed_audio / TTS |
| Synthwave bed + SFX | pending | seed_audio |
| Vice Signal soul (face) | NOT needed Ep01 | higgsfield-soul-id (backlog) |
