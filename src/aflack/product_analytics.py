"""Product analytics instrumentation for the content pipeline.

Tracks key product events (content generated, published, analytics captured)
and provides hooks for exporting to external analytics platforms (PostHog,
Amplitude, Mixpanel). Events are stored locally in the metrics_store table
and can be forwarded to external services.
"""

from __future__ import annotations

import json
from typing import Any

from .db import connect

PRODUCT_EVENTS = {
    "content_generated": "A creative was generated (Higgsfield or other)",
    "content_published": "Content was published to a platform",
    "analytics_captured": "Analytics snapshot was recorded",
    "compliance_checked": "Compliance gate was evaluated",
    "insight_distilled": "A new insight was created or reinforced",
    "proposal_created": "An improvement proposal was filed",
    "daemon_cycle_completed": "An improvement daemon cycle finished",
    "cost_recorded": "A cost was recorded in the ledger",
}


def track_event(event_name: str, *, properties: dict[str, Any] | None = None, user_id: str = "system") -> None:
    """Track a product event with properties.

    Events are stored in the metrics_store table and can be exported
    to external analytics platforms via the export_events function.
    """
    if event_name not in PRODUCT_EVENTS:
        raise ValueError(f"Unknown product event: {event_name}")

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO metrics_store (name, value, tags, recorded_at)
            VALUES (%s, 1, %s::jsonb, now())
            """,
            (f"product_{event_name}", json.dumps({"user_id": user_id, "properties": properties or {}})),
        )
        conn.commit()


def export_events(event_name: str | None = None, limit: int = 1000) -> list[dict[str, Any]]:
    """Export product events for forwarding to external analytics platforms."""
    query = """
        SELECT name, value, tags, recorded_at
        FROM metrics_store
        WHERE name LIKE 'product_%'
    """
    params: list[Any] = []
    if event_name:
        query += " AND name = %s"
        params.append(f"product_{event_name}")
    query += " ORDER BY recorded_at DESC LIMIT %s"
    params.append(limit)

    with connect() as conn, conn.cursor() as cur:
        cur.execute(query, params)
        return [
            {
                "event": row[0].replace("product_", ""),
                "value": float(row[1]),
                "properties": row[2] if isinstance(row[2], dict) else json.loads(row[2] or "{}"),
                "timestamp": row[3].isoformat() if row[3] else None,
            }
            for row in cur.fetchall()
        ]


def product_funnel_summary() -> dict[str, int]:
    """Return a summary of product funnel events."""
    summary: dict[str, int] = {}
    for event in PRODUCT_EVENTS:
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM metrics_store WHERE name = %s",
                (f"product_{event}",),
            )
            row = cur.fetchone()
        summary[event] = int(row[0]) if row else 0
    return summary
