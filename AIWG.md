<!-- AIWG:claude-md-hook:start -->
<!-- aiwg-managed -->
<!-- AIWG.md is the CLAUDE.md companion for non-Claude providers; same content. -->

# AIWG


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

An **AIWG workspace** with a working Python application. The `src/aflack/`
package is a local affiliate content pipeline CLI: research, generate,
validate, publish, and learn. It has a Postgres-backed event store (pgGraph +
pgvector), a Postiz publishing path, analytics aggregation, economics tracking,
a learning/insight layer, and an improvement daemon with human safety gates.

- Git repository with `origin` remote: `https://github.com/ChronodeAi/aflack.git`
  Delivery policy in `.aiwg/aiwg.config`: `mode: direct`, `default_branch: main`,
  `force_push_policy: never`.
- Provider: `claude` (a `codex` deployment also exists under `.codex/`).
- All AIWG frameworks are installed (`aiwg use all`): `sdlc-complete`,
  `research-complete`, `forensics-complete`, `security-engineering`,
  `knowledge-base`, `media-curator`, `media-marketing-kit`, `ops-complete`.

## Build and Test Commands

```bash
# Install dependencies (uses uv)
uv sync --extra dev

# Lint
ruff check src tests

# Format check
ruff format --check src tests

# Type check
mypy src

# Run unit tests (39 tests, unittest)
python -m unittest discover -s tests -v

# Compile check
python -m compileall -q src

# Run the CLI
aflack --help
```

## Layout

- `src/aflack/` — Python package: `cli.py`, `db.py`, `config.py`, `analytics.py`,
  `publishing.py`, `compliance.py`, `economics.py`, `learning.py`, `daemon.py`,
  `memory.py`, `tracing.py`, `aside_scan.py`, `prompt_quality.py`.
- `db/migrations/` — SQL migrations (init, publish queue, funnel, learning, analytics).
- `docker/pggraph-pgvector/` — Docker image for local Postgres.
- `tests/` — Unit tests (unittest, 39 tests).
- `scripts/` — Daemon launch scripts (launchd + cron).
- `.aiwg/AIWG.md` — normalized project context (source of truth for the
  generated `AIWG.md`, `AGENTS.md`, and the managed block above). Edit here, then
  run `aiwg regenerate` — never hand-edit the generated bridge files.
- `.aiwg/aiwg.config` — provider, delivery, and parallelism config.
- `.aiwg/activity.log` — append-only timeline of AIWG operations on this workspace.
- `.agents/skills/`, `.claude/`, `.codex/` — deployed AIWG skills/agents/rules per provider.
- `.codebase-memory/` — codebase-memory MCP index artifact.

## Working here

- Build/test/lint commands are listed above. The AIWG CLI and skills are also
  available (invoked as `/<skill-name>` or via `aiwg discover "<intent>"` then
  `aiwg show skill <name>`). Prefer skills over raw `aiwg` subcommands for
  actions — see `aiwg-utils-quickref`.
- Parallelism is capped (`.aiwg/aiwg.config`): 4 subagents, 2 ralph loops,
  4 mission-control missions. Take the MIN of this cap and any others when
  fanning out.
- To check workspace state, use the `aiwg-status` skill or read
  `.aiwg/activity.log`.
- Safety gates: no public publishing, paid generation, account changes, DM/comment
  automation, or ad spend without explicit operator approval.

<!-- AIWG-PARALLELISM-CAP:START -->
## Parallelism Cap

This project caps parallel agent fan-out (#1359):

- **max_parallel_subagents**: 4 (provider default for claude)
- **max_parallel_ralph_loops**: 2 (provider default for claude)
- **max_parallel_mc_missions**: 4 (provider default for claude)

*Rationale*: Provider default for claude — adjust via 'aiwg config set --project parallelism.max_parallel_subagents N'

When spawning parallel subagents, take the MIN of: this cap, `AIWG_CONTEXT_WINDOW` budget, the RLM 7-agent hard cap (RLM dispatches only), and the natural task decomposition. Bump via `aiwg config set --project parallelism.max_parallel_subagents N`.

<!-- AIWG-PARALLELISM-CAP:END -->

<!-- aiwg-context-finalization:START -->
## Context Finalization

This section is synthesized after template emission from the current workspace state. Preserve operator-authored content outside AIWG-managed blocks; rerun `aiwg regenerate` to refresh this section after provider, framework, or MCP wiring changes.

### Workspace Snapshot

- Configured providers: claude
- Installed frameworks/addons: all
- Recorded deployments: claude, codex, factory
- Normalized project context: `.aiwg/AIWG.md`

### Discover-First Protocol

Classify every user turn FIRST: is it a **new directive** or a continuation? When a message names or references an AIWG command/capability — even as pasted content like an `address-issues` tracker table, an issue list, or a `flow-*` name — treat it as a new directive and ACT: run `aiwg discover "<the need>"`, fetch with `aiwg show <type> <name>`, and invoke it. Do NOT ask "what would you like me to do with these?" when the action is implied — a pasted `address-issues #1234` table means run the address-issues workflow on those issues.

Also run `aiwg discover` before declining an AIWG request as out of scope or inventing a workflow from memory. The CLI ranks AIWG capabilities across the installed corpus and rebuilds the index from `$AIWG_ROOT` automatically, so a "no matches" for a command you know is deployed is a bug — not a signal it is absent. Commands AIWG deploys to your provider command directory (`.opencode/command/`, `.claude/commands/`, `~/.codex/prompts/`, …) ARE discoverable this way; fetch them with `aiwg show command <name>`. This prevents decline-without-search failures, ask-instead-of-act on new directives, and hallucinated skill or agent names. Full rule: `agentic/code/addons/aiwg-utils/rules/skill-discovery.md`.

### Engagement Verification

When a user asks whether AIWG is active or engaged in this project, run or read `aiwg status --probe --json` and report the result plainly: engaged state, project root, deployed provider files, installed frameworks/addons, and the next action from the probe. Do not add AIWG attribution, signatures, generated-by text, or passive footers to user files, commits, PRs, comments, code headers, or docs.

### Source Model

- `.aiwg/AIWG.md` is the normalized project-local context entry point.
- Root `AIWG.md` is the generated cross-provider companion loaded through `AGENTS.md` and provider twins.
- `AGENTS.md`, `WARP.md`, `.hermes.md`, and `.github/copilot-instructions.md` are provider-facing bridges, not replacements for `.aiwg/AIWG.md`.
<!-- aiwg-context-finalization:END -->
