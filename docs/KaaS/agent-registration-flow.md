# Cherry KaaS 에이전트 통신 아키텍처

## 개요

Cherry KaaS는 MCP(Model Context Protocol) Streamable HTTP를 통해 원격 에이전트와 통신한다.
에이전트가 Cherry에 접속해서 지식을 비교하고, 구매하고, 대화하는 플랫폼.

## 통신 프로토콜

### MCP Streamable HTTP

- **전송 방식**: HTTP POST + SSE (Server-Sent Events) 스트리밍
- **엔드포인트**: `https://cherry-kaas.com/mcp` (단일 URL)
- **인증**: Cherry API Key (`ck_live_...`) — HTTP 헤더로 전달
- **양방향**: 클라이언트→서버 (tool 호출), 서버→클라이언트 (Elicitation, Sampling, Notification)

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
```

## 에이전트 등록 플로우

### 1단계: 웹에서 에이전트 계정 생성

사용자가 Cherry KaaS 웹사이트에서:

1. Dashboard → 에이전트 등록
2. 입력: **에이전트 이름** + **MetaMask 지갑 연결**
3. 등록 완료 → **Cherry API Key** 발급 (`ck_live_...`)
4. **MCP 엔드포인트 URL** 안내: `https://cherry-kaas.com/mcp`
5. 크레딧 충전 (Deposit)

### 2단계: 로컬 에이전트에 MCP 연결 설정

**Claude Desktop:**
```json
{
  "mcpServers": {
    "cherry-kaas": {
      "url": "https://cherry-kaas.com/mcp",
      "headers": {
        "Authorization": "Bearer ck_live_발급받은키"
      }
    }
  }
}
```

**Claude Code:**
```bash
claude mcp add cherry-kaas --url https://cherry-kaas.com/mcp --header "Authorization: Bearer ck_live_..."
```

**커스텀 에이전트:**
```
MCP Client SDK로 Streamable HTTP 연결
엔드포인트: https://cherry-kaas.com/mcp
인증: Authorization: Bearer ck_live_...
```

### 3단계: 에이전트 연결 완료

에이전트가 MCP 엔드포인트에 접속하면 Cherry가 인식.
웹 Dashboard에 "Connected" 상태 표시.

---

## 3가지 핵심 시나리오

### 시나리오 1: 지식 비교 (Compare) — Elicitation 활용

**트리거**: 웹에서 유저가 Compare 버튼 클릭

**흐름:**
```
1. [웹] 유저가 카탈로그에서 Compare 버튼 클릭
2. [Cherry → 에이전트] Elicitation 요청:
   "보유 지식 목록을 제출해주세요"
   {
     type: "elicitation/create",
     message: "현재 보유한 지식 목록을 제출해주세요",
     schema: {
       type: "object",
       properties: {
         known_topics: {
           type: "array",
           items: { type: "object", properties: { topic: { type: "string" }, lastUpdated: { type: "string" } } }
         }
       }
     }
   }
3. [에이전트] 로컬 파일/DB에서 보유 지식 목록 수집
4. [에이전트 → Cherry] Elicitation 응답:
   {
     known_topics: [
       { topic: "rag", lastUpdated: "2025-01-01" },
       { topic: "embeddings", lastUpdated: "2025-06-01" }
     ]
   }
5. [Cherry] 카탈로그와 비교 → gap 분석
6. [웹] 카탈로그에 태그 표시:
   - ✅ Up-to-date (에이전트가 최신 보유)
   - ⚠️ Outdated (에이전트 지식이 오래됨)
   - 🔴 Gap (에이전트가 모르는 개념)
```

### 시나리오 2: 지식 구매 (Purchase) — Tool Call

**트리거**: 웹에서 유저가 Purchase 버튼 클릭, 또는 에이전트가 자발적으로

**흐름:**
```
1. [에이전트 → Cherry] Tool 호출:
   purchase_concept({ concept_id: "rag" })
2. [Cherry] 크레딧 차감 + content_md 조회 + provenance hash 생성
3. [Cherry → 에이전트] Tool 응답:
   {
     content_md: "# RAG\n## 개요\nRAG는 LLM이...",
     evidence: [...],
     provenance: { hash: "0x...", explorer_url: "..." },
     credits_consumed: 20,
     credits_remaining: 180
   }
4. [에이전트] content_md를 로컬에 저장 (파일, DB 등)
5. [웹] 구매 이력에 실시간 표시
```

### 시나리오 3: 에이전트와 대화 (Chat) — Sampling 활용

**트리거**: 웹 채팅방에서 유저가 에이전트에게 지시

**흐름:**
```
1. [웹] 유저: "RAG에 대해 Cherry에게 물어봐"
2. [Cherry → 에이전트] Sampling 요청:
   sampling/createMessage({
     messages: [
       { role: "user", content: "Cherry KaaS 카탈로그에서 RAG 관련 지식을 검색해서 알려줘" }
     ],
     systemPrompt: "너는 Cherry KaaS에서 지식을 구매하는 에이전트야..."
   })
3. [에이전트] 자체 LLM으로 처리 → Cherry tool 호출 결정
4. [에이전트 → Cherry] search_catalog({ query: "rag" })
5. [Cherry → 에이전트] 검색 결과 반환
6. [에이전트] LLM이 결과 정리
7. [에이전트 → Cherry] Sampling 응답:
   "RAG 관련 지식이 있습니다. Quality 4.8점. 구매할까요?"
8. [웹] 채팅방에 에이전트 응답 표시
```

---

## 웹 UI 구성

| 페이지 | 기능 | MCP 연동 |
|--------|------|----------|
| 카탈로그 | 지식 브라우징 + Compare 태그 | Elicitation으로 지식 비교 |
| 카탈로그 상세 | Purchase/Follow 버튼 | Tool call로 구매 |
| Dashboard | 에이전트 등록/충전/이력 | 연결 상태 모니터링 |
| 채팅 콘솔 | 유저↔에이전트↔Cherry 3자 대화 | Sampling으로 에이전트 대화 |
| 지식 큐레이팅 | 관리자 concept/evidence CRUD | - |

---

## 역할 분리

| 구분 | 웹사이트 | Cherry 서버 | 로컬 에이전트 |
|------|---------|------------|-------------|
| 역할 | 유저 인터페이스 | 지식 플랫폼 + MCP 서버 | 지식 소비자 |
| 하는 일 | 등록, 충전, 브라우징, 채팅 UI | API 제공, 비교, 크레딧 관리 | 지식 제출, 구매, 로컬 저장, LLM 처리 |
| 통신 | REST API ↔ Cherry 서버 | MCP Streamable HTTP ↔ 에이전트 | MCP Client |
| LLM | 없음 | 없음 | 에이전트 자체 보유 |
| 지식 저장 | 없음 (표시만) | 카탈로그 DB | 로컬 파일/DB |

---

## MCP Server 구성

### Tools (에이전트 → Cherry)

| Tool | 설명 | 크레딧 |
|------|------|--------|
| search_catalog | 카탈로그 검색 | 무료 |
| get_concept | 개념 상세 조회 (preview) | 무료 |
| purchase_concept | 구매 → content_md 반환 | 20cr |
| follow_concept | 팔로우 → 업데이트 포함 | 25cr |
| compare_knowledge | 보유 지식 vs 카탈로그 비교 | 무료 |

### Elicitation (Cherry → 에이전트)

| 요청 | 설명 |
|------|------|
| request_knowledge_list | 에이전트에게 보유 지식 목록 요청 |

### Sampling (Cherry → 에이전트 LLM)

| 요청 | 설명 |
|------|------|
| agent_chat | 유저 메시지를 에이전트 LLM에 전달, 응답 수신 |

### Notifications (Cherry → 에이전트)

| 알림 | 설명 |
|------|------|
| knowledge_updated | 팔로우 중인 개념의 content 업데이트 알림 |
| credits_low | 크레딧 부족 경고 |

---

## 구현 순서

### Phase 1: MCP Streamable HTTP 서버 (필수)
1. 기존 stdio MCP 서버 → Streamable HTTP 전환
2. API Key 인증 미들웨어
3. 세션 관리 (연결된 에이전트 추적)

### Phase 2: Elicitation (Compare 기능)
1. 웹 Compare 버튼 → Cherry 서버 → 에이전트에 Elicitation 요청
2. 에이전트 응답 수신 → gap 분석 → 웹에 태그 표시

### Phase 3: Sampling (채팅 기능)
1. 웹 채팅 입력 → Cherry 서버 → 에이전트에 Sampling 요청
2. 에이전트 LLM 응답 수신 → 웹 채팅에 표시

### Phase 4: 실시간 모니터링
1. 에이전트 연결 상태 WebSocket으로 웹에 push
2. 구매/비교 이벤트 실시간 대시보드 표시

---

## 기술 스택

| 구성 요소 | 기술 |
|----------|------|
| MCP Server | @modelcontextprotocol/sdk + Streamable HTTP transport |
| 웹 ↔ 서버 | REST API + WebSocket (실시간 이벤트) |
| 에이전트 ↔ 서버 | MCP Streamable HTTP (JSON-RPC over HTTP+SSE) |
| 인증 | Cherry API Key (Bearer token) |
| 블록체인 | Status Network Sepolia (gasless provenance) |
