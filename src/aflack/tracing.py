"""Full-trace event capture ("every bullet tracer").

Every pipeline stage, daemon tick, and agent input/output is appended to
`pipeline_events`. This is the raw substrate the learning loop consumes.
"""

from __future__ import annotations

import json
import secrets
from dataclasses import dataclass
from typing import Any

from .db import connect, fetchone_required


def new_trace_id(prefix: str = "trace") -> str:
    """Generate a correlation id for one end-to-end run."""

    return f"{prefix}-{secrets.token_hex(6)}"


@dataclass(frozen=True)
class Event:
    trace_id: str
    stage: str
    actor: str
    event_type: str
    payload: dict[str, Any]


def record_event(
    trace_id: str,
    stage: str,
    actor: str,
    event_type: str,
    payload: dict[str, Any] | None = None,
    *,
    ref_type: str | None = None,
    ref_id: int | None = None,
) -> int:
    """Append one pipeline event and return its id."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO pipeline_events (trace_id, stage, actor, event_type, payload, ref_type, ref_id)
            VALUES (%s, %s, %s, %s, %s::jsonb, %s, %s)
            RETURNING id
            """,
            (trace_id, stage, actor, event_type, json.dumps(payload or {}), ref_type, ref_id),
        )
        event_id = fetchone_required(cur)[0]
        conn.commit()
        return int(event_id)


def trace_events(trace_id: str) -> list[dict[str, Any]]:
    """Return all events for a trace in order (for replay/audit)."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, stage, actor, event_type, payload, created_at
            FROM pipeline_events
            WHERE trace_id = %s
            ORDER BY id ASC
            """,
            (trace_id,),
        )
        rows = cur.fetchall()
    return [
        {
            "id": r[0],
            "stage": r[1],
            "actor": r[2],
            "event_type": r[3],
            "payload": r[4],
            "created_at": r[5].isoformat() if r[5] else None,
        }
        for r in rows
    ]
