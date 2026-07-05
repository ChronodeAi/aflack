"""N+1 query detection utility for raw SQL applications.

Since aflack uses raw psycopg cursors instead of an ORM, traditional N+1
detection tools (like Django's nplusone) don't apply. This module provides
a query counter that wraps database operations and warns when a function
executes an excessive number of queries, which is the hallmark of N+1.

Usage in tests:
    detector = NPlusOneDetector(threshold=5)
    detector.start_function("my_function")
    # ... run code that makes queries ...
    detector.record_query()  # call after each cur.execute()
    detector.check("my_function")
    assert not detector.violations
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class QueryViolation:
    function_name: str
    query_count: int
    threshold: int


@dataclass
class NPlusOneDetector:
    """Detect potential N+1 query patterns by counting queries per operation.

    Set a threshold based on expected query count. If a function exceeds
    the threshold, it likely has an N+1 pattern (e.g., querying in a loop).
    """

    threshold: int = 10
    query_count: int = 0
    violations: list[QueryViolation] = field(default_factory=list)

    def record_query(self) -> None:
        self.query_count += 1

    def check(self, function_name: str) -> None:
        if self.query_count > self.threshold:
            self.violations.append(
                QueryViolation(
                    function_name=function_name,
                    query_count=self.query_count,
                    threshold=self.threshold,
                )
            )

    def reset(self) -> None:
        self.query_count = 0
        self.violations.clear()
