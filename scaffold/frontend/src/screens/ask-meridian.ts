/**
 * Ask MERIDIAN — Phase 1.
 *
 * DETERMINISTIC AND READ-ONLY. Every answer comes from the backend's declared catalogue, which is
 * matched without a language model. This screen renders that response; it invents nothing, and it
 * calls no mutating route.
 *
 * NOT AUTHORITY. Displayed messages are navigation context only. They do not alter the person,
 * beliefs, decisions or the run, and they are not persisted as memory — a refresh clears them,
 * because they were never state.
 *
 * BRIEFING REMAINS THE LANDING SCREEN. Ask MERIDIAN is a prominent navigation item, not the default.
 */

import { escapeHtml } from '../components/epistemic.ts'
import { briefingMap } from '../components/briefing-viz.ts'
import { mapCallouts } from '../engine/presentation.ts'
import type { RunResult } from '../engine/client.ts'

export const ASK_SPEAKER = 'ASK MERIDIAN'
export const ASK_SPEAKER_AUTHORITY = 'Engine-grounded explanation · Read only'
export const ASK_ENDPOINT = '/api/ask-meridian/query'

/** The four starters shown on the home screen. No unexplained fictional name appears here. */
export const STARTERS: readonly string[] = [
  'Brief me on the current situation.',
  'How are the economy and supply chains reacting?',
  'How are people and groups reacting?',
  'What does MERIDIAN know — and what remains uncertain?',
]

export const ASK_NOTE =
  'Ask in your own words. This version can explain the current fictional scenario but cannot change it.'

export interface AskComponent {
  component_type: string
  title: string
  body: Record<string, unknown>
}
export interface AskEvidence { label: string; destination: string; kind: string }
export interface AskResponse {
  response_id: string
  matched_intent: string | null
  normalized_question: string
  mode: string
  read_only: boolean
  supported: boolean
  short_answer: string
  components: AskComponent[]
  evidence: AskEvidence[]
  limitations: string[]
  suggested_follow_ups: string[]
  supported_questions: string[]
  execution_status: string
  run_integration: Record<string, unknown>
}
export interface AskMessage { role: 'user' | 'meridian'; text: string; response?: AskResponse }

/**
 * Canonical map. The SAME `briefingMap` the Briefing renders, at a smaller displayed size — never a
 * simplified redraw, and never an empty placeholder box. A weaker miniature imitation of a good
 * existing component is not an acceptable substitute for resizing the real one.
 *
 * Without a run there is no engine state to draw, so the card says so rather than showing an empty
 * frame that a reader could mistake for a map with nothing on it.
 */
function canonicalMapCard(run?: RunResult): string {
  if (!run) {
    return `<figure class="askc askc--map" data-component="CanonicalMapCard">
      <figcaption class="askc__t">Kestral Strait
        <span class="pill pill--boundary" data-status="UNAVAILABLE">
          <span class="visually-hidden">Status: </span>UNAVAILABLE</span></figcaption>
      <p class="askc__abs" data-canonical-map="unavailable">Map UNAVAILABLE — no run state is loaded.</p>
    </figure>`
  }
  const days = Math.max(1, Math.round(run.projection.simulated_hours / 24))
  return `<figure class="askc askc--map" data-component="CanonicalMapCard">
    <figcaption class="askc__t">Kestral Strait <span class="m m--e" title="engine result">E</span></figcaption>
    <div class="askc__map" data-canonical-map="briefing-canonical-map"
         aria-label="Fictional map of the Kestral Strait, the same component the Briefing View uses.">
      ${briefingMap(run, mapCallouts(run), days)}
    </div>
  </figure>`
}

/**
 * Boundary card.
 *
 * The status is a WORD, not a symbol. A bare "?" beside a heading reads as stray punctuation or an
 * unfinished sentence, and a symbol alone cannot carry the distinction between "we chose not to
 * model this" and "we have no value for it". The pill states which, in text, and never relies on
 * colour to do so.
 */
function boundaryCard(c: AskComponent): string {
  const items = (c.body.not_modelled as string[] | undefined) ?? []
  const extras = Object.entries(c.body).filter(([k]) => k !== 'not_modelled')
  // A declared not-modelled list is a modelling boundary; anything else here is a missing value.
  const status = items.length ? 'NOT MODELLED' : 'UNAVAILABLE'
  return `<section class="askc askc--boundary" data-component="ModelBoundaryCard">
    <h4 class="askc__t">${escapeHtml(c.title)}
      <span class="pill pill--boundary" data-status="${status.replace(' ', '_')}">
        <span class="visually-hidden">Status: </span>${status}</span></h4>
    ${items.length ? `<ul class="askc__tags">${items.map((i) => `<li>${escapeHtml(i)}</li>`).join('')}</ul>` : ''}
    ${extras.length ? `<dl class="askc__kv">${extras
      .map(([k, v]) => `<dt>${escapeHtml(k.replace(/_/g, ' '))}</dt><dd>${escapeHtml(String(v))}</dd>`)
      .join('')}</dl>` : ''}
  </section>`
}

/**
 * Population-group card.
 *
 * The absence statement is one of the most important honesty properties in the product, so it is
 * NOT metadata. "breakdown UNAVAILABLE" was previously the faintest text on the screen, at the
 * smallest size — the opposite of the weight it deserves. It now reads as a legible status line
 * with the reason stated in full.
 *
 * It says the breakdown is unavailable. It does not say it is zero, and it does not invent a
 * distribution to fill the gap.
 */
function groupCard(c: AskComponent): string {
  const groups = (c.body.groups as Array<Record<string, string>> | undefined) ?? []
  return `<section class="askc askc--group" data-component="PopulationGroupCard">
    <h4 class="askc__t">${escapeHtml(c.title)}
      <span class="pill pill--group" data-status="GROUP_LEVEL_MODEL">
        <span class="visually-hidden">Status: </span>GROUP-LEVEL MODEL</span></h4>
    <p class="askc__note">MERIDIAN knows the group average, not how every person inside the group
      differs.</p>
    <ul class="askc__rows">${groups
      .map((g) => `<li class="askc__grow">
        <span class="askc__gname">${escapeHtml(String(g.name))}</span>
        <span class="askc__gres">${escapeHtml(String(g.result))}</span>
        <span class="askc__gabs" data-availability="${escapeHtml(String(g.breakdown ?? 'UNAVAILABLE'))}">
          Individual breakdown unavailable</span></li>`)
      .join('')}</ul>
  </section>`
}

function decisionCard(c: AskComponent): string {
  const b = c.body as Record<string, unknown>
  const blocked = (b.unavailable_options as string[] | undefined) ?? []
  return `<section class="askc askc--decision" data-component="DecisionCard">
    <h4 class="askc__t">${escapeHtml(c.title)} <span class="m m--e" title="engine result">E</span></h4>
    <p class="askc__sel">${escapeHtml(String(b.selected_action_label ?? '—'))}</p>
    <p class="askc__exec" data-execution-status="${escapeHtml(String(b.execution_status ?? 'NOT_EXECUTED'))}">
      ${escapeHtml(String(b.default_statement ?? 'Selected by the declared rule. Not executed.'))}</p>
    ${blocked.length ? `<p class="askc__blocked">Unavailable: ${blocked.map(escapeHtml).join(', ')}</p>` : ''}
  </section>`
}

function rowsCard(c: AskComponent, key: string, kind: string): string {
  const rows = (c.body[key] as Array<Record<string, string>> | undefined) ?? []
  return `<section class="askc" data-component="${escapeHtml(kind)}">
    <h4 class="askc__t">${escapeHtml(c.title)}</h4>
    <ul class="askc__rows">${rows
      .map((r) => `<li><span>${escapeHtml(String(r.name ?? r.label ?? ''))}</span>
        <span>${escapeHtml(String(r.result ?? r.position ?? ''))}</span></li>`)
      .join('')}</ul>
  </section>`
}

function genericCard(c: AskComponent): string {
  return `<section class="askc" data-component="${escapeHtml(c.component_type)}">
    <h4 class="askc__t">${escapeHtml(c.title)}</h4>
    <dl class="askc__kv">${Object.entries(c.body)
      .map(([k, v]) => `<dt>${escapeHtml(k.replace(/_/g, ' '))}</dt><dd>${escapeHtml(
        typeof v === 'object' ? JSON.stringify(v) : String(v))}</dd>`)
      .join('')}</dl>
  </section>`
}

function component(c: AskComponent, run?: RunResult): string {
  switch (c.component_type) {
    case 'CanonicalMapCard': return canonicalMapCard(run)
    case 'ModelBoundaryCard': return boundaryCard(c)
    case 'PopulationGroupCard': return groupCard(c)
    case 'DecisionCard': return decisionCard(c)
    case 'PersonSummaryCard': return rowsCard(c, 'people', 'PersonSummaryCard')
    case 'OrganisationPositionCard': return rowsCard(c, 'organisations', 'OrganisationPositionCard')
    default: return genericCard(c)
  }
}

function answer(r: AskResponse, run?: RunResult): string {
  const chips = r.supported ? r.suggested_follow_ups : r.supported_questions
  return `<article class="askmsg askmsg--m" data-supported="${r.supported}">
    <header class="askmsg__who">
      <span class="askmsg__av" aria-hidden="true">M</span>
      <span class="askmsg__nm">${escapeHtml(ASK_SPEAKER)}</span>
      <span class="askmsg__auth">${escapeHtml(ASK_SPEAKER_AUTHORITY)}</span>
      <span class="askmsg__ro">READ ONLY</span>
    </header>
    <p class="askmsg__text">${escapeHtml(r.short_answer)}</p>
    ${r.components.map((c) => component(c, run)).join('')}
    ${r.evidence.length ? `<nav class="askev" aria-label="Evidence">
      ${r.evidence.map((e) => `<button type="button" class="askev__b" data-destination="${escapeHtml(e.destination)}"
        data-kind="${escapeHtml(e.kind)}">${escapeHtml(e.label)}</button>`).join('')}</nav>` : ''}
    ${r.limitations.length ? `<ul class="asklim" aria-label="Limitations">
      ${r.limitations.map((l) => `<li>${escapeHtml(l)}</li>`).join('')}</ul>` : ''}
    ${chips.length ? `<nav class="askchips" aria-label="${r.supported ? 'Suggested follow-up questions' : 'Supported questions'}">
      ${chips.map((q) => `<button type="button" class="askchip" data-question="${escapeHtml(q)}">${escapeHtml(q)}</button>`).join('')}</nav>` : ''}
  </article>`
}

/** The home state: heading, note, four starters. Never an unexplained fictional name. */
export function askHome(): string {
  return `<div class="askhome">
    <h1 class="askhome__h">What would you like to know?</h1>
    <p class="askhome__note">${escapeHtml(ASK_NOTE)}</p>
    <h2 class="askhome__lbl">AVAILABLE NOW</h2>
    <div class="askhome__grid">${STARTERS.map(
      (q) => `<button type="button" class="askstart" data-question="${escapeHtml(q)}">${escapeHtml(q)}</button>`,
    ).join('')}</div>
  </div>`
}

/**
 * The whole screen. `messages` are display-only session context, never authority.
 *
 * `run` is the SAME engine run the Briefing renders, passed in so the context panel can draw the
 * real canonical map rather than a placeholder. It is optional only so the screen degrades honestly
 * before a run has loaded.
 */
export function askMeridianView(messages: AskMessage[] = [], run?: RunResult): string {
  const latest = [...messages].reverse().find((m) => m.response)?.response
  return `<section class="ask" aria-label="Ask MERIDIAN">
    <div class="ask__main">
      <div class="ask__thread" role="log" aria-live="polite" aria-label="Conversation">
        ${messages.length === 0 ? askHome() : messages.map((m) =>
          m.role === 'user'
            ? `<p class="askmsg askmsg--u"><span class="visually-hidden">You asked: </span>${escapeHtml(m.text)}</p>`
            : m.response
              ? answer(m.response, run)
              // A MERIDIAN message without a response is a failure notice, not an answer. It must
              // still be shown — silently rendering nothing would read as "no answer exists".
              : `<article class="askmsg askmsg--m askmsg--unavailable" data-supported="false">
                  <header class="askmsg__who">
                    <span class="askmsg__av" aria-hidden="true">M</span>
                    <span class="askmsg__nm">${escapeHtml(ASK_SPEAKER)}</span>
                    <span class="askmsg__ro">READ ONLY</span>
                  </header>
                  <p class="askmsg__text">${escapeHtml(m.text)}</p>
                </article>`,
        ).join('')}
      </div>
      <form class="askform" data-ask-form>
        <label class="visually-hidden" for="ask-input">Ask a question</label>
        <input id="ask-input" class="askform__in" type="text" autocomplete="off"
               placeholder="Ask anything…" data-ask-input>
        <button type="submit" class="askform__send">SEND</button>
        <button type="button" class="askform__reset" data-ask-reset>Clear</button>
      </form>
    </div>
    <aside class="ask__ctx" aria-label="Current context">
      <h2 class="ask__ctxh">CURRENT CONTEXT</h2>
      ${latest && latest.components.length
        ? latest.components.slice(0, 2).map((c) => component(c, run)).join('')
        : canonicalMapCard(run)}
      <p class="ask__ctxnote">This panel follows the answer. Session messages are display context
        only — they are not saved and do not change the simulation.</p>
    </aside>
  </section>`
}
