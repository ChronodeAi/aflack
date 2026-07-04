from __future__ import annotations

import json
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from aflack.memory import consolidate_insights_to_lessons


class FakeCursor:
    def __init__(self, insights, existing_by_content):
        self.insights = list(insights)
        self.existing_by_content = existing_by_content
        self.inserted = []
        self._last = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        if "FROM insights" in sql:
            self._last = "insights"
            return
        if "FROM lessons" in sql:
            self._last = ("existing", params[1])
            return
        if "INSERT INTO lessons" in sql:
            lesson_id = 100 + len(self.inserted)
            self.inserted.append((lesson_id, params))
            self._last = ("insert", lesson_id)
            return
        raise AssertionError(f"unexpected SQL: {sql}")

    def fetchall(self):
        if self._last == "insights":
            return self.insights
        raise AssertionError("fetchall called after unexpected query")

    def fetchone(self):
        if isinstance(self._last, tuple) and self._last[0] == "existing":
            content = self._last[1]
            existing_id = self.existing_by_content.get(content)
            return (existing_id,) if existing_id else None
        if isinstance(self._last, tuple) and self._last[0] == "insert":
            return (self._last[1],)
        raise AssertionError("fetchone called after unexpected query")


class FakeConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


class MemoryConsolidationTests(unittest.TestCase):
    def test_consolidates_active_insights_into_traceable_lessons(self):
        insights = [
            (1, "hook", "Open with a concrete claim.", 0.8, 3),
            (2, "cta", "Use one keyword CTA.", 0.7, 2),
        ]
        cursor = FakeCursor(insights, {})
        conn = FakeConnection(cursor)

        @contextmanager
        def fake_connect():
            yield conn

        with patch("aflack.memory.connect", fake_connect):
            result = consolidate_insights_to_lessons(min_confidence=0.6, limit=5)

        self.assertEqual(result.scanned, 2)
        self.assertEqual(result.created, 2)
        self.assertEqual(result.skipped_existing, 0)
        self.assertEqual(result.lesson_ids, [100, 101])
        self.assertTrue(conn.committed)
        _, first_params = cursor.inserted[0]
        self.assertEqual(first_params[0], "procedural")
        self.assertEqual(first_params[1], "hook: Open with a concrete claim.")
        self.assertEqual(json.loads(first_params[2])[0]["id"], 1)

    def test_skips_existing_lesson_content(self):
        content = "hook: Open with a concrete claim."
        insights = [(1, "hook", "Open with a concrete claim.", 0.8, 3)]
        cursor = FakeCursor(insights, {content: 42})
        conn = FakeConnection(cursor)

        @contextmanager
        def fake_connect():
            yield conn

        with patch("aflack.memory.connect", fake_connect):
            result = consolidate_insights_to_lessons(min_confidence=0.6, limit=5)

        self.assertEqual(result.scanned, 1)
        self.assertEqual(result.created, 0)
        self.assertEqual(result.skipped_existing, 1)
        self.assertEqual(result.lesson_ids, [])
        self.assertEqual(cursor.inserted, [])


if __name__ == "__main__":
    unittest.main()
