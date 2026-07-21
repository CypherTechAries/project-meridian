/**
 * Ask MERIDIAN Phase 1 — frontend honesty and accessibility tests.
 *
 * Asserts Briefing remains the landing view, the four starters render without an unexplained
 * fictional name, answers carry the read-only speaker header and their limitations, decisions state
 * NOT EXECUTED, population groups state they are averages, and no cabinet or person dialogue is
 * presented as implemented.
 */

import { beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import {
  ABSENCE_TOKENS,
  ASK_ENDPOINT,
  ASK_NOTE,
  ASK_SPEAKER,
  ASK_SPEAKER_AUTHORITY,
  STARTERS,
  UNDECLARED_STATUS,
  askHome,
  askMeridianView,
  classifyBoundaryStatus,
} from '../src/screens/ask-meridian.ts'
import type { AskResponse } from '../src/screens/ask-meridian.ts'
import { API_BASE } from '../src/engine/api.ts'
import { briefingMap } from '../src/components/briefing-viz.ts'
import { mapCallouts } from '../src/engine/presentation.ts'

function el(html: string): HTMLElement {
  const d = document.createElement('div')
  d.innerHTML = html
  return d
}

/** A response shaped exactly like the backend's, so the test exercises the real render path. */
function decisionResponse(): AskResponse {
  return {
    response_id: 'ask-explain_person_decision-broadcast-journalist',
    matched_intent: 'EXPLAIN_PERSON_DECISION',
    normalized_question: 'why did the journalist seek another source',
    mode: 'EXPLORE',
    read_only: true,
    supported: true,
    short_answer:
      "The person selected 'seek additional corroboration' because it best supported the goal to " +
      'publish an accurate report. Nothing was executed.',
    components: [
      {
        component_type: 'DecisionCard',
        title: 'Decision',
        body: {
          selected_action_label: 'seek additional corroboration',
          execution_status: 'NOT_EXECUTED',
          default_statement: 'Selected by the declared rule. Not executed.',
          unavailable_options: ['a-publish-now'],
          blocking_constraints: { 'a-publish-now': ['c-corroboration'] },
        },
      },
      {
        component_type: 'ModelBoundaryCard',
        title: 'What MERIDIAN does not model',
        body: { not_modelled: ['memory', 'relationships', 'intelligence', 'competence'] },
      },
    ],
    evidence: [{ label: 'Show the calculation', destination: '/api/virtual-person/x', kind: 'api' }],
    limitations: ['This is a packaged snapshot, not live run state.', 'Nothing was executed.'],
    suggested_follow_ups: ['What does MERIDIAN know — and what remains uncertain?'],
    supported_questions: [...STARTERS],
    execution_status: 'NOT_EXECUTED',
    run_integration: { connected_to_authoritative_run: false },
  }
}

function reactionResponse(): AskResponse {
  return {
    ...decisionResponse(),
    matched_intent: 'SHOW_PUBLIC_REACTION',
    short_answer: 'Population groups are represented by averages.',
    components: [
      {
        component_type: 'PopulationGroupCard',
        title: 'Population groups — averages, not individuals',
        body: {
          note: 'Group-level averages. MERIDIAN does not model the individuals inside these groups.',
          groups: [{ name: 'Port workers', result: 'average moved a little', breakdown: 'UNAVAILABLE' }],
        },
      },
    ],
  }
}

function unsupportedResponse(): AskResponse {
  return {
    ...decisionResponse(),
    matched_intent: null,
    supported: false,
    short_answer: 'I cannot answer that question in this version.',
    components: [{ component_type: 'UnsupportedQuestionCard', title: 'Not supported', body: {} }],
    evidence: [],
    suggested_follow_ups: [],
  }
}

describe('landing view and navigation', () => {
  let root: HTMLElement
  beforeEach(() => {
    root = document.createElement('div')
    mount(root, initialSnapshot())
  })

  it('1 · Briefing remains the default landing view', () => {
    const active = root.querySelector('[aria-pressed="true"], .modesw__b--on, [data-mode="briefing"]')
    expect(root.textContent).toContain('Briefing')
    // the briefing situation summary is present on first mount
    expect(root.querySelector('.briefing')).not.toBeNull()
    expect(active === null || active.textContent?.toLowerCase()).toBeTruthy()
  })

  it('2 · Ask MERIDIAN appears in navigation', () => {
    expect(root.textContent).toContain('Ask MERIDIAN')
  })

  /*
   * REACHABILITY. The first version of this milestone rendered a nav link to "#ask" that nothing
   * handled, and no module imported the screen at all: every unit test passed while the screen was
   * unreachable in the running application. These two tests exercise the real control.
   */
  it('2a · the Ask MERIDIAN control opens the screen from Briefing', () => {
    const btn = root.querySelector<HTMLElement>('[data-mode="ask"]')
    expect(btn).not.toBeNull()
    btn!.click()
    expect(root.querySelector('[aria-label="Ask MERIDIAN"]')).not.toBeNull()
    expect(root.querySelector('[data-ask-form]')).not.toBeNull()
  })

  it('2b · Briefing remains reachable from the Ask screen', () => {
    root.querySelector<HTMLElement>('[data-mode="ask"]')!.click()
    const back = root.querySelector<HTMLElement>('[data-mode="briefing"]')
    expect(back).not.toBeNull()
    back!.click()
    expect(root.querySelector('.lede__h')).not.toBeNull()
  })
})

describe('Ask MERIDIAN home', () => {
  it('3 · the four current starter questions render', () => {
    const home = el(askHome())
    const starters = [...home.querySelectorAll('.askstart')].map((b) => b.textContent?.trim())
    expect(starters).toHaveLength(4)
    for (const s of STARTERS) expect(starters).toContain(s)
    expect(home.textContent).toContain(ASK_NOTE)
  })

  it('4 · no unexplained fictional name is shown as a starter', () => {
    const home = askHome().toLowerCase()
    for (const name of ['mara', 'venn', 'tomas', 'varo', 'elian', 'soro']) {
      expect(home).not.toContain(name)
    }
  })

  it('5 · current and future capabilities are not confused', () => {
    const home = askHome()
    expect(home).toContain('AVAILABLE NOW')
    // no future concept is presented as available
    for (const t of ['intelligence', 'diplomatic', 'military', 'cabinet']) {
      expect(home.toLowerCase()).not.toContain(t)
    }
  })
})

describe('answers', () => {
  it('6 · the read-only speaker header remains visible', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    expect(v.textContent).toContain(ASK_SPEAKER)
    expect(v.textContent).toContain(ASK_SPEAKER_AUTHORITY)
    expect(v.textContent).toContain('READ ONLY')
  })

  it('7 · a starter carries the question it will send', () => {
    const home = el(askHome())
    const first = home.querySelector('.askstart') as HTMLElement
    expect(first.dataset.question).toBe(STARTERS[0])
    // This assertion previously required the endpoint to be page-relative, which is exactly the
    // defect that made Ask MERIDIAN 404 in the real browser: the test locked the bug in place.
    // It now requires the shared backend base. See tests/api-routing.test.ts.
    expect(ASK_ENDPOINT).toBe(`${API_BASE}/api/ask-meridian/query`)
  })

  it('8 · a supported answer renders text and evidence components', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    expect(v.querySelector('.askmsg__text')?.textContent).toContain('seek additional corroboration')
    expect(v.querySelectorAll('.askev__b').length).toBeGreaterThan(0)
    expect(v.querySelector('[data-component="ModelBoundaryCard"]')).not.toBeNull()
  })

  /*
   * The map card previously emitted an EMPTY div that nothing ever painted into, and asserting on
   * its data attribute alone did not catch that. These tests assert drawn content.
   */
  it('9 · the canonical map is the real Briefing component, drawn', () => {
    const run = initialSnapshot()
    const v = el(askMeridianView([], run))
    const map = v.querySelector('[data-canonical-map]') as HTMLElement
    expect(map.dataset.canonicalMap).toBe('briefing-canonical-map')
    // byte-identical to what the Briefing draws: the same component, not a redraw
    const days = Math.max(1, Math.round(run.projection.simulated_hours / 24))
    const expected = el(briefingMap(run, mapCallouts(run), days))
    expect(map.innerHTML.trim()).toBe(expected.innerHTML.trim())
    expect(map.querySelector('svg')).not.toBeNull()
    expect(map.querySelectorAll('path, circle').length).toBeGreaterThan(5)
  })

  it('9a · with no run the map says UNAVAILABLE rather than showing an empty frame', () => {
    const v = el(askMeridianView([]))
    const map = v.querySelector('[data-canonical-map]') as HTMLElement
    expect(map.dataset.canonicalMap).toBe('unavailable')
    expect(map.textContent).toContain('UNAVAILABLE')
    expect(v.querySelector('.askc__map')).toBeNull()
  })

  it('9b · an unreachable engine renders a visible UNAVAILABLE notice, not silence', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: 'Answer UNAVAILABLE — the engine could not be reached.' }]))
    expect(v.textContent).toContain('UNAVAILABLE')
    expect(v.querySelector('.askmsg--unavailable')).not.toBeNull()
  })

  it('10 · a person decision answer states NOT EXECUTED', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    const card = v.querySelector('[data-component="DecisionCard"]') as HTMLElement
    expect(card.querySelector('[data-execution-status]')?.getAttribute('data-execution-status'))
      .toBe('NOT_EXECUTED')
    expect(card.textContent).toContain('Not executed')
  })

  it('11 · population-group cards state they are group-level averages', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: reactionResponse() }]))
    const card = v.querySelector('[data-component="PopulationGroupCard"]') as HTMLElement
    expect(card.querySelector('[data-status="GROUP_LEVEL_MODEL"]')?.textContent)
      .toContain('GROUP-LEVEL MODEL')
    expect(card.textContent).toContain(
      'MERIDIAN knows the group average, not how every person inside the group')
  })

  /*
   * The absence statement is one of the most important honesty properties in the product. It was
   * previously the faintest and smallest text on the screen; these tests pin the corrected weight
   * so it cannot quietly regress to metadata.
   */
  it('11a · every group row states the individual breakdown is unavailable, readably', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: reactionResponse() }]))
    const rows = [...v.querySelectorAll('.askc__grow')]
    expect(rows.length).toBeGreaterThan(0)
    for (const r of rows) {
      const abs = r.querySelector('.askc__gabs') as HTMLElement
      expect(abs.textContent?.trim()).toBe('Individual breakdown unavailable')
      expect(abs.dataset.availability).toBe('UNAVAILABLE')
      // it must not be styled as the faintest metadata on the card
      expect(abs.className).not.toContain('askc__abs')
    }
  })

  it('11b · an unavailable breakdown is never rendered as zero or as a distribution', () => {
    const v = askMeridianView([{ role: 'meridian', text: '', response: reactionResponse() }])
    expect(v).not.toContain('breakdown 0')
    expect(v).not.toContain('0%')
    expect(v).toContain('Individual breakdown unavailable')
  })

  it('11c · no bare question-mark marker sits beside a heading', () => {
    const responses = [decisionResponse(), reactionResponse(), unsupportedResponse()]
    const views = [askMeridianView([]), askHome(),
      ...responses.map((r) => askMeridianView([{ role: 'meridian', text: '', response: r }]))]
    for (const html of views) {
      const d = el(html)
      for (const h of d.querySelectorAll('.askc__t')) {
        expect(h.textContent?.trim().endsWith('?')).toBe(false)
        expect(h.querySelector('.m--u')).toBeNull()
      }
    }
  })

  /*
   * STATUS-PILL MAPPING · explicit and exhaustive.
   *
   * The mapping has no catch-all. An unrecognised shape renders a visible STATUS UNDECLARED pill
   * and reports itself, because labelling an UNKNOWN — or any component shape added later — as
   * UNAVAILABLE would misstate what MERIDIAN actually has.
   */
  describe('status-pill mapping', () => {
    const card = (title: string, body: Record<string, unknown>): AskResponse => ({
      ...decisionResponse(),
      components: [{ component_type: 'ModelBoundaryCard', title, body }],
    })
    const pillOf = (r: AskResponse): HTMLElement =>
      el(askMeridianView([{ role: 'meridian', text: '', response: r }]))
        .querySelector('[data-component="ModelBoundaryCard"] .pill') as HTMLElement

    it('11f · a model-boundary card renders NOT MODELLED', () => {
      const p = pillOf(card('What MERIDIAN does not model', { not_modelled: ['intelligence'] }))
      expect(p.dataset.status).toBe('NOT_MODELLED')
      expect(p.textContent).toContain('NOT MODELLED')
      expect(p.dataset.declared).toBe('true')
      // and the classifier agrees, independent of the render
      expect(classifyBoundaryStatus({ not_modelled: ['intelligence'] }))
        .toEqual({ status: 'NOT MODELLED', declared: true })
    })

    it('11g · an unavailable-data card renders UNAVAILABLE', () => {
      const body = { population_group_breakdown: 'UNAVAILABLE', cohort_confidence: 'NOT_MODELLED' }
      const p = pillOf(card('Unavailable data', body))
      expect(p.dataset.status).toBe('UNAVAILABLE')
      expect(p.dataset.declared).toBe('true')
      expect(classifyBoundaryStatus(body)).toEqual({ status: 'UNAVAILABLE', declared: true })
    })

    it('11h · explicitly unknown content renders UNKNOWN, not UNAVAILABLE', () => {
      const body = { provenance: 'UNKNOWN', cohort_confidence: 'NOT_MODELLED' }
      expect(classifyBoundaryStatus(body)).toEqual({ status: 'UNKNOWN', declared: true })
      expect(pillOf(card('Unknown provenance', body)).dataset.status).toBe('UNKNOWN')
    })

    it('11i · an unexpected shape cannot silently render UNAVAILABLE', () => {
      const shapes: Array<Record<string, unknown>> = [
        {},                                   // empty
        { note: 'some future prose' },        // unrecognised string
        { not_modelled: [] },                 // declared key, but nothing declared in it
        { not_modelled: 'intelligence' },     // wrong type
        { count: 0 },                         // zero is not an absence declaration
        { value: '' },                        // empty string is not an absence declaration
        { value: null },                      // null is not an absence declaration
        { value: false },                     // false is not an absence declaration
        { value: 'unavailable' },             // lower case is not the declared token
      ]
      const spy = vi.spyOn(console, 'error').mockImplementation(() => {})
      for (const body of shapes) {
        const c = classifyBoundaryStatus(body)
        expect(c.declared).toBe(false)
        expect(c.status).toBe(UNDECLARED_STATUS)
        const p = pillOf(card('Something new', body))
        expect(p.dataset.status).not.toBe('UNAVAILABLE')
        expect(p.dataset.declared).toBe('false')
        expect(p.textContent).toContain(UNDECLARED_STATUS)
      }
      // The development signal fires for every unrecognised shape. Twice per shape, because the
      // view renders the same component in the thread and again in the context panel.
      expect(spy).toHaveBeenCalledTimes(shapes.length * 2)
      for (const [message] of spy.mock.calls) {
        expect(String(message)).toContain('undeclared boundary component shape')
      }
      spy.mockRestore()
    })

    it('11j · every declared token maps to a distinct status', () => {
      expect(ABSENCE_TOKENS).toEqual(['UNKNOWN', 'UNAVAILABLE', 'NOT_MODELLED'])
      expect(classifyBoundaryStatus({ a: 'UNKNOWN' }).status).toBe('UNKNOWN')
      expect(classifyBoundaryStatus({ a: 'UNAVAILABLE' }).status).toBe('UNAVAILABLE')
      expect(classifyBoundaryStatus({ a: 'NOT_MODELLED' }).status).toBe('NOT MODELLED')
    })
  })

  it('11d · boundary status is a word, with screen-reader text, not colour alone', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    const pill = v.querySelector('[data-component="ModelBoundaryCard"] .pill') as HTMLElement
    expect(pill.textContent).toContain('Status: ')
    expect(pill.textContent).toContain('NOT MODELLED')
    expect(pill.dataset.status).toBe('NOT_MODELLED')
  })

  it('11e · a boundary card with no declared list is labelled UNAVAILABLE', () => {
    const r: AskResponse = {
      ...decisionResponse(),
      components: [{
        component_type: 'ModelBoundaryCard',
        title: 'Unavailable data',
        body: { 'population group breakdown': 'UNAVAILABLE', 'cohort confidence': 'NOT_MODELLED' },
      }],
    }
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: r }]))
    const pill = v.querySelector('[data-component="ModelBoundaryCard"] .pill') as HTMLElement
    expect(pill.dataset.status).toBe('UNAVAILABLE')
    expect(pill.textContent).toContain('UNAVAILABLE')
  })

  it('12 · the model-boundary card remains visible', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    const b = v.querySelector('[data-component="ModelBoundaryCard"]') as HTMLElement
    expect(b.textContent).toContain('intelligence')
    expect(b.textContent).toContain('competence')
  })

  it('13 · an unsupported question shows the supported alternatives', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: unsupportedResponse() }]))
    expect(v.querySelector('[data-component="UnsupportedQuestionCard"]')).not.toBeNull()
    const chips = [...v.querySelectorAll('.askchip')].map((c) => c.textContent?.trim())
    for (const s of STARTERS) expect(chips).toContain(s)
  })
})

describe('session, safety and accessibility', () => {
  it('14 · a reset control exists and clears display history only', () => {
    const v = el(askMeridianView([{ role: 'user', text: 'hello' }]))
    expect(v.querySelector('[data-ask-reset]')).not.toBeNull()
    // an empty message list renders the home state — nothing persisted
    expect(el(askMeridianView([])).querySelector('.askhome')).not.toBeNull()
  })

  it('15 · session messages call no mutation route', () => {
    const v = askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }])
    for (const bad of ['/runs/', '/decision', 'method="post"', 'DELETE', 'PATCH']) {
      expect(v).not.toContain(bad)
    }
    expect(ASK_ENDPOINT).toContain('/ask-meridian/query')
  })

  it('16 · no cabinet or person dialogue is presented as implemented', () => {
    const v = askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]).toLowerCase()
    for (const t of ['cabinet', 'minister says', 'commander', 'speaking as']) {
      expect(v).not.toContain(t)
    }
  })

  it('17 · starters and evidence controls are keyboard-reachable buttons', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    for (const sel of ['.askchip', '.askev__b']) {
      for (const b of v.querySelectorAll(sel)) {
        expect(b.tagName).toBe('BUTTON')
        expect(b.getAttribute('type')).toBe('button')
      }
    }
    const home = el(askHome())
    for (const b of home.querySelectorAll('.askstart')) expect(b.tagName).toBe('BUTTON')
  })

  it('18 · status meaning is written as text, not carried by colour alone', () => {
    const v = el(askMeridianView([{ role: 'meridian', text: '', response: decisionResponse() }]))
    expect(v.textContent).toContain('READ ONLY')
    expect(v.textContent).toContain('Not executed')
    // limitations are rendered as readable text
    expect(v.querySelector('.asklim')?.textContent).toContain('packaged snapshot')
  })

  it('19 · regions and live areas are labelled for screen readers', () => {
    const v = el(askMeridianView([]))
    expect(v.querySelector('[role="log"]')?.getAttribute('aria-label')).toBeTruthy()
    expect(v.querySelector('aside')?.getAttribute('aria-label')).toBe('Current context')
    expect(v.querySelector('label[for="ask-input"]')).not.toBeNull()
  })
})
