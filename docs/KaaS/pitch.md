# Cherry KaaS — The Content Layer for Agent Commerce

"Agent Resource Development"
BuidlHack 2026 | Status Network Track + NEAR Protocol Track

> **Cherry KaaS is Stripe for AI agent knowledge.** Agents query human-curated knowledge, every query gets a gasless on-chain receipt, Karma tiers govern pricing, and curators earn 40% — all without a single gas fee.

---

## The Problem

AI agents are blind. They scrape the web, call general-purpose LLMs, and confidently recommend deprecated tools, hallucinate APIs, and miss entire domains of knowledge. 61% of enterprises report AI accuracy issues. The cost of wrong knowledge cascades through agent-to-agent chains.

The haystack is enormous — RSS feeds, changelogs, Discord announcements, research papers, YouTube videos. The signal is buried in noise. And no one is solving this *for the agents that increasingly run our systems*.

Finding **relevant, current, verified** knowledge is the bottleneck.

---

## What We Built

Cherry KaaS (Knowledge-as-a-Service) turns a live, human-curated knowledge graph into an agent-native marketplace with blockchain provenance.

**The foundation already runs in production:**

- **80+** knowledge concepts — RAG architectures, embedding models, prompt engineering, and more
- **600+** evidence nodes — each a sourced, verified data point from real articles, papers, and docs
- **20+** domain expert curators — weekly review cycles keep knowledge current
- **MECE-structured knowledge graph** — mutually exclusive, collectively exhaustive relationships
- **Automated ingestion** — RSS, Twitter, YouTube, blogs, PDFs flow through AI-powered scoring and synthesis

**KaaS is the API layer that opens this to any AI agent.**

---

## How It Works

An agent queries Cherry KaaS. Five things happen, fully autonomous:

1. **Agent registers** — permissionless, no KYC. Gets an API key and wallet address.
2. **Agent syncs with catalog** — 80+ concepts with quality scores, free to explore.
3. **Agent purchases knowledge** — ~20 credits per concept. Karma tier discounts apply (0%–30%).
4. **Structured response delivers** — evidence nodes, source attribution, quality scores, curator comments. Not raw search results — curated, verified knowledge.
5. **On-chain provenance recorded** — SHA256 hash of the response stored gaslessly. Permanent proof of what the agent consumed, when, and from which source.

Then: **40% of query revenue flows to the creator/curator** who maintains that knowledge. Sustainable creation/curation, not volunteer burnout.

---

## User Flows

### For Agent Builders

```
Register agent → Browse catalog (free) → Purchase concept (~20 credits)
→ Receive structured knowledge → Provenance on-chain → Repeat
```

- **MCP Server**: One import line in Claude, GPT, LangChain, or CrewAI. 97M+ potential agent instances.
- **REST API**: `/v1/` versioned endpoints. Register, browse, purchase, follow, deposit credits.
- **WebSocket Subscriptions**: Follow a concept, receive real-time push when knowledge changes. Kills the stale vector store problem.

**Knowledge Gap Analysis** — An agent submits what it already knows. We compare against 80+ concepts and return matched, gaps, and prioritized recommendations. A diagnostic for your AI's blind spots.

### For Curators

```
Curate knowledge (weekly reviews) → Knowledge enters graph
→ Agents purchase → 40% reward distributed on-chain → Withdraw gaslessly
```

20+ domain experts already maintain the knowledge graph. KaaS turns their volunteer effort into a revenue stream. Every query touching their concepts earns them on-chain rewards, withdrawable gaslessly on Status Network.


### For Private Queries (NEAR TEE)

```
Agent toggles Privacy Mode → Query encrypted → Enters TEE (Qwen3-30B on Intel TDX)
→ Processed against knowledge graph → Response returns → No one saw the query
→ On-chain provenance hash recorded on NEAR
```

Agents querying sensitive topics — proprietary architectures, security vulnerabilities, competitive intelligence — can't afford to expose their queries. Privacy Mode routes through NEAR AI Cloud TEE. The server, NEAR, and the infrastructure never see what was asked.

---

## How It's Made

### Smart Contracts

**EVM — CherryCredit.sol** (Status Network)

- `deposit()` — Agent deposits credits
- `consumeCredit()` — Deducts credits with Karma-tiered discounts
- `recordProvenance()` — Stores SHA256 hash of response data, gaslessly
- `distributeReward()` — 40% to curator, gaslessly

Deployed at `0x153DAcC25Ad05DcFb1f258c28eb47e48c13e682b` (Status Sepolia). Redeploying on Hoodi Testnet.

**NEAR — cherry_credit.ts** (NEAR Protocol)

- Same credit, provenance, and reward logic, written in near-sdk-js
- Deployed at `tomatojams.testnet`
- Handles NEAR-side provenance for TEE queries

### Backend

- **NestJS** API server with modular architecture
- **6 MCP tools** exposed via `mcp-server.ts` — register, browse, purchase, follow, compare, query, subscribe
- **Chain adapter pattern** (`chain-adapter/interface.ts`) — Status, and NEAR, implementations behind a clean interface
- **Karma tier engine** in `kaas-agent.entity.ts` — Bronze/Silver/Gold/Platinum with 0%/5%/15%/30% credit discounts

### Privacy Layer (NEAR)

- **NEAR AI Cloud TEE** — OpenAI-compatible endpoint at `https://cloud-api.near.ai/v1/chat/completions` / **Qwen3-30B** running on Intel TDX — hardware-attested private inference
- **Privacy toggle** in `kaas-llm.controller.ts` — agents choose transparent or private mode
- Attestation proves exact model and execution environment

### Frontend

- **Next.js** web dashboard — agent registration, catalog browsing, Karma tier display, credit balance, provenance receipts

### AI Pipeline

- **Python AI services** — automated ingestion, scoring, classification, synthesis
- Sources: RSS, Twitter/X, YouTube, Substack, arXiv, documentation sites
- MECE classification into 80+ concepts with evidence node extraction

---

## Track Alignment

### Status Network — Best Privacy-First or Agentic App

| Requirement                             | How We Meet It                                                                               |
| --------------------------------------- | -------------------------------------------------------------------------------------------- |
| AI agents transacting onchain gaslessly | MCP server → REST API → WebSocket. Every query is a gasless transaction.                     |
| Karma-tiered throughput                 | Bronze (0%) to Platinum (30%) discounts. Higher Karma = more queries/day.                    |
| Spam-protected access                   | Karma as sybil-resistance. Earned through staking, bridging, liquidity provision. Soulbound. |
| Autonomous pipeline                     | Register → browse → purchase → provenance → curator reward. Zero human in the loop.          |
| Privacy-preserving provenance           | SHA256 hashes on-chain. Activity is provable but not linkable to real-world identity.        |

**This is our strongest track.** Cherry KaaS is fundamentally an agent-to-blockchain application. The entire product is designed around autonomous agents consuming knowledge and transacting on-chain without gas.

### NEAR Protocol — TEE-Based Privacy

| Criteria (Weight)          | How We Meet It                                                                                      |
| -------------------------- | --------------------------------------------------------------------------------------------------- |
| Innovation (30%)           | TEE + on-chain provenance combination. Private queries with public proof. No one else does this.    |
| Impact (25%)               | Enterprise agents querying sensitive topics need privacy. / creators' rights are protected          |
| Technical Excellence (20%) | Clean multi-chain adapter pattern. NEAR contract mirrors EVM logic. OpenAI-compatible TEE endpoint. |
| Privacy Design (15%)       | Layered: TEE for queries, on-chain hashes for proof, pseudonymous identity. Opt-in toggle.          |
| Presentation (10%)         | Side-by-side demo: transparent vs TEE private query. The contrast makes the value obvious.          |

**Innovation angle:** We're not just running an LLM in a TEE. We're running a knowledge marketplace where the query-response lifecycle is private (TEE) but the economic transaction is verifiable (on-chain).

---

## Vision

### Soulbound Reputation (Status Network)

Karma is the beginning. The long-term vision is a soulbound reputation system where curators earn non-transferable reputation for quality contributions. Agents that consistently deliver accurate results build verifiable track records. This extends to digital twins — on-chain representations of a curator's expertise that continue to serve agents autonomously, backed by proof of competence.

### Privacy-Preserving Knowledge Delivery

Curators choose what to reveal. Their prompts, proprietary knowledge structures, and custom tools remain private. KaaS delivers *extracted knowledge* from the knowledge base, not the raw source. This matters for copyright and know-how protection — a tax attorney's curated guide is valuable precisely because the reasoning methodology is not exposed.

With TEE (NEAR), this privacy is cryptographically guaranteed. The knowledge is useful; the know-how remains the creator's. And the chain proves it.

---

## The Demo

1. **Agent asks a question**: "What's the best embedding model for Korean text?"
2. **Structured answer returns**: 3 evidence nodes, each with source, date, and curator comment. Quality score: 4.2/5.
3. **On-chain receipt appears in real-time**: Status Network explorer shows the gasless transaction. Permanent proof.
4. **Karma tier displayed**: Agent's on-chain reputation visible. Higher tiers get credit discounts.
5. **Curator gets paid**: 40% of query revenue distributed to the human who curated this knowledge.
6. **Privacy Mode toggle**: Same query through NEAR TEE. Query invisible to everyone. Provenance hash still recorded.

**The "wow" moment**: Two queries side-by-side — one transparent (visible in logs), one private (only the provenance hash remains). Private queries, public proof.

---

## Built On

| Layer | Tech |
|---|---|
| Blockchain (EVM) | Status Network — gasless transactions, Karma reputation, provenance |
| Blockchain (NEAR) | NEAR Protocol — TEE-attested private queries, provenance |
| Agent Protocol | MCP — native integration with Claude, GPT, LangChain, CrewAI |
| Knowledge Base | Cherry Knowledge Graph — 80+ concepts, 600+ evidence, 20+ curators |
| Smart Contracts | Solidity (EVM) + near-sdk-js (NEAR) |
| Backend | NestJS + TypeScript |
| Frontend | Next.js |
| AI Services | Python — ingestion, scoring, classification, synthesis |
| Privacy | NEAR AI Cloud TEE (Qwen3-30B, Intel TDX) |

---

*Cherry in the Haystack → Cherry KaaS: Curated knowledge, agent-native access, on-chain proof.*
