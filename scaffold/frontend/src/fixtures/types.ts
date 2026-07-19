/**
 * Fixture contract for the MERIDIAN C0 prototype.
 *
 * NOTHING HERE COMES FROM THE SIMULATION ENGINE. Every record is hand-authored fixture data.
 * The envelope below exists so that a mixed fixture/live build at C1 can stay honest per-record
 * rather than per-page: `origin` is the field that tells a reader which values are real.
 *
 * The epistemic vocabulary is fixed by founder decision D2 (19 July 2026) and may not be extended
 * without a further decision.
 */

/** Founder decision D2. `AUTHORITATIVE` describes STATE QUALITY, not player access. */
export type EpistemicStatus =
  | 'AUTHORITATIVE'
  | 'ASSESSED'
  | 'DISPUTED'
  | 'UNKNOWN'
  | 'PRESENTATION_ONLY'

/**
 * Founder decision D2. Deliberately ordinal words, never a percentage: no numeric confidence may
 * be displayed unless a documented mechanism produced it, and no such mechanism exists.
 */
export type Confidence = 'HIGH' | 'MEDIUM' | 'LOW' | 'NOT_APPLICABLE'

/** `engine` is reserved for values genuinely produced by the engine. C0 uses only `fixture`. */
export type Origin = 'fixture' | 'engine'

/**
 * Required on every displayable record. A component that renders a value without one of these is
 * a build failure — see `assertEnvelope` and the "unmarked content" rule (research F9): labelling
 * only some content inflates the apparent authority of everything unlabelled.
 */
export interface Envelope {
  prototype_data: true
  scenario_id: string
  scenario_version: string
  simulation_tick: number
  player_role: string
  /** Why this role can see this. Placeholder in C0 — no auth layer exists. */
  visibility_basis: string
  epistemic_status: EpistemicStatus
  confidence: Confidence
  /** What produced this claim. In C0 always a fixture author note. */
  provenance: string
  last_updated: string
  origin: Origin
}

export interface Claim extends Envelope {
  id: string
  label: string
  /** Display value. `null` means UNKNOWN or UNAVAILABLE — which are distinct from zero. */
  value: string | null
  /** Distinguishes "we do not know" from "this cannot be shown to you" from "zero". */
  absence?: 'UNKNOWN' | 'UNAVAILABLE' | 'NOT_APPLICABLE'
  detail?: string
}

/** One hop of the hand-authored propagation chain (founder decision G3). */
export interface ChainHop extends Envelope {
  id: string
  ordinal: number
  stage: string
  actor: string
  /** What is happening at this hop. */
  summary: string
  /** Named entities involved — all pre-materialised fixture entities (founder decision G1). */
  entities: EntityRef[]
  /**
   * Ranked contributors, each naming its mechanism (research T18 — fact-checked).
   * An aggregate without this does not ship.
   */
  contributors: Contributor[]
}

export interface Contributor {
  label: string
  /** The named mechanism behind this contributor. */
  mechanism: string
  weight: string
}

/**
 * `materialised: false` entities are aggregate or minimal-reference records ONLY. Opening one must
 * never generate biography, beliefs, relationships or identity (founder decision G1).
 */
export interface EntityRef {
  id: string
  name: string
  kind: 'person' | 'organisation' | 'cohort' | 'state' | 'business'
  materialised: boolean
  note?: string
}

export interface Panel extends Envelope {
  id: string
  title: string
  /** Short line shown under the title. */
  standfirst: string
  claims: Claim[]
}

export interface QueueItem extends Envelope {
  id: string
  title: string
  detail: string
  /**
   * Non-empty by construction. An item with no available response is a stream event, not a
   * decision (research: HSE's rule that status indicators must not be designated as alarms).
   */
  affordances: string[]
  deadline_label: string | null
}

export interface StreamEvent extends Envelope {
  id: string
  tick: number
  text: string
  /** Low-relevance events are DIMMED, never filtered out. */
  relevance: 'normal' | 'low'
}

export interface Crisis extends Envelope {
  id: string
  name: string
  standfirst: string
  location_label: string
  day_label: string
}

export interface ScenarioFixture {
  prototype_data: true
  scenario_id: string
  scenario_version: string
  simulation_tick: number
  player_role: string
  world: { id: string; name: string; is_fictional: true }
  crisis: Crisis
  chain: ChainHop[]
  panels: Panel[]
  queue: QueueItem[]
  stream: StreamEvent[]
}

/**
 * Build-time honesty assertion. Throws if a record is missing its envelope or claims a
 * non-fixture origin in a prototype build.
 *
 * This is the mechanism behind "unmarked content is a build failure". It is deliberately loud:
 * the entire remediation phase exists because artefacts claimed properties they did not have, and
 * a polished screenshot is an artefact.
 */
export function assertEnvelope(record: Partial<Envelope>, where: string): void {
  if (record.prototype_data !== true) {
    throw new Error(`[fixture-honesty] ${where}: prototype_data must be literally true`)
  }
  if (record.origin !== 'fixture') {
    throw new Error(
      `[fixture-honesty] ${where}: origin is "${record.origin}" but this is a prototype build. ` +
        `Only 'fixture' is permitted until the engine genuinely supplies the value.`,
    )
  }
  const required: (keyof Envelope)[] = [
    'scenario_id',
    'scenario_version',
    'simulation_tick',
    'player_role',
    'visibility_basis',
    'epistemic_status',
    'confidence',
    'provenance',
    'last_updated',
  ]
  for (const key of required) {
    if (record[key] === undefined || record[key] === null || record[key] === '') {
      throw new Error(`[fixture-honesty] ${where}: missing required envelope field "${key}"`)
    }
  }
}
