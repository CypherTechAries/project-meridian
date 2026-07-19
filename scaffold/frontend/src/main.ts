/**
 * MERIDIAN — application shell.
 *
 * MIXED-ORIGIN SCREEN. The Strategic Command Centre now shows genuine P0.5 engine output beside
 * hand-authored fixture content. That changes what the global disclosure must say: the old
 * "FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE" would now be FALSE, because part of the
 * screen genuinely is connected. It is replaced with a mixed-origin disclosure, and every record
 * carries its own compact origin marker (E / F / U / N/A).
 *
 * The stronger fixture-only wording is retained for screens that remain entirely fixture-backed.
 */

import './tokens.css'
import './styles.css'

import { initialSnapshot, runDemonstration, stageByField } from './engine/client.ts'
import type { RunResult } from './engine/client.ts'
import { escapeHtml } from './components/epistemic.ts'

import { commandCentre, decisionRail, transitionStrip } from './screens/command-centre.ts'

export const FICTION_DISCLOSURE = 'FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION'
export const MIXED_DISCLOSURE =
  'INTERACTIVE PROTOTYPE — MIXED ENGINE AND FIXTURE DATA — NOT A PREDICTIVE SYSTEM'

const NAV = [
  { id: 'command', label: 'Command Centre', built: true },
  { id: 'society', label: 'Society Pulse', built: false },
  { id: 'timeline', label: 'Causal Timeline', built: false },
  { id: 'entities', label: 'Entity Dossiers', built: false },
  { id: 'composer', label: 'Command', built: false },
]

/** Plain-language band for a 0..1 chain value. Describes, never predicts. */
function severityPhrase(v: number): string {
  if (v >= 0.5) return 'severe'
  if (v >= 0.25) return 'elevated'
  if (v > 0) return 'emerging'
  return 'at rest'
}

function disclosures(): string {
  return `<div class="disclosures" role="region" aria-label="Prototype disclosures">
    <span class="disc"><span class="disc__glyph" aria-hidden="true">◈</span>${FICTION_DISCLOSURE}</span>
    <span class="disc__sep" aria-hidden="true">│</span>
    <span class="disc disc--mixed">${MIXED_DISCLOSURE}</span>
  </div>`
}

function brandMark(): string {
  return `<svg class="brand__mark" viewBox="0 0 32 32" aria-hidden="true">
    <circle cx="16" cy="16" r="13" fill="none" stroke="var(--cyan-dim)" stroke-width="1.2"/>
    <ellipse cx="16" cy="16" rx="6.5" ry="13" fill="none" stroke="var(--cyan-dim)" stroke-width="0.9"/>
    <line x1="3" y1="16" x2="29" y2="16" stroke="var(--cyan-dim)" stroke-width="0.9"/>
    <line x1="16" y1="1" x2="16" y2="31" stroke="var(--cyan)" stroke-width="1.2"/>
    <circle cx="16" cy="16" r="2.2" fill="var(--cyan)"/>
  </svg>`
}

function topbar(run: RunResult): string {
  const p = run.projection
  const conn =
    run.connection === 'live'
      ? '<span class="tb__v tb__v--live">LIVE</span>'
      : `<span class="tb__v tb__v--stale">${run.connection === 'snapshot' ? 'SNAPSHOT' : 'UNAVAILABLE'}</span>`
  return `<div class="topbar" role="region" aria-label="Scenario and run status">
    <div class="topbar__left">
      <h1 class="scenario-title">Kestral Strait</h1>
      <span class="scenario-sub">Demonstration run — ${escapeHtml(run.mode)}</span>
    </div>
    <div class="topbar__right">
      <span class="tb"><span class="tb__k">engine</span>${conn}</span>
      <span class="tb"><span class="tb__k">rule pack</span><span class="tb__v">${escapeHtml(p.rule_pack_version)}</span></span>
      <span class="tb"><span class="tb__k">tick</span><span class="tb__v">Tick ${p.tick}</span></span>
      <span class="tb"><span class="tb__k">horizon</span><span class="tb__v">${p.demonstration_horizon_ticks} ticks · ${(p.simulated_hours / 24).toFixed(0)} days</span></span>
    </div>
  </div>`
}

function nav(run: RunResult): string {
  const p = run.projection
  return `<nav class="nav" aria-label="Primary">
    <div class="brand">${brandMark()}<span class="brand__name">MERIDIAN</span></div>
    <ul>
      ${NAV.map(
        (n) => `<li><a class="nav__item ${n.built ? 'is-active' : 'is-disabled'}"
          ${n.built ? 'href="#main" aria-current="page"' : 'aria-disabled="true" tabindex="-1"'}>
          <span>${n.label}</span>${n.built ? '' : '<span class="nav__tag">not built</span>'}
        </a></li>`,
      ).join('')}
    </ul>
    <div class="sysblock">
      <h2 class="sysblock__h">System status</h2>
      <div class="sysrow"><span class="sysrow__k">Engine</span><span class="sysrow__v ${run.connection === 'live' ? 'sysrow__v--ok' : 'sysrow__v--warn'}">${run.connection === 'live' ? 'ONLINE' : 'OFFLINE'}</span></div>
      <div class="sysrow"><span class="sysrow__k">Data</span><span class="sysrow__v sysrow__v--warn">MIXED</span></div>
      <div class="sysrow"><span class="sysrow__k">Scenario</span><span class="sysrow__v">${escapeHtml(p.scenario_id)}</span></div>
      <div class="sysrow"><span class="sysrow__k">Seed</span><span class="sysrow__v">${run.seed}</span></div>
      <div class="sysrow"><span class="sysrow__k">Revision</span><span class="sysrow__v">${p.state_revision}</span></div>
    </div>
  </nav>`
}

function shell(run: RunResult): string {
  return `${disclosures()}
  ${topbar(run)}
  <div class="layout">
    ${nav(run)}
    <main class="main" id="main" aria-label="Strategic Command Centre">${commandCentre(run)}</main>
    <aside class="rail" aria-label="Decisions and inspector">${decisionRail(run)}</aside>
  </div>
  ${transitionStrip(run)}`
}

/** Inspector: full provenance lives here, not on every card. */
function wireInspector(root: HTMLElement, run: RunResult): void {
  const p = run.projection
  const body = root.querySelector<HTMLElement>('#inspector-body')
  if (!body) return

  const index = new Map<string, { title: string; detail: string }>()

  /*
   * TWO LAYERS. Mechanism identifiers and raw chain field names made the inspector read as a
   * debugger. The operational summary now leads in plain language; the identifiers are unchanged
   * and complete, one disclosure away, so a technical reviewer loses nothing.
   */
  const plain = (f: string): string => (f.replace('chain.', '').replace(/_/g, ' '))

  for (const s of p.stages) {
    const sources = s.source_fields.map(plain)
    index.set(s.field, {
      title: s.label,
      detail: `
        <ul class="insp__sum">
          <li><strong>${escapeHtml(s.label)}</strong> is ${escapeHtml(severityPhrase(s.value))},
              at ${s.value.toFixed(4)} of 1.000.</li>
          ${sources.length ? `<li>Driven by ${escapeHtml(sources.join(' and '))}.</li>` : ''}
          <li>${escapeHtml(s.lifecycle)}</li>
          <li>Updated at tick ${s.last_updated_tick}${s.lag_ticks ? `, ${s.lag_ticks} tick(s) behind its cause` : ''}.</li>
        </ul>
        <details class="insp__tech">
          <summary>Technical detail</summary>
          <dl class="provgrid">
            <dt>Mechanism</dt><dd>${escapeHtml(s.mechanism ?? '—')}</dd>
            <dt>Version</dt><dd>${escapeHtml(s.mechanism_version ?? '—')}</dd>
            <dt>Exact value</dt><dd>${s.value.toFixed(6)}</dd>
            <dt>Origin</dt><dd>${escapeHtml(s.origin)}</dd>
            <dt>Status</dt><dd>${escapeHtml(s.epistemic_status)}</dd>
            <dt>Confidence</dt><dd>${escapeHtml(s.confidence)}</dd>
            <dt>Stage</dt><dd>${s.stage} — ${escapeHtml(s.stage_name)}</dd>
            <dt>Lag</dt><dd>${s.lag_ticks} tick(s)</dd>
            <dt>Raw sources</dt><dd>${escapeHtml(s.source_fields.join(', '))}</dd>
            <dt>Updated</dt><dd>tick ${s.last_updated_tick}</dd>
          </dl>
        </details>`,
    })
  }
  for (const c of p.cohorts) {
    index.set(c.cohort_id, {
      title: c.label.replace(/-/g, ' '),
      detail: `
        <p class="insp__mech">${escapeHtml(c.provenance)}</p>
        <dl class="provgrid">
          <dt>Concern</dt><dd>${c.value.toFixed(6)}</dd>
          <dt>Population</dt><dd>${c.represents_population.toLocaleString()}</dd>
          <dt>Share</dt><dd>${(c.population_share * 100).toFixed(2)}% of aggregate weight</dd>
          <dt>Exposure</dt><dd>${c.income_sensitivity.toFixed(2)} (declared in scenario)</dd>
          <dt>Origin</dt><dd>${escapeHtml(c.origin)}</dd>
        </dl>
        <p class="insp__note">Population affects aggregate magnitude only. It says nothing about
        whether this cohort is right, and nothing about what any individual does.</p>`,
    })
  }
  for (const o of p.government_options) {
    index.set(o.option_id, {
      title: o.label.replace(/_/g, ' '),
      detail: `
        <p class="insp__mech">${escapeHtml(o.provenance)}</p>
        <dl class="provgrid">
          <dt>Status</dt><dd>${escapeHtml(o.value)}</dd>
          <dt>Driven by</dt><dd>${escapeHtml(o.driven_by)}</dd>
          <dt>Origin</dt><dd>${escapeHtml(o.origin)}</dd>
        </dl>
        <p class="insp__note">Status only. No cost, effect or execution path exists for any option
        in this prototype.</p>`,
    })
  }
  for (const t of p.recent_transitions) {
    index.set(t.transition_id, {
      title: `${t.mechanism} · t${t.tick}`,
      detail: `
        <p class="insp__mech">${escapeHtml(t.mechanism)}@${escapeHtml(t.mechanism_version)}</p>
        <dl class="provgrid">
          <dt>Sources</dt><dd>${escapeHtml(t.source_fields.join(', ') || '—')}</dd>
          <dt>Parents</dt><dd>${escapeHtml(t.causal_parents.join(', ') || 'none')}</dd>
          <dt>Draws</dt><dd>${escapeHtml(t.draw_refs.join(', ') || 'none')}</dd>
          <dt>Change</dt><dd>${escapeHtml(JSON.stringify(t.delta).slice(0, 160))}</dd>
        </dl>
        <p class="insp__note">Causal parents record adjacency within a tick. This is not a replay
        and not a reconstructed causal graph — the run is ephemeral and nothing is persisted.</p>`,
    })
  }

  const select = (id: string): void => {
    const hit = index.get(id)
    if (!hit) return
    root.querySelectorAll('.is-selected').forEach((n) => n.classList.remove('is-selected'))
    // Attribute-value matching without CSS.escape, which jsdom does not provide.
    root.querySelectorAll('[data-card-id]').forEach((n) => {
      if ((n as HTMLElement).dataset.cardId === id) n.classList.add('is-selected')
    })
    body.innerHTML = `<h3 class="insp__title">${escapeHtml(hit.title)}</h3>${hit.detail}`
  }

  const handler = (ev: Event): void => {
    const el = (ev.target as HTMLElement | null)?.closest<HTMLElement>('[data-card-id]')
    if (!el?.dataset.cardId) return
    if (ev.type === 'keydown') {
      const k = (ev as KeyboardEvent).key
      if (k !== 'Enter' && k !== ' ') return
      ev.preventDefault()
    }
    select(el.dataset.cardId)
  }
  root.addEventListener('click', handler)
  root.addEventListener('keydown', handler)

  // Open with the headline value selected, so the inspector is never an empty box.
  const political = stageByField(p, 'political_pressure')
  if (political) select(political.field)
}

export function mount(root: HTMLElement, run: RunResult): void {
  root.innerHTML = shell(run)
  wireInspector(root, run)
}

const app = document.getElementById('app')
if (app) {
  // First paint from the bundled recorded snapshot so the layout is inspectable immediately,
  // then replace with a genuine live run. The status chip states which is showing.
  mount(app, initialSnapshot())
  void runDemonstration('incident', 20).then((run) => mount(app, run))
}
