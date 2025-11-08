# cherry-in-the-haystack - Epic Breakdown

**Author:** HK
**Date:** 2025-11-08
**Project Level:** Medium
**Target Scale:** 50,000 monthly users within 6 months

---

## Overview

This document provides the complete epic and story breakdown for cherry-in-the-haystack, decomposing the requirements from the [PRD](./PRD.md) into implementable stories.

### Epic Summary

This project delivers **The LLM Engineering Handbook** through 6 sequential and parallel epics:

**Phase 1: Core MVP (Sequential - Epics 1-4)**
- **Epic 1: Foundation & Core Infrastructure** - Establish technical foundation and transform Auto-News codebase
- **Epic 2: Intelligent Content Ingestion Pipeline** - Automated multi-source aggregation with AI-powered quality scoring
- **Epic 3: AI-Powered Knowledge Synthesis** - MECE taxonomy and intelligent content synthesis
- **Epic 4: Automated Publication System** - Postgres → GitHub → Jupyter Book pipeline with weekly updates

**Phase 2: Community & Quality (Parallel - Epics 5-6)**
- **Epic 5: Community Contribution Framework** - Enable collective intelligence through GitHub PR workflow
- **Epic 6: Content Quality & Lifecycle Management** - Maintain trust through quality controls and freshness

**Delivery Strategy:**
- Epics 1-4 must complete sequentially to deliver working MVP
- Epics 5-6 enhance the MVP and can run in parallel
- Each story is vertically sliced for single-session dev agent completion
- Stories use BDD acceptance criteria for clarity and testability

**Product Magic Delivered:**
- 🌟 **Clarity** - MECE structure helps users say "now I understand"
- 🌟 **Confidence** - Quality curation users can trust
- 🌟 **Speed** - Weekly updates keep handbook feeling alive
- 🌟 **Community Intelligence** - Knowledge that compounds instead of fades

---

## Epic 1: Foundation & Core Infrastructure

**Goal:** Establish a solid technical foundation that transforms the existing Auto-News infrastructure into a handbook-ready platform, enabling all subsequent development work.

**Value:** This epic creates the foundation that allows the team to build, test, and deploy the handbook efficiently. Without this infrastructure, no content pipeline or publication can function.

---

### Story 1.1: Project Initialization and Repository Setup

As a **developer**,
I want **a clean, well-organized project repository with proper structure and documentation**,
So that **the team can collaborate effectively and follow consistent development practices**.

**Acceptance Criteria:**

**Given** the existing Auto-News codebase exists
**When** I initialize the handbook project repository
**Then** the repository includes:
- Clear directory structure separating handbook code from Auto-News dependencies
- README.md with project overview, setup instructions, and architecture summary
- .gitignore configured for Python, Node.js, and environment files
- requirements.txt or pyproject.toml for Python dependencies
- package.json for any Node.js/frontend dependencies
- LICENSE file (appropriate open-source license)
- CONTRIBUTING.md with contribution guidelines
- Development environment setup guide

**And** the repository has proper branch protection rules on main branch

**And** GitHub repository settings configured (description, topics, website URL)

**Prerequisites:** None (this is the first story)

**Technical Notes:**
- Keep Auto-News codebase in separate directory (e.g., `/auto-news-engine/`)
- Handbook-specific code in `/handbook/` or root level
- Use poetry or pip-tools for dependency management
- Consider monorepo structure if Auto-News and handbook share significant code

---

### Story 1.2: Database Infrastructure Setup

As a **backend engineer**,
I want **Postgres database configured with proper schemas for content storage**,
So that **we can store ingested content, review status, and processed items reliably**.

**Acceptance Criteria:**

**Given** the project repository is initialized
**When** I set up the database infrastructure
**Then** Postgres database is provisioned with:
- Database schema for raw ingested content (source, URL, date, category, raw_text)
- Database schema for scored content (content_id, score, reviewer_id, approval_status)
- Database schema for approved content (approved_date, category, processed_markdown)
- Proper indexes on frequently queried fields (date, category, approval_status)
- Migration scripts using Alembic or similar tool

**And** database connection configuration uses environment variables (not hardcoded)

**And** basic CRUD operations tested with sample data

**Prerequisites:** Story 1.1 (repository setup)

**Technical Notes:**
- Consider PostgreSQL hosted options: Supabase, Railway, Neon, or self-hosted
- Schema design should support idempotent inserts (prevent duplicates)
- Include created_at, updated_at timestamps for audit trail
- Design for future scaling (proper normalization)
- Keep vector embeddings separate from relational data initially

---

### Story 1.3: Vector Database Foundation

As a **ML engineer**,
I want **vector database initialized for semantic deduplication and similarity search**,
So that **we can efficiently detect duplicate content and enable future semantic search**.

**Acceptance Criteria:**

**Given** the project has database infrastructure
**When** I set up the vector database
**Then** vector database is configured with:
- Selected provider (ChromaDB, Milvus, or Pinecone) integrated
- Collection/index for content embeddings
- Embedding model selected (e.g., OpenAI text-embedding-3-small, sentence-transformers)
- Basic insert and similarity search operations working
- Configuration for cosine similarity threshold (e.g., 0.85 for duplicates)

**And** vector database connection uses environment variables

**And** sample embeddings stored and queried successfully

**Prerequisites:** Story 1.2 (database setup)

**Technical Notes:**
- Start with ChromaDB for simplicity (local or cloud)
- Embedding dimension should match model (e.g., 1536 for OpenAI, 384 for MiniLM)
- Store metadata alongside vectors (content_id, category, date)
- Plan for migration path between providers
- Consider cost: ChromaDB (free/self-hosted) vs Pinecone (paid)

---

### Story 1.4: Auto-News Engine Adaptation

As a **backend engineer**,
I want **existing Auto-News DAGs adapted for handbook-specific content sources**,
So that **we can reuse proven ingestion logic while targeting LLM-focused sources**.

**Acceptance Criteria:**

**Given** Auto-News codebase is available in the repository
**When** I adapt the engine for handbook use case
**Then** the adapted system:
- Identifies and documents which Auto-News operators are reusable
- Configures source list for LLM-focused channels (Twitter accounts, Discord servers, GitHub repos, RSS feeds)
- Updates categorization logic for handbook categories (Basics, Advanced, Newly Discovered subcategories)
- Ensures deduplication logic runs before scoring (cost optimization)
- Outputs to handbook Postgres schema (not original Notion structure)

**And** Airflow DAGs are runnable in development environment

**And** test run successfully ingests from at least 3 sources

**Prerequisites:** Story 1.2 (database setup)

**Technical Notes:**
- Reference: `bmad/docs/reference/auto-news-upstream/autonews-README.md`
- May need to update operator interfaces for new database schema
- Keep Auto-News operational for any existing users during transition
- Consider extracting core logic into shared library

---

### Story 1.5: GitHub Actions CI/CD Pipeline

As a **DevOps engineer**,
I want **automated CI/CD pipeline for testing and deployment**,
So that **code changes are validated automatically and deployments are reliable**.

**Acceptance Criteria:**

**Given** the repository has code and tests
**When** I configure GitHub Actions workflows
**Then** the CI/CD pipeline includes:
- **Continuous Integration workflow** that runs on PRs:
  - Linting (flake8, black, or ruff)
  - Unit tests with pytest
  - Type checking (mypy) if using type hints
  - Dependency security scanning (e.g., safety, pip-audit)
- **Deployment workflow** that runs on main branch push:
  - Builds Jupyter Book from markdown files
  - Deploys to GitHub Pages (gh-pages branch)
  - Reports deployment status
- Workflow status badges in README.md

**And** workflows complete in under 10 minutes

**And** failed workflows send notifications (GitHub notifications or Slack)

**Prerequisites:** Story 1.1 (repository setup)

**Technical Notes:**
- Use GitHub Actions cache to speed up dependency installation
- Separate CI (fast feedback) from deployment (slower, only on main)
- Consider matrix testing for multiple Python versions if needed
- GitHub Pages deployment uses `peaceiris/actions-gh-pages` or similar

---

### Story 1.6: Jupyter Book Configuration

As a **frontend developer**,
I want **Jupyter Book configured with basic theme and structure**,
So that **we have a professional documentation site ready for content**.

**Acceptance Criteria:**

**Given** the repository has handbook content structure
**When** I configure Jupyter Book
**Then** the configuration includes:
- `_config.yml` with project metadata (title, author, logo)
- `_toc.yml` defining 3-section structure (Basics, Advanced, Newly Discovered)
- Theme customization (colors, fonts matching brand)
- Required extensions installed:
  - sphinx-design (card layouts)
  - sphinx-togglebutton (collapsible sections)
  - sphinxext-opengraph (social previews)
- Sample placeholder content in each section
- Local build script for development (`jupyter-book build`)

**And** Jupyter Book builds successfully without errors

**And** built HTML is viewable locally in browser

**Prerequisites:** Story 1.1 (repository setup)

**Technical Notes:**
- Create placeholder files: `basics/index.md`, `advanced/index.md`, `newly-discovered/index.md`
- Custom CSS for branding in `_static/custom.css`
- Maximum 2-level TOC depth enforced
- Consider using Jupyter Book's built-in search (no additional setup)

---

### Story 1.7: Development Environment and Testing Infrastructure

As a **developer**,
I want **documented development environment setup and testing framework**,
So that **new contributors can start quickly and code quality is maintained**.

**Acceptance Criteria:**

**Given** the project has core infrastructure
**When** I set up development tooling
**Then** the development environment includes:
- Virtual environment setup instructions (venv or poetry)
- Local environment variables template (`.env.example`)
- Docker Compose file for local Postgres and vector DB (optional but recommended)
- Pre-commit hooks configured (linting, formatting)
- Test fixtures and sample data for development
- Testing documentation (how to run tests, write new tests, test data location)

**And** `pytest` test framework configured with:
- Unit tests directory structure (`tests/unit/`)
- Integration tests directory (`tests/integration/`)
- Test coverage reporting (pytest-cov)
- Minimum coverage threshold set (e.g., 70%)

**And** a new developer can set up environment in under 30 minutes following README

**Prerequisites:** Stories 1.1, 1.2, 1.3 (repository, database, vector DB)

**Technical Notes:**
- Use `python-dotenv` for environment variable management
- Docker Compose makes onboarding much faster (include Postgres, ChromaDB)
- Pre-commit config: `pre-commit install` in setup instructions
- Include sample API keys or mock credentials for testing
- Document external dependencies (Notion API, OpenAI API, etc.)

---

## Epic 2: Intelligent Content Ingestion Pipeline

**Goal:** Build an automated content ingestion system that discovers, deduplicates, and scores LLM-related content from multiple sources, surfacing only the highest-quality material for human review.

**Value:** This epic delivers the core "signal from noise" capability - automatically filtering the 80% noise so users only see valuable insights. This is the engine that enables weekly updates and comprehensive coverage without overwhelming reviewers.

---

### Story 2.1: Multi-Source Content Aggregation

As a **content curator**,
I want **Auto-News to pull from 10+ LLM-focused sources automatically**,
So that **we capture comprehensive coverage of the LLM ecosystem without manual monitoring**.

**Acceptance Criteria:**

**Given** the Auto-News engine is adapted for handbook use
**When** I configure content sources
**Then** the system successfully pulls from:
- At least 5 Twitter accounts (e.g., @AnthropicAI, @OpenAI, key researchers)
- At least 2 Discord servers (with proper bot permissions)
- At least 3 GitHub organizations/repositories (releases, discussions)
- At least 3 RSS feeds (blogs, newsletters)
- Papers from arXiv (LLM-related categories)

**And** each source includes metadata: source_type, source_name, URL, poll_frequency

**And** source health monitoring tracks last successful pull and error rate

**And** content is stored in raw_content table with source attribution

**Prerequisites:** Story 1.4 (Auto-News engine adaptation)

**Technical Notes:**
- Use existing Auto-News operators where possible
- Twitter: May need official API or scraping (consider rate limits)
- Discord: Requires bot with MESSAGE_READ permissions
- GitHub: Use GitHub API for releases, discussions, issues
- Implement exponential backoff for failed pulls
- Consider source priority levels (high/medium/low)

---

### Story 2.2: Content-Level Deduplication

As a **backend engineer**,
I want **duplicate content identified and filtered before AI scoring**,
So that **we reduce API costs and don't show users the same news repeated multiple times**.

**Acceptance Criteria:**

**Given** raw content is ingested from multiple sources
**When** the deduplication process runs
**Then** the system:
- Generates embeddings for each content item (title + first 500 chars)
- Queries vector database for similar content (cosine similarity > 0.85)
- Marks duplicate items with reference to original
- Only processes unique content for scoring
- Preserves all source URLs for duplicate cluster

**And** deduplication completes within 100ms per item

**And** 95%+ accuracy in identifying true duplicates (test with known duplicates)

**And** duplicate detection results logged for quality monitoring

**Prerequisites:** Story 1.3 (vector database), Story 2.1 (content aggregation)

**Technical Notes:**
- Embedding model: OpenAI text-embedding-3-small or sentence-transformers
- Store embeddings in vector DB with metadata (content_id, source, date)
- Consider URL normalization (same article, different UTM parameters)
- Keep first-seen original, mark later ones as duplicates
- Weekly review of false positives/negatives

---

### Story 2.3: AI-Powered Quality Scoring

As a **ML engineer**,
I want **AI agent to automatically score content quality on 1-5 scale**,
So that **only top-tier content (score 5) reaches human reviewers**.

**Acceptance Criteria:**

**Given** unique content items are identified
**When** the AI scoring agent runs
**Then** each item receives a score (1-5) based on:
- **Relevance:** Direct impact on LLM engineering practices
- **Depth:** Substantial insight vs surface-level announcement
- **Novelty:** New information vs rehashed content
- **Practicality:** Actionable for practitioners

**And** scoring prompt includes:
- Clear rubric for each score level
- Examples of score-5 content
- Context about handbook goals (clarity, confidence, speed)

**And** scoring completes within 5 minutes for batches of 100 items

**And** only score-5 items are queued for human review

**And** scores are stored with reasoning/justification for auditability

**Prerequisites:** Story 2.2 (deduplication)

**Technical Notes:**
- Use structured output (JSON) for score + reasoning
- Consider multi-LLM provider support (OpenAI, Anthropic, Ollama fallback)
- Implement retry logic with exponential backoff
- Track API costs per scoring run
- Scoring prompt should be version-controlled and improvable
- Pattern learning: Track human override rate to improve scoring

---

### Story 2.4: Notion Review Workflow Integration

As a **content reviewer**,
I want **score-5 items automatically sent to Notion for weekly human review**,
So that **I can efficiently approve or reject high-quality content in one place**.

**Acceptance Criteria:**

**Given** content items scored as 5 by AI
**When** the Notion sync process runs
**Then** each score-5 item creates a Notion database entry with:
- Title, source URL, publication date, category
- AI score reasoning
- Full content preview
- Review status field (Pending, Approved, Rejected)
- Reviewer assignment field
- Tags for easy filtering

**And** Notion API rate limits are respected (3 requests/second)

**And** bidirectional sync: approvals in Notion update Postgres status

**And** weekly batch review workflow documented for reviewers

**And** automated reminder sent to reviewers on review day

**Prerequisites:** Story 2.3 (AI scoring)

**Technical Notes:**
- Use Notion API v2
- Create dedicated Notion database for handbook review
- Notion webhook or polling for status changes
- Handle Notion API errors gracefully (retry, fallback to manual)
- Consider Notion export capability if migration needed
- Document Notion workspace setup for new reviewers

---

### Story 2.5: Approval Queue and Status Tracking

As a **content manager**,
I want **clear visibility into content pipeline status from ingestion to approval**,
So that **I can monitor health, identify bottlenecks, and ensure weekly publish cadence**.

**Acceptance Criteria:**

**Given** content flows through the pipeline stages
**When** I check pipeline status
**Then** I can see:
- Content items by status: Ingested, Deduplicated, Scored, In Review, Approved, Rejected, Published
- Weekly metrics: total ingested, unique items, score-5 count, approval rate
- Bottleneck alerts: items stuck in review > 7 days
- Source performance: items per source, approval rate by source

**And** status dashboard includes:
- Daily/weekly ingestion volume charts
- Score distribution (1-5 across all content)
- Review velocity (time from score-5 to approval)
- Top performing sources

**And** alerts sent for critical issues:
- No approvals in current week (Thursday check)
- Source failures (3+ consecutive failures)
- AI scoring errors > 10% rate

**Prerequisites:** Stories 2.1, 2.2, 2.3, 2.4 (full pipeline)

**Technical Notes:**
- Use Airflow UI for DAG monitoring (existing capability)
- Build custom dashboard with Streamlit or Grafana
- Store metrics in Postgres (time-series optimized)
- Email/Slack alerts for critical issues
- Weekly summary report generation

---

### Story 2.6: Category Classification and Tagging

As a **content curator**,
I want **content automatically categorized into handbook sections and tagged**,
So that **approved content flows to the correct handbook section without manual sorting**.

**Acceptance Criteria:**

**Given** content item is scored and queued for review
**When** the classification process runs
**Then** each item is assigned:
- **Primary section:** Basics, Advanced, or Newly Discovered
- **Secondary category** (for Newly Discovered):
  - Model Updates
  - Framework/Library/Tools Updates
  - Productivity Tools
  - Business Cases & Case Studies
  - How People Use AI
- **Tags:** relevant keywords (e.g., "RAG", "fine-tuning", "GPT-4", "LangChain")

**And** classification uses AI with clear rules:
- Basics: Foundational concepts from established resources
- Advanced: Deep technical content requiring expertise
- Newly Discovered: Fresh, time-sensitive updates

**And** classification accuracy validated by human reviewers

**And** reviewers can override AI classification in Notion

**Prerequisites:** Story 2.4 (Notion workflow)

**Technical Notes:**
- Use LLM with structured output for classification
- Provide classification rubric in prompt
- Track classification accuracy (human override rate)
- Support evolving taxonomy (new categories, deprecated tags)
- Consider hierarchical tags (parent: RAG, child: multi-hop, hybrid)

---

## Epic 3: AI-Powered Knowledge Synthesis

**Goal:** Transform raw approved content into structured, synthesized knowledge organized in a MECE taxonomy that helps users gain clarity and understanding.

**Value:** This epic delivers the "Clarity" promise - the structured knowledge map that helps users say "now I understand". It takes scattered content and creates cohesive, well-organized explanations.

---

### Story 3.1: MECE Taxonomy Design and Implementation

As a **knowledge architect**,
I want **a clear, logical taxonomy that is Mutually Exclusive and Collectively Exhaustive**,
So that **users can navigate handbook without confusion, gaps, or overlaps**.

**Acceptance Criteria:**

**Given** we understand the LLM engineering landscape
**When** I design the taxonomy
**Then** the structure includes:
- **3 main sections:** Basics, Advanced, Newly Discovered
- **Parent-child hierarchy** (maximum 2 levels):
  - Basics: 6 parent topics (Prompting, RAG, Fine-tuning, Agents, Embeddings, Evaluation)
  - Advanced: Same 6 domains with advanced sub-topics
  - Newly Discovered: 5 categories (Model Updates, Framework Updates, Productivity Tools, Business Cases, How People Use AI)
- **Navigation structure** encoded in `_toc.yml` for Jupyter Book

**And** taxonomy documented with:
- Clear definitions for each section
- Decision criteria for content placement
- Examples of content that fits each category

**And** taxonomy supports evolution (new topics can be added without restructure)

**Prerequisites:** None (design work)

**Technical Notes:**
- Document taxonomy in `taxonomy.md` for consistency
- Create placeholder index pages for each parent topic
- Build taxonomy validation script (checks content fits rules)
- Plan for "uncategorized" items that don't fit cleanly

---

### Story 3.2: Chunk-Level Deduplication for Synthesis

As a **ML engineer**,
I want **paragraph-level deduplication for Basics/Advanced content**,
So that **synthesized pages don't contain redundant information from multiple sources**.

**Acceptance Criteria:**

**Given** curated text sources (PDFs, books, blog posts) for Basics/Advanced sections
**When** the chunk-level deduplication runs
**Then** the system:
- Splits documents into paragraphs/chunks (semantic boundaries, not just newlines)
- Generates embeddings for each chunk
- Identifies similar chunks across sources (cosine similarity > 0.90)
- Marks unique vs duplicate chunks
- Preserves source attribution for each unique chunk

**And** deduplication works incrementally (new content compared to existing)

**And** similar concepts from different perspectives are preserved (not over-deduplicated)

**Prerequisites:** Story 1.3 (vector database), Story 3.1 (taxonomy)

**Technical Notes:**
- Use semantic chunking (not fixed-size) - respect sentence/paragraph boundaries
- Higher similarity threshold than content-level (0.90 vs 0.85) - more conservative
- Store chunk embeddings with metadata (source, page, parent_topic)
- Handle multi-perspective content (same concept, different explanations)
- Consider LangChain or LlamaIndex for chunking

---

### Story 3.3: AI Synthesis Engine for Basics Section

As a **content creator**,
I want **AI to synthesize curated sources into cohesive Basics topic pages**,
So that **users get distilled, well-structured introductions to foundational concepts**.

**Acceptance Criteria:**

**Given** unique chunks from curated sources for a Basics topic
**When** the synthesis engine runs
**Then** it generates:
- **Overview:** Clear introduction explaining the concept
- **Core Concepts:** Key ideas broken down with examples
- **Practical Examples:** Real-world use cases and code snippets
- **Trade-offs:** When to use vs not use
- **Further Reading:** Links to original sources

**And** synthesized content:
- Cites original sources inline
- Maintains accuracy (no hallucinations)
- Uses clear, accessible language
- Includes diagrams/visualizations where helpful (placeholder for human creation)
- Follows consistent format across all Basics pages

**And** synthesis quality validated by human reviewer before publication

**Prerequisites:** Story 3.2 (chunk deduplication)

**Technical Notes:**
- Multi-stage synthesis: extract key points → organize → generate prose → cite sources
- Use structured output for consistency
- Long context LLM beneficial (Claude with 200k context, GPT-4 Turbo)
- Store synthesis prompts in version control
- Human-in-the-loop for final review

---

### Story 3.4: AI Synthesis Engine for Advanced Section

As a **technical writer**,
I want **AI to synthesize deep technical content for Advanced topics**,
So that **experienced practitioners find substantial, detailed information**.

**Acceptance Criteria:**

**Given** unique chunks from curated sources for an Advanced topic
**When** the synthesis engine runs
**Then** it generates:
- **Deep Dive:** Comprehensive technical explanation
- **Implementation Details:** Architecture patterns, algorithms, code examples
- **Performance Considerations:** Benchmarks, optimization techniques
- **Edge Cases:** Common pitfalls and how to handle them
- **Research Context:** Recent papers, state-of-the-art approaches

**And** synthesized content:
- Assumes reader has basics knowledge (links to Basics sections)
- Includes mathematical notation where appropriate
- Provides production-ready code examples
- Cites academic papers and technical blogs
- Highlights conflicting information with analysis

**And** Advanced content reviewed by domain experts before publication

**Prerequisites:** Story 3.3 (Basics synthesis), Story 3.2 (chunk deduplication)

**Technical Notes:**
- Similar process to Basics synthesis but different prompt/tone
- Longer, more detailed pages acceptable for Advanced
- May need multiple LLM calls for complex topics
- Technical accuracy is critical - prioritize expert review
- Include "last updated" dates (research moves fast)

---

### Story 3.5: Parent-Child Content Hierarchy

As a **handbook user**,
I want **clear navigation from parent concepts to child implementations**,
So that **I can start broad and drill down into specific techniques**.

**Acceptance Criteria:**

**Given** synthesized content for parent and child topics
**When** I navigate the handbook
**Then** each parent page:
- Provides high-level overview of the domain
- Links to all child pages with brief descriptions
- Shows "what you'll learn" for each child topic
- Indicates difficulty level or prerequisites

**And** each child page:
- References parent page for context
- Provides focused, specific content
- Links to related child pages (e.g., "Naive RAG" → "Advanced RAG")
- Shows breadcrumb navigation (Parent → Child)

**And** maximum 2-level depth enforced (no grandchildren)

**And** Jupyter Book TOC reflects this structure clearly

**Prerequisites:** Stories 3.3, 3.4 (synthesized content)

**Technical Notes:**
- Enforce hierarchy in `_toc.yml` configuration
- Use Jupyter Book sections and chapters
- Breadcrumbs via Jupyter Book theme
- Cross-references use MyST-NB link syntax
- Consider "you might also like" recommendations

---

### Story 3.6: Content Freshness and Update Triggers

As a **content maintainer**,
I want **automated detection of stale content requiring updates**,
So that **handbook remains accurate as the LLM field evolves**.

**Acceptance Criteria:**

**Given** Basics/Advanced content has been published
**When** the staleness detection runs (weekly)
**Then** it flags content needing review if:
- Major version release of mentioned framework (e.g., LangChain 0.2 → 0.3)
- New research contradicts established techniques
- Content older than 6 months without recent validation
- High user feedback indicating outdated information

**And** flagged content creates GitHub issue with:
- Page link, staleness reason, suggested update source
- Priority level (critical, high, medium, low)
- Assigned to content team member

**And** "last reviewed" date shown on each page

**And** update workflow documented for contributors

**Prerequisites:** Story 3.4 (Advanced synthesis)

**Technical Notes:**
- Track framework versions mentioned in content
- Use GitHub API to monitor releases for tracked projects
- Store "last_reviewed_date" in page frontmatter
- Manual validation still required (automation suggests, humans decide)
- Consider using AI to draft update proposals

---

### Story 3.7: Evolving Taxonomy Management

As a **product manager**,
I want **ability to add new categories and migrate content as field evolves**,
So that **handbook taxonomy stays relevant without major rewrites**.

**Acceptance Criteria:**

**Given** a new important LLM topic emerges (e.g., "Multimodal AI")
**When** I add it to taxonomy
**Then** the process includes:
- Create new parent topic page with definition
- Update `_toc.yml` to include new section
- Migrate relevant content from "Newly Discovered" if applicable
- Update taxonomy documentation
- Notify contributors of new category

**And** deprecated categories can be:
- Merged into other categories (with redirects)
- Archived with explanation
- Content preserved in git history

**And** taxonomy changes don't break existing links (redirects maintained)

**And** taxonomy review happens quarterly

**Prerequisites:** Story 3.1 (initial taxonomy)

**Technical Notes:**
- Document taxonomy change process in `CONTRIBUTING.md`
- Use Jupyter Book redirects for moved/deprecated pages
- Git tags for taxonomy versions (v1.0, v1.1, etc.)
- Announce taxonomy changes to contributors
- Gradual migration preferred over big-bang changes

---

## Epic 4: Automated Publication System

**Goal:** Build end-to-end automation that takes approved content from Postgres, commits to GitHub, builds Jupyter Book, and deploys to public site - delivering fresh content to users within hours.

**Value:** This epic delivers the "Speed" promise - weekly updates that keep the handbook feeling "alive". It completes the automation chain from human approval to public site.

---

### Story 4.1: Postgres to GitHub Markdown Pipeline

As a **automation engineer**,
I want **approved content automatically converted to markdown and committed to GitHub**,
So that **weekly batch publications happen without manual intervention**.

**Acceptance Criteria:**

**Given** content items approved in Notion and synced to Postgres
**When** the weekly batch job runs (or manual trigger)
**Then** the pipeline:
- Queries Postgres for approved items since last publish
- Converts each item to markdown with proper frontmatter (title, date, category, tags, source URL)
- Organizes files by category folder structure (`newly-discovered/model-updates/2025-11-08-gpt45-release.md`)
- Creates git commit with descriptive message (e.g., "Weekly publish: 15 items (2025-11-08)")
- Pushes directly to main branch (automated committer)

**And** idempotent: re-running doesn't create duplicates

**And** commit includes all metadata changes (updates, not just new items)

**And** pipeline logs all actions for audit trail

**And** rollback capability if batch contains errors

**Prerequisites:** Story 2.5 (approval queue), Story 1.5 (GitHub Actions)

**Technical Notes:**
- Use GitHub API or git CLI for commits
- Automated committer: dedicated service account or bot
- Markdown template with consistent frontmatter format
- Handle special characters in filenames (sanitize titles)
- Consider using conventional commits format
- Dry-run mode for testing

---

### Story 4.2: Jupyter Book Theme Customization

As a **UI/UX designer**,
I want **Jupyter Book styled with custom branding and visual design**,
So that **handbook has professional, distinct visual identity**.

**Acceptance Criteria:**

**Given** basic Jupyter Book is configured
**When** I apply custom styling
**Then** the handbook includes:
- **Brand colors:** Primary, secondary, accent colors applied throughout
- **Logo:** Project logo in header/nav
- **Typography:** Clear, readable fonts (headers, body, code)
- **Custom CSS:** Additional styling in `_static/custom.css`
- **Favicon:** Custom icon for browser tabs
- **Footer:** Copyright, license, contribution link

**And** styling is mobile-responsive

**And** maintains accessibility (sufficient contrast, readable font sizes)

**And** style guide documented for contributors

**Prerequisites:** Story 1.6 (Jupyter Book configuration)

**Technical Notes:**
- Override Jupyter Book theme variables in `_config.yml`
- Custom CSS for elements not configurable via config
- Test on multiple browsers and screen sizes
- Consider dark mode support (future enhancement)
- Logo assets in SVG format (scalable)

---

### Story 4.3: Card Layouts for "Newly Discovered" Section

As a **handbook user**,
I want **visually distinct card-based presentation for recent updates**,
So that **I can quickly scan latest developments at a glance**.

**Acceptance Criteria:**

**Given** "Newly Discovered" content is published
**When** I view the section
**Then** each item displays as a card with:
- **Title:** Clear, clickable headline
- **Summary:** 1-2 line description
- **Date:** Publication date badge
- **Category:** Visual badge (Model Updates, Framework Updates, etc.)
- **External link:** Icon/button to original source
- **Card hover effect:** Visual feedback

**And** cards are grouped by category with category headers

**And** layout is responsive grid (4 columns desktop, 2 tablet, 1 mobile)

**And** "Last 30 days" and "Archive" collapsible sections

**Prerequisites:** Story 4.2 (theme customization)

**Technical Notes:**
- Use sphinx-design extension for card/grid components
- MyST-NB syntax for cards: `{card}` directive
- CSS Grid or Flexbox for responsive layout
- Category badges with distinct colors
- sphinx-togglebutton for collapsible archive sections

---

### Story 4.4: SEO and Social Sharing Optimization

As a **growth marketer**,
I want **handbook pages optimized for search engines and social sharing**,
So that **content reaches wider audience through organic discovery**.

**Acceptance Criteria:**

**Given** handbook pages are published
**When** pages are crawled or shared
**Then** each page includes:
- **SEO meta tags:** title, description, keywords
- **Open Graph tags:** for Facebook, LinkedIn sharing
- **Twitter Card tags:** for Twitter previews
- **Structured data:** schema.org markup (Article, TechArticle)
- **Sitemap:** Auto-generated XML sitemap
- **Robots.txt:** Proper crawling directives

**And** URLs are descriptive (e.g., `/basics/rag/naive-rag` not `/page123`)

**And** images have alt text for accessibility and SEO

**And** pages load fast (optimized images, minimal JS)

**And** mobile-friendly (passes Google Mobile-Friendly Test)

**Prerequisites:** Story 4.2 (theme customization)

**Technical Notes:**
- Use sphinxext-opengraph extension for OG tags
- Frontmatter includes meta description for each page
- Jupyter Book auto-generates sitemap
- Test with Google Rich Results Test
- Optimize images: WebP format, responsive sizes
- CDN via GitHub Pages for fast delivery

---

### Story 4.5: GitHub Actions Deployment Automation

As a **DevOps engineer**,
I want **Jupyter Book automatically built and deployed on every main branch push**,
So that **content goes live immediately after GitHub commit**.

**Acceptance Criteria:**

**Given** markdown content is committed to main branch
**When** GitHub Actions workflow triggers
**Then** the deployment process:
- Installs Jupyter Book dependencies (cached for speed)
- Runs `jupyter-book build` on content directory
- Validates build (no errors, all links valid)
- Deploys HTML to `gh-pages` branch
- Invalidates any caches if needed
- Updates deployment status

**And** full build completes in under 5 minutes

**And** zero-downtime deployment (old version live until new ready)

**And** deployment failures don't take down live site

**And** deployment status visible in GitHub UI and README badge

**Prerequisites:** Story 1.5 (CI/CD pipeline), Story 4.1 (Postgres→GitHub pipeline)

**Technical Notes:**
- Use peaceiris/actions-gh-pages action
- Dependency caching: pip cache, Jupyter Book cache
- Incremental builds if supported (future optimization)
- Deployment notifications to Slack/Discord
- Manual deployment workflow for hotfixes

---

### Story 4.6: Content Metadata and Timestamps

As a **handbook user**,
I want **clear indicators of when content was published and last updated**,
So that **I can trust content currency and relevance**.

**Acceptance Criteria:**

**Given** published handbook pages
**When** I view any page
**Then** I see:
- **Publication date:** When content first published
- **Last updated date:** Most recent content modification
- **Source link:** Original source URL for "Newly Discovered" items
- **Version indicator:** For framework-specific content (e.g., "LangChain 0.3")

**And** dates are in readable format (e.g., "November 8, 2025")

**And** "last updated" auto-updates from git history or frontmatter

**And** very old content (>6 months) shows staleness warning

**Prerequisites:** Story 4.2 (theme customization)

**Technical Notes:**
- Frontmatter: `date`, `last_updated`, `version` fields
- Custom Jupyter Book extension to display dates
- Git hooks can auto-update last_modified date
- Consider "freshness indicator" visual (green/yellow/red)
- Timezone handling (UTC or local)

---

### Story 4.7: Rollback and Deployment Safety

As a **site administrator**,
I want **ability to quickly rollback bad deployments**,
So that **site quality is protected and issues can be fixed fast**.

**Acceptance Criteria:**

**Given** a deployment introduces errors (broken links, formatting issues, bad content)
**When** I need to rollback
**Then** I can:
- Revert git commit (standard `git revert`)
- Trigger manual re-deployment of previous version
- Keep problematic content in separate branch for fixing
- Deployment automatically rolls back on build failure

**And** previous version remains live during failed build

**And** rollback process documented and tested

**And** post-rollback checklist (fix issue, test, re-deploy)

**Prerequisites:** Story 4.5 (deployment automation)

**Technical Notes:**
- GitHub Pages serves from gh-pages branch (previous version stays until new succeeds)
- Git history allows easy revert
- Failed builds don't update gh-pages
- Monitoring alerts for broken links, 404s
- Staging environment for pre-production testing (future enhancement)

---

## Epic 5: Community Contribution Framework

**Goal:** Enable community members to contribute handbook content, submit sources, and collaborate effectively - turning the handbook into collective intelligence that compounds.

**Value:** This epic delivers the "Community Intelligence" magic - where contributions make knowledge compound instead of fade. It scales content creation beyond the core team.

---

### Story 5.1: GitHub PR Workflow for Content Contributions

As a **community contributor**,
I want **clear process to submit handbook content via GitHub pull requests**,
So that **I can share my knowledge while maintaining quality standards**.

**Acceptance Criteria:**

**Given** I want to contribute handbook content
**When** I follow the contribution workflow
**Then** I can:
- Fork the handbook repository
- Create feature branch for my contribution
- Edit or create markdown files following templates
- Submit pull request with description
- See automated checks run (linting, link validation)
- Receive feedback from maintainers
- Iterate on changes until approved

**And** CONTRIBUTING.md document includes:
- Step-by-step PR workflow
- Content guidelines and quality standards
- Markdown formatting examples
- How to run local preview (Jupyter Book build)

**And** PR template auto-populates with checklist

**And** automated checks validate:
- Markdown syntax correct
- Links are valid (no 404s)
- Frontmatter complete
- File naming conventions followed

**Prerequisites:** Story 1.1 (repository setup), Story 1.5 (CI/CD)

**Technical Notes:**
- Use GitHub PR templates (`.github/pull_request_template.md`)
- Automated checks: markdown-lint, linkchecker
- PR review requires maintainer approval
- Consider "good first issue" labels for new contributors
- Clear merge policy (squash vs merge commits)

---

### Story 5.2: Content Templates and Style Guide

As a **new contributor**,
I want **clear templates and examples for different content types**,
So that **my contributions match handbook standards without guesswork**.

**Acceptance Criteria:**

**Given** I'm creating new content
**When** I reference contribution documentation
**Then** I find templates for:
- **Basics topic page** (overview, concepts, examples, trade-offs, further reading)
- **Advanced topic page** (deep dive, implementation, performance, edge cases)
- **Newly Discovered item** (title, summary, category, source link)
- **Frontmatter requirements** (title, date, category, tags, description)

**And** style guide covers:
- Voice and tone (clear, practical, professional)
- Code example formatting
- Citation format for sources
- Image guidelines (alt text, sizing, placement)
- When to link to other sections

**And** examples of "good" vs "needs improvement" content

**Prerequisites:** Story 3.1 (taxonomy documentation)

**Technical Notes:**
- Templates in `/templates/` directory
- Style guide in `STYLE_GUIDE.md`
- Include before/after examples
- Link to external resources (technical writing guides)
- Consider automated style checking (vale, write-good)

---

### Story 5.3: URL Submission Mechanism

As a **community member**,
I want **easy way to submit URLs for Auto-News to monitor**,
So that **I can help expand content coverage when I discover great sources**.

**Acceptance Criteria:**

**Given** I discover a valuable LLM content source
**When** I submit it
**Then** submission mechanism:
- Simple web form or GitHub issue template
- Fields: URL, source type (Twitter, Discord, RSS, blog), category, reason for inclusion
- URL validation (format check, reachability)
- Confirmation message with "under review" status

**And** submitted URLs queued in GitHub issues with label "source-submission"

**And** maintainers review and decide (approve/reject with reason)

**And** approved sources added to Auto-News configuration

**And** submitter receives notification of decision

**Prerequisites:** Story 2.1 (multi-source aggregation)

**Technical Notes:**
- GitHub issue form template (YAML-based forms)
- Alternative: Simple web form hosted on GitHub Pages
- URL validation: regex check, HTTP HEAD request
- Maintainer workflow: review, test source, add to config
- Track source performance post-approval

---

### Story 5.4: Contributor Recognition and Profiles

As a **contributor**,
I want **my contributions recognized publicly**,
So that **I feel valued and motivated to continue contributing**.

**Acceptance Criteria:**

**Given** I've made contributions to the handbook
**When** I check the contributors page
**Then** I see:
- **Contributors page** listing all contributors
- GitHub avatar and username
- Number of merged PRs
- Types of contributions (content, sources, code, reviews)
- Optional: contributor bio/links (if provided)

**And** contribution stats automatically updated (from git history)

**And** "Top contributors this month" highlight section

**And** optional contributor badges: "Founding Contributor", "Subject Matter Expert", "Code Contributor"

**Prerequisites:** Story 5.1 (PR workflow)

**Technical Notes:**
- Use git log to extract contributor data
- GitHub API for user profiles and avatars
- Generate contributors page automatically (script or CI)
- Consider all-contributors bot for automation
- Optional: contributor tiers based on impact

---

### Story 5.5: Content Review Process for Community PRs

As a **maintainer**,
I want **efficient process to review and approve community contributions**,
So that **quality is maintained without creating bottleneck**.

**Acceptance Criteria:**

**Given** community member submits content PR
**When** maintainers review
**Then** review process includes:
- **Automated checks** run first (linting, links, frontmatter)
- **Reviewer assignment** based on content category
- **Review checklist:**
  - Content accuracy
  - Matches style guide
  - Citations present and valid
  - Appropriate difficulty level (Basics vs Advanced)
  - No promotional content
- **Feedback mechanism:** inline comments, suggested changes
- **Approval workflow:** 1 maintainer approval minimum

**And** review turnaround target: 48 hours for simple fixes, 7 days for new pages

**And** clear acceptance/rejection criteria documented

**And** rejected PRs include constructive feedback and improvement suggestions

**Prerequisites:** Story 5.1 (PR workflow), Story 5.2 (templates)

**Technical Notes:**
- Use GitHub review features (request changes, approve)
- CODEOWNERS file for auto-assignment by category
- Review checklist in PR template
- Consider requiring passing CI before human review
- Documentation for new reviewers

---

### Story 5.6: Contributor Onboarding and Support

As a **new contributor**,
I want **welcoming onboarding experience and support when stuck**,
So that **I can contribute successfully even without deep technical expertise**.

**Acceptance Criteria:**

**Given** I'm a new contributor
**When** I engage with the project
**Then** I experience:
- **Welcome message** on first PR (GitHub Actions bot)
- **Getting Started guide** (setup dev environment in under 30 min)
- **First contribution guide** (easy, low-risk tasks)
- **Community channels:** Discord/Slack for questions
- **FAQ** for common contributor questions

**And** "good first issue" labels identify beginner-friendly tasks

**And** maintainers respond to questions within 24 hours

**And** video walkthrough available (optional): "Your first handbook contribution"

**Prerequisites:** Story 5.1 (PR workflow)

**Technical Notes:**
- Use first-interaction GitHub Action for welcome message
- Create "good first issue" labels and tag appropriate issues
- Maintain FAQ in wiki or docs
- Consider monthly contributor office hours
- Track contributor retention metrics

---

## Epic 6: Content Quality & Lifecycle Management

**Goal:** Maintain handbook quality, freshness, and reliability through systematic quality controls, monitoring, and operational excellence.

**Value:** This epic delivers the "Confidence" promise - users trust the handbook as consistently high-quality, accurate, and up-to-date. It's the operational backbone that keeps the handbook healthy long-term.

---

### Story 6.1: Multi-Stage Content Approval Gates

As a **quality manager**,
I want **systematic quality gates at each pipeline stage**,
So that **only high-quality, accurate content reaches users**.

**Acceptance Criteria:**

**Given** content flows through the pipeline
**When** each stage processes content
**Then** approval gates enforce:
- **Stage 1 (AI Scoring):** Only score-5 items proceed
- **Stage 2 (Human Review):** Reviewer explicitly approves/rejects with reason
- **Stage 3 (Pre-Publish Validation):** Automated checks (markdown lint, link validation, frontmatter complete)
- **Stage 4 (PR Review for contributions):** Maintainer approval required
- **Stage 5 (Post-Deploy Monitoring):** Smoke tests after deployment

**And** rejection at any stage includes:
- Clear reason for rejection
- Actionable feedback for improvement
- Path to resubmission

**And** approval metrics tracked:
- Approval rate by stage
- Common rejection reasons
- Time spent in each stage

**Prerequisites:** Story 2.4 (Notion review), Story 5.5 (PR review)

**Technical Notes:**
- Document approval criteria for each stage
- Track metrics in Postgres (stage, timestamp, decision, reason)
- Dashboard showing approval funnel
- Alert on unusual patterns (e.g., spike in rejections)
- Periodic review of rejection reasons to improve upstream quality

---

### Story 6.2: Automated Link Validation and Health Monitoring

As a **handbook maintainer**,
I want **automated detection of broken links and content issues**,
So that **users don't encounter errors and content stays reliable**.

**Acceptance Criteria:**

**Given** handbook is published with external links
**When** link validation runs (weekly)
**Then** the system:
- Checks all external URLs (HTTP status codes)
- Identifies broken links (404, 500, timeout)
- Creates GitHub issues for broken links with priority labels
- Checks internal cross-references (handbook page → handbook page)
- Validates image URLs and accessibility

**And** validation runs:
- Pre-publish (CI check on PRs)
- Post-publish (weekly scheduled job)
- On-demand (manual trigger)

**And** issues include:
- Page containing broken link
- Link URL and error type
- Suggested action (update, remove, archive)

**Prerequisites:** Story 4.5 (deployment automation)

**Technical Notes:**
- Use linkchecker or custom script
- Respect robots.txt and rate limits
- Handle temporary failures (retry logic)
- Whitelist known-flaky domains
- Consider using link archival service (archive.org) for critical sources

---

### Story 6.3: Content Error Correction Workflow

As a **handbook user or contributor**,
I want **easy way to report errors and see them corrected quickly**,
So that **handbook stays accurate and I can trust the content**.

**Acceptance Criteria:**

**Given** I discover an error in handbook content
**When** I report it
**Then** I can:
- Create GitHub issue using "Report Error" template
- Describe error: location, what's wrong, suggested fix
- See issue triaged by maintainers (priority label)
- Track status and resolution

**And** error correction workflow:
- **Critical errors** (factual inaccuracies): fixed within 24 hours
- **High priority** (outdated content): fixed within 7 days
- **Medium priority** (clarity improvements): fixed within 30 days
- **Low priority** (style/formatting): batched with other updates

**And** fix notification sent to reporter

**And** "last reviewed" date updates after correction

**Prerequisites:** Story 4.6 (content metadata)

**Technical Notes:**
- GitHub issue template: `.github/ISSUE_TEMPLATE/report-error.md`
- Issue labels: error-critical, error-high, error-medium, error-low
- Fast-track process for critical errors (direct commit, skip PR)
- Document error types and triage criteria
- Thank reporters (community engagement)

---

### Story 6.4: Source Health Monitoring and Management

As a **content operations manager**,
I want **visibility into Auto-News source performance and health**,
So that **I can maintain high-quality input sources and remove failing ones**.

**Acceptance Criteria:**

**Given** Auto-News monitors multiple sources
**When** I check source health dashboard
**Then** I see for each source:
- **Health status:** Active, Degraded, Failing, Inactive
- **Metrics:** Total items pulled, successful pulls, failure rate, last successful pull
- **Content quality:** Approval rate for items from this source
- **Trend data:** Performance over time (7 days, 30 days)

**And** alerts sent for:
- 3+ consecutive failures (source investigation needed)
- Approval rate < 20% (low-quality source)
- No new content in 14 days (stale source)

**And** source management actions:
- Pause failing source temporarily
- Remove consistently low-quality sources
- Adjust poll frequency based on value

**Prerequisites:** Story 2.1 (multi-source aggregation), Story 2.5 (status tracking)

**Technical Notes:**
- Store source health metrics in Postgres
- Dashboard: Streamlit, Grafana, or custom web page
- Define health thresholds (degraded vs failing)
- Automated pause after 5 consecutive failures
- Manual re-enable after investigation
- Document source removal criteria

---

### Story 6.5: Content Staleness Detection and Refresh System

As a **content curator**,
I want **automated identification of outdated content requiring updates**,
So that **handbook stays current without manual tracking of every page**.

**Acceptance Criteria:**

**Given** handbook content has been published
**When** staleness detection runs (weekly)
**Then** content is flagged as stale if:
- Mentioned framework has major version release
- Referenced research has been superseded
- No human review in past 6 months
- User reports indicate outdated information
- Breaking changes in mentioned tools/APIs

**And** stale content workflow:
- GitHub issue created with "content-stale" label
- Issue includes: page, staleness reason, suggested sources for update
- Assigned to subject matter expert or content team
- Includes priority (critical/high/medium/low)

**And** very stale content (12+ months) shows warning banner to users

**And** refresh process documented (research, update, review, publish)

**Prerequisites:** Story 3.6 (update triggers), Story 6.2 (monitoring)

**Technical Notes:**
- Track framework versions mentioned in content (frontmatter or auto-detect)
- Monitor GitHub releases for tracked projects
- Parse frontmatter `last_reviewed_date`
- AI can suggest whether content needs update (compare to recent sources)
- Balance staleness warnings vs alert fatigue

---

### Story 6.6: Operational Monitoring and Alerting

As a **operations engineer**,
I want **comprehensive monitoring of all pipeline components**,
So that **issues are detected and resolved before users are impacted**.

**Acceptance Criteria:**

**Given** the handbook platform is operational
**When** monitoring systems run
**Then** they track:
- **Pipeline health:** Airflow DAG success rate, task duration, failures
- **Database health:** Query performance, connection pool, storage usage
- **Vector DB health:** Query latency, index size, availability
- **Deployment health:** Build success rate, deployment duration, site uptime
- **API health:** LLM provider response times, rate limits, costs

**And** alerts sent for:
- Pipeline failures (Airflow DAG failures)
- Database issues (connection failures, high latency)
- Deployment failures (build errors, deployment timeouts)
- API issues (rate limit approaching, unusual costs)
- Site downtime (GitHub Pages unavailable)

**And** alerts routed to:
- Email for non-urgent issues
- Slack/Discord for moderate issues
- PagerDuty/on-call for critical issues

**And** runbooks document response procedures for common alerts

**Prerequisites:** Story 2.5 (pipeline tracking), Story 4.5 (deployment automation)

**Technical Notes:**
- Use Airflow built-in monitoring + alerting
- Database monitoring: pg_stat_statements, connection pool metrics
- Site uptime: UptimeRobot, Pingdom, or custom health check
- Cost monitoring: Track API spending per provider
- Log aggregation: Consider ELK stack or simple log files
- Define SLOs (service level objectives) for key metrics

---

### Story 6.7: Quality Metrics Dashboard and Reporting

As a **product manager**,
I want **clear visibility into handbook quality and operational metrics**,
So that **I can track progress toward goals and identify improvement areas**.

**Acceptance Criteria:**

**Given** handbook has been operational for at least 1 week
**When** I view the quality dashboard
**Then** I see metrics including:
- **Content metrics:** Total pages, new pages this week, updated pages, stale pages
- **Quality metrics:** AI scoring distribution, human approval rate, error reports
- **Pipeline metrics:** Items ingested, deduplicated, scored, approved, published
- **Source metrics:** Active sources, health status, top performing sources
- **Community metrics:** Contributors, PRs merged, response time
- **User metrics:** Page views (if analytics added), most visited pages

**And** trends over time (weekly, monthly, quarterly)

**And** export capability (CSV, PDF report)

**And** automated weekly report emailed to stakeholders

**Prerequisites:** Stories 2.5, 6.1, 6.4 (various tracking systems)

**Technical Notes:**
- Centralized metrics in Postgres (time-series tables)
- Dashboard: Streamlit, Metabase, Grafana, or custom
- Key metrics aligned with success criteria from PRD
- Automated report generation (weekly summary)
- Public vs private metrics (some internal only)
- Consider publishing public metrics page (transparency)

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._

---

## Epic Breakdown Summary

### Overview

This epic breakdown transforms the cherry-in-the-haystack PRD into **40 implementable stories** organized across **6 epics**. The breakdown follows BMad Method principles: vertically sliced stories, BDD acceptance criteria, clear dependencies, and sizing optimized for 200k context dev agents.

### Epic Statistics

| Epic | Stories | Focus | Phase | Dependencies |
|------|---------|-------|-------|--------------|
| Epic 1: Foundation & Core Infrastructure | 7 | Technical foundation | MVP (Sequential) | None (first epic) |
| Epic 2: Intelligent Content Ingestion Pipeline | 6 | Signal from noise | MVP (Sequential) | Epic 1 |
| Epic 3: AI-Powered Knowledge Synthesis | 7 | Clarity through structure | MVP (Sequential) | Epic 2 |
| Epic 4: Automated Publication System | 7 | Speed through automation | MVP (Sequential) | Epic 3 |
| Epic 5: Community Contribution Framework | 6 | Collective intelligence | Growth (Parallel) | Epic 4 |
| Epic 6: Content Quality & Lifecycle Management | 7 | Sustained confidence | Growth (Parallel) | Epic 4 |
| **Total** | **40 stories** | | | |

### Delivery Timeline

**Phase 1: Core MVP (Epics 1-4) - Sequential Execution**
```
Epic 1 (Foundation)
  ↓
Epic 2 (Ingestion Pipeline)
  ↓
Epic 3 (AI Synthesis)
  ↓
Epic 4 (Publication)
  ↓
MVP LAUNCH ✓
```

**Phase 2: Growth & Quality (Epics 5-6) - Parallel Execution**
```
Epic 5 (Community) ←→ Epic 6 (Quality Management)
  ↓
Full Platform Maturity ✓
```

### Requirements Coverage

**100% Coverage of PRD Functional Requirements:**
- ✅ All 8 FR areas mapped to specific stories
- ✅ All MVP acceptance criteria covered
- ✅ Critical NFRs embedded in story acceptance criteria

**Product Magic Delivered:**
- 🌟 **Clarity** - Epic 3 delivers MECE taxonomy helping users "now I understand"
- 🌟 **Confidence** - Epic 6 maintains quality users can trust
- 🌟 **Speed** - Epic 4 enables weekly updates keeping handbook "alive"
- 🌟 **Community Intelligence** - Epic 5 makes knowledge compound instead of fade

### Story Quality Standards

All stories follow these standards:
- ✅ **BDD Format:** Given/When/Then acceptance criteria
- ✅ **Vertical Slicing:** Complete functionality across all layers
- ✅ **Clear Prerequisites:** Only backward dependencies (no forward refs)
- ✅ **Single-Session Sizing:** Completable by one dev agent in one focused session
- ✅ **Technical Guidance:** Implementation notes for every story
- ✅ **User Value:** Clear "So that..." statements connecting to user needs

### Key Dependencies

**Critical Path (MVP):**
1. Story 1.1 (Project Setup) → Enables all other work
2. Story 1.2 (Database) → Required for all data storage
3. Story 1.3 (Vector DB) → Required for deduplication
4. Story 2.3 (AI Scoring) → Gates content quality
5. Story 3.1 (Taxonomy) → Defines content structure
6. Story 4.1 (Postgres→GitHub) → Connects pipeline to publication

**Parallel Work Opportunities:**
- Epic 1: Stories 1.5, 1.6, 1.7 can partially overlap
- Epic 4: Stories 4.2, 4.3, 4.4 can be done in parallel
- Epics 5 & 6: Can run simultaneously after Epic 4 completes

### Next Steps

**Immediate: Architecture Phase**
Run `/bmad:bmm:workflows:architecture` to:
- Validate technical decisions for Auto-News → Handbook transformation
- Document integration points and data flows
- Finalize infrastructure choices (Postgres hosting, vector DB provider, etc.)
- Create architectural decision records (ADRs)

**Then: Implementation Phase**
1. Set up sprint tracking with `/bmad:bmm:workflows:sprint-planning`
2. For each story, run `/bmad:bmm:workflows:create-story` to generate detailed implementation plan
3. Execute stories with `/bmad:bmm:workflows:dev-story`
4. Use `/bmad:bmm:workflows:code-review` for quality validation

### Success Metrics Alignment

Each epic directly supports PRD success criteria:

**Clarity Metrics (Epic 3):**
- User feedback: "Ah, now I finally understand"
- MECE structure covers 95% of LLM engineering decisions

**Confidence Metrics (Epics 2, 6):**
- 90%+ approval rating from human reviewers
- Quality controls maintain consistent standards

**Speed Metrics (Epics 2, 4):**
- Weekly "Newly Discovered" updates
- Content published within 48 hours of approval
- Users catch up in minutes, not days

**Community Metrics (Epic 5):**
- 20+ active contributors at launch → 50+ within 6 months
- Clear contribution pathways with <48 hour review turnaround

---

**Epic breakdown complete and validated.** Ready for architecture phase and implementation.

**Document saved:** `C:\Users\Hankeol\Desktop\Dev\cherry-in-the-haystack\docs\epics.md`

**Total Stories:** 40 stories across 6 epics
**MVP Stories:** 27 stories (Epics 1-4)
**Growth Stories:** 13 stories (Epics 5-6)
