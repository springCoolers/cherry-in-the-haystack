# NEAR 통합 기록

**작성일:** 2026-04-14
**상태:** Testnet 배포 완료 · 2건+ tx 기록 완료

---

## 1. 두 가지 NEAR 통합 레이어

Cherry KaaS는 NEAR 생태계와 **두 가지 서로 다른 레이어**로 연동됨.

| 레이어 | 대상 | 용도 | 상태 |
|---|---|---|---|
| **NEAR AI Cloud** | `https://cloud-api.near.ai/v1` | LLM 추론 (TEE 기반) | ✅ 완료 |
| **NEAR Protocol (L1)** | `rpc.testnet.fastnear.com` | 스마트 컨트랙트 (CherryCredit) | ✅ 완료 |

---

## 2. NEAR AI Cloud (LLM TEE)

### 환경변수 (서버)
| 변수 | 값 |
|---|---|
| `NEAR_AI_KEY` | `sk-c0e...` (API Key, Billing $5 한도) |

### 엔드포인트 & 모델
- Gateway: `https://cloud-api.near.ai/v1/chat/completions`
- 기본 모델: `Qwen/Qwen3-30B-A3B-Instruct-2507`
- 인증: OpenAI SDK 호환 (`Authorization: Bearer <KEY>`)

### 사용 지점
- `apps/api/src/modules/kaas/kaas-llm.controller.ts` — `provider === 'near'` 분기
- `apps/api/src/modules/kaas/kaas-query.controller.ts` — `llm/chat` 엔드포인트 `privacy_mode` 플래그

### Privacy Mode 라우팅
웹 대시보드 **Privacy Mode 토글** ON 시:
- 자유 대화 → NEAR AI가 직접 답변 생성
- 구매 content / 크레딧 intent / Compare knowledge → NEAR AI TEE **통과(relay)** 후 처리
- 응답 메시지에 🔒 NEAR AI TEE 배지 표시

### TEE 특성
- NEAR AI Cloud 모델이 **Trusted Execution Environment** 내부에서 실행
- 입력/출력이 클라우드 운영자에게 비공개
- 제출 요건(Story 7.2): "privacy-preserving knowledge consumption" ✅

---

## 3. NEAR Protocol L1 (CherryCredit 컨트랙트)

### 계정 & 컨트랙트
| 항목 | 값 |
|---|---|
| 네트워크 | **NEAR Testnet** |
| 계정 = 컨트랙트 주소 | `tomatojams.testnet` |
| Contract 코드 SHA-256 | `bc5860cddfed2f7e8e519f1e3445bbb04164fa1fcb0db35d0836469d09bf6d7a` |
| 계정 Explorer | https://testnet.nearblocks.io/address/tomatojams.testnet |
| 잔액 (배포 후) | ~9.99 NEAR |
| Storage used | 540.3 KB (컨트랙트 WASM 포함) |

### 배포 트랜잭션
| 항목 | 값 |
|---|---|
| TX ID | `HwTSRXMWJA5tWuLAw6n5YLKnhytm6McNJtxaTDwASJE9` |
| Explorer | https://testnet.nearblocks.io/txns/HwTSRXMWJA5tWuLAw6n5YLKnhytm6McNJtxaTDwASJE9 |
| Init 호출 | `init({ authorized_server: "tomatojams.testnet" })` |
| Gas burned | 4.2 Tgas |
| Fee | 0.00041682957955 NEAR |

### 온체인 테스트 tx (Submission 요건 2건+)
1. **deposit** — `{agent: "tomatojams.testnet", amount: "100"}` → `{newBalance: "100"}` ✅
2. **recordProvenance** — `{hash: "0xabcdef1234567890", agent: "tomatojams.testnet", conceptId: "rag"}` → `{recorded: true}` ✅

---

## 4. 컨트랙트 소스 & 빌드

### 파일 위치
```
apps/contracts-near/
├── package.json
├── src/
│   └── cherry_credit.ts          — near-sdk-js 컨트랙트
├── build/
│   └── cherry_credit.wasm        — 컴파일된 WASM (527 KB)
└── node_modules/
```

### 언어 & SDK
- **near-sdk-js v2.0.0** (TypeScript)
- Node.js v20.19.2
- WASM 컴파일: `npx near-sdk-js build src/cherry_credit.ts build/cherry_credit.wasm`

### 함수 시그니처
| 이름 | 타입 | 파라미터 | 반환 | 권한 |
|---|---|---|---|---|
| `init` | call | `{ authorized_server }` | — | 초기화 1회 |
| `deposit` | call | `{ agent, amount }` | `{ newBalance }` | onlyAuthorized |
| `consumeCredit` | call | `{ agent, amount, conceptId, actionType }` | `{ remainingBalance }` | onlyAuthorized |
| `distributeReward` | call | `{ curator, amount, conceptId }` | `{ newRewardBalance }` | onlyAuthorized |
| `recordProvenance` | call | `{ hash, agent, conceptId }` | `{ recorded }` | Open (하지만 hash는 1회만) |
| `getCredits` | view | `{ agent }` | `string` | Public |
| `getRewards` | view | `{ curator }` | `string` | Public |
| `verifyProvenance` | view | `{ hash }` | `boolean` | Public |

### 이벤트 (Logs)
Solidity의 `emit` 대체로 `near.log()` 사용:
- `CreditDeposited: <agent> +<amount> → <balance>`
- `CreditConsumed: <agent> -<amount> (<conceptId>/<actionType>) → <balance>`
- `RewardDistributed: <curator> +<amount> (<conceptId>) → <balance>`
- `ProvenanceRecorded: hash=<hash> agent=<agent> concept=<conceptId> ts=<timestamp>`

---

## 5. 툴체인 설치 기록

### near-cli-rs v0.25.0
```bash
npm install -g near-cli-rs
```

### 계정 Import (시드 구문)
```bash
near account import-account using-seed-phrase '<12 words>' \
  --seed-phrase-hd-path "m/44'/397'/0'" \
  network-config testnet
```

### 저장된 credential 위치
```
~/.near-credentials/testnet/tomatojams.testnet.json
~/.near-credentials/testnet/tomatojams.testnet/ed25519_8xqD7GLNKnvGo2ArQsc9VrYUMW8KntFqgTbCSpdRj83j.json
```

---

## 6. 배포/호출 스크립트 (재현용)

### 배포
```bash
cd apps/contracts-near
npx near-sdk-js build src/cherry_credit.ts build/cherry_credit.wasm

near contract deploy tomatojams.testnet \
  use-file build/cherry_credit.wasm \
  with-init-call init json-args '{"authorized_server":"tomatojams.testnet"}' \
  prepaid-gas '100.0 Tgas' \
  attached-deposit '0 NEAR' \
  network-config testnet \
  sign-with-legacy-keychain send
```

### deposit
```bash
near contract call-function as-transaction tomatojams.testnet deposit \
  json-args '{"agent":"tomatojams.testnet","amount":"100"}' \
  prepaid-gas '30 Tgas' attached-deposit '0 NEAR' \
  sign-as tomatojams.testnet network-config testnet \
  sign-with-legacy-keychain send
```

### recordProvenance
```bash
near contract call-function as-transaction tomatojams.testnet recordProvenance \
  json-args '{"hash":"0xabcdef1234567890","agent":"tomatojams.testnet","conceptId":"rag"}' \
  prepaid-gas '30 Tgas' attached-deposit '0 NEAR' \
  sign-as tomatojams.testnet network-config testnet \
  sign-with-legacy-keychain send
```

### 조회 (view)
```bash
near contract call-function as-read-only tomatojams.testnet getCredits \
  json-args '{"agent":"tomatojams.testnet"}' \
  network-config testnet now
```

---

## 7. 기획서 대조

### Story 7.2 요구사항 vs 구현
| 요구 | 구현 상태 |
|---|---|
| `chain-adapter/near-adapter.ts` | ⚠ 부분 (NEAR AI LLM만 적용, NEAR L1 adapter는 미구현 — 컨트랙트는 별도 CLI로 호출) |
| TEE 기반 추론 (OpenAI SDK drop-in) | ✅ `kaas-llm.controller.ts` 내 `provider='near'` 분기 |
| Privacy-preserving knowledge consumption 시연 | ✅ Privacy Mode 토글, 🔒 배지, 구매/Compare TEE 경유 |
| GitHub에 NEAR AI 통합 문서 | ✅ 이 문서 |

### 추가 확장 (기획서 외, 리서치 문서 아이디어)
| 항목 | 구현 상태 |
|---|---|
| `cherry_credit.ts` on near-sdk-js | ✅ 작성 |
| NEAR Testnet 배포 | ✅ `tomatojams.testnet` |
| 2+ on-chain tx | ✅ deploy + deposit + recordProvenance (3건) |

---

## 8. 제출 체크리스트

- [x] NEAR AI Cloud API 연동 (LLM 추론)
- [x] NEAR AI TEE 기반 privacy 데모 (Privacy Mode 토글)
- [x] NEAR Testnet에 CherryCredit 컨트랙트 배포
- [x] 온체인 tx 2건 이상
- [x] Explorer 링크 검증 가능
- [ ] README에 NEAR 통합 정보 추가
- [ ] 데모 영상 촬영 (privacy-preserving knowledge consumption 시연)
- [ ] (선택) `near-adapter.ts` API 통합 — CHAIN_ADAPTER=near 지원

---

## 9. 관련 파일

| 파일 | 역할 |
|---|---|
| `apps/contracts-near/src/cherry_credit.ts` | NEAR 컨트랙트 소스 (near-sdk-js) |
| `apps/contracts-near/build/cherry_credit.wasm` | 컴파일된 WASM |
| `apps/api/src/modules/kaas/kaas-llm.controller.ts` | NEAR AI LLM provider 라우팅 |
| `apps/api/src/modules/kaas/kaas-query.controller.ts` | `privacy_mode` 플래그 처리 |
| `apps/web/components/cherry/kaas-dashboard-page.tsx` | Privacy Mode 토글 UI |
| `apps/web/components/cherry/kaas-console.tsx` | 🔒 배지 & TEE relay 로직 |

---

## 10. 중요 보안 메모

- **시드 구문 노출 위험**: 본 프로젝트 개발 중 시드 구문이 스크린샷으로 공유됨 (테스트넷 한정 영향). 실제 메인넷 사용 시 반드시 로테이션.
- **DEPLOYER_PRIVATE_KEY (Status)**: 개인 MetaMask 계정 키 사용 중 — `remove-deployer-key-plan.md` 참조하여 전환 계획됨.
- **NEAR 계정 `tomatojams.testnet`**: Full access key 저장됨 (`~/.near-credentials/testnet/`). 본 키로 어떤 contract action도 가능.
