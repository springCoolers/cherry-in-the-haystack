# Memo: Codebase Restructure — TypeScript and Python Services

**To:** Team
**From:** Hankeol (Tech Lead)
**Date:** 2026-04-07
**Subject:** Final codebase structure and upcoming FastAPI server creation

---

## Summary

We've finalized the codebase structure after migrating from `dev/`. Here's what changed and what's coming next.

---

## New Structure

```
cherry-in-the-haystack/
├── apps/                       # TypeScript apps (NestJS, Next.js)
│   ├── api/                     # Port 4000
│   └── web/                     # Port 3000
├── python_services/             # Python services
│   ├── packages/                # Reusable Python packages
│   │   ├── agent/
│   │   ├── idea_to_graph_ontology/
│   │   ├── news_collector/
│   │   └── text_extract_ideas/
│   └── api/                     # ← NEW: FastAPI server (Port 8000)
├── docs/
├── _bmad-output/
└── docker-compose.yml
```

---

## What Changed

| Before | After | Why |
|--------|-------|-----|
| `dev/packages/*` | `python_services/packages/*` | Clearer grouping of Python code |
| Root `pyproject.toml` | Root `pyproject.toml` (consolidated) | Single source of truth for Python deps |
| Scattered Python deps | Consolidated at root | Easier dependency management |
| No FastAPI server | `python_services/api/` (coming soon) | Unified Python API endpoint |

---

## Why This Structure?

### 1. TypeScript and Python are Separate Worlds

**They cannot share modules.** Different runtimes, different dependency systems.

- TypeScript → Node.js → pnpm workspaces → `apps/`
- Python → CPython → Poetry → `python_services/`

**Communication:** HTTP (TS calls Python via `fetch`/`axios`)

### 2. `apps/` Stays at Root (Not `next_js_webapp/`)

**Why:** pnpm workspace requires `node_modules` at root.

Moving `apps/` into a subfolder would break:
- Workspace resolution
- All import paths
- pnpm's dependency sharing

### 3. `python_services/api/` Works (Unlike `next_js_webapp/`)

**Why:** Python has no "workspace" constraint.

- Imports are flexible (relative, `sys.path`, `PYTHONPATH`)
- Poetry doesn't require root-level structure
- Docker builds are simpler with grouped Python code

---

## Port Allocation (Final)

| Service | Port | Technology |
|---------|------|------------|
| Web frontend | 3000 | Next.js |
| Web backend (NestJS) | 4000 | TypeScript |
| Python API (FastAPI) | 8000 | Python |
| PostgreSQL | 5432 | - |
| GraphDB | 7200 | - |
| Redis | 6379 | - |

---

## What's Next: FastAPI Server

We're creating `python_services/api/` — a single FastAPI server that exposes all Python packages.

**Endpoints:**
```
POST /api/v1/pdf/extract          → text_extract_ideas package
POST /api/v1/ontology/extract     → idea_to_graph_ontology package
POST /api/v1/ontology/update      → idea_to_graph_ontology package
POST /api/v1/writer/generate      → agent package
POST /api/v1/news/collect         → news_collector package
GET  /api/v1/health               → Health check
```

**TypeScript client** will be created in `packages/pipeline/src/integrations/python-client.ts`

---

## Development Workflow

### Running Services

```bash
# Terminal 1: NestJS backend
cd apps/api && pnpm dev

# Terminal 2: Next.js frontend
cd apps/web && pnpm dev

# Terminal 3: FastAPI server
cd python_services/api && uvicorn main:app --reload

# Terminal 4: Docker services
docker-compose up
```

### Adding a New Python Package

1. Create package in `python_services/packages/my_package/`
2. Add to `python_services/api/routes/my_package.py`
3. Register route in `python_services/api/main.py`

---

## Documentation

- **ADR:** `docs/architecture/code-structure-decision.md` (ADR-010)
- **API Contract:** `_bmad-output/planning-artifacts/epic-1-2-team-integration-plan.md`

---

**Questions? Ask in #engineering or ping me directly.**

— Hankeol
