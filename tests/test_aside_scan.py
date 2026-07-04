from __future__ import annotations

import unittest

from aflack.aside_scan import (
    canonical_platform,
    coerce_int,
    compute_engagement_rate,
    observation_content_hash,
)


class AsideScanPureLogicTests(unittest.TestCase):
    def test_coerce_int_social_suffixes(self):
        self.assertEqual(coerce_int("1.2M"), 1_200_000)
        self.assertEqual(coerce_int("45k"), 45_000)
        self.assertEqual(coerce_int("12,345"), 12_345)
        self.assertIsNone(coerce_int("unknown"))

    def test_compute_engagement_rate_prefers_views(self):
        obs = {
            "views": "100k",
            "followers": "1m",
            "likes": "5k",
            "comments": 100,
            "saves": 400,
            "shares": 500,
        }
        self.assertAlmostEqual(compute_engagement_rate(obs), 0.06)

    def test_canonical_platform_accepts_composite_sources(self):
        self.assertEqual(canonical_platform("youtube/public_web"), "youtube")
        self.assertEqual(canonical_platform("public_web/tiktok/instagram/youtube"), "tiktok")
        self.assertEqual(canonical_platform("skool/public_web"), "other")

    def test_observation_content_hash_is_stable(self):
        a = observation_content_hash(
            {
                "platform": "TikTok",
                "handle": "@Creator",
                "url": "https://example.com/video/1",
                "title": "Hook",
                "hook_text": "First line",
            }
        )
        b = observation_content_hash(
            {
                "platform": "tiktok",
                "handle": "creator",
                "url": "https://example.com/video/1",
                "title": "hook",
                "hook_text": "first line",
            }
        )
        self.assertEqual(a, b)


if __name__ == "__main__":
    unittest.main()
