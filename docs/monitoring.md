# Monitoring and Observability

## Overview

The aflack pipeline provides observability through structured logging, distributed
tracing, metrics collection, and error tracking. This document describes where to
check deployment impact and system health.

## Telemetry Sources

### Structured Logging
- **Module**: `src/aflack/logging.py` (structlog with JSON output)
- **Log scrubbing**: Sensitive fields (API keys, passwords, tokens) are automatically redacted
- **Configure**: `from aflack.logging import configure_logging, get_logger`

### Distributed Tracing
- **Module**: `src/aflack/tracing.py`
- **CLI**: `aflack trace-show <trace_id>` to replay full event traces
- **Storage**: `pipeline_events` table in Postgres
- Every pipeline run gets a unique `trace_id` propagated through all stages

### Metrics Collection
- **Module**: `src/aflack/metrics.py`
- **Storage**: `metrics_store` table in Postgres
- Counters, gauges, and timing measurements
- Query with `aflack` CLI or direct SQL

### Error Tracking
- **Module**: `src/aflack/error_tracking.py`
- **Breadcrumbs**: Add context before errors occur
- **Stack traces**: Full traceback captured with each exception
- **CLI**: Errors visible in `pipeline_events` table

## Deployment Impact

After deploying changes:
1. Run `aflack daemon-status` to verify daemon health
2. Check `aflack analytics-status` for traffic anomalies
3. Review `aflack economics-status` for cost/revenue impact
4. Query `metrics_store` for performance regressions
5. Check `pipeline_events` for new errors

## Alerting

Alerts are generated when:
- Daemon run status is `failed`
- Cost ledger exceeds daily caps (configured in `.env`)
- Compliance gate blocks content
- Postiz API returns errors

Monitor these by checking:
```bash
aflack daemon-status
aflack economics-status
aflack proposals-list
```

## Build Performance Tracking

Build duration is measured on every CI run using
`scripts/track_build_performance.py`. The script times each build step
(dependency install, compile, lint, format, typecheck, tests) and writes
a markdown summary table to the GitHub Actions step summary.

- **CI integration**: CI and Deploy Staging workflows both run the tracker
- **Local usage**: `python scripts/track_build_performance.py [--json report.json]`
- **Cache**: uv cache is enabled in CI (`enable-cache: true`) for incremental builds
- **Output**: Markdown table in GitHub Actions summary, optional JSON report file

### Reading Build Metrics

In GitHub Actions, check the job summary for the "Build Performance Report"
table showing per-step durations and pass/fail status. Trends over time can
be observed by comparing summaries across workflow runs.

## Feature Flag Health

Feature flags are checked for dead and stale references on every CI run
using `scripts/detect_dead_flags.py`. The script:

1. Scans source code for `is_enabled()`, `get_flag()`, and `set_flag()` calls
2. Compares against flags defined in the database (or SQL migrations)
3. Reports dead flags (defined but unreferenced), stale flags (disabled and
   unchanged for 30+ days), and orphaned references (used but undefined)

### Flag Lifecycle

1. **Create**: `set_flag("my_flag", enabled=False, rollout_percentage=0, description="...")`
2. **Roll out**: Increase `rollout_percentage` gradually (0 to 100)
3. **Monitor**: Check analytics and error tracking during rollout
4. **Clean up**: Once at 100% and stable, remove code references and delete the flag
5. **Detect dead flags**: CI runs `detect_dead_flags.py` to catch unreferenced flags

## Profiling

For performance profiling of generation or pipeline operations:
```bash
python -m cProfile -o profile.out -m aflack.cli improve-cycle
python -m pstats profile.out
```

The `aflack metrics timing()` context manager can be used to measure
operation durations in code.
