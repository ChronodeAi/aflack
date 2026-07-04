"""Learning layer: benchmark intelligence, insight distillation, and proposals.

This module turns observed competitor content into deduplicated, temporally
valid insights, and insights into concrete improvement proposals for our own
skills/rules/workflows/agents. It is the "continually improve" core.

Anti-rot principles:
- Dedup: insights key on a normalized content_hash; re-observing an insight
  strengthens it (support_count, confidence) instead of duplicating it.
- Temporal validity: insights can be retired (invalid_at) so stale patterns do
  not accumulate in the context window.
- Evidence-bound: benchmark creators require proof of REAL success, not vanity
  metrics, before they reach `verified` credibility.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any

from .db import connect


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def insight_hash(scope: str, statement: str) -> str:
    return hashlib.sha256(f"{scope}::{_normalize(statement)}".encode()).hexdigest()[:32]


@dataclass(frozen=True)
class Insight:
    id: int
    scope: str
    statement: str
    confidence: float
    support_count: int
    status: str


# --- Benchmark creators -------------------------------------------------------

def upsert_creator(
    *,
    platform: str,
    handle: str,
    display_name: str | None = None,
    niche: str | None = None,
    followers: int | None = None,
    source_url: str | None = None,
    metadata: dict[str, Any] | None = None,
) -> int:
    """Insert or update a benchmark creator candidate."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO benchmark_creators
              (platform, handle, display_name, niche, followers, source_url, metadata)
            VALUES (%s, %s, %s, %s, %s, %s, %s::jsonb)
            ON CONFLICT (platform, handle) DO UPDATE SET
              display_name = COALESCE(EXCLUDED.display_name, benchmark_creators.display_name),
              niche = COALESCE(EXCLUDED.niche, benchmark_creators.niche),
              followers = COALESCE(EXCLUDED.followers, benchmark_creators.followers),
              source_url = COALESCE(EXCLUDED.source_url, benchmark_creators.source_url),
              updated_at = now()
            RETURNING id
            """,
            (platform, handle, display_name, niche, followers, source_url, json.dumps(metadata or {})),
        )
        creator_id = cur.fetchone()[0]
        conn.commit()
        return int(creator_id)


def score_creator_credibility(
    *,
    proof_engagement_rate: float | None,
    proof_monetization: str | None,
    proof_consistency_days: int | None,
) -> str:
    """Grade REAL success signals, not vanity metrics.

    A creator only reaches `verified` when there is observable monetization AND a
    real engagement rate AND a sustained posting cadence. Follower count alone
    never grants credibility.
    """

    signals = 0
    if proof_engagement_rate is not None and proof_engagement_rate >= 0.02:
        signals += 1
    if proof_monetization:
        signals += 1
    if proof_consistency_days is not None and proof_consistency_days >= 14:
        signals += 1

    if signals >= 3:
        return "verified"
    if signals == 2:
        return "plausible"
    if signals == 1:
        return "weak"
    return "unverified"


def set_creator_proof(
    creator_id: int,
    *,
    proof_engagement_rate: float | None = None,
    proof_monetization: str | None = None,
    proof_consistency_days: int | None = None,
    proof_notes: str | None = None,
) -> str:
    """Attach proof-of-success and recompute credibility. Returns credibility."""

    credibility = score_creator_credibility(
        proof_engagement_rate=proof_engagement_rate,
        proof_monetization=proof_monetization,
        proof_consistency_days=proof_consistency_days,
    )
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE benchmark_creators SET
              proof_engagement_rate = %s,
              proof_monetization = %s,
              proof_consistency_days = %s,
              proof_notes = %s,
              credibility = %s,
              updated_at = now()
            WHERE id = %s
            """,
            (proof_engagement_rate, proof_monetization, proof_consistency_days,
             proof_notes, credibility, creator_id),
        )
        conn.commit()
    return credibility


# --- Insights (deduped, temporally valid) ------------------------------------

def distill_insight(
    *,
    scope: str,
    statement: str,
    evidence: list[dict[str, Any]] | None = None,
    confidence: float = 0.5,
) -> tuple[int, bool]:
    """Create or strengthen an insight.

    Returns (insight_id, created). If the insight already exists (same hash),
    it is reinforced: support_count += 1 and confidence nudged upward, capped.
    """

    h = insight_hash(scope, statement)
    with connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, support_count, confidence FROM insights WHERE content_hash = %s", (h,))
        row = cur.fetchone()
        if row:
            insight_id, support_count, existing_conf = row
            new_conf = min(1.0, float(existing_conf) + 0.1)
            cur.execute(
                """
                UPDATE insights SET
                  support_count = support_count + 1,
                  confidence = %s,
                  evidence = evidence || %s::jsonb,
                  status = 'active',
                  invalid_at = NULL,
                  updated_at = now()
                WHERE id = %s
                """,
                (new_conf, json.dumps(evidence or []), insight_id),
            )
            conn.commit()
            return int(insight_id), False

        cur.execute(
            """
            INSERT INTO insights (scope, statement, evidence, confidence, content_hash)
            VALUES (%s, %s, %s::jsonb, %s, %s)
            RETURNING id
            """,
            (scope, statement, json.dumps(evidence or []), confidence, h),
        )
        insight_id = cur.fetchone()[0]
        conn.commit()
        return int(insight_id), True


def retire_insight(insight_id: int, reason: str = "") -> None:
    """Mark an insight retired so it stops feeding the active context."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            UPDATE insights SET status = 'retired', invalid_at = now(),
              metadata = metadata || %s::jsonb, updated_at = now()
            WHERE id = %s
            """,
            (json.dumps({"retire_reason": reason}), insight_id),
        )
        conn.commit()


def active_insights(scope: str | None = None, limit: int = 20, min_confidence: float = 0.0) -> list[Insight]:
    """Return active insights, highest-confidence first (relevance-gated retrieval)."""

    clauses = ["status = 'active'", "confidence >= %s"]
    params: list[Any] = [min_confidence]
    if scope:
        clauses.append("scope = %s")
        params.append(scope)
    params.append(limit)
    where = " AND ".join(clauses)
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT id, scope, statement, confidence, support_count, status
            FROM insights
            WHERE {where}
            ORDER BY confidence DESC, support_count DESC, updated_at DESC
            LIMIT %s
            """,
            params,
        )
        return [Insight(*row) for row in cur.fetchall()]


# --- Improvement proposals ---------------------------------------------------

def propose_improvement(
    *,
    target_type: str,
    target_name: str,
    change_summary: str,
    rationale: str,
    source_insight_ids: list[int] | None = None,
) -> int:
    """Record a concrete proposal to evolve a skill/rule/workflow/agent.

    Identical open or already-applied proposals are reused instead of duplicated;
    repeated daemon cycles should reinforce insights, not spam the operator with
    the same ask.
    """

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id
            FROM improvement_proposals
            WHERE target_type = %s
              AND target_name = %s
              AND change_summary = %s
              AND status IN ('proposed', 'approved', 'applied')
            ORDER BY
              CASE status
                WHEN 'proposed' THEN 1
                WHEN 'approved' THEN 2
                WHEN 'applied' THEN 3
                ELSE 4
              END,
              created_at DESC
            LIMIT 1
            """,
            (target_type, target_name, change_summary),
        )
        row = cur.fetchone()
        if row:
            proposal_id = row[0]
            cur.execute(
                """
                UPDATE improvement_proposals
                SET source_insight_ids = (
                    SELECT ARRAY(
                      SELECT DISTINCT unnest(source_insight_ids || %s::bigint[])
                    )
                  ),
                  updated_at = now()
                WHERE id = %s
                """,
                (source_insight_ids or [], proposal_id),
            )
            conn.commit()
            return int(proposal_id)

        cur.execute(
            """
            INSERT INTO improvement_proposals
              (target_type, target_name, change_summary, rationale, source_insight_ids)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
            """,
            (target_type, target_name, change_summary, rationale, source_insight_ids or []),
        )
        proposal_id = cur.fetchone()[0]
        conn.commit()
        return int(proposal_id)


def open_proposals(limit: int = 50) -> list[dict[str, Any]]:
    """Return proposals awaiting human decision (proposed/approved, not applied)."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, target_type, target_name, change_summary, status
            FROM improvement_proposals
            WHERE status IN ('proposed', 'approved')
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        )
        return [
            {"id": r[0], "target_type": r[1], "target_name": r[2],
             "change_summary": r[3], "status": r[4]}
            for r in cur.fetchall()
        ]


def dedupe_open_proposals() -> int:
    """Supersede duplicate open proposals, keeping the newest copy.

    Returns the number of proposals marked superseded.
    """

    superseded = 0
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT target_type, target_name, change_summary, array_agg(id ORDER BY created_at DESC)
            FROM improvement_proposals
            WHERE status IN ('proposed', 'approved')
            GROUP BY target_type, target_name, change_summary
            HAVING count(*) > 1
            """
        )
        groups = cur.fetchall()
        for _target_type, _target_name, _change_summary, ids in groups:
            keep_id, duplicate_ids = ids[0], ids[1:]
            if not duplicate_ids:
                continue
            cur.execute(
                "SELECT source_insight_ids FROM improvement_proposals WHERE id = ANY(%s)",
                ([keep_id, *duplicate_ids],),
            )
            merged_set: set[int] = set()
            for row in cur.fetchall():
                for insight_id in row[0] or []:
                    merged_set.add(int(insight_id))
            merged_sources = sorted(merged_set)
            cur.execute(
                """
                UPDATE improvement_proposals
                SET source_insight_ids = %s,
                    updated_at = now()
                WHERE id = %s
                """,
                (merged_sources, keep_id),
            )
            cur.execute(
                """
                UPDATE improvement_proposals
                SET status = 'superseded',
                    updated_at = now(),
                    metadata = metadata || %s::jsonb
                WHERE id = ANY(%s)
                """,
                (json.dumps({"superseded_by": keep_id}), duplicate_ids),
            )
            superseded += len(duplicate_ids)
        conn.commit()
    return superseded
