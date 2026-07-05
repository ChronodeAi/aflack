"""Structured logging with log scrubbing for the content pipeline.

Uses structlog for structured JSON output and includes a redaction processor
that scrubs sensitive fields (API keys, passwords, tokens) from log entries.
"""

from __future__ import annotations

import re
from collections.abc import MutableMapping
from typing import Any, cast

import structlog

_REDACT_KEYS = {
    "password",
    "api_key",
    "apikey",
    "token",
    "secret",
    "authorization",
    "postiz_api_key",
    "database_url",
}

_REDACT_PATTERNS = [
    re.compile(r"(gho_|ghp_|ghs_|ghr_|github_pat_)[A-Za-z0-9_]{36,}"),
    re.compile(r"(sk-)[A-Za-z0-9]{20,}"),
    re.compile(r"(Bearer\s+)[A-Za-z0-9\-._~+\/]+"),
    re.compile(r"(password=)[^\s&]+", re.IGNORECASE),
]


def _redact_value(value: Any) -> Any:
    if isinstance(value, str):
        redacted = value
        for pattern in _REDACT_PATTERNS:
            redacted = pattern.sub(r"\1***REDACTED***", redacted)
        return redacted
    return value


def _redact_processor(
    _logger: Any, _method_name: str, event_dict: MutableMapping[str, Any]
) -> MutableMapping[str, Any]:
    for key in list(event_dict.keys()):
        if key.lower() in _REDACT_KEYS:
            event_dict[key] = "***REDACTED***"
        else:
            event_dict[key] = _redact_value(event_dict[key])
    return event_dict


def configure_logging(*, dev_mode: bool = False) -> None:
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _redact_processor,
            structlog.dev.ConsoleRenderer() if dev_mode else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(0),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str = "aflack") -> structlog.stdlib.BoundLogger:
    return cast(structlog.stdlib.BoundLogger, structlog.get_logger(name))
