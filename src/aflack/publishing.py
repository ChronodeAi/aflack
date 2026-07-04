"""Publishing abstractions.

Postiz is the primary scheduling/posting app. This module intentionally starts
as a safe stub: it prepares/persists Postiz scheduling intents and marks work as
needs_auth until the self-hosted Postiz API/auth flow is verified.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

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

    V1 does not call Postiz yet. It writes scheduling intent to `publish_queue`
    and marks the item `needs_auth`, which is the safe state until Postiz's
    self-hosted API key/OAuth flow is configured.
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

