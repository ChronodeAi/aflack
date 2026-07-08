# aflack

Local affiliate content pipeline: research, generate, validate, publish, learn.

A content-factory control plane for affiliate video content. It manages the full
lifecycle from niche research through compliant generation, Postiz publishing,
analytics capture, economics tracking, and autonomous improvement loops.

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (dependency management)
- Docker (for local Postgres with pgGraph + pgvector)

## Quick Start

```bash
# Install dependencies
uv sync

# Copy environment template and fill in secrets
cp .env.example .env

# Start local Postgres (pgGraph + pgvector + pg_cron)
docker build -t aflack/pggraph-pgvector:0.1.8-pgvector0.8.4 docker/pggraph-pgvector
docker volume create aflack_pggraph_data
docker run -d --name pggraph \
  -e POSTGRES_PASSWORD=postgres \
  -p 127.0.0.1:55432:5432 \
  -v aflack_pggraph_data:/var/lib/postgresql/data \
  aflack/pggraph-pgvector:0.1.8-pgvector0.8.4

# Apply database migrations
aflack migrate

# Seed a smoke-test graph
aflack seed-smoke

# Run compliance checks
aflack compliance-smoke
```

## Development

```bash
# Lint
ruff check src tests

# Format check
ruff format --check src tests

# Type check
mypy src

# Run tests
python -m unittest discover -s tests -v

# Compile check
python -m compileall -q src
```

## Project Structure

```
src/aflack/        Python package (CLI, DB, analytics, publishing, learning, daemon)
db/migrations/     SQL migrations (init, publish queue, funnel, learning, analytics)
docker/            Docker image for local Postgres (pgGraph + pgvector)
tests/             Unit tests (unittest)
scripts/           Daemon launch scripts (launchd + cron)
.aiwg/             AIWG workspace artifacts (SDLC, planning, reports)
```

## CLI Commands

Run `aflack --help` for the full list. Key commands:

| Command | Purpose |
|---|---|
| `aflack migrate` | Apply SQL migrations |
| `aflack db-status` | Show database extensions and tables |
| `aflack seed-smoke` | Insert a test Product-Creative-Result graph |
| `aflack compliance-smoke` | Run deterministic compliance checks |
| `aflack economics-status` | Show all-time economics rollup |
| `aflack roi-scale-gate` | Block scale-up unless analytics show positive margin |
| `aflack analytics-status` | Show aggregate analytics |
| `aflack daemon-status` | Show improvement daemon status |
| `aflack insights-list` | List active deduped insights |
| `aflack proposals-list` | List open improvement proposals |
| `aflack trace-show <trace_id>` | Replay a full event trace |

## Safety Gates

The pipeline enforces human gates for: public publishing, paid generation spend,
account/channel changes, comment/DM/follow automation, and ad spend. All
generation and publishing actions require explicit operator approval.

## Observability

- **Structured logging**: `src/aflack/logging.py` (structlog with JSON output and log scrubbing)
- **Distributed tracing**: `aflack trace-show <trace_id>` replays full event traces
- **Metrics collection**: `src/aflack/metrics.py` (counters, gauges, timing)
- **Error tracking**: `src/aflack/error_tracking.py` (breadcrumbs, stack traces, context)
- **Product analytics**: `src/aflack/product_analytics.py` (funnel events, export hooks)
- **Monitoring guide**: `docs/monitoring.md`
- **Incident runbooks**: `docs/runbooks/incident-response.md`

## Profiling

```bash
python -m cProfile -o profile.out -m aflack.cli improve-cycle
python -m pstats profile.out
```

## Dependency Updates

Dependabot is configured for weekly updates. See `docs/dependency-update-policy.md`
for the minimum release age policy (7 days before merge).

## License

Proprietary. All rights reserved.
