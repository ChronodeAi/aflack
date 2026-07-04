from __future__ import annotations

from contextlib import contextmanager
import unittest
from unittest.mock import patch

from aflack.config import Settings
from aflack.publishing import PostizPublisher


class FakeCursor:
    def __init__(self, row):
        self.row = row
        self.sql = None
        self.params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, sql, params=None):
        self.sql = sql
        self.params = params

    def fetchone(self):
        return self.row


class FakeConnection:
    def __init__(self, row):
        self._row = row

    def cursor(self):
        return FakeCursor(self._row)


class PostizPublisherTests(unittest.TestCase):
    def _publisher_url(self, base_url: str, path: str = "/api/public/v1/integrations") -> str:
        settings = Settings(postiz_base_url=base_url, postiz_api_key="test-key")
        with patch("aflack.publishing.load_settings", return_value=settings):
            return PostizPublisher()._url(path)

    def test_cloud_root_base_url_uses_public_v1(self):
        self.assertEqual(
            self._publisher_url("https://api.postiz.com"),
            "https://api.postiz.com/public/v1/integrations",
        )

    def test_cloud_api_base_url_is_not_double_prefixed(self):
        self.assertEqual(
            self._publisher_url("https://api.postiz.com/public/v1"),
            "https://api.postiz.com/public/v1/integrations",
        )

    def test_local_root_base_url_uses_api_public_v1(self):
        self.assertEqual(
            self._publisher_url("http://localhost:4007"),
            "http://localhost:4007/api/public/v1/integrations",
        )

    def test_local_api_base_url_is_not_double_prefixed(self):
        self.assertEqual(
            self._publisher_url("http://localhost:4007/api/public/v1"),
            "http://localhost:4007/api/public/v1/integrations",
        )

    def test_build_queue_payload_does_not_submit(self):
        row = (
            123,
            "GTA 6 countdown",
            "Original AI-assisted commentary package.",
            ["GTA6", "YouTubeShorts"],
            "Disclosure: affiliate links may earn commission. AI-assisted visuals.",
            None,
            "youtube",
        )

        @contextmanager
        def fake_connect():
            yield FakeConnection(row)

        with patch("aflack.publishing.connect", fake_connect):
            payload = PostizPublisher().build_queue_payload(
                123,
                "youtube-integration-id",
                as_draft=True,
            )

        self.assertEqual(payload["type"], "draft")
        self.assertEqual(payload["posts"][0]["integration"]["id"], "youtube-integration-id")
        content = payload["posts"][0]["value"][0]["content"]
        self.assertIn("GTA 6 countdown", content)
        self.assertIn("#GTA6 #YouTubeShorts", content)
        self.assertIn("Disclosure:", content)
        settings = payload["posts"][0]["settings"]
        self.assertEqual(settings["title"], "GTA 6 countdown")
        self.assertEqual(settings["type"], "private")


if __name__ == "__main__":
    unittest.main()
