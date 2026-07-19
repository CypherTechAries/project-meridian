/**
 * Strategic Command Centre — redesigned.
 *
 * WHAT CHANGED AND WHY. The first build gave every card equal weight and opened with a text
 * briefing, so the eye had nowhere to land and the user had to read before understanding. It read
 * as a case-management dashboard. This version establishes a deliberate hierarchy within the first
 * five seconds:
 *
 *   1. Where is the crisis?        → the situation map dominates
 *   2. What is happening now?      → crisis status, one large number
 *   3. How severe?                 → key metrics with trend
 *   4. How is society reacting?    → cohort impact, population-weighted
 *   5. What must I decide?         → decision rail, right
 *   6. What is real?               → compact origin markers everywhere
 *
 * The complete eight-stage causal trace has been REMOVED from this screen. It belongs in the
 * Causal Timeline. The command centre shows the strategic consequence, not every underlying
 * record — showing both was the main cause of the previous screen's flatness.
 *
 * Values marked `E` come from a genuine P0.5 engine run. Values marked `F` are hand-authored
 * fixture content. The distinction is per-record and never aggregated across origins.
 */

import type { OptionEntry, Projection, RunResult } from '../engine/client.ts'
import { stageByField } from '../engine/client.ts'
import { escapeHtml } from '../components/epistemic.ts'
import { originBadge, originLegend, panelHead } from '../components/origin.ts'
import { bar, mapLegend, situationMap, sparkline, trajectoryChart } from '../components/viz.ts'

/** Domain accents. Colour carries meaning here, and never carries it alone. */
const TONE: Record<string, string> = {
  incident_severity: 'crisis',
  insurer_risk: 'logistics',
  premium_pressure: 'logistics',
  rerouting_level: 'logistics',
  port_activity_deficit: 'economic',
  employment_pressure: 'economic',
  household_expectation_pressure: 'social',
  narrative_attention: 'narrative',
  collective_activity: 'narrative',
  political_pressure: 'political',
}

/** Compact chain summary. The FULL trace lives in the Causal Timeline, not here. */
const CHAIN_SUMMARY = [
  { field: 'incident_severity', short: 'Incident', tone: 'crisis' },
  { field: 'insurer_risk', short: 'Insurer risk', tone: 'logistics' },
  { field: 'rerouting_level', short: 'Rerouting', tone: 'logistics' },
  { field: 'employment_pressure', short: 'Employment', tone: 'economic' },
  { field: 'household_expectation_pressure', short: 'Households', tone: 'social' },
  { field: 'narrative_attention', short: 'Narrative', tone: 'narrative' },
  { field: 'political_pressure', short: 'Politics', tone: 'political' },
]

/*
 * Four metrics, not six. 'political_pressure' IS the Crisis status headline and 'narrative_attention'
 * already appears in the propagation summary — repeating them here bought duplication, not insight,
 * and pushed the fourth row out of the panel. All seven chain values remain on screen.
 */
const KEY_METRICS = [
  'insurer_risk',
  'rerouting_level',
  'employment_pressure',
  'household_expectation_pressure',
]

/** Short display names. The projection's full labels are correct but too long for a metric row. */
const SHORT_LABEL: Record<string, string> = {
  insurer_risk: 'Insurer risk',
  rerouting_level: 'Rerouting',
  employment_pressure: 'Employment',
  household_expectation_pressure: 'Households',
  narrative_attention: 'Narrative attention',
  political_pressure: 'Political pressure',
}

/**
 * Direction over the last five ticks of the run's OWN trajectory. This is a description of values
 * the engine already produced, not a forecast and not a rate: no extrapolation, no smoothing.
 * Returns null when there is too little trajectory to say anything truthful.
 */
function direction(series: number[]): { word: string; tone: string } | null {
  if (series.length < 6) return null
  const now = series[series.length - 1] ?? 0
  const then = series[series.length - 6] ?? 0
  const delta = now - then
  // Threshold is relative to the value's own scale, so small series are not called "rising".
  if (Math.abs(delta) < Math.max(0.004, Math.abs(now) * 0.02)) return { word: 'STABLE', tone: 'flat' }
  return delta > 0 ? { word: 'RISING', tone: 'up' } : { word: 'EASING', tone: 'down' }
}

function severityWord(v: number): string {
  if (v >= 0.5) return 'SEVERE'
  if (v >= 0.25) return 'ELEVATED'
  if (v > 0) return 'EMERGING'
  return 'AT REST'
}

function optionRow(o: OptionEntry): string {
  const state = o.value.toLowerCase()
  return `<li class="opt" data-card-id="${escapeHtml(o.option_id)}" tabindex="0" role="button"
      aria-label="${escapeHtml(o.label.replace(/_/g, ' '))} — ${escapeHtml(o.value)}. Select to inspect.">
    <span class="opt__name">${escapeHtml(o.label.replace(/_/g, ' '))}</span>
    <span class="opt__state opt__state--${state}">
      <span class="opt__dot" aria-hidden="true"></span>${escapeHtml(o.value)}
    </span>
  </li>`
}

function metricRow(p: Projection, traj: RunResult['trajectory'], field: string): string {
  const s = stageByField(p, field)
  if (!s) return ''
  const tone = TONE[field] ?? 'neutral'
  const series = traj.map((t) => Number(t[field] ?? 0))
  const dir = direction(series)
  return `<li class="krow" data-card-id="${escapeHtml(field)}" tabindex="0" role="button"
      aria-label="${escapeHtml(s.label)} ${s.value.toFixed(4)}${dir ? `, ${dir.word.toLowerCase()} over the last five ticks` : ''}. Select to inspect provenance.">
    <span class="krow__label">${escapeHtml(SHORT_LABEL[field] ?? s.label)}</span>
    ${sparkline(series, tone)}
    <span class="krow__val krow__val--${tone}">${s.value.toFixed(4)}</span>
    ${dir ? `<span class="krow__dir krow__dir--${dir.tone}">${dir.word}</span>` : '<span class="krow__dir krow__dir--none">—</span>'}
  </li>`
}

export function commandCentre(run: RunResult): string {
  const p = run.projection
  const traj = run.trajectory
  const political = stageByField(p, 'political_pressure')?.value ?? 0
  const incident = stageByField(p, 'incident_severity')?.value ?? 0
  const rerouting = stageByField(p, 'rerouting_level')?.value ?? 0
  const household = stageByField(p, 'household_expectation_pressure')?.value ?? 0
  const engineOrigin = run.connection === 'unavailable' ? 'unavailable' : 'engine'

  return `
  <div class="scc">

    <!-- ── Situation map: the dominant element ─────────────────────────── -->
    <section class="panel panel--map" aria-labelledby="p-map">
      ${panelHead('Situation overview', 'Fictional Kestral Strait — routing state', engineOrigin, { id: 'p-map' })}
      <div class="panel__body panel__body--flush">
        ${situationMap(rerouting, p.incident_active)}
        <div class="map__foot">
          ${mapLegend()}
          <span class="map__note">Invented geography. No real-world map data.</span>
        </div>
      </div>
    </section>

    <!-- ── Crisis status: one large number ─────────────────────────────── -->
    <section class="panel panel--crisis" aria-labelledby="p-crisis">
      ${panelHead('Crisis status', 'Political pressure', engineOrigin, { id: 'p-crisis' })}
      <div class="panel__body">
        <div class="bignum" data-card-id="political_pressure" tabindex="0" role="button"
             aria-label="Political pressure ${political.toFixed(4)} of 1.000, ${severityWord(political)}. Select to inspect.">
          <span class="bignum__value">${political.toFixed(4)}</span>
          <span class="bignum__scale">/ 1.000</span>
          <span class="bignum__word bignum__word--${severityWord(political).toLowerCase().replace(' ', '-')}">${severityWord(political)}</span>
        </div>
        ${trajectoryChart(traj, [{ field: 'political_pressure', label: 'Political pressure', tone: 'political' }], 66)}
      </div>
    </section>

    <!-- ── Government options ──────────────────────────────────────────── -->
    <section class="panel panel--options" aria-labelledby="p-opts">
      ${panelHead('Decision options', 'Availability and constraints', engineOrigin, { id: 'p-opts' })}
      <div class="panel__body">
        <ul class="opts">${p.government_options.map(optionRow).join('')}</ul>
        <div class="chainsum">
          <h3 class="chainsum__h">Propagation to here</h3>
          <ol class="chainsum__list">${CHAIN_SUMMARY.map((c) => {
            const v = stageByField(p, c.field)?.value ?? 0
            return `<li class="chainsum__step">
              <span class="chainsum__dot chainsum__dot--${c.tone}" aria-hidden="true"></span>
              <span class="chainsum__name">${escapeHtml(c.short)}</span>
              <span class="chainsum__val">${v.toFixed(3)}</span>
            </li>`
          }).join('')}</ol>
          <p class="chainsum__note">Summary only. The full nine-mechanism trace belongs in Causal Timeline.</p>
        </div>
      </div>
      <p class="panel__foot">Status only. This prototype computes no cost or effect for an option, and none can be executed.</p>
    </section>

    <!-- ── Key metrics ─────────────────────────────────────────────────── -->
    <section class="panel panel--metrics" aria-labelledby="p-metrics">
      ${panelHead(`Key metrics`, 'Engine indicators', engineOrigin, { id: 'p-metrics' })}
      <div class="panel__body">
        <ul class="krows">${KEY_METRICS.map((f) => metricRow(p, traj, f)).join('')}</ul>
      </div>
    </section>

    <!-- ── Incident ────────────────────────────────────────────────────── -->
    <section class="panel panel--incident" aria-labelledby="p-incident">
      ${panelHead('Incident status', p.incident_active ? 'Active blockade' : 'No active incident', engineOrigin, { id: 'p-incident' })}
      <div class="panel__body">
        <div class="incident" data-card-id="incident_severity" tabindex="0" role="button"
             aria-label="Incident severity ${incident.toFixed(3)}. Select to inspect.">
          <div class="incident__row">
            <span class="incident__label">Severity</span>
            <span class="incident__val">${incident.toFixed(3)}</span>
          </div>
          ${bar(incident, 'crisis')}
        </div>
      </div>
      <p class="panel__foot">Active for ${p.tick} ticks · ${p.simulated_hours.toFixed(0)} simulated hours</p>
    </section>

    <!-- ── Cohort impact: population-weighted ──────────────────────────── -->
    <section class="panel panel--cohorts" aria-labelledby="p-cohorts">
      ${panelHead('Cohort impact', 'Population-weighted concern', engineOrigin, { id: 'p-cohorts' })}
      <div class="panel__body">
        <ul class="cohorts">${p.cohorts
          .slice()
          .sort((a, b) => b.value - a.value)
          .map(
            (c, i) => `<li class="cohort${i === 0 ? ' cohort--top' : ''}" data-card-id="${escapeHtml(c.cohort_id)}" tabindex="0" role="button"
              aria-label="${escapeHtml(c.label)} concern ${c.value.toFixed(3)}, representing ${c.represents_population.toLocaleString()} people, ${(c.population_share * 100).toFixed(1)} per cent of aggregate weight${i === 0 ? '. Most affected cohort' : ''}. Select to inspect.">
              <span class="cohort__name">${escapeHtml(c.label.replace(/-/g, ' '))}</span>
              <span class="cohort__val">${c.value.toFixed(3)}<span class="cohort__share">${(c.population_share * 100).toFixed(0)}%</span></span>
              ${bar(c.value, 'social')}
            </li>`,
          )
          .join('')}</ul>
        <div class="cohorts__agg" data-card-id="household_expectation_pressure" tabindex="0" role="button"
             aria-label="Population-weighted aggregate concern ${household.toFixed(4)}. Select to inspect.">
          <span class="cohorts__agg-label">Population-weighted aggregate</span>
          <span class="cohorts__agg-val">${household.toFixed(4)}</span>
        </div>
      </div>
      <p class="panel__foot">Population affects aggregate magnitude only — never whether a cohort is right, and never what an individual does.</p>
    </section>

    <!-- ── Intelligence snapshot: honestly fixture ─────────────────────── -->
    <section class="panel panel--intel" aria-labelledby="p-intel">
      ${panelHead('Intelligence snapshot', 'Fixture briefing', 'fixture', { id: 'p-intel' })}
      <div class="panel__body">
        <p class="intel__line">Crew families hold a vigil at the port gate. Coverage splits between external coercion and government mishandling.</p>
      </div>
      <p class="panel__foot">Hand-authored fixture. The engine models no media outlets, no named individuals and no narrative content.</p>
    </section>

    <!-- ── Provenance + origin legend ──────────────────────────────────── -->
    <section class="panel panel--prov" aria-labelledby="p-prov">
      ${panelHead('Provenance', 'Source, status and origin', 'engine', { id: 'p-prov' })}
      <div class="panel__body">
        <dl class="provgrid">
          <dt>Rule pack</dt><dd>${escapeHtml(p.rule_pack_version)}</dd>
          <dt>Scenario</dt><dd>${escapeHtml(p.scenario_id)}</dd>
          <dt>Origin</dt><dd>Mixed — engine and fixture</dd>
          <dt>Status</dt><dd>AUTHORITATIVE</dd>
          <dt>Confidence</dt><dd>NOT_APPLICABLE</dd>
          <dt>Updated</dt><dd>Tick ${p.tick}</dd>
        </dl>
        ${originLegend()}
        <details class="disc-more">
          <summary>What confidence means here</summary>
          <p>Not applicable — the engine computes, it does not estimate. Values follow from declared
          rules, so there is no uncertainty figure to report and a percentage here would be
          fabricated. NOT_APPLICABLE means inapplicable, not withheld and not unknown.</p>
        </details>
      </div>
    </section>
  </div>`
}

/*
 * Right rail: decisions, then the inspector.
 *
 * HONESTY NOTE ON URGENCY. The engine has no clock, no deadline and no expiry, so this rail shows
 * NO countdown and NO due time — inventing one would be fabrication. What it shows instead is real:
 * an option's status is computed from declared thresholds, so ENABLED outranks CONSTRAINED, which
 * outranks AVAILABLE. The consequence domains are read from each option's actual `driven_by` chain
 * field, not authored per option. The affordance inspects; it cannot execute, and says so.
 */

/** Maps a chain field to the domains it bears on. Derived from the field itself, never invented. */
const DOMAIN_OF: Record<string, string[]> = {
  political_pressure: ['political', 'legal'],
  narrative_attention: ['political', 'social'],
  household_expectation_pressure: ['social', 'economic'],
  employment_pressure: ['economic', 'social'],
  rerouting_level: ['economic', 'diplomatic'],
  insurer_risk: ['economic', 'legal'],
  incident_severity: ['diplomatic', 'political'],
}

const PRIORITY: Record<string, number> = { ENABLED: 0, CONSTRAINED: 1, AVAILABLE: 2 }

function domainsFor(drivenBy: string): string[] {
  return DOMAIN_OF[drivenBy.replace('chain.', '')] ?? []
}

function decisionCard(o: OptionEntry, primary: boolean): string {
  const field = o.driven_by.replace('chain.', '')
  const name = o.label.replace(/_/g, ' ')
  const why =
    o.value === 'ENABLED'
      ? `${SHORT_LABEL[field] ?? field} has passed the threshold this option declares, so it is now open.`
      : `${SHORT_LABEL[field] ?? field} has risen far enough to constrain this option, but not to open it.`
  return `<li class="ditem ${primary ? 'ditem--primary' : ''} ditem--${o.value.toLowerCase()}"
      data-card-id="${escapeHtml(o.option_id)}" tabindex="0" role="button"
      aria-label="${escapeHtml(name)} is ${escapeHtml(o.value)}${primary ? ', highest priority' : ''}. ${escapeHtml(why)} Select to inspect.">
    <div class="ditem__top">
      <span class="ditem__state">${escapeHtml(o.value)}</span>
      ${primary ? '<span class="ditem__rank">HIGHEST PRIORITY</span>' : ''}
    </div>
    <span class="ditem__name">${escapeHtml(name)}</span>
    ${primary ? `<p class="ditem__why">${escapeHtml(why)}</p>` : ''}
    <div class="ditem__meta">
      <ul class="dom">${domainsFor(o.driven_by)
        .map((d) => `<li class="dom__chip dom__chip--${d}">${d}</li>`)
        .join('')}</ul>
      <span class="ditem__act" aria-hidden="true">Inspect</span>
    </div>
  </li>`
}

export function decisionRail(run: RunResult): string {
  const p = run.projection
  const enabled = p.government_options
    .filter((o) => o.value !== 'AVAILABLE')
    .slice()
    .sort((a, b) => (PRIORITY[a.value] ?? 9) - (PRIORITY[b.value] ?? 9))

  return `<section class="rail__decisions" aria-labelledby="p-dec">
    <header class="rail__head">
      <h2 class="rail__title" id="p-dec">Decisions awaiting you</h2>
      <span class="rail__count">${enabled.length}</span>
    </header>
    <ul class="dlist">
      ${
        enabled.length
          ? enabled.map((o, i) => decisionCard(o, i === 0)).join('')
          : `<li class="ditem ditem--none">No option has changed status. Political pressure is below every declared threshold.</li>`
      }
    </ul>
    <p class="rail__foot">Display only. Selecting a decision opens its provenance — nothing can be
    submitted, priced, validated or executed in this prototype.</p>
  </section>

  <section class="rail__inspector" aria-labelledby="p-insp">
    <header class="rail__head"><h2 class="rail__title" id="p-insp">Inspector</h2></header>
    <div id="inspector-body" class="rail__body">
      <p class="insp__empty">Select any metric, cohort, option or map element to see its mechanism, source fields and provenance.</p>
    </div>
  </section>`
}

/** Compact bottom strip: the most recent engine transitions. Not a replay, not an event log. */
export function transitionStrip(run: RunResult): string {
  const recent = run.projection.recent_transitions.slice(-4).reverse()
  return `<section class="tstrip" aria-labelledby="p-tstrip">
    <h2 class="tstrip__title" id="p-tstrip">Latest engine changes ${originBadge('engine')}</h2>
    <ul class="tstrip__list">
      ${recent
        .map(
          (t) => `<li class="tstrip__item" data-card-id="${escapeHtml(t.transition_id)}" tabindex="0" role="button"
            aria-label="Tick ${t.tick}, ${escapeHtml(t.mechanism)}. Select to inspect.">
            <span class="tstrip__tick">t${t.tick}</span>
            <span class="tstrip__mech">${escapeHtml(t.mechanism)}</span>
            <span class="tstrip__field">${escapeHtml(Object.keys(t.delta)[0]?.replace('chain.', '') ?? '')}</span>
          </li>`,
        )
        .join('')}
    </ul>
    <span class="tstrip__note">Ephemeral run — not persisted, not a replay.</span>
  </section>`
}

