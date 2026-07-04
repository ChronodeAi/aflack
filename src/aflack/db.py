"""Database access for the local event store."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg import Connection

from .config import load_settings


@contextmanager
def connect() -> Iterator[Connection]:
    """Open a Postgres connection using local settings."""

    settings = load_settings()
    with psycopg.connect(settings.database_url) as conn:
        yield conn


def exec_sql(sql: str) -> None:
    """Execute one SQL script inside a transaction."""

    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()

