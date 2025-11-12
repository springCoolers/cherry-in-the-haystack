# Epic Technical Specification: Foundation & Core Infrastructure

Date: 2025-11-12
Author: HK
Epic ID: epic-1
Status: Draft

---

## Overview

Epic 1 establishes the foundational technical infrastructure that transforms the existing Auto-News content curation tool into The LLM Engineering Handbook platform. This epic focuses on creating a solid, scalable foundation that enables all subsequent development work, including content ingestion pipelines, AI synthesis, and automated publication.

The epic adapts proven Auto-News infrastructure (Apache Airflow for orchestration, event-driven data pipelines) while introducing new handbook-specific components: PostgreSQL database with pgvector extension for content and embeddings storage, Jupyter Book for professional documentation site generation, and modern Python tooling (Poetry, Ruff, Loguru) following 2024 best practices.

This foundational work directly supports the PRD's success criteria by enabling weekly automated updates (Speed), establishing the infrastructure for comprehensive content coverage (Clarity through MECE taxonomy), and creating a reliable platform that contributors can trust (Confidence through 99.5% uptime).

## Objectives and Scope

**In Scope for Epic 1:**

- Repository structure and development environment setup with modern Python tooling
- PostgreSQL database (Amazon RDS) with schemas for content storage, scoring, and review tracking
- pgvector extension setup for semantic deduplication and similarity search
- Auto-News engine adaptation to target LLM-focused content sources instead of general tech news
- GitHub Actions CI/CD pipeline for automated testing, linting, and Jupyter Book deployment
- Jupyter Book configuration with 3-section structure (Basics, Advanced, Newly Discovered)
- Development environment documentation enabling new contributors to set up in under 30 minutes

**Out of Scope for Epic 1:**

- Content ingestion from specific sources (Epic 2)
- AI-powered scoring and synthesis engines (Epic 2-3)
- Notion review workflow integration (Epic 2)
- Actual content creation or seeding (Epic 3-4)
- Community contribution workflows (Epic 5)
- Production monitoring and alerting systems (Epic 6)

**Success Criteria:**

- Developer can clone repo, run setup script, and have working local environment in <30 minutes
- Postgres database operational with all required schemas and pgvector indexes
- CI/CD pipeline runs automatically on every PR (linting, tests, builds)
- Jupyter Book builds successfully locally and via GitHub Actions
- Foundation supports 1000+ handbook pages, 50K monthly visitors (per architecture NFRs)

## System Architecture Alignment

Epic 1 implements the core architectural decisions defined in architecture.md:

**Database Layer (ADR-001, ADR-002):**
- Amazon RDS PostgreSQL 16 (db.t3.small, ~$25/month) provides relational storage
- pgvector 0.8.0 extension adds vector storage capabilities for embeddings
- Single database handles both relational and vector data, simplifying architecture

**Pipeline Foundation (Brownfield Constraint):**
- Keeps existing Apache Airflow orchestration from Auto-News
- Adapts Auto-News operators to target LLM-focused sources
- Establishes new handbook/ directory separate from auto-news-engine/ codebase

**Publication Layer (ADR-004):**
- Jupyter Book 1.0.4 for static site generation (professional docs out-of-the-box)
- PyData Sphinx Theme provides responsive, accessible default styling
- GitHub Pages deployment ($0 cost, 99.5% uptime via GitHub's SLA)

**Development Tooling (From Python Pipeline Starter):**
- Poetry for dependency management (pyproject.toml modern standard)
- Ruff for linting/formatting (replaces isort, flake8, pylint - 10-100x faster)
- Loguru for structured logging with JSON output
- pytest + pytest-cov for testing with 70% coverage target

**Critical Integration Points:**
- Airflow ↔ PostgreSQL: DAGs will read/write content, embeddings, review status
- Python Pipeline ↔ pgvector: Similarity search for deduplication (<100ms per NFR-P3)
- GitHub Actions ↔ Jupyter Book: Automated build and deploy on main branch commits
- Local Dev: Docker Compose provides Postgres + pgvector matching production

## Detailed Design

### Services and Modules

This epic establishes the foundational module structure that all subsequent epics will build upon:

| Module | Responsibility | Key Components | Owner/Story |
|--------|---------------|----------------|-------------|
| **handbook/config/** | Application configuration and settings | - settings.py (environment variables)<br>- logging_config.py (Loguru setup)<br>- llm_config.py (multi-provider setup for future) | Story 1.1, 1.7 |
| **handbook/db_connection/** | Database connectivity and operations | - postgres.py (RDS connection pooling)<br>- pgvector.py (vector operations wrapper) | Story 1.2, 1.3 |
| **auto-news-engine/** | Existing Auto-News codebase (adapted) | - dags/ (Airflow orchestration)<br>- operators/ (reusable ingestion logic)<br>- config/ (source configuration) | Story 1.4 |
| **handbook-content/** | Jupyter Book publication layer | - _config.yml (site configuration)<br>- _toc.yml (3-section structure)<br>- _static/ (custom CSS, logo) | Story 1.6 |
| **.github/workflows/** | CI/CD automation | - ci.yml (lint, test, type check)<br>- deploy.yml (Jupyter Book build & deploy) | Story 1.5 |
| **tests/** | Testing infrastructure | - unit/ (isolated tests)<br>- integration/ (DB, API tests)<br>- fixtures/ (sample data) | Story 1.7 |
| **scripts/** | Operational scripts | - setup_pgvector.sql (DB init)<br>- backup_vector_db.py (maintenance) | Story 1.2, 1.3 |

### Data Models and Contracts

**PostgreSQL Schema (Story 1.2):**

```sql
-- Content ingestion table
CREATE TABLE content_items (
  id BIGSERIAL PRIMARY KEY,
  source TEXT NOT NULL,              -- 'twitter', 'discord', 'github', 'rss'
  source_url TEXT NOT NULL,
  title TEXT,
  raw_text TEXT NOT NULL,
  publication_date TIMESTAMPTZ,
  category TEXT,                     -- 'model-updates', 'framework-updates', etc.
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for query performance
CREATE INDEX idx_content_source ON content_items(source);
CREATE INDEX idx_content_category ON content_items(category);
CREATE INDEX idx_content_created_at ON content_items(created_at DESC);

-- Embeddings table with pgvector extension
CREATE TABLE embeddings (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  chunk_hash TEXT NOT NULL,          -- SHA256 of chunk text (for dedup)
  embedding vector(1536),            -- pgvector type, OpenAI text-embedding-3-small
  chunk_text TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- pgvector index for similarity search (Story 1.3)
CREATE INDEX idx_embeddings_vector ON embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);  -- Optimized for 100K vectors

CREATE UNIQUE INDEX idx_embeddings_chunk_hash ON embeddings (chunk_hash);

-- AI scoring results table
CREATE TABLE content_scores (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE CASCADE,
  score INTEGER CHECK (score BETWEEN 1 AND 5),
  reasoning TEXT,
  provider TEXT,                     -- 'openai', 'gemini'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Human review status table
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
  frontmatter JSONB,                 -- {title, date, category, tags, source_url}
  target_path TEXT,                  -- e.g. 'newly-discovered/model-updates/2025-11-08-gpt45.md'
  published BOOLEAN DEFAULT FALSE,
  published_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Dead-letter queue for failed pipeline items
CREATE TABLE failed_items (
  id BIGSERIAL PRIMARY KEY,
  content_id BIGINT REFERENCES content_items(id) ON DELETE SET NULL,
  stage TEXT,                        -- 'deduplication', 'scoring', 'synthesis'
  failure_reason TEXT,
  attempt_count INTEGER DEFAULT 1,
  last_attempted TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Python Data Models (Story 1.7):**

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class ContentItem:
    """Represents raw ingested content."""
    id: Optional[int]
    source: str
    source_url: str
    title: Optional[str]
    raw_text: str
    publication_date: Optional[datetime]
    category: Optional[str]
    created_at: datetime
    updated_at: datetime

@dataclass
class Embedding:
    """Represents vector embedding of content chunk."""
    id: Optional[int]
    content_id: int
    chunk_hash: str
    embedding: list[float]  # 1536 dimensions
    chunk_text: str
    created_at: datetime

@dataclass
class ContentScore:
    """AI quality score for content item."""
    id: Optional[int]
    content_id: int
    score: int  # 1-5
    reasoning: str
    provider: str
    created_at: datetime
```

### APIs and Interfaces

**Database Connection Interface (Story 1.2):**

```python
# handbook/db_connection/postgres.py
from contextlib import contextmanager
from psycopg3.pool import ConnectionPool
from handbook.config.settings import DATABASE_URL

class PostgresConnection:
    """PostgreSQL connection manager with pooling."""

    def __init__(self):
        self.pool = ConnectionPool(
            conninfo=DATABASE_URL,
            min_size=5,
            max_size=20,
            timeout=10.0
        )

    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        conn = self.pool.getconn()
        try:
            with conn.transaction():
                yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            self.pool.putconn(conn)

    def execute_query(self, query: str, params: tuple = ()):
        """Execute query and return results."""
        with self.transaction() as conn:
            cursor = conn.execute(query, params)
            return cursor.fetchall()
```

**pgvector Operations Interface (Story 1.3):**

```python
# handbook/db_connection/pgvector.py
from typing import List, Tuple

class PgVectorOperations:
    """pgvector similarity search operations."""

    def __init__(self, db_connection: PostgresConnection):
        self.db = db_connection

    def insert_embedding(self, content_id: int, chunk_hash: str,
                        embedding: List[float], chunk_text: str) -> int:
        """Insert embedding into vector database."""
        query = """
        INSERT INTO embeddings (content_id, chunk_hash, embedding, chunk_text)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (chunk_hash) DO NOTHING
        RETURNING id
        """
        result = self.db.execute_query(
            query,
            (content_id, chunk_hash, embedding, chunk_text)
        )
        return result[0][0] if result else None

    def find_similar(self, embedding: List[float],
                    threshold: float = 0.85,
                    limit: int = 10) -> List[Tuple[int, float]]:
        """Find similar embeddings using cosine similarity."""
        query = """
        SELECT content_id, 1 - (embedding <=> %s::vector) AS similarity
        FROM embeddings
        WHERE 1 - (embedding <=> %s::vector) > %s
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """
        results = self.db.execute_query(
            query,
            (embedding, embedding, threshold, embedding, limit)
        )
        return [(row[0], row[1]) for row in results]
```

**Jupyter Book Configuration (Story 1.6):**

```yaml
# handbook-content/_config.yml
title: The LLM Engineering Handbook
author: cherry-in-the-haystack contributors
logo: _static/logo.svg

execute:
  execute_notebooks: off

repository:
  url: https://github.com/your-org/cherry-in-the-haystack
  branch: main

html:
  use_repository_button: true
  use_issues_button: true
  use_edit_page_button: true

sphinx:
  extra_extensions:
    - sphinx_design
    - sphinx_togglebutton
    - sphinxext.opengraph
  config:
    html_theme_options:
      navigation_depth: 2
      show_toc_level: 2
```

```yaml
# handbook-content/_toc.yml
format: jb-book
root: intro
chapters:
  - file: basics/index
    sections:
      - file: basics/prompting/index
      - file: basics/rag/index
      - file: basics/fine-tuning/index
      - file: basics/agents/index
      - file: basics/embeddings/index
      - file: basics/evaluation/index

  - file: advanced/index
    sections:
      - file: advanced/prompting/index
      - file: advanced/rag/index
      - file: advanced/fine-tuning/index
      - file: advanced/agents/index
      - file: advanced/embeddings/index
      - file: advanced/evaluation/index

  - file: newly-discovered/index
    sections:
      - file: newly-discovered/model-updates/index
      - file: newly-discovered/framework-updates/index
      - file: newly-discovered/productivity-tools/index
      - file: newly-discovered/business-cases/index
      - file: newly-discovered/how-people-use-ai/index
```

### Workflows and Sequencing

**Story Dependency Graph:**

```
Story 1.1 (Project Init)
    ├─→ Story 1.2 (Database Setup)
    │     └─→ Story 1.3 (Vector DB)
    │           └─→ Story 1.4 (Auto-News Adaptation)
    ├─→ Story 1.5 (CI/CD Pipeline)
    ├─→ Story 1.6 (Jupyter Book Config)
    └─→ Story 1.7 (Dev Environment)
              └─→ (Depends on 1.2, 1.3 for Docker Compose)
```

**Critical Path:** 1.1 → 1.2 → 1.3 → 1.4 (sequential, foundation for Epic 2)

**Parallel Work:** Stories 1.5, 1.6 can be done in parallel with 1.2-1.4

**Development Workflow Sequence:**

1. **Local Setup (Story 1.1, 1.7):**
   - Clone repo → Install Poetry → Copy .env.example → Configure API keys
   - Run `docker-compose up -d` for local Postgres + pgvector

2. **Database Initialization (Story 1.2, 1.3):**
   - Execute setup_pgvector.sql to create schema
   - Verify pgvector extension installed (`SELECT * FROM pg_extension WHERE extname = 'vector';`)
   - Test connection pooling with sample queries

3. **Jupyter Book Local Build (Story 1.6):**
   - `cd handbook-content` → `jupyter-book build .` → Open `_build/html/index.html`
   - Verify 3-section structure renders correctly

4. **CI/CD Validation (Story 1.5):**
   - Push to feature branch → GitHub Actions runs ci.yml
   - Verify linting (ruff), tests (pytest), type checking (mypy) pass
   - Merge to main → GitHub Actions runs deploy.yml → Jupyter Book deploys to gh-pages

## Non-Functional Requirements

### Performance

**NFR-P1: Database Query Performance**
- PostgreSQL queries complete in <50ms for simple reads (90th percentile)
- pgvector similarity search completes in <100ms for 100K vectors (per architecture NFR-P3)
- Connection pool maintains 5-20 connections without exhaustion under load
- Database supports 1000+ handbook pages without degradation (per architecture NFR-S1)

**NFR-P2: Jupyter Book Build Performance**
- Local build completes in <2 minutes for empty handbook structure
- CI/CD build completes in <5 minutes with dependency caching
- Full rebuild for 1000 pages completes in <10 minutes (per architecture NFR-S1)

**NFR-P3: Development Environment Setup**
- New developer can clone, setup, and run tests in <30 minutes (per Epic 1 success criteria)
- Docker Compose starts Postgres + pgvector in <60 seconds
- Poetry dependency installation completes in <3 minutes (with cache)

### Security

**NFR-SEC1: Credential Management**
- All API keys stored in environment variables, never in code or git history
- `.env.example` provides template without actual secrets
- Database credentials use AWS IAM authentication where possible
- GitHub Actions uses GitHub Secrets for sensitive values

**NFR-SEC2: Database Security**
- RDS PostgreSQL encryption at rest enabled (AWS KMS)
- Security group limits access to Airflow instances only
- Connection strings use SSL/TLS for data in transit
- Database backups encrypted with same KMS key

**NFR-SEC3: Dependency Security**
- All Python dependencies pinned to specific versions in poetry.lock
- Dependabot enabled for automated security updates
- CI/CD runs safety check on dependencies (no high-severity CVEs)
- Quarterly manual review of dependency chain

**NFR-SEC4: Access Control**
- GitHub repository requires PR approval for main branch
- RDS database uses principle of least privilege (application role only)
- Local development uses separate credentials from production
- Admin access to infrastructure limited to 2-3 maintainers

### Reliability/Availability

**NFR-R1: Database Reliability**
- RDS automated backups enabled (daily, 30-day retention per architecture data schema)
- Point-in-time recovery enabled for disaster recovery
- Database monitoring alerts on connection failures
- Failover to standby instance in case of primary failure (Multi-AZ if production)

**NFR-R2: CI/CD Reliability**
- GitHub Actions workflows have 95%+ success rate
- Failed builds don't block local development
- Deployment failures preserve previous working version (zero-downtime per architecture)
- Rollback capability via git revert + automatic redeploy

**NFR-R3: Development Environment Reliability**
- Docker Compose configuration is version-controlled and tested
- Local Postgres + pgvector mirrors production schema exactly
- Test fixtures provide consistent, reproducible test data
- Setup scripts are idempotent (safe to run multiple times)

### Observability

**NFR-O1: Logging**
- Structured logging with Loguru (JSON format for machine parsing)
- Log levels: DEBUG (local), INFO (CI), WARNING (alerts), ERROR (immediate action)
- All database operations logged with query, duration, result count
- Airflow DAG logs accessible via Airflow UI

**NFR-O2: Monitoring**
- Database performance metrics visible in AWS CloudWatch (per architecture)
- CI/CD build duration tracked and reported
- GitHub Actions status badges in README.md
- Local development: logs written to `logs/` directory (git-ignored)

**NFR-O3: Error Tracking**
- Python exceptions include full stack trace and context
- Database errors logged with query and parameters (sanitized)
- CI/CD failures send notifications via GitHub (email/Slack in future)
- Failed tests provide clear error messages and reproduction steps

**NFR-O4: Documentation**
- README.md provides quickstart guide
- CONTRIBUTING.md documents development workflow
- Inline code comments for complex logic
- Database schema documented with SQL comments

## Dependencies and Integrations

### Python Dependencies (pyproject.toml)

**Core Infrastructure:**
- `python = "^3.10"` - Python runtime (modern type hints, match statements)
- `poetry = "^1.8"` - Dependency management
- `ruff = "^0.6"` - Fast linting and formatting
- `loguru = "^0.7"` - Structured logging

**Database:**
- `psycopg[binary,pool] = "^3.2"` - PostgreSQL adapter with connection pooling
- `pgvector = "^0.3"` - pgvector Python client

**Testing:**
- `pytest = "^8.0"` - Testing framework
- `pytest-cov = "^5.0"` - Coverage reporting
- `pytest-mock = "^3.14"` - Mocking for tests

**Jupyter Book (Static Site Generation):**
- `jupyter-book = "^1.0.4"` - Documentation site generator
- `sphinx-design = "^0.6"` - Card layouts and grids
- `sphinx-togglebutton = "^0.3"` - Collapsible sections
- `sphinxext-opengraph = "^0.9"` - Social media preview tags

**Airflow (Existing Auto-News):**
- `apache-airflow = "existing"` - Keep current version from Auto-News
- Existing operators reused where possible

**Utilities:**
- `python-dotenv = "^1.0"` - Environment variable loading
- `httpx = "^0.27"` - Async HTTP client
- `pydantic = "^2.0"` - Data validation (optional, for future API)

### External Service Dependencies

**Amazon RDS PostgreSQL 16:**
- **Purpose:** Primary database for content, embeddings, review status
- **Connection:** psycopg3 with connection pooling (5-20 connections)
- **Authentication:** IAM database authentication or username/password
- **Cost:** ~$25/month (db.t3.small, 20GB gp3)

**GitHub:**
- **Repository Hosting:** Main codebase and handbook content
- **GitHub Actions:** CI/CD automation (ci.yml, deploy.yml)
- **GitHub Pages:** Static site hosting ($0 cost)
- **GitHub API:** Used in future for automated commits (Epic 4)

**Docker (Local Development):**
- **PostgreSQL 16:** Local database matching production
- **pgvector 0.8.0:** Vector extension matching production
- **Docker Compose:** Orchestrates local services

### Integration Architecture

**1. Airflow → PostgreSQL (Story 1.4)**
```
Auto-News DAGs → Execute SQL queries → PostgreSQL
                                     ↓
                             Store content_items, embeddings
```
- Connection via Airflow connections (configured in Airflow UI)
- Use connection pooling to avoid exhaustion
- Idempotent operations (UPSERT patterns)

**2. Python Application → PostgreSQL (Story 1.2)**
```
handbook/db_connection/postgres.py → ConnectionPool → RDS PostgreSQL
```
- Pool size: 5 min, 20 max connections
- Transaction management via context managers
- SSL/TLS for data in transit

**3. Python Application → pgvector (Story 1.3)**
```
handbook/db_connection/pgvector.py → SQL queries → pgvector extension
```
- Vector similarity: `embedding <=> $1` (cosine distance operator)
- ivfflat index for performance (<100ms queries)
- Batch insertions using COPY for efficiency

**4. GitHub Actions → Jupyter Book → GitHub Pages (Story 1.5, 1.6)**
```
Push to main → GitHub Actions trigger → Install deps (cached)
                                      ↓
                              jupyter-book build
                                      ↓
                              Deploy to gh-pages branch
                                      ↓
                              Live on GitHub Pages
```
- Automated deployment on every main branch commit
- Build caching speeds up deployment (30s vs 2min)
- Zero-downtime deployment (old version live until new ready)

**5. Docker Compose → Local Services (Story 1.7)**
```
docker-compose up → Start Postgres container
                  → Start pgvector extension
                  → Expose port 5432 to host
```
- Local development mirrors production environment
- Same PostgreSQL version (16), same pgvector version (0.8.0)
- Isolated from production data

## Acceptance Criteria (Authoritative)

These criteria define "done" for Epic 1 and must be verified before moving to Epic 2:

### AC-1: Repository Structure and Configuration
**Given** the repository is initialized
**When** a developer clones the repository
**Then** the structure includes:
- ✅ Root-level pyproject.toml with Poetry configuration
- ✅ handbook/ directory for handbook-specific pipeline code
- ✅ auto-news-engine/ directory with existing Auto-News codebase
- ✅ handbook-content/ directory with Jupyter Book structure
- ✅ .github/workflows/ with ci.yml and deploy.yml
- ✅ tests/ directory with unit/ and integration/ subdirectories
- ✅ README.md with project overview and setup instructions
- ✅ CONTRIBUTING.md with development workflow
- ✅ .env.example with required environment variables template

### AC-2: PostgreSQL Database Setup
**Given** AWS RDS PostgreSQL 16 is provisioned
**When** the database initialization script runs
**Then**:
- ✅ All tables created: content_items, embeddings, content_scores, review_status, approved_content, failed_items
- ✅ All indexes created including btree and pgvector ivfflat indexes
- ✅ Foreign key constraints enforce referential integrity
- ✅ Database connection pool configured (5 min, 20 max connections)
- ✅ Connection test successfully inserts and queries sample data
- ✅ Database backups configured (daily, 30-day retention)

### AC-3: pgvector Extension Operational
**Given** PostgreSQL database is set up
**When** pgvector operations are tested
**Then**:
- ✅ pgvector extension version 0.8.0 installed successfully
- ✅ ivfflat index created on embeddings.embedding column
- ✅ Sample embedding (1536 dimensions) inserted successfully
- ✅ Similarity search query completes in <100ms for 1000 sample vectors
- ✅ Cosine distance operator (<->) returns accurate similarity scores
- ✅ Duplicate detection works (same embedding returns similarity ~1.0)

### AC-4: Auto-News Engine Adapted
**Given** existing Auto-News codebase is available
**When** Auto-News is adapted for handbook use case
**Then**:
- ✅ Reusable operators identified and documented
- ✅ Source configuration updated for LLM-focused sources (placeholder sources configured)
- ✅ Output target updated to handbook Postgres schema (not original Notion structure)
- ✅ Airflow DAGs runnable in development environment
- ✅ Test run successfully connects to new Postgres schema

### AC-5: GitHub Actions CI/CD Pipeline
**Given** GitHub repository has Actions workflows
**When** a pull request is created
**Then** ci.yml workflow:
- ✅ Runs ruff linting (no errors)
- ✅ Runs pytest with coverage report (70% minimum)
- ✅ Runs mypy type checking (no errors)
- ✅ Completes in under 5 minutes
- ✅ Status check blocks merge if any step fails

**When** changes are merged to main
**Then** deploy.yml workflow:
- ✅ Builds Jupyter Book successfully
- ✅ Deploys to gh-pages branch
- ✅ Site accessible at GitHub Pages URL
- ✅ Completes in under 10 minutes

### AC-6: Jupyter Book Configuration
**Given** Jupyter Book is configured
**When** the book is built locally
**Then**:
- ✅ Build completes without errors in <2 minutes
- ✅ Generated HTML includes 3 main sections (Basics, Advanced, Newly Discovered)
- ✅ Table of contents renders with 2-level hierarchy
- ✅ Custom CSS and logo applied correctly
- ✅ sphinx-design, sphinx-togglebutton, sphinxext-opengraph extensions loaded
- ✅ Mobile-responsive layout verified
- ✅ Search functionality works (built-in Sphinx search)

### AC-7: Development Environment Setup
**Given** a new developer follows README instructions
**When** they set up the development environment
**Then**:
- ✅ Complete setup (clone, Poetry install, Docker Compose up, run tests) in <30 minutes
- ✅ Docker Compose starts Postgres + pgvector without errors
- ✅ Database connection test passes
- ✅ All tests run successfully with pytest
- ✅ Jupyter Book builds locally without errors
- ✅ Linting passes with ruff check
- ✅ Developer can create feature branch, make changes, and run full validation locally

## Traceability Mapping

| Acceptance Criteria | PRD Requirement | Architecture Component | Story | Test Approach |
|---------------------|-----------------|------------------------|-------|---------------|
| **AC-1: Repository Structure** | FR-1.1 (Multi-source ingestion foundation) | Project Structure (arch.md) | Story 1.1 | Manual verification of directory structure, README content |
| **AC-2: PostgreSQL Setup** | FR-8.1 (Vector storage), NFR-R3 (Data integrity) | Database Schema (arch.md), ADR-001 | Story 1.2 | Integration test: create all tables, verify indexes, connection pool test |
| **AC-3: pgvector Operational** | FR-1.2 (Intelligent deduplication), FR-8.1 (Vector storage) | pgvector Integration, ADR-002 | Story 1.3 | Integration test: insert embeddings, similarity query performance test |
| **AC-4: Auto-News Adapted** | FR-1.1 (Multi-source content collection) | Auto-News Engine Adaptation (arch.md) | Story 1.4 | Integration test: run DAG, verify Postgres schema output |
| **AC-5: CI/CD Pipeline** | NFR-M1 (Code quality), NFR-R2 (CI/CD reliability) | GitHub Actions Workflows (arch.md) | Story 1.5 | Automated: GitHub Actions runs on every PR/merge |
| **AC-6: Jupyter Book Config** | FR-4.2 (Structured handbook display), ADR-004 | Jupyter Book Configuration (arch.md) | Story 1.6 | Manual: local build, verify HTML output, responsive test |
| **AC-7: Dev Environment** | NFR-M2 (Documentation), Epic 1 Success Criteria | Development Environment (arch.md) | Story 1.7 | Manual: timed setup following README by new contributor |

**Coverage Analysis:**
- ✅ **PRD FR-1.1** (Multi-source aggregation foundation): AC-1, AC-4
- ✅ **PRD FR-1.2** (Deduplication foundation): AC-3
- ✅ **PRD FR-4.2** (Handbook display): AC-6
- ✅ **PRD FR-8.1** (Vector storage): AC-2, AC-3
- ✅ **Architecture ADR-001** (RDS PostgreSQL): AC-2
- ✅ **Architecture ADR-002** (pgvector): AC-3
- ✅ **Architecture ADR-004** (Jupyter Book): AC-6
- ✅ **NFR-M1, M2** (Code quality, documentation): AC-5, AC-7
- ✅ **NFR-R2, R3** (Reliability): AC-2, AC-5

**Gaps Identified:** None - all Epic 1 acceptance criteria trace to PRD requirements and architectural decisions.

## Risks, Assumptions, Open Questions

### Risks

**RISK-1: pgvector Performance Degradation at Scale**
- **Severity:** Medium
- **Probability:** Low
- **Description:** pgvector may not meet <100ms query performance for 100K+ vectors despite ivfflat indexing
- **Mitigation:**
  - Benchmark with 100K sample vectors during Story 1.3
  - If performance degrades: tune ivfflat lists parameter (currently 100, may need 200)
  - Fallback: Migrate to dedicated vector DB (Pinecone, ChromaDB) in Epic 2-3 if needed
- **Owner:** Story 1.3 implementer

**RISK-2: Auto-News Airflow Version Compatibility**
- **Severity:** Medium
- **Probability:** Medium
- **Description:** Auto-News may use older Airflow version incompatible with new handbook DAGs
- **Mitigation:**
  - Document existing Airflow version during Story 1.4
  - Keep handbook DAGs compatible with Auto-News Airflow version
  - If incompatible: run handbook DAGs on separate Airflow instance
- **Owner:** Story 1.4 implementer

**RISK-3: GitHub Pages Build Timeout**
- **Severity:** Low
- **Probability:** Low
- **Description:** Jupyter Book build may exceed 10-minute GitHub Actions timeout for large handbooks
- **Mitigation:**
  - Monitor build duration in Story 1.5, 1.6
  - Optimize build: incremental builds (if Jupyter Book adds support), asset compression
  - Fallback: Deploy to Netlify or Vercel (also free for static sites)
- **Owner:** Story 1.5, 1.6 implementers

**RISK-4: RDS Cost Overrun**
- **Severity:** Low
- **Probability:** Low
- **Description:** RDS db.t3.small may be undersized, requiring upgrade to db.t3.medium (~$50/month)
- **Mitigation:**
  - Monitor CloudWatch metrics during development
  - Start with db.t3.small as planned
  - Upgrade if CPU >80% sustained or connection pool exhaustion
- **Owner:** Infrastructure owner

### Assumptions

**ASSUMPTION-1: Single Database Sufficient**
- **Description:** Single PostgreSQL database can handle both relational data and pgvector embeddings without performance issues
- **Validation:** Benchmark during Story 1.2, 1.3 with realistic data volumes
- **If False:** Separate relational DB and vector DB (impacts architecture, increases cost)

**ASSUMPTION-2: Existing Auto-News Operators Reusable**
- **Description:** Auto-News ingestion operators can be adapted for handbook sources without major rewrites
- **Validation:** Review Auto-News codebase during Story 1.4
- **If False:** Write new operators from scratch (impacts Story 1.4 effort, may delay Epic 2)

**ASSUMPTION-3: GitHub Pages Meets Performance NFRs**
- **Description:** GitHub Pages CDN delivers <2 second page load on 3G (NFR-P1 from PRD)
- **Validation:** Load test after Story 1.6 deployment
- **If False:** Migrate to dedicated CDN (Cloudflare, CloudFront) or static host (Netlify, Vercel)

**ASSUMPTION-4: Docker Compose Sufficient for Local Dev**
- **Description:** Docker Compose with Postgres + pgvector provides adequate local development environment
- **Validation:** New contributor setup test during Story 1.7
- **If False:** Provide alternative setup (e.g., Postgres.app, native install) or improve Docker Compose docs

### Open Questions

**QUESTION-1: RDS Multi-AZ for Production?**
- **Question:** Should RDS be configured with Multi-AZ for high availability?
- **Impact:** Cost increases from ~$25 to ~$50/month
- **Decision Needed:** Before Story 1.2 implementation
- **Recommendation:** Start with single-AZ for MVP, add Multi-AZ when reaching production scale (5K+ users)

**QUESTION-2: Separate Airflow Instance for Handbook?**
- **Question:** Should handbook DAGs run on separate Airflow instance or share Auto-News Airflow?
- **Impact:** Separate instance = more operational overhead but cleaner separation
- **Decision Needed:** During Story 1.4
- **Recommendation:** Share Auto-News Airflow initially, split later if conflicts arise

**QUESTION-3: Custom Domain for GitHub Pages?**
- **Question:** Use custom domain (e.g., llm-handbook.dev) or GitHub default (username.github.io)?
- **Impact:** Custom domain improves branding but adds DNS configuration
- **Decision Needed:** Before Story 1.5, 1.6 deployment
- **Recommendation:** Start with GitHub default for MVP, add custom domain in Epic 4 (publication polish)

**QUESTION-4: pgvector Index Tuning Parameters?**
- **Question:** What are optimal ivfflat index parameters (lists, probes) for 100K vectors?
- **Impact:** Affects query performance (<100ms requirement)
- **Decision Needed:** During Story 1.3 implementation
- **Recommendation:** Start with lists=100 (architecture default), tune based on benchmarks

## Test Strategy Summary

### Unit Testing (Story 1.7)
**Scope:** Isolated testing of individual functions and classes

**Test Files:**
- `tests/unit/test_postgres.py` - Database connection pooling, transaction management
- `tests/unit/test_pgvector.py` - Embedding insertion, similarity search logic
- `tests/unit/test_config.py` - Configuration loading, environment variables

**Approach:**
- Use pytest with pytest-mock for mocking external dependencies
- Mock database connections (no actual DB needed)
- Fast execution (<10 seconds for all unit tests)
- 70% code coverage minimum

**Example Test:**
```python
def test_postgres_connection_pool(mocker):
    """Test connection pool initialization."""
    mock_pool = mocker.patch('psycopg.pool.ConnectionPool')
    conn = PostgresConnection()
    assert conn.pool is not None
    mock_pool.assert_called_once()
```

### Integration Testing (Story 1.2, 1.3, 1.7)
**Scope:** Test interaction with real database

**Test Files:**
- `tests/integration/test_postgres_integration.py` - Real database operations
- `tests/integration/test_pgvector_integration.py` - Real vector similarity search

**Approach:**
- Use Docker Compose to spin up test Postgres + pgvector
- Run tests against real database (not mocked)
- Clean up test data after each test (fixtures)
- Slower execution (~1-2 minutes for all integration tests)

**Example Test:**
```python
def test_pgvector_similarity_search(test_db):
    """Test real similarity search with pgvector."""
    pgvector = PgVectorOperations(test_db)

    # Insert sample embeddings
    embedding1 = [0.1] * 1536
    pgvector.insert_embedding(1, "hash1", embedding1, "text1")

    # Search for similar
    results = pgvector.find_similar(embedding1, threshold=0.8)
    assert len(results) == 1
    assert results[0][1] > 0.99  # High similarity
```

### End-to-End Testing (Story 1.5, 1.6)
**Scope:** Full workflow validation

**Test Scenarios:**
1. **CI/CD Pipeline Test:**
   - Create test PR → Verify ci.yml runs → Check all stages pass
   - Merge to main → Verify deploy.yml runs → Check site deployed

2. **Local Development Test:**
   - New contributor follows README → Completes setup in <30 minutes → All tests pass

3. **Jupyter Book Build Test:**
   - Local build → Verify HTML output → Check all sections render → Test search

**Approach:**
- Manual testing for MVP (automated later)
- Document test cases in `tests/e2e/test_plan.md`
- Smoke test checklist for deployment validation

### Performance Testing (Story 1.3)
**Scope:** Verify NFR performance requirements

**Test Cases:**
1. **Database Query Performance:**
   - Insert 10K content_items → Query by category → Verify <50ms

2. **pgvector Performance:**
   - Insert 100K embeddings → Similarity search → Verify <100ms

3. **Jupyter Book Build:**
   - Build empty structure → Verify <2 minutes
   - Build with 100 pages → Verify <5 minutes

**Approach:**
- Use pytest-benchmark for timing
- Run on representative hardware (CI environment)
- Fail test if performance degrades below threshold

### Security Testing (Story 1.7)
**Scope:** Verify security requirements

**Test Cases:**
1. **Credential Management:**
   - Scan codebase for hardcoded secrets → Verify none found
   - Check .env.example has no real values

2. **Dependency Security:**
   - Run `poetry export | safety check` → Verify no high-severity CVEs
   - Dependabot configured and enabled

**Approach:**
- Automated in CI/CD (ci.yml includes safety check)
- Manual review of .env.example and configuration files

### Testing Coverage Target
- **Unit Tests:** 70% code coverage minimum
- **Integration Tests:** Cover all database operations
- **E2E Tests:** Cover critical user paths (setup, build, deploy)
- **Performance Tests:** All NFR-P requirements validated
