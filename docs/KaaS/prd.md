---
stepsCompleted: [1, 2, 2b, 2c, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
classification:
  projectType: api_backend
  projectTypeSecondary: blockchain_web3
  domain: developer_platform_api_marketplace
  complexity: high
  projectContext: brownfield
inputDocuments:
  - '_bmad-output/planning-artifacts/product-brief-cherry-kaas.md'
  - '_bmad-output/planning-artifacts/product-brief-cherry-kaas-distillate.md'
  - '_bmad-output/planning-artifacts/research/market-agent-knowledge-trading-research.md'
  - '_bmad-output/planning-artifacts/research/technical-buidlhack2026-stack-research.md'
  - '_bmad-output/brainstorming/brainstorming-session-001.md'
  - 'docs/PRD/index.md'
  - 'docs/PRD/functional-requirements.md'
  - 'docs/PRD/executive-summary.md'
workflowType: 'prd'
documentCounts:
  briefs: 2
  research: 2
  brainstorming: 1
  projectDocs: 3
---

# Product Requirements Document - cherry-in-the-haystack

**Author:** Jihan
**Date:** 2026-04-14

## Executive Summary

Cherry KaaS (Knowledge-as-a-Service) is a blockchain-powered API platform that enables AI agents to discover, query, and subscribe to human-curated, domain-specialized knowledge. Built as an extension of the existing Cherry-in-the-Haystack knowledge graph — 80+ concepts, 600+ evidence nodes, MECE-structured relationships maintained by 20+ expert curators — Cherry KaaS opens this verified knowledge to any AI agent through MCP protocol and REST APIs.

The core problem: AI agents operate on unverified knowledge. They scrape the web, call general-purpose LLMs, and produce recommendations with no provenance trail. 61% of enterprises report AI accuracy issues, and cascading hallucinations in agent-to-agent chains amplify errors at scale. As agent commerce grows toward $50B+ by 2030, the cost of unverified knowledge scales with it.

Cherry KaaS solves this by providing a complete agent knowledge consumption flow: agents register, browse a free catalog, then consume knowledge via pay-per-query or real-time subscription — with every consumption event recorded as an on-chain provenance hash. This creates a verifiable "knowledge receipt" — proof of what an AI consumed, when, and from which curated source.

The hybrid architecture is a deliberate design choice: centralized transaction processing delivers sub-100ms API latency with zero gas cost per query, while blockchain records only where trust matters — provenance hashes, payment records, and curator reward withdrawals. MCP-native distribution means every compatible agent framework (Claude, GPT, LangChain, CrewAI) can integrate with zero custom code.

Target audience: AI agent builders who need reliable domain knowledge without building bespoke RAG pipelines, knowledge curators who earn revenue from agent consumption (40% revenue share), and enterprises requiring auditable AI knowledge provenance for compliance (EU AI Act Article 13).

Built for BuidlHack2026 hackathon with multi-track submission: Status Network (primary — gasless agent transactions + Karma curator reputation), BNB Chain and NEAR AI (secondary — via Chain Adapter pattern). Deadline: April 16, 2026.

### What Makes This Special

**"AI knowledge receipts on blockchain"** — Every time an agent queries Cherry KaaS, the answer and its provenance hash appear on-screen in real-time, permanently recorded on-chain. No other platform provides verifiable proof of what knowledge an AI agent consumed and when.

Three reinforcing differentiators:

1. **MCP-native distribution** — Listed in MCP directories, Cherry KaaS is one import away from 97M+ potential agent instances. Not a custom integration — a protocol-level knowledge service. Competitors require bespoke API wrappers; Cherry works out of the box with Claude, GPT, LangChain, and CrewAI.

2. **Human-curated knowledge, not raw data** — Unlike RAG pipelines (stale at indexing) or blockchain-AI projects (raw compute/data), Cherry provides MECE-structured, source-attributed knowledge maintained by domain experts through weekly review cycles.

3. **Managed RAG replacement** — Subscription mode pushes real-time updates when knowledge changes, eliminating the stale vector store problem that plagues every custom RAG pipeline.

The timing convergence: MCP donated to Linux Foundation (97M downloads), Google A2A at 150+ partners, payment rails commoditizing (Visa Trusted Agent Protocol, Coinbase x402). Infrastructure is ready — the missing piece is verified content for agents to consume.

## Project Classification

- **Project Type:** API Backend (primary) + Blockchain/Web3 (secondary)
- **Domain:** Developer Platform / API Marketplace (agent-facing knowledge API with credit-based billing and on-chain transparency)
- **Complexity:** High (multi-chain blockchain + MCP protocol + real-time WebSocket + 4-day hackathon constraint)
- **Project Context:** Brownfield — extending existing Cherry-in-the-Haystack platform with agent-facing API and blockchain payment transparency layer

## Success Criteria

### User Success

- **Agent Builder:** MCP 서버 임포트 한 줄로 Cherry 지식 쿼리 가능 — 커스텀 RAG 파이프라인 구축 불필요
- **Demo Audience (Judges):** "이 에이전트가 뭘 참고했는지" 온체인 영수증으로 즉시 확인 가능 — 블록체인 프로비넌스의 실용적 가치를 체감
- **Curator:** 에이전트 쿼리로 자신의 큐레이션이 수익을 발생시키는 것을 확인

### Business Success

**Primary Goal: Status Network 트랙 수상 ($5,000)**
- Status Network 완성도 100% — 가스리스 에이전트 거래 + Karma 큐레이터 평판 완벽 작동
- General 트랙 ($6,000) 동시 노출 — Status Network 완성도가 곧 General 경쟁력
- BNB Chain / NEAR AI 트랙은 제출 요건만 충족 (최소 온체인 거래, 데모 영상, GitHub)

**Post-Hackathon (3-6 months):**
- 50 registered agent builders (MCP directory, agent framework integrations)
- Hallucination rate reduction: 40%+ vs baseline RAG (A/B comparison)
- $500+/month curator payouts demonstrating unit economics
- LangChain and CrewAI tool registry integration

### Technical Success

**Hackathon — 단 하나의 기준: 데모 중 실패하지 않는 것**
- Happy path 5회 연속 성공 (데모 직전 검증)
- End-to-end flow 작동: register → browse → query → subscribe → pay → curator reward
- 온체인 해시가 화면에 실시간 표시
- 성능 목표는 "체감상 빠름" — 구체적 ms 기준 불필요

**데이터 전략: (기획자 확인 보류)**
- 실제 Cherry 지식 그래프 라이브 데이터 사용이 이상적 (심사 임팩트)
- 대안: 2-3개 핵심 개념만 실제 데이터 + 나머지 시딩
- 기획자 확인 후 결정

### Measurable Outcomes

| Metric | Target | Measurement |
|--------|--------|-------------|
| Status Network 가스리스 트랜잭션 | 5건 이상 | 블록 익스플로러 검증 |
| Karma 티어 읽기/표시 | 작동 확인 | 데모 중 표시 |
| MCP 서버 → Claude 쿼리 | 라이브 데모 | 실시간 시연 |
| 온체인 프로비넌스 해시 | 쿼리당 1건 기록 | 화면 표시 + 익스플로러 |
| 데모 영상 | Status 2분 + BNB/NEAR 각 2-4분 | 제출 완료 |
| 해피패스 연속 성공 | 5회 | 데모 직전 검증 |

## User Journeys

### Journey 1: Hackathon Judge — "이거 진짜네"

**Persona:** Park, BuidlHack2026 Status Network 트랙 심사위원. 블록체인 프로젝트 50개를 2시간 안에 평가해야 한다. 대부분의 프로젝트는 "AI + blockchain" 키워드만 붙여놓은 토큰 발행 앱. 의미 있는 실사용 케이스를 찾고 있다.

**Opening Scene:** 데모 영상 2분짜리를 클릭한다. 또 다른 AI+블록체인 프로젝트인가 싶은 피로감.

**Rising Action:**
1. 화면에 Claude 에이전트가 Cherry KaaS에 질문한다: "What's the best embedding model for Korean text?"
2. 답변이 돌아온다 — 단순 LLM 답변이 아니라, 출처별 에비던스가 구조화되어 있고 품질 스코어가 붙어있다
3. **"와!" 순간**: 답변 옆에 온체인 해시가 실시간으로 팝업된다. Status Network 익스플로러 링크를 클릭하면 — 이 AI가 이 지식을 소비했다는 영수증이 가스리스로 블록체인에 기록되어 있다
4. Karma 티어가 화면에 표시된다 — 큐레이터의 평판 등급이 곧 지식 품질의 신호

**Climax:** "이건 토큰 팔려는 프로젝트가 아니라, 실제로 에이전트가 검증된 지식을 사고 그 증거가 온체인에 남는 시스템이구나." 다른 프로젝트와 결이 다르다는 걸 체감한다.

**Resolution:** README와 GitHub를 확인한다. MCP 서버라서 Claude에 바로 연결된다는 걸 보고, "이건 데모 이후에도 쓸 수 있겠다"고 판단. 높은 점수를 준다.

**이 저니가 드러내는 P0 개발 목록:**
- 에이전트 쿼리 → 구조화된 답변 화면
- 온체인 해시 실시간 팝업 + 익스플로러 링크
- Karma 티어 표시
- 가스리스 트랜잭션 작동 증명
- MCP 서버 라이브 연동

---

### Journey 2: Agent Builder — "RAG 파이프라인 안 만들어도 되네"

**Persona:** Minjun, AI 스타트업 백엔드 개발자. 코딩 어시스턴트를 만들고 있는데, 기술 스택 추천 기능의 RAG 파이프라인을 유지보수하는 데 매주 반나절씩 쏟고 있다. 블로그 크롤링 → 벡터 스토어 갱신 → 결과 품질 확인의 반복.

**Opening Scene:** RAG 추천 결과가 또 틀렸다. 3개월 전에 deprecated된 프레임워크를 자신 있게 추천하고 있다. 벡터 스토어를 갱신해야 하는데 이번 주 스프린트에 시간이 없다.

**Rising Action:**
1. MCP 디렉토리에서 Cherry KaaS를 발견한다. "Knowledge-as-a-Service for AI Agents" — 관심이 간다
2. `POST /agents/register`로 등록. 관심 도메인: AI frameworks, embedding models
3. `GET /catalog`으로 무료 카탈로그 탐색 — 80+개 개념, 품질 스코어, 최종 업데이트 날짜가 보인다. "embedding models" 개념을 클릭하면 미리보기가 나온다
4. 크레딧 충전 후 `POST /purchase`로 개념 구매: "embedding-models, budget=20 credits"
5. 구조화된 답변 수신: 3개 에비던스 노드, 각각 출처·날짜·큐레이터 코멘트 포함. 프로비넌스 해시 확인 가능

**Climax:** 쿼리 응답에 프로비넌스 해시가 붙어있다. "내 에이전트가 뭘 참고했는지 증명할 수 있는 거잖아." 구독 기능(Phase 2)이 나오면 벡터 스토어 갱신도 완전히 대체될 것이라는 로드맵이 보인다.

**Resolution:** MCP 서버 설정 한 줄 추가로 코딩 어시스턴트에 Cherry 지식 연동 완료. RAG 파이프라인 유지보수 시간이 0이 된다. 쿼리 비용 월 $1~2로 반나절/주의 시간을 산다.

**이 저니가 드러내는 개발 목록:**
- Agent registration API
- Catalog browsing API (free, with previews and quality scores)
- Purchase / Follow API (구매 일회성, 팔로우 자동구독)
- Credit system (charge, consume, balance check)
- MCP server integration (one-import setup)

---

### Journey 3: Curator — "내 큐레이션이 돈이 되네"

**Persona:** Hyejin, Cherry Knowledge Team 멤버. 매주 수요일 리뷰 사이클에서 AI 프레임워크 관련 에비던스 20건을 검토한다. 6개월째 자원봉사 — 보람은 있지만 지속성에 의문.

**Opening Scene:** 이번 주 리뷰 완료. 평소처럼 Notion에서 에비던스 검증하고 개념에 연결.

**Rising Action:**
1. KaaS 대시보드에서 이번 주 자신의 큐레이션이 에이전트 쿼리 47건에 활용된 것을 확인
2. 47건 × 평균 10크레딧 × 40% 큐레이터 몫 = 188크레딧 ($1.88) 이번 주 수익

**Climax:** 온체인 출금 버튼 클릭 — 가스리스로 Status Network에 수익이 이체된다. 블록 익스플로러에서 트랜잭션 확인.

**Resolution:** "큐레이션을 계속할 이유가 생겼다." 에이전트 수요가 높은 개념을 확인하고 다음 주 리뷰에서 해당 도메인에 집중하기로 한다.

**이 저니가 드러내는 개발 목록:**
- Curator reward calculation (40% revenue share per query)
- On-chain reward withdrawal (gasless on Status Network)
- Basic earnings visibility (데모에서 한 장면이면 충분)

---

### Journey Requirements Summary

| Priority | Capability | Revealed By | MVP Status |
|----------|-----------|-------------|------------|
| P0 | 온체인 해시 실시간 표시 + 익스플로러 링크 | Judge | Must-have |
| P0 | Karma 티어 읽기/표시 | Judge | Must-have |
| P0 | 가스리스 트랜잭션 작동 | Judge | Must-have |
| P0 | MCP 서버 라이브 연동 (Claude) | Judge, Builder | Must-have |
| P0 | 구조화된 쿼리 응답 (에비던스 + 출처 + 스코어) | Judge, Builder | Must-have |
| P1 | Agent registration API | Builder | Must-have |
| P1 | Catalog browsing API (free previews) | Builder | Must-have |
| P1 | Purchase / Follow API | Builder | Must-have |
| P1 | Subscription API (WebSocket push) | Builder | Should-have (Phase 2) |
| P1 | Credit system (charge/consume) | Builder | Must-have |
| P1 | Knowledge Gap Analysis (catalog compare) | Builder | Must-have |
| P2 | Curator reward calculation + on-chain withdrawal | Curator | Must-have (1 scene) |

## Domain-Specific Requirements

### Blockchain Integration Constraints

- **Status Network (Primary):** `linea_estimateGas` 필수 사용 (`eth_gasPrice` 금지), `from` 필드 필수, 가스비 캐싱 금지 — 매 트랜잭션 재추정
- **Chain Adapter Pattern:** `CHAIN_ADAPTER=status|bnb|near` 환경변수로 체인 전환. 인터페이스 동일, 구현만 분리
- **Smart Contract:** CherryCredit.sol (ERC-20) — deposit(), consumeCredit(), distributeReward(), recordProvenance(). Status Network에서 Karma 티어 할인 추가
- **NEAR는 EVM이 아님:** near-sdk-js 별도 컨트랙트 패턴 필요

### MCP Protocol Compliance

- **MCP Server 표준 준수:** Tools (query_knowledge, get_concept, search_concepts), Resources (concept://{id}, evidence://{id}), Prompts (explain_concept)
- **@modelcontextprotocol/sdk** 패키지 사용
- MCP 디렉토리 등록 가능한 형태로 구현

### API Marketplace Patterns

- **Free tier gateway:** 카탈로그 탐색은 무료, 쿼리/구독은 크레딧 필요
- **Rate limiting:** API key 티어별 제한 (MVP에서는 단순 구현)
- **Structured response format:** 에비던스 + 출처 + 품질 스코어 + 프로비넌스 해시를 일관된 JSON 스키마로

### Hackathon Submission Compliance

- **Status Network:** 5+ 가스리스 트랜잭션, Karma 티어 읽기/표시, 2분 데모 영상, GitHub + README, 라이브 데모
- **BNB Chain:** 2+ 온체인 트랜잭션, 데모 영상, #ConsumerAIonBNB 트윗, 공개 GitHub
- **NEAR AI:** NEAR AI Cloud 사용 데모, 데모 영상
- **General:** 프로젝트 설명, 데모 링크, 발표 덱

### Risk Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Status Network 테스트넷 불안정 | 데모 실패 | 데모 직전 해피패스 5회 검증, 폴백 녹화 영상 준비 |
| 가스리스 트랜잭션 실패 | 핵심 차별점 상실 | linea_estimateGas 정확 구현, from 필드 누락 방지 |
| MCP 서버 연결 끊김 | 라이브 데모 실패 | 로컬 MCP 서버 + 로컬 Claude 연동으로 네트워크 의존성 최소화 |
| 지식 그래프 데이터 부족 | 데모 임팩트 저하 | 기획자 확인 후 실제/시딩 데이터 전략 결정 (보류 중) |
| 3개 트랙 동시 개발로 집중도 분산 | Status Network 완성도 저하 | Day 1-3은 Status Network 전용, Day 4에만 BNB/NEAR 체크리스트 처리 |

## Innovation & Novel Patterns

### Detected Innovation Areas

1. **AI Knowledge Provenance on Blockchain** — AI 에이전트의 지식 소비를 온체인 영수증으로 기록하는 최초의 시스템. 기존 블록체인-AI 프로젝트는 인프라(컴퓨팅, 데이터 스토리지)에 집중하나, Cherry KaaS는 **콘텐츠 레이어** — 검증된 지식 자체를 거래 대상으로 삼는다.

2. **MCP-native Knowledge Marketplace** — MCP 프로토콜 위에 지식 마켓플레이스를 구축한 사례가 없음. MCP 서버 50+개가 존재하지만 모두 도구(tool) 접근용이고, 유료 지식 서비스는 Cherry KaaS가 최초.

3. **Hybrid Architecture (Centralized Speed + On-chain Trust)** — 완전 온체인(Bittensor, Olas)도 아니고 완전 오프체인(Perplexity API)도 아닌 하이브리드. API 속도 + 블록체인 감사 가능성을 동시에 제공하는 의도적 설계 결정.

### Market Context & Competitive Landscape

- **직접 경쟁자 없음:** 인간 큐레이션 + 블록체인 프로비넌스 + 에이전트 네이티브 API를 결합한 서비스가 부재
- **인접 경쟁:** Bittensor(raw compute), Olas(agent tasks), Perplexity API(search results) — 모두 다른 레이어
- **시장 타이밍:** MCP 97M downloads, A2A 150+ partners, 결제 인프라 상용화(Visa, Coinbase x402) — 인프라 준비 완료, 콘텐츠 레이어 부재

### Validation Approach

- **Hackathon as validation:** 심사위원 반응이 첫 시장 검증 — "이게 진짜 필요한 서비스인가"에 대한 전문가 피드백
- **Post-hackathon:** MCP 디렉토리 등록 후 50명 에이전트 빌더 확보 여부로 제품-시장 적합성 판단
- **핵심 가설:** "에이전트 빌더는 검증된 지식 API에 돈을 낼 의향이 있다" — 월 $1~2 구독으로 RAG 유지보수 반나절/주 절약. ROI 환산: 개발자 시급 $50 기준, 반나절/주 = $200/주 = **$800/월 절약 vs $1~2/월 구독비 (400x~800x ROI)**

### Innovation Risk Mitigation

| Innovation Risk | Mitigation |
|----------------|------------|
| MCP 생태계가 예상보다 느리게 성장 | REST API 동시 제공으로 MCP 의존도 분산 |
| 에이전트 빌더의 유료 지식 수요 불확실 | 무료 카탈로그 → 유료 전환 퍼널로 수요 검증 |
| 온체인 프로비넌스의 실용적 가치 의문 | EU AI Act Article 13 규제 요건과 연계하여 compliance 가치 강조 |

## API Backend Specific Requirements

### Project-Type Overview

Cherry KaaS는 AI 에이전트 전용 Knowledge API 서버로, MCP 프로토콜과 REST API 두 채널을 통해 지식을 제공한다. 핵심 설계 원칙: MCP 서버가 primary 배포 채널이며, REST API는 MCP 미지원 클라이언트를 위한 보조 채널.

### Endpoint Specifications

**Base URL:** `/api/v1/`

**Public Endpoints (인증 불필요):**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/agents/register` | 에이전트 등록, API key 발급 |
| GET | `/v1/catalog` | 개념 목록 + 미리보기 + 품질 스코어 + 최종 업데이트 |
| GET | `/v1/catalog/:conceptId` | 개념 상세 미리보기 (무료) |

**Authenticated Endpoints (API Key 필수):**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v1/purchase` | 개념 구매 — 전체 지식(evidence 포함) 일회성 수령 |
| POST | `/v1/follow` | 개념 팔로우 — 업데이트 시 자동 구독 수령 |
| GET | `/v1/credits/balance` | 크레딧 잔액 조회 |
| POST | `/v1/credits/deposit` | 크레딧 충전 (온체인 트랜잭션 연동) |
| POST | `/v1/rewards/withdraw` | 큐레이터 보상 온체인 출금 |
| POST | `/v1/catalog/compare` | 에이전트 보유 지식 vs 카탈로그 갭 분석 |

**MCP Server Tools (동일 기능, MCP 프로토콜):**

| Tool | Maps to |
|------|---------|
| `purchase_concept` | POST /v1/purchase |
| `follow_concept` | POST /v1/follow |
| `get_concept` | GET /v1/catalog/:conceptId |
| `search_concepts` | GET /v1/catalog?q=... |
| `compare_knowledge` | POST /v1/catalog/compare |

**MCP Resources:** `concept://{id}`, `evidence://{id}`
**MCP Prompts:** `explain_concept`

### Authentication Model

- **MVP:** API Key (등록 시 발급) + JWT 세션 토큰
- **Wallet signature (EIP-712):** 크레딧 충전/출금 시 지갑 서명 필요
- **Rate limiting:** API key 당 100 req/min (MVP 단순 구현)
- **별도 SDK 없음:** MCP 서버가 SDK 역할 — "MCP 서버 하나로 Claude, LangChain, CrewAI 다 됩니다"

### Data Schemas

**Purchase Request:**
```json
{
  "concept_id": "rag",
  "action": "purchase",
  "budget": 20,
  "language": "en"
}
```

**Follow Request:**
```json
{
  "concept_id": "rag",
  "action": "follow",
  "budget_per_update": 5
}
```

**Purchase/Follow Response:**
```json
{
  "answer": { "summary": "...", "concepts": [...], "evidence": [...] },
  "quality_score": 4.2,
  "sources": [{ "url": "...", "author": "...", "date": "..." }],
  "credits_consumed": 20,
  "provenance": {
    "hash": "0xabc123...",
    "chain": "status",
    "explorer_url": "https://sepoliascan.status.network/tx/0xabc123..."
  }
}
```

**Compare Request:**
```json
{
  "known_topics": ["RAG", "fine-tuning", "prompt engineering"],
  "domain": "AI Engineering"
}
```

**Compare Response:**
```json
{
  "matched": [
    { "topic": "RAG", "concept_id": "rag", "quality_score": 4.8 }
  ],
  "gaps": [
    { "concept_id": "chain-of-thought", "title": "Chain-of-Thought Prompting", "quality_score": 4.5, "reason": "Not in agent's knowledge base" },
    { "concept_id": "embeddings", "title": "Embeddings & Vector Databases", "quality_score": 4.2, "reason": "Not in agent's knowledge base" }
  ],
  "recommendations": [
    { "concept_id": "chain-of-thought", "action": "purchase", "estimated_credits": 20 }
  ]
}
```

**Subscription Event (WebSocket push):**
```json
{
  "type": "evidence_added",
  "concept_id": "embedding-models",
  "evidence_summary": "...",
  "provenance_hash": "0xdef456...",
  "freshness": 0.95
}
```

### Error Codes

도메인 특화 에러코드 3종 (데모 중 에러 상황을 오히려 기능 시연으로 활용):

```json
{ "code": "INSUFFICIENT_CREDITS", "message": "Not enough credits for this query", "credits_required": 20, "credits_available": 5 }
```
```json
{ "code": "KARMA_TIER_REQUIRED", "message": "This feature requires Silver tier or above", "required_tier": "silver" }
```
```json
{ "code": "CONCEPT_NOT_FOUND", "message": "Concept not found in knowledge graph", "concept_id": "rag" }
```

표준 HTTP 에러: 400 (bad request), 401 (unauthorized), 429 (rate limited), 500 (server error)

### Technical Architecture Considerations

- **Modular Monolith** (Node.js/Express/TypeScript) — 해커톤 속도 우선, 마이크로서비스 아님
- **Event-driven:** in-memory EventEmitter (MVP), Redis Pub/Sub 업그레이드 가능
- **Database:** SQLite (MVP), PostgreSQL (post-hackathon)
- **WebSocket:** ws 라이브러리로 구독 push
- **Versioning:** `/v1/` prefix — 프로덕션 고려 + 향후 breaking change 시 `/v2/` 분리

### Implementation Considerations

- Chain Adapter 패턴으로 블록체인 레이어 추상화 — API 서버 코드는 체인에 무관
- MCP 서버와 REST API가 동일 비즈니스 로직 공유 (서비스 레이어 분리)
- 모든 쿼리 응답에 provenance hash 포함 — 블록체인 기록은 비동기 처리로 API 응답 지연 방지

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP Approach:** Demo MVP — 해커톤 심사위원이 타겟. "작동하는 엔드투엔드 데모"가 유일한 기준. 기능 수보다 핵심 플로우의 완성도에 집중.

**Resource Requirements:** 1인 개발 (4일), 기존 Cherry 지식 그래프 + AWS 인프라 활용

### MVP Feature Set (Phase 1 — Hackathon April 16)

**Core Journey Supported:** Judge 저니 (데모 시나리오 = P0 개발 목록)

**Must-Have:**
- Agent registration + API key 발급
- Catalog browsing (free, 미리보기 + 품질 스코어) + Knowledge Gap Analysis
- Purchase / Follow API (구매 일회성 + 팔로우 자동구독)
- Credit system (charge, consume, balance)
- On-chain provenance hash (실시간 표시 + 익스플로러 링크)
- Karma tier 읽기/표시/할인 적용
- MCP server (query_knowledge, get_concept, search_concepts)
- Curator reward calculation + on-chain withdrawal (데모 1장면)
- CherryCredit.sol 스마트 컨트랙트 (Status Network, gasless)
- `/v1/` API versioning

**Should-Have (시간 여유 시):**
- Subscription API (WebSocket push) — Must-have에서 하향. 데모 시연 구조적 어려움 + 구현 복잡도 대비 임팩트 낮음. 엔드포인트 스펙은 문서에 유지
- Chain Adapter + BNB Chain 제출 요건 (2+ 온체인 트랜잭션, 데모 영상)
- Chain Adapter + NEAR AI 제출 요건 (NEAR AI Cloud 데모)

**Won't-Have in MVP:**
- SLA Lite auto-credit
- Curator earnings page (/kaas/curator)
- MCP integration guide page (/kaas/mcp)
- Performance optimization (latency targets)
- Separate npm SDK package

### Post-MVP Features

**Phase 2 (Growth — post-hackathon 3-6 months):**
- Subscription API (WebSocket real-time push) — MVP 스펙 기반 구현
- Tiered pricing (purchase/follow/bundle/custom synthesis)
- Agent DID authentication
- Query analytics → curator demand signals pipeline
- Knowledge bundle packages
- LangChain / CrewAI tool registry listing
- Curator earnings dashboard
- MCP integration guide

**Phase 3 (Expansion — 6-12 months):**
- Curate-to-Earn tokenomics
- Domain-specialized guilds (DAO governance)
- Knowledge futures / prediction markets
- Agent-to-agent knowledge reselling + curator royalties
- Multi-domain expansion (crypto/DeFi, biotech, regulatory)
- Dynamic pricing (supply/demand signals)
- Cherry KaaS as Bittensor subnet / Olas knowledge service

### Risk Mitigation Strategy

**Technical Risks:**
- 최대 기술 리스크: Status Network gasless 트랜잭션 구현 (linea_estimateGas 특수 처리)
- 완화: Day 1에 스마트 컨트랙트 + gasless 동작 먼저 검증, 나머지는 이 위에 빌드

**Market Risks:**
- 최대 시장 리스크: 에이전트 빌더의 유료 지식 수요 불확실
- 완화: 해커톤 심사위원 피드백이 첫 시장 검증. Post-hackathon MCP 디렉토리 등록 후 50명 확보 여부로 판단

**Resource Risks:**
- 1인 개발 + 4일 제약
- 완화: Day 1-3 Status Network 전용 → Day 4 BNB/NEAR 최소 요건. 절대 메인 트랙 희생하지 않음
- 최소 기능 세트: Query → 온체인 해시만 작동해도 데모 가능 (등록/카탈로그는 하드코딩 폴백). 크레딧 시스템도 하드코딩 폴백 가능 (잔액 250 고정, 차감만 UI에 표시)

## Functional Requirements

### 1. Agent Identity & Access

- **FR1:** Agent can register with domain interests and receive an API key
- **FR2:** Agent can authenticate API requests using issued API key
- **FR3:** Agent can connect wallet (EIP-712 signature) for on-chain transactions

### 2. Knowledge Discovery

- **FR4:** Agent can browse the full concept catalog without authentication
- **FR5:** Agent can view concept previews including quality score, source count, and last updated date
- **FR6:** Agent can search concepts by keyword or category
- **FR7:** Agent can view detailed concept information including related concepts and evidence count

### 3. Knowledge Consumption

- **FR8:** Agent can purchase a concept to receive the full structured knowledge (evidence, sources, curator comments, quality scores) via one-time credit deduction
- **FR8a:** Agent can follow a concept to automatically receive updated knowledge when the concept is updated (recurring credit deduction per update)
- **FR9:** Agent can set a budget cap (in credits) per purchase or follow subscription
- **FR10:** Agent can receive structured responses containing evidence nodes, source attribution, curator comments, and quality scores
- **FR11:** Agent can access knowledge via MCP server tools (query_knowledge, get_concept, search_concepts)
- **FR12:** Agent can access knowledge via MCP resources (concept://{id}, evidence://{id})

### 4. Credit & Payment System

- **FR13:** Agent can view current credit balance
- **FR14:** Agent can deposit credits via on-chain transaction (gasless on Status Network)
- **FR15:** System deducts credits per purchase (one-time ~20cr per concept) or per follow update (~5cr per update notification)
- **FR16:** System applies Karma tier discount to credit consumption (tiered: 30%/15%/5%/0%)
- **FR17:** System returns INSUFFICIENT_CREDITS error with required/available amounts when balance is insufficient
- **FR18:** System returns KARMA_TIER_REQUIRED error when feature requires higher tier

### 5. On-chain Provenance

- **FR19:** System records provenance hash on-chain for every knowledge query (gasless on Status Network)
- **FR19a:** Provenance recording executes asynchronously — API response returns immediately with provisional hash, on-chain confirmation follows in background
- **FR20:** Agent can view provenance hash and block explorer link in query response
- **FR21:** System displays provenance hash in real-time on query result screen
- **FR22:** Any party can verify knowledge consumption record via block explorer

### 6. Karma Integration (Status Network)

- **FR23:** System reads agent's Karma balance and tier from on-chain contract
- **FR24:** System displays Karma tier in agent profile and query responses
- **FR25:** System applies tier-based benefits (credit discount, rate limit increase)

### 7. Curator Rewards

- **FR26:** System calculates curator reward share (40% of query revenue) per contributing curator
- **FR27:** Curator can withdraw accumulated rewards via gasless on-chain transaction
- **FR28:** Curator can view basic earnings information (total earned, pending withdrawal)

### 8. Smart Contract Operations

- **FR29:** CherryCredit.sol supports deposit(), consumeCredit(), distributeReward(), recordProvenance()
- **FR30:** Smart contract emits events: CreditConsumed, RewardDistributed, ProvenanceRecorded
- **FR31:** All contract operations execute gaslessly on Status Network

### 9. Multi-chain Support (Should-have)

- **FR32:** System supports chain switching via Chain Adapter pattern (CHAIN_ADAPTER env var)
- **FR33:** System can deploy and operate on BNB Chain (opBNB testnet) with minimum 2 on-chain transactions
- **FR34:** System can integrate with NEAR AI Cloud for TEE-based inference demo

### 10. Knowledge Gap Analysis

- **FR37:** Agent can submit a list of its own knowledge topics and receive a gap analysis report comparing against the Cherry catalog
- **FR38:** System returns structured gap report containing: matched concepts (already known), missing concepts (knowledge gaps), and recommended queries to fill gaps
- **FR39:** Agent can access knowledge gap analysis via MCP server tool (compare_knowledge)

### 11. Error Handling & Resilience

- **FR35:** System returns domain-specific error codes (INSUFFICIENT_CREDITS, KARMA_TIER_REQUIRED, CONCEPT_NOT_FOUND) with actionable context
- **FR36:** System supports hardcoded fallback mode for demo resilience (fixed catalog, fixed credit balance 250)

## Non-Functional Requirements

### Performance

- **NFR1:** API query response returns to client before on-chain provenance recording completes (async architecture)
- **NFR2:** Demo happy path completes end-to-end without perceptible delay (no spinner longer than 3 seconds)
- **NFR3:** System sustains 5 consecutive demo runs without failure or degradation

### Security

- **NFR4:** API keys are generated with sufficient entropy and transmitted only over HTTPS
- **NFR5:** Wallet signatures (EIP-712) are verified server-side before executing on-chain transactions (deposit, withdrawal)
- **NFR6:** Credit balance modifications require authenticated API key — no unauthenticated credit operations
- **NFR7:** Smart contract functions with financial impact (distributeReward, consumeCredit) are restricted to authorized callers (owner/server)

### Integration

- **NFR8:** MCP server complies with @modelcontextprotocol/sdk standards — compatible with Claude, GPT, LangChain, CrewAI without custom adapters
- **NFR9:** Status Network integration uses `linea_estimateGas` exclusively (never `eth_gasPrice`), with `from` field mandatory on every call
- **NFR10:** Chain Adapter interface is identical across Status/BNB/NEAR — switching requires only environment variable change, no code modification
- **NFR11:** Existing Cherry knowledge graph data (concepts, evidence, sources) is consumed read-only — KaaS does not modify the source knowledge base

### Reliability

- **NFR12:** 환경변수 `DEMO_FALLBACK=true` 설정 시 하드코딩 폴백 모드 활성화 — 데모 직전 수동 전환 가능, 장애 시 즉시 환경변수 변경으로 폴백
- **NFR13:** On-chain transaction failure does not block API response — provenance recording retries independently in background
