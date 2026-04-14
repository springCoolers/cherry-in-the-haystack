---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
status: 'complete'
completedAt: '2026-04-14'
inputDocuments:
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad-output/planning-artifacts/product-brief-cherry-kaas.md'
  - '_bmad-output/planning-artifacts/product-brief-cherry-kaas-distillate.md'
  - '_bmad-output/planning-artifacts/research/technical-buidlhack2026-stack-research.md'
  - 'docs/architecture/index.md'
workflowType: 'architecture'
project_name: 'cherry-in-the-haystack'
user_name: 'Jihan'
date: '2026-04-14'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
39 FRs across 11 capability areas. Core architectural components:
- **API Gateway Layer** — Agent registration, authentication (API Key + JWT + EIP-712), rate limiting, error handling, fallback mode (FR1-3, FR35-36)
- **Knowledge Service** — Catalog browsing, purchase/follow concept acquisition, MCP server integration. Highest complexity component (FR4-12)
- **Credit Engine** — Balance management, deposit via on-chain transaction, per-query deduction with Karma tier discount, domain-specific error codes (FR13-18)
- **Blockchain Adapter** — Async provenance recording, smart contract operations (CherryCredit.sol), multi-chain support via Chain Adapter pattern (FR19-22, FR29-34)
- **Karma Reader** — On-chain Karma balance/tier read from Status Network contracts, tier-based benefits application (FR23-25)
- **Curator Reward Service** — Revenue share calculation (40%), on-chain withdrawal, basic earnings visibility (FR26-28)

**Non-Functional Requirements:**
13 NFRs driving architecture:
- **Async architecture mandatory** — API response before on-chain confirmation (NFR1, NFR13)
- **Demo stability over performance** — 5 consecutive runs without failure (NFR3)
- **Status Network RPC specifics** — linea_estimateGas only, from field mandatory, no caching (NFR9)
- **Chain Adapter interface** — Environment variable swap only, no code changes (NFR10)
- **Manual fallback switch** — DEMO_FALLBACK=true env var for demo resilience (NFR12)
- **Read-only knowledge graph** — KaaS does not modify source Cherry data (NFR11)

**Scale & Complexity:**
- Primary domain: API Backend + Blockchain Integration
- Complexity level: High
- Estimated architectural components: ~8 (API Gateway, Knowledge Service, Credit Engine, Blockchain Adapter ×3, Karma Reader, Curator Reward, MCP Server)
- Constraint: 4-day hackathon, 1 developer, modular monolith

### Technical Constraints & Dependencies

- **Runtime:** Node.js/Express/TypeScript modular monolith
- **Database:** SQLite (MVP) → PostgreSQL (post-hackathon)
- **Blockchain primary:** Status Network (Linea zkEVM stack, gasless, Chain ID 1660990954)
- **Blockchain secondary:** opBNB (Chain ID 5611), NEAR AI (non-EVM, near-sdk-js)
- **MCP SDK:** @modelcontextprotocol/sdk
- **Smart contracts:** Solidity (EVM) + near-sdk-js (NEAR)
- **Existing infrastructure:** Cherry knowledge graph (read-only), AWS hosting
- **Time allocation:** Day 1-3 Status Network exclusive, Day 4 BNB/NEAR checklist only

### Cross-Cutting Concerns Identified

1. **Async provenance recording** — Every query triggers background on-chain recording; API response includes provisional hash before chain confirmation
2. **Chain Adapter abstraction** — Credit deposit, provenance recording, reward withdrawal all require chain-specific implementations behind unified interface
3. **Fallback mode** — DEMO_FALLBACK=true must branch across Knowledge Service (fixed catalog), Credit Engine (fixed balance 250), and API Gateway (bypass auth)
4. **Authentication multiplexing** — Public endpoints (no auth), API Key endpoints (query/subscribe), Wallet signature endpoints (deposit/withdraw) — three auth modes coexisting

## Starter Template Evaluation

### Primary Technology Domain

API Backend + Blockchain Integration, extending existing pnpm monorepo.

### Starter Options Considered

**Option A: 새 프로젝트 생성 (create-t3-app, create-next-app 등)**
- ❌ 불필요 — 이미 모노레포가 존재하고 빌드 인프라(TypeScript, ESLint, Prettier, Vitest)가 세팅됨

**Option B: 기존 모노레포에 KaaS 패키지 추가**
- ✅ 가장 빠르고 자연스러운 접근 — 기존 인프라 재사용

### Selected Approach: 기존 모노레포 확장 (파일 추가만)

**Rationale:** Brownfield 프로젝트. 기존 `apps/web/` (solteti.site)과 `apps/api/`에 KaaS 화면과 엔드포인트를 파일 추가로 확장. 새 앱 생성 없음. 배포 포인트 추가 없음.

**KaaS 추가 구조:**
```
cherry-in-the-haystack/
├── apps/
│   ├── web/                          # 기존 solteti.site — KaaS 화면 추가
│   │   ├── app/kaas/catalog/         # NEW: 카탈로그 페이지
│   │   ├── app/kaas/query/           # NEW: 쿼리 + 온체인 해시 표시
│   │   └── app/kaas/dashboard/       # NEW: 크레딧/큐레이터 대시보드
│   └── api/                          # 기존 API — KaaS 엔드포인트 추가
│       ├── src/routes/v1/kaas/*      # NEW: /api/v1/kaas/* 엔드포인트
│       └── mcp-server.ts             # NEW: MCP 별도 진입점
├── packages/
│   ├── pipeline/                     # 기존
│   ├── kaas-core/                    # NEW: 비즈니스 로직 (Knowledge, Credit, Reward)
│   └── chain-adapter/                # NEW: 블록체인 어댑터 (Status/BNB/NEAR)
├── contracts/                        # NEW: Hardhat + Solidity
```

**기존 코드 수정:** 사이드바에 KaaS 섹션 링크 추가 1건만. 나머지는 전부 파일 추가.

**Architectural Decisions by Existing Monorepo:**
- Language & Runtime: TypeScript 5.9+, Node.js 20+, ESM ("type": "module")
- Package Manager: pnpm 9+ workspaces
- Testing: Vitest 2.0
- Linting: ESLint 9 + TypeScript parser
- Formatting: Prettier 3
- Build: pnpm -r build

**New Packages:**
- `packages/kaas-core/` — 순수 TypeScript, 프레임워크 무관 비즈니스 로직
- `apps/api/src/modules/kaas/chain-adapter/` — ethers.js v6 (EVM) + near-sdk-js (NEAR)
- `contracts/` — Hardhat + Solidity (CherryCredit.sol)

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
1. Database: 기존 PostgreSQL + knex 확장 (SQLite 불필요)
2. Knowledge graph access: 시딩 스냅샷 (그래프 DB 위치 확인 전까지)
3. Wallet: MetaMask only

**Deferred Decisions (Post-MVP):**
- ORM 전환 (knex → Drizzle 등)
- WalletConnect 지원
- 그래프 DB 직접 연결 (위치 확인 후)

### Data Architecture

**Database:** 기존 PostgreSQL (pgvector/pgvector:pg16) + knex 마이그레이션

**신규 테이블 6개 (kaas 스키마):**

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `kaas.concept` | 카탈로그 — 에이전트가 구매하는 지식 상품 | id, title, category, summary, content_md(실제 지식 본문), quality_score, related_concepts(JSONB) |
| `kaas.evidence` | 개념별 출처 + 큐레이터 코멘트 | concept_id(FK), source, summary, curator, curator_tier, comment |
| `kaas.agent` | 에이전트 등록 (멀티에이전트 지원) | api_key, wallet_address, llm_provider, llm_model, llm_api_key, karma_tier, domain_interests, knowledge(JSONB) |
| `kaas.credit_ledger` | 크레딧 충전/차감 이력 | agent_id(FK), amount, type (deposit/consume), tx_hash, chain |
| `kaas.query_log` | 구매/팔로우 히스토리 + 프로비넌스 | agent_id(FK), concept_id, action_type [purchase/follow], credits_consumed, provenance_hash |
| `kaas.curator_reward` | 큐레이터 수익 적립 (40% revenue share) | curator_id, query_log_id(FK), amount, withdrawn, withdrawal_tx_hash |

데이터 흐름: concept/evidence(지식 상품) → agent(구매자) → query_log(구매 기록) → curator_reward(보상)

**Knowledge Graph Access:** 시딩 스냅샷 (JSON/seed SQL) — 그래프 DB(GraphDB) 위치 확인 전까지. 연결 레이어는 인터페이스로 추상화하여 나중에 그래프 DB 연결로 교체 가능.

### Authentication & Security

- **Agent auth:** API Key (kaas.agent 테이블에서 발급/검증)
- **Wallet auth:** MetaMask + EIP-712 서명 (크레딧 충전/출금 시)
- **Smart contract access control:** owner/server만 financial operations 호출 가능
- **DEMO_FALLBACK=true:** 환경변수로 폴백 모드 수동 전환

### API & Communication Patterns

**REST API (웹 ↔ Cherry 서버):**
- 기존 apps/api/에 `/api/v1/kaas/*` 라우트 추가
- 웹 프론트엔드에서 에이전트 등록, 충전, 이력 조회, 카탈로그 관리에 사용
- Error handling: 도메인 특화 3종 (INSUFFICIENT_CREDITS, KARMA_TIER_REQUIRED, CONCEPT_NOT_FOUND) + 표준 HTTP

**MCP Streamable HTTP (에이전트 ↔ Cherry 서버):**
- 전송: HTTP POST + SSE (Server-Sent Events) 스트리밍
- 엔드포인트: `https://cherry-kaas.com/mcp` (단일 URL)
- 인증: Cherry API Key → HTTP Authorization: Bearer 헤더
- 세션: 연결된 에이전트 추적, Dashboard에 연결 상태 표시
- 라이브러리: `@modelcontextprotocol/sdk` Streamable HTTP transport 또는 `@nestjs-mcp/server`

**MCP 양방향 통신:**

| 방향 | 프로토콜 | 용도 |
|------|---------|------|
| 에이전트 → Cherry | Tool Call | search_catalog, get_concept, purchase_concept, follow_concept, compare_knowledge |
| Cherry → 에이전트 | Elicitation | 에이전트에게 보유 지식 목록 요청 (Compare 시) |
| Cherry → 에이전트 | Sampling | 에이전트 LLM에 메시지 전달 (3자 대화 시) |
| Cherry → 에이전트 | Notification | 팔로우 개념 업데이트, 크레딧 부족 경고 |

**Elicitation (Cherry → 에이전트 데이터 요청):**
- Cherry가 에이전트에게 구조화된 데이터를 요청
- 예: "보유 지식 목록을 제출해주세요" + JSON Schema
- 에이전트가 로컬 파일/DB에서 수집 후 응답
- 타임아웃: 30초 (무응답 시 빈 목록으로 처리)
- 최대 토픽 수: 500개

**Sampling (Cherry → 에이전트 LLM 호출):**
- Cherry가 에이전트의 LLM에 메시지를 전달
- 에이전트 쪽에서 자체 LLM으로 처리 후 응답
- 인증: 기존 MCP 세션의 Bearer token으로 식별
- 토큰 제한: max_tokens 512
- 에러 시: Cherry가 fallback 메시지 반환 ("에이전트 응답 없음")

**Async provenance:** API 응답 즉시 반환 → 백그라운드 온체인 기록

```
┌─────────────────┐          HTTP POST / SSE          ┌─────────────────┐
│   로컬 에이전트   │ ◄──────────────────────────────► │  Cherry KaaS    │
│  (MCP Client)    │     Streamable HTTP Transport     │  (MCP Server)   │
│                  │                                    │                  │
│  - Claude Desktop│   → tool call (purchase, compare) │  - NestJS API    │
│  - Claude Code   │   ← tool response (content_md)   │  - PostgreSQL    │
│  - Custom Agent  │   ← elicitation (지식목록 요청)    │  - Blockchain    │
│                  │   → elicitation response           │                  │
│                  │   ← sampling (LLM 질문)            │                  │
│                  │   → sampling response              │                  │
└─────────────────┘                                    └─────────────────┘
        ↕                                                      ↕
   로컬 파일시스템                                          REST API
   (지식 저장)                                         (웹 프론트엔드)
```

### Frontend Architecture

- **기존 apps/web/ (Next.js) 확장** — app/kaas/* 라우트 추가
- **Wallet:** wagmi + viem, MetaMask only
- **State:** React hooks (useState/useEffect) — 별도 상태 관리 라이브러리 불필요 (페이지 3개)
- **온체인 해시 표시:** 쿼리 응답 시 provenance hash + explorer link 실시간 렌더링

### Infrastructure & Deployment

- **기존 AWS 인프라 그대로** — 추가 배포 불필요
- **Docker:** 기존 docker-compose.yml에 의존 (PostgreSQL, GraphDB, Redis)
- **Smart contract:** Hardhat으로 Status Network 테스트넷 배포, Day 1에 검증
- **환경변수:** CHAIN_ADAPTER=status|bnb|near, DEMO_FALLBACK=true/false

### Decision Impact Analysis

**Implementation Sequence:**
1. contracts/ — CherryCredit.sol 배포 + gasless 검증 (Day 1)
2. apps/api/src/modules/kaas/chain-adapter/ — Status Network 어댑터 구현 (Day 1)
3. DB 마이그레이션 — kaas_* 4개 테이블 추가 (Day 1)
4. packages/kaas-core/ — Knowledge, Credit, Reward 서비스 (Day 1-2)
5. apps/api/ — /api/v1/kaas/* 엔드포인트 (Day 2)
6. apps/api/mcp-server.ts — MCP 서버 (Day 2)
7. apps/web/app/kaas/query/ — Query 페이지 (Day 2 후반) ← "와!" 순간, 최우선
8. apps/web/app/kaas/catalog/ + dashboard/ (Day 3)
9. 데모 영상 + BNB/NEAR 최소 요건 (Day 4)

**폴백:** Query 페이지만 작동하면 데모 가능. Catalog/Dashboard 미완성 허용.

**Cross-Component Dependencies:**
- chain-adapter → kaas-core (provenance, credit deposit/withdrawal)
- kaas-core → 기존 PostgreSQL (agent, credit, query, reward 테이블)
- kaas-core → knowledge seed data (시딩 스냅샷)
- apps/api routes → kaas-core (비즈니스 로직)
- apps/web/kaas/* → apps/api/v1/kaas/* (REST 호출)
- mcp-server.ts → kaas-core (동일 서비스 레이어)

## Implementation Patterns & Consistency Rules

### 기존 코드베이스 컨벤션 (따라야 함)

기존 apps/api/는 **NestJS 10** 기반 (PRD의 Express 결정을 NestJS로 수정):
- Controller/Service/Module 패턴
- Zod validation pipe
- Swagger 데코레이터
- kebab-case 파일명 (`article-ingestion.service.ts`)
- PascalCase 클래스명 (`ArticleIngestionService`)
- camelCase 함수/변수명

### Naming Patterns

**Database (기존 PostgreSQL 컨벤션 유지):**
- 테이블: snake_case, `kaas_` prefix (`kaas.agent`, `kaas.credit_ledger`)
- 컬럼: snake_case (`wallet_address`, `api_key`, `created_at`)
- FK: `{table}_id` (`agent_id`, `curator_id`)
- Index: `idx_{table}_{column}` (`idx_kaas.agent_api_key`)

**API Endpoints:**
- REST: `/api/v1/kaas/{resource}` (복수형: `/agents`, `/credits`, `/queries`)
- Route params: `:id` (NestJS 스타일)
- Query params: camelCase (`?conceptId=...`)

**Code (NestJS 패턴):**
- 파일: kebab-case (`kaas-query.service.ts`, `kaas-credit.controller.ts`)
- 클래스: PascalCase (`KaasQueryService`, `KaasCreditController`)
- 함수/변수: camelCase (`executeQuery`, `creditBalance`)
- 상수: SCREAMING_SNAKE (`CHAIN_ADAPTER`, `DEMO_FALLBACK`)

**NestJS 모듈 구조:**
```
apps/api/src/modules/kaas/
├── kaas.module.ts
├── kaas-agent.controller.ts      # /agents (등록, 프로필)
├── kaas-query.controller.ts      # /queries (쿼리, 카탈로그, 갭 분석)
├── kaas-credit.controller.ts     # /credits (잔액, 충전)
├── kaas-reward.controller.ts     # /rewards (출금, 조회)
├── kaas-query.service.ts
├── kaas-credit.service.ts
├── kaas-reward.service.ts
├── kaas-provenance.service.ts
├── input-dto/
│   ├── query.dto.ts
│   ├── register.dto.ts
│   └── deposit.dto.ts
└── entity/
```
폴백: 시간 없으면 kaas.controller.ts 하나로 시작 → 나중에 분리. 동작은 동일.

### Format Patterns

**API Response:**
```json
{ "data": { ... }, "meta": { "creditsConsumed": 20, "provenance": { ... } } }
```
에러:
```json
{ "statusCode": 400, "code": "INSUFFICIENT_CREDITS", "message": "...", "details": { ... } }
```

**JSON 필드:** camelCase (API 응답) — DB는 snake_case이므로 서비스 레이어에서 변환

**Date:** ISO 8601 (`2026-04-14T00:00:00Z`)

### Process Patterns

**비동기 프로비넌스:**
1. 쿼리 실행 + provisional hash 생성
2. API 응답 즉시 반환 (provisional hash 포함)
3. EventEmitter로 `provenance.record` 이벤트 발행
4. 리스너가 백그라운드에서 온체인 기록
5. 실패 시 3회 재시도 후 로그

**폴백 모드:**
```typescript
if (process.env.DEMO_FALLBACK === 'true') {
  return SEED_DATA;
}
```

**Chain Adapter 인터페이스:**
```typescript
interface IChainAdapter {
  recordProvenance(hash: string): Promise<TxResult>;
  depositCredit(agent: string, amount: number): Promise<TxResult>;
  withdrawReward(curator: string, amount: number): Promise<TxResult>;
  getKarmaTier(address: string): Promise<KarmaTier>;
}
```

### Enforcement Guidelines

**All AI Agents MUST:**
- NestJS Controller/Service/Module 패턴 사용 (Express 직접 사용 금지)
- Zod DTO로 입력 검증
- `kaas_` prefix로 새 DB 테이블 생성
- chain-adapter 인터페이스를 통해서만 블록체인 호출
- DEMO_FALLBACK 분기를 모든 외부 의존성 호출에 포함

## Project Structure & Boundaries

### Complete Project Directory Structure (KaaS 변경사항)

```
cherry-in-the-haystack/
├── apps/
│   ├── web/                                    # 기존 solteti.site
│   │   ├── components/cherry/
│   │   │   ├── sidebar.tsx                     # MODIFY: SECTIONS에 KaaS 섹션 추가
│   │   │   └── mobile-sidebar.tsx              # MODIFY: 동일 (모바일 사이드바 별도 시)
│   │   └── app/kaas/
│   │       ├── layout.tsx                      # NEW: KaaS 섹션 레이아웃
│   │       ├── catalog/
│   │       │   └── page.tsx                    # NEW: 카탈로그 브라우징 (FR4-7)
│   │       ├── query/
│   │       │   └── page.tsx                    # NEW: 쿼리 + 온체인 해시 표시 (FR8-10, FR19-22) ← P0
│   │       └── dashboard/
│   │           └── page.tsx                    # NEW: 크레딧 잔액 + 큐레이터 보상 (FR13, FR28)
│   │
│   └── api/                                    # 기존 NestJS
│       └── src/
│           ├── app.module.ts                   # MODIFY: KaasModule import 추가
│           ├── modules/kaas/
│           │   ├── kaas.module.ts              # NEW
│           │   ├── kaas-agent.controller.ts    # NEW: POST /agents/register (FR1)
│           │   ├── kaas-query.controller.ts    # NEW: GET /catalog, POST /query (FR4-10)
│           │   ├── kaas-credit.controller.ts   # NEW: GET /credits/balance, POST /credits/deposit (FR13-14)
│           │   ├── kaas-reward.controller.ts   # NEW: POST /rewards/withdraw (FR27)
│           │   ├── kaas-query.service.ts       # NEW
│           │   ├── kaas-credit.service.ts      # NEW
│           │   ├── kaas-reward.service.ts      # NEW
│           │   ├── kaas-provenance.service.ts  # NEW: 비동기 온체인 프로비넌스 기록
│           │   ├── kaas-knowledge.service.ts   # NEW: 시딩 스냅샷 → 카탈로그/쿼리 응답
│           │   ├── input-dto/
│           │   │   ├── register-agent.dto.ts   # NEW
│           │   │   ├── query-knowledge.dto.ts  # NEW
│           │   │   └── deposit-credit.dto.ts   # NEW
│           │   └── entity/
│           │       ├── kaas-agent.entity.ts            # NEW
│           │       ├── kaas-credit-ledger.entity.ts    # NEW
│           │       ├── kaas-query-log.entity.ts        # NEW
│           │       └── kaas-curator-reward.entity.ts   # NEW
│           │
│           └── mcp-server.ts                   # NEW: MCP 별도 진입점 (FR11-12)
│
├── packages/
│   ├── chain-adapter/                          # NEW
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── interface.ts                    # IChainAdapter 인터페이스
│   │   │   ├── status-adapter.ts               # Status Network (Primary)
│   │   │   ├── bnb-adapter.ts                  # opBNB (Should-have)
│   │   │   ├── near-adapter.ts                 # NEAR (Should-have)
│   │   │   └── mock-adapter.ts                 # DEMO_FALLBACK용
│   │   └── tsconfig.json
│   │
│   └── kaas-core/                              # NEW
│       ├── package.json
│       ├── src/
│       │   ├── index.ts
│       │   ├── knowledge/
│       │   │   ├── knowledge.repository.ts     # 시딩 데이터 읽기 인터페이스
│       │   │   └── seed-data.json              # 데모용 개념/에비던스 스냅샷
│       │   ├── credit/
│       │   │   └── credit.calculator.ts        # Karma 할인, purchase/follow 가격
│       │   └── provenance/
│       │       └── hash.generator.ts           # 프로비넌스 해시 생성
│       └── tsconfig.json
│
├── contracts/                                  # NEW
│   ├── package.json
│   ├── hardhat.config.ts
│   ├── contracts/
│   │   └── CherryCredit.sol
│   ├── scripts/
│   │   └── deploy.ts
│   ├── test/
│   │   └── CherryCredit.test.ts
│   └── .env.example
│
└── knex/migrations/
    └── 20260413_create_kaas_tables.ts
```

### 기존 코드 수정 목록 (총 3건)

| File | Change |
|------|--------|
| `apps/web/components/cherry/sidebar.tsx` | SECTIONS 배열에 KAAS 섹션 추가 (Knowledge Catalog, Query Knowledge, Dashboard — 기존 DIGEST/LEARNING과 동일 패턴, 별도 /kaas 인덱스 페이지 불필요) |
| `apps/web/components/cherry/mobile-sidebar.tsx` | 동일 (모바일 사이드바 별도 시) |
| `apps/api/src/app.module.ts` | KaasModule import 추가 |

나머지는 전부 신규 파일.

### Architectural Boundaries

**API Boundaries:**
- Public: `GET /api/v1/kaas/catalog/*`, `POST /api/v1/kaas/catalog/compare` (인증 없음)
- Auth (API Key): `POST /api/v1/kaas/queries`, `GET /api/v1/kaas/credits/balance`
- Auth (API Key + Wallet): `POST /api/v1/kaas/credits/deposit`, `POST /api/v1/kaas/rewards/withdraw`
- MCP: Streamable HTTP 엔드포인트 (`/mcp`), Bearer token 인증, 세션 관리

**Package Dependencies:**
```
apps/api (NestJS) → kaas module → chain-adapter/
apps/api/mcp (Streamable HTTP) → kaas module (동일 서비스 레이어)
apps/web (Next.js) → apps/api (REST API) + WebSocket (실시간 이벤트)
에이전트 (MCP Client) → apps/api/mcp (Streamable HTTP)
```

**Data Boundaries:**
- `kaas-core/knowledge/` → seed-data.json (그래프 DB 연결 전까지)
- `kaas-core` → PostgreSQL `kaas_*` 테이블 (knex)
- `chain-adapter` → 블록체인 RPC (IChainAdapter 뒤)

### FR to Structure Mapping

| FR | File |
|----|------|
| FR1 (등록) | kaas-agent.controller.ts |
| FR4-7 (카탈로그) | kaas-query.controller.ts + kaas-knowledge.service.ts |
| FR8-10 (쿼리) | kaas-query.controller.ts + kaas-query.service.ts |
| FR11-12 (MCP) | mcp-server.ts |
| FR13-18 (크레딧) | kaas-credit.controller.ts + kaas-credit.service.ts |
| FR19-22 (프로비넌스) | kaas-provenance.service.ts + chain-adapter |
| FR23-25 (Karma) | chain-adapter/status-adapter.ts |
| FR26-28 (큐레이터) | kaas-reward.controller.ts + kaas-reward.service.ts |
| FR29-31 (컨트랙트) | contracts/CherryCredit.sol |
| FR32-34 (멀티체인) | chain-adapter/bnb-adapter.ts + near-adapter.ts |
| FR35-36 (에러/폴백) | 모든 컨트롤러 + mock-adapter.ts |
| FR37-38 (갭 분석) | kaas-query.controller.ts + kaas-knowledge.service.ts |
| FR39 (MCP 갭 분석) | mcp-server.ts (compare_knowledge tool) |

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:** NestJS 10 + knex + chain-adapter + kaas-core — 호환 문제 없음. TypeScript 5.9 ESM 전체 일관. wagmi + viem + MetaMask, Hardhat + ethers.js v6 충돌 없음.

**Pattern Consistency:** kebab-case 파일명, PascalCase 클래스, camelCase 변수 전체 일관. NestJS Controller/Service/Module 기존 코드와 동일. `kaas_` prefix DB 테이블 네임스페이스 충돌 없음.

**Structure Alignment:** 기존 모노레포 apps/packages 구조 그대로 확장. 기존 코드 수정 3건만.

### Requirements Coverage ✅

모든 FR1-39 + NFR1-13 아키텍처 커버리지 검증 완료. 누락 없음.

### Gap Resolutions

**Gap 1 — seed-data.json 구조 (해결):**
```json
{
  "concepts": [
    { "id": "rag", "title": "Retrieval-Augmented Generation", "category": "Basics", "summary": "...", "quality_score": 4.8, "source_count": 12, "updated_at": "2026-02-20" }
  ],
  "evidence": [
    { "id": "rag-ev-001", "concept_id": "rag", "source": "Chip Huyen — AI Engineering", "summary": "..." }
  ]
}
```
RAG, Chain-of-Thought, Embeddings 3개 개념으로 시작.

**Gap 2 — MCP 서버 실행 방식 (해결):**
별도 프로세스. `"start:mcp": "ts-node src/mcp-server.ts"` — NestJS와 분리하여 MCP 연결 끊김이 전체 앱에 영향 주지 않도록.

### Architecture Readiness Assessment

**Overall Status: READY FOR IMPLEMENTATION**
**Confidence Level: High**

**Strengths:** 기존 인프라 100% 재사용, 코드 수정 최소 3건, Chain Adapter 멀티체인 추상화, DEMO_FALLBACK 데모 안정성.

**Implementation Priority:**
1. Day 1: contracts/ 배포 + chain-adapter/status + DB 마이그레이션
2. Day 2: NestJS kaas 모듈 + MCP 서버 + Query 페이지
3. Day 3: Catalog + Dashboard 페이지
4. Day 4: 데모 영상 + BNB/NEAR
