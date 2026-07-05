"""Database access for the local event store."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import psycopg
from psycopg import Connection, Cursor

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


def fetchone_required(cur: Cursor) -> tuple[Any, ...]:
    """Return fetchone result, asserting a row exists."""

    row = cur.fetchone()
    assert row is not None, "query returned no rows"
    return row
