"""Error tracking with context for production debugging.

Provides structured error capture with breadcrumbs, user context, and stack
trace information. Errors are persisted to the pipeline_events table and can
be forwarded to external error tracking services (Sentry, Bugsnag).
"""

from __future__ import annotations

import traceback
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from .tracing import record_event


@dataclass
class ErrorContext:
    error_type: str
    error_message: str
    stack_trace: str
    breadcrumbs: list[dict[str, Any]] = field(default_factory=list)
    user_context: dict[str, Any] = field(default_factory=dict)
    extra: dict[str, Any] = field(default_factory=dict)


_breadcrumbs: list[dict[str, Any]] = []


def add_breadcrumb(
    message: str, *, category: str = "default", level: str = "info", data: dict[str, Any] | None = None
) -> None:
    _breadcrumbs.append(
        {
            "message": message,
            "category": category,
            "level": level,
            "data": data or {},
            "timestamp": datetime.now(UTC).isoformat(),
        }
    )


def set_user_context(**kwargs: Any) -> dict[str, Any]:
    return dict(kwargs)


def capture_exception(
    exc: Exception, *, user_context: dict[str, Any] | None = None, extra: dict[str, Any] | None = None
) -> str:
    ctx = ErrorContext(
        error_type=type(exc).__name__,
        error_message=str(exc),
        stack_trace="".join(traceback.format_exception(type(exc), exc, exc.__traceback__)),
        breadcrumbs=list(_breadcrumbs),
        user_context=user_context or {},
        extra=extra or {},
    )
    error_id = f"err-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    record_event(
        trace_id=error_id,
        stage="error",
        actor="error-tracking",
        event_type="exception",
        payload={
            "error_id": error_id,
            "error_type": ctx.error_type,
            "error_message": ctx.error_message,
            "stack_trace": ctx.stack_trace,
            "breadcrumbs": ctx.breadcrumbs,
            "user_context": ctx.user_context,
            "extra": ctx.extra,
        },
    )
    _breadcrumbs.clear()
    return error_id


def capture_message(message: str, *, level: str = "error", extra: dict[str, Any] | None = None) -> str:
    error_id = f"msg-{datetime.now(UTC).strftime('%Y%m%d%H%M%S')}"
    record_event(
        trace_id=error_id,
        stage="error",
        actor="error-tracking",
        event_type="message",
        payload={
            "error_id": error_id,
            "level": level,
            "message": message,
            "extra": extra or {},
        },
    )
    return error_id
