/**
 * Compact origin and epistemic markers.
 *
 * WHY THIS REPLACED THE PREVIOUS TREATMENT. The first build printed full-width `FICTIONAL` and
 * `FIXTURE` words inside every card. That was honest but overpowering: the provenance system read
 * louder than the crisis, which inverts what the screen is for. The safety requirement is that a
 * cropped screenshot still declares what it shows — not that the declaration dominates.
 *
 * So each card now carries a single compact badge (E / F / U / N/A) plus a small fictional-world
 * datum mark. Both survive a crop. Full provenance opens in the inspector.
 *
 * Never colour alone: every badge carries a letter, a title and an accessible label.
 */

import { escapeHtml } from './epistemic.ts'

export type Origin = 'engine' | 'fixture' | 'unknown' | 'unavailable'

const ORIGIN_META: Record<Origin, { code: string; name: string; meaning: string }> = {
  engine: {
    code: 'E',
    name: 'ENGINE-DERIVED',
    meaning: 'Computed by the simulation engine during this run.',
  },
  fixture: {
    code: 'F',
    name: 'FIXTURE',
    meaning: 'Hand-authored illustrative content. Not computed by the engine.',
  },
  unknown: {
    code: 'U',
    name: 'UNKNOWN',
    meaning: 'Not known. Distinct from unavailable, and distinct from zero.',
  },
  unavailable: {
    code: 'N/A',
    name: 'UNAVAILABLE',
    meaning: 'Not computed by any implemented mechanism.',
  },
}

export function originBadge(origin: Origin): string {
  const m = ORIGIN_META[origin]
  return `<span class="ob ob--${origin}" title="${escapeHtml(m.name)} — ${escapeHtml(m.meaning)}">
    <span class="ob__code" aria-hidden="true">${m.code}</span>
    <span class="u-sr">${escapeHtml(m.name)}</span>
  </span>`
}

/**
 * Crop-safe fictional-world mark. Small enough to live on every panel, explicit enough that a
 * cropped screenshot of one panel still says the world is fictional.
 */
export function fictionMark(): string {
  return `<span class="fmark" title="Fictional simulation — not real-world intelligence or prediction.">
    <svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="6" r="5"/><line x1="6" y1="1" x2="6" y2="11"/></svg>
    <span class="fmark__txt">FICTIONAL</span>
  </span>`
}

/** Panel header: title, optional subtitle, fiction mark and origin badge. */
export function panelHead(
  title: string,
  subtitle: string,
  origin: Origin,
  opts: { id?: string } = {},
): string {
  // Row 1 carries the title and the compact markers; row 2 is a single-line subtitle. The markers
  // never compete with the subtitle for width, so neither can force the other to wrap.
  return `<header class="panel__head">
    <div class="panel__headrow">
      <h2 class="panel__title"${opts.id ? ` id="${escapeHtml(opts.id)}"` : ''}>${escapeHtml(title)}</h2>
      <span class="panel__marks">${fictionMark()}${originBadge(origin)}</span>
    </div>
    ${subtitle ? `<p class="panel__sub">${escapeHtml(subtitle)}</p>` : ''}
  </header>`
}

export function originLegend(): string {
  return `<ul class="olegend">${(Object.keys(ORIGIN_META) as Origin[])
    .map((o) => {
      const m = ORIGIN_META[o]
      return `<li><span class="ob ob--${o}"><span class="ob__code" aria-hidden="true">${m.code}</span></span>
        <span class="olegend__name">${escapeHtml(m.name)}</span></li>`
    })
    .join('')}<li class="olegend__fiction">${fictionMark()}
      <span class="olegend__name">Fictional world</span></li></ul>`
}

/**
 * Value renderer that keeps unknown, unavailable and zero visually distinct.
 * Zero is a number; the other two are not, and must never be shown as one.
 */
export function metricValue(value: number | null, absence?: 'unknown' | 'unavailable'): string {
  if (value === null || value === undefined) {
    const label = absence === 'unavailable' ? 'Not computed' : 'Not known'
    return `<span class="metric__absent" data-absence="${absence ?? 'unknown'}">${label}</span>`
  }
  return `<span class="metric__num">${value.toFixed(4)}</span>`
}
