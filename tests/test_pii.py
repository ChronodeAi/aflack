from __future__ import annotations

import unittest

from aflack.pii import (
    CREATOR_DATA_CLASSIFICATION,
    classify_field,
    detect_pii,
    mask_creator_data,
)


class DetectPIITests(unittest.TestCase):
    def test_clean_content_reports_no_pii(self):
        result = detect_pii("A public gaming creator with 120k followers.")

        self.assertFalse(result.has_pii)
        self.assertEqual(result.detected_types, [])
        self.assertEqual(result.masked_content, "A public gaming creator with 120k followers.")

    def test_email_is_detected_and_masked(self):
        result = detect_pii("Reach me at creator@example.com for collabs.")

        self.assertTrue(result.has_pii)
        self.assertIn("email", result.detected_types)
        self.assertNotIn("creator@example.com", result.masked_content)
        self.assertIn("[EMAIL_REDACTED]", result.masked_content)

    def test_multiple_pii_types_detected(self):
        result = detect_pii("Call 555-123-4567 or SSN 123-45-6789 at 10.0.0.1")

        self.assertTrue(result.has_pii)
        for pii_type in ("phone", "ssn", "ip_address"):
            self.assertIn(pii_type, result.detected_types)
        self.assertNotIn("555-123-4567", result.masked_content)
        self.assertNotIn("123-45-6789", result.masked_content)
        self.assertNotIn("10.0.0.1", result.masked_content)

    def test_credit_card_is_detected(self):
        result = detect_pii("card 4111 1111 1111 1111 on file")

        self.assertTrue(result.has_pii)
        self.assertIn("credit_card", result.detected_types)
        self.assertIn("[CREDIT_CARD_REDACTED]", result.masked_content)


class MaskCreatorDataTests(unittest.TestCase):
    def test_sensitive_fields_masked_public_left_intact(self):
        data = {
            "handle": "@vice_signal",
            "followers": 42000,
            "monetization": "affiliate + sponsorship",
            "proof_notes": "verified by DM screenshot",
        }

        masked = mask_creator_data(data)

        self.assertEqual(masked["handle"], "@vice_signal")
        self.assertEqual(masked["followers"], 42000)
        self.assertEqual(masked["monetization"], "***MASKED***")
        self.assertEqual(masked["proof_notes"], "***MASKED***")

    def test_original_dict_not_mutated(self):
        data = {"monetization": "affiliate"}

        mask_creator_data(data)

        self.assertEqual(data["monetization"], "affiliate")

    def test_unknown_keys_passed_through(self):
        data = {"custom_metric": 1}

        masked = mask_creator_data(data)

        self.assertEqual(masked["custom_metric"], 1)


class ClassifyFieldTests(unittest.TestCase):
    def test_public_field(self):
        self.assertEqual(classify_field("handle"), "public")

    def test_sensitive_field(self):
        self.assertEqual(classify_field("monetization"), "sensitive")

    def test_unknown_field(self):
        self.assertEqual(classify_field("not_a_field"), "unknown")

    def test_classification_map_covers_expected_keys(self):
        self.assertIn("platform", CREATOR_DATA_CLASSIFICATION)
        self.assertEqual(CREATOR_DATA_CLASSIFICATION["source_url"], "public")


if __name__ == "__main__":
    unittest.main()
