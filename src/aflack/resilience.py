"""Resilience patterns for external service calls.

Provides circuit breaker and retry-with-backoff patterns for calls to external
services like the Postiz API. Prevents cascading failures and handles transient
errors gracefully.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

T = TypeVar("T")


def with_retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator: retry with exponential backoff and jitter."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential_jitter(initial=base_delay, max=max_delay),
            retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
            reraise=True,
        )(func)

    return decorator


class CircuitBreaker:
    """Simple circuit breaker for external service calls.

    Tracks failures and opens the circuit after a threshold, preventing
    further calls until a cooldown period elapses.
    """

    def __init__(self, *, failure_threshold: int = 5, cooldown_seconds: float = 60.0) -> None:
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds
        self._failure_count = 0
        self._state: str = "closed"
        self._opened_at: float = 0.0

    @property
    def state(self) -> str:
        return self._state

    def record_success(self) -> None:
        self._failure_count = 0
        self._state = "closed"

    def record_failure(self) -> None:
        self._failure_count += 1
        if self._failure_count >= self.failure_threshold:
            self._state = "open"
            import time

            self._opened_at = time.monotonic()

    def can_execute(self) -> bool:
        if self._state == "closed":
            return True
        if self._state == "open":
            import time

            if time.monotonic() - self._opened_at >= self.cooldown_seconds:
                self._state = "half-open"
                return True
            return False
        return True
