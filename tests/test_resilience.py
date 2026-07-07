from __future__ import annotations

import unittest

from aflack.resilience import CircuitBreaker, with_retry


class WithRetryTests(unittest.TestCase):
    def test_retries_transient_error_then_succeeds(self):
        calls = {"count": 0}

        @with_retry(max_attempts=3, base_delay=0.0, max_delay=0.0)
        def flaky() -> str:
            calls["count"] += 1
            if calls["count"] < 2:
                raise ConnectionError("transient")
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(calls["count"], 2)

    def test_non_retryable_error_raised_immediately(self):
        calls = {"count": 0}

        @with_retry(max_attempts=3, base_delay=0.0, max_delay=0.0)
        def boom() -> None:
            calls["count"] += 1
            raise ValueError("not transient")

        with self.assertRaises(ValueError):
            boom()
        self.assertEqual(calls["count"], 1)

    def test_reraises_after_max_attempts(self):
        calls = {"count": 0}

        @with_retry(max_attempts=2, base_delay=0.0, max_delay=0.0)
        def always_fails() -> None:
            calls["count"] += 1
            raise TimeoutError("still down")

        with self.assertRaises(TimeoutError):
            always_fails()
        self.assertEqual(calls["count"], 2)


class CircuitBreakerTests(unittest.TestCase):
    def test_starts_closed_and_allows_execution(self):
        breaker = CircuitBreaker(failure_threshold=3)

        self.assertEqual(breaker.state, "closed")
        self.assertTrue(breaker.can_execute())

    def test_opens_after_reaching_failure_threshold(self):
        breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=60.0)

        breaker.record_failure()
        self.assertEqual(breaker.state, "closed")
        breaker.record_failure()

        self.assertEqual(breaker.state, "open")
        self.assertFalse(breaker.can_execute())

    def test_success_resets_to_closed(self):
        breaker = CircuitBreaker(failure_threshold=1)
        breaker.record_failure()
        self.assertEqual(breaker.state, "open")

        breaker.record_success()

        self.assertEqual(breaker.state, "closed")
        self.assertTrue(breaker.can_execute())

    def test_cooldown_elapsed_moves_to_half_open(self):
        breaker = CircuitBreaker(failure_threshold=1, cooldown_seconds=0.0)
        breaker.record_failure()
        self.assertEqual(breaker.state, "open")

        # With a zero-second cooldown, the elapsed check passes immediately.
        self.assertTrue(breaker.can_execute())
        self.assertEqual(breaker.state, "half-open")


if __name__ == "__main__":
    unittest.main()
