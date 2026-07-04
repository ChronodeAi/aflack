"""Configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str = "postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph"


def load_settings() -> Settings:
    """Load local settings from environment and optional .env."""

    load_dotenv()
    return Settings(
        database_url=os.environ.get(
            "DATABASE_URL",
            "postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph",
        )
    )

