from __future__ import annotations

import unittest
from contextlib import contextmanager
from decimal import Decimal
from unittest.mock import patch

from aflack.analytics import (
    AnalyticsSnapshot,
    current_analytics_rollup,
    record_snapshot,
    snapshot_from_postiz_payload,
)


class FakeCursor:
    def __init__(self, responses):
        self.responses = list(responses)
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def fetchone(self):
        return self.responses.pop(0)


class FakeConnection:
    def __init__(self, responses):
        self.cursor_obj = FakeCursor(responses)
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


class AnalyticsTests(unittest.TestCase):
    def test_snapshot_normalization_rejects_negative_counters(self):
        with self.assertRaises(ValueError):
            AnalyticsSnapshot.normalized(platform="YouTube", source="manual", views=-1)

    def test_snapshot_normalization_coerces_inputs(self):
        snapshot = AnalyticsSnapshot.normalized(
            platform=" YouTube ",
            source="manual",
            views="10",
            likes="2",
            ctr="0.15",
            revenue="1.25",
        )

        self.assertEqual(snapshot.platform, "youtube")
        self.assertEqual(snapshot.views, 10)
        self.assertEqual(snapshot.likes, 2)
        self.assertEqual(snapshot.ctr, Decimal("0.15"))
        self.assertEqual(snapshot.revenue, Decimal("1.25"))

    def test_record_snapshot_persists_normalized_payload(self):
        conn = FakeConnection([(42,)])

        @contextmanager
        def fake_connect():
            yield conn

        snapshot = AnalyticsSnapshot.normalized(
            platform="youtube",
            source="manual",
            publish_queue_id=7,
            views=100,
            raw={"source": "unit-test"},
        )

        with patch("aflack.analytics.connect", fake_connect):
            snapshot_id = record_snapshot(snapshot)

        self.assertEqual(snapshot_id, 42)
        self.assertTrue(conn.committed)
        params = conn.cursor_obj.executed[0][1]
        self.assertEqual(params[0], 7)
        self.assertEqual(params[3], "youtube")
        self.assertEqual(params[7], 100)

    def test_current_rollup_can_filter_by_platform(self):
        conn = FakeConnection([(2, 150, 5, 3, 2, 1, 8, 4, Decimal("12.00"))])

        @contextmanager
        def fake_connect():
            yield conn

        with patch("aflack.analytics.connect", fake_connect):
            rollup = current_analytics_rollup(platform="YouTube")

        self.assertEqual(rollup.snapshots, 2)
        self.assertEqual(rollup.total_views, 150)
        self.assertEqual(rollup.total_conversions, 4)
        self.assertEqual(rollup.total_revenue, Decimal("12.00"))
        self.assertEqual(conn.cursor_obj.executed[0][1], ("youtube",))

    def test_snapshot_from_postiz_payload_flattens_common_metrics(self):
        snapshot = snapshot_from_postiz_payload(
            {
                "data": {
                    "postId": "post-123",
                    "views": "1000",
                    "likeCount": 40,
                    "comment_count": 5,
                    "shareCount": 3,
                    "linkClicks": 9,
                    "estimatedRevenue": "2.50",
                },
                "retention": {"0": 1.0, "10": 0.72},
            },
            platform="YouTube",
            publish_queue_id=2,
            creative_id=1,
        )

        self.assertEqual(snapshot.source, "postiz")
        self.assertEqual(snapshot.platform, "youtube")
        self.assertEqual(snapshot.source_post_id, "post-123")
        self.assertEqual(snapshot.views, 1000)
        self.assertEqual(snapshot.likes, 40)
        self.assertEqual(snapshot.comments, 5)
        self.assertEqual(snapshot.shares, 3)
        self.assertEqual(snapshot.clicks, 9)
        self.assertEqual(snapshot.revenue, Decimal("2.50"))
        self.assertEqual(snapshot.retention["10"], 0.72)


if __name__ == "__main__":
    unittest.main()
