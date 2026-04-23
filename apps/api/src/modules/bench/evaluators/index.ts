import type { Evaluator } from './types'
import { set1OracleEvaluator } from './set1-oracle.evaluator'
import { set2HunterEvaluator } from './set2-hunter.evaluator'
import { set3PolicyEvaluator } from './set3-policy.evaluator'

const REGISTRY: Record<string, Evaluator> = {
  [set1OracleEvaluator.id]: set1OracleEvaluator,
  [set2HunterEvaluator.id]: set2HunterEvaluator,
  [set3PolicyEvaluator.id]: set3PolicyEvaluator,
}

export function getEvaluator(id: string): Evaluator {
  const e = REGISTRY[id]
  if (!e) throw new Error(`[bench] Unknown evaluator: ${id}`)
  return e
}

export * from './types'
