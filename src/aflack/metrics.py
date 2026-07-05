"""Metrics collection for engineering telemetry.

Provides a lightweight metrics interface for counting events, timing operations,
and recording gauges. Metrics are persisted to the pipeline_events table and
can be exported to external monitoring systems.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from .db import connect


def increment(name: str, *, value: int = 1, tags: dict[str, Any] | None = None) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO metrics_store (name, value, tags, recorded_at)
            VALUES (%s, %s, %s::jsonb, now())
            """,
            (name, value, _tags_to_json(tags)),
        )
        conn.commit()


def gauge(name: str, value: float, *, tags: dict[str, Any] | None = None) -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO metrics_store (name, value, tags, recorded_at)
            VALUES (%s, %s, %s::jsonb, now())
            """,
            (name, value, _tags_to_json(tags)),
        )
        conn.commit()


@contextmanager
def timing(name: str, *, tags: dict[str, Any] | None = None) -> Iterator[None]:
    start = time.monotonic()
    yield
    duration_ms = (time.monotonic() - start) * 1000
    all_tags = tags or {}
    all_tags["unit"] = "ms"
    increment(f"{name}_duration_ms", value=int(duration_ms), tags=all_tags)


def _tags_to_json(tags: dict[str, Any] | None) -> str:
    import json

    return json.dumps(tags or {})


def summary(name: str, limit: int = 100) -> dict[str, Any]:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT name, COUNT(*), SUM(value), AVG(value), MIN(value), MAX(value)
            FROM metrics_store
            WHERE name = %s
            GROUP BY name
            """,
            (name,),
        )
        row = cur.fetchone()
    if not row:
        return {"name": name, "count": 0}
    return {
        "name": row[0],
        "count": int(row[1]),
        "sum": float(row[2]) if row[2] is not None else 0,
        "avg": float(row[3]) if row[3] is not None else 0,
        "min": float(row[4]) if row[4] is not None else 0,
        "max": float(row[5]) if row[5] is not None else 0,
    }
