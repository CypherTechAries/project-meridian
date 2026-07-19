/**
 * Epistemic status and confidence chips — founder decision D2.
 *
 * These are load-bearing correctness surfaces, not styling. The visual encoding IS the honesty
 * guarantee: get it wrong and the charter is breached, not merely the aesthetic.
 *
 * Every status carries THREE redundant signals — glyph, text token, colour — so the encoding
 * survives greyscale, forced-colors mode and colour-blind viewing. Colour is never alone.
 */

import type { Confidence, EpistemicStatus } from '../fixtures/types.ts'

interface StatusPresentation {
  glyph: string
  token: string
  meaning: string
}

/**
 * `AUTHORITATIVE` describes STATE QUALITY, not player access (founder D2). A role-filtered
 * projection may hide authoritative fields, and a clearance-gated projection must never be
 * described as a raw ground-truth read.
 */
const STATUS: Record<EpistemicStatus, StatusPresentation> = {
  AUTHORITATIVE: {
    glyph: '◆',
    token: 'AUTHORITATIVE',
    meaning: 'State quality: authoritative. This describes the quality of the state, not your access to it.',
  },
  ASSESSED: {
    glyph: '◈',
    token: 'ASSESSED',
    meaning: 'An assessment, not an observation. Derived by judgement from other information.',
  },
  DISPUTED: {
    glyph: '◇',
    token: 'DISPUTED',
    meaning: 'Competing assessments exist and are retained. No single reading is asserted.',
  },
  UNKNOWN: {
    glyph: '○',
    token: 'UNKNOWN',
    meaning: 'Not known. Distinct from unavailable, and distinct from zero.',
  },
  PRESENTATION_ONLY: {
    glyph: '▢',
    token: 'PRESENTATION-ONLY',
    meaning: 'Display element. Must never influence simulation outcomes and is not engine state.',
  },
}

/**
 * Ordinal words only. No numeric percentage is ever shown: founder D2 forbids displaying a number
 * unless a documented mechanism produced it, and no mechanism produces confidence today.
 */
const CONFIDENCE: Record<Confidence, { token: string; bars: string }> = {
  HIGH: { token: 'HIGH', bars: '▮▮▮' },
  MEDIUM: { token: 'MED', bars: '▮▮▯' },
  LOW: { token: 'LOW', bars: '▮▯▯' },
  NOT_APPLICABLE: { token: 'N/A', bars: '▯▯▯' },
}

export function statusMeaning(status: EpistemicStatus): string {
  return STATUS[status].meaning
}

export function epistemicChip(status: EpistemicStatus): string {
  const s = STATUS[status]
  const cls = status.toLowerCase().replace('_', '-')
  return `<span class="chip chip--${cls}" title="${escapeHtml(s.meaning)}">
    <span class="chip__glyph" aria-hidden="true">${s.glyph}</span><span class="chip__token">${s.token}</span>
  </span>`
}

/**
 * Confidence is omitted entirely when NOT_APPLICABLE rather than rendered as an empty meter —
 * an empty meter reads as "low", which would be a fabricated claim.
 */
export function confidenceChip(confidence: Confidence): string {
  if (confidence === 'NOT_APPLICABLE') return ''
  const c = CONFIDENCE[confidence]
  return `<span class="conf" title="Confidence: ${c.token}. Ordinal only — no numeric confidence is computed.">
    <span class="conf__bars" aria-hidden="true">${c.bars}</span><span class="conf__token">${c.token}</span>
  </span>`
}

/**
 * Absence rendering. Unknown, unavailable and zero are three different things and must look
 * different — a missing row silently reads as zero, which is the failure this guards against.
 */
export function absenceValue(absence: 'UNKNOWN' | 'UNAVAILABLE' | 'NOT_APPLICABLE'): string {
  const label =
    absence === 'UNKNOWN' ? 'Not known' : absence === 'UNAVAILABLE' ? 'Not available to this role' : 'Not applicable'
  return `<span class="absent" data-absence="${absence}">${label}</span>`
}

export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}
