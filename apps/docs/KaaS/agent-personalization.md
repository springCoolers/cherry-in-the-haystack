# 에이전트 개인화 기획서 — 이메일 로그인 기반 사용자별 에이전트 격리

## 목표

이메일 로그인한 사용자만 자기 에이전트를 등록/관리할 수 있고, 다른 사용자의 에이전트/지갑/거래는 보이지 않는다.

## 현재 상태 (Before)

```
모든 에이전트 → SYSTEM_USER_ID (00000000-...) → 모든 사람이 다 봄
로그인 시스템 → 있지만 KaaS에서 안 씀
DB 스키마 → kaas.agent.user_id 컬럼 존재 (미사용)
```

## 변경 후 (After)

```
사용자 A 로그인 → 에이전트 등록 → A의 user_id로 저장 → A만 보임
사용자 B 로그인 → 에이전트 등록 → B의 user_id로 저장 → B만 보임
비로그인 → 대시보드 접근 시 로그인 화면으로 이동
```

## 기존 인프라 (이미 구현됨, 변경 불필요)

| 항목 | 상태 | 위치 |
|---|---|---|
| 매직링크 이메일 로그인 | ✅ 완비 | `apps/api/src/modules/app_user/` |
| JWT 발급/검증 | ✅ 완비 | `RoleJwtStrategy` + `AuthGuard('jwt')` |
| `@AuthUser('id')` 데코레이터 | ✅ 완비 | `apps/api/src/common/decorators/auth-user.decorator.ts` |
| `OptionalJwtAuthGuard` | ✅ 완비 | `apps/api/src/middleware/optional-jwt-auth.guard.ts` |
| 프론트 로그인 UI | ✅ 완비 | `apps/web/app/login/page.tsx` |
| localStorage에 accessToken 저장 | ✅ 완비 | 로그인 시 자동 |
| DB `kaas.agent.user_id` 컬럼 | ✅ 존재 | FK → `core.app_user(id)` + 인덱스 |

---

## 단계별 구현 계획

### Phase 1: 백엔드 — 에이전트 컨트롤러 개인화

**파일:** `apps/api/src/modules/kaas/kaas-agent.controller.ts`

**변경 내용:**
1. `SYSTEM_USER_ID` 상수 삭제
2. `@UseGuards(AuthGuard('jwt'))` 추가 (컨트롤러 레벨)
3. 각 엔드포인트에서 `@AuthUser('id') userId: string` 사용

**상세:**

```
POST /register
  Before: agentService.register(SYSTEM_USER_ID, dto)
  After:  agentService.register(userId, dto)     ← JWT에서 userId 추출

GET /
  Before: agentService.findByUserId(SYSTEM_USER_ID)
  After:  agentService.findByUserId(userId)       ← 로그인 유저의 에이전트만

DELETE /:id
  Before: 소유권 체크 없음
  After:  agent.user_id === userId 확인 후 삭제

PATCH /:id/model
  Before: 소유권 체크 없음
  After:  agent.user_id === userId 확인 후 수정

GET /:id/karma
  Before: 소유권 체크 없음
  After:  agent.user_id === userId 확인 후 조회
```

**테스트:**
- [ ] JWT 없이 `POST /register` → 401
- [ ] 유저 A 로그인 → 에이전트 등록 → 유저 A의 `GET /` → 등록한 에이전트 보임
- [ ] 유저 B 로그인 → `GET /` → 유저 A의 에이전트 안 보임
- [ ] 유저 B가 유저 A 에이전트 `DELETE` 시도 → 403
- [ ] 유저 A가 자기 에이전트 `DELETE` → 성공

---

### Phase 2: 백엔드 — findAgent fallback 제거

**파일:** `kaas-query.controller.ts`, `kaas-credit.controller.ts`

**변경 내용:**
두 파일의 `findAgent()` 헬퍼에서 `SYSTEM_USER_ID` fallback 제거.

```
Before:
  if (apiKey) return agentService.authenticate(apiKey)
  const agents = await agentService.findByUserId('00000000-...')
  return agents[0]

After:
  if (apiKey) return agentService.authenticate(apiKey)
  throw new UnauthorizedException('API Key required')
```

**왜 이렇게:**
- MCP 클라이언트(Claude Code)는 항상 `api_key`를 보냄 → 정상 동작
- 웹 대시보드도 에이전트 선택 시 `api_key`를 보냄 → 정상 동작
- `api_key` 없이 호출하는 경우는 없어야 함

**테스트:**
- [ ] `api_key` 있는 구매 요청 → 정상 동작
- [ ] `api_key` 없는 구매 요청 → 401
- [ ] 대시보드에서 에이전트 선택 후 구매 → 정상 (api_key 자동 전달)

---

### Phase 3: 프론트 — API 호출에 인증 헤더 추가

**파일:** `apps/web/lib/api.ts`

**변경 내용:**

1. 인증 헤더 헬퍼 함수 추가:
```ts
function authHeaders(): Record<string, string> {
  const token = typeof window !== 'undefined' ? localStorage.getItem('accessToken') : null
  return token ? { 'Authorization': `Bearer ${token}` } : {}
}
```

2. 3개 함수에 헤더 추가:
```
fetchAgents()     → headers에 authHeaders() 추가
registerAgent()   → headers에 authHeaders() 추가
deleteAgent()     → headers에 authHeaders() 추가
```

3. 나머지 함수 (purchaseConcept, followConcept, fetchBalance, fetchHistory, fetchLedger 등):
   - `api_key`를 body/query로 전달 → 에이전트 레벨 인증 → 변경 불필요

**테스트:**
- [ ] 로그인 안 한 상태에서 대시보드 열기 → 에이전트 목록 비어있거나 에러
- [ ] 로그인 후 대시보드 열기 → 내 에이전트만 보임
- [ ] 로그인 후 에이전트 등록 → 성공 + 내 user_id로 저장됨
- [ ] 로그인 후 에이전트 삭제 → 성공

---

### Phase 4: 프론트 — 비로그인 시 대시보드 접근 차단

**파일:** `apps/web/app/page.tsx` 또는 `apps/web/components/cherry/kaas-dashboard-page.tsx`

**변경 내용:**
대시보드 모달 열 때 `accessToken`이 없으면 로그인 페이지로 유도.

```
대시보드 버튼 클릭
  → accessToken 있음? → 대시보드 열기
  → accessToken 없음? → "로그인이 필요합니다" 메시지 + 로그인 버튼
```

**테스트:**
- [ ] 비로그인 상태에서 Dashboard 버튼 클릭 → 로그인 유도 메시지
- [ ] 로그인 후 Dashboard 버튼 클릭 → 정상 열림
- [ ] 로그인 후 에이전트 등록/구매/충전 → 전부 내 계정 기준

---

### Phase 5: 기존 데이터 처리

**문제:** 이미 `SYSTEM_USER_ID`로 등록된 에이전트들이 DB에 있음.

**방안:**
- 기존 에이전트는 그대로 둠 (SYSTEM_USER_ID 소유)
- 실제 사용자가 로그인하면 새로 등록
- 심사위원이 각자 로그인 → 각자 에이전트 등록 → 서로 안 보임

**테스트:**
- [ ] 기존 SYSTEM_USER_ID 에이전트는 아무도 접근 못 함 (유령 데이터)
- [ ] 새 사용자 로그인 → 에이전트 0개 → 새로 등록 → 정상

---

## 데이터 흐름 (변경 후)

```
[사용자 브라우저]
  1. solteti.site 접속
  2. Login 클릭 → 이메일 입력 → 매직링크 발송
  3. 이메일 클릭 → JWT 발급 → localStorage 저장

[대시보드]
  4. Dashboard 클릭 → accessToken 확인 → 대시보드 열림
  5. fetchAgents() → Authorization: Bearer <token> →
     서버: JWT 검증 → userId 추출 → findByUserId(userId) → 내 에이전트만 반환
  6. 에이전트 등록 → Authorization: Bearer <token> →
     서버: JWT 검증 → userId 추출 → register(userId, dto) → 내 user_id로 저장
  7. MetaMask 연결 → 지갑 주소 → 내 에이전트에 저장

[Claude Code 연결]
  8. 대시보드에서 MCP 명령어 복사 (내 api_key 포함)
  9. 터미널에서 실행 → cherry-agent 다운로드 + MCP 등록
  10. Claude Code에서 지식 구매 → api_key로 인증 → 내 에이전트 크레딧 차감

[다른 사용자]
  11. 다른 사용자는 4~10 동일 과정 → 완전히 분리된 에이전트/지갑/거래
```

## 변경 파일 요약

| Phase | 파일 | 변경 | 난이도 |
|---|---|---|---|
| 1 | `kaas-agent.controller.ts` | JWT guard + AuthUser + 소유권 체크 | 소 |
| 2 | `kaas-query.controller.ts` | SYSTEM_USER_ID fallback 제거 | 극소 |
| 2 | `kaas-credit.controller.ts` | SYSTEM_USER_ID fallback 제거 | 극소 |
| 3 | `apps/web/lib/api.ts` | authHeaders() + 3개 함수 헤더 추가 | 소 |
| 4 | `kaas-dashboard-page.tsx` | 비로그인 시 대시보드 접근 차단 | 극소 |

**총 5개 파일, 예상 시간: 30~40분**

## 위험 요소

1. **매직링크 이메일 발송**: Resend API 키(`RESEND_API_KEY`)가 `.env`에 있는지 확인 필요. 배포 서버에도 설정돼야 함.
2. **JWT 만료**: 토큰 만료 시 대시보드에서 자동 로그아웃 처리 필요 (현재 미구현이면 추가).
3. **CORS**: 배포 서버에서 로그인 API 호출 시 CORS 설정 확인 (현재 `CORS_ORIGINS`에 도메인 포함 필요).
4. **기존 에이전트 접근 불가**: `SYSTEM_USER_ID`로 등록된 에이전트는 로그인한 사용자 누구도 접근 못 함. 심사 전 데이터 정리 필요할 수 있음.

## 심사 시나리오

```
심사위원 A: solteti.site 접속 → 로그인 → 에이전트 "judge-A" 등록 → 200cr 자동 지급
심사위원 B: solteti.site 접속 → 로그인 → 에이전트 "judge-B" 등록 → 200cr 자동 지급
심사위원 A: 지식 구매 → 보고서 확인 → 심사위원 B의 에이전트/거래 안 보임
심사위원 B: 자기만의 에이전트/지갑/거래 확인 → 완전 개인화
```
