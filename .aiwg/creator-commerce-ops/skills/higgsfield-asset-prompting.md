# Skill: higgsfield-asset-prompting

Purpose: turn a short-form script/shot list into generation-ready Higgsfield,
Seedance, Soul, or image/video prompt packs that are both compliant and
attention-native.

## Required Inputs

- niche and target platform,
- script with timestamps,
- active benchmark insights,
- world bible or visual continuity rules,
- compliance constraints,
- CTA/funnel destination,
- prior asset failures or accepted canon references.

## Output Contract

Do not emit one generic prompt for the whole video. Emit:

1. seed/master-image prompts when continuity matters,
2. one prompt per shot/beat,
3. opening-frame intent for each shot,
4. camera/motion direction,
5. visible problem/tension,
6. final-frame payoff or loop target,
7. negative/compliance constraints,
8. text-render fallback plan,
9. QC checklist and kill criteria.

## Prompt Quality Gate

Every short-form asset prompt must contain:

- a positive relevance anchor, such as `GTA6 day-one`, `launch night`,
  `Vice`, `open-world`, or the current event/story window,
- a viewer problem, mystery, contradiction, or tension,
- a motion/edit instruction,
- a visible payoff or end-state reveal,
- explicit negative constraints for brands, source footage, logos, likeness,
  and platform-sensitive marks.

Prompts that only describe a safe object, desk, product, icon card, or mood are
not generation-ready. "Safe but boring" is a failed prompt, not a pass.

## Good Pattern

```text
Opening frame: [story-native problem visible immediately].
Motion: [camera move or edit grammar].
Middle action: [diagnostic, conflict, or transformation].
Final frame payoff: [what changes, what is revealed, why viewer stayed].
Continuity: [world/character/seed references].
Negatives: [rights, logos, likeness, prohibited claims].
```

## GTA6 / Vice Signal Rules

- Use GTA6 as commentary/context, not as source media.
- If the prompt says `GTA`, `Rockstar`, or `Take-Two`, it should usually be in
  the negative/compliance block unless the phrase is a text overlay such as
  `GTA6 day-one setup`.
- Make the world do the work: diegetic countdowns, launch-night diagnostics,
  Vice-world billboards, neon lab interfaces, stadium screens, or creator
  workbench props.
- Avoid generic "gaming desk" shots unless the desk is carrying story pressure.

## Validation

Run or mirror `aflack.prompt_quality.check_short_asset_prompt` for representative
prompts before spend. A prompt may pass compliance and still fail virality.
