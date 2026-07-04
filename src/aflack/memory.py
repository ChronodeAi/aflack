"""Thin, swappable memory interface.

Week-1 implementation stores episodic/semantic/procedural lessons in Postgres
and relies on pgGraph relationships over the event model. Vector retrieval can
be added by populating the `embedding` columns (pgvector is installed).
"""

from __future__ import annotations

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

