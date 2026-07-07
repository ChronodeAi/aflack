from __future__ import annotations

import json
import os
import tempfile
import unittest
from contextlib import contextmanager
from decimal import Decimal
from unittest.mock import patch

from typer.testing import CliRunner

from aflack.analytics import AnalyticsRollup
from aflack.cli import app
from aflack.daemon import DaemonStatus
from aflack.draft_review import DraftReviewRollup


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.sql = sql
        self.params = params

    def fetchall(self):
        return self.rows


class FakeConnection:
    def __init__(self, rows):
        self.rows = rows

    def cursor(self):
        return FakeCursor(self.rows)


class CliJsonTests(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_daemon_status_json(self):
        status = DaemonStatus(
            daemon="improvement-daemon",
            latest_run={"id": 1, "status": "succeeded", "counts": {"scanned": 0}},
            active_insights=2,
            open_proposals=0,
            recent_events=3,
            blocked_actions=["public_publish"],
        )
        with patch("aflack.cli.get_daemon_status", return_value=status):
            result = self.runner.invoke(app, ["daemon-status", "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["daemon"], "improvement-daemon")
        self.assertEqual(payload["latest_run"]["status"], "succeeded")
        self.assertEqual(payload["blocked_actions"], ["public_publish"])

    def test_analytics_status_json(self):
        rollup = AnalyticsRollup(
            snapshots=2,
            total_views=10,
            total_likes=1,
            total_comments=2,
            total_shares=3,
            total_saves=4,
            total_clicks=5,
            total_conversions=6,
            total_revenue=Decimal("7.50"),
        )
        with patch("aflack.cli.current_analytics_rollup", return_value=rollup):
            result = self.runner.invoke(app, ["analytics-status", "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["snapshots"], 2)
        self.assertEqual(payload["total_revenue"], "7.50")

    def test_publish_queue_status_json(self):
        rows = [
            (2, 1, "youtube", "short", "submitted_to_postiz", "postiz-1", "", ""),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(rows)

        with patch("aflack.cli.connect", fake_connect):
            result = self.runner.invoke(app, ["publish-queue-status", "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["items"][0]["postiz_post_id"], "postiz-1")
        self.assertIsNone(payload["items"][0]["platform_post_id"])

    def test_prompt_quality_json_failure_uses_exit_code_one(self):
        result = self.runner.invoke(app, ["prompt-quality", "--text", "A gaming video about GTA 6", "--json"])

        self.assertEqual(result.exit_code, 1)
        payload = json.loads(result.output)
        self.assertFalse(payload["passed"])
        self.assertGreater(len(payload["blocks"]), 0)

    def test_compliance_smoke_json(self):
        result = self.runner.invoke(app, ["compliance-smoke", "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertTrue(payload["allowed_sample"]["passed"])
        self.assertFalse(payload["blocked_sample"]["passed"])

    def test_loop_status_json_reads_control_plane_state(self):
        previous_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp:
            try:
                os.chdir(tmp)
                from pathlib import Path

                state_dir = Path(".aiwg/loops/content-factory")
                state_dir.mkdir(parents=True)
                (state_dir / "state.yaml").write_text(
                    "\n".join(
                        [
                            "schema: aiwg.loop.state.v1",
                            "loop_id: content-factory",
                            "status: active",
                            "phase: controlled-construction",
                            'updated_at: "2026-07-05T00:16:02Z"',
                            "active_iteration: I3",
                            "active_slice: cockpit-visibility",
                            "current_human_gates:",
                            "  - public_publish",
                            "current_approved_bounds:",
                            "  - draft_only",
                            "latest_validation:",
                            "  tests: pass_73",
                            "  aiwg_index: pass_149_artifacts",
                            "next_safe_actions:",
                            "  - render_review",
                        ]
                    )
                )
                result = self.runner.invoke(app, ["loop-status", "--json"])
            finally:
                os.chdir(previous_cwd)

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["active_slice"], "cockpit-visibility")
        self.assertEqual(payload["current_human_gates"], ["public_publish"])
        self.assertEqual(payload["latest_validation"]["tests"], "pass_73")

    def test_draft_review_record_json_never_authorizes_publish(self):
        with patch("aflack.cli.record_draft_review", return_value=7):
            result = self.runner.invoke(
                app,
                [
                    "draft-review-record",
                    "--queue-id",
                    "2",
                    "--reviewer",
                    "Ace",
                    "--verdict",
                    "revise-prompt",
                    "--hook",
                    "4",
                    "--retention",
                    "3",
                    "--payoff",
                    "3",
                    "--compliance",
                    "5",
                    "--cta",
                    "4",
                    "--asset-quality",
                    "2",
                    "--block",
                    "unreadable text",
                    "--lesson",
                    "avoid generic product closeups",
                    "--json",
                ],
            )

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["id"], 7)
        self.assertEqual(payload["verdict"], "revise_prompt")
        self.assertFalse(payload["public_publish_authorized"])
        self.assertEqual(payload["blocks"], ["unreadable text"])

    def test_draft_review_status_json(self):
        rollup = DraftReviewRollup(
            reviews=3,
            publish_candidates=1,
            keep_private=1,
            revise_prompt=1,
            revise_script=0,
            killed=0,
            avg_hook=4.0,
            avg_retention=3.67,
            avg_payoff=3.33,
            avg_compliance=5.0,
            avg_cta=4.0,
            avg_asset_quality=3.0,
        )
        with patch("aflack.cli.draft_review_rollup", return_value=rollup):
            result = self.runner.invoke(app, ["draft-review-status", "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertEqual(payload["reviews"], 3)
        self.assertEqual(payload["publish_candidates"], 1)
        self.assertFalse(payload["public_publish_automation_ready"])


if __name__ == "__main__":
    unittest.main()
