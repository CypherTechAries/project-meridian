/**
 * Where the reader is in the scenario.
 *
 * THE FAILURE THIS FIXES. Testing the briefing as head of state, the founder read the situation as
 * *"halfway into the simulation and things have slowed down"*. It is the LAST recorded point — day
 * five of five, three ticks past the peak. The card said "Day 5" and never said day five **of
 * what**, so there was no way to know.
 *
 * That was not cosmetic. It produced the wrong explanation for why the options felt weak, and it
 * would have contaminated a cold test in exactly the same way.
 *
 * These tests hold two properties:
 *
 *   1. Every clause is DERIVED from the shared packaged state — no second factual account. Change
 *      the run and the sentence changes with it; shorten the run and it stops claiming to be the end.
 *   2. The position never contradicts the direction the rest of the interface reports, because both
 *      read the same field.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'
import {
  POSITION_CAVEAT,
  fieldState,
  plainDirection,
  scenarioPosition,
} from '../src/engine/presentation.ts'

const run = initialSnapshot()
let root: HTMLElement

beforeEach(() => {
  root = document.createElement('div')
  root.id = 'app'
  document.body.innerHTML = ''
  document.body.appendChild(root)
  mount(root, run)
})

const positionEl = (): HTMLElement => root.querySelector('[data-scenario-position]')!

describe('P1-P4 · the position agrees with the packaged run', () => {
  it('P1 · the packaged run really is at its declared horizon', () => {
    // The claim the sentence makes, checked against the state rather than assumed.
    expect(run.state!.ticks).toBe(run.state!.horizon_ticks)
    expect(run.state!.is_final_recorded_tick).toBe(true)
  })

  it('P2 · the line states it is the final recorded day', () => {
    expect(positionEl()).not.toBeNull()
    expect(positionEl().textContent).toMatch(/final recorded day of this scenario/i)
  })

  it('P3 · the peak claim matches the shared field, and is not asserted blind', () => {
    const political = fieldState(run, 'political_pressure')!
    expect(political.post_peak).toBe(true)
    expect(political.direction).toBe('FALLING')
    // Only then may the sentence say so.
    expect(positionEl().textContent).toMatch(/peaked earlier and is now falling/i)
  })

  it('P4 · the caveat is present and refuses to predict', () => {
    const text = root.textContent ?? ''
    expect(text).toContain(POSITION_CAVEAT)
    expect(text).toMatch(/does not predict what happens next/i)
  })
})

describe('P5-P7 · it is derived, not authored', () => {
  it('P5 · a shorter run does NOT claim to be the end of the scenario', () => {
    const partial: RunResult = {
      ...run,
      state: { ...run.state!, ticks: 12, is_final_recorded_tick: false },
    }
    const pos = scenarioPosition(partial)!
    expect(pos.line).not.toMatch(/final recorded day/i)
    expect(pos.line).toMatch(/unfinished scenario/i)
  })

  it('P6 · a rising run does not claim the peak has passed', () => {
    const rising: RunResult = {
      ...run,
      state: {
        ...run.state!,
        fields: {
          ...run.state!.fields,
          political_pressure: {
            ...run.state!.fields.political_pressure!,
            direction: 'RISING',
            post_peak: false,
          },
        },
      },
    }
    const pos = scenarioPosition(rising)!
    expect(pos.line).toMatch(/still rising/i)
    expect(pos.line).not.toMatch(/peaked earlier/i)
  })

  it('P7 · with no shared state there is no position claim at all', () => {
    const blind: RunResult = { ...run, state: undefined }
    expect(scenarioPosition(blind)).toBeNull()
    const r = document.createElement('div')
    mount(r, blind, 'ask')
    expect(r.querySelector('[data-scenario-position]')).toBeNull()
  })
})

describe('P8-P10 · no contradiction, and no hidden claim', () => {
  it('P8 · the position agrees with the direction the impact rows report', () => {
    const political = fieldState(run, 'political_pressure')!
    const rowDirection = plainDirection(political)
    expect(rowDirection).toBe('falling')
    // Both read the same field, so the card cannot say "falling" in one place and "rising" in
    // another — the defect that made the Briefing and Ask contradict each other before.
    expect(positionEl().textContent).toMatch(new RegExp(rowDirection!, 'i'))
    expect(root.querySelector('[data-row="politics"]')?.textContent).toMatch(/falling/i)
  })

  it('P9 · the position is visible without expanding anything', () => {
    // It must not be inside a <details>, and must not be a screen-reader-only note.
    const el = positionEl()
    expect(el.closest('details')).toBeNull()
    expect(el.className).not.toMatch(/visually-hidden|u-sr/)
  })

  it('P10 · it introduces no tick, seed, horizon number or probability', () => {
    const t = positionEl().textContent ?? ''
    expect(t).not.toMatch(/\btick\b/i)
    expect(t).not.toMatch(/\bseed\b/i)
    expect(t).not.toMatch(/\d+\s?%/)
    expect(t).not.toMatch(/likely|probably|expect|forecast|will\b/i)
  })
})
