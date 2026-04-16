# cherry-kaas-agent — 독립 에이전트 패키지 기획서

## 개요

Cherry KaaS 서비스에서 사용자의 로컬 Claude Code와 원격 서버를 연결하는 경량 에이전트 패키지.
npm으로 배포하여 `npx` 한 줄로 누구나 실행 가능.

## 배경 (왜 필요한가)

Cherry KaaS는 웹 서비스다. 구조:

```
[원격 서버 solteti.site]          [사용자 로컬 PC]
  지식 마켓 (API + DB)      ←→     사용자의 Claude Code + 에이전트
```

- 서버: 지식 카탈로그, 구매/판매, 큐레이터 보상, 온체인 기록
- 로컬: 사용자의 AI 에이전트 (Claude Code)

이 둘이 소통해야 한다:
- 에이전트가 지식을 검색/구매 (MCP 도구)
- 서버가 에이전트에게 보고서 요청 (WebSocket)
- 에이전트가 자기 지식 상태를 보고 (self-report)

### 현재 문제

`mcp-server.ts`가 로컬 프로젝트 파일 + DB 직접 접속에 의존:
- 프로젝트 소스 코드 필요 (`start-mcp.sh` 경로)
- DB 비밀번호 필요 (`.env`에서 읽음)
- `.env`의 `KAAS_WS_URL`이 `localhost:4000`으로 박혀있음

→ 개발자 PC에서만 동작. 일반 사용자는 사용 불가.

## 목표

**일반 사용자(Claude Code 사용자)가 프로젝트 소스 코드 없이, 명령어 한 줄로 자신의 에이전트를 Cherry KaaS 서버에 연결.**

## 사용자 여정

### 1단계: 에이전트 등록 (웹사이트)
```
solteti.site → Dashboard → + 버튼 → 에이전트 이름/지갑 입력 → 등록
→ API 키 발급 (ck_live_xxx) — DB에 저장
```

### 2단계: 연결 명령어 복사 (대시보드)
대시보드에 표시:
```bash
claude mcp add \
  --transport stdio \
  --env KAAS_AGENT_API_KEY=ck_live_xxx \
  --env KAAS_WS_URL=https://solteti.site \
  cherry-kaas -- npx -y cherry-kaas-agent
```
복사 버튼 제공. API 키와 서버 URL은 자동 채움.

### 3단계: 터미널에서 실행 (사용자 PC)
사용자가 복사한 명령어를 붙여넣기 → Enter.
- `npx -y`가 npm에서 `cherry-kaas-agent` 패키지를 자동 다운로드 + 실행
- 프로젝트 파일 필요 없음
- DB 비밀번호 필요 없음
- Node.js만 있으면 됨 (Claude Code 필수 요건이므로 이미 설치됨)

### 4단계: Claude Code에서 사용
```
사용자: "RAG 개념 구매해줘"
Claude: → MCP 도구 purchase_concept 호출 → 서버 API에 HTTP 요청 → 구매 완료

사용자: 대시보드에서 📚 Diff 클릭
서버: → WebSocket으로 에이전트에 self-report 요청
에이전트: → 보고서 생성 → 서버로 전송 → 대시보드에 표시
```

### 해제
```bash
claude mcp remove cherry-kaas
```

## 패키지 아키텍처

### 통신 구조
```
Claude Code ←── stdio (MCP 프로토콜) ──→ cherry-kaas-agent
                                              │
                                              ├── HTTP ──→ solteti.site/api/v1/kaas/*
                                              │            (도구 실행: 검색, 구매, 팔로우 등)
                                              │            (인증: api_key를 body/query로 전달)
                                              │
                                              └── WebSocket ──→ solteti.site/kaas
                                                                (self-report, compare, knowledge 제출)
                                                                (인증: api_key를 auth로 전달)
```

### 패키지 내부

```
cherry-kaas-agent/
  package.json      name: "cherry-kaas-agent", bin: { "cherry-kaas-agent": "./bin/agent.js" }
  bin/agent.js      진입점 (#!/usr/bin/env node)
  lib/
    mcp-tools.js    MCP 도구 핸들러 (서버 HTTP API 호출)
    ws-client.js    WebSocket 연결 + 이벤트 핸들러
```

### 의존성 (최소한)

| 패키지 | 용도 |
|---|---|
| `@modelcontextprotocol/sdk` | MCP stdio 서버 |
| `socket.io-client` | WebSocket 연결 |
| `fetch` (내장) | 서버 API 호출 — Node.js 18+ 내장, 별도 설치 불필요 |

**불필요한 것 (제거):**
- `knex` — DB 직접 접속 안 함
- `pg` — PostgreSQL 드라이버 불필요
- `dotenv` — 환경변수는 Claude Code `--env`로 전달
- `ethers` — 온체인 작업은 서버가 처리
- `config.ts` — 로컬 `.env` 의존 끊음

### 환경변수 (Claude Code `--env`로 전달)

| 변수 | 설명 | 예시 |
|---|---|---|
| `KAAS_AGENT_API_KEY` | 에이전트 인증 키 (대시보드에서 발급) | `ck_live_xxx` |
| `KAAS_WS_URL` | 서버 주소 (대시보드 명령어에 포함) | `https://solteti.site` |

이 두 개만 있으면 동작. 설정 파일 불필요.
- `KAAS_AGENT_API_KEY`는 HTTP API 호출 시 인증에도 사용
- `KAAS_WS_URL`은 WebSocket 연결과 HTTP API 호출 베이스 URL 둘 다에 사용

## MCP 도구 목록

서버 API를 HTTP로 호출. 인증은 `api_key`를 body/query로 전달 (기존 REST API 방식 그대로):

| 도구 | 설명 | 서버 API | 인증 |
|---|---|---|---|
| `search_catalog` | 지식 카탈로그 검색 | `GET /api/v1/kaas/catalog?q=...` | 불필요 (공개) |
| `get_concept` | 개념 상세 조회 | `GET /api/v1/kaas/catalog/:id` | 불필요 (공개) |
| `purchase_concept` | 개념 구매 (크레딧 차감 + 온체인) | `POST /api/v1/kaas/purchase` | body `api_key` |
| `follow_concept` | 개념 팔로우 (업데이트 구독) | `POST /api/v1/kaas/follow` | body `api_key` |
| `compare_knowledge` | 보유 지식 vs 카탈로그 비교 | `POST /api/v1/kaas/catalog/compare` | body `api_key` |
| `submit_knowledge` | 보유 지식 제출 | WebSocket `submit_knowledge` | WebSocket auth |
| `generate_self_report` | 자기 지식 보고서 생성 + 제출 | WebSocket `submit_self_report` | WebSocket auth |
| `get_room_history` | 채팅 대화 이력 조회 | `POST /api/v1/kaas/mcp/ws-chat` | body `api_key` |
| `reply_to_room` | 채팅 메시지 전송 | WebSocket `room_message` | WebSocket auth |

## WebSocket 이벤트

| 이벤트 | 방향 | 설명 |
|---|---|---|
| `connect` | agent → server | 연결 (auth: `{ api_key }`) |
| `connected` | server → agent | 인증 성공 (agentId, agentName 반환) |
| `request_knowledge` | server → agent | Compare 요청 → 에이전트가 보유 지식 제출 |
| `submit_knowledge` | agent → server | 보유 지식 목록 전송 |
| `request_self_report` | server → agent | 보고서 요청 |
| `submit_self_report` | agent → server | 보고서 제출 (`triggered_by: 'request'`) |
| `room_message` | 양방향 | 3자 대화 (사용자 ↔ Cherry ↔ 에이전트) |

## 서버 측 필요 작업

에이전트 패키지가 HTTP로 호출할 API 중 현재 없는 것:

| 필요 API | 용도 | 현재 상태 | 작업 |
|---|---|---|---|
| `POST /api/v1/kaas/agents/:id/knowledge` | 에이전트 보유 지식 REST 제출 | WebSocket으로만 가능 | 신규 엔드포인트 추가 |

나머지 (`catalog`, `purchase`, `follow`, `compare`, `ws-chat`)는 이미 존재.

## 보안

- API 키는 `--env`로 프로세스 환경변수에만 전달 (파일 저장 안 함)
- DB 비밀번호, 서버 내부 정보 사용자에게 노출 없음
- 모든 데이터는 서버 API를 통해서만 접근 (서버가 권한 검증)
- API 키 탈취 시: 대시보드에서 해당 에이전트 삭제 + 재등록으로 무효화
- WebSocket 인증: 연결 시 `auth: { api_key }` 전달 → 서버가 DB에서 검증

## 대시보드 변경

### 연결 명령어 (CLAUDE CODE CONNECTION 섹션)
```bash
claude mcp add \
  --transport stdio \
  --env KAAS_AGENT_API_KEY=ck_live_xxx \
  --env KAAS_WS_URL=https://solteti.site \
  cherry-kaas -- npx -y cherry-kaas-agent
```
- `ck_live_xxx` → 해당 에이전트 API 키로 자동 채움
- `https://solteti.site` → 현재 도메인으로 자동 채움
- 복사 버튼 제공

### 해제 명령어
```bash
claude mcp remove cherry-kaas
```

## 구현 순서

### Phase 1: 패키지 골격
- [ ] `apps/agent-package/` 디렉토리 생성
- [ ] `package.json` 작성 (name: `cherry-kaas-agent`, version, bin, dependencies)
- [ ] 진입점 `bin/agent.js` — MCP stdio 서버 시작 + WebSocket 연결

### Phase 2: MCP 도구 (DB 직접 조회 → 서버 HTTP API 호출)
- [ ] `search_catalog` — `GET /api/v1/kaas/catalog` 호출
- [ ] `get_concept` — `GET /api/v1/kaas/catalog/:id` 호출
- [ ] `purchase_concept` — `POST /api/v1/kaas/purchase` 호출 (body에 `api_key`)
- [ ] `follow_concept` — `POST /api/v1/kaas/follow` 호출
- [ ] `compare_knowledge` — `POST /api/v1/kaas/catalog/compare` 호출
- [ ] `get_room_history` — `POST /api/v1/kaas/mcp/ws-chat` 호출
- [ ] `reply_to_room` — WebSocket `room_message` emit

### Phase 3: WebSocket
- [ ] 서버 연결 + API 키 인증 (기존 `mcp-server.ts` 로직 재사용)
- [ ] `request_knowledge` → 보유 지식 제출
- [ ] `request_self_report` → 보고서 생성 + 제출
- [ ] `room_message` → 3자 대화 수신/발신

### Phase 4: 서버 API 보완
- [ ] `POST /api/v1/kaas/agents/:id/knowledge` 엔드포인트 추가 (보유 지식 REST 제출)

### Phase 5: 배포
- [ ] npm publish (`cherry-kaas-agent`)
- [ ] `npx -y cherry-kaas-agent` 실행 확인
- [ ] 대시보드 명령어 업데이트 (올바른 Claude Code 문법)
- [ ] 매뉴얼 업데이트

## 타임라인

| Phase | 예상 시간 |
|---|---|
| Phase 1: 패키지 골격 | 30분 |
| Phase 2: MCP 도구 | 1시간 |
| Phase 3: WebSocket | 30분 |
| Phase 4: 서버 API 보완 | 20분 |
| Phase 5: 배포 | 30분 |
| **합계** | **2시간 50분** |

## 비고

- Claude Code 사용자는 Node.js가 이미 설치되어 있음 (Claude Code 필수 요건)
- `npx -y`는 패키지를 자동 설치 + 캐시하므로 두 번째 실행부터 빠름
- 서버 API가 모든 권한 검증/DB 조회를 담당 — 에이전트 패키지는 중개자 역할만
- 기존 `mcp-server.ts` (프로젝트 내장 버전)은 개발용으로 유지 가능
- 에이전트 패키지는 로컬 파일, DB, `.env`에 일절 의존하지 않음
