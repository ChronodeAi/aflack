from __future__ import annotations

import unittest

from aflack.learning import insight_hash, score_creator_credibility


class LearningPureLogicTests(unittest.TestCase):
    def test_insight_hash_is_normalized_and_stable(self):
        a = insight_hash("hook", "Open on a concrete claim.")
        b = insight_hash("hook", "  open   ON a   Concrete claim.  ")
        self.assertEqual(a, b)  # dedup survives whitespace/case

    def test_insight_hash_scope_separates(self):
        self.assertNotEqual(
            insight_hash("hook", "same text"),
            insight_hash("cta", "same text"),
        )

    def test_credibility_requires_real_signals_not_vanity(self):
        # Huge followers but no proof -> still unverified.
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=None,
                proof_monetization=None,
                proof_consistency_days=None,
            ),
            "unverified",
        )

    def test_credibility_verified_needs_all_three(self):
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=0.05,
                proof_monetization="affiliate",
                proof_consistency_days=30,
            ),
            "verified",
        )

    def test_credibility_partial_signals(self):
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=0.05,
                proof_monetization="affiliate",
                proof_consistency_days=3,
            ),
            "plausible",
        )
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=0.005,
                proof_monetization=None,
                proof_consistency_days=None,
            ),
            "unverified",
        )


if __name__ == "__main__":
    unittest.main()
