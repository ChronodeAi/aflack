# ADR-0004: Use Claude Code CLI (`claude-fable-5`) as the video director runtime

**Status**: Accepted
**Date**: 2026-07-04

## Context

The project needs a "director" for videos: an agentic role that reads niche research, official reference packs, persona briefs, compliance rules, benchmark gold sets, and produces/coordinates shot direction, scripts, generation prompts, and quality review.

The user wants this director to run from a **Claude Code CLI session inside this project**, not as an opaque hosted model call embedded in the app.

## Decision

Use the local `claude` CLI from this repository as the video director runtime:

```bash
claude --model claude-fable-5 --effort high --name gta6-director
```

The Claude CLI help confirms `--model` accepts aliases (`fable`, `opus`, `sonnet`) or a full model name such as `claude-fable-5`.

## Role

The director session is responsible for:

- reading `.aiwg/` project context and ADRs,
- enforcing GTA6 footage/compliance rules,
- turning official trailer references into ORIGINAL content plans,
- assigning persona lanes (Vice Signal, Lore Vault, Patch Notes, Rng Goblin, Loadout Lab),
- writing scripts/shot lists/generation prompts,
- coordinating Higgsfield runs through approved wrappers,
- feeding publish-ready metadata into the Postiz queue only after compliance passes,
- capturing lessons back into the local memory/event store.

## Constraints

- Runs from the project root (`/Users/ace/aflack`) so it inherits AIWG context, agentmemory, Aside, Firecrawl, and Postiz integration.
- Must not directly publish public content; it hands off to the compliance gate + Postiz.
- Must not download/remix/reupload Rockstar footage or same-seed regenerate from official/pre-release video.
- Output must be recorded in the event store and economics ledger when it spends credits/tokens.

## Future frameworkization

When this project graduates into an AIWG framework, the director becomes a framework agent/daemon role:

- `video-director`
- `creative-producer`
- `compliance-gatekeeper`
- `performance-memory-curator`

The CLI invocation remains the runtime bridge for local/operator-controlled sessions.
