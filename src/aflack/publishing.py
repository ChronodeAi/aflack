"""Publishing abstractions.

Postiz is the primary scheduling/posting app. The adapter is safe by default:
without `POSTIZ_API_KEY` and a connected platform integration id, it persists
intent as `needs_auth`; with both configured it submits a draft/scheduled post
through Postiz's public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
import json
from typing import Literal
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .config import load_settings
from .db import connect

TargetFormat = Literal["short", "longform", "reel", "post", "story", "other"]


@dataclass(frozen=True)
class PublishIntent:
    creative_id: int
    platform: str
    target_format: TargetFormat
    title: str
    description: str = ""
    hashtags: list[str] = field(default_factory=list)
    disclosure_text: str = ""
    scheduled_at: datetime | None = None


class PostizPublisher:
    """Postiz-backed publisher adapter.

    Public API facts verified from the running Postiz container:
    - Auth header is raw API key in `Authorization` (no `Bearer` prefix).
    - `POST /api/public/v1/posts` accepts `type`, `shortLink`, `date`, `tags`,
      and `posts[].integration.id` + `posts[].value[].content/image`.
    """

    def enqueue(self, intent: PublishIntent) -> int:
        """Persist a publish intent and return the queue id."""

        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO publish_queue (
                  creative_id, platform, target_format, title, description,
                  hashtags, disclosure_text, scheduled_at, status, metadata
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'needs_auth',
                        '{"publisher":"postiz","mode":"stub"}')
                RETURNING id
                """,
                (
                    intent.creative_id,
                    intent.platform,
                    intent.target_format,
                    intent.title,
                    intent.description,
                    intent.hashtags,
                    intent.disclosure_text,
                    intent.scheduled_at,
                ),
            )
            queue_id = cur.fetchone()[0]
            conn.commit()
            return int(queue_id)

    def list_integrations(self) -> list[dict]:
        """List connected Postiz integrations using the public API."""

        settings = load_settings()
        if not settings.postiz_api_key:
            raise RuntimeError("POSTIZ_API_KEY is not set")
        return self._request("GET", "/api/public/v1/integrations")

    def submit_queue_item(self, queue_id: int, integration_id: str, *, as_draft: bool = True) -> dict:
        """Submit one queued item to Postiz and persist the returned id/status.

        Uses draft mode by default; public publishing remains a human gate.
        """

        settings = load_settings()
        if not settings.postiz_api_key:
            self._mark(queue_id, "needs_auth", "POSTIZ_API_KEY is not set")
            raise RuntimeError("POSTIZ_API_KEY is not set")

        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, title, description, hashtags, disclosure_text, scheduled_at
                FROM publish_queue
                WHERE id = %s
                """,
                (queue_id,),
            )
            row = cur.fetchone()
        if not row:
            raise ValueError(f"publish_queue id={queue_id} not found")

        _, title, description, hashtags, disclosure, scheduled_at = row
        content = "\n\n".join(part for part in [title, description, disclosure] if part)
        if hashtags:
            content += "\n\n" + " ".join(f"#{tag.lstrip('#')}" for tag in hashtags)
        date = (scheduled_at or (datetime.now(UTC) + timedelta(hours=1))).isoformat()
        payload = {
            "type": "draft" if as_draft else "schedule",
            "shortLink": False,
            "date": date,
            "tags": [],
            "creationMethod": "API",
            "posts": [
                {
                    "integration": {"id": integration_id},
                    "value": [{"content": content, "image": []}],
                    "settings": {},
                }
            ],
        }

        try:
            response = self._request("POST", "/api/public/v1/posts", payload)
        except Exception as exc:
            self._mark(queue_id, "failed", str(exc))
            raise

        postiz_id = str(response.get("id") or response.get("group") or response.get("postId") or "")
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE publish_queue
                SET status = %s,
                    postiz_post_id = NULLIF(%s, ''),
                    metadata = metadata || %s::jsonb,
                    updated_at = now()
                WHERE id = %s
                """,
                (
                    "submitted_to_postiz",
                    postiz_id,
                    json.dumps({"postiz_response": response}),
                    queue_id,
                ),
            )
            conn.commit()
        return response

    def _request(self, method: str, path: str, payload: dict | None = None):
        settings = load_settings()
        if not settings.postiz_api_key:
            raise RuntimeError("POSTIZ_API_KEY is not set")
        body = json.dumps(payload).encode("utf-8") if payload is not None else None
        req = Request(
            f"{settings.postiz_base_url}{path}",
            data=body,
            method=method,
            headers={
                "Authorization": settings.postiz_api_key,
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(req, timeout=20) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Postiz API {exc.code}: {raw}") from exc

    def _mark(self, queue_id: int, status: str, error: str | None = None) -> None:
        with connect() as conn, conn.cursor() as cur:
            cur.execute(
                """
                UPDATE publish_queue
                SET status = %s, error = %s, updated_at = now()
                WHERE id = %s
                """,
                (status, error, queue_id),
            )
            conn.commit()
