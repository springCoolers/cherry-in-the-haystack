# Cherry in the Haystack (w/Marketplace)

> "Where Curators Build Knowledge for Subscribed Agents to Upskill"

A monorepo that continuously ingests AI Engineering content from the web, scores it for quality, synthesizes it into structured knowledge pages, and publishes it as a searchable handbook.

---

## 🏆 BuidlHack2026 Submission — Cherry In the Marketplace 

**Cherry in the Haystack Marketplace is a Knowledge-as-a-Service (KaaS)**. This opens this curated handbook to AI agents via **MCP Protocol** + **on-chain payment/provenance**. Agents browse the catalog, purchase concepts with gasless crypto, and receive provable, auditable knowledge receipts on-chain.

### Multi-chain Deployment

| Track | Network | Contract / Account | Status |
|---|---|---|---|
| **Status Network** (Primary) | Status Sepolia — Chain ID `1660990954` | [`0x153DAcC25Ad05DcFb1f258c28eb47e48c13e682b`](https://sepoliascan.status.network/address/0x153DAcC25Ad05DcFb1f258c28eb47e48c13e682b) | ✅ Live, gasless |
| **NEAR AI Cloud** (TEE LLM) | `cloud-api.near.ai/v1` (Qwen3-30B) | API-level integration | ✅ Live |
| **NEAR Protocol** (L1 contract) | NEAR Testnet | [`tomatojams.testnet`](https://testnet.nearblocks.io/address/tomatojams.testnet) | ✅ Live |
| BNB Chain (opBNB) | Chain ID `5611` | — | ⏸ Skipped (track optional) |

**Key on-chain transactions (NEAR):**
- Contract deploy: [`HwTSRXMWJA5tWuLAw6n5YLKnhytm6McNJtxaTDwASJE9`](https://testnet.nearblocks.io/txns/HwTSRXMWJA5tWuLAw6n5YLKnhytm6McNJtxaTDwASJE9)
- Functions exercised on-chain: `init`, `deposit`, `recordProvenance`

### Features

- 🛒 **Agent Shopping** — 9 AI/ML concepts catalog, purchase with credits (20cr/purchase, 25cr/follow)
- 🔗 **Provenance on-chain** — Every purchase records a hash on Status Network; every re-purchase generates a unique hash (no duplicate rejection)
- 🔒 **Privacy Mode (NEAR AI TEE)** — Toggle in dashboard. When ON, sensitive agent data (knowledge list, purchase intent, content payload) is relayed through NEAR AI Cloud's TEE before server processing. Free chat is generated entirely in TEE.
- 🎁 **Curator Rewards** — 40% of each purchase auto-distributed to knowledge curator, recorded on-chain
- 🔌 **MCP Server** — stdio (Claude Desktop/Code) + Streamable HTTP. 5 tools + 2 resources. Elicitation & Sampling supported.
- 🌐 **WebSocket realtime** — knowledge updates, MCP session tracking

### Repo Guide for Marketplace

| Path | Role |
|---|---|
| [`apps/contracts/contracts/CherryCredit.sol`](apps/contracts/contracts/CherryCredit.sol) | Solidity contract (Status, EVM) |
| [`apps/contracts-near/src/cherry_credit.ts`](apps/contracts-near/src/cherry_credit.ts) | NEAR near-sdk-js contract |
| [`apps/api/src/modules/kaas/`](apps/api/src/modules/kaas/) | NestJS API (catalog, purchase, credits, MCP, rewards) |
| [`apps/web/components/cherry/kaas-*.tsx`](apps/web/components/cherry/) | Web dashboard / console / catalog |
| [`apps/api/src/mcp-server.ts`](apps/api/src/mcp-server.ts) | MCP stdio server |
| [`apps/docs/KaaS/NEAR-integration.md`](apps/docs/KaaS/NEAR-integration.md) | NEAR integration full details |
| [`apps/docs/KaaS_plan/`](apps/docs/KaaS_plan/) | Implementation plan, checklist, progress log |
| [`apps/docs/KaaS/prd.md`](apps/docs/KaaS/prd.md), [`architecture.md`](apps/docs/KaaS/architecture.md), [`epics.md`](apps/docs/KaaS/epics.md) | Product / architecture / epic docs |

### Marketplace Environment Variables (server-side)

```bash
# Status Network
DEPLOYER_PRIVATE_KEY=<server wallet for tx signing>
CHERRY_CREDIT_ADDRESS=0x153DAcC25Ad05DcFb1f258c28eb47e48c13e682b
STATUS_RPC_URL=https://public.sepolia.rpc.status.network
CHAIN_ADAPTER=status
DEMO_FALLBACK=false

# NEAR AI Cloud (LLM TEE)
NEAR_AI_KEY=sk-...   # cloud.near.ai/keys

# OpenAI (default non-privacy LLM)
OPENAI_API_KEY=sk-proj-...
```

Frontend env (public):
```bash
NEXT_PUBLIC_API_URL=http://localhost:4000
```

### Quick Marketplace Demo Flow

1. `pnpm dev` → web at `:3000`, API at `:4000`
2. Open the KaaS Dashboard, register a new Agent (connect MetaMask for wallet address)
3. Catalog → select concept → **Purchase** — tx signed by server, recorded on Status
4. Toggle **🔒 Privacy Mode** ON → repeat purchase → content + intent relayed via NEAR AI TEE; chat LLM answered by Qwen3-30B
5. Dashboard → **Rewards** tab shows 40% curator revenue with tx links
6. `claude mcp add cherry-kaas apps/api/start-mcp.sh --env KAAS_AGENT_API_KEY=...` → Claude Desktop reads catalog & purchases natively

---

## Prerequisites

| Tool           | Version |
| -------------- | ------- |
| Node.js        | 20+     |
| pnpm           | 9+      |
| Python         | 3.10+   |
| Poetry         | 1.8+    |
| Docker Desktop | Latest  |

---

## Quick Start

```bash
# 1. Install TypeScript dependencies
pnpm install

# 2. Start local database services (PostgreSQL 16 + pgvector, GraphDB, Redis)
docker-compose up -d

# 3. Copy environment variables and fill in your values
cp .env.example .env

# 4. Install Python dependencies
poetry install

# 5. Start the development server
pnpm dev
```

---

## Project Structure

See [`docs/architecture/project-structure.md`](docs/architecture/project-structure.md) for the full directory layout.

---


---

# Cherry in the Haystack Marketplace - Agent Resource Development Platform

"Where Curators Build Knowledge for Subscribed Agents to Upskill"
BuidlHack 2026 | General Track + Status Network Track + NEAR Protocol Track

## The Problem

AI agents don't just get things wrong. Most of the time, they don't know what to look for. A coding agent has to ask you what "MCP" is while building one. That's data drift.

The problem deepens outside your domain: it writes a Japanese landing page using Western conversion patterns. The agent knowledge problem isn't just accuracy. It's retrieving the knowledge you didn't know you needed.

The haystack is enormous: RSS feeds, changelogs, Discord announcements, research papers, YouTube videos. The signal is buried in noise. Finding relevant, current, verified knowledge is the bottleneck.

We help you and your agent get there.

---

## What We Built

Cherry in the Haystack Marketplace is KASS (Knowledge-as-a-Service): a live, human-curated knowledge graph transformed into an agent-native marketplace with blockchain-backed provenance.

**The foundation — Cherry in the Haystack — already runs in production:**

- **Cherry in the Haystack**: an open-source, community-driven system for continuous knowledge curation  
  - **MECE-structured knowledge graph**: mutually exclusive, collectively exhaustive relationships  
  - **Automated ingestion pipeline**: RSS, Twitter, YouTube, blogs, and PDFs flow through AI-powered scoring and synthesis  
  - **20+ domain expert curators**: weekly review cycles keep knowledge current  

- **Domain-specific knowledge bases built as modular verticals:**
  - **Cherry for AI Engineers**: the first use case of a living, continuously updated knowledge base for Agent builders  
  - **Cherry for Blockchain Engineers** : coming next  
  - **More domains to follow** : expanding across technical and professional fields  

**Next layer: Marketplace**

- Connects this knowledge layer directly to agents — enabling agent-native access, usage, and value exchange
---

## How Marketplace Works

1. **Agent registers on marketplace**  
   Permissionless, no KYC. Gets an API key and wallet address.

2. **Agent syncs with catalog**  
   80+ concepts with quality scores, free to explore.

3. **Agent purchases knowledge**  
   ~20 credits per concept. Karma tier discounts apply (0%–30%).  
   Higher Karma through consistent usage unlocks better pricing.

4. **Structured response delivered through TEE**  
   Includes evidence nodes, source attribution, quality scores, and curator comments.  
   Creators control what gets revealed. Agents can query privately.  
   The raw knowledge stays protected — only the answer is exposed.

5. **On-chain provenance recorded**  
   SHA256 hash of the response is stored gaslessly.  
   Provides permanent proof of what the agent consumed, when, and from which source.

6. **query revenue flows to the creator/curator** who maintains that knowledge. Sustainable creation/curation, not volunteer burnout.

### Foundation: Cherry in the Haystack

Content flows in from everywhere: RSS, Twitter, YouTube, blogs, PDFs, research papers. An AI pipeline scores and classifies every piece into a MECE-structured knowledge graph

Then humans verify. AI Engineers gather to verify the news impact weekly and which keywords get to live or die monthly. They score quality, add context, flag stale entries, and approve what goes live. 


---

## User Flows

### For Agent Builders (Knowledge buyers)

```
Register agent → Browse catalog (free) → Purchase concept (~20 credits)
→ Receive structured knowledge (TEE possible) → Provenance on-chain → Repeat
```

**Knowledge Gap Analysis** — an agent submits its internal knowledge base and ontology. We map it against ontology in the community graph and return what matches, what's missing, and what to prioritize(like 'git diff'). A diagnostic for your agent's blind spots.

Agents receive curated, verified knowledge with source attribution and quality scores. Queries can run privately through TEE: the marketplace never sees what your agent asked or received.

**Integration paths:**
- **MCP Server** — plug-and-play integration  
- **REST API** — for custom stacks  
- **WebSocket subscriptions** — follow concepts and receive real-time updates as knowledge evolves

### For Curators (Knowledge Suppliers)


```
Curate knowledge (weekly reviews) → Knowledge enters the graph → Agents purchase → 40% rewards distributed on-chain → Withdraw gaslessly
```

- **20+ domain experts** already maintain the knowledge graph as volunteers  
- KaaS turns this effort into earnings  
- Every query touching your concepts generates on-chain rewards  
- Rewards are withdrawable gaslessly on Status Network  

Your expertise compounds: the better you curate, the more queries flow through your knowledge — and the more you earn.

---

### For Creators (Knowledge Suppliers )

```
Creator publishes knowledge → Sets visibility rules → Agent queries through TEE → Only the answer leaves the enclave → Raw material stays protected → On-chain provenance recorded on NEAR
```

- Creators control what the world sees  
- Proprietary methodologies, curated frameworks, and domain-specific reasoning remain inside the TEE  
- Agents get the answer, not the recipe  
- On-chain provenance proves delivery without exposing underlying content

---

## How It's Made (what to check for - judges! )

### Smart Contracts

**EVM — CherryCredit.sol** (Status Network)

- `deposit()` — Agent deposits credits
- `consumeCredit()` — Deducts credits with Karma-tiered discounts
- `recordProvenance()` — Stores SHA256 hash of response data, gaslessly
- `distributeReward()` — n% to curator, gaslessly

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

## Future Vision

### From Knowledge to 'Digital Twins' in TEE  
  
Creator → Deploys a digital twin inside a trusted enclave → Agents consult it → Only the output leaves the enclave → On-chain receipt proves the interaction  
  
- A creator’s digital twin runs securely inside a TEE  
- Agents access domain-specific expertise without exposing underlying knowledge  
- Methodologies, proprietary frameworks, and reasoning never leave the enclave  
- Only the consultation output is delivered, with verifiable on-chain proof  
  
Knowledge was the first product. Agentic Freelancing is next.

### Soulbound Reputation (Status Network)

Karma is the beginning. The long-term vision is a soulbound reputation system where curators earn non-transferable reputation for quality contributions. Agents that consistently deliver accurate results build verifiable track records. This extends to digital twins — on-chain representations of a curator's expertise that continue to serve agents autonomously, backed by proof of competence. The creator sets the boundaries. The twin operates within them.


---

*Cherry in the Haystack → Marketplace KaaS: Curated knowledge, agent-native access, on-chain proof.*


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
