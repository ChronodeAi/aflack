from __future__ import annotations

import unittest
from contextlib import contextmanager
from unittest.mock import patch

from aflack import learning
from aflack.learning import (
    Insight,
    _normalize,
    active_insights,
    dedupe_open_proposals,
    distill_insight,
    insight_hash,
    open_proposals,
    propose_improvement,
    retire_insight,
    score_creator_credibility,
    set_creator_proof,
    upsert_creator,
)


class MultiResultCursor:
    """Cursor returning queued fetchone/fetchall results per execute() call."""

    def __init__(self, *, fetchone_rows=None, fetchall_rows=None):
        self._fetchone_rows = list(fetchone_rows) if fetchone_rows is not None else []
        self._fetchall_rows = list(fetchall_rows) if fetchall_rows is not None else []
        self.executed: list[str] = []
        self.params: list = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.executed.append(sql)
        self.params.append(params)

    def fetchone(self):
        return self._fetchone_rows.pop(0) if self._fetchone_rows else None

    def fetchall(self):
        return self._fetchall_rows.pop(0) if self._fetchall_rows else []


class FakeConn:
    def __init__(self, cursor):
        self.cursor_obj = cursor
        self.committed = False

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        self.committed = True


def fake_connect(conn):
    @contextmanager
    def _cm():
        yield conn

    return _cm


class PureFunctionTests(unittest.TestCase):
    def test_normalize_collapses_whitespace_and_lowercases(self):
        self.assertEqual(_normalize("  Open   ON a\tClaim  "), "open on a claim")

    def test_insight_hash_is_stable_and_normalized(self):
        h1 = insight_hash("hook", "Open on a claim.")
        h2 = insight_hash("hook", "  open   on a claim.  ")
        self.assertEqual(h1, h2)
        self.assertEqual(len(h1), 32)

    def test_insight_hash_differs_by_scope(self):
        self.assertNotEqual(insight_hash("hook", "x"), insight_hash("cta", "x"))


class CredibilityTests(unittest.TestCase):
    def test_verified_needs_all_three_signals(self):
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=0.05, proof_monetization="affiliate", proof_consistency_days=30
            ),
            "verified",
        )

    def test_two_signals_is_plausible(self):
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=0.05, proof_monetization="affiliate", proof_consistency_days=None
            ),
            "plausible",
        )

    def test_one_signal_is_weak(self):
        self.assertEqual(
            score_creator_credibility(
                proof_engagement_rate=None, proof_monetization="sponsor", proof_consistency_days=5
            ),
            "weak",
        )

    def test_no_signals_is_unverified(self):
        self.assertEqual(
            score_creator_credibility(proof_engagement_rate=0.01, proof_monetization=None, proof_consistency_days=3),
            "unverified",
        )


class UpsertCreatorTests(unittest.TestCase):
    def test_upsert_returns_id_and_commits(self):
        conn = FakeConn(MultiResultCursor(fetchone_rows=[(21,)]))
        with patch.object(learning, "connect", fake_connect(conn)):
            creator_id = upsert_creator(platform="youtube", handle="@vice", followers=5000)

        self.assertEqual(creator_id, 21)
        self.assertTrue(conn.committed)


class SetCreatorProofTests(unittest.TestCase):
    def test_computes_credibility_and_writes(self):
        conn = FakeConn(MultiResultCursor())
        with patch.object(learning, "connect", fake_connect(conn)):
            credibility = set_creator_proof(
                21, proof_engagement_rate=0.05, proof_monetization="affiliate", proof_consistency_days=30
            )

        self.assertEqual(credibility, "verified")
        self.assertTrue(conn.committed)


class DistillInsightTests(unittest.TestCase):
    def test_new_insight_created(self):
        # First fetchone (dedup lookup) returns None -> insert path; second returns new id.
        cur = MultiResultCursor(fetchone_rows=[None, (7,)])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            insight_id, created = distill_insight(scope="hook", statement="open on a claim", confidence=0.5)

        self.assertEqual(insight_id, 7)
        self.assertTrue(created)
        self.assertTrue(conn.committed)

    def test_existing_insight_reinforced(self):
        # Dedup lookup returns a row -> update path, no new id fetch.
        cur = MultiResultCursor(fetchone_rows=[(7, 2, 0.5)])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            insight_id, created = distill_insight(scope="hook", statement="open on a claim")

        self.assertEqual(insight_id, 7)
        self.assertFalse(created)


class RetireInsightTests(unittest.TestCase):
    def test_retire_executes_update_and_commits(self):
        conn = FakeConn(MultiResultCursor())
        with patch.object(learning, "connect", fake_connect(conn)):
            retire_insight(7, reason="stale")
        self.assertTrue(conn.committed)
        self.assertIn("status = 'retired'", conn.cursor_obj.executed[0])


class ActiveInsightsTests(unittest.TestCase):
    def test_maps_rows_to_insight_objects(self):
        rows = [
            (1, "hook", "open on a claim", 0.7, 3, "active"),
            (2, "cta", "one word CTA", 0.6, 2, "active"),
        ]
        cur = MultiResultCursor(fetchall_rows=[rows])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            insights = active_insights(scope="hook", limit=5, min_confidence=0.5)

        self.assertEqual(len(insights), 2)
        self.assertIsInstance(insights[0], Insight)
        self.assertEqual(insights[0].scope, "hook")
        self.assertEqual(insights[1].confidence, 0.6)
        # scope filter adds a clause; params include min_confidence, scope, limit.
        self.assertIn("hook", conn.cursor_obj.params[0])


class ProposeImprovementTests(unittest.TestCase):
    def test_reuses_existing_proposal(self):
        # First fetchone returns an existing proposal id -> update-and-return path.
        cur = MultiResultCursor(fetchone_rows=[(15,)])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            pid = propose_improvement(
                target_type="skill",
                target_name="hook-authoring",
                change_summary="fold insights",
                rationale="repeated support",
                source_insight_ids=[1, 2],
            )
        self.assertEqual(pid, 15)
        self.assertTrue(conn.committed)

    def test_creates_new_proposal(self):
        # First fetchone (dedup) None; second returns the inserted id.
        cur = MultiResultCursor(fetchone_rows=[None, (16,)])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            pid = propose_improvement(
                target_type="rule",
                target_name="compliance-before-publish",
                change_summary="add disclosure check",
                rationale="observed gap",
            )
        self.assertEqual(pid, 16)


class OpenProposalsTests(unittest.TestCase):
    def test_maps_rows(self):
        rows = [(9, "skill", "hook-authoring", "fold insights", "proposed")]
        cur = MultiResultCursor(fetchall_rows=[rows])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            props = open_proposals(limit=10)
        self.assertEqual(props[0]["id"], 9)
        self.assertEqual(props[0]["target_name"], "hook-authoring")
        self.assertEqual(props[0]["status"], "proposed")


class DedupeOpenProposalsTests(unittest.TestCase):
    def test_supersedes_duplicates(self):
        # Group query returns one duplicate group with keep=30, dupes=[29, 28].
        group_rows = [("skill", "hook-authoring", "fold insights", [30, 29, 28])]
        # Then a source_insight_ids fetchall for the merge.
        source_rows = [([1, 2],), ([2, 3],), ([4],)]
        cur = MultiResultCursor(fetchall_rows=[group_rows, source_rows])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            count = dedupe_open_proposals()

        self.assertEqual(count, 2)  # two duplicates superseded
        self.assertTrue(conn.committed)

    def test_no_duplicates_returns_zero(self):
        cur = MultiResultCursor(fetchall_rows=[[]])
        conn = FakeConn(cur)
        with patch.object(learning, "connect", fake_connect(conn)):
            count = dedupe_open_proposals()
        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
