---
stepsCompleted: [1, 2, 3]
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/architecture.md'
---

# Cherry KaaS - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Cherry KaaS, decomposing the requirements from the PRD and Architecture into implementable stories for BuidlHack2026 hackathon (deadline: April 16, 2026).

## Requirements Inventory

### Functional Requirements

- FR1: Agent can register with domain interests and receive an API key
- FR2: Agent can authenticate API requests using issued API key
- FR3: Agent can connect wallet (EIP-712 signature) for on-chain transactions
- FR4: Agent can browse the full concept catalog without authentication
- FR5: Agent can view concept previews including quality score, source count, and last updated date
- FR6: Agent can search concepts by keyword or category
- FR7: Agent can view detailed concept information including related concepts and evidence count
- FR8: Agent can purchase a concept (one-time) or follow a concept (auto-subscribe to updates)
- FR9: Agent can set a budget cap (in credits) per query
- FR10: Agent can receive structured responses containing evidence nodes, source attribution, curator comments, and quality scores
- FR11: Agent can access knowledge via MCP server tools (query_knowledge, get_concept, search_concepts)
- FR12: Agent can access knowledge via MCP resources (concept://{id}, evidence://{id})
- FR13: Agent can view current credit balance
- FR14: Agent can deposit credits via on-chain transaction (gasless on Status Network)
- FR15: System deducts credits per purchase (20cr) or per follow update (~5cr)
- FR16: System applies Karma tier discount to credit consumption (tiered: 30%/15%/5%/0%)
- FR17: System returns INSUFFICIENT_CREDITS error with required/available amounts when balance is insufficient
- FR18: System returns KARMA_TIER_REQUIRED error when feature requires higher tier
- FR19: System records provenance hash on-chain for every knowledge query (gasless on Status Network)
- FR19a: Provenance recording executes asynchronously — API response returns immediately with provisional hash
- FR20: Agent can view provenance hash and block explorer link in query response
- FR21: System displays provenance hash in real-time on query result screen
- FR22: Any party can verify knowledge consumption record via block explorer
- FR23: System reads agent's Karma balance and tier from on-chain contract
- FR24: System displays Karma tier in agent profile and query responses
- FR25: System applies tier-based benefits (credit discount, rate limit increase)
- FR26: System calculates curator reward share (40% of query revenue) per contributing curator
- FR27: Curator can withdraw accumulated rewards via gasless on-chain transaction
- FR28: Curator can view basic earnings information (total earned, pending withdrawal)
- FR29: CherryCredit.sol supports deposit(), consumeCredit(), distributeReward(), recordProvenance()
- FR30: Smart contract emits events: CreditConsumed, RewardDistributed, ProvenanceRecorded
- FR31: All contract operations execute gaslessly on Status Network
- FR32: System supports chain switching via Chain Adapter pattern (CHAIN_ADAPTER env var)
- FR33: System can deploy and operate on BNB Chain (opBNB testnet) with minimum 2 on-chain transactions
- FR34: System can integrate with NEAR AI Cloud for TEE-based inference demo
- FR35: System returns domain-specific error codes with actionable context
- FR36: System supports hardcoded fallback mode for demo resilience (DEMO_FALLBACK=true)

### NonFunctional Requirements

- NFR1: API query response returns before on-chain provenance recording completes (async)
- NFR2: Demo happy path completes without perceptible delay (no spinner > 3s)
- NFR3: System sustains 5 consecutive demo runs without failure
- NFR4: API keys generated with sufficient entropy, transmitted only over HTTPS
- NFR5: Wallet signatures (EIP-712) verified server-side before on-chain transactions
- NFR6: Credit balance modifications require authenticated API key
- NFR7: Smart contract financial functions restricted to authorized callers
- NFR8: MCP server complies with @modelcontextprotocol/sdk standards
- NFR9: Status Network uses linea_estimateGas exclusively, from field mandatory
- NFR10: Chain Adapter interface identical across chains — env var swap only
- NFR11: Existing Cherry knowledge graph consumed read-only
- NFR12: DEMO_FALLBACK=true env var activates hardcoded fallback mode
- NFR13: On-chain transaction failure does not block API response

### Additional Requirements

- 기존 모노레포 확장 — 신규 앱 생성 없음, 기존 apps/web + apps/api에 파일 추가
- NestJS 모듈 패턴 (kaas.module.ts + 4개 컨트롤러/서비스)
- DB 마이그레이션: kaas.agent, kaas.credit_ledger, kaas.query_log, kaas.curator_reward 4개 테이블
- chain-adapter 패키지: IChainAdapter 인터페이스 + Status/BNB/NEAR/Mock 구현
- kaas-core 패키지: 프레임워크 무관 비즈니스 로직
- contracts/: Hardhat + CherryCredit.sol
- MCP 서버: 별도 프로세스 (start:mcp 스크립트)
- kaas.concept + kaas.evidence 테이블: 9개 개념 (RAG, CoT, Embeddings, Fine-tuning, Multi-Agent, Evaluation, Prompt Engineering, Agent Architectures, Semantic Search)
- 사이드바 수정: SECTIONS 배열에 KAAS 섹션 추가 (기존 코드 수정 3건)

### UX Design Requirements

N/A — UX 문서 미작성

### FR Coverage Map

| FR | Epic | Description |
|----|------|-------------|
| FR1 | Epic 2 | Agent registration |
| FR2 | Epic 2 | API key authentication |
| FR3 | Epic 3 | Wallet connection (EIP-712) |
| FR4 | Epic 2 | Catalog browsing |
| FR5 | Epic 2 | Concept previews |
| FR6 | Epic 2 | Concept search |
| FR7 | Epic 2 | Concept detail |
| FR8 | Epic 2 | Purchase / Follow concept |
| FR9 | Epic 2 | Budget cap |
| FR10 | Epic 2 | Structured responses |
| FR11 | Epic 4 | MCP tools |
| FR12 | Epic 4 | MCP resources |
| FR13 | Epic 3 / Epic 5 (UI) | Credit balance |
| FR14 | Epic 3 | Credit deposit (on-chain) |
| FR15 | Epic 3 | Credit deduction per purchase/follow |
| FR16 | Epic 3 | Karma tier discount |
| FR17 | Epic 3 | INSUFFICIENT_CREDITS error |
| FR18 | Epic 3 | KARMA_TIER_REQUIRED error |
| FR19 | Epic 3 | On-chain provenance recording |
| FR19a | Epic 3 | Async provenance |
| FR20 | Epic 3 / Epic 5 (UI) | Provenance hash in response + display |
| FR21 | Epic 5 | Real-time hash display on screen |
| FR22 | Epic 3 | Block explorer verification |
| FR23 | Epic 1 | Karma balance read |
| FR24 | Epic 1 / Epic 5 (UI) | Karma tier display |
| FR25 | Epic 1 | Karma tier benefits |
| FR26 | Epic 6 | Curator reward calculation |
| FR27 | Epic 6 | On-chain reward withdrawal |
| FR28 | Epic 6 / Epic 5 (UI) | Earnings visibility |
| FR29 | Epic 1 | CherryCredit.sol functions |
| FR30 | Epic 1 | Contract events |
| FR31 | Epic 1 | Gasless operations |
| FR32 | Epic 7 | Chain Adapter pattern |
| FR33 | Epic 7 | BNB Chain deployment |
| FR34 | Epic 7 | NEAR AI integration |
| FR35 | Epic 2 | Domain error codes |
| FR36 | Epic 2 | Fallback mode |
| FR37 | Epic 2 | Knowledge gap analysis — submit known topics |
| FR38 | Epic 2 | Gap report — matched, missing, recommendations |
| FR39 | Epic 4 | MCP compare_knowledge tool |

## Epic List

### Epic 1: Smart Contract & Blockchain Foundation (Day 1)
에이전트가 가스리스로 온체인 거래를 실행할 수 있다. CherryCredit.sol 배포 + Status Network gasless 동작 검증.
**FRs covered:** FR29, FR30, FR31, FR23, FR24, FR25

### Epic 2: Knowledge API & Catalog (Day 2)
에이전트가 지식 카탈로그를 탐색하고, 자연어 쿼리로 구조화된 답변을 받을 수 있다. 보유 지식 대비 갭 분석도 제공한다.
**FRs covered:** FR1, FR2, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR35, FR36, FR37, FR38

### Epic 3: Credit System & Provenance (Day 2)
에이전트가 크레딧으로 결제하고, 모든 쿼리의 온체인 영수증을 받을 수 있다. (데모 "와!" 순간)
**FRs covered:** FR3, FR13, FR14, FR15, FR16, FR17, FR18, FR19, FR19a, FR20, FR21, FR22

### Epic 4: MCP Server (Day 3)
에이전트가 MCP 프로토콜로 Cherry 지식에 원클릭 접근할 수 있다.
**FRs covered:** FR11, FR12, FR39

### Epic 5: Demo Dashboard (Day 3)
심사위원이 데모에서 쿼리→온체인 해시→Karma 표시를 시각적으로 확인할 수 있다.
**FRs covered:** FR20 (UI), FR21 (UI), FR24 (UI), FR13 (UI), FR28 (UI)

### Epic 6: Curator Rewards (Day 3)
큐레이터가 에이전트 쿼리로 발생한 수익을 확인하고 온체인으로 출금할 수 있다.
**FRs covered:** FR26, FR27, FR28

### Epic 7: Multi-chain Submission (Day 4, Should-have)
BNB Chain과 NEAR AI 트랙 제출 요건을 충족할 수 있다.
**FRs covered:** FR32, FR33, FR34

---

## Epic 1: Smart Contract & Blockchain Foundation

에이전트가 가스리스로 온체인 거래를 실행할 수 있다.

### Story 1.1: CherryCredit.sol 배포 및 Gasless 검증

As a developer,
I want CherryCredit.sol을 Status Network 테스트넷에 배포하고 gasless 동작을 검증,
So that 모든 후속 온체인 기능의 기반이 준비된다.

**Acceptance Criteria:**

**Given** Hardhat 프로젝트가 contracts/에 설정됨
**When** deploy.ts 스크립트를 실행
**Then** CherryCredit.sol이 Status Network 테스트넷(Chain ID 1660990954)에 배포됨
**And** deposit(), consumeCredit(), distributeReward(), recordProvenance() 함수가 존재함
**And** CreditConsumed, RewardDistributed, ProvenanceRecorded 이벤트가 emit됨
**And** linea_estimateGas로 추정 시 baseFeePerGas === 0x0 (gasless 확인)
**And** 컨트랙트 주소가 .env에 기록됨

### Story 1.2: Chain Adapter — Status Network 구현

As a developer,
I want IChainAdapter 인터페이스와 Status Network 어댑터를 구현,
So that 비즈니스 로직이 블록체인 구현 세부사항을 모른 채 온체인 기능을 호출할 수 있다.

**Acceptance Criteria:**

**Given** apps/api/src/modules/kaas/chain-adapter/ 디렉토리가 생성됨
**When** StatusAdapter가 IChainAdapter를 구현
**Then** recordProvenance(hash) → Status Network에 gasless 트랜잭션 실행
**And** depositCredit(agent, amount) → CherryCredit.deposit() 호출
**And** withdrawReward(curator, amount) → CherryCredit.distributeReward() 호출
**And** getKarmaTier(address) → Karma 컨트랙트에서 티어 조회
**And** CHAIN_ADAPTER=status 환경변수로 어댑터 선택 가능
**And** MockAdapter (DEMO_FALLBACK용)도 함께 구현

### Story 1.3: DB 마이그레이션 — KaaS 테이블 생성

As a developer,
I want kaas_* 4개 테이블을 PostgreSQL에 생성,
So that 에이전트, 크레딧, 쿼리, 보상 데이터를 저장할 수 있다.

**Acceptance Criteria:**

**Given** knex 마이그레이션 파일 20260413_create_kaas_tables.ts가 생성됨
**When** 마이그레이션 실행
**Then** kaas.agent (api_key, wallet_address, karma_tier, domain_interests, created_at) 생성
**And** kaas.credit_ledger (agent_id FK, amount, type, tx_hash, created_at) 생성
**And** kaas.query_log (agent_id FK, concept_id, action_type [purchase|follow], credits_consumed, provenance_hash, chain, created_at) 생성
**And** kaas.curator_reward (curator_id, query_log_id FK, amount, withdrawn boolean, withdrawal_tx_hash, created_at) 생성
**And** idx_kaas.agent_api_key 인덱스 생성

---

## Epic 2: Knowledge API & Catalog

에이전트가 지식 카탈로그를 탐색하고, 자연어 쿼리로 구조화된 답변을 받을 수 있다.

### Story 2.1: 지식 카탈로그 DB 테이블 + KnowledgeService 구현

As an agent builder,
I want Cherry 지식 카탈로그의 개념/에비던스 데이터에 DB를 통해 접근,
So that 카탈로그 조회, 구매, 비교의 데이터 소스가 준비된다.

**Acceptance Criteria:**

**Given** kaas.concept + kaas.evidence 테이블에 9개 개념이 INSERT됨
**When** KnowledgeService가 DB에서 데이터를 조회
**Then** 9개 개념이 조회됨 (RAG, Chain-of-Thought, Embeddings, Fine-tuning, Multi-Agent, Evaluation, Prompt Engineering, Agent Architectures, Semantic Search)
**And** 각 개념에 id, title, category, summary, content_md(실제 지식 본문), quality_score, source_count, updated_at, related_concepts 포함
**And** 각 개념에 2-3개 에비던스 (id, concept_id, source, summary, curator, curator_tier, comment) 연결
**And** 카탈로그 조회 시 content_md 제외 (미리보기만), 구매 시 content_md 포함
**And** KnowledgeService는 Knex DB 조회 (seed-data.json 사용 안 함)

### Story 2.2: Agent 등록 및 API Key 인증

As an agent builder,
I want 에이전트를 등록하고 API key를 발급받아 인증된 요청을 보낼 수 있다,
So that KaaS API에 안전하게 접근할 수 있다.

**Acceptance Criteria:**

**Given** NestJS kaas.module.ts와 kaas-agent.controller.ts가 생성됨
**When** POST /api/v1/kaas/agents/register에 domain_interests와 wallet_address 전송
**Then** kaas.agent 레코드 생성 + 충분한 엔트로피의 API key 반환
**And** 이후 요청에 Authorization: Bearer {api_key} 헤더로 인증 가능
**And** 잘못된 API key 시 401 Unauthorized 반환
**And** Zod DTO로 입력 검증
**And** Swagger 데코레이터 포함

### Story 2.3: 카탈로그 브라우징 API

As an agent builder,
I want 개념 카탈로그를 인증 없이 탐색하고 검색,
So that 유료 쿼리 전에 어떤 지식이 있는지 미리 확인할 수 있다.

**Acceptance Criteria:**

**Given** kaas-query.controller.ts가 생성됨
**When** GET /api/v1/kaas/catalog 호출
**Then** 전체 개념 목록 반환 (id, title, category, quality_score, source_count, updated_at)
**And** GET /api/v1/kaas/catalog/:conceptId로 개념 상세 + 에비던스 카운트 + 관련 개념 조회
**And** GET /api/v1/kaas/catalog?q=embedding으로 키워드 검색
**And** 인증 불필요 (Public endpoint)
**And** CONCEPT_NOT_FOUND 에러코드 반환 (존재하지 않는 conceptId)

### Story 2.4: 지식 구매 / 팔로우 API

As an agent builder,
I want 개념을 구매하거나 팔로우하여 구조화된 지식을 받을 수 있다,
So that 내 에이전트에 검증된 지식을 통합할 수 있다.

**Acceptance Criteria:**

**Given** 인증된 에이전트가 API key를 보유
**When** POST /api/v1/kaas/purchase에 { concept_id, budget } 전송
**Then** 해당 개념의 전체 지식 반환: answer (summary + concepts + evidence), quality_score, sources, credits_consumed
**And** 크레딧 일회성 차감 (20cr per concept)
**And** 구매 로그가 kaas.query_log에 기록됨
**When** POST /api/v1/kaas/follow에 { concept_id, budget_per_update } 전송
**Then** 해당 개념 팔로우 등록, 업데이트 시 자동으로 최신 지식 수령
**And** 업데이트당 크레딧 자동 차감 (25cr (업데이트 포함))
**And** DEMO_FALLBACK=true 시 시딩 데이터에서 매칭하여 응답

### Story 2.5: Knowledge Gap Analysis API

As an agent builder,
I want 내 에이전트가 보유한 지식 목록을 Cherry 카탈로그와 비교하여 부족한 개념을 파악,
So that 어떤 지식을 추가로 구매해야 하는지 데이터 기반으로 결정할 수 있다.

**Acceptance Criteria:**

**Given** 인증된 에이전트가 API key를 보유 (또는 Public 접근 가능)
**When** POST /api/v1/kaas/catalog/compare에 { known_topics: ["RAG", "fine-tuning"], domain: "AI Engineering" } 전송
**Then** 구조화된 갭 리포트 반환:
  - matched: 카탈로그에 존재하고 에이전트도 보유한 개념 (concept_id, quality_score)
  - gaps: 카탈로그에 있지만 에이전트가 보유하지 않은 개념 (concept_id, title, quality_score, reason)
  - recommendations: 우선 구매 추천 (concept_id, action [purchase|follow], estimated_credits)
**And** 매칭은 키워드 기반 유사도 비교 (정확 매칭 + 부분 매칭)
**And** gaps는 quality_score 내림차순으로 정렬 (품질 높은 지식 우선 추천)
**And** DEMO_FALLBACK=true 시 시딩 데이터에서 매칭하여 응답
**And** 인증 불필요 (Public endpoint) — 무료 카탈로그 탐색의 확장

---

## Epic 3: Credit System & Provenance

에이전트가 크레딧으로 결제하고, 모든 쿼리의 온체인 영수증을 받을 수 있다.

### Story 3.1: 크레딧 잔액 조회 및 차감

As an agent builder,
I want 크레딧 잔액을 확인하고 쿼리 시 자동 차감되도록,
So that 지식 소비 비용을 관리할 수 있다.

**Acceptance Criteria:**

**Given** 인증된 에이전트가 존재
**When** GET /api/v1/kaas/credits/balance 호출
**Then** 현재 크레딧 잔액 반환
**And** 구매 시 20cr 일회성 차감, 팔로우 업데이트 시 Follow 25cr (업데이트 포함)
**And** Karma 티어별 할인 적용 (30%/15%/5%/0%)
**And** 잔액 부족 시 INSUFFICIENT_CREDITS 에러 반환 (credits_required, credits_available 포함)
**And** 차감 이력이 kaas.credit_ledger에 type=consume으로 기록
**And** DEMO_FALLBACK=true 시 잔액 250 고정, 차감만 UI에 표시

### Story 3.2: 크레딧 충전 (온체인)

As an agent builder,
I want MetaMask 지갑으로 크레딧을 충전,
So that 쿼리에 사용할 크레딧을 확보할 수 있다.

**Acceptance Criteria:**

**Given** 에이전트가 MetaMask 지갑을 연결 (EIP-712 서명)
**When** POST /api/v1/kaas/credits/deposit에 amount + wallet signature 전송
**Then** CherryCredit.deposit() 온체인 호출 (gasless on Status Network)
**And** 서버에서 EIP-712 서명 검증 후 실행
**And** kaas.credit_ledger에 type=deposit, tx_hash 기록
**And** 잔액이 충전액만큼 증가
**And** KARMA_TIER_REQUIRED 에러 반환 (해당 기능이 특정 티어 필요 시)

### Story 3.3: 비동기 프로비넌스 기록 및 해시 반환

As an agent builder,
I want 모든 쿼리에 온체인 프로비넌스 해시가 포함된 응답을 받을 수 있다,
So that AI가 소비한 지식의 출처를 검증할 수 있다.

**Acceptance Criteria:**

**Given** 인증된 에이전트가 쿼리를 실행
**When** 쿼리 응답이 생성됨
**Then** 응답에 provenance.hash + provenance.explorer_url 포함
**And** API 응답은 온체인 기록 완료 전에 즉시 반환 (provisional hash)
**And** EventEmitter로 'provenance.record' 이벤트 발행 → 백그라운드에서 온체인 기록
**And** chain-adapter.recordProvenance(hash) 호출로 Status Network에 gasless 기록
**And** 온체인 기록 실패 시 3회 재시도 후 로그 (API 응답 블로킹 없음)
**And** 블록 익스플로러(sepoliascan.status.network)에서 트랜잭션 검증 가능
**And** kaas.query_log에 provenance_hash, chain 기록

---

## Epic 4: MCP Server

에이전트가 MCP 프로토콜로 Cherry 지식에 원클릭 접근할 수 있다.

### Story 4.1: MCP Server — Streamable HTTP

As an agent builder,
I want MCP Streamable HTTP로 Cherry KaaS에 원격 접속,
So that 로컬 에이전트가 어디서든 Cherry에 연결하여 지식을 검색/구매할 수 있다.

**Acceptance Criteria:**

**Given** MCP 서버가 Streamable HTTP transport로 실행됨
**When** 에이전트가 `https://cherry-kaas.com/mcp` 엔드포인트에 HTTP POST 요청
**Then** Bearer token (ck_live_...) 으로 에이전트 인증
**And** Tools 5개: search_catalog, get_concept, purchase_concept, follow_concept, compare_knowledge
**And** Resources 2개: kaas://catalog, kaas://concept/{id}
**And** 세션 관리: 연결된 에이전트 추적, Dashboard에 Connected 상태 표시
**And** SSE 스트리밍으로 실시간 응답
**And** 라이브러리: @modelcontextprotocol/sdk Streamable HTTP 또는 @nestjs-mcp/server

**Error Handling:**
- 인증 실패 → 401 Unauthorized
- 크레딧 부족 → INSUFFICIENT_CREDITS 에러
- 개념 미존재 → CONCEPT_NOT_FOUND 에러
- 타임아웃 → 30초, 504 Gateway Timeout

### Story 4.2: Elicitation — 에이전트 지식 비교

As a user,
I want 카탈로그에서 Compare 버튼을 누르면 에이전트의 보유 지식과 자동 비교,
So that 에이전트가 뭘 모르는지 한눈에 파악하고 필요한 지식을 구매할 수 있다.

**Acceptance Criteria:**

**Given** 에이전트가 MCP Streamable HTTP로 Cherry에 연결됨
**When** 웹에서 유저가 Compare 버튼 클릭
**Then** Cherry 서버가 에이전트에게 Elicitation 요청 전송:
  - message: "보유 지식 목록을 제출해주세요"
  - schema: { known_topics: [{ topic: string, lastUpdated: string }] }
**And** 에이전트가 로컬에서 보유 지식 수집 → Cherry에 응답
**And** Cherry가 카탈로그와 비교 → upToDate/outdated/gaps 분류
**And** 웹 카탈로그에 태그 표시: ✅ Up-to-date / ⚠️ Outdated / 🔴 Gap

**Error Handling:**
- 에이전트 미연결 → "에이전트가 연결되지 않았습니다" 메시지
- 에이전트 타임아웃 (30초) → 빈 목록으로 처리, 전체 Gap 표시
- 에이전트가 거부 (decline) → "에이전트가 지식 목록 공유를 거부했습니다"
- 토픽 500개 초과 → 최근 500개만 처리

### Story 4.3: Sampling — 3자 대화

As a user,
I want 채팅에서 에이전트에게 지시하면 에이전트가 Cherry에 물어보고 답변,
So that 유저↔에이전트↔Cherry 3자 대화를 통해 필요한 지식을 자연스럽게 구매할 수 있다.

**Acceptance Criteria:**

**Given** 에이전트가 MCP Streamable HTTP로 Cherry에 연결됨
**When** 웹 채팅에서 유저가 메시지 입력 (예: "RAG에 대해 Cherry에게 물어봐")
**Then** Cherry 서버가 에이전트에게 Sampling 요청 전송:
  - messages: [{ role: "user", content: "..." }]
  - systemPrompt: "너는 Cherry KaaS에서 지식을 구매하는 에이전트..."
**And** 에이전트가 자체 LLM으로 처리
**And** 에이전트가 필요하면 Cherry tool 호출 (search_catalog, purchase_concept 등)
**And** 에이전트 응답을 웹 채팅에 표시
**And** 3자 구분: User(사용자) / Agent(에이전트) / Cherry(플랫폼)

**Error Handling:**
- 에이전트 미연결 → "에이전트를 먼저 연결해주세요"
- 에이전트 LLM 에러 → "에이전트 응답 실패"
- 토큰 제한: max_tokens 512

### Story 4.4: Notifications — 실시간 알림

As an agent,
I want Cherry에서 팔로우 중인 개념이 업데이트되면 알림을 받고,
So that 최신 지식을 자동으로 갱신할 수 있다.

**Acceptance Criteria:**

**Given** 에이전트가 MCP로 연결 중이고 개념 X를 팔로우 중
**When** 관리자가 개념 X의 content_md를 수정
**Then** Cherry가 에이전트에게 Notification 전송: knowledge_updated { concept_id, updated_at }
**And** 에이전트가 자동으로 최신 content_md를 가져감

---

## Epic 5: Demo Dashboard

심사위원이 데모에서 쿼리→온체인 해시→Karma 표시를 시각적으로 확인할 수 있다.

### Story 5.1: Query 페이지 — "와!" 순간 (P0)

As a hackathon judge,
I want 에이전트 쿼리 → 구조화된 답변 → 온체인 해시 팝업을 한 화면에서 확인,
So that "이 AI가 검증된 지식을 소비하고 영수증이 블록체인에 남는다"를 체감할 수 있다.

**Acceptance Criteria:**

**Given** apps/web/app/kaas/query/page.tsx가 생성됨
**When** 사용자가 에이전트에게 개념 구매/팔로우를 지시
**Then** 구조화된 답변 표시 (에비던스 노드, 출처, 큐레이터 코멘트, 품질 스코어)
**And** 답변 옆에 온체인 프로비넌스 해시가 실시간으로 팝업
**And** 해시 클릭 시 Status Network 블록 익스플로러 링크로 이동
**And** Karma 티어가 화면에 표시 (에이전트/큐레이터)
**And** 크레딧 차감 표시 (예: 250 → 230)
**And** 사이드바 KAAS 섹션에서 "Query Knowledge" 클릭으로 접근

### Story 5.2: Catalog 페이지

As a hackathon judge,
I want 지식 카탈로그를 시각적으로 탐색,
So that Cherry KaaS에 어떤 지식이 있는지 확인할 수 있다.

**Acceptance Criteria:**

**Given** apps/web/app/kaas/catalog/page.tsx가 생성됨
**When** 페이지 접근
**Then** 개념 목록 카드 표시 (title, category, quality_score, source_count, updated_at)
**And** 검색 입력으로 개념 필터링
**And** 개념 클릭 시 상세 미리보기 (에비던스 카운트, 관련 개념)
**And** 인증 불필요

### Story 5.3: Dashboard 페이지

As a hackathon judge,
I want 크레딧 잔액과 큐레이터 수익을 한눈에 확인,
So that 결제 시스템과 보상 메커니즘이 실제로 작동하는지 볼 수 있다.

**Acceptance Criteria:**

**Given** apps/web/app/kaas/dashboard/page.tsx가 생성됨
**When** 인증된 에이전트가 접근
**Then** 크레딧 잔액 표시
**And** 최근 구매/팔로우 이력 (개념명, 유형, 차감 크레딧, provenance hash)
**And** 큐레이터 수익 요약 (총 적립, 미출금)
**And** 크레딧 충전 버튼 (MetaMask 연동)
**And** 보상 출금 버튼 (gasless 트랜잭션)

### Story 5.4: 사이드바 Agent Shopping 섹션 추가

As a user,
I want 기존 solteti.site 사이드바에서 KaaS 기능에 접근,
So that 별도 URL 없이 기존 사이트 내에서 KaaS를 사용할 수 있다.

**Acceptance Criteria:**

**Given** apps/web/components/cherry/sidebar.tsx 수정
**When** 사이드바 렌더링
**Then** SECTIONS 배열에 AGENT SHOPPING 섹션 추가 (DIGEST 다음, HOT 뱃지 포함)
**And** 하위 항목: Knowledge Catalog (ShoppingBag 아이콘)
**And** Query Knowledge는 별도 페이지가 아닌 플로팅 콘솔로 제공 (카탈로그 구매 버튼 → 콘솔 자동 팝업)
**And** Dashboard는 카탈로그 헤더의 "My Dashboard" 버튼 → 모달로 제공
**And** mobile-sidebar.tsx는 Sidebar 컴포넌트를 재사용하므로 별도 수정 불필요

---

## Epic 6: Curator Rewards

큐레이터가 에이전트 쿼리로 발생한 수익을 확인하고 온체인으로 출금할 수 있다.

### Story 6.1: 큐레이터 보상 계산 및 출금

As a knowledge curator,
I want 에이전트 쿼리로 발생한 수익을 확인하고 온체인으로 출금,
So that 큐레이션 활동에 대한 경제적 보상을 받을 수 있다.

**Acceptance Criteria:**

**Given** 에이전트 쿼리가 실행되어 크레딧이 소비됨
**When** 쿼리에 사용된 에비던스의 큐레이터가 식별됨
**Then** 쿼리 수익의 40%가 기여 큐레이터에게 배분 계산됨
**And** kaas.curator_reward에 curator_id, query_log_id, amount 기록
**And** GET /api/v1/kaas/rewards/balance로 총 적립/미출금 조회 가능
**And** POST /api/v1/kaas/rewards/withdraw로 출금 요청 시 chain-adapter.withdrawReward() 호출
**And** gasless 트랜잭션으로 Status Network에 출금 실행
**And** withdrawal_tx_hash가 kaas.curator_reward에 기록
**And** 블록 익스플로러에서 출금 트랜잭션 검증 가능

---

## Epic 7: Multi-chain Submission

BNB Chain과 NEAR AI 트랙 제출 요건을 충족할 수 있다.

### Story 7.1: BNB Chain (opBNB) 제출 요건 충족

As a hackathon participant,
I want opBNB 테스트넷에 최소 요건을 배포,
So that BNB Chain 트랙($5,000)에 제출할 수 있다.

**Acceptance Criteria:**

**Given** chain-adapter/bnb-adapter.ts가 구현됨
**When** CHAIN_ADAPTER=bnb로 전환
**Then** CherryCredit.sol이 opBNB 테스트넷(Chain ID 5611)에 배포됨
**And** 최소 2건의 성공적 온체인 트랜잭션 (deposit + recordProvenance)
**And** 공개 GitHub + README에 opBNB 배포 정보 포함
**And** 2-4분 데모 영상 촬영
**And** #ConsumerAIonBNB 트윗 게시

### Story 7.2: NEAR AI 제출 요건 충족

As a hackathon participant,
I want NEAR AI Cloud 통합 데모를 준비,
So that NEAR AI 트랙($5,000)에 제출할 수 있다.

**Acceptance Criteria:**

**Given** chain-adapter/near-adapter.ts가 구현됨
**When** NEAR AI Cloud(cloud-api.near.ai) 연동
**Then** TEE 기반 추론 데모 작동 (OpenAI SDK 호환 base_url 교체)
**And** 데모 영상에서 privacy-preserving knowledge consumption 시연
**And** GitHub에 NEAR AI 통합 문서 포함
