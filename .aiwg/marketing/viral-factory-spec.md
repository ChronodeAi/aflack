# Viral Video Content Factory — Spec v1

**Created**: 2026-07-04 · **Company**: Memetics · **Prime directive**: engineered virality — views are the product.
**Synthesized from**: REF-004 (creator playbooks), fifa-ig-field-study.md, fifa-tiktok-field-study.md, trend-radar-2026-07-04.md, hook library, Tier-2 event policy (decision memo), operator directives (personas optional; sequential agents; draft→promote; real-world grounding).

## North-star metrics

| Metric | Target | Why |
|---|---|---|
| **Sends/shares per reach** | ≥2% (3%+ = viral) | Platform-stated #1 signal; DM shares weigh 3-5x likes (Mosseri) |
| Time-from-trend-to-publish | **<3 hours** | Professional bar (REF-004); moments die in 24h |
| Viral hit rate | ≥5% of posts >1M views | Portfolio math beats per-post hopes |
| Retention | <30s cuts: ~100% (loop-engineered); 60s+ cuts: 80-90% | Viral thresholds (REF-004 §2) |
| Views/week | compounding WoW | The product |

## The pipeline (per post)

```
1 TREND RADAR   → what spiked in the last 24h (daily Firecrawl sweep + field-study refresh 2x/wk)
2 MOMENT BRIEF  → Aside WATCHES real highlights → second-by-second choreography doc (facts, not pixels)
3 HOOK SYNTH    → hook library templates × REF-004 formulas; first-frame text readable on mute
4 GENERATION    → GPT-Image-2 draft → Soul/NB2 promote → Seedance i2v (own canon frames as refs)
5 CUT & LOOP    → sub-30s discovery cut (seamless loop) + 60s+ TikTok-monetizable cut; captions from word 1
6 PUBLISH       → Postiz (ADR-0001); native per-platform files (no watermarks); platform music picker
                  for official/trending audio (intro/outro only); AI-labels ON; TikTok caption SEO stuffed
7 MEASURE       → per-post: shares/reach, retention curve, rewatch — into event store (ADR-0002)
8 MEMORY LOOP   → performance events into pggraph memory (ADR-0003) → next batch weights winners
```

## Batch composition — Hormozi 70/20/10 (REF-004 §4)

70% proven winners (formats that already scored for us) · 20% iterations (winner + new twist) · 10% experiments (new formats/lanes). Post cadence ramp: 1-2/day/platform once accounts live.

## Format playbook (from the field-study leaderboard, rendered Tier-2)

| Field-observed format (views ceiling) | Our Tier-2 version |
|---|---|
| **AI/absurd meme remix (40M — highest ceiling)** | Native lane: original AI comedy scenes riffing on real memed moments; stylized recognizable-but-obviously-AI players; parody framing |
| Emotional underdog edit-montage (19-35M) | Moment-brief-driven stylized recreation of the underdog arc (this week: Cape Verde/Vozinha) + our narration; no broadcast pixels |
| GOAT worship/fan-crowd (6-14M) | Vice-world crowd/atmosphere scenes + commentary naming real players (speech is free) |
| TikTok velocity edits | Our own generated footage velocity-cut with TikTok-native grammar |

**Main-character tracker** (weekly): virality follows whoever the tournament makes protagonist — this week Vozinha + Haaland, not only Messi/Ronaldo. Persona-free formats are first-class (operator directive); Vice Signal appears only where the character adds reach or brand equity.

## Lanes

1. **FIFA reactive lane** (NOW → Jul 19+): daily moment-driven Tier-2 content; highest-velocity lane.
2. **Vice-final series** (bridge): Ep1 asset-complete; Ep2 branches on Portugal–Spain Monday.
3. **GTA6 lane** (Jul → Nov 19): hook batches banked; scales as launch nears.
4. **B2B fly-through** (backlog): activates post-FIFA sprint; first non-view revenue line.

## Platform discipline

- TikTok: caption SEO with exact match phrases ("FIFA World Cup 2026", fixture names) — TikTok search ranks it; 60s+ cut for Creator Rewards eligibility.
- IG: sub-30s loop cut for discovery; shares-optimized endings ("send this to the friend who…").
- Official FIFA anthem: platform music-picker only (platform-licensed), intro/outro, never baked into files.
- No watermarks cross-posted, ever (downranking).
- AI-content labels always on: legally required posture AND the AI-meme lane thrives with them.

## Revenue design (REF-004 §5 — platform payouts are rounding errors)

Views → audience → brand deals (70% of creator income at scale) + affiliate (Loadout Lab lane) + DM-automation funnels (comment-keyword → product; 300-400% conversion lift) + B2B fly-through revenue. TikTok Creator Rewards on 60s+ cuts as bonus, never the plan.

## Compliance delta (standing)

Tier 2 = ceiling for real-event content (memo: `.aiwg/security/decision-memo-event-reference-policy.md`); Tier 3 requires signed override. GTA6 pre-release gate absolute. Adverse finding logged: IG reportedly deprioritizes obvious-AI content — mitigate via human-feel VO, parody framing, shares-first design (REF-004 §7).

## Ops cadence

- Daily: trend sweep → moment briefs → batch generation (sequential, per operator policy) → publish → metrics ingest.
- 2x/week: field-study refresh (Aside), hook-library update.
- Weekly: main-character tracker, format leaderboard re-rank, 70/20/10 rebalance, credit budget review.
