# Reference Documentation

This folder contains all reference documentation for the **cherry-in-the-haystack** project.

## Project Overview

**cherry-in-the-haystack** is a fork of [auto-news](https://github.com/finaldie/auto-news), an automatic news aggregator with LLM capabilities.

### What We're Building

We're extending auto-news with advanced knowledge management capabilities:

1. **Chunk-level Deduplication Agents**: Intelligent deduplication at the content chunk level to eliminate redundancy
2. **MECE Knowledge Base**: Mutually Exclusive, Collectively Exhaustive knowledge organization with compare/contrast capabilities
3. **Jupyter Book-style UI**: Modern, book-like interface for knowledge exploration

---

## Documentation Index

### 1. Notion Exports (Product Planning)

Our product planning and requirements documentation:

- **[Cherry Product Overview](notion-export/Cherry%20Product%20Overview%20(250813).md)** - High-level product vision and overview
- **[Product Development](notion-export/product%20development.md)** - Development approach and methodology
- **[Requirements Document](notion-export/requirements%20document.md)** - Detailed requirements and specifications

### 2. Upstream auto-news Documentation

Original project documentation:

- **[auto-news README](auto-news-upstream/autonews-README.md)** - Complete documentation of the original auto-news project
- **[auto-news Wiki](https://github.com/finaldie/auto-news/wiki)** - Comprehensive wiki with setup guides and features
- **[Original Repository](https://github.com/finaldie/auto-news)** - Source repository we forked from

#### Key auto-news Features (Foundation)

- RSS/Reddit/Twitter feed aggregation with LLM-powered insights
- YouTube video transcript analysis
- Web article insights generation
- Content filtering based on interests
- Weekly recap generation
- Notion-based reading experience
- TODO list generation from takeaways
- Journal note organization
- Multi-LLM backend support (OpenAI, Google Gemini, Ollama)

---

## Architecture Context

### Current auto-news Architecture

- **Backend**: Python-based with Apache Airflow for workflow orchestration
- **Data Storage**: ChromaDB for vector storage
- **LLM Integration**: Multiple provider support
- **Distribution**: Kubernetes-ready with Helm charts
- **Frontend**: Notion-based interface

### Our Additions (cherry-in-the-haystack)

We're building on top of this foundation:

1. **Deduplication Layer**:
   - New agents for chunk-level analysis
   - Semantic similarity detection
   - Intelligent content merging

2. **Knowledge Organization**:
   - MECE structure implementation
   - Compare/contrast engine
   - Relationship mapping between content

3. **New UI Layer**:
   - Jupyter Book-inspired frontend
   - Rich content rendering
   - Navigation and search

---

## For AI Agents & Developers

When working on this project, consider:

### Key Constraints

- Must maintain compatibility with existing auto-news data pipeline
- Existing Airflow DAGs handle data collection and processing
- ChromaDB is the vector storage layer
- Multi-LLM backend must remain flexible

### Integration Points

- Hook into existing content processing pipeline for deduplication
- Extend data model for MECE knowledge structure
- New UI layer should consume existing Notion content or migrate it

### Dependencies

- Python (existing codebase)
- Apache Airflow (workflow orchestration)
- ChromaDB (vector database)
- LLM providers (OpenAI/Gemini/Ollama)
- Additional: Frontend framework TBD for Jupyter Book UI

---

## Quick Links

- **Upstream Project**: https://github.com/finaldie/auto-news
- **Upstream Wiki**: https://github.com/finaldie/auto-news/wiki
- **Upstream Blog Post**: https://finaldie.com/blog/auto-news-an-automated-news-aggregator-with-llm/
- **Video Introduction**: https://www.youtube.com/watch?v=hKFIyfAF4Z4
- **Data Flows Video**: https://www.youtube.com/watch?v=WAGlnRht8LE

---

## Document Usage

These reference documents should be consulted when:

1. **Planning Phase (PRD)**: Understanding requirements and product vision
2. **Architecture Phase**: Designing integration with existing auto-news architecture
3. **Implementation**: Ensuring compatibility and understanding existing patterns
4. **Testing**: Validating against original requirements

---

*Last Updated: 2025-11-07*
*Project: cherry-in-the-haystack*
*Track: BMad Method (Brownfield)*
