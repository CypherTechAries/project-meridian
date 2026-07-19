/**
 * Kestral Strait — hand-authored fixture scenario, version 1.0.0.
 *
 * FOUNDER DECISION G3: this propagation chain is HAND-AUTHORED. It was not computed, simulated,
 * emergent or live, and must never be described as any of those. MERIDIAN's three simulation tiers
 * do not causally influence one another today (open critical finding 1), so no computed propagation
 * exists to render. This file illustrates the INTENDED chain so the interface can be designed and
 * reviewed; the first computed chain arrives at C2, gated on P0.4A and P0.5.
 *
 * The Republic of Vantara is fictional. No real nation, organisation or person is depicted.
 */

import type { ScenarioFixture } from './types.ts'

const SCENARIO_ID = 'kestral-strait'
const VERSION = '1.0.0'
const TICK = 412
const ROLE = 'national_situation_lead'

/** Envelope defaults. Every record still declares its own epistemic status explicitly. */
function env(
  epistemic_status: ScenarioFixture['crisis']['epistemic_status'],
  confidence: ScenarioFixture['crisis']['confidence'],
  provenance: string,
  visibility_basis: string,
  last_updated: string,
) {
  return {
    prototype_data: true as const,
    scenario_id: SCENARIO_ID,
    scenario_version: VERSION,
    simulation_tick: TICK,
    player_role: ROLE,
    visibility_basis,
    epistemic_status,
    confidence,
    provenance,
    last_updated,
    origin: 'fixture' as const,
  }
}

export const kestralStrait: ScenarioFixture = {
  prototype_data: true,
  scenario_id: SCENARIO_ID,
  scenario_version: VERSION,
  simulation_tick: TICK,
  player_role: ROLE,
  world: { id: 'vantara', name: 'Republic of Vantara', is_fictional: true },

  crisis: {
    ...env(
      'AUTHORITATIVE',
      'HIGH',
      'Fixture author — scenario definition',
      'Scenario-level fact available to every role',
      'tick 401',
    ),
    id: 'crisis-kestral',
    name: 'Kestral Strait closure',
    standfirst:
      'Two bulk carriers held at the northern approach for a fourth day. The strait carries most of Vantara’s imported grain and refined fuel.',
    location_label: 'Kestral Strait · northern approach',
    day_label: 'Day 41',
  },

  chain: [
    {
      ...env('AUTHORITATIVE', 'HIGH', 'Fixture author — scenario definition', 'Publicly observable', 'tick 401'),
      id: 'hop-1',
      ordinal: 1,
      stage: 'Maritime incident',
      actor: 'Kestral Strait',
      summary: 'Transit halted at the northern approach. Two carriers held; twelve more diverted to holding patterns.',
      entities: [
        { id: 'org-port-authority', name: 'Kestral Port Authority', kind: 'organisation', materialised: true },
      ],
      contributors: [
        { label: 'Vessels held', mechanism: 'Scenario-authored initial condition', weight: 'primary' },
        { label: 'Approach closure', mechanism: 'Scenario-authored initial condition', weight: 'primary' },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative insurer response', 'Commercial reporting available to this role', 'tick 404'),
      id: 'hop-2',
      ordinal: 2,
      stage: 'Insurer risk assessment',
      actor: 'Marine underwriters',
      summary: 'War-risk surcharge applied to the northern approach. Cover for the inner strait quoted case-by-case.',
      entities: [
        { id: 'org-meridian-marine', name: 'Coastal Mutual Marine', kind: 'organisation', materialised: true },
        { id: 'cohort-underwriters', name: 'Underwriting syndicates', kind: 'cohort', materialised: false, note: 'Aggregate only — no individual is materialised' },
      ],
      contributors: [
        { label: 'Route risk reclassified', mechanism: 'Insurer risk-repricing rule', weight: 'primary' },
        { label: 'Claims exposure forecast', mechanism: 'Insurer risk-repricing rule', weight: 'secondary' },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative carrier response', 'Commercial reporting available to this role', 'tick 405'),
      id: 'hop-3',
      ordinal: 3,
      stage: 'Carrier rerouting',
      actor: 'Shipping lines',
      summary: 'Three lines suspend Kestral calls and reroute south. Added transit time quoted at nine to eleven days.',
      entities: [
        { id: 'org-anseld-line', name: 'Anseld Line', kind: 'business', materialised: true },
      ],
      contributors: [
        { label: 'Premium increase', mechanism: 'Carrier cost-avoidance response', weight: 'primary' },
        { label: 'Schedule reliability', mechanism: 'Carrier cost-avoidance response', weight: 'secondary' },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative exposure model', 'Economic reporting available to this role', 'tick 407'),
      id: 'hop-4',
      ordinal: 4,
      stage: 'Port and employment exposure',
      actor: 'Kestral port district',
      summary: 'Dock rosters cut. Handling, haulage and warehousing shifts reduced across the port district.',
      entities: [
        { id: 'cohort-dockworkers', name: 'Port district workers', kind: 'cohort', materialised: false, note: 'Aggregate cohort — represents a weighted population, not individuals' },
        { id: 'person-ilva', name: 'Ilva Marren', kind: 'person', materialised: true, note: 'Port union convenor' },
      ],
      contributors: [
        { label: 'Reduced vessel calls', mechanism: 'Port throughput → labour demand', weight: 'primary' },
        { label: 'Warehousing slowdown', mechanism: 'Port throughput → labour demand', weight: 'secondary' },
      ],
    },
    {
      ...env('ASSESSED', 'LOW', 'Fixture author — illustrative household response', 'Survey reporting available to this role', 'tick 409'),
      id: 'hop-5',
      ordinal: 5,
      stage: 'Household expectations',
      actor: 'Coastal households',
      summary: 'Expectation of fuel and staple price rises reported across coastal districts. Precautionary buying noted at three inland depots.',
      entities: [
        { id: 'cohort-coastal-households', name: 'Coastal households', kind: 'cohort', materialised: false, note: 'Aggregate cohort' },
      ],
      contributors: [
        { label: 'Income insecurity', mechanism: 'Employment exposure → household expectation', weight: 'primary' },
        { label: 'Price anticipation', mechanism: 'Supply interruption → price expectation', weight: 'primary' },
      ],
    },
    {
      ...env('DISPUTED', 'LOW', 'Fixture author — two competing assessments retained', 'Open media monitoring', 'tick 410'),
      id: 'hop-6',
      ordinal: 6,
      stage: 'Media and family activity',
      actor: 'Press, broadcast and crew families',
      summary:
        'Crew families hold a vigil at the port gate. Coverage splits: one framing treats the closure as external coercion, another as government mishandling.',
      entities: [
        { id: 'org-vantara-broadcast', name: 'Vantara Broadcast', kind: 'organisation', materialised: true },
        { id: 'person-teo', name: 'Teo Halvard', kind: 'person', materialised: true, note: 'Crew family spokesperson' },
      ],
      contributors: [
        { label: 'External-coercion framing', mechanism: 'Narrative adoption among coastal audiences', weight: 'contested' },
        { label: 'Government-mishandling framing', mechanism: 'Narrative adoption among inland audiences', weight: 'contested' },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative political response', 'Parliamentary reporting', 'tick 411'),
      id: 'hop-7',
      ordinal: 7,
      stage: 'Political pressure',
      actor: 'Assembly and coalition partners',
      summary: 'Opposition tables an urgent question. Two coalition partners request the legal advice underpinning the holding posture.',
      entities: [
        { id: 'org-assembly', name: 'National Assembly', kind: 'organisation', materialised: true },
        { id: 'person-rusk', name: 'Della Rusk', kind: 'person', materialised: true, note: 'Coalition finance spokesperson' },
      ],
      contributors: [
        { label: 'Constituency employment exposure', mechanism: 'Local exposure → representative pressure', weight: 'primary' },
        { label: 'Media framing pressure', mechanism: 'Narrative adoption → political salience', weight: 'secondary' },
      ],
    },
    {
      ...env('UNKNOWN', 'NOT_APPLICABLE', 'Not modelled — no engine evaluates outcomes', 'Would require an authoritative options model', 'tick 412'),
      id: 'hop-8',
      ordinal: 8,
      stage: 'Government options',
      actor: 'Executive',
      summary: null as unknown as string,
      entities: [],
      contributors: [],
    },
  ],

  panels: [
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative civil response', 'Open reporting', 'tick 410'),
      id: 'panel-civil',
      title: 'Civilian and family response',
      standfirst: 'Who is affected, and how they are responding',
      claims: [
        {
          ...env('AUTHORITATIVE', 'HIGH', 'Fixture author — scenario definition', 'Publicly observable', 'tick 410'),
          id: 'c-vigil', label: 'Vigil at port gate', value: 'Fourth consecutive evening',
        },
        {
          ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative survey', 'Survey reporting', 'tick 409'),
          id: 'c-precaution', label: 'Precautionary buying', value: 'Reported at three inland depots',
        },
        {
          ...env('UNKNOWN', 'NOT_APPLICABLE', 'No mechanism produces this', 'Would require a household model', 'tick 412'),
          id: 'c-hardship', label: 'Household hardship', value: null, absence: 'UNKNOWN',
          detail: 'No household-level model exists. This is not zero — it is unmeasured.',
        },
      ],
    },
    {
      ...env('DISPUTED', 'LOW', 'Fixture author — competing assessments retained', 'Open media monitoring', 'tick 410'),
      id: 'panel-media',
      title: 'Media and narratives',
      standfirst: 'Competing framings, both retained',
      claims: [
        {
          ...env('DISPUTED', 'LOW', 'Fixture author — framing A', 'Open media monitoring', 'tick 410'),
          id: 'm-coercion', label: 'External coercion framing', value: 'Dominant in coastal coverage',
          detail: 'Competing assessment: see “Government mishandling framing”.',
        },
        {
          ...env('DISPUTED', 'LOW', 'Fixture author — framing B', 'Open media monitoring', 'tick 410'),
          id: 'm-mishandling', label: 'Government mishandling framing', value: 'Dominant in inland coverage',
          detail: 'Competing assessment: see “External coercion framing”.',
        },
        {
          ...env('PRESENTATION_ONLY', 'NOT_APPLICABLE', 'Fixture author — illustrative label only', 'Presentation element', 'tick 412'),
          id: 'm-tone', label: 'Coverage tone', value: 'Escalating',
          detail: 'Presentation-only label. No mechanism computes tone; this must never influence outcomes.',
        },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative market response', 'Commercial reporting', 'tick 407'),
      id: 'panel-markets',
      title: 'Shipping, insurance and markets',
      standfirst: 'Commercial reaction to the closure',
      claims: [
        {
          ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative insurer response', 'Commercial reporting', 'tick 404'),
          id: 'k-warrisk', label: 'War-risk surcharge', value: 'Applied — northern approach',
        },
        {
          ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative carrier response', 'Commercial reporting', 'tick 405'),
          id: 'k-reroute', label: 'Lines suspending calls', value: 'Three of eleven',
        },
        {
          ...env('UNKNOWN', 'NOT_APPLICABLE', 'No fiscal path exists in the engine', 'Would require a treasury model', 'tick 412'),
          id: 'k-treasury', label: 'Treasury exposure', value: null, absence: 'UNAVAILABLE',
          detail: 'Unavailable, not zero. No engine action touches fiscal state.',
        },
      ],
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative political response', 'Parliamentary reporting', 'tick 411'),
      id: 'panel-politics',
      title: 'Political pressure and foreign response',
      standfirst: 'Domestic pressure, foreign governments and foreign publics',
      claims: [
        {
          ...env('AUTHORITATIVE', 'HIGH', 'Fixture author — scenario definition', 'Parliamentary record', 'tick 411'),
          id: 'p-uq', label: 'Urgent question tabled', value: 'Opposition — tomorrow’s sitting',
        },
        {
          ...env('ASSESSED', 'MEDIUM', 'Fixture author — illustrative coalition response', 'Parliamentary reporting', 'tick 411'),
          id: 'p-legal', label: 'Legal advice requested', value: 'Two coalition partners',
        },
        {
          ...env('ASSESSED', 'LOW', 'Fixture author — illustrative foreign response', 'Diplomatic reporting', 'tick 409'),
          id: 'p-foreign-gov', label: 'Foreign governments', value: 'Two states seek clarification of transit intent',
        },
        {
          ...env('ASSESSED', 'LOW', 'Fixture author — illustrative foreign public response', 'Open media monitoring', 'tick 410'),
          id: 'p-foreign-pub', label: 'Foreign publics', value: 'Solidarity coverage in one neighbouring state',
        },
      ],
    },
  ],

  queue: [
    {
      ...env('AUTHORITATIVE', 'HIGH', 'Fixture author — illustrative decision', 'Assigned to this role', 'tick 412'),
      id: 'q-1',
      title: 'Respond to the urgent question',
      detail: 'The Assembly sits tomorrow. A response posture has not been selected.',
      affordances: ['Draft a response posture', 'Request legal advice first', 'Defer to the Foreign Secretary'],
      deadline_label: 'Before tick 420',
    },
    {
      ...env('AUTHORITATIVE', 'HIGH', 'Fixture author — illustrative decision', 'Assigned to this role', 'tick 411'),
      id: 'q-2',
      title: 'Publish or withhold the legal advice',
      detail: 'Two coalition partners have requested it. Publication is irreversible.',
      affordances: ['Publish in full', 'Publish a summary', 'Withhold and state why'],
      deadline_label: 'Before tick 418',
    },
  ],

  stream: [
    {
      ...env('AUTHORITATIVE', 'HIGH', 'Fixture author', 'Publicly observable', 'tick 412'),
      id: 's-1', tick: 412, text: 'Coalition finance spokesperson requests the legal advice.', relevance: 'normal',
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author', 'Open media monitoring', 'tick 411'),
      id: 's-2', tick: 411, text: 'Vigil at the port gate enters a fourth evening.', relevance: 'normal',
    },
    {
      ...env('ASSESSED', 'MEDIUM', 'Fixture author', 'Commercial reporting', 'tick 410'),
      id: 's-3', tick: 410, text: 'A third line suspends Kestral calls.', relevance: 'normal',
    },
    {
      ...env('PRESENTATION_ONLY', 'NOT_APPLICABLE', 'Fixture author — routine log line', 'Presentation element', 'tick 409'),
      id: 's-4', tick: 409, text: 'Routine port bulletin published. No change to holding posture.', relevance: 'low',
    },
    {
      ...env('PRESENTATION_ONLY', 'NOT_APPLICABLE', 'Fixture author — routine log line', 'Presentation element', 'tick 408'),
      id: 's-5', tick: 408, text: 'Weather advisory lifted for the southern route.', relevance: 'low',
    },
  ],
}
