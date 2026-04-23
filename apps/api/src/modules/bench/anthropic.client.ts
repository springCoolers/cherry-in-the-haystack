/**
 * Anthropic Claude client with a tool-use loop.
 *
 * Single entry point `callClaude()` supports both:
 *   - baseline calls (no system prompt, no tools) — returns model text directly
 *   - enhanced calls (system + tools + dispatcher) — runs the tool-use loop
 *     until the model returns `stop_reason: "end_turn"` or the safety cap is hit
 *
 * All tool calls are captured in `toolCalls` for logging + evaluation.
 */

import Anthropic from '@anthropic-ai/sdk'

import type { AnthropicToolSchema } from './sets/set-definitions'

export const DEFAULT_MODEL = 'claude-haiku-4-5'

let sharedClient: Anthropic | null = null
function getClient(): Anthropic {
  if (!sharedClient) {
    const apiKey = process.env.ANTHROPIC_API_KEY
    if (!apiKey) {
      throw new Error(
        '[bench] ANTHROPIC_API_KEY is not set. Add it to apps/api/.env',
      )
    }
    sharedClient = new Anthropic({ apiKey })
  }
  return sharedClient
}

export interface ToolCallRecord {
  name: string
  input: Record<string, unknown>
  output?: unknown
  error?: string
  durationMs: number
}

export interface ClaudeCallInput {
  messages: Array<{ role: 'user' | 'assistant'; content: string }>
  system?: string
  tools?: AnthropicToolSchema[]
  toolDispatcher?: (
    name: string,
    input: Record<string, unknown>,
  ) => Promise<unknown>
  model?: string
  maxTokens?: number
  temperature?: number
  maxToolIterations?: number
}

export interface ClaudeCallResult {
  text: string
  stopReason: string | null
  usage: {
    inputTokens: number
    outputTokens: number
    totalTokens: number
  }
  toolCalls: ToolCallRecord[]
  latencyMs: number
  model: string
  iterations: number
}

/** Safety cap — prevents runaway tool loops if the model never converges. */
const DEFAULT_MAX_TOOL_ITERATIONS = 5

export async function callClaude(
  input: ClaudeCallInput,
): Promise<ClaudeCallResult> {
  const client = getClient()
  const model = input.model ?? DEFAULT_MODEL
  const maxTokens = input.maxTokens ?? 1024
  const temperature = input.temperature ?? 0
  const maxIter = input.maxToolIterations ?? DEFAULT_MAX_TOOL_ITERATIONS
  const wantsTools = Array.isArray(input.tools) && input.tools.length > 0

  const started = Date.now()
  const toolCalls: ToolCallRecord[] = []
  let inputTokens = 0
  let outputTokens = 0
  let iterations = 0

  // Mutable working copy of the conversation.
  const conversation: Array<
    Anthropic.Messages.MessageParam
  > = input.messages.map((m) => ({ role: m.role, content: m.content }))

  let stopReason: string | null = null
  let finalText = ''

  // eslint-disable-next-line no-constant-condition
  while (true) {
    iterations++

    const res = await client.messages.create({
      model,
      max_tokens: maxTokens,
      temperature,
      ...(input.system ? { system: input.system } : {}),
      ...(wantsTools ? { tools: input.tools } : {}),
      messages: conversation,
    })

    inputTokens += res.usage?.input_tokens ?? 0
    outputTokens += res.usage?.output_tokens ?? 0
    stopReason = res.stop_reason ?? null

    const textParts = res.content.filter(
      (c): c is Anthropic.Messages.TextBlock => c.type === 'text',
    )
    const toolUseBlocks = res.content.filter(
      (c): c is Anthropic.Messages.ToolUseBlock => c.type === 'tool_use',
    )

    // Keep the LAST textual answer as our response text.
    const lastText = textParts.map((p) => p.text).join('\n').trim()
    if (lastText) finalText = lastText

    // No more tool calls or we're out of the tools regime — done.
    if (
      stopReason !== 'tool_use' ||
      toolUseBlocks.length === 0 ||
      !input.toolDispatcher ||
      iterations >= maxIter
    ) {
      break
    }

    // Append the assistant turn (unchanged, as SDK requires).
    conversation.push({ role: 'assistant', content: res.content })

    // Execute all tool calls in parallel and build tool_result blocks.
    const results = await Promise.all(
      toolUseBlocks.map(async (tu) => {
        const callStarted = Date.now()
        try {
          const out = await input.toolDispatcher!(
            tu.name,
            (tu.input ?? {}) as Record<string, unknown>,
          )
          const rec: ToolCallRecord = {
            name: tu.name,
            input: (tu.input ?? {}) as Record<string, unknown>,
            output: out,
            durationMs: Date.now() - callStarted,
          }
          toolCalls.push(rec)
          return {
            type: 'tool_result' as const,
            tool_use_id: tu.id,
            content: JSON.stringify(out),
          }
        } catch (err) {
          const msg = err instanceof Error ? err.message : String(err)
          toolCalls.push({
            name: tu.name,
            input: (tu.input ?? {}) as Record<string, unknown>,
            error: msg,
            durationMs: Date.now() - callStarted,
          })
          return {
            type: 'tool_result' as const,
            tool_use_id: tu.id,
            content: `Error: ${msg}`,
            is_error: true,
          }
        }
      }),
    )

    // Feed the tool_result back as a user turn.
    conversation.push({ role: 'user', content: results })
  }

  return {
    text: finalText,
    stopReason,
    usage: {
      inputTokens,
      outputTokens,
      totalTokens: inputTokens + outputTokens,
    },
    toolCalls,
    latencyMs: Date.now() - started,
    model,
    iterations,
  }
}
