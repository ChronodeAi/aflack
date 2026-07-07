-- Time-series analytics capture for published videos/posts.
-- `results` remains the compact rollup table; analytics_snapshots is the
-- normalized ingestion layer for Postiz, platform APIs, and manual imports.

CREATE TABLE IF NOT EXISTS analytics_snapshots (
  id BIGSERIAL PRIMARY KEY,
  publish_queue_id BIGINT REFERENCES publish_queue(id) ON DELETE SET NULL,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE SET NULL,
  channel_id BIGINT REFERENCES channels(id) ON DELETE SET NULL,
  platform TEXT NOT NULL,
  source TEXT NOT NULL CHECK (source IN ('postiz', 'youtube', 'tiktok', 'instagram', 'manual', 'other')),
  source_post_id TEXT,
  platform_url TEXT,
  views BIGINT NOT NULL DEFAULT 0,
  likes BIGINT NOT NULL DEFAULT 0,
  comments BIGINT NOT NULL DEFAULT 0,
  shares BIGINT NOT NULL DEFAULT 0,
  saves BIGINT NOT NULL DEFAULT 0,
  clicks BIGINT NOT NULL DEFAULT 0,
  conversions BIGINT NOT NULL DEFAULT 0,
  watch_time_seconds NUMERIC,
  average_view_duration_seconds NUMERIC,
  average_percentage_viewed NUMERIC,
  ctr NUMERIC,
  revenue NUMERIC NOT NULL DEFAULT 0,
  retention JSONB NOT NULL DEFAULT '{}'::jsonb,
  raw JSONB NOT NULL DEFAULT '{}'::jsonb,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_publish_queue ON analytics_snapshots(publish_queue_id);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_creative ON analytics_snapshots(creative_id);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_platform_source ON analytics_snapshots(platform, source);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_captured_at ON analytics_snapshots(captured_at DESC);

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);
