---
title: "Product Brief: Cherry KaaS — Knowledge-as-a-Service for AI Agents"
status: "complete"
created: "2026-04-14"
updated: "2026-04-14"
inputs:
  - "_bmad-output/brainstorming/brainstorming-session-001.md"
  - "_bmad-output/planning-artifacts/research/market-agent-knowledge-trading-research.md"
  - "_bmad-output/planning-artifacts/research/technical-buidlhack2026-stack-research.md"
  - "docs/PRD/executive-summary.md"
  - "docs/PRD/product-scope.md"
  - "docs/Buidlhack 340f199edf7c80a48949c6ce31b1f4eb.md"
---

# Product Brief: Cherry KaaS

**The Verified Knowledge Layer for the AI Agent Economy**

## Executive Summary

Imagine an AI agent recommending a $200K technology migration — confidently citing a framework that was deprecated last month. This happens daily. 61% of enterprises report AI accuracy issues, and hallucinating agents use 34% more confident language than when stating facts. As agents begin transacting billions in commerce ($50B+ projected by 2030), the consequences of unverified knowledge scale with them.

**Cherry KaaS** is a blockchain-powered Knowledge-as-a-Service platform that lets AI agents discover, query, and subscribe to human-curated, domain-specialized knowledge. Think of it as the credit rating agency for AI knowledge — just as Moody's and S&P rate financial instruments so markets can function, Cherry verifies and structures knowledge so the agent economy can function reliably.

Built on Cherry-in-the-Haystack's existing knowledge graph — 80+ concepts, 600+ evidence nodes, MECE-structured relationships maintained by 20+ expert curators across 50+ sources — Cherry KaaS opens this verified knowledge to any AI agent through the MCP protocol and standard APIs, with blockchain-backed provenance and transparent payments.

The timing is now: MCP has hit 97M downloads (donated to Linux Foundation), Google A2A has 150+ partners, and agent commerce protocols are crystallizing in 2026. Payment rails are commoditizing (Visa Trusted Agent Protocol, Coinbase x402). The value is shifting to **what agents consume** — and no one is providing verified, curated knowledge at the protocol level.

## The Problem

AI agents today operate on unverified knowledge. They scrape the web, call general-purpose LLMs, and hope for the best. When an agent makes a consequential decision — recommending a technology stack, evaluating a business strategy, synthesizing research — there's no way to guarantee the quality or provenance of its inputs. KPMG (2026) identifies knowledge engineering as "the key to AI agent value," yet no standard exists for agents to access verified knowledge.

Most agent builders today rely on static RAG pipelines with stale vector stores — knowledge that was current when indexed but degrades silently. Existing blockchain-AI projects address infrastructure (ASI Alliance — now fractured over governance disputes) or agent-to-agent task execution (Olas, 10M+ transactions). None provide **structured, human-verified, continuously-updated knowledge** that agents can consume on demand.

The result: agents building on sand, cascading hallucinations in agent-to-agent chains, enterprises unable to trust agent outputs, and no accountability when knowledge is wrong.

## The Solution

Cherry KaaS provides a complete agent knowledge consumption flow:

- **Discover** — Agents register, set domain interests, and browse a free knowledge catalog with concept previews, quality scores, and freshness indicators
- **Consume** — Two modes: **query** (natural language question + depth control: summary/concept/evidence + budget cap) or **subscription** (real-time WebSocket/Webhook push when knowledge updates — managed RAG with human curation, replacing stale vector stores)
- **Pay** — Credit system: 1 credit ~ $0.01, basic query ~ 5 credits, deep query ~ 20 credits, subscription ~ 100 credits/month. Prepaid with on-chain provenance recording
- **Reward** — Curators earn 40% of transaction revenue, settled server-side with on-chain withdrawal. Quality-gated: only Knowledge Team-reviewed content generates rewards

**Hybrid architecture by design:** Centralized transaction processing (sub-100ms latency, zero gas cost per query) with blockchain transparency only where it adds trust — provenance hashes, payment records, curator withdrawals. This is a deliberate architectural advantage: fully on-chain competitors pay ~$0.03/tx on BSC or suffer DeFi-grade latency. Cherry KaaS delivers API-grade speed with blockchain-grade auditability.

**MCP as distribution channel:** Cherry KaaS as an MCP server means every MCP-compatible agent (Claude, GPT, Vercel AI SDK, LangChain) can discover and consume verified knowledge with zero custom integration. This isn't just a demo — it's the primary go-to-market: listed in MCP directories, one import away from 97M+ potential agent instances.

## What Makes This Different

| | Cherry KaaS | RAG Pipelines | Blockchain-AI (Bittensor, Olas) |
|---|---|---|---|
| **Knowledge quality** | Human-curated, MECE-structured, source-attributed | Stale at indexing time, no curation | Raw data or unverified model outputs |
| **Freshness** | Subscription push on every update | Re-index and hope | Varies by subnet/service |
| **Agent-native** | MCP/API-first, query + subscription | Custom per-project | Human dashboards retrofitted |
| **Provenance** | On-chain hash per evidence item | None | On-chain but complex |
| **Cost to query** | ~$0.05-0.20/query, $0 gas | Embedding + LLM costs | Gas + token staking |

**Why not just use Perplexity/web search?** Perplexity returns search results an agent must evaluate. Cherry returns pre-evaluated, structured knowledge with provenance — the difference between handing someone a library card and handing them a verified expert briefing.

## Who This Serves

**Primary: AI Agent Builders** — developers deploying agents that need reliable domain knowledge. They want API-key simplicity, predictable pricing, and verifiable quality. Pain point: every RAG pipeline they build is a bespoke maintenance burden.

**Secondary: Knowledge Curators** — Cherry's 20+ domain experts who earn revenue from agent consumption. At projected volume (10K queries/month), top curators earn ~$200/month — growing with agent adoption.

**Tertiary: Enterprises** — organizations deploying agents internally who need audit trails and provenance for compliance. EU AI Act Article 13 transparency obligations make provenance a regulatory requirement, not a nice-to-have.

## Hackathon Strategy (BuidlHack2026)

**Primary track: Status Network** — gasless agent transactions + Karma curator reputation is the most natural fit. Zero gas cost removes agent friction entirely, and Karma maps directly to curator quality tiers. This track gets full polish.

**Secondary tracks (BNB Chain, NEAR AI)** via Chain Adapter pattern — single codebase, environment variable swap. Functional demos that meet submission requirements, maximizing total prize exposure.

| Track | Chain | Cherry KaaS Story | Priority | Prize Pool |
|---|---|---|---|---|
| **Status Network** | Gasless L2 | Agentic workflows: gasless knowledge queries + Karma curator reputation | **Primary** | $5,000 |
| **BNB Chain** | opBNB L2 | Consumer AI: agents trading verified knowledge on BNB ecosystem | Secondary | $5,000 |
| **NEAR AI** | TEE inference | Private AI: verifiable knowledge consumption with cryptographic privacy | Secondary | $5,000 |
| **General** | — | Best overall project | — | $6,000 |

**Demo flow:** Live MCP demo — Claude agent queries Cherry KaaS for "best embedding model for Korean text," receives curated, source-attributed answer with on-chain provenance hash, all gasless on Status Network.

## Success Criteria

**Hackathon (April 16):**
- Working end-to-end demo: register → browse → query → subscribe → pay → curator reward
- MCP server live with Claude consuming Cherry knowledge
- Deployed on 3 testnets with verifiable on-chain transactions
- Compelling 3-minute demo video per track

**Post-Hackathon (3-6 months):**
- 50 registered agent builders (recruited via MCP directory listing, agent framework integrations, developer community outreach)
- A/B comparison: hallucination rate of agents using Cherry vs baseline RAG (target: 40%+ reduction)
- $500+ monthly curator payouts demonstrating unit economics work
- Integration with LangChain and CrewAI tool registries

## Scope

**MVP (Hackathon):**
- Agent registry & catalog API (free browsing)
- Query mode (pay-per-query, depth control)
- Subscription mode (WebSocket real-time push)
- Credit system (prepaid, on-chain record)
- Curator reward settlement (40% revenue share)
- MCP server (query_knowledge, get_concept, search_concepts)
- Chain Adapter for multi-track deployment

**Not in MVP:**
- Knowledge token marketplace / DEX trading
- Knowledge futures or prediction markets
- Agent DID authentication
- Curate-to-Earn tokenomics
- Guild/DAO governance
- Data flywheel (query analytics → curator demand signals)

## Vision & Growth Flywheel

**The flywheel that makes this self-reinforcing:**

More agent queries → richer consumption analytics → curators see demand signals and earn more → curators produce higher-demand content → agents get better answers → more agents join

**Phase 2 (post-hackathon):** Tiered pricing, agent reputation, DID authentication, query-to-curation demand signals, multi-domain expansion (crypto/DeFi analysis, biotech, regulatory tracking — domains where agents need curated knowledge and willingness-to-pay is 10x higher)

**Phase 3 (ecosystem):** Curate-to-Earn tokenomics, domain-specialized guilds, knowledge futures markets, agent-to-agent reselling with automatic curator royalties. Cherry KaaS as a Bittensor subnet, an Olas knowledge service, embedded in every major agent framework.

Not competing with infrastructure — sitting on top of it as the content layer that makes agents actually useful.
