# Shop Redesign — Implementation Guide

> 1-work-guidelines.md 의 C2 drill-down + 진짜 구매 플로우를 구현하는 단계별 순서

---

## Phase 0 — 기반 (30 min)

### 0-1. `apps/web/lib/shop-sets.ts` 생성

```typescript
import { mockInventory, type SetTag, SET_META } from "./workshop-mock"
import type { AgentBuildInput } from "@/lib/bench-api"

export interface ShopSet {
  id: string
  domain: SetTag
  title: string
  subtitle: string
  icon: string
  equipped: AgentBuildInput
  priceBundled: number
  priceSum: number
  qualityScore: number
  installs: number
}

// Workshop buildForSet 로직과 1:1 일치 — 인벤토리 setTag 변경 시 자동 반영
function equippedForDomain(tag: SetTag): AgentBuildInput {
  const first = (t: string) =>
    mockInventory.find((i) => i.type === t && i.setTag?.includes(tag))?.id ?? null
  const skills = mockInventory
    .filter((i) => i.type === "skill" && i.setTag?.includes(tag))
    .slice(0, 3)
  return {
    prompt: first("prompt"),
    mcp: first("mcp"),
    skillA: skills[0]?.id ?? null,
    skillB: skills[1]?.id ?? null,
    skillC: skills[2]?.id ?? null,
    orchestration: first("orchestration"),
    memory: first("memory"),
  }
}

const DOMAIN_META: Record<SetTag, { title: string; subtitle: string; icon: string }> = {
  hunter:   { title: "Shopping AI",  subtitle: "Marketplace deal hunter",         icon: "🛍" },
  quant:    { title: "Quant AI",     subtitle: "Multi-asset crypto analyst",       icon: "💹" },
  research: ... // grounded/policy 각각 정의
}

export const SHOP_SETS: ShopSet[] = (Object.keys(SET_META) as SetTag[]).map((tag) => {
  const equipped = equippedForDomain(tag)
  const slots = Object.values(equipped).filter(Boolean).length
  const priceSum = slots * 18  // 평균 낱개 가격 × 슬롯 수 (간이)
  return {
    id: `set-${tag}`,
    domain: tag,
    ...DOMAIN_META[tag],
    equipped,
    priceBundled: Math.round(priceSum * 0.85), // 15% 번들 할인
    priceSum,
    qualityScore: 4.6,
    installs: 100 + Math.floor(Math.random() * 500),
  }
})
```

### 0-2. Component 가격 정의

- `workshop-mock.ts` 의 `InventoryItem` 에 `priceCredits?: number` 추가 (optional)
- 기본값: type별 기본 가격 (prompt=20, mcp=25, skill=15, orch=10, memory=8)

---

## Phase 1 — Shop 프론트 (2h)

### 1-1. `ShopSetCard` 컴포넌트

```tsx
// apps/web/components/cherry/shop-set-card.tsx
export function ShopSetCard({ set, onBuy, onInspect }: {
  set: ShopSet
  onBuy: () => void
  onInspect: () => void
}) {
  const slots = Object.values(set.equipped).filter(Boolean).length
  return (
    <article className="rounded-2xl border p-5 bg-white shadow-sm hover:shadow-md">
      <header className="flex items-start justify-between">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">{set.icon}</span>
            <h3 className="text-[18px] font-extrabold text-[#3A2A1C]">{set.title}</h3>
          </div>
          <p className="text-[12px] text-[#6B4F2A] mt-1">{set.subtitle}</p>
        </div>
        <span className="text-[10px] font-bold text-[#9A7C55]">{slots}/7</span>
      </header>

      {/* slot-type 배지 바 (Workshop TYPE_THEME 재사용) */}
      <div className="flex gap-1 mt-3">{/* PROMPT / MCP / SKILL×3 / ORCH / MEM */}</div>

      <div className="flex items-center gap-3 mt-4">
        <button onClick={onBuy} className="...">Buy set — {set.priceBundled} cr</button>
        <button onClick={onInspect} className="...">자세히 →</button>
      </div>
    </article>
  )
}
```

### 1-2. `ShopSetDetailModal` 컴포넌트

- `set.equipped` 순회 → InventoryItem lookup → 슬롯 배지 + 이름 + 설명 + 낱개 Buy
- 하단: 전체 세트 Buy CTA

### 1-3. Shop 페이지 재작성

```tsx
// apps/web/app/start/shop/page.tsx
export default function ShopPage() {
  const [domain, setDomain] = useState<"all" | SetTag>("all")
  const [inspectSet, setInspectSet] = useState<ShopSet | null>(null)
  const [buyTarget, setBuyTarget] = useState<PurchaseTarget | null>(null)

  const visible = domain === "all" ? SHOP_SETS : SHOP_SETS.filter((s) => s.domain === domain)

  return (
    <div>
      <header>...</header>
      <DomainTabs value={domain} onChange={setDomain} />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {visible.map((s) => (
          <ShopSetCard key={s.id} set={s}
            onBuy={() => setBuyTarget({ kind: "set", set: s })}
            onInspect={() => setInspectSet(s)} />
        ))}
      </div>
      {inspectSet && (
        <ShopSetDetailModal set={inspectSet} onClose={() => setInspectSet(null)}
          onBuySet={() => { setInspectSet(null); setBuyTarget({ kind: "set", set: inspectSet }) }}
          onBuyComponent={(cardId, price) => { setBuyTarget({ kind: "component", cardId, price }) }} />
      )}
      <PurchaseModal open={!!buyTarget} ... />
    </div>
  )
}
```

---

## Phase 2 — 서버 신규 엔드포인트 (2h)

### 2-1. `apps/api/src/modules/kaas/buy-set.controller.ts`

```typescript
@Controller('v1/kaas/sets')
export class BuySetController {
  constructor(private readonly buySet: BuySetService) {}

  @Post('buy')
  async buy(@Body() body: { set_id: string; api_key: string; chain?: string }) {
    return this.buySet.execute(body.set_id, body.api_key, body.chain ?? 'status')
  }
}
```

### 2-2. `BuySetService.execute()`

```
1. set_id → equipped 배열 resolve (shop-sets 서버 쪽 미러 — 하드코딩 금지, setTag 기반)
2. 번들 가격 계산 + 크레딧 충분 확인
3. 단일 트랜잭션으로 크레딧 차감
4. agent_id lookup via api_key
5. 각 component에 대해:
   - serialize.ts 의 cardToSkillFile() 호출 → SKILL.md 생성
   - WS save_skill_request 전송
6. 구매 기록 knowledge 테이블에 각 component_id 저장
7. provenance on-chain 기록 (chain 선택 로직 메인 사이트와 동일)
8. 응답: { installed: [...], provenance, credits_consumed }
```

### 2-3. Nest 모듈 등록

- `kaas.module.ts` 의 controllers 배열에 `BuySetController` 추가
- providers 배열에 `BuySetService` 추가
- 필요 의존성: `KaasWsGateway`, `KaasAgentService`, `CreditsService`, `ChainService`

---

## Phase 3 — 프론트 API wrapper (30 min)

### 3-1. `apps/web/lib/api.ts`

```typescript
export async function buySet(
  apiKey: string,
  setId: string,
  chain: "status" | "near" = "status",
) {
  const res = await fetch(`${KAAS_BASE}/sets/buy`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ set_id: setId, api_key: apiKey, chain }),
  })
  if (!res.ok) throw new Error(`buySet ${res.status}: ${await res.text()}`)
  return res.json()
}
```

### 3-2. PurchaseModal 분기

- `PurchaseTarget` union 확장: `{ kind: "component", ... } | { kind: "set", set: ShopSet }`
- `handleConfirm` 에서 kind 별 분기 — `purchaseConcept()` vs `buySet()`
- 로딩 메시지 세트 모드용 별도 풀 (`"Installing 6 skills…"` 등)

---

## Phase 4 — OWNED 갱신 (기존 로직 재사용, 15 min)

- 구매 성공 후 `window.dispatchEvent(new CustomEvent("kaas-purchase-complete"))` — 기존과 동일
- Shop 페이지의 세트 카드에 "✓ OWNED" 오버레이 추가 (component 전부 보유 시)
- 부분 보유: "4/7 installed" 배지

---

## Phase 5 — QA (1h) — checklist-table.md 참조

- 세트 구매 → Claude Code self-report 에서 4-6개 디렉토리 확인
- 낱개 구매 → 해당 하나만 생성
- 크레딧 부족 → 에러 토스트
- 에이전트 미연결 → 409 처리 (기존 install-build 와 동일 패턴)
- 세트 부분 보유 상태에서 세트 buy → 이미 있는 건 skip, 없는 것만 설치

---

## 작업 순서 (권장)

1. Phase 0 — shop-sets.ts + component 가격
2. Phase 1 — 프론트 UI (서버 없이 mock 반환으로 먼저 렌더 확인)
3. Phase 2 — 서버 엔드포인트 + serialize 재사용
4. Phase 3 — 프론트-서버 연결
5. Phase 4 — OWNED 뱃지 통합
6. Phase 5 — 전체 플로우 QA

총 예상 시간: 6-7시간
