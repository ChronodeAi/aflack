from __future__ import annotations

import unittest

import structlog

from aflack.logging import (
    _redact_processor,
    _redact_value,
    configure_logging,
    get_logger,
)


class RedactValueTests(unittest.TestCase):
    def test_non_string_returned_unchanged(self):
        self.assertEqual(_redact_value(42), 42)
        self.assertEqual(_redact_value(None), None)

    def test_bearer_token_redacted(self):
        redacted = _redact_value("Authorization Bearer abc123DEF456ghi")
        self.assertIn("Bearer ***REDACTED***", redacted)
        self.assertNotIn("abc123DEF456ghi", redacted)

    def test_openai_style_key_redacted(self):
        redacted = _redact_value("using sk-ABCDEFGHIJKLMNOPQRSTUVWX")
        self.assertIn("sk-***REDACTED***", redacted)

    def test_password_query_param_redacted(self):
        redacted = _redact_value("db url password=hunter2secret&host=x")
        self.assertIn("password=***REDACTED***", redacted)
        self.assertNotIn("hunter2secret", redacted)

    def test_plain_string_unchanged(self):
        self.assertEqual(_redact_value("a normal log line"), "a normal log line")


class RedactProcessorTests(unittest.TestCase):
    def test_sensitive_keys_fully_redacted(self):
        event_dict = {
            "event": "publish attempt",
            "api_key": "postiz-secret-value",
            "postiz_api_key": "another-secret",
            "count": 3,
        }

        result = _redact_processor(None, "info", event_dict)

        self.assertEqual(result["api_key"], "***REDACTED***")
        self.assertEqual(result["postiz_api_key"], "***REDACTED***")
        self.assertEqual(result["event"], "publish attempt")
        self.assertEqual(result["count"], 3)

    def test_value_patterns_redacted_in_non_sensitive_keys(self):
        event_dict = {"message": "token Bearer abcDEF123456xyz used"}

        result = _redact_processor(None, "info", event_dict)

        self.assertIn("Bearer ***REDACTED***", result["message"])
        self.assertNotIn("abcDEF123456xyz", result["message"])


class LoggerConfigTests(unittest.TestCase):
    def test_configure_logging_dev_mode_runs(self):
        configure_logging(dev_mode=True)
        logger = get_logger("test-dev")
        self.assertIsNotNone(logger)

    def test_configure_logging_json_mode_and_get_logger(self):
        configure_logging(dev_mode=False)
        logger = get_logger("aflack")
        self.assertIsNotNone(logger)
        # get_logger returns a structlog bound logger proxy
        self.assertTrue(hasattr(logger, "info"))

    def tearDown(self):
        # Reset structlog to defaults so config changes don't leak across tests.
        structlog.reset_defaults()


if __name__ == "__main__":
    unittest.main()
