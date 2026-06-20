# DocuForge Autonomous

Production-oriented SaaS foundation for an autonomous AI-powered YouTube documentary business system.

The platform is designed to answer every day:

> What documentary should I create today to maximize views, retention, subscribers, and revenue?

## Implemented so far

### Phase 1

- Architecture document in `docs/ARCHITECTURE.md`
- PostgreSQL schema in `db/migrations/001_initial_schema.sql`
- FastAPI backend with agent framework, provider router, workflow planner, channel brain, and REST endpoints
- Next.js dashboard shell with all requested product areas
- Docker Compose, Kubernetes deployment starter, and CI pipeline

### Phase 2

- JWT/password security helpers and Google OAuth URL/scopes for YouTube upload and analytics access
- Expanded schema for RBAC roles, refresh tokens, OAuth accounts, provider usage events, billing customers, and subscriptions
- Content pipeline services for script generation, narration humanization, scene planning, SEO metadata, subtitles, image prompts, voice plans, and render plans
- Additional agents for research, fact verification, competition analysis, and thumbnail variant prediction
- Analytics insight engine and Channel Brain-ready improvement recommendations
- API endpoints for Google OAuth URL generation, full content pipeline planning, and analytics insights
- Unit tests for provider fallback, agent thresholds, verification, viral prediction, and content/media planning


### Phase 3

- Executable workflow runtime with create, enqueue, run-next, pause, resume, cancel, retry state, queue depth, and job output tracking
- Provider health snapshots and token-cost estimation primitives for quota/cost operations
- Workflow and provider health API endpoints
- Workflow dashboard page for queue, retry, pause/resume, and parallel-job visibility
- Additional unit tests for workflow runtime state transitions and provider health/cost behavior

## Run locally

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs

## Run checks

```bash
python -m compileall backend/app
PYTHONPATH=backend pytest -q
```
