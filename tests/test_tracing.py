from __future__ import annotations

import json
import unittest
from contextlib import contextmanager
from datetime import UTC, datetime
from unittest.mock import patch

from aflack.tracing import new_trace_id, record_event, trace_events


class FakeInsertCursor:
    def __init__(self):
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.params = params

    def fetchone(self):
        return (77,)


class FakeInsertConnection:
    def __init__(self):
        self.cursor_obj = FakeInsertCursor()
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


class FakeTraceCursor:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.params = params

    def fetchall(self):
        return [
            (
                1,
                "validate",
                "tester",
                "output",
                {"passed": True},
                datetime(2026, 7, 4, 22, 0, tzinfo=UTC),
            )
        ]


class FakeTraceConnection:
    def cursor(self):
        return FakeTraceCursor()


class TracingTests(unittest.TestCase):
    def test_new_trace_id_uses_prefix(self):
        trace_id = new_trace_id("unit")
        self.assertTrue(trace_id.startswith("unit-"))
        self.assertGreater(len(trace_id), len("unit-"))

    def test_record_event_serializes_payload_and_commits(self):
        conn = FakeInsertConnection()

        @contextmanager
        def fake_connect():
            yield conn

        with patch("aflack.tracing.connect", fake_connect):
            event_id = record_event(
                "trace-1",
                "validate",
                "tester",
                "output",
                {"passed": True},
                ref_type="package",
                ref_id=9,
            )

        self.assertEqual(event_id, 77)
        self.assertTrue(conn.committed)
        params = conn.cursor_obj.params
        self.assertEqual(params[0], "trace-1")
        self.assertEqual(json.loads(params[4]), {"passed": True})
        self.assertEqual(params[5], "package")
        self.assertEqual(params[6], 9)

    def test_trace_events_returns_ordered_dicts_with_iso_dates(self):
        @contextmanager
        def fake_connect():
            yield FakeTraceConnection()

        with patch("aflack.tracing.connect", fake_connect):
            events = trace_events("trace-1")

        self.assertEqual(events[0]["id"], 1)
        self.assertEqual(events[0]["stage"], "validate")
        self.assertEqual(events[0]["payload"], {"passed": True})
        self.assertEqual(events[0]["created_at"], "2026-07-04T22:00:00+00:00")


if __name__ == "__main__":
    unittest.main()
