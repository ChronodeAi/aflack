# Vice Signal EP001 — Analytics Capture Status

**Date**: 2026-07-07  
**Status**: DEFERRED / NO ANALYTICS CAPTURED

## Reason

Analytics capture requires either a public publish event or an explicitly
approved private-test signal. Neither has occurred in this execution. Capturing
synthetic or zero-result analytics as if it represented market performance would
pollute the ROI gate.

## DB-backed command results

```text
uv run aflack analytics-status
snapshots=0
total_views=0
total_likes=0
total_comments=0
total_shares=0
total_saves=0
total_clicks=0
total_conversions=0
total_revenue=0

uv run aflack economics-status
total_cost=0
revenue=0
contribution_margin=0
generated_creatives=0
cost_per_generated=None

uv run aflack roi-scale-gate
scale_allowed=False
reason=blocked: ROI unmeasured; no analytics snapshots captured
snapshots=0
conversions=0
revenue=0
total_cost=0
contribution_margin=0
min_conversions=1
min_margin=0
```

## Next valid analytics action

After final-render approval and a separately approved public publish/private
signal, run either Postiz analytics ingestion or manual analytics capture, then
rerun economics and ROI gates.
