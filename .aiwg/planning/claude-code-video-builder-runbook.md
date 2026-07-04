# Claude Code Video Builder Runbook

**Created**: 2026-07-04  
**Purpose**: Use Claude Code as the video director/builder before any Higgsfield generation or Postiz submission.

## Runtime

```bash
claude --model claude-fable-5 --effort high --name gta6-director
```

For bounded non-interactive planning packets:

```bash
claude --model claude-fable-5 --effort high --max-budget-usd 1 -p "$(cat .aiwg/prompts/claude-code/<prompt>.md)"
```

## What Claude Code is allowed to do in this phase

- Read project context.
- Produce video strategy, scripts, shot lists, storyboard beats, editing notes, captions, CTA, and compliance checklists.
- Produce Higgsfield prompt candidates as text only.
- Produce Postiz draft metadata as text only.
- Identify exactly what a human must approve next.

## What Claude Code is not allowed to do without explicit approval

- Run paid Higgsfield generation.
- Download, clip, reupload, same-seed remix, or transform official Rockstar/GTA6 footage.
- Submit to Postiz Cloud.
- Publicly publish or schedule a post.
- Automate comments/DMs.
- Change OAuth/channel/account settings.

## Video package contract

Each Claude Code video builder output must include:

1. Package ID and persona.
2. Platform and format.
3. Hook.
4. Script with timestamps.
5. Shot list / storyboard.
6. Original-visuals-only generation prompt.
7. Editing notes.
8. Title.
9. Description.
10. Pinned comment.
11. CTA keyword and lead magnet.
12. Compliance checklist.
13. Economics/spend gate.
14. Next human decision.

## Current first package

- Package: `VS-EP001`
- Persona: `Vice Signal`
- Platform: YouTube Shorts
- CTA keyword: `JARVIS`
- Lead magnet: `GTA6 AI Content Workflow`
- Constraint: no Rockstar footage, no same-seed regeneration, no public publish.
