/**
 * Workshop build → Claude Code SKILL.md serializer.
 *
 * Turns an `equipped` slot map (`{prompt, mcp, skillA, skillB, skillC,
 * orchestration, memory}` of card ids) into the payloads the WebSocket
 * save_skill_request flow already understands ([kaas-ws.gateway.ts:427]).
 *
 * Per `apps/docs/install-skill/1-work-guidelines.md`:
 *   - prompt / skill  cards → ~/.claude/skills/cherry-{p|s}-<short>/SKILL.md
 *   - mcp              card → no file (tool is activated via `claude mcp add`)
 *   - orchestration + memory → folded into cherry-build-meta/SKILL.md
 *   - Frontmatter is STRICTLY `name` + `description` (Claude Code compat).
 *     Custom metadata goes in a `<!-- cherry-workshop ... -->` comment block.
 */

import { CARD_REGISTRY } from './card-registry'
import type { AgentBuildInput } from './compose-runtime'
import type { SaveSkillRequestPayload } from '../../kaas/kaas-ws.gateway'

/** Extended slot key: regular equip slots + a synthetic `_meta` for the
 *  build summary SKILL.md. */
export type ExtSlotKey =
  | 'prompt'
  | 'mcp'
  | 'skillA'
  | 'skillB'
  | 'skillC'
  | 'orchestration'
  | 'memory'
  | '_meta'

export interface SkillFile {
  slot: ExtSlotKey
  /** Original card id (`inv-p-oracle`) or synthetic id for meta files. */
  cardId: string
  /** Directory relative to `~/.claude/skills/`, e.g. `cherry-p-oracle`. */
  dir: string
  /** Filename inside dir — always `SKILL.md` in this system. */
  file: string
  /** Frontmatter `name`. */
  name: string
  /** Frontmatter `description`. */
  description: string
  /** Body written after the frontmatter (includes `<!-- -->` meta comment). */
  body: string
}

export interface BuildContext {
  buildId: string
  buildName: string
  agentId: string
  installedAt: string
  runId: string
}

export interface SkipEntry {
  slot: string
  card_id: string | null
  reason: string
}

/** Card metadata (title + summary) — duplicated from
 *  `apps/web/lib/workshop-mock.ts` because the backend needs name/description
 *  for the SKILL.md frontmatter. Keep these in sync manually; see the
 *  inventory list in workshop-mock.ts for the source of truth. */
const CARD_METADATA: Record<string, { name: string; description: string }> = {
  // prompts
  'inv-p-oracle': {
    name: 'Market Oracle',
    description:
      'Crypto market analyst. Cites real prices with timestamp + source; never guesses.',
  },
  'inv-p-hunter': {
    name: 'Marketplace Hunter',
    description:
      'Deal hunter that returns strict JSON listings; never invents records.',
  },
  'inv-p-policy': {
    name: 'Policy Expert',
    description:
      'Answers only from retrieved Cherry docs; cites doc IDs; says "I don\'t have that" when missing.',
  },
  'inv-p-quant': {
    name: 'Quantitative Analyst',
    description:
      'Multi-asset analyst that fetches each price, compares movement, identifies biggest mover.',
  },
  'inv-p-grounded': {
    name: 'Grounded Researcher',
    description:
      'Retrieves docs first, cites doc IDs, flags missing fields — never invents.',
  },
  // skills
  'inv-s-decomp': {
    name: 'Multi-step Decomposition',
    description:
      'Break tasks into explicit subtasks; require a numeric "step" field per entity.',
  },
  'inv-s-json-strict': {
    name: 'JSON Strict',
    description:
      'Output ONLY valid JSON matching the requested schema. No prose, no fences.',
  },
  'inv-s-citation': {
    name: 'Citation Discipline',
    description:
      'Every factual claim carries an inline source + timestamp tag.',
  },
  'inv-s-multihop': {
    name: 'Multi-hop Retrieval',
    description:
      'One targeted search per sub-question, never a single broad query.',
  },
  'inv-s-abstention': {
    name: 'Abstention Discipline',
    description:
      'If a field is not in retrieved docs, flag it missing — never invent.',
  },
}

const SLOT_DIR_PREFIX: Partial<Record<ExtSlotKey, string>> = {
  prompt: 'cherry-p-',
  skillA: 'cherry-s-',
  skillB: 'cherry-s-',
  skillC: 'cherry-s-',
}

const META_DIR = 'cherry-build-meta'

/** Strip the `inv-[pms]-` prefix. `inv-p-oracle` → `oracle`. */
function shortId(cardId: string): string {
  return cardId.replace(/^inv-[pms]-/, '')
}

/** Build a `<!-- cherry-workshop ... -->` block with simple YAML-ish key:val
 *  pairs. Claude Code frontmatter parser ignores HTML comments, so this is
 *  safe to ship alongside the body. */
function commentMeta(fields: Record<string, unknown>): string {
  const lines: string[] = []
  for (const [k, v] of Object.entries(fields)) {
    if (v === null || v === undefined) {
      lines.push(`${k}: null`)
    } else if (typeof v === 'object') {
      lines.push(`${k}:`)
      for (const [k2, v2] of Object.entries(v as Record<string, unknown>)) {
        lines.push(`  ${k2}: ${v2 === null || v2 === undefined ? 'null' : String(v2)}`)
      }
    } else {
      lines.push(`${k}: ${String(v)}`)
    }
  }
  return `<!-- cherry-workshop\n${lines.join('\n')}\n-->\n\n`
}

/**
 * Convert one equip slot + card id into a SkillFile. Returns `null` when:
 *   - slot is mcp / orchestration / memory (handled elsewhere),
 *   - cardId is null / empty,
 *   - card id is unknown (caller may record in `failed[]`),
 *   - card type doesn't match the slot (edge case).
 */
export function cardToSkillFile(
  slot: 'prompt' | 'skillA' | 'skillB' | 'skillC' | 'mcp' | 'orchestration' | 'memory',
  cardId: string | null,
  ctx: BuildContext,
): SkillFile | null {
  if (slot === 'mcp' || slot === 'orchestration' || slot === 'memory') return null
  if (!cardId) return null

  const card = CARD_REGISTRY[cardId]
  if (!card) return null

  const meta = CARD_METADATA[cardId]
  if (!meta) return null

  const prefix = SLOT_DIR_PREFIX[slot]
  if (!prefix) return null

  let contentText = ''
  if (card.type === 'prompt' && slot === 'prompt') {
    contentText = card.systemPrompt
  } else if (card.type === 'skill' && slot !== 'prompt') {
    contentText = card.promptSuffix
  } else {
    // card type doesn't match the slot (e.g. skill card in prompt slot)
    return null
  }

  const body =
    commentMeta({
      card_id: cardId,
      slot,
      build_id: ctx.buildId,
      agent_id: ctx.agentId,
      installed_at: ctx.installedAt,
      run_id: ctx.runId,
    }) + contentText

  return {
    slot,
    cardId,
    dir: prefix + shortId(cardId),
    file: 'SKILL.md',
    name: meta.name,
    description: meta.description,
    body,
  }
}

/** Assemble the synthetic `cherry-build-meta/SKILL.md` summarizing the whole
 *  build. Returns `null` if every slot is empty (caller should 400). */
export function buildMetaSkillFile(
  equipped: AgentBuildInput,
  ctx: BuildContext,
): SkillFile | null {
  const equippedCount = Object.values(equipped).filter(Boolean).length
  if (equippedCount === 0) return null

  const orchCard = equipped.orchestration ? CARD_REGISTRY[equipped.orchestration] : null
  const memCard = equipped.memory ? CARD_REGISTRY[equipped.memory] : null

  const orchestrationId =
    orchCard?.type === 'orchestration' ? orchCard.orchId : null
  const memoryMode = memCard?.type === 'memory' ? memCard.mode : null
  const memoryMaxIter = memCard?.type === 'memory' ? memCard.maxIterations : null

  const datePart = ctx.installedAt.slice(0, 10)
  const description = `Workshop build installed ${datePart} · ${ctx.buildName} · ${equippedCount} slot${equippedCount === 1 ? '' : 's'} equipped.`

  const body =
    commentMeta({
      type: 'build-meta',
      build_id: ctx.buildId,
      build_name: ctx.buildName,
      agent_id: ctx.agentId,
      installed_at: ctx.installedAt,
      run_id: ctx.runId,
      slots: equipped as unknown as Record<string, unknown>,
      orchestration_id: orchestrationId,
      memory_mode: memoryMode,
      memory_max_iterations: memoryMaxIter,
    }) +
    'This skill file records which Workshop build was installed to this agent. Not a functional skill — metadata only.'

  return {
    slot: '_meta',
    cardId: `cherry-workshop-meta-${ctx.buildId}-${ctx.agentId.slice(0, 8)}`,
    dir: META_DIR,
    file: 'SKILL.md',
    name: 'Build meta',
    description,
    body,
  }
}

/** Walk the equip slots, collect SkillFiles for prompt/skillA/B/C, and
 *  record mcp/orchestration/memory as `skipped[]` entries with a reason. */
export function collectSkillFiles(
  equipped: AgentBuildInput,
  ctx: BuildContext,
): { files: SkillFile[]; skipped: SkipEntry[] } {
  const files: SkillFile[] = []
  const skipped: SkipEntry[] = []

  const slots: Array<'prompt' | 'skillA' | 'skillB' | 'skillC'> = [
    'prompt',
    'skillA',
    'skillB',
    'skillC',
  ]
  for (const slot of slots) {
    const cardId = equipped[slot]
    if (!cardId) continue // empty slot — neither saved nor skipped
    const file = cardToSkillFile(slot, cardId, ctx)
    if (file) files.push(file)
    // unknown card id → caller records in `failed[]` when this returns null
  }

  if (equipped.mcp) {
    skipped.push({
      slot: 'mcp',
      card_id: equipped.mcp,
      reason:
        'mcp slot — referenced by id only (tool activation handled by `claude mcp add`)',
    })
  }
  if (equipped.orchestration) {
    skipped.push({
      slot: 'orchestration',
      card_id: equipped.orchestration,
      reason: 'merged into build-meta',
    })
  }
  if (equipped.memory) {
    skipped.push({
      slot: 'memory',
      card_id: equipped.memory,
      reason: 'merged into build-meta',
    })
  }

  return { files, skipped }
}

/** Convert a SkillFile to the payload shape `KaasWsGateway.requestSaveSkill`
 *  already expects ([kaas-ws.gateway.ts:427]). Synthetic `concept_id` per
 *  install-skill §4-4 so the existing DB record flow stays unchanged. */
export function toSavePayload(
  file: SkillFile,
  makeRequestId: () => string,
): SaveSkillRequestPayload {
  const conceptId =
    file.slot === '_meta'
      ? file.cardId // pre-computed: cherry-workshop-meta-<buildId>-<agentShort>
      : `cherry-workshop-${file.cardId}`
  const targetDir = `~/.claude/skills/${file.dir}`
  const targetFile = `${targetDir}/${file.file}`

  return {
    request_id: makeRequestId(),
    concept_id: conceptId,
    title: file.name,
    summary: file.description,
    content_md: file.body,
    target_dir: targetDir,
    target_file: targetFile,
  }
}
