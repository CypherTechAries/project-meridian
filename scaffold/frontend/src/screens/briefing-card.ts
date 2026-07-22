/**
 * The Briefing, as a card in the Ask MERIDIAN thread.
 *
 * WHY IT MOVED. The Briefing was a 2,635px document — 2.9 screenfuls, 835 words — in which the one
 * thing that "needs attention" began 257px *below the fold*. Length equalled the sum of all its
 * content, and importance had no effect on position. The only screen that read easily was the
 * conversation, because a conversation answers one question at a time and shows nothing you did
 * not ask for.
 *
 * So the Briefing is now the thread's FIRST ANSWER: a card you can read in one screen, with every
 * deeper level reached by asking rather than by expanding.
 *
 * THREE DECLARED DEPTHS, and detail never leaks upward:
 *   1 · the sentence  — here
 *   2 · the explanation — Ask, by selecting a row
 *   3 · the number    — technical evidence, and nowhere else
 *
 * The per-section "Show where this comes from" disclosures are gone. Their bodies were raw field
 * names (`chain.household_expectation_pressure`), which is level 3 material sitting at level 1.
 */

import type { RunResult } from '../engine/client.ts'
import { escapeHtml } from '../components/epistemic.ts'
import {
  NOTHING_EXECUTES, ROW_FIELD, claimEvidence, headlineAndAsk, impactRows, plainDecision,
  primaryDecision, scenarioPosition,
} from '../engine/presentation.ts'
import type { ImpactRow } from '../engine/presentation.ts'

const ARROW: Record<string, string> = { rising: '↑', falling: '↓', steady: '→' }

/**
 * One impact row, with the evidence for its own claim behind one control.
 *
 * EVIDENCE IS CLAIM-DRIVEN. A reader sees "pressure is low" and can ask to see exactly that: the
 * value, which way it is moving, where it came from, when it last changed, and the mechanism that
 * set it. They are never asked to browse a table of eighteen engine values to find it.
 *
 * EVERY ROW HAS THE SAME CONTROL. That is deliberate. An earlier version made the row itself a
 * button that asked a catalogue question — which worked for People and Economy and had to be inert
 * for Politics, because the catalogue has no question about the government (issue #37). Two rows
 * that behaved and one that did not is exactly the inconsistency that makes an interface feel
 * broken. "Show evidence" works for every claim, so the affordance is uniform.
 *
 * #37 is NOT hidden by this: there is still no way to ask MERIDIAN about politics, and no helper
 * offers one. The gap is in the catalogue, where it belongs, rather than dressed as a dead control.
 */
function row(r: ImpactRow, run: RunResult): string {
  const ev = claimEvidence(run, ROW_FIELD[r.id])
  return `<li class="brow-i">
    <div class="brow" data-row="${escapeHtml(r.id)}">
      <span class="brow__t">${escapeHtml(r.title)}</span>
      <span class="brow__l">${escapeHtml(r.line)}</span>
      ${r.direction && r.directionSubject
        ? `<span class="brow__d brow__d--${r.direction}">
             <span aria-hidden="true">${ARROW[r.direction] ?? ''}</span>
             <span class="visually-hidden">${escapeHtml(r.directionSubject)} is </span>${escapeHtml(r.direction)}</span>`
        : '<span class="brow__d brow__d--none">not established</span>'}
    </div>
    ${ev
      ? `<details class="bev" data-evidence="${escapeHtml(r.id)}">
           <summary class="bev__s">Show evidence</summary>
           <dl class="bev__b">
             <dt>Exact value</dt><dd class="bev__num">${escapeHtml(ev.value)}</dd>
             <dt>Level</dt><dd>${escapeHtml(ev.level)}</dd>
             <dt>Direction</dt><dd>${escapeHtml(ev.direction)}</dd>
             <dt>Origin</dt><dd>${escapeHtml(ev.origin)}</dd>
             <dt>Last changed</dt><dd>${escapeHtml(ev.lastChanged)}</dd>
             <dt>Mechanism</dt><dd class="bev__num">${escapeHtml(ev.mechanism)}</dd>
           </dl>
         </details>`
      : ''}
  </li>`
}

/**
 * The card.
 *
 * Everything above the "more" controls is the two-second read: what happened, what it is doing to
 * people, the economy and the government, and the one decision waiting. Nothing else.
 */
export function briefingCard(run: RunResult): string {
  const { headline } = headlineAndAsk(run)
  const rows = impactRows(run)
  const primary = primaryDecision(run.projection)
  const d = primary ? plainDecision(primary) : null

  return `<article class="bcard" data-briefing-card aria-label="Situation briefing">
    <header class="bcard__hd">
      <span class="bcard__badge">BRIEFING</span>
      <span class="bcard__meta">Day ${Math.max(1, Math.round(run.projection.simulated_hours / 24))} · fictional scenario</span>
    </header>

    <h1 class="bcard__h">${escapeHtml(headline)}</h1>

    <!--
      WHERE THE READER IS. The founder test read this as "halfway into the simulation"; it is the
      last recorded point, three ticks past the peak. Visible without expanding anything, because a
      reader who misjudges the arc misjudges everything else on the card.
      Every clause is derived from the shared packaged state. Changing the entry point is #41.
    -->
    ${(() => {
      const pos = scenarioPosition(run)
      return pos
        ? `<p class="bcard__pos" data-scenario-position>${escapeHtml(pos.line)}</p>
           <p class="bcard__poscav">${escapeHtml(pos.caveat)}</p>`
        : ''
    })()}

    <ul class="brows">${rows.map((r) => row(r, run)).join('')}</ul>

    ${d
      ? `<section class="bdec" aria-labelledby="bdec-h">
           <p class="bdec__k">One decision is waiting</p>
           <h2 class="bdec__h" id="bdec-h">${escapeHtml(d.question)}</h2>
           <div class="bdec__c" role="group" aria-label="Choices — display only">
             ${d.described
               ? d.choices.map((c, i) => `<button type="button" class="choice ${i === 0 ? 'choice--a' : 'choice--b'}"
                   data-choice="${escapeHtml(c)}">${escapeHtml(c)}</button>`).join('')
               : ''}
           </div>
           <p class="bdec__n" data-nothing-executes>${escapeHtml(NOTHING_EXECUTES)}</p>
         </section>`
      : `<section class="bdec"><h2 class="bdec__h">No decision is waiting.</h2>
           <p class="bdec__n" data-nothing-executes>${escapeHtml(NOTHING_EXECUTES)}</p></section>`}

    <!--
      ONE next action. The first answer is not a dossier: the causal chain, the group breakdown and
      the model boundaries are all opened FROM here, not stacked into it.
    -->
    <footer class="bcard__ft">
      <button type="button" class="bcard__more bcard__more--go" data-show-diagram>
        Show how this fits together</button>
    </footer>
  </article>`
}
