# Architecture

## Executive Summary

cherry-in-the-haystack transforms an existing Auto-News infrastructure into The LLM Engineering Handbook through a multi-stage architecture combining proven pipeline technology (Apache Airflow) with modern static site generation (Jupyter Book). The architecture prioritizes automation, quality, and weekly update velocity while maintaining 99.5% uptime and sub-2-second page loads.

## Project Initialization

**First Implementation Story: Handbook Foundation Setup**

The project builds on existing Auto-News infrastructure while establishing new handbook-specific components:

### Jupyter Book Initialization (NEW)
```bash
# Create Jupyter Book structure for handbook publication
pip install jupyter-book==1.0.4
jupyter-book create handbook-content
cd handbook-content
jupyter-book build .
```

This establishes the publication layer with professional documentation site infrastructure.

### Python Pipeline Structure (ADAPT EXISTING)
```bash
# Modern Python tooling for handbook pipeline
pip install poetry ruff loguru
poetry init

# Project structure follows 2024 best practices:
# - Separation of Auto-News engine from handbook-specific pipeline
# - Modular operator design (ingestion, deduplication, scoring, synthesis)
# - Modern tooling: Ruff (linting), Poetry (dependencies), Loguru (logging)
```

**Starter-Provided Architectural Decisions:**

### From Jupyter Book Starter:
- **Static Site Generator:** Jupyter Book 1.0.4 (Sphinx-based)
- **Build System:** sphinx-build with MyST-NB markdown parser
- **Theme:** PyData Sphinx Theme (mobile-responsive, accessible)
- **Search:** Built-in Sphinx search (no additional setup)
- **Configuration:** YAML-based (_config.yml, _toc.yml)
- **Deployment Target:** Static HTML/CSS/JS (GitHub Pages compatible)
- **Content Format:** MyST Markdown + Jupyter Notebooks

### From Modern Python Pipeline Structure:
- **Linting/Formatting:** Ruff (replaces isort, flake8, pylint)
- **Dependency Management:** Poetry with pyproject.toml
- **Logging Framework:** Loguru (structured logging)
- **Code Style:** @dataclass for data models, type hints throughout
- **Project Structure:** Modular separation (config/, db_connection/, pipeline/)
- **Existing Foundation:** Apache Airflow for orchestration (keep existing)

**Note:** Story 1.1 (Project Initialization) should execute these commands to establish base architecture.

## Project Context Understanding

**Project:** cherry-in-the-haystack (The LLM Engineering Handbook)

**Scale & Complexity:**
- 6 epics with 40 total stories
- Medium complexity web application + API backend (hybrid)
- Target: 50,000 monthly users within 6 months
- 20+ active contributors expanding to 50+

**Core Functionality:**
The product transforms the existing Auto-News personal content curation tool into The LLM Engineering Handbook - a living, community-driven knowledge base serving as the default reference for AI product builders. The system provides:
- Continuously updated, structured map of LLM engineering knowledge
- Multi-stage pipeline: Content Ingestion → Human Review → AI Synthesis → Public Handbook
- MECE (Mutually Exclusive, Collectively Exhaustive) taxonomy for clarity
- Weekly automated updates maintaining content freshness

**Critical NFRs:**
- **Performance:** Page load under 2 seconds on 3G, search results under 500ms
- **Reliability:** 99.5% uptime, weekly publish cycle 100% execution rate
- **Scalability:** Support 1,000+ handbook pages, 50,000 monthly visitors, 50+ contributors
- **Update Velocity:** Content published within 48 hours of approval
- **Quality:** 90%+ approval rating from human reviewers, 95% coverage of LLM engineering topics

**Brownfield Context:**
- Existing Auto-News codebase with Apache Airflow DAGs
- Proven event-driven data pipeline for content aggregation
- LLM-powered categorization, ranking, and summarization capabilities
- Current output to Notion workspaces (to be transformed to handbook pipeline)

**Unique Challenges:**
- Chunk-level deduplication at scale (paragraph-level similarity detection)
- AI-powered quality scoring (1-5 scale) with cost optimization
- Multi-LLM provider support with graceful fallback (OpenAI, Gemini, Ollama)
- Weekly automated publication pipeline: Postgres → GitHub → Jupyter Book → GitHub Pages
- Novel pattern: Human-in-the-loop AI synthesis with peer review workflow

## Decision Summary

| Category | Decision | Version | Affects Epics | Rationale |
| -------- | -------- | ------- | ------------- | --------- |
| **CRITICAL DECISIONS** |
| Static Site Generator | Jupyter Book | 1.0.4 | Epic 4 (Publication) | PROVIDED BY STARTER - Professional docs site, GitHub Pages compatible, built-in search |
| Python Tooling | Poetry + Ruff + Loguru | Latest | All Epics | PROVIDED BY STARTER - Modern 2024 best practices, Ruff replaces 3 tools |
| Orchestration | Apache Airflow | Existing | Epic 2 (Ingestion) | BROWNFIELD - Keep existing Auto-News orchestration |
| Relational Database | Amazon RDS PostgreSQL | PostgreSQL 16 | All Epics | Usage-based pricing fits batch workload, ~$25/month, automated backups, AWS-native |
| Vector Database | pgvector (PostgreSQL extension) | 0.8.0 | Epic 2, 3 (Dedup, Synthesis) | $0 cost, simplified architecture, handles 100K+ vectors, <100ms queries |
| Primary LLM (Scoring) | OpenAI GPT-4o-mini | Latest | Epic 2 (Quality Scoring) | $0.15-0.60/1M tokens, reliable structured output, perfect for batch scoring |
| Secondary LLM (Synthesis) | Anthropic Claude 3.5 Sonnet | Latest | Epic 3 (AI Synthesis) | $3-15/1M tokens, superior prose quality, 200K context for documents |
| Fallback LLM | Google Gemini 1.5 Flash | Latest | All LLM tasks | $0.075-0.30/1M tokens, 80% cheaper fallback, 1M token context |
| Embedding Model | OpenAI text-embedding-3-small | Latest | Epic 2, 3 (Deduplication) | $0.02/1M tokens, 1536 dims, 95%+ accuracy, ~$1 one-time for 100K chunks |
| **IMPORTANT DECISIONS** |
| Airflow Hosting | Existing Setup | Current Version | Epic 2 (Ingestion) | BROWNFIELD - Keep existing Auto-News Airflow deployment, migrate to MAWA later if needed |
| Notion Integration | Polling (5 min intervals) | Notion API v2 | Epic 2 (Review Workflow) | Simple, reliable, respects 3 req/sec rate limit, Airflow DAG scheduled task |
| GitHub Automation | Bot Account with PAT | GitHub API v3 | Epic 4 (Publication) | Dedicated bot account (handbook-bot), PAT with repo write, clear attribution |
| Vector DB Hosting | RDS PostgreSQL (same DB) | pgvector 0.8.0 | Epic 2, 3 | No separate service needed, pgvector extension in RDS, ivfflat indexes |
| LLM Fallback Strategy | Sequential with Exponential Backoff | N/A | All LLM tasks | GPT-4o-mini → Gemini Flash → Dead-letter queue, 1/2/4 min backoff |
| **NICE-TO-HAVE DECISIONS** |
| Monitoring Solution | AWS CloudWatch + Airflow UI | Built-in | All Epics | Start with CloudWatch for RDS/infrastructure, Airflow UI for DAGs, upgrade to Grafana later |
| Alerting Channels | Email + Slack webhook | N/A | Operations | Email for non-urgent, Slack for moderate/critical, PagerDuty later if needed |
| Local Development | Docker Compose | Latest | Development | Postgres + pgvector + ChromaDB in Docker, matches CI environment |
| Testing Framework | pytest + pytest-cov | Latest | All Epics | 70% coverage target, unit + integration tests, pytest fixtures for test data |
| Error Handling | Retry with Dead-Letter Queue | N/A | All Pipelines | 3 retries with exponential backoff, DLQ for permanent failures, manual review workflow |

## Project Structure

```
cherry-in-the-haystack/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                          # Linting, tests, type checking
│   │   ├── deploy.yml                      # Jupyter Book build & GitHub Pages deploy
│   │   └── link-check.yml                  # Weekly broken link validation
│   ├── ISSUE_TEMPLATE/
│   │   ├── report-error.md                 # Content error reporting
│   │   └── submit-source.md                # URL submission for Auto-News
│   └── pull_request_template.md            # PR template with checklist
│
├── auto-news-engine/                       # Existing Auto-News codebase
│   ├── dags/                               # Airflow DAGs (existing)
│   ├── operators/                          # Reusable Auto-News operators
│   ├── config/                             # Auto-News configuration
│   └── tests/                              # Auto-News tests
│
├── handbook/                                # New handbook-specific pipeline
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py                     # Environment variables, configs
│   │   ├── logging_config.py               # Loguru configuration
│   │   └── llm_config.py                   # Multi-provider LLM setup
│   │
│   ├── db_connection/
│   │   ├── __init__.py
│   │   ├── postgres.py                     # RDS PostgreSQL connector
│   │   └── pgvector.py                     # pgvector operations wrapper
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── ingestion/
│   │   │   ├── __init__.py
│   │   │   ├── twitter_operator.py         # Twitter content aggregation
│   │   │   ├── discord_operator.py         # Discord monitoring
│   │   │   ├── github_operator.py          # GitHub releases/discussions
│   │   │   └── rss_operator.py             # RSS feed polling
│   │   │
│   │   ├── deduplication/
│   │   │   ├── __init__.py
│   │   │   ├── embedder.py                 # OpenAI embedding generation
│   │   │   ├── similarity.py               # pgvector similarity search
│   │   │   └── chunker.py                  # Semantic chunking (LangChain)
│   │   │
│   │   ├── scoring/
│   │   │   ├── __init__.py
│   │   │   ├── ai_scorer.py                # LLM-based quality scoring
│   │   │   ├── scoring_prompts.py          # Version-controlled prompts
│   │   │   └── fallback_handler.py         # Multi-LLM fallback logic
│   │   │
│   │   ├── synthesis/
│   │   │   ├── __init__.py
│   │   │   ├── basics_synthesizer.py       # Basics section synthesis
│   │   │   ├── advanced_synthesizer.py     # Advanced section synthesis
│   │   │   ├── synthesis_prompts.py        # Claude synthesis prompts
│   │   │   └── citation_manager.py         # Source citation tracking
│   │   │
│   │   └── publication/
│   │       ├── __init__.py
│   │       ├── postgres_to_github.py       # Weekly batch Postgres → GitHub
│   │       ├── markdown_formatter.py       # Content → Markdown conversion
│   │       └── github_committer.py         # Bot account commit logic
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── notion_client.py                # Notion API polling
│   │   └── github_client.py                # GitHub API wrapper
│   │
│   ├── dags/
│   │   ├── __init__.py
│   │   ├── ingestion_dag.py                # Daily content ingestion
│   │   ├── scoring_dag.py                  # AI scoring pipeline
│   │   ├── notion_sync_dag.py              # Notion bidirectional sync
│   │   └── publication_dag.py              # Weekly Postgres → GitHub → Deploy
│   │
│   └── models/
│       ├── __init__.py
│       ├── content.py                      # Content dataclasses
│       ├── embeddings.py                   # Embedding dataclasses
│       └── review.py                       # Review status dataclasses
│
├── handbook-content/                        # Jupyter Book content (public handbook)
│   ├── _config.yml                         # Jupyter Book configuration
│   ├── _toc.yml                            # Table of contents (3 sections)
│   ├── _static/
│   │   ├── custom.css                      # Custom branding styles
│   │   └── logo.svg                        # Project logo
│   │
│   ├── basics/                             # Basics section
│   │   ├── index.md                        # Basics landing page
│   │   ├── prompting/
│   │   │   ├── index.md                    # Parent concept
│   │   │   ├── basic-prompting.md          # Child implementation
│   │   │   └── prompt-templates.md         # Child implementation
│   │   ├── rag/
│   │   │   ├── index.md
│   │   │   ├── naive-rag.md
│   │   │   └── advanced-rag.md
│   │   ├── fine-tuning/
│   │   ├── agents/
│   │   ├── embeddings/
│   │   └── evaluation/
│   │
│   ├── advanced/                           # Advanced section
│   │   ├── index.md
│   │   ├── prompting/
│   │   │   ├── chain-of-thought.md
│   │   │   └── constitutional-ai.md
│   │   ├── rag/
│   │   └── ... (same structure as basics)
│   │
│   └── newly-discovered/                   # Newly Discovered section
│       ├── index.md                        # Landing with card layouts
│       ├── model-updates/
│       │   └── 2025-11-08-gpt45-release.md
│       ├── framework-updates/
│       ├── productivity-tools/
│       ├── business-cases/
│       └── how-people-use-ai/
│
├── tests/
│   ├── unit/
│   │   ├── test_embedder.py
│   │   ├── test_scorer.py
│   │   └── test_synthesizer.py
│   ├── integration/
│   │   ├── test_postgres_pgvector.py
│   │   ├── test_notion_sync.py
│   │   └── test_github_commit.py
│   └── fixtures/
│       └── sample_content.json
│
├── docs/                                    # Project documentation (separate from handbook)
│   ├── PRD.md                              # Product requirements (existing)
│   ├── epics.md                            # Epic breakdown (existing)
│   ├── architecture.md                     # This document
│   └── bmm-workflow-status.yaml            # Workflow tracking (existing)
│
├── scripts/
│   ├── setup_pgvector.sql                  # Database initialization
│   ├── seed_basics.py                      # Initial content seeding
│   └── backup_vector_db.py                 # Vector DB backup script
│
├── .env.example                            # Environment variable template
├── .gitignore                              # Python, Node, env files
├── docker-compose.yml                      # Local dev: Postgres + pgvector
├── pyproject.toml                          # Poetry dependencies
├── poetry.lock                             # Locked dependencies
├── README.md                               # Project overview
├── CONTRIBUTING.md                         # Contribution guidelines
├── STYLE_GUIDE.md                          # Content style guide
└── LICENSE                                 # Open source license
```

## Epic to Architecture Mapping

| Epic | Stories | Architecture Components | Key Technologies |
|------|---------|------------------------|------------------|
| **Epic 1: Foundation & Core Infrastructure** | 1.1-1.7 (7 stories) | - `pyproject.toml` (Poetry)<br>- `handbook/config/` (settings, logging)<br>- `handbook/db_connection/` (Postgres, pgvector)<br>- `auto-news-engine/` (adapt existing)<br>- `.github/workflows/` (CI/CD)<br>- `handbook-content/_config.yml` (Jupyter Book)<br>- `docker-compose.yml`, `tests/` | - RDS PostgreSQL 16 + pgvector 0.8.0<br>- Poetry + Ruff + Loguru<br>- Jupyter Book 1.0.4<br>- GitHub Actions<br>- Docker Compose |
| **Epic 2: Intelligent Content Ingestion Pipeline** | 2.1-2.6 (6 stories) | - `handbook/pipeline/ingestion/` (operators)<br>- `handbook/pipeline/deduplication/` (embedder, similarity)<br>- `handbook/pipeline/scoring/` (AI scorer, fallback)<br>- `handbook/integrations/notion_client.py`<br>- `handbook/dags/ingestion_dag.py`<br>- `handbook/dags/scoring_dag.py`<br>- `handbook/dags/notion_sync_dag.py` | - OpenAI text-embedding-3-small<br>- GPT-4o-mini (scoring)<br>- Gemini 1.5 Flash (fallback)<br>- pgvector ivfflat indexes<br>- Notion API v2<br>- Apache Airflow |
| **Epic 3: AI-Powered Knowledge Synthesis** | 3.1-3.7 (7 stories) | - `handbook/pipeline/synthesis/` (synthesizers, prompts)<br>- `handbook/pipeline/deduplication/chunker.py`<br>- `handbook-content/_toc.yml` (MECE taxonomy)<br>- `handbook-content/basics/` (6 parent topics)<br>- `handbook-content/advanced/` (6 domains)<br>- `handbook/models/content.py` | - Claude 3.5 Sonnet (synthesis)<br>- pgvector (chunk deduplication)<br>- LangChain (semantic chunking)<br>- 200K context window |
| **Epic 4: Automated Publication System** | 4.1-4.7 (7 stories) | - `handbook/pipeline/publication/` (Postgres→GitHub)<br>- `handbook-content/_static/` (custom CSS, logo)<br>- `handbook-content/newly-discovered/` (card layouts)<br>- `handbook/integrations/github_client.py`<br>- `.github/workflows/deploy.yml`<br>- `handbook/dags/publication_dag.py` | - GitHub Bot Account + PAT<br>- Jupyter Book build system<br>- sphinx-design (card layouts)<br>- GitHub Pages<br>- Weekly cron trigger |
| **Epic 5: Community Contribution Framework** | 5.1-5.6 (6 stories) | - `.github/ISSUE_TEMPLATE/` (error reports, URL submission)<br>- `.github/pull_request_template.md`<br>- `CONTRIBUTING.md`, `STYLE_GUIDE.md`<br>- `.github/workflows/ci.yml` (PR validation)<br>- `templates/` (content templates) | - GitHub PR workflow<br>- markdown-lint<br>- link validation<br>- CODEOWNERS for auto-assignment |
| **Epic 6: Content Quality & Lifecycle Management** | 6.1-6.7 (7 stories) | - `.github/workflows/link-check.yml`<br>- `handbook/pipeline/scoring/` (multi-stage gates)<br>- `scripts/` (monitoring, backups)<br>- AWS CloudWatch integration<br>- Dead-letter queue in Postgres | - CloudWatch + Airflow UI<br>- Email + Slack webhooks<br>- pytest + pytest-cov (70% coverage)<br>- Exponential backoff + retry logic |

### Architecture Boundaries by Epic

**Epic 1-2 (Data Pipeline Layer):**
- Airflow DAGs orchestrate ingestion, deduplication, scoring
- pgvector stores embeddings in RDS Postgres
- Multi-LLM fallback (GPT-4o-mini → Gemini Flash)
- Notion API polls for review status every 5 minutes

**Epic 3 (AI Synthesis Layer):**
- Claude 3.5 Sonnet synthesizes Basics/Advanced content
- Chunk-level deduplication prevents redundancy
- MECE taxonomy enforced in `_toc.yml`
- Parent-child hierarchy (2 levels max)

**Epic 4 (Publication Layer):**
- Weekly batch: Approved content → Markdown → GitHub commit
- GitHub Actions triggers Jupyter Book build automatically
- Deploys to GitHub Pages (`gh-pages` branch)
- Zero-downtime deployments

**Epic 5-6 (Quality & Community Layer):**
- GitHub PR workflow for content contributions
- Multi-stage approval gates (AI → Human → Automated checks)
- Link validation + staleness detection
- CloudWatch monitoring + Slack alerts

## Technology Stack Details

### Core Technologies

**Backend Pipeline:**
- **Language:** Python 3.10+ (for Airflow compatibility and modern type hints)
- **Dependency Management:** Poetry 1.8+ with pyproject.toml
- **Orchestration:** Apache Airflow (existing Auto-News deployment)
- **Linting/Formatting:** Ruff (replaces isort, flake8, pylint)
- **Logging:** Loguru (structured logging with JSON output)
- **Testing:** pytest 8.0+, pytest-cov, pytest-mock

**Databases:**
- **Relational:** Amazon RDS PostgreSQL 16 (db.t3.small, 20GB gp3)
- **Vector:** pgvector 0.8.0 extension (ivfflat indexes with cosine similarity)
- **Connection Pooling:** psycopg3 with connection pooling

**LLM Providers:**
- **Primary (Scoring):** OpenAI GPT-4o-mini via openai==1.x Python SDK
- **Secondary (Synthesis):** Anthropic Claude 3.5 Sonnet via anthropic==0.x SDK
- **Fallback:** Google Gemini 1.5 Flash via google-generativeai SDK
- **Embeddings:** OpenAI text-embedding-3-small (1536 dimensions)

**Publication:**
- **Static Site Generator:** Jupyter Book 1.0.4 (Sphinx-based)
- **Theme:** PyData Sphinx Theme (responsive, accessible)
- **Extensions:** sphinx-design, sphinx-togglebutton, sphinxext-opengraph
- **Deployment:** GitHub Pages (automated via GitHub Actions)

**Integrations:**
- **Review Workflow:** Notion API v2 (polling every 5 minutes)
- **Source Control:** GitHub API v3 (bot account with PAT)
- **Monitoring:** AWS CloudWatch + Airflow UI
- **Alerting:** Email + Slack webhooks

### Integration Points

**1. Airflow ↔ PostgreSQL**
- DAGs read/write to Postgres tables (content, embeddings, review_status)
- Connection pooling via Airflow connections
- Idempotent inserts with UPSERT patterns

**2. Python Pipeline ↔ pgvector**
- Embeddings stored as `vector(1536)` type in Postgres
- Similarity queries: `SELECT * FROM embeddings ORDER BY embedding <-> $1 LIMIT 10`
- Batch insertion with `COPY` for performance

**3. Pipeline ↔ OpenAI/Anthropic/Gemini**
- Sequential fallback: Try primary → secondary → fallback
- Exponential backoff: 1min, 2min, 4min delays
- Dead-letter queue in Postgres for failed items
- Cost tracking per provider in CloudWatch metrics

**4. Airflow ↔ Notion**
- Poll Notion database every 5 minutes via DAG
- Query for `review_status` changes since last sync
- Bidirectional: Notion status updates → Postgres, Postgres approvals → Notion
- Rate limit respect: max 3 requests/second

**5. Pipeline ↔ GitHub**
- Bot account (`handbook-bot`) with repo write PAT
- Weekly batch: Query approved items → Generate markdown → Commit to main
- Commit format: "Weekly publish: {count} items ({date})"
- GitHub Actions webhook triggers on main branch push

**6. GitHub Actions ↔ Jupyter Book**
- On push to main: Install dependencies → Build book → Deploy to gh-pages
- Build timeout: 10 minutes max
- Cache dependencies for faster builds
- Deployment status → Slack notification

## Novel Pattern Designs

Your project includes **3 novel architectural patterns** that don't have standard off-the-shelf solutions:

### Pattern 1: Multi-Stage Human-in-the-Loop AI Pipeline

**Purpose:** Combine automated AI quality assessment with human peer review to achieve 90%+ content quality approval while processing 500+ items/week.

**Problem it solves:** Pure AI scoring lacks nuance and context; pure human review doesn't scale. This pattern balances automation with human wisdom.

**Components:**
1. **AI Scoring Agent** (`handbook/pipeline/scoring/ai_scorer.py`)
   - Responsibility: Score 1-5 based on relevance, depth, novelty, practicality
   - Technology: GPT-4o-mini with structured JSON output
   - Output: Score + reasoning (stored for auditability)

2. **Score Filter** (Airflow DAG logic)
   - Responsibility: Only pass score-5 items to human review
   - Filters 80% of noise automatically

3. **Notion Review Queue** (`handbook/integrations/notion_client.py`)
   - Responsibility: Present score-5 items to human reviewers
   - Technology: Notion database with review status fields
   - Polling: Every 5 minutes via Airflow DAG

4. **Bidirectional Sync** (`handbook/dags/notion_sync_dag.py`)
   - Responsibility: Keep Postgres and Notion in sync
   - Pattern: Postgres is source of truth, Notion is review interface
   - Status flow: AI scored → Notion queue → Human approved → Postgres approved

**Data Flow:**
```
Raw Content → Deduplication → AI Scoring (1-5) → [Filter: score==5] →
Notion Queue → Human Review → [Approved] → Postgres → Publication
```

**Implementation Guide for AI Agents:**
- AI Scoring: Use GPT-4o-mini with temperature=0.3 for consistency
- Store scoring reasoning for pattern learning (future enhancement)
- Human review status tracked in `review_status` table (pending/approved/rejected)
- Notion polling respects 3 req/sec rate limit with exponential backoff
- Weekly batch publication triggered by approved status count threshold

**Affects Epics:** Epic 2 (Stories 2.3, 2.4, 2.5)

---

### Pattern 2: Chunk-Level Vector Deduplication with Cost Optimization

**Purpose:** Achieve 95%+ duplicate detection accuracy at paragraph level while minimizing embedding API costs through intelligent pre-filtering.

**Problem it solves:** Content-level deduplication misses near-duplicates; per-token embedding costs add up fast. This pattern optimizes for both quality and cost.

**Components:**
1. **Pre-Filter** (`handbook/pipeline/deduplication/similarity.py`)
   - Responsibility: Quick exact-match check before embedding
   - Technology: PostgreSQL full-text search (tsvector)
   - Filters: 60-70% exact duplicates before embedding API call

2. **Semantic Chunker** (`handbook/pipeline/deduplication/chunker.py`)
   - Responsibility: Split content into semantic paragraphs
   - Technology: LangChain RecursiveCharacterTextSplitter (respects sentence boundaries)
   - Chunk size: 500-1000 tokens (tuned for embedding quality vs cost)

3. **Embedding Generator** (`handbook/pipeline/deduplication/embedder.py`)
   - Responsibility: Generate embeddings only for unique chunks
   - Technology: OpenAI text-embedding-3-small (batch API for 50% discount)
   - Caching: Store embeddings in pgvector with chunk hash

4. **Similarity Search** (`handbook/pipeline/deduplication/similarity.py`)
   - Responsibility: Find similar chunks using cosine similarity
   - Technology: pgvector ivfflat index
   - Threshold: 0.85 for content-level, 0.90 for chunk-level
   - Query performance: <100ms for 100K vectors

**Data Flow:**
```
Raw Content → Pre-Filter (exact match) → [New?] → Semantic Chunking →
Embedding API (batch) → pgvector Insert → Similarity Query →
[Duplicate?] → Mark for skipping / [Unique?] → Pass to Scoring
```

**Implementation Guide for AI Agents:**
- Always run pre-filter before embedding to save API costs
- Use batch embedding API (up to 2048 chunks per request) for 50% discount
- Store chunk hash (SHA256) alongside embedding for quick lookup
- Idempotent: Re-running deduplication on same content doesn't duplicate vectors
- Similarity threshold tunable via environment variable (default: 0.85)

**Affects Epics:** Epic 2 (Story 2.2), Epic 3 (Story 3.2)

---

### Pattern 3: Multi-LLM Fallback with Provider-Agnostic Interface

**Purpose:** Ensure 99%+ pipeline success rate despite individual LLM provider rate limits, outages, or degraded performance.

**Problem it solves:** Relying on a single LLM provider creates single point of failure. This pattern provides graceful degradation across providers.

**Components:**
1. **LLM Config** (`handbook/config/llm_config.py`)
   - Responsibility: Define provider priority and credentials
   - Configuration:
     ```python
     PROVIDERS = [
       ("openai", "gpt-4o-mini", {"temperature": 0.3}),
       ("gemini", "gemini-1.5-flash", {"temperature": 0.3}),
     ]
     ```

2. **Fallback Handler** (`handbook/pipeline/scoring/fallback_handler.py`)
   - Responsibility: Try providers sequentially with exponential backoff
   - Algorithm:
     ```
     for provider in PROVIDERS:
       try:
         result = provider.call(prompt)
         return result
       except RateLimitError:
         continue to next provider
       except Exception as e:
         log error, try next provider
     # All failed
     add_to_dead_letter_queue()
     ```

3. **Provider Adapters** (`handbook/pipeline/scoring/providers/`)
   - Responsibility: Normalize API interfaces across OpenAI, Anthropic, Gemini
   - Pattern: Adapter pattern with common interface
   - Methods: `score(content)`, `synthesize(chunks)`, `embed(text)`

4. **Dead-Letter Queue** (Postgres table: `failed_items`)
   - Responsibility: Store items that failed all providers
   - Fields: content_id, failure_reason, attempt_count, last_attempted
   - Manual review workflow: Weekly check of DLQ by maintainers

**Data Flow:**
```
Content → Try GPT-4o-mini → [Success] → Return result
                         → [Rate Limit] → Try Gemini Flash → [Success] → Return
                                                           → [Fail] → Dead-Letter Queue
```

**Implementation Guide for AI Agents:**
- Each provider has 3 retry attempts with exponential backoff (1min, 2min, 4min)
- Cost tracking: Log provider used and token count to CloudWatch
- Provider health: Track success rate per provider for monitoring
- Fallback decision: If primary fails 3 times, skip directly to secondary for next 10 minutes
- DLQ: Manual review workflow documented in operations runbook

**Affects Epics:** Epic 2 (Stories 2.3, 2.6), Epic 3 (Stories 3.3, 3.4)

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

### NAMING PATTERNS

**Database Tables & Columns:**
- Tables: Plural, lowercase, snake_case → `content_items`, `embeddings`, `review_status`
- Columns: Lowercase, snake_case → `content_id`, `created_at`, `source_url`
- Foreign keys: `{table}_id` → `content_id` (references content table)
- Timestamps: Always include `created_at`, `updated_at` (timestamptz with timezone)

**Python Modules & Classes:**
- Files: Lowercase, snake_case → `ai_scorer.py`, `notion_client.py`
- Classes: PascalCase → `AIScorer`, `NotionClient`, `ContentModel`
- Functions/Methods: Lowercase, snake_case → `score_content()`, `get_embeddings()`
- Constants: UPPERCASE, snake_case → `MAX_RETRIES`, `SIMILARITY_THRESHOLD`

**Airflow DAGs & Tasks:**
- DAG names: Lowercase, hyphen-separated → `ingestion-daily`, `publication-weekly`
- Task IDs: Lowercase, snake_case → `fetch_content`, `deduplicate_chunks`
- DAG file names: Match DAG name → `ingestion_dag.py` contains `ingestion-daily`

**Jupyter Book Content:**
- Folders: Lowercase, hyphen-separated → `newly-discovered`, `model-updates`
- Files: Lowercase, hyphen-separated → `naive-rag.md`, `chain-of-thought.md`
- Anchors/IDs: Lowercase, hyphen-separated → `#advanced-prompting`

### STRUCTURE PATTERNS

**Test Organization:**
- Tests co-located by type: `tests/unit/`, `tests/integration/`, `tests/fixtures/`
- Test files mirror source: `handbook/pipeline/scoring/ai_scorer.py` → `tests/unit/test_ai_scorer.py`
- Fixture files: `tests/fixtures/sample_content.json` (shared test data)

**Component Organization:**
- By pipeline stage: `pipeline/ingestion/`, `pipeline/deduplication/`, etc.
- Not by technology: NO `pipeline/airflow/`, `pipeline/postgres/`
- Reason: Agents work on functional areas, not tech stacks

**Configuration:**
- Environment variables: `.env` file (never commit), `.env.example` (template)
- App config: `handbook/config/settings.py` (loads from env)
- Secrets: AWS Systems Manager Parameter Store or environment variables
- Feature flags: Config file, not hardcoded

### FORMAT PATTERNS

**API Response Wrapper (Internal):**
```python
{
  "success": true,
  "data": {...},
  "error": null,
  "metadata": {
    "provider": "openai",
    "cost_cents": 0.015,
    "timestamp": "2025-11-08T12:00:00Z"
  }
}
```
**Error responses:** `success=false`, `error` contains `{"type": "RateLimitError", "message": "..."}`

**Date/Time Formats:**
- Storage: UTC timestamps in PostgreSQL (`timestamptz`)
- API/Logs: ISO 8601 with timezone → `2025-11-08T12:00:00Z`
- Display (Jupyter Book): Human-readable → `November 8, 2025`
- NO epoch timestamps, NO timezone-naive datetimes

**Logging Format (Loguru):**
```python
logger.info("Processing content", extra={
  "content_id": 123,
  "source": "twitter",
  "stage": "deduplication",
  "duration_ms": 450
})
```
- Always structured (JSON-serializable)
- Include context: content_id, stage, relevant IDs
- Use appropriate levels: DEBUG, INFO, WARNING, ERROR, CRITICAL

**Markdown Frontmatter (Jupyter Book):**
```yaml
---
title: "Naive RAG: Getting Started"
date: 2025-11-08
last_updated: 2025-11-08
category: basics
tags: [rag, retrieval, embeddings]
source_url: https://example.com/original-article
---
```

### COMMUNICATION PATTERNS

**Airflow Task Communication:**
- Use XCom for small data (<1MB): `task_instance.xcom_push(key="content_ids", value=[1,2,3])`
- Use Postgres for large data: Write to table, pass ID via XCom
- NO file-based communication between tasks

**LLM Provider Communication:**
- Always use provider adapters (`handbook/pipeline/scoring/providers/`)
- Never call OpenAI/Anthropic/Gemini APIs directly in business logic
- Adapter interface: `score(content: str) -> ScoreResult`
- Enables testing with mock providers

**Database Transactions:**
- Use context managers: `with db.transaction():`
- Commit per logical unit (one content item, one batch)
- Rollback on any exception
- Idempotent operations: UPSERT, not INSERT

### LIFECYCLE PATTERNS

**Loading States:**
- DAG tasks: Use Airflow task states (running, success, failed)
- Long operations: Log progress every 10% → `logger.info("Progress: 50/100 items processed")`
- User-facing: "Last updated" timestamps in Jupyter Book

**Error Recovery:**
- Transient errors: Retry 3 times with exponential backoff (1min, 2min, 4min)
- Rate limits: Switch to fallback provider immediately
- Permanent errors: Log to dead-letter queue, alert maintainers
- Partial failures: Process remaining items, report failures at end

**Retry Logic (Standard Pattern):**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=60, max=240))
def call_llm_api(prompt: str) -> str:
    # May raise exceptions, tenacity will retry
    return provider.call(prompt)
```

### LOCATION PATTERNS

**Static Assets:**
- Jupyter Book: `handbook-content/_static/` (custom.css, logo.svg)
- Images: `handbook-content/_static/images/` (diagrams, screenshots)
- Downloads: `handbook-content/_static/downloads/` (PDFs, data files)

**Database Migrations:**
- Location: `handbook/db_connection/migrations/`
- Naming: `001_initial_schema.sql`, `002_add_embeddings_table.sql`
- Apply: Manual via script (no ORM migrations for simplicity)

**Logs:**
- Application logs: CloudWatch Logs (streamed from Airflow)
- Airflow logs: Airflow UI + CloudWatch
- Local dev logs: `logs/` directory (git-ignored)

## Consistency Rules

### Cross-Cutting Enforcement

**All agents MUST:**
1. Use naming patterns exactly as specified (no exceptions)
2. Log structured JSON with context (content_id, stage, duration)
3. Handle errors with retry logic (3 attempts, exponential backoff)
4. Write tests for all new code (70% coverage minimum)
5. Use type hints for all function signatures
6. Document complex logic with inline comments
7. Never commit secrets or API keys

**Code Review Checklist (Automated):**
- Ruff linting passes (no warnings)
- Type checking passes (mypy)
- All tests pass (pytest)
- Coverage >= 70% for new code
- No hardcoded credentials
- Markdown files have valid frontmatter

## Data Architecture

### Database Schema (PostgreSQL + pgvector)

**Core Tables:**

```sql
-- Content ingestion
CREATE TABLE content_items (
  id BIGSERIAL PRIMARY KEY,
  source TEXT NOT NULL,  -- 'twitter', 'discord', 'github', 'rss'
  source_url TEXT NOT NULL,
  title TEXT,
  raw_text TEXT NOT NULL,
  publication_date TIMESTAMPTZ,
  category TEXT,  -- 'model-updates', 'framework-updates', etc.
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Embeddings for deduplication
CREATE TABLE embeddings (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  chunk_hash TEXT NOT NULL,  -- SHA256 of chunk text
  embedding vector(1536),  -- pgvector type
  chunk_text TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
CREATE UNIQUE INDEX ON embeddings (chunk_hash);

-- AI scoring results
CREATE TABLE content_scores (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  score INTEGER CHECK (score BETWEEN 1 AND 5),
  reasoning TEXT,
  provider TEXT,  -- 'openai', 'gemini'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Human review status
CREATE TABLE review_status (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  status TEXT CHECK (status IN ('pending', 'approved', 'rejected')),
  reviewer TEXT,
  notion_page_id TEXT,
  reviewed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Approved content ready for publication
CREATE TABLE approved_content (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  processed_markdown TEXT NOT NULL,
  frontmatter JSONB,  -- title, date, category, tags, source_url
  target_path TEXT,  -- 'newly-discovered/model-updates/2025-11-08-gpt45.md'
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dead-letter queue for failed items
CREATE TABLE failed_items (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE SET NULL,
  stage TEXT,  -- 'deduplication', 'scoring', 'synthesis'
  failure_reason TEXT,
  attempt_count INTEGER DEFAULT 1,
  last_attempted TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Data Relationships

```
content_items (1) → (many) embeddings
content_items (1) → (1) content_scores
content_items (1) → (1) review_status
content_items (1) → (0..1) approved_content
```

### Data Flow

**Ingestion → Publication:**
1. Raw content → `content_items` table
2. Chunks + embeddings → `embeddings` table
3. AI score → `content_scores` table (score=5 proceeds)
4. Notion sync → `review_status` table (status='pending')
5. Human approval → `review_status.status='approved'`
6. Markdown generation → `approved_content` table
7. Weekly batch → GitHub commit → Jupyter Book → Live site

## API Contracts

### Internal Python APIs

**LLM Provider Adapter Interface:**
```python
from dataclasses import dataclass
from typing import Protocol

@dataclass
class ScoreResult:
    score: int  # 1-5
    reasoning: str
    provider: str
    cost_cents: float

class LLMProvider(Protocol):
    def score(self, content: str) -> ScoreResult:
        """Score content quality on 1-5 scale."""
        ...

    def synthesize(self, chunks: list[str]) -> str:
        """Synthesize chunks into cohesive content."""
        ...
```

**Embedding Interface:**
```python
from typing import Protocol

class EmbeddingProvider(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for list of texts."""
        ...

    def embed_batch(self, texts: list[str], batch_size: int = 2048) -> list[list[float]]:
        """Batch embedding for cost optimization."""
        ...
```

### External APIs

**Notion API (Polling):**
- Endpoint: `https://api.notion.com/v1/databases/{database_id}/query`
- Method: POST
- Rate limit: 3 requests/second
- Polling frequency: Every 5 minutes via Airflow DAG

**GitHub API (Commit):**
- Endpoint: `https://api.github.com/repos/{owner}/{repo}/contents/{path}`
- Method: PUT (create/update file)
- Authentication: Bot account PAT (Bearer token)
- Commit message format: "Weekly publish: {count} items ({date})"

## Security Architecture

### Credential Management
- **API Keys:** Stored in environment variables (never in code)
- **AWS:** Use IAM roles for RDS access (no passwords in connection strings)
- **GitHub PAT:** Stored in GitHub Secrets for Actions, env var for local Airflow
- **Notion API Token:** Environment variable with quarterly rotation

### Data Protection
- **In Transit:** HTTPS for all external API calls (OpenAI, Anthropic, Gemini, Notion, GitHub)
- **At Rest:** RDS encryption enabled (AWS KMS), backup encryption enabled
- **Secrets:** Never log API keys, mask in error messages

### Access Control
- **RDS:** IAM database authentication, limited security group (Airflow only)
- **GitHub:** Bot account with repo write permission only (no admin)
- **Notion:** Read/write access to review database only

### Vulnerability Management
- **Dependencies:** Dependabot automated PRs for security updates
- **Scanning:** Weekly Ruff + safety checks in CI/CD
- **Critical updates:** Apply within 48 hours of disclosure

## Performance Considerations

### Database Performance
- **pgvector Index:** ivfflat with lists=100 for 100K vectors (sub-100ms queries)
- **Connection Pooling:** Max 20 connections, min 5 idle
- **Query Optimization:** EXPLAIN ANALYZE for slow queries, add indexes as needed
- **Batch Operations:** Use `COPY` for bulk inserts (10x faster than individual INSERTs)

### LLM API Optimization
- **Batch Embeddings:** OpenAI batch API (2048 texts/request, 50% discount)
- **Prompt Caching:** Claude prompt caching for repeated synthesis prompts (90% savings)
- **Rate Limit Handling:** Exponential backoff + fallback provider
- **Cost Monitoring:** Track spend per provider, alert if >$50/month

### Jupyter Book Build
- **Incremental Builds:** Not supported in 1.0.4, full rebuild required (~5 min for 1000 pages)
- **Dependency Caching:** GitHub Actions caches pip dependencies (30s install vs 2min)
- **Asset Optimization:** Compress images (WebP format), minify CSS
- **CDN:** GitHub Pages CDN for fast global delivery

### Pipeline Performance
- **Parallel Processing:** Airflow parallelism=4 (process 4 content items simultaneously)
- **Async I/O:** Use httpx for async HTTP requests (3x faster than requests library)
- **Deduplication:** Pre-filter with exact match before embedding (saves 60% API costs)

## Deployment Architecture

### Production Environment (AWS)

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                               │
│                                                                 │
│  ┌────────────────┐         ┌──────────────────┐              │
│  │  Apache Airflow │────────▶│  RDS PostgreSQL  │              │
│  │  (Existing)     │         │  + pgvector      │              │
│  │                 │         │  (db.t3.small)   │              │
│  └────────────────┘         └──────────────────┘              │
│          │                                                      │
│          │ (Polls every 5min)                                  │
│          ▼                                                      │
│  ┌────────────────┐         ┌──────────────────┐              │
│  │  Notion API    │         │  OpenAI API      │              │
│  │  (Review)      │         │  Anthropic API   │              │
│  │                │         │  Gemini API      │              │
│  └────────────────┘         └──────────────────┘              │
│                                                                 │
│  ┌────────────────┐         ┌──────────────────┐              │
│  │  CloudWatch    │         │  GitHub API      │              │
│  │  (Monitoring)  │         │  (Commits)       │              │
│  └────────────────┘         └──────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
                                      │
                                      │ (Weekly commit triggers build)
                                      ▼
                            ┌──────────────────┐
                            │  GitHub Actions  │
                            │  (Jupyter Book)  │
                            └──────────────────┘
                                      │
                                      │ (Deploy)
                                      ▼
                            ┌──────────────────┐
                            │  GitHub Pages    │
                            │  (Public Site)   │
                            └──────────────────┘
```

### Deployment Process

**Weekly Publication Cycle:**
1. **Sunday 00:00 UTC:** Airflow DAG queries approved content from Postgres
2. **Sunday 00:05 UTC:** Generate markdown files with frontmatter
3. **Sunday 00:10 UTC:** Bot account commits to main branch (single commit, all files)
4. **Sunday 00:11 UTC:** GitHub Actions workflow triggers automatically
5. **Sunday 00:16 UTC:** Jupyter Book build completes (~5 min)
6. **Sunday 00:17 UTC:** Deploy to gh-pages branch
7. **Sunday 00:18 UTC:** Live on handbook site (zero downtime)
8. **Sunday 00:20 UTC:** Slack notification: "Weekly publish complete: 23 items"

**Rollback Procedure:**
1. Identify issue (broken links, formatting errors)
2. `git revert <commit_hash>` on main branch
3. Push triggers automatic rebuild and redeployment
4. Previous version live within 10 minutes

## Development Environment

### Prerequisites

- **Python:** 3.10 or higher (for match statements, type hints)
- **Poetry:** 1.8+ (`curl -sSL https://install.python-poetry.org | python3 -`)
- **Docker:** For local Postgres + pgvector
- **Node.js:** 18+ (for any Jupyter Book custom extensions)
- **Git:** 2.30+ (for CLI workflows)

### Setup Commands

```bash
# Clone repository
git clone https://github.com/your-org/cherry-in-the-haystack.git
cd cherry-in-the-haystack

# Install Python dependencies
poetry install

# Start local database
docker-compose up -d postgres

# Initialize database schema
psql -h localhost -U postgres -f scripts/setup_pgvector.sql

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys (OpenAI, Anthropic, Gemini, Notion, GitHub)

# Run tests
poetry run pytest tests/ --cov=handbook --cov-report=term-missing

# Build Jupyter Book locally
cd handbook-content
poetry run jupyter-book build .
# Open _build/html/index.html in browser

# Run Airflow locally (optional, complex setup)
# See docs/local-airflow-setup.md for detailed instructions
```

### Local Development Workflow

1. Create feature branch: `git checkout -b feature/add-xyz`
2. Make changes, write tests
3. Run linting: `poetry run ruff check handbook/`
4. Run tests: `poetry run pytest tests/`
5. Build Jupyter Book locally to preview
6. Commit and push
7. Open PR (automated CI checks run)
8. Maintainer reviews and merges

## Architecture Decision Records (ADRs)

### ADR-001: Use RDS PostgreSQL instead of Aurora Serverless

**Context:** Need managed PostgreSQL for content storage and pgvector for embeddings.

**Decision:** Amazon RDS PostgreSQL (db.t3.small) instead of Aurora Serverless v2.

**Rationale:**
- Cost: RDS ~$25/month vs Aurora ~$43/month minimum
- Workload: Batch-based (weekly), not bursty real-time traffic
- Aurora doesn't scale to zero (0.5 ACU minimum always running)
- RDS sufficient for 100K vectors with pgvector

**Status:** Accepted

---

### ADR-002: Use pgvector instead of dedicated vector database

**Context:** Need vector storage for 100K+ embeddings for deduplication.

**Decision:** pgvector (PostgreSQL extension) instead of Pinecone, Chroma Cloud, or Weaviate.

**Rationale:**
- Cost: $0 (included in RDS) vs $70+/month for managed vector DBs
- Simplicity: Single database for relational + vector data
- Performance: <100ms queries for 100K vectors meets NFR-P3
- Scale: Sufficient for MVP and growth phase (up to 1M vectors)

**Status:** Accepted

**When to revisit:** If vector count exceeds 1M or query latency >100ms

---

### ADR-003: Multi-LLM Provider Strategy

**Context:** Need reliable LLM access despite rate limits and outages.

**Decision:** Multi-provider with sequential fallback (GPT-4o-mini → Gemini Flash).

**Rationale:**
- Reliability: 99%+ pipeline success rate (NFR requirement)
- Cost optimization: Right model for right task (scoring vs synthesis)
- Provider diversity: Avoid single vendor lock-in
- Graceful degradation: Continue operations if one provider fails

**Status:** Accepted

**Providers:** OpenAI (primary scoring), Claude (synthesis), Gemini (fallback)

---

### ADR-004: Jupyter Book over custom web app

**Context:** Need public-facing handbook site with good UX.

**Decision:** Jupyter Book (static site generator) instead of Next.js/React custom app.

**Rationale:**
- Time to market: Professional docs site out-of-the-box
- Zero infrastructure: GitHub Pages hosting (free, reliable)
- Focus on content: Avoid building custom CMS/web app
- Performance: Static HTML = fast, SEO-friendly
- Cost: $0 hosting vs $50+/month for Next.js on Vercel/AWS

**Status:** Accepted

**When to revisit:** If we need user accounts, real-time features, or interactive tools

---

_Generated by BMAD Decision Architecture Workflow v1.3.2_
_Date: 2025-11-08_
_For: HK_
