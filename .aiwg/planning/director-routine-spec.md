# Director Routine Spec — Lean Jarvis-Style Content Loop

**Created**: 2026-07-04
**Runtime**: Claude Code CLI `claude-fable-5`
**Scope**: one director, one operator, two active personas (Vice Signal + Loadout Lab)

## Principle

Do not create a 9-agent org chart. The director performs the roles sequentially and writes structured rows to the event store. Humans approve publish/DM/spend. Only automate proven steps.

## Weekly routine

1. Refresh official/reference sources and benchmark examples.
2. Append 25-50 candidate hooks/briefs into the event store.
3. Pick 3-5 candidates for the next batch based on:
   - funnel match (JARVIS or LOADOUT),
   - production difficulty,
   - compliance risk,
   - expected YouTube funnel value.
4. Mark selected rows `draft`.

## Daily routine

1. Read open `draft` hooks/scripts.
2. For each active persona:
   - Vice Signal: attention/news/Shorts concept.
   - Loadout Lab: affiliate/gear/monetization concept.
3. Produce:
   - hook,
   - script,
   - Higgsfield prompt,
   - visual direction,
   - CTA keyword,
   - pinned comment/description text,
   - compliance checklist.
4. Queue to `publish_queue` as draft/needs_auth.
5. Stop before paid generation or public publish unless operator approves.

## V1 funnel mapping

| Keyword | Persona | Platform mode | Lead magnet |
|---|---|---|---|
| JARVIS | Vice Signal | YouTube pinned comment + description | GTA6 AI Content Workflow |
| LOADOUT | Loadout Lab | YouTube pinned comment + description | GTA6 Loadout Checklist |

## Scale gate

Do not scale to 20/day until a hook→CTA→lead-magnet→conversion loop is positive. Volume without funnel proof burns credits.
