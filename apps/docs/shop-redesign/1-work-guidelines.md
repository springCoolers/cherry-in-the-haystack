# Shop Redesign — Work Guidelines

> 작성: 2026-04-25
> 범위: `/start/shop` 소비자 대상 마켓플레이스 재구성
> 선행: `install-skill/` 4문서 참고 (설치 플로우, SKILL.md 직렬화)

---

## 1. 목적

- **현재 문제**: Shop이 밋밋한 단일 그리드. 카드 종류 구분 없음. 구매해도 Workshop 슬롯과 매핑 안 됨.
- **목표 1**: 일반인이 "내 AI 뭐 시킬까?" → **도메인별 완성품(세트)** 한 번 클릭으로 설치.
- **목표 2**: Workshop과 **용어·슬롯 구조가 일관**되게 유지. 개별 카드 구매도 가능 (빌더용).
- **목표 3**: **구매 = 진짜 다운로드**. 서버 구매 확정 → 에이전트에 SKILL.md 저장 → self-report 로 목록 반영. 가짜 UI 금지.

---

## 2. UX — C2 drill-down 방식 확정

### 2-1. Shop 메인 화면

- 상단 탭: `[ALL] [🛍 Shopping] [💹 Quant] [📚 Research] [📜 Policy]`
- 각 탭 = **풀세트 hero 카드 1개**만 표시 (도메인당 완성형 AI)
- `ALL` = 4개 세트 전부 그리드

### 2-2. 세트 hero 카드 구성

```
┌─────────────────────────────────┐
│ 🎁 Quant AI  [7/7]              │
│ 암호화폐 다중자산 분석가          │
│ [PROMPT][MCP][SKILL×3][ORCH][MEM]│ ← 슬롯 배지
│ ⋆⋆⋆⋆⋆ 4.6  · 127 installs       │
│                                  │
│ [Buy set — 120 cr] [자세히 →]   │
└─────────────────────────────────┘
```

- 배지 = Workshop 슬롯 아이콘과 **동일 색·동일 라벨** (PROMPT/MCP/SKILL/ORCH/MEM)
- Buy set 클릭 → **세트 구매 모달** (character-driven, 기존 PurchaseModal 재사용)
- 자세히 클릭 → **세트 상세 모달** (아래)

### 2-3. 세트 상세 모달

```
┌──────────────────────────────────┐
│ Quant AI 세트 구성                │
│ ─────────────────────────────    │
│ [PROMPT] Quantitative Analyst    │
│   다중자산 분석 역할              │
│   15 cr  [낱개 Buy]               │
│                                   │
│ [MCP] Crypto Price                │
│   CoinGecko 가격 조회             │
│   20 cr  [낱개 Buy]               │
│                                   │
│ [SKILL] JSON Strict               │
│   10 cr  [낱개 Buy]               │
│ …                                 │
│ ─────────────────────────────    │
│ [전체 세트 한 번에 Buy — 120 cr] │
│ (5% 번들 할인 포함)               │
└──────────────────────────────────┘
```

- 각 항목 = 슬롯 배지 + 이름 + 한 줄 설명 + 낱개 가격 + Buy
- 맨 아래 = 세트 일괄 구매 CTA (할인 적용된 가격)
- 상세 모달 안에서 개별 구매 가능 → 빌더 니즈도 충족

---

## 3. 데이터 모델

### 3-1. Shop이 파는 3종

| 유형 | 설명 | 예시 |
|------|------|------|
| **Set product** | Workshop 풀세트 = prompt+mcp+skills+orch+mem 묶음 | Quant AI, Hunter AI |
| **Component product** | 낱개 슬롯 카드 1개 | Quant prompt, Crypto MCP |
| **Knowledge concept** | 기존 A-MEM/RLoT 등 연구 논문 | 별도 "Knowledge" 탭 or 제거 (결정 필요) |

### 3-2. Set product 정의

```typescript
interface ShopSet {
  id: string              // "set-quant", "set-hunter" ...
  domain: DomainTag       // "quant" | "hunter" | "research" | "policy"
  title: string           // "Quant AI"
  subtitle: string        // "암호화폐 다중자산 분석가"
  icon: string            // "💹"
  equipped: AgentBuildInput  // prompt + mcp + skills + orch + memory 슬롯 맵
  priceBundled: number    // 120 (할인 적용)
  priceSum: number        // 126 (낱개 합, 표시용)
  qualityScore: number    // 4.6
  installs: number        // 127
}
```

- **도메인 `quant` ↔ Workshop `setTag: ["quant"]`** 자동 매칭 → 인벤토리 변경 시 Shop도 자동 반영
- `ShopSet.equipped` = Workshop `buildForSet(tag)` 로직과 동일 — 하드코딩 금지

### 3-3. Component product

- `InventoryItem` 재사용 — 각 카드에 `priceCredits` 필드 추가
- 카테고리 필터는 도메인(setTag) 기반, 탭 안에서 slot-type으로 2차 정렬 가능

---

## 4. 구매 플로우 — 진짜 다운로드 + 자가 보고

### 4-1. Component (낱개) 구매

1. 사용자가 낱개 Buy 클릭
2. PurchaseModal → `POST /api/v1/kaas/purchase` (기존 API 재사용)
3. 서버: 크레딧 차감 + provenance 기록 + WebSocket `save_skill_request` 에이전트에 전송
4. 에이전트: `~/.claude/skills/cherry-<slug>/SKILL.md` 파일 생성 + `save_skill_ack` 응답
5. 서버가 응답 통합 후 프론트에 반환
6. 프론트: **`kaas-purchase-complete`** + **`kaas-self-report`** 이벤트 dispatch
7. Shop의 Compare 로직이 OWNED 뱃지 즉시 갱신

### 4-2. Set (묶음) 구매

**서버 신규 엔드포인트**: `POST /api/v1/kaas/sets/buy`
```json
{
  "set_id": "set-quant",
  "api_key": "ck_live_...",
  "chain": "status"
}
```

서버 내부:
1. `ShopSet.equipped` 로 7슬롯 카드 id 배열 resolve
2. 각 슬롯 카드에 해당하는 component purchase 순차 실행 (트랜잭션)
3. 번들 할인 적용 후 총 크레딧 차감 1회
4. `save_skill_request` 여러 번 → 에이전트에 각 SKILL.md 저장
5. `cherry-build-meta` SKILL.md 도 저장 (Install 플로우와 동일)
6. 응답: `installed[]` + 통합 provenance + 총 차감 크레딧

프론트:
- Set 구매 시 동일 PurchaseModal 재사용 (문자열만 "Set installation" 등으로 분기)
- 성공 시 `kaas-self-report` 이벤트 → Compare 재실행 → 4-6개 OWNED 뱃지 동시 점등

### 4-3. 검증 — self-report가 유일한 진실

- 구매 완료 ≠ 설치 완료. 반드시 에이전트의 `local_skills.items` 에 새 항목이 떴는지 확인.
- PurchaseModal success phase: 서버 응답의 `installed[]` 개수 + self-report 재조회 후 매칭 개수를 같이 표시.
- 불일치 시 에러 메시지: "구매됐지만 에이전트 설치 실패. 에이전트 재시작 후 재시도하세요."

---

## 5. 파일 영향 범위

### 신규
- `apps/web/components/cherry/shop-set-card.tsx` — hero 카드 컴포넌트
- `apps/web/components/cherry/shop-set-detail-modal.tsx` — 자세히 모달
- `apps/web/lib/shop-sets.ts` — ShopSet 정의 (setTag → equipped 파생)
- `apps/api/src/modules/kaas/buy-set.controller.ts` — 서버 신규 엔드포인트
- `apps/api/src/modules/kaas/buy-set.service.ts` — 세트 구매 오케스트레이션

### 수정
- `apps/web/app/start/shop/page.tsx` — KaasCatalogPage 대신 새 ShopGrid
- `apps/web/components/cherry/purchase-modal.tsx` — set mode 분기 추가
- `apps/web/lib/api.ts` — `buySet()` 함수 추가
- `apps/web/components/cherry/kaas-catalog-page.tsx` — 지금 Shop 위에 얹힌 상태 → Shop에서 분리, 메인 사이트 전용으로 유지

### 삭제/이동
- Shop에서 knowledge concepts 분리. 옵션:
  - A: `/start/shop`에 두 번째 탭 "Papers"
  - B: 완전 제거 (심사용 단순화)
  - C: 유지 — "ALL" 탭에만 세트 아래 섹션으로

---

## 6. Workshop과의 일관성 (사용자 요구)

| 항목 | Workshop | Shop |
|------|----------|------|
| 슬롯 아이콘/색 | 기존 TYPE_THEME | **동일 재사용** |
| 도메인 매핑 | `setTag: ["quant"]` | 동일 태그로 세트 정의 |
| 풀세트 설치 | Fullset Equip 버튼 | Buy set 버튼 (구매 후 자동 설치) |
| OWNED 판단 | self-report 기반 | **동일** (kaas-self-report 이벤트 공유) |
| 구매 명령어 활성화 | cherry <tag> 로 ... | **동일** 복사 프롬프트 (세트 구매 성공 시 모달에 표시) |

---

## 7. 비범위 (이번 스코프 제외)

- Knowledge concept 큐레이션 편집 (별도 기획)
- 다국어 (전부 영어 고정)
- 세트 커스터마이즈 (= Workshop 담당)
- Shop 내 "내가 산 것" 보관함 (→ 에이전트 self-report로 대체)
