/**
 * API routing regression tests.
 *
 * These exist because of a defect every other test missed. Ask MERIDIAN used a bare relative path
 * (`/api/ask-meridian/query`) while the Briefing used an absolute one. In vitest that difference is
 * invisible — `fetch` is stubbed and nobody compares the two URLs — so 106 tests passed while the
 * real browser posted every question to the Vite dev server and got a 404 HTML page back.
 *
 * The lesson encoded here: assert the URL that is actually requested, and assert that the two
 * screens agree about it. A test that only checks a constant equals itself would not have caught it.
 */

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { mount } from '../src/main.ts'
import { initialSnapshot, runDemonstration, RUN_ENDPOINT } from '../src/engine/client.ts'
import { API_BASE, DEFAULT_API_BASE, apiUrl } from '../src/engine/api.ts'
import { ASK_ENDPOINT, STARTERS } from '../src/screens/ask-meridian.ts'
import type { AskResponse } from '../src/screens/ask-meridian.ts'

let root: HTMLElement

beforeEach(() => {
  root = document.createElement('div')
  root.id = 'app'
  document.body.innerHTML = ''
  document.body.appendChild(root)
  // The Ask thread is module-level state in `main.ts`. Clear it through the real reset control, so
  // one test's messages cannot be mistaken for another test's answer.
  mount(root, initialSnapshot(), 'ask')
  root.querySelector<HTMLElement>('[data-ask-reset]')?.click()
})

afterEach(() => {
  vi.unstubAllGlobals()
})

/**
 * A catalogue answer with the field names the BACKEND actually returns, checked against a live
 * response from `POST /api/ask-meridian/query`. An invented shape would let a routing test pass
 * against a response the real screen cannot render.
 */
function answer(): AskResponse {
  return {
    response_id: 'ask-brief_current_situation-scenario',
    matched_intent: 'BRIEF_CURRENT_SITUATION',
    normalized_question: 'brief me on the current situation',
    mode: 'EXPLORE',
    read_only: true,
    supported: true,
    short_answer: 'The Kestral Strait remains blocked.',
    components: [],
    evidence: [],
    limitations: ['This is a packaged snapshot, not live run state.'],
    suggested_follow_ups: [],
    supported_questions: [],
    execution_status: 'NOT_EXECUTED',
    run_integration: { execution_status: 'NOT_EXECUTED' },
  }
}

/** Open Ask MERIDIAN the way a user does, then click the first starter. */
async function clickFirstStarter(): Promise<void> {
  mount(root, initialSnapshot())
  const askNav = [...root.querySelectorAll<HTMLElement>('.navbtn')].find(
    (b) => b.textContent?.includes('Ask MERIDIAN'),
  )
  expect(askNav, 'Ask MERIDIAN must be reachable from the Briefing').toBeTruthy()
  askNav?.click()
  const starter = root.querySelector<HTMLElement>('.askstart')
  expect(starter, 'a starter question must be present').toBeTruthy()
  starter?.click()
  // Let the fetch promise and the two re-mounts settle.
  await new Promise((r) => setTimeout(r, 0))
  await new Promise((r) => setTimeout(r, 0))
}

describe('shared API base', () => {
  it('R1 · Ask and the Briefing resolve through the same backend base', () => {
    const askOrigin = new URL(ASK_ENDPOINT).origin
    const runOrigin = new URL(RUN_ENDPOINT).origin
    expect(askOrigin).toBe(runOrigin)
    expect(askOrigin).toBe(new URL(API_BASE).origin)
  })

  it('R2 · both endpoints are absolute, so neither can resolve against the dev server', () => {
    // The exact shape of the original defect: a path-relative URL inherits the page origin.
    for (const url of [ASK_ENDPOINT, RUN_ENDPOINT]) {
      expect(url.startsWith('/'), `${url} must not be page-relative`).toBe(false)
      expect(() => new URL(url)).not.toThrow()
    }
  })

  it('R3 · the base is declared in one place and defaults to the local backend', () => {
    expect(API_BASE).toBe(DEFAULT_API_BASE)
    expect(apiUrl('/api/x')).toBe(`${DEFAULT_API_BASE}/api/x`)
    // A path without a leading slash must not silently produce a different host.
    expect(new URL(apiUrl('api/x')).origin).toBe(new URL(DEFAULT_API_BASE).origin)
  })

  it('R4 · a starter question is POSTed to the backend, not to the page origin', async () => {
    // Typed parameters so the recorded URL is inspectable rather than an untyped tuple.
    const fetchSpy = vi.fn(async (_input: RequestInfo | URL, _init?: RequestInit) =>
      new Response(JSON.stringify(answer()), { status: 200, headers: { 'content-type': 'application/json' } }),
    )
    vi.stubGlobal('fetch', fetchSpy)
    await clickFirstStarter()

    expect(fetchSpy).toHaveBeenCalled()
    const requested = String(fetchSpy.mock.calls[0]?.[0])
    expect(requested).toBe(ASK_ENDPOINT)
    expect(new URL(requested).origin).toBe(new URL(API_BASE).origin)
    // window.location.origin under jsdom is NOT the backend — this is the assertion that fails
    // if anyone reintroduces a relative path.
    expect(new URL(requested).origin).not.toBe(window.location.origin)
  })

  it('R5 · the backend answer is what the screen renders', async () => {
    vi.stubGlobal('fetch', async () =>
      new Response(JSON.stringify(answer()), { status: 200, headers: { 'content-type': 'application/json' } }),
    )
    await clickFirstStarter()
    expect(root.textContent).toContain('The Kestral Strait remains blocked.')
    expect(root.textContent).not.toContain('UNAVAILABLE')
  })
})

describe('a failed request is never rendered as an answer', () => {
  it('R6 · a 404 from the dev server shows UNAVAILABLE, not a MERIDIAN reply', async () => {
    // Exactly what the browser used to receive: Vite's HTML 404 page.
    vi.stubGlobal('fetch', async () =>
      new Response('<!doctype html><title>404</title>', {
        status: 404,
        headers: { 'content-type': 'text/html' },
      }),
    )
    await clickFirstStarter()
    expect(root.textContent).toContain('UNAVAILABLE')
    expect(root.textContent).toContain('404')
    expect(root.textContent).not.toContain('doctype')
  })

  it('R7 · a 200 that is not a catalogue answer is still UNAVAILABLE', async () => {
    // A dev server can return 200 with an HTML shell. A body without a matched intent is not an
    // answer, whatever the status line said.
    vi.stubGlobal('fetch', async () =>
      new Response(JSON.stringify({ detail: 'not found' }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    )
    await clickFirstStarter()
    expect(root.textContent).toContain('UNAVAILABLE')
    expect(root.textContent).not.toContain('not found')
  })

  it('R7a · a declined question is an ANSWER, not a transport failure', async () => {
    // The backend returns HTTP 200, `supported: false` and `matched_intent: null` for a question
    // outside the catalogue. That is a real answer. An earlier version of the guard above keyed on
    // `matched_intent` and turned every declined question into "the engine could not be reached" —
    // replacing an honest refusal with a false claim about the transport.
    vi.stubGlobal('fetch', async () =>
      new Response(
        JSON.stringify({
          ...answer(),
          matched_intent: null,
          supported: false,
          short_answer: 'I cannot answer that question in this version.',
          supported_questions: [...STARTERS],
        }),
        { status: 200, headers: { 'content-type': 'application/json' } },
      ),
    )
    await clickFirstStarter()
    const last = root.querySelector('.askmsg--m:last-of-type') as HTMLElement
    expect(root.textContent).toContain('I cannot answer that question in this version.')
    expect(root.textContent).not.toContain('could not be reached')
    expect(last?.classList.contains('askmsg--unavailable')).toBe(false)
    // Bounded: it says what it CAN answer instead.
    expect(root.querySelectorAll('.askchip').length).toBeGreaterThan(0)
  })

  it('R8 · an actual backend failure produces the visible UNAVAILABLE state', async () => {
    vi.stubGlobal('fetch', async () => {
      throw new TypeError('Failed to fetch')
    })
    await clickFirstStarter()
    const visible = root.textContent ?? ''
    expect(visible).toContain('Answer UNAVAILABLE')
    expect(visible).toContain('Nothing has been assumed in its place.')
    // The user's question stays on screen; only the answer is absent.
    expect(visible).toContain(STARTERS[0] as string)
  })

  it('R9 · a Briefing run failure marks the connection unavailable rather than faking a live run', async () => {
    vi.stubGlobal('fetch', async () => {
      throw new TypeError('Failed to fetch')
    })
    const result = await runDemonstration()
    expect(result.connection).toBe('unavailable')
    expect(result.error).toBeTruthy()
  })
})
