from __future__ import annotations

import unittest

from aflack.compliance import check_publish_item


class ComplianceGateTests(unittest.TestCase):
    def test_original_ai_affiliate_disclosed_content_passes(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text=(
                "Disclosure: AI-generated original visuals. Affiliate links may earn "
                "commission. Not affiliated with Rockstar Games."
            ),
            script_body="Practical launch setup checklist with original visuals only.",
            persona_is_ai=True,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.blocks, [])
        self.assertEqual(result.warnings, [])

    def test_blocked_source_provenance_fails(self):
        for provenance in (
            "rockstar_pre_release_footage",
            "leaked_footage",
            "official_trailer_footage_reupload",
            "same_seed_regeneration_of_official_footage",
        ):
            with self.subTest(provenance=provenance):
                result = check_publish_item(
                    source_provenance=provenance,
                    disclosure_text="Disclosure: AI visuals; affiliate links may earn commission.",
                    script_body="Original commentary.",
                )

                self.assertFalse(result.passed)
                self.assertIn(f"blocked source provenance: {provenance}", result.blocks)

    def test_missing_affiliate_disclosure_fails(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: AI-generated original visuals.",
            script_body="Launch setup checklist.",
        )

        self.assertFalse(result.passed)
        self.assertIn("missing affiliate disclosure", result.blocks)

    def test_false_firsthand_access_claim_fails(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: AI visuals; affiliate links may earn commission.",
            script_body="I played the leaked build and this setup is mandatory.",
        )

        self.assertFalse(result.passed)
        self.assertIn("false firsthand access claim: 'i played the leaked'", result.blocks)

    def test_medical_claim_marker_fails(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: AI visuals; affiliate links may earn commission.",
            script_body="This controller grip will cure wrist pain.",
        )

        self.assertFalse(result.passed)
        self.assertIn("possible prohibited medical/health claim: 'cure'", result.blocks)

    def test_ai_persona_without_ai_disclosure_warns(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: affiliate links may earn commission.",
            script_body="Original gaming setup guide.",
            persona_is_ai=True,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.blocks, [])
        self.assertIn(
            "AI/synthetic persona: consider explicit AI disclosure per platform/FTC",
            result.warnings,
        )

    def test_non_ai_persona_without_ai_disclosure_does_not_warn(self):
        result = check_publish_item(
            source_provenance="original_ai_visuals",
            disclosure_text="Disclosure: affiliate links may earn commission.",
            script_body="Original gaming setup guide.",
            persona_is_ai=False,
        )

        self.assertTrue(result.passed)
        self.assertEqual(result.blocks, [])
        self.assertEqual(result.warnings, [])


if __name__ == "__main__":
    unittest.main()
