# DocuForge Autonomous Architecture

DocuForge Autonomous is a SaaS platform that answers daily: **what documentary should I create today to maximize views, retention, subscribers, and revenue?** It runs a closed autonomous loop: discover, expand, research, verify, score, select, generate, publish, analyze, learn, and improve.

## Services

- **Frontend**: Next.js 15 dashboard for operators, approvals, analytics, channel brain, media, publishing, billing, and administration.
- **API**: FastAPI REST service with JWT auth, Google OAuth hooks, OpenAPI docs, tenant isolation, orchestration endpoints, and agent controls.
- **Workers**: Python workflow workers backed by Redis queues for long-running research, generation, rendering, publishing, analytics, and learning jobs.
- **PostgreSQL**: System of record for tenants, projects, opportunities, research, scripts, assets, videos, publishing state, analytics, provider usage, workflows, jobs, and logs.
- **Redis**: Queue, cache, locks, health snapshots, and rate-limit counters.
- **MinIO**: Object storage for generated images, voiceovers, subtitles, thumbnails, renders, source documents, and exports.
- **Prometheus/Grafana**: Metrics, dashboards, alerts, provider health, workflow latency, queue depth, cost, and failure rates.

## Autonomous Agent Graph

1. Trend Discovery Agent ingests trend sources and creates opportunities.
2. Topic Expansion Agent enriches opportunities with questions, context, connected stories, and implications.
3. Research Agent builds timelines, facts, stats, references, quotes, people, organizations, and key events.
4. Fact Verification Agent cross-checks claims, removes unsupported statements, and emits confidence scores.
5. Competition Analysis Agent evaluates YouTube competition and opportunity gaps.
6. Viral Prediction Agent predicts viral score, CTR, retention, and watch time.
7. Monetization Prediction Agent estimates RPM, brand safety, and revenue potential.
8. Topic Selection Agent approves only opportunities exceeding configurable thresholds.
9. Script Generation Agent creates documentary scripts with hook, intro, acts, conclusion, and CTA.
10. Hindi Humanization Agent adapts narration for Hindi, English, or Hinglish with pauses and suspense.
11. Scene Planner Agent turns scripts into timed scenes with visuals, voiceover, motion, SFX, and music notes.
12. Image, Video, Motion Graphics, Voice, Sound Design, Subtitle, Thumbnail, SEO, and Publishing agents generate and ship the final YouTube package.
13. Analytics Engine imports YouTube performance metrics.
14. Channel Brain learns category, topic, language, format, thumbnail, title, and pacing preferences from every upload.

## AI Provider Router

Priority order: Groq, NVIDIA NIM, OpenRouter, local Qwen, local Llama. The router performs health checks, quota checks, retry with exponential backoff, cost-aware provider selection, rate-limit handling, usage logging, and automatic fallback.

## Workflow Engine

Workflows are durable database records with jobs. Jobs support pending, running, completed, failed, canceled, paused, and retrying states. The engine supports queueing, scheduling, retries, resume, pause, cancel, error recovery, and parallel branches.

## Security

- JWT access tokens and refresh-token rotation.
- Google OAuth account linking.
- Organization-scoped RBAC.
- Secret-based provider credentials.
- Signed object storage URLs.
- Audit logs for sensitive operations.
- Per-organization quotas and rate limits.
