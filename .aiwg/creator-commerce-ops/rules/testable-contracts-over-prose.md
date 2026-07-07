# Testable Contracts over Prose

**Status**: active  
**Applies to**: skills, rules, workflows, agents, daemon behaviors, content package generators, and validation gates

## Rule

Agentic instructions must be written as testable contracts whenever the behavior affects pipeline quality, safety, money, public publishing, or memory promotion. Markdown guidance can explain intent, but the enforcing boundary should be a deterministic check the agent can run and repair against.

## Required Pattern

Every new or materially changed skill, rule, workflow, agent, or daemon behavior must include one of:

- an executable test command,
- a schema validation command,
- a smoke command,
- a deterministic checklist with pass/fail conditions,
- a named construction task explaining why the check cannot exist yet.

If an artifact has no deterministic check, it cannot be used as an autonomous daemon gate or high-risk enforcement boundary.

## Smith-First Authoring

Before hand-authoring a reusable skill or agent:

1. Run `aiwg discover "<capability>"`.
2. Inspect the selected result with `aiwg show <type> <name>`.
3. Reuse an existing artifact when the semantic match is strong.
4. Use SkillSmith for new trigger-based skills.
5. Use AgentSmith for new specialist agents.

Rules remain project-local authored artifacts in this workspace unless a canonical AIWG RuleSmith/scaffold route is discovered.

## Acceptance Checks

Before construction handoff or proposal application, verify:

- new framework artifacts name their validation path,
- daemon changes preserve human-gated blocked actions,
- generated content packages pass compliance smoke checks before publishing,
- AIWG index rebuild succeeds after artifact changes,
- tests or smoke checks are recorded in the relevant report or handoff.

