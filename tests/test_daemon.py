from __future__ import annotations

import unittest
from contextlib import contextmanager
from datetime import UTC, datetime
from unittest.mock import patch

from aflack.daemon import BLOCKED_DAEMON_ACTIONS, get_daemon_status


class FakeCursor:
    def __init__(self, responses):
        self.responses = list(responses)
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchone(self):
        return self.responses.pop(0)


class FakeConnection:
    def __init__(self, responses):
        self._cursor = FakeCursor(responses)

    def cursor(self):
        return self._cursor


class DaemonStatusTests(unittest.TestCase):
    def test_get_daemon_status_reports_latest_run_and_counts(self):
        started = datetime(2026, 7, 4, 22, 0, tzinfo=UTC)
        finished = datetime(2026, 7, 4, 22, 1, tzinfo=UTC)
        responses = [
            (
                7,
                "improvement-daemon",
                "improve-abc123",
                "succeeded",
                started,
                finished,
                "scanned=1 distilled=2 reinforced=3 proposed=0",
                {"scanned": 1, "distilled": 2},
                None,
            ),
            (12,),
            (0,),
            (5,),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(responses)

        with patch("aflack.daemon.connect", fake_connect):
            status = get_daemon_status()

        self.assertEqual(status.daemon, "improvement-daemon")
        self.assertEqual(status.latest_run["id"], 7)
        self.assertEqual(status.latest_run["status"], "succeeded")
        self.assertEqual(status.latest_run["started_at"], started.isoformat())
        self.assertEqual(status.active_insights, 12)
        self.assertEqual(status.open_proposals, 0)
        self.assertEqual(status.recent_events, 5)
        self.assertEqual(status.blocked_actions, BLOCKED_DAEMON_ACTIONS)

    def test_get_daemon_status_handles_never_run(self):
        responses = [
            None,
            (0,),
            (0,),
            (0,),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(responses)

        with patch("aflack.daemon.connect", fake_connect):
            status = get_daemon_status()

        self.assertIsNone(status.latest_run)
        self.assertEqual(status.active_insights, 0)
        self.assertEqual(status.open_proposals, 0)
        self.assertEqual(status.recent_events, 0)


if __name__ == "__main__":
    unittest.main()
