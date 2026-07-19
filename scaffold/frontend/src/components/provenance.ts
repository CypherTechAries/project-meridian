/**
 * Provenance rendering — the crop-invariant carrier.
 *
 * Research finding R6: a boxed tinted rectangle is read as advertising and skipped. A government
 * design system reports its own container-based differentiation is frequently not noticed. So the
 * carrier here is STRUCTURAL — a full-height gutter rule on the left edge of every card, coloured
 * by epistemic status and always accompanied by a text token.
 *
 * The founder additionally requires the fictional-world disclosure to survive CROPPING. A single
 * page-level banner does not. Every card therefore carries its own fixture marker, so a cropped
 * screenshot of one card still declares what it is.
 *
 * Research finding F9 (implied truth effect): labelling only AI-generated text raises the
 * perceived accuracy of everything unlabelled. BOTH classes must be marked positively, and
 * unmarked content is a build failure — enforced by `assertEnvelope` and by the marker test.
 */

import type { Envelope } from '../fixtures/types.ts'
import { confidenceChip, epistemicChip, escapeHtml } from './epistemic.ts'

/** The compact visible treatment. Detail goes behind expansion, per founder D2. */
export function provenanceLine(e: Envelope): string {
  return `<div class="prov">
    <span class="prov__fiction" title="This world is fictional. Not real-world intelligence or prediction.">FICTIONAL</span>
    <span class="prov__origin" data-origin="${e.origin}">${e.origin === 'fixture' ? 'FIXTURE' : 'ENGINE'}</span>
    <span class="prov__sep" aria-hidden="true">·</span>
    <span class="prov__src">${escapeHtml(e.provenance)}</span>
    <span class="prov__sep" aria-hidden="true">·</span>
    <span class="prov__tick">updated ${escapeHtml(e.last_updated)}</span>
  </div>`
}

/** Full detail, shown in the inspector panel rather than on every card. */
export function provenanceDetail(e: Envelope): string {
  const rows: [string, string][] = [
    ['Epistemic status', e.epistemic_status],
    ['Confidence', e.confidence],
    ['Origin', e.origin === 'fixture' ? 'Fixture — hand-authored, not from the engine' : 'Engine'],
    ['Provenance', e.provenance],
    ['Visibility basis', e.visibility_basis],
    ['Player role', e.player_role],
    ['Last updated', e.last_updated],
    ['Scenario', `${e.scenario_id} v${e.scenario_version}`],
    ['Simulation tick', String(e.simulation_tick)],
  ]
  return `<dl class="provdetail">${rows
    .map(
      ([k, v]) =>
        `<dt>${escapeHtml(k)}</dt><dd>${escapeHtml(v)}</dd>`,
    )
    .join('')}</dl>`
}

/**
 * Card wrapper. The `data-epistemic` attribute drives the gutter rule; the fixture marker is
 * rendered inside the card so it survives a crop.
 */
export function card(
  e: Envelope,
  opts: { id: string; title: string; standfirst?: string; body: string; selectable?: boolean },
): string {
  const selectable = opts.selectable !== false
  return `<article class="card" data-epistemic="${e.epistemic_status}" data-card-id="${escapeHtml(opts.id)}"
    ${selectable ? `tabindex="0" role="button" aria-label="${escapeHtml(opts.title)} — select to inspect provenance"` : ''}>
    <div class="card__gutter" aria-hidden="true"></div>
    <div class="card__inner">
      <header class="card__head">
        <h3 class="card__title">${escapeHtml(opts.title)}</h3>
        <div class="card__chips">${epistemicChip(e.epistemic_status)}${confidenceChip(e.confidence)}</div>
      </header>
      ${opts.standfirst ? `<p class="card__standfirst">${escapeHtml(opts.standfirst)}</p>` : ''}
      <div class="card__body">${opts.body}</div>
      ${provenanceLine(e)}
    </div>
  </article>`
}
