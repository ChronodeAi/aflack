from __future__ import annotations

import unittest
from contextlib import contextmanager
from decimal import Decimal
from unittest.mock import patch

from aflack.economics import current_rollup


class FakeCursor:
    def __init__(self, responses):
        self.responses = list(responses)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        return None

    def fetchone(self):
        return self.responses.pop(0)


class FakeConnection:
    def __init__(self, responses):
        self.responses = responses

    def cursor(self):
        return FakeCursor(self.responses)


class EconomicsRollupTests(unittest.TestCase):
    def test_current_rollup_calculates_margin_and_cost_per_generated(self):
        responses = [
            (Decimal("12.50"),),
            (Decimal("50.00"),),
            (5,),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(responses)

        with patch("aflack.economics.connect", fake_connect):
            rollup = current_rollup()

        self.assertEqual(rollup.total_cost, Decimal("12.50"))
        self.assertEqual(rollup.revenue, Decimal("50.00"))
        self.assertEqual(rollup.contribution_margin, Decimal("37.50"))
        self.assertEqual(rollup.generated_creatives, 5)
        self.assertEqual(rollup.cost_per_generated, Decimal("2.50"))

    def test_current_rollup_avoids_division_by_zero(self):
        responses = [
            (Decimal("12.50"),),
            (Decimal("0"),),
            (0,),
        ]

        @contextmanager
        def fake_connect():
            yield FakeConnection(responses)

        with patch("aflack.economics.connect", fake_connect):
            rollup = current_rollup()

        self.assertEqual(rollup.contribution_margin, Decimal("-12.50"))
        self.assertIsNone(rollup.cost_per_generated)


if __name__ == "__main__":
    unittest.main()
