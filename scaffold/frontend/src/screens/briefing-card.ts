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
import { NOTHING_EXECUTES, headlineAndAsk, impactRows, plainDecision, primaryDecision } from '../engine/presentation.ts'
import type { ImpactRow } from '../engine/presentation.ts'

const ARROW: Record<string, string> = { rising: '↑', falling: '↓', steady: '→' }

/**
 * One impact row.
 *
 * THE ROW IS THE CONTROL. A repeated "Explain this" button on every row read as clutter, so the
 * whole row is the affordance and the label appears on hover or focus. It is a real `<button>`, so
 * keyboard access and screen-reader semantics come for free rather than being bolted on.
 *
 * "Ask about this" rather than "Explain this", because it describes what actually happens: a
 * question is sent to MERIDIAN.
 *
 * Where the catalogue has no question — politics, today — the row is NOT a control. A row that
 * reliably produces a refusal is worse than a row that does nothing. That gap is issue #37 and it
 * is meant to be visible.
 */
function row(r: ImpactRow): string {
  const inner = `<span class="brow__t">${escapeHtml(r.title)}</span>
    <span class="brow__l">${escapeHtml(r.line)}</span>
    ${r.direction && r.directionSubject
      ? `<span class="brow__d brow__d--${r.direction}">
           <span aria-hidden="true">${ARROW[r.direction] ?? ''}</span>
           <span class="visually-hidden">${escapeHtml(r.directionSubject)} is </span>${escapeHtml(r.direction)}</span>`
      : '<span class="brow__d brow__d--none">not established</span>'}`

  if (!r.askQuestion) {
    return `<li><div class="brow brow--static" data-row="${escapeHtml(r.id)}">${inner}
      <span class="brow__ask brow__ask--none">&nbsp;</span></div></li>`
  }
  return `<li><button type="button" class="brow brow--ask" data-row="${escapeHtml(r.id)}"
      data-ask-question="${escapeHtml(r.askQuestion)}"
      aria-label="Ask MERIDIAN about ${escapeHtml(r.title.toLowerCase())}">${inner}
    <span class="brow__ask" aria-hidden="true">Ask about this →</span></button></li>`
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
  const others = run.projection.government_options.length - (primary ? 1 : 0)

  return `<article class="bcard" data-briefing-card aria-label="Situation briefing">
    <header class="bcard__hd">
      <span class="bcard__badge">BRIEFING</span>
      <span class="bcard__meta">Day ${Math.max(1, Math.round(run.projection.simulated_hours / 24))} · fictional scenario</span>
    </header>

    <h1 class="bcard__h">${escapeHtml(headline)}</h1>

    <p class="brows__hint">Select any row to ask MERIDIAN about it.</p>
    <ul class="brows">${rows.map(row).join('')}</ul>

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

    <footer class="bcard__ft">
      <button type="button" class="bcard__more" data-ask-question="Brief me on the current situation.">Tell me more</button>
      <button type="button" class="bcard__more" data-show-diagram>How this fits together</button>
      ${others > 0
        ? `<button type="button" class="bcard__more" data-ask-question="Brief me on the current situation.">${others} other decision${others === 1 ? '' : 's'}</button>`
        : ''}
      <button type="button" class="bcard__more bcard__more--quiet" data-mode="analysis">Exact numbers</button>
    </footer>
  </article>`
}
