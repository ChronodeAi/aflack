"""Thin, swappable memory interface.

Week-1 implementation stores episodic/semantic/procedural lessons in Postgres
and relies on pgGraph relationships over the event model. Vector retrieval can
be added by populating the `embedding` columns (pgvector is installed).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Literal

from .db import connect

MemoryScope = Literal["episodic", "semantic", "procedural"]


@dataclass(frozen=True)
class Lesson:
    id: int
    scope: MemoryScope
    content: str


class MemoryStore:
    """Minimal memory API; keep callers decoupled from the backing engine."""

    def capture_lesson(self, scope: MemoryScope, content: str, links: list[dict] | None = None) -> int:
        """Persist a distilled lesson and return its id."""

        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO lessons (scope, content, links)
                VALUES (%s, %s, %s::jsonb)
                RETURNING id
                """,
                (scope, content, links or []),
            )
            lesson_id = cur.fetchone()[0]
            conn.commit()
            return int(lesson_id)

    def recent_lessons(self, scope: MemoryScope | None = None, limit: int = 10) -> list[Lesson]:
        """Return recent lessons, optionally filtered by memory scope."""

        where = "WHERE scope = %s" if scope else ""
        params = (scope, limit) if scope else (limit,)
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT id, scope, content
                FROM lessons
                {where}
                ORDER BY created_at DESC
                LIMIT %s
                """,
                params,
            )
            return [Lesson(id=row[0], scope=row[1], content=row[2]) for row in cur.fetchall()]


@dataclass(frozen=True)
class ConsolidationResult:
    scanned: int
    created: int
    skipped_existing: int
    lesson_ids: list[int]


def consolidate_insights_to_lessons(
    *,
    min_confidence: float = 0.6,
    limit: int = 20,
    scope: MemoryScope = "procedural",
) -> ConsolidationResult:
    """Promote high-confidence active insights into durable lessons.

    This is intentionally conservative: it deduplicates by exact lesson content
    and keeps source insight IDs in links so the lesson remains traceable.
    """

    lesson_ids: list[int] = []
    scanned = 0
    skipped = 0

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, scope, statement, confidence, support_count
            FROM insights
            WHERE status = 'active'
              AND confidence >= %s
            ORDER BY confidence DESC, support_count DESC, updated_at DESC, id DESC
            LIMIT %s
            """,
            (min_confidence, limit),
        )
        insights = cur.fetchall()
        scanned = len(insights)

        for insight_id, insight_scope, statement, confidence, support_count in insights:
            content = f"{insight_scope}: {statement}"
            cur.execute(
                """
                SELECT id
                FROM lessons
                WHERE scope = %s AND content = %s AND invalid_at IS NULL
                LIMIT 1
                """,
                (scope, content),
            )
            existing = cur.fetchone()
            if existing:
                skipped += 1
                continue

            links = [
                {
                    "type": "insight",
                    "id": int(insight_id),
                    "scope": insight_scope,
                    "confidence": float(confidence),
                    "support_count": int(support_count),
                }
            ]
            cur.execute(
                """
                INSERT INTO lessons (scope, content, links)
                VALUES (%s, %s, %s::jsonb)
                RETURNING id
                """,
                (scope, content, json.dumps(links)),
            )
            lesson_ids.append(int(cur.fetchone()[0]))

        conn.commit()

    return ConsolidationResult(
        scanned=scanned,
        created=len(lesson_ids),
        skipped_existing=skipped,
        lesson_ids=lesson_ids,
    )
