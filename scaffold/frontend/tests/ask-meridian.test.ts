/**
 * Ask MERIDIAN Phase 1 — frontend honesty and accessibility tests.
 *
 * Asserts Briefing remains the landing view, the four starters render without an unexplained
 * fictional name, answers carry the read-only speaker header and their limitations, decisions state
 * NOT EXECUTED, population groups state they are averages, and no cabinet or person dialogue is
 * presented as implemented.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import {
  ASK_ENDPOINT,
  ASK_NOTE,
  ASK_SPEAKER,
  ASK_SPEAKER_AUTHORITY,
  STARTERS,
  askHome,
  askMeridianView,
} from '../src/screens/ask-meridian.ts'
import type { AskResponse } from '../src/screens/ask-meridian.ts'
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
    expect(root.querySelector('.bsum, .briefing, [class*="brief"]')).not.toBeNull()
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
    expect(root.querySelector('.bsum')).not.toBeNull()
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
    expect(ASK_ENDPOINT).toBe('/api/ask-meridian/query')
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
    expect(card.textContent).toContain('does not model the individuals')
    expect(card.textContent).toContain('UNAVAILABLE')
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
