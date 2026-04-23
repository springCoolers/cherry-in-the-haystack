/**
 * Card registry — maps every inventory card id the frontend can equip to
 * its concrete server-side implementation.
 *
 * For Phase 1 (3 slots wired end-to-end):
 *   - 3 prompt cards  → raw system prompt strings
 *   - 3 mcp cards     → concrete BenchTool instances
 *   - 3 memory cards  → tool-use iteration caps
 *
 * Phase 2 (later): add skill + orchestration cards with real semantics.
 * Until then, those slots are inert — composeRuntime simply ignores them.
 */

import { coingeckoTool } from '../tools/coingecko.tool'
import { marketplaceTool } from '../tools/marketplace.tool'
import { catalogTool } from '../tools/catalog.tool'
import type { BenchTool } from '../tools/tool-registry'

export type CardType = 'prompt' | 'mcp' | 'memory'

export type MemoryMode = 'none' | 'short' | 'retrieval'

export interface PromptCardImpl {
  type: 'prompt'
  systemPrompt: string
}

export interface McpCardImpl {
  type: 'mcp'
  tool: BenchTool
}

export interface MemoryCardImpl {
  type: 'memory'
  mode: MemoryMode
  maxIterations: number
}

export type CardImpl = PromptCardImpl | McpCardImpl | MemoryCardImpl

export const CARD_REGISTRY: Record<string, CardImpl> = {
  /* ══════════ System prompts ══════════ */
  'inv-p-oracle': {
    type: 'prompt',
    systemPrompt:
      "You are a crypto market analyst. Always cite current prices with a timestamp and source. Never guess — if you don't have a tool result, say so.",
  },
  'inv-p-hunter': {
    type: 'prompt',
    systemPrompt:
      'You are a deal-hunting assistant. Return exactly 3 listings as valid JSON: [{id, title, price, seller, posted_at}]. Use only the search tool — do not invent listings. No prose outside the JSON.',
  },
  'inv-p-policy': {
    type: 'prompt',
    systemPrompt:
      'Answer only using retrieved Cherry docs. Cite doc IDs in brackets like [doc:karma-v2]. If the answer is not in retrieved docs, respond exactly: "I don\'t have that information."',
  },

  /* ══════════ MCP tools ══════════ */
  'inv-m-crypto': { type: 'mcp', tool: coingeckoTool },
  'inv-m-market': { type: 'mcp', tool: marketplaceTool },
  'inv-m-catalog': { type: 'mcp', tool: catalogTool },

  /* ══════════ Memory modes ══════════ */
  'inv-me-none': {
    type: 'memory',
    mode: 'none',
    maxIterations: 1, // single shot — Claude must answer in one go, no retry
  },
  'inv-me-short': {
    type: 'memory',
    mode: 'short',
    maxIterations: 5, // standard tool-use loop
  },
  'inv-me-retrieval': {
    type: 'memory',
    mode: 'retrieval',
    maxIterations: 10, // extended loop, more room to retrieve + reflect
  },
}

export function getCard(id: string | null | undefined): CardImpl | null {
  if (!id) return null
  return CARD_REGISTRY[id] ?? null
}
