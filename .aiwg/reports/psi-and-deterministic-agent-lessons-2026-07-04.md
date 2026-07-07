# PSI and Deterministic Agent Lessons

**Date**: 2026-07-04  
**Status**: Construction input  
**Sources**: Firecrawl scrape of Pocket transcript `Deterministic AI tests for VOD pipeline`; PSI project architecture/runbook docs; AIWG AgentSmith and SkillSmith docs

## Summary

The strongest shared lesson is that agent behavior becomes reliable when prose instructions are backed by deterministic contracts. Skills, rules, workflows, agents, daemon ticks, and content-stage outputs should not rely on markdown guidance alone. Important behavior needs schema checks, smoke commands, acceptance criteria, or test fixtures that the agent must run and repair against.

## Firecrawl transcript lesson

The Pocket transcript described a VOD pipeline where markdown skills alone were not enough to keep AI stages reliable. The useful pattern was:

1. AI completes a pipeline stage.
2. A deterministic test suite runs outside the model.
3. Failures are returned as concrete repair instructions.
4. The AI fixes the artifact.
5. Tests rerun until pass or block.

Project implication: every serious content-factory capability should include a `Deterministic Checks` section. Prose explains intent, but code/tests/contracts enforce the boundary.

## PSI lessons to transfer

PSI's daemon and RBI control-plane docs suggest a stronger runtime shape for this project:

- Keep daemon state explicit: loop definition, state, budget, constraints, and append-only run log.
- Separate operator intent, mission control, daemon execution, provider session, and sandbox state.
- Prevent self-verification for high-risk outputs; route verification to a separate checker or deterministic command.
- Treat budget exhaustion, missing locks, unsafe actions, and failed contract checks as stop conditions.
- Use a canonical artifact envelope so downstream agents consume stable fields instead of scraping prose.

Recommended future layout:

```text
.aiwg/loops/content-factory/
  LOOP.md
  state.yaml
  budget.yaml
  constraints.yaml
  run-log.jsonl
```

## Smithing policy

AIWG Smiths should be the default authoring path for reusable agentic artifacts:

- Use `aiwg discover` / `aiwg show` before creating a new skill or agent.
- Use SkillSmith for reusable trigger-based skills.
- Use AgentSmith for specialist agents.
- No RuleSmith was found in the current AIWG installation, so rules remain project-local artifacts until a canonical rulesmith/scaffold path exists.
- New skills and agents should be generated from the AIWG Smith catalog/definition flow where available instead of hand-rolled from memory.

## Construction actions

- Add @.aiwg/creator-commerce-ops/rules/testable-contracts-over-prose.md requiring deterministic checks for new or changed skills, rules, workflows, agents, and daemon behaviors.
- Update @.aiwg/planning/daemon-runtime-architecture.md with the PSI-style content-factory control plane as a construction backlog item.
- Keep Postgres as the content-pipeline memory system of record while using agentmemory for coding-agent/session recall.
- During construction, convert high-value prompt/rule guidance into executable tests or schemas before enabling autonomous daemon use.
- Carry these constraints into @.aiwg/planning/frameworkization-roadmap.md before any AIWG framework promotion.
