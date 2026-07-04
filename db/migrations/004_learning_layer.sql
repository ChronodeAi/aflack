-- Continuous-improvement / learning layer.
-- Purpose: capture competitor intelligence, distilled insights, and concrete
-- proposals to evolve skills/rules/workflows/agents. This is the substrate that
-- turns "surfing top creators" into reproducible pipeline improvements.
--
-- Design: relational tables are the source of truth. agentmemory (episodic) and
-- the semantic-memory MCP (fortemi) are derived indexes fed from these rows.

-- Creators we benchmark against. `proof_*` fields exist to force evidence of REAL
-- success (engagement/monetization signals), not just follower/wealth flexing.
CREATE TABLE IF NOT EXISTS benchmark_creators (
  id BIGSERIAL PRIMARY KEY,
  platform TEXT NOT NULL CHECK (platform IN ('instagram', 'tiktok', 'youtube', 'x', 'other')),
  handle TEXT NOT NULL,
  display_name TEXT,
  niche TEXT,
  followers BIGINT,
  -- Evidence of genuine success beyond vanity metrics:
  proof_engagement_rate NUMERIC,          -- likes+comments+saves / views or followers
  proof_monetization TEXT,                -- observed offer: affiliate, product, course, sponsor, platform-payout
  proof_consistency_days INTEGER,         -- observed posting streak / cadence window
  proof_notes TEXT,                       -- how we verified real success
  credibility TEXT NOT NULL DEFAULT 'unverified'
    CHECK (credibility IN ('unverified', 'weak', 'plausible', 'verified', 'rejected')),
  status TEXT NOT NULL DEFAULT 'candidate'
    CHECK (status IN ('candidate', 'active', 'archived', 'rejected')),
  source_url TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(platform, handle)
);

-- Individual high-performing videos/posts we dissect for reusable patterns.
CREATE TABLE IF NOT EXISTS benchmark_videos (
  id BIGSERIAL PRIMARY KEY,
  creator_id BIGINT REFERENCES benchmark_creators(id) ON DELETE CASCADE,
  platform TEXT NOT NULL,
  url TEXT,
  title TEXT,
  hook_text TEXT,
  format TEXT,                            -- short, reel, longform, carousel, etc.
  duration_seconds NUMERIC,
  views BIGINT,
  likes BIGINT,
  comments BIGINT,
  saves BIGINT,
  shares BIGINT,
  cta_pattern TEXT,                       -- observed CTA (comment keyword, link in bio, etc.)
  structure JSONB NOT NULL DEFAULT '{}'::jsonb,   -- beat-by-beat breakdown
  observed_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  content_hash TEXT,                      -- dedup key for the same observed video
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(platform, url)
);

-- Distilled, reusable insights. Deduped via content_hash; temporally valid so
-- stale patterns can be retired instead of rotting the context window.
CREATE TABLE IF NOT EXISTS insights (
  id BIGSERIAL PRIMARY KEY,
  scope TEXT NOT NULL CHECK (scope IN ('hook', 'structure', 'pacing', 'cta', 'funnel',
                                       'thumbnail', 'audio', 'persona', 'niche', 'compliance', 'other')),
  statement TEXT NOT NULL,                -- the distilled lesson, one sentence
  evidence JSONB NOT NULL DEFAULT '[]'::jsonb,   -- links to benchmark_videos / results
  confidence NUMERIC NOT NULL DEFAULT 0.5 CHECK (confidence >= 0 AND confidence <= 1),
  support_count INTEGER NOT NULL DEFAULT 1,      -- how many observations back it
  contradiction_count INTEGER NOT NULL DEFAULT 0,
  content_hash TEXT NOT NULL,             -- dedup: normalized(statement+scope)
  status TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'superseded', 'retired')),
  valid_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  invalid_at TIMESTAMPTZ,
  embedding vector(384),
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(content_hash)
);

-- Concrete proposals to change our own pipeline artifacts. This is the bridge
-- from "insight" to "reproducible skill/rule/workflow". Applying a proposal to a
-- real skill/rule file is a HUMAN-GATED step.
CREATE TABLE IF NOT EXISTS improvement_proposals (
  id BIGSERIAL PRIMARY KEY,
  target_type TEXT NOT NULL CHECK (target_type IN ('skill', 'rule', 'workflow', 'agent', 'template', 'prompt')),
  target_name TEXT NOT NULL,             -- e.g. "hook-authoring", "benchmark-before-scale"
  change_summary TEXT NOT NULL,
  rationale TEXT NOT NULL,
  source_insight_ids BIGINT[] NOT NULL DEFAULT '{}',
  status TEXT NOT NULL DEFAULT 'proposed'
    CHECK (status IN ('proposed', 'approved', 'applied', 'rejected', 'superseded')),
  applied_path TEXT,                     -- file path once a human applies it
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Full-trace event store ("every bullet tracer"). Every pipeline step, daemon
-- tick, and agent input/output is appended here for later learning.
CREATE TABLE IF NOT EXISTS pipeline_events (
  id BIGSERIAL PRIMARY KEY,
  trace_id TEXT NOT NULL,                -- correlates one end-to-end run
  stage TEXT NOT NULL,                   -- scan, distill, propose, produce, validate, publish, learn
  actor TEXT NOT NULL,                   -- daemon, director, operator, agent name
  event_type TEXT NOT NULL,             -- start, input, output, decision, gate, error, end
  payload JSONB NOT NULL DEFAULT '{}'::jsonb,
  ref_type TEXT,
  ref_id BIGINT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Daemon/cron run bookkeeping so autonomous loops are auditable and resumable.
CREATE TABLE IF NOT EXISTS daemon_runs (
  id BIGSERIAL PRIMARY KEY,
  daemon TEXT NOT NULL,                  -- trend-watcher, distiller, roi-sentinel, etc.
  trace_id TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'running'
    CHECK (status IN ('running', 'succeeded', 'failed', 'skipped', 'blocked')),
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  finished_at TIMESTAMPTZ,
  summary TEXT,
  counts JSONB NOT NULL DEFAULT '{}'::jsonb,   -- {scanned, distilled, proposed, ...}
  error TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_benchmark_videos_creator ON benchmark_videos(creator_id);
CREATE INDEX IF NOT EXISTS idx_benchmark_videos_hash ON benchmark_videos(content_hash);
CREATE INDEX IF NOT EXISTS idx_insights_scope_status ON insights(scope, status);
CREATE INDEX IF NOT EXISTS idx_insights_validity ON insights(status, valid_at, invalid_at);
CREATE INDEX IF NOT EXISTS idx_proposals_target ON improvement_proposals(target_type, status);
CREATE INDEX IF NOT EXISTS idx_events_trace ON pipeline_events(trace_id, created_at);
CREATE INDEX IF NOT EXISTS idx_events_stage ON pipeline_events(stage, created_at);
CREATE INDEX IF NOT EXISTS idx_daemon_runs_daemon ON daemon_runs(daemon, started_at);

SELECT graph.reset();
SELECT * FROM graph.auto_discover('public', NULL, true);
