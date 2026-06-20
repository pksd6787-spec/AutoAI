CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE organizations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  plan TEXT NOT NULL DEFAULT 'starter',
  settings JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT,
  google_sub TEXT UNIQUE,
  full_name TEXT,
  role TEXT NOT NULL DEFAULT 'member',
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  channel_id TEXT,
  language TEXT NOT NULL DEFAULT 'hinglish',
  niche TEXT,
  settings JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE ai_providers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  provider_type TEXT NOT NULL,
  priority INT NOT NULL,
  base_url TEXT,
  encrypted_api_key BYTEA,
  model_defaults JSONB NOT NULL DEFAULT '{}',
  quota_limit NUMERIC,
  quota_used NUMERIC NOT NULL DEFAULT 0,
  cost_per_1k_input NUMERIC NOT NULL DEFAULT 0,
  cost_per_1k_output NUMERIC NOT NULL DEFAULT 0,
  health_status TEXT NOT NULL DEFAULT 'unknown',
  last_health_check TIMESTAMPTZ,
  enabled BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE opportunities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  topic TEXT NOT NULL,
  source TEXT NOT NULL,
  growth_rate NUMERIC NOT NULL DEFAULT 0,
  search_demand NUMERIC NOT NULL DEFAULT 0,
  audience_interest NUMERIC NOT NULL DEFAULT 0,
  trend_velocity NUMERIC NOT NULL DEFAULT 0,
  expansion JSONB NOT NULL DEFAULT '{}',
  competition_score NUMERIC,
  opportunity_score NUMERIC,
  viral_score NUMERIC,
  predicted_ctr NUMERIC,
  predicted_retention NUMERIC,
  predicted_watch_time_seconds INT,
  monetization_score NUMERIC,
  estimated_rpm NUMERIC,
  brand_safety_score NUMERIC,
  status TEXT NOT NULL DEFAULT 'discovered',
  selected_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE research_items (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
  item_type TEXT NOT NULL,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  source_url TEXT,
  source_name TEXT,
  occurred_at TIMESTAMPTZ,
  confidence_score NUMERIC NOT NULL DEFAULT 0,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE scripts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  opportunity_id UUID NOT NULL REFERENCES opportunities(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  language TEXT NOT NULL,
  hook TEXT NOT NULL,
  introduction TEXT NOT NULL,
  act_1 TEXT NOT NULL,
  act_2 TEXT NOT NULL,
  act_3 TEXT NOT NULL,
  conclusion TEXT NOT NULL,
  call_to_action TEXT NOT NULL,
  humanized_script TEXT,
  verification_score NUMERIC NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'draft',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE scenes (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  script_id UUID NOT NULL REFERENCES scripts(id) ON DELETE CASCADE,
  scene_number INT NOT NULL,
  duration_seconds INT NOT NULL,
  visual_description TEXT NOT NULL,
  voiceover TEXT NOT NULL,
  transition TEXT,
  motion_plan TEXT,
  sound_effects TEXT[],
  music_requirements TEXT,
  metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE assets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
  project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
  scene_id UUID REFERENCES scenes(id) ON DELETE SET NULL,
  asset_type TEXT NOT NULL,
  storage_key TEXT NOT NULL,
  mime_type TEXT NOT NULL,
  provider TEXT,
  prompt TEXT,
  metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE videos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  script_id UUID REFERENCES scripts(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'planning',
  storage_key TEXT,
  duration_seconds INT,
  seo_metadata JSONB NOT NULL DEFAULT '{}',
  render_metadata JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE thumbnails (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  storage_key TEXT NOT NULL,
  variant_label TEXT NOT NULL,
  predicted_ctr NUMERIC NOT NULL DEFAULT 0,
  selected BOOLEAN NOT NULL DEFAULT false,
  metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE publishing_records (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  youtube_video_id TEXT,
  scheduled_at TIMESTAMPTZ,
  published_at TIMESTAMPTZ,
  status TEXT NOT NULL DEFAULT 'draft',
  metadata JSONB NOT NULL DEFAULT '{}',
  error_message TEXT
);

CREATE TABLE analytics_snapshots (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
  views BIGINT NOT NULL DEFAULT 0,
  ctr NUMERIC NOT NULL DEFAULT 0,
  retention NUMERIC NOT NULL DEFAULT 0,
  watch_time_seconds BIGINT NOT NULL DEFAULT 0,
  average_view_duration_seconds INT NOT NULL DEFAULT 0,
  subscribers_gained INT NOT NULL DEFAULT 0,
  revenue NUMERIC NOT NULL DEFAULT 0,
  rpm NUMERIC NOT NULL DEFAULT 0,
  engagement JSONB NOT NULL DEFAULT '{}',
  audience JSONB NOT NULL DEFAULT '{}',
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE channel_brain_profiles (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
  preference_key TEXT NOT NULL,
  preference_value TEXT NOT NULL,
  weight NUMERIC NOT NULL DEFAULT 1,
  evidence JSONB NOT NULL DEFAULT '{}',
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE(project_id, preference_key, preference_value)
);

CREATE TABLE workflows (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  project_id UUID REFERENCES projects(id) ON DELETE CASCADE,
  workflow_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  input JSONB NOT NULL DEFAULT '{}',
  output JSONB NOT NULL DEFAULT '{}',
  scheduled_at TIMESTAMPTZ,
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
  job_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  attempts INT NOT NULL DEFAULT 0,
  max_attempts INT NOT NULL DEFAULT 3,
  input JSONB NOT NULL DEFAULT '{}',
  output JSONB NOT NULL DEFAULT '{}',
  error_message TEXT,
  run_after TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at TIMESTAMPTZ,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE system_logs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  organization_id UUID REFERENCES organizations(id) ON DELETE CASCADE,
  workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
  job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,
  level TEXT NOT NULL,
  message TEXT NOT NULL,
  context JSONB NOT NULL DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_opportunities_project_score ON opportunities(project_id, status, viral_score DESC, opportunity_score DESC, monetization_score DESC);
CREATE INDEX idx_jobs_ready ON jobs(status, run_after);
CREATE INDEX idx_analytics_video_time ON analytics_snapshots(video_id, captured_at DESC);
