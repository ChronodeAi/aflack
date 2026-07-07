from __future__ import annotations

import json
import unittest
from contextlib import contextmanager
from datetime import UTC, datetime
from unittest.mock import patch

from aflack.product_analytics import (
    PRODUCT_EVENTS,
    export_events,
    product_funnel_summary,
    track_event,
)


class FakeCursor:
    def __init__(self, *, fetchall_rows=None, fetchone_row=None):
        self._fetchall_rows = fetchall_rows or []
        self._fetchone_row = fetchone_row
        self.executed = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed = sql
        self.params = params

    def fetchall(self):
        return self._fetchall_rows

    def fetchone(self):
        return self._fetchone_row


class FakeConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


def _fake_connect(conn):
    @contextmanager
    def _cm():
        yield conn

    return _cm


class TrackEventTests(unittest.TestCase):
    def test_unknown_event_raises(self):
        with self.assertRaises(ValueError):
            track_event("not_a_real_event")

    def test_known_event_inserts_and_commits(self):
        conn = FakeConnection(FakeCursor())
        with patch("aflack.product_analytics.connect", _fake_connect(conn)):
            track_event("content_generated", properties={"credits": 360}, user_id="system")

        self.assertTrue(conn.committed)
        self.assertIn("INSERT INTO metrics_store", conn.cursor_obj.executed)
        self.assertEqual(conn.cursor_obj.params[0], "product_content_generated")
        tags = json.loads(conn.cursor_obj.params[1])
        self.assertEqual(tags["user_id"], "system")
        self.assertEqual(tags["properties"], {"credits": 360})


class ExportEventsTests(unittest.TestCase):
    def test_export_maps_rows(self):
        ts = datetime(2026, 7, 4, 22, 3, tzinfo=UTC)
        rows = [("product_content_published", 1, {"user_id": "system"}, ts)]
        conn = FakeConnection(FakeCursor(fetchall_rows=rows))
        with patch("aflack.product_analytics.connect", _fake_connect(conn)):
            events = export_events()

        self.assertEqual(events[0]["event"], "content_published")
        self.assertEqual(events[0]["value"], 1.0)
        self.assertEqual(events[0]["properties"], {"user_id": "system"})
        self.assertEqual(events[0]["timestamp"], "2026-07-04T22:03:00+00:00")
        # No event filter -> no name filter clause params beyond the limit.
        self.assertEqual(conn.cursor_obj.params, [1000])

    def test_export_with_event_filter_adds_name_param(self):
        conn = FakeConnection(FakeCursor(fetchall_rows=[]))
        with patch("aflack.product_analytics.connect", _fake_connect(conn)):
            export_events(event_name="cost_recorded", limit=50)

        self.assertIn("product_cost_recorded", conn.cursor_obj.params)
        self.assertIn(50, conn.cursor_obj.params)

    def test_export_parses_string_tags(self):
        rows = [("product_cost_recorded", 2, '{"user_id": "system"}', None)]
        conn = FakeConnection(FakeCursor(fetchall_rows=rows))
        with patch("aflack.product_analytics.connect", _fake_connect(conn)):
            events = export_events()

        self.assertEqual(events[0]["properties"], {"user_id": "system"})
        self.assertIsNone(events[0]["timestamp"])


class FunnelSummaryTests(unittest.TestCase):
    def test_summary_counts_each_event(self):
        # connect() is invoked once per known event; return a fixed count each time.
        conn = FakeConnection(FakeCursor(fetchone_row=(3,)))
        with patch("aflack.product_analytics.connect", _fake_connect(conn)):
            summary = product_funnel_summary()

        self.assertEqual(set(summary.keys()), set(PRODUCT_EVENTS.keys()))
        for count in summary.values():
            self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()
