# Project Overview: cherry-in-the-haystack

## Executive Summary

**cherry-in-the-haystack** is a monorepo project containing **Auto-News**, an intelligent content aggregation and curation system powered by Large Language Models (LLMs). The project automates the collection, processing, filtering, and distribution of information from multiple sources (RSS, Reddit, Twitter, YouTube, Arxiv) to help users stay informed efficiently in the AI era.

**Project Status**: Active Development
**Primary Application**: Auto-News Data Pipeline (Python/Airflow)
**Architecture**: Monorepo with 3 planned application parts (1 active, 2 planned)

## Project Purpose

Auto-News solves the information overload problem by:

1. **Automating Content Aggregation**: Pulls from multiple sources automatically
2. **Intelligent Filtering**: Uses LLMs to categorize, rank, and filter content based on user interests
3. **Insight Generation**: Summarizes articles, videos, and papers with key takeaways
4. **Unified Reading Experience**: Delivers curated content to Notion workspaces
5. **Action Extraction**: Generates TODO lists from journal notes and insights
6. **Weekly Recaps**: Provides top-k content summaries for quick catch-up

## Project Structure

### Repository Type

**Monorepo** with clear application boundaries

### Application Parts

| Part | Status | Tech Stack | Purpose |
|------|--------|------------|---------|
| **api** | ✅ Active | Python, Airflow, LangChain | Data pipeline backend for content aggregation and LLM processing |
| **web** | 📋 Planned | Next.js, React | Frontend web interface (currently placeholder) |
| **agent** | 📋 Planned | Python, LangChain | LLM agent and prompt management system (currently placeholder) |

## Technology Stack Summary

### Primary Technologies

- **Language**: Python 3.11+
- **Orchestration**: Apache Airflow 2.8.4
- **LLM Frameworks**: LangChain 0.3.1, LlamaIndex 0.9+
- **Multi-Agent**: AutoGen (ag2) 0.2.2
- **Containerization**: Docker, Kubernetes
- **Deployment**: Helm, ArgoCD

### Data Infrastructure

| Component | Technologies | Purpose |
|-----------|-------------|---------|
| **Relational DB** | MySQL 8.x | Metadata, indexes, patch tracking |
| **Cache** | Redis | Deduplication, temporary storage |
| **Vector Store** | Milvus, ChromaDB, Pinecone | Semantic search, embedding storage |

### LLM Providers

- **OpenAI** (ChatGPT, embeddings)
- **Google Gemini**
- **Ollama** (local deployment option)

### Content Sources

- RSS feeds
- Reddit
- Twitter/X
- YouTube (with transcript extraction)
- Arxiv papers
- Web articles

### Output Targets

- **Primary**: Notion workspaces
- **Secondary**: Obsidian vaults

## Architecture Pattern

**Event-Driven Data Pipeline** with orchestrated DAG workflows

## Key Features

1. Multi-Source Aggregation (RSS, Reddit, Twitter, YouTube, Arxiv, Web)
2. LLM-Powered Insights (categorization, ranking, summarization)
3. Intelligent Filtering (removes 80%+ noise)
4. YouTube Transcript Processing
5. Weekly Top-K Recap
6. TODO Generation
7. Journal Processing with AI insights
8. Deep Dive Research (multi-agent, experimental)
9. Multi-LLM Support
10. Flexible Deployment options

## Repository Organization

```
cherry-in-the-haystack/
├── dev/           # Primary development code
│   ├── apps/      # Applications (api, web, agent)
│   ├── packages/  # Shared modules
│   ├── infra/     # Infrastructure as Code
│   └── scripts/   # Automation scripts
├── test/          # Testing environment
├── bmad/          # BMAD framework integration
└── docs/          # Project documentation
```

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| OS | Linux, macOS | Linux, macOS |
| CPU | 2 cores | 8 cores |
| Memory | 6GB | 16GB |
| Disk | 20GB | 100GB |

## License

Apache License 2.0
