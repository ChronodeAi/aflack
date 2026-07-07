from __future__ import annotations

import unittest
from unittest.mock import patch

from aflack import error_tracking
from aflack.error_tracking import (
    ErrorContext,
    add_breadcrumb,
    capture_exception,
    capture_message,
    set_user_context,
)


class ErrorContextTests(unittest.TestCase):
    def test_defaults_are_independent(self):
        ctx = ErrorContext(error_type="ValueError", error_message="boom", stack_trace="trace")
        self.assertEqual(ctx.breadcrumbs, [])
        self.assertEqual(ctx.user_context, {})
        self.assertEqual(ctx.extra, {})
        ctx.breadcrumbs.append({"x": 1})

        other = ErrorContext(error_type="KeyError", error_message="k", stack_trace="t")
        self.assertEqual(other.breadcrumbs, [])


class SetUserContextTests(unittest.TestCase):
    def test_returns_kwargs_as_dict(self):
        result = set_user_context(user_id="creator-1", plan="free")
        self.assertEqual(result, {"user_id": "creator-1", "plan": "free"})


class BreadcrumbAndCaptureTests(unittest.TestCase):
    def setUp(self):
        error_tracking._breadcrumbs.clear()

    def tearDown(self):
        error_tracking._breadcrumbs.clear()

    def test_add_breadcrumb_appends_structured_entry(self):
        add_breadcrumb("started publish", category="publish", level="info", data={"queue_id": 2})

        self.assertEqual(len(error_tracking._breadcrumbs), 1)
        crumb = error_tracking._breadcrumbs[0]
        self.assertEqual(crumb["message"], "started publish")
        self.assertEqual(crumb["category"], "publish")
        self.assertEqual(crumb["level"], "info")
        self.assertEqual(crumb["data"], {"queue_id": 2})
        self.assertIn("timestamp", crumb)

    def test_capture_exception_records_event_and_clears_breadcrumbs(self):
        captured = {}

        def fake_record_event(*, trace_id, stage, actor, event_type, payload):
            captured["trace_id"] = trace_id
            captured["stage"] = stage
            captured["event_type"] = event_type
            captured["payload"] = payload
            return 1

        add_breadcrumb("before failure")
        with patch.object(error_tracking, "record_event", fake_record_event):
            try:
                raise ValueError("something failed")
            except ValueError as exc:
                error_id = capture_exception(exc, user_context={"user_id": "u1"}, extra={"attempt": 3})

        self.assertTrue(error_id.startswith("err-"))
        self.assertEqual(captured["stage"], "error")
        self.assertEqual(captured["event_type"], "exception")
        self.assertEqual(captured["payload"]["error_type"], "ValueError")
        self.assertEqual(captured["payload"]["error_message"], "something failed")
        self.assertEqual(captured["payload"]["user_context"], {"user_id": "u1"})
        self.assertEqual(captured["payload"]["extra"], {"attempt": 3})
        self.assertEqual(len(captured["payload"]["breadcrumbs"]), 1)
        # Breadcrumbs are cleared after a capture.
        self.assertEqual(error_tracking._breadcrumbs, [])

    def test_capture_message_records_event(self):
        captured = {}

        def fake_record_event(*, trace_id, stage, actor, event_type, payload):
            captured["event_type"] = event_type
            captured["payload"] = payload
            return 1

        with patch.object(error_tracking, "record_event", fake_record_event):
            message_id = capture_message("queue stalled", level="warning", extra={"queue_id": 2})

        self.assertTrue(message_id.startswith("msg-"))
        self.assertEqual(captured["event_type"], "message")
        self.assertEqual(captured["payload"]["level"], "warning")
        self.assertEqual(captured["payload"]["message"], "queue stalled")
        self.assertEqual(captured["payload"]["extra"], {"queue_id": 2})


if __name__ == "__main__":
    unittest.main()
