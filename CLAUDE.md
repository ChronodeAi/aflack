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
