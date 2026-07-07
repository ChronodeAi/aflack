"""CLI runner tests with explicit requirement-ID traceability.

Each test is annotated with the FR-xxx IDs it covers to close the
IOC hardening gap identified in the 2026-07-05 traceability report.

These tests complement the JSON-mode tests in test_cli.py by covering:
  - Plain-text (non-JSON) output paths for the five critical status commands.
  - The passing case for prompt-quality (JSON + text mode).

Requirements covered: FR-007, FR-008, FR-011, FR-013, FR-020, FR-021.
"""

from __future__ import annotations

import json
import unittest
from contextlib import contextmanager
from decimal import Decimal
from unittest.mock import patch

from typer.testing import CliRunner

from aflack.analytics import AnalyticsRollup
from aflack.cli import app
from aflack.daemon import DaemonStatus

# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

_PASSING_PROMPT = (
    "Vertical 9:16 GTA6 day-one setup audit scene. Opening frame: a controller sits under a "
    "neon countdown reading LAUNCH NIGHT, while the analog stick drifts by itself. Crash zoom "
    "to the stick test as the UI fails, then a yellow FIX FIRST label snaps on. The final frame "
    "reveals the whole boring-smart day-one setup checklist and loops back to the first frame. "
    "No real brand logos, no Rockstar or Take-Two logos, no GTA footage, no trailer frames, "
    "no real-person likeness."
)


class FakeCursor:
    def __init__(self, rows):
        self.rows = list(rows)
        self.row = self.rows[0] if self.rows else None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.sql = sql
        self.params = params

    def fetchall(self):
        return self.rows

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, rows):
        self.rows = rows

    def cursor(self):
        return FakeCursor(self.rows)

    def commit(self):
        self.committed = True


# ---------------------------------------------------------------------------
# FR-020: Machine-readable status — daemon-status text mode
# ---------------------------------------------------------------------------


class DaemonStatusTextTests(unittest.TestCase):
    """FR-020: daemon-status plain-text output path."""

    def setUp(self):
        self.runner = CliRunner()

    def test_daemon_status_text_never_run(self):
        """FR-020: daemon-status text mode reports never-run state correctly."""
        status = DaemonStatus(
            daemon="improvement-daemon",
            latest_run=None,
            active_insights=0,
            open_proposals=0,
            recent_events=0,
            blocked_actions=["public_publish"],
        )
        with patch("aflack.cli.get_daemon_status", return_value=status):
            result = self.runner.invoke(app, ["daemon-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("daemon=improvement-daemon", result.output)
        self.assertIn("latest_run_id=None", result.output)
        self.assertIn("latest_status=never_run", result.output)
        self.assertIn("blocked_actions=", result.output)
        self.assertIn("public_publish", result.output)

    def test_daemon_status_text_with_run(self):
        """FR-020: daemon-status text mode shows latest run summary when run exists."""
        run = {
            "id": 42,
            "trace_id": "aflack-abc123",
            "status": "succeeded",
            "started_at": "2026-07-05T01:00:00Z",
            "finished_at": "2026-07-05T01:00:10Z",
            "summary": "scanned 5 insights",
            "counts": {"scanned": 5, "proposed": 1},
            "error": None,
        }
        status = DaemonStatus(
            daemon="improvement-daemon",
            latest_run=run,
            active_insights=3,
            open_proposals=1,
            recent_events=5,
            blocked_actions=["public_publish", "higgsfield_generation"],
        )
        with patch("aflack.cli.get_daemon_status", return_value=status):
            result = self.runner.invoke(app, ["daemon-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("latest_run_id=42", result.output)
        self.assertIn("latest_trace_id=aflack-abc123", result.output)
        self.assertIn("latest_status=succeeded", result.output)
        self.assertIn("active_insights=3", result.output)
        self.assertIn("open_proposals=1", result.output)


# ---------------------------------------------------------------------------
# FR-013, FR-020: analytics-status text mode
# ---------------------------------------------------------------------------


class AnalyticsStatusTextTests(unittest.TestCase):
    """FR-013, FR-020: analytics-status plain-text output path."""

    def setUp(self):
        self.runner = CliRunner()

    def test_analytics_status_text_output(self):
        """FR-013, FR-020: analytics-status text mode shows all rollup fields."""
        rollup = AnalyticsRollup(
            snapshots=5,
            total_views=1000,
            total_likes=50,
            total_comments=10,
            total_shares=20,
            total_saves=15,
            total_clicks=30,
            total_conversions=3,
            total_revenue=Decimal("75.00"),
        )
        with patch("aflack.cli.current_analytics_rollup", return_value=rollup):
            result = self.runner.invoke(app, ["analytics-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("snapshots=5", result.output)
        self.assertIn("total_views=1000", result.output)
        self.assertIn("total_likes=50", result.output)
        self.assertIn("total_revenue=75.00", result.output)


# ---------------------------------------------------------------------------
# FR-008, FR-020: publish-queue-status text mode
# ---------------------------------------------------------------------------


class PublishQueueStatusTextTests(unittest.TestCase):
    """FR-008, FR-020: publish-queue-status plain-text output path."""

    def setUp(self):
        self.runner = CliRunner()

    def test_publish_queue_status_empty_text_output(self):
        """FR-008, FR-020: empty publish queue text mode shows placeholder message."""

        @contextmanager
        def fake_connect():
            yield FakeConnection([])

        with patch("aflack.cli.connect", fake_connect):
            result = self.runner.invoke(app, ["publish-queue-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("no publish queue items", result.output)

    def test_publish_queue_status_text_with_item(self):
        """FR-008, FR-012, FR-020: publish-queue text mode lists queue item fields."""
        rows = [
            (3, 2, "youtube", "short", "submitted_to_postiz", "postiz-99", "", ""),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(rows)

        with patch("aflack.cli.connect", fake_connect):
            result = self.runner.invoke(app, ["publish-queue-status"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("id=3", result.output)
        self.assertIn("platform=youtube", result.output)
        self.assertIn("postiz_post_id=postiz-99", result.output)
        self.assertIn("status=submitted_to_postiz", result.output)


# ---------------------------------------------------------------------------
# FR-011, FR-021: prompt-quality passing case (JSON + text)
# ---------------------------------------------------------------------------


class PromptQualityPassTests(unittest.TestCase):
    """FR-011, FR-021: prompt-quality gate — passing prompt path."""

    def setUp(self):
        self.runner = CliRunner()

    def test_prompt_quality_json_pass(self):
        """FR-011, FR-021: strong prompt returns exit code 0 with passed=True in JSON."""
        result = self.runner.invoke(app, ["prompt-quality", "--text", _PASSING_PROMPT, "--json"])

        self.assertEqual(result.exit_code, 0)
        payload = json.loads(result.output)
        self.assertTrue(payload["passed"])
        self.assertEqual(payload["blocks"], [])

    def test_prompt_quality_text_pass(self):
        """FR-011, FR-021: strong prompt text mode reports passed=True and exits 0."""
        result = self.runner.invoke(app, ["prompt-quality", "--text", _PASSING_PROMPT])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("passed=True", result.output)
        self.assertIn("blocks=[]", result.output)


# ---------------------------------------------------------------------------
# FR-007, FR-020: compliance-smoke text mode
# ---------------------------------------------------------------------------


class ComplianceSmokeTextTests(unittest.TestCase):
    """FR-007, FR-020: compliance-smoke plain-text output path."""

    def setUp(self):
        self.runner = CliRunner()

    def test_compliance_smoke_text_output(self):
        """FR-007, FR-020: compliance-smoke text mode prints allow/block status."""
        result = self.runner.invoke(app, ["compliance-smoke"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("allowed_sample passed=True", result.output)
        self.assertIn("blocked_sample passed=False", result.output)


# ---------------------------------------------------------------------------
# FR-004, FR-005: setup/persona command coverage
# ---------------------------------------------------------------------------


class SetupAndCreatorCommandTests(unittest.TestCase):
    """FR-004, FR-005: beachhead and creator setup command paths."""

    def setUp(self):
        self.runner = CliRunner()

    def test_set_beachhead_locks_gta6_youtube_first_niche(self):
        """FR-004: set-beachhead writes the selected beachhead and reports id."""

        @contextmanager
        def fake_connect():
            yield FakeConnection([(99,)])

        with patch("aflack.cli.connect", fake_connect):
            result = self.runner.invoke(app, ["set-beachhead"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Beachhead locked: gta6-ai-persona-gaming", result.output)
        self.assertIn("niche_id=99", result.output)

    def test_creator_add_normalizes_empty_optional_fields(self):
        """FR-005: creator-add registers a benchmark creator candidate."""
        with patch("aflack.cli.upsert_creator", return_value=12) as upsert:
            result = self.runner.invoke(
                app,
                [
                    "creator-add",
                    "instagram",
                    "loadoutlab",
                    "--followers",
                    "1000",
                ],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("creator_id=12", result.output)
        upsert.assert_called_once_with(
            platform="instagram",
            handle="loadoutlab",
            display_name=None,
            niche=None,
            followers=1000,
            source_url=None,
        )

    def test_creator_proof_reports_computed_credibility(self):
        """FR-005: creator-proof stores real-success evidence and reports credibility."""
        with patch("aflack.cli.set_creator_proof", return_value="verified") as set_proof:
            result = self.runner.invoke(
                app,
                [
                    "creator-proof",
                    "12",
                    "--engagement-rate",
                    "0.05",
                    "--monetization",
                    "affiliate",
                    "--consistency-days",
                    "30",
                    "--notes",
                    "public funnel evidence",
                ],
            )

        self.assertEqual(result.exit_code, 0)
        self.assertIn("creator_id=12 credibility=verified", result.output)
        set_proof.assert_called_once_with(
            12,
            proof_engagement_rate=0.05,
            proof_monetization="affiliate",
            proof_consistency_days=30,
            proof_notes="public funnel evidence",
        )


if __name__ == "__main__":
    unittest.main()
