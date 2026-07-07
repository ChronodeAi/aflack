"""Structured draft/render review capture for the publish-quality learning loop."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal

from .db import connect, fetchone_required

DraftVerdict = Literal["keep_private", "revise_prompt", "revise_script", "publish_candidate", "kill"]
VALID_VERDICTS: set[str] = {"keep_private", "revise_prompt", "revise_script", "publish_candidate", "kill"}


def _score(value: int, name: str) -> int:
    parsed = int(value)
    if parsed < 1 or parsed > 5:
        raise ValueError(f"{name} must be between 1 and 5")
    return parsed


def _string_items(values: list[str] | None) -> list[str]:
    return [value.strip() for value in values or [] if value.strip()]


@dataclass(frozen=True)
class DraftReviewInput:
    publish_queue_id: int | None
    creative_id: int | None
    reviewer: str
    verdict: DraftVerdict
    hook_score: int
    retention_score: int
    payoff_score: int
    compliance_score: int
    cta_score: int
    asset_quality_score: int
    blocks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    lessons: list[str] = field(default_factory=list)
    policy_update_candidate: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def normalized(
        cls,
        *,
        publish_queue_id: int | None = None,
        creative_id: int | None = None,
        reviewer: str,
        verdict: str,
        hook_score: int,
        retention_score: int,
        payoff_score: int,
        compliance_score: int,
        cta_score: int,
        asset_quality_score: int,
        blocks: list[str] | None = None,
        warnings: list[str] | None = None,
        lessons: list[str] | None = None,
        policy_update_candidate: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> DraftReviewInput:
        if publish_queue_id is None and creative_id is None:
            raise ValueError("publish_queue_id or creative_id is required")
        if not reviewer.strip():
            raise ValueError("reviewer is required")
        normalized_verdict = verdict.strip().replace("-", "_")
        if normalized_verdict not in VALID_VERDICTS:
            raise ValueError(f"verdict must be one of: {', '.join(sorted(VALID_VERDICTS))}")
        return cls(
            publish_queue_id=publish_queue_id,
            creative_id=creative_id,
            reviewer=reviewer.strip(),
            verdict=normalized_verdict,  # type: ignore[arg-type]
            hook_score=_score(hook_score, "hook_score"),
            retention_score=_score(retention_score, "retention_score"),
            payoff_score=_score(payoff_score, "payoff_score"),
            compliance_score=_score(compliance_score, "compliance_score"),
            cta_score=_score(cta_score, "cta_score"),
            asset_quality_score=_score(asset_quality_score, "asset_quality_score"),
            blocks=_string_items(blocks),
            warnings=_string_items(warnings),
            lessons=_string_items(lessons),
            policy_update_candidate=(policy_update_candidate or "").strip() or None,
            metadata=metadata or {},
        )

    @property
    def average_score(self) -> float:
        scores = [
            self.hook_score,
            self.retention_score,
            self.payoff_score,
            self.compliance_score,
            self.cta_score,
            self.asset_quality_score,
        ]
        return round(sum(scores) / len(scores), 2)


@dataclass(frozen=True)
class DraftReviewRollup:
    reviews: int
    publish_candidates: int
    keep_private: int
    revise_prompt: int
    revise_script: int
    killed: int
    avg_hook: float
    avg_retention: float
    avg_payoff: float
    avg_compliance: float
    avg_cta: float
    avg_asset_quality: float


def record_draft_review(review: DraftReviewInput) -> int:
    """Persist a structured review and return its id."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO draft_reviews (
              publish_queue_id, creative_id, reviewer, verdict,
              hook_score, retention_score, payoff_score, compliance_score,
              cta_score, asset_quality_score, blocks, warnings, lessons,
              policy_update_candidate, metadata
            )
            VALUES (
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s::jsonb, %s::jsonb, %s::jsonb, %s, %s::jsonb
            )
            RETURNING id
            """,
            (
                review.publish_queue_id,
                review.creative_id,
                review.reviewer,
                review.verdict,
                review.hook_score,
                review.retention_score,
                review.payoff_score,
                review.compliance_score,
                review.cta_score,
                review.asset_quality_score,
                json.dumps(review.blocks),
                json.dumps(review.warnings),
                json.dumps(review.lessons),
                review.policy_update_candidate,
                json.dumps(review.metadata),
            ),
        )
        review_id = fetchone_required(cur)[0]
        conn.commit()
        return int(review_id)


def draft_review_rollup() -> DraftReviewRollup:
    """Return aggregate review counts and score averages."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT
              COUNT(*)::bigint,
              COUNT(*) FILTER (WHERE verdict = 'publish_candidate')::bigint,
              COUNT(*) FILTER (WHERE verdict = 'keep_private')::bigint,
              COUNT(*) FILTER (WHERE verdict = 'revise_prompt')::bigint,
              COUNT(*) FILTER (WHERE verdict = 'revise_script')::bigint,
              COUNT(*) FILTER (WHERE verdict = 'kill')::bigint,
              COALESCE(AVG(hook_score), 0),
              COALESCE(AVG(retention_score), 0),
              COALESCE(AVG(payoff_score), 0),
              COALESCE(AVG(compliance_score), 0),
              COALESCE(AVG(cta_score), 0),
              COALESCE(AVG(asset_quality_score), 0)
            FROM draft_reviews
            """
        )
        row = fetchone_required(cur)
    return DraftReviewRollup(
        reviews=int(row[0]),
        publish_candidates=int(row[1]),
        keep_private=int(row[2]),
        revise_prompt=int(row[3]),
        revise_script=int(row[4]),
        killed=int(row[5]),
        avg_hook=round(float(row[6]), 2),
        avg_retention=round(float(row[7]), 2),
        avg_payoff=round(float(row[8]), 2),
        avg_compliance=round(float(row[9]), 2),
        avg_cta=round(float(row[10]), 2),
        avg_asset_quality=round(float(row[11]), 2),
    )
