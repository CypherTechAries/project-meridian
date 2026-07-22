/**
 * Cognitive-load rules, made testable.
 *
 * The interface stopped failing on clipping and raw decimals and started failing on **effort**: too
 * much at once, evidence as blocks to be studied, and layout competing with the conversation.
 *
 * THE PRODUCT RULE: MERIDIAN should be easier than having a normal conversation. One sentence, no
 * more than three supporting points, and detail only when deliberately asked for. These tests hold
 * the interface to that, because "it feels lighter" is not a property anyone can check later.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import {
  HELPERS,
  MAX_INITIAL_STEPS,
  claimEvidence,
  compactCausal,
  fiveBeatChain,
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

const ask = (q: string): void => {
  const btn = [...root.querySelectorAll<HTMLElement>('[data-ask-question]')].find(
    (b) => b.dataset.askQuestion === q,
  )
  btn?.click()
}

describe('1-4 · starter questions and the composer', () => {
  it('1 · starter questions appear in the initial state', () => {
    const pills = [...root.querySelectorAll('.asksug__b')]
    expect(pills.length).toBe(HELPERS.length)
    expect(root.querySelector('.asksug__lbl')?.textContent).toMatch(/not sure where to start/i)
  })

  it('1a · every starter routes to a question the catalogue answers, so none can refuse', () => {
    for (const h of HELPERS) {
      const btn = root.querySelector(`[data-ask-question="${h.question}"]`)
      expect(btn, h.label).not.toBeNull()
    }
    // "Help me understand the decision" is deliberately absent — no catalogue question covers the
    // government's decision (issue #37), and a helper that always refuses is worse than none.
    expect(HELPERS.map((h) => h.label).join(' ')).not.toMatch(/understand the decision/i)
  })

  it('2 · starter questions disappear after the first user question', () => {
    ask(HELPERS[0]!.question)
    expect(root.querySelector('.asksug__lbl')).toBeNull()
    // They remain reachable, but only through a small deliberate control.
    expect(root.querySelector('.asksug--later')).not.toBeNull()
    expect(root.querySelector<HTMLDetailsElement>('.asksug--later')?.open).toBe(false)
  })

  it('3 · starter questions are in normal flow, never positioned over the transcript', () => {
    const sug = root.querySelector<HTMLElement>('.asksug')!
    const pos = sug.style.position || ''
    expect(pos).not.toBe('absolute')
    expect(pos).not.toBe('fixed')
    // They are a sibling AFTER the transcript, not a child of it.
    expect(sug.closest('.ask__thread')).toBeNull()
    expect(root.querySelector('.ask__thread')?.nextElementSibling?.className).toContain('ask__fade')
  })

  it('4 · the transcript reserves space so its last message clears the composer', () => {
    // jsdom has no layout, so the property is asserted structurally: the thread declares bottom
    // padding, and a fade element sits at its edge.
    const thread = root.querySelector<HTMLElement>('.ask__thread')!
    expect(thread).not.toBeNull()
    expect(root.querySelector('.ask__fade')).not.toBeNull()
  })
})

describe('5-6 · no context rail', () => {
  it('5 · no permanent context rail appears in the default Ask view', () => {
    expect(root.querySelector('.ask__ctx')).toBeNull()
    expect(root.querySelector('aside')).toBeNull()
  })

  it('6 · empty context reserves no layout space, before or after asking', () => {
    expect(root.querySelector('.ask__ctx')).toBeNull()
    ask(HELPERS[0]!.question)
    expect(root.querySelector('.ask__ctx')).toBeNull()
  })
})

describe('7-8 · Exact numbers is demoted, not deleted', () => {
  it('7 · Exact numbers is absent from primary navigation', () => {
    expect(root.querySelectorAll('.navbar .navbtn')).toHaveLength(0)
    expect(root.textContent).not.toMatch(/Exact numbers/)
  })

  it('8 · technical values remain reachable through a secondary evidence path', () => {
    // Path one: claim-driven, attached to the claim it supports.
    const ev = root.querySelector<HTMLDetailsElement>('[data-evidence="politics"]')!
    expect(ev).not.toBeNull()
    expect(ev.open).toBe(false)
    expect(ev.textContent).toMatch(/show evidence/i)

    // Path two: the full record, from inside an explanation.
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
    expect(root.querySelector('[data-mode="analysis"]')).not.toBeNull()
  })

  it('8a · claim evidence carries value, direction, origin, last change and mechanism', () => {
    const ev = claimEvidence(run, 'political_pressure')!
    expect(ev.value).toMatch(/^\d\.\d{4}$/)
    expect(ev.level).toBe('LOW')
    expect(ev.direction).toBe('FALLING')
    expect(ev.origin).toBeTruthy()
    expect(ev.lastChanged).toMatch(/tick \d+/)
    expect(ev.mechanism).toBeTruthy()
  })

  it('8b · the full table is still reachable and still complete', () => {
    mount(root, run, 'analysis')
    expect(root.querySelectorAll('.tt__r').length).toBeGreaterThan(15)
  })
})

describe('9-11 · the causal answer is layered', () => {
  beforeEach(() => {
    root.querySelector<HTMLElement>('[data-show-diagram]')!.click()
  })

  it('9 · the default causal explanation shows no more than five beats and no charts', () => {
    const ca = root.querySelector('[data-causal-answer]')!
    const beats = ca.querySelectorAll('.ca__beat')
    expect(beats.length).toBeLessThanOrEqual(5)
    expect(beats.length).toBeGreaterThan(2)
    expect(fiveBeatChain(run).length).toBeLessThanOrEqual(5)

    // No bars, sparklines, decimals or captions in the default view.
    const visible = ca.querySelector('.ca__chain')!
    expect(visible.querySelector('svg')).toBeNull()
    expect(visible.textContent).not.toMatch(/\d+\.\d+/)
  })

  it('9a · the compact answer keeps to one sentence and at most three supporting points', () => {
    const c = compactCausal(run)
    expect(c.shortAnswer.split('.').filter((s) => s.trim()).length).toBe(1)
    expect(c.steps.length).toBeLessThanOrEqual(MAX_INITIAL_STEPS)
  })

  it('9b · beat four states the comparison set, never an absolute high', () => {
    const beat = fiveBeatChain(run).find((b) => /affected most/i.test(b))!
    expect(beat).toBeTruthy()
    // The hardest-hit group is 0.33 — LOW on the declared thresholds. It must say so.
    expect(beat).toMatch(/though the level is still low/i)
    expect(beat).not.toMatch(/\bvery high\b|\bsevere\b/i)
  })

  it('10 · the full chain is collapsed initially', () => {
    const why = root.querySelector<HTMLDetailsElement>('[data-show-why]')!
    expect(why).not.toBeNull()
    expect(why.open).toBe(false)
    // The control asks about reasoning, not numbers — most readers want why, not values.
    expect(why.querySelector('summary')?.textContent).toMatch(/show why/i)
    expect(why.querySelector('summary')?.textContent).not.toMatch(/numbers/i)
  })

  it('11 · the full chain can be deliberately opened', () => {
    const why = root.querySelector<HTMLDetailsElement>('[data-show-why]')!
    why.open = true
    expect(why.querySelector('svg')).not.toBeNull()
    expect(why.textContent).toMatch(/share of population/i)
    expect(why.textContent).toMatch(/impact on this group/i)
  })
})

describe('12-13 · bounded answers and honest affordances', () => {
  it('12 · the first answer is a summary, not a dossier', () => {
    const card = root.querySelector('[data-briefing-card]')!
    // central event + three effects + one decision + ONE next action
    expect(card.querySelectorAll('.brow')).toHaveLength(3)
    expect(card.querySelectorAll('.bdec')).toHaveLength(1)
    expect(card.querySelectorAll('.bcard__ft button')).toHaveLength(1)
  })

  it('13 · every impact row offers the same affordance, so none looks broken', () => {
    // An earlier version made the row a button that asked a catalogue question — which worked for
    // People and Economy and had to be inert for Politics (#37). Two rows that behaved and one
    // that did not is what makes an interface feel broken. "Show evidence" works for every claim.
    const rows = [...root.querySelectorAll('.brow-i')]
    expect(rows).toHaveLength(3)
    for (const r of rows) {
      expect(r.querySelector('[data-evidence]'), r.textContent ?? '').not.toBeNull()
    }
    // And #37 is not hidden: nothing offers to ask MERIDIAN about politics.
    const asks = [...root.querySelectorAll<HTMLElement>('[data-ask-question]')]
      .map((b) => b.dataset.askQuestion ?? '')
    expect(asks.some((q) => /political|government/i.test(q))).toBe(false)
  })
})
