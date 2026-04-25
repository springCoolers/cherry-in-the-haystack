# Agent Trade — Work Guidelines

> 작성: 2026-04-25
> 범위: `/start/shop` 에 **By Agent** 탭 추가. 다른 에이전트의 지식과 내 지식을 **diff** 한 뒤 부족한 항목을 **구매**.
> 선행: `install-skill/`, `shop-redesign/` 4문서 (Shop / InstallBuildService / self-report 기반 OWNED).

---

## 1. 목적

- 데모 시나리오: 두 Claude Code 인스턴스 (예: Mac/Linux). 각자 다른 SKILL.md 세트 보유. 한 쪽이 상대 지식 둘러보고 부족한 것 구매.
- 핵심: **상대방 지식 파일 ↔ 내 지식 파일 비교** → 차이점 시각화 → **구매로 채우기**.
- 교환(exchange) 은 **이번 스코프 제외** — 구매만.

---

## 2. UX

### 2-1. Shop 의 세 번째 큰 탭

```
┌──────────────────────────────────────────────────────┐
│ By Domain  │  By Component  │  By Agent  ← 신규     │
└──────────────────────────────────────────────────────┘
```

### 2-2. By Agent 탭 — 에이전트 목록

```
[Listing Agents on Cherry]                             [My agent: Claude (Mac) ▼]

┌──────────────────────────┐  ┌──────────────────────────┐
│ Bob's Claude (Linux)     │  │ Alice's GPT              │
│ 🥈 Silver · 12 skills    │  │ 🥉 Bronze · 7 skills     │
│ Has 5 skills you don't   │  │ Has 2 skills you don't   │
│  [View knowledge →]      │  │  [View knowledge →]      │
└──────────────────────────┘  └──────────────────────────┘
```

- 자기 자신은 목록에서 제외 (또는 흐림 처리)
- 우상단에 **My agent** 셀렉터 — 내가 어느 에이전트 기준으로 비교할지 선택
- 카드 한눈에 보이는 정보:
  - 에이전트 이름 / Karma tier / 보유 스킬 개수 / **"내가 모르는 것 N개"** ← diff 결과 미리보기

### 2-3. 에이전트 상세 모달 — Knowledge Diff

```
Bob's Claude · Knowledge Diff vs My Claude

┌─ Both have (3) ──────────────────────────────────┐
│  ✓ A-MEM    ✓ Quant set    ✓ JSON Strict         │
└──────────────────────────────────────────────────┘

┌─ Only Bob has — buyable (5) ────────────────────┐
│  📚 Self-Repair Loop          [Buy 30cr]         │
│  📚 Active Context Curation   [Buy 30cr]         │
│  📚 RLoT Reasoning            [Buy 30cr]         │
│  🎁 Hunter set                [Buy 60cr]         │
│  🎁 Research set              [Buy 90cr]         │
└──────────────────────────────────────────────────┘

┌─ Only my Claude has (2) ────────────────────────┐
│  · Citation Discipline                           │
│  · Plan-and-Execute                              │
└──────────────────────────────────────────────────┘
```

- 3 컬럼/3 섹션 구조: **Both / Only Theirs (Buyable) / Only Mine (Reference)**
- "Only Theirs" 만 Buy 버튼 노출
- 각 항목 클릭 시 카드 소스 모달 (이미 있는 `CardSourceModal` 재사용 가능)

### 2-4. 구매 플로우

- Buy 클릭 → 기존 **PurchaseModal** 재사용 (set 모드 또는 component 모드)
- 항목 종류에 따라 분기:
  - **Shop set** (id `set-*`) → `buySet` 호출 (기존 `/shop/buy-and-install`)
  - **Knowledge concept** (UUID id `019dac...`) → 기존 `purchaseConcept`
  - **Workshop card** (id `inv-*`) → 단일 카드 install 경로 필요 (없으면 set 으로 감싸 재사용)

---

## 3. 데이터 모델 — 새 데이터 거의 없음

### 3-1. 진실의 원천

- **에이전트의 지식 = self-report 의 `local_skills.items[]`** (install-skill 시점부터 확립된 패턴 그대로)
- DB 의 `agent.knowledge` JSONB 는 보조 정보 (퍼지 매칭에 안 씀, 이미 컨텍스트에서 드롭)

### 3-2. ShopAgent 응답 (서버 신규)

```typescript
interface ShopAgent {
  id: string
  name: string
  ownerName: string         // user.name (개인정보 제한적 노출)
  karmaTier: string
  skillCount: number
  /** self-report 기반 cherry-* 디렉토리 슬러그 배열 */
  ownedSlugs: string[]
}
```

### 3-3. AgentDiff 응답 (서버 신규)

```typescript
interface AgentDiff {
  me: { id: string; ownedSlugs: string[] }
  them: { id: string; ownedSlugs: string[] }
  /** 양쪽 다 보유 — 표시만, 액션 없음 */
  both: DiffItem[]
  /** 상대만 보유 — 구매 가능 후보 */
  onlyTheirs: BuyableDiffItem[]
  /** 나만 보유 — 표시만 */
  onlyMine: DiffItem[]
}

interface DiffItem {
  slug: string              // "cherry-019dac01-1111-..." 의 슬러그 부분
  cardId: string            // "set-quant" / "019dac01-..." / "inv-p-hunter"
  title: string
  summary: string
  kind: "set" | "concept" | "card"
}

interface BuyableDiffItem extends DiffItem {
  /** 구매 경로 + 가격 (서버가 결정) */
  purchase: {
    endpoint: "shop/buy-and-install" | "purchase"
    price: number
    body: Record<string, unknown>  // 그대로 fetch 본문에 사용
  }
}
```

### 3-4. 슬러그 → 종류 분류 규칙

서버가 `cherry-<slug>` 폴더명에서 종류 판별:
- `cherry-set-<tag>` (또는 `cherry-build-meta` + meta 안의 build_id 가 `set-*`) → **set**
- `cherry-019dac…` (UUID 패턴) → **concept** (KaasCatalog)
- `cherry-p-…`, `cherry-s-…`, `cherry-m-…`, `cherry-o-…`, `cherry-me-…` → **card** (Workshop 컴포넌트)
- 그 외 → **unknown** (UI 에서 구매 비활성, 표시만)

---

## 4. 구매 플로우 — 기존 재사용

### 4-1. set 종류

`POST /v1/kaas/shop/buy-and-install` 그대로 — `set_id` 만 다른 슬러그.

### 4-2. concept 종류

`POST /v1/kaas/purchase` 그대로 — `concept_id`.

### 4-3. card 종류 (Workshop 컴포넌트 단품)

현재는 단일 카드 구매 경로 없음 (Shop 의 By Component 는 보기 전용). 두 옵션:
- **A. 카드 단품도 set 으로 감싸 install** — 새 endpoint `POST /shop/buy-card-and-install` (단일 카드를 7슬롯 중 해당 슬롯에 넣은 1슬롯 미니 set 으로 처리)
- **B. card 종류는 이번 스코프에서 구매 불가, 표시만** — UX 단순화

→ **추천 B** (이번 스코프). 데모는 `set-*` + `019dac…` concept 두 종류로 충분.

### 4-4. 결제 후 검증

- 기존 `kaas-purchase-complete` window 이벤트 dispatch
- diff 결과 자동 갱신 (Compare 재실행) — 산 항목이 "Only Theirs" → "Both" 로 이동
- self-report 도 자동 호출되어 OWNED 뱃지 갱신

---

## 5. 신규 API

| Method | Path | 목적 |
|--------|------|------|
| `GET`  | `/v1/kaas/shop/agents?exclude_self=ck_live_…` | 거래 가능 에이전트 목록 (skillCount 포함). `exclude_self` 는 자기 에이전트 빼기 |
| `GET`  | `/v1/kaas/shop/agents/:id/diff?vs_api_key=ck_live_…` | 두 에이전트 지식 diff |

서버는 양쪽 에이전트의 self-report 를 fetch (or 마지막 캐시) 후 `local_skills.items` 비교.

**미연결 에이전트 처리**: 상대방이 오프라인이면 마지막 self-report 캐시 사용 — 없으면 `unavailable` 반환.

---

## 6. 파일 영향 범위

### 신규 (server)
- `apps/api/src/modules/kaas/shop/agent-trade.controller.ts`
- `apps/api/src/modules/kaas/shop/agent-trade.service.ts`
- `apps/api/src/modules/kaas/shop/skill-classifier.ts` — 슬러그 → kind 분류 + 가격 + 구매 경로 결정

### 신규 (web)
- `apps/web/components/cherry/shop-by-agent.tsx` — 큰 탭 콘텐츠
- `apps/web/components/cherry/shop-agent-card.tsx`
- `apps/web/components/cherry/shop-agent-diff-modal.tsx` — Both/Only Theirs/Only Mine 3섹션
- `apps/web/lib/api.ts` — `fetchShopAgents()`, `fetchAgentDiff()`

### 수정
- `apps/web/app/start/shop/page.tsx` — 큰 탭 3개로 확장 (By Domain / By Component / **By Agent**)
- `apps/api/src/modules/kaas/kaas.module.ts` — Controller/Service 등록

---

## 7. Workshop / 기존 Shop 과의 일관성

| 항목 | 기존 Shop | By Agent 탭 |
|------|-----------|-------------|
| 슬롯/카드 색 | TYPE_THEME | **재사용** |
| OWNED 판단 | self-report | **동일 — diff 의 핵심 입력** |
| 구매 후 갱신 | `kaas-purchase-complete` 이벤트 | **재사용** |
| 자동 장착 | 없음 | **없음** (Shop 영역 일관) |

---

## 8. 비범위

- 교환 (exchange / swap) — 다음 스코프
- 카드 단품 구매 (Workshop 컴포넌트만 따로 사기)
- 가격 협상 / 리스팅 — 시스템 고정가만
- 에이전트 평가/리뷰
- 차단/신고

---

## 9. 결정 기록

| # | 결정 | 이유 |
|---|------|------|
| D1 | 진실은 self-report | 기존 패턴 일관, DB drift 회피 |
| D2 | 구매 종류는 set + concept 두 가지만 | 카드 단품은 별도 인프라 필요, 이번 데모 핵심 아님 |
| D3 | 가격은 서버가 결정 | 사용자별 협상 없음, 데모 단순화 |
| D4 | 미연결 에이전트는 마지막 캐시 | 양쪽 동시 온라인 강제 비현실적 |
| D5 | 자기 자신 제외 | UX 노이즈 방지, exclude_self 쿼리 파라미터로 명시 |
| D6 | 큐레이터 보상은 기존 `KaasCuratorRewardService` 그대로 | 신규 분배 로직 만들지 않음 |
