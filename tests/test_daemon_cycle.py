from __future__ import annotations

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from aflack import daemon
from aflack.daemon import (
    BLOCKED_DAEMON_ACTIONS,
    get_daemon_status,
    run_improvement_cycle,
)


class QueueCursor:
    """Cursor returning queued fetchone/fetchall results per execute() call."""

    def __init__(self, *, fetchone_rows=None, fetchall_rows=None, rowcount=1):
        self._fetchone_rows = list(fetchone_rows) if fetchone_rows is not None else []
        self._fetchall_rows = list(fetchall_rows) if fetchall_rows is not None else []
        self.rowcount = rowcount
        self.executed: list[str] = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append(sql)

    def fetchone(self):
        return self._fetchone_rows.pop(0) if self._fetchone_rows else None

    def fetchall(self):
        return self._fetchall_rows.pop(0) if self._fetchall_rows else []


class QueueConn:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


class SequencedConnect:
    """Yields a fresh connection (with a preset cursor) for each `connect()` call.

    run_improvement_cycle opens several independent `connect()` contexts
    (start_run, ingest, candidate_insights, finish_run). Each needs its own
    cursor with the right canned rows.
    """

    def __init__(self, cursors):
        self._cursors = list(cursors)
        self.conns: list[QueueConn] = []

    def __call__(self):
        @contextmanager
        def _cm():
            cur = self._cursors.pop(0) if self._cursors else QueueCursor()
            conn = QueueConn(cur)
            self.conns.append(conn)
            yield conn

        return _cm()


class RunImprovementCycleTests(unittest.TestCase):
    def test_orchestration_only_mode_no_scan(self):
        # connect() call order in orchestration-only mode:
        #   1. _start_run -> RETURNING id
        #   2. _candidate_insights -> COUNT, cta_rows fetchall, monetization fetchone
        #   3. _finish_run -> UPDATE (no fetch)
        start_cur = QueueCursor(fetchone_rows=[(101,)])
        candidate_cur = QueueCursor(
            fetchone_rows=[(0,), (0, 0, 0, 0, 0)],  # n=0, monetization tuple
            fetchall_rows=[[]],  # cta_rows empty
        )
        finish_cur = QueueCursor()
        seq = SequencedConnect([start_cur, candidate_cur, finish_cur])

        with patch.object(daemon, "connect", seq):
            with patch.object(daemon, "record_event", lambda *a, **k: 1):
                # distill_insight: first 4 baseline insights created, rest reinforced
                with patch.object(daemon, "distill_insight", lambda **k: (1, True)):
                    with patch.object(daemon, "active_insights", lambda **k: []):
                        result = run_improvement_cycle(niche="gta6-ai-persona-gaming")

        self.assertEqual(result.run_id, 101)
        self.assertTrue(result.trace_id.startswith("improve-"))
        self.assertEqual(result.scanned, 0)
        self.assertGreaterEqual(result.distilled, 4)  # 4 baseline insights
        self.assertEqual(result.proposed, 0)  # active_insights empty -> no proposal
        self.assertEqual(result.blocked_actions, BLOCKED_DAEMON_ACTIONS)

    def test_delegated_scan_and_proposal(self):
        start_cur = QueueCursor(fetchone_rows=[(102,)])
        # ingest cursor: one item inserted, rowcount 1
        ingest_cur = QueueCursor(rowcount=1)
        candidate_cur = QueueCursor(
            fetchone_rows=[(0,), (0, 0, 0, 0, 0)],
            fetchall_rows=[[]],
        )
        finish_cur = QueueCursor()
        seq = SequencedConnect([start_cur, ingest_cur, candidate_cur, finish_cur])

        class FakeInsight:
            id = 5

        def fake_scan(niche):
            return [{"platform": "instagram", "url": "https://x/1", "title": "clip"}]

        with patch.object(daemon, "connect", seq):
            with patch.object(daemon, "record_event", lambda *a, **k: 1):
                with patch.object(daemon, "distill_insight", lambda **k: (1, True)):
                    with patch.object(daemon, "active_insights", lambda **k: [FakeInsight()]):
                        with patch.object(daemon, "propose_improvement", lambda **k: 55) as _p:
                            result = run_improvement_cycle(niche="gta6", scan_fn=fake_scan)

        self.assertEqual(result.run_id, 102)
        self.assertEqual(result.scanned, 1)
        self.assertEqual(result.proposed, 1)  # active_insights non-empty -> one proposal
        self.assertIn("proposed=1", result.summary)


class GetDaemonStatusTests(unittest.TestCase):
    def test_status_never_run(self):
        # Single connect() context; queries: run_row(None), active count, open count, events count.
        cur = QueueCursor(
            fetchone_rows=[None, (0,), (0,), (0,)],
        )
        conn = QueueConn(cur)

        @contextmanager
        def _cm():
            yield conn

        with patch.object(daemon, "connect", _cm):
            status = get_daemon_status("improvement-daemon")

        self.assertIsNone(status.latest_run)
        self.assertEqual(status.active_insights, 0)
        self.assertEqual(status.open_proposals, 0)
        self.assertEqual(status.blocked_actions, BLOCKED_DAEMON_ACTIONS)

    def test_status_with_latest_run(self):
        from datetime import UTC, datetime

        run_row = (
            7,
            "improvement-daemon",
            "improve-xyz",
            "succeeded",
            datetime(2026, 7, 4, 22, 0, tzinfo=UTC),
            datetime(2026, 7, 4, 22, 0, 5, tzinfo=UTC),
            "ok",
            {"distilled": 4},
            None,
        )
        cur = QueueCursor(fetchone_rows=[run_row, (6,), (1,), (30,)])
        conn = QueueConn(cur)

        @contextmanager
        def _cm():
            yield conn

        with patch.object(daemon, "connect", _cm):
            status = get_daemon_status()

        self.assertIsNotNone(status.latest_run)
        assert status.latest_run is not None
        self.assertEqual(status.latest_run["id"], 7)
        self.assertEqual(status.latest_run["status"], "succeeded")
        self.assertEqual(status.latest_run["started_at"], "2026-07-04T22:00:00+00:00")
        self.assertEqual(status.active_insights, 6)
        self.assertEqual(status.open_proposals, 1)
        self.assertEqual(status.recent_events, 30)


if __name__ == "__main__":
    unittest.main()
