-- Publishing integration: Postiz-backed scheduling intents and platform credentials status.

CREATE TABLE IF NOT EXISTS platform_credentials (
  id BIGSERIAL PRIMARY KEY,
  platform TEXT NOT NULL,
  auth_mode TEXT NOT NULL CHECK (auth_mode IN ('postiz_oauth', 'postiz_api_key', 'aside_session', 'manual')),
  status TEXT NOT NULL DEFAULT 'unknown' CHECK (status IN ('unknown', 'needs_setup', 'connected', 'expired', 'failed')),
  notes TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(platform, auth_mode)
);

CREATE TABLE IF NOT EXISTS publish_queue (
  id BIGSERIAL PRIMARY KEY,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE CASCADE,
  channel_id BIGINT REFERENCES channels(id) ON DELETE SET NULL,
  platform TEXT NOT NULL,
  target_format TEXT NOT NULL CHECK (target_format IN ('short', 'longform', 'reel', 'post', 'story', 'other')),
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  hashtags TEXT[] NOT NULL DEFAULT '{}'::text[],
  disclosure_text TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN (
    'draft',
    'queued',
    'submitted_to_postiz',
    'scheduled',
    'published',
    'failed',
    'needs_manual_review',
    'needs_auth'
  )),
  scheduled_at TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  postiz_post_id TEXT,
  platform_post_id TEXT,
  platform_url TEXT,
  error TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_publish_queue_status ON publish_queue(status, scheduled_at);
CREATE INDEX IF NOT EXISTS idx_publish_queue_creative ON publish_queue(creative_id);
CREATE INDEX IF NOT EXISTS idx_publish_queue_platform ON publish_queue(platform);

-- Default platform credential placeholders for the GTA6 YouTube-first branch.
INSERT INTO platform_credentials (platform, auth_mode, status, notes)
VALUES
  ('youtube', 'postiz_oauth', 'needs_setup', 'Connect YouTube channel in Postiz; expect private/draft/manual-publish constraints until API/audit path verified.'),
  ('tiktok', 'postiz_oauth', 'needs_setup', 'Connect TikTok in Postiz if using Shorts/TikTok cross-posting; Aside fallback if API flow blocks.'),
  ('x', 'postiz_oauth', 'needs_setup', 'Optional gaming-channel distribution.'),
  ('instagram', 'postiz_oauth', 'needs_setup', 'Optional Reels cross-posting.')
ON CONFLICT (platform, auth_mode) DO NOTHING;

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);

