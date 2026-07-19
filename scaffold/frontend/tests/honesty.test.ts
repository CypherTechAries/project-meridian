/**
 * C0 honesty tests.
 *
 * These do not merely check that the screen renders. They assert the properties that make a
 * fixture-backed prototype honest, because a polished screenshot is documentation and this project
 * exists to correct documentation that claimed more than the code delivered.
 */

import { describe, expect, it, beforeEach } from 'vitest'
import { kestralStrait } from '../src/fixtures/kestral-strait.v1.ts'
import { assertEnvelope } from '../src/fixtures/types.ts'
import type { Envelope } from '../src/fixtures/types.ts'
import { FICTION_DISCLOSURE, FIXTURE_DISCLOSURE } from '../src/components/disclosure.ts'
import { mount } from '../src/main.ts'

const ALLOWED_STATUS = ['AUTHORITATIVE', 'ASSESSED', 'DISPUTED', 'UNKNOWN', 'PRESENTATION_ONLY']
const ALLOWED_CONF = ['HIGH', 'MEDIUM', 'LOW', 'NOT_APPLICABLE']

function allRecords(): { where: string; rec: Envelope }[] {
  const out: { where: string; rec: Envelope }[] = [{ where: 'crisis', rec: kestralStrait.crisis }]
  kestralStrait.chain.forEach((h, i) => out.push({ where: `chain[${i}]`, rec: h }))
  kestralStrait.panels.forEach((p, i) => {
    out.push({ where: `panels[${i}]`, rec: p })
    p.claims.forEach((c, j) => out.push({ where: `panels[${i}].claims[${j}]`, rec: c }))
  })
  kestralStrait.queue.forEach((q, i) => out.push({ where: `queue[${i}]`, rec: q }))
  kestralStrait.stream.forEach((s, i) => out.push({ where: `stream[${i}]`, rec: s }))
  return out
}

describe('fixture envelope', () => {
  it('every displayable record carries a complete envelope', () => {
    for (const { where, rec } of allRecords()) {
      expect(() => assertEnvelope(rec, where)).not.toThrow()
    }
  })

  it('every record declares fixture origin — no record claims to come from the engine', () => {
    for (const { where, rec } of allRecords()) {
      expect(rec.origin, where).toBe('fixture')
    }
  })

  it('every record sets prototype_data literally true', () => {
    for (const { where, rec } of allRecords()) {
      expect(rec.prototype_data, where).toBe(true)
    }
  })

  it('uses only the approved epistemic vocabulary (founder D2)', () => {
    for (const { where, rec } of allRecords()) {
      expect(ALLOWED_STATUS, where).toContain(rec.epistemic_status)
      expect(ALLOWED_CONF, where).toContain(rec.confidence)
    }
  })

  it('the world is declared fictional', () => {
    expect(kestralStrait.world.is_fictional).toBe(true)
  })
})

describe('no fabricated numbers', () => {
  it('displays no numeric confidence percentage anywhere', () => {
    const root = document.createElement('div')
    mount(root)
    // A percentage adjacent to confidence language would be a fabricated precision claim.
    const text = root.textContent ?? ''
    expect(text).not.toMatch(/\d+\s?%/)
  })
})

describe('decision queue integrity', () => {
  it('every queue item has at least one affordance', () => {
    // HSE's rule made machine-checkable: a status indicator must not be designated a decision.
    for (const q of kestralStrait.queue) {
      expect(q.affordances.length, q.id).toBeGreaterThan(0)
    }
  })
})

describe('absence handling', () => {
  it('unknown and unavailable render distinctly and are never dropped', () => {
    const root = document.createElement('div')
    mount(root)
    const absent = root.querySelectorAll('.absent')
    expect(absent.length).toBeGreaterThan(0)
    const kinds = new Set(Array.from(absent).map((n) => n.getAttribute('data-absence')))
    // Both classes are present in the fixture, and both must survive to the DOM.
    expect(kinds.has('UNKNOWN')).toBe(true)
    expect(kinds.has('UNAVAILABLE')).toBe(true)
  })

  it('a null value never renders as zero', () => {
    const root = document.createElement('div')
    mount(root)
    const absent = Array.from(root.querySelectorAll('.absent')).map((n) => n.textContent?.trim())
    for (const t of absent) {
      expect(t).not.toBe('0')
      expect(t).toBeTruthy()
    }
  })
})

describe('disclosures', () => {
  let root: HTMLElement

  beforeEach(() => {
    root = document.createElement('div')
    mount(root)
  })

  it('renders both disclosures verbatim', () => {
    const text = root.textContent ?? ''
    expect(text).toContain(FICTION_DISCLOSURE)
    expect(text).toContain(FIXTURE_DISCLOSURE)
  })

  it('repeats both disclosures top and bottom so a crop cannot remove them', () => {
    const fiction = Array.from(root.querySelectorAll('.disclose--fiction'))
    const fixture = Array.from(root.querySelectorAll('.disclose--fixture'))
    expect(fiction.length).toBeGreaterThanOrEqual(2)
    expect(fixture.length).toBeGreaterThanOrEqual(2)
  })

  it('provides no control that could dismiss a disclosure', () => {
    const bands = root.querySelectorAll('.disclosures')
    for (const b of Array.from(bands)) {
      expect(b.querySelector('button')).toBeNull()
      expect(b.querySelector('[aria-label*="close" i]')).toBeNull()
    }
  })
})

describe('per-card fixture marking (crop invariance)', () => {
  it('every card carries its own FIXTURE marker, not only the page banner', () => {
    const root = document.createElement('div')
    mount(root)
    const provs = Array.from(root.querySelectorAll('.prov'))
    expect(provs.length).toBeGreaterThan(0)
    for (const p of provs) {
      const origin = p.querySelector('.prov__origin')
      expect(origin?.textContent?.trim()).toBe('FIXTURE')
    }
  })

  it('every card also carries a FICTIONAL marker — the B5 disclosure must survive a crop', () => {
    // A crop that excludes both page banners must still declare that the world is fictional.
    // Verified against a real cropped capture in scripts/screenshot.mjs.
    const root = document.createElement('div')
    mount(root)
    const provs = Array.from(root.querySelectorAll('.prov'))
    for (const p of provs) {
      expect(p.querySelector('.prov__fiction')?.textContent?.trim()).toBe('FICTIONAL')
    }
  })

  it('every epistemic chip carries a glyph and a text token, never colour alone', () => {
    const root = document.createElement('div')
    mount(root)
    const chips = Array.from(root.querySelectorAll('.chip'))
    expect(chips.length).toBeGreaterThan(0)
    for (const c of chips) {
      expect(c.querySelector('.chip__glyph')).not.toBeNull()
      expect(c.querySelector('.chip__token')?.textContent?.trim()).toBeTruthy()
    }
  })
})

describe('non-materialised entities', () => {
  it('aggregate entities are marked and never given individual detail', () => {
    const root = document.createElement('div')
    mount(root)
    const aggregates = Array.from(root.querySelectorAll('.ent--aggregate'))
    expect(aggregates.length).toBeGreaterThan(0)
    for (const a of aggregates) {
      expect(a.textContent).toContain('aggregate')
    }
  })

  it('no fixture entity is materialised implicitly — the flag is explicit on every reference', () => {
    for (const hop of kestralStrait.chain) {
      for (const e of hop.entities) {
        expect(typeof e.materialised, `${hop.id}/${e.id}`).toBe('boolean')
      }
    }
  })
})

describe('aggregate contributors', () => {
  it('every chain hop with a summary names its mechanisms', () => {
    // Research T18 (fact-checked): an aggregate without a ranked contributor list does not ship.
    for (const hop of kestralStrait.chain) {
      if (hop.epistemic_status === 'UNKNOWN') continue
      expect(hop.contributors.length, hop.id).toBeGreaterThan(0)
      for (const c of hop.contributors) {
        expect(c.mechanism, `${hop.id}/${c.label}`).toBeTruthy()
      }
    }
  })
})

describe('shell', () => {
  it('renders the five landmark regions and marks unbuilt screens as unbuilt', () => {
    const root = document.createElement('div')
    mount(root)
    expect(root.querySelector('nav[aria-label="Primary"]')).not.toBeNull()
    expect(root.querySelector('main#main')).not.toBeNull()
    expect(root.querySelector('aside[aria-label="Context and inspection"]')).not.toBeNull()
    expect(root.querySelector('[role="log"]')).not.toBeNull()
    expect(root.querySelector('[aria-label="Scenario and role status"]')).not.toBeNull()

    const disabled = Array.from(root.querySelectorAll('.nav__item.is-disabled'))
    expect(disabled.length).toBe(4)
    for (const d of disabled) expect(d.textContent).toContain('not built')
  })

  it('renders the full propagation chain including the unresolved final hop', () => {
    const root = document.createElement('div')
    mount(root)
    const hops = root.querySelectorAll('.hop')
    expect(hops.length).toBe(kestralStrait.chain.length)
    expect(root.querySelector('.hop--unresolved')).not.toBeNull()
  })

  it('labels the chain as a hand-authored fixture trace', () => {
    const root = document.createElement('div')
    mount(root)
    const text = root.textContent ?? ''
    expect(text).toMatch(/not computed/i)
  })
})
