/**
 * MERIDIAN C0 prototype — application shell and entry point.
 *
 * FIXTURE DATA ONLY. Nothing in this application is connected to the simulation engine. There is
 * no live model call, no authoritative validation, no cross-tier propagation, no event sourcing,
 * no replay, no state hashing, no persistence, no role-based access enforcement and no tier
 * promotion. The interface must not imply any of them.
 */

import './tokens.css'
import './styles.css'

import { kestralStrait } from './fixtures/kestral-strait.v1.ts'
import { assertEnvelope } from './fixtures/types.ts'
import type { Envelope } from './fixtures/types.ts'
import { disclosureBands, disclosureFooter } from './components/disclosure.ts'
import { provenanceDetail } from './components/provenance.ts'
import { statusMeaning } from './components/epistemic.ts'
import { decisionQueue, eventStream, strategicCommandCentre } from './screens/strategic-command-centre.ts'

const fx = kestralStrait

/**
 * Build-time honesty gate. Every displayable record must carry a complete envelope declaring it
 * as prototype fixture data. Unmarked content is a build failure (research F9) — labelling only
 * some content raises the apparent authority of everything unlabelled.
 */
function verifyFixtureHonesty(): void {
  assertEnvelope(fx.crisis, 'crisis')
  fx.chain.forEach((h, i) => assertEnvelope(h, `chain[${i}]`))
  fx.panels.forEach((p, i) => {
    assertEnvelope(p, `panels[${i}]`)
    p.claims.forEach((c, j) => assertEnvelope(c, `panels[${i}].claims[${j}]`))
  })
  fx.queue.forEach((q, i) => {
    assertEnvelope(q, `queue[${i}]`)
    // HSE's rule made machine-checkable: a status indicator must not be designated a decision.
    if (q.affordances.length === 0) {
      throw new Error(`[fixture-honesty] queue[${i}] has no affordance — it is a stream event, not a decision`)
    }
  })
  fx.stream.forEach((s, i) => assertEnvelope(s, `stream[${i}]`))
  if (fx.world.is_fictional !== true) {
    throw new Error('[fixture-honesty] world.is_fictional must be literally true')
  }
}

const NAV = [
  { id: 'situation', label: 'Situation', active: true },
  { id: 'society', label: 'Society Pulse', active: false },
  { id: 'entities', label: 'Entities', active: false },
  { id: 'timeline', label: 'Causal Timeline', active: false },
  { id: 'composer', label: 'Command', active: false },
]

function shell(): string {
  return `
  ${disclosureBands()}

  <div class="statusbar" role="region" aria-label="Scenario and role status">
    <div class="statusbar__left">
      <span class="brand">MERIDIAN</span>
      <span class="sb__world">${fx.world.name}</span>
      <span class="sb__tag">FICTIONAL</span>
    </div>
    <div class="statusbar__right">
      <span class="sb__item"><span class="sb__k">scenario</span><span class="sb__v">${fx.scenario_id} v${fx.scenario_version}</span></span>
      <span class="sb__item"><span class="sb__k">tick</span><span class="sb__v mono">${fx.simulation_tick}</span></span>
      <span class="sb__item"><span class="sb__k">clock</span><span class="sb__v">HELD</span></span>
      <span class="sb__item"><span class="sb__k">role</span><span class="sb__v">${fx.player_role}</span></span>
      <span class="sb__mode" title="Mode is indicated by text and border weight, never colour alone.">EXPLORE</span>
    </div>
  </div>

  <div class="layout">
    <nav class="nav" aria-label="Primary">
      <ul>
        ${NAV.map(
          (n) => `<li><a class="nav__item ${n.active ? 'is-active' : 'is-disabled'}"
              ${n.active ? 'href="#main" aria-current="page"' : 'aria-disabled="true" tabindex="-1"'}>
            ${n.label}${n.active ? '' : '<span class="nav__soon">not built</span>'}
          </a></li>`,
        ).join('')}
      </ul>
      <p class="nav__note">Four screens are specified but not built. They are listed so the shell's shape is honest, and disabled so it is clear they do not exist.</p>
    </nav>

    <main class="main" id="main" aria-label="Strategic Command Centre">
      ${strategicCommandCentre(fx)}
    </main>

    <aside class="context" aria-label="Context and inspection">
      ${decisionQueue(fx)}
      <section class="inspector" aria-label="Inspector" id="inspector">
        <h3 class="secthead">Inspector</h3>
        <div id="inspector-body" class="inspector__body">
          <p class="inspector__empty">Select any card, chain hop, claim or event to inspect its epistemic status, provenance and visibility basis.</p>
        </div>
      </section>
    </aside>
  </div>

  ${eventStream(fx)}

  ${disclosureFooter()}
  `
}

/** Index every displayable record by id so the inspector can resolve a selection. */
function buildIndex(): Map<string, { title: string; env: Envelope }> {
  const idx = new Map<string, { title: string; env: Envelope }>()
  idx.set(fx.crisis.id, { title: fx.crisis.name, env: fx.crisis })
  fx.chain.forEach((h) => idx.set(h.id, { title: `${h.ordinal}. ${h.stage}`, env: h }))
  fx.panels.forEach((p) => {
    idx.set(p.id, { title: p.title, env: p })
    p.claims.forEach((c) => idx.set(c.id, { title: c.label, env: c }))
  })
  fx.queue.forEach((q) => idx.set(q.id, { title: q.title, env: q }))
  fx.stream.forEach((s) => idx.set(s.id, { title: `t${s.tick} — ${s.text}`, env: s }))
  return idx
}

function wireInspector(root: HTMLElement): void {
  const index = buildIndex()
  const body = root.querySelector<HTMLElement>('#inspector-body')
  if (!body) return

  const select = (id: string): void => {
    const hit = index.get(id)
    if (!hit) return
    root.querySelectorAll('.is-selected').forEach((n) => n.classList.remove('is-selected'))
    root.querySelectorAll(`[data-card-id="${CSS.escape(id)}"]`).forEach((n) => n.classList.add('is-selected'))
    body.innerHTML = `
      <h4 class="inspector__title">${hit.title}</h4>
      <p class="inspector__meaning">${statusMeaning(hit.env.epistemic_status)}</p>
      ${provenanceDetail(hit.env)}
      <p class="inspector__warn">This record is hand-authored fixture data. It was not produced by the simulation engine.</p>`
  }

  root.addEventListener('click', (ev) => {
    const el = (ev.target as HTMLElement | null)?.closest<HTMLElement>('[data-card-id]')
    if (el?.dataset.cardId) select(el.dataset.cardId)
  })
  root.addEventListener('keydown', (ev) => {
    if (ev.key !== 'Enter' && ev.key !== ' ') return
    const el = (ev.target as HTMLElement | null)?.closest<HTMLElement>('[data-card-id]')
    if (el?.dataset.cardId) {
      ev.preventDefault()
      select(el.dataset.cardId)
    }
  })
}

export function mount(root: HTMLElement): void {
  verifyFixtureHonesty()
  root.innerHTML = shell()
  wireInspector(root)
}

const app = document.getElementById('app')
if (app) mount(app)
