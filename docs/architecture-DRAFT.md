# Architecture - DRAFT IN PROGRESS

**Project:** cherry-in-the-haystack (The LLM Engineering Handbook)
**Author:** HK
**Date:** 2025-11-08
**Status:** 🚧 DRAFT - Architecture workflow in progress

---

## Progress Summary

**Completed Steps:**
- ✅ Step 1: Loaded and understood project context (PRD, Epics)
- ✅ Step 2: Evaluated starter templates (Jupyter Book already running)
- ✅ Step 3: Identified remaining architectural decisions

**Next Step:** Step 4 - Make collaborative architectural decisions

---

## Project Context

### Project Overview
The LLM Engineering Handbook evolves from a personal content curation tool (Auto-News) into a living, community-driven knowledge base serving as the default reference for AI builders.

**Scale:**
- 6 epics with 40 total stories
- MVP: 27 stories (Epics 1-4)
- Growth: 13 stories (Epics 5-6)

**Core Architecture:**
```
Stage 1: Auto-News Ingestion (Twitter, Discord, GitHub, RSS, Papers)
  ↓ Deduplication (vector similarity)
  ↓ AI Scoring (1-5 scale)
Stage 2: Human Peer Review in Notion (weekly approval)
  ↓
Stage 3: AI Synthesis (MECE knowledge structure)
  ↓
Stage 4: Automated Publication (Postgres → GitHub → Jupyter Book → GitHub Pages)
```

### Critical NFRs
- **Performance:** < 2 second page loads, < 5 minute Jupyter Book builds
- **Freshness:** Weekly "Newly Discovered" updates, 48-hour publish cycle
- **Quality:** 90%+ approval rating, multi-stage quality gates
- **Scale:** Support 1,000+ pages, 50,000 monthly visitors, 50+ contributors

---

## Architectural Decisions to Make

### CRITICAL (Block Everything)

#### 1. Database Infrastructure
**Decision:** Postgres Hosting Choice
- Options: Self-hosted, Supabase, Neon, Railway, Render
- Considerations: Cost, scaling, backup/restore, connection pooling
- **Status:** ⏸️ PENDING

**Decision:** Vector Database Provider
- Options: ChromaDB (free/self-hosted), Milvus, Pinecone (paid)
- Considerations: Cost, performance, embedding dimensions, scaling
- **Status:** ⏸️ PENDING

#### 2. LLM Provider Strategy
**Decision:** Primary LLM Provider
- Options: OpenAI (GPT-4), Anthropic (Claude), Google (Gemini), Ollama (local)
- Considerations: Cost per token, quality, rate limits, context windows
- **Status:** ⏸️ PENDING

**Decision:** Fallback Pattern
- Options: Single provider with retry, or multi-provider with automatic failover
- **Status:** ⏸️ PENDING

#### 3. Monorepo Organization
**Decision:** Repository Structure
- Options: Keep current structure and extend, or refactor into formal monorepo pattern
- Where does Jupyter Book content live?
- **Status:** ⏸️ PENDING

### IMPORTANT (Shape Architecture)

#### 4. Auto-News DAG Adaptation
**Decision:** Operator Reuse Strategy
- Which Auto-News operators are reusable vs need modification?
- Separate DAG for handbook pipeline or extend existing?
- **Status:** ⏸️ PENDING

#### 5. Postgres → GitHub Automation
**Decision:** Automation Tool Choice
- Options: Python script, GitHub Actions, or dedicated service
- Git Strategy: Direct commits vs PR workflow
- **Status:** ⏸️ PENDING

#### 6. Content Processing Pipeline
**Decision:** Embedding Model
- Options: OpenAI text-embedding-3-small, sentence-transformers (local)
- **Status:** ⏸️ PENDING

**Decision:** Deduplication Thresholds
- Content-level: 0.85? 0.90?
- Chunk-level: 0.90? 0.95?
- **Status:** ⏸️ PENDING

#### 7. Integration Architecture
**Decision:** Notion Integration
- Continue using Notion for human review or build custom UI?
- **Status:** ⏸️ PENDING

**Decision:** GitHub Actions Workflow
- Trigger on every commit or scheduled?
- **Status:** ⏸️ PENDING

### NICE-TO-HAVE (Can Defer)

#### 8. Development Environment
- Dependency Management: Poetry, pip-tools, or requirements.txt?
- Docker Compose for local development?

#### 9. Testing Strategy
- Test Framework: pytest?
- Coverage Targets?

#### 10. Monitoring & Observability
- Logging format?
- Alerting channels?

---

## Resume Instructions

To resume this architecture workflow, run:

```bash
/bmad:bmm:workflows:architecture
```

The workflow will load this draft and continue from Step 4: Making collaborative architectural decisions.

---

## Existing Infrastructure

### Current Tech Stack (from Auto-News)
- **Python:** 3.11+
- **Orchestration:** Apache Airflow 2.8.4
- **LLM Framework:** LangChain 0.3.1, LlamaIndex, AutoGen
- **Data Processing:** Pandas, custom operators
- **Output:** Notion integration

### Web Interface (Already Running)
- **Static Site:** Jupyter Book
- **Hosting:** GitHub Pages
- **Deployment:** GitHub Actions

---

_This is a draft document. It will be completed during the architecture workflow._

_Generated: 2025-11-08_
_Last Updated: 2025-11-08 (Session paused)_
