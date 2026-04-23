// Workshop — Mock data and types.
//
// 7 slots / 5 types stay in the UI; each card carries a unique "jigsaw" shape
// so a user can see at a glance which slot it belongs to (prompt ↔ circle,
// mcp ↔ square, skill ↔ triangle, orchestration ↔ diamond, memory ↔ hexagon).
//
// Agent Execution Flow (top → bottom):
//   ① System Prompt  → agent identity
//   ② MCP Tools      → callable tools
//   ③ Skills × 3     → domain knowledge (3 parallel slots)
//   ④ Orchestration  → execution control
//   ⑤ Memory         → state management
//
// Inventory is curated: only cards whose prompts / tools are wired end-to-end
// to /v1/kaas/bench/compare appear here. Skill + orchestration slots stay
// present (for future presets) even though no real cards fill them yet.

export type SkillType = "prompt" | "mcp" | "skill" | "orchestration" | "memory"

/** Diablo-style "set" tag — cards that share the same tag form an optimal
 *  combo. When all 3 cards of a set (prompt + mcp + memory) are equipped,
 *  the benchmark runs at peak effectiveness for that set's task. */
export type SetTag = "oracle" | "hunter" | "policy"

export interface SetMeta {
  label: string
  symbol: string  // short glyph (alchemy / tarot style)
  color: string
  softBg: string
}

export const SET_META: Record<SetTag, SetMeta> = {
  oracle: { label: "Oracle Set",   symbol: "🜂", color: "#8B6C2A", softBg: "#F5E9C8" },
  hunter: { label: "Hunter Set",   symbol: "🜄", color: "#8F1D12", softBg: "#F6D8D0" },
  policy: { label: "Policy Set",   symbol: "🜁", color: "#2D3B66", softBg: "#D8DEEF" },
}

export interface InventoryItem {
  id: string
  title: string
  type: SkillType
  category: string
  updatedAt: string // ISO date
  source: "purchased" | "followed" | "builtin" | "custom"
  sourceAgent?: string // For followed items: the originating agent's name
  summary?: string // Shown on card hover
  fileName?: string // For custom items: original uploaded filename
  content?: string // For custom items: raw text content (prompt body / config / etc.)
  /** Diablo-style set membership — matching tags = optimal combo. */
  setTag?: SetTag
}

export type SlotKey =
  | "prompt"
  | "mcp"
  | "skillA"
  | "skillB"
  | "skillC"
  | "orchestration"
  | "memory"

/** Step number in the Agent Execution Flow (1~5) */
export type FlowStep = 1 | 2 | 3 | 4 | 5

export interface SlotConfig {
  label: string
  accept: SkillType[]
  icon: string
  hint: string
  flowStep: FlowStep
  emptyLabel: string
}

/** An Agent Build — one saved slot configuration. Users keep multiple builds
 *  and switch between them via tabs. Each build has its own listing state. */
export interface AgentBuild {
  id: string
  name: string
  equipped: Record<SlotKey, string | null>
  isListedOnMarket: boolean
}

export interface WorkshopState {
  builds: AgentBuild[]
  activeBuildId: string
  inventory: InventoryItem[]
  isFollowingAny: boolean
  cloneSimilarity?: number
}

export function emptyEquipped(): Record<SlotKey, string | null> {
  return {
    prompt: null,
    mcp: null,
    skillA: null,
    skillB: null,
    skillC: null,
    orchestration: null,
    memory: null,
  }
}

export function makeBuild(id: string, name: string): AgentBuild {
  return { id, name, equipped: emptyEquipped(), isListedOnMarket: false }
}

export const SLOT_META: Record<SlotKey, SlotConfig> = {
  prompt: {
    label: "System Prompt",
    accept: ["prompt"],
    icon: "🧬",
    hint: "Defines the agent's role and discipline",
    flowStep: 1,
    emptyLabel: "Defines the agent's role and discipline",
  },
  mcp: {
    label: "MCP Tools",
    accept: ["mcp"],
    icon: "🛠",
    hint: "Tools the agent can call via MCP servers",
    flowStep: 2,
    emptyLabel: "Tools the agent can call via MCP servers",
  },
  skillA: {
    label: "Skill A",
    accept: ["skill"],
    icon: "✨",
    hint: "Primary domain knowledge",
    flowStep: 3,
    emptyLabel: "Primary domain knowledge",
  },
  skillB: {
    label: "Skill B",
    accept: ["skill"],
    icon: "✨",
    hint: "Secondary domain knowledge",
    flowStep: 3,
    emptyLabel: "Secondary domain knowledge",
  },
  skillC: {
    label: "Skill C",
    accept: ["skill"],
    icon: "✨",
    hint: "Tertiary domain knowledge",
    flowStep: 3,
    emptyLabel: "Tertiary domain knowledge",
  },
  orchestration: {
    label: "Orchestration",
    accept: ["orchestration"],
    icon: "🧭",
    hint: "Agent loop pattern (ReAct / CodeAct / Plan-and-Execute)",
    flowStep: 4,
    emptyLabel: "Agent loop pattern (ReAct / CodeAct / Plan-and-Execute)",
  },
  memory: {
    label: "Memory",
    accept: ["memory"],
    icon: "💾",
    hint: "Conversation-history retention policy",
    flowStep: 5,
    emptyLabel: "Conversation-history retention policy",
  },
}

/** Real inventory — every card maps 1:1 to a real server-side behavior.
 *  The 3 preset combinations that work end-to-end in bench:
 *    Oracle   = prompt:p-oracle  + mcp:m-crypto   + memory:me-short
 *    Hunter   = prompt:p-hunter  + mcp:m-market   + memory:me-none
 *    Policy   = prompt:p-policy  + mcp:m-catalog  + memory:me-retrieval
 */
export const mockInventory: InventoryItem[] = [
  // ── System Prompts (3) ──
  {
    id: "inv-p-oracle",
    title: "Market Oracle",
    type: "prompt",
    category: "Analyst",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "oracle",
    summary:
      "Crypto market analyst. Cites real prices with timestamp + source; never guesses.",
  },
  {
    id: "inv-p-hunter",
    title: "Marketplace Hunter",
    type: "prompt",
    category: "Extraction",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "hunter",
    summary:
      "Deal hunter that returns strict JSON listings; never invents records.",
  },
  {
    id: "inv-p-policy",
    title: "Policy Expert",
    type: "prompt",
    category: "Grounded",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "policy",
    summary:
      "Answers only from retrieved Cherry docs; cites doc IDs; says \"I don't have that\" when missing.",
  },

  // ── MCP Tools (3) ──
  {
    id: "inv-m-crypto",
    title: "Crypto Price",
    type: "mcp",
    category: "Finance",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "oracle",
    summary:
      "Live crypto prices via CoinGecko. Tool: get_crypto_price(symbol).",
  },
  {
    id: "inv-m-market",
    title: "Marketplace Search",
    type: "mcp",
    category: "Shopping",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "hunter",
    summary:
      "Internal marketplace DB. Tool: search_marketplace(query, max_price, sealed_only).",
  },
  {
    id: "inv-m-catalog",
    title: "Cherry Catalog",
    type: "mcp",
    category: "Docs",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "policy",
    summary:
      "Cherry internal policy docs. Tool: search_catalog(query, limit).",
  },

  // ── Memory modes (3) ──
  {
    id: "inv-me-none",
    title: "Stateless",
    type: "memory",
    category: "None",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "hunter",
    summary: "No retention — each turn starts fresh.",
  },
  {
    id: "inv-me-short",
    title: "Short-term",
    type: "memory",
    category: "Conversation",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "oracle",
    summary: "Full conversation context preserved within the session.",
  },
  {
    id: "inv-me-retrieval",
    title: "Retrieval buffer",
    type: "memory",
    category: "Tool output",
    updatedAt: "2026-04-23",
    source: "builtin",
    setTag: "policy",
    summary: "Retrieved tool results stay available across turns.",
  },
]

const DEFAULT_BUILDS: AgentBuild[] = [
  makeBuild("build-a", "Build A"),
  makeBuild("build-b", "Build B"),
  makeBuild("build-c", "Build C"),
]

export const defaultWorkshopState: WorkshopState = {
  builds: DEFAULT_BUILDS,
  activeBuildId: DEFAULT_BUILDS[0].id,
  inventory: mockInventory,
  isFollowingAny: false,
  cloneSimilarity: 0,
}

// v7: 7 slots restored, jigsaw shapes added, inventory still lean (9 real cards).
export const WORKSHOP_STORAGE_KEY = "cherry_workshop_state_v7"

/** Order of type filter buttons in the UI */
export const SKILL_TYPE_ORDER: SkillType[] = [
  "prompt",
  "mcp",
  "skill",
  "orchestration",
  "memory",
]
