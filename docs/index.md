# Project Documentation Index

**Project**: cherry-in-the-haystack (Auto-News)
**Type**: Monorepo - Data Pipeline Application
**Generated**: 2025-11-07
**Scan Level**: Deep

## Project Overview

cherry-in-the-haystack is a monorepo containing Auto-News, an intelligent content aggregation system that uses LLMs to automatically collect, filter, and curate information from multiple sources (RSS, Reddit, Twitter, YouTube, Arxiv). The system helps users stay informed efficiently by removing 80%+ noise and generating actionable insights.

### Repository Structure

- **Type**: Monorepo with 3 application parts
- **Primary Language**: Python 3.11+
- **Architecture**: Event-Driven Data Pipeline with DAG Orchestration

### Quick Reference

#### Part: API (Active Development)

- **Type**: Data Pipeline (Apache Airflow)
- **Tech Stack**: Python 3.11, Airflow 2.8.4, LangChain 0.3.1, LlamaIndex, AutoGen
- **Root**: `dev/apps/api/`
- **Status**: ✅ Production-ready
- **Key Features**: Multi-source aggregation, LLM processing, Vector storage, Notion integration

#### Part: Web (Planned)

- **Type**: Frontend
- **Tech Stack**: Next.js, React (planned)
- **Root**: `dev/apps/web/`
- **Status**: 📋 Placeholder

#### Part: Agent (Planned)

- **Type**: LLM Agent System
- **Tech Stack**: Python, LangChain (planned)
- **Root**: `dev/apps/agent/`
- **Status**: 📋 Placeholder

## Generated Documentation

### Core Documentation

- [Project Overview](./project-overview.md) - High-level project summary and purpose
- [Source Tree Analysis](./source-tree-analysis.md) - Complete codebase structure with annotations
- [Architecture - API](./architecture-api.md) - Technical architecture and design patterns
- [Development Guide - API](./development-guide-api.md) - Setup and development workflow

### Existing Documentation

- [Auto-News README](../dev/apps/api/README.md) - Comprehensive original documentation
- [Auto-News Wiki](https://github.com/finaldie/auto-news/wiki) - Official wiki (external)
- [Dev Directory README](../dev/README.md) - Development directory overview (Korean)
- [Apps README](../dev/apps/README.md) - Applications overview (Korean)
- [Deployment - Helm](../dev/apps/api/helm/README.md) - Kubernetes Helm deployment
- [Deployment - ArgoCD](../dev/apps/api/argocd/README.md) - GitOps deployment

### Reference Documentation

- [Upstream Auto-News README](./reference/auto-news-upstream/autonews-README.md) - Upstream reference
- [Product Development Notes](./reference/notion-export/product development.md) - Planning docs

## Technology Stack

### API Application

| Category | Technology | Version |
|----------|------------|---------|
| **Orchestration** | Apache Airflow | 2.8.4 |
| **Runtime** | Python | 3.11 |
| **LLM Framework** | LangChain | 0.3.1 |
| **RAG** | LlamaIndex | 0.9+ |
| **Multi-Agent** | AutoGen (ag2) | 0.2.2 |
| **Relational DB** | MySQL | 8.x |
| **Cache** | Redis | Latest |
| **Vector DB** | Milvus, ChromaDB, Pinecone | 2.4+, 0.4+, Latest |
| **Container** | Docker | Latest |
| **Orchestrator** | Kubernetes | Latest |
| **Deployment** | Helm, ArgoCD | Latest |

### LLM Providers

- OpenAI (ChatGPT, embeddings)
- Google Gemini
- Ollama (local option)

### Content Sources

- RSS Feeds
- Reddit
- Twitter/X
- YouTube
- Arxiv
- Web Articles

## Getting Started

### For New Developers

1. **Understand the Project**:
   - Read [Project Overview](./project-overview.md)
   - Review [Architecture - API](./architecture-api.md)
   - Explore [Source Tree Analysis](./source-tree-analysis.md)

2. **Set Up Development Environment**:
   - Follow [Development Guide - API](./development-guide-api.md)
   - Configure environment variables
   - Run `make deps && make build && make deploy && make init && make start`

3. **Explore the Codebase**:
   - **DAGs**: `dev/apps/api/dags/*.py` - Airflow workflows
   - **Operators**: `dev/apps/api/src/ops_*.py` - Business logic
   - **LLM Integration**: `dev/apps/api/src/llm_*.py` - LLM layer
   - **Data Layer**: `dev/apps/api/src/*_cli.py` - Database clients

### For AI-Assisted Development

**When planning new features**, use this index as the primary context source:

- **UI-only features**: Reference [Architecture - API](./architecture-api.md) for Notion integration patterns
- **Data pipeline features**: Reference [Source Tree Analysis](./source-tree-analysis.md) for operator patterns
- **LLM features**: Reference [Architecture - API](./architecture-api.md) for LLM layer design
- **Full-stack features**: Reference all architecture docs + integration patterns

### Quick Access

#### Entry Points

- **Airflow UI**: http://localhost:8080 (local development)
- **Airflow DAGs**: `dev/apps/api/dags/*.py` (`news_pulling`, `collect_weekly`, `journal_daily`, etc.)
- **Main Pipeline**: `dev/apps/api/dags/news_pulling.py:37` (news_pulling DAG)
- **Makefile**: `dev/apps/api/Makefile:1` (build commands)

#### Critical Files

- **Project Config**: `dev/apps/api/pyproject.toml:1` (Python dependencies)
- **Docker Image**: `dev/apps/api/docker/Dockerfile:1` (container definition)
- **Environment Template**: `dev/apps/api/.env.template` (configuration)
- **Database Schema**: `dev/apps/api/src/db_tables.py:1` (MySQL tables)
- **Redis Keys**: `dev/apps/api/src/data_model.py:1` (cache schema)
- **LLM Prompts**: `dev/apps/api/src/llm_prompts.py:1` (prompt templates)
- **Notion Integration**: `dev/apps/api/src/notion.py:1` (70KB comprehensive client)

#### Key Operators

- **Article Processing**: `dev/apps/api/src/ops_article.py:21` (OperatorArticle class)
- **Journal Processing**: `dev/apps/api/src/ops_journal.py` (OperatorJournal class)
- **RSS Aggregation**: `dev/apps/api/src/ops_rss.py` (OperatorRSS class)
- **YouTube Integration**: `dev/apps/api/src/ops_youtube.py` (OperatorYouTube class)
- **Twitter Integration**: `dev/apps/api/src/ops_twitter.py` (OperatorTwitter class)
- **Reddit Integration**: `dev/apps/api/src/ops_reddit.py` (OperatorReddit class)

## Data Architecture

### Data Flow

```
[Sources] → [Ingestion] → [LLM Processing] → [Vector Storage] → [Distribution]
    ↓           ↓              ↓                   ↓                  ↓
 RSS, etc   Operators   Categorize/Rank      Milvus/ChromaDB      Notion
```

### Databases

- **MySQL**: Metadata, indexes, patch tracking
- **Redis**: Caching, deduplication
- **Milvus/ChromaDB**: Vector embeddings for semantic search

### Pipeline Stages

1. **Ingestion**: Source operators pull content
2. **Deduplication**: Redis cache checks
3. **LLM Processing**: Categorization, ranking, summarization
4. **Embedding**: Content vectorization
5. **Distribution**: Publish to Notion workspaces

## Deployment

### Local Development

```bash
cd dev/apps/api
make deps build deploy init start
```

Access Airflow UI at http://localhost:8080

### Production Deployment

- **Docker Compose**: For small deployments
- **Kubernetes + Helm**: For production clusters
- **ArgoCD**: GitOps continuous deployment

See [Development Guide - API](./development-guide-api.md) for detailed instructions.

## Development Workflow

### Adding New Features

1. **Plan**: Review architecture and existing patterns
2. **Implement**:
   - Create operator in `src/ops_*.py`
   - Create Airflow tasks in `src/af_*.py`
   - Create DAG in `dags/*.py`
3. **Test**: Run locally via Airflow UI
4. **Deploy**: Build, push, and deploy via Makefile

### Modifying Existing Features

1. Edit source files in `dev/apps/api/src/`
2. Rebuild: `make build`
3. Deploy: `make deploy`
4. Push DAGs: `make push_dags`

## Common Tasks

### Development

- **Start services**: `make start`
- **Stop services**: `make stop`
- **View logs**: `make logs`
- **Build image**: `make build`
- **Deploy**: `make deploy`

### Kubernetes

- **Build for K8s**: `make k8s-docker-build repo=... tag=...`
- **Deploy to K8s**: `make k8s-helm-install`
- **Port forward**: `kubectl port-forward service/auto-news-webserver 8080:8080 -n auto-news`

## Integration Points

### External APIs

- Notion API (primary output)
- OpenAI API (LLM and embeddings)
- Google Gemini API (alternative LLM)
- Twitter/X API (content source)
- Reddit API (content source)
- YouTube API (content source)

### Internal Services

- Apache Airflow (orchestration)
- MySQL (metadata storage)
- Redis (caching layer)
- Milvus/ChromaDB (vector storage)

## Testing

### Unit Tests

```bash
cd dev/apps/api/src
python3 -m pytest tests/
```

### Integration Tests

- Run DAGs in Airflow UI
- Verify output in Notion workspace
- Check database state

## Troubleshooting

Common issues and solutions documented in [Development Guide - API](./development-guide-api.md#troubleshooting).

## Project Metrics

- **Source Files**: 70+ Python modules
- **DAG Workflows**: 6 Airflow DAGs
- **Operators**: 10+ content type operators
- **LLM Providers**: 3 (OpenAI, Gemini, Ollama)
- **Vector Databases**: 3 (Milvus, ChromaDB, Pinecone)
- **Content Sources**: 6 (RSS, Reddit, Twitter, YouTube, Arxiv, Web)

## BMAD Integration

This project uses the **BMAD (BMad AI Development)** framework for AI-assisted development workflows. BMAD provides:

- Structured workflow guidance
- Agent-based development
- Documentation automation
- Story and epic management

BMAD directory: `bmad/`

## Support and Resources

- **GitHub**: https://github.com/finaldie/auto-news
- **Wiki**: https://github.com/finaldie/auto-news/wiki
- **Issues**: https://github.com/finaldie/auto-news/issues
- **Managed Service**: https://dots.dotsfy.com/
- **Mobile Apps**: iOS App Store, Google Play

## License

Apache License 2.0

## Next Steps

### For Development

1. Set up local environment: [Development Guide - API](./development-guide-api.md)
2. Understand architecture: [Architecture - API](./architecture-api.md)
3. Explore codebase: [Source Tree Analysis](./source-tree-analysis.md)

### For Brownfield PRD

When creating a PRD for new features in this existing project:

1. Use this index as primary context
2. Reference [Architecture - API](./architecture-api.md) for design patterns
3. Review [Source Tree Analysis](./source-tree-analysis.md) for reusable components
4. Check [Development Guide - API](./development-guide-api.md) for conventions

### For AI Agents

This documentation is optimized for AI-assisted development. When working on this project:

- Start with this index for high-level context
- Drill down into specific docs as needed
- Reference architecture for design decisions
- Use source tree analysis for navigation
- Follow conventions in development guide
