from __future__ import annotations

import unittest

from aflack.draft_review import DraftReviewInput


class DraftReviewInputTests(unittest.TestCase):
    def test_normalized_review_requires_queue_or_creative(self):
        with self.assertRaises(ValueError):
            DraftReviewInput.normalized(
                reviewer="Ace",
                verdict="keep_private",
                hook_score=3,
                retention_score=3,
                payoff_score=3,
                compliance_score=3,
                cta_score=3,
                asset_quality_score=3,
            )

    def test_normalized_review_validates_verdict_and_scores(self):
        with self.assertRaises(ValueError):
            DraftReviewInput.normalized(
                publish_queue_id=2,
                reviewer="Ace",
                verdict="ship_it",
                hook_score=3,
                retention_score=3,
                payoff_score=3,
                compliance_score=3,
                cta_score=3,
                asset_quality_score=3,
            )
        with self.assertRaises(ValueError):
            DraftReviewInput.normalized(
                publish_queue_id=2,
                reviewer="Ace",
                verdict="keep_private",
                hook_score=6,
                retention_score=3,
                payoff_score=3,
                compliance_score=3,
                cta_score=3,
                asset_quality_score=3,
            )

    def test_average_score_and_list_cleanup(self):
        review = DraftReviewInput.normalized(
            publish_queue_id=2,
            reviewer=" Ace ",
            verdict="revise_prompt",
            hook_score=5,
            retention_score=4,
            payoff_score=3,
            compliance_score=5,
            cta_score=4,
            asset_quality_score=3,
            blocks=["", "unreadable end card"],
            warnings=["  weak first frame  "],
            lessons=["tighten visual promise"],
        )

        self.assertEqual(review.reviewer, "Ace")
        self.assertEqual(review.average_score, 4.0)
        self.assertEqual(review.blocks, ["unreadable end card"])
        self.assertEqual(review.warnings, ["weak first frame"])


if __name__ == "__main__":
    unittest.main()
