# Vice Signal EP001 — Script Relevance Reset

**Date**: 2026-07-08  
**Decision**: Freeze new asset generation. Move back to script writing.  
**Reason**: Original renders were not relevant enough to the original script ask.

## Operator feedback

> "Let's not build more assets, we need to work on our script writing. Our original renders were nowhere near relevant to the original script ask."

## Decision

- No new Higgsfield generations.
- No new render assembly work.
- No public publish escalation.
- The current `final-render-candidate-v2.mp4` remains a **visual experiment / rejected-for-script-relevance review cut**, not a publish candidate.
- EP001 moves back to **Script Room** until the script, visual receipts, and shot list are aligned.

## What went wrong

The prior package had a decent *concept* but a weak script-to-visual contract.

### Root mismatch

The script promised a concrete creator-workflow story:

- an AI content channel that "runs itself";
- a written workflow;
- persona, prompts, shot lists, publishing checklist;
- an exact workflow viewers could get by commenting `JARVIS`.

The renders mostly delivered:

- neon skyline;
- synth persona;
- generic "AI-generated" stamps;
- CTA end card.

That means the viewer saw aesthetic world-building, but not enough proof of the
workflow. The words said "machine"; the visuals said "vibe." The content did
not pay off its own hook.

## New script rule: every line needs a receipt

Before a line survives, it must answer:

1. What exactly is the viewer seeing while this line plays?
2. Does that visual prove, demonstrate, or intensify the line?
3. Can this be shown with existing local/non-paid assets, screen recordings,
   simple text cards, diagrams, or original graphics?
4. If the visual is only aesthetic, does the line actually need it?

If the answer is no, cut or rewrite the line.

## Script guardrails going forward

### Do

- Lead with a real, concrete claim we can show.
- Make the body demonstrate the system, not merely describe it.
- Use screen-recordable artifacts: `.aiwg` package, prompt table, shot list,
  publish checklist, ROI gate, approval gate, analytics gate.
- Turn compliance into credibility: "no leaked footage, no ripped trailer clips."
- Use countdown/hype only as context, not the whole substance.
- Close with a CTA that directly matches what was demonstrated.

### Do not

- Do not claim the channel "runs itself" unless the video shows automation.
- Do not ask the model for a vague cinematic world when the script needs proof.
- Do not let a persona render substitute for a workflow demonstration.
- Do not generate more assets before the script has a concrete beat-by-beat visual receipt list.
- Do not use Rockstar/GTA6 footage, logos, typography, or same-seed remixes.

## Reframe options

### Option A — Keep the AI workflow angle, but make it concrete

**Positioning**: "I built the pre-production system for GTA6 content before the game launches."

Pros:
- Matches what we actually have: `.aiwg` packages, scripts, shot lists, gates.
- Strong for the `JARVIS` workflow lead magnet.
- Avoids fake performance claims.

Cons:
- Less immediately exciting than in-world cinematic content.
- Requires better screen/diagram storytelling.

### Option B — Switch to Vice Signal as hype analyst

**Positioning**: "Everyone is waiting for GTA6 content. I am building the audience system now."

Pros:
- Closer to proven hook patterns in `hook-batch-001.md` and `liked-content-tips.md`.
- Can use countdown/news/contrarian structures.

Cons:
- Needs current facts refreshed at render time.
- Lead magnet becomes less direct unless the video bridges from GTA6 hype to creator workflow.

### Option C — Inside-the-game fiction format later

**Positioning**: "Transmission from a city that does not open yet."

Pros:
- Best use for original cinematic renders.
- Strong character/world retention.

Cons:
- Not the right vehicle for explaining a creator workflow.
- Should be a separate format, not EP001's first workflow CTA.

## Recommended direction

Use **Option A** for EP001 reset: a proof-led workflow script. Save the cinematic
Vice Signal world for a later "Transmission" series after the script engine is
stronger.

## Rewritten EP001 script v2 — proof-led workflow

**Working title**: `I built the GTA6 content system before the game launches`  
**Target length**: 35-42 seconds  
**CTA**: Comment `JARVIS` for the workflow.  
**Core promise**: The viewer sees the actual workflow scaffold, not just AI visuals.

| Time | VO | On-screen / visual receipt | Why it belongs |
|---|---|---|---|
| 0:00-0:03 | "GTA6 is not out yet. That is exactly why I am building the content system now." | Big text: `GAME NOT OUT. SYSTEM ALREADY BUILT.` plus quick screen flash of the EP001 package filename. | Clear, honest urgency. No fake gameplay claim. |
| 0:03-0:07 | "Most creators are waiting for footage. I am building the machine that turns one angle into scripts, shots, captions, and a publish checklist." | Four-box pipeline diagram: `ANGLE → SCRIPT → SHOTS → PUBLISH CHECKLIST`. | Shows the actual machine; avoids vague automation claim. |
| 0:07-0:13 | "This is the part people skip: pre-production. The hook, the visual proof, the CTA, and the compliance gate all have to match before you spend a credit." | Scroll/crop of package sections: hook options, timestamped script, compliance checklist, spend gate. | Pays off the "system" claim with receipts. |
| 0:13-0:20 | "Here is the mistake I caught: a cool neon render is useless if it does not prove the line in the script." | Split card: left `VIBE`; right `RECEIPT`. Put the rejected render frame under `VIBE`, package/shot table under `RECEIPT`. | Directly incorporates the learning from this failure; high trust. |
| 0:20-0:27 | "So the rule is simple: every sentence needs a visual receipt. If the viewer cannot see the proof, the line gets cut." | Checklist animation: `Line → Receipt → Proof → Keep/Cut`. | Turns process into memorable framework. |
| 0:27-0:34 | "That is how you build a GTA6 channel without leaked clips, fake insider claims, or ripped trailer footage." | Compliance cards: `NO LEAKS`, `NO RIPPED FOOTAGE`, `ORIGINAL/AI DISCLOSED`, `NOT AFFILIATED`. | Compliance becomes differentiated credibility. |
| 0:34-0:40 | "I am turning this into a repeatable workflow. Comment `JARVIS` and I will send the exact script-to-shot checklist." | CTA card: `COMMENT JARVIS` / `SCRIPT → SHOT CHECKLIST`. Disclosure line below. | CTA now matches what the viewer saw. |

## Caption-first version

For Shorts/TikTok/Reels, the caption layer should carry the full structure even
if audio is weak:

1. `GAME NOT OUT. SYSTEM ALREADY BUILT.`
2. `ANGLE → SCRIPT → SHOTS → PUBLISH CHECKLIST`
3. `PRE-PRODUCTION BEFORE CREDITS`
4. `VIBE IS NOT PROOF`
5. `EVERY LINE NEEDS A VISUAL RECEIPT`
6. `NO LEAKS. NO RIPPED FOOTAGE. AI DISCLOSED.`
7. `COMMENT JARVIS FOR THE CHECKLIST`

## Visual receipt contract

Before any future generation/render, produce this table first:

| Script line | Required visual receipt | Existing source | Asset needed? | Approved? |
|---|---|---|---|---|
| GTA6 is not out yet... | Package filename + countdown/fact card | `.aiwg/marketing/vice-signal/episode-001-claude-code-package.md` | No | Pending |
| Most creators are waiting... | Pipeline diagram | Can make locally as text/diagram | No | Pending |
| This is pre-production... | Package sections | Existing markdown | No | Pending |
| Mistake I caught... | Rejected render frame vs script table | Existing v2 frame + package | No | Pending |
| Every sentence needs receipt... | Keep/cut checklist | Local text graphic | No | Pending |
| Without leaked clips... | Compliance cards | Existing compliance checklist | No | Pending |
| Comment JARVIS... | CTA card | Local text graphic | No | Pending |

## What this changes about production

The next render should be mostly:

- screen-recording style proof cards;
- zooms into the `.aiwg` package;
- simple diagrams;
- one or two short clips from the existing render only as examples of "vibe";
- no new generated cinematic scene work.

This is cheaper, more relevant, and better aligned with the CTA.

## New acceptance criteria for script approval

A script is approved only when:

- [ ] hook is specific and repayable;
- [ ] every body beat has a visual receipt;
- [ ] CTA matches the demonstrated value;
- [ ] compliance claims are explicit and non-defensive;
- [ ] no fake automation, fake insider, fake gameplay, fake revenue, or fake scarcity claims;
- [ ] shot list can be executed without paid generation unless separately approved.

## Human approval question

Do you want EP001 to pivot to this proof-led workflow script?

Recommended response:

- `approve script reset`
- `revise script reset: <notes>`

Approving this does **not** approve new asset generation or public publishing.
