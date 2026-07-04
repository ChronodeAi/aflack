"""Aside scan ingestion for Instagram/TikTok creator research.

The browser/Aside layer gathers observations from logged-in Instagram/TikTok
sessions and writes them as JSON. This module imports that JSON into the local
source-of-truth tables without scraping private APIs or fabricating data.

Contract:
{
  "source": "aside",
  "niche": "gta6-ai-persona-gaming",
  "observations": [
    {
      "platform": "instagram" | "tiktok" | "youtube",
      "handle": "creator_handle",
      "display_name": "Creator",
      "profile_url": "https://...",
      "followers": 12345,
      "url": "https://.../reel/...",
      "title": "...",
      "hook_text": "...",
      "format": "short",
      "views": 100000,
      "likes": 5000,
      "comments": 200,
      "saves": 1000,
      "shares": 800,
      "cta_pattern": "comment keyword",
      "structure": {"beats": [...]},
      "proof_monetization": "affiliate/course/sponsor/...",
      "proof_consistency_days": 30,
      "proof_notes": "Why this creator appears genuinely successful"
    }
  ]
}
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .db import connect
from .learning import set_creator_proof, upsert_creator
from .tracing import new_trace_id, record_event


@dataclass(frozen=True)
class ImportSummary:
    trace_id: str
    observations_seen: int
    creators_upserted: int
    videos_inserted: int
    videos_duplicate: int
    creators_verified_or_plausible: int


def coerce_int(value: Any) -> int | None:
    """Parse social metric strings like `1.2M`, `45k`, or `12,300`."""

    if value is None or value == "":
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = str(value).strip().lower().replace(",", "")
    multiplier = 1
    if text.endswith("k"):
        multiplier = 1_000
        text = text[:-1]
    elif text.endswith("m"):
        multiplier = 1_000_000
        text = text[:-1]
    elif text.endswith("b"):
        multiplier = 1_000_000_000
        text = text[:-1]
    try:
        return int(float(text) * multiplier)
    except ValueError:
        return None


def compute_engagement_rate(obs: dict[str, Any]) -> float | None:
    """Compute engagement from observable metrics; prefer views denominator."""

    likes = coerce_int(obs.get("likes")) or 0
    comments = coerce_int(obs.get("comments")) or 0
    saves = coerce_int(obs.get("saves")) or 0
    shares = coerce_int(obs.get("shares")) or 0
    views = coerce_int(obs.get("views"))
    followers = coerce_int(obs.get("followers"))
    denominator = views or followers
    if not denominator:
        return None
    return (likes + comments + saves + shares) / denominator


def canonical_platform(value: Any) -> str:
    """Map composite scan source labels to the database platform enum."""

    text = str(value or "other").strip().lower()
    allowed = {"instagram", "tiktok", "youtube", "x"}
    for part in text.split("/"):
        if part in allowed:
            return part
    return text if text in {"instagram", "tiktok", "youtube", "x"} else "other"


def observation_content_hash(obs: dict[str, Any]) -> str:
    """Stable dedup key for observations even when URLs are absent/unstable."""

    parts = []
    for key in ("platform", "handle", "url", "title", "hook_text"):
        value = str(obs.get(key, "") or "").strip().lower()
        if key == "handle":
            value = value.lstrip("@")
        parts.append(value)
    material = "|".join(parts)
    return hashlib.sha256(material.encode()).hexdigest()[:32]


def load_scan_file(path: str | Path) -> dict[str, Any]:
    """Read and minimally validate an Aside scan JSON file."""

    data = json.loads(Path(path).read_text())
    observations = data.get("observations")
    if not isinstance(observations, list):
        raise ValueError("scan JSON must contain an observations array")
    return data


def import_aside_scan(path: str | Path, *, actor: str = "aside-scan-import") -> ImportSummary:
    """Import an Aside scan JSON file into benchmark creator/video tables."""

    data = load_scan_file(path)
    niche = data.get("niche") or "unknown"
    observations: list[dict[str, Any]] = data["observations"]
    trace_id = new_trace_id("aside-scan")
    record_event(
        trace_id,
        "scan",
        actor,
        "input",
        {"path": str(path), "niche": niche, "count": len(observations)},
    )

    creators_seen: set[int] = set()
    videos_inserted = 0
    videos_duplicate = 0
    credible = 0

    for obs in observations:
        platform = canonical_platform(obs.get("platform"))
        handle = (obs.get("handle") or "").strip().lstrip("@")
        if not handle:
            record_event(trace_id, "scan", actor, "error", {"reason": "missing handle", "observation": obs})
            continue

        creator_id = upsert_creator(
            platform=platform,
            handle=handle,
            display_name=obs.get("display_name"),
            niche=niche,
            followers=coerce_int(obs.get("followers")),
            source_url=obs.get("profile_url"),
            metadata={"source": data.get("source", "aside")},
        )
        creators_seen.add(creator_id)

        credibility = set_creator_proof(
            creator_id,
            proof_engagement_rate=compute_engagement_rate(obs),
            proof_monetization=obs.get("proof_monetization"),
            proof_consistency_days=coerce_int(obs.get("proof_consistency_days")),
            proof_notes=obs.get("proof_notes"),
        )
        if credibility in {"verified", "plausible"}:
            credible += 1

        content_hash = obs.get("content_hash") or observation_content_hash(obs)
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO benchmark_videos
                  (creator_id, platform, url, title, hook_text, format, duration_seconds,
                   views, likes, comments, saves, shares, cta_pattern, structure,
                   content_hash, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s, %s::jsonb)
                ON CONFLICT (platform, url) DO NOTHING
                """,
                (
                    creator_id,
                    platform,
                    obs.get("url") or f"urn:aside:{content_hash}",
                    obs.get("title"),
                    obs.get("hook_text"),
                    obs.get("format") or "short",
                    obs.get("duration_seconds"),
                    coerce_int(obs.get("views")),
                    coerce_int(obs.get("likes")),
                    coerce_int(obs.get("comments")),
                    coerce_int(obs.get("saves")),
                    coerce_int(obs.get("shares")),
                    obs.get("cta_pattern"),
                    json.dumps(obs.get("structure", {})),
                    content_hash,
                    json.dumps({"source": data.get("source", "aside"), "raw": obs}),
                ),
            )
            inserted = cur.rowcount == 1
            conn.commit()
        if inserted:
            videos_inserted += 1
        else:
            videos_duplicate += 1

    summary = ImportSummary(
        trace_id=trace_id,
        observations_seen=len(observations),
        creators_upserted=len(creators_seen),
        videos_inserted=videos_inserted,
        videos_duplicate=videos_duplicate,
        creators_verified_or_plausible=credible,
    )
    record_event(trace_id, "scan", actor, "output", summary.__dict__)
    return summary
