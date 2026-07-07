# Higgsfield Prompt Audit

**Date**: 2026-07-04  
**Scope**: Claude/Fable render prompts, Loadout Lab v1 assets, creator-commerce prompt rules  
**Decision**: v1 Loadout Lab prompts were compliant but not generation-worthy for viral Shorts

## Finding

The supplied Loadout Lab prompts were safe but weak:

- They described product-adjacent objects instead of a GTA6-native story moment.
- GTA6 appeared mostly in the negative block (`no GTA footage`) rather than as a positive launch-night relevance anchor.
- They had UI motion but no real retention payoff.
- They could become B-roll, but they do not justify paid generation as primary assets.

Example rejected pattern:

```text
Vertical 9:16 macro close-up of a generic matte-black game controller...
floating neutral analog-stick test grid...
FIX FIRST...
Mood: practical, honest, buyer-guide, launch prep.
```

Why it fails: there is no visible GTA6/day-one pressure, no final-frame reason to stay, and no story-specific asset that a gaming viewer would recognize as timely.

## New Gate

Added deterministic prompt gate:

```bash
aflack prompt-quality --text "<prompt>"
```

The old controller prompt fails with:

```text
missing positive GTA6/day-one/Vice relevance anchor
missing visible payoff or end-state reveal
```

The revised prompt pattern passes:

```text
Opening frame: GTA6 day-one setup audit...
Motion: crash zoom...
Middle action: test fails...
Final frame: checklist reveal / loop...
Negatives: logos, footage, likeness, marks...
```

## Creator/Market Lessons From Aside Pass

Aside surfaced or reinforced these creator models:

| Creator / model | Evidence type | Lesson for prompts |
|---|---|---|
| Roboverse | Higgsfield tutorial with 205k+ views; teaches controlled production pipeline, consistency, intentional videos | Prompt packs must control continuity, camera, and shot purpose; not random cool outputs. |
| Nate Herk / AI Automation Society | Large Skool/community + Claude/Higgsfield automation content | Product is the repeatable operating system; prompts should be encoded as workflows and skills. |
| Daniel Riley / AI Video Bootcamp | Large Skool AI video/image community | Beginners pay to avoid guessing; our prompt rules must make failure modes explicit. |
| AI Guy / Egor Roslov | AI video/course/community pattern surfaced in Aside memory | Sell prompt libraries and production systems, not single outputs. |
| Lucas Walter / AI automation/news-to-script pattern | Automation funnel surfaced in Aside memory | Turn research into scripts into asset prompts with a fixed schema. |
| UGC creator/coaches | Brand partnership and UGC coaching evidence surfaced by Aside | Native-feeling creator format beats polished product shots; prompts must simulate a human reason to watch. |

## Implemented Changes

- Added `src/aflack/prompt_quality.py`.
- Added `tests/test_prompt_quality.py`.
- Added CLI command `aflack prompt-quality`.
- Added `.aiwg/creator-commerce-ops/skills/higgsfield-asset-prompting.md`.
- Added `.aiwg/creator-commerce-ops/rules/no-safe-boring-generation.md`.
- Updated `.aiwg/creator-commerce-ops/workflows/claude-video-production.md`.
- Revised `.aiwg/marketing/loadout-lab/episode-001-affiliate-package.md` with a v2 story-native asset prompt pack.

## New Prompt Contract

Every paid-generation prompt must include:

1. positive story relevance anchor,
2. first-frame hook,
3. viewer problem or tension,
4. camera/edit motion,
5. visible final-frame payoff,
6. continuity/world-bible reference,
7. compliance negatives,
8. QC/kill criteria.

## Operational Rule

Safe but boring is blocked. A compliant prompt can still fail construction if it does not create an asset that is likely to hold attention inside a Short.
