# Tech Lead Code Review Guide — Day 2-3 Discovery Phase

**Purpose:** Step-by-step guide for reviewing existing code before Epic 1+2 integration

**Target Audience:** Tech Lead / Architect (Hankeol)

**When:** Day 2-3 of the integration sprint (Discovery & Architecture phase)

---

## 📋 Overview: What "Review the Code" Actually Means

"Review the code" in Day 2-3 means **understanding what already exists** so you can:

1. Identify what can be reused vs. what needs to be built
2. Define realistic API contracts based on actual implementations
3. Spot integration risks before they become blockers
4. Create accurate architecture diagrams

This is **NOT** about PR-style code reviews. It's about **discovery and documentation**.

---

## 🔍 Step-by-Step Review Checklist

### Phase 1: TypeScript Code Review (Tech Lead + Web Dev)

#### 1. Review Main Pipeline Package
**Location:** `packages/pipeline/`

**What to check:**
- [ ] What jobs already exist? → `src/jobs/*.ts`
- [ ] What's the current job structure? → Read `status-check.ts` as reference
- [ ] What utilities exist? → `src/utils/*.ts`
- [ ] What's the package.json structure? → Dependencies, scripts

**Specific actions:**
```bash
# List all existing jobs
ls -la packages/pipeline/src/jobs/

# Read each job file to understand pattern
cat packages/pipeline/src/jobs/status-check.ts

# Check dependencies
cat packages/pipeline/package.json
```

**What to document:**
| Finding | Details | Impact |
|---------|---------|--------|
| Existing jobs | status-check.ts | Reuse as template for new jobs |
| Missing jobs | pdf-ingestion, embedding-build, ontology-extraction, writer-agent | Need to create |
| Dependencies | @anthropic-ai/sdk, pg, node-cron | Add FastAPI client, axios/fetch |

---

#### 2. Review Web Apps Structure
**Location:** `apps/api` and `apps/web`

**What to check:**
- [ ] NestJS API structure → `apps/api/src/`
- [ ] Next.js web structure → `apps/web/src/`
- [ ] Existing API routes → What endpoints exist?
- [ ] Database connection setup → How is Postgres connected?

**Specific actions:**
```bash
# Find all API controllers/route handlers
find apps/api/src -name "*.controller.ts" -o -name "*.route.ts"

# Check database configuration
cat apps/api/src/database/database.service.ts
# or similar file
```

**What to document:**
| Finding | Details | Impact |
|---------|---------|--------|
| API framework | NestJS | Can add Python integration module |
| DB connection | Prisma? raw pg? | Determines how to call Python APIs |
| Auth setup | None? JWT? | Affects Python API security |

---

### Phase 2: Python Code Review (All Team Members)

#### 3. Review Ontology Package (AI Engineer focus)
**Location:** `dev/packages/ontology/`

**What to check:**
- [ ] Entry points → What scripts/commands run this?
- [ ] Main classes → `ontology_graph_manager.py`, `graph_query_engine.py`
- [ ] Dependencies → `requirements.txt` or `pyproject.toml`
- [ ] GraphDB connection → How is Neptune/GraphDB connected?
- [ ] Current API surface → What functions are public?

**Specific actions:**
```bash
# List all Python modules
find dev/packages/ontology/src -name "*.py" -not -path "*/.venv/*"

# Check dependencies
cat dev/packages/ontology/requirements.txt
# or
cat dev/packages/ontology/pyproject.toml

# Find main entry points
cat dev/packages/ontology/src/__init__.py
```

**Code review template for ontology:**

For each major module, document:
```markdown
### Module: `ontology_graph_manager.py`
- **Purpose:** Manages ontology graph using NetworkX
- **Key classes:** `OntologyGraphManager`
- **Key methods to expose as API:**
  - `stage_add_concept(concept_id, parent_id, label, description)` → POST /ontology/extract
  - `commit_staging()` → POST /ontology/update
- **Dependencies:** networkx, GraphQueryEngine, VectorStore
- **State management:** Has `real_graph` and `staging_graph` - affects API design
- **Issues/notes:** Korean comments, complex graph logic
```

**What to document overall:**
| Component | Current State | API Exposure Plan |
|-----------|---------------|-------------------|
| Ontology extraction | ConceptMatcher class | POST /ontology/extract |
| Graph update | OntologyGraphManager.commit_staging() | POST /ontology/update |
| Graph query | GraphQueryEngine.query() | Internal use (or GET /ontology/query) |
| Vector search | VectorStore.find_similar() | Part of /ontology/extract |

---

#### 4. Review PDF Extractor Package (ETL Pipeline Builder focus)
**Location:** `dev/packages/pdf_knowledge_extractor/`

**What to check:**
- [ ] Entry points → `run_pipeline.py`, `run_chapters.py`
- [ ] PDF processing logic → What libraries? (pdfplumber, pypdf?)
- [ ] Chunking strategy → How are chunks created?
- [ ] Output format → What data structure?
- [ ] Dependencies → `requirements.txt`

**Specific actions:**
```bash
# List Python files
find dev/packages/pdf_knowledge_extractor -name "*.py" -not -path "*/.venv/*"

# Check main script
cat dev/packages/pdf_knowledge_extractor/run_pipeline.py

# Check dependencies
cat dev/packages/pdf_knowledge_extractor/requirements.txt
```

**Code review template for PDF extractor:**
```markdown
### Module: PDF Pipeline
- **Entry point:** `run_pipeline.py` → `python run_pipeline.py <pdf_path>`
- **Main functions:**
  - `extract_pdf(path)` → Returns text/structured data
  - `chunk_text(text, strategy)` → Returns list of chunks
  - `generate_embeddings(chunks)` → Returns vectors
- **Output:** Saves to ? (Postgres? files?)
- **Dependencies:** pdfplumber, langchain, anthropic
- **Issues/notes:**
  - Needs refactoring into functions (not scripts)
  - No error handling
  - Hardcoded paths
```

**What to document:**
| Component | Current State | API Exposure Plan |
|-----------|---------------|-------------------|
| PDF extraction | Script-based | POST /pdf/extract |
| Chunking | Hybrid/TOC-based | POST /pdf/chunk |
| Embeddings | OpenAI embeddings | POST /embeddings/generate |

---

### Phase 3: Feature Branch Review (All Team Members)

#### 5. Review Feature Branches
**Branches to check:**
- `feat/pdf-extractor-v2` (ETL)
- `feat/pdf-knowledge-extractor` (ETL)
- `feature/ontology` (AI Engineer)
- `feat/agent-writer` (AI Engineer)

**For each branch:**
```bash
# Check out branch
git checkout feat/pdf-extractor-v2

# See what changed
git diff main..feat/pdf-extractor-v2 --stat

# Read key new files
git diff main..feat/pdf-extractor-v2 -- <specific_file>

# Return to main
git checkout main
```

**What to document per branch:**
```markdown
### Branch: `feat/pdf-extractor-v2`
- **Purpose:** Improved PDF extraction with better chunking
- **Key changes:**
  - New: `hybrid_chunking.py` → Expose as API
  - Changed: PDF metadata extraction
  - Removed: Old regex-based chunker
- **Ready for integration:** Yes/No
- ** blockers:** None / needs refactoring / conflicts with main
```

---

### Phase 4: Infrastructure & Database Review (Tech Lead)

#### 6. Review Database Schema
**Location:** `docs/architecture/ddl-v1.0.sql`

**What to check:**
- [ ] What schemas exist? (core, handbook, content, concept, snapshot)
- [ ] What tables exist in each schema?
- [ ] What are foreign key relationships?
- [ ] What indexes exist?
- [ ] Is pgvector extension used?

**Specific actions:**
```bash
# Read DDL
cat docs/architecture/ddl-v1.0.sql | grep "CREATE TABLE" | head -20

# Check for pgvector
cat docs/architecture/ddl-v1.0.sql | grep -i vector

# Check handbook schema (for PDF chunks)
cat docs/architecture/ddl-v1.0.sql | grep -A 20 "handbook\."
```

**What to document:**
| Schema | Tables | Purpose | Integration Notes |
|--------|--------|---------|-------------------|
| handbook | paragraph_chunk, paragraph_embedding | PDF evidence | Python writes here |
| content | article, source | Curated content | Notion sync |
| concept | concept_page, concept_changelog | Writer Agent output | TS orchestrates |
| core | pipeline_run, prompt_template | Pipeline control | TS orchestration |

---

#### 7. Review Docker Infrastructure
**Location:** `docker-compose.yml`

**What to check:**
- [ ] What services are defined?
- [ ] What ports are exposed?
- [ ] What environment variables are needed?
- [ ] Is GraphDB/Neptune included?

**Specific actions:**
```bash
# Check services
cat docker-compose.yml | grep -E "^\s+\w+:" | head -10

# Check ports
cat docker-compose.yml | grep -E "ports:"
```

**What to document:**
| Service | Port | Purpose | Integration Impact |
|---------|------|---------|-------------------|
| postgres | 5432 | Main DB | Python needs connection string |
| graphdb | 7200 | Ontology | Python connects directly |
| python-api | 8000 | FastAPI server | NEW - need to add |
| redis | 6379 | Cache | Optional for Python API |

---

## 📝 Code Review Output Template

Create a shared doc (Google Doc or `docs/team/code-review-findings.md`) with:

### Section 1: TypeScript State
```
Existing jobs:
- [x] status-check.ts - Pattern for new jobs
- [ ] pdf-ingestion.ts - TODO
- [ ] embedding-build.ts - TODO
- [ ] ontology-extraction.ts - TODO
- [ ] writer-agent.ts - TODO

Package structure:
- packages/pipeline/src/jobs/ - Job scripts
- packages/pipeline/src/integrations/ - TODO (create for Python client)
- packages/pipeline/src/utils/ - Helpers

Dependencies to add:
- axios or fetch (for Python API calls)
- @types/node-cron (already there)
```

### Section 2: Python State
```
Ontology package (dev/packages/ontology/):
- ✓ Working GraphDB integration
- ✓ Vector store (ChromaDB)
- ✗ No API layer (need FastAPI)
- ✗ Script-based entry points (refactor needed)

PDF extractor package (dev/packages/pdf_knowledge_extractor/):
- ✓ PDF parsing works
- ✓ Chunking implemented
- ✗ No API layer (need FastAPI)
- ✗ No error handling

Common dependencies to standardize:
- fastapi >= 0.104.0
- uvicorn >= 0.24.0
- pydantic >= 2.0
- anthropic >= 0.7.0
- langchain >= 0.1.0
```

### Section 3: Integration Points
```
1. TS → Python (HTTP)
   - Base URL: http://localhost:8000/api/v1
   - Auth: Shared API key header
   - Timeout: 5 minutes default

2. Python → Postgres
   - Direct connection via psycopg3
   - Connection string from env: DATABASE_URL

3. Python → GraphDB
   - Direct connection (existing)
   - Keep as-is

4. Python → Claude API
   - Anthropic SDK (existing)
   - Keep as-is
```

### Section 4: Risks & Issues
```
High Priority:
- [ ] PDF extractor has no error handling → Add try/catch
- [ ] No Python API layer exists → Build FastAPI wrapper
- [ ] Feature branches may have conflicts → Test merge early

Medium Priority:
- [ ] GraphDB connection strings hardcoded → Move to env
- [ ] Different Python versions possible → Standardize on 3.12
- [ ] No tests for Python code → Add pytest

Low Priority:
- [ ] Korean comments in ontology package → Translate to English
- [ ] Inconsistent code style → Add black/flake8
```

---

## 🎯 Decision Points

After code review, make these decisions:

### Decision 1: Python API Server Structure
```
Option A: Single FastAPI server (recommended)
- pros: Simpler deployment, one port
- cons: Mixed concerns

Option B: Separate servers (ETL + AI)
- pros: Independent scaling
- cons: More complex, 2 ports to manage

CHOICE: Option A - Single server with route groups
```

### Decision 2: TypeScript Integration Pattern
```
Option A: HTTP client (recommended)
- pros: Standard, debuggable, language-agnostic
- cons: Network overhead

Option B: Python process spawning
- pros: No network, faster
- cons: Harder to debug, coupling

CHOICE: Option A - HTTP with fetch/axios
```

### Decision 3: Database Access Pattern
```
Question: Should Python write directly to Postgres, or return data to TS?

Option A: Python writes directly (recommended for bulk)
- Use for: PDF chunks, embeddings (large data)
- Reason: Avoid passing large payloads through HTTP

Option B: Python returns, TS writes (recommended for metadata)
- Use for: Pipeline runs, status updates
- Reason: Keep transaction control in TS

CHOICE: Hybrid - Python writes bulk data, TS writes metadata
```

---

## 📅 Day 2-3 Timeline

### Day 2 Morning (2 hours)
- [ ] Tech Lead: Review TypeScript structure
- [ ] AI Engineer: Review ontology package
- [ ] ETL Builder: Review PDF extractor package

### Day 2 Afternoon (2 hours)
- [ ] Tech Lead: Review DDL and docker-compose
- [ ] Web Dev: Review apps/api and apps/web
- [ ] All: Document findings in shared doc

### Day 3 Morning (2 hours)
- [ ] Tech Lead: Review feature branches
- [ ] All: Test running existing code locally
- [ ] All: Identify what needs to be refactored

### Day 3 Afternoon (2 hours)
- [ ] Tech Lead: Synthesize findings into architecture diagram
- [ ] All: Define and sign off on API contract
- [ ] Tech Lead: Create detailed implementation task list

---

## ✅ Completion Criteria

Day 2-3 "Review the code" is complete when:

1. **Documentation exists:** Every team member has documented their component
2. **API contract defined:** All endpoints specified with request/response schemas
3. **Risks identified:** Critical blockers listed with mitigation plans
4. **Architecture finalized:** Diagram shows all components and communication paths
5. **Sign-off obtained:** All team members agree on the integration approach

---

## 🔗 References

- Original integration plan: `_bmad-output/planning-artifacts/epic-1-2-team-integration-plan.md`
- API contract template: (same file, section "API Contract")
- Architecture decisions: `docs/architecture/adr-*.md`

---

**Created:** 2026-04-07
**For:** Epic 1+2 Integration Sprint
**Version:** 1.0
