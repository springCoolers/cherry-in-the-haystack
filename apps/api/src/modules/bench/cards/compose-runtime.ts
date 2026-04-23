/**
 * Build → runtime composer.
 *
 * Takes a user's equipped AgentBuild (which card ids are in which slots) and
 * produces the concrete runtime config the Anthropic client needs:
 *   - systemPrompt (string | undefined — baseline-style when absent)
 *   - tools[] (tool definitions + dispatcher)
 *   - maxIterations (from memory card, defaults to 5 when absent)
 *
 * Phase 1: only prompt / mcp / memory slots are honored. skill and
 * orchestration slots are accepted but have no runtime effect (no cards
 * exist for them yet).
 */

import { buildToolDispatcher, type BenchTool } from '../tools/tool-registry'
import type { AnthropicToolSchema } from '../sets/set-definitions'
import { getCard, type MemoryMode } from './card-registry'

export interface AgentBuildInput {
  prompt: string | null
  mcp: string | null
  skillA: string | null
  skillB: string | null
  skillC: string | null
  orchestration: string | null
  memory: string | null
}

export interface RuntimeConfig {
  systemPrompt: string | undefined
  tools: AnthropicToolSchema[]
  toolDispatcher?: (
    name: string,
    input: Record<string, unknown>,
  ) => Promise<unknown>
  maxIterations: number
  memoryMode: MemoryMode
  /** Diagnostic: which slots actually contributed something. */
  appliedSlots: {
    prompt: boolean
    mcp: boolean
    memory: boolean
    skillsIgnored: number
    orchestrationIgnored: boolean
  }
}

/** Default when memory slot is empty — same as `short`. */
const DEFAULT_MAX_ITER = 5
const DEFAULT_MEMORY_MODE: MemoryMode = 'short'

export function composeRuntime(build: AgentBuildInput): RuntimeConfig {
  // ── Prompt ──
  const promptCard = getCard(build.prompt)
  const systemPrompt =
    promptCard?.type === 'prompt' ? promptCard.systemPrompt : undefined

  // ── MCP tool ──
  const mcpCard = getCard(build.mcp)
  const benchTools: BenchTool[] =
    mcpCard?.type === 'mcp' ? [mcpCard.tool] : []
  const tools = benchTools.map((t) => t.definition)
  const toolDispatcher =
    benchTools.length > 0 ? buildToolDispatcher(benchTools) : undefined

  // ── Memory ──
  const memCard = getCard(build.memory)
  const maxIterations =
    memCard?.type === 'memory' ? memCard.maxIterations : DEFAULT_MAX_ITER
  const memoryMode =
    memCard?.type === 'memory' ? memCard.mode : DEFAULT_MEMORY_MODE

  // ── Phase-1 ignored slots (future: skill / orchestration) ──
  const skillsIgnored = [build.skillA, build.skillB, build.skillC].filter(
    Boolean,
  ).length
  const orchestrationIgnored = Boolean(build.orchestration)

  return {
    systemPrompt,
    tools,
    toolDispatcher,
    maxIterations,
    memoryMode,
    appliedSlots: {
      prompt: Boolean(promptCard),
      mcp: Boolean(mcpCard),
      memory: Boolean(memCard),
      skillsIgnored,
      orchestrationIgnored,
    },
  }
}
