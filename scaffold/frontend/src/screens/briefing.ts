/**
 * Briefing — the landing screen, rebuilt after the first user usability test failed.
 *
 * See docs/design/FIRST-USER-USABILITY-TEST.md. The previous version was a command-centre wall: a
 * dominant map, a decision stack, three cards each carrying a badge and a trend strip, an origin
 * legend, and engine vocabulary throughout. A first-time user could not read it.
 *
 * This screen answers three questions in order, and nothing else:
 *
 *   1. What happened?          — one headline sentence
 *   2. Why does it matter?     — three short sentences, then People / Economy / Politics
 *   3. What needs attention?   — one decision, written as a question
 *
 * WHAT IS DELIBERATELY ABSENT from the default view: decimals, ticks, seeds, revisions, rule-pack
 * identifiers, raw action identifiers, provenance panels, trend graphs, origin badges on every
 * card, and the large map. None of that is deleted — all of it stays reachable through the
 * evidence controls and the technical route. It simply is not the first thing a reader meets.
 *
 * EVERY sentence still comes from `engine/presentation.ts`. Simplifying the words did not licence
 * authoring them: a readable sentence is still a claim, and a claim must be true of this run.
 */

import type { OptionEntry, RunResult } from '../engine/client.ts'
import {
  NOTHING_EXECUTES,
  crisisLede,
  plainDecision,
  plainSections,
  primaryDecision,
  situationModel,
  situationSummary,
} from '../engine/presentation.ts'
import type { PlainSection } from '../engine/presentation.ts'
import { escapeHtml } from '../components/epistemic.ts'
import { STARTERS } from './ask-meridian.ts'
import { situationDiagram } from '../components/briefing-viz.ts'

/**
 * The prototype's hardest limit, stated wherever a choice is shown.
 * Re-exported; the single definition lives in `engine/presentation.ts`, which the diagram also reads.
 */
export { NOTHING_EXECUTES }

/**
 * Direction, in one ordinary word plus a shape that does not depend on colour.
 * No trend graph: observation 3 recorded that the tiny graphs crowded the cards and explained
 * nothing. The exact series is still available through the evidence control.
 */
function directionLine(s: PlainSection): string {
  if (!s.direction || !s.directionSubject) return ''
  const arrow = s.direction === 'rising' ? '↑' : s.direction === 'falling' ? '↓' : '→'
  return `<p class="sec__dir sec__dir--${s.direction}">
    <span class="sec__arrow" aria-hidden="true">${arrow}</span>
    ${escapeHtml(s.directionSubject)} is <strong>${escapeHtml(s.direction)}</strong></p>`
}

/**
 * One of the three impact sections.
 *
 * The evidence control is a native <details>. Technical values live inside it and nowhere else on
 * this screen, so a reader who does not want them never sees them, and a reader who does is one
 * click away rather than one screen away.
 */
function section(s: PlainSection): string {
  return `<section class="sec sec--${s.id}" aria-labelledby="sec-${s.id}">
    <h3 class="sec__h" id="sec-${s.id}">${escapeHtml(s.title)}</h3>
    ${s.sentences.map((t) => `<p class="sec__p">${escapeHtml(t)}</p>`).join('')}
    ${directionLine(s)}
    ${s.caveat ? `<p class="sec__caveat">${escapeHtml(s.caveat)}</p>` : ''}
    <details class="ev">
      <summary class="ev__s">Show where this comes from</summary>
      <div class="ev__b">
        <p class="ev__note">These are the engine values behind the sentences above.
          ${s.origin === 'engine'
            ? 'They are produced by the simulation.'
            : s.origin === 'unavailable'
              ? 'The engine is unreachable, so these are from a recorded snapshot.'
              : 'They come from declared fixture input.'}</p>
        <ul class="ev__list">${s.sources.map((f) => `<li><code>${escapeHtml(f)}</code></li>`).join('')}</ul>
      </div>
    </details>
  </section>`
}

/**
 * The one decision, written as a question.
 *
 * Observation 8: "Publish Legal Advice" is an internal action label. The question, the explanation
 * and the two choices all come from `plainDecision`, which declares them per option rather than
 * deriving prose from an identifier. No consequence is stated, because the prototype computes none.
 */
function decision(o: OptionEntry): string {
  const d = plainDecision(o)
  return `<section class="dec" aria-labelledby="dec-h" data-option-id="${escapeHtml(d.optionId)}">
    <p class="dec__kicker">Needs a decision</p>
    <h2 class="dec__h" id="dec-h">${escapeHtml(d.question)}</h2>
    ${d.context.map((t) => `<p class="dec__p">${escapeHtml(t)}</p>`).join('')}
    <p class="dec__standing">${escapeHtml(d.standing)}</p>
    ${d.described
      ? `<div class="dec__choices" role="group" aria-label="Choices — display only">
           ${d.choices.map((c, i) => `<button type="button" class="choice ${i === 0 ? 'choice--a' : 'choice--b'}"
             data-choice="${escapeHtml(c)}">${escapeHtml(c)}</button>`).join('')}
         </div>`
      : ''}
    <p class="dec__note" data-nothing-executes>${escapeHtml(NOTHING_EXECUTES)}</p>
    <details class="ev">
      <summary class="ev__s">Show the calculation</summary>
      <div class="ev__b">
        <p class="ev__note">This option's standing is decided by one engine value. Its identifier,
          exact number and update history are in the technical evidence view.</p>
        <ul class="ev__list">
          <li>option: <code>${escapeHtml(o.option_id)}</code></li>
          <li>status: <code>${escapeHtml(o.value)}</code></li>
          <li>driven by: <code>${escapeHtml(o.driven_by)}</code></li>
        </ul>
      </div>
    </details>
  </section>`
}

/** Other options, collapsed. They must not compete with the primary decision on first view. */
function otherDecisions(options: OptionEntry[]): string {
  if (options.length === 0) return ''
  return `<details class="others">
    <summary class="others__s">See other decisions (${options.length})</summary>
    <div class="others__b">
      ${options.map((o) => {
        const d = plainDecision(o)
        return `<article class="others__i" data-option-id="${escapeHtml(d.optionId)}">
          <h4 class="others__h">${escapeHtml(d.question)}</h4>
          <p class="others__p">${escapeHtml(d.standing)}</p>
        </article>`
      }).join('')}
      <p class="dec__note">${escapeHtml(NOTHING_EXECUTES)}</p>
    </div>
  </details>`
}

/**
 * The situation diagram, behind a control.
 *
 * Observation 7 recorded that the map looked artificial and did not help. It has now been replaced
 * rather than restyled: MERIDIAN has no spatial model, so a map had to invent placement for facts
 * the scenario does not hold. What sits here shows how one thing led to another (issue #33).
 *
 * It stays behind a control and stays out of the default view until a cold reader has actually
 * passed the five-second test. The limitation below is stated next to the control, not buried in a
 * document — a reader who opens it is entitled to know it has not met that bar yet.
 */
export const MAP_LIMITATION =
  'This diagram is supporting evidence and has not yet passed the five-second comprehension test — ' +
  'no first-time reader has been asked to explain it yet. It replaces a map, because MERIDIAN does ' +
  'not model locations, distances or routes. Nothing on this screen depends on reading it.'

function whereSection(run: RunResult): string {
  return `<details class="where">
    <summary class="where__s">Show how this fits together</summary>
    <div class="where__b">
      <p class="where__note">A fictional scenario. This is a diagram of how one thing led to
        another — <strong>not a map</strong>. MERIDIAN does not model locations, distances or
        routes, so nothing here is anywhere.</p>
      <p class="where__limit"><strong>Known limitation.</strong> ${escapeHtml(MAP_LIMITATION)}</p>
      ${situationDiagram(situationModel(run))}
    </div>
  </details>`
}

export function briefingView(run: RunResult): string {
  const p = run.projection
  const summary = situationSummary(run)
  const lede = crisisLede(run)
  const sections = plainSections(run)
  const primary = primaryDecision(p)
  const others = p.government_options.filter((o) => o.option_id !== primary?.option_id)

  return `<div class="briefing">

    <!-- 1 · What happened? ─────────────────────────────────────────────── -->
    <header class="lede">
      <h1 class="lede__h">${escapeHtml(summary.headline)}</h1>
      ${lede.length
        ? `<p class="lede__p">${lede.map(escapeHtml).join(' ')}</p>`
        : '<p class="lede__p">Nothing further has been established about the situation yet.</p>'}
    </header>

    <!-- 2 · Why does it matter? ────────────────────────────────────────── -->
    <div class="secs">
      ${sections.map(section).join('')}
    </div>

    <!-- 3 · What needs attention? ──────────────────────────────────────── -->
    ${primary
      ? decision(primary)
      : `<section class="dec"><h2 class="dec__h">No decision is waiting.</h2>
           <p class="dec__note">${escapeHtml(NOTHING_EXECUTES)}</p></section>`}

    ${otherDecisions(others)}

    ${whereSection(run)}

    <!-- 4 · What can I ask? ─────────────────────────────────────────────── -->
    <section class="askprompt" aria-labelledby="lbl-ask">
      <h2 class="askprompt__h" id="lbl-ask">You can ask about this</h2>
      <p class="askprompt__p">Ask in your own words. This version can explain the situation but
        cannot change it. For example:</p>
      <ul class="askprompt__list">
        ${STARTERS.slice(0, 3).map((q) => `<li>${escapeHtml(q)}</li>`).join('')}
      </ul>
      <button type="button" class="askprompt__go" data-mode="ask">Ask MERIDIAN</button>
    </section>

    <!-- 5 · What does MERIDIAN not know? ───────────────────────────────── -->
    <section class="unknown" aria-labelledby="lbl-unknown">
      <h2 class="unknown__h" id="lbl-unknown">What MERIDIAN does not know</h2>
      <p class="unknown__p">This is one fictional scenario, not a forecast. MERIDIAN does not know
        what will happen next, whether people would really behave this way, or anything about the
        real world. It models a first-order change in what people believe, a current situation and a
        declared decision — and nothing else.</p>
      <p class="unknown__p">Where a value is not known it is marked unknown or unavailable, never
        zero. Population groups are averages; the individuals inside them are not modelled.</p>
    </section>

    <footer class="bfoot">
      <button type="button" class="bfoot__tech" data-mode="analysis">Open technical evidence</button>
      <p class="bfoot__note">The technical view shows exact values, engine identifiers and update
        history. It is built for inspection, not for reading.</p>
    </footer>
  </div>`
}
