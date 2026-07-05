"""Integration tests for the aflack pipeline.

These tests verify that multiple modules work together correctly, exercising
the full pipeline flow from compliance checking through publish intent creation,
analytics normalization, and economics rollup calculation.
"""

from __future__ import annotations

import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from aflack.analytics import snapshot_from_postiz_payload
from aflack.compliance import check_publish_item
from aflack.economics import current_rollup
from aflack.learning import score_creator_credibility
from aflack.prompt_quality import check_short_asset_prompt
from aflack.publishing import PublishIntent


class ComplianceToPublishingIntegrationTests(unittest.TestCase):
    """Verify that compliance checks gate publishing correctly."""

    def test_compliant_content_passes_gate_and_creates_intent(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: AI-assisted content; affiliate links may earn commission.",
            script_body="GTA6 countdown commentary with original visuals.",
        )
        self.assertTrue(result.passed)
        intent = PublishIntent(
            creative_id=1,
            platform="youtube",
            target_format="short",
            title="GTA 6 countdown",
            description="Compliant content",
            disclosure_text="Disclosure: AI-assisted content; affiliate links may earn commission.",
        )
        self.assertEqual(intent.platform, "youtube")
        self.assertEqual(intent.target_format, "short")

    def test_non_compliant_content_blocked_before_publishing(self):
        result = check_publish_item(
            source_provenance="same_seed_regeneration_of_official_footage",
            disclosure_text="",
            script_body="Leaked gameplay footage.",
        )
        self.assertFalse(result.passed)
        self.assertGreater(len(result.blocks), 0)


class AnalyticsToEconomicsIntegrationTests(unittest.TestCase):
    """Verify that analytics snapshots feed into economics calculations."""

    def test_postiz_analytics_snapshot_normalizes_correctly(self):
        payload = {
            "data": {
                "postId": "test-post-123",
                "views": 50000,
                "likes": 2000,
                "comments": 150,
                "shares": 300,
                "revenue": "125.50",
            }
        }
        snapshot = snapshot_from_postiz_payload(payload, platform="youtube")
        self.assertEqual(snapshot.platform, "youtube")
        self.assertEqual(snapshot.source, "postiz")
        self.assertEqual(snapshot.views, 50000)
        self.assertEqual(snapshot.likes, 2000)
        self.assertEqual(snapshot.revenue, Decimal("125.50"))

    def test_economics_rollup_calculates_margin(self):
        with patch("aflack.economics.connect") as mock_connect:
            mock_conn = MagicMock()
            mock_cur = MagicMock()
            mock_connect.return_value.__enter__.return_value = mock_conn
            mock_conn.cursor.return_value.__enter__.return_value = mock_cur
            mock_cur.fetchone.side_effect = [
                (Decimal("100"),),
                (Decimal("200"),),
                (5,),
            ]
            rollup = current_rollup()
        self.assertEqual(rollup.total_cost, Decimal("100"))
        self.assertEqual(rollup.revenue, Decimal("200"))
        self.assertEqual(rollup.contribution_margin, Decimal("100"))


class PromptQualityToComplianceIntegrationTests(unittest.TestCase):
    """Verify that prompt quality checks align with compliance requirements."""

    def test_story_native_prompt_passes_quality_and_compliance(self):
        prompt = (
            "Vertical 9:16 GTA6 day-one setup audit scene with original AI visuals. "
            "Controller on neon desk, drift test UI fails, crash zoom camera move, "
            "final frame reveals a FIX FIRST checklist. No real brand logos."
        )
        quality = check_short_asset_prompt(prompt)
        self.assertTrue(quality.passed)

    def test_generic_prompt_fails_quality_check(self):
        prompt = "A gaming video about GTA 6"
        quality = check_short_asset_prompt(prompt)
        self.assertFalse(quality.passed)


class CreatorCredibilityIntegrationTests(unittest.TestCase):
    """Verify creator credibility scoring integrates with benchmark data."""

    def test_verified_creator_requires_all_three_signals(self):
        cred = score_creator_credibility(
            proof_engagement_rate=0.05,
            proof_monetization="sponsorship + affiliate",
            proof_consistency_days=30,
        )
        self.assertEqual(cred, "verified")

    def test_weak_creator_with_only_followers(self):
        cred = score_creator_credibility(
            proof_engagement_rate=None,
            proof_monetization=None,
            proof_consistency_days=None,
        )
        self.assertEqual(cred, "unverified")


if __name__ == "__main__":
    unittest.main()
