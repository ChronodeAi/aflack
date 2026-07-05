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

## Profiling

For performance profiling of generation or pipeline operations:
```bash
python -m cProfile -o profile.out -m aflack.cli improve-cycle
python -m pstats profile.out
```

The `aflack metrics timing()` context manager can be used to measure
operation durations in code.
