"""Configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph"
    postiz_base_url: str = "http://localhost:4007"
    postiz_api_key: str | None = None


def load_settings() -> Settings:
    """Load local settings from environment and optional .env."""

    load_dotenv()
    return Settings(
        database_url=os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph",
        ),
        postiz_base_url=os.environ.get("POSTIZ_BASE_URL", "http://localhost:4007").rstrip("/"),
        postiz_api_key=os.environ.get("POSTIZ_API_KEY") or None,
    )
