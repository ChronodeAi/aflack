-- Funnel/lead-magnet layer inspired by observed Jarvis/Higgsfield keyword-CTA pattern.

CREATE TABLE IF NOT EXISTS lead_magnets (
  id BIGSERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL DEFAULT '',
  url TEXT,
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'retired')),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS funnel_keywords (
  id BIGSERIAL PRIMARY KEY,
  keyword TEXT NOT NULL UNIQUE,
  lead_magnet_id BIGINT REFERENCES lead_magnets(id) ON DELETE SET NULL,
  platform TEXT NOT NULL DEFAULT 'youtube',
  delivery_mode TEXT NOT NULL DEFAULT 'pinned_comment_description' CHECK (delivery_mode IN (
    'pinned_comment_description',
    'comment_to_dm',
    'manual_dm',
    'email_capture',
    'other'
  )),
  dm_copy TEXT NOT NULL DEFAULT '',
  disclosure_text TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'active', 'retired')),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE publish_queue
  ADD COLUMN IF NOT EXISTS funnel_keyword_id BIGINT REFERENCES funnel_keywords(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS lead_magnet_id BIGINT REFERENCES lead_magnets(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS idx_funnel_keywords_keyword ON funnel_keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_publish_queue_funnel ON publish_queue(funnel_keyword_id, lead_magnet_id);

-- V1 GTA6/Jarvis-style funnel candidates (draft until actual lead magnet exists).
INSERT INTO lead_magnets (title, description, status, metadata)
VALUES
  ('GTA6 AI Content Workflow', 'A short guide showing how the GTA6 AI-persona content loop works: research, script, original visuals, validation, Postiz.', 'draft', '{"niche":"gta6-ai-persona-gaming"}'),
  ('GTA6 Loadout Checklist', 'Affiliate-ready checklist for gaming gear before GTA6 launch: controller, headset, capture card, monitor, storage.', 'draft', '{"niche":"gta6-ai-persona-gaming","persona":"Loadout Lab"}')
ON CONFLICT DO NOTHING;

INSERT INTO funnel_keywords (keyword, lead_magnet_id, platform, delivery_mode, dm_copy, disclosure_text, status, metadata)
SELECT 'JARVIS', id, 'youtube', 'pinned_comment_description',
       'Comment JARVIS for the AI content workflow. Link is in the pinned comment/description.',
       'Disclosure: AI-assisted content; affiliate links may earn commission.',
       'draft',
       '{"persona":"Vice Signal","note":"YouTube-native equivalent of comment-to-DM"}'
FROM lead_magnets WHERE title = 'GTA6 AI Content Workflow'
ON CONFLICT (keyword) DO NOTHING;

INSERT INTO funnel_keywords (keyword, lead_magnet_id, platform, delivery_mode, dm_copy, disclosure_text, status, metadata)
SELECT 'LOADOUT', id, 'youtube', 'pinned_comment_description',
       'Comment LOADOUT for the GTA6 setup checklist. Link is in the pinned comment/description.',
       'Disclosure: AI-assisted content; affiliate links may earn commission.',
       'draft',
       '{"persona":"Loadout Lab","affiliate_lane":true}'
FROM lead_magnets WHERE title = 'GTA6 Loadout Checklist'
ON CONFLICT (keyword) DO NOTHING;

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);

