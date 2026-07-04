<!-- AIWG:claude-md-hook:start -->

# AIWG

@AIWG.md

<!--
  This block is managed by `aiwg regenerate` and `aiwg use`.
  Operator content above and below this block is preserved on regenerate.
  To change AIWG.md content, edit .aiwg/AIWG.md (the normalized source)
  then run `aiwg regenerate`.
-->

<!-- AIWG:claude-md-hook:end -->

<!--
  Operator section below is preserved by `aiwg regenerate` / `aiwg use`.
  Keep AIWG-authored guidance inside the managed block above.
-->

## What this repository is

This is an **AIWG workspace**, not a conventional software project. As of this
writing it contains **no application source code** — only AIWG tooling and empty
framework scaffolds. Do not look for a build system, test suite, or app entry
point; there is none yet. If code is later added, re-run `/init` to regenerate
this file with real build/test/architecture guidance.

- Not a git repository (no `.git`). Delivery policy in `.aiwg/aiwg.config` still
  declares `mode: pr-required`, `default_branch: main`, `require_ci_green: true`,
  `force_push_policy: never` — honor these once a repo exists.
- Provider: `claude` (a `codex` deployment also exists under `.codex/`).
- All AIWG frameworks are installed (`aiwg use all`, v2026.6.11): `sdlc-complete`,
  `research-complete`, `forensics-complete`, `security-engineering`,
  `knowledge-base`, `media-curator`, `media-marketing-kit`, `ops-complete`.

## Layout

- `.aiwg/AIWG.md` — normalized project context (source of truth for the
  generated `AIWG.md`, `AGENTS.md`, and the managed block above). Edit here, then
  run `aiwg regenerate` — never hand-edit the generated bridge files.
- `.aiwg/aiwg.config` — provider, delivery, and parallelism config.
- `.aiwg/frameworks/<name>/` — per-framework artifact directories (currently
  empty skeletons; SDLC artifacts land under `.aiwg/` subdirectories).
- `.aiwg/activity.log` — append-only timeline of AIWG operations on this workspace.
- `.agents/skills/`, `.claude/`, `.codex/` — deployed AIWG skills/agents/rules per provider.
- `.codebase-memory/` — codebase-memory MCP index artifact.

## Working here

- There are no npm/make/pytest commands. The operative surface is the `aiwg` CLI
  and AIWG skills (invoked as `/<skill-name>` or via `aiwg discover "<intent>"`
  then `aiwg show skill <name>`). Prefer skills over raw `aiwg` subcommands for
  actions — see `aiwg-utils-quickref`.
- Parallelism is capped (`.aiwg/aiwg.config`): 4 subagents, 2 ralph loops,
  4 mission-control missions. Take the MIN of this cap and any others when
  fanning out.
- To check workspace state, use the `aiwg-status` skill or read
  `.aiwg/activity.log`.
