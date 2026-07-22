/**
 * Technical evidence — a reference table, not a dashboard.
 *
 * WHY IT CHANGED. The previous screen was eight panels holding 662 words, 24 decimals and strings
 * like `M-POLITICAL-PRESSURE`, `@1.0.0` and `chain_lag_bookkeeping`. The founder's description was
 * "the notebook of a nuclear physicist", and that is a fair reading of what it was: a dashboard
 * layout applied to reference material.
 *
 * Nobody browses forty exact values. They LOOK ONE UP. So this is a table with a filter, one row
 * per value, sorted by the causal chain the engine declares. Boring and findable beats dense and
 * impressive.
 *
 * It is level 3 of three declared depths — the sentence, the explanation, the number — and it is
 * the ONLY place engine identifiers, mechanism ids and exact decimals may appear.
 */

import type { CohortEntry, OptionEntry, RunResult } from '../engine/client.ts'
import { escapeHtml } from '../components/epistemic.ts'
import { fieldState } from '../engine/presentation.ts'

interface Row {
  /** Plain name a reader can search for. */
  name: string
  /** The engine's own identifier. Level 3 only. */
  id: string
  value: string
  level: string
  direction: string
  origin: string
  /**
   * NOT_APPLICABLE for engine values, and that is a claim, not a gap: the engine COMPUTES a value,
   * it does not estimate one, and no mechanism produces a confidence. Inventing one here would be
   * exactly the fabricated precision the project forbids.
   */
  confidence: string
  tick: string
  mechanism: string
  group: string
  /**
   * The declared question that covers this row's part of the scenario, or null where the catalogue
   * has none. Null rows are not controls — a row that reliably produces a refusal is worse than an
   * inert one. See issue #37.
   */
  ask: string | null
}

/**
 * Row-group → declared question.
 *
 * Deliberately group-level, not per-value. The catalogue answers eight declared questions about
 * areas of the scenario; it cannot answer "tell me about insurer_risk". Promising per-value
 * explanations would be a promise the engine cannot keep, so the instruction above the table says
 * "about that part of the scenario" and means it.
 *
 * Political pressure, narrative attention, collective activity and the government options have no
 * declared question at all — that is issue #37, and those rows are inert rather than misleading.
 */
const GROUP_QUESTION: Record<string, string | null> = {
  'Causal chain': 'How are the economy and supply chains reacting?',
  'Population groups': 'How are people and groups reacting?',
  'Government options': null,
}
const NO_QUESTION_FIELDS = ['political_pressure', 'narrative_attention', 'collective_activity']

function questionFor(group: string, id: string): string | null {
  if (NO_QUESTION_FIELDS.includes(id)) return null
  return GROUP_QUESTION[group] ?? null
}

function num(v: number): string {
  return v.toFixed(4)
}

function chainRows(run: RunResult): Row[] {
  return run.projection.stages.map((s) => {
    const f = fieldState(run, s.field)
    return {
      name: s.label,
      id: s.field,
      value: typeof s.value === 'number' ? num(s.value) : String(s.value),
      level: f ? f.level : 'NOT ESTABLISHED',
      // An unmeasured direction is stated as such. It is never shown as STEADY.
      direction: f ? (f.direction_measured ? f.direction : 'NOT MEASURED') : '—',
      origin: s.origin ?? 'engine',
      confidence: s.confidence ?? 'NOT_APPLICABLE',
      tick: String(s.last_updated_tick ?? ''),
      mechanism: s.provenance ?? '',
      group: 'Causal chain',
      ask: questionFor('Causal chain', s.field),
    }
  })
}

function cohortRows(run: RunResult): Row[] {
  return run.projection.cohorts.map((c: CohortEntry) => ({
    name: c.label.replace(/-/g, ' '),
    id: c.cohort_id,
    value: num(c.value),
    level: '',
    direction: '',
    origin: c.origin ?? 'engine',
    confidence: (c as { confidence?: string }).confidence ?? 'NOT_APPLICABLE',
    tick: String(c.last_updated_tick ?? ''),
    mechanism: c.provenance ?? '',
    group: 'Population groups',
    ask: questionFor('Population groups', c.cohort_id),
  }))
}

function optionRows(run: RunResult): Row[] {
  return run.projection.government_options.map((o: OptionEntry) => ({
    // The projection's label for an option IS the identifier. Show plain words in the name column
    // and keep the identifier underneath, like every other row.
    name: (o.label || o.option_id).replace(/_/g, ' '),
    id: o.option_id,
    value: o.value,
    level: '',
    direction: '',
    origin: o.origin ?? 'engine',
    confidence: (o as { confidence?: string }).confidence ?? 'NOT_APPLICABLE',
    tick: String(o.last_updated_tick ?? ''),
    mechanism: o.driven_by ?? '',
    group: 'Government options',
    ask: questionFor('Government options', o.option_id),
  }))
}

export function technicalRows(run: RunResult): Row[] {
  return [...chainRows(run), ...cohortRows(run), ...optionRows(run)]
}

function tableRow(r: Row): string {
  // THE ROW IS THE CONTROL. Eighteen repeated buttons would be clutter, so the row itself is the
  // affordance and the label appears on hover or focus. `tabindex` + `role="button"` gives keyboard
  // operation and the right screen-reader semantics; a <tr> cannot be a <button>.
  const interactive = r.ask
    ? ` tabindex="0" role="button" data-ask-question="${escapeHtml(r.ask)}"
        aria-label="Ask MERIDIAN about ${escapeHtml(r.name)}"`
    : ''
  return `<tr class="tt__r${r.ask ? ' tt__r--ask' : ''}" data-field="${escapeHtml(r.id)}"
      data-group="${escapeHtml(r.group)}"${interactive}
      data-search="${escapeHtml(`${r.name} ${r.id} ${r.mechanism}`.toLowerCase())}">
    <td class="tt__name">${escapeHtml(r.name)}<span class="tt__id">${escapeHtml(r.id)}</span></td>
    <td class="tt__num">${escapeHtml(r.value)}</td>
    <td>${escapeHtml(r.level)}</td>
    <td>${escapeHtml(r.direction)}</td>
    <td>${escapeHtml(r.origin)}</td>
    <td class="tt__conf">${escapeHtml(r.confidence)}</td>
    <td class="tt__num">${escapeHtml(r.tick)}</td>
    <td class="tt__mech">${escapeHtml(r.mechanism)}</td>
    <td class="tt__askc">${r.ask ? '<span class="tt__ask">Ask about this →</span>' : ''}</td>
  </tr>`
}

export function technicalTable(run: RunResult): string {
  const rows = technicalRows(run)
  const groups = [...new Set(rows.map((r) => r.group))]

  return `<div class="tt" aria-label="Technical evidence">
    <div class="tt__bar">
      <label class="tt__lbl" for="tt-filter">Find a value</label>
      <input id="tt-filter" class="tt__filter" type="search" data-tt-filter autocomplete="off"
             placeholder="name, identifier or mechanism…">
      <span class="tt__count" data-tt-count>${rows.length} values</span>
    </div>
    <p class="tt__note">Every value the run produced, with its identifier, origin, the tick it last
      changed and the mechanism that set it. Exact numbers appear here and nowhere else.</p>
    <p class="tt__hint">Select any row to ask MERIDIAN about that part of the scenario. Rows without
      a declared question are not selectable.</p>
    ${groups
      .map(
        (g) => `<section class="tt__g">
          <h3 class="tt__gh">${escapeHtml(g)}
            <span class="fmark" title="Fictional world">FICTIONAL</span></h3>
          <table class="tt__t">
            <thead><tr>
              <th scope="col">Value</th><th scope="col">Number</th><th scope="col">Level</th>
              <th scope="col">Direction</th><th scope="col">Origin</th>
              <th scope="col">Confidence</th><th scope="col">Tick</th><th scope="col">Mechanism</th>
              <th scope="col"><span class="visually-hidden">Ask MERIDIAN</span></th>
            </tr></thead>
            <tbody>${rows.filter((r) => r.group === g).map(tableRow).join('')}</tbody>
          </table>
        </section>`,
      )
      .join('')}
    <p class="tt__empty" data-tt-empty hidden>No value matches that search.</p>

    <section class="tt__limits" data-tt-limits>
      <h3 class="tt__gh">What this run is, and is not
        <span class="fmark" title="Fictional world">FICTIONAL</span></h3>
      <ul class="tt__lim">
        ${run.limitations.map((l) => `<li>${escapeHtml(l)}</li>`).join('')}
      </ul>
      <h3 class="tt__gh">Declared not implemented
        <span class="fmark" title="Fictional world">FICTIONAL</span></h3>
      <ul class="tt__lim" data-not-implemented>
        ${(run.projection.not_implemented ?? []).map((n) => `<li>${escapeHtml(String(n))}</li>`).join('')}
      </ul>
      <p class="tt__note">Population size affects the <strong>magnitude</strong> of a group's
        contribution and nothing else — it does not make a group more or less concerned. Where a
        value is not known it is marked UNKNOWN, UNAVAILABLE or NOT_MODELLED, and
        <strong>never rendered as zero</strong>.</p>
    </section>
  </div>`
}

/** Filter behaviour. Plain substring match over name, identifier and mechanism. */
export function wireTechnicalTable(root: HTMLElement, onAsk?: (question: string) => void): void {
  if (onAsk) {
    root.querySelectorAll<HTMLElement>('.tt__r--ask').forEach((tr) => {
      const q = tr.dataset.askQuestion
      if (!q) return
      tr.addEventListener('click', () => onAsk(q))
      tr.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          onAsk(q)
        }
      })
    })
  }
  const input = root.querySelector<HTMLInputElement>('[data-tt-filter]')
  const count = root.querySelector<HTMLElement>('[data-tt-count]')
  const empty = root.querySelector<HTMLElement>('[data-tt-empty]')
  if (!input) return

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase()
    let shown = 0
    root.querySelectorAll<HTMLElement>('.tt__r').forEach((tr) => {
      const hit = q === '' || (tr.dataset.search ?? '').includes(q)
      tr.hidden = !hit
      if (hit) shown += 1
    })
    // A group with nothing left in it is hidden too, so the reader is not left staring at headings.
    root.querySelectorAll<HTMLElement>('.tt__g').forEach((g) => {
      g.hidden = [...g.querySelectorAll<HTMLElement>('.tt__r')].every((r) => r.hidden)
    })
    if (count) count.textContent = q === '' ? `${shown} values` : `${shown} of ${root.querySelectorAll('.tt__r').length} values`
    if (empty) empty.hidden = shown > 0
  })
}
