---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments: ['docs/Buidlhack 340f199edf7c80a48949c6ce31b1f4eb.md']
workflowType: 'research'
lastStep: 1
research_type: 'technical'
research_topic: 'BuidlHack2026 Sponsor Tech Stacks for Cherry KaaS MVP'
research_goals: 'Evaluate BNB Chain, Status Network, and NEAR AI tech stacks for implementing Cherry Knowledge-as-a-Service MVP — subscription streams, query API, credit system, curator rewards with on-chain transparency'
user_name: 'Jihan'
date: '2026-04-14'
web_research_enabled: true
source_verification: true
---

# Technical Research: BuidlHack2026 Sponsor Tech Stacks for Cherry KaaS MVP

**Date:** 2026-04-14
**Author:** Jihan
**Research Type:** Technical

---

## Research Overview

This technical research evaluates three BuidlHack2026 sponsor tech stacks — **BNB Chain (opBNB/Greenfield)**, **Status Network (가스리스 L2/Karma/RLN)**, and **NEAR AI (TEE/OpenAI 호환)** — for implementing Cherry Knowledge-as-a-Service MVP. The research covers network configuration, smart contract patterns, API/MCP integration, and a 4-day implementation plan for multi-track hackathon submission.

**핵심 발견:** Status Network이 Cherry KaaS에 가장 자연스럽게 매칭 (가스리스 에이전트 거래 + Karma 큐레이터 평판). Chain Adapter 패턴으로 3개 트랙 동시 제출 가능하며, MCP 서버 구현이 데모의 킬러 포인트. 기존 AWS 인프라 + 테스트넷으로 추가 비용 $0.

See Executive Summary below for strategic recommendations and implementation roadmap.

---

## Technical Research Scope Confirmation

**Research Topic:** BuidlHack2026 Sponsor Tech Stacks for Cherry KaaS MVP
**Research Goals:** Evaluate BNB Chain, Status Network, and NEAR AI for implementing Cherry KaaS — multi-track submission strategy

**Target Tracks:**
1. **BNB Chain** ($5K) — Consumer AI + Agent workflows on opBNB/BSC
2. **Status Network** ($5K) — Gasless L2 + Karma reputation + RLN privacy for agents
3. **NEAR AI** ($5K) — TEE-based verifiable private AI + OpenAI SDK compatible

**Cherry KaaS MVP Components to Map:**
- Agent Registry & Catalog API (#29, #30)
- Query Mode + Subscription Stream (#32, #33, #20-22)
- Credit System (#34)
- Curator Rewards with on-chain transparency (#27)
- SLA Lite (#28)

**Technical Research Scope:**
- Architecture Analysis — each chain's design patterns and how Cherry maps onto them
- Implementation Approaches — SDKs, smart contracts, deployment patterns
- Technology Stack — languages, frameworks, tools per sponsor
- Integration Patterns — MCP/A2A protocol compatibility, API design
- Performance Considerations — gas costs, latency, throughput per chain

**Scope Confirmed:** 2026-04-14

---

## Technology Stack Analysis — 3개 트랙별 상세

---

### Track 1: BNB Chain (opBNB + BSC + Greenfield)

**아키텍처:**
- **opBNB** — Optimism OP Stack (Bedrock) 기반 L2, BSC에 결산
- **BSC (BNB Smart Chain)** — EVM 호환 L1
- **BNB Greenfield** — 탈중앙 스토리지, S3 호환 API

**성능 스펙:**

| 메트릭 | opBNB | BSC |
|--------|-------|-----|
| TPS | 10,000 (200M gas/s) | ~160 |
| 블록 타임 | ~1초 | ~3초 |
| 가스비 | <$0.001/tx | ~$0.03/tx |
| 목표 가스비 | $0.0005/tx | - |

**네트워크 설정 (테스트넷):**

| 항목 | 값 |
|------|-----|
| Network Name | opBNB Testnet |
| Chain ID | `5611` |
| Gas Token | tBNB |
| RPC | `https://opbnb-testnet-rpc.bnbchain.org/` |
| Public RPC | `https://opbnb-testnet.publicnode.com` |
| Block Explorer | `https://testnet.opbnbscan.com` |
| Bridge | `https://opbnb-testnet-bridge.bnbchain.org` |
| Faucet | [BSC Faucet](https://www.bnbchain.org/en/testnet-faucet) |

**개발 도구:**
- **언어:** Solidity (EVM 호환)
- **프레임워크:** Hardhat, Foundry, Remix
- **SDK:** ethers.js v6, viem, Web3.js
- **Greenfield SDK:** Go SDK, JavaScript SDK ([API Docs](https://docs.bnbchain.org/bnb-greenfield/for-developers/apis-and-sdks/))
- **Greenfield SP API:** REST API ([GitHub](https://github.com/bnb-chain/greenfield))

**Greenfield 스토리지:**
- Amazon S3 호환 API — 기존 Web2 스토리지와 동일한 인터페이스
- 데이터 마켓플레이스 기능 내장 — 데이터 자산 생성/리스팅/거래/판매
- [Greenfield Data Marketplace Contracts](https://github.com/bnb-chain/greenfield-data-marketplace-contracts) 오픈소스
- MindPress 데이터 마켓플레이스 데모 앱

**Cherry KaaS MVP 매핑:**

| Cherry 컴포넌트 | BNB Chain 구현 |
|----------------|---------------|
| 크레딧 시스템 (#34) | opBNB 스마트 컨트랙트 — ERC-20 크레딧 토큰, 충전/소비 로직 |
| 큐레이터 보상 (#27) | opBNB 컨트랙트 — 기여 비율 기록, 출금 시 BSC 전송 |
| Provenance 기록 | opBNB에 거래 해시 기록 (<$0.001/건) |
| 지식 저장소 | Greenfield에 에비던스/컨셉 데이터 저장 (S3 API) |
| 카탈로그 API (#30) | 중앙 서버 + Greenfield 메타데이터 읽기 |
| 에이전트 거래 | Consumer AI 에이전트가 Cherry API 호출 → 온체인 정산 |

**해커톤 요구사항 체크:**
- ✅ opBNB/BSC 메인넷 또는 테스트넷 배포
- ✅ 최소 2건 성공적 온체인 트랜잭션
- ✅ 작동하는 데모 (웹앱/봇/에이전트)
- ✅ 2-4분 데모 영상
- ✅ GitHub 공개 레포

_Source: [opBNB Docs](https://docs.bnbchain.org/bnb-opbnb/core-concepts/gas-and-fees/), [opBNB Metrics](https://docs.bnbchain.org/bnb-opbnb/core-concepts/opbnb-metrics/), [Greenfield](https://greenfield.bnbchain.org/en), [Greenfield Marketplace](https://github.com/bnb-chain/greenfield-data-marketplace-frontend)_

---

### Track 2: Status Network (가스리스 L2 + Karma + RLN)

**아키텍처:**
- **Linea zkEVM 스택** 기반 Ethereum L2
- **가스리스 실행** — 프로토콜 레벨에서 가스 제거 (paymaster/relayer 없음)
- **Karma** — 비양도성(soulbound) 평판 토큰, 스테이킹/브릿지/LP/앱 사용으로 획득
- **RLN (Rate Limiting Nullifier)** — ZK 기반 스팸 방지, 가스비 대체

**핵심 기술 특성:**

| 메트릭 | Status Network |
|--------|---------------|
| 가스비 | **$0 (완전 무료)** |
| 스팸 방지 | RLN (ZK proof 기반 rate limiting) |
| 평판 시스템 | Karma 티어 → 일일 무료 트랜잭션 할당량 (`txPerEpoch`) |
| 프라이버시 | 지갑 프리펀딩 불필요 → 가스 행동 기반 추적 불가 |
| 스택 | Linea zkEVM (EVM 호환) |

**네트워크 설정 (테스트넷):**

| 항목 | 값 |
|------|-----|
| Network Name | Status Network Testnet |
| Chain ID | `1660990954` (0x6300b5ea) |
| Gas Token | ETH (가스리스이므로 실제 소비 안 됨) |
| RPC | `https://public.sepolia.rpc.status.network` |
| WebSocket RPC | 비공개 — Telegram(@statusl2)에서 요청 |
| Block Explorer | `https://sepoliascan.status.network` |
| Bridge | `https://bridge.status.network` |

**Karma 컨트랙트 주소 (테스트넷):**

| 컨트랙트 | 주소 |
|----------|------|
| **Karma** | `0x7ec5Dc75D09fAbcD55e76077AFa5d4b77D112fde` |
| **KarmaTiers** | `0xc7fCD786a161f42bDaF66E18a67C767C23cFd30C` |
| **KarmaNFT** | `0xf78d58742840C0ee00b17EE062855392d10a0305` |
| **StakeManager** | `0x5cDf1646E4c1D21eE94DED1DA8da3Ca450dc96D1` |
| **L2 Faucet** | `0x06338B70F1eAbc60d7A82C083e605C07F78bb878` |
| **Multicall3** | `0xcA11bde05977b3631167028862bE2a173976CA11` |

**Karma 온체인 읽기 패턴:**
```solidity
// 1. Karma 잔액 조회
uint256 balance = IKarma(KARMA_ADDR).balanceOf(agent);

// 2. 티어 조회
uint8 tierId = IKarmaTiers(TIERS_ADDR).getTierIdByKarmaBalance(balance);
Tier memory tier = IKarmaTiers(TIERS_ADDR).getTierById(tierId);
// tier.name, tier.txPerEpoch, tier.minKarma, tier.maxKarma
```

**가스리스 트랜잭션 핵심 — `linea_estimateGas`:**
```javascript
// eth_estimateGas 대신 linea_estimateGas 사용 (필수)
const { gasLimit, baseFeePerGas, priorityFeePerGas } =
  await provider.send('linea_estimateGas', [{
    from: agentAddress,  // from 필수!
    to: cherryContractAddr,
    data: encodedCalldata
  }]);

// baseFeePerGas === "0x0" && priorityFeePerGas === "0x0" → 가스리스!
const maxFeePerGas = BigInt(baseFeePerGas) + BigInt(priorityFeePerGas);
```

**주의사항:**
- `eth_gasPrice`, `eth_feeHistory` 사용 금지 → `linea_estimateGas`만 사용
- 캐싱 금지 — 매번 재추정
- `from` 필드 필수 (Karma/quota 로직 적용을 위해)

**개발 도구:**
- **언어:** Solidity (EVM 호환)
- **프레임워크:** Scaffold-ETH 2 Extension ([GitHub](https://github.com/status-im/status-network-scaffold-extension)), Hardhat, Foundry, Remix
- **배포:** `--network statusSepolia`, 검증은 Blockscout
- **Monorepo:** [status-network-monorepo](https://github.com/status-im/status-network-monorepo)
- **멘토링:** Discord @yjkellyjoo ([BuidlHack Discord](https://discord.gg/Z5enQnsaau))

**Cherry KaaS MVP 매핑:**

| Cherry 컴포넌트 | Status Network 구현 |
|----------------|-------------------|
| 에이전트 쿼리 (#32) | **가스리스 트랜잭션으로 에이전트가 무료로 쿼리** — 핵심 차별점! |
| Karma = 큐레이터 평판 (#27) | Karma 티어를 큐레이터 신뢰도로 활용, 높은 Karma = 더 많은 거래 허용 |
| 에이전트 레지스트리 (#29) | Karma 기반 시빌 저항 — 봇 스팸 방지 |
| 프라이버시 (#22) | RLN으로 에이전트 쿼리 내용 프라이버시 보장 |
| SLA (#28) | 가스리스 → SLA 위반 시 크레딧 환불 비용 $0 |
| 크레딧 시스템 (#34) | 커스텀 ERC-20 + Karma 티어별 할인 |

**해커톤 요구사항 체크:**
- ✅ Status Network Hoodi 테스트넷 가스리스 배포
- ✅ 5건+ 가스리스 트랜잭션
- ✅ Karma 티어 온체인 읽기 + 앱에서 표시/활용
- ✅ 2분 데모 영상
- ✅ GitHub 오픈소스 + README

**평가 가중치 매핑:**
- 프라이버시 & 에이전트 활용 (30%) → 에이전트 지식 거래 + RLN 프라이버시
- Karma 활용도 (25%) → 큐레이터 평판 + 시빌 저항 + 티어별 접근
- 가스리스 UX (20%) → 에이전트가 가스 관리 없이 지식 거래
- 완성도 (15%) → 작동하는 데모
- 재미 & 매력 (10%) → "검증된 지식의 에이전트 마켓" 컨셉

_Source: [Status Network](https://status.network/), [Status Network Docs](https://docs.status.network/), [Scaffold Extension](https://github.com/status-im/status-network-scaffold-extension), [Status Blog](https://our.status.im/status-network-in-2025-building-a-gasless-and-private-layer-2/)_

---

### Track 3: NEAR AI (TEE 기반 검증 가능 프라이빗 AI)

**아키텍처:**
- **NEAR AI Cloud** — Intel TDX 기반 TEE (Trusted Execution Environment)
- **NVIDIA GPU** — TEE 보호 하에서 AI 추론
- **OpenAI SDK 호환** — 기존 OpenAI 코드 그대로 사용 가능
- **NEAR L1 블록체인** — 온체인 어카운트빌리티

**핵심 기술 특성:**

| 메트릭 | NEAR AI Cloud |
|--------|--------------|
| 프라이버시 | 하드웨어 레벨 격리 (Intel TDX CVM) |
| 검증 가능성 | 암호학적 attestation — 어떤 모델이 처리했는지 증명 |
| API 호환성 | OpenAI SDK 드롭인 교체 |
| 성능 | 최소 레이턴시 오버헤드 |
| 사인 | 요청 + 추론 결과 암호학적 서명 |

**API 엔드포인트:**

| 항목 | 값 |
|------|-----|
| Gateway | `https://cloud-api.near.ai` |
| Direct Completions | `https://{model-slug}.completions.near.ai` |
| Endpoints 목록 | `https://completions.near.ai/endpoints` |
| 인증 | Bearer Token (`Authorization: Bearer YOUR_API_KEY`) |

**사용 가능 모델 (예시):**
- `qwen35-122b.completions.near.ai`
- `qwen3-30b.completions.near.ai`
- `gpt-oss-120b.completions.near.ai`

**OpenAI SDK 드롭인 교체:**
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://cloud-api.near.ai/v1",
    api_key="YOUR_NEAR_AI_KEY"
)

response = client.chat.completions.create(
    model="qwen35-122b",
    messages=[{"role": "user", "content": "RAG chunk size 최적화 방법?"}]
)
# TLS 종료가 TEE 내부에서 발생 → 프롬프트가 TEE 밖에서 평문 노출 없음
```

**개발 도구:**
- **SDK:** OpenAI Python/JS SDK 그대로 사용 (base_url만 변경)
- **Private-ML-SDK:** 보안 모델 실행, attestation 생성, 암호학적 서명
- **문서:** [docs.near.ai](https://docs.near.ai/)
- **Quickstart:** [docs.near.ai/cloud/quickstart](https://docs.near.ai/cloud/quickstart/)
- **TEE 검증:** [Attestation Verification](https://docs.near.ai/cloud/verification)
- **지원:** Telegram [t.me/nearaialpha](https://t.me/nearaialpha)

**Cherry KaaS MVP 매핑:**

| Cherry 컴포넌트 | NEAR AI 구현 |
|----------------|-------------|
| 쿼리 모드 (#32) | 에이전트 쿼리 → NEAR AI TEE에서 처리 → 지식 프라이버시 보장 |
| Writer Agent (FR-4.2) | TEE 내에서 합성 → 입력 에비던스가 외부에 노출되지 않음 |
| Provenance (#22) | TEE attestation = "이 지식이 이 모델에 의해 이 시점에 처리됨" 암호학적 증명 |
| 에이전트 인증 | NEAR 계정 시스템으로 에이전트 인증 |
| 구독 스트림 (#33) | 서버 사이드 + NEAR 온체인 기록 |

**해커톤 요구사항 체크:**
- ✅ TEE 기반 프라이버시 활용
- ✅ 실제 문제 해결 (지식 품질 + 프라이버시)
- ✅ Attestation 활용
- ✅ 데모 + 설명

**평가 가중치 매핑:**
- Innovation (30%) → TEE로 "검증 가능한 지식 거래" = 기존에 없던 컨셉
- Impact (25%) → 에이전트 환각 문제 + 지식 프라이버시 = 실제 문제
- Technical Excellence (20%) → OpenAI SDK 호환 + attestation 통합
- Privacy Design (15%) → 쿼리 내용이 TEE 밖으로 유출 안 됨
- Presentation (10%) → 데모

_Source: [NEAR AI Docs](https://docs.near.ai/), [NEAR AI Private Inference](https://docs.near.ai/cloud/private-inference/), [NEAR AI Cloud](https://docs.near.ai/cloud/guides/openai-compatibility)_

---

## 3개 트랙 비교 — Cherry KaaS MVP 적합성

| 기준 | BNB Chain | Status Network | NEAR AI |
|------|-----------|---------------|---------|
| **Cherry 핵심 매칭도** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **구현 난이도** | 중간 | 쉬움 (가스리스) | 중간 |
| **차별화 스토리** | Consumer AI 에이전트 | 가스리스 에이전트 + Karma 평판 | 검증 가능한 프라이빗 지식 |
| **온체인 비용** | <$0.001/tx | $0/tx | NEAR tx 비용 |
| **개발 도구 성숙도** | 높음 (EVM 생태계) | 중간 (신규 네트워크) | 중간 (OpenAI 호환) |
| **상금** | $5K | $5K | $5K |
| **추가 스토리지** | ✅ Greenfield | ❌ | ❌ |
| **프라이버시** | ❌ | ✅ RLN | ✅ TEE |
| **평판 시스템** | ❌ | ✅ Karma | ❌ |

### 추천 멀티 트랙 전략

**핵심 아키텍처 (공통):**
```
Cherry 중앙 서버 (API + 지식 그래프)
    ├── /catalog (무료)
    ├── /query (과금)
    ├── /subscribe (구독)
    └── /curator/rewards (보상 조회)
```

**Track별 온체인 레이어:**
- **BNB Chain:** opBNB에 크레딧 컨트랙트 + Greenfield에 지식 저장
- **Status Network:** 가스리스 에이전트 거래 + Karma 큐레이터 평판
- **NEAR AI:** TEE에서 지식 쿼리 처리 + attestation 증명

**복수 트랙 제출 시 코드 재사용:**
- Cherry 중앙 서버 = 동일 (Node.js/Python API)
- 온체인 레이어만 트랙별로 교체 (Solidity 컨트랙트 / NEAR 컨트랙트)
- 프론트엔드 데모 = 동일 (지갑 연결만 다름)

---

## Integration Patterns Analysis

### Cherry KaaS API 설계 패턴

**REST API (핵심):**
```
GET  /catalog/concepts              — 컨셉 목록 (무료)
GET  /catalog/concepts/{id}/preview — 미리보기 (무료)
GET  /catalog/concepts/{id}/stats   — 통계 (무료)
POST /query                         — 지식 쿼리 (과금)
POST /subscribe                     — 구독 등록 (과금)
GET  /agent/balance                 — 크레딧 잔액
GET  /agent/history                 — 거래 이력
POST /curator/withdraw              — 큐레이터 보상 출금
```

**WebSocket (구독 스트림):**
```
WS /stream
  → subscribe: { concepts: ["RAG"], events: ["evidence_added"] }
  ← event: { type, concept_id, summary, cost_deducted, balance }
```

**Webhook (대안):**
```
POST /subscribe
  { concepts: [...], delivery: "webhook", webhook_url: "..." }
→ Cherry가 이벤트 발생 시 에이전트 URL로 HTTP POST
```

**설계 근거:**
- WebSocket: 실시간 양방향 통신, 에이전트가 지속 연결 유지 시 최적
- Webhook: 에이전트가 서버리스이거나 간헐적 연결 시 적합, 상태 비저장
- REST: 쿼리 모드 + 카탈로그 탐색에 적합, 가장 단순

_Source: [Hookdeck](https://hookdeck.com/webhooks/guides/when-to-use-webhooks), [Alchemy Webhooks](https://www.alchemy.com/webhooks), [Postman Blog](https://blog.postman.com/examining-use-cases-for-asynchronous-apis-webhooks-and-websockets/)_

### MCP (Model Context Protocol) 통합

**Cherry를 MCP 서버로 구현하면:**
- 모든 MCP 호환 에이전트(Claude, OpenAI, Vercel AI SDK 등)가 Cherry 지식에 바로 접근
- 2026년 3월 기준 50+ 공식 서버, 150+ 커뮤니티 구현 존재
- SDK: TypeScript, Python, C#, Java, Kotlin

**Cherry MCP Server 구조:**
```
MCP Server: cherry-knowledge
├── Tools:
│   ├── query_knowledge(question, depth, budget)
│   ├── get_concept(concept_id)
│   └── search_concepts(keyword)
├── Resources:
│   ├── concept://{id} — 컨셉 데이터
│   └── evidence://{id} — 에비던스 데이터
└── Prompts:
    └── explain_concept(topic) — 컨셉 설명 프롬프트
```

**해커톤 임팩트:** MCP 서버 구현 시 "어떤 AI 에이전트든 Cherry 지식에 접근 가능" → 데모에서 Claude/GPT가 Cherry를 tool로 사용하는 것을 시연 가능

_Source: [MCP Docs](https://modelcontextprotocol.io/docs/getting-started/intro), [DEV.to MCP Guide](https://dev.to/universe7creator/the-complete-guide-to-model-context-protocol-mcp-building-ai-native-applications-in-2026-5e57), [OpenAI MCP](https://openai.github.io/openai-agents-python/mcp/)_

### 스마트 컨트랙트 통합 패턴

**CherryCredit.sol (ERC-20 기반 크레딧 시스템):**
```solidity
// 핵심 함수
deposit(amount)        — 크레딧 충전 (BNB/ETH → 크레딧 토큰)
consume(agentId, amount, queryHash)  — 쿼리/구독 비용 차감
withdrawReward(curatorId) — 큐레이터 보상 출금
getBalance(agentId)    — 잔액 조회

// 이벤트 (블록체인 이벤트 → Webhook으로 에이전트에 알림)
event CreditConsumed(address agent, uint256 amount, bytes32 queryHash)
event RewardDistributed(address curator, uint256 amount)
event ProvenanceRecorded(bytes32 knowledgeHash, uint256 timestamp)
```

**트랙별 컨트랙트 배포:**

| 트랙 | 체인 | 컨트랙트 | 특이사항 |
|------|------|---------|---------|
| BNB Chain | opBNB Testnet (5611) | CherryCredit.sol | 표준 ERC-20, Hardhat 배포 |
| Status Network | Status Testnet (1660990954) | CherryCredit.sol + KarmaIntegration | **가스리스 배포** (`linea_estimateGas`), Karma 읽기 |
| NEAR AI | NEAR Testnet | cherry_credit.ts | near-sdk-js, 별도 구현 |

**Hardhat 네트워크 설정:**
```typescript
// hardhat.config.ts
networks: {
  opbnbTestnet: {
    url: "https://opbnb-testnet-rpc.bnbchain.org/",
    chainId: 5611,
    accounts: [process.env.PRIVATE_KEY],
  },
  statusTestnet: {
    url: "https://public.sepolia.rpc.status.network",
    chainId: 1660990954,
    accounts: [process.env.PRIVATE_KEY],
    // Status: linea_estimateGas 사용 필요 — 커스텀 가스 추정
  },
}
```

_Source: [OpenZeppelin ERC-20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol), [Ethereum.org ERC-20](https://ethereum.org/developers/docs/standards/tokens/erc-20/), [CryptoAPIs Webhooks](https://cryptoapis.io/blog/6-webhooks-push-notifications-for-blockchain-events)_

### 블록체인 이벤트 → 구독 스트림 연동

**아키텍처 흐름:**
```
Knowledge Team이 에비던스 추가
    ↓
Cherry 서버가 변경 감지
    ↓
온체인에 provenance 해시 기록 (CherryCredit.emit ProvenanceRecorded)
    ↓
블록체인 이벤트 리스너가 감지
    ↓
구독 에이전트에게 WebSocket/Webhook 푸시
    ↓
에이전트 크레딧 자동 차감
```

**이벤트 리스너 구현:**
- **BNB Chain:** opBNB WebSocket RPC + ethers.js `contract.on("event")`
- **Status Network:** 동일 패턴 (EVM 호환) + Blockscout API
- **NEAR AI:** NEAR Indexer 또는 NEAR Lake Framework

### 인증 패턴

**API 인증 (중앙화):**
- API Key 기반 — 에이전트 등록 시 발급
- JWT 토큰 — 세션 관리
- Rate limiting — 크레딧 잔액 기반

**온체인 인증 (하이브리드):**
- 지갑 서명(EIP-712) → 서버가 검증 → API 접근 허용
- Status Network: Karma 티어 확인 → 일일 할당량 설정
- NEAR AI: NEAR 계정 서명 → TEE 접근 인증

### 해커톤 MVP 통합 아키텍처 (최종)

```
┌─────────────────────────────────────────────┐
│              AI Agent (Claude/GPT 등)         │
│  ┌─────────┐  ┌──────────┐  ┌────────────┐ │
│  │ MCP Tool │  │ REST API │  │ WebSocket  │ │
│  └────┬─────┘  └────┬─────┘  └─────┬──────┘ │
└───────┼──────────────┼──────────────┼────────┘
        │              │              │
┌───────┴──────────────┴──────────────┴────────┐
│           Cherry KaaS Server (Node.js)        │
│  ┌──────────┐ ┌──────────┐ ┌───────────────┐│
│  │ Catalog   │ │ Query    │ │ Subscription  ││
│  │ Service   │ │ Service  │ │ Manager       ││
│  └──────────┘ └──────────┘ └───────────────┘│
│  ┌──────────┐ ┌──────────┐ ┌───────────────┐│
│  │ Credit   │ │ Curator  │ │ Provenance    ││
│  │ Manager  │ │ Rewards  │ │ Recorder      ││
│  └────┬─────┘ └────┬─────┘ └──────┬────────┘│
└───────┼─────────────┼──────────────┼─────────┘
        │             │              │
┌───────┴─────────────┴──────────────┴─────────┐
│         On-Chain Layer (트랙별 교체)           │
│                                               │
│  [BNB] opBNB + Greenfield                     │
│  [Status] Hoodi Testnet (가스리스 + Karma)     │
│  [NEAR] NEAR Testnet + TEE                    │
└───────────────────────────────────────────────┘

---

## Architectural Patterns — 해커톤 MVP 설계

### System Architecture: Modular Monolith → 마이크로서비스 가능

**해커톤 MVP 원칙:** "증명하기 위해 만드는 것이지, 감동시키기 위해 만드는 것이 아님" — 모듈형, 가벼운, 변경 가능한 구조

**선택: Modular Monolith (Node.js/Express)**
- 해커톤 2-4일 내 구현 가능
- 단일 서버에 모듈형 서비스 분리
- 추후 마이크로서비스로 분해 용이

```
cherry-kaas-server/
├── src/
│   ├── modules/
│   │   ├── catalog/        — 카탈로그 API (#30)
│   │   ├── query/          — 쿼리 서비스 (#32)
│   │   ├── subscription/   — 구독 매니저 (#33, #20-22)
│   │   ├── credit/         — 크레딧 매니저 (#34)
│   │   ├── curator/        — 큐레이터 보상 (#27)
│   │   └── provenance/     — 온체인 기록
│   ├── chain-adapters/     — 트랙별 온체인 어댑터
│   │   ├── bnb.adapter.ts
│   │   ├── status.adapter.ts
│   │   └── near.adapter.ts
│   ├── mcp-server/         — MCP 프로토콜 서버
│   └── app.ts              — Express 앱 엔트리
├── contracts/
│   ├── solidity/           — BNB + Status용
│   │   └── CherryCredit.sol
│   └── near/               — NEAR용
│       └── cherry_credit.ts
├── frontend/               — 데모 대시보드
└── docker-compose.yml
```

_Source: [SaM Solutions](https://sam-solutions.com/blog/node-js-mvp-development/), [Softermii](https://www.softermii.com/blog/for-startups/mvp-development-guide-process-costs-and-real-examples)_

### 이벤트 드리븐 패턴 — 구독 스트림

**Cherry 내부 이벤트 버스:**
- 포인트투포인트 대신 이벤트 버스 패턴 사용
- N개 에이전트 × 이벤트 허브 = O(N) 연결 (확장 가능)
- 해커톤 MVP: 인메모리 EventEmitter → 추후 Redis Pub/Sub 또는 Kafka로 교체

```
[Knowledge Update] → EventBus.emit("evidence:added", data)
                         ↓
              ┌──────────┴──────────┐
              ↓                     ↓
    WebSocket Clients        Webhook Dispatcher
    (실시간 에이전트)          (비동기 에이전트)
```

_Source: [Atlan](https://atlan.com/know/event-driven-architecture-for-ai-agents/), [NovaSarc](https://www.novasarc.com/integration-trends-2026-api-microservices-eda)_

### Chain Adapter 패턴 — 복수 트랙 지원

**Strategy Pattern으로 온체인 레이어 추상화:**

```typescript
interface ChainAdapter {
  recordProvenance(hash: string): Promise<TxReceipt>
  consumeCredit(agentId: string, amount: number): Promise<TxReceipt>
  distributeReward(curatorId: string, amount: number): Promise<TxReceipt>
  getBalance(agentId: string): Promise<number>
  getReputation?(agentId: string): Promise<number> // Status Karma
}

// 트랙별 구현
class BNBAdapter implements ChainAdapter { ... }    // opBNB + Greenfield
class StatusAdapter implements ChainAdapter { ... }  // 가스리스 + Karma
class NEARAdapter implements ChainAdapter { ... }    // TEE + NEAR 계정
```

**장점:**
- 환경변수로 트랙 전환: `CHAIN_ADAPTER=status`
- 동일 비즈니스 로직, 온체인만 교체
- 각 트랙 제출 시 해당 어댑터만 활성화

### 보안 아키텍처

**레이어별 보안:**

| 레이어 | 보안 패턴 |
|--------|----------|
| API | API Key + Rate Limiting (크레딧 기반) |
| 인증 | EIP-712 지갑 서명 또는 NEAR 계정 서명 |
| 데이터 | HTTPS + 온체인 provenance 해시 |
| 프라이버시 (Status) | RLN ZK proof — 에이전트 신원 비공개 |
| 프라이버시 (NEAR) | TEE 내 쿼리 처리 — 인프라 제공자도 접근 불가 |
| 스마트 컨트랙트 | OpenZeppelin 기반, 기본 접근 제어 |

### 배포 전략

**해커톤 빠른 배포:**

| 컴포넌트 | 배포 대상 | 도구 |
|---------|----------|------|
| Cherry API 서버 | AWS (기존 호스팅) | Docker / PM2 |
| 프론트엔드 데모 | AWS (기존 호스팅) | Next.js (SSR 또는 정적) |
| 스마트 컨트랙트 (BNB) | opBNB 테스트넷 (Chain ID: 5611) | Hardhat |
| 스마트 컨트랙트 (Status) | Status Testnet (Chain ID: 1660990954) | Hardhat/Foundry |
| NEAR 컨트랙트 | NEAR 테스트넷 | NEAR CLI |
| MCP 서버 | Cherry API와 동일 AWS 서버 | MCP SDK (TypeScript) |

**비용:** 기존 AWS 인프라 활용 + 테스트넷 = 추가 비용 $0

_Source: [Cabot Solutions](https://www.cabotsolutions.com/blog/mvp-development-tools-and-tech-stack-every-founder-should-know-in-2026), [Fast.io](https://fast.io/resources/ai-agent-microservices-architecture/), [Pluralsight](https://www.pluralsight.com/resources/blog/ai-and-data/architecting-microservices-agentic-ai)_

### 해커톤 구현 우선순위 (4일 기준)

| Day | 작업 | 산출물 |
|-----|------|--------|
| **Day 1** | 스마트 컨트랙트 + Chain Adapter | CherryCredit.sol 배포, 어댑터 연결 |
| **Day 2** | Cherry API 서버 코어 | /catalog, /query, /subscribe 엔드포인트 |
| **Day 3** | MCP 서버 + 데모 에이전트 | Claude/GPT가 Cherry tool 사용하는 데모 |
| **Day 4** | 프론트엔드 + 영상 + 발표자료 | 데모 대시보드, 2-4분 영상, 피치덱 |

---

## Implementation Guide — 실전 구현 가이드

### 기술 스택 확정

| 레이어 | 기술 | 근거 |
|--------|------|------|
| **API 서버** | Node.js + Express/Fastify + TypeScript | 빠른 개발, EVM 라이브러리 호환 |
| **MCP 서버** | `@modelcontextprotocol/sdk` (TypeScript) | 공식 SDK, tool/resource 등록 |
| **스마트 컨트랙트** | Solidity + OpenZeppelin + Hardhat | EVM 호환 (BNB + Status 공유) |
| **NEAR 컨트랙트** | TypeScript (near-sdk-js) | JS 개발자 친화적 |
| **프론트엔드** | Next.js + wagmi/viem | 지갑 연결, 컨트랙트 상호작용 |
| **실시간 통신** | ws (WebSocket) 라이브러리 | 구독 스트림 |
| **온체인 상호작용** | ethers.js v6 | opBNB/Status 이벤트 리스닝 |
| **데이터 저장** | SQLite (MVP) → PostgreSQL | 해커톤 속도 우선 |
| **배포** | AWS (호스팅 보유) (프론트) + Railway (API) | 무료 티어, 빠른 배포 |

### MCP 서버 구현 핵심

```typescript
// Cherry MCP Server — 핵심 구조
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "cherry-knowledge", version: "1.0.0" });

// Tool: 지식 쿼리
server.registerTool("query_knowledge", {
  title: "Query Cherry Knowledge",
  description: "Query verified LLM knowledge with provenance",
  inputSchema: z.object({
    question: z.string(),
    depth: z.enum(["summary", "concept", "evidence"]),
    budget: z.number().optional()
  })
}, async ({ question, depth, budget }) => {
  // Cherry API 호출 → 결과 반환
  const result = await cherryAPI.query(question, depth, budget);
  return { content: [{ type: "text", text: JSON.stringify(result) }] };
});

// Tool: 컨셉 검색
server.registerTool("search_concepts", { ... });

// Resource: 컨셉 데이터
server.resource("concept://{id}", async (uri) => { ... });
```

**에이전트 데모 시나리오:**
1. Claude/GPT가 MCP를 통해 Cherry에 연결
2. 사용자: "RAG에서 chunk size 최적화 방법 알려줘"
3. 에이전트 → `query_knowledge("RAG chunk size optimization", "evidence", 50)`
4. Cherry → 검증된 에비던스 + provenance 해시 반환
5. 에이전트가 검증된 지식 기반으로 답변 생성

_Source: [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk), [MCP Server Guide](https://github.com/anthropics/skills/blob/main/skills/mcp-builder/reference/node_mcp_server.md), [FreeCodeCamp MCP Tutorial](https://www.freecodecamp.org/news/how-to-build-a-custom-mcp-server-with-typescript-a-handbook-for-developers/)_

### 스마트 컨트랙트 핵심 코드

```solidity
// CherryCredit.sol — BNB Chain + Status Network 공용
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract CherryCredit is ERC20, Ownable {
    // 이벤트
    event CreditConsumed(address indexed agent, uint256 amount, bytes32 queryHash);
    event RewardDistributed(address indexed curator, uint256 amount);
    event ProvenanceRecorded(bytes32 indexed knowledgeHash, uint256 timestamp);

    // 에이전트 크레딧 충전
    function deposit() external payable {
        uint256 credits = msg.value * CREDIT_RATE;
        _mint(msg.sender, credits);
    }

    // 쿼리 비용 차감 (Cherry 서버가 호출)
    function consumeCredit(address agent, uint256 amount, bytes32 queryHash)
        external onlyOwner {
        _burn(agent, amount);
        emit CreditConsumed(agent, amount, queryHash);
    }

    // 큐레이터 보상 분배
    function distributeReward(address curator, uint256 amount)
        external onlyOwner {
        _mint(curator, amount);
        emit RewardDistributed(curator, amount);
    }

    // Provenance 기록
    function recordProvenance(bytes32 knowledgeHash)
        external onlyOwner {
        emit ProvenanceRecorded(knowledgeHash, block.timestamp);
    }
}
```

**Status Network 추가 — Karma 통합 (실제 테스트넷 주소):**
```solidity
// Status 트랙에서만 사용
// Karma: 0x7ec5Dc75D09fAbcD55e76077AFa5d4b77D112fde
// KarmaTiers: 0xc7fCD786a161f42bDaF66E18a67C767C23cFd30C

interface IKarma {
    function balanceOf(address account) external view returns (uint256);
}

interface IKarmaTiers {
    struct Tier {
        uint256 minKarma;
        uint256 maxKarma;
        string name;
        uint256 txPerEpoch;
    }
    function getTierIdByKarmaBalance(uint256 balance) external view returns (uint8);
    function getTierById(uint8 tierId) external view returns (Tier memory);
}

// Karma 티어별 할인 적용
function getDiscountRate(address agent) public view returns (uint256) {
    uint256 karma = IKarma(0x7ec5Dc75D09fAbcD55e76077AFa5d4b77D112fde).balanceOf(agent);
    uint8 tierId = IKarmaTiers(0xc7fCD786a161f42bDaF66E18a67C767C23cFd30C)
        .getTierIdByKarmaBalance(karma);
    // 티어별 할인: 높은 Karma = 더 많은 할인
    if (tierId >= 3) return 30; // 30% 할인
    if (tierId >= 2) return 15;
    if (tierId >= 1) return 5;
    return 0;
}
```

### 이벤트 리스너 구현 (ethers.js v6)

```typescript
// opBNB/Status 이벤트 리스닝 → 구독 에이전트에게 푸시
import { WebSocketProvider, JsonRpcProvider, Contract } from "ethers";

// opBNB: WSS 지원 — WebSocketProvider 사용
// Status: WSS 비공개 — JsonRpcProvider + polling 또는 Telegram에서 WSS 요청
const provider = new WebSocketProvider(CHAIN_WS_URL); // opBNB
// const provider = new JsonRpcProvider("https://public.sepolia.rpc.status.network"); // Status fallback
const contract = new Contract(CHERRY_CREDIT_ADDR, ABI, provider);

// v6 패턴: ContractPayload 이벤트
contract.on("ProvenanceRecorded", (knowledgeHash, timestamp, event) => {
    subscriptionManager.broadcast({
        type: "provenance_recorded",
        knowledgeHash,
        timestamp: Number(timestamp),
        txHash: event.log.transactionHash
    });
});

contract.on("CreditConsumed", (agent, amount, queryHash, event) => {
    // 해당 에이전트에게 잔액 업데이트 푸시
    subscriptionManager.notifyAgent(agent, {
        type: "credit_consumed",
        amount: Number(amount),
        balance: await contract.balanceOf(agent)
    });
});
```

_Source: [Moralis Event Listening](https://moralis.com/how-to-listen-to-smart-contract-events-using-ethers-js/), [Chainstack Redundant Listener](https://docs.chainstack.com/docs/ethereum-redundant-event-llstener-ethers-web3js)_

### 트랙별 제출 전략

**BNB Chain 트랙 — "Consumer AI Agent Knowledge Trading"**
- 강조: opBNB 저비용 거래 + Greenfield 지식 저장 + 에이전트 워크플로우
- 데모: 에이전트가 Cherry에서 지식 구매 → opBNB에 거래 기록 → Greenfield에 지식 저장
- 해커톤 요구: BSC/opBNB 온체인 증명 + 2건+ 트랜잭션 + #ConsumerAIonBNB 트윗

**Status Network 트랙 — "Gasless Knowledge Agents with Karma Reputation"**
- 강조: **가스리스 에이전트 거래** + Karma 큐레이터 평판 + RLN 프라이버시
- 데모: 에이전트가 $0 비용으로 지식 쿼리 → Karma로 큐레이터 신뢰도 표시
- 해커톤 요구: 가스리스 배포 + 5건+ 가스리스 tx + Karma 읽기/표시

**NEAR AI 트랙 — "Verifiable Private Knowledge for AI Agents"**
- 강조: TEE에서 지식 쿼리 처리 = **인프라 제공자도 내용 못 봄** + attestation 증명
- 데모: 에이전트가 민감한 지식 쿼리 → TEE 처리 → attestation 반환
- 해커톤 요구: TEE 프라이버시 활용 + attestation 통합

### 리스크 & 완화

| 리스크 | 확률 | 완화 |
|--------|------|------|
| 테스트넷 불안정 | 중간 | 3개 트랙 모두 준비 → 1개 실패해도 나머지 제출 |
| MCP 구현 시간 부족 | 낮음 | MCP SDK가 잘 되어있음, 기본 tool 2-3개면 충분 |
| Karma SDK 미완성 | 중간 | 직접 컨트랙트 호출로 대체 가능 |
| NEAR TEE 접근 제한 | 낮음 | OpenAI SDK 호환이라 진입 장벽 낮음 |
| 데모 영상 퀄리티 | 2분 영상 1개 | 트랙별 맞춤 영상 3개 (2-4분) |

### 성공 메트릭

| 메트릭 | 최소 목표 | 이상적 목표 |
|--------|----------|------------|
| 온체인 트랜잭션 | 5건 | 20건+ |
| MCP Tool 수 | 2개 | 5개 |
| 데모 시나리오 | 1개 | 3개 (쿼리/구독/큐레이터) |
| 에이전트 통합 | Claude만 | Claude + GPT |
| 트랙 제출 | 2개 | 3개 |

---

## Executive Summary

### Cherry KaaS × BuidlHack2026: Verified Knowledge Layer for AI Agents

**프로젝트:** Cherry-in-the-Haystack의 블록체인 확장 — AI 에이전트가 큐레이션된 LLM 지식을 거래하는 Knowledge-as-a-Service

**해커톤:** BuidlHack2026 (KBWA), 마감 April 16-17, 2026, 최종 피치 April 18

### 3개 트랙 제출 전략

| 트랙 | 상금 | Cherry 스토리 | 핵심 기술 |
|------|------|-------------|----------|
| **Status Network** | $5K | 가스리스 에이전트 지식 거래 + Karma 큐레이터 평판 | `linea_estimateGas`, Karma 컨트랙트, RLN |
| **BNB Chain** | $5K | Consumer AI 에이전트 + Greenfield 지식 저장 | opBNB (Chain 5611), Greenfield S3 API |
| **NEAR AI** | $5K | 검증 가능한 프라이빗 지식 처리 | TEE (Intel TDX), OpenAI SDK 호환 |
| **General** | $6K | 위 3개 통합 데모 | 전체 아키텍처 |

### 아키텍처 핵심 결정

1. **Modular Monolith (Node.js/TypeScript)** — 해커톤 속도 + 추후 확장
2. **Chain Adapter Pattern** — `CHAIN_ADAPTER=status|bnb|near` 환경변수로 트랙 전환
3. **MCP Server** — Claude/GPT가 Cherry를 tool로 사용 → 킬러 데모
4. **CherryCredit.sol** — ERC-20 기반, BNB+Status 공유, Karma 할인 통합
5. **AWS 배포** — 기존 호스팅 활용, 추가 비용 $0

### 핵심 네트워크 설정 요약

| | opBNB Testnet | Status Testnet | NEAR AI |
|---|---|---|---|
| Chain ID | `5611` | `1660990954` | N/A (API) |
| RPC | `opbnb-testnet-rpc.bnbchain.org` | `public.sepolia.rpc.status.network` | `cloud-api.near.ai` |
| 가스비 | <$0.001 | **$0** | API 과금 |
| Karma | ❌ | `0x7ec5...112fde` | ❌ |
| 특수 API | Greenfield S3 | `linea_estimateGas` | OpenAI SDK 호환 |

### 4일 실행 플랜

| Day | 핵심 작업 | 산출물 |
|-----|----------|--------|
| **1** | CherryCredit.sol 배포 (opBNB + Status) + Chain Adapter | 2개 테스트넷에 컨트랙트 라이브 |
| **2** | Cherry API 서버 (/catalog, /query, /subscribe) + 크레딧 시스템 | 작동하는 REST API |
| **3** | MCP 서버 + 데모 에이전트 (Claude가 Cherry tool 사용) + NEAR AI 통합 | 에이전트가 검증된 지식으로 답변 |
| **4** | 프론트엔드 대시보드 + 2-4분 데모 영상 + 피치덱 | 3개 트랙 제출 완료 |

### 기술적 리스크 & 완화

| 리스크 | 완화 |
|--------|------|
| Status WSS 비공개 | JSON-RPC polling 또는 Telegram에서 요청 |
| Karma SDK 미완성 | 직접 컨트랙트 호출 (주소 확보 완료) |
| NEAR AI 403 에러 | API Key 사전 확보, Telegram 지원 활용 |
| 3개 트랙 동시 제출 부담 | Chain Adapter로 코어 코드 공유, 온체인만 교체 |

### Source Documentation

**공식 개발자 문서:**
- [opBNB Network Info](https://docs.bnbchain.org/bnb-opbnb/get-started/network-info/)
- [opBNB Gas & Fees](https://docs.bnbchain.org/bnb-opbnb/core-concepts/gas-and-fees/)
- [Greenfield APIs & SDKs](https://docs.bnbchain.org/bnb-greenfield/for-developers/apis-and-sdks/)
- [Status Network Docs](https://docs.status.network/)
- [Status Gasless Integration](https://docs.status.network/build-for-karma/guides/gasless-integration)
- [Status Reputation Integration](https://docs.status.network/build-for-karma/guides/reputation-integration)
- [Status Scaffold-ETH Extension](https://github.com/status-im/status-network-scaffold-extension)
- [NEAR AI Docs](https://docs.near.ai/)
- [NEAR AI Private Inference](https://docs.near.ai/cloud/private-inference/)
- [NEAR AI Quickstart](https://docs.near.ai/cloud/quickstart/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Server Guide](https://modelcontextprotocol.io/docs/getting-started/intro)
- [OpenZeppelin ERC-20](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/token/ERC20/ERC20.sol)

**해커톤 리소스:**
- [BuidlHack Discord](https://discord.gg/Z5enQnsaau)
- Status 멘토: @yjkellyjoo
- NEAR AI 지원: [t.me/nearaialpha](https://t.me/nearaialpha)
- Status Builders: [t.me/statusl2](https://t.me/statusl2)

---

**Technical Research Completion Date:** 2026-04-14
**Deadline:** April 16-17, 2026 (제출) / April 18 (최종 피치)
**Source Verification:** All facts cited with official documentation
**Confidence Level:** High — 공식 docs + 실제 컨트랙트 주소 검증 완료
```
