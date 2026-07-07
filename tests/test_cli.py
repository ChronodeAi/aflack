from __future__ import annotations

import unittest
from contextlib import contextmanager
from decimal import Decimal
from unittest.mock import patch

from typer.testing import CliRunner

from aflack import cli
from aflack.analytics import AnalyticsRollup, AnalyticsSnapshot
from aflack.cli import app
from aflack.daemon import DaemonStatus
from aflack.economics import EconomicsRollup
from aflack.learning import Insight

runner = CliRunner()


class FakeCursor:
    """Minimal cursor supporting the `with conn.cursor() as cur` protocol."""

    def __init__(self, *, fetchone_rows=None, fetchall_rows=None):
        # fetchone_rows is a list consumed one-per-call to support multi-query commands.
        self._fetchone_rows = list(fetchone_rows) if fetchone_rows is not None else []
        self._fetchall_rows = fetchall_rows if fetchall_rows is not None else []
        self.executed: list[str] = []
        self.params: list = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append(sql)
        self.params.append(params)

    def fetchone(self):
        if self._fetchone_rows:
            return self._fetchone_rows.pop(0)
        return None

    def fetchall(self):
        return self._fetchall_rows


class FakeConnection:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


def fake_connect_factory(conn):
    @contextmanager
    def _cm():
        yield conn

    return _cm


class ComplianceSmokeTests(unittest.TestCase):
    def test_compliance_smoke_reports_pass_and_block(self):
        result = runner.invoke(app, ["compliance-smoke"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("allowed_sample passed=True", result.stdout)
        self.assertIn("blocked_sample passed=False", result.stdout)


class PromptQualityCommandTests(unittest.TestCase):
    def test_missing_input_is_bad_parameter(self):
        result = runner.invoke(app, ["prompt-quality"])
        self.assertNotEqual(result.exit_code, 0)

    def test_text_prompt_evaluated(self):
        result = runner.invoke(app, ["prompt-quality", "--text", "just a plain generic line"])
        # A weak prompt fails the gate -> exit code 1, but output still printed.
        self.assertIn("passed=", result.stdout)
        self.assertIn("blocks=", result.stdout)


class EconomicsStatusTests(unittest.TestCase):
    def test_economics_status_prints_rollup(self):
        rollup = EconomicsRollup(
            total_cost=Decimal("10"),
            revenue=Decimal("25"),
            contribution_margin=Decimal("15"),
            generated_creatives=3,
            cost_per_generated=Decimal("3.33"),
        )
        with patch.object(cli, "current_rollup", lambda: rollup):
            result = runner.invoke(app, ["economics-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("total_cost=10", result.stdout)
        self.assertIn("revenue=25", result.stdout)
        self.assertIn("contribution_margin=15", result.stdout)
        self.assertIn("generated_creatives=3", result.stdout)


class AnalyticsStatusTests(unittest.TestCase):
    def test_analytics_status_prints_rollup(self):
        rollup = AnalyticsRollup(
            snapshots=2,
            total_views=1000,
            total_likes=50,
            total_comments=10,
            total_shares=5,
            total_saves=3,
            total_clicks=20,
            total_conversions=4,
            total_revenue=Decimal("12.50"),
        )
        with patch.object(cli, "current_analytics_rollup", lambda p=None: rollup):
            result = runner.invoke(app, ["analytics-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("snapshots=2", result.stdout)
        self.assertIn("total_views=1000", result.stdout)
        self.assertIn("total_revenue=12.50", result.stdout)


class AnalyticsRecordManualTests(unittest.TestCase):
    def test_manual_snapshot_recorded(self):
        with patch.object(cli, "record_snapshot", lambda snap: 99):
            result = runner.invoke(
                app,
                ["analytics-record-manual", "youtube", "--views", "500", "--conversions", "7"],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("analytics_snapshot_id=99", result.stdout)
        self.assertIn("platform=youtube", result.stdout)
        self.assertIn("views=500", result.stdout)
        self.assertIn("conversions=7", result.stdout)

    def test_negative_counter_rejected(self):
        # AnalyticsSnapshot.normalized raises ValueError on negative counters.
        result = runner.invoke(app, ["analytics-record-manual", "youtube", "--views", "-1"])
        self.assertEqual(result.exit_code, 2)
        self.assertIn("analytics snapshot rejected", result.stdout)


class CostRecordTests(unittest.TestCase):
    def test_invalid_json_metadata_rejected(self):
        result = runner.invoke(
            app,
            ["cost-record", "creative", "1", "higgsfield", "5", "credit", "--metadata", "{not json"],
        )
        self.assertEqual(result.exit_code, 2)
        self.assertIn("metadata must be valid JSON", result.stdout)

    def test_non_object_metadata_rejected(self):
        result = runner.invoke(
            app,
            ["cost-record", "creative", "1", "higgsfield", "5", "credit", "--metadata", "[1,2]"],
        )
        self.assertNotEqual(result.exit_code, 0)

    def test_valid_cost_recorded(self):
        conn = FakeConnection(FakeCursor(fetchone_rows=[(123,)]))
        with patch.object(cli, "connect", fake_connect_factory(conn)):
            result = runner.invoke(
                app,
                ["cost-record", "creative", "1", "higgsfield", "5", "credit", "--metadata", '{"source":"test"}'],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("cost_ledger_id=123", result.stdout)
        self.assertTrue(conn.committed)


class PublishQueueStatusTests(unittest.TestCase):
    def test_empty_queue(self):
        conn = FakeConnection(FakeCursor(fetchall_rows=[]))
        with patch.object(cli, "connect", fake_connect_factory(conn)):
            result = runner.invoke(app, ["publish-queue-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("(no publish queue items)", result.stdout)

    def test_populated_queue(self):
        rows = [(2, 5, "youtube", "short", "needs_auth", "cmr6", "", "")]
        conn = FakeConnection(FakeCursor(fetchall_rows=rows))
        with patch.object(cli, "connect", fake_connect_factory(conn)):
            result = runner.invoke(app, ["publish-queue-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("id=2", result.stdout)
        self.assertIn("platform=youtube", result.stdout)
        self.assertIn("postiz_post_id=cmr6", result.stdout)


class PublishSmokeTests(unittest.TestCase):
    def test_no_creatives_raises(self):
        conn = FakeConnection(FakeCursor(fetchone_rows=[None]))
        with patch.object(cli, "connect", fake_connect_factory(conn)):
            result = runner.invoke(app, ["publish-smoke"])
        self.assertNotEqual(result.exit_code, 0)

    def test_creates_intent(self):
        conn = FakeConnection(FakeCursor(fetchone_rows=[(7,)]))

        class FakePublisher:
            def enqueue(self, intent):
                return 42

        with patch.object(cli, "connect", fake_connect_factory(conn)):
            with patch.object(cli, "PostizPublisher", FakePublisher):
                result = runner.invoke(app, ["publish-smoke"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("queue_id=42", result.stdout)


class PostizCommandTests(unittest.TestCase):
    def test_integrations_lists_channels(self):
        class FakePublisher:
            def list_integrations(self):
                return [{"id": "int-1", "identifier": "youtube", "name": "YT Chan"}]

        with patch.object(cli, "PostizPublisher", FakePublisher):
            result = runner.invoke(app, ["postiz-integrations"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("int-1", result.stdout)
        self.assertIn("youtube", result.stdout)

    def test_integrations_runtime_error_exits_2(self):
        class FakePublisher:
            def list_integrations(self):
                raise RuntimeError("POSTIZ_API_KEY missing")

        with patch.object(cli, "PostizPublisher", FakePublisher):
            result = runner.invoke(app, ["postiz-integrations"])

        self.assertEqual(result.exit_code, 2)
        self.assertIn("POSTIZ_API_KEY missing", result.stdout)

    def test_preview_prints_payload(self):
        class FakePublisher:
            def build_queue_payload(self, queue_id, integration_id, *, as_draft=True):
                return {"type": "draft", "queue": queue_id}

        with patch.object(cli, "PostizPublisher", FakePublisher):
            result = runner.invoke(app, ["postiz-preview", "2", "int-1"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn('"queue": 2', result.stdout)

    def test_submit_prints_response(self):
        class FakePublisher:
            def submit_queue_item(self, queue_id, integration_id, *, as_draft=True):
                return {"ok": True, "postId": "abc"}

        with patch.object(cli, "PostizPublisher", FakePublisher):
            result = runner.invoke(app, ["postiz-submit", "2", "int-1"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("postId", result.stdout)


class LearningCommandTests(unittest.TestCase):
    def test_insights_list_empty(self):
        with patch.object(cli, "active_insights", lambda *a, **k: []):
            result = runner.invoke(app, ["insights-list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("(no active insights)", result.stdout)

    def test_insights_list_rows(self):
        insight = Insight(
            id=1, scope="hook", statement="open on a claim", confidence=0.7, support_count=3, status="active"
        )
        with patch.object(cli, "active_insights", lambda *a, **k: [insight]):
            result = runner.invoke(app, ["insights-list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("[1]", result.stdout)
        self.assertIn("hook", result.stdout)
        self.assertIn("open on a claim", result.stdout)

    def test_insight_add(self):
        with patch.object(cli, "distill_insight", lambda **k: (5, True)):
            result = runner.invoke(app, ["insight-add", "cta", "one word CTA wins", "--confidence", "0.6"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("insight_id=5 created=True", result.stdout)

    def test_proposals_list_empty(self):
        with patch.object(cli, "open_proposals", lambda **k: []):
            result = runner.invoke(app, ["proposals-list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("(no open proposals)", result.stdout)

    def test_proposals_list_rows(self):
        prop = {
            "id": 9,
            "target_type": "skill",
            "target_name": "hook-authoring",
            "status": "proposed",
            "change_summary": "fold insights",
        }
        with patch.object(cli, "open_proposals", lambda **k: [prop]):
            result = runner.invoke(app, ["proposals-list"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("[9]", result.stdout)
        self.assertIn("skill:hook-authoring", result.stdout)

    def test_proposals_dedupe(self):
        with patch.object(cli, "dedupe_open_proposals", lambda: 4):
            result = runner.invoke(app, ["proposals-dedupe"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("superseded=4", result.stdout)

    def test_creator_add(self):
        with patch.object(cli, "upsert_creator", lambda **k: 11):
            result = runner.invoke(app, ["creator-add", "youtube", "@vice", "--followers", "5000"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("creator_id=11", result.stdout)

    def test_creator_proof(self):
        with patch.object(cli, "set_creator_proof", lambda cid, **k: "plausible"):
            result = runner.invoke(app, ["creator-proof", "11", "--engagement-rate", "0.05"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("creator_id=11 credibility=plausible", result.stdout)

    def test_memory_consolidate(self):
        class FakeResult:
            scanned = 5
            created = 2
            skipped_existing = 3
            lesson_ids = [1, 2]

        with patch.object(cli, "consolidate_insights_to_lessons", lambda **k: FakeResult()):
            result = runner.invoke(app, ["memory-consolidate"])
        self.assertEqual(result.exit_code, 0)
        self.assertIn("scanned=5", result.stdout)
        self.assertIn("created=2", result.stdout)
        self.assertIn("lesson_ids=[1, 2]", result.stdout)


class ImproveCycleTests(unittest.TestCase):
    def test_improve_cycle_reports_summary(self):
        from aflack.daemon import CycleResult

        cycle = CycleResult(
            trace_id="improve-abc",
            run_id=3,
            scanned=0,
            distilled=4,
            reinforced=0,
            proposed=1,
            blocked_actions=["higgsfield_generation", "public_publish"],
            summary="scanned=0 distilled=4 reinforced=0 proposed=1",
        )
        with patch.object(cli, "run_improvement_cycle", lambda **k: cycle):
            result = runner.invoke(app, ["improve-cycle"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("trace_id=improve-abc", result.stdout)
        self.assertIn("proposed=1", result.stdout)
        self.assertIn("higgsfield_generation", result.stdout)


class DaemonStatusTests(unittest.TestCase):
    def test_daemon_status_never_run(self):
        status = DaemonStatus(
            daemon="improvement-daemon",
            latest_run=None,
            active_insights=0,
            open_proposals=0,
            recent_events=0,
            blocked_actions=["public_publish"],
        )
        with patch.object(cli, "get_daemon_status", lambda d: status):
            result = runner.invoke(app, ["daemon-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("latest_status=never_run", result.stdout)
        self.assertIn("active_insights=0", result.stdout)

    def test_daemon_status_with_run(self):
        status = DaemonStatus(
            daemon="improvement-daemon",
            latest_run={
                "id": 7,
                "trace_id": "improve-xyz",
                "status": "succeeded",
                "started_at": "2026-07-04T22:00:00+00:00",
                "finished_at": "2026-07-04T22:00:05+00:00",
                "summary": "ok",
                "counts": {"distilled": 4},
                "error": None,
            },
            active_insights=6,
            open_proposals=1,
            recent_events=30,
            blocked_actions=["public_publish"],
        )
        with patch.object(cli, "get_daemon_status", lambda d: status):
            result = runner.invoke(app, ["daemon-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("latest_run_id=7", result.stdout)
        self.assertIn("latest_status=succeeded", result.stdout)
        self.assertIn("active_insights=6", result.stdout)


class TraceShowTests(unittest.TestCase):
    def test_trace_show_prints_events(self):
        events = [
            {
                "created_at": "2026-07-04T22:00:00+00:00",
                "stage": "start",
                "actor": "improvement-daemon",
                "event_type": "start",
                "payload": {"niche": "gta6"},
            }
        ]
        with patch.object(cli, "trace_events", lambda tid: events):
            result = runner.invoke(app, ["trace-show", "improve-xyz"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("start", result.stdout)
        self.assertIn("improvement-daemon", result.stdout)


class AsideScanImportTests(unittest.TestCase):
    def test_import_reports_summary(self):
        from aflack.aside_scan import ImportSummary

        summary = ImportSummary(
            trace_id="scan-1",
            observations_seen=8,
            creators_upserted=8,
            videos_inserted=6,
            videos_duplicate=2,
            creators_verified_or_plausible=4,
        )
        with patch.object(cli, "import_aside_scan", lambda p: summary):
            # Use an existing file path so Typer's Path arg resolves; content ignored via patch.
            result = runner.invoke(app, ["aside-scan-import", "pyproject.toml"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("trace_id=scan-1", result.stdout)
        self.assertIn("observations_seen=8", result.stdout)
        self.assertIn("videos_duplicate=2", result.stdout)

    def test_import_failure_exits_2(self):
        def boom(path):
            raise ValueError("bad scan json")

        with patch.object(cli, "import_aside_scan", boom):
            result = runner.invoke(app, ["aside-scan-import", "pyproject.toml"])

        self.assertEqual(result.exit_code, 2)
        self.assertIn("scan import failed", result.stdout)


class AnalyticsRecordManualSnapshotShapeTests(unittest.TestCase):
    def test_snapshot_normalized_used(self):
        # Confirms the CLI builds a real AnalyticsSnapshot and passes it through.
        captured = {}

        def fake_record(snap: AnalyticsSnapshot) -> int:
            captured["platform"] = snap.platform
            captured["views"] = snap.views
            return 1

        with patch.object(cli, "record_snapshot", fake_record):
            result = runner.invoke(app, ["analytics-record-manual", "TikTok", "--views", "10"])

        self.assertEqual(result.exit_code, 0)
        # normalized() lowercases the platform.
        self.assertEqual(captured["platform"], "tiktok")
        self.assertEqual(captured["views"], 10)


if __name__ == "__main__":
    unittest.main()
