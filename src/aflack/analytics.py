"""Analytics ingestion and rollups for the content loop."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Literal

from .db import connect, fetchone_required

AnalyticsSource = Literal["postiz", "youtube", "tiktok", "instagram", "manual", "other"]


def _non_negative_int(value: int | str | None) -> int:
    if value is None or value == "":
        return 0
    parsed = int(value)
    if parsed < 0:
        raise ValueError("analytics counters must be non-negative")
    return parsed


def _optional_decimal(value: Decimal | int | float | str | None) -> Decimal | None:
    if value in (None, ""):
        return None
    parsed = Decimal(str(value))
    if parsed < 0:
        raise ValueError("analytics decimal values must be non-negative")
    return parsed


def _decimal_or_zero(value: Decimal | int | float | str | None) -> Decimal:
    return _optional_decimal(value) or Decimal("0")


def _first_metric(payload: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def _flatten_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    """Flatten common analytics envelopes while preserving raw separately."""

    flat: dict[str, Any] = {}
    for key, value in payload.items():
        if key in {"data", "analytics", "metrics", "post", "summary"} and isinstance(value, dict):
            flat.update(_flatten_metrics(value))
        elif not isinstance(value, (dict, list)):
            flat[key] = value
    return flat


@dataclass(frozen=True)
class AnalyticsSnapshot:
    platform: str
    source: AnalyticsSource
    publish_queue_id: int | None = None
    creative_id: int | None = None
    channel_id: int | None = None
    source_post_id: str | None = None
    platform_url: str | None = None
    views: int = 0
    likes: int = 0
    comments: int = 0
    shares: int = 0
    saves: int = 0
    clicks: int = 0
    conversions: int = 0
    watch_time_seconds: Decimal | None = None
    average_view_duration_seconds: Decimal | None = None
    average_percentage_viewed: Decimal | None = None
    ctr: Decimal | None = None
    revenue: Decimal = Decimal("0")
    retention: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)
    captured_at: datetime | None = None

    @classmethod
    def normalized(
        cls,
        *,
        platform: str,
        source: AnalyticsSource,
        publish_queue_id: int | None = None,
        creative_id: int | None = None,
        channel_id: int | None = None,
        source_post_id: str | None = None,
        platform_url: str | None = None,
        views: int | str | None = 0,
        likes: int | str | None = 0,
        comments: int | str | None = 0,
        shares: int | str | None = 0,
        saves: int | str | None = 0,
        clicks: int | str | None = 0,
        conversions: int | str | None = 0,
        watch_time_seconds: Decimal | int | float | str | None = None,
        average_view_duration_seconds: Decimal | int | float | str | None = None,
        average_percentage_viewed: Decimal | int | float | str | None = None,
        ctr: Decimal | int | float | str | None = None,
        revenue: Decimal | int | float | str | None = 0,
        retention: dict[str, Any] | None = None,
        raw: dict[str, Any] | None = None,
        captured_at: datetime | None = None,
    ) -> AnalyticsSnapshot:
        if not platform.strip():
            raise ValueError("platform is required")
        return cls(
            platform=platform.strip().lower(),
            source=source,
            publish_queue_id=publish_queue_id,
            creative_id=creative_id,
            channel_id=channel_id,
            source_post_id=(source_post_id or None),
            platform_url=(platform_url or None),
            views=_non_negative_int(views),
            likes=_non_negative_int(likes),
            comments=_non_negative_int(comments),
            shares=_non_negative_int(shares),
            saves=_non_negative_int(saves),
            clicks=_non_negative_int(clicks),
            conversions=_non_negative_int(conversions),
            watch_time_seconds=_optional_decimal(watch_time_seconds),
            average_view_duration_seconds=_optional_decimal(average_view_duration_seconds),
            average_percentage_viewed=_optional_decimal(average_percentage_viewed),
            ctr=_optional_decimal(ctr),
            revenue=_decimal_or_zero(revenue),
            retention=retention or {},
            raw=raw or {},
            captured_at=captured_at,
        )


def snapshot_from_postiz_payload(
    payload: dict[str, Any],
    *,
    platform: str,
    publish_queue_id: int | None = None,
    creative_id: int | None = None,
    channel_id: int | None = None,
    postiz_post_id: str | None = None,
    platform_url: str | None = None,
) -> AnalyticsSnapshot:
    """Normalize a Postiz analytics response into the local snapshot schema."""

    flat = _flatten_metrics(payload)
    source_post_id = str(
        _first_metric(flat, "postId", "post_id", "id", "releaseId", "release_id") or postiz_post_id or ""
    )
    return AnalyticsSnapshot.normalized(
        platform=platform,
        source="postiz",
        publish_queue_id=publish_queue_id,
        creative_id=creative_id,
        channel_id=channel_id,
        source_post_id=source_post_id or None,
        platform_url=platform_url or _first_metric(flat, "url", "platformUrl", "platform_url", "link"),
        views=_first_metric(flat, "views", "viewCount", "view_count", "impressions", "plays"),
        likes=_first_metric(flat, "likes", "likeCount", "like_count"),
        comments=_first_metric(flat, "comments", "commentCount", "comment_count"),
        shares=_first_metric(flat, "shares", "shareCount", "share_count", "reposts"),
        saves=_first_metric(flat, "saves", "saveCount", "save_count", "bookmarks"),
        clicks=_first_metric(flat, "clicks", "clickCount", "click_count", "linkClicks", "link_clicks"),
        conversions=_first_metric(flat, "conversions", "conversionCount", "conversion_count"),
        watch_time_seconds=_first_metric(flat, "watchTimeSeconds", "watch_time_seconds", "watchTime", "watch_time"),
        average_view_duration_seconds=_first_metric(
            flat,
            "averageViewDurationSeconds",
            "average_view_duration_seconds",
            "avgViewDuration",
            "avg_view_duration",
        ),
        average_percentage_viewed=_first_metric(
            flat,
            "averagePercentageViewed",
            "average_percentage_viewed",
            "avgPercentViewed",
            "avg_percent_viewed",
        ),
        ctr=_first_metric(flat, "ctr", "clickThroughRate", "click_through_rate"),
        revenue=_first_metric(flat, "revenue", "estimatedRevenue", "estimated_revenue"),
        retention=payload.get("retention") if isinstance(payload.get("retention"), dict) else {},
        raw=payload,
    )


@dataclass(frozen=True)
class AnalyticsRollup:
    snapshots: int
    total_views: int
    total_likes: int
    total_comments: int
    total_shares: int
    total_saves: int
    total_clicks: int
    total_conversions: int
    total_revenue: Decimal


def record_snapshot(snapshot: AnalyticsSnapshot) -> int:
    """Persist one analytics snapshot and return its id."""

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO analytics_snapshots (
              publish_queue_id, creative_id, channel_id, platform, source,
              source_post_id, platform_url, views, likes, comments, shares,
              saves, clicks, conversions, watch_time_seconds,
              average_view_duration_seconds, average_percentage_viewed, ctr,
              revenue, retention, raw, captured_at
            )
            VALUES (
              %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
              %s, %s, %s, %s, %s, %s::jsonb, %s::jsonb, COALESCE(%s, now())
            )
            RETURNING id
            """,
            (
                snapshot.publish_queue_id,
                snapshot.creative_id,
                snapshot.channel_id,
                snapshot.platform,
                snapshot.source,
                snapshot.source_post_id,
                snapshot.platform_url,
                snapshot.views,
                snapshot.likes,
                snapshot.comments,
                snapshot.shares,
                snapshot.saves,
                snapshot.clicks,
                snapshot.conversions,
                snapshot.watch_time_seconds,
                snapshot.average_view_duration_seconds,
                snapshot.average_percentage_viewed,
                snapshot.ctr,
                snapshot.revenue,
                json.dumps(snapshot.retention),
                json.dumps(snapshot.raw),
                snapshot.captured_at,
            ),
        )
        snapshot_id = int(fetchone_required(cur)[0])
        conn.commit()
        return snapshot_id


def current_analytics_rollup(platform: str | None = None) -> AnalyticsRollup:
    """Return aggregate metrics across analytics snapshots."""

    where = ""
    params: tuple[str, ...] = ()
    if platform:
        where = "WHERE platform = %s"
        params = (platform.strip().lower(),)

    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            f"""
            SELECT
              COUNT(*),
              COALESCE(SUM(views), 0),
              COALESCE(SUM(likes), 0),
              COALESCE(SUM(comments), 0),
              COALESCE(SUM(shares), 0),
              COALESCE(SUM(saves), 0),
              COALESCE(SUM(clicks), 0),
              COALESCE(SUM(conversions), 0),
              COALESCE(SUM(revenue), 0)
            FROM analytics_snapshots
            {where}
            """,
            params,
        )
        row = fetchone_required(cur)

    return AnalyticsRollup(
        snapshots=int(row[0]),
        total_views=int(row[1]),
        total_likes=int(row[2]),
        total_comments=int(row[3]),
        total_shares=int(row[4]),
        total_saves=int(row[5]),
        total_clicks=int(row[6]),
        total_conversions=int(row[7]),
        total_revenue=row[8],
    )
