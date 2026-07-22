/**
 * "How this situation fits together" — five beats, and nothing else.
 *
 * WHAT THIS REPLACES. The situation diagram showed six bands, each carrying a title, a sentence, a
 * level, a magnitude bar, a sparkline and two captions: roughly thirty pieces of information
 * presented at once. It was a report wearing a diagram's clothes, and a reader lost interest before
 * any of it landed.
 *
 * THE DEFAULT VIEW NOW CONTAINS: five short beats and one control. No bars, no sparklines, no
 * decimals, no captions, no miniature charts.
 *
 * THE CONTROL SAYS "SHOW WHY", not "show the numbers". Most readers do not want the numbers; they
 * want to know why the conclusion was reached. The numbers are one further step in, for the reader
 * who actually wants them.
 *
 * Nothing was deleted — the full chain, the group breakdown, levels and directions, and the exact
 * evidence are all still reachable, each opened deliberately.
 */

import type { RunResult } from '../engine/client.ts'
import { escapeHtml } from '../components/epistemic.ts'
import { fiveBeatChain, situationModel } from '../engine/presentation.ts'
import { situationDiagram } from '../components/briefing-viz.ts'

/**
 * The five-beat chain.
 *
 * Beat four names its comparison set — "affected most, though the level is still low" — because
 * "most affected" alone reads as "badly affected". The hardest-hit group sits at 0.33, which is LOW
 * on the declared thresholds, and the beat must not imply otherwise.
 */
export function causalAnswer(run: RunResult): string {
  const beats = fiveBeatChain(run)
  const m = situationModel(run)

  return `<div class="ca" data-causal-answer>
    <ol class="ca__chain" data-causal-steps>
      ${beats
        .map(
          (b, i) => `<li class="ca__beat${i === 0 ? ' ca__beat--first' : ''}">
            <span class="ca__beat-t">${escapeHtml(b)}</span>
          </li>`,
        )
        .join('')}
    </ol>

    <!--
      ONE control. It opens on purpose and never on load: the expanded view is the old dense
      picture, which is genuinely useful once asked for and actively harmful as a default.
    -->
    <details class="ca__d" data-show-why>
      <summary class="ca__s">Show why</summary>
      <div class="ca__db">

        <section class="ca__sec">
          <h4 class="ca__h">How each step follows from the one before</h4>
          ${situationDiagram(m)}
        </section>

        <section class="ca__sec">
          <h4 class="ca__h">Share of population, against impact</h4>
          <p class="ca__note">These are two different things. The size of a group does not decide
            how hard it is hit — here the hardest-hit group is the smallest.</p>
          <table class="ca__grp">
            <thead><tr>
              <th scope="col">Group</th>
              <th scope="col">Share of population</th>
              <th scope="col">Impact on this group</th>
            </tr></thead>
            <tbody>${m.groups
              .map(
                (g) => `<tr>
                  <td>${escapeHtml(g.name)}</td>
                  <td class="ca__num">${g.sharePercent}%</td>
                  <td>${escapeHtml(g.level)}${
                    g.mostAffected
                      ? ' <span class="ca__top">· highest impact among the groups shown</span>'
                      : ''
                  }</td>
                </tr>`,
              )
              .join('')}</tbody>
          </table>
          <p class="ca__note">${escapeHtml(m.groupsNote)}</p>
        </section>

        <p class="ca__deeper">
          <button type="button" class="ca__btn" data-mode="analysis">Show the exact evidence</button>
          <span class="ca__deeper-n">Exact values, identifiers and mechanisms. Built to be checked,
            not read.</span>
        </p>
      </div>
    </details>
  </div>`
}
