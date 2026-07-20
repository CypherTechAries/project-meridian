/**
 * Derived presentation model — the SINGLE source of every plain-language claim on screen.
 *
 * WHY THIS MODULE EXISTS. Usability rule 6a: a readable sentence is still a claim, and claims must
 * be true of the current run. Two failures this prevents:
 *
 *   1. Authored copy. "Port shifts cancelled" and "Three carriers diverted" read well and are
 *      NOT SUPPORTED by any engine field — the engine models no shifts, no carrier count and no
 *      named families. Sentences like those may not be rendered at all.
 *   2. Contradiction. The earlier wireframe simultaneously called political pressure "near its
 *      peak" and "steady". Both Briefing and Analysis now consume THIS derivation, so the same
 *      value cannot be described three ways in three places.
 *
 * Every function here reads the projection or the run's own trajectory. Nothing is hard-coded to
 * the Kestral screenshot; change the run and the sentences change or disappear.
 */

import type { Projection, RunResult, TrajectoryPoint } from './client.ts'
import { stageByField } from './client.ts'

export type DirectionWord = 'RISING' | 'EASING' | 'STABLE'

/** The complete derived state of one chain value. Both views render from this, never from raw. */
export interface DerivedTrend {
  field: string
  value: number
  /** Direction over the last five ticks of the run's own trajectory. */
  direction: DirectionWord | null
  peakTick: number
  peakValue: number
  /** 0..1 — how much of its own peak the value still holds. */
  peakRetention: number
  /** True when the value has turned over but still holds most of its peak. */
  nearPeak: boolean
  /**
   * True when the peak is in the past and the value has fallen measurably from it.
   *
   * Deliberately independent of `direction`, which reads a five-tick window and can report STABLE
   * for a slow decline. At tick 20 political pressure peaked at 17 and has fallen 0.004 - too
   * little for the window to call EASING, but "has begun to ease" is nonetheless TRUE and saying
   * only "steady" would hide the turn.
   */
  postPeak: boolean
  /** Plain-language label. Derived; never authored. */
  label: string
  /** One supporting sentence, or null when nothing truthful can be added. */
  explanation: string | null
  /** The last five ticks of this value, for the card trend line. Engine output, not smoothed. */
  recent: number[]
}

const NEAR_PEAK_RETENTION = 0.9

function series(traj: TrajectoryPoint[], field: string): number[] {
  return traj.map((t) => Number(t[field] ?? 0))
}

/**
 * Direction from the last five ticks of values the engine already produced.
 * A description of what happened — never a forecast, rate or extrapolation.
 * Returns null when the trajectory is too short to say anything truthful.
 */
export function directionOf(values: number[]): DirectionWord | null {
  if (values.length < 6) return null
  const now = values[values.length - 1] ?? 0
  const then = values[values.length - 6] ?? 0
  const delta = now - then
  if (Math.abs(delta) < Math.max(0.004, Math.abs(now) * 0.02)) return 'STABLE'
  return delta > 0 ? 'RISING' : 'EASING'
}

function peakOf(values: number[]): { tick: number; value: number } {
  let best = { tick: 0, value: -Infinity }
  values.forEach((v, i) => {
    if (v > best.value) best = { tick: i + 1, value: v }
  })
  return best
}

/**
 * Trend labels. Note the composite case: a value that has turned over but still holds ≥90% of its
 * peak is described as BOTH easing and near its peak, in one sentence, because saying only one of
 * those would be misleading. This is the exact case the Kestral run is in at tick 20.
 */
export function deriveTrend(p: Projection, traj: TrajectoryPoint[], field: string): DerivedTrend | null {
  const stage = stageByField(p, field)
  if (!stage) return null
  const values = series(traj, field)
  const direction = directionOf(values)
  const peak = peakOf(values)
  const retention = peak.value > 0 ? stage.value / peak.value : 0
  const nearPeak = direction !== 'RISING' && retention >= NEAR_PEAK_RETENTION && peak.tick > 0
  const lastTick = values.length
  const postPeak = peak.tick > 0 && peak.tick < lastTick && peak.value - stage.value > peak.value * 0.005

  let label: string
  if (direction === 'RISING') label = 'is rising'
  else if (postPeak && nearPeak) label = 'has begun to ease but remains near its peak'
  else if (direction === 'EASING' || postPeak) label = 'is easing'
  else if (nearPeak) label = 'is holding near its peak'
  else if (direction === 'STABLE') label = 'is steady'
  else label = 'is not yet established'

  return {
    field,
    value: stage.value,
    direction,
    peakTick: peak.tick,
    peakValue: peak.value,
    peakRetention: retention,
    nearPeak,
    postPeak,
    label,
    explanation: stage.lifecycle || null,
    recent: values.slice(-5),
  }
}

/** A consequence domain card. Scenario-defined, not a permanent platform category. */
export interface ConsequenceDomain {
  id: 'people' | 'economy' | 'politics'
  title: string
  /** Plain-language state. Derived from the fields listed in `sources`. */
  statement: string
  trend: DerivedTrend | null
  /** Chain fields this statement is derived from — the copy-to-state evidence trail. */
  sources: string[]
  origin: 'engine' | 'fixture' | 'unavailable'
}

function topCohort(p: Projection) {
  return p.cohorts.slice().sort((a, b) => b.value - a.value)[0]
}

/**
 * The three Kestral v0.1 consequence domains.
 *
 * SCENARIO-DEFINED, not universal. Another scenario might use public health, institutional trust,
 * security, infrastructure or international response. This function is where that variation would
 * live; the Briefing View renders whatever it returns.
 */
export function consequenceDomains(run: RunResult): ConsequenceDomain[] {
  const p = run.projection
  const traj = run.trajectory
  const origin: ConsequenceDomain['origin'] = run.connection === 'unavailable' ? 'unavailable' : 'engine'

  const household = deriveTrend(p, traj, 'household_expectation_pressure')
  const rerouting = deriveTrend(p, traj, 'rerouting_level')
  const employment = deriveTrend(p, traj, 'employment_pressure')
  const political = deriveTrend(p, traj, 'political_pressure')
  const top = topCohort(p)

  // Cohort name is rendered exactly as the scenario declares it — no paraphrase, no invented group.
  const topName = top ? top.label.replace(/-/g, ' ') : null

  return [
    {
      id: 'people',
      title: 'People',
      statement: topName
        ? `Concern is highest among ${topName}`
        : 'No cohort concern has been computed',
      trend: household,
      sources: ['cohorts[].value', 'chain.household_expectation_pressure'],
      origin,
    },
    {
      id: 'economy',
      title: 'Economy',
      statement:
        rerouting && rerouting.value > 0.5
          ? 'Most carriers are still avoiding the strait'
          : rerouting && rerouting.value > 0
            ? 'Some carriers are avoiding the strait'
            : 'Shipping is following normal routes',
      trend: rerouting ?? employment,
      sources: ['chain.rerouting_level', 'chain.employment_pressure'],
      origin,
    },
    {
      id: 'politics',
      title: 'Politics',
      statement: political ? `Political pressure ${political.label}` : 'Political pressure not established',
      trend: political,
      sources: ['chain.political_pressure', 'chain.narrative_attention', 'chain.collective_activity'],
      origin,
    },
  ]
}

/** One-paragraph situation summary. Every clause traceable to a field. */
export interface SituationSummary {
  /** Short declarative headline. Derived from incident state and elapsed simulated time. */
  headline: string
  text: string
  sources: string[]
}

const WORD_DAYS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

/** Numbers written as words read better at headline size; beyond ten, fall back to digits. */
function dayWord(n: number): string {
  return WORD_DAYS[n] ?? String(n)
}

/** Two or three numbered map callouts, each gated on a field that establishes it. */
export function mapCallouts(run: RunResult): string[] {
  const p = run.projection
  const traj = run.trajectory
  const out: string[] = []
  const port = deriveTrend(p, traj, 'port_activity_deficit')
  const reroute = deriveTrend(p, traj, 'rerouting_level')
  const political = deriveTrend(p, traj, 'political_pressure')
  if (port && port.value > 0.3) out.push('Port activity disrupted')
  if (reroute && reroute.value > 0.5) out.push('Carriers rerouted south')
  if (political && (political.direction === 'RISING' || political.nearPeak)) out.push('Political pressure persists')
  return out.slice(0, 3)
}

export function situationSummary(run: RunResult): SituationSummary {
  const p = run.projection
  const traj = run.trajectory
  const days = Math.max(1, Math.round(p.simulated_hours / 24))
  const insurer = deriveTrend(p, traj, 'insurer_risk')
  const rerouting = deriveTrend(p, traj, 'rerouting_level')
  const employment = deriveTrend(p, traj, 'employment_pressure')
  const political = deriveTrend(p, traj, 'political_pressure')

  const parts: string[] = []
  parts.push(
    p.incident_active
      ? `The blockade has disrupted shipping for ${days} day${days === 1 ? '' : 's'}.`
      : `No incident is active.`,
  )

  const upstreamEasing = [insurer, rerouting].filter((t) => t?.direction === 'EASING').length
  if (upstreamEasing >= 2) parts.push('Insurers and carriers are beginning to stabilise,')
  else if (upstreamEasing === 1) parts.push('Upstream disruption is partly stabilising,')
  else parts.push('Upstream disruption continues,')

  // Only claims the chain supports: employment exposure and sustained political pressure.
  const tail: string[] = []
  if (employment && employment.value > 0.2) tail.push('port and employment exposure has increased')
  if (political && (political.direction === 'RISING' || political.nearPeak)) {
    tail.push('and narrative and collective activity continue to sustain political pressure')
  }
  parts.push(tail.length ? `but ${tail.join(' ')}.` : 'and downstream effects remain limited.')

  const days2 = Math.max(1, Math.round(p.simulated_hours / 24))
  const headline = p.incident_active
    ? `The strait has been blocked for ${dayWord(days2)} day${days2 === 1 ? '' : 's'}.`
    : 'No incident is currently active.'

  // The body sentence drops the leading "The blockade has disrupted..." clause, which the headline
  // now carries, so the two do not repeat each other.
  const body = parts.slice(1).join(' ').replace(/^([a-z])/, (m) => m.toUpperCase())

  return {
    headline,
    text: body.replace(/,\s+but/, ', but'),
    sources: [
      'projection.incident_active',
      'projection.simulated_hours',
      'chain.insurer_risk',
      'chain.rerouting_level',
      'chain.employment_pressure',
      'chain.political_pressure',
    ],
  }
}

/** "Since yesterday" — the previous tick compared with the current one. */
export function sinceYesterday(run: RunResult): string {
  const traj = run.trajectory
  if (traj.length < 2) return 'No previous tick to compare.'
  const fields: [string, string][] = [
    ['rerouting_level', 'carrier rerouting'],
    ['employment_pressure', 'employment exposure'],
    ['political_pressure', 'political pressure'],
  ]
  const moves = fields
    .map(([f, name]) => {
      const now = Number(traj[traj.length - 1]?.[f] ?? 0)
      const prev = Number(traj[traj.length - 2]?.[f] ?? 0)
      const d = now - prev
      if (Math.abs(d) < 0.0005) return `${name} steady`
      return `${name} ${d > 0 ? 'up' : 'down'}`
    })
    .join(' · ')
  return moves
}

/** The single decision the Briefing View surfaces, if one is genuinely waiting. */
export function primaryDecision(p: Projection) {
  const enabled = p.government_options.filter((o) => o.value === 'ENABLED')
  const constrained = p.government_options.filter((o) => o.value === 'CONSTRAINED')
  return enabled[0] ?? constrained[0] ?? null
}
