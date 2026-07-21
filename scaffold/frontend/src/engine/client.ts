/**
 * Engine client — fetches a real P0.5 demonstration run.
 *
 * HONESTY MODEL. Every value this returns is marked with its true origin. When the backend
 * answers, values are ENGINE. When it does not, the screen must say so rather than silently
 * rendering a bundled snapshot as though it were live — so the fallback is marked UNAVAILABLE at
 * the connection level and the bundled snapshot is only used to keep the layout inspectable.
 *
 * The bundled snapshot is a real recorded response, not invented data, but a recording is not a
 * live run. `connection` is what the interface must key off.
 */

import snapshot from '../fixtures/engine-snapshot.json'
import { RUN_PATH, apiUrl } from './api.ts'

export type RunMode = 'baseline' | 'incident' | 'counterfactual'
export type Connection = 'live' | 'snapshot' | 'unavailable'

export interface ChainStage {
  label: string
  value: number
  field: string
  stage: number
  stage_name: string
  epistemic_status: string
  confidence: string
  provenance: string
  origin: string
  mechanism: string | null
  mechanism_version: string | null
  source_fields: string[]
  lag_ticks: number
  lifecycle: string
  last_updated_tick: number
}

export interface CohortEntry {
  label: string
  value: number
  cohort_id: string
  represents_population: number
  population_share: number
  income_sensitivity: number
  epistemic_status: string
  provenance: string
  origin: string
  last_updated_tick: number
}

export interface OptionEntry {
  label: string
  value: string
  option_id: string
  driven_by: string
  epistemic_status: string
  provenance: string
  origin: string
  last_updated_tick: number
}

export interface TransitionEntry {
  transition_id: string
  tick: number
  mechanism: string
  mechanism_version: string
  source_fields: string[]
  causal_parents: string[]
  draw_refs: string[]
  delta: Record<string, { before?: unknown; after?: unknown }>
  origin: string
}

export interface TrajectoryPoint {
  tick: number
  [field: string]: number
}

export interface Projection {
  origin: string
  scenario_id: string
  scenario_version: string
  rule_pack_version: string
  tick: number
  simulated_hours: number
  tick_duration_minutes: number
  demonstration_horizon_ticks: number
  state_revision: number
  incident_active: boolean
  stages: ChainStage[]
  cohorts: CohortEntry[]
  government_options: OptionEntry[]
  recent_transitions: TransitionEntry[]
  not_implemented: string[]
}

/**
 * One field of the backend's authoritative scenario state.
 *
 * THIS IS THE FACT. The frontend does not decide whether political pressure is low or falling; it
 * reads that here and chooses words for it. See `backend/app/simulation/scenario_state.py`.
 */
export interface FieldState {
  field: string
  value: number
  level: 'NONE' | 'LOW' | 'MODERATE' | 'HIGH'
  direction: 'RISING' | 'FALLING' | 'STEADY' | 'NOT_ESTABLISHED'
  peak_value: number
  peak_tick: number
  peak_retention: number
  near_peak: boolean
  post_peak: boolean
  direction_measured: boolean
}

export interface ScenarioState {
  scenario_id: string
  seed: number
  ticks: number
  simulated_hours: number
  fields: Record<string, FieldState>
}

export interface RunResult {
  connection: Connection
  contract_version: string
  mode: RunMode
  disabled_mechanism: string | null
  ticks: number
  seed: number
  projection: Projection
  /**
   * The shared authoritative state. Optional only because an old recorded snapshot may predate it;
   * where it is absent the plain-language layer says so rather than inventing a level.
   */
  state?: ScenarioState
  trajectory: TrajectoryPoint[]
  limitations: string[]
  error?: string
}

/** Resolved through the shared API base — the same one Ask MERIDIAN uses. See `api.ts`. */
export const RUN_ENDPOINT = apiUrl(RUN_PATH)

function fromSnapshot(connection: Connection, error?: string): RunResult {
  return { ...(snapshot as unknown as RunResult), connection, error }
}

export async function runDemonstration(
  mode: RunMode = 'incident',
  ticks = 20,
): Promise<RunResult> {
  try {
    const res = await fetch(RUN_ENDPOINT, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ mode, ticks }),
      signal: AbortSignal.timeout(4000),
    })
    if (!res.ok) return fromSnapshot('unavailable', `backend returned ${res.status}`)
    const body = (await res.json()) as RunResult
    return { ...body, connection: 'live' }
  } catch (e) {
    // Honest failure: the layout still renders, but the interface says the engine is unreachable
    // and every value is marked as a recorded snapshot rather than a live result.
    return fromSnapshot('unavailable', e instanceof Error ? e.message : 'unreachable')
  }
}

/** Synchronous bundled snapshot, for first paint before the request resolves. */
export function initialSnapshot(): RunResult {
  return fromSnapshot('snapshot')
}

export function stageByField(p: Projection, field: string): ChainStage | undefined {
  return p.stages.find((s) => s.field === field)
}
