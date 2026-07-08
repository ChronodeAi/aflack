-- Analytics snapshots captured from Postiz/platform/manual sources.
-- These rows close the loop from publish_queue -> platform outcome -> ROI gate.

CREATE TABLE IF NOT EXISTS analytics_snapshots (
    id BIGSERIAL PRIMARY KEY,
    publish_queue_id BIGINT REFERENCES publish_queue(id) ON DELETE SET NULL,
    creative_id BIGINT REFERENCES creatives(id) ON DELETE SET NULL,
    channel_id BIGINT REFERENCES channels(id) ON DELETE SET NULL,
    platform TEXT NOT NULL,
    source TEXT NOT NULL CHECK (source IN ('postiz', 'youtube', 'tiktok', 'instagram', 'manual', 'other')),
    source_post_id TEXT,
    platform_url TEXT,
    views BIGINT NOT NULL DEFAULT 0 CHECK (views >= 0),
    likes BIGINT NOT NULL DEFAULT 0 CHECK (likes >= 0),
    comments BIGINT NOT NULL DEFAULT 0 CHECK (comments >= 0),
    shares BIGINT NOT NULL DEFAULT 0 CHECK (shares >= 0),
    saves BIGINT NOT NULL DEFAULT 0 CHECK (saves >= 0),
    clicks BIGINT NOT NULL DEFAULT 0 CHECK (clicks >= 0),
    conversions BIGINT NOT NULL DEFAULT 0 CHECK (conversions >= 0),
    watch_time_seconds NUMERIC CHECK (watch_time_seconds IS NULL OR watch_time_seconds >= 0),
    average_view_duration_seconds NUMERIC CHECK (
        average_view_duration_seconds IS NULL OR average_view_duration_seconds >= 0
    ),
    average_percentage_viewed NUMERIC CHECK (
        average_percentage_viewed IS NULL OR average_percentage_viewed >= 0
    ),
    ctr NUMERIC CHECK (ctr IS NULL OR ctr >= 0),
    revenue NUMERIC NOT NULL DEFAULT 0 CHECK (revenue >= 0),
    retention JSONB NOT NULL DEFAULT '{}'::jsonb,
    raw JSONB NOT NULL DEFAULT '{}'::jsonb,
    captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_queue ON analytics_snapshots(publish_queue_id, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_creative ON analytics_snapshots(creative_id, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_platform ON analytics_snapshots(platform, captured_at DESC);
CREATE INDEX IF NOT EXISTS idx_analytics_snapshots_source_post ON analytics_snapshots(source, source_post_id);

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);
