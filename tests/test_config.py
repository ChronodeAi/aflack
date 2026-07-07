from __future__ import annotations

import os
import unittest
from unittest.mock import patch

from aflack.config import load_settings


class ConfigTests(unittest.TestCase):
    def test_load_settings_uses_local_defaults_without_env(self):
        with patch.dict(os.environ, {}, clear=True), patch("aflack.config.load_dotenv"):
            settings = load_settings()

        self.assertEqual(
            settings.database_url,
            "postgresql://postgres:aflack_local_dev@127.0.0.1:55432/graph",
        )
        self.assertEqual(settings.postiz_base_url, "http://localhost:4007")
        self.assertIsNone(settings.postiz_api_key)

    def test_load_settings_uses_env_and_trims_postiz_base_url(self):
        env = {
            "DATABASE_URL": "postgresql://example.invalid/aflack",
            "POSTIZ_BASE_URL": "https://api.postiz.com/public/v1/",
            "POSTIZ_API_KEY": "test-key",
        }
        with patch.dict(os.environ, env, clear=True), patch("aflack.config.load_dotenv"):
            settings = load_settings()

        self.assertEqual(settings.database_url, "postgresql://example.invalid/aflack")
        self.assertEqual(settings.postiz_base_url, "https://api.postiz.com/public/v1")
        self.assertEqual(settings.postiz_api_key, "test-key")

    def test_empty_postiz_api_key_is_none(self):
        with patch.dict(os.environ, {"POSTIZ_API_KEY": ""}, clear=True), patch("aflack.config.load_dotenv"):
            settings = load_settings()

        self.assertIsNone(settings.postiz_api_key)


if __name__ == "__main__":
    unittest.main()
