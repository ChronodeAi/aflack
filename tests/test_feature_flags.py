from __future__ import annotations

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from aflack import feature_flags
from aflack.feature_flags import (
    FeatureFlag,
    _hash_percentage,
    get_flag,
    is_enabled,
    set_flag,
)


class FakeCursor:
    def __init__(self, row):
        self._row = row
        self.executed = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed = sql
        self.params = params

    def fetchone(self):
        return self._row


class FakeConnection:
    def __init__(self, row):
        self.cursor_obj = FakeCursor(row)
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


def _fake_connect(row):
    @contextmanager
    def _cm():
        yield FakeConnection(row)

    return _cm


class HashPercentageTests(unittest.TestCase):
    def test_hash_percentage_in_range_and_deterministic(self):
        first = _hash_percentage("flag:creator-1")
        second = _hash_percentage("flag:creator-1")
        self.assertEqual(first, second)
        self.assertGreaterEqual(first, 0)
        self.assertLess(first, 100)


class GetFlagTests(unittest.TestCase):
    def test_missing_flag_returns_none(self):
        with patch("aflack.feature_flags.connect", _fake_connect(None)):
            self.assertIsNone(get_flag("missing"))

    def test_present_flag_maps_row_to_dataclass(self):
        row = ("new_publisher", True, 50, "gradual rollout")
        with patch("aflack.feature_flags.connect", _fake_connect(row)):
            flag = get_flag("new_publisher")

        self.assertIsNotNone(flag)
        assert flag is not None  # for type-checkers
        self.assertEqual(flag.name, "new_publisher")
        self.assertTrue(flag.enabled)
        self.assertEqual(flag.rollout_percentage, 50)
        self.assertEqual(flag.description, "gradual rollout")


class IsEnabledTests(unittest.TestCase):
    def test_absent_flag_disabled(self):
        with patch.object(feature_flags, "get_flag", lambda name: None):
            self.assertFalse(is_enabled("x"))

    def test_disabled_flag_returns_false(self):
        flag = FeatureFlag("x", enabled=False, rollout_percentage=100, description="")
        with patch.object(feature_flags, "get_flag", lambda name: flag):
            self.assertFalse(is_enabled("x"))

    def test_full_rollout_returns_true(self):
        flag = FeatureFlag("x", enabled=True, rollout_percentage=100, description="")
        with patch.object(feature_flags, "get_flag", lambda name: flag):
            self.assertTrue(is_enabled("x", context_key="creator-1"))

    def test_partial_rollout_without_context_uses_positive_percentage(self):
        flag = FeatureFlag("x", enabled=True, rollout_percentage=25, description="")
        with patch.object(feature_flags, "get_flag", lambda name: flag):
            self.assertTrue(is_enabled("x"))

    def test_zero_percentage_without_context_is_false(self):
        flag = FeatureFlag("x", enabled=True, rollout_percentage=0, description="")
        with patch.object(feature_flags, "get_flag", lambda name: flag):
            self.assertFalse(is_enabled("x"))

    def test_partial_rollout_with_context_uses_hash_bucket(self):
        flag = FeatureFlag("x", enabled=True, rollout_percentage=40, description="")
        with patch.object(feature_flags, "get_flag", lambda name: flag):
            with patch.object(feature_flags, "_hash_percentage", lambda key: 10):
                self.assertTrue(is_enabled("x", context_key="creator-1"))
            with patch.object(feature_flags, "_hash_percentage", lambda key: 90):
                self.assertFalse(is_enabled("x", context_key="creator-1"))


class SetFlagTests(unittest.TestCase):
    def test_set_flag_executes_upsert_and_commits(self):
        conn = FakeConnection(None)

        @contextmanager
        def _cm():
            yield conn

        with patch("aflack.feature_flags.connect", _cm):
            set_flag("beta", enabled=True, rollout_percentage=30, description="beta gate")

        self.assertTrue(conn.committed)
        self.assertIn("INSERT INTO feature_flags", conn.cursor_obj.executed)
        self.assertEqual(conn.cursor_obj.params, ("beta", True, 30, "beta gate"))


if __name__ == "__main__":
    unittest.main()
