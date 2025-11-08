# Source Tree Analysis

## Project Structure Overview

cherry-in-the-haystack is organized as a monorepo with a clear separation between development code, testing environments, and the BMAD framework integration.

## Root Structure

```
cherry-in-the-haystack/
├── dev/                 # Main development code (Auto-News application)
├── test/                # Testing and experimentation environment
├── bmad/                # BMAD (BMad AI Development) framework integration
├── docs/                # Project documentation (generated and reference)
└── .venv/               # Python virtual environment
```

## Development Directory (`dev/`)

The primary application code resides in the `dev/` directory, following a monorepo pattern with multiple application parts.

```
dev/
├── .github/
│   └── workflows/       # CI/CD GitHub Actions workflows
├── apps/                # Application code (3 parts: API, Web, Agent)
│   ├── api/             # ⭐ Active: Data pipeline backend (Auto-News)
│   ├── web/             # Planned: Frontend application (Next.js/React)
│   └── agent/           # Planned: LLM agent and prompt management
├── packages/            # Shared modules and utilities
├── infra/               # Infrastructure as Code (IaC) and deployment scripts
├── scripts/             # Build, migration, and automation scripts
└── README.md            # Dev directory overview
```

## API Application (`dev/apps/api/`) - Active Development

The Auto-News data pipeline is the core active application with comprehensive infrastructure.

### API Directory Structure

```
dev/apps/api/
├── src/                 # 🔵 Source code (70+ Python modules)
│   ├── af_*.py          # Airflow task operators (start, pull, save, end, etc.)
│   ├── ops_*.py         # Core operators (article, journal, notion, rss, youtube, etc.)
│   ├── llm_*.py         # LLM integration (agent, prompts, autogen)
│   ├── embedding_*.py   # Embedding providers (OpenAI, HuggingFace, Ollama)
│   ├── db_*.py          # Database clients (MySQL, Redis)
│   ├── *_cli.py         # Vector DB clients (ChromaDB, Milvus, LlamaIndex)
│   ├── notion.py        # Notion API integration (70KB - comprehensive)
│   ├── data_model.py    # Redis key schemas
│   ├── db_tables.py     # MySQL table definitions
│   └── utils.py         # Shared utilities
├── dags/                # 🟢 Airflow DAG definitions (6 workflows)
│   ├── news_pulling.py  # Hourly news aggregation (main pipeline)
│   ├── collect_weekly.py # Weekly top content recap
│   ├── journal_daily.py # Daily journal processing
│   ├── sync_dist.py     # Distribution sync
│   ├── todo.py          # TODO list generation
│   └── upgrade.py       # System upgrade tasks
├── docker/              # 🔶 Docker containerization
│   ├── Dockerfile       # Apache Airflow 2.8.4 + Python 3.11
│   ├── docker-compose.yml # Multi-container setup
│   ├── requirements.txt # Python dependencies
│   └── portainer/       # Portainer configuration
├── helm/                # ⚙️ Kubernetes Helm charts
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/       # K8s resource templates
├── argocd/              # 🚀 ArgoCD GitOps deployment
│   └── templates/
├── Makefile             # Build and deployment automation
├── pyproject.toml       # Python project configuration (auto-news 0.1.0)
├── install.env          # Installation environment variables
└── README.md            # Comprehensive Auto-News documentation
```

### Source Code Organization

The `src/` directory contains 70+ Python modules organized by functionality:

**Airflow Task Operators** (`af_*.py`):
- Entry points for DAG tasks
- Orchestrate data flow between operators
- Handle task lifecycle (start, end, clean)

**Core Operators** (`ops_*.py`):
- `ops_article.py` - Web article processing
- `ops_journal.py` - Journal notes processing
- `ops_rss.py` - RSS feed aggregation
- `ops_youtube.py` - YouTube transcript extraction
- `ops_twitter.py` - Twitter/X integration
- `ops_reddit.py` - Reddit content aggregation
- `ops_notion.py` - Notion workspace integration
- `ops_obsidian.py` - Obsidian vault integration
- `ops_collection.py` - Content collection management
- `ops_stats.py` - Statistics and analytics
- `ops_deepdive.py` - Multi-agent deep research
- `ops_base.py` - Base operator class

**LLM Integration** (`llm_*.py`):
- `llm_agent.py` - LLM agent orchestration (15KB)
- `llm_autogen.py` - AutoGen multi-agent framework (23KB)
- `llm_prompts.py` - Prompt templates (14KB)
- `llm_const.py` - LLM constants

**Embedding Layer** (`embedding_*.py`):
- `embedding.py` - Base embedding interface
- `embedding_openai.py` - OpenAI embeddings
- `embedding_openai_0x.py` - OpenAI v0.x compatibility
- `embedding_openai_1x.py` - OpenAI v1.x compatibility
- `embedding_hf.py` - HuggingFace embeddings
- `embedding_hf_inst.py` - HuggingFace Instruct models
- `embedding_ollama.py` - Ollama local embeddings
- `embedding_agent.py` - Embedding agent orchestration
- `embedding_utils.py` - Embedding utilities

**Database Layer** (`*_cli.py`, `db_*.py`):
- `mysql_cli.py` - MySQL client
- `redis_cli.py` - Redis cache client
- `chromadb_cli.py` - ChromaDB vector store
- `milvus_cli.py` - Milvus vector database
- `llama_index_cli.py` - LlamaIndex integration
- `db_cli.py` - Unified DB client
- `db_cli_base.py` - DB client base class
- `db_tables.py` - MySQL schema definitions
- `data_model.py` - Redis key schemas

**Integration Modules**:
- `notion.py` - Comprehensive Notion API client (70KB)
- `notion_init.py` - Notion workspace initialization
- `tweets.py` - Twitter/X API integration
- `reddit_agent.py` - Reddit API client
- `tpl_obsidian.py` - Obsidian template rendering

**Operations Support**:
- `ops_audio2text.py` - Audio transcription (Whisper)
- `ops_milvus.py` - Milvus operations
- `ops_todo.py` - TODO management
- `utils.py` - Shared utilities

**Patches and Migrations**:
- `patches.py` - Patch orchestration
- `patch_0.py`, `patch_1.py`, `patch_2.py` - Database migrations

### DAG Workflows

Six Airflow DAGs orchestrate the data pipeline:

1. **news_pulling** - Core hourly pipeline
   - Schedule: Every hour at minute 15
   - Tasks: start → prepare → pull → save → finish
   - Aggregates content from all configured sources

2. **collect_weekly** - Weekly recap
   - Aggregates top content from the week
   - Generates insights and summaries

3. **journal_daily** - Daily journal processing
   - Processes journal entries
   - Generates insights and TODOs

4. **sync_dist** - Distribution synchronization
   - Syncs processed content to distribution targets

5. **todo** - TODO list generation
   - Extracts action items from content
   - Publishes to Notion

6. **upgrade** - System maintenance
   - Database migrations
   - System upgrades

## Web Application (`dev/apps/web/`) - Planned

Frontend application placeholder for the Auto-News web interface.

**Planned Stack:**
- Next.js / React
- Currently contains only README with Korean documentation

## Agent Application (`dev/apps/agent/`) - Planned

LLM agent, prompt management, and evaluation system.

**Planned Components:**
- Prompt templates and version management
- LLM API integration
- Agent logic
- Performance metrics and evaluation

## Packages Directory (`dev/packages/`)

Intended for shared modules:
- Utilities
- Design system components
- Common libraries

Currently placeholder with README.

## Infrastructure Directory (`dev/infra/`)

Infrastructure as Code and deployment scripts.

Currently placeholder with README.

## Scripts Directory (`dev/scripts/`)

CI/CD, migration, and synchronization scripts.

Currently placeholder with README.

## GitHub Workflows (`dev/.github/workflows/`)

CI/CD automation using GitHub Actions.

## Test Directory (`test/`)

Testing and experimentation environment separate from production code.

```
test/
├── .claude/             # Claude Code test configuration
└── .specify/            # Specify design system tests (if applicable)
```

## BMAD Directory (`bmad/`)

BMad AI Development framework integration for AI-assisted development workflows.

```
bmad/
├── core/                # Core BMAD framework components
├── bmm/                 # BMad Method workflows and agents
├── bmb/                 # BMad Builder workflows
└── docs/                # BMAD documentation and reference materials
```

## Documentation Directory (`docs/`)

Project documentation including generated docs and reference materials.

```
docs/
├── stories/             # Development stories and epics
├── bmm-workflow-status.yaml # Workflow tracking
└── reference/           # Reference documentation
    ├── auto-news-upstream/ # Upstream Auto-News docs
    └── notion-export/      # Notion exported docs
```

## Critical Integration Points

### Data Flow

1. **Ingestion**: Source operators pull from RSS, Reddit, Twitter, YouTube
2. **Processing**: LLM agents categorize, rank, and summarize content
3. **Embedding**: Content vectorized using OpenAI/HF/Ollama
4. **Storage**:
   - MySQL: Metadata and indexes
   - Redis: Caching and deduplication
   - Milvus/ChromaDB: Vector storage for semantic search
5. **Distribution**: Published to Notion workspaces

### External Dependencies

- Notion API (primary output interface)
- OpenAI API (LLM and embeddings)
- Google Gemini API (alternative LLM)
- Ollama (local LLM option)
- Twitter/X API
- Reddit API
- YouTube API

### Deployment Targets

- **Docker Compose**: Local development and small deployments
- **Kubernetes + Helm**: Production cluster deployment
- **ArgoCD**: GitOps continuous deployment

## Entry Points

### API Application

- **Airflow DAGs**: `dev/apps/api/dags/*.py`
- **Task Operators**: `dev/apps/api/src/af_*.py`
- **Dockerfile**: `dev/apps/api/docker/Dockerfile`
- **Makefile**: `dev/apps/api/Makefile` (local deployment commands)

### Build and Deployment

- `make deps` - Install dependencies
- `make build` - Build Docker image
- `make deploy` - Deploy Airflow stack
- `make init` - Initialize databases
- `make start` - Start services

## File Naming Conventions

- `af_*.py` - Airflow task operators
- `ops_*.py` - Core business logic operators
- `llm_*.py` - LLM-related modules
- `embedding_*.py` - Embedding provider implementations
- `*_cli.py` - Database and service clients
- `db_*.py` - Database layer
- `patch_*.py` - Database migrations

## Key Observations

1. **Monorepo Structure**: Clear separation of concerns with dedicated directories for each application part
2. **Active Development**: API application is fully implemented; Web and Agent are placeholders
3. **Comprehensive Deployment**: Multiple deployment strategies (Docker, K8s, ArgoCD)
4. **Modular Architecture**: Clean separation between operators, LLM layer, embedding providers, and databases
5. **Multi-LLM Support**: Flexible LLM backend (OpenAI, Gemini, Ollama)
6. **Vector Database Flexibility**: Supports ChromaDB, Milvus, and Pinecone
7. **Airflow-Centric**: Pipeline orchestration via Airflow DAGs
8. **Notion-Centric Output**: Primary user interface through Notion workspaces
