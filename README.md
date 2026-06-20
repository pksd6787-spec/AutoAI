# DocuForge Autonomous



- Architecture document in `docs/ARCHITECTURE.md`
- PostgreSQL schema in `db/migrations/001_initial_schema.sql`
- FastAPI backend with agent framework, provider router, workflow planner, channel brain, and REST endpoints
- Next.js dashboard shell with all requested product areas
- Docker Compose, Kubernetes deployment starter, and CI pipeline


## Run locally

```bash
docker compose up --build
```

API docs: http://localhost:8000/docs
