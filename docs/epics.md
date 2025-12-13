# cherry-in-the-haystack - Epic Breakdown

**Author:** HK
**Date:** 2025-12-06
**Project Level:** Medium
**Target Scale:** 50,000 monthly users within 6 months

---

## Overview

This document provides the complete epic and story breakdown for cherry-in-the-haystack, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

### Epic Summary

This project delivers **Cherry for AI Engineers** through 5 sequential epics implementing a two-layer knowledge architecture:

**Phase 1: Core MVP (Sequential - Epics 1-4)**
- **Epic 1: Foundation & Core Infrastructure** - Establish two-layer architecture (Evidence + Concept layers) and adapt Auto-News
- **Epic 2: Newly Discovered Pipeline** - Auto-News → Notion (primary) → Postgres backup → GitHub weekly publication
- **Epic 3: Evidence Ingestion & Knowledge Graph** - Document → Evidence Layer (Postgres) → Concept Layer (GraphDB) with normalized concepts
- **Epic 4: Writer Agent & Publication** - Knowledge graph → Writer Agent synthesis → Patchnote aggregation → GitHub → Jupyter Book

**Phase 2: Growth & Quality (Parallel - Epic 5)**
- **Epic 5: Community & Quality Operations** - GitHub PR workflow, monitoring, link validation, two-layer backup

**Delivery Strategy:**
- Epics 1-4 must complete sequentially to deliver working MVP
- Epic 5 enhances the MVP and can run in parallel to Epic 4 completion
- Each story is vertically sliced for single-session dev agent completion
- Stories use BDD acceptance criteria for clarity and testability

**Product Magic Delivered:**
- 🌟 **Clarity** - Two-layer knowledge graph enables intelligent synthesis
- 🌟 **Confidence** - Quality curation users can trust
- 🌟 **Speed** - Weekly updates keep handbook feeling alive
- 🌟 **Community Intelligence** - Knowledge that compounds instead of fades

---

## Epic 1: Foundation & Core Infrastructure

**Goal:** Establish technical foundation with two-layer knowledge architecture (Evidence Layer in PostgreSQL + Concept Layer in GraphDB), adapt Auto-News infrastructure, and set up Jupyter Book publication system.

**Value:** This epic creates the foundational two-layer architecture that enables intelligent knowledge synthesis. Without this infrastructure, no content pipeline or Writer Agent synthesis can function.

---

### Story 1.1: Handbook Foundation Setup

As a **developer**,
I want **handbook project initialized with modern Python tooling and Jupyter Book structure**,
So that **the team can build on proven foundations with clear separation from Auto-News codebase**.

**Acceptance Criteria:**

**Given** the existing Auto-News codebase exists in the repository
**When** I initialize the handbook foundation
**Then** the project structure includes:
- Poetry dependency management with `pyproject.toml` configured
- Ruff linting/formatting configuration (replaces flake8, black, isort)
- Loguru structured logging setup in `handbook/config/logging_config.py`
- Jupyter Book initialized in `handbook-content/` with `_config.yml` and `_toc.yml`
- Modern Python 3.10+ with type hints throughout
- Separation: `/auto-news-engine/` (existing) + `/handbook/` (new pipeline code)

**And** I can successfully run:
- `poetry install` (installs dependencies)
- `ruff check handbook/` (linting passes)
- `jupyter-book build handbook-content` (builds without errors)

**And** README.md documents:
- Architecture overview (two-layer knowledge system)
- Setup instructions for new developers
- Link to architecture.md for detailed technical decisions

**Prerequisites:** None (this is the first story)

**Technical Notes:**
- Follow architecture.md Project Initialization section (lines 13-56)
- Use Poetry 1.8+ for dependency management
- Ruff configuration in `pyproject.toml` (replaces multiple tools)
- Jupyter Book 1.0.4 with PyData Sphinx Theme
- Keep Auto-News operational during transition (separate concerns)
- Docker Compose for local development (Postgres + pgvector setup)

---

### Story 1.2: Evidence Layer Database Setup (PostgreSQL)

As a **backend engineer**,
I want **Amazon RDS PostgreSQL 16 configured with Evidence Layer schema**,
So that **we can store document paragraphs, extracted concepts, and Notion backup data**.

**Acceptance Criteria:**

**Given** the handbook foundation is initialized
**When** I set up the Evidence Layer
**Then** the PostgreSQL database includes:
- **Raw HTML Archive table** (for Auto-News ingestion - stores HTML before parsing)
- **Notion News Backup table** (daily backup of Notion Newly Discovered DB)
- **Documents table** (metadata for Basics/Advanced source documents)
- **Evidence Paragraphs table** (paragraph text, extracted_concept field, metadata)
- **Evidence Metadata table** (additional context, keywords, entities)
- **Pipeline Runs table** (tracking execution and costs)
- **Failed Items table** (dead-letter queue for retries)

**And** database connection module `handbook/db_connection/postgres.py` implements:
- Connection pooling (psycopg3 with max 20 connections)
- Environment variable configuration (DATABASE_URL)
- Context manager for transactions
- Idempotent UPSERT operations

**And** migration scripts in `scripts/setup_evidence_layer.sql` are executable and documented

**And** I can successfully insert and query sample evidence paragraphs

**Prerequisites:** Story 1.1 (project initialization)

**Technical Notes:**
- Follow architecture.md Evidence Layer schema (lines 758-989)
- Amazon RDS PostgreSQL 16, db.t3.small instance (~$25/month)
- Use psycopg3 (modern PostgreSQL adapter with type hints)
- Include indexes: content_hash, extracted_concept, paragraph_hash, simhash64
- Schema supports semantic deduplication (simhash64 field from auto-news benchmarking)
- Cost tracking fields: llm_tokens_used, llm_cost_cents, llm_provider
- Notion backup table links to raw_html_archive via raw_html_id foreign key

---

### Story 1.3: Concept Layer Database Setup (GraphDB)

As a **backend engineer**,
I want **GraphDB RDF graph database initialized with Concept Layer schema**,
So that **we can store normalized concepts with typed relations for Writer Agent synthesis**.

**Acceptance Criteria:**

**Given** the Evidence Layer is set up
**When** I initialize the Concept Layer
**Then** the GraphDB includes:
- **Concept nodes** with properties: concept_id (UUID), concept_name (normalized noun phrase), summary, definition, contributors, confidence_score, evidence_count
- **Relationship types defined:**
  - PREREQUISITE (strength, contributor, created_at)
  - RELATED (relation_type: comparison/alternative/complementary, strength)
  - SUBTOPIC (handbook_path, order_index)
  - EXTENDS (extension_type: advanced_technique/variant/optimization)
  - CONTRADICTS (explanation, source)

**And** database connection module `handbook/db_connection/graph_db.py` implements:
- GraphDB connection with environment variable configuration
- Query methods: load_concept(), find_similar_concepts(), create_concept(), add_relation()
- Support for Cypher-like queries (or SPARQL for RDF)
- Connection pooling for concurrent Writer Agent queries

**And** initialization script `scripts/setup_graph_db.py` creates schema and sample concepts

**And** I can successfully create a concept, add relations, and query the graph

**Prerequisites:** Story 1.2 (Evidence Layer setup)

**Technical Notes:**
- Follow architecture.md Concept Layer schema (lines 991-1114)
- Use GraphDB (open-source RDF graph database) - free, self-hosted
- Concept nodes store ONLY metadata - NO evidence text (evidence stored in Postgres)
- Evidence-concept linkage via `extracted_concept` field in Evidence Layer
- Query pattern: Load concept from GraphDB → Query Postgres by extracted_concept field
- Relations are dynamic and extensible (can add new relation types)
- Target performance: Sub-500ms queries for Writer Agent
- Alternative: Neo4j if GraphDB has limitations (track as ADR)

---

### Story 1.4: Vector Database Setup (pgvector)

As a **ML engineer**,
I want **pgvector extension enabled for document embeddings in PostgreSQL**,
So that **we can perform semantic search on Basics/Advanced documents**.

**Acceptance Criteria:**

**Given** the Evidence Layer PostgreSQL is running
**When** I set up the vector database
**Then** the system includes:
- pgvector extension installed and enabled (`CREATE EXTENSION vector;`)
- **document_embeddings table** with:
  - vector(1536) column for OpenAI text-embedding-3-small
  - References to evidence_paragraph_id
  - Metadata: document_id, paragraph_text (denormalized), handbook_topic
- IVFFlat index created (lists=100 for ~100K vectors)
- Search function `search_similar_paragraphs()` implemented

**And** database connection module `handbook/db_connection/vector_db.py` implements:
- Embedding storage and retrieval
- Cosine similarity search (<100ms for top-10 queries)
- Batch insertion for efficiency

**And** I can successfully:
- Store embeddings for sample paragraphs
- Query similar paragraphs using cosine similarity
- Filter by handbook_topic during search

**Prerequisites:** Story 1.2 (Evidence Layer setup)

**Technical Notes:**
- Follow architecture.md Vector Database schema (lines 1116-1209)
- pgvector is a PostgreSQL extension (no separate database needed)
- Embeddings ONLY for Basics/Advanced documents (NOT Newly Discovered news)
- OpenAI text-embedding-3-small: 1536 dimensions, $0.02/1M tokens
- IVFFlat index: `lists = sqrt(row_count)` → 100 for 100K vectors
- Use `vector_cosine_ops` for cosine similarity (1 - distance)
- Store paragraph_text denormalized for faster retrieval in search results
- Cost tracking: embedding_cost_cents field

---

### Story 1.5: Auto-News Engine Adaptation

As a **backend engineer**,
I want **existing Auto-News Airflow DAGs adapted for handbook Newly Discovered pipeline**,
So that **we can reuse proven ingestion/deduplication/scoring logic with Notion as primary output**.

**Acceptance Criteria:**

**Given** the Auto-News codebase exists in `/auto-news-engine/`
**When** I adapt the engine for handbook use
**Then** the adapted system:
- Identifies reusable operators: ingestion, deduplication, categorization, scoring
- Configures LLM-focused sources (Twitter, Discord, GitHub, RSS, papers)
- Updates categorization for handbook taxonomy (Model Updates, Framework Updates, Productivity Tools, Business Cases, How People Use AI)
- Modifies output: Auto-News writes directly to **Notion DB** (NOT Postgres first)
- Ensures deduplication runs before AI scoring (cost optimization)
- Preserves existing Auto-News functionality (brownfield constraint)

**And** Airflow DAGs are runnable in development environment with test mode

**And** configuration file documents:
- Which operators are reused vs new
- Source list with poll frequencies
- Notion database ID for handbook review workspace

**And** test run successfully ingests from at least 3 sources and writes to Notion

**Prerequisites:** Story 1.2 (Evidence Layer for backup)

**Technical Notes:**
- Follow architecture.md Novel Pattern 2: Notion as Primary (lines 480-528)
- Auto-News writes to Notion DB (primary workspace for Knowledge Team)
- Daily backup DAG: Notion → Postgres (one-way, NOT bidirectional sync)
- Keep existing Auto-News operators modular for reuse
- Reference PRD section on Auto-News upstream (line 1168)
- Notion API v2 with rate limit handling (3 requests/second)
- Consider extracting core logic into shared library (`auto-news-engine/operators/`)

---

### Story 1.6: GitHub Actions CI/CD Pipeline

As a **DevOps engineer**,
I want **automated CI/CD pipeline for linting, testing, and Jupyter Book deployment**,
So that **code quality is enforced and handbook updates deploy automatically**.

**Acceptance Criteria:**

**Given** the handbook repository has code and tests
**When** I configure GitHub Actions workflows
**Then** the CI pipeline includes:
- **`.github/workflows/ci.yml`** (runs on PRs):
  - Ruff linting (`ruff check handbook/`)
  - pytest unit tests with coverage report
  - Type checking with mypy
  - markdown-lint for content files
  - Link validation (optional on PR, required weekly)
- **`.github/workflows/deploy.yml`** (runs on main branch push):
  - Install Jupyter Book dependencies (cached)
  - Build handbook (`jupyter-book build handbook-content/`)
  - Deploy to GitHub Pages (gh-pages branch)
  - Build timeout: 10 minutes max
  - Deployment status badge in README

**And** workflows complete in under 10 minutes

**And** failed workflows send notifications (GitHub notifications initially)

**And** deployment is zero-downtime (previous version stays live until new build succeeds)

**Prerequisites:** Story 1.1 (project initialization)

**Technical Notes:**
- Follow architecture.md CI/CD patterns (lines 750-753)
- Use peaceiris/actions-gh-pages for deployment
- Cache pip dependencies for faster builds (30s vs 2min)
- Separate fast CI (linting, tests) from slower deployment
- Deployment only on main branch (not PRs)
- Future: Add staging environment for pre-production testing

---

### Story 1.7: Local Development Environment Setup

As a **developer**,
I want **Docker Compose environment with all databases for local development**,
So that **new contributors can set up the full stack in under 30 minutes**.

**Acceptance Criteria:**

**Given** the project has database schemas defined
**When** I run local setup
**Then** the development environment includes:
- **`docker-compose.yml`** with services:
  - PostgreSQL 16 with pgvector extension
  - GraphDB (or Neo4j for local testing)
  - Optional: Airflow for local DAG testing
- **`.env.example`** template with required variables:
  - DATABASE_URL, GRAPH_DB_URL
  - OPENAI_API_KEY, ANTHROPIC_API_KEY, GOOGLE_API_KEY
  - NOTION_API_TOKEN, GITHUB_PAT
- **Setup script** `scripts/setup_local.sh`:
  - Starts Docker Compose
  - Runs database migrations
  - Seeds sample data
  - Validates connections

**And** documentation in `docs/local-setup.md`:
- Prerequisites (Docker, Poetry, Python 3.10+)
- Step-by-step setup guide
- How to run tests locally
- How to build Jupyter Book locally
- Troubleshooting common issues

**And** a new developer can complete setup in under 30 minutes

**Prerequisites:** Stories 1.2, 1.3, 1.4 (all database schemas)

**Technical Notes:**
- Docker Compose simplifies onboarding significantly
- Mount volumes for persistence during development
- Use healthchecks for service dependencies
- Include sample .env with mock/test API keys where possible
- Document local Airflow setup separately (complex, optional)
- Pre-commit hooks configuration: `pre-commit install`

---

## Epic 2: Newly Discovered Pipeline

**Goal:** Build automated weekly publication pipeline where Auto-News ingests content → writes to Notion (primary) → daily backup to Postgres → weekly GitHub publication with category/source-specific formatting.

**Value:** This epic delivers the "Speed" promise - weekly fresh content that keeps the handbook feeling "alive". Leverages existing Auto-News engine while treating Notion as the primary workspace for human review.

---

### Story 2.1: Notion Database as Primary Workspace

As a **content curator**,
I want **Auto-News to write scored content directly to Notion database**,
So that **Knowledge Team can review and edit in familiar interface without backend complexity**.

**Acceptance Criteria:**

**Given** Auto-News engine is adapted for handbook sources
**When** scored content (score 5) is ready for review
**Then** Auto-News writes to Notion database with:
- Page properties: Title, Summary, Score, Category, Source, Source URL, Tags, Review Status, Reviewer
- Page content blocks with full article summary and notes
- Notion API v2 integration with rate limit handling (3 req/sec)
- Auto-assignment to Knowledge Team members (round-robin or by category)

**And** Notion database structure follows PRD specification:
- Database ID configured in environment variables
- Properties schema matches architecture.md (lines 1212-1283)
- Review workflow: Pending → In Review → Approved/Rejected

**And** configuration module `handbook/integrations/notion_client.py` implements:
- Create/update page methods
- Query database with filters
- Pagination for large result sets
- Error handling with retry logic

**And** test run successfully creates pages in Notion for sample content

**Prerequisites:** Story 1.5 (Auto-News adaptation)

**Technical Notes:**
- Follow architecture.md Novel Pattern 2: Notion as Primary (lines 480-528)
- Notion is PRIMARY - Postgres is backup only (one-way sync)
- Notion API v2 with official SDK: `notion-client` package
- Store Notion database ID and API token in environment variables
- Handle Notion API rate limits gracefully (exponential backoff)
- Knowledge Team works entirely in Notion - no custom backend UI needed
- Weekly review cycle: Wednesday meetings documented in PRD

---

### Story 2.2: Daily Notion to Postgres Backup

As a **data engineer**,
I want **daily automated backup from Notion to Postgres Evidence Layer**,
So that **we maintain data ownership and enable analytics without Notion API dependency**.

**Acceptance Criteria:**

**Given** Notion database contains reviewed content
**When** daily backup DAG runs (00:00 UTC)
**Then** the backup process:
- Queries all pages from Notion Newly Discovered database
- Stores in `notion_news_backup` table with full metadata
- Links to `raw_html_archive` via `raw_html_id` if HTML exists
- Uses UPSERT based on `notion_page_id` (idempotent)
- Tracks backup timestamp and status

**And** Airflow DAG `handbook/dags/notion_backup_dag.py` implements:
- Scheduled execution: Daily at 00:00 UTC
- Pagination handling for large datasets
- Error handling with retry logic
- Metrics logging (items backed up, duration, errors)

**And** backup is ONE-WAY ONLY:
- Notion → Postgres (data flows this direction)
- NO reverse sync (Postgres changes don't update Notion)
- Notion is always source of truth

**And** backup completes within 10 minutes for 1000+ items

**Prerequisites:** Story 1.2 (Evidence Layer), Story 2.1 (Notion integration)

**Technical Notes:**
- Follow architecture.md data flow (lines 1356-1361)
- Notion API pagination: `start_cursor` for large databases
- UPSERT prevents duplicates on re-runs
- Store `notion_created_at` and `notion_last_edited_at` for tracking
- Pipeline run tracked in `pipeline_runs` table
- Alert if backup fails (email/Slack)
- Historical tracking enables analytics and rollback if needed

---

### Story 2.3: Category and Topic Matching

As a **content curator**,
I want **news items automatically matched to handbook topics and categories**,
So that **approved content flows to the correct handbook section without manual sorting**.

**Acceptance Criteria:**

**Given** Notion contains reviewed news items
**When** category matching runs
**Then** each item is classified into:
- **Primary category** (one of 5 Newly Discovered categories):
  - Model Updates
  - Framework/Library/Tools Updates
  - Productivity Tools
  - Business Cases & Case Studies
  - How People Use AI
- **Handbook topic tags** (if applicable): RAG, prompting, fine-tuning, agents, embeddings, evaluation
- **Keywords** extracted for searchability

**And** matching module `handbook/pipeline/newly_discovered/category_matcher.py` implements:
- LLM-based classification with structured output
- Confidence scores for each classification
- Fallback to "General" category if uncertain
- Human override capability in Notion (reviewer can change category)

**And** matching accuracy tracked:
- Log AI classifications with confidence
- Track human override rate
- Improve prompt based on patterns

**And** matched categories stored in Postgres backup and used for GitHub organization

**Prerequisites:** Story 2.2 (Notion backup)

**Technical Notes:**
- Use Claude or GPT-4 with structured JSON output
- Classification prompt includes category definitions from PRD
- Store confidence scores for quality monitoring
- Human overrides in Notion take precedence
- Consider caching classifications to reduce API costs
- Topic tags enable cross-linking to Basics/Advanced sections (future)

---

### Story 2.4: Category-Specific and Source-Specific Formatting

As a **content publisher**,
I want **markdown generation with formatting that varies by category and source type**,
So that **different content types display optimally for their purpose**.

**Acceptance Criteria:**

**Given** approved news items with assigned categories
**When** markdown generation runs
**Then** the format dispatcher applies category-specific templates:
- **Model Updates:** Title, release date, key changes, API updates, pricing, external link
- **Framework Updates:** Tool name, version, change summary, migration notes, link to release
- **Productivity Tools:** Tool description, use case, features, pricing tier, installation
- **Business Cases:** Company, product launch, architecture insights, results/metrics, link
- **How People Use AI:** Brief summary, domain/industry, workflow description, link

**And** source-specific formatting:
- Twitter threads: Preserve thread structure, author attribution
- GitHub releases: Version number prominent, changelog format
- Blog posts: Author, publication, key takeaways
- Papers: Authors, abstract, key findings, arXiv link

**And** formatting module `handbook/pipeline/newly_discovered/format_dispatcher.py` implements:
- Template system for each category
- Jinja2 templates for markdown generation
- Frontmatter with metadata (date, category, source_url, tags)
- Consistent style across same-category items

**And** generated markdown follows MyST syntax for Jupyter Book compatibility

**Prerequisites:** Story 2.3 (category matching)

**Technical Notes:**
- Follow architecture.md Novel Pattern 2 integration (lines 480-528)
- Templates in `handbook/pipeline/publication/templates/`
- Frontmatter format specified in architecture.md (lines 664-674)
- Handle special characters in titles (sanitize for filenames)
- Image URLs embedded as markdown (no local download in MVP)
- Consider using existing `weekly_update.py` script from auto-news

---

### Story 2.5: Weekly GitHub Publication Workflow

As a **automation engineer**,
I want **approved content automatically committed to GitHub repository weekly**,
So that **handbook updates go live without manual file operations**.

**Acceptance Criteria:**

**Given** Notion contains approved items for the week
**When** weekly publication DAG runs (Sunday 00:00 UTC or manual trigger)
**Then** the publication process:
- Queries Notion for all items with status="Approved" since last publish
- Generates markdown files using category-specific formatting
- Organizes files: `newly-discovered/{category}/YYYY-MM-DD-{slug}.md`
- Creates single git commit with all files
- Commit message: "Weekly publish: {count} items ({date})"
- Pushes to main branch using bot account

**And** Airflow DAG `handbook/dags/weekly_publish_dag.py` implements:
- Scheduled execution: Weekly Sunday 00:00 UTC
- Dry-run mode for testing
- Rollback capability if errors detected
- Post-publish: Update items in Notion with "published_date"

**And** GitHub committer module `handbook/pipeline/publication/github_committer.py` uses:
- Bot account with Personal Access Token (repo write permission)
- GitHub API for file creation/updates
- Atomic commits (all files in one commit)
- Clear attribution in commit message

**And** published items marked in Notion to prevent duplicates

**Prerequisites:** Story 2.4 (formatting)

**Technical Notes:**
- Follow architecture.md deployment architecture (lines 1527-1537)
- Bot account: `handbook-bot` with PAT stored in environment variables
- Use PyGithub or GitHub API directly
- Idempotent: Re-running doesn't create duplicates (check existing files)
- Trigger GitHub Actions deployment automatically on push
- Manual trigger workflow for ad-hoc publications
- Log all publication actions for audit trail

---

### Story 2.6: Weekly Publication Monitoring and Alerts

As a **operations manager**,
I want **visibility into weekly publication health and immediate alerts for failures**,
So that **content updates are reliable and issues are caught early**.

**Acceptance Criteria:**

**Given** weekly publication workflow is operational
**When** I check publication health
**Then** monitoring shows:
- Last successful publish date and item count
- Publication history (weekly trend: items published over time)
- Approval velocity (time from Auto-News score → Notion approval → GitHub)
- Source performance (which sources contribute approved items)
- Error rates (failed publications, reasons)

**And** alerts sent for:
- Publication failure (GitHub commit failed, Notion query failed)
- No approvals in current week (Thursday check - reminds team)
- Low approval rate (<20% of score-5 items approved)
- Unusual item count (spike or drought)

**And** alerting channels:
- Email for weekly summary reports
- Slack webhook for moderate issues
- PagerDuty/on-call for critical failures (optional, future)

**And** dashboard accessible via:
- Airflow UI (built-in DAG monitoring)
- Custom dashboard (Streamlit or Grafana - optional)
- Weekly email report to stakeholders

**Prerequisites:** Story 2.5 (publication workflow)

**Technical Notes:**
- Store metrics in `pipeline_runs` table
- Airflow built-in monitoring + alerting
- Email alerts via SMTP configuration
- Slack webhook for real-time notifications
- Track metrics: approval_rate, time_to_publish, source_health
- Weekly report generation automated (Python script)
- Consider CloudWatch integration for AWS infrastructure monitoring

---

## Epic 3: Evidence Ingestion & Knowledge Graph

**Goal:** Implement the two-layer knowledge architecture pattern: Document → Evidence Layer (Postgres paragraphs) → Concept Layer (GraphDB normalized concepts) with intelligent concept matching and vectorization.

**Value:** This epic delivers the "Clarity" foundation - the two-layer architecture that enables Writer Agent to synthesize coherent handbook pages from structured knowledge with full traceability.

---

### Story 3.1: Document Chunking Pipeline

As a **ML engineer**,
I want **documents split into semantically meaningful paragraphs for evidence storage**,
So that **each paragraph can be analyzed, concept-extracted, and cited independently**.

**Acceptance Criteria:**

**Given** Basics/Advanced source documents (PDFs, HTML, markdown)
**When** document chunking pipeline runs
**Then** the system:
- Extracts text from multiple formats (PDF, HTML, markdown, plain text)
- Splits into paragraphs respecting semantic boundaries (not fixed-size chunks)
- Preserves metadata: document_id, page_number, paragraph_index, section_title
- Generates paragraph_hash (SHA256) for exact duplicate detection
- Generates simhash64 for approximate similarity detection
- Stores in `evidence_paragraphs` table

**And** chunking module `handbook/pipeline/evidence_ingestion/document_chunker.py` implements:
- Format handlers for PDF (PyPDF2/pdfplumber), HTML (BeautifulSoup), markdown
- Semantic chunking (respect sentence/paragraph boundaries, not byte limits)
- Metadata extraction (page numbers from PDFs, headings from HTML/markdown)
- Batch processing for multiple documents

**And** chunking quality validated:
- Average paragraph length: 100-500 words
- Semantic coherence (not splitting mid-sentence)
- Metadata accuracy

**Prerequisites:** Story 1.2 (Evidence Layer)

**Technical Notes:**
- Follow architecture.md Evidence Layer schema (lines 828-905)
- Use LangChain RecursiveCharacterTextSplitter or custom semantic chunker
- simhash64 field inspired by auto-news benchmarking for deduplication
- Store raw paragraph text without modification
- Track processing status in `documents` table
- Handle edge cases: tables, code blocks, equations (preserve formatting)

---

### Story 3.2: Concept Extraction with Claude

As a **ML engineer**,
I want **main idea concepts extracted from each paragraph using Claude Sonnet**,
So that **paragraphs can be linked to normalized concepts in the knowledge graph**.

**Acceptance Criteria:**

**Given** paragraphs stored in Evidence Layer
**When** concept extraction runs
**Then** for each paragraph, Claude extracts:
- **Extracted concept:** Single normalized noun phrase representing main idea
- **Extraction confidence:** 0.00 - 1.00 score
- **Importance score:** 1.00 - 5.00 (relevance to LLM engineering)
- **Sampling weight:** For soft deduplication (similar paragraphs get lower weight)

**And** extraction module `handbook/pipeline/evidence_ingestion/concept_extractor.py` implements:
- Claude 3.5 Sonnet API integration with structured output
- Prompt engineering for consistent noun-phrase extraction
- Batch processing (multiple paragraphs per API call for cost efficiency)
- Cost tracking (tokens used, cost in cents)
- Retry logic with exponential backoff

**And** concept extraction follows rules:
- Concepts are noun phrases (not sentences): "Retrieval-Augmented Generation", "Prompt Caching", "Fine-Tuning with LoRA"
- Concepts are normalized (consistent naming across sources)
- Generic concepts rejected ("Introduction", "Overview", "Conclusion")
- Multi-concept paragraphs use primary concept only

**And** extraction quality metrics tracked:
- Confidence distribution
- Concept diversity (unique concepts / total paragraphs)
- LLM cost per paragraph

**Prerequisites:** Story 3.1 (document chunking)

**Technical Notes:**
- Follow architecture.md Novel Pattern 1: Two-Layer Architecture (lines 435-477)
- Claude 3.5 Sonnet: 200K context, superior concept extraction, $3-15/1M tokens
- Structured output: JSON with concept_name, confidence, importance, reasoning
- Prompt includes examples of good/bad concept extractions
- Store in `extracted_concept` field of `evidence_paragraphs` table
- Fallback to Gemini Flash if Claude unavailable ($0.075-0.30/1M tokens)

---

### Story 3.3: Concept Matching and Normalization

As a **knowledge engineer**,
I want **extracted concepts matched against existing GraphDB concepts**,
So that **the same concept from different sources maps to one normalized node**.

**Acceptance Criteria:**

**Given** paragraphs with extracted concepts
**When** concept matching runs
**Then** for each extracted concept:
- Query GraphDB for similar existing concepts (semantic similarity)
- If match found (similarity > 0.90): Use existing concept_name, update paragraph's extracted_concept field
- If no match: Create new concept node in GraphDB with initial properties
- Store match confidence and decision reasoning

**And** matching module `handbook/pipeline/evidence_ingestion/concept_matcher.py` implements:
- Semantic similarity search in GraphDB (embedding-based or LLM-based)
- Configurable similarity threshold (default 0.90)
- Human-in-the-loop for ambiguous matches (0.80-0.90 range)
- Batch processing for efficiency
- Match history tracking (merge decisions, new concept creation)

**And** GraphDB updater `handbook/pipeline/evidence_ingestion/graph_updater.py`:
- Creates concept nodes with metadata (name, aliases, summary, contributors)
- Updates evidence_count when paragraphs linked
- Adds initial relations if detected (e.g., "RAG" RELATES_TO "Embeddings")
- Tracks concept creation timestamp and contributor

**And** matching quality validated:
- False positive rate (different concepts incorrectly merged)
- False negative rate (same concept not matched)
- Manual review workflow for ambiguous cases

**Prerequisites:** Story 1.3 (Concept Layer), Story 3.2 (concept extraction)

**Technical Notes:**
- Follow architecture.md Concept Matching section (lines 397-407)
- Semantic matching via embeddings + cosine similarity OR LLM judge
- Consider using Claude for match decisions (context-aware, handles nuance)
- Store match decisions in `evidence_metadata` table for audit
- Concept normalization prevents graph fragmentation
- Monthly review: Knowledge Team validates concept merges

---

### Story 3.4: Document Vectorization with pgvector

As a **ML engineer**,
I want **paragraph embeddings stored in pgvector for semantic search**,
So that **users can search Basics/Advanced content semantically (future feature)**.

**Acceptance Criteria:**

**Given** paragraphs stored in Evidence Layer with extracted concepts
**When** vectorization runs
**Then** for each paragraph:
- Generate embedding using OpenAI text-embedding-3-small (1536 dims)
- Store in `document_embeddings` table with metadata
- Link to evidence_paragraph_id
- Denormalize paragraph_text for faster search retrieval
- Track embedding cost

**And** vectorization module `handbook/db_connection/vector_db.py` implements:
- OpenAI embedding API integration
- Batch processing (2048 texts per request for 50% discount)
- IVFFlat index maintenance (rebuild when row count doubles)
- Cosine similarity search function
- Cost optimization (cache embeddings, avoid re-vectorizing)

**And** vector search tested:
- Query: "How does retrieval-augmented generation work?"
- Returns: Top 10 relevant paragraphs with similarity scores
- Filter by handbook_topic (optional)
- Sub-100ms query latency

**And** ONLY Basics/Advanced documents vectorized (NOT Newly Discovered news)

**Prerequisites:** Story 1.4 (pgvector setup), Story 3.1 (paragraphs available)

**Technical Notes:**
- Follow architecture.md Vector Database schema (lines 1116-1209)
- OpenAI text-embedding-3-small: $0.02/1M tokens, 1536 dimensions
- Batch API for cost savings: 2048 texts/request
- IVFFlat index: `lists = sqrt(row_count)` → start with 100
- Store handbook_topic (extracted from document metadata or concept)
- Vector search is supplementary (Graph DB is primary knowledge store)
- Use `vector_cosine_ops` for cosine similarity

---

### Story 3.5: Evidence Metadata Enrichment

As a **content curator**,
I want **paragraphs enriched with metadata beyond extracted concepts**,
So that **Writer Agent has rich context for synthesis and citation**.

**Acceptance Criteria:**

**Given** paragraphs with extracted concepts
**When** metadata enrichment runs
**Then** each paragraph's `evidence_metadata` table includes:
- **Extract type:** core_summary, supporting_detail, counterpoint, example
- **Keywords:** Key terms and phrases (5-10 per paragraph)
- **Entities:** Named entities (people, organizations, concepts) as JSONB
- **Handbook topic:** Primary topic area (rag, prompting, fine-tuning, etc.)
- **Handbook subtopic:** More specific categorization

**And** enrichment module extracts:
- Named entities using spaCy or Claude
- Keywords using TF-IDF or Claude
- Extract type classification using LLM
- Topic assignment based on concept matching

**And** metadata enables:
- Writer Agent filtering (e.g., "core summaries only for overview section")
- Evidence type diversity in synthesis (mix summaries, examples, counterpoints)
- Cross-linking between handbook sections
- Quality filtering (importance_score prioritization)

**And** enrichment is incremental (new paragraphs enriched, existing preserved)

**Prerequisites:** Story 3.3 (concept matching)

**Technical Notes:**
- Follow architecture.md Evidence Metadata table (lines 906-924)
- spaCy for fast NER, Claude for nuanced extraction
- Store entities as JSONB for flexibility
- Keywords useful for future full-text search
- Handbook topic inference: Use concept to topic mapping
- Extract type helps Writer Agent structure pages logically
- Balance enrichment cost vs value (prioritize high-importance paragraphs)

---

### Story 3.6: Evidence Ingestion Airflow DAG

As a **data engineer**,
I want **end-to-end Airflow DAG orchestrating document → evidence → concept → graph pipeline**,
So that **ingestion is automated, monitored, and recoverable**.

**Acceptance Criteria:**

**Given** source documents are available (S3, local filesystem, URLs)
**When** evidence ingestion DAG runs
**Then** the pipeline executes sequentially:
1. **Document intake:** Register document in `documents` table
2. **Chunking:** Split into paragraphs, store in `evidence_paragraphs`
3. **Concept extraction:** Claude extracts concepts, stores in `extracted_concept` field
4. **Concept matching:** Match/merge with GraphDB, update `extracted_concept`
5. **Vectorization:** Generate embeddings, store in `document_embeddings`
6. **Metadata enrichment:** Enrich `evidence_metadata` table
7. **Completion:** Mark document as processed, track metrics

**And** Airflow DAG `handbook/dags/evidence_ingestion_dag.py` implements:
- Task dependencies with proper error handling
- Idempotent tasks (re-running doesn't duplicate data)
- Checkpoint/resume capability (restart from failed task)
- Cost tracking per task (LLM tokens, API costs)
- Metrics logging (paragraphs processed, concepts created, duration)

**And** DAG supports:
- Manual trigger for ad-hoc document ingestion
- Batch processing (multiple documents in one run)
- Dry-run mode for testing
- Failed item tracking in `failed_items` table

**And** monitoring dashboard shows:
- Pipeline status (running, succeeded, failed)
- Current document being processed
- Cost accumulation (real-time)
- Estimated completion time

**Prerequisites:** Stories 3.1-3.5 (all ingestion components)

**Technical Notes:**
- Follow architecture.md pipeline structure (lines 161-176)
- Use Airflow XCom for small data passing (<1MB)
- Use Postgres for large data (pass IDs via XCom)
- Implement retry logic (3 attempts with exponential backoff)
- Dead-letter queue for permanent failures
- Alert if DAG fails or costs exceed threshold
- Manual review for ambiguous concept matches (human-in-the-loop task)

---

### Story 3.7: Evidence Deduplication and Quality Scoring

As a **ML engineer**,
I want **semantically similar paragraphs identified and quality-scored**,
So that **Writer Agent uses diverse, high-quality evidence without redundancy**.

**Acceptance Criteria:**

**Given** paragraphs stored in Evidence Layer with embeddings
**When** deduplication and scoring runs
**Then** the system:
- Uses simhash64 for fast approximate duplicate detection
- Uses vector cosine similarity for semantic duplicate detection (threshold 0.92)
- Clusters similar paragraphs (same concept, similar content)
- Identifies representative paragraph per cluster (highest importance_score)
- Assigns sampling_weight (higher for unique, lower for redundant)
- Uses LLM judge to score paragraph quality (originality, depth, accuracy)

**And** deduplication module identifies:
- Exact duplicates (same paragraph from different sources)
- Near-duplicates (paraphrased content)
- Semantic clusters (related but distinct paragraphs)

**And** quality scoring evaluates:
- **Originality:** Novel insight vs common knowledge (1.00-5.00)
- **Depth:** Superficial vs detailed explanation (1.00-5.00)
- **Technical accuracy:** Correctness of claims (1.00-5.00)
- **Weighted total:** Combined score for prioritization

**And** deduplication results stored:
- cluster_id in `evidence_paragraphs` table
- is_representative flag for cluster representatives
- sampling_weight for probabilistic sampling

**And** Writer Agent uses deduplication data to ensure evidence diversity

**Prerequisites:** Story 3.4 (vectorization), Story 3.5 (metadata)

**Technical Notes:**
- Follow architecture.md semantic deduplication fields (lines 844-857, 884-890)
- simhash64 for O(1) approximate matching (fast)
- Vector similarity for precise semantic matching (slower but accurate)
- LLM judge scores stored: judge_originality, judge_depth, judge_technical_accuracy
- Inspired by auto-news benchmarking (reference in architecture.md)
- Soft deduplication: Don't delete, just down-weight (preserve for context)
- Monthly re-scoring as knowledge graph evolves

---

## Epic 4: Writer Agent & Publication

**Goal:** Build Writer Agent that queries knowledge graph → synthesizes handbook pages → generates diagrams → aggregates patchnotes → publishes to GitHub → deploys via Jupyter Book.

**Value:** This epic delivers the synthesis magic - transforming structured knowledge into coherent, traceable handbook pages with automated diagram generation and change tracking.

---

### Story 4.1: Knowledge Graph Query Engine

As a **backend engineer**,
I want **Writer Agent to efficiently query concepts, relations, and evidence from knowledge graph**,
So that **synthesis has complete context for generating high-quality pages**.

**Acceptance Criteria:**

**Given** concepts and evidence stored in two-layer architecture
**When** Writer Agent queries for a concept (e.g., "RAG")
**Then** the query engine returns:
- **Concept metadata:** concept_id, concept_name, summary, definition, contributors, confidence_score
- **Relations by type:**
  - Prerequisites: Concepts that must be understood first
  - Related: Comparison/alternative/complementary concepts
  - Subtopics: Narrower concepts under this one
  - Extends: Advanced versions of this concept
  - Contradicts: Opposing viewpoints
- **Evidence paragraphs:** Query Postgres by `extracted_concept = 'RAG'`, ordered by importance_score
- **Evidence metadata:** Extract type, keywords, entities, handbook topic

**And** query module `handbook/pipeline/writer_agent/graph_query.py` implements:
- GraphDB Cypher/SPARQL queries for concept + relations
- Postgres queries for evidence paragraphs (via extracted_concept field)
- Join operations (concept → relations → evidence)
- Caching for frequently queried concepts
- Sub-500ms query latency for typical concept

**And** query result format:
```python
{
  "concept": {...},
  "prerequisites": [{concept, relation_metadata, evidence_previews}],
  "related": [{concept, relation_type, evidence_previews}],
  "subtopics": [{concept, handbook_path, evidence_previews}],
  "extends": [{concept, extension_type, evidence_previews}],
  "contradicts": [{concept, explanation, evidence_previews}],
  "evidence": [{paragraph_text, source, page, importance_score, extract_type}]
}
```

**Prerequisites:** Story 1.3 (Concept Layer), Story 3.3 (concept matching)

**Technical Notes:**
- Follow architecture.md Novel Pattern 3: Writer Agent Query (lines 530-579)
- Two-step query: (1) GraphDB for concept + relations, (2) Postgres for evidence
- Evidence linkage via `extracted_concept` field in Evidence Layer
- Example queries in architecture.md (lines 1082-1114)
- Batch queries for efficiency when generating multiple pages
- Consider query result caching (Redis) for performance

---

### Story 4.2: Page Synthesis with Claude Writer Agent

As a **content creator**,
I want **Claude to synthesize handbook pages from graph query results**,
So that **users get coherent, well-cited explanations with full source traceability**.

**Acceptance Criteria:**

**Given** knowledge graph query results for a concept
**When** Writer Agent synthesizes a page
**Then** the generated page follows Concept Page Structure (PRD lines 440-490):
- **Title:** Concept name
- **Summary:** 1-2 sentence definition
- **Dynamic relation blocks** (only non-empty sections):
  - Prerequisites: With "why" explanations and evidence previews
  - Related: With relation type and evidence previews
  - Subtopics: With handbook paths
  - Extends: With extension types
  - Contradicts: With explanations
- **Sources & Commentary:** Reading order suggestions, context for each source
- **Contributors:** Knowledge Team members who curated this concept

**And** synthesis module `handbook/pipeline/writer_agent/page_synthesizer.py` implements:
- Claude 3.5 Sonnet integration (200K context for comprehensive synthesis)
- Synthesis prompts in `handbook/pipeline/writer_agent/synthesis_prompts.py`
- Structured output matching Concept Page format
- Evidence preview format: `"[excerpt]" — [source] [paraphrase/direct/figure]`
- Citation style consistent across all pages
- Cost tracking per page synthesis

**And** synthesis quality requirements:
- No hallucinations (all claims backed by evidence)
- Proper attribution (every fact cited to source)
- Clear "why" explanations for each relation
- Evidence diversity (mix core_summary, examples, counterpoints)
- Appropriate depth for section (Basics vs Advanced)

**And** output is MyST Markdown compatible with Jupyter Book

**Prerequisites:** Story 4.1 (graph query engine)

**Technical Notes:**
- Follow architecture.md Novel Pattern 3: Writer Agent (lines 530-579)
- Claude 3.5 Sonnet: 200K context, superior prose quality, $3-15/1M tokens
- Prompt engineering: Include graph structure, evidence, and output format examples
- Handle conflicting evidence (surface disagreements, don't hide)
- Generate frontmatter: title, date, last_updated, handbook_topic, contributors
- Fallback to Gemini Flash if Claude unavailable
- Human review recommended before first publication (quality gate)

---

### Story 4.3: Image Generation Agent with MCP Server

As a **content creator**,
I want **automated diagram and chart generation for handbook pages**,
So that **visual explanations enhance understanding without manual design work**.

**Acceptance Criteria:**

**Given** a handbook concept needs visual explanation
**When** Image Generation Agent is invoked
**Then** the agent:
- Receives diagram specification (type, content, style)
- Calls Custom MCP Server for image generation
- Receives image file path from MCP Server
- Inserts image reference into markdown file
- Stores image in `handbook-content/_static/images/`
- Updates markdown with proper MyST image syntax

**And** image generation module `handbook/pipeline/image_generation/image_agent.py` implements:
- Custom Agent logic for diagram planning
- MCP client `handbook/pipeline/image_generation/mcp_client.py` for server communication
- Markdown inserter `handbook/pipeline/image_generation/markdown_inserter.py`
- Support for diagram types: flowcharts, architecture diagrams, concept maps, graphs

**And** MCP Server capabilities:
- Generates diagrams from structured specifications
- Returns image files (PNG, SVG formats)
- Configurable via environment variables (MCP_SERVER_URL)

**And** Airflow DAG `handbook/dags/image_generation_dag.py` orchestrates:
- Time-to-time generation (manual trigger or scheduled)
- Batch processing for multiple diagrams
- Image optimization (compression, format conversion)
- Git commit of generated images

**And** images follow naming convention: `{concept-slug}-{diagram-type}.{ext}`

**Prerequisites:** Story 4.2 (page synthesis)

**Technical Notes:**
- Follow architecture.md Novel Pattern for Image Generation (lines 426-433)
- Custom Agent + MCP Server architecture (decoupled design)
- MCP SDK for server communication
- Image types: Mermaid diagrams, D3.js charts, custom illustrations
- Alt text generation for accessibility
- Consider diagram versioning (update when content changes)
- Future: Auto-detect when diagrams needed based on content

---

### Story 4.4: Patchnote Aggregation System

As a **content maintainer**,
I want **centralized tracking of all Basics/Advanced page changes**,
So that **users can see what's new without checking individual pages**.

**Acceptance Criteria:**

**Given** Writer Agent generates or updates a Basics/Advanced page
**When** the page is committed to GitHub
**Then** patchnote aggregator:
- Prepends entry to `handbook-content/patchnote.md`
- Format: `- [YYYY-MM-DD] Updated [Concept Name]: [summary of changes]`
- Summary generated by comparing old vs new content (if update) or listing key sections (if new)
- Chronological order (newest first)
- Categories changes: New page, Major update, Minor update, Corrections

**And** aggregation module `handbook/pipeline/writer_agent/patchnote_aggregator.py` implements:
- Diff detection (git diff for existing pages)
- Change summarization (LLM-generated summary of what changed)
- Patchnote formatting and prepending
- Deduplication (don't duplicate if re-generating same page)

**And** patchnote.md structure:
```markdown
# Handbook Updates

## 2025-12-06
- [New] Added concept: "Retrieval-Augmented Generation" - Core RAG patterns and implementations
- [Major] Updated "Prompt Caching" - Added Claude prompt caching details and cost analysis

## 2025-11-29
- [Minor] Updated "Fine-Tuning" - Fixed typo in LoRA explanation
```

**And** patchnote updates are atomic (included in same commit as page changes)

**Prerequisites:** Story 4.2 (page synthesis)

**Technical Notes:**
- Follow architecture.md Patchnote Aggregator (lines 559-562)
- Use git diff to detect changes (compare HEAD vs new content)
- LLM summarization for change descriptions (Claude or GPT-4)
- Prepend to file (don't append) for reverse chronological order
- Track in Evidence Layer: concept_name, change_type, change_date
- Monthly review: Archive old patchnotes (keep last 6 months visible)

---

### Story 4.5: Writer Agent Airflow DAG

As a **automation engineer**,
I want **end-to-end DAG orchestrating graph query → synthesis → image generation → patchnote → GitHub commit**,
So that **handbook page generation is automated and monitored**.

**Acceptance Criteria:**

**Given** concepts exist in knowledge graph with sufficient evidence
**When** Writer Agent DAG runs (monthly trigger after concept review)
**Then** the pipeline executes:
1. **Concept selection:** Identify concepts ready for page generation (new or updated)
2. **Graph query:** Load concept + relations + evidence for each
3. **Page synthesis:** Claude generates markdown following Concept Page structure
4. **Image generation:** Generate diagrams if specified (optional task)
5. **Patchnote update:** Aggregate changes to patchnote.md
6. **GitHub commit:** Commit generated pages + images + patchnote
7. **Metrics tracking:** Log pages generated, tokens used, costs, duration

**And** Airflow DAG `handbook/dags/writer_agent_dag.py` implements:
- Monthly scheduled execution (2nd Saturday after Knowledge Team concept review)
- Manual trigger for ad-hoc generation
- Parallel processing (generate multiple pages concurrently)
- Error handling with retry logic
- Human review gate (optional - approve before commit)
- Cost monitoring and alerts

**And** DAG supports:
- Dry-run mode (generate locally, don't commit)
- Single-concept mode (test one page generation)
- Batch mode (generate all pending concepts)
- Rollback capability (revert bad generations)

**And** monitoring shows:
- Pages generated this run
- Total cost (LLM tokens + API calls)
- Generation quality scores
- Failed concepts (for manual review)

**Prerequisites:** Stories 4.1-4.4 (all Writer Agent components)

**Technical Notes:**
- Follow architecture.md Writer Agent DAG structure (lines 206-208)
- Parallel task execution for scalability (Airflow parallelism)
- Use Airflow XCom for concept IDs, Postgres for large data
- Implement checkpoint/resume for long-running batches
- Alert if costs exceed budget or quality issues detected
- Integration with GitHub committer (story 4.6)

---

### Story 4.6: Jupyter Book Theme and Layout Customization

As a **UI/UX designer**,
I want **Jupyter Book styled with custom branding and handbook-specific layouts**,
So that **the handbook has professional, distinct visual identity**.

**Acceptance Criteria:**

**Given** basic Jupyter Book is configured
**When** I apply custom styling
**Then** the handbook includes:
- **Brand identity:**
  - Custom logo in `_static/logo.svg`
  - Brand colors (primary, secondary, accent) in `_config.yml`
  - Custom fonts (headers, body, code)
  - Favicon in `_static/favicon.ico`
- **Layout enhancements:**
  - Card layouts for Newly Discovered section (sphinx-design)
  - Collapsible sections for archived news (sphinx-togglebutton)
  - Code syntax highlighting with appropriate theme
  - Responsive design (mobile, tablet, desktop)
- **Custom CSS:** `_static/custom.css` for additional styling
- **Footer:** Copyright, license, contribution link, "Last updated" timestamp

**And** styling follows accessibility standards:
- WCAG 2.1 AA color contrast ratios
- Keyboard navigation support
- Screen reader compatibility
- Semantic HTML structure

**And** theme configuration in `_config.yml`:
```yaml
html:
  use_edit_page_button: true
  use_repository_button: true
  use_issues_button: true
sphinx:
  config:
    html_theme_options:
      logo: "_static/logo.svg"
      primary_color: "#your-brand-color"
```

**And** style guide documented in `STYLE_GUIDE.md`

**Prerequisites:** Story 1.1 (Jupyter Book initialization)

**Technical Notes:**
- Follow architecture.md theme customization (lines 849-855)
- PyData Sphinx Theme (Jupyter Book default) is highly customizable
- sphinx-design for card grids (Newly Discovered section)
- sphinx-togglebutton for collapsible content
- Test on Chrome, Firefox, Safari, Edge (last 2 major versions)
- Mobile-first responsive design
- Consider dark mode support (future enhancement)

---

### Story 4.7: Automated GitHub Pages Deployment

As a **DevOps engineer**,
I want **Jupyter Book automatically built and deployed on every content commit**,
So that **handbook updates go live immediately without manual intervention**.

**Acceptance Criteria:**

**Given** content is committed to main branch (Newly Discovered weekly OR Basics/Advanced monthly)
**When** GitHub Actions deployment workflow triggers
**Then** the deployment process:
1. Checks out repository
2. Installs Jupyter Book dependencies (with caching)
3. Builds handbook (`jupyter-book build handbook-content/`)
4. Validates build (no errors, HTML generated)
5. Deploys to gh-pages branch (GitHub Pages)
6. Deployment completes within 10 minutes

**And** `.github/workflows/deploy.yml` implements:
- Trigger on push to main branch (any content changes)
- Dependency caching (pip cache for 30s installs vs 2min)
- Build validation (exit on error, don't deploy broken builds)
- Deployment using `peaceiris/actions-gh-pages` action
- Deployment status badge in README.md

**And** deployment is zero-downtime:
- Previous version stays live until new build succeeds
- Failed builds don't update gh-pages branch
- Rollback via git revert on main branch

**And** post-deployment actions:
- Slack notification with deployment status
- Update deployment timestamp in Notion (optional)
- Clear CDN cache if needed (GitHub Pages CDN automatic)

**Prerequisites:** Story 1.6 (CI/CD pipeline), Story 4.5 (Writer Agent commits)

**Technical Notes:**
- Follow architecture.md Deployment Architecture (lines 1486-1537)
- GitHub Pages serves from gh-pages branch
- peaceiris/actions-gh-pages handles branch management
- Cache strategy: `actions/cache` for pip dependencies
- Build timeout: 10 minutes max (fail fast)
- Incremental builds not supported in Jupyter Book 1.0.4 (full rebuild)
- Future optimization: Investigate Jupyter Book caching mechanisms

---

## Epic 5: Community & Quality Operations

**Goal:** Enable community contributions via GitHub PR workflow while maintaining operational excellence through monitoring, link validation, error correction, and two-layer database backup.

**Value:** This epic delivers sustained "Confidence" - users trust the handbook through community contributions, quality controls, and operational reliability.

---

### Story 5.1: GitHub PR Workflow for Content Contributions

As a **community contributor**,
I want **clear process to submit handbook content via GitHub pull requests**,
So that **I can share knowledge while maintainers ensure quality standards**.

**Acceptance Criteria:**

**Given** I want to contribute handbook content
**When** I follow the contribution workflow
**Then** I can:
- Fork the handbook repository
- Create feature branch for my contribution
- Edit or create markdown files following templates
- Submit pull request with description
- See automated checks run (linting, link validation, frontmatter validation)
- Receive feedback from maintainers
- Iterate on changes until approved

**And** `.github/pull_request_template.md` includes:
- PR checklist (frontmatter complete, links valid, follows style guide)
- Contribution type (new page, update, correction, image)
- Testing notes (how contributor verified changes)

**And** automated checks in CI workflow validate:
- Markdown syntax correct (markdown-lint)
- Links are valid (no 404s) - optional on PR, required weekly
- Frontmatter complete (title, date, category, tags present)
- File naming conventions followed (lowercase, hyphens, no spaces)
- Jupyter Book builds successfully

**And** `.github/ISSUE_TEMPLATE/` includes:
- `report-error.md` - Report content errors
- `submit-source.md` - Submit URLs for Auto-News monitoring

**Prerequisites:** Story 1.6 (CI/CD pipeline)

**Technical Notes:**
- Follow architecture.md community contribution patterns
- Use markdown-lint in CI for style enforcement
- linkchecker or custom script for link validation
- CODEOWNERS file for auto-assignment by section (e.g., `basics/**` → @basics-team)
- PR review requires 1 maintainer approval minimum
- Clear merge policy: Squash commits for cleaner history
- Consider "good first issue" labels for new contributors

---

### Story 5.2: Content Templates and Style Guide

As a **new contributor**,
I want **clear templates and style guidance for different content types**,
So that **my contributions match handbook standards without guesswork**.

**Acceptance Criteria:**

**Given** I'm creating new content
**When** I reference contribution documentation
**Then** I find templates for:
- **Basics/Advanced concept page** (generated by Writer Agent, but editable)
- **Newly Discovered item** (category-specific templates from Story 2.4)
- **Frontmatter requirements:**
  ```yaml
  ---
  title: "Concept Name"
  date: 2025-12-06
  last_updated: 2025-12-06
  category: basics|advanced|newly-discovered
  tags: [rag, prompting, llm]
  contributors: [github_username]
  ---
  ```

**And** `STYLE_GUIDE.md` documents:
- **Voice and tone:** Clear, practical, professional (avoid hype, be objective)
- **Writing style:** Use examples, explain trade-offs, cite sources
- **Code examples:** Properly formatted with syntax highlighting and comments
- **Citations:** How to cite sources (inline links, evidence preview format)
- **Images:** Alt text requirements, file naming, placement
- **Cross-linking:** When and how to link to other handbook sections

**And** `CONTRIBUTING.md` includes:
- Step-by-step PR workflow
- How to run local Jupyter Book build for preview
- How to report errors or suggest improvements
- Expectations for PR response time (48 hours first response)

**And** templates in `/templates/` directory:
- `basics-template.md`
- `advanced-template.md`
- `newly-discovered-template.md`

**Prerequisites:** Story 5.1 (PR workflow)

**Technical Notes:**
- Style guide should reference PRD's concept page structure (lines 440-490)
- Examples of "good" vs "needs improvement" content
- Link to external resources (Chicago Manual of Style, technical writing guides)
- Consider automated style checking (vale, write-good) in future
- Keep templates in sync with Writer Agent output format

---

### Story 5.3: Automated Link Validation and Monitoring

As a **handbook maintainer**,
I want **automated detection of broken links and content issues**,
So that **users don't encounter errors and handbook stays reliable**.

**Acceptance Criteria:**

**Given** handbook is published with external links
**When** link validation runs (weekly via GitHub Actions)
**Then** the system:
- Checks all external URLs (HTTP status codes, timeout handling)
- Identifies broken links (404, 500, timeout)
- Checks internal cross-references (handbook page → handbook page)
- Validates image URLs and accessibility
- Creates GitHub issues for broken links with "broken-link" label

**And** `.github/workflows/link-check.yml` implements:
- Weekly scheduled run (Sunday night after weekly publication)
- On-demand manual trigger
- Uses linkchecker or custom script
- Respects robots.txt and rate limits
- Retry logic for temporary failures

**And** issues created include:
- Page containing broken link (file path and line number)
- Link URL and error type (404, 500, timeout, SSL error)
- Suggested action (update link, use archive.org, remove, mark deprecated)
- Priority label (critical for core content, low for archived news)

**And** validation whitelist for known-flaky domains

**Prerequisites:** Story 4.7 (deployment)

**Technical Notes:**
- linkchecker tool or custom Python script with requests library
- Handle temporary failures (retry 3 times with backoff)
- Whitelist: domains known to block crawlers but work in browsers
- Consider using Internet Archive Wayback Machine for dead links
- Pre-publish validation in PR checks (subset of links only for speed)
- Weekly full validation post-publish

---

### Story 5.4: Error Correction Workflow

As a **handbook user or contributor**,
I want **easy way to report errors and see them corrected quickly**,
So that **handbook stays accurate and I can trust the content**.

**Acceptance Criteria:**

**Given** I discover an error in handbook content
**When** I report it via GitHub issue
**Then** I can:
- Create issue using "Report Error" template (`.github/ISSUE_TEMPLATE/report-error.md`)
- Describe error: page location, what's wrong, suggested fix (optional)
- See issue triaged by maintainers with priority label
- Track status and resolution
- Receive notification when fixed

**And** error correction workflow:
- **Critical errors** (factual inaccuracies, security issues): Fixed within 24 hours
- **High priority** (outdated content, major typos): Fixed within 7 days
- **Medium priority** (clarity improvements, formatting): Fixed within 30 days
- **Low priority** (style tweaks, minor formatting): Batched with other updates

**And** issue template includes:
- Page URL or file path
- Error description
- Suggested correction (optional)
- Error type (factual, outdated, typo, formatting, other)

**And** fix process:
- Create fix branch from main
- Make correction with proper commit message referencing issue
- Update `last_updated` date in frontmatter
- Submit PR (fast-track for critical errors)
- Close issue when deployed

**And** thank reporters in PR description (community engagement)

**Prerequisites:** Story 5.1 (PR workflow)

**Technical Notes:**
- Issue labels: error-critical, error-high, error-medium, error-low
- CODEOWNERS handles auto-assignment by section
- Fast-track process for critical: Direct commit to main (skip PR review)
- Document triage criteria in CONTRIBUTING.md
- Track error rates (errors reported / pages published) as quality metric
- Monthly review of common error patterns to improve processes

---

### Story 5.5: Two-Layer Database Backup Strategy

As a **operations engineer**,
I want **automated backup of both Evidence and Concept layers with retention policies**,
So that **knowledge graph data is protected and recoverable from disasters**.

**Acceptance Criteria:**

**Given** the two-layer architecture is operational
**When** backup process runs (daily for Postgres, weekly for GraphDB)
**Then** backups include:
- **Evidence Layer (Postgres RDS):**
  - Automated RDS snapshots (daily, 30-day retention)
  - Manual snapshots before major schema changes
  - Point-in-time recovery enabled (7-day window)
- **Concept Layer (GraphDB):**
  - Weekly export to JSON/RDF format
  - Stored in S3 with versioning enabled
  - 60-day retention (8 weekly snapshots + monthly archives)
- **Vector DB (pgvector):** Included in Postgres RDS backups

**And** backup script `scripts/backup_databases.py` implements:
- GraphDB export via API or CLI
- S3 upload with encryption at rest
- Verification: Test restore on staging environment monthly
- Backup metadata logged (timestamp, size, status)

**And** restore procedures documented:
- Postgres: RDS snapshot restore (documented in runbook)
- GraphDB: Import from S3 backup file
- Test restore annually (disaster recovery drill)

**And** backup monitoring:
- Alert if backup fails (email + Slack)
- Weekly backup health report
- Storage cost tracking (S3 costs)

**Prerequisites:** Stories 1.2 (Evidence Layer), 1.3 (Concept Layer)

**Technical Notes:**
- Follow architecture.md backup strategy references
- RDS automated backups: Enable in AWS console, free within retention window
- GraphDB backup: Use native export functionality or pg_dump equivalent
- S3 lifecycle policies for cost optimization (transition to Glacier after 60 days)
- Encryption: Server-side encryption (SSE-S3) for S3 buckets
- IAM roles for backup script (least privilege access)
- Document RPO (Recovery Point Objective): 24 hours, RTO (Recovery Time Objective): 4 hours

---

### Story 5.6: Operational Monitoring and Alerting

As a **operations engineer**,
I want **comprehensive monitoring of all pipeline components with actionable alerts**,
So that **issues are detected early and resolved before users are impacted**.

**Acceptance Criteria:**

**Given** the handbook platform is operational
**When** monitoring systems run
**Then** they track:
- **Pipeline health:**
  - Airflow DAG success rate (all 4 DAGs: notion_backup, evidence_ingestion, writer_agent, weekly_publish)
  - Task duration and failures
  - Dead-letter queue size (failed_items table)
- **Database health:**
  - Postgres: Connection pool usage, query latency, storage usage
  - GraphDB: Query latency, node count, relationship count
  - pgvector: Index performance, embedding storage
- **Deployment health:**
  - GitHub Actions workflow success rate
  - Jupyter Book build duration
  - GitHub Pages uptime
- **API health:**
  - LLM provider response times (Claude, OpenAI, Gemini)
  - Rate limit proximity (% of limit used)
  - API costs (daily and monthly tracking)

**And** alerting rules:
- **Critical (immediate):**
  - Pipeline failure (Airflow DAG failed)
  - Database connection failures
  - Deployment failure (GitHub Actions workflow failed)
  - Site downtime (GitHub Pages unavailable)
- **High (within 1 hour):**
  - API rate limit approaching (>80% of limit)
  - High API costs (>$50/day)
  - Slow queries (>5s latency)
- **Medium (within 24 hours):**
  - Weekly publication missed (Sunday check)
  - Backup failure
  - High dead-letter queue size (>100 items)

**And** alerting channels:
- Email for non-urgent issues and weekly summaries
- Slack webhook for moderate and critical issues
- PagerDuty for critical production incidents (optional, future)

**And** monitoring dashboard (Airflow UI + optional custom dashboard):
- Pipeline status overview
- Cost tracking (LLM tokens, API calls)
- Quality metrics (pages generated, approval rates)
- System health (database, API, deployment)

**Prerequisites:** Stories 2.6 (publication monitoring), 3.6 (evidence ingestion monitoring)

**Technical Notes:**
- Use AWS CloudWatch for RDS and infrastructure monitoring
- Airflow built-in monitoring + alerting for DAGs
- Store metrics in `pipeline_runs` table for historical tracking
- Email alerts via SMTP (Gmail, SendGrid, or AWS SES)
- Slack incoming webhooks for real-time notifications
- Define SLOs (Service Level Objectives): 99.5% uptime, <2s page load, <24h content freshness
- Runbooks document response procedures for each alert type

---

## Epic Breakdown Summary

### Overview

This epic breakdown transforms the cherry-in-the-haystack PRD and updated architecture.md into **33 implementable stories** organized across **5 epics**. The breakdown reflects the novel two-layer knowledge architecture and follows BMad Method principles: vertically sliced stories, BDD acceptance criteria, clear dependencies, and sizing optimized for 200k context dev agents.

### Epic Statistics

| Epic | Stories | Focus | Phase | Dependencies |
|------|---------|-------|-------|--------------|
| Epic 1: Foundation & Core Infrastructure | 7 | Two-layer architecture setup | MVP (Sequential) | None (first epic) |
| Epic 2: Newly Discovered Pipeline | 6 | Notion-primary weekly publication | MVP (Sequential) | Epic 1 |
| Epic 3: Evidence Ingestion & Knowledge Graph | 7 | Two-layer knowledge system | MVP (Sequential) | Epics 1-2 |
| Epic 4: Writer Agent & Publication | 7 | Synthesis + image generation | MVP (Sequential) | Epics 1-3 |
| Epic 5: Community & Quality Operations | 6 | Contributions + operations | Growth (Parallel) | Epic 4 |
| **Total** | **33 stories** | | | |

### Delivery Timeline

**Phase 1: Core MVP (Epics 1-4) - Sequential Execution**
```
Epic 1 (Foundation: Two-Layer DB)
  ↓
Epic 2 (Newly Discovered: Notion → GitHub)
  ↓
Epic 3 (Knowledge Graph: Evidence → Concepts)
  ↓
Epic 4 (Writer Agent: Graph → Pages)
  ↓
MVP LAUNCH ✓
```

**Phase 2: Growth & Quality (Epic 5) - Parallel to Epic 4 Completion**
```
Epic 5 (Community + Operations)
  ↓
Full Platform Maturity ✓
```

### Architecture Coverage

**Novel Patterns Implemented:**
- ✅ **Pattern 1: Two-Layer Architecture** (Epic 3) - Evidence Layer (Postgres) ↔ Concept Layer (GraphDB) with normalized concepts
- ✅ **Pattern 2: Notion as Primary** (Epic 2) - One-way backup flow, NOT bidirectional sync
- ✅ **Pattern 3: Writer Agent Query** (Epic 4) - Graph query → synthesis with full traceability
- ✅ **Image Generation via MCP** (Epic 4) - Custom Agent + MCP Server for diagrams

**PRD Requirements Coverage:**
- ✅ **FR.1: Newly Discovered Pipeline** → Epic 2 (6 stories)
- ✅ **FR.2: Evidence Ingestion** → Epic 3 Stories 3.1-3.5 (5 stories)
- ✅ **FR.3: Concept Normalization** → Epic 3 Stories 3.2-3.3 (2 stories)
- ✅ **FR.4: Writer Agent Synthesis** → Epic 4 Stories 4.1-4.2 (2 stories)
- ✅ **FR.5: Image Generation** → Epic 4 Story 4.3 (1 story)
- ✅ **FR.6: Patchnote Aggregation** → Epic 4 Story 4.4 (1 story)
- ✅ **FR.7: Community Contributions** → Epic 5 Stories 5.1-5.2 (2 stories)
- ✅ **FR.8: Operational Excellence** → Epic 5 Stories 5.3-5.6 (4 stories)

### Product Magic Delivered

- 🌟 **Clarity** - Epic 3 builds two-layer knowledge graph enabling intelligent, traceable synthesis
- 🌟 **Confidence** - Epic 5 maintains quality through monitoring, validation, and community contributions
- 🌟 **Speed** - Epic 2 enables weekly updates with Notion→GitHub pipeline (48-hour approval→publish)
- 🌟 **Community Intelligence** - Epic 5 GitHub PR workflow makes knowledge compound instead of fade

### Story Quality Standards

All stories follow these standards:
- ✅ **BDD Format:** Given/When/Then acceptance criteria
- ✅ **Vertical Slicing:** Complete functionality across all layers
- ✅ **Clear Prerequisites:** Only backward dependencies (no forward references)
- ✅ **Single-Session Sizing:** Completable by one dev agent in one focused session
- ✅ **Technical Guidance:** Implementation notes reference architecture.md line numbers
- ✅ **User Value:** Clear "So that..." statements connecting to user needs

### Key Dependencies

**Critical Path (MVP - Epics 1-4):**
1. Story 1.1 (Project Setup) → Enables all other work
2. Story 1.2 (Evidence Layer) → Required for all evidence storage
3. Story 1.3 (Concept Layer) → Required for knowledge graph
4. Story 1.4 (pgvector) → Required for semantic search
5. Story 1.5 (Auto-News Adaptation) → Enables Newly Discovered pipeline
6. Story 2.1 (Notion Primary) → Establishes review workflow
7. Story 3.2 (Concept Extraction) → Core of two-layer architecture
8. Story 3.3 (Concept Matching) → Prevents graph fragmentation
9. Story 4.1 (Graph Query) → Enables Writer Agent
10. Story 4.2 (Page Synthesis) → Generates handbook content

**Parallel Work Opportunities:**
- Epic 1: Stories 1.6 (CI/CD) and 1.7 (Local Dev) can overlap with database setup
- Epic 2: Stories 2.3 (Category Matching) and 2.4 (Formatting) can partially overlap
- Epic 3: Stories 3.4 (Vectorization) and 3.5 (Metadata Enrichment) can run in parallel after 3.3
- Epic 4: Stories 4.6 (Theme) can run in parallel with 4.1-4.5 (Writer Agent)
- Epic 5: All 6 stories can begin once Epic 4 completes (parallel to Epic 4 finalization)

### Technical Innovations

**Two-Layer Architecture Benefits:**
- Normalized concepts prevent knowledge fragmentation
- Evidence paragraphs maintain full source traceability
- Writer Agent queries graph for structure, Postgres for evidence
- Concept relations enable intelligent page synthesis
- Soft deduplication via sampling_weight (no data deletion)

**Notion-as-Primary Benefits:**
- Knowledge Team works in familiar interface
- No custom backend UI needed (cost savings)
- One-way backup maintains data ownership
- Simple integration (Auto-News writes directly to Notion)

**Writer Agent Design Benefits:**
- Claude 200K context for comprehensive synthesis
- Evidence preview format ensures proper citation
- Patchnote aggregation tracks all changes centrally
- Image generation via MCP decouples concerns

### Cost Projections

**Infrastructure (Monthly):**
- Amazon RDS PostgreSQL 16 (db.t3.small): ~$25
- GraphDB (self-hosted on EC2 t3.small): ~$15
- S3 backups: ~$5
- GitHub Pages: Free
- **Total Infrastructure: ~$45/month**

**LLM API Usage (Monthly estimates for moderate usage):**
- Claude 3.5 Sonnet (concept extraction, synthesis, scoring): ~$50-150
- OpenAI embeddings (text-embedding-3-small): ~$5-20
- Gemini Flash (fallback): ~$10-30
- **Total LLM: ~$65-200/month**

**Total Monthly Cost: ~$110-245/month** (scales with content volume)

### Success Metrics Alignment

**PRD Success Criteria Coverage:**

| Metric | Epic Coverage | Target |
|--------|---------------|--------|
| 50K monthly users within 6 months | Epic 4 (publication), Epic 5 (community) | Tracked via analytics |
| Weekly content updates | Epic 2 (Newly Discovered pipeline) | Sunday publication cadence |
| 48-hour approval→publish | Epic 2 (Notion workflow) | Automated tracking |
| 90%+ human approval rating | Epic 2 (scoring), Epic 5 (quality) | Tracked in Notion |
| 95% topic coverage | Epic 3 (concept graph) | Concept count vs taxonomy |

### Next Steps

**After Epic Breakdown Approval:**

1. **Validate Architecture Decisions** (if needed):
   - Run `/bmad:bmm:workflows:architecture` to refine technical choices
   - Confirm GraphDB vs Neo4j decision
   - Validate Notion API limitations for scale

2. **Solutioning Gate Check**:
   - Run `/bmad:bmm:workflows:solutioning-gate-check` to ensure PRD + architecture + epics alignment
   - Verify no gaps or contradictions

3. **Begin Implementation** (Phase 4):
   - Run `/bmad:bmm:workflows:sprint-planning` to set up sprint tracking
   - Start with Epic 1 Story 1.1 (Foundation Setup)
   - Use `/bmad:bmm:workflows:create-story` for detailed story implementation plans
   - Execute with `/bmad:bmm:workflows:dev-story`
   - Review with `/bmad:bmm:workflows:code-review`

---

**Epic breakdown complete and validated against updated architecture.md**

**Document saved:** `C:\Users\Hankeol\Desktop\Dev\cherry-in-the-haystack\docs\epics.md`

**Epic Count:** 5 epics
**Story Count:** 33 stories (MVP: 27 stories | Growth: 6 stories)
**Novel Patterns:** 3 architectural innovations fully covered
**PRD Coverage:** 100% functional requirements mapped

