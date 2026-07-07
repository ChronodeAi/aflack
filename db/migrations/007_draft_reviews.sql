-- Structured human/operator review outcomes for the first-100 Postiz draft ramp.
-- This is the learning input for publish-quality policy; it does not authorize
-- public publishing by itself.

CREATE TABLE IF NOT EXISTS draft_reviews (
  id BIGSERIAL PRIMARY KEY,
  publish_queue_id BIGINT REFERENCES publish_queue(id) ON DELETE SET NULL,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE SET NULL,
  reviewer TEXT NOT NULL,
  verdict TEXT NOT NULL CHECK (
    verdict IN ('keep_private', 'revise_prompt', 'revise_script', 'publish_candidate', 'kill')
  ),
  hook_score SMALLINT NOT NULL CHECK (hook_score BETWEEN 1 AND 5),
  retention_score SMALLINT NOT NULL CHECK (retention_score BETWEEN 1 AND 5),
  payoff_score SMALLINT NOT NULL CHECK (payoff_score BETWEEN 1 AND 5),
  compliance_score SMALLINT NOT NULL CHECK (compliance_score BETWEEN 1 AND 5),
  cta_score SMALLINT NOT NULL CHECK (cta_score BETWEEN 1 AND 5),
  asset_quality_score SMALLINT NOT NULL CHECK (asset_quality_score BETWEEN 1 AND 5),
  blocks JSONB NOT NULL DEFAULT '[]'::jsonb,
  warnings JSONB NOT NULL DEFAULT '[]'::jsonb,
  lessons JSONB NOT NULL DEFAULT '[]'::jsonb,
  policy_update_candidate TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  reviewed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_draft_reviews_queue ON draft_reviews(publish_queue_id);
CREATE INDEX IF NOT EXISTS idx_draft_reviews_creative ON draft_reviews(creative_id);
CREATE INDEX IF NOT EXISTS idx_draft_reviews_verdict ON draft_reviews(verdict);
CREATE INDEX IF NOT EXISTS idx_draft_reviews_reviewed_at ON draft_reviews(reviewed_at DESC);

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);
