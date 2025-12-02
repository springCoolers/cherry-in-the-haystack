# cherry-in-the-haystack - Product Requirements Document

**Author:** HK
**Date:** 2025-11-07
**Version:** 1.0

---

## Executive Summary

**cherry-in-the-haystack** evolves from a personal content curation tool into **Cherry for LLM Engineers** — a living, community-driven knowledge base that serves as the default reference for anyone building with AI products.

The product addresses the critical problem of fragmented, rapidly-changing LLM knowledge that overwhelms practitioners. Engineers, builders, and product teams currently rely on scattered Twitter posts, Discord chats, papers, repos, and blog updates that become outdated within weeks. There is no single, living source of truth that organizes this knowledge and helps people make practical decisions when building real AI products.

**Cherry for LLM Engineers provides:**
- Continuously updated, structured map of what matters right now
- Clear explanations, trade-offs, and practical examples
- Collective intelligence that compounds instead of fading
- Orientation in a chaotic, fast-moving landscape
- Living knowledge graph connecting concepts, evidence, and sources

### What Makes This Special

**"Orientation in chaos through collective intelligence that compounds."**

This isn't just documentation — it's a living knowledge base sustained by a community of active practitioners that becomes more valuable every week. The magic happens when someone realizes:

> *"This isn't just information — it's the exact distillation of what I needed, at the right level, and up-to-date."*

**The "Wow" Moments:**
- A founder reads "Choosing your embedding model" and instantly knows the trade-offs for their use case
- An engineer finds a clean, minimal reference architecture for retrieval or agent orchestration that just clicks
- A newcomer sees they can follow the map instead of drowning in noise
- Users experience: **Clarity** ("Ah, now I understand"), **Confidence** ("I know which approach to choose"), and **Speed** ("I caught up in minutes, not days")

---

## Project Classification

**Technical Type:** Web Application + API Backend (Hybrid)
**Domain:** EdTech / Knowledge Management
**Complexity:** Medium

### Architecture Evolution

The product builds on the existing Auto-News infrastructure, transforming it from a personal curation tool into a multi-stage, human-in-the-loop knowledge synthesis platform:

**Current Architecture:** Auto-News (Personal Content Aggregation)
- Event-driven data pipeline with Apache Airflow
- LLM-powered categorization, ranking, summarization
- Output to Notion workspaces

**New Architecture:** Cherry for LLM Engineers Platform
```
Stage 1: Content Ingestion (Auto-News Engine)
  ↓
Stage 2: Knowledge Team Review (Notion Review System)
  ↓
Stage 3: Knowledge Graph Building (Graph DB with Ontology + Evidence + Link Layers)
  ↓
Stage 4: Writer Agent Synthesis (AI-generated pages from knowledge graph)
  ↓
Stage 5: Publication (Public Web Interface)
```

**Knowledge Infrastructure: Concept-Centric Graph Database**

A three-layer knowledge system optimized for stable concept ontology with dynamic evidence:

- **1. Concept Layer** (Stable, normalized)
  - Abstract ideas as unique noun-phrase nodes (e.g., "Evaluation-Driven Development")
  - Concepts reused across all sources for consistency
  - Relations between concepts: prerequisite, related, subtopic, extends, contradicts
  - Evidence NOT stored in concept nodes (only linked)
  - Each concept includes: title, summary, relations, sources

- **2. Evidence Layer** (High volume, source-attached)
  - Paragraphs/snippets with full source metadata
  - Types: paraphrase, direct quote, figure reference
  - Evidence can link to multiple concepts
  - Schema: evidence_id, source, location, text, excerpt, comment, tags, linked_concepts

- **3. Linking Layer** (Dynamic mappings)
  - Connects concepts ↔ evidence via typed relations
  - Link schema: concept_id, evidence_id, relation_type, confidence_score
  - Every evidence must link to ≥1 concept
  - Enables dynamic relation blocks in UI with embedded evidence previews

**Design Goals:**
- Clean concept graph (concepts only, no evidence nodes)
- Evidence previews embedded inside relation blocks
- Stable concept ontology + dynamic evidence accumulation

**Future Vision:** "GitHub for Personal Knowledge Management"
- Personal knowledge repositories
- Cross-user synchronization with AI assistance
- Collaborative knowledge graphs

---

## Success Criteria

Success means Cherry becomes the **most time-efficient way to stay sharp in the LLM world**, where people return naturally and recommend it enthusiastically.

### User Experience Success Metrics

**Clarity:** Users consistently report "Ah, now I finally understand"
- Measured by: User feedback, comprehension surveys, community testimonials

**Confidence:** Users know which approach to choose and why
- Measured by: Decision velocity, reduced follow-up questions, practical application reports

**Speed:** Users catch up on latest developments in minutes, not days
- Measured by: Time-to-insight metrics, return visit frequency, daily active users

**Practicality:** Users find actionable examples, architectures, prompts, benchmarks
- Measured by: Code snippet usage, reference architecture adoption, community implementations

### Community & Growth Metrics

- **Active Contributors:** 20+ team members (current baseline) growing to 50+ within 6 months
  - **Knowledge Team:** Structured subset responsible for weekly news review, monthly concept reviews, and study sessions
- **Content Freshness:** Critical sections updated within 1 week of major releases
- **User Engagement:**
  - 10,000 unique monthly readers within 3 months
- **Community Impact:**
  - Recognized as go-to reference in AI engineering communities (Twitter, Discord, Reddit mentions)
  - Referenced in production codebases and technical blogs
  - Contributors include practitioners from leading AI companies

### Technical Quality Metrics

- **Content Quality:** AI-assisted curation maintains 90%+ approval rating from human reviewers
- **Knowledge Coverage:** MECE (Mutually Exclusive, Collectively Exhaustive) structure covers 95% of common LLM engineering decisions
- **Update Velocity:** New content ingested, reviewed, and published within 48 hours of submission

---

## Product Scope

Cherry for LLM Engineers is organized into three main content sections, each with distinct content pipelines and update mechanisms.

### Content Structure

#### 1. Basics Section
**Purpose:** Foundation concepts covered in established resources (O'Reilly books, canonical lectures)

**Topics:**
- Prompting techniques and patterns
- Retrieval-Augmented Generation (RAG)
- Fine-tuning strategies
- Agent architectures
- Embeddings and vector databases
- Evaluation methodologies

**Content Pipeline:**
```
Curated Text Sources → Evidence Layer Storage → Ontology Building → Writer Agent Synthesis → Publication
```

**Content Promotion Flow:**
- New concepts emerge in **Advanced** section first
- Concepts with sustained importance (metric-based evaluation) promote to **Basics** section
- Monthly review cycle (2nd Saturday) for concept promotion decisions

**Update Strategy:** Continuously updated as new authoritative books or significant lectures emerge

#### 2. Advanced Section
**Purpose:** Deep technical content not suitable for beginners or general use

**Topics:** Same domains as Basics, but with advanced depth:
- Advanced prompting (chain-of-thought, constitutional AI)
- Multi-hop RAG, hybrid search
- PEFT, LoRA, QLoRA techniques
- Multi-agent orchestration
- Custom embedding models
- Adversarial evaluation, benchmarking

**Content Pipeline:** Same as Basics section (Evidence Layer → Ontology → Writer Agent)

**Update Strategy:** Continuous updates from cutting-edge research and practitioner insights. New concepts appear here first before potential promotion to Basics.

#### 3. Newly Discovered Section
**Purpose:** Fresh, high-value content from the rapidly evolving LLM ecosystem

**Categories** (evolving taxonomy):

1. **Model Updates**
   - New model releases (GPT-4.5, LLaMA3, Claude 4, etc.)
   - Version changes: model size, token limits, inference speed
   - API updates: features, pricing, endpoints (function calling, embeddings)
   - Protocol/auth changes (one-liner + external link)

2. **Framework/Library/Tools Updates**
   - Ecosystem landscape map (4-6 key tools, digest format)
   - Link to comprehensive landscape: https://malywut.github.io/ai-engineering-landscape/
   - Update cards: 1-2 line summaries of key changes
   - Stable/Beta releases and deprecation notices
   - Major dependency updates (Accelerate, PEFT, etc.)
   - Collapsible accumulated news archive

3. **Productivity Tools**
   - "Our Mini Product Hunt" - curated productivity tool directory
   - **Hall of Fame:** Proven tools that enhance AI development (Lovable, Superclaude, etc.)
   - **General:** Newly introduced, trending productivity tools

4. **Business Cases & Case Studies** ⭐ (Priority)
   - Company product launches (chatbots, document automation) with architecture details
   - Conference presentations (e.g., Baemin's text-to-SQL implementation)
   - VC funding & M&A trends in LLM space
   - ROI analysis, success/failure stories
   - Productivity research results (3-line summary + references)

5. **How People Use AI**
   - Domain-specific prompts and workflows
   - Brief news items ("AI chat adoption in schools", emerging use patterns)

**Content Pipeline:**
```
Auto-News Aggregation → Deduplication → AI Agent Scoring (1-5) → Knowledge Team Weekly Review → Graph DB Mapping → Direct Publish (NO synthesis)
```

**Knowledge Team Review Process (Weekly - Wednesday):**
1. Assigned team members review their allocated news items in Notion DB
2. Team validates and corrects:
   - Summary accuracy
   - Score (1-5 scale)
   - Relation to ontology graph (LLM-assisted mapping)
3. Status changed to "finished" when review complete
4. Top 20 items (score 5, sorted) flow to weekly newsletter generation

**Update Strategy:** Weekly batch approval and publication of top-rated content

---

### MVP - Minimum Viable Product

**Core Infrastructure:**
- ✅ Auto-News engine configured for LLM-focused sources (Twitter, Discord, GitHub, papers, blogs)
- ✅ Vector database & system operating at content level (pre-scoring)
- ✅ AI agent 1-5 scoring system integrated into Notion
- ✅ Notion-based Knowledge Team review workflow with weekly approval cycle
- ✅ Graph Database with three-layer architecture:
  - Ontology Layer: Concept nodes and relationships
  - Evidence Layer: Source texts and materials
  - Link Layer: Concept-to-evidence mappings
- ✅ Writer Agent for Basics/Advanced page generation from knowledge graph

**Content at Launch:**
- **Basics Section:**
  - Topics extracted from Curated Books and Lectures
- **Advanced Section:**
  - Topics extracted from Curated Books and Lectures
- **Newly Discovered:**
  - All 5 categories established with initial content
  - Minimum 10 entries per category from first month of curation

**Web Interface:**
- Public-facing static website (read-only)
- Navigation structure for 3 main sections
- Clean, readable layout optimized for technical content
- Mobile-responsive design
- NO user accounts, bookmarking, search, or commenting in MVP

**Contribution Workflow:**
- GitHub PR workflow for content contributions
- URL submission mechanism for new data sources
- 20+ person team active (content + development contributors)
- **Knowledge Team** (subset of contributors):
  - Weekly review cycle (Wednesday) for news validation and ontology mapping
  - Monthly concept promotion meetings (2nd Saturday)
  - Wednesday study sessions for evidence layer seeding

**AI Capabilities:**
- Chunk-level (paragraph) deduplication and value assessment
- Automatic identification of unique, value-adding content vs noise
- AI-assisted quality scoring (1-5 scale)
- LLM-based ontology graph mapping (concept-to-news relationships)
- Writer Agent for page generation:
  - Loads concept + connected concepts + relationships from Graph DB
  - Collects mapped evidence sources (글감)
  - Generates appropriate outline structure
  - Composes pages by citing/paraphrasing evidence

**What's NOT in MVP:**
- In-app editing
- User accounts and personalization
- Advanced search functionality
- Commenting and discussion features
- Bookmarking and reading lists
- Email notifications
- API access for programmatic use

---

### Growth Features (Post-MVP)

**Enhanced Web Experience:**
- Full-text search across all sections
- User accounts with reading history
- Bookmarking and personal reading lists
- Table of contents with progress tracking
- Dark mode and reading preferences

**Community Features:**
- In-app editing for approved contributors
- Comment and discussion threads per page
- Contributor profiles and recognition
- Community voting on content priorities
- Suggested edits and improvement workflow

**Content Intelligence:**
- Semantic search using embeddings
- Related content recommendations
- Personalized content suggestions based on reading history
- "What's changed since last visit" summaries
- Email digests for subscribed topics

**Synthesis Enhancements:**
- Multi-source synthesis for controversial topics
- Automatic comparison tables (e.g., "Embedding models compared")
- Timeline visualization for framework evolution
- Automated "changelog" for major topic updates

**Developer Tools:**
- Public API for content access
- Webhook integrations
- RSS feeds per category
- Markdown export functionality

**Analytics & Insights:**
- Most-read topics and trending sections
- Content gap analysis
- Community contribution metrics dashboard
- Impact tracking (references, citations)

---

### Vision Features (Future)

**"GitHub for Personal Knowledge Management"**

**Personal Knowledge Repositories:**
- Users maintain their own private knowledge bases
- Fork and customize content to personal context
- Private notes and annotations layer over public content
- Personal taxonomy and organization preferences

**Knowledge Synchronization:**
- Cross-user "sync" mechanism powered by AI agents
- Discover when others update topics you're tracking
- Merge insights from multiple contributors
- Conflict resolution for diverging perspectives

**Collaborative Knowledge Graphs:**
- Visual knowledge maps showing concept relationships
- Community-built concept ontology
- Link discovery between disparate sources
- Exploration interface for knowledge navigation

**AI-Powered Personal Assistants:**
- Personal AI agent that understands your knowledge gaps
- Proactive recommendations based on your work context
- Automated synthesis of your reading into personal summaries
- Query interface: "What do I need to know about X for my project Y?"

**Advanced Synthesis:**
- Multi-perspective synthesis (academic vs practitioner vs business)
- Automatic contradiction detection and resolution proposals
- Temporal analysis: "How has thinking evolved on X?"
- Predictive insights: "What's likely to matter in 6 months?"

**Integration Ecosystem:**
- Notion, Obsidian, Roam integration for personal notes
- IDE plugins for in-context reference
- Slack/Discord bots for team knowledge sharing
- CI/CD integration for automated best practice checks

**Governance & Quality:**
- Reputation system for contributors
- Expert endorsements for critical content
- Peer review workflows with specialized tracks
- Conflict resolution mechanisms for contentious topics

---

## Web Application + API Backend Specific Requirements

### MVP Architecture: Static Site Generation (Jupyter Book)

For MVP, Cherry uses **Jupyter Book** for static site generation rather than a custom web application. This provides:
- Professional documentation layout out-of-the-box
- Zero infrastructure overhead for hosting
- Fast, SEO-friendly static pages
- Focus on content pipeline automation rather than web development

### System Architecture

**Newly Discovered Content Pipeline:**
```
Auto-News Ingestion + Deduplication
  ↓
AI Scoring (1-5) + Auto-assignment to Knowledge Team members
  ↓
Knowledge Team Review (Notion - Wednesday weekly)
  - Validate summaries
  - Confirm scores
  - LLM-assisted ontology graph mapping
  ↓
Graph DB Link Layer (concept-to-news mappings)
  ↓
Automated GitHub Commit (top 20 items, markdown files)
  ↓
Jupyter Book Rebuild (GitHub Actions)
  ↓
GitHub Pages Deployment
```

**Basics/Advanced Content Pipeline:**
```
Curated Text Sources (PDFs, books, websites, study materials)
  ↓
Evidence Layer Storage (Graph DB)
  ↓
Knowledge Team Study Sessions (Wednesday - evidence review)
  ↓
Ontology Extraction (new concept noun phrases detected monthly)
  ↓
Knowledge Team Concept Review (2nd Saturday monthly)
  - Evaluate new concept candidates (word count metrics)
  - Discuss and finalize TOC updates
  - Decide concept promotion (Advanced → Basics)
  ↓
Writer Agent Page Generation
  - Load concept + connected concepts + relationships
  - Collect mapped evidence sources
  - Generate outline
  - Compose page (cite/paraphrase evidence)
  ↓
Automated GitHub Commit (new/updated pages)
  ↓
Jupyter Book Rebuild (GitHub Actions)
  ↓
GitHub Pages Deployment
```

### Concept Page Structure (UI Design)

**Design Philosophy:** Concept-first rendering with dynamic relation blocks and embedded evidence previews.

**Page Layout for Basics/Advanced Concepts:**

```
Concept: [Concept Title]
Summary: [1-2 sentence definition]

Prerequisites:
  - [Related Concept Name]
      Why: [1-line explanation of relationship]
      ↳ "[Evidence excerpt]" — [Source] [paraphrase/direct/figure]
  - [Another Prerequisite]
      Why: [...]
      ↳ "[Evidence preview]" — [Source] [type]

Related:
  - [Related Concept]
      Why: [...]
      ↳ "[Evidence excerpt]" — [Source] [type]

Subtopics:
  - [Narrower Concept]
      Why: [...]
      ↳ "[Evidence excerpt]" — [Source] [type]

Extends:
  - [Advanced Version Concept]
      Why: [...]
      ↳ "[Evidence excerpt]" — [Source] [type]

Sources & Commentary:
  1. [Source A] — [Reading order suggestion, e.g., "easiest intro"]
  2. [Source B] — [Context, e.g., "complements A"]
  3. [Paper C] — [Comment, e.g., "canonical reference"]

Contributors: [Knowledge Team members who curated this concept]

[Optional: Graph visualization showing this concept's position]
```

**Dynamic Relation Blocks:**
- Each relation type (Prerequisites, Related, Subtopics, Extends, Contradicts) is a repeatable block
- Rendered only if relations exist (empty sections not shown)
- Evidence previews embedded directly under each related concept
- Multiple evidence items per relation displayed as indented list

**Evidence Preview Format:**
- Excerpt: 1-2 sentences from source material
- Source: Book/paper/blog with location (e.g., "Ch3", "Section 2.1")
- Comment type: [paraphrase], [direct], [figure] indicates how evidence is used

### Content Repository Structure

**GitHub Repository Organization:**
- Single repository for Cherry content
- Separate repository for Auto-News pipeline codebase

**Content Structure (2-level depth):**
```
cherry-repo/
├── basics/
│   ├── prompting/
│   │   ├── index.md (parent concept)
│   │   ├── basic-prompting.md
│   │   └── prompt-templates.md
│   ├── rag/
│   │   ├── index.md (parent concept)
│   │   ├── naive-rag.md
│   │   └── advanced-rag.md
│   └── ... (fine-tuning, agents, embeddings, evaluation)
├── advanced/
│   ├── prompting/
│   │   ├── chain-of-thought.md
│   │   └── constitutional-ai.md
│   └── ...
├── newly-discovered/
│   ├── model-updates/
│   │   └── 2025-11-07-gpt45-release.md
│   ├── framework-updates/
│   ├── productivity-tools/
│   ├── business-cases/
│   └── how-people-use-ai/
└── _config.yml (Jupyter Book configuration)
```

**Parent-Child Concept Hierarchy:**
- **Parent:** High-level concept page (e.g., "RAG", "Prompting", "Fine-tuning")
- **Child:** Specific implementations or techniques (e.g., "Naive RAG", "Basic Prompting", "LoRA Fine-tuning")
- Maximum 2 levels of depth to maintain clarity and navigation simplicity

### Automation Requirements
**GitHub → Jupyter Book Deployment:**
- **Trigger:** GitHub Actions on push to main branch
- **Process:**
  1. Build Jupyter Book HTML
  2. Deploy to GitHub Pages
  3. Invalidate cache if needed
- **Build Time:** Target under 5 minutes for full rebuild
- **Incremental Builds:** Investigate Jupyter Book incremental build support

### Jupyter Book Configuration

**Standard Configuration with Customizations:**

**Required Features:**
- Table of contents with 2-level hierarchy
- Search functionality (built-in Jupyter Book search)
- Mobile-responsive design (default)
- Syntax highlighting for code blocks
- Markdown + Myst-NB support

**Custom Styling Needs:**
- Brand colors and logo
- Card layouts for "Newly Discovered" section
- Collapsible sections for accumulated news
- External link indicators
- Category badges/tags

**Plugins & Extensions:**
- `sphinx-design` for card layouts and grids
- `sphinx-togglebutton` for collapsible sections
- `sphinxext-opengraph` for social media previews
- Custom CSS for branding and special layouts

**Navigation:**
- Three primary sections in sidebar (Basics, Advanced, Newly Discovered)
- Category grouping within each section
- Breadcrumbs for orientation
- "Last updated" timestamps on pages

### Hosting & Deployment

**GitHub Pages:**
- **Domain:** Custom domain (https://springcoolers.github.io/llm-handbook/_contents/intro.html)
- **SSL:** Automatic via GitHub Pages
- **Branch:** Deploy from `gh-pages` branch (Jupyter Book standard)
- **Build Frequency:** On every commit to main (automated)

**Performance:**
- Static HTML/CSS/JS - no server-side processing
- CDN delivery via GitHub Pages
- Target page load: Under 2 seconds on 3G connection
- Optimize images and assets for web delivery

**SEO Optimization:**
- Server-side rendered HTML (static, fully crawlable)
- Sitemap auto-generated by Jupyter Book
- Meta tags and Open Graph for social sharing
- Structured data for search engines (schema.org)
- Descriptive URLs (e.g., `/basics/rag/naive-rag` not `/page123`)

### Content Seeding Strategy

**Initial Population:**

**Basics Section:**
1. Source curated content from:
   - O'Reilly books (PDF extraction)
   - Canonical blog posts and documentation
   - Academic papers and tutorials
2. AI extracts and normalize paragraph level's key concepts
3. AI writes relation(link), check the ontology on Graph DB for similar concept, add or merge with the concepts
4. Writer Agent writes pages, based on TOC given by knowledge team 
5. Human editing for clarity and structure
6. Manual PR submission for review, Merge and publish

**Advanced Section :**
- Same process as Basics, but with deeper technical content

**Newly Discovered Section:**
- Seed with first month of Auto-News curation
- 10+ entries per category from existing Notion database
- Backfill high-quality content from recent months

### Browser & Platform Support

**Supported Browsers:**
- Modern evergreen browsers (Chrome, Firefox, Safari, Edge)
- Last 2 major versions
- No Internet Explorer support

**Mobile Support:**
- Responsive design (Jupyter Book default)
- Touch-friendly navigation
- Optimized for mobile reading experience

**Accessibility:**
- WCAG 2.1 AA compliance target
- Keyboard navigation
- Screen reader compatibility
- Semantic HTML structure
- Sufficient color contrast

---

## Functional Requirements

Organized by user-facing capabilities, each requirement connects to the core product value: **helping practitioners find clarity, confidence, and speed in the rapidly-evolving LLM landscape.**

### 1. Content Ingestion & Aggregation

**FR-1.1: Multi-Source Content Collection**
- **Description:** Automatically aggregate LLM-related content from diverse sources (Twitter, Discord, GitHub, papers, blogs, RSS feeds)
- **User Value:** Users get comprehensive coverage without manually monitoring dozens of channels
- **Acceptance Criteria:**
  - Auto-News engine pulls from at least 10 configured sources
  - New content discovered within 24 hours of publication
  - Source metadata preserved (URL, date, author, platform)
  - Configurable source priorities and categories
- **Magic Thread:** 🌟 This is the foundation - comprehensive coverage enables the "wow" moment of discovering everything in one place

**FR-1.2: Intelligent Deduplication**
- **Description:** Identify and filter duplicate or redundant content before processing
- **User Value:** Users see unique insights, not the same news repeated 10 times
- **Acceptance Criteria:**
  - Content-level deduplication before scoring (exact matches, near-duplicates)
  - Chunk-level deduplication for Basics/Advanced synthesis (paragraph similarity)
  - 95%+ accuracy in identifying true duplicates
  - Preserve original source for merged duplicates
- **Domain Constraint:** Must run before AI scoring to reduce API costs

### 2. Content Quality Assessment

**FR-2.1: AI-Powered Content Scoring**
- **Description:** Automatically evaluate content relevance and quality on 1-5 scale
- **User Value:** Only high-quality, relevant content reaches users - the 80% noise is filtered out
- **Acceptance Criteria:**
  - AI agent scores content based on defined criteria (relevance, depth, novelty, practicality)
  - Score 5 = top-tier content worthy of inclusion
  - Scoring completes within 5 minutes of ingestion
  - Pattern-based learning improves scoring accuracy over time
- **Magic Thread:** 🌟 This delivers the "speed" promise - users trust the curation quality

**FR-2.2: Knowledge Team Review Workflow**
- **Description:** Structured weekly review and approval process managed by Knowledge Team in Notion
- **User Value:** Community wisdom and domain expertise ensures quality, not just AI judgment
- **Acceptance Criteria:**
  - Score-5 items auto-assigned to Knowledge Team members in Notion
  - Team members can validate summaries, adjust scores, and request edits
  - Weekly review cycle (Wednesday) with structured meeting
  - LLM-assisted ontology graph mapping during review
  - Status tracking: pending → in_review → finished
  - Top 20 finished items (score 5) flow to newsletter generation
  - Audit trail of all review decisions

**FR-2.3: Content Value Assessment**
- **Description:** AI identifies unique, value-adding information vs repetitive noise
- **User Value:** Users encounter fresh insights, not rehashed content
- **Acceptance Criteria:**
  - Chunk-level (paragraph) analysis for novelty
  - Comparison against vector database of existing content
  - "Unique" flag for truly novel information
  - Value score based on: novelty, depth, practical applicability, evidence quality

### 3. Knowledge Graph & Database Management

**FR-3.1: Graph Database Three-Layer Architecture**
- **Description:** Concept-centric knowledge system with stable ontology and dynamic evidence
- **User Value:** Structured knowledge enables intelligent synthesis, relationship discovery, and evidence traceability
- **Acceptance Criteria:**

  **Concept Layer (Stable):**
  - Store concepts as unique noun-phrase nodes only (no sentences, no examples in nodes)
  - Concepts must be reusable across all sources
  - Relation types: prerequisite, related, subtopic, extends, contradicts (dynamic, extensible)
  - Evidence NEVER stored in concept nodes (only linked)
  - Concept schema: title, summary, relations (with embedded evidence previews), sources, contributors
  - Concepts must support dynamic relation block rendering in UI

  **Evidence Layer (High Volume):**
  - Store paragraphs/snippets separately from concepts
  - Required metadata: source, location, text, excerpt, comment, tags, linked_concepts
  - Evidence types: paraphrase, direct quote, figure reference
  - Evidence can link to multiple concepts (many-to-many)
  - Evidence previews format: excerpt + source + comment (shown in relation blocks)

  **Linking Layer (Dynamic):**
  - Link schema: concept_id, evidence_id, relation_type, confidence_score
  - Every evidence MUST link to ≥1 concept
  - Support relation-type filtering and confidence thresholds
  - Enable dynamic relation block queries (e.g., "get all prerequisites with evidence for concept X")

  **Performance:**
  - Graph queries complete in under 500ms for writer agent
  - Support concurrent reads during page generation
  - Efficient traversal for concept → related concepts → evidence chains

  **Integration:**
  - Coexists with Vector DB (used only for deduplication)
  - Graph view shows concepts only (no evidence nodes cluttering visualization)

- **Magic Thread:** 🌟 The concept-centric graph makes knowledge reusable and evidence traceable

**FR-3.2: Ontology Extraction & Concept Discovery**
- **Description:** Monthly extraction of new concept noun phrases from evidence layer
- **User Value:** Cherry stays current with emerging LLM concepts and techniques
- **Acceptance Criteria:**
  - Monthly batch job (2nd Saturday) extracts new concept candidates from evidence layer
  - Word count and frequency metrics filter noise vs meaningful concepts
  - LLM-assisted concept relationship detection
  - Concept candidates presented to Knowledge Team for review
  - Approved concepts added to Ontology Layer with initial relationships
  - New concepts default to Advanced section (promotion to Basics based on sustained importance)

**FR-3.3: Evidence Collection & Study Sessions**
- **Description:** Knowledge Team study sessions populate Evidence Layer with curated texts
- **User Value:** High-quality source materials ensure accuracy and depth
- **Acceptance Criteria:**
  - Wednesday study sessions review texts (books, papers, documentation)
  - Reviewed texts stored in Evidence Layer with metadata (source, date, topic, quality)
  - Text chunking for efficient storage and retrieval
  - Evidence tagged with relevant concept associations
  - Study session notes captured for context

### 4. AI Synthesis & Knowledge Structuring

**FR-4.1: MECE Knowledge Organization**
- **Description:** Structure content into Mutually Exclusive, Collectively Exhaustive taxonomy
- **User Value:** Users can navigate logically without gaps or overlaps - delivers the "clarity" promise
- **Acceptance Criteria:**
  - 3 main sections: Basics, Advanced, Newly Discovered
  - 2-level hierarchy: parent concepts → child implementations
  - No concept should fit in multiple categories
  - All LLM engineering topics covered (95% coverage target)
  - Taxonomy evolves based on emerging topics
- **Magic Thread:** 🌟 This is the "orientation in chaos" - the structured map that makes users say "now I understand"

**FR-4.2: Writer Agent for Page Generation**
- **Description:** AI agent generates Basics/Advanced pages from knowledge graph using structured schemas
- **User Value:** Users get distilled, well-structured knowledge from multiple evidence sources with full traceability
- **Acceptance Criteria:**
  - **Input:** Concept node from Ontology Layer (triggered monthly after concept review)
  - **Step 1:** Query CONCEPT schema from Graph DB
    - Load target concept + connected concepts + relationships
    - Retrieve relation types (prerequisite, related, subtopic, extends, contradicts)
  - **Step 2:** Query LINK schema to collect evidence_ids for this concept
    - Filter by relation type and confidence threshold
  - **Step 3:** Query EVIDENCE schema to retrieve full evidence details
    - Full text, excerpts, source metadata, comment types
  - **Step 4:** Generate page structure following Concept Page UI Design:
    - Title and summary
    - Dynamic relation blocks (only non-empty sections)
    - Evidence previews embedded in each relation item
    - Sources & Commentary section with reading order
    - Contributors list
  - **Step 5:** Compose page content by:
    - Citing evidence with proper attribution
    - Paraphrasing where appropriate
    - Maintaining evidence preview format (excerpt + source + comment type)
    - Including "why" explanations for each relation
  - Generated pages follow style guide (clarity, examples, trade-offs)
  - Flag conflicting evidence from multiple sources for Knowledge Team review
  - Page generation completes within 10 minutes per concept
  - Output: Markdown file conforming to Concept Page Structure
- **Domain Constraint:** EdTech quality standards - must be accurate and pedagogically sound
- **Magic Thread:** 🌟 Writer agent transforms fragmented evidence into coherent, traceable knowledge

**FR-4.3: Concept Promotion Flow (Advanced → Basics)**
- **Description:** Promote concepts from Advanced to Basics based on sustained importance
- **User Value:** Basics section reflects truly foundational concepts, not just trendy topics
- **Acceptance Criteria:**
  - New concepts default to Advanced section
  - Metric-based evaluation tracks concept importance over time (mentions, usage, stability)
  - Monthly Knowledge Team review (2nd Saturday) evaluates promotion candidates
  - Promoted concepts move from Advanced → Basics with page updates
  - Promotion decisions documented with rationale
  - Community can suggest promotion candidates via GitHub issues

**FR-4.4: Evolving Taxonomy Management**
- **Description:** Continuously update content categories as LLM field evolves
- **User Value:** Cherry stays current with emerging topics and techniques
- **Acceptance Criteria:**
  - New categories can be added without restructuring
  - Content can be reassigned when taxonomy changes
  - Category deprecation with content migration plan
  - "Newly Discovered" categories reviewed quarterly for relevance

### 5. Content Publishing & Distribution

**FR-5.1: Automated Publication Pipeline**
- **Description:** Approved content automatically flows from Notion → GitHub → Jupyter Book → Public site
- **User Value:** Fresh content reaches users within hours, not days - delivers the "speed" promise
- **Acceptance Criteria:**
  - Weekly batch: Notion → GitHub commit (markdown files)
  - GitHub push triggers Jupyter Book rebuild (under 5 minutes)
  - GitHub Pages deployment automatic
  - Zero-downtime deployments
  - Rollback capability for broken builds
- **Magic Thread:** 🌟 Weekly updates keep Cherry feeling "alive"

**FR-5.2: Structured Content Display**
- **Description:** Jupyter Book renders content with professional layout and navigation
- **User Value:** Users can read, navigate, and search efficiently
- **Acceptance Criteria:**
  - 3-section navigation (Basics, Advanced, Newly Discovered)
  - 2-level TOC with parent-child hierarchy
  - Built-in search functionality
  - Mobile-responsive design
  - Syntax highlighting for code
  - "Last updated" timestamps
  - Breadcrumb navigation

### 6. Content Contribution & Collaboration

**FR-6.1: GitHub PR Workflow for Direct Content**
- **Description:** Contributors can also submit complete pages via GitHub pull requests (alternative to evidence submission)
- **User Value:** Flexibility for contributors who prefer writing full pages vs submitting evidence
- **Acceptance Criteria:**
  - Contributors fork repo, create branch, submit PR
  - PR template with contribution guidelines
  - Automated checks: markdown linting, link validation
  - Maintainer review and approval required
  - Merge triggers automatic rebuild
- **Note:** Evidence submission (FR-6.1) is preferred for knowledge graph integration

**FR-6.2: URL Submission for Sources**
- **Description:** Community submits URLs for Auto-News to monitor
- **User Value:** Crowdsourced source discovery expands coverage
- **Acceptance Criteria:**
  - Simple form/interface for URL submission
  - Validation: URL format, domain reachability
  - Queue for maintainer review
  - Approved URLs added to Auto-News source list
  - Feedback to submitter (approved/rejected/reason)

### 7. Content Source Management

**FR-7.1: Auto-News Source Configuration**
- **Description:** Manage which sources Auto-News monitors for "Newly Discovered"
- **User Value:** Focused on LLM-specific sources, not generic tech news
- **Acceptance Criteria:**
  - Configuration file lists: source URL, category mapping, polling frequency
  - Sources include: Twitter accounts, Discord channels, GitHub orgs, RSS feeds, blogs
  - Per-source enable/disable toggle
  - Source health monitoring (last successful pull, error rate)

**FR-7.2: Curated Text Management for Basics/Advanced**
- **Description:** Manage library of curated sources (books, papers, canonical posts)
- **User Value:** Authoritative, high-quality foundation content
- **Acceptance Criteria:**
  - Document registry: source metadata (title, author, URL, PDF, publication date)
  - Extraction pipeline: PDF → text, web → markdown
  - Version tracking for updated sources
  - Source prioritization (canonical vs supplementary)

### 8. Quality Control & Moderation

**FR-8.1: Content Correction & Updates**
- **Description:** Fix errors, update outdated information, improve clarity
- **User Value:** Cherry remains accurate and trustworthy over time
- **Acceptance Criteria:**
  - Error reporting mechanism (GitHub issues)
  - Fast-track corrections for critical errors
  - "Last updated" dates show freshness
  - Changelog for major page updates
  - Deprecated content marked clearly with alternatives

### 9. Vector Database & Semantic Search (Backend)

**FR-9.1: Vector Storage for Deduplication**
- **Description:** Store embeddings of all unique content chunks
- **User Value:** Enables intelligent deduplication and similarity detection
- **Acceptance Criteria:**
  - Embeddings generated for all approved content
  - Vector database indexes: source, category, date, topic
  - Similarity search: cosine similarity threshold for duplicates
  - Efficient querying (under 100ms for similarity check)

---

## Acceptance Criteria Summary

**MVP Launch Readiness:**
- ✅ Auto-News pipeline operational (ingestion → review → publish)
- ✅ Jupyter Book deployed on GitHub Pages with custom domain
- ✅ GitHub PR workflow documented and tested
- ✅ Content freshness: at least one "Newly Discovered" update per week

---

## Non-Functional Requirements

These quality attributes ensure Cherry delivers on its promise of being the **most time-efficient way to stay sharp in the LLM world.**

### Performance

**Why it matters for THIS product:** Speed is one of the three core value promises. Users must be able to "catch up in minutes, not days."

**NFR-P1: Page Load Performance**
- Pages load in under 2 seconds on 3G connection
- Time to First Contentful Paint (FCP): under 1 second
- Largest Contentful Paint (LCP): under 2.5 seconds
- Images and assets optimized for web delivery
- Lazy loading for images below the fold

**NFR-P2: Search Response Time**
- Built-in Jupyter Book search returns results in under 500ms
- Search indexes updated within 1 minute of content deployment
- Graceful degradation if search temporarily unavailable

**NFR-P3: Pipeline Processing Performance**
- Auto-News content ingestion: process 100+ items/hour
- AI scoring: complete scoring within 5 minutes of ingestion
- Deduplication check: under 100ms per item (vector similarity)
- AI synthesis: generate synthesized page within 10 minutes
- Notion → GitHub commit: batch of 50 items in under 2 minutes
- Jupyter Book rebuild: full site build under 5 minutes

**NFR-P4: API Rate Limiting Compliance**
- Respect LLM provider rate limits (OpenAI, Gemini, Ollama)
- Exponential backoff for transient failures
- Queue management for batch processing
- Cost optimization through caching and deduplication

### Scalability

**Why it matters for THIS product:** Content and user base expected to grow 5x within 6 months. Platform must scale gracefully.

**NFR-S1: Content Volume Scaling**
- Support 1,000+ pages without performance degradation
- **Graph DB** handles 10,000+ concept nodes with 100,000+ relationships efficiently
- Vector database handles 100,000+ embedded chunks efficiently (deduplication only)
- Jupyter Book builds scale to 1,000+ pages (under 10 minutes)

**NFR-S2: Traffic Scaling**
- Handle 50,000 unique monthly visitors (10x growth from baseline)
- GitHub Pages CDN handles traffic spikes (e.g., viral social posts)
- Concurrent user capacity: 1,000+ simultaneous readers
- Static site architecture provides natural horizontal scalability

**NFR-S3: Contributor Scaling**
- Support 50+ active contributors (2.5x current team)
- GitHub PR workflow handles 20+ open PRs simultaneously
- Notion review workflow supports 10+ reviewers
- Clear contribution guidelines reduce maintainer bottleneck

**NFR-S4: Source Scaling**
- Auto-News monitors 50+ sources without degradation
- Add new sources without pipeline reconfiguration
- Handle 500+ new items per day during major release cycles

### Reliability & Availability

**Why it matters for THIS product:** Users must trust Cherry as a dependable reference. "Living knowledge base" requires consistent updates.

**NFR-R1: Public Site Uptime**
- 99.5% uptime target (GitHub Pages SLA)
- Zero-downtime deployments
- Graceful fallback for broken builds (previous version remains live)
- Automated health checks via GitHub Actions

**NFR-R2: Pipeline Reliability**
- Auto-News ingestion: 99% successful pull rate from active sources
- AI scoring: 95% success rate (with retry logic)
- Weekly publish cycle: 100% execution (manual override if automation fails)
- Failed pipeline stages alert maintainers via notifications

**NFR-R3: Data Integrity**
- No data loss during pipeline processing
- Idempotent operations (re-running doesn't create duplicates)
- Postgres backups: daily with 30-day retention
- **Graph DB backups:** daily with 60-day retention (all three layers)
- Vector database backups: weekly with 60-day retention
- Git history serves as content version control

**NFR-R4: Error Recovery**
- Automated retry with exponential backoff for transient failures
- Dead-letter queue for permanently failed items
- Manual intervention workflow for critical failures
- Rollback capability for bad deployments (git revert)

### Security

**Why it matters for THIS product:** Protect API credentials and maintain trust. Public site is read-only, reducing attack surface.

**NFR-SEC1: Credential Management**
- API keys stored in environment variables (not in code)
- GitHub Secrets for sensitive credentials in Actions
- Notion API tokens rotated quarterly
- LLM provider API keys with minimal required permissions
- Postgres credentials use strong passwords with limited access

**NFR-SEC2: Input Validation**
- URL submissions validated (format, domain, reachability)
- Markdown content sanitized to prevent XSS
- File uploads restricted (if implemented in future)
- Rate limiting on URL submission form (prevent spam)

**NFR-SEC3: Dependency Security**
- Automated dependency scanning (Dependabot, Snyk)
- Quarterly security updates for critical dependencies
- No known high-severity CVEs in production dependencies
- Python packages from trusted sources (PyPI)

**NFR-SEC4: Data Privacy**
- No collection of personal user data in MVP (static site, no analytics)
- Source URLs submitted by users may contain author names (public info)
- API keys and internal data not exposed in public repos
- Compliance with GitHub's data privacy policies

### Accessibility

**Why it matters for THIS product:** As educational infrastructure for global community, must be accessible to all builders regardless of ability.

**NFR-A1: WCAG 2.1 AA Compliance**
- Keyboard navigation for all interactive elements
- Screen reader compatibility (semantic HTML, ARIA labels)
- Sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- Alt text for all meaningful images
- Captions or transcripts for video content (if added)

**NFR-A2: Responsive Design**
- Mobile-friendly layout (Jupyter Book default)
- Touch targets minimum 44x44 pixels
- Text reflows without horizontal scrolling
- Font size user-adjustable via browser settings

**NFR-A3: Content Readability**
- Plain language where possible (technical terms explained)
- Hierarchical heading structure (H1 → H2 → H3)
- Lists for scannable content
- Code blocks with syntax highlighting
- Avoid jargon without definitions

### Integration

**Why it matters for THIS product:** Multiple systems must work together seamlessly for the automated pipeline to function.

**NFR-I1: Auto-News Integration**
- Clean API contract between Auto-News, Notion and Postgres
- Structured data format for content items (JSON schema)
- Error handling for malformed data
- Version compatibility between Auto-News and Cherry repo

**NFR-I2: Notion Integration**
- Notion API rate limits respected (3 requests/second)
- Robust handling of Notion API changes
- Fallback for Notion downtime (manual review queue)
- Export capability if Notion migration needed

**NFR-I3: GitHub Integration**
- GitHub Actions workflows reliable and maintainable
- Clear separation: content repo vs Auto-News codebase
- Automated commits use dedicated bot account
- Webhook for deployment notifications

**NFR-I4: Graph Database Integration**
- Three-layer architecture (Ontology, Evidence, Link) consistently maintained
- Clean API for Writer Agent to query concepts, relationships, and evidence
- Support for Neo4j or compatible graph database
- Efficient graph traversal queries (under 500ms)
- Backup/restore procedures for all three layers
- Migration path if graph DB provider changes

**NFR-I5: Vector Database Integration**
- Pluggable architecture supports multiple providers (Milvus, ChromaDB, Pinecone)
- Consistent embedding format across providers
- Migration path between vector DB providers
- Backup/restore procedures documented
- **Note:** Vector DB used only for deduplication (Graph DB is primary knowledge store)

**NFR-I6: Multi-LLM Provider Support**
- Graceful fallback between OpenAI, Gemini, Ollama
- Configuration-driven provider selection
- Cost tracking per provider
- Consistent output format across providers

### Maintainability

**Why it matters for THIS product:** 20+ contributors need clear, well-organized codebase to collaborate effectively.

**NFR-M1: Code Quality**
- Python code follows PEP 8 style guide
- Type hints for function signatures
- Comprehensive docstrings for public APIs
- Linting enforced in CI/CD (flake8, black)
- Unit test coverage target: 70%+

**NFR-M2: Documentation**
- README files in all major directories
- Architecture documentation (this PRD + technical docs)
- Setup/installation guide for new contributors
- Troubleshooting guide for common issues
- API documentation for internal modules

**NFR-M3: Modularity**
- Clear separation of concerns (ingestion, scoring, synthesis, publishing)
- Operator pattern for content types (existing Auto-News pattern)
- Pluggable components (LLM providers, vector databases)
- Configuration files, not hardcoded values

**NFR-M4: Monitoring & Observability**
- Structured logging for all pipeline stages
- Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Airflow UI for DAG monitoring (existing)
- GitHub Actions logs for build/deploy monitoring
- Alerting for critical failures (email, Slack)

**NFR-M5: Testing Strategy**
- Unit tests for core logic (deduplication, scoring algorithms)
- Integration tests for pipeline stages
- End-to-end smoke tests for full pipeline
- Manual testing checklist for Jupyter Book deployments
- Test data fixtures for reproducible testing

### Data Quality & Freshness

**Why it matters for THIS product:** "Living knowledge base" promise requires continuous, high-quality updates.

**NFR-DQ1: Content Freshness**
- "Newly Discovered" updated at least weekly
- "Last updated" timestamps accurate to the hour
- Stale content flagged after 6 months (for Basics/Advanced)
- Major LLM releases reflected within 48 hours

**NFR-DQ2: Content Accuracy**
- Source citations required for all factual claims
- Contradictory information flagged and surfaced
- Error corrections within 24 hours of reported issue
- Community review before major updates

**NFR-DQ3: Metadata Quality**
- All pages have required frontmatter (title, date, category, tags)
- SEO metadata complete and descriptive
- Categories assigned consistently
- Tags follow controlled vocabulary

---

## References

- **Project Overview:** .\docs\project-overview.md
- **Architecture Documentation:** .\docs\architecture-api.md
- **Auto-News Upstream Reference:** .\docs\reference\auto-news-upstream\autonews-README.md

---

## Next Steps

**Immediate Next Step: Epic & Story Breakdown**

Run: `/bmad:bmm:workflows:create-epics-and-stories`

This workflow will:
1. Load this PRD automatically
2. Transform requirements into implementable epics
3. Create bite-sized stories (optimized for 200k context dev agents)
4. Organize by delivery phases

**Subsequent Steps:**

2. **UX Design** (if needed for custom Jupyter Book styling)
   - Run: `/bmad:bmm:workflows:create-ux-design`
   - Focus on card layouts, collapsible sections, branding

3. **Architecture Review**
   - Run: `/bmad:bmm:workflows:architecture`
   - Validate technical decisions for Auto-News → Cherry transformation
   - Document integration points and data flows

4. **Implementation**
   - Follow BMM Phase 4 sprint planning
   - Execute stories with `/bmad:bmm:workflows:dev-story`

---

## Product Magic Summary

**Cherry for LLM Engineers delivers "orientation in chaos" through:**

🌟 **Comprehensive Coverage** - Auto-News aggregates from 10+ sources so users don't have to monitor dozens of channels

🌟 **Intelligent Curation** - AI scoring + human review filters 80% noise, surfacing only top-tier insights

🌟 **MECE Knowledge Structure** - Logical navigation without gaps or overlaps makes users say "now I understand"

🌟 **Living Updates** - Weekly "Newly Discovered" content keeps Cherry feeling alive and current

🌟 **Community Intelligence** - 20+ contributors make collective knowledge compound instead of fade

🌟 **Clarity, Confidence, Speed** - Users consistently report: "This is exactly what I needed, at the right level, up-to-date"

**The "wow" moment:** When someone realizes they can follow the map instead of drowning in noise - finding the exact distillation they needed, saving days of research.

**Future vision:** Evolves into "GitHub for Personal Knowledge Management" where everyone maintains knowledge repos and syncs with the community through AI-powered collaboration.

---

_This PRD captures the essence of cherry-in-the-haystack's transformation from personal curation tool to the default reference for AI builders worldwide._

_Created through collaborative discovery between HK and AI facilitator using BMad Method._

_Date: 2025-11-07_

