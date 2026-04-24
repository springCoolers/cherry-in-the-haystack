/**
 * serialize — pure-function unit tests for Workshop → SKILL.md conversion.
 *
 * No Claude API. No Nest bootstrap. No filesystem writes. Run with:
 *   cd apps/api && npx ts-node --transpile-only src/modules/bench/cards/serialize.test.ts
 */

import {
  cardToSkillFile,
  buildMetaSkillFile,
  collectSkillFiles,
  toSavePayload,
  type BuildContext,
} from './serialize'
import type { AgentBuildInput } from './compose-runtime'

let passed = 0
let failed = 0

function ok(label: string, cond: boolean, detail?: string) {
  if (cond) {
    passed++
    console.log('  ✓', label)
  } else {
    failed++
    console.log('  ✗', label, detail ? `— ${detail}` : '')
  }
}

function section(title: string) {
  console.log('\n' + '─'.repeat(70))
  console.log(title)
  console.log('─'.repeat(70))
}

function ctx(overrides: Partial<BuildContext> = {}): BuildContext {
  return {
    buildId: 'build-a',
    buildName: 'Build A',
    agentId: 'clx12345678',
    installedAt: '2026-04-24T06:30:00Z',
    runId: 'abc12345',
    ...overrides,
  }
}

function emptyEquipped(): AgentBuildInput {
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

/* ══════════ Test 1: prompt card → SKILL.md ══════════ */
section('Test 1 — prompt card (inv-p-oracle)')
{
  const f = cardToSkillFile('prompt', 'inv-p-oracle', ctx())
  ok('returns SkillFile', f !== null)
  if (f) {
    ok('dir is cherry-p-oracle', f.dir === 'cherry-p-oracle')
    ok('file is SKILL.md', f.file === 'SKILL.md')
    ok('name is Market Oracle', f.name === 'Market Oracle')
    ok('description starts with "Crypto"', f.description.startsWith('Crypto'))
    ok('body contains cherry-workshop comment', f.body.includes('<!-- cherry-workshop'))
    ok('body contains card_id', f.body.includes('card_id: inv-p-oracle'))
    ok('body contains slot', f.body.includes('slot: prompt'))
    ok('body contains systemPrompt content', f.body.includes('crypto market analyst'))
    ok('slot is prompt', f.slot === 'prompt')
    ok('cardId is inv-p-oracle', f.cardId === 'inv-p-oracle')
  }
}

/* ══════════ Test 2: skill card → SKILL.md ══════════ */
section('Test 2 — skill card (inv-s-json-strict) in skillB slot')
{
  const f = cardToSkillFile('skillB', 'inv-s-json-strict', ctx())
  ok('returns SkillFile', f !== null)
  if (f) {
    ok('dir is cherry-s-json-strict', f.dir === 'cherry-s-json-strict')
    ok('name is JSON Strict', f.name === 'JSON Strict')
    ok('slot is skillB', f.slot === 'skillB')
    ok('body contains promptSuffix', /pure JSON/i.test(f.body))
  }
}

/* ══════════ Test 3: mcp slot returns null ══════════ */
section('Test 3 — mcp slot always returns null')
{
  const f = cardToSkillFile('mcp', 'inv-m-crypto', ctx())
  ok('returns null for mcp slot', f === null)
}

/* ══════════ Test 4: orchestration slot returns null ══════════ */
section('Test 4 — orchestration slot always returns null')
{
  const f = cardToSkillFile('orchestration', 'inv-o-plan-execute', ctx())
  ok('returns null for orchestration slot', f === null)
}

/* ══════════ Test 5: memory slot returns null ══════════ */
section('Test 5 — memory slot always returns null')
{
  const f = cardToSkillFile('memory', 'inv-me-short', ctx())
  ok('returns null for memory slot', f === null)
}

/* ══════════ Test 6: unknown card id returns null ══════════ */
section('Test 6 — unknown card id (inv-x-bogus)')
{
  const f = cardToSkillFile('prompt', 'inv-x-bogus', ctx())
  ok('returns null for unknown card id', f === null)
}

/* ══════════ Test 7: buildMetaSkillFile ══════════ */
section('Test 7 — buildMetaSkillFile with full equip')
{
  const equipped: AgentBuildInput = {
    prompt: 'inv-p-oracle',
    mcp: 'inv-m-crypto',
    skillA: 'inv-s-decomp',
    skillB: null,
    skillC: null,
    orchestration: 'inv-o-plan-execute',
    memory: 'inv-me-short',
  }
  const f = buildMetaSkillFile(equipped, ctx())
  ok('returns SkillFile', f !== null)
  if (f) {
    ok('dir is cherry-build-meta', f.dir === 'cherry-build-meta')
    ok('file is SKILL.md', f.file === 'SKILL.md')
    ok('name is Build meta', f.name === 'Build meta')
    ok('description mentions Build A', f.description.includes('Build A'))
    ok('description mentions 5 slots', f.description.includes('5 slots'))
    ok('body contains build_id', f.body.includes('build_id: build-a'))
    ok('body contains prompt slot id', f.body.includes('prompt: inv-p-oracle'))
    ok('body contains null skillB', f.body.includes('skillB: null'))
    ok('body contains orchestration_id', f.body.includes('orchestration_id: plan-execute'))
    ok('body contains memory_mode', f.body.includes('memory_mode: short'))
    ok('body contains memory_max_iterations', f.body.includes('memory_max_iterations: 5'))
    ok('slot is _meta', f.slot === '_meta')
  }
}

/* ══════════ Test 8: empty equipped → buildMetaSkillFile null ══════════ */
section('Test 8 — empty build → buildMetaSkillFile returns null')
{
  const f = buildMetaSkillFile(emptyEquipped(), ctx())
  ok('returns null for empty build', f === null)
}

/* ══════════ Bonus: collectSkillFiles happy path ══════════ */
section('Test 9 — collectSkillFiles aggregates correctly')
{
  const equipped: AgentBuildInput = {
    prompt: 'inv-p-oracle',
    mcp: 'inv-m-crypto',
    skillA: 'inv-s-decomp',
    skillB: 'inv-s-json-strict',
    skillC: null,
    orchestration: 'inv-o-plan-execute',
    memory: 'inv-me-short',
  }
  const r = collectSkillFiles(equipped, ctx())
  ok('files.length === 3 (prompt + 2 skills)', r.files.length === 3)
  ok('files[0].slot === prompt', r.files[0]?.slot === 'prompt')
  ok('files[1].slot === skillA', r.files[1]?.slot === 'skillA')
  ok('skipped.length === 3 (mcp + orch + memory)', r.skipped.length === 3)
  ok(
    'mcp reason mentions "claude mcp add"',
    r.skipped.find((s) => s.slot === 'mcp')?.reason.includes('claude mcp add') ?? false,
  )
  ok(
    'orchestration reason is "merged into build-meta"',
    r.skipped.find((s) => s.slot === 'orchestration')?.reason === 'merged into build-meta',
  )
}

/* ══════════ Bonus: toSavePayload shape ══════════ */
section('Test 10 — toSavePayload produces gateway-compatible payload')
{
  const f = cardToSkillFile('prompt', 'inv-p-oracle', ctx())
  if (!f) {
    ok('SkillFile created', false)
  } else {
    let counter = 0
    const makeRequestId = () => `req-${++counter}`
    const p = toSavePayload(f, makeRequestId)
    ok('request_id is req-1', p.request_id === 'req-1')
    ok('concept_id is cherry-workshop-inv-p-oracle', p.concept_id === 'cherry-workshop-inv-p-oracle')
    ok('title === name', p.title === 'Market Oracle')
    ok('summary === description', p.summary === f.description)
    ok('content_md === body', p.content_md === f.body)
    ok('target_dir starts with ~/.claude/skills/', p.target_dir.startsWith('~/.claude/skills/'))
    ok('target_file ends with SKILL.md', p.target_file.endsWith('SKILL.md'))
  }
}

/* ══════════ Bonus: meta toSavePayload concept_id ══════════ */
section('Test 11 — toSavePayload for _meta uses pre-computed cardId as concept_id')
{
  const equipped: AgentBuildInput = {
    ...emptyEquipped(),
    prompt: 'inv-p-oracle',
  }
  const meta = buildMetaSkillFile(equipped, ctx())
  if (!meta) {
    ok('meta SkillFile created', false)
  } else {
    const p = toSavePayload(meta, () => 'req-meta')
    ok(
      'concept_id starts with cherry-workshop-meta-',
      p.concept_id.startsWith('cherry-workshop-meta-'),
    )
    ok('does NOT have double cherry-workshop- prefix', !p.concept_id.startsWith('cherry-workshop-cherry-'))
    ok('target_dir is ~/.claude/skills/cherry-build-meta', p.target_dir === '~/.claude/skills/cherry-build-meta')
  }
}

/* ══════════ Summary ══════════ */
console.log('\n' + '═'.repeat(70))
console.log(`  ${passed} passed · ${failed} failed`)
console.log('═'.repeat(70))
if (failed > 0) process.exit(1)
