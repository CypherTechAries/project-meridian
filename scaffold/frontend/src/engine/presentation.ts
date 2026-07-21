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

import type { FieldState, OptionEntry, Projection, RunResult, TrajectoryPoint } from './client.ts'
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
  const out: string[] = []
  const port = fieldState(run, 'port_activity_deficit')
  const reroute = fieldState(run, 'rerouting_level')
  const political = fieldState(run, 'political_pressure')
  if (port && port.value > 0.3) out.push('Port activity disrupted')
  if (reroute && reroute.value > 0.5) out.push('Carriers rerouted south')
  if (political && (political.direction === 'RISING' || political.near_peak)) out.push('Political pressure persists')
  return out.slice(0, 3)
}

export function situationSummary(run: RunResult): SituationSummary {
  const p = run.projection
  const days = Math.max(1, Math.round(p.simulated_hours / 24))
  const insurer = fieldState(run, 'insurer_risk')
  const rerouting = fieldState(run, 'rerouting_level')
  const employment = fieldState(run, 'employment_pressure')
  const political = fieldState(run, 'political_pressure')

  const parts: string[] = []
  parts.push(
    p.incident_active
      ? `The blockade has disrupted shipping for ${days} day${days === 1 ? '' : 's'}.`
      : `No incident is active.`,
  )

  const upstreamEasing = [insurer, rerouting].filter((t) => t?.direction === 'FALLING').length
  if (upstreamEasing >= 2) parts.push('Insurers and carriers are beginning to stabilise,')
  else if (upstreamEasing === 1) parts.push('Upstream disruption is partly stabilising,')
  else parts.push('Upstream disruption continues,')

  // Only claims the chain supports: employment exposure and sustained political pressure.
  const tail: string[] = []
  if (employment && employment.value > 0.2) tail.push('port and employment exposure has increased')
  if (political && (political.direction === 'RISING' || political.near_peak)) {
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

/* ══════════════════════════════════════════════════════════════════════════════════════════════
 * PLAIN LANGUAGE
 *
 * Added by the first-user usability reset. A first-time reader could not understand the previous
 * default view: decimals with no meaning, engine vocabulary, and internal action labels presented
 * as questions. See docs/design/FIRST-USER-USABILITY-TEST.md.
 *
 * These helpers change WORDS ONLY. Every one of them reads the same derived trends as before, so a
 * sentence here is still a claim the run supports. Nothing is authored to fit the screenshot, and
 * where the run does not establish something, the sentence is omitted rather than invented.
 * ══════════════════════════════════════════════════════════════════════════════════════════════ */

/**
 * THE FACTS COME FROM THE BACKEND.
 *
 * `run.state` is the single authoritative reading of the packaged run, computed once in
 * `backend/app/simulation/scenario_state.py` and shared by every surface. Ask MERIDIAN reads the
 * same object. The frontend chooses WORDS for that state; it does not decide what the state is.
 *
 * This exists because the two surfaces contradicted each other. Ask asserted "political pressure
 * is still high" as hand-written prose while the Briefing derived "low" and "falling" from the run.
 * Prose cannot follow the engine. Only one of them was reading anything.
 */
export function fieldState(run: RunResult, field: string): FieldState | null {
  return run.state?.fields?.[field] ?? null
}

/** Ordinary words for a direction. Never "peaked", "lagged", "post-peak" or "retention". */
export type PlainDirection = 'rising' | 'falling' | 'steady'

export function plainDirection(f: FieldState | null): PlainDirection | null {
  if (!f) return null
  if (f.direction === 'RISING') return 'rising'
  if (f.direction === 'FALLING') return 'falling'
  if (f.direction === 'STEADY') return 'steady'
  // NOT_ESTABLISHED: the backend could not measure a direction. Say nothing rather than "steady",
  // which would claim we looked and found no movement.
  return null
}

/** How much of something there is, in words a reader already owns. Never a decimal. */
export function plainLevel(f: FieldState | null): string {
  if (!f) return 'not established'
  switch (f.level) {
    case 'HIGH': return 'high'
    case 'MODERATE': return 'moderate'
    case 'LOW': return 'low'
    case 'NONE': return 'none recorded'
  }
}

/**
 * The three short sentences under the headline.
 *
 * Each is gated on the field that establishes it, so a run in a different state produces a
 * different set — or fewer. The founder's example lede reads "Political pressure is rising"; that
 * is written here as whatever the run actually shows, which at the tested state is a value that is
 * high and has only just started to come down. Readability may not be bought with a false clause.
 */
export function crisisLede(run: RunResult): string[] {
  const out: string[] = []

  const reroute = fieldState(run, 'rerouting_level')
  if (reroute && reroute.value > 0.5) out.push('Most ships are going the long way round.')
  else if (reroute && reroute.value > 0) out.push('Some ships are going the long way round.')

  const port = fieldState(run, 'port_activity_deficit')
  if (port && port.value > 0.3) out.push('Work at the coastal ports has fallen.')

  const political = fieldState(run, 'political_pressure')
  const dir = plainDirection(political)
  if (political && dir === 'rising') out.push('Pressure on the government is building.')
  else if (political && dir === 'falling') out.push('Pressure on the government has started to come down.')
  else if (political) out.push('Pressure on the government is holding steady.')

  return out
}

/** One plain section of the situation: what is happening to people, trade, or the government. */
export interface PlainSection {
  id: 'people' | 'economy' | 'politics'
  title: string
  /** One or two sentences. Ordinary language, no numbers, no engine terms. */
  sentences: string[]
  /** Direction of movement where the run establishes one; null where it does not. */
  direction: PlainDirection | null
  /** What the direction applies to, named in ordinary words. */
  directionSubject: string | null
  /**
   * A plain-language limit on how the section should be read, where one is needed.
   *
   * Politics carries one. The engine currently reports pressure on the government as low and
   * falling during a blockade, which reads as a judgement unless it is stated that this is one
   * packaged fictional run at one point in time. The value is not softened or hidden — an
   * inconvenient engine result is still a result.
   */
  caveat: string | null
  /** Chain fields behind the sentences — shown only inside the evidence control. */
  sources: string[]
  origin: 'engine' | 'fixture' | 'unavailable'
}

/**
 * People, Economy, Politics — the part of the old interface the first-time user understood.
 * Kept, and rewritten so the sentences carry no numbers and no machinery.
 */
/**
 * The politics caveat.
 *
 * Three things it must say, in ordinary words: this is the state in this packaged fictional run;
 * it is measured at the point the scenario has reached; and it is neither a prediction nor a
 * verdict on any real crisis. It does not excuse or reinterpret the number.
 */
export function politicsCaveat(p: Projection): string {
  const days = Math.max(1, Math.round(p.simulated_hours / 24))
  // Words, not digits — the headline says "five days" and this sentence sat beside it saying "5".
  const dayPhrase = days === 1 ? 'one day in' : `${dayWord(days)} days in`
  // "packaged run" is internal vocabulary. A reader needs to know two things: this is made up,
  // and it is a moment in a story rather than a forecast.
  // "fictional" stays — it is a standing honesty requirement, and it is a word a reader owns.
  // "packaged" and "run" go: they are internal vocabulary and carry no meaning for a first user.
  return `That is what this fictional scenario shows ${dayPhrase} — the situation at this point in
    the story, not a prediction of what happens next, and not a judgement about how a real
    government would handle a real crisis.`.replace(/\s+/g, ' ')
}

export function plainSections(run: RunResult): PlainSection[] {
  const p = run.projection
  const origin: PlainSection['origin'] = run.connection === 'unavailable' ? 'unavailable' : 'engine'

  const household = fieldState(run, 'household_expectation_pressure')
  const employment = fieldState(run, 'employment_pressure')
  const reroute = fieldState(run, 'rerouting_level')
  const port = fieldState(run, 'port_activity_deficit')
  const political = fieldState(run, 'political_pressure')
  const attention = fieldState(run, 'narrative_attention')
  const top = topCohort(p)

  const people: string[] = []
  if (top) {
    people.push(`Worry is highest among the ${top.label.replace(/-/g, ' ')} group.`)
  }
  if (employment && employment.value > 0.2) {
    people.push('People whose work depends on the ports are the most exposed.')
  } else if (household) {
    people.push('Households elsewhere are less affected so far.')
  }

  const economy: string[] = []
  if (reroute && reroute.value > 0.5) {
    economy.push('Shipping companies are avoiding the strait and sailing a longer route instead.')
  } else if (reroute && reroute.value > 0) {
    economy.push('Some shipping companies are avoiding the strait.')
  } else {
    economy.push('Shipping is following its normal route.')
  }
  if (port && port.value > 0.3) {
    economy.push('Less cargo is arriving, so there is less work at the ports.')
  }

  const politics: string[] = []
  if (political) {
    // Both facts, in one sentence. The level alone reads as "nothing much is happening"; the
    // near-peak fact alone reads as "pressure is severe". Ask MERIDIAN used to state only the
    // second, which is how the two screens ended up contradicting each other.
    // "in this run" is internal vocabulary — a first-time reader does not know what a run is.
    // "so far" says the same thing in words they already own.
    const near = political.near_peak
      ? ' — but it is close to the highest it has been so far'
      : ''
    politics.push(`Pressure on the government is ${plainLevel(political)}${near}.`)
  }
  if (attention && attention.value > 0.1) {
    // No causal clause here. "which keeps that pressure on" was both an unestablished claim and a
    // direct contradiction of the direction line beneath it, which currently reads "falling".
    politics.push('People are paying attention to it and talking about it.')
  }

  return [
    {
      id: 'people',
      title: 'People',
      sentences: people,
      direction: plainDirection(household ?? employment),
      directionSubject: 'worry among households',
      caveat: null,
      sources: ['cohorts[].value', 'chain.household_expectation_pressure', 'chain.employment_pressure'],
      origin,
    },
    {
      id: 'economy',
      title: 'Economy',
      sentences: economy,
      direction: plainDirection(reroute),
      // The direction line reads "<subject> is <direction>", so the subject must be a singular
      // noun phrase. "ships avoiding the strait is falling" was simply ungrammatical.
      directionSubject: 'the number of ships avoiding the strait',
      caveat: null,
      sources: ['chain.rerouting_level', 'chain.port_activity_deficit'],
      origin,
    },
    {
      id: 'politics',
      title: 'Politics',
      sentences: politics,
      direction: plainDirection(political),
      directionSubject: 'pressure on the government',
      caveat: politicsCaveat(p),
      sources: ['chain.political_pressure', 'chain.narrative_attention', 'chain.collective_activity'],
      origin,
    },
  ]
}

/**
 * A government option written so it makes sense to someone arriving cold.
 *
 * DECLARED, NOT GENERATED. "publish_legal_advice" is an internal identifier; turning it into
 * "Publish Legal Advice" and calling that a question was the failure recorded as observation 8.
 * Each entry below is a hand-written plain-language description of an option the scenario already
 * declares. It describes WHAT THE OPTION IS. It states no consequence, because this prototype
 * computes none, and it promises no effect, because nothing is ever executed.
 *
 * An option with no entry here falls back to a readable form of its own label and says plainly that
 * no description has been written for it — it is never dressed up as a question it is not.
 */
export interface PlainDecision {
  optionId: string
  /** The decision as a question a first-time reader can answer. */
  question: string
  /** Two sentences: what the thing is, and why the choice matters. No consequences claimed. */
  context: string[]
  /** The two plain choices offered. Display only. */
  choices: [string, string]
  /** Why the option currently stands where it does, in ordinary words. */
  standing: string
  /** True when this option has a declared plain-language description. */
  described: boolean
}

const DECISION_COPY: Record<string, { question: string; context: string[]; choices: [string, string] }> = {
  publish_legal_advice: {
    question: 'Should the government publish its legal assessment now?',
    context: [
      'The government has had lawyers look at whether the blockade is lawful, and it has not yet ' +
        'shown anyone what they concluded.',
      'Publishing it would put the government’s own account on the record while people are still ' +
        'deciding what to believe.',
    ],
    choices: ['Publish the assessment now', 'Wait for more verification'],
  },
  pursue_quiet_diplomacy: {
    question: 'Should the government try to settle this privately first?',
    context: [
      'Talking privately means approaching the other side directly instead of saying anything in ' +
        'public.',
      'It keeps the disagreement out of the open for now, and it means the government says nothing ' +
        'publicly while people are waiting to hear from it.',
    ],
    choices: ['Open private talks', 'Keep handling it publicly'],
  },
  declare_emergency_powers: {
    question: 'Should the government take emergency powers?',
    context: [
      'Emergency powers let a government act without going through its usual approvals.',
      'They are the strongest step available here, and they are hard to step back from once taken.',
    ],
    choices: ['Take emergency powers', 'Carry on without them'],
  },
}

export function plainDecision(o: OptionEntry): PlainDecision {
  const copy = DECISION_COPY[o.option_id]
  // Ordinary words for what the engine calls ENABLED / CONSTRAINED / AVAILABLE.
  const standing =
    o.value === 'ENABLED'
      ? 'This choice is open to the government now.'
      : o.value === 'CONSTRAINED'
        ? 'This choice is limited at the moment — the situation has moved far enough to restrict it, but not far enough to open it.'
        : 'This choice is available, and nothing in the situation has changed its standing yet.'

  if (!copy) {
    return {
      optionId: o.option_id,
      question: o.label.replace(/_/g, ' '),
      context: ['No plain-language description has been written for this option yet.'],
      choices: ['—', '—'],
      standing,
      described: false,
    }
  }
  return { optionId: o.option_id, question: copy.question, context: copy.context,
           choices: copy.choices, standing, described: true }
}

/* ══════════════════════════════════════════════════════════════════════════════════════════════
 * SITUATION MODEL — the facts the situation diagram may show
 *
 * Issue #33. MERIDIAN's engine has NO SPATIAL MODEL: no coordinates, no geometry, no port entities,
 * and political pressure is a single scalar with no location. A map would therefore have to invent
 * placement for two of the five questions a reader must be able to answer.
 *
 * So the diagram shows STRUCTURE, not geography — the causal chain the engine actually models,
 * arranged by relationship. This model is what it may draw. Anything absent from here must not
 * appear on screen.
 *
 * "Northshore" and "Southport" are deliberately NOT here. They were hard-coded in the old map
 * component and are not scenario entities; they were part of the mock, not engine truth.
 * ══════════════════════════════════════════════════════════════════════════════════════════════ */

export interface SituationStage {
  id: string
  /** Short heading, plain words. */
  title: string
  /** One sentence stating what is happening. */
  sentence: string
  /** Plain level word, or null where the run does not establish one. */
  level: string | null
  /** 0..1 for the magnitude bar. Null where there is no value to show. */
  magnitude: number | null
  direction: PlainDirection | null
  /** The run's own recorded values, for the change-over-time line. Empty when not recorded. */
  series: number[]
  /** Stated when `series` is empty, so an absent line is never read as a flat one. */
  seriesNote: string | null
}

export interface SituationGroup {
  name: string
  /** 0..1, this group's own pressure value. */
  value: number
  /** Whole per cent of the population. Never a decimal. */
  sharePercent: number
}

export interface SituationModel {
  days: number
  blockadeActive: boolean
  stages: SituationStage[]
  groups: SituationGroup[]
  groupsNote: string
  decision: PlainDecision | null
  otherChoices: number
  executionNote: string
  /** Rendered on the diagram. The reader is told what kind of picture this is. */
  kindNote: string
}

const NOT_RECORDED =
  'MERIDIAN does not record that value at every step, so no change line is shown.'

/**
 * Declared once, here, because both the Briefing and the situation diagram state it. `briefing.ts`
 * re-exports it so existing importers are unaffected; a second copy of this sentence is exactly the
 * duplication the shared-state work removed.
 */
export const NOTHING_EXECUTES = 'Decision support only — nothing will be executed.'

function stageFrom(
  run: RunResult, id: string, field: string, title: string, sentence: string,
): SituationStage {
  const f = fieldState(run, field)
  const series = run.trajectory
    .map((t) => t[field])
    .filter((v): v is number => typeof v === 'number')
  return {
    id,
    title,
    sentence,
    level: f ? plainLevel(f) : null,
    magnitude: f ? Math.min(1, Math.max(0, f.value)) : null,
    direction: plainDirection(f),
    series,
    seriesNote: series.length >= 2 ? null : NOT_RECORDED,
  }
}

/**
 * The five questions this must answer, through layout and relationship:
 * what is blocked · who is affected · what pressure is building (NOT as a place) ·
 * what trade-offs are visible · what changed over time.
 */
export function situationModel(run: RunResult): SituationModel {
  const p = run.projection
  const days = Math.max(1, Math.round(p.simulated_hours / 24))

  const stages: SituationStage[] = []

  stages.push(
    stageFrom(run, 'shipping', 'rerouting_level', 'Ships take the long way round',
      'Shipping is avoiding the strait, taking a longer route.'),
  )
  stages.push(
    stageFrom(run, 'ports', 'port_activity_deficit', 'Less cargo, less work',
      'Less cargo arrives, so there is less work at the ports.'),
  )
  stages.push(
    stageFrom(run, 'pressure', 'political_pressure', 'Pressure on the government',
      'People are paying attention, and the government feels it.'),
  )

  // Top three groups by their own pressure value. Named exactly as the scenario declares them —
  // no paraphrase, no invented group, and no location, because groups have none.
  const groups: SituationGroup[] = p.cohorts
    .slice()
    .sort((a, b) => b.value - a.value)
    .slice(0, 3)
    .map((c) => ({
      name: c.label.replace(/-/g, ' '),
      value: Math.min(1, Math.max(0, c.value)),
      sharePercent: Math.round(c.population_share * 100),
    }))

  const primary = primaryDecision(p)

  return {
    days,
    blockadeActive: p.incident_active,
    stages,
    groups,
    groupsNote:
      'Bar length is how much each group is affected. These are averages — MERIDIAN does not ' +
      'model the individuals inside them.',
    decision: primary ? plainDecision(primary) : null,
    otherChoices: Math.max(0, p.government_options.length - (primary ? 1 : 0)),
    executionNote: NOTHING_EXECUTES,
    kindNote:
      'This shows how one thing led to another — not where anything is. MERIDIAN does not model ' +
      'locations, distances or routes.',
  }
}

/* ══════════════════════════════════════════════════════════════════════════════════════════════
 * COMPACT IMPACT ROWS — R1/R2
 *
 * The three impact sections were 855px of the Briefing's 2,635px, and each carried a "Show where
 * this comes from" disclosure whose body was raw field names (`chain.household_expectation_pressure`).
 * Nobody who is not a backend developer needs that on a reading screen.
 *
 * A row is now one line, and its evidence route is A QUESTION rather than a panel. `askQuestion` is
 * always a question the catalogue can actually answer — asking something it must decline would be
 * a worse experience than the disclosure it replaces.
 * ══════════════════════════════════════════════════════════════════════════════════════════════ */

export interface ImpactRow {
  id: 'people' | 'economy' | 'politics'
  title: string
  /** One line. The first sentence of the section, which is the one that carries the state. */
  line: string
  direction: PlainDirection | null
  directionSubject: string | null
  /**
   * The declared question that explains this row, or null where the catalogue has none.
   *
   * Politics is currently null: there is no catalogue question about political pressure or the
   * government's response. That gap is issue #37, and it is left visible here rather than papered
   * over by sending a question that would be declined.
   */
  askQuestion: string | null
}

const ROW_QUESTION: Record<ImpactRow['id'], string | null> = {
  people: 'How are people and groups reacting?',
  economy: 'How are the economy and supply chains reacting?',
  politics: null,
}

export function impactRows(run: RunResult): ImpactRow[] {
  return plainSections(run).map((s) => ({
    id: s.id,
    title: s.title,
    line: s.sentences[0] ?? 'Not established in this scenario.',
    direction: s.direction,
    directionSubject: s.directionSubject,
    askQuestion: ROW_QUESTION[s.id],
  }))
}

/**
 * The one sentence that must be readable in two seconds.
 *
 * Deliberately short and deliberately singular: what has happened, and what is being decided. If
 * this cannot be read at a glance, no amount of detail below it helps.
 */
export function headlineAndAsk(run: RunResult): { headline: string; decision: string | null } {
  const primary = primaryDecision(run.projection)
  return {
    headline: situationSummary(run).headline,
    decision: primary ? plainDecision(primary).question : null,
  }
}
