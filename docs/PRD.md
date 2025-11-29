# cherry-in-the-haystack - Product Requirements Document

**Author:** HK
**Date:** 2025-11-07
**Version:** 1.0

---

## Executive Summary

**cherry-in-the-haystack** evolves from a personal content curation tool into **The LLM Engineering Handbook** — a living, community-driven knowledge base that serves as the default reference for anyone building with AI products.

The product addresses the critical problem of fragmented, rapidly-changing LLM knowledge that overwhelms practitioners. Engineers, builders, and product teams currently rely on scattered Twitter posts, Discord chats, papers, repos, and blog updates that become outdated within weeks. There is no single, living source of truth that organizes this knowledge and helps people make practical decisions when building real AI products.

**The LLM Engineering Handbook provides:**
- Continuously updated, structured map of what matters right now
- Clear explanations, trade-offs, and practical examples
- Collective intelligence that compounds instead of fading
- Orientation in a chaotic, fast-moving landscape

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

**New Architecture:** The LLM Engineering Handbook Platform
> 해당 부분에 sync db　등이 들어가야 할 것으로 보입니다.
```
Stage 1: Content Ingestion (Auto-News Engine)
  ↓
Stage 2: Human Peer Review (Notion Review System)
  ↓
Stage 3: AI Synthesis (MECE Knowledge Structure)
  ↓
Stage 4: Publication (Public Handbook Web Interface)
```

**Future Vision:** "GitHub for Personal Knowledge Management"
- Personal knowledge repositories
- Cross-user synchronization with AI assistance
- Collaborative knowledge graphs

---

## Success Criteria

Success means the handbook becomes the **most time-efficient way to stay sharp in the LLM world**, where people return naturally and recommend it enthusiastically.

### User Experience Success Metrics

**Clarity:** Users consistently report "Ah, now I finally understand this"
- Measured by: User feedback, comprehension surveys, community testimonials

**Confidence:** Users know which approach to choose and why
- Measured by: Decision velocity, reduced follow-up questions, practical application reports

**Speed:** Users catch up on latest developments in minutes, not days
- Measured by: Time-to-insight metrics, return visit frequency, daily active users

**Practicality:** Users find actionable examples, architectures, prompts, benchmarks
- Measured by: Code snippet usage, reference architecture adoption, community implementations

### Community & Growth Metrics

- **Active Contributors:** 20+ team members (current baseline) growing to 50+ within 6 months
- **Content Freshness:** Critical sections updated within 1 week of major releases
- **User Engagement:**
  - 10,000 unique monthly readers within 3 months
  - 50,000 unique monthly readers within 6 months
  - Average 3+ pages per session
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

The LLM Engineering Handbook is organized into three main content sections, each with distinct content pipelines and update mechanisms.

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
> 이 부분도 rating등이 빠진 것으로 보입니다.
```
Curated Text Sources → Deduplication (chunk-level) → AI Synthesis → Vector Database → Handbook Publication
```

**Update Strategy:** Continuously updated as new authoritative books or significant lectures emerge

#### 2. Advanced Section
**Purpose:** Deep technical content not suitable for beginners or general use

**Topics:** Same domains as Basics, but with advanced depth:
> LLM에 관한 내용이긴 하지만 예시들을 조정할 필요가 있지 않을까 합니다.
- Advanced prompting (chain-of-thought, constitutional AI)
- Multi-hop RAG, hybrid search
- PEFT, LoRA, QLoRA techniques
- Multi-agent orchestration
- Custom embedding models
- Adversarial evaluation, benchmarking

**Content Pipeline:** Same as Basics section

**Update Strategy:** Continuous updates from cutting-edge research and practitioner insights

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
  > 왜 이게 Priority일까?
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
Auto-News Aggregation → Deduplication → AI Agent Scoring (1-5) → Score 5 Items → Weekly Human Approval → Direct Publish (NO synthesis)
```

**Update Strategy:** Weekly batch approval and publication of top-rated content

---

### MVP - Minimum Viable Product

**Core Infrastructure:**
- ✅ Auto-News engine configured for LLM-focused sources (Twitter, Discord, GitHub, papers, blogs)
- ✅ Deduplication system operating at content level (pre-scoring)
- ✅ AI agent 1-5 scoring system integrated into Notion
- ✅ Notion-based human review workflow with weekly approval cycle
- ✅ Vector database for deduplicated, value-added content storage
- ✅ AI synthesis agents for Basics/Advanced content (chunk-level analysis)

**Content at Launch:**
- **Basics Section:**
> ContentList/Source보고 topic 수정 필요
  - Minimum 6 core topic pages (Prompting, RAG, Fine-tuning, Agents, Embeddings, Evaluation)
  - Each topic with introductory content and practical examples
- **Advanced Section:**
  - At least 3 advanced topics with deep technical content
- **Newly Discovered:**
  - All 5 categories established with initial content
  - Minimum 10 entries per category from first month of curation

**Web Interface:**
> 우선은 깃북위주로 생각하자.
- Public-facing static website (read-only)
- Navigation structure for 3 main sections
- Clean, readable layout optimized for technical content
- Mobile-responsive design
- NO user accounts, bookmarking, search, or commenting in MVP

**Contribution Workflow:**
- GitHub PR workflow for handbook text contributions
- URL submission mechanism for new data sources
- 20-person team active (content + development contributors)

**AI Capabilities:**
- Chunk-level (paragraph) deduplication and value assessment
- Automatic identification of unique, value-adding content vs noise
- AI-assisted quality scoring (1-5 scale)
- Pattern-based content quality evaluation

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
- Public API for handbook content access
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
- Fork and customize handbook content to personal context
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
- IDE plugins for in-context handbook reference
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

For MVP, the handbook uses **Jupyter Book** for static site generation rather than a custom web application. This provides:
- Professional documentation layout out-of-the-box
- Zero infrastructure overhead for hosting
- Fast, SEO-friendly static pages
- Focus on content pipeline automation rather than web development

### System Architecture

**Newly Discovered Content Pipeline:**
```
Auto-News Ingestion
  ↓
Notion Review (1-5 scoring + weekly approval)
  ↓
Postgres Database (approved score-5 items)
  ↓
Automated GitHub Commit (markdown files)
  ↓
Jupyter Book Rebuild (GitHub Actions)
  ↓
GitHub Pages Deployment
```

**Basics/Advanced Content Pipeline:**
```
Curated Text Sources (PDFs, books, websites)
  ↓
AI Synthesis & Deduplication
  ↓
Manual GitHub PR (markdown files)
  ↓
Jupyter Book Rebuild (GitHub Actions)
  ↓
GitHub Pages Deployment
```

### Content Repository Structure

**GitHub Repository Organization:**
- Single repository for handbook content
- Separate repository for Auto-News pipeline codebase

**Content Structure (2-level depth):**
```
handbook-repo/
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

**Postgres → GitHub Pipeline:**
- **Trigger:** Weekly batch job (or on-demand trigger)
- **Process:**
  1. Query Postgres for approved score-5 items
  2. Format as markdown files with metadata (date, category, source)
  3. Direct commit to GitHub (no PR, automated committer)
  4. Organize by category folder structure
- **Idempotency:** Handle duplicate prevention and update logic
- **Metadata:** Each markdown file includes frontmatter (title, date, category, tags, source URL)

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
- **Domain:** Custom domain (e.g., `llm-handbook.dev` or `handbook.cherry-ai.dev`)
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

**Basics Section (6 core topics):**
1. Source curated content from:
   - O'Reilly books (PDF extraction)
   - Canonical blog posts and documentation
   - Academic papers and tutorials
2. AI synthesis to extract key concepts
3. Human editing for clarity and structure
4. Manual PR submission for review
5. Merge and publish

**Advanced Section (3 topics minimum):**
- Same process as Basics, but with deeper technical content

**Newly Discovered Section:**
- Seed with first month of Auto-News curation
- 10+ entries per category from existing Notion database
- Backfill high-quality content from recent months

**Timeline:**
- Basics seeding: 2-4 weeks (parallel work on 6 topics)
- Advanced seeding: 1-2 weeks (3 topics)
- Newly Discovered seeding: 1 week (batch import from existing curation)

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

### API Requirements (Future)

**Not in MVP**, but considerations for Growth phase:

**Content API:**
- REST endpoints for handbook content
- JSON responses with markdown content
- Endpoints:
  - `GET /api/sections` - List all sections
  - `GET /api/sections/{section}/topics` - Topics in section
  - `GET /api/topics/{topic}` - Topic content
  - `GET /api/search?q=query` - Search content

**Contribution API:**
- Accept URL submissions
- Webhook for GitHub PR notifications
- Integration with Notion review workflow

**Design Considerations:**
- GraphQL may be better for flexible querying
- Rate limiting and authentication for public API
- Versioning strategy (v1, v2, etc.)

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
  - Score 5 = top-tier content worthy of handbook inclusion
  - Scoring completes within 5 minutes of ingestion
  - Pattern-based learning improves scoring accuracy over time
- **Magic Thread:** 🌟 This delivers the "speed" promise - users trust the curation quality

**FR-2.2: Human Peer Review Workflow**
- **Description:** Weekly human review and approval of top-scored content in Notion
- **User Value:** Community wisdom ensures quality, not just AI judgment
- **Acceptance Criteria:**
  - Score-5 items queued in Notion review dashboard
  - Reviewers can approve, reject, or request edits
  - Weekly batch approval cycle (configurable)
  - Approved items automatically flow to next pipeline stage
  - Audit trail of reviewer decisions

**FR-2.3: Content Value Assessment**
- **Description:** AI identifies unique, value-adding information vs repetitive noise
- **User Value:** Users encounter fresh insights, not rehashed content
- **Acceptance Criteria:**
  - Chunk-level (paragraph) analysis for novelty
  - Comparison against vector database of existing content
  - "Unique" flag for truly novel information
  - Value score based on: novelty, depth, practical applicability, evidence quality

### 3. AI Synthesis & Knowledge Structuring

**FR-3.1: MECE Knowledge Organization**
- **Description:** Structure content into Mutually Exclusive, Collectively Exhaustive taxonomy
- **User Value:** Users can navigate logically without gaps or overlaps - delivers the "clarity" promise
- **Acceptance Criteria:**
  - 3 main sections: Basics, Advanced, Newly Discovered
  - 2-level hierarchy: parent concepts → child implementations
  - No concept should fit in multiple categories
  - All LLM engineering topics covered (95% coverage target)
  - Taxonomy evolves based on emerging topics
- **Magic Thread:** 🌟 This is the "orientation in chaos" - the structured map that makes users say "now I understand"

**FR-3.2: Content Synthesis for Basics/Advanced**
- **Description:** AI synthesizes curated sources into cohesive explanations
- **User Value:** Users get distilled knowledge, not raw dumps of information
- **Acceptance Criteria:**
  - Extract key concepts from multiple sources
  - Generate unified explanations with examples
  - Identify trade-offs and decision criteria
  - Cite original sources for verification
  - Flag conflicting information for human review
- **Domain Constraint:** EdTech quality standards - must be accurate and pedagogically sound

**FR-3.3: Evolving Taxonomy Management**
- **Description:** Continuously update content categories as LLM field evolves
- **User Value:** Handbook stays current with emerging topics and techniques
- **Acceptance Criteria:**
  - New categories can be added without restructuring
  - Content can be reassigned when taxonomy changes
  - Category deprecation with content migration plan
  - "Newly Discovered" categories reviewed quarterly for promotion to Basics/Advanced

### 4. Content Publishing & Distribution

**FR-4.1: Automated Publication Pipeline**
- **Description:** Approved content automatically flows from Postgres → GitHub → Jupyter Book → Public site
- **User Value:** Fresh content reaches users within hours, not days - delivers the "speed" promise
- **Acceptance Criteria:**
  - Weekly batch: Postgres → GitHub commit (markdown files)
  - GitHub push triggers Jupyter Book rebuild (under 5 minutes)
  - GitHub Pages deployment automatic
  - Zero-downtime deployments
  - Rollback capability for broken builds
- **Magic Thread:** 🌟 Weekly updates keep the handbook feeling "alive"

**FR-4.2: Structured Handbook Display**
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

**FR-4.3: Content Metadata & Organization**
- **Description:** Every page includes structured metadata for discoverability
- **User Value:** Users find content via search engines and social sharing
- **Acceptance Criteria:**
  - Frontmatter: title, date, category, tags, source URL
  - SEO meta tags (title, description, keywords)
  - Open Graph tags for social sharing
  - Descriptive URLs (e.g., `/basics/rag/naive-rag`)
  - Auto-generated sitemap

**FR-4.4: "Newly Discovered" Card Layouts**
- **Description:** Visual card-based presentation for recent updates
- **User Value:** Users quickly scan latest developments with visual hierarchy
- **Acceptance Criteria:**
  - Card format with: title, summary (1-2 lines), date, category badge, external link
  - 5 category groups (Model Updates, Framework Updates, Productivity Tools, Business Cases, How People Use AI)
  - Collapsible sections for accumulated news
  - Chronological ordering within categories
  - "Last 30 days" and "Archive" views

### 5. Content Contribution & Collaboration

**FR-5.1: GitHub PR Workflow for Content**
- **Description:** Contributors submit handbook text via GitHub pull requests
- **User Value:** Community can contribute knowledge while maintaining quality gates
- **Acceptance Criteria:**
  - Contributors fork repo, create branch, submit PR
  - PR template with contribution guidelines
  - Automated checks: markdown linting, link validation
  - Maintainer review and approval required
  - Merge triggers automatic handbook rebuild
- **Magic Thread:** 🌟 Community contributions make intelligence "compound"

**FR-5.2: URL Submission for Sources**
- **Description:** Community submits URLs for Auto-News to monitor
- **User Value:** Crowdsourced source discovery expands coverage
- **Acceptance Criteria:**
  - Simple form/interface for URL submission
  - Validation: URL format, domain reachability
  - Queue for maintainer review
  - Approved URLs added to Auto-News source list
  - Feedback to submitter (approved/rejected/reason)

**FR-5.3: Contributor Recognition**
- **Description:** Track and display contributor names/avatars
- **User Value:** Recognition motivates ongoing participation
- **Acceptance Criteria:**
  - "Contributors" page listing all contributors
  - GitHub profile integration
  - Contribution stats (PRs merged, URLs submitted, reviews)
  - Optional: contributor badges/tiers

### 6. Content Source Management

**FR-6.1: Auto-News Source Configuration**
- **Description:** Manage which sources Auto-News monitors for "Newly Discovered"
- **User Value:** Focused on LLM-specific sources, not generic tech news
- **Acceptance Criteria:**
  - Configuration file lists: source URL, category mapping, polling frequency
  - Sources include: Twitter accounts, Discord channels, GitHub orgs, RSS feeds, blogs
  - Per-source enable/disable toggle
  - Source health monitoring (last successful pull, error rate)

**FR-6.2: Curated Text Management for Basics/Advanced**
- **Description:** Manage library of curated sources (books, papers, canonical posts)
- **User Value:** Authoritative, high-quality foundation content
- **Acceptance Criteria:**
  - Document registry: source metadata (title, author, URL, PDF, publication date)
  - Extraction pipeline: PDF → text, web → markdown
  - Version tracking for updated sources
  - Source prioritization (canonical vs supplementary)

### 7. Quality Control & Moderation

**FR-7.1: Content Approval Gates**
- **Description:** Multi-stage approval prevents low-quality content from publication
- **User Value:** Users trust the handbook as consistently high-quality
- **Acceptance Criteria:**
  - Stage 1: AI scoring (1-5, only 5s proceed)
  - Stage 2: Human peer review (weekly approval)
  - Stage 3: Automated checks (markdown, links, formatting)
  - Stage 4: Maintainer approval for GitHub PRs
- **Magic Thread:** 🌟 Quality gates deliver the "confidence" promise

**FR-7.2: Content Correction & Updates**
- **Description:** Fix errors, update outdated information, improve clarity
- **User Value:** Handbook remains accurate and trustworthy over time
- **Acceptance Criteria:**
  - Error reporting mechanism (GitHub issues)
  - Fast-track corrections for critical errors
  - "Last updated" dates show freshness
  - Changelog for major page updates
  - Deprecated content marked clearly with alternatives

**FR-7.3: Conflict Resolution for Contradictory Information**
- **Description:** Handle cases where sources disagree
- **User Value:** Users see multiple perspectives on controversial topics
- **Acceptance Criteria:**
  - Flag contradictions during synthesis
  - Present multiple viewpoints with evidence
  - Community discussion mechanism (future: comments)
  - Expert endorsements for preferred approaches

### 8. Vector Database & Semantic Search (Backend)

**FR-8.1: Vector Storage for Deduplication**
- **Description:** Store embeddings of all unique content chunks
- **User Value:** Enables intelligent deduplication and similarity detection
- **Acceptance Criteria:**
  - Embeddings generated for all approved content
  - Vector database indexes: source, category, date, topic
  - Similarity search: cosine similarity threshold for duplicates
  - Efficient querying (under 100ms for similarity check)

**FR-8.2: Semantic Search Foundation (Future)**
- **Description:** Vector database enables future semantic search capabilities
- **User Value:** Not in MVP, but foundation laid for Growth phase
- **Acceptance Criteria:**
  - Embeddings compatible with future search API
  - Metadata supports faceted search
  - Related content identification ready

---

## Acceptance Criteria Summary

**MVP Launch Readiness:**
- ✅ 6 Basics topics live with practical examples
- ✅ 3 Advanced topics with deep content
- ✅ 5 "Newly Discovered" categories populated (10+ items each)
- ✅ Auto-News pipeline operational (ingestion → review → publish)
- ✅ Jupyter Book deployed on GitHub Pages with custom domain
- ✅ GitHub PR workflow documented and tested
- ✅ 20+ active contributors onboarded
- ✅ Content freshness: at least one "Newly Discovered" update per week

---

## Non-Functional Requirements

These quality attributes ensure the handbook delivers on its promise of being the **most time-efficient way to stay sharp in the LLM world.**

### Performance

**Why it matters for THIS product:** Speed is one of the three core value promises. Users must be able to "catch up in minutes, not days."

**NFR-P1: Page Load Performance**
- Handbook pages load in under 2 seconds on 3G connection
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
- Postgres → GitHub commit: batch of 50 items in under 2 minutes
- Jupyter Book rebuild: full site build under 5 minutes

**NFR-P4: API Rate Limiting Compliance**
- Respect LLM provider rate limits (OpenAI, Gemini, Ollama)
- Exponential backoff for transient failures
- Queue management for batch processing
- Cost optimization through caching and deduplication

### Scalability

**Why it matters for THIS product:** Content and user base expected to grow 5x within 6 months. Platform must scale gracefully.

**NFR-S1: Content Volume Scaling**
- Support 1,000+ handbook pages without performance degradation
- Vector database handles 100,000+ embedded chunks efficiently
- Postgres handles 10,000+ reviewed items
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

**Why it matters for THIS product:** Users must trust the handbook as a dependable reference. "Living knowledge base" requires consistent updates.

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
- Clean API contract between Auto-News and Postgres
- Structured data format for content items (JSON schema)
- Error handling for malformed data
- Version compatibility between Auto-News and handbook repo

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

**NFR-I4: Vector Database Integration**
- Pluggable architecture supports multiple providers (Milvus, ChromaDB, Pinecone)
- Consistent embedding format across providers
- Migration path between vector DB providers
- Backup/restore procedures documented

**NFR-I5: Multi-LLM Provider Support**
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

- **Project Overview:** C:\Users\Hankeol\Desktop\Dev\cherry-in-the-haystack\docs\project-overview.md
- **Architecture Documentation:** C:\Users\Hankeol\Desktop\Dev\cherry-in-the-haystack\docs\architecture-api.md
- **Auto-News Upstream Reference:** C:\Users\Hankeol\Desktop\Dev\cherry-in-the-haystack\bmad\docs\reference\auto-news-upstream\autonews-README.md

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
   - Validate technical decisions for Auto-News → Handbook transformation
   - Document integration points and data flows

4. **Implementation**
   - Follow BMM Phase 4 sprint planning
   - Execute stories with `/bmad:bmm:workflows:dev-story`

---

## Product Magic Summary

**The LLM Engineering Handbook delivers "orientation in chaos" through:**

🌟 **Comprehensive Coverage** - Auto-News aggregates from 10+ sources so users don't have to monitor dozens of channels

🌟 **Intelligent Curation** - AI scoring + human review filters 80% noise, surfacing only top-tier insights

🌟 **MECE Knowledge Structure** - Logical navigation without gaps or overlaps makes users say "now I understand"

🌟 **Living Updates** - Weekly "Newly Discovered" content keeps the handbook feeling alive and current

🌟 **Community Intelligence** - 20+ contributors make collective knowledge compound instead of fade

🌟 **Clarity, Confidence, Speed** - Users consistently report: "This is exactly what I needed, at the right level, up-to-date"

**The "wow" moment:** When someone realizes they can follow the map instead of drowning in noise - finding the exact distillation they needed, saving days of research.

**Future vision:** Evolves into "GitHub for Personal Knowledge Management" where everyone maintains knowledge repos and syncs with the community through AI-powered collaboration.

---

_This PRD captures the essence of cherry-in-the-haystack's transformation from personal curation tool to the default reference for AI builders worldwide._

_Created through collaborative discovery between HK and AI facilitator using BMad Method._

_Date: 2025-11-07_

