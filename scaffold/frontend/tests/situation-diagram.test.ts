/**
 * The situation diagram makes no spatial claim (issue #33).
 *
 * MERIDIAN's engine has no spatial model — no coordinates, no geometry, no port entities, and
 * political pressure is a single scalar with no location. The previous component was a map, and it
 * invented coastlines, decorative settlement lights and two place names that were hard-coded in the
 * renderer rather than declared by the scenario.
 *
 * These tests hold the replacement to the rule that made it necessary: **it may show structure, and
 * it may not show place.** Every fact on it comes from the model; anything absent from the model
 * must be absent from the screen.
 */

import { describe, expect, it } from 'vitest'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'
import { situationModel } from '../src/engine/presentation.ts'
import { situationDiagram } from '../src/components/briefing-viz.ts'

const run = initialSnapshot()
const model = situationModel(run)

function el(html: string): HTMLElement {
  const d = document.createElement('div')
  d.innerHTML = html
  return d
}

const svg = el(situationDiagram(model))
const text = (svg.textContent ?? '').toLowerCase()

describe('D1-D4 · no spatial claim', () => {
  it('D1 · the mock place names are gone', () => {
    // "Northshore" and "Southport" were hard-coded in briefing-viz.ts and are not scenario
    // entities. They were part of the old mock, not engine truth.
    expect(text).not.toContain('northshore')
    expect(text).not.toContain('southport')
  })

  it('D2 · it does not call itself a map, and says what it is instead', () => {
    expect(model.kindNote).toContain('not where anything is')
    expect(text).toContain('not where anything is')
    // The aria-label must not describe a map either — a screen-reader user gets the same honesty.
    const label = (svg.querySelector('svg')?.getAttribute('aria-label') ?? '').toLowerCase()
    expect(label).toContain('situation diagram')
    expect(label).not.toMatch(/\bmap of\b/)
  })

  it('D3 · it names no location, distance or route', () => {
    for (const word of ['coastline', 'kilometre', 'nautical', 'latitude', 'longitude', 'north of', 'south of']) {
      expect(text).not.toContain(word)
    }
  })

  it('D4 · it invents no ports — the engine has no port entities', () => {
    // port_activity_deficit is a single scalar. Any *named* port would be invented.
    expect(text).toContain('ports')
    expect(text).not.toMatch(/port of |harbour of |\bberth\b/)
  })
})

describe('D5-D9 · the five cold-test questions', () => {
  it('D5 · Q1 what is blocked — the origin band states it first', () => {
    expect(model.blockadeActive).toBe(true)
    expect(text).toContain('the strait is closed')
    expect(svg.querySelector('[data-stage="origin"]')).not.toBeNull()
  })

  it('D6 · Q2 who is affected — named groups with their share of the population', () => {
    expect(model.groups.length).toBeGreaterThan(0)
    expect(svg.querySelector('[data-stage="groups"]')).not.toBeNull()
    for (const g of model.groups) {
      expect(text).toContain(g.name.toLowerCase())
      expect(Number.isInteger(g.sharePercent)).toBe(true)
    }
    // Groups are averages, and the diagram must say so.
    expect(text).toContain('does not model the individuals')
  })

  it('D7 · Q3 pressure is shown as a level, never as a place', () => {
    const pressure = model.stages.find((s) => s.id === 'pressure')
    expect(pressure).toBeTruthy()
    expect(pressure!.level).toBe('low')
    expect(pressure!.direction).toBe('falling')
    expect(svg.querySelector('[data-stage="pressure"]')).not.toBeNull()
    // A magnitude bar and a level word — not a marker, a zone or a coordinate.
    expect(svg.querySelector('[data-stage="pressure"] .sd__bar')).not.toBeNull()
  })

  it('D8 · Q4 trade-offs — the choices are visible and stated as not executed', () => {
    expect(model.decision).toBeTruthy()
    expect(text).toContain(model.decision!.question.toLowerCase())
    for (const c of model.decision!.choices) expect(text).toContain(c.toLowerCase())
    expect(text).toContain('nothing will be executed')
  })

  it('D9 · Q5 change over time — drawn where recorded, absent where not', () => {
    const shipping = model.stages.find((s) => s.id === 'shipping')!
    expect(shipping.series.length).toBeGreaterThan(5)
    expect(svg.querySelector('[data-stage="shipping"] .sd__spark')).not.toBeNull()

    // port_activity_deficit is NOT recorded per tick. A flat line would be a claim, so there must
    // be no line at all — and the diagram must say why.
    const ports = model.stages.find((s) => s.id === 'ports')!
    expect(ports.series.length).toBe(0)
    expect(ports.seriesNote).toBeTruthy()
    expect(svg.querySelector('[data-stage="ports"] .sd__spark')).toBeNull()
    expect(text).toContain('not recorded each step')
  })
})

describe('D10-D12 · it invents nothing', () => {
  it('D10 · every stage magnitude comes from the model', () => {
    for (const s of model.stages) {
      if (s.magnitude === null) continue
      expect(s.magnitude).toBeGreaterThanOrEqual(0)
      expect(s.magnitude).toBeLessThanOrEqual(1)
    }
  })

  it('D11 · with no shared state it withholds levels rather than deriving them', () => {
    const blind: RunResult = { ...run, state: undefined }
    const m = situationModel(blind)
    for (const s of m.stages) {
      expect(s.level, `${s.id} level`).toBeNull()
      expect(s.magnitude, `${s.id} magnitude`).toBeNull()
      expect(s.direction, `${s.id} direction`).toBeNull()
    }
    // It still renders, and says the level is not established rather than showing an empty bar.
    expect(el(situationDiagram(m)).textContent).toContain('not established')
  })

  it('D12 · no decimals are drawn', () => {
    // The Briefing's standing rule: no decimals in the default view. The diagram is inside it.
    expect(svg.textContent ?? '').not.toMatch(/\b\d+\.\d+\b/)
  })

  it('D12a · the peak is marked, so a rising line beside the word "falling" is legible', () => {
    // The line covers the whole scenario; the direction word covers the recent window. Political
    // pressure rose for seventeen steps and has edged down since, so the line climbs while the
    // label reads "falling". Without the turn marked, that reads as a contradiction on sight.
    const pressure = model.stages.find((s) => s.id === 'pressure')!
    expect(pressure.direction).toBe('falling')
    const band = svg.querySelector('[data-stage="pressure"]')!
    expect(band.querySelector('.sd__spark-peak')).not.toBeNull()
    expect(band.textContent).toContain('highest')
    // And the line's window is named, rather than left for the reader to assume.
    expect(band.textContent).toContain('start of the scenario to now')
  })

  it('D13 · the diagram grows with its content instead of being cropped', () => {
    const box = svg.querySelector('svg')?.getAttribute('viewBox') ?? ''
    const height = Number(box.split(/\s+/)[3])
    // Six bands cannot fit the old 430px map frame; a fixed frame would clip them.
    expect(height).toBeGreaterThan(600)
    expect(svg.querySelector('svg')?.getAttribute('preserveAspectRatio')).toContain('meet')
  })
})
