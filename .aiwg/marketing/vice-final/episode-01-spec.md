# Episode 01 — "The Final Everyone Wants Doesn't Exist Yet"

**Ship by**: 2026-07-05 night (must land before Portugal–Spain, Mon Jul 6 Dallas)
**Runtime**: 28s vertical (9:16) · **Persona**: Vice Signal (VO only — no face needed, no soul-training dependency)
**Transmission #**: 001

## Script (VO + on-screen text + shots)

| t | Shot | VO (Vice Signal — fast, low, confident) | On-screen text |
|---|------|------|------|
| 0-2s | S1: Aerial night — neon stadium glowing alone on the Vice waterfront, city behind | "The final everyone wants… doesn't exist yet." | THE FINAL EVERYONE WANTS DOESN'T EXIST YET |
| 2-6s | S2: Push-in past palm trees to stadium gates; marquee reads "JULY 19" | "The real one's in New Jersey. So we built our own — in Vice." | WE BUILT OURS IN VICE |
| 6-11s | S3: Interior bowl reveal — 80,000 empty seats, scoreboard holo: **7 — 10** | "Two number sevens and tens have been circling each other for twenty years. They've never met in a final." | 20 YEARS. NEVER IN A FINAL. |
| 11-16s | S4: Tunnel shot — two kits hanging opposite: crimson **V7**, azure **X10** (no crests, no names) | "In our city, the match is already scheduled. Down to the last player. Simulated a thousand times." | SIMULATED 1,000 TIMES |
| 16-22s | S5: Stadium mega-screen: bracket graphic "3 WINS AWAY" ×2; cut to city billboard ticker | "But out there? Each of them is three real wins away. And Portugal plays Spain — Monday." | 3 WINS AWAY · PORTUGAL v SPAIN — MONDAY |
| 22-26s | S6: Storm clouds gathering over the lit stadium; one seat section lights flicker on | "If they survive… Transmission 002 drops after the whistle." | TRANSMISSION 002: AFTER THE WHISTLE |
| 26-28s | S7: Return to S1 aerial framing (loop point) | "The city's ready. Are they?" | FOLLOW FOR THE FINAL VICE DESERVES |

**Hidden detail (rewatch seed)**: in S3, one seat in the empty bowl is occupied (silhouette). Do not mention in VO; pin a comment "someone's already in the stadium 👀" 1h after posting.

**Loop**: S7 matches S1 camera position/lighting → seamless autoplay replay.

## Caption

> The real final is in New Jersey. We built ours. Two GOATs, three wins each, one city that's already ready. Portugal–Spain Monday decides everything. Transmission 002 after the whistle. 🌴
> (AI-generated original world — not game footage.)
> #worldcup2026 #messi #ronaldo #vicecity #ai

Caption may name real players (commentary); visuals never depict them.

## Higgsfield production plan

**Pipeline**: generate 4 master seed IMAGES (world anchors, below) → image-to-video (Seedance 2.0) per shot with camera-move prompts → VO (Vice Signal voice) → synthwave bed + crowd-distant ambience (seed_audio) → edit to beat sheet.

### Master seed images (generate first — these anchor ALL episodes)

| ID | Prompt (GPT Image 2, 9:16 unless noted) |
|---|---|
| SEED-A | Cinematic aerial night shot of an original retro-futurist football stadium on a neon-lit Miami-inspired waterfront, glowing magenta and teal rim lighting, palm trees, 1980s-Miami-noir synthwave atmosphere, wet asphalt reflections, city skyline with pink-orange haze behind, marquee sign reading "JULY 19", photoreal cinematic grade, anamorphic, no logos, no real-world brands |
| SEED-B | Interior of a vast empty football stadium bowl at night, 80,000 teal seats, giant holographic scoreboard floating above the pitch displaying only "7 — 10" in neon, magenta pitch-edge lighting, volumetric haze, retro-futurist Miami-noir style, one single distant silhouetted figure seated alone in the stands, cinematic, no logos |
| SEED-C | Players' tunnel of a neon-lit stadium, two football kits hanging on opposite walls facing each other: left kit deep crimson with emerald trim and a stylized "V7", right kit pale azure with ivory trim and a stylized "X10" (solid color, no stripes), dramatic rim lighting, mist on the floor, cinematic tension, no faces, no crests, no brand logos |
| SEED-D | Neon city street at night, Miami-inspired, giant animated billboard ticker above traffic reading "3 WINS AWAY" and "FINAL · JULY 19", palm silhouettes, wet streets reflecting magenta/teal signage, synthwave cinematic grade, no real brands or logos |

### Shot generation (image-to-video from seeds)

- S1/S7 ← SEED-A: slow orbital drone push (S7: reverse to matching frame)
- S2 ← SEED-A variant: low dolly through palms toward gates
- S3 ← SEED-B: rising crane reveal, scoreboard flare
- S4 ← SEED-C: slow lateral dolly between the kits
- S5 ← SEED-D + SEED-B screen insert: ticker animation
- S6 ← SEED-A + storm-sky variation: timelapse clouds, lights flicker

### Audio

- VO: Vice Signal voice (seed_audio TTS or configured voice) — script above, 24s of speech budget
- Music: dark synthwave bed, 100-110 BPM, builds at 16s
- SFX: distant crowd swell under S3, thunder under S6

## Pre-publish gate (from series-spec compliance checklist)

- [ ] Re-verify Mon fixture is still Portugal–Spain, Dallas (schedule can shift)
- [ ] No crests/stripes/real likenesses slipped into generations (inspect every frame batch)
- [ ] AI-label on; caption includes "AI-generated original world" line
- [ ] Countdown numbers current at render time
