/**
 * MERIDIAN — application shell.
 *
 * MIXED-ORIGIN SCREEN. The Strategic Command Centre now shows genuine P0.5 engine output beside
 * hand-authored fixture content. That changes what the global disclosure must say: the old
 * "FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE" would now be FALSE, because part of the
 * screen genuinely is connected. It is replaced with a mixed-origin disclosure, and every record
 * carries its own compact origin marker (E / F / U / N/A).
 *
 * The stronger fixture-only wording is retained for screens that remain entirely fixture-backed.
 */

import './tokens.css'
import './styles.css'
import './briefing.css'

import { initialSnapshot, runDemonstration } from './engine/client.ts'
import type { RunResult } from './engine/client.ts'
import { escapeHtml } from './components/epistemic.ts'

import { technicalTable, wireTechnicalTable } from './screens/technical-table.ts'
import { ASK_ENDPOINT, askMeridianView } from './screens/ask-meridian.ts'
import type { AskMessage, AskResponse } from './screens/ask-meridian.ts'

/**
 * Depth mode. Briefing is the DEFAULT; Analysis holds the detailed dashboard.
 *
 * These are depth modes, not product-navigation destinations - Analysis is not a sibling of
 * Society Pulse or Entity Dossiers, it is the same screen with more of itself shown. The switch is
 * VISIBLE rather than a keyboard shortcut, because a first-time user will not discover a shortcut
 * (usability rule 1).
 */
/**
 * ASK IS THE LANDING SCREEN, and the Briefing is its first answer.
 *
 * This reverses the earlier "Briefing remains the landing screen" rule, on the founder's decision.
 * The reason is measured, not stylistic: the Briefing screen was 2.9 screenfuls in which the one
 * decision waiting began below the fold, while the conversation was the only surface anyone could
 * read at a glance. The doctrine it restores is the project's own — chat is the doorway, visuals
 * are the evidence, the deterministic engine is the authority.
 *
 * There is no longer a 'briefing' mode. There are two destinations: the conversation, and the
 * technical evidence beneath it.
 */
export type Mode = 'ask' | 'analysis'
let currentMode: Mode = 'ask'

/**
 * Ask MERIDIAN session messages. Display context only — deliberately a module-level variable and
 * NOT persisted anywhere, so a reload clears them. They were never state.
 */
let askMessages: AskMessage[] = [{ role: 'meridian', text: '', kind: 'briefing' }]

/** The thread always opens with the Briefing. Clearing returns to it, never to an empty screen. */
function openingThread(): AskMessage[] {
  return [{ role: 'meridian', text: '', kind: 'briefing' }]
}

export const FICTION_DISCLOSURE = 'FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION'
export const MIXED_DISCLOSURE =
  'INTERACTIVE PROTOTYPE — MIXED ENGINE AND FIXTURE DATA — NOT A PREDICTIVE SYSTEM'


function disclosures(): string {
  return `<div class="disclosures" role="region" aria-label="Prototype disclosures">
    <span class="disc"><span class="disc__glyph" aria-hidden="true">◈</span>${FICTION_DISCLOSURE}</span>
    <span class="disc__sep" aria-hidden="true">│</span>
    <span class="disc disc--mixed">${MIXED_DISCLOSURE}</span>
  </div>`
}

function topbar(run: RunResult, mode: Mode = 'ask'): string {
  const p = run.projection
  const conn =
    run.connection === 'live'
      ? '<span class="tb__v tb__v--live">LIVE</span>'
      : `<span class="tb__v tb__v--stale">${run.connection === 'snapshot' ? 'SNAPSHOT' : 'UNAVAILABLE'}</span>`
  return `<div class="topbar" role="region" aria-label="Scenario and run status">
    <div class="topbar__left">
      <h1 class="scenario-title">Kestral Strait</h1>
      <span class="scenario-sub">Day ${Math.max(1, Math.round(p.simulated_hours / 24))} · fictional</span>
      ${modeSwitch(mode)}
    </div>
    <div class="topbar__right">
      ${
        /*
         * The engine chip and every identifier belong to the technical view. Observation 1: the
         * default screen opened with run status instead of the situation. Briefing shows neither.
         */
        mode === 'analysis'
          ? `<span class="tb"><span class="tb__k">engine</span>${conn}</span>
             <span class="tb"><span class="tb__k">rule pack</span><span class="tb__v">${escapeHtml(p.rule_pack_version)}</span></span>
             <span class="tb"><span class="tb__k">tick</span><span class="tb__v">Tick ${p.tick}</span></span>
             <span class="tb"><span class="tb__k">horizon</span><span class="tb__v">${p.demonstration_horizon_ticks} ticks · ${(p.simulated_hours / 24).toFixed(0)} days</span></span>`
          : ''
      }
    </div>
  </div>`
}

/**
 * Primary navigation.
 *
 * ANALYSIS IS NOT HERE. The first-user test recorded the Analysis card wall as unintelligible, so
 * it is no longer offered as one of two equal ways to read the situation. It remains reachable, as
 * "technical evidence", from the foot of the Briefing and from the Ask screen — a deliberate
 * secondary route rather than the normal user experience. Nothing under it was deleted.
 *
 * ASK MERIDIAN IS A BUTTON. Observation 10: it read as a logo. It now sits beside Briefing, in the
 * same shape and weight as its sibling, with an icon and a real label.
 */
/**
 * THERE IS NO PRIMARY NAVIGATION.
 *
 * "Exact numbers" used to sit here as one of two things the product offered. A first-time reader
 * cannot say why those values matter, what to look for, or what decision the table helps them
 * make — so offering it as half the product was a category error.
 *
 * The conversation is the product. Technical evidence is reached from a specific claim
 * ("Show evidence" on a row) or from inside an explanation ("Show the exact evidence"), which is
 * where it means something. The full table remains as a secondary audit route, not a destination.
 */
function modeSwitch(_mode: Mode): string {
  return ''
}

function shell(run: RunResult, mode: Mode): string {
  if (mode === 'ask') {
    return `${briefingDisclosure()}
    ${topbar(run, mode)}
    <main class="main main--ask" id="main" aria-label="Ask MERIDIAN">
      ${askMeridianView(askMessages, run)}
    </main>`
  }
  /*
   * TECHNICAL EVIDENCE. Formerly "Analysis", and formerly one of two equal reading modes. The
   * first-user test rejected it as a default experience, so it is now labelled for what it is and
   * is reached only deliberately. Its content is unchanged and nothing under it was deleted.
   */
  return `${disclosures()}
  ${topbar(run, mode)}
  <div class="techbar" role="region" aria-label="Technical evidence notice">
    <span class="techbar__t">Technical evidence — every exact value, with its identifier, origin and
      mechanism. Built to be looked up, not read.</span>
    <button type="button" class="techbar__back" data-mode="ask">Back to the briefing</button>
  </div>
  <main class="main main--tech" id="main" aria-label="Technical evidence">${technicalTable(run)}</main>`
}

/** Briefing keeps the disclosure, compactly. Simplification may not remove an honesty property. */
function briefingDisclosure(): string {
  return `<div class="disclosures disclosures--compact" role="region" aria-label="Prototype disclosures">
    <span class="disc"><span class="disc__glyph" aria-hidden="true">◈</span>${FICTION_DISCLOSURE}</span>
    <span class="disc__sep" aria-hidden="true">│</span>
    <span class="disc disc--mixed">${MIXED_DISCLOSURE}</span>
  </div>`
}

/**
 * Ask MERIDIAN interactions.
 *
 * READ ONLY. The single network call is a POST to the catalogue endpoint, which returns an
 * explanation and changes nothing; there is no other request from this screen. If the call fails,
 * the screen says the answer is UNAVAILABLE rather than inventing one — an absent answer is never
 * shown as an empty or neutral one.
 */
function wireAsk(root: HTMLElement, run: RunResult): void {
  const remount = (): void => mount(root, run, 'ask')

  async function ask(question: string): Promise<void> {
    const q = question.trim()
    if (!q) return
    askMessages = [...askMessages, { role: 'user', text: q }]
    remount()
    try {
      const res = await fetch(ASK_ENDPOINT, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ question: q }),
      })
      // A non-2xx is never an answer. A 404 in particular means the request did not reach the
      // engine at all — that must show as UNAVAILABLE, not as a MERIDIAN reply.
      if (!res.ok) throw new Error(`the engine returned HTTP ${res.status}`)
      const response = (await res.json()) as AskResponse
      // A body that is not catalogue-shaped is not an answer, whatever the status code was — a dev
      // server can return 200 with an HTML shell or a bare error object.
      //
      // The test is `supported` + `short_answer`, NOT `matched_intent`. A question the catalogue
      // declines to answer is a real, valid response with `matched_intent: null`, and treating it
      // as a transport failure would replace an honest "I cannot answer that" with a false claim
      // that the engine was unreachable.
      if (!response || typeof response.supported !== 'boolean' || typeof response.short_answer !== 'string') {
        throw new Error('the response was not a MERIDIAN answer')
      }
      askMessages = [...askMessages, { role: 'meridian', text: '', response }]
    } catch (e) {
      const why = e instanceof Error ? e.message : 'the engine could not be reached'
      askMessages = [
        ...askMessages,
        {
          role: 'meridian',
          text: `Answer UNAVAILABLE — ${why}. Nothing has been assumed in its place.`,
        },
      ]
    }
    remount()
  }

  root.querySelectorAll<HTMLElement>('.askstart, .askchip').forEach((b) => {
    b.addEventListener('click', () => void ask(b.dataset.question ?? ''))
  })
  root.querySelector<HTMLFormElement>('[data-ask-form]')?.addEventListener('submit', (e) => {
    e.preventDefault()
    const input = root.querySelector<HTMLInputElement>('[data-ask-input]')
    if (!input) return
    const q = input.value
    input.value = ''
    void ask(q)
  })
  root.querySelector<HTMLElement>('[data-ask-reset]')?.addEventListener('click', () => {
    // Back to the briefing, not to an empty screen. The briefing is the thread's floor.
    askMessages = openingThread()
    remount()
  })
  // R2 — evidence by ASKING. A row's "Explain this" sends a question the catalogue can answer,
  // replacing the per-section disclosure that used to print raw field names on a reading screen.
  root.querySelectorAll<HTMLElement>('[data-ask-question]').forEach((b) => {
    b.addEventListener('click', () => void ask(b.dataset.askQuestion ?? ''))
  })
  // The situation diagram is an ANSWER in the thread, not a panel bolted to a screen.
  root.querySelector<HTMLElement>('[data-show-diagram]')?.addEventListener('click', () => {
    askMessages = [...askMessages, { role: 'meridian', text: '', kind: 'diagram' }]
    remount()
  })
  // Evidence opens the read-only route the answer was derived from. GET only.
  root.querySelectorAll<HTMLElement>('.askev__b').forEach((b) => {
    b.addEventListener('click', () => {
      const d = b.dataset.destination
      if (d) window.open(d, '_blank', 'noopener')
    })
  })
}

/**
 * Send a question that originated outside the Ask screen (a technical-table row).
 *
 * The user message is appended by the caller before the mode switch, so the question is visible
 * immediately rather than appearing only once the answer resolves.
 */
async function askFromTable(root: HTMLElement, run: RunResult, question: string): Promise<void> {
  try {
    const res = await fetch(ASK_ENDPOINT, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ question }),
    })
    if (!res.ok) throw new Error(`the engine returned HTTP ${res.status}`)
    const response = (await res.json()) as AskResponse
    if (!response || typeof response.supported !== 'boolean' || typeof response.short_answer !== 'string') {
      throw new Error('the response was not a MERIDIAN answer')
    }
    askMessages = [...askMessages, { role: 'meridian', text: '', response }]
  } catch (e) {
    const why = e instanceof Error ? e.message : 'the engine could not be reached'
    askMessages = [...askMessages, {
      role: 'meridian',
      text: `Answer UNAVAILABLE — ${why}. Nothing has been assumed in its place.`,
    }]
  }
  mount(root, run, 'ask')
}

export function mount(root: HTMLElement, run: RunResult, mode: Mode = 'ask'): void {
  currentMode = mode
  // Releases the Analysis viewport lock on the reading screens — see #app in styles.css.
  root.dataset.mode = mode
  root.innerHTML = shell(run, mode)
  if (mode === 'analysis') {
    // Selecting a row returns to the conversation and asks. Evidence is a question, not a panel.
    wireTechnicalTable(root, (question) => {
      askMessages = [...askMessages, { role: 'user', text: question }]
      mount(root, run, 'ask')
      void askFromTable(root, run, question)
    })
  }
  if (mode === 'ask') {
    wireAsk(root, run)
    /*
     * SCROLL TO THE NEWEST MESSAGE.
     *
     * Without this a new answer lands below the fold and the control that produced it appears to
     * have done nothing — which is exactly how it looked when "Show how this fits together" was
     * first wired up. A conversation must always show what it just said.
     */
    const thread = root.querySelector<HTMLElement>('.ask__thread')
    if (thread) thread.scrollTop = thread.scrollHeight
  }

  // Depth switch, and the Briefing affordances that open Analysis at the relevant detail.
  root.querySelectorAll<HTMLElement>('[data-mode]').forEach((btn) => {
    btn.addEventListener('click', () => mount(root, run, btn.dataset.mode as Mode))
  })
}

const app = document.getElementById('app')
if (app) {
  // First paint from the bundled recorded snapshot so the layout is inspectable immediately,
  // then replace with a genuine live run. The status chip states which is showing.
  mount(app, initialSnapshot(), 'ask')
  void runDemonstration('incident', 20).then((run) => mount(app, run, currentMode))
}
