/**
 * The Briefing must render the BACKEND's state, not its own reading of the numbers.
 *
 * The two surfaces contradicted each other in the real browser: Ask MERIDIAN said political
 * pressure was "still high" while the Briefing said "low" and "falling". Ask's claim was authored
 * prose; the Briefing's was derived. Neither knew about the other.
 *
 * The fix put one authoritative reading on the backend (`scenario_state.py`). These tests assert
 * the frontend consumes it — and, critically, that it stops describing the run when the shared
 * state is absent rather than falling back to a private derivation. A silent fallback would
 * recreate the second source of truth this work exists to delete.
 */

import { describe, expect, it } from 'vitest'
import { initialSnapshot } from '../src/engine/client.ts'
import type { FieldState, RunResult } from '../src/engine/client.ts'
import {
  crisisLede,
  deriveTrend,
  fieldState,
  mapCallouts,
  plainDirection,
  plainLevel,
  plainSections,
  situationSummary,
} from '../src/engine/presentation.ts'

const run = initialSnapshot()

/** Rebuild a run with one shared value replaced. Nothing else changes. */
function withField(base: RunResult, field: string, patch: Partial<FieldState>): RunResult {
  const existing = base.state?.fields?.[field]
  if (!existing) throw new Error(`fixture has no shared state for ${field}`)
  return {
    ...base,
    state: {
      ...base.state!,
      fields: { ...base.state!.fields, [field]: { ...existing, ...patch } },
    },
  }
}

function politics(r: RunResult): string {
  const section = plainSections(r).find((s) => s.id === 'politics')
  return [...section!.sentences, section!.direction ?? ''].join(' ')
}

describe('the shared state is present and is the source', () => {
  it('S1 · the bundled snapshot carries the backend state', () => {
    expect(run.state).toBeTruthy()
    expect(run.state?.fields?.political_pressure).toBeTruthy()
  })

  it('S2 · level and direction come from the backend, not from a local threshold', () => {
    const f = fieldState(run, 'political_pressure')!
    expect(plainLevel(f)).toBe('low')
    expect(plainDirection(f)).toBe('falling')

    // Change ONLY the backend's verdict; the value is untouched. If the frontend were still
    // classifying the number itself, these would not move.
    const asHigh = withField(run, 'political_pressure', { level: 'HIGH', direction: 'RISING' })
    const g = fieldState(asHigh, 'political_pressure')!
    expect(plainLevel(g)).toBe('high')
    expect(plainDirection(g)).toBe('rising')
  })

  it('S3 · changing the shared value changes the rendered Briefing sentence', () => {
    expect(politics(run)).toContain('low')
    const raised = withField(run, 'political_pressure', { level: 'HIGH', direction: 'RISING' })
    const text = politics(raised)
    expect(text).toContain('high')
    expect(text).not.toContain('is low')
    expect(text).toContain('rising')
  })

  it('S4 · the level and the near-peak fact are BOTH stated', () => {
    // Stating only one is what made the contradiction possible: "low" alone reads as calm,
    // "near its peak" alone reads as severe. The run supports both.
    const f = fieldState(run, 'political_pressure')!
    expect(f.near_peak).toBe(true)
    expect(politics(run)).toMatch(/low.*close to the highest/)
  })

  it('S5 · an unmeasured direction is not rendered as steady', () => {
    const port = fieldState(run, 'port_activity_deficit')!
    expect(port.direction).toBe('NOT_ESTABLISHED')
    expect(plainDirection(port)).toBeNull()
  })
})

describe('the frontend has no second opinion', () => {
  it('S6 · the local technical derivation agrees with the backend authority', () => {
    // `deriveTrend` still exists for the technical view, which needs peak ticks and the recent
    // series. It must never DISAGREE with the authority — if it does, the technical screen and the
    // Briefing would contradict each other exactly as Ask once did.
    for (const field of ['political_pressure', 'rerouting_level', 'employment_pressure']) {
      const shared = fieldState(run, field)!
      const local = deriveTrend(run.projection, run.trajectory, field)!
      expect(local.value, field).toBeCloseTo(shared.value, 6)
      expect(local.nearPeak, `${field} nearPeak`).toBe(shared.near_peak)
      expect(local.postPeak, `${field} postPeak`).toBe(shared.post_peak)
      if (shared.direction_measured) {
        const localPlain =
          local.direction === 'RISING' ? 'RISING'
            : local.direction === 'EASING' || local.postPeak ? 'FALLING'
              : 'STEADY'
        expect(localPlain, `${field} direction`).toBe(shared.direction)
      }
    }
  })

  it('S7 · with the shared state absent the Briefing withholds the claim', () => {
    // It must NOT quietly recompute from the raw numbers. An absent authority is an absent fact.
    const blind: RunResult = { ...run, state: undefined }
    const section = plainSections(blind).find((s) => s.id === 'politics')!
    expect(section.sentences.join(' ')).not.toContain('low')
    expect(section.direction).toBeNull()
    expect(crisisLede(blind).join(' ')).not.toContain('Pressure on the government')
    expect(mapCallouts(blind)).not.toContain('Political pressure persists')
  })

  it('S8 · the headline summary reads the shared state too', () => {
    expect(situationSummary(run).headline).toBeTruthy()
    const raised = withField(run, 'political_pressure', { near_peak: false, direction: 'FALLING' })
    // The "sustains political pressure" clause is gated on the shared near-peak fact.
    expect(situationSummary(run).text).toContain('sustain political pressure')
    expect(situationSummary(raised).text).not.toContain('sustain political pressure')
  })
})
