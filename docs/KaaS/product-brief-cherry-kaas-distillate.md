---
title: "Product Brief Distillate: Cherry KaaS"
type: llm-distillate
source: "product-brief-cherry-kaas.md"
created: "2026-04-14"
purpose: "Token-efficient context for downstream PRD creation — rejected ideas, technical constraints, competitive intelligence, scope signals, and open questions"
---

# Cherry KaaS — Detail Pack for PRD

## Rejected Ideas (do not re-propose)

- **#1 Knowledge Token Marketplace (DEX-style)** — Too complex for MVP; requires token economics design, liquidity bootstrapping, AMM mechanics. Deferred to Phase 3.
- **#2 Knowledge Futures Trading** — Prediction market for concept value. Interesting but regulatory risk + complexity. Phase 3.
- **#3 Knowledge Dividend Model** — Automatic royalty distribution to curators. Replaced by simpler 40% revenue share in MVP.
- **#7 Agent-to-Agent Knowledge Reselling** — Secondary market with original curator royalties via smart contract. Requires mature ecosystem. Phase 3.
- **#13 Agent DID Authentication** — Decentralized identity + on-chain API key. Valuable but not needed for hackathon demo. Phase 2.
- **#15 Curation Quality Staking** — Curators stake tokens on knowledge quality, slashing for low quality. Needs token economy. Phase 2.
- **#23 Full SLA Smart Contract** — Replaced by #28 SLA Lite (server-side monitoring + auto-credit). Full on-chain SLA is overengineered for MVP.
- **#24-26 DeFi Liquidity Pool (full version)** — AMM-based concept pools, evidence value weighting, curator dashboard. All deferred to Phase 3.
- **3-track equal effort** — Skeptic review flagged risk of 3 half-working demos. Decision: Status Network primary (full polish), BNB/NEAR secondary (functional but not demo-polished).
- **Fully on-chain transaction processing** — Rejected for MVP. Adds latency ($0.03/tx on BSC, variable on others) without proportional user value. Hybrid model: centralized processing + on-chain provenance/withdrawal only.

## Requirements Hints (captured during discovery)

### Pricing & Economics
- 1 credit ~ $0.01 USD
- Basic query (summary depth) ~ 5 credits ($0.05)
- Deep query (full evidence) ~ 20 credits ($0.20)
- Subscription (per concept/month) ~ 100 credits ($1.00)
- Curator revenue share: 40% of transaction revenue
- Credit purchase: fiat or token (prepaid), on-chain record of consumption
- Dynamic pricing mentioned in brainstorm (#21): concept activity-based pricing, early-bird discounts for new concepts — Phase 2
- SLA Lite (#28): server monitors update frequency, auto-credits if below threshold

### API Design (from brainstorming)
- `POST /agents/register` — profile + interest domains → recommended subscriptions
- `GET /catalog` — free concept list with previews, stats, quality scores
- `POST /query` — natural language question + depth (summary/concept/evidence) + budget cap
- `POST /subscribe` — concept/category/curator unit + WebSocket/Webhook delivery
- Event format (#22): structured JSON with type, concept_id, evidence_summary, provenance_hash, freshness score
- Subscription units (#20): by concept, category, relationship type, or curator

### Authentication & Security
- MVP: API Key + JWT + wallet signature (EIP-712)
- Phase 2: Agent DID (decentralized identity)
- Rate limiting per API key tier

### Knowledge Quality
- Quality score needs methodology (reviewer flagged this as gap)
- Suggested formula: source_count x recency x curator_reputation x peer_review_status
- Knowledge Team weekly review (Wednesday) is the quality gate — only reviewed content generates curator rewards
- Monthly concept promotion cycle (2nd Saturday) for Basics/Advanced progression

## Technical Constraints & Decisions

### Architecture
- **Modular Monolith** (Node.js/Express/TypeScript) — not microservices for hackathon speed
- **Chain Adapter pattern** — interface with swap via env var (CHAIN_ADAPTER=status|bnb|near)
- **Event-driven** — in-memory EventEmitter (MVP), upgradable to Redis Pub/Sub
- **Database** — SQLite for MVP, PostgreSQL post-hackathon
- **WebSocket** — ws library for subscription push
- **Frontend** — Next.js + wagmi/viem for wallet integration

### Smart Contracts
- **CherryCredit.sol (ERC-20)** shared across BNB + Status
  - Functions: deposit(), consumeCredit(), distributeReward(), recordProvenance()
  - Events: CreditConsumed, RewardDistributed, ProvenanceRecorded
  - Status Network addition: Karma tier discount (30%/15%/5%/0% by tier)
- **NEAR**: near-sdk-js, separate contract pattern (NEAR is not EVM)

### Chain-Specific Details
- **Status Network (PRIMARY)**
  - Chain ID: 1660990954 (0x6300b5ea)
  - RPC: https://public.sepolia.rpc.status.network
  - Explorer: https://sepoliascan.status.network
  - Karma contract: 0x7ec5Dc75D09fAbcD55e76077AFa5d4b77D112fde
  - KarmaTiers: 0xc7fCD786a161f42bDaF66E18a67C767C23cFd30C
  - CRITICAL: Must use linea_estimateGas (not eth_gasPrice); from field required; baseFeePerGas===0x0 confirms gasless
  - Requirements: 5+ gasless txs, Karma tier read/display, 2-min demo video, GitHub + README, live demo
- **BNB Chain (opBNB)**
  - Chain ID: 5611 (testnet)
  - RPC: https://opbnb-testnet-rpc.bnbchain.org/
  - 10K TPS, <$0.001/tx, 1s blocks
  - Requirements: 2+ on-chain txs, demo video, #ConsumerAIonBNB tweet, public GitHub
- **NEAR AI**
  - Gateway: https://cloud-api.near.ai
  - OpenAI SDK drop-in (base_url=cloud-api.near.ai/v1)
  - Models: qwen35-122b, qwen3-30b, gpt-oss-120b
  - TEE attestation for verifiable inference
  - Judging: Innovation 30%, Impact 25%, Technical Excellence 20%, Privacy Design 15%

### MCP Server
- Package: @modelcontextprotocol/sdk
- Tools: query_knowledge, get_concept, search_concepts
- Resources: concept://{id}, evidence://{id}
- Prompts: explain_concept
- 50+ official MCP servers exist in ecosystem as reference

### Build Plan (4 days)
- Day 1: Smart contracts + chain adapters
- Day 2: API server core (/catalog, /query, /subscribe)
- Day 3: MCP server + demo agent + NEAR AI integration
- Day 4: Frontend dashboard + demo videos (2-4 min) + pitch deck

## Competitive Intelligence

### Direct Competitors (Blockchain-AI)
- **ASI Alliance (FET)** — Merged Fetch.ai + SingularityNET + Ocean Protocol, $7.5B mcap. Now fractured over governance disputes. Infrastructure focus, not curated knowledge.
- **Bittensor (TAO)** — $3.13B mcap, 128 subnets, ~$100M annualized revenue. But revenue vs subsidy imbalance (top subnet $2.4M revenue vs $52M subsidy). Raw compute/data, not curated knowledge.
- **Olas (Autonolas)** — 10M+ agent-to-agent transactions, $13.8M raised. Agent task execution marketplace, not knowledge. Cherry could integrate as an Olas knowledge service.
- **Masa** — 1.4M users, raw data marketplace. No curation layer.
- **OriginTrail (TRAC)** — Decentralized knowledge graph for supply chain. Enterprise focus, not agent-native.
- **ChainGPT** — AI tools for blockchain analytics. Tooling, not knowledge marketplace.

### Substitutes (non-blockchain)
- **Perplexity API** — Search results an agent must evaluate. Cherry provides pre-evaluated, structured knowledge. Different value prop.
- **Custom RAG pipelines** — Bespoke per-project, stale at indexing time, maintenance burden. Cherry is managed RAG with human curation.
- **Wolfram Alpha API** — Structured knowledge but math/science only, no LLM/AI domain, no blockchain provenance.

### Market Data Points
- AI agent market: $9.1-15B (2026) → $139-221B (2034), CAGR 40.5%
- Blockchain-AI integration: $681M (2025) → $4.3B (2034), CAGR 22.93%
- Agent commerce: $50B+ by 2030; 20-30% online transactions will involve AI agent mediation
- Gartner: 40% enterprise apps will embed agents by end of 2026 (up from <5% in 2025)
- BNB Chain: 40K+ on-chain agents with ERC-8004 identity standard
- 75% drop in weekly crypto code commits vs 2025 — AI absorbing blockchain talent. Cherry at intersection attracts both.
- 72% enterprises plan to deploy agents from "trusted technology providers"; top criteria: security/audit (75%)
- KPMG 2026: "knowledge engineering is the key to AI agent value"

## User Scenarios (richer than exec summary)

### Scenario 1: Agent Builder (Primary)
Dev building a coding assistant that recommends tech stacks. Currently uses RAG over blog posts — recommendations go stale within weeks. Integrates Cherry KaaS via MCP (one import). Agent now returns curated, source-attributed recommendations with freshness scores. Subscribes to "frameworks" category for real-time updates. Pays ~$10/month in credits.

### Scenario 2: Knowledge Curator (Secondary)
AI engineering expert on Cherry's Knowledge Team. Reviews 20 evidence items/week (Wednesday cycle). With KaaS, their curated content generates agent queries. At 10K queries/month platform-wide, top curator earns ~$200/month. Demand signals show which concepts agents query most — curator prioritizes those for deeper coverage.

### Scenario 3: Enterprise Compliance (Tertiary)
Fintech deploying internal agents for regulatory analysis. EU AI Act Article 13 requires documentation of knowledge sources. Cherry KaaS provides on-chain provenance hash per evidence item — auditable proof of what knowledge the agent consumed and when. Subscription mode ensures agents always use current regulatory interpretations.

## Hackathon Submission Checklist

### General Track (all tracks)
- [ ] Project description (via Ludium portal)
- [ ] Demo link (live URL or video, 3 min max)
- [ ] Presentation deck

### Status Network (PRIMARY)
- [ ] Deploy smart contract gaslessly on Hoodi Testnet
- [ ] Execute 5+ gasless transactions (core app functionality)
- [ ] Read user's Karma tier on-chain and display/use in app
- [ ] 2-minute demo video (English preferred, Korean OK)
- [ ] Open-source GitHub + README
- [ ] Live functional demo accessible to judges

### BNB Chain
- [ ] Deploy on opBNB/BSC testnet
- [ ] 2+ successful on-chain transactions within hackathon timeframe
- [ ] 2-4 minute demo video showing end-to-end user flow
- [ ] Public GitHub with README + setup steps
- [ ] Tweet with demo video tagging @BNBChain + #ConsumerAIonBNB

### NEAR AI
- [ ] Working demo using NEAR AI Cloud (TEE inference)
- [ ] Attestation verification integration
- [ ] Demo video showing privacy-preserving knowledge consumption

### Deadline
- **April 16, 23:59 KST** — all submissions
- **April 17** — judging, finalist selection
- **April 18, 13:00 KST** — Final Pitch Day (onsite livestream)

## Open Questions

- **Curator onboarding for KaaS**: Do existing Knowledge Team members automatically become KaaS curators, or is there an opt-in/new agreement needed?
- **Knowledge domain expansion timing**: When to move beyond AI/LLM domain? Crypto/DeFi and biotech identified as high-value verticals with 10x willingness-to-pay.
- **Data flywheel implementation**: Query analytics → curator demand signals pipeline — how complex should this be in Phase 2? Simple dashboard vs. algorithmic bounty board?
- **Token design**: If/when to introduce a native token vs. continuing with credit system. Token adds complexity + regulatory risk but enables Curate-to-Earn and DeFi integrations.
- **Partnership priority**: MCP directory listing vs. LangChain/CrewAI integration vs. Olas service registration — which first for maximum agent reach?
- **Switching cost strategy**: Beyond content moat, what agent-specific features accumulate value over time? (personalized indices, query history, custom domain subscriptions)
