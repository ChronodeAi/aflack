-- Day-1 local event store schema for the affiliate content pipeline.
-- Source of truth: relational tables. Graph/vector layers are derived indexes.

CREATE EXTENSION IF NOT EXISTS graph;
CREATE EXTENSION IF NOT EXISTS pg_cron;
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS niches (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  status TEXT NOT NULL DEFAULT 'diagnostic',
  scorecard JSONB NOT NULL DEFAULT '{}'::jsonb,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS products (
  id BIGSERIAL PRIMARY KEY,
  niche_id BIGINT REFERENCES niches(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  source_url TEXT,
  affiliate_program TEXT,
  commission NUMERIC,
  margin_notes TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS personas (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  higgsfield_ref TEXT,
  ethics_policy TEXT NOT NULL,
  disclosure_mode TEXT NOT NULL DEFAULT 'onscreen+caption',
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS hooks (
  id BIGSERIAL PRIMARY KEY,
  niche_id BIGINT REFERENCES niches(id) ON DELETE SET NULL,
  text TEXT NOT NULL,
  source_ref TEXT,
  benchmark_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  embedding vector(384),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS scripts (
  id BIGSERIAL PRIMARY KEY,
  product_id BIGINT REFERENCES products(id) ON DELETE SET NULL,
  persona_id BIGINT REFERENCES personas(id) ON DELETE SET NULL,
  hook_id BIGINT REFERENCES hooks(id) ON DELETE SET NULL,
  body TEXT NOT NULL,
  claim_flags JSONB NOT NULL DEFAULT '[]'::jsonb,
  embedding vector(384),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS creatives (
  id BIGSERIAL PRIMARY KEY,
  script_id BIGINT REFERENCES scripts(id) ON DELETE SET NULL,
  higgsfield_job_id TEXT,
  media_path TEXT,
  duration_seconds NUMERIC,
  cost_credits NUMERIC NOT NULL DEFAULT 0,
  validation_metrics JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS creative_variants (
  id BIGSERIAL PRIMARY KEY,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE CASCADE,
  change_note TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS channels (
  id BIGSERIAL PRIMARY KEY,
  platform TEXT NOT NULL,
  account_ref TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(platform, account_ref)
);

CREATE TABLE IF NOT EXISTS disclosures (
  id BIGSERIAL PRIMARY KEY,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE CASCADE,
  disclosure_type TEXT NOT NULL,
  content TEXT NOT NULL,
  approved BOOLEAN NOT NULL DEFAULT false,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS claims (
  id BIGSERIAL PRIMARY KEY,
  script_id BIGINT REFERENCES scripts(id) ON DELETE SET NULL,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE SET NULL,
  text TEXT NOT NULL,
  risk_level TEXT NOT NULL DEFAULT 'unknown',
  decision TEXT NOT NULL DEFAULT 'pending',
  rationale TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS results (
  id BIGSERIAL PRIMARY KEY,
  creative_id BIGINT REFERENCES creatives(id) ON DELETE CASCADE,
  channel_id BIGINT REFERENCES channels(id) ON DELETE SET NULL,
  views BIGINT,
  retention JSONB NOT NULL DEFAULT '{}'::jsonb,
  ctr NUMERIC,
  conversions BIGINT,
  revenue NUMERIC NOT NULL DEFAULT 0,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS lessons (
  id BIGSERIAL PRIMARY KEY,
  scope TEXT NOT NULL CHECK (scope IN ('episodic', 'semantic', 'procedural')),
  content TEXT NOT NULL,
  links JSONB NOT NULL DEFAULT '[]'::jsonb,
  valid_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  invalid_at TIMESTAMPTZ,
  embedding vector(384),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS cost_ledger (
  id BIGSERIAL PRIMARY KEY,
  ref_type TEXT NOT NULL,
  ref_id BIGINT,
  cost_type TEXT NOT NULL CHECK (cost_type IN ('higgsfield', 'token', 'tool', 'operator', 'other')),
  amount NUMERIC NOT NULL,
  unit TEXT NOT NULL,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  recorded_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_products_niche ON products(niche_id);
CREATE INDEX IF NOT EXISTS idx_scripts_product ON scripts(product_id);
CREATE INDEX IF NOT EXISTS idx_creatives_script ON creatives(script_id);
CREATE INDEX IF NOT EXISTS idx_results_creative ON results(creative_id);
CREATE INDEX IF NOT EXISTS idx_cost_ledger_ref ON cost_ledger(ref_type, ref_id);
CREATE INDEX IF NOT EXISTS idx_lessons_scope_validity ON lessons(scope, valid_at, invalid_at);

-- Graph index is derived from PK/FK relationships.
-- Reset stale registration first (pgGraph alpha: dropped tables leave dangling
-- registration that breaks auto_discover), then rediscover over the current schema.
SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);

