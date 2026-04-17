# Track Requirements Mapping — Cherry KaaS

BuidlHack 2026 | Status Network Track + NEAR Protocol Track

---

## 1. Status Network Track

### Main Bounty: Best Privacy-First or Agentic App

**Requirement:** Leverage gasless + privacy stack (Karma / RLN) in at least one of these ways:

#### 1a. Privacy-Preserving Interactions ✅

> *Build applications where users can act onchain without linking their activity to a persistent identity.*

| Requirement | How We Meet It | Status |
|---|---|---|
| No wallet pre-funding (no gas correlation) | Agents register with an address, query knowledge, and record provenance — all gaslessly. No gas behavior = no identity fingerprint. | ✅ Working |
| RLN rate-limits via ZK proofs (no behavioral fingerprinting) | Agent queries flow through RLN-gated access. The network knows the query is authorized, but not which agent made it. | ⚠️ Needs RLN integration |
| On-chain actions without persistent identity link | Provenance hashes are SHA256 of response data — not of the agent's identity. Queries are recorded, identities aren't. | ✅ Working |

**What we have:**
- `CherryCredit.sol` deployed at `0x153DAcC25Ad05DcFb1f258c28eb47e48c13e682b` (Status Sepolia)
- `recordProvenance()` stores SHA256 hashes gaslessly — agent activity is provable but not linkable to a real-world identity
- `status-adapter.ts` handles all transactions without gas pre-funding

**Gap to fill:**
- Integrate RLN for ZK proof-based rate limiting on agent queries. Currently rate-limiting is off-chain. RLN would make agent query patterns private even from the network.

---

#### 1b. Agentic / Autonomous Workflows ✅ (Strongest fit)

> *Design AI agents, bots, or automated pipelines that transact onchain gaslessly. Use Karma-tiered throughput for sustainable, spam-protected access.*

| Requirement | How We Meet It | Status |
|---|---|---|
| AI agents that transact onchain gaslessly | MCP server enables Claude, GPT, LangChain, CrewAI agents to query, purchase, and subscribe to knowledge — all transactions are gasless on Status Network. | ✅ Working |
| Karma-tiered throughput for agents | Bronze/Silver/Gold/Platinum tiers with 0%/5%/15%/30% credit discounts. Higher Karma = more queries per day. | ✅ Working |
| Spam-protected access to block space | Karma as sybil-resistance — agents earn Karma through legitimate usage, preventing spam while preserving gaslessness. | ✅ Working |
| Autonomous pipeline | Agent registers → browses catalog → purchases knowledge → receives structured response → provenance recorded on-chain → curator rewarded. Fully autonomous, no human in the loop. | ✅ Working |

**What we have:**
- `mcp-server.ts` — 7 MCP tools for agent-native interaction
- `kaas-agent.entity.ts` — Karma tier tracking with discount logic
- `CherryCredit.sol` — `consumeCredit()`, `recordProvenance()`, `distributeReward()` all gasless
- 5 API channels: MCP, REST, WebSocket, LLM proxy, Web dashboard

**Strength for this track:**
This is our strongest alignment. Cherry KaaS is fundamentally an agent-to-blockchain application. The entire product is designed around autonomous agents consuming knowledge and transacting on-chain without gas.

---

#### 1c. Reputation-Gated Experiences ✅

> *Use Karma as sybil-resistant, privacy-preserving gating: unlock features, tier service access, create trust hierarchies — without KYC.*

| Requirement               | How We Meet It                                                                                                                                          | Status                                            |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Karma as gating mechanism | Agent Karma tier determines credit discounts (0%–30%) and daily query quotas. No KYC, no transferable tokens — just on-chain participation history.     | ✅ Working                                         |
| Tiered service access     | Bronze agents pay full price. Gold agents get 15% off. Platinum gets 30% off. Service quality scales with reputation.                                   | ✅ Working                                         |
| Sybil-resistant           | Karma is soulbound — earned through staking SNT, bridging, liquidity provision. Cannot be bought or transferred. Each agent's Karma is uniquely earned. | ⚠️ Currently mock; needs real Karma contract read |
| No KYC required           | Agent identity is just an address + Karma tier. No personal information needed to access premium features.                                              | ✅ Working                                         |

**What we have:**
- `consumeCredits()` in service layer applies Karma-based discounts
- Web dashboard displays Karma tier and balance
- Agent registration is permissionless — no KYC, no verification beyond address

**Gap to fill:**
- Read real Karma contract on Status Network Hoodi Testnet (currently using mock balance). This is also a Builder Quest requirement.

---

### Builder Quest Checklist

| #   | Task                                                             | How We Meet It                                                                                                                                                                                             | Status                              |
| --- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| 1   | Deploy ≥1 smart contract gaslessly on Hoodi Testnet              | `CherryCredit.sol` deployed on Status Sepolia. Need to redeploy on Hoodi Testnet.                                                                                                                          | ⚠️ Needs Hoodi deployment           |
| 2   | Execute 5+ gasless transactions demonstrating core functionality | `deposit()` → `consumeCredit()` → `recordProvenance()` → `distributeReward()` = 4 tx types. Can demonstrate: (1) agent deposit, (2-3) two concept purchases, (4) provenance recording, (5) curator reward. | ✅ Ready                             |
| 3   | Read user's Karma tier on-chain and display/use in app           | Currently mock. Need to call Status Network Karma contract to read real tier.                                                                                                                              | ⚠️ Needs Karma contract integration |
| 4   | 2-minute demo video (English preferred, Korean OK)               | Not yet created.                                                                                                                                                                                           | ❌ TODO                              |
| 5   | Open-source on GitHub with README                                | Code is on GitHub. README exists in `docs/KaaS/pitch.md`. Need dedicated README.                                                                                                                           | ⚠️ Needs README                     |
| 6   | Live functional demo accessible to judges                        | API running, web dashboard available. MCP server functional.                                                                                                                                               | ✅ Ready                             |

### Summary for Status Network

| Dimension           | Fit   | Notes                                                                 |
| ------------------- | ----- | --------------------------------------------------------------------- |
| Agentic workflows   | ⭐⭐⭐⭐⭐ | Core product is agent-native. Strongest alignment.                    |
| Karma-tiered access | ⭐⭐⭐⭐  | Already built into credit system. Needs real Karma contract read.     |
| Gasless provenance  | ⭐⭐⭐⭐⭐ | Every query generates an on-chain receipt. Gasless by design.         |
| Privacy (RLN)       | ⭐⭐⭐   | Provenance is pseudonymous. RLN integration would push this to ⭐⭐⭐⭐⭐. |
| Builder Quest       | ⭐⭐⭐⭐  | 4/6 tasks ready. Need Hoodi deploy, Karma read, demo video, README.   |

**Key message for judges:** Cherry KaaS is the content layer for agent commerce on Status Network. Agents query human-curated knowledge, every query is recorded gaslessly as an on-chain provenance receipt, Karma tiers govern access and pricing, and curators earn 40% rewards — all without a single gas fee.

---

## 2. NEAR Protocol Track

### Judging Criteria Breakdown

#### Innovation (30%) — Novel use of TEE-based privacy

| Aspect                                         | How We Meet It                                                                                                                                                                           | Status                        |
| ---------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| TEE for knowledge queries                      | Privacy Mode routes agent queries through NEAR AI Cloud TEE (Qwen3-30B on Intel TDX). Agent purchase intent is encrypted — even our server doesn't see what the agent is asking.         | ✅ Working                     |
| Private AI chat with curated knowledge         | Agent asks a question → TEE processes it against curated knowledge graph → response generated inside TEE → no one (not us, not NEAR, not the infrastructure) sees the query or response. | ✅ Working                     |
| Verifiable computation                         | NEAR AI provides attestation proving the exact model (Qwen3-30B) that processed the data. Agents can verify their knowledge wasn't tampered with.                                        | ⚠️ Attestation display needed |
| Novel combination: TEE + blockchain provenance | Knowledge is processed privately (TEE) but its provenance is recorded publicly (NEAR smart contract). Private processing + public proof — the best of both worlds.                       | ✅ Working                     |

**What we have:**
- `kaas-llm.controller.ts` — LLM proxy with privacy toggle
- `near-adapter.ts` — NEAR contract integration for provenance recording
- NEAR contract at `tomatojams.testnet` with same credit/provenance/reward logic
- OpenAI-compatible endpoint: `https://cloud-api.near.ai/v1/chat/completions`

**Innovation angle:** We're not just running an LLM in a TEE. We're running a knowledge marketplace where the entire query-response lifecycle is private (TEE) but the economic transaction is verifiable (on-chain). This combination doesn't exist elsewhere.

---

#### Impact (25%) — Solving a real problem that required private AI

| Aspect | How We Meet It |
|---|---|
| The problem is real | 61% of enterprises report AI accuracy issues. Agents confidently recommend deprecated tools. The cost of wrong knowledge cascades through agent-to-agent chains. |
| Privacy is necessary, not optional | Agents often query sensitive topics: proprietary architectures, business strategies, security vulnerabilities. Without TEE, the knowledge provider sees every query. With TEE, queries are invisible even to us. |
| Measurable impact | Knowledge Gap Analysis diagnoses agent blind spots. 80+ concepts, 600+ evidence nodes already curated. Agents can fill gaps without exposing what they don't know. |
| Real users | Cherry in the Haystack already serves 20+ curators and covers AI Engineering domain. KaaS extends this to any agent. |

**Impact narrative:** Enterprise agents querying "what's our competitor's weakness?" or "what's the latest security vulnerability?" can't afford to expose their queries to a central server. TEE makes the query invisible while still delivering curated, verified answers. This isn't a nice-to-have — it's a requirement for enterprise agent adoption.

---

#### Technical Excellence (20%) — Clean code, proper use of attestation

| Aspect | How We Meet It | Status |
|---|---|---|
| Clean code architecture | Monorepo: Next.js frontend, NestJS backend, Solidity + NEAR contracts, MCP server, Python AI services. Each layer is independently deployable. | ✅ Working |
| Proper TEE integration | Uses NEAR AI Cloud endpoint with OpenAI SDK compatibility. No custom cryptography — leverage platform guarantees. | ✅ Working |
| Attestation usage | TEE provides hardware attestation for model execution. Need to surface this in the demo. | ⚠️ Show attestation proof in UI |
| Multi-chain adapter pattern | `chain-adapter/interface.ts` with Status + NEAR + Mock implementations. Clean abstraction for multi-chain support. | ✅ Working |
| NEAR contract | `cherry_credit.ts` — near-sdk-js with credit, provenance, and reward functions. Mirrors EVM contract logic. | ✅ Working |

**Gap to fill:**
- Display TEE attestation in the demo (show the cryptographic proof that Qwen3-30B actually processed the query)
- Surface attestation metadata in the API response

---

#### Privacy Design (15%) — Thoughtful approach to user data protection

| Aspect | How We Meet It |
|---|---|
| Query privacy | Agent queries through TEE are invisible to the server. Even if our database is compromised, query contents are never stored in plaintext. |
| Provenance without exposure | On-chain provenance records SHA256 hashes — proof that a transaction happened, but not what was queried. Public verifiability + private content. |
| No data retention of sensitive queries | TEE processes and returns results without persisting the input. The hash proves it happened; the content stays private. |
| Layered privacy | NEAR contract handles economics (public). TEE handles knowledge queries (private). Agent identity is just an address (pseudonymous). Three layers of protection. |
| Opt-in privacy | Privacy Mode is a toggle. Agents can choose transparent mode (faster, logged) or private mode (TEE-protected, no logging). |

---

#### Presentation (10%) — Clear demo and explanation

| Aspect | Plan |
|---|---|
| Demo flow | (1) Agent asks sensitive question → (2) Privacy Mode routes to TEE → (3) Curated answer returns with evidence nodes → (4) On-chain provenance recorded on NEAR → (5) TEE attestation displayed as proof of private execution |
| "Wow" moment | Show two queries side-by-side: one transparent (query visible in logs), one private (query invisible, only provenance hash remains). The contrast makes the value obvious. |
| Technical explanation | Explain the TEE privacy flow: "Your query enters the TEE. Inside, Qwen3-30B processes it against our curated knowledge graph. The answer comes out. No one — not us, not NEAR, not Intel — saw what went in." |

---

### Summary for NEAR

| Dimension | Weight | Fit | Notes |
|---|---|---|---|
| Innovation | 30% | ⭐⭐⭐⭐⭐ | TEE + on-chain provenance combination is novel. No one else does private knowledge queries with public proof. |
| Impact | 25% | ⭐⭐⭐⭐ | Enterprise agents need private knowledge queries. 61% accuracy issue makes this urgent. |
| Technical Excellence | 20% | ⭐⭐⭐⭐ | Clean multi-chain architecture. Need to surface attestation in demo. |
| Privacy Design | 15% | ⭐⭐⭐⭐⭐ | Layered privacy: TEE for queries, on-chain hashes for proof, pseudonymous identity. Opt-in toggle. |
| Presentation | 10% | ⭐⭐⭐⭐ | Side-by-side demo (transparent vs private) is compelling. Needs video. |

**Key message for judges:** Cherry KaaS is a knowledge marketplace where AI agents can privately query human-curated knowledge through TEE, with every transaction verifiable on NEAR Protocol. Private queries, public proof, trusted answers.

---

## 3. Cross-Track Synergies

Both tracks reinforce each other. Here's where they overlap:

| Feature      | Status Network                           | NEAR Protocol                  | Combined Value                             |
| ------------ | ---------------------------------------- | ------------------------------ | ------------------------------------------ |
| Provenance   | Gasless on-chain receipts (Karma-tiered) | TEE-attested private execution | Public proof of private computation        |
| Agent access | MCP + REST + WebSocket                   | TEE-routed LLM proxy           | Agents get knowledge publicly or privately |
| Economics    | 40% curator rewards, gasless             | Same reward logic on NEAR      | Multi-chain curator economy                |
| Reputation   | Karma tiers (soulbound)                  | —                              | Sybil-resistant agent identity             |
| Privacy      | RLN rate limiting (planned)              | TEE query encryption           | Double privacy: who asked + what was asked |

**The combined pitch:** Agents query knowledge privately (NEAR TEE), transact gaslessly with reputation-tiered access (Status Karma), and every interaction is recorded as a verifiable on-chain receipt (both chains). Private queries, gasless transactions, public proof.

---

## 4. Future Roadmap / Vision

### Status Network — Soulbound Reputation & Privacy-Preserving Knowledge

**Soulbound Reputation**

Karma is just the beginning. The long-term vision is a soulbound reputation system that proves this knowledge base — and the agents built on top of it — actually gets things done. Curators earn non-transferable reputation for quality contributions. Agents that consistently deliver accurate results build verifiable track records. In the long term, this extends to digital twins of the creator — an on-chain representation of a curator's expertise that continues to serve agents, backed by proof of competence rather than self-reported credentials.

For the user (agent builder): reputation is a trust signal. You know the knowledge you're buying comes from someone whose curation history is on-chain and verifiable. No fake reviews, no bought authority — just earned, soulbound proof.

**Privacy-Preserving Knowledge Delivery**

Curators choose what to reveal. Their full prompts, proprietary knowledge structures, and custom tools remain private — KaaS delivers *extracted knowledge* from the knowledge base, not the raw source. This matters for copyright and know-how protection. A tax attorney's curated tax law guide is valuable precisely because the attorney's reasoning methodology is not exposed — only the verified output is delivered.

For the consumer: quality is guaranteed by the chain. Every piece of knowledge has a provenance receipt. You don't need to see *how* the curator made it to trust *that* it's verified.

### NEAR Protocol — Privacy-Preserving Knowledge with TEE

**Creator Privacy via TEE**

The same privacy principle, amplified by TEE. Curators' prompts, knowledge structures, and tools are processed inside a Trusted Execution Environment. Even the infrastructure provider cannot see what the creator built. KaaS delivers the extracted knowledge — the final, verified output — without exposing the creator's proprietary methodology.

This is critical for copyright and know-how protection. A creator's competitive advantage is their curation process. TEE ensures that process stays private while the output reaches agents who need it. The knowledge is useful; the know-how remains the creator's.

For the consumer: quality is guaranteed by the chain + TEE attestation. You get a cryptographic proof that the knowledge was generated by a specific model, inside a TEE, at a specific time. No trust required — just verification.

### Combined Vision

| Aspect | Today | Future |
|---|---|---|
| Creator privacy | Opt-in toggle, server-side | TEE-enforced, cryptographically guaranteed |
| Knowledge delivery | Structured response with sources | Extracted knowledge only — source methodology stays private |
| Reputation | Karma tiers (participation-based) | Soulbound reputation (competence-proven, non-transferable) |
| Agent trust | Provenance receipt per query | Full agent track record — "this agent's knowledge has been correct X times" |
| Digital twins | Not yet | On-chain representation of creator expertise, serving agents autonomously |

**One-liner:** Curators' know-how stays private. Their output is verifiable. Agents consume trusted knowledge without ever seeing the recipe — and the chain proves it.

---

## 5. Action Items Before Submission

### Must-do (blocks submission)

- [ ] Deploy `CherryCredit.sol` on Status Network Hoodi Testnet (not just Sepolia)
- [ ] Read real Karma contract on-chain (replace mock balance)
- [ ] Execute and document 5+ gasless transactions on Hoodi
- [ ] Create README.md in English for GitHub repo
- [ ] Record 2-minute demo video
- [ ] Surface TEE attestation in demo UI for NEAR track

### Should-do (strengthens pitch)

- [ ] Side-by-side demo: transparent query vs TEE private query
- [ ] Show Karma tier impact in demo (Bronze vs Platinum pricing)
- [ ] Display on-chain provenance receipt in real-time during demo
- [ ] Show curator reward flow end-to-end
- [ ] Knowledge Gap Analysis demo for "wow" factor

### Nice-to-have (differentiation)

- [ ] RLN integration for Status Network privacy story
- [ ] Attestation verification endpoint in API
- [ ] Multi-chain provenance: same query, receipts on both chains
