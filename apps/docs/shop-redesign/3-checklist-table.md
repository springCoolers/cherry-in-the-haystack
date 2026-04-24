# Shop Redesign — QA Checklist

> 구매가 "진짜" 작동하는지 end-to-end 검증. self-report = 유일한 진실.

---

## UI / UX

| # | 항목 | 합격 기준 |
|---|------|----------|
| U1 | Shop 메인 열기 | 도메인 탭 4개 + `ALL` 보임. 각 탭에 세트 hero 카드 1개. `ALL`은 4개 그리드 |
| U2 | 세트 hero 카드 | 슬롯 배지 색상이 Workshop TYPE_THEME와 **정확히 동일**. 슬롯 개수(N/7) 표시 |
| U3 | 도메인 탭 클릭 | 해당 도메인 세트만 필터. URL 상태 반영 여부는 선택 |
| U4 | 자세히 클릭 | 상세 모달 열림. 세트 구성 카드 6-7개 목록 + 각 낱개 Buy 버튼 + 하단 세트 Buy CTA |
| U5 | 상세 모달 → 낱개 Buy | PurchaseModal이 컴포넌트 모드로 열림 |
| U6 | 세트 Buy | PurchaseModal이 세트 모드로 열림. 로딩 메시지 "Installing N skills…" 순환 |
| U7 | Cherry 캐릭터 | idle/loading/success/error 4단계 표정 변화 정상 |

---

## 구매 · 낱개 (component)

| # | 항목 | 합격 기준 |
|---|------|----------|
| C1 | 낱개 구매 성공 | PurchaseModal success. 서버 응답에 `provenance.hash` 존재. `explorer_url` 클릭 가능 |
| C2 | Claude Code 자가 보고 | `~/.claude/skills/cherry-<slug>/SKILL.md` 생성 확인 (ls로 확인) |
| C3 | self-report 반영 | 구매 후 Shop 카탈로그의 OWNED 뱃지 즉시 점등 |
| C4 | 크레딧 차감 | 잔액이 정확히 -가격만큼 줄어듦 |
| C5 | 중복 구매 방지 | 이미 있는 카드 다시 Buy 시 "Already Owned" 표시 or 비활성 |
| C6 | 크레딧 부족 | 에러 토스트 "Not enough credits". PurchaseModal error phase |
| C7 | 에이전트 미연결 | 409 반환. "Agent offline — connect in Install Skill tab" 메시지 |

---

## 구매 · 세트 (set bundle)

| # | 항목 | 합격 기준 |
|---|------|----------|
| S1 | 세트 Buy 클릭 | PurchaseModal 열림. 총 가격이 **번들 할인 적용된 값** 표시 |
| S2 | 서버 `POST /sets/buy` | 200 응답. `installed[]`에 세트 슬롯 수(보통 6-7)만큼 항목 |
| S3 | Claude Code 측 | `~/.claude/skills/`에 **세트 구성 전부**(prompt/mcp/skill×N/orch/memory) + `cherry-build-meta` 생성 |
| S4 | self-report 전체 반영 | 상세 모달 재오픈 시 각 컴포넌트에 ✓ OWNED |
| S5 | Shop 카드 전체 OWNED | 세트 카드에 "OWNED" 또는 "Installed" 뱃지 |
| S6 | 크레딧 1회 차감 | N번 차감 아님. 번들 가격 1번만 |
| S7 | 부분 보유에서 세트 Buy | 이미 있는 것 skip, 없는 것만 새로 설치. 크레딧은 차액만 차감 |
| S8 | 번들 provenance | 체인 기록 **1건** (세트 단위 tx hash) 또는 명시적 N건 — 정책 결정 필요 |
| S9 | 한 개라도 설치 실패 | 207 Multi-Status. 성공 컴포넌트만 OWNED. 실패 목록 표시 |
| S10 | 활성화 프롬프트 | 성공 시 모달에 "cherry <tag> 로 ..." 복사 가능 명령어 (install-build와 동일) |

---

## Workshop 일관성

| # | 항목 | 합격 기준 |
|---|------|----------|
| W1 | 슬롯 배지 디자인 | Shop의 PROMPT/MCP/SKILL/ORCH/MEM 색·아이콘이 Workshop과 100% 동일 |
| W2 | 인벤토리 setTag 변경 시 | Shop 세트도 자동 재구성 (하드코딩 금지) |
| W3 | 세트 구매 후 Workshop 이동 | Workshop 빌드 슬롯에 자동 장착 여부 — 정책 결정 (강제 장착 vs 수동) |
| W4 | FULLSET 필터 vs Shop 세트 | 용어 통일 — 두 곳 다 "Full Set" 또는 "Complete AI" 택일 |

---

## 데이터 정합성

| # | 항목 | 합격 기준 |
|---|------|----------|
| D1 | OWNED 소스 | 오직 self-report `local_skills.items` 기반. DB `agent.knowledge` fuzzy match 사용 금지 |
| D2 | 파일 수동 삭제 후 | `~/.claude/skills/cherry-*` 삭제 + Claude Code 재시작 → Shop OWNED 전부 해제 |
| D3 | 다른 에이전트 전환 | OWNED 뱃지가 해당 에이전트 기준으로 갱신 |
| D4 | 실제 체인 기록 | chain="status" 기본. tx hash 가 진짜 Status Sepolia 에 존재 (explorer 조회 성공) |

---

## 회귀 / 기타

| # | 항목 | 합격 기준 |
|---|------|----------|
| R1 | 메인 사이트 (`/`) Shop | 건드리지 않음 — KaasCatalogPage 기존 동작 유지 |
| R2 | Workshop 설치 플로우 | 변경 없음. Phase 2 서버 작업이 기존 install-build 에 영향 없어야 |
| R3 | Benchmark 탭 | Shop 변경으로 영향 없음 |
| R4 | TS 컴파일 | `npx tsc --noEmit` 0 에러 (기존 미해결 에러 제외) |
| R5 | Hydration | SSR/CSR mismatch 경고 없음 |

---

## 데모 시나리오 (심사자)

1. Shop 열기 → 4개 세트 보임
2. Quant 탭 → hero 카드 클릭 "자세히"
3. 상세 모달에서 구성 확인 (6-7개 컴포넌트)
4. "Buy set" → Cherry 로딩 → "✓ Installed on 클로드"
5. Transaction 링크 클릭 → Status Sepolia explorer 열림
6. 모달 닫기 → 세트 카드에 OWNED 뱃지
7. Install Skill 탭에서 Live proof → 6-7개 cherry-* 디렉토리 확인
8. Claude Code에서 `cherry quant 로 Compare BTC, ETH, SOL...` → 정상 동작
