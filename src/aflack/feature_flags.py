"""Feature flag infrastructure for safe rollouts.

Simple file-based feature flags stored in the database. Supports percentage-based
rollouts and per-creator overrides. Agents can ship changes behind toggles,
reducing risk of agent-authored code affecting all users immediately.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from .db import connect


@dataclass(frozen=True)
class FeatureFlag:
    name: str
    enabled: bool
    rollout_percentage: int
    description: str


def _hash_percentage(key: str) -> int:
    h = hashlib.sha256(key.encode()).hexdigest()
    return int(h[:8], 16) % 100


def get_flag(name: str) -> FeatureFlag | None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT name, enabled, rollout_percentage, description FROM feature_flags WHERE name = %s",
            (name,),
        )
        row = cur.fetchone()
    if not row:
        return None
    return FeatureFlag(name=row[0], enabled=row[1], rollout_percentage=row[2], description=row[3])


def is_enabled(name: str, *, context_key: str = "") -> bool:
    flag = get_flag(name)
    if not flag or not flag.enabled:
        return False
    if flag.rollout_percentage >= 100:
        return True
    if not context_key:
        return flag.rollout_percentage > 0
    return _hash_percentage(f"{name}:{context_key}") < flag.rollout_percentage


def set_flag(name: str, *, enabled: bool, rollout_percentage: int = 100, description: str = "") -> None:
    with connect() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO feature_flags (name, enabled, rollout_percentage, description)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (name) DO UPDATE SET
              enabled = EXCLUDED.enabled,
              rollout_percentage = EXCLUDED.rollout_percentage,
              description = EXCLUDED.description,
              updated_at = now()
            """,
            (name, enabled, rollout_percentage, description),
        )
        conn.commit()
