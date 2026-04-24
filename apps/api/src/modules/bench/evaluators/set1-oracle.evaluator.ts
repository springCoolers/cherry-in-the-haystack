/**
 * SET 1 — Market Oracle evaluator.
 *
 * Scores answers on real-time factual grounding. Metrics:
 *   - Task completion (did the answer include a usable price number?)
 *   - Price error % (|claimed − truth| / truth * 100, worst across claimed numbers)
 *   - Hallucinated numbers (numbers that don't match any fetched tool value)
 *   - Citation count (timestamp / source mentions)
 *   - Groundedness (did tools actually fire?)
 */

import { fetchCryptoPrice, type CryptoPriceResult } from '../tools/coingecko.tool'
import type {
  EvalContext,
  EvalResult,
  Evaluator,
  Metric,
} from './types'

interface GroundTruth {
  prices: CryptoPriceResult[]
  fetchedAt: string
}

/**
 * Captures ground truth at evaluation time.
 * For a fair comparison, both baseline and enhanced are judged against the same snapshot.
 */
export async function captureOracleGroundTruth(
  symbols: string[],
): Promise<GroundTruth> {
  const prices = await Promise.all(symbols.map((s) => fetchCryptoPrice(s)))
  return { prices, fetchedAt: new Date().toISOString() }
}

/** Extract $-prefixed or comma-separated USD-looking numbers from text. */
function extractDollarAmounts(text: string): number[] {
  // Match: $80,734  $80734.50  $80734  $80.7k  80,000 USD  etc
  const pattern = /\$?\s?([\d]{1,3}(?:,\d{3})+|\d{3,})(?:\.\d+)?/g
  const out: number[] = []
  for (const m of text.matchAll(pattern)) {
    const clean = m[1].replace(/,/g, '')
    const n = parseFloat(clean)
    if (!Number.isNaN(n) && n >= 100) out.push(n) // filter tiny ints like years
  }
  return out
}

function closestPercentError(claimed: number, truth: number): number {
  return Math.abs(claimed - truth) / truth * 100
}

export const set1OracleEvaluator: Evaluator = {
  id: 'set-1-oracle',
  async evaluate(ctx: EvalContext): Promise<EvalResult> {
    const gt = ctx.groundTruth as GroundTruth
    const answer = ctx.answer ?? ''
    const metrics: Metric[] = []

    // ── Extract prices the answer claims ──
    const allNumbers = extractDollarAmounts(answer)

    // We only care about numbers that could plausibly be a price CLAIM for
    // the tracked symbol(s). Derived numbers (half of BTC, fiat totals, etc.)
    // share the same magnitude but aren't claims about the asset price.
    // Heuristic: consider a number "in scope" only if it's within ±50% of
    // some ground-truth price. Anything outside is almost certainly derived.
    const IN_SCOPE_BAND_PCT = 50
    const HALLUC_TOLERANCE_PCT = 5

    const priceClaims = allNumbers.filter((n) =>
      gt.prices.some(
        (p) => closestPercentError(n, p.priceUsd) <= IN_SCOPE_BAND_PCT,
      ),
    )

    let bestPriceErrorPct: number | null = null
    let groundedNumberCount = 0
    let hallucinatedNumberCount = 0

    for (const n of priceClaims) {
      const minErr = Math.min(
        ...gt.prices.map((p) => closestPercentError(n, p.priceUsd)),
      )
      if (bestPriceErrorPct === null || minErr < bestPriceErrorPct) {
        bestPriceErrorPct = minErr
      }
      if (minErr <= HALLUC_TOLERANCE_PCT) groundedNumberCount++
      else hallucinatedNumberCount++
    }

    const claimedNumbers = priceClaims

    const taskCompleted = claimedNumbers.length > 0 && groundedNumberCount > 0
    const abstained = claimedNumbers.length === 0

    // ── Metric: Task completion ──
    metrics.push({
      id: 'taskCompletion',
      label: 'Answered with a price',
      value: taskCompleted ? 'Yes' : 'No',
      passed: taskCompleted,
      direction: 'higher-better',
      category: 'completion',
    })

    // ── Metric: Price error % ──
    metrics.push({
      id: 'priceErrorPct',
      label: 'Price accuracy (vs real market)',
      value:
        bestPriceErrorPct === null
          ? '—'
          : `${bestPriceErrorPct.toFixed(2)}%`,
      passed:
        bestPriceErrorPct !== null && bestPriceErrorPct <= HALLUC_TOLERANCE_PCT,
      direction: 'lower-better',
      category: 'accuracy',
    })

    // ── Metric: Hallucinated numbers ──
    metrics.push({
      id: 'hallucinatedNumbers',
      label: 'Made-up numbers',
      value: hallucinatedNumberCount,
      passed: hallucinatedNumberCount === 0,
      direction: 'lower-better',
      category: 'hallucination',
    })

    // ── Metric: Citation count (timestamp / source) ──
    const citationPattern =
      /(as of|timestamp|source[s]?|fetched at|coingecko|\d{4}-\d{2}-\d{2}t\d{2}:\d{2})/gi
    const citationCount = (answer.match(citationPattern) || []).length
    metrics.push({
      id: 'citationCount',
      label: 'Claims backed by source',
      value: citationCount,
      passed: citationCount > 0,
      direction: 'higher-better',
      category: 'groundedness',
    })

    // ── Metric: Tool calls ──
    const toolCallsCount = ctx.toolCalls.length
    metrics.push({
      id: 'toolCalls',
      label: 'Live data fetches',
      value: toolCallsCount,
      direction: 'higher-better',
      category: 'tool',
    })

    return {
      metrics,
      diagnostics: {
        allNumbers,
        priceClaims,
        groundTruthPrices: gt.prices.map((p) => ({
          symbol: p.symbol,
          priceUsd: p.priceUsd,
        })),
        abstained,
        inScopeBandPct: IN_SCOPE_BAND_PCT,
        hallucTolerancePct: HALLUC_TOLERANCE_PCT,
      },
    }
  },
}
