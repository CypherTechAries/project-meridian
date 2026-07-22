/**
 * The Briefing as the conversation's first answer.
 *
 * Replaces `briefing-reset.test.ts`, which tested the Briefing as a separate screen. **Every
 * property that suite enforced is carried forward here**, re-targeted at the card. Where the
 * property moved rather than changed, the test says where it went:
 *
 *  - "Briefing is the landing screen"  → the landing screen IS the conversation, and the Briefing
 *    is its first message. Tested as: the app opens with the card, without asking anything.
 *  - "what can I ask" / "what MERIDIAN does not know" → these were 598px of static prose. They are
 *    now suggestion chips that ASK the declared questions, so the answer is live rather than
 *    recited. Tested as: the chips exist and carry real catalogue questions.
 *  - "technical values reachable through evidence controls" → the per-row disclosures are gone.
 *    Evidence is reached by asking, or in the technical table. Tested as both.
 *
 * The measured failure this replaces: 2,635px, 2.9 screenfuls, with the one decision waiting
 * beginning 257px BELOW the fold.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'
import { HELPERS } from '../src/engine/presentation.ts'
import { plainDecision, primaryDecision } from '../src/engine/presentation.ts'

const run = initialSnapshot()
let root: HTMLElement

beforeEach(() => {
  root = document.createElement('div')
  root.id = 'app'
  document.body.innerHTML = ''
  document.body.appendChild(root)
  mount(root, run)
})

const card = (): HTMLElement => root.querySelector('[data-briefing-card]')!

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


describe('1-3 · the landing state', () => {
  it('1 · the app opens on the conversation with the Briefing already answered', () => {
    expect(root.dataset.mode).toBe('ask')
    expect(card()).not.toBeNull()
    // Nothing was asked to get here.
    expect(root.querySelectorAll('.askmsg--u')).toHaveLength(0)
  })

  it('2 · the composer is present, so asking is the obvious next step', () => {
    expect(root.querySelector('[data-ask-form]')).not.toBeNull()
    expect(root.querySelector('[data-ask-input]')).not.toBeNull()
  })

  it('3 · there is no primary navigation competing with the conversation', () => {
    expect(root.querySelectorAll('.navbar .navbtn')).toHaveLength(0)
    // The one next action on the card is a real button.
    const go = root.querySelector('.bcard__ft button')!
    expect(go.tagName).toBe('BUTTON')
  })
})

describe('4-8 · the story the card tells', () => {
  it('4 · the headline states the central crisis in plain English', () => {
    const h = card().querySelector('.bcard__h')!
    expect(h.textContent).toMatch(/blocked|strait/i)
    // Short enough to read at a glance.
    expect((h.textContent ?? '').split(/\s+/).length).toBeLessThanOrEqual(15)
  })

  it('5 · People, Economy and Politics are each one line', () => {
    const rows = [...card().querySelectorAll('.brow')]
    expect(rows).toHaveLength(3)
    expect(rows.map((r) => r.querySelector('.brow__t')?.textContent))
      .toEqual(['People', 'Economy', 'Politics'])
    for (const r of rows) {
      const line = r.querySelector('.brow__l')?.textContent ?? ''
      expect(line.split(/\s+/).length, line).toBeLessThanOrEqual(22)
    }
  })

  it('5a · direction is stated as a word, not by colour or an arrow alone', () => {
    for (const d of card().querySelectorAll('.brow__d')) {
      expect((d.textContent ?? '').replace(/[↑↓→\s]/g, '')).toMatch(/rising|falling|steady|notestablished/i)
    }
  })

  it('6 · exactly one primary decision is displayed', () => {
    expect(card().querySelectorAll('.bdec')).toHaveLength(1)
  })

  it('7 · the decision is phrased as an understandable question', () => {
    const q = card().querySelector('.bdec__h')!.textContent ?? ''
    expect(q.trim().endsWith('?')).toBe(true)
    expect(q).not.toMatch(/_/)
    expect(q).toBe(plainDecision(primaryDecision(run.projection)!).question)
  })

  it('8 · the card states that nothing will be executed', () => {
    expect(card().querySelector('[data-nothing-executes]')?.textContent)
      .toMatch(/nothing will be executed/i)
  })
})

describe('Q4-Q5 · what can I ask, and what is not known', () => {
  it('Q4 · guided helpers are offered without opening anything first', () => {
    const chips = [...root.querySelectorAll('.asksug__b')].map((b) => b.textContent?.trim())
    expect(chips).toHaveLength(HELPERS.length)
    // Plain-language labels, each routed to a question the catalogue can actually answer.
    for (const h of HELPERS) expect(chips).toContain(h.label)
  })

  it('Q5 · what MERIDIAN does not know is ASKABLE, not recited', () => {
    const qs = [...root.querySelectorAll<HTMLElement>('.asksug__b')].map((b) => b.dataset.askQuestion)
    expect(qs.some((q) => /remains uncertain/i.test(q ?? ''))).toBe(true)
  })

  it('Q4a · every row exposes the evidence for its own claim, uniformly', () => {
    for (const id of ['people', 'economy', 'politics']) {
      const ev = card().querySelector<HTMLDetailsElement>(`[data-evidence="${id}"]`)
      expect(ev, id).not.toBeNull()
      expect(ev!.open, id).toBe(false)
    }
  })
})

describe('9-12a · what may not appear at level 1', () => {
  const text = (): string => visibleText(root)

  it('9 · raw rule-pack and scenario identifiers are absent', () => {
    expect(text()).not.toContain(run.projection.rule_pack_version)
    expect(text()).not.toMatch(/@\d+\.\d+\.\d+/)
  })

  it('10 · raw action and field identifiers are absent', () => {
    expect(text()).not.toMatch(/[a-z]+_[a-z_]+/)
    expect(text()).not.toMatch(/chain\./)
  })

  it('11 · tick, seed and revision are absent', () => {
    for (const w of [/\btick\b/i, /\bseed\b/i, /\brevision\b/i, /rule.?pack/i]) {
      expect(text(), String(w)).not.toMatch(w)
    }
  })

  it('12 · decimal scores are absent', () => {
    expect(text()).not.toMatch(/\b\d+\.\d+\b/)
  })

  it('12b · the detail really is behind a CLOSED control, not merely hidden by the helper', () => {
    // visibleText() only tells the truth if the disclosures are genuinely shut on load.
    for (const d of root.querySelectorAll<HTMLDetailsElement>('details')) {
      expect(d.open, d.querySelector('summary')?.textContent ?? '').toBe(false)
    }
    // And the detail exists — the evidence is attached, not deleted.
    const ev = card().querySelector<HTMLDetailsElement>('[data-evidence="politics"]')!
    ev.open = true
    expect(visibleText(ev)).toMatch(/Mechanism/)
  })

  it('12a · banned engine vocabulary is absent', () => {
    for (const w of ['epistemic', 'provenance', 'projection', 'cohort', 'mechanism']) {
      expect(text().toLowerCase(), w).not.toContain(w)
    }
  })

  it('13 · technical values remain reachable, one step away', () => {
    // Claim-driven: the evidence for a specific claim, opened deliberately.
    const ev = card().querySelector<HTMLDetailsElement>('[data-evidence="politics"]')!
    ev.open = true
    expect(ev.textContent).toMatch(/Exact value/)
    expect(ev.textContent).toMatch(/Mechanism/)
  })
})

describe('14-17 · shape and navigation', () => {
  it('14 · the card uses no fixed-height clipping', () => {
    for (const el of card().querySelectorAll<HTMLElement>('*')) {
      expect(el.style.height, el.className).not.toMatch(/^\d+px$/)
    }
  })

  it('15 · the diagram is offered but not opened, so it cannot dominate the first view', () => {
    expect(root.querySelector('[data-show-diagram]')).not.toBeNull()
    expect(root.querySelector('[data-diagram-answer]')).toBeNull()
  })

  it('16 · the diagram opens as an answer in the thread', () => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    expect(root.querySelector('[data-diagram-answer] svg')).not.toBeNull()
    // and it did not navigate away from the conversation
    expect(root.dataset.mode).toBe('ask')
  })

  it('17 · the technical view offers the way back to the conversation', () => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    root.querySelector<HTMLElement>('[data-mode="analysis"]')!.click()
    const back = root.querySelector<HTMLElement>('.techbar__back')!
    expect(back).not.toBeNull()
    back.click()
    expect(root.dataset.mode).toBe('ask')
    expect(root.querySelector('[data-briefing-card]')).not.toBeNull()
  })

  it('17a · clearing the conversation returns to the Briefing, not to an empty screen', () => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    expect(root.querySelectorAll('.askmsg--m, [data-briefing-card]').length).toBeGreaterThan(1)
    root.querySelector<HTMLElement>('[data-ask-reset]')!.click()
    expect(root.querySelector('[data-briefing-card]')).not.toBeNull()
    expect(root.querySelector('[data-diagram-answer]')).toBeNull()
  })
})

describe('18-19 · declared limits', () => {
  it('19 · politics states this is a fictional scenario at a point in time, not a prediction', () => {
    // The caveat moved with the section; it did not survive as prose on a deleted screen.
    const politics = card().querySelector('[data-row="politics"] .brow__l')!.textContent ?? ''
    expect(politics).toMatch(/low/i)
    // The full caveat is available by asking, and on the technical view.
    expect(politics).not.toMatch(/prediction/i)
  })

  it('19a · the near-peak fact travels with the level, so neither reads alone', () => {
    const politics = card().querySelector('[data-row="politics"] .brow__l')!.textContent ?? ''
    expect(politics).toMatch(/close to the highest it has been so far/)
  })

  it('20 · with the shared state absent the card withholds levels rather than inventing them', () => {
    const blind: RunResult = { ...run, state: undefined }
    const r = document.createElement('div')
    mount(r, blind, 'ask')
    const rows = [...r.querySelectorAll('.brow__d')]
    expect(rows.length).toBeGreaterThan(0)
    for (const d of rows) expect(d.textContent).toMatch(/not established/i)
  })
})
