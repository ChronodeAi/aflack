from __future__ import annotations

import json
import unittest
from contextlib import contextmanager
from unittest.mock import patch

from aflack import metrics
from aflack.metrics import _tags_to_json, gauge, increment, summary, timing


class FakeCursor:
    def __init__(self, row=None):
        self._row = row
        self.executed = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed = sql
        self.params = params

    def fetchone(self):
        return self._row


class FakeConnection:
    def __init__(self, row=None):
        self.cursor_obj = FakeCursor(row)
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


class TagsToJsonTests(unittest.TestCase):
    def test_none_becomes_empty_object(self):
        self.assertEqual(json.loads(_tags_to_json(None)), {})

    def test_dict_serialized(self):
        self.assertEqual(json.loads(_tags_to_json({"stage": "publish"})), {"stage": "publish"})


class IncrementGaugeTests(unittest.TestCase):
    def test_increment_inserts_and_commits(self):
        conn = FakeConnection()
        with patch("aflack.metrics.connect", _fake_connect(conn)):
            increment("publish_attempts", value=2, tags={"platform": "youtube"})

        self.assertTrue(conn.committed)
        self.assertIn("INSERT INTO metrics_store", conn.cursor_obj.executed)
        self.assertEqual(conn.cursor_obj.params[0], "publish_attempts")
        self.assertEqual(conn.cursor_obj.params[1], 2)
        self.assertEqual(json.loads(conn.cursor_obj.params[2]), {"platform": "youtube"})

    def test_gauge_inserts_and_commits(self):
        conn = FakeConnection()
        with patch("aflack.metrics.connect", _fake_connect(conn)):
            gauge("queue_depth", 5.0)

        self.assertTrue(conn.committed)
        self.assertEqual(conn.cursor_obj.params[0], "queue_depth")
        self.assertEqual(conn.cursor_obj.params[1], 5.0)


class TimingTests(unittest.TestCase):
    def test_timing_emits_duration_metric(self):
        captured = {}

        def fake_increment(name, *, value=1, tags=None):
            captured["name"] = name
            captured["value"] = value
            captured["tags"] = tags

        with patch.object(metrics, "increment", fake_increment):
            with timing("render", tags={"stage": "assemble"}):
                pass

        self.assertEqual(captured["name"], "render_duration_ms")
        self.assertGreaterEqual(captured["value"], 0)
        self.assertEqual(captured["tags"]["unit"], "ms")
        self.assertEqual(captured["tags"]["stage"], "assemble")


class SummaryTests(unittest.TestCase):
    def test_summary_no_rows_returns_zero_count(self):
        conn = FakeConnection(row=None)
        with patch("aflack.metrics.connect", _fake_connect(conn)):
            result = summary("unknown_metric")

        self.assertEqual(result, {"name": "unknown_metric", "count": 0})

    def test_summary_aggregates_row(self):
        row = ("latency", 4, 40, 10.0, 5.0, 20.0)
        conn = FakeConnection(row=row)
        with patch("aflack.metrics.connect", _fake_connect(conn)):
            result = summary("latency")

        self.assertEqual(result["name"], "latency")
        self.assertEqual(result["count"], 4)
        self.assertEqual(result["sum"], 40.0)
        self.assertEqual(result["avg"], 10.0)
        self.assertEqual(result["min"], 5.0)
        self.assertEqual(result["max"], 20.0)


if __name__ == "__main__":
    unittest.main()
