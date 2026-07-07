# Director Routine Spec — Lean Jarvis-Style Content Loop

**Created**: 2026-07-04
**Runtime**: Claude Code CLI `claude-fable-5`
**Scope**: one director, one operator, two active personas available (Vice Signal + Loadout Lab), persona-free formats allowed

## Principle

Do not create a 9-agent org chart. The director performs the ADR-0005 roles sequentially and writes structured rows to the event store. Humans approve publish/DM/spend/account actions. Only automate proven steps, and follow ADR-0006 when a persona-free format has stronger virality evidence than a persona wrapper.

## Weekly routine

1. Refresh official/reference sources and benchmark examples.
2. Append 25-50 candidate hooks/briefs into the event store.
3. Pick 3-5 candidates for the next batch based on:
   - trend size and speed-to-publish,
   - expected shares/retention,
   - funnel match (JARVIS or LOADOUT),
   - production difficulty,
   - compliance risk,
   - expected YouTube funnel value.
4. Mark selected rows `draft`.

## Daily routine

1. Read open `draft` hooks/scripts.
2. Choose the strongest format:
   - Vice Signal: attention/news/Shorts concept.
   - Loadout Lab: affiliate/gear/monetization concept.
   - Persona-free: trend, meme, explainer, benchmark imitation, or hook pattern that should outperform a persona-led format.
3. Produce:
   - hook,
   - script,
   - Higgsfield prompt,
   - visual direction,
   - CTA keyword,
   - pinned comment/description text,
   - compliance checklist.
4. Queue to `publish_queue` as draft/needs_auth or create a Postiz payload preview.
5. Stop before paid generation or public publish unless operator approves.

## V1 funnel mapping

| Keyword | Persona | Platform mode | Lead magnet |
|---|---|---|---|
| JARVIS | Vice Signal | YouTube pinned comment + description | GTA6 AI Content Workflow |
| LOADOUT | Loadout Lab | YouTube pinned comment + description | GTA6 Loadout Checklist |
| WORKFLOW | Persona-free or Vice Signal | YouTube pinned comment + description | AI Video Automation Prompt Pack |

## Scale gate

Do not scale to 20/day until a hook→CTA→lead-magnet→conversion loop is positive. Volume without funnel proof burns credits.
