/**
 * C0 honesty tests — carried forward through the Ask-first rebuild.
 *
 * The interface changed shape twice now. The Briefing screen became a card in the conversation, and
 * the eight-panel command centre became a searchable table. **No honesty property was allowed to be
 * deleted along with the screen that used to carry it.** Each suite below names where the property
 * now lives.
 *
 * Two properties changed form rather than moving:
 *
 *  - **Crop safety.** A cropped screenshot of one panel had to declare the world fictional. Panels
 *    are gone; the fiction mark now rides every table section heading and the briefing card header.
 *  - **Unbuilt screens.** The side navigation used to advertise four screens marked "not built".
 *    They are no longer advertised at all, which is a stronger position than labelling them. That
 *    property is preserved BY REMOVAL and is tested as such.
 *
 * Nothing here was relaxed to accommodate the new layout.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { FICTION_DISCLOSURE, MIXED_DISCLOSURE, mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'
import { technicalRows } from '../src/screens/technical-table.ts'

const ALLOWED_CONF = ['HIGH', 'MEDIUM', 'LOW', 'NOT_APPLICABLE']
const run = initialSnapshot()
let root: HTMLElement

function mountAt(mode: 'ask' | 'analysis' = 'ask', r: RunResult = run): HTMLElement {
  const el = document.createElement('div')
  el.id = 'app'
  document.body.innerHTML = ''
  document.body.appendChild(el)
  mount(el, r, mode)
  return el
}


/**
 * Text a reader can actually SEE.
 *
 * Content inside a closed `<details>` is not on the default view — that is the whole mechanism of
 * progressive disclosure. `textContent` cannot tell the difference, so these rules would otherwise
 * forbid ever attaching evidence to a claim, which is precisely what the interface now does.
 *
 * The companion assertion is that the detail really is CLOSED. Both halves are needed: this helper
 * alone would let anything hide in an open disclosure.
 */
function visibleText(node: Element | null): string {
  if (!node) return ''
  let out = ''
  const walk = (n: Node): void => {
    if (n.nodeType === 3) { out += n.nodeValue ?? ''; return }
    if (n.nodeType !== 1) return
    const el = n as Element
    if (el.tagName === 'DETAILS' && !(el as HTMLDetailsElement).open) {
      const s = el.querySelector('summary')
      if (s) walk(s)
      return
    }
    if (el.classList.contains('visually-hidden') || el.classList.contains('u-sr')) return
    for (const c of Array.from(el.childNodes)) walk(c)
  }
  walk(node)
  return out
}

beforeEach(() => {
  root = mountAt()
})

describe('disclosures', () => {
  it('renders the fictional-simulation disclosure verbatim', () => {
    expect(root.textContent).toContain(FICTION_DISCLOSURE)
  })

  it('renders the MIXED-origin disclosure, because the screen is not fixture-only', () => {
    expect(root.textContent).toContain(MIXED_DISCLOSURE)
    expect(root.textContent).not.toContain('NOT CONNECTED TO THE SIMULATION ENGINE')
  })

  it('provides no control that could dismiss a disclosure', () => {
    const band = root.querySelector('.disclosures')!
    expect(band.querySelector('button')).toBeNull()
    expect(band.querySelector('[aria-label*="close" i]')).toBeNull()
    expect(band.querySelector('[aria-label*="dismiss" i]')).toBeNull()
  })

  it('carries the disclosures on BOTH destinations, not only the landing one', () => {
    for (const mode of ['ask', 'analysis'] as const) {
      expect(mountAt(mode).textContent, mode).toContain(FICTION_DISCLOSURE)
    }
  })
})

describe('crop safety', () => {
  it('the briefing card carries a fictional-world marker in its own header', () => {
    // A screenshot of just the card must not read as a real-world briefing.
    expect(root.querySelector('.bcard__meta')?.textContent).toMatch(/fictional/i)
  })

  it('every technical section carries its own fictional-world marker', () => {
    // The phrase "fictional-world marker" is load-bearing: the backend suite
    // (test_b5_controls.py::test_17) asserts this file still enforces crop safety by name, so the
    // property cannot be quietly dropped in a redesign. It has already survived two.
    const r = mountAt('analysis')
    const sections = [...r.querySelectorAll('.tt__gh')]
    expect(sections.length).toBeGreaterThan(2)
    for (const h of sections) {
      expect(h.querySelector('.fmark'), `section missing fiction mark: ${h.textContent}`).not.toBeNull()
    }
  })

  it('the fictional-world marker carries text, not only an icon or a colour', () => {
    const mark = mountAt('analysis').querySelector('.fmark')!
    expect((mark.textContent ?? '').trim().length).toBeGreaterThan(3)
  })

  it('the situation diagram states it is fictional inside the drawing', () => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    expect(root.querySelector('[data-diagram-answer]')?.textContent).toMatch(/fictional/i)
  })
})

describe('engine versus fixture', () => {
  it('marks the connection state, so a recorded snapshot is never shown as live', () => {
    expect(mountAt('analysis').textContent).toMatch(/SNAPSHOT|LIVE|UNAVAILABLE/)
  })

  it('states the origin of every value it shows', () => {
    const rows = technicalRows(run)
    expect(rows.length).toBeGreaterThan(10)
    for (const r of rows) expect(r.origin, r.id).toBeTruthy()
  })

  it('renders an honest unavailable state when the backend cannot be reached', () => {
    const offline: RunResult = { ...run, connection: 'unavailable' }
    expect(mountAt('analysis', offline).textContent).toContain('UNAVAILABLE')
  })
})

describe('no fabricated precision', () => {
  it('displays no numeric confidence percentage anywhere', () => {
    for (const mode of ['ask', 'analysis'] as const) {
      expect(mountAt(mode).textContent, mode).not.toMatch(/\d+\s?%\s?confiden/i)
    }
  })

  it('reports confidence as NOT_APPLICABLE rather than inventing one', () => {
    // The engine COMPUTES a value; it does not estimate one, and no mechanism produces a
    // confidence. A number here would be fabricated precision.
    for (const r of technicalRows(run)) expect(r.confidence, r.id).toBe('NOT_APPLICABLE')
    expect(mountAt('analysis').textContent).toContain('NOT_APPLICABLE')
  })

  it('only uses the approved confidence vocabulary', () => {
    for (const r of technicalRows(run)) expect(ALLOWED_CONF).toContain(r.confidence)
  })
})

describe('absence handling', () => {
  it('never renders an unmeasured direction as steady', () => {
    // port_activity_deficit is not recorded per tick. STEADY would claim we looked and found no
    // movement; NOT MEASURED says we did not look.
    const port = technicalRows(run).find((r) => r.id === 'port_activity_deficit')!
    expect(port.direction).toBe('NOT MEASURED')
  })

  it('states that absence is never rendered as zero', () => {
    expect(mountAt('analysis').textContent).toMatch(/never rendered as zero/i)
  })

  it('does not render an unavailable capability as a zero', () => {
    const list = mountAt('analysis').querySelector('[data-not-implemented]')!
    expect(list.querySelectorAll('li').length).toBeGreaterThan(0)
    expect(list.textContent).not.toMatch(/\b0\b/)
  })
})

describe('honest scope', () => {
  it('states that the run is ephemeral and not a replay', () => {
    const t = mountAt('analysis').textContent ?? ''
    expect(t).toMatch(/ephemeral/i)
    expect(t).toMatch(/no replay/i)
  })

  it('lists every capability the engine declares it does not have', () => {
    const list = mountAt('analysis').querySelector('[data-not-implemented]')!
    for (const cap of run.projection.not_implemented ?? []) {
      expect(list.textContent, cap).toContain(cap)
    }
  })

  it('does not claim replay, event sourcing or persistence as capabilities', () => {
    const list = mountAt('analysis').querySelector('[data-not-implemented]')!
    expect(list.textContent).toContain('replay')
    expect(list.textContent).toContain('persistence')
  })

  it('states that population affects magnitude only', () => {
    expect(mountAt('analysis').textContent).toMatch(/magnitude/i)
  })

  it('advertises no screen it has not built', () => {
    // PRESERVED BY REMOVAL — see the note at the top of this file.
    for (const mode of ['ask', 'analysis'] as const) {
      const t = mountAt(mode).textContent ?? ''
      for (const gone of ['Society Pulse', 'Causal Timeline', 'Entity Dossiers']) {
        expect(t, `${gone} still advertised in ${mode}`).not.toContain(gone)
      }
    }
  })

  it('offers no destination that is not worth being one', () => {
    // "Exact numbers" was half the primary navigation. A first-time reader cannot say why those
    // values matter or what decision they help with, so it is no longer a destination at all.
    expect(root.querySelectorAll('.navbar .navbtn')).toHaveLength(0)
    expect(root.textContent).not.toMatch(/Exact numbers/)
  })
})

describe('engine values reach the screen', () => {
  it('renders the political pressure the run actually produced', () => {
    const actual = run.projection.stages.find((s) => s.field === 'political_pressure')!.value
    expect(technicalRows(run).find((r) => r.id === 'political_pressure')!.value)
      .toBe(actual.toFixed(4))
    expect(mountAt('analysis').textContent).toContain(actual.toFixed(4))
  })

  it('renders every cohort from the projection, not a selection', () => {
    expect(technicalRows(run).filter((r) => r.group === 'Population groups'))
      .toHaveLength(run.projection.cohorts.length)
  })

  it('renders every government option, including the ones not open', () => {
    const rows = technicalRows(run).filter((r) => r.group === 'Government options')
    expect(rows).toHaveLength(run.projection.government_options.length)
    expect(rows.map((r) => r.value)).toContain('CONSTRAINED')
  })

  it('shows the real rule-pack version', () => {
    expect(mountAt('analysis').textContent).toContain(run.projection.rule_pack_version)
  })

  it('names the mechanism behind each chain value', () => {
    for (const r of technicalRows(run).filter((x) => x.group === 'Causal chain')) {
      expect(r.mechanism, r.id).toBeTruthy()
    }
  })
})

describe('detail never leaks upward', () => {
  it('the conversation shows no engine identifier, mechanism id or exact decimal', () => {
    // VISIBLE text: evidence attached to a claim sits behind a closed control, and a closed
    // control is not the default view. The companion assertion below proves it is really closed.
    const t = visibleText(root)
    expect(t).not.toMatch(/chain\.[a-z_]+/)
    expect(t).not.toMatch(/M-[A-Z]+-[A-Z]+/)
    expect(t).not.toMatch(/@\d+\.\d+\.\d+/)
    expect(t).not.toMatch(/\b\d+\.\d{3,}\b/)
  })

  it('claim evidence is attached but closed, so detail is opt-in rather than absent', () => {
    for (const d of root.querySelectorAll<HTMLDetailsElement>('details')) expect(d.open).toBe(false)
    const ev = root.querySelector<HTMLDetailsElement>('[data-evidence="politics"]')!
    expect(ev).not.toBeNull()
    ev.open = true
    expect(visibleText(ev)).toMatch(/M-[A-Z]+/)
  })

  it('the exact numbers live in the technical view, and only there', () => {
    const tech = mountAt('analysis').textContent ?? ''
    expect(tech).toMatch(/\b\d+\.\d{4}\b/)
    expect(tech).toMatch(/M-[A-Z]+/)
  })

  it('the technical view says what it is for, and offers the way back', () => {
    const r = mountAt('analysis')
    expect(r.querySelector('.techbar')?.textContent).toMatch(/looked up, not read/i)
    expect(r.querySelector('.techbar__back')).not.toBeNull()
  })
})

describe('structure and accessibility basics', () => {
  it('renders the landmark regions', () => {
    expect(root.querySelector('main')).not.toBeNull()
    expect(root.querySelector('[role="region"]')).not.toBeNull()
    // No <nav>: there is no primary navigation to landmark. The conversation is the product.
    expect(root.querySelector('[role="log"]')).not.toBeNull()
  })

  it('gives the situation diagram a descriptive text alternative', () => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    const label = root.querySelector('[data-diagram-answer] svg')!.getAttribute('aria-label') ?? ''
    expect(label.length).toBeGreaterThan(80)
    expect(label).toContain('fictional')
  })

  it('gives every control an accessible name', () => {
    for (const mode of ['ask', 'analysis'] as const) {
      mountAt(mode).querySelectorAll('button').forEach((b) => {
        const name = (b.textContent ?? '').trim() || b.getAttribute('aria-label') || ''
        expect(name.length, `${mode}: ${b.className}`).toBeGreaterThan(0)
      })
    }
  })

  it('uses real headings, not styled text', () => {
    expect(root.querySelector('h1')).not.toBeNull()
    expect(mountAt('analysis').querySelectorAll('h3').length).toBeGreaterThan(0)
  })

  it('does not communicate direction by colour alone', () => {
    root.querySelectorAll('.brow__d').forEach((d) => {
      expect((d.textContent ?? '').replace(/[↑↓→\s]/g, '').length).toBeGreaterThan(0)
    })
  })

  it('labels the conversation as a live region', () => {
    expect(root.querySelector('[role="log"]')?.getAttribute('aria-live')).toBe('polite')
  })
})

describe('technical evidence is a reference, not a dashboard', () => {
  it('offers a way to find a value rather than requiring a reader to scan', () => {
    const r = mountAt('analysis')
    expect(r.querySelector('[data-tt-filter]')).not.toBeNull()
    expect(r.querySelector('[data-tt-count]')?.textContent).toMatch(/\d+ values/)
  })

  it('leads each row with words, keeping the identifier beneath rather than instead', () => {
    const first = mountAt('analysis').querySelector('.tt__name')!
    expect(first.querySelector('.tt__id')).not.toBeNull()
    expect(first.textContent).not.toMatch(/^[a-z_]+$/)
  })

  it('groups rows so a reader knows what kind of value they are looking at', () => {
    const groups = [...mountAt('analysis').querySelectorAll('.tt__gh')].map((h) => h.textContent)
    expect(groups.join(' ')).toContain('Causal chain')
    expect(groups.join(' ')).toContain('Population groups')
    expect(groups.join(' ')).toContain('Government options')
  })
})

describe('nothing executes', () => {
  it('states it wherever a choice is shown', () => {
    expect(root.querySelector('[data-nothing-executes]')?.textContent)
      .toMatch(/nothing will be executed/i)
  })

  it('offers no control that claims to act on the world', () => {
    const verbs = /^(execute|run|apply|commit|deploy|launch|send to|order)\b/i
    root.querySelectorAll('button').forEach((b) => {
      expect(verbs.test((b.textContent ?? '').trim()), b.textContent ?? '').toBe(false)
    })
  })

  it('an unreachable engine still renders the briefing rather than an empty screen', () => {
    const offline: RunResult = { ...run, connection: 'unavailable' }
    expect(mountAt('ask', offline).querySelector('[data-briefing-card]')).not.toBeNull()
  })
})
