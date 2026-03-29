# cherry-in-the-haystack - Epic Breakdown

**Author:** HK
**Date:** 2026-03-19
**Project Level:** High Complexity SaaS Platform (Brownfield Transformation)
**Target Scale:** 50,000 MAU, 500 concurrent paid users, 50+ enterprise clients

---

## Overview

This document provides the complete epic and story breakdown for cherry-in-the-haystack, decomposing the requirements from the [PRD](./PRD/index.md) into implementable stories.

The product transforms from a personal content curation pipeline into **Cherry for AI Engineers** — a multi-tier SaaS platform (Free / Paid / Enterprise) with community-curated knowledge, personalized intelligence, and enterprise content creation capabilities.

**10 Epics in total, sequenced for incremental value delivery:**

| # | Epic | Value Delivered |
|---|------|----------------|
| 1 | Foundation & Core Infrastructure | Stable base for all subsequent work |
| 2 | Content Ingestion & Newly Discovered Pipeline | Weekly fresh LLM content, automated |
| 3 | Knowledge Graph & Evidence Layer | Concept-centric knowledge system |
| 4 | Writer Agent & Knowledge Synthesis | Structured Basics/Advanced pages |
| 5 | Web Application Frontend | Public-facing dynamic webapp |
| 6 | User Management & Authentication | Accounts, tiers, billing |
| 7 | Personalization Engine | Paid-tier custom feeds |
| 8 | Adaptive Knowledge Base | Paid-tier personal KB |
| 9 | Newsletter Studio | Enterprise newsletter generation |
| 10 | Community & Quality Operations | Sustained content quality |

---

## Epic 1: Foundation & Core Infrastructure

**Goal:** Establish the monorepo, multi-database infrastructure, CI/CD pipelines, and shared tooling that all subsequent epics depend on. This epic adapts the existing curation pipeline into the brownfield SaaS project structure.

---

### Story 1.1: Monorepo & Project Scaffolding

As a contributor,
I want a well-structured monorepo with consistent tooling,
So that I can develop any part of the system without configuration friction.

**Acceptance Criteria:**

**Given** the repository is cloned fresh
**When** I run the setup command
**Then** all workspaces (frontend, backend API, pipeline packages) are installed and lint/type-check passes with zero errors

**And** the folder structure matches the architecture spec (`packages/pipeline/`, `apps/web/`, `apps/api/`, `handbook/`)
**And** pnpm workspaces + Python virtual environment are both functional
**And** a root `Makefile` or `justfile` provides unified commands (`make dev`, `make test`, `make lint`)

**Prerequisites:** None

**Technical Notes:** pnpm workspace monorepo; Python `handbook/` package alongside TypeScript packages; `.nvmrc` for Node version pinning; `pyproject.toml` for Python tooling (ruff, mypy); shared ESLint + Prettier config

---

### Story 1.2: PostgreSQL Database Initialization

As a developer,
I want a production-ready PostgreSQL schema with migration tooling,
So that all application data (users, content, preferences) is stored reliably.

**Acceptance Criteria:**

**Given** Docker Compose is running
**When** I run the migration command
**Then** all required tables are created with correct types, indexes, and constraints

**And** the migration is idempotent (re-running does not create duplicates or errors)
**And** a seed script populates test fixtures for local development
**And** database connection pooling is configured (pg-pool or equivalent)

**Prerequisites:** Story 1.1

**Technical Notes:** Use Drizzle ORM or Prisma for TypeScript migrations; tables include: `content_items`, `sources`, `user_accounts`, `user_preferences`, `reading_history`, `newsletter_drafts`, `custom_topics`; indexes on frequently queried columns (source_id, score, status, created_at)

---

### Story 1.3: Graph Database Initialization (Two-Layer Architecture)

As a knowledge engineer,
I want the Graph DB initialized with the two-layer concept-evidence schema,
So that concept nodes and evidence records can be stored and queried efficiently.

**Acceptance Criteria:**

**Given** the graph database service is running
**When** the setup script executes
**Then** the Concept Layer schema is created (nodes: title, summary, relations, sources, contributors)

**And** the Evidence Layer schema is created (nodes: evidence_id, source, location, text, excerpt, comment, tags, linked_concepts)
**And** required indexes for efficient traversal are in place (concept → related concepts → evidence chains in < 500ms)
**And** a sample concept with linked evidence can be inserted and retrieved via the query API

**Prerequisites:** Story 1.1

**Technical Notes:** Neo4j or compatible graph DB; Python `handbook/db_connection/graph_db.py` client; relation types defined: prerequisite, related, subtopic, extends, contradicts; evidence link is many-to-many (evidence ↔ concepts)

---

### Story 1.4: Vector Database Initialization

As a pipeline engineer,
I want the vector database configured for content deduplication,
So that embeddings can be stored and similarity searches run under 100ms.

**Acceptance Criteria:**

**Given** the vector DB service is running (Milvus, ChromaDB, or Pinecone)
**When** an embedding is inserted
**Then** a cosine similarity search returns the top-N matches within 100ms

**And** the collection schema includes metadata fields: source, category, date, topic
**And** the vector DB client is abstracted behind a pluggable interface (swap providers without code changes)
**And** local dev uses an in-memory or file-backed provider; production uses cloud provider

**Prerequisites:** Story 1.1

**Technical Notes:** Python `handbook/db_connection/vector_db.py`; embedding model: OpenAI `text-embedding-3-small` or equivalent; pluggable interface pattern per NFR-I5; used only for deduplication (not primary knowledge store)

---

### Story 1.5: Docker Compose Local Development Environment

As a developer,
I want a single `docker-compose up` command to run all services locally,
So that I can develop and test without manual service configuration.

**Acceptance Criteria:**

**Given** Docker is installed
**When** I run `docker-compose up`
**Then** PostgreSQL, Graph DB, Vector DB, and Redis are all running and health-checked

**And** environment variables are loaded from `.env.local` (with `.env.example` committed)
**And** data volumes persist across restarts
**And** services are accessible at documented localhost ports

**Prerequisites:** Stories 1.2, 1.3, 1.4

**Technical Notes:** `docker-compose.yml` at project root; Redis for caching (NFR-P2); include pgAdmin or similar for local DB inspection; `.env.example` documents all required vars

---

### Story 1.6: CI/CD Pipelines (GitHub Actions)

As a contributor,
I want automated CI checks and deployment pipelines,
So that every pull request is validated and merges are deployed reliably.

**Acceptance Criteria:**

**Given** a pull request is opened
**When** GitHub Actions runs
**Then** lint, type-check, and unit tests all pass before merge is allowed

**And** the deploy workflow triggers on merge to `main` and achieves zero-downtime deployment
**And** failed pipeline stages send alert notifications (email or Slack)
**And** rollback via `git revert` + re-deploy is documented and tested

**Prerequisites:** Story 1.1

**Technical Notes:** `.github/workflows/ci.yml` (lint, test, type-check); `.github/workflows/deploy.yml` (blue-green or rolling deploy); dedicated bot account for automated commits; webhook for deployment notifications

---

### Story 1.7: Database Backup Automation

As an operator,
I want automated daily backups for all databases with documented restore procedures,
So that no data is lost in the event of a failure.

**Acceptance Criteria:**

**Given** the backup job is scheduled
**When** it runs daily
**Then** Postgres is backed up with 30-day retention

**And** Graph DB is backed up with 60-day retention
**And** Vector DB is backed up weekly with 60-day retention
**And** restore procedure is documented and has been tested end-to-end

**Prerequisites:** Stories 1.2, 1.3, 1.4, 1.6

**Technical Notes:** `scripts/backup_databases.py`; use cloud storage (S3/GCS) for backup files; scheduled via GitHub Actions cron or cloud scheduler; alert on backup failure

---

## Epic 2: Content Ingestion & "Newly Discovered" Pipeline

**Goal:** Automatically aggregate LLM content from 10+ sources, deduplicate it, score it with AI, route it through Notion for Knowledge Team weekly review, and publish top-rated items to the webapp weekly.

---

### Story 2.1: Content Source Configuration System

As a pipeline operator,
I want a configuration file that defines all monitored content sources,
So that sources can be added, removed, or toggled without code changes.

**Acceptance Criteria:**

**Given** a `sources.yaml` (or equivalent) config file exists
**When** the pipeline starts
**Then** it reads source definitions (URL, category mapping, polling frequency, enable/disable toggle)

**And** sources include: Twitter accounts, Discord channels, GitHub orgs, RSS feeds, blogs
**And** per-source health is tracked (last successful pull, error rate)
**And** adding a new source requires only a config file edit (no code changes)

**Prerequisites:** Story 1.2

**Technical Notes:** FR-7.1; config in `packages/pipeline/src/sources/sources.yaml`; source health stored in Postgres `sources` table; operator pattern for each source type (modular)

---

### Story 2.2: Multi-Source Content Ingestion

As a practitioner,
I want LLM-related content aggregated automatically from all configured sources,
So that I get comprehensive coverage without monitoring dozens of channels manually.

**Acceptance Criteria:**

**Given** sources are configured and the ingestion job runs
**When** a new item is published on any monitored source
**Then** it is discovered and stored within 24 hours

**And** source metadata is preserved: URL, date, author, platform
**And** the pipeline processes 100+ items per hour
**And** source-specific adapters handle API auth, rate limits, and pagination

**Prerequisites:** Stories 1.2, 2.1

**Technical Notes:** FR-1.1; adapters in `packages/pipeline/src/newly-discovered/`; operator pattern for each source type; exponential backoff on transient failures; dead-letter queue for permanently failed items

---

### Story 2.3: Content Deduplication

As a user,
I want unique insights in my feed — not the same story repeated 10 times,
So that every item I see adds genuine value.

**Acceptance Criteria:**

**Given** a new content item is ingested
**When** deduplication runs before AI scoring
**Then** exact matches and near-duplicates (95%+ accuracy) are identified and filtered

**And** chunk-level (paragraph) deduplication flags near-duplicate paragraphs within an item
**And** the original source is preserved for merged duplicates
**And** deduplication uses vector similarity (cosine threshold) against the Vector DB
**And** the deduplication check completes in under 100ms per item

**Prerequisites:** Stories 1.4, 2.2

**Technical Notes:** FR-1.2; content-level dedup runs first (cheaper), then chunk-level; embeddings generated using configured embedding model; dedup must run before AI scoring to reduce API costs

---

### Story 2.4: AI-Powered Content Scoring (1-5)

As a Knowledge Team member,
I want content automatically scored 1-5 for relevance and quality,
So that I can focus review time on the highest-value items.

**Acceptance Criteria:**

**Given** a deduplicated content item exists
**When** the scoring agent runs
**Then** it assigns a score 1-5 based on relevance, depth, novelty, and practicality

**And** scoring completes within 5 minutes of ingestion
**And** score 5 = top-tier content worthy of inclusion in Newly Discovered
**And** the scoring prompt and criteria are configurable without code changes
**And** LLM provider failures trigger exponential backoff and retry

**Prerequisites:** Story 2.3

**Technical Notes:** FR-2.1; scoring agent in `packages/pipeline/src/scoring/`; supports multi-LLM (OpenAI, Gemini, Ollama) per NFR-I6; score stored in `content_items.score` column; cost optimization via caching

---

### Story 2.5: Notion Review Workflow Integration

As a Knowledge Team member,
I want scored content items automatically surfaced in Notion for weekly review,
So that I can validate summaries, adjust scores, and map items to the ontology.

**Acceptance Criteria:**

**Given** content items are scored
**When** score-5 items exist
**Then** they are auto-assigned to Knowledge Team members in Notion with status `pending`

**And** team members can update: summary accuracy, score, ontology graph mapping
**And** status flows: `pending` → `in_review` → `finished`
**And** all review decisions are logged with an audit trail
**And** Notion API rate limits (3 req/s) are respected with backoff

**Prerequisites:** Story 2.4

**Technical Notes:** FR-2.2; `packages/pipeline/src/integrations/notion-client.ts`; Notion DB schema: item, score, summary, assignee, status, review_notes, ontology_mapping; LLM-assisted ontology mapping suggestions during review

---

### Story 2.6: Notion → PostgreSQL Backup Job

As an operator,
I want reviewed Notion content backed up to PostgreSQL automatically,
So that content data is not solely dependent on Notion's availability.

**Acceptance Criteria:**

**Given** Notion review data exists
**When** the backup job runs (daily)
**Then** all reviewed items and their metadata are synced to the `content_items` Postgres table

**And** the sync is idempotent (re-running does not create duplicates)
**And** fallback to Postgres read-only mode activates if Notion is unavailable

**Prerequisites:** Stories 1.2, 2.5

**Technical Notes:** FR-NFR-I2; `packages/pipeline/src/jobs/notion-backup.ts`; incremental sync using `last_modified` timestamp; Notion downtime triggers manual review queue fallback

---

### Story 2.7: Weekly Content Publication Job

As a user,
I want the top-rated content published to the webapp weekly,
So that the Newly Discovered section always has fresh, high-quality items.

**Acceptance Criteria:**

**Given** the weekly publish job runs (e.g., Thursday after Wednesday review)
**When** execution completes
**Then** the top 20 `finished` score-5 items are exported as markdown files to the webapp content repo

**And** deployment triggers automatically after export (zero-downtime)
**And** rollback capability exists for broken builds
**And** "Last updated" timestamps on published pages are accurate to the hour

**Prerequisites:** Stories 2.5, 2.6, 1.6

**Technical Notes:** FR-5.1; `packages/pipeline/src/jobs/weekly-publish.ts`; output: markdown files in `packages/pipeline/src/publication/`; score < 4 items go to Notion but are excluded from newsletter and top 20 must-reads (per project routing rules)

---

## Epic 3: Knowledge Graph & Evidence Layer

**Goal:** Build and populate the two-layer knowledge graph — curated evidence from authoritative sources forms the Evidence Layer, which is then organized into the Concept Ontology Layer that powers Writer Agent synthesis.

---

### Story 3.1: Evidence Ingestion Pipeline (Curated Texts)

As a Knowledge Team member,
I want to ingest books, papers, and canonical posts into the Evidence Layer,
So that authoritative source material is available for AI synthesis.

**Acceptance Criteria:**

**Given** a curated text source (PDF, web URL, or markdown)
**When** the ingestion pipeline runs
**Then** the text is extracted, chunked, and stored in the Evidence Layer with full metadata

**And** metadata includes: source title, author, URL/PDF reference, publication date, topic, quality rating
**And** chunks are tagged with relevant concept associations (initial auto-tagging)
**And** version tracking captures updated sources
**And** text chunking uses semantic boundaries (paragraphs), not arbitrary character counts

**Prerequisites:** Stories 1.2, 1.3

**Technical Notes:** FR-3.3, FR-7.2; `handbook/pipeline/evidence_ingestion/`; PDF extraction via `pdfminer` or `pypdf`; web → markdown via `trafilatura`; chunk size ~500 tokens with overlap; Evidence Layer schema per FR-3.1

---

### Story 3.2: Concept Node Management API

As a Knowledge Team member,
I want to create, update, and relate concept nodes in the Ontology Layer,
So that the knowledge graph accurately reflects the LLM engineering domain.

**Acceptance Criteria:**

**Given** the Graph DB is initialized
**When** I use the concept management API
**Then** I can create concept nodes with: title (noun-phrase only), summary, relation types

**And** relation types supported: prerequisite, related, subtopic, extends, contradicts
**And** evidence is never stored in concept nodes — only linked via evidence_id
**And** concept queries return connected concepts + relationship types in < 500ms
**And** the API is callable by both the Writer Agent and the Notion review interface

**Prerequisites:** Story 1.3

**Technical Notes:** FR-3.1; `handbook/db_connection/graph_db.py`; enforce noun-phrase naming convention in validation; concepts are reusable across all sources; graph view shows concepts only (no evidence nodes cluttering visualization)

---

### Story 3.3: Evidence-to-Concept Linking

As a knowledge engineer,
I want evidence chunks to be linked to relevant concept nodes,
So that the Writer Agent can retrieve all evidence for a concept in one query.

**Acceptance Criteria:**

**Given** evidence chunks exist in the Evidence Layer
**When** the linking process runs (manual or LLM-assisted)
**Then** each evidence chunk is associated with one or more concept nodes (many-to-many)

**And** evidence previews can be retrieved per concept: excerpt + source + comment type
**And** evidence types are tracked: paraphrase, direct quote, figure reference
**And** linking can be done via the Notion review interface (LLM-assisted suggestions)

**Prerequisites:** Stories 3.1, 3.2

**Technical Notes:** FR-3.1; evidence `linked_concepts` field stores concept IDs; LLM suggests likely concept links during Wednesday study sessions; Knowledge Team confirms/corrects suggestions

---

### Story 3.4: Monthly Ontology Extraction Job

As a knowledge engineer,
I want a monthly batch job to identify new concept candidates from the Evidence Layer,
So that the ontology stays current with emerging LLM concepts.

**Acceptance Criteria:**

**Given** the monthly batch job runs (2nd Saturday)
**When** execution completes
**Then** new concept noun-phrase candidates are extracted from unlinked or under-linked evidence

**And** word count and frequency metrics filter noise from meaningful concepts
**And** LLM-assisted relationship detection suggests where new concepts connect to existing ones
**And** candidates are surfaced to the Knowledge Team in Notion for review and approval
**And** approved concepts default to the Advanced section (not Basics)

**Prerequisites:** Stories 3.1, 3.2, 3.3

**Technical Notes:** FR-3.2; `handbook/pipeline/evidence_ingestion/ontology_extractor.py`; scheduled via cron or GitHub Actions; noun-phrase extraction via spaCy or similar NLP library; frequency threshold configurable

---

## Epic 4: Writer Agent & Knowledge Synthesis

**Goal:** Transform the knowledge graph into polished, structured Basics/Advanced concept pages using an AI Writer Agent that produces the four-section format (Overview → Cherries → Child Concepts → Progressive References).

---

### Story 4.1: Writer Agent Core Pipeline

As a practitioner,
I want structured concept pages generated from the knowledge graph,
So that I get distilled, well-cited knowledge without reading dozens of sources myself.

**Acceptance Criteria:**

**Given** a concept node exists in the Ontology Layer with linked evidence
**When** the Writer Agent runs for that concept
**Then** it queries the CONCEPT schema (concept + connected concepts + relationships)

**And** it queries the EVIDENCE schema (full text, excerpts, source metadata, comment types)
**And** it generates a page following the four-section format:
  1. Overview (definition + why it matters + practical relevance)
  2. Cherries (MECE summaries: source title + structured key insight)
  3. Child Concepts / Co-occurring Concepts (relationships with brief explanations)
  4. Progressive References (MECE learning path: "Start here → Next → Deeper")
**And** page generation completes within 10 minutes per concept
**And** output is a markdown file conforming to the Concept Page Structure

**Prerequisites:** Stories 3.2, 3.3

**Technical Notes:** FR-4.2; `handbook/pipeline/writer_agent/`; LLM prompt templates for each section; evidence citations use proper attribution; paraphrasing vs direct quote tracked; multi-LLM support (OpenAI, Gemini, Ollama)

---

### Story 4.2: Conflicting Evidence Detection & Flagging

As a Knowledge Team member,
I want conflicting evidence from multiple sources flagged during page generation,
So that I can review and resolve contradictions before publishing.

**Acceptance Criteria:**

**Given** the Writer Agent generates a page
**When** evidence from multiple sources contradicts on the same claim
**Then** the conflict is flagged in the output markdown (e.g., `<!-- CONFLICT: Source A says X, Source B says Y -->`)

**And** flagged pages are queued for Knowledge Team review before publication
**And** conflicting sections are not published until resolved

**Prerequisites:** Story 4.1

**Technical Notes:** FR-4.2 domain constraint; contradiction detection via LLM comparison of evidence excerpts on the same claim; conflict queue stored in Postgres

---

### Story 4.3: Concept Promotion Flow (Advanced → Basics)

As a practitioner,
I want the Basics section to reflect truly foundational concepts — not just trendy ones,
So that I can trust the Basics section as a stable learning foundation.

**Acceptance Criteria:**

**Given** the monthly review runs (2nd Saturday)
**When** concept promotion candidates are evaluated
**Then** concepts with sustained importance metrics (mentions, usage, stability over 3+ months) are surfaced for review

**And** Knowledge Team approves/rejects promotion candidates
**And** promoted concepts move from Advanced → Basics with page updates and re-generation trigger
**And** promotion decisions are documented with rationale in the Graph DB

**Prerequisites:** Stories 4.1, 3.4

**Technical Notes:** FR-4.3; importance metric = aggregate of: evidence link count, mention frequency in new content, cross-concept relation density; promotion flag stored on concept node; Writer Agent re-runs for promoted concepts

---

### Story 4.4: Evolving Taxonomy Management

As a knowledge engineer,
I want to add, reassign, or deprecate content categories without restructuring the system,
So that Cherry stays current as the LLM field evolves.

**Acceptance Criteria:**

**Given** a new LLM topic category emerges
**When** I add it to the taxonomy config
**Then** concepts can be assigned to the new category immediately without pipeline changes

**And** content can be reassigned when taxonomy changes
**And** deprecated categories show a migration plan and redirect to replacement categories
**And** "Newly Discovered" categories are reviewed quarterly (automated reminder)

**Prerequisites:** Story 4.1

**Technical Notes:** FR-4.4; taxonomy defined in `packages/pipeline/src/sources/taxonomy.yaml`; category assignments stored in Postgres with soft-delete for deprecation

---

### Story 4.5: Writer Agent Publication to Webapp

As a contributor,
I want generated concept pages automatically deployed to the webapp,
So that Basics/Advanced content stays up-to-date without manual file copying.

**Acceptance Criteria:**

**Given** the Writer Agent generates a new or updated page
**When** the page passes conflict checks
**Then** the markdown file is committed to the webapp content directory and deployment triggers

**And** deployment is zero-downtime
**And** "Last updated" timestamps are accurate
**And** failed deploys alert maintainers and do not overwrite the previous good state

**Prerequisites:** Stories 4.1, 4.2, 1.6

**Technical Notes:** FR-5.1; `packages/pipeline/src/jobs/writer-agent.ts` orchestrates Python agent + Git commit; automated bot account for commits; rollback via `git revert`

---

## Epic 5: Web Application Frontend

**Goal:** Replace the static Jupyter Book with a dynamic, responsive web application that renders all Cherry content (Basics, Advanced, Newly Discovered) with professional navigation, search, and i18n support.

---

### Story 5.1: Web App Foundation & Routing

As a user,
I want to access Cherry through a fast, modern web application,
So that I can browse knowledge without the limitations of a static site.

**Acceptance Criteria:**

**Given** the web app is deployed
**When** I visit the homepage
**Then** the app loads with FCP < 1 second and LCP < 2.5 seconds on a 3G connection

**And** three top-level routes exist: `/basics`, `/advanced`, `/newly-discovered`
**And** server-side rendering (SSR) or static generation is used for content pages
**And** the app is mobile-responsive with touch targets ≥ 44×44px

**Prerequisites:** Story 1.6

**Technical Notes:** Next.js (App Router) or equivalent SSR framework; Tailwind CSS for styling; content loaded from markdown files generated by pipeline; deployed to Vercel or equivalent cloud host; replaces GitHub Pages / Jupyter Book

---

### Story 5.2: Content Navigation & Two-Level TOC

As a practitioner,
I want clear, hierarchical navigation across all knowledge sections,
So that I can orient myself and jump to exactly what I need.

**Acceptance Criteria:**

**Given** I am on any content page
**When** I look at the sidebar/navigation
**Then** I see a two-level TOC: parent concepts → child implementations for Basics and Advanced

**And** the Newly Discovered section shows the 4 main categories with subcategories
**And** breadcrumb navigation is present on all pages
**And** active section is highlighted in the navigation
**And** navigation is accessible via keyboard (WCAG 2.1 AA)

**Prerequisites:** Story 5.1

**Technical Notes:** FR-5.2; dynamic TOC generated from markdown frontmatter; Newly Discovered categories: Research & Models, Service & System Building, Industry & Business Applications, Ecosystem & Governance

---

### Story 5.3: Concept Page Rendering (Four-Section Format)

As a practitioner,
I want concept pages rendered with the full four-section structure,
So that I get a clear, evidence-backed understanding of each concept.

**Acceptance Criteria:**

**Given** I navigate to a Basics or Advanced concept page
**When** the page renders
**Then** I see: Overview → Cherries → Child Concepts → Progressive References sections in order

**And** relation blocks are rendered dynamically (only non-empty sections shown)
**And** evidence previews in Cherries show: excerpt + source + comment type
**And** Progressive References show the MECE learning path with clear "Start here → Next" progression
**And** code blocks have syntax highlighting
**And** "Last updated" timestamp is visible

**Prerequisites:** Stories 5.1, 4.5

**Technical Notes:** FR-5.2, FR-4.2; MDX or remark plugins for custom rendering; relation block components are reusable; syntax highlighting via Prism or Shiki

---

### Story 5.4: Search Functionality

As a user,
I want to search across all Cherry content,
So that I can find specific concepts, techniques, or topics in seconds.

**Acceptance Criteria:**

**Given** I type a query in the search bar
**When** results load
**Then** relevant pages appear within 500ms

**And** search covers titles, summaries, and content body across all sections
**And** results show: page title, section (Basics/Advanced/Newly Discovered), brief excerpt
**And** search index updates within 1 minute of new content being published
**And** graceful degradation message is shown if search is temporarily unavailable

**Prerequisites:** Story 5.1

**Technical Notes:** FR-5.2; use Algolia, MeiliSearch, or Pagefind (static-friendly); search index built during deploy pipeline; query under 500ms per NFR-P3

---

### Story 5.5: Internationalization (i18n) Infrastructure

As a global user,
I want the Cherry interface available in my language,
So that I can use the platform comfortably in English or Korean.

**Acceptance Criteria:**

**Given** I visit Cherry for the first time
**When** my browser language is Korean
**Then** the UI defaults to Korean (navigation, buttons, labels, error messages, form fields)

**And** a language selector in the header lets me switch between English and Korean
**And** my language preference is saved (for logged-in users) or via cookie (anonymous)
**And** adding a new language requires only adding a translation JSON file (no code changes)
**And** date/time and number formatting respect the selected locale

**Prerequisites:** Story 5.1

**Technical Notes:** FR-13.1, FR-13.3; i18next or next-intl; translation files in `apps/web/locales/en.json` and `apps/web/locales/ko.json`; browser language detection via `Accept-Language` header; RTL layout scaffolded for future languages; content language separate from UI language

---

### Story 5.6: Newly Discovered Category Pages

As a practitioner,
I want to browse the Newly Discovered section organized by category,
So that I can quickly scan the freshest LLM developments relevant to me.

**Acceptance Criteria:**

**Given** I navigate to `/newly-discovered`
**When** the page loads
**Then** I see the 4 main categories with their subcategories listed

**And** each category page shows a ranked list of articles (title, summary, source, date, score)
**And** articles are sorted by score descending, then by date
**And** "Last updated" timestamp reflects the latest weekly publish cycle

**Prerequisites:** Stories 5.1, 5.2, 2.7

**Technical Notes:** FR-5.2; category pages are statically generated from markdown; article list component is shared and reused for personalized views in Epic 7

---

### Story 5.7: Performance, SEO & Accessibility Polish

As a user,
I want Cherry to load fast, be findable via search engines, and be accessible to all,
So that the platform is inclusive and performant under real-world conditions.

**Acceptance Criteria:**

**Given** any content page is loaded
**When** measured by Lighthouse or Core Web Vitals
**Then** Performance ≥ 90, Accessibility ≥ 90, SEO ≥ 90

**And** all pages have complete SEO metadata (title, description, Open Graph tags)
**And** all meaningful images have alt text
**And** keyboard navigation works for all interactive elements
**And** lazy loading is applied to images below the fold
**And** CDN handles traffic spikes (configured in deploy)

**Prerequisites:** Stories 5.1–5.6

**Technical Notes:** NFR-A1, NFR-A2, NFR-P1; Core Web Vitals budgets enforced in CI; `next/image` for optimized images; semantic HTML and ARIA labels throughout

---

## Epic 6: User Management & Authentication

**Goal:** Enable secure user accounts with tier-based access (Free / Paid / Enterprise), billing integration, and GDPR-compliant data management — the gateway to all personalization and monetization features.

---

### Story 6.1: User Registration & Email Verification

As a new user,
I want to create an account with email and password,
So that I can access personalized features.

**Acceptance Criteria:**

**Given** I submit the registration form
**When** the form is valid
**Then** my account is created with a hashed password (bcrypt/argon2)

**And** a verification email is sent with a token that expires after 24 hours
**And** I cannot access authenticated features until email is verified
**And** the form validates: email format, password strength, duplicate email check
**And** account lockout activates after 5 failed login attempts

**Prerequisites:** Stories 1.2, 5.1

**Technical Notes:** FR-10.1; password hashing with argon2id; email via SendGrid or equivalent; verification token stored in Postgres with expiry; rate limiting on registration endpoint

---

### Story 6.2: OAuth Login (Google & GitHub)

As a user,
I want to sign in with Google or GitHub,
So that I don't need to remember another password.

**Acceptance Criteria:**

**Given** I click "Sign in with Google" or "Sign in with GitHub"
**When** OAuth flow completes
**Then** I am logged in and my account is created if it doesn't exist

**And** OAuth accounts can be linked to existing email/password accounts
**And** JWT session token is issued with appropriate expiration
**And** sessions are invalidated on logout across all devices

**Prerequisites:** Story 6.1

**Technical Notes:** FR-10.1; OAuth2 with PKCE; NextAuth.js or equivalent; JWT stored in httpOnly cookie; multi-device session tracking in Postgres

---

### Story 6.3: User Tier Management & Feature Gating

As a product manager,
I want users assigned to Free, Paid, or Enterprise tiers with corresponding feature access,
So that tier-based value differentiation is enforced consistently across the product.

**Acceptance Criteria:**

**Given** a user has a specific tier (Free / Paid / Enterprise)
**When** they access a feature
**Then** tier-gated features are accessible to the correct tiers and blocked for others

**And** Free tier: all community content, read-only, no auth required for browsing
**And** Paid tier: everything in Free + custom sources, personalization, adaptive KB
**And** Enterprise tier: everything in Paid + Newsletter Studio
**And** upgrade/downgrade flows work with Stripe proration

**Prerequisites:** Stories 6.1, 6.2

**Technical Notes:** FR-10.2; tier stored in `user_accounts.tier` column; middleware checks tier on each authenticated route; Stripe webhook updates tier on subscription changes; feature flags via tier check (not a separate feature flag system)

---

### Story 6.4: User Profile & Account Management

As a user,
I want to view and manage my account details and preferences,
So that I have control over my personal information.

**Acceptance Criteria:**

**Given** I am logged in
**When** I visit my profile page
**Then** I see: name, email, tier, join date, and preference settings

**And** I can change my email (with verification), name, and password
**And** I can delete my account (GDPR right to deletion — personal data purged within 30 days)
**And** I can export all my data as JSON (GDPR right to portability)
**And** I can opt out of reading history tracking

**Prerequisites:** Story 6.3

**Technical Notes:** FR-10.3; NFR-SEC5; soft-delete on account deletion (personal data purged via scheduled job at 30 days, billing records retained 7 years per tax law); data export endpoint streams JSON

---

### Story 6.5: Billing Integration (Stripe)

As a user,
I want to upgrade to Paid or Enterprise tier via a secure checkout,
So that I can access advanced features.

**Acceptance Criteria:**

**Given** I am on the upgrade page
**When** I complete Stripe checkout
**Then** my tier is updated immediately via Stripe webhook

**And** Stripe billing portal allows managing subscriptions, updating payment methods
**And** downgrade at period end (not immediate cancellation) is supported
**And** failed payments trigger grace period notification emails

**Prerequisites:** Story 6.3

**Technical Notes:** FR-10.2; Stripe Checkout + Customer Portal; webhook endpoint validates Stripe signature; subscription metadata maps to `user_accounts.tier`; proration calculated by Stripe automatically

---

## Epic 7: Personalization Engine

**Goal:** Give paid users a fully personalized experience — custom sources, natural language scoring criteria, entity-level entity follows, and category-level filtering — so "Newly Discovered" shows exactly what matters to them.

---

### Story 7.1: Custom Source Management (Paid Tier)

As a paid user,
I want to add and manage my own private content sources,
So that my feed includes sources unique to my work and interests.

**Acceptance Criteria:**

**Given** I am a paid user on the custom sources page
**When** I add a new source URL (RSS, Twitter, blog)
**Then** the source is validated (format, domain reachability) and added to my profile

**And** the Content Ingestion Pipeline ingests my custom sources within 1 hour
**And** content from my custom sources is visible only to me
**And** I can toggle sources active/inactive and delete sources
**And** community sources can be followed/unfollowed from a browseable registry

**Prerequisites:** Stories 6.3, 2.2

**Technical Notes:** FR-11.1; custom sources stored in `user_sources` table with user_id; pipeline adapts existing source adapters for user-specific sources; isolation via user_id filter on all content queries

---

### Story 7.2: Natural Language Scoring Criteria (Paid Tier)

As a paid user,
I want to define my content preferences in plain English,
So that Cherry scores and ranks content exactly how I want — without configuring weights manually.

**Acceptance Criteria:**

**Given** I enter natural language criteria (e.g., "I care more about business cases than theory")
**When** I confirm the settings
**Then** an AI interprets my criteria and generates scoring weights

**And** a confirmation UI shows the interpreted weights (e.g., "Business Cases: 2×, Theory: 0.5×")
**And** I can refine and iterate (re-enter criteria → see new weights)
**And** scoring weights apply to my personalized feed ranking and content prioritization
**And** users who don't configure criteria see the community default scoring

**Prerequisites:** Story 6.3

**Technical Notes:** FR-11.2; preference parsing via LLM in < 3 seconds (NFR-P5); weights stored in `user_preferences.scoring_weights` (JSON); A/B comparison: community score vs personal score visible in UI

---

### Story 7.3: Entity Follow Registry (Paid Tier)

As a paid user,
I want to follow specific models, frameworks, and tools from a registry,
So that articles mentioning what I care about are surfaced prominently.

**Acceptance Criteria:**

**Given** I open the Entity Registry
**When** I follow an entity (e.g., "Claude", "LangChain") and assign a weight
**Then** articles mentioning that entity are ranked higher in my feed

**And** entities I unfollow are excluded from my Newly Discovered feed
**And** per-entity weight is configurable (e.g., Claude = 2×, GPT-4 = 1×)
**And** no follow config = neutral (all entities shown at weight 1.0 default)
**And** entity registry is maintained by the Knowledge Team and synchronized from the Graph DB

**Prerequisites:** Stories 6.3, 3.2

**Technical Notes:** FR-11.3; entity registry stored in Postgres `entities` table (populated from Graph DB concept nodes tagged as models/frameworks/tools); user follows stored in `user_entity_follows`; impact_score calculated per NFR-S4

---

### Story 7.4: Category Filtering & Personalized Feed (Paid Tier)

As a paid user,
I want to show/hide entire Newly Discovered categories and assign per-category weights,
So that my feed only shows what I care about, ranked by what matters to me.

**Acceptance Criteria:**

**Given** I configure my category preferences
**When** I view the Newly Discovered section
**Then** hidden categories are excluded and shown categories are ranked by my per-category weights

**And** a "Community | For You" toggle per category page switches between views
**And** community page is the fallback for categories with no preference set
**And** personalized pages show filtered + reranked article lists (same structure as community pages, no synthesis)
**And** all preferences persist across sessions and update immediately (no cache delay)

**Prerequisites:** Stories 6.3, 5.6, 7.2, 7.3

**Technical Notes:** FR-11.3; ranking signal: `user_article_state.impact_score` (source weight × entity weight × scoring preference); personalized feed generated in < 2 seconds (NFR-P5); preferences stored in `user_preferences.category_filters`

---

### Story 7.5: Adaptive Content Scoring with Explanations

As a paid user,
I want to understand why content is ranked the way it is for me,
So that I can trust and refine my personalization settings.

**Acceptance Criteria:**

**Given** I view an article in my personalized feed
**When** I expand the score explanation
**Then** I see: "This scored high because of your preference for Business Cases (2×) and your follow of Claude"

**And** a side-by-side A/B comparison shows my personal score vs the community score
**And** score explanations are generated without additional LLM calls (purely from weight math)

**Prerequisites:** Story 7.4

**Technical Notes:** FR-11.4; explanation template: "Scored {personal_score} (community: {community_score}) — boosted by: {factors}"; factors derived from `user_article_state` breakdown; no LLM needed for explanation generation

---

## Epic 8: Adaptive Knowledge Base (Paid Tier)

**Goal:** Let paid users build their own private knowledge base by adding custom topics with reference articles, then commanding the Writer Agent to generate personalized concept pages — a KB that rewrites itself on demand.

---

### Story 8.1: Custom Topic Creation

As a paid user,
I want to add custom topics that aren't in the community knowledge base,
So that Cherry covers my team's internal context and specialized use cases.

**Acceptance Criteria:**

**Given** I am on the Custom KB page
**When** I create a new topic with name, category (Basics/Advanced), and description
**Then** the topic is saved to my private knowledge base

**And** I can upload or link reference articles/evidence for the topic
**And** evidence is extracted from my references (PDF or URL) and stored in my user-specific Evidence Layer
**And** my custom topics are visible only to me (isolated from community content)
**And** topic list view shows all my custom topics with status (has references, generated, not generated)

**Prerequisites:** Story 6.3

**Technical Notes:** FR-12.1; `custom_topics` table with `user_id` FK; user-specific evidence stored with `user_id` isolation in Evidence Layer; PDF/URL extraction reuses pipeline from Story 3.1; evidence tagged with custom topic associations

---

### Story 8.2: Writer Agent Regeneration for Custom Topics

As a paid user,
I want to trigger the Writer Agent to generate a page for my custom topic,
So that my knowledge base adapts to my context on-demand.

**Acceptance Criteria:**

**Given** I have a custom topic with reference evidence
**When** I click "Generate Page"
**Then** the Writer Agent loads my custom evidence and generates a four-section page

**And** generation completes within 10 minutes
**And** the generated page is saved in my personal knowledge base
**And** I can add more evidence and regenerate (iterate freely)
**And** my custom page is private — not visible to other users

**Prerequisites:** Stories 8.1, 4.1

**Technical Notes:** FR-12.2; Writer Agent runs with user-specific evidence context + community Graph DB for related concepts; page stored in `custom_topic_pages` table (not in community content files); generation queued as async job with progress indicator

---

### Story 8.3: Custom KB Management

As a paid user,
I want to manage my custom topics, edit evidence, and export my knowledge base,
So that I have full control over my personalized knowledge.

**Acceptance Criteria:**

**Given** I am on the Custom KB management page
**When** I interact with my topics
**Then** I can edit topic name/description, delete topics, add/remove/edit reference articles

**And** I can trigger regeneration after making changes
**And** I can export my entire personal KB as markdown files
**And** the UI clearly distinguishes between community content and my custom content

**Prerequisites:** Story 8.2

**Technical Notes:** FR-12.3; export endpoint streams a ZIP of markdown files; soft-delete on topic deletion; regeneration clears old page and triggers new Writer Agent job

---

## Epic 9: Newsletter Studio (Enterprise Tier)

**Goal:** Enable enterprise teams to go from curated content → polished newsletter in 15 minutes — with configurable agent, one-click draft generation, version history, and email distribution.

---

### Story 9.1: Newsletter Configuration Panel

As an enterprise user,
I want to configure my newsletter agent with tone, structure, and audience settings,
So that every generated draft matches my brand voice and target audience automatically.

**Acceptance Criteria:**

**Given** I open the Newsletter Studio
**When** I configure a newsletter profile
**Then** I can set: tone (Professional/Casual/Technical/Friendly), structure template, audience level, focus areas

**And** I can save multiple configurations (e.g., "Weekly Tech Brief", "Monthly Executive Summary")
**And** each config has a natural language custom instructions field
**And** configuration presets exist for common newsletter types
**And** saved configs are private to my enterprise workspace

**Prerequisites:** Story 6.3

**Technical Notes:** FR-14.1; `newsletter_configs` table with `enterprise_id`; multi-tenancy: configs isolated per enterprise workspace (NFR-SEC6); no cross-enterprise data leakage

---

### Story 9.2: Content Selection Interface

As an enterprise user,
I want to browse and select content items and evidence for my newsletter,
So that I pick the best stories from the curated pool before generating a draft.

**Acceptance Criteria:**

**Given** I open the content selection panel
**When** the "Highly Rated This Week" view loads
**Then** I see score-5 community-curated content + my enterprise's custom source content

**And** I can filter by: category, date range, topic
**And** I can multi-select articles and evidence items
**And** selected items show a preview before generation
**And** I can toggle which sources (community + enterprise custom) are included

**Prerequisites:** Stories 9.1, 7.1, 2.7

**Technical Notes:** FR-14.2; selection state stored in session (not persisted until draft is created); community content from Postgres `content_items` (score=5, status=finished); enterprise custom source content isolated per workspace

---

### Story 9.3: One-Click Newsletter Draft Generation

As an enterprise user,
I want to generate a polished newsletter draft in one click from my configuration and selected content,
So that I go from curation to draft in under 5 minutes.

**Acceptance Criteria:**

**Given** I have a configuration and selected content items
**When** I click "Generate Draft"
**Then** the Newsletter Agent synthesizes a draft based on config + selected evidence

**And** generation completes in under 5 minutes
**And** output formats are available: Markdown, Plain Text, HTML
**And** 90%+ of generated drafts require only minor edits (not major rewrites)
**And** the draft includes proper citations and evidence attribution
**And** the draft follows the selected structure template and matches the specified tone and audience level

**Prerequisites:** Stories 9.2, 9.1

**Technical Notes:** FR-14.3; generation queued as async job with progress indicator; newsletter agent prompt = config settings + selected evidence; output stored in `newsletter_drafts` table; multi-LLM support

---

### Story 9.4: In-App Editor & Draft Refinement

As an enterprise user,
I want to edit and refine my generated draft in the app,
So that I can polish the newsletter without switching to another tool.

**Acceptance Criteria:**

**Given** a draft has been generated
**When** I open the editor
**Then** I can edit in rich-text mode, markdown mode, or preview mode

**And** changes are auto-saved (version save < 1 second)
**And** the editor supports track changes/edit history within a session
**And** I can switch between editor and preview without losing changes

**Prerequisites:** Story 9.3

**Technical Notes:** FR-14.3; TipTap or ProseMirror for rich-text editing; markdown ↔ rich-text sync; preview renders the HTML email version

---

### Story 9.5: Version History & A/B Testing

As an enterprise user,
I want to compare different draft versions and restore previous ones,
So that I can test different angles and always revert if needed.

**Acceptance Criteria:**

**Given** I have multiple draft versions
**When** I open the version history panel
**Then** I see all previous versions with timestamps and optional tags (e.g., "Draft 1 - Technical Focus")

**And** I can compare any two versions side-by-side
**And** I can restore any previous version (creates a new version — does not overwrite)
**And** each version has a notes field for team collaboration context
**And** version history supports 1,000+ versions without performance impact

**Prerequisites:** Story 9.4

**Technical Notes:** FR-14.4; append-only versions table; restore = copy content of old version into new version record; side-by-side diff via `diff-match-patch` or similar; versions capped per draft (configurable, default 100 before archiving old ones)

---

### Story 9.6: Email Distribution

As an enterprise user,
I want to send my finished newsletter to my email list directly from Cherry,
So that my workflow stays within one tool from curation to inbox.

**Acceptance Criteria:**

**Given** I have a finished newsletter draft
**When** I send to my email list
**Then** the newsletter is delivered to all subscribers

**And** I can import, add, and remove subscribers from my list
**And** I can send a preview to test emails before full send
**And** I can schedule a send or send immediately
**And** send status is tracked per recipient (sent, failed, bounced)
**And** send queue processes 100,000+ emails per hour for large lists (< 30 min for 10K subscribers)

**Prerequisites:** Story 9.3

**Technical Notes:** FR-14.5; email via SendGrid or Mailchimp integration; HTML rendering from draft markdown; subscriber list stored in `newsletter_subscribers` table with `enterprise_id` isolation; batch send via queue (Redis/BullMQ)

---

## Epic 10: Community & Quality Operations

**Goal:** Sustain content quality and community trust through URL submission, source management, error reporting, monitoring, and observability — the operational backbone that keeps Cherry running reliably.

---

### Story 10.1: Community URL Submission for Sources

As a community member,
I want to submit URLs for the Knowledge Team to consider adding as monitored sources,
So that the community helps expand Cherry's coverage.

**Acceptance Criteria:**

**Given** I submit a URL via the contribution form
**When** the form validates the input
**Then** the URL (format, domain reachability) is validated and queued for maintainer review

**And** I receive feedback (approved/rejected/reason)
**And** approved URLs are added to the Content Ingestion Pipeline source config
**And** the submission form has rate limiting to prevent spam

**Prerequisites:** Story 5.1

**Technical Notes:** FR-6.1; submission stored in `source_submissions` table; rate limiting via IP + session; maintainer review UI (admin-only route); on approval, source is added to `sources.yaml` config

---

### Story 10.2: Curated Text Source Library Management

As a Knowledge Team member,
I want a managed library of authoritative sources (books, papers, canonical posts),
So that Evidence Layer ingestion always starts from high-quality, versioned references.

**Acceptance Criteria:**

**Given** I add a new source to the library
**When** it is saved
**Then** it is registered with full metadata: title, author, URL/PDF, publication date, priority (canonical/supplementary)

**And** the extraction pipeline (PDF → text, URL → markdown) runs automatically on new additions
**And** updated versions of sources are tracked (version history)
**And** the library is browseable with filter/sort

**Prerequisites:** Stories 3.1, 1.2

**Technical Notes:** FR-7.2; `curated_sources` table; PDF extraction triggered on upload; web extraction re-runs on URL change; priority field influences evidence weighting in Writer Agent

---

### Story 10.3: Error Reporting & Content Correction Workflow

As a user,
I want to report errors in Cherry's content and see them fixed quickly,
So that I can trust Cherry as an accurate, authoritative reference.

**Acceptance Criteria:**

**Given** I spot an error on a content page
**When** I click "Report Error"
**Then** a GitHub Issue is created with: page URL, reported error, reporter info

**And** critical errors have a fast-track correction path (same-day fix target)
**And** corrections update the "Last updated" timestamp and add to the page changelog
**And** deprecated content is marked clearly with alternatives linked

**Prerequisites:** Story 5.3

**Technical Notes:** FR-8.1; GitHub Issues integration via API; error types: factual error, outdated info, broken link, unclear explanation; corrections committed via bot account; changelog stored in page frontmatter

---

### Story 10.4: Monitoring, Observability & Alerting

As an operator,
I want structured logging, pipeline monitoring, and alerting for critical failures,
So that I can detect and resolve issues before users are impacted.

**Acceptance Criteria:**

**Given** the system is running in production
**When** any pipeline stage fails or a service goes down
**Then** an alert is sent via email and Slack within 5 minutes

**And** structured logs exist for all pipeline stages (ingestion, scoring, review, publication) with log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
**And** a scheduler monitoring dashboard shows job status and execution logs
**And** GitHub Actions logs cover build/deploy monitoring
**And** a public status page is available for transparency during incidents

**Prerequisites:** Stories 1.6, 2.7, 4.5

**Technical Notes:** NFR-M4, NFR-R1; logging via `structlog` (Python) and `pino` (TypeScript); Sentry for error tracking; uptime monitoring via Betterstack or similar; status page via Statuspage.io or custom; Slack webhook integration for alerts

---

---

_For implementation: Use the `create-story` workflow to generate individual story implementation plans from this epic breakdown._
