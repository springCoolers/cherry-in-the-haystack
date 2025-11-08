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

{{decision_table_rows}}

## Project Structure

```
{{project_root}}/
{{source_tree}}
```

## Epic to Architecture Mapping

{{epic_mapping_table}}

## Technology Stack Details

### Core Technologies

{{core_stack_details}}

### Integration Points

{{integration_details}}

{{novel_pattern_designs_section}}

## Implementation Patterns

These patterns ensure consistent implementation across all AI agents:

{{implementation_patterns}}

## Consistency Rules

### Naming Conventions

{{naming_conventions}}

### Code Organization

{{code_organization_patterns}}

### Error Handling

{{error_handling_approach}}

### Logging Strategy

{{logging_approach}}

## Data Architecture

{{data_models_and_relationships}}

## API Contracts

{{api_specifications}}

## Security Architecture

{{security_approach}}

## Performance Considerations

{{performance_strategies}}

## Deployment Architecture

{{deployment_approach}}

## Development Environment

### Prerequisites

{{development_prerequisites}}

### Setup Commands

```bash
{{setup_commands}}
```

## Architecture Decision Records (ADRs)

{{key_architecture_decisions}}

---

_Generated by BMAD Decision Architecture Workflow v1.3.2_
_Date: 2025-11-08_
_For: HK_
