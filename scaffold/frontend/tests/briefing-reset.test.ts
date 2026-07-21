/**
 * Briefing — first-user usability reset.
 *
 * The previous Briefing tests asserted the structure of a screen that failed its first usability
 * test: a dominant map, a decision stack, three cards each carrying a trend graph and an origin
 * badge. Those assertions were removed with the design they described. These replace them.
 *
 * Every test here pins something the first-time user could not do, or something they must never be
 * shown again. See docs/design/FIRST-USER-USABILITY-TEST.md.
 *
 * All of them drive the REAL application shell through `mount()`, not the view function directly —
 * that distinction is what earlier milestones learned the hard way.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'
import { MAP_LIMITATION, NOTHING_EXECUTES } from '../src/screens/briefing.ts'
import { plainDecision, plainSections, primaryDecision } from '../src/engine/presentation.ts'
import { STARTERS } from '../src/screens/ask-meridian.ts'

let root: HTMLElement
const run: RunResult = initialSnapshot()

beforeEach(() => {
  root = document.createElement('div')
  mount(root, run)
})

/** Text of the briefing main region only — never the disclosure strip or the shell chrome. */
function briefingText(): string {
  return root.querySelector('.main--briefing')?.textContent ?? ''
}

/**
 * What a reader actually SEES on arrival: the briefing with every collapsed panel's body removed.
 *
 * The distinction matters and is the whole point of the reset. Identifiers, exact values and engine
 * field names are not deleted — they are moved inside `<details>` elements that are closed by
 * default. Asserting they are absent from `briefingText()` would forbid the very place they are
 * supposed to live, and would be satisfied only by deleting the evidence. Summaries are kept,
 * because a closed summary IS visible.
 */
function defaultText(): string {
  const main = root.querySelector('.main--briefing')
  if (!main) return ''
  const clone = main.cloneNode(true) as HTMLElement
  for (const d of clone.querySelectorAll('details')) {
    for (const child of [...d.children]) {
      if (child.tagName.toLowerCase() !== 'summary') child.remove()
    }
  }
  return clone.textContent ?? ''
}

describe('1-3 · landing, navigation and the Ask control', () => {
  it('1 · Briefing is the landing screen', () => {
    expect(root.querySelector('.briefing')).not.toBeNull()
    expect(root.querySelector('.main--briefing')).not.toBeNull()
    const on = root.querySelector('.navbtn.is-on')
    expect(on?.querySelector('.navbtn__l')?.textContent?.trim()).toBe('Briefing')
    expect(on?.getAttribute('aria-pressed')).toBe('true')
  })

  it('2 · Analysis is not in the primary navigation', () => {
    const nav = root.querySelector('.navbar') as HTMLElement
    expect(nav).not.toBeNull()
    const labels = [...nav.querySelectorAll('.navbtn__l')].map((b) => b.textContent?.trim())
    expect(labels).toEqual(['Briefing', 'Ask MERIDIAN'])
    expect(nav.textContent?.toLowerCase()).not.toContain('analysis')
    // and no control anywhere in the nav switches to it
    expect(nav.querySelector('[data-mode="analysis"]')).toBeNull()
  })

  it('3 · Ask MERIDIAN is visibly and semantically a button', () => {
    const ask = root.querySelector('.navbar [data-mode="ask"]') as HTMLElement
    expect(ask.tagName).toBe('BUTTON')
    expect(ask.getAttribute('type')).toBe('button')
    expect(ask.textContent).toContain('Ask MERIDIAN')
    expect(ask.hasAttribute('aria-pressed')).toBe(true)
    // the same shape and weight as its sibling — not a wordmark styled apart from the nav
    const briefing = root.querySelector('.navbar [data-mode="briefing"]') as HTMLElement
    expect(ask.className.replace(' is-on', '')).toBe(briefing.className.replace(' is-on', ''))
  })
})

describe('4-8 · the story the screen tells', () => {
  it('4 · the headline states the central crisis in plain English', () => {
    const h1 = root.querySelector('.lede__h') as HTMLElement
    const text = h1.textContent?.trim() ?? ''
    expect(text).toMatch(/^The strait has been blocked for \w+ days?\.$/)
    // written in words, and derived from the run rather than authored
    const days = Math.max(1, Math.round(run.projection.simulated_hours / 24))
    expect(text).toContain(['zero', 'one', 'two', 'three', 'four', 'five', 'six'][days] ?? String(days))
    // no digits, no units, no machinery in the first thing a reader sees
    expect(text).not.toMatch(/\d/)
  })

  it('4a · the supporting sentences are short and plain', () => {
    const lede = root.querySelector('.lede__p')?.textContent?.trim() ?? ''
    expect(lede.length).toBeGreaterThan(20)
    expect(lede).not.toMatch(/\d/)
    for (const term of ['tick', 'credence', 'cohort', 'threshold', 'provenance']) {
      expect(lede.toLowerCase()).not.toContain(term)
    }
  })

  it('5 · People, Economy and Politics are visible', () => {
    const heads = [...root.querySelectorAll('.sec__h')].map((h) => h.textContent?.trim())
    expect(heads).toEqual(['People', 'Economy', 'Politics'])
    for (const s of root.querySelectorAll('.sec')) {
      // each section carries at least one readable sentence
      expect(s.querySelectorAll('.sec__p').length).toBeGreaterThan(0)
      expect((s.querySelector('.sec__p')?.textContent ?? '').length).toBeGreaterThan(15)
    }
  })

  it('5a · direction is stated as a word, not by colour or a graph alone', () => {
    const sections = plainSections(run)
    const withDirection = sections.filter((s) => s.direction)
    expect(withDirection.length).toBeGreaterThan(0)
    for (const s of withDirection) {
      const el = root.querySelector(`.sec--${s.id} .sec__dir`) as HTMLElement
      expect(el.textContent).toContain(s.direction!)
    }
    // the tiny trend graphs are gone
    expect(root.querySelectorAll('.main--briefing .tline').length).toBe(0)
  })

  it('6 · only one primary decision is displayed initially', () => {
    // exactly one open decision block
    expect(root.querySelectorAll('.main--briefing .dec').length).toBe(1)
    // the others exist but are collapsed behind a control
    const others = root.querySelector('.others') as HTMLDetailsElement
    if (others) {
      expect(others.open).toBe(false)
      expect(others.querySelector('.others__s')?.textContent).toContain('See other decisions')
    }
  })

  it('7 · the decision is phrased as an understandable question', () => {
    const h = root.querySelector('.dec__h')?.textContent?.trim() ?? ''
    expect(h.endsWith('?')).toBe(true)
    expect(h.split(' ').length).toBeGreaterThan(4)
    // the internal label is not the user-facing question
    expect(h).not.toMatch(/_/)
    expect(h.toLowerCase()).not.toBe('publish legal advice')
    // and the question is explained before any choice is offered
    expect(root.querySelectorAll('.dec__p').length).toBeGreaterThanOrEqual(2)
  })

  it('8 · the page states that nothing will be executed', () => {
    const note = root.querySelector('[data-nothing-executes]')?.textContent?.trim()
    expect(note).toBe(NOTHING_EXECUTES)
    expect(note).toContain('nothing will be executed')
    // the choices are display only and claim no outcome
    const text = defaultText().toLowerCase()
    expect(text).not.toMatch(/this will (reduce|increase|cause)|outcome:|result:/)
  })
})

describe('4a-5a · the five questions the interface must answer unprompted', () => {
  /*
   * The acceptance criteria are that a reader, with no prior explanation, can answer: what happened,
   * why it matters, what needs attention, what they can ask, and what MERIDIAN does not know. A cold
   * verification pass found questions 4 and 5 unanswered on the Briefing; these pin the fix.
   */
  it('Q4 · the Briefing says what can be asked, without opening Ask first', () => {
    const sec = root.querySelector('.askprompt') as HTMLElement
    expect(sec).not.toBeNull()
    expect(sec.textContent).toContain('Ask in your own words')
    const examples = [...sec.querySelectorAll('.askprompt__list li')].map((l) => l.textContent?.trim())
    expect(examples.length).toBeGreaterThanOrEqual(3)
    // the examples are the questions Ask MERIDIAN actually accepts — they cannot drift apart
    for (const e of examples) expect(STARTERS).toContain(e!)
  })

  it('Q4a · the prompt offers a working route into Ask MERIDIAN', () => {
    const go = root.querySelector('.askprompt__go') as HTMLElement
    expect(go.tagName).toBe('BUTTON')
    go.click()
    expect(root.querySelector('[data-ask-form]')).not.toBeNull()
  })

  it('Q5 · the Briefing states what MERIDIAN does not know', () => {
    const sec = root.querySelector('.unknown') as HTMLElement
    expect(sec).not.toBeNull()
    expect(sec.querySelector('.unknown__h')?.textContent).toContain('does not know')
    const t = sec.textContent ?? ''
    expect(t).toContain('not a forecast')
    expect(t).toMatch(/never\s+zero/)
    expect(t).toContain('averages')
  })
})

describe('9-13 · what the default view may not show', () => {
  it('9 · raw rule-pack identifiers are absent from the default Briefing', () => {
    const t = defaultText()
    expect(t).not.toMatch(/M-[A-Z-]+@/)
    expect(t).not.toMatch(/@\d+\.\d+\.\d+/)
    expect(t.toLowerCase()).not.toContain('rule pack')
    expect(t).not.toContain(run.projection.rule_pack_version)
  })

  it('10 · raw action identifiers are absent', () => {
    const t = defaultText()
    for (const o of run.projection.government_options) {
      // the identifier itself, and the underscored label it is built from
      expect(t).not.toContain(o.option_id)
      expect(t).not.toContain(o.label)
    }
    expect(t).not.toMatch(/\b[a-z]+_[a-z_]+\b/)
  })

  it('11 · tick, seed and revision are absent from the default Briefing', () => {
    const t = defaultText().toLowerCase()
    for (const term of ['tick', 'seed', 'revision', 'horizon', 'state_revision']) {
      expect(t).not.toContain(term)
    }
    expect(defaultText()).not.toContain(String(run.projection.state_revision))
  })

  it('12 · decimal crisis scores are absent from the default Briefing', () => {
    const t = defaultText()
    expect(t).not.toMatch(/\d+\.\d+/)
    // every stage value, at the precision the engine reports it
    for (const s of run.projection.stages) {
      expect(t).not.toContain(String(s.value))
      expect(t).not.toContain(s.value.toFixed(4))
    }
  })

  it('12a · banned engine vocabulary is absent from the default Briefing', () => {
    const t = defaultText().toLowerCase()
    for (const term of ['credence', 'provenance', 'lagged', 'peaked', 'state mass', 'alignment',
                        'threshold', 'rule pack', 'propagation', 'cohort', 'fixture',
                        'causal slice', 'epistemic']) {
      expect(t, `banned term "${term}"`).not.toContain(term)
    }
  })

  it('13 · technical values remain reachable through evidence controls', () => {
    const evs = [...root.querySelectorAll('.main--briefing details.ev')] as HTMLDetailsElement[]
    expect(evs.length).toBeGreaterThanOrEqual(4) // three sections + the decision
    for (const d of evs) {
      expect(d.open).toBe(false) // closed by default: not shown, but not deleted
      expect(d.querySelector('summary')).not.toBeNull()
      expect((d.querySelector('.ev__b')?.textContent ?? '').length).toBeGreaterThan(20)
    }
    // the decision's evidence really does carry the identifiers the default view withholds
    const primary = primaryDecision(run.projection)!
    const decEv = root.querySelector('.dec details.ev')?.textContent ?? ''
    expect(decEv).toContain(primary.option_id)
    expect(decEv).toContain(primary.driven_by)
    // present in the DOM (so reachable), absent from what is shown on arrival
    expect(briefingText()).toContain(primary.option_id)
    expect(defaultText()).not.toContain(primary.option_id)
    // and the technical route is offered explicitly
    expect(root.querySelector('.bfoot__tech')?.textContent).toContain('technical evidence')
  })
})

describe('14-15 · layout may not hide content', () => {
  it('14 · no briefing card uses fixed-height clipping', () => {
    for (const el of root.querySelectorAll('.briefing, .briefing *')) {
      const style = (el as HTMLElement).getAttribute('style') ?? ''
      expect(style).not.toMatch(/(^|;)\s*height\s*:/)
      expect(style).not.toMatch(/max-height\s*:/)
      expect(style).not.toMatch(/overflow\s*:\s*hidden/)
    }
    // the old dashboard grid, which sized panels by the viewport, is gone
    expect(root.querySelector('.bviz')).toBeNull()
    expect(root.querySelector('.bneeds')).toBeNull()
    expect(root.querySelector('.ccards')).toBeNull()
  })

  it('15 · the secondary decision is not cropped or competing on first view', () => {
    const others = root.querySelector('.others') as HTMLDetailsElement | null
    if (!others) return // a run with a single option is legitimate
    expect(others.open).toBe(false)
    // every other option is present inside, in full, with its plain question
    const ids = [...others.querySelectorAll('.others__i')].map((n) => n.getAttribute('data-option-id'))
    const primary = primaryDecision(run.projection)!
    const expected = run.projection.government_options
      .filter((o) => o.option_id !== primary.option_id)
      .map((o) => o.option_id)
    expect(ids).toEqual(expected)
    for (const o of run.projection.government_options) {
      if (o.option_id === primary.option_id) continue
      expect(others.textContent).toContain(plainDecision(o).question)
    }
  })
})

describe('16-17 · navigation through the real shell', () => {
  it('16 · Ask MERIDIAN opens through the real application shell', () => {
    const btn = root.querySelector('.navbar [data-mode="ask"]') as HTMLElement
    btn.click()
    expect(root.querySelector('[aria-label="Ask MERIDIAN"]')).not.toBeNull()
    expect(root.querySelector('[data-ask-form]')).not.toBeNull()
  })

  it('17 · Briefing remains reachable from Ask MERIDIAN', () => {
    ;(root.querySelector('.navbar [data-mode="ask"]') as HTMLElement).click()
    const back = root.querySelector('.navbar [data-mode="briefing"]') as HTMLElement
    expect(back).not.toBeNull()
    back.click()
    expect(root.querySelector('.briefing')).not.toBeNull()
    expect(root.querySelector('.lede__h')).not.toBeNull()
  })

  it('17a · technical evidence is reachable, labelled, and offers the way back', () => {
    ;(root.querySelector('.bfoot__tech') as HTMLElement).click()
    const bar = root.querySelector('.techbar') as HTMLElement
    expect(bar).not.toBeNull()
    expect(bar.textContent).toContain('Technical evidence')
    // the detail the Briefing withholds really is here
    expect(root.textContent).toContain(run.projection.rule_pack_version)
    ;(bar.querySelector('.techbar__back') as HTMLElement).click()
    expect(root.querySelector('.briefing')).not.toBeNull()
  })
})

/**
 * Founder review items 3 and 4: the map keeps an honest limitation next to its control, and the
 * politics section states what its inconvenient value is and is not.
 */
describe('18-19 · declared limits on the map and on politics', () => {
  it('18 · the map control carries a stated limitation and the map stays closed by default', () => {
    const where = root.querySelector('details.where') as HTMLDetailsElement
    expect(where).not.toBeNull()
    expect(where.open, 'the map must not display automatically').toBe(false)
    const limit = where.querySelector('.where__limit') as HTMLElement
    expect(limit).not.toBeNull()
    expect(limit.textContent).toContain('five-second comprehension test')
    expect(limit.textContent).toContain('supporting evidence')
    // The wording is declared once, so the screen and the record cannot drift apart.
    expect(limit.textContent).toContain(MAP_LIMITATION.slice(0, 60))
  })

  it('19 · politics states the value is this fictional scenario at this point, not a prediction', () => {
    const politics = root.querySelector('.sec--politics') as HTMLElement
    expect(politics).not.toBeNull()
    const caveat = politics.querySelector('.sec__caveat') as HTMLElement
    expect(caveat, 'the politics section must carry a reading limit').not.toBeNull()
    const t = caveat.textContent ?? ''
    expect(t).toContain('fictional scenario')
    expect(t).toContain('not a prediction')
    expect(t).toMatch(/not a judgement about how a real government/)
    // It qualifies the value; it must not replace or soften it.
    expect(politics.textContent).toContain('Pressure on the government is')
  })

  it('19a · only politics carries the caveat, so it reads as specific rather than boilerplate', () => {
    const sections = plainSections(run)
    expect(sections.filter((s) => s.caveat !== null).map((s) => s.id)).toEqual(['politics'])
  })
})
