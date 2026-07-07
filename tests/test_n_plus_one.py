from __future__ import annotations

import unittest

from aflack.n_plus_one import NPlusOneDetector, QueryViolation


class NPlusOneDetectorTests(unittest.TestCase):
    def test_below_threshold_has_no_violations(self):
        detector = NPlusOneDetector(threshold=5)
        for _ in range(5):
            detector.record_query()

        detector.check("safe_function")

        self.assertEqual(detector.query_count, 5)
        self.assertEqual(detector.violations, [])

    def test_over_threshold_records_violation(self):
        detector = NPlusOneDetector(threshold=3)
        for _ in range(7):
            detector.record_query()

        detector.check("chatty_function")

        self.assertEqual(len(detector.violations), 1)
        violation = detector.violations[0]
        self.assertIsInstance(violation, QueryViolation)
        self.assertEqual(violation.function_name, "chatty_function")
        self.assertEqual(violation.query_count, 7)
        self.assertEqual(violation.threshold, 3)

    def test_reset_clears_count_and_violations(self):
        detector = NPlusOneDetector(threshold=1)
        detector.record_query()
        detector.record_query()
        detector.check("loop_query")
        self.assertTrue(detector.violations)

        detector.reset()

        self.assertEqual(detector.query_count, 0)
        self.assertEqual(detector.violations, [])

    def test_default_threshold(self):
        detector = NPlusOneDetector()
        self.assertEqual(detector.threshold, 10)


if __name__ == "__main__":
    unittest.main()
