# Architecture

## Executive Summary

cherry-in-the-haystack transforms an existing Auto-News infrastructure into The 'Cherry for LLM Engineers' through a two-layer knowledge architecture: Evidence Layer (Postgres for source paragraphs), Concept Layer (Graph DB for normalized concepts). The system operates three distinct pipelines: (1) Newly Discovered content flows through Auto-News → Notion (primary) → Postgres backup → GitHub, (2) Basics/Advanced content ingestion extracts concepts from documents into the two-layer knowledge graph, and (3) Writer Agent synthesizes handbook-style, wiki-like pages from the knowledge graph. The architecture prioritizes automation, human-in-the-loop quality control, and weekly update velocity while maintaining 99.5% uptime and sub-2-second page loads.

## Project Initialization

**First Implementation Story: Handbook Foundation Setup**

The project builds on existing Auto-News infrastructure while establishing new handbook-specific components:

### Jupyter Book Initialization (ADAPT EXISITING)
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

**Project:** cherry-in-the-haystack (Cherry for AI Engineers)

**Scale & Complexity:**
- 5 epics with 33 total stories
- Medium complexity web application + API backend (hybrid)
- Target: 50,000 monthly users within 6 months
- 20+ active contributors expanding to 50+

**Core Functionality:**
The product transforms the existing Auto-News personal content curation tool into 'Cherry for AI Engineers' - a living, community-driven knowledge base serving as the default reference for AI product builders. The system provides:
- **Two-Layer Knowledge Architecture:** Evidence Layer (Postgres) → Concept Layer (Graph DB)
- **Three Distinct Pipelines:**
  - **Newly Discovered:** Auto-News → Notion (primary workspace) → Postgres (daily backup) → GitHub
  - **Basics/Advanced Ingestion:** Documents → Evidence extraction → Concept normalization → Graph DB
  - **Basics/Advanced Publication:** Knowledge graph → Writer Agent synthesis → Markdown → GitHub → Jupyter Book
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
- Existing Jupyter book
- Proven event-driven data pipeline for content aggregation
- LLM-powered categorization, ranking, and summarization capabilities
- Current output to Notion workspaces (to be transformed to handbook pipeline)

**Unique Challenges:**
- **Two-layer knowledge graph architecture:** Evidence (Postgres) ↔ Concepts (Graph DB)
- **Concept normalization:** Extract main ideas from paragraphs, match/merge with existing concepts in Graph DB
- **Notion as primary workspace:** Daily backup to Postgres, not reverse sync
- **Multiple publication formats:** Category-specific and source-specific markdown output formats
- **Writer Agent synthesis:** Generate handbook pages from graph queries (concept + relations + evidence)
- **Image generation workflow:** Custom MCP server for automated diagram/graph creation
- **Patch note aggregation:** Track Basics/Advanced changes in centralized patchnote.md

## Decision Summary

| Category                         | Decision                            | Version         | Affects Epics                   | Rationale                                                                                    |
| -------------------------------- | ----------------------------------- | --------------- | ------------------------------- | -------------------------------------------------------------------------------------------- |
| **CRITICAL DECISIONS**           |                                     |                 |                                 |                                                                                              |
| Static Site Generator            | Jupyter Book                        | 1.0.4           | Epic 4 (Publication)            | PROVIDED BY STARTER - Professional docs site, GitHub Pages compatible, built-in search       |
| Python Tooling                   | Poetry + Ruff + Loguru              | Latest          | All Epics                       | PROVIDED BY STARTER - Modern 2024 best practices, Ruff replaces 3 tools                      |
| Orchestration                    | Apache Airflow                      | Existing        | Epic 2 (Ingestion)              | BROWNFIELD - Keep existing Auto-News orchestration                                           |
| Evidence Layer DB                | Amazon RDS PostgreSQL               | PostgreSQL 16   | Epic 3 (Basics/Advanced)        | Stores document paragraphs with extracted concepts + metadata, ~$25/month                    |
| Concept Layer DB                 | GraphDB                             | Latest (Free)   | Epic 3 (Knowledge Graph)        | Open-source RDF graph database - stores normalized concepts + relations                      |
| Vector Database                  | pgvector                            | Latest          | Epic 3 (Document Search)        | PostgreSQL extension - vectorizes Basics/Advanced documents only                             |
| Primary LLM (Concept Extraction) | Anthropic Claude 3.5 Sonnet         | Latest          | Epic 3 (Evidence Ingestion)     | $3-15/1M tokens, superior concept extraction, 200K context for documents                     |
| Secondary LLM (Writer Agent)     | Anthropic Claude 3.5 Sonnet         | Latest          | Epic 3 (Page Generation)        | $3-15/1M tokens, superior prose quality, 200K context for graph synthesis                    |
| Fallback LLM                     | Google Gemini 1.5 Flash             | Latest          | All LLM tasks                   | $0.075-0.30/1M tokens, 80% cheaper fallback, 1M token context                                |
| Embedding Model                  | OpenAI text-embedding-3-small       | Latest          | Epic 3 (Document Vectorization) | $0.02/1M tokens, 1536 dims, for Basics/Advanced document search only                         |
| **IMPORTANT DECISIONS**          |                                     |                 |                                 |                                                                                              |
| Airflow Hosting                  | Existing Setup                      | Current Version | Epic 2 (Ingestion)              | BROWNFIELD - Keep existing Auto-News Airflow deployment, migrate to MAWA later if needed     |
| Notion Integration               | Primary Workspace + Daily Backup    | Notion API v2   | Epic 2 (Newly Discovered)       | Notion is primary data source, daily backup to Postgres, Auto-News writes directly to Notion |
| GitHub Automation                | Bot Account with PAT                | GitHub API v3   | Epic 4 (Publication)            | Dedicated bot account (handbook-bot), PAT with repo write, clear attribution                 |
| Image Generation                 | Custom Agent + MCP Server           | Latest MCP SDK  | Epic 4, 6                       | Custom agent calls MCP server for diagram/graph generation, added to markdown files          |
| LLM Fallback Strategy            | Sequential with Exponential Backoff | N/A             | All LLM tasks                   | Claude Sonnet → Gemini Flash → Dead-letter queue, 1/2/4 min backoff                          |
| **NICE-TO-HAVE DECISIONS**       |                                     |                 |                                 |                                                                                              |
| Monitoring Solution              | AWS CloudWatch + Airflow UI         | Built-in        | All Epics                       | Start with CloudWatch for RDS/infrastructure, Airflow UI for DAGs, upgrade to Grafana later  |
| Alerting Channels                | Email + Slack webhook               | N/A             | Operations                      | Email for non-urgent, Slack for moderate/critical, PagerDuty later if needed                 |
| Local Development                | Docker Compose                      | Latest          | Development                     | Postgres + pgvector + ChromaDB in Docker, matches CI environment                             |
| Testing Framework                | pytest + pytest-cov                 | Latest          | All Epics                       | 70% coverage target, unit + integration tests, pytest fixtures for test data                 |
| Error Handling                   | Retry with Dead-Letter Queue        | N/A             | All Pipelines                   | 3 retries with exponential backoff, DLQ for permanent failures, manual review workflow       |

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
│   │   ├── postgres.py                     # Evidence Layer (Postgres)
│   │   ├── graph_db.py                     # Concept Layer (Graph DB - TBD)
│   │   └── vector_db.py                    # Vector DB for document embeddings
│   │
│   ├── pipeline/
│   │   ├── __init__.py
│   │   ├── newly_discovered/               # Pipeline for Newly Discovered content
│   │   │   ├── __init__.py
│   │   │   ├── notion_backup.py            # Daily Notion → Postgres backup
│   │   │   ├── category_matcher.py         # Match news to handbook topics
│   │   │   ├── format_dispatcher.py        # Category/source-specific formatting
│   │   │   └── weekly_update.py            # EXISTING - Weekly news publishing script
│   │   │
│   │   ├── evidence_ingestion/             # Pipeline for Basics/Advanced documents
│   │   │   ├── __init__.py
│   │   │   ├── document_chunker.py         # Chunk documents to paragraph level
│   │   │   ├── concept_extractor.py        # Extract & normalize main ideas (Claude)
│   │   │   ├── concept_matcher.py          # Match concepts with Graph DB
│   │   │   ├── evidence_storage.py         # Store paragraphs in Evidence Layer
│   │   │   └── graph_updater.py            # Add/merge concepts in Graph DB
│   │   │
│   │   ├── writer_agent/                   # Writer Agent for page generation
│   │   │   ├── __init__.py
│   │   │   ├── graph_query.py              # Query concept + relations + evidence
│   │   │   ├── page_synthesizer.py         # Generate handbook pages (Claude)
│   │   │   ├── synthesis_prompts.py        # Writer Agent prompts
│   │   │   └── patchnote_aggregator.py     # Aggregate changes to patchnote.md
│   │   │
│   │   ├── image_generation/               # Image/diagram generation
│   │   │   ├── __init__.py
│   │   │   ├── image_agent.py              # Custom agent for image generation
│   │   │   ├── mcp_client.py               # MCP server client
│   │   │   └── markdown_inserter.py        # Insert images into markdown files
│   │   │
│   │   └── publication/
│   │       ├── __init__.py
│   │       ├── notion_to_github.py         # Notion → GitHub for Newly Discovered
│   │       ├── markdown_formatter.py       # Category/source-specific formatting
│   │       └── github_committer.py         # Bot account commit logic
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── notion_client.py                # Notion API polling
│   │   └── github_client.py                # GitHub API wrapper
│   │
│   ├── dags/
│   │   ├── __init__.py
│   │   ├── notion_backup_dag.py            # Daily Notion → Postgres backup
│   │   ├── evidence_ingestion_dag.py       # Document → Evidence → Concept → Graph
│   │   ├── writer_agent_dag.py             # Generate pages from knowledge graph
│   │   ├── weekly_publish_dag.py           # Weekly Newly Discovered publication
│   │   └── image_generation_dag.py         # Time-to-time image generation
│   │
│   └── models/
│       ├── __init__.py
│       ├── evidence.py                     # Evidence Layer dataclasses (paragraphs)
│       ├── concept.py                      # Concept dataclasses (for Graph DB)
│       └── news.py                         # Newly Discovered news dataclasses
│
├── handbook-content/                        # Jupyter Book content (public handbook)
│   ├── _config.yml                         # Jupyter Book configuration
│   ├── _toc.yml                            # Table of contents (3 sections)
│   ├── patchnote.md                        # Aggregated changes to Basics/Advanced
│   ├── _static/
│   │   ├── custom.css                      # Custom branding styles
│   │   ├── logo.svg                        # Project logo
│   │   └── images/                         # Generated diagrams/graphs
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
│   ├── setup_evidence_layer.sql            # Evidence Layer (Postgres) schema
│   ├── setup_graph_db.py                   # Concept Layer (Graph DB) initialization
│   ├── setup_vector_db.py                  # Vector DB initialization
│   ├── seed_basics.py                      # Initial evidence ingestion
│   ├── backup_databases.py                 # Backup all two layers
│   └── migrate_existing_data.py            # Migration script for brownfield data
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
| **Epic 1: Foundation & Core Infrastructure** | 1.1-1.7 (7 stories) | - `pyproject.toml` (Poetry)<br>- `handbook/config/` (settings, logging)<br>- `handbook/db_connection/` (Postgres, GraphDB, pgvector)<br>- `auto-news-engine/` (adapt existing)<br>- `.github/workflows/` (CI/CD)<br>- `handbook-content/_config.yml` (Jupyter Book)<br>- `scripts/setup_*.sql/py` (two-layer initialization) | - RDS PostgreSQL 16 (Evidence Layer)<br>- GraphDB (Concept Layer)<br>- pgvector (document embeddings)<br>- Poetry + Ruff + Loguru<br>- Jupyter Book 1.0.4<br>- Docker Compose |
| **Epic 2: Newly Discovered Pipeline** | 2.1-2.6 (6 stories) | - `auto-news-engine/` (existing - ingestion, dedup, scoring)<br>- Notion DB (primary workspace)<br>- `handbook/pipeline/newly_discovered/` (backup, matching, formatting)<br>- `handbook/pipeline/newly_discovered/weekly_update.py` (EXISTING)<br>- `handbook/dags/notion_backup_dag.py`<br>- `handbook/dags/weekly_publish_dag.py` | - Auto-News operators<br>- Notion API v2 (primary)<br>- Daily Postgres backup<br>- Category/source-specific formatting<br>- Apache Airflow |
| **Epic 3: Evidence Ingestion & Knowledge Graph** | 3.1-3.7 (7 stories) | - `handbook/pipeline/evidence_ingestion/` (chunker, extractor, matcher, storage)<br>- `handbook/db_connection/postgres.py` (Evidence Layer)<br>- `handbook/db_connection/graph_db.py` (Concept Layer)<br>- `handbook/db_connection/vector_db.py` (document vectorization)<br>- `handbook/models/evidence.py`, `concept.py`<br>- `handbook/dags/evidence_ingestion_dag.py` | - Claude 3.5 Sonnet (concept extraction)<br>- GraphDB (concept normalization + relations)<br>- pgvector (document search)<br>- Paragraph-level chunking|
| **Epic 4: Writer Agent & Publication** | 4.1-4.7 (7 stories) | - `handbook/pipeline/writer_agent/` (graph query, synthesizer, patchnote, chart generation)<br>- `handbook/pipeline/publication/` (Notion→GitHub, formatting, committer)<br>- `handbook/pipeline/image_generation/` (agent, MCP client, inserter)<br>- `handbook-content/_static/` (custom CSS, images)<br>- `handbook-content/patchnote.md` (aggregated changes)<br>- `handbook/dags/writer_agent_dag.py`<br>- `handbook/dags/image_generation_dag.py`<br>- `.github/workflows/deploy.yml` | - Claude 3.5 Sonnet (page synthesis)<br>- GraphDB query (concept + relations + evidence)<br>- Custom Image Agent + MCP Server (chart/diagram generation)<br>- GitHub Bot Account + PAT<br>- Jupyter Book build<br>- Category/source-specific markdown formats |
| **Epic 5: Community Contribution Framework** | 5.1-5.6 (6 stories) | - `.github/ISSUE_TEMPLATE/` (error reports, URL submission)<br>- `.github/pull_request_template.md`<br>- `CONTRIBUTING.md`, `STYLE_GUIDE.md`<br>- `.github/workflows/ci.yml` (PR validation)<br>- `templates/` (content templates)<br>- `.github/workflows/link-check.yml`<br>- `scripts/backup_databases.py` (two-layer backup)<br>- AWS CloudWatch integration | - GitHub PR workflow<br>- markdown-lint<br>- link validation<br>- CODEOWNERS for auto-assignment<br>- CloudWatch + Airflow UI<br>- Email + Slack webhooks<br>- pytest + pytest-cov (70% coverage)<br>- two-layer backup strategy |

### Architecture Boundaries by Epic

**Epic 1 (Foundation Layer):**
- two-layer database setup: Evidence (PostgreSQL 16), Concept (GraphDB), pgvector
- Auto-News engine adaptation for handbook use
- Jupyter Book initialization with custom theme
- Docker Compose for local development

**Epic 2 (Newly Discovered Pipeline):**
- Auto-News → Notion (primary workspace) for scoring and categorization
- Daily backup: Notion → Postgres (backup only, no reverse sync)
- Weekly publication: Notion → GitHub (category/source-specific formatting)
- Existing `weekly_update.py` script integration

**Epic 3 (Evidence Ingestion & Knowledge Graph):**
- Document chunking at paragraph level
- Claude extracts & normalizes main ideas (concepts)
- Concept matching/merging with GraphDB
- Evidence Layer stores paragraphs + metadata
- pgvector stores document embeddings

**Epic 4 (Writer Agent & Publication):**
- Writer Agent queries knowledge graph (concept + relations + evidence)
- Claude synthesizes handbook-style pages from graph
- Chart generation via Custom Image Agent + MCP Server
- Automated diagram/graph creation for handbook pages
- Patchnote aggregation for Basics/Advanced changes
- GitHub deployment with Jupyter Book build

**Epic 5 (Community & Quality):**
- GitHub PR workflow for content contributions
- Link validation + two-layer backup
- CloudWatch monitoring + Slack alerts
- Testing framework with 70% coverage target

## Technology Stack Details

### Core Technologies

**Backend Pipeline:**
- **Language:** Python 3.10+ (for Airflow compatibility and modern type hints)
- **Dependency Management:** Poetry 1.8+ with pyproject.toml
- **Orchestration:** Apache Airflow (existing Auto-News deployment)
- **Linting/Formatting:** Ruff (replaces isort, flake8, pylint)
- **Logging:** Loguru (structured logging with JSON output)
- **Testing:** pytest 8.0+, pytest-cov, pytest-mock

**Databases (two-Layer Architecture):**
- **Evidence Layer:** Amazon RDS PostgreSQL 16 (db.t3.small, 20GB gp3) - stores document paragraphs with extracted concepts + metadata
- **Concept Layer:** GraphDB (open-source RDF graph database) - stores normalized concepts + relations (prerequisite, related, subtopic, extends, contradicts)
- **Vector DB:** pgvector (PostgreSQL extension) - vectorizes Basics/Advanced documents for search
- **Notion DB:** Primary workspace for Newly Discovered content (scored by Auto-News)
- **Connection Pooling:** psycopg3 for Postgres, native pooling for GraphDB

**LLM Providers:**
- **Concept Extraction:** Anthropic Claude 3.5 Sonnet via anthropic==0.x SDK (200K context for documents)
- **Writer Agent:** Anthropic Claude 3.5 Sonnet via anthropic==0.x SDK (synthesizes handbook pages from graph)
- **Fallback:** Google Gemini 1.5 Flash via google-generativeai SDK
- **Embeddings:** OpenAI text-embedding-3-small (1536 dimensions) - for document vectorization only
- **Auto-News Scoring:** Handled by existing Auto-News engine (writes to Notion)

**Publication:**
- **Static Site Generator:** Jupyter Book 1.0.4 (Sphinx-based)
- **Theme:** PyData Sphinx Theme (responsive, accessible)
- **Extensions:** sphinx-design, sphinx-togglebutton, sphinxext-opengraph
- **Deployment:** GitHub Pages (automated via GitHub Actions)

**Integrations:**
- **Notion (Primary Workspace):** Notion API v2 - primary data source for Newly Discovered, daily backup to Postgres
- **Source Control:** GitHub API v3 (bot account with PAT) - automated commits for handbook content
- **Image Generation:** Custom MCP Server - generates diagrams/graphs for handbook pages
- **Monitoring:** AWS CloudWatch + Airflow UI
- **Alerting:** Email + Slack webhooks

### Integration Points

**1. Auto-News Engine → Notion (Newly Discovered Pipeline)**
- Auto-News DAGs run ingestion, deduplication, categorization, scoring
- Write scored content directly to Notion DB (primary workspace)
- Knowledge team reviews/edits columns in Notion
- **NO** reverse sync from Postgres to Notion

**2. Notion → Postgres (Daily Backup)**
- Daily Airflow DAG: `notion_backup_dag.py`
- Read all Newly Discovered content from Notion
- Store in Postgres Evidence Layer for backup and historical tracking
- One-way sync: Notion is source of truth

**3. Document Chunker → Evidence Layer (Basics/Advanced Ingestion)**
- Chunk documents at paragraph level (semantic boundaries)
- Claude extracts main idea (concept noun phrase) from each paragraph
- Store in Postgres Evidence Layer: `paragraph_text`, `extracted_concept`, `metadata` (book, page, paragraph #)

**4. Concept Matcher → Graph DB (Concept Normalization)**
- Query Graph DB for similar concepts (semantic matching)
- If match exists: Use existing concept_id, update evidence paragraph's extracted_concept field
- If no match: Create new concept node in Graph DB with relations, update evidence paragraph's extracted_concept field

**5. Evidence Layer → Vector DB (Document Vectorization)**
- Vectorize paragraph text using OpenAI text-embedding-3-small
- Store in Vector DB for document search (Basics/Advanced only)
- Separate from Graph DB - used for different purposes

**6. Writer Agent → Knowledge Graph (Page Generation)**
- Query sequence:
  1. Load concept from Graph DB (target concept + relations)
  2. Query Evidence Layer for paragraphs where extracted_concept matches the target concept
  3. Fetch evidence paragraphs from Postgres Evidence Layer
  4. Synthesize page with Claude using concept + relations + evidence
- Output: Markdown file with citations

**7. Publication Pipeline → GitHub**
- **Newly Discovered:** Notion → Category/source-specific formatting → GitHub
- **Basics/Advanced:** Writer Agent output → Patchnote aggregation → GitHub
- Bot account (`handbook-bot`) with repo write PAT
- Commit format varies by pipeline

**8. GitHub Actions → Jupyter Book**
- On push to main: Install dependencies → Build book → Deploy to gh-pages
- Build timeout: 10 minutes max
- Cache dependencies for faster builds
- Deployment status → Slack notification

**9. Image Generation Agent → MCP Server**
- Custom Image Agent calls MCP Server for diagram/graph generation
- MCP Server returns image file paths
- Agent inserts images into markdown files in `_static/images/`
- Triggered time-to-time via Airflow DAG or manual workflow

## Novel Pattern Designs

Your project includes **3 novel architectural patterns** that don't have standard off-the-shelf solutions:

### Pattern 1: Two-Layer Knowledge Architecture (Evidence → Concept)

**Purpose:** Separate stable concept ontology from high-volume evidence storage while maintaining dynamic linkage for knowledge synthesis.

**Problem it solves:** Traditional knowledge bases either store everything in one place (cluttered) or separate concerns without proper linkage. This pattern enables clean concept graphs with dynamic evidence accumulation.

**Components:**
1. **Evidence Layer** (`handbook/db_connection/postgres.py` + Evidence tables)
   - Responsibility: Store document paragraphs with extracted concepts and metadata
   - Technology: Amazon RDS PostgreSQL 16
   - Schema: `paragraph_text`, `extracted_concept`, `book_name`, `page_number`, `paragraph_index`, `created_at`
   - High volume: 100K+ paragraphs expected

2. **Concept Layer** (`handbook/db_connection/graph_db.py` + GraphDB)
   - Responsibility: Store normalized concepts as unique nodes with typed relations
   - Technology: GraphDB (open-source RDF graph database)
   - Node properties: `concept_name` (noun phrase), `summary`, `contributors`
   - Edge types: `prerequisite`, `related`, `subtopic`, `extends`, `contradicts`
   - Stable ontology: Concepts reused across all evidence

2. **Concept Matcher** (`handbook/pipeline/evidence_ingestion/concept_matcher.py`)
   - Responsibility: Match extracted concepts with existing concepts in Graph DB
   - Technology: Claude 3.5 Sonnet for semantic matching
   - Logic: If similar concept exists → merge, else → create new concept node

**Data Flow:**
```
Document → Paragraph Chunking → Concept Extraction (Claude) →
Evidence Layer (Postgres) → Concept Matching (Graph DB query) →
[Match found?] → Update extracted_concept field in Evidence Layer / [No match?] → Create new concept node + Update extracted_concept field in Evidence Layer
→ Vectorize paragraph (Vector DB)
```

**Implementation Guide for AI Agents:**
- Evidence Layer uses standard Postgres operations (INSERT, SELECT)
- Graph DB queries for concept similarity: semantic matching via embeddings or LLM
- Writer Agent queries: Load concept → Query Evidence Layer by extracted_concept field → Fetch evidence paragraphs
- No evidence stored IN concept nodes - only referenced via extracted_concept field in Evidence Layer

**Affects Epics:** Epic 3 (Stories 3.1-3.7)

---

### Pattern 2: Notion as Primary Workspace with One-Way Backup

**Purpose:** Use Notion as the active collaboration workspace for knowledge team while maintaining data ownership through automated daily backups.

**Problem it solves:** Traditional architectures treat databases as primary with UI as secondary. This pattern inverts that for human-centric workflows while ensuring data safety.

**Components:**
1. **Auto-News Engine** (existing)
   - Responsibility: Ingest, deduplicate, categorize, score content
   - Output: Write scored content directly to Notion DB
   - Knowledge team works in Notion (primary workspace)

2. **Notion DB** (primary)
   - Responsibility: Active collaboration space for Knowledge Team
   - Columns: title, summary, score, category, source_url, review_status, tags
   - Knowledge team edits directly in Notion interface
   - No application backend - Notion API is the interface

3. **Daily Backup DAG** (`handbook/dags/notion_backup_dag.py`)
   - Responsibility: Read all content from Notion, store in Postgres
   - Schedule: Daily at 00:00 UTC
   - Technology: Notion API v2 with pagination
   - One-way sync: Notion → Postgres (no reverse sync)

4. **Postgres Evidence Layer** (backup)
   - Responsibility: Historical backup and data ownership
   - Schema: Same as Notion structure + `notion_page_id`, `backup_timestamp`
   - Used for: Analytics, rollback, data migration

**Data Flow:**
```
Auto-News Engine → Notion DB (primary) ← Knowledge Team edits
                     ↓
              (Daily 00:00 UTC)
                     ↓
            Postgres Evidence Layer (backup, one-way)
                     ↓
            Weekly Publication → GitHub
```

**Implementation Guide for AI Agents:**
- Auto-News writes to Notion, NOT Postgres
- Postgres is backup only - never update Notion from Postgres
- Backup script is idempotent: `UPSERT` based on `notion_page_id`
- If Notion data lost: Restore from Postgres backup manually
- Weekly publication reads from Notion, not Postgres

**Affects Epics:** Epic 2 (Stories 2.1-2.6)

---

### Pattern 3: Writer Agent Graph Query Synthesis

**Purpose:** Generate handbook pages by querying knowledge graph for concept + relations + evidence, then synthesizing with LLM.

**Problem it solves:** Traditional CMS stores finished pages. This pattern generates pages dynamically from structured knowledge, enabling automatic updates when evidence/concepts change.

**Components:**
1. **Graph Query Module** (`handbook/pipeline/writer_agent/graph_query.py`)
   - Responsibility: Query knowledge graph for target concept
   - Steps:
     1. Load concept node from Graph DB by concept_name
     2. Traverse relations (prerequisite, related, subtopic, extends, contradicts)
     3. Return: concept + related_concepts

2. **Evidence Fetcher** (Postgres queries)
   - Responsibility: Fetch evidence paragraphs from Evidence Layer
   - Input: concept_name from Graph DB
   - Query: SELECT * FROM evidence_paragraphs WHERE extracted_concept = concept_name
   - Output: Full paragraph text + metadata (book, page, paragraph #)
   - Batched queries for performance

3. **Page Synthesizer** (`handbook/pipeline/writer_agent/page_synthesizer.py`)
   - Responsibility: Generate handbook page from graph data
   - Technology: Claude 3.5 Sonnet (200K context)
   - Input: concept + relations + evidence paragraphs
   - Output: Markdown following Concept Page Structure (from PRD)
   - Includes: Title, summary, dynamic relation blocks, evidence previews, sources

4. **Patchnote Aggregator** (`handbook/pipeline/writer_agent/patchnote_aggregator.py`)
   - Responsibility: Track changes to Basics/Advanced pages
   - Output: Prepend summary to `patchnote.md`
   - Format: `- [Date] Updated [Concept]: [summary of changes]`

**Data Flow:**
```
Trigger (concept_name) → Query Graph DB (concept + relations) →
Query Evidence Layer by extracted_concept (paragraphs) →
Claude Synthesis (concept + relations + evidence) → Markdown →
Patchnote Aggregation → GitHub Commit
```

**Implementation Guide for AI Agents:**
- Writer Agent follows PRD specification for Concept Page UI Design (see PRD lines 449-490)
- Dynamic relation blocks: Only render non-empty sections
- Evidence previews: `excerpt + source + comment type [paraphrase/direct/figure]`
- Citations must include source attribution
- Patchnote format: Prepend to top of file, chronological order (newest first)
- Monthly trigger: Generate pages for new concepts after Knowledge Team concept review

**Affects Epics:** Epic 4 (Stories 4.1-4.7)

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

This section defines the comprehensive two-layer architecture: Evidence Layer (Postgres), Concept Layer (Graph DB), and Vector Database, plus Notion as primary workspace.

### Evidence Layer (PostgreSQL 16)

The Evidence Layer uses Amazon RDS PostgreSQL 16 and stores two types of data: (1) Newly Discovered content backup from Notion, and (2) Basics/Advanced evidence paragraphs extracted from documents.

#### Newly Discovered Tables (Notion Backup)

```sql
-- Raw HTML storage for newly discovered content (before parsing/deduplication)
CREATE TABLE raw_html_archive (
  id BIGSERIAL PRIMARY KEY,
  source_url TEXT NOT NULL,
  raw_html TEXT NOT NULL,  -- Complete HTML content as fetched
  content_hash TEXT NOT NULL,  -- SHA256 hash for deduplication

  -- Source metadata
  source TEXT,  -- 'twitter', 'rss', 'reddit', 'github', etc.
  fetch_timestamp TIMESTAMPTZ DEFAULT NOW(),
  http_status_code INTEGER,
  content_type TEXT,

  -- Processing status
  processed BOOLEAN DEFAULT FALSE,
  parsed_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_raw_html_source_url ON raw_html_archive(source_url);
CREATE INDEX idx_raw_html_content_hash ON raw_html_archive(content_hash);
CREATE INDEX idx_raw_html_processed ON raw_html_archive(processed, fetch_timestamp DESC);
CREATE INDEX idx_raw_html_fetch_timestamp ON raw_html_archive(fetch_timestamp DESC);

-- Daily backup of Notion Newly Discovered database
CREATE TABLE notion_news_backup (
  id BIGSERIAL PRIMARY KEY,
  notion_page_id TEXT UNIQUE NOT NULL,  -- Notion page UUID
  raw_html_id BIGINT REFERENCES raw_html_archive(id),  -- Link to raw HTML if available
  title TEXT NOT NULL,
  summary TEXT,  -- AI-generated summary from Auto-News
  score INTEGER CHECK (score BETWEEN 1 AND 5),
  category TEXT,  -- 'model-updates', 'framework-updates', etc.
  source TEXT,  -- 'twitter', 'rss', 'reddit', 'github', etc.
  source_url TEXT NOT NULL,
  tags TEXT[],
  review_status TEXT CHECK (review_status IN ('pending', 'approved', 'rejected')),
  reviewer TEXT,

  -- Metadata
  notion_created_at TIMESTAMPTZ,
  notion_last_edited_at TIMESTAMPTZ,
  backup_timestamp TIMESTAMPTZ DEFAULT NOW(),

  -- Cost tracking (from Auto-News processing)
  llm_tokens_used INTEGER,
  llm_cost_cents NUMERIC(10, 4),
  llm_provider TEXT,  -- 'claude', 'gemini', 'gpt-4'

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notion_backup_notion_id ON notion_news_backup(notion_page_id);
CREATE INDEX idx_notion_backup_category ON notion_news_backup(category);
CREATE INDEX idx_notion_backup_review_status ON notion_news_backup(review_status);
CREATE INDEX idx_notion_backup_backup_timestamp ON notion_news_backup(backup_timestamp DESC);
```

#### Evidence Layer Tables (Basics/Advanced)

```sql
-- Document metadata for Basics/Advanced ingestion
CREATE TABLE documents (
  id BIGSERIAL PRIMARY KEY,
  document_type TEXT NOT NULL,  -- 'book', 'blog', 'paper', 'video_transcript'
  source_identifier TEXT NOT NULL,  -- Book title, blog URL, paper DOI, video ID
  source_url TEXT,
  author TEXT,
  publication_date DATE,

  -- Processing metadata
  processing_status TEXT CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')) DEFAULT 'pending',
  total_paragraphs INTEGER,
  paragraphs_processed INTEGER DEFAULT 0,

  -- Semantic deduplication fields (inspired by auto-news benchmarking)
  simhash64 BIGINT,  -- Fast approximate duplicate detection
  cluster_id TEXT,   -- Semantic cluster assignment
  is_representative BOOLEAN DEFAULT FALSE,  -- Representative doc in cluster

  -- LLM judge scores (for prioritization)
  judge_originality NUMERIC(3, 2),  -- 1.00 - 5.00
  judge_depth NUMERIC(3, 2),
  judge_technical_accuracy NUMERIC(3, 2),
  judge_weighted_total NUMERIC(3, 2),

  -- Cost tracking
  llm_tokens_used INTEGER DEFAULT 0,
  llm_cost_cents NUMERIC(10, 4) DEFAULT 0,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_documents_status ON documents(processing_status);
CREATE INDEX idx_documents_cluster ON documents(cluster_id);
CREATE INDEX idx_documents_simhash ON documents(simhash64);

-- Evidence paragraphs extracted from documents
CREATE TABLE evidence_paragraphs (
  id BIGSERIAL PRIMARY KEY,
  document_id BIGINT REFERENCES documents(id) ON DELETE CASCADE,

  -- Paragraph content
  paragraph_text TEXT NOT NULL,
  paragraph_index INTEGER NOT NULL,  -- Position in document (0-indexed)

  -- Extracted concept (main idea)
  extracted_concept TEXT,  -- Noun phrase representing main idea
  extraction_confidence NUMERIC(3, 2),  -- 0.00 - 1.00

  -- Location metadata
  page_number INTEGER,
  section_title TEXT,

  -- Semantic deduplication
  paragraph_hash TEXT NOT NULL,  -- SHA256 for exact duplicate detection
  simhash64 BIGINT,  -- Fast similarity detection

  -- Quality scoring
  importance_score NUMERIC(3, 2),  -- 1.00 - 5.00 (from LLM judge)
  sampling_weight NUMERIC(3, 2),  -- For soft deduplication sampling

  -- Cost tracking
  llm_tokens_used INTEGER DEFAULT 0,
  llm_cost_cents NUMERIC(10, 4) DEFAULT 0,
  llm_provider TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_evidence_document ON evidence_paragraphs(document_id);
CREATE INDEX idx_evidence_concept ON evidence_paragraphs(extracted_concept);
CREATE INDEX idx_evidence_hash ON evidence_paragraphs(paragraph_hash);
CREATE INDEX idx_evidence_simhash ON evidence_paragraphs(simhash64);
CREATE INDEX idx_evidence_importance ON evidence_paragraphs(importance_score DESC);

-- Evidence metadata (additional context)
CREATE TABLE evidence_metadata (
  id BIGSERIAL PRIMARY KEY,
  evidence_id BIGINT REFERENCES evidence_paragraphs(id) ON DELETE CASCADE,

  -- Extraction details
  extract_type TEXT,  -- 'core_summary', 'supporting_detail', 'counterpoint', 'example'
  keywords TEXT[],
  entities JSONB,  -- Named entities extracted (person, organization, concept)

  -- Relations to handbook structure
  handbook_topic TEXT,  -- 'rag', 'prompting', 'fine-tuning', etc.
  handbook_subtopic TEXT,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_metadata_evidence ON evidence_metadata(evidence_id);
CREATE INDEX idx_metadata_topic ON evidence_metadata(handbook_topic);

-- Pipeline run tracking
CREATE TABLE pipeline_runs (
  id BIGSERIAL PRIMARY KEY,
  pipeline_name TEXT NOT NULL,  -- 'notion_backup', 'evidence_ingestion', 'writer_agent'
  run_status TEXT CHECK (run_status IN ('running', 'success', 'failed')) DEFAULT 'running',

  items_processed INTEGER DEFAULT 0,
  items_failed INTEGER DEFAULT 0,

  started_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,

  -- Cost tracking
  total_llm_tokens INTEGER DEFAULT 0,
  total_cost_cents NUMERIC(10, 4) DEFAULT 0,

  error_message TEXT
);

CREATE INDEX idx_pipeline_runs_name ON pipeline_runs(pipeline_name);
CREATE INDEX idx_pipeline_runs_started ON pipeline_runs(started_at DESC);

-- Failed items (dead-letter queue)
CREATE TABLE failed_items (
  id BIGSERIAL PRIMARY KEY,
  pipeline_run_id BIGINT REFERENCES pipeline_runs(id) ON DELETE SET NULL,

  item_type TEXT NOT NULL,  -- 'document', 'paragraph', 'notion_page'
  item_id TEXT NOT NULL,

  stage TEXT NOT NULL,  -- 'chunking', 'extraction', 'concept_matching', 'graph_update'
  failure_reason TEXT,
  error_details JSONB,

  attempt_count INTEGER DEFAULT 1,
  last_attempted TIMESTAMPTZ DEFAULT NOW(),
  resolved BOOLEAN DEFAULT FALSE,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_failed_items_resolved ON failed_items(resolved, created_at DESC);
CREATE INDEX idx_failed_items_stage ON failed_items(stage);

-- Knowledge verification contributors (community work)
CREATE TABLE knowledge_verification_contributors (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL UNIQUE,
  active BOOLEAN DEFAULT TRUE,

  -- Additional metadata
  email TEXT,
  github_username TEXT,
  contributions_count INTEGER DEFAULT 0,
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  last_contribution_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_contributors_active ON knowledge_verification_contributors(active);
CREATE INDEX idx_contributors_contributions ON knowledge_verification_contributors(contributions_count DESC);
```

### Concept Layer (Graph Database)

The Concept Layer stores normalized concepts as nodes with typed relations using GraphDB (open-source RDF graph database).

#### Concept Node Schema

```cypher
// Concept node properties
(:Concept {
  concept_id: string (UUID),
  concept_name: string (noun phrase, normalized),
  aliases: [string],  // Alternative names/synonyms
  summary: string (1-2 sentences),
  definition: string (detailed explanation),

  // Metadata
  contributors: [string],  // Who added/refined this concept
  confidence_score: float (0.0 - 1.0),  // How well-established this concept is
  evidence_count: integer,  // Number of linked evidence items

  created_at: datetime,
  updated_at: datetime
})
```

#### Relationship Types

```cypher
// 1. PREREQUISITE: Concept A must be understood before Concept B
(:Concept)-[:PREREQUISITE {
  strength: float (0.0 - 1.0),  // How essential is this prerequisite?
  contributor: string,
  created_at: datetime
}]->(:Concept)

// Example: "Embeddings" -[:PREREQUISITE]-> "Semantic Search"

// 2. RELATED: Concepts that are commonly discussed together
(:Concept)-[:RELATED {
  relation_type: string,  // 'comparison', 'alternative', 'complementary'
  strength: float (0.0 - 1.0),
  contributor: string,
  created_at: datetime
}]->(:Concept)

// Example: "RAG" -[:RELATED {relation_type: 'alternative'}]-> "Fine-tuning"

// 3. SUBTOPIC: Parent-child hierarchy in handbook structure
(:Concept)-[:SUBTOPIC {
  handbook_path: string,  // 'basics/rag/naive-rag'
  order_index: integer,  // Position in parent's children list
  created_at: datetime
}]->(:Concept)

// Example: "RAG" -[:SUBTOPIC]-> "Naive RAG"

// 4. EXTENDS: Concept B is an advanced/extended version of Concept A
(:Concept)-[:EXTENDS {
  extension_type: string,  // 'advanced_technique', 'variant', 'optimization'
  created_at: datetime
}]->(:Concept)

// Example: "Naive RAG" -[:EXTENDS]-> "Advanced RAG with Reranking"

// 5. CONTRADICTS: Concepts that represent opposing views or approaches
(:Concept)-[:CONTRADICTS {
  explanation: string,
  source: string,  // Which evidence discusses this contradiction?
  created_at: datetime
}]->(:Concept)

// Example: "Long Context Windows" -[:CONTRADICTS]-> "RAG for Large Docs"
```

#### Concept-Evidence Relation

The relation between concepts and evidence is maintained through the `extracted_concept` field in the Evidence Layer (Postgres). Each evidence paragraph has an `extracted_concept` field that references a concept name in the Graph DB.

**Query Pattern:**
```cypher
// 1. Load concept from Graph DB
MATCH (c:Concept {concept_name: 'RAG'})
RETURN c

// 2. Fetch evidence paragraphs from Postgres by extracted_concept field
// (Executed in Postgres, not Graph DB)
SELECT * FROM evidence_paragraphs WHERE extracted_concept = 'RAG'
```

This approach simplifies the architecture by eliminating a separate layer and using the natural foreign key relationship through the concept name field.

#### Writer Agent Query Examples

```cypher
// Query 1: Get concept with all relations (Graph DB)
MATCH (c:Concept {concept_name: 'RAG'})
OPTIONAL MATCH (c)-[pre:PREREQUISITE]->(prereq:Concept)
OPTIONAL MATCH (c)-[rel:RELATED]->(related:Concept)
OPTIONAL MATCH (c)-[sub:SUBTOPIC]->(subtopic:Concept)
OPTIONAL MATCH (c)-[ext:EXTENDS]->(extension:Concept)
OPTIONAL MATCH (c)-[con:CONTRADICTS]->(contradiction:Concept)
RETURN c,
       collect(DISTINCT {concept: prereq, strength: pre.strength}) as prerequisites,
       collect(DISTINCT {concept: related, type: rel.relation_type}) as related_concepts,
       collect(DISTINCT subtopic) as subtopics,
       collect(DISTINCT extension) as extensions,
       collect(DISTINCT contradiction) as contradictions

// Query 2: Fetch evidence paragraphs (Postgres)
SELECT * FROM evidence_paragraphs WHERE extracted_concept = 'RAG' ORDER BY importance_score DESC

// Query 3: Find concepts by semantic similarity (Graph DB)
MATCH (c:Concept)
WHERE c.concept_name CONTAINS 'retrieval' OR c.concept_name CONTAINS 'search'
RETURN c
ORDER BY c.evidence_count DESC
LIMIT 10

// Query 4: Get concept hierarchy for handbook section (Graph DB)
MATCH path = (parent:Concept {concept_name: 'RAG'})-[:SUBTOPIC*]->(child:Concept)
RETURN path
ORDER BY length(path)
```

### Vector Database Schema (pgvector)

The vector database uses pgvector extension in PostgreSQL for document embeddings and semantic search. This is specifically for Basics/Advanced documents only.

#### Document Embeddings Table

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Document embeddings for semantic search
CREATE TABLE document_embeddings (
  id BIGSERIAL PRIMARY KEY,
  evidence_paragraph_id BIGINT REFERENCES evidence_paragraphs(id) ON DELETE CASCADE,

  -- Vector embedding (1536 dimensions for text-embedding-3-small)
  embedding vector(1536) NOT NULL,

  -- Metadata for search context
  document_id BIGINT REFERENCES documents(id),
  paragraph_text TEXT NOT NULL,  -- Denormalized for faster retrieval
  handbook_topic TEXT,  -- 'rag', 'prompting', 'fine-tuning', etc.

  -- Embedding generation metadata
  model TEXT DEFAULT 'text-embedding-3-small',
  embedding_cost_cents NUMERIC(10, 4),

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create IVFFlat index for approximate nearest neighbor search
-- lists=100 is optimal for ~100K vectors (sqrt of row count)
CREATE INDEX idx_embeddings_vector ON document_embeddings
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX idx_embeddings_paragraph ON document_embeddings(evidence_paragraph_id);
CREATE INDEX idx_embeddings_document ON document_embeddings(document_id);
CREATE INDEX idx_embeddings_topic ON document_embeddings(handbook_topic);

-- Similarity search function
CREATE OR REPLACE FUNCTION search_similar_paragraphs(
  query_embedding vector(1536),
  topic_filter TEXT DEFAULT NULL,
  result_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
  paragraph_id BIGINT,
  paragraph_text TEXT,
  similarity FLOAT,
  document_id BIGINT,
  handbook_topic TEXT
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    de.evidence_paragraph_id,
    de.paragraph_text,
    1 - (de.embedding <=> query_embedding) AS similarity,
    de.document_id,
    de.handbook_topic
  FROM document_embeddings de
  WHERE (topic_filter IS NULL OR de.handbook_topic = topic_filter)
  ORDER BY de.embedding <=> query_embedding
  LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;
```

#### Usage Examples

```sql
-- Search for similar paragraphs across all topics
SELECT * FROM search_similar_paragraphs(
  (SELECT embedding FROM document_embeddings WHERE id = 123),
  NULL,
  10
);

-- Search within specific topic
SELECT * FROM search_similar_paragraphs(
  '[0.1, 0.2, ...]'::vector(1536),  -- Query embedding from OpenAI
  'rag',  -- Filter by RAG topic
  5  -- Top 5 results
);

-- Direct cosine similarity search (without function)
SELECT
  evidence_paragraph_id,
  paragraph_text,
  1 - (embedding <=> '[0.1, 0.2, ...]'::vector(1536)) AS similarity
FROM document_embeddings
ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector(1536)
LIMIT 10;
```

### Notion Database Structure

Notion serves as the primary workspace for Newly Discovered content. Auto-News writes directly to Notion.

#### Notion Properties Schema

```json
{
  "database_id": "auto_news_newly_discovered",
  "title": "Newly Discovered - Auto News",
  "properties": {
    "Title": {
      "type": "title",
      "title": [{"text": {"content": "GPT-4.5 Released with 50% Cost Reduction"}}]
    },
    "Summary": {
      "type": "rich_text",
      "rich_text": [{"text": {"content": "OpenAI announced GPT-4.5..."}}]
    },
    "Score": {
      "type": "select",
      "select": {"name": "5"}
    },
    "Category": {
      "type": "select",
      "select": {"name": "Model Updates"}
    },
    "Source": {
      "type": "select",
      "select": {"name": "RSS"}
    },
    "Source URL": {
      "type": "url",
      "url": "https://openai.com/blog/gpt-4.5"
    },
    "Tags": {
      "type": "multi_select",
      "multi_select": [
        {"name": "LLM"},
        {"name": "API"},
        {"name": "Cost Optimization"}
      ]
    },
    "Review Status": {
      "type": "status",
      "status": {"name": "Pending"}
    },
    "Reviewer": {
      "type": "people",
      "people": []
    },
    "Created At": {
      "type": "created_time",
      "created_time": "2025-11-08T12:00:00.000Z"
    },
    "Last Edited": {
      "type": "last_edited_time",
      "last_edited_time": "2025-11-08T15:30:00.000Z"
    }
  },
  "page_content": {
    "blocks": [
      {
        "type": "paragraph",
        "paragraph": {
          "rich_text": [{"text": {"content": "Full article summary and notes..."}}]
        }
      }
    ]
  }
}
```

### Data Relationships Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        TWO-LAYER ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐         ┌──────────────────┐                  │
│  │  Notion DB       │────────▶│ Evidence Layer   │                  │
│  │  (Primary)       │  Daily  │ (Postgres)       │                  │
│  │                  │  Backup │                  │                  │
│  │  - Auto-News     │         │  - notion_news   │                  │
│  │    writes here   │         │    _backup       │                  │
│  │  - Knowledge     │         │                  │                  │
│  │    team edits    │         │  - documents     │                  │
│  └──────────────────┘         │  - evidence_     │                  │
│                                │    paragraphs    │                  │
│                                │  - evidence_     │                  │
│                                │    metadata      │                  │
│                                └──────────────────┘                  │
│                                         │                             │
│                                         │ extracted_concept field    │
│                                         ▼                             │
│  ┌──────────────────┐                                                │
│  │  Concept Layer   │                                                │
│  │  (GraphDB)       │                                                │
│  │                  │                                                │
│  │  - Concept nodes │                                                │
│  │  - Relations:    │                                                │
│  │    PREREQUISITE  │                                                │
│  │    RELATED       │                                                │
│  │    SUBTOPIC      │                                                │
│  │    EXTENDS       │                                                │
│  │    CONTRADICTS   │                                                │
│  └──────────────────┘                                                │
│           │                            ▲                              │
│           │                            │                              │
│           ▼                            │ Queries concept             │
│  ┌──────────────────┐                 │                              │
│  │  Writer Agent    │─────────────────┘                              │
│  │                  │                                                │
│  │  1. Query Graph  │         ┌──────────────────┐                  │
│  │  2. Get concept  │         │  Vector DB       │                  │
│  │     name         │         │  (pgvector)      │                  │
│  │  3. Query        │         │                  │                  │
│  │     Postgres by  │         │                  │                  │
│  │     concept      │         │  - Document      │                  │
│  │  4. Synthesize   │         │    embeddings    │                  │
│  │     page         │◀────────│  - Similarity    │                  │
│  └──────────────────┘  Search │    search        │                  │
│           │              query └──────────────────┘                  │
│           ▼                            ▲                              │
│  ┌──────────────────┐                 │ Vectorize                   │
│  │  Handbook        │                 │                              │
│  │  (Markdown)      │                 │                              │
│  └──────────────────┘                 │                              │
│                                        │                              │
│                         Evidence Layer ─┘                            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘

Data Flow:
1. Newly Discovered: Auto-News → Raw HTML Archive → Notion → Daily Backup → Postgres
2. Basics/Advanced: Document → Chunking → Evidence Layer (Postgres)
                                        → Concept Extraction (Claude)
                                        → Concept Matching (GraphDB)
                                        → Vectorization (pgvector)
3. Publication: Writer Agent → Query GraphDB → Fetch Evidence → Synthesize → GitHub
```

### Data Flow Summary

**Pipeline 1 - Newly Discovered:**
1. Auto-News fetches content → saves raw HTML to `raw_html_archive` table (before any processing)
2. Auto-News parses HTML → deduplicates → scores with LLM → writes to Notion DB (primary)
3. Knowledge team reviews/edits in Notion
4. Daily backup DAG (00:00 UTC): Notion → Postgres `notion_news_backup` table (one-way sync, links to raw HTML)
5. Weekly publication DAG: Notion → Category/source formatting → GitHub → Jupyter Book

**Pipeline 2 - Basics/Advanced Ingestion:**
1. Document ingestion → `documents` table (Postgres)
2. Chunking → Extract paragraphs → `evidence_paragraphs` table
3. Claude extracts concepts from each paragraph → `extracted_concept` field
4. Concept matcher queries GraphDB for similar concepts
5. If match: Update `extracted_concept` field in Evidence Layer with matched concept name
6. If no match: Create new Concept node in GraphDB + update `extracted_concept` field with new concept name
7. Vectorize paragraph → Store in pgvector for document search
8. Update `evidence_metadata` with additional context

**Pipeline 3 - Writer Agent Publication:**
1. Trigger with concept_name (e.g., "RAG")
2. Query GraphDB: Load concept + relations (PREREQUISITE, RELATED, etc.)
3. Query Evidence Layer: SELECT * FROM evidence_paragraphs WHERE extracted_concept = 'RAG'
4. Fetch evidence paragraphs from Postgres
5. Claude synthesizes handbook page from concept + relations + evidence
6. Aggregate changes to `patchnote.md`
7. Commit to GitHub → Jupyter Book build → Live site

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

### ADR-004: Use GraphDB for Concept Layer

**Context:** Need a graph database to store normalized concepts with typed relations (prerequisite, related, subtopic, extends, contradicts).

**Decision:** GraphDB (open-source RDF graph database) instead of Neo4j, AWS Neptune, or ArangoDB.

**Rationale:**
- Open source: Free for self-hosting, no vendor lock-in
- RDF/SPARQL standard: Industry-standard semantic web technologies
- Triple store model: Natural fit for concept-relation-concept triples
- Reasonable performance: Handles 10K+ concepts with sub-second queries
- Active community: Well-maintained with regular updates
- Cost: $0 for open-source version vs $200+/month for managed alternatives

**Status:** Accepted

**When to revisit:** If concept count exceeds 50K nodes or query complexity requires enterprise features

---

### ADR-005: Jupyter Book over custom web app

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
