/**
 * Briefing View — the default player experience, built to the founder-approved mockup.
 *
 * Composition: header · dominant crisis visual (68%) with situation summary beneath · NEEDS YOU
 * decision stack (32%) · three consequence cards · origin legend.
 *
 * EVERY sentence comes from `engine/presentation.ts`. Three things in the mockup are NOT rendered,
 * because no engine field establishes them and a readable sentence is still a claim:
 *
 *   - `TICK 120` and `20:00 LOCAL` — the run is at tick 20 and the engine models no clock.
 *   - `Greenport Docks` / `Veteran Anchorage` — not in scenario data. Northshore and Southport are.
 *   - any vessel count, deadline, or named human activity.
 *
 * Honesty properties that survive simplification: the fictional disclosure and its crop survival,
 * per-card origin markers, and the statement that no decision can be executed.
 */

import type { OptionEntry, RunResult } from '../engine/client.ts'
import {
  consequenceDomains,
  mapCallouts,
  primaryDecision,
  sinceYesterday,
  situationSummary,
} from '../engine/presentation.ts'
import type { ConsequenceDomain, DerivedTrend } from '../engine/presentation.ts'
import { escapeHtml } from '../components/epistemic.ts'
import { originBadge } from '../components/origin.ts'
import { briefingMap, trendLine } from '../components/briefing-viz.ts'

/** Domain icons. Original geometry — no third-party icon set. */
const ICONS: Record<string, string> = {
  people: `<circle cx="9" cy="8" r="3.2"/><circle cx="17.5" cy="9.5" r="2.4"/>
    <path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6" fill="none"/><path d="M16 20c0-2.4 1.3-4.4 3.2-5" fill="none"/>`,
  economy: `<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z" fill="none"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9" fill="none"/>`,
  politics: `<path d="M4 20h16M6 20V10M10 20V10M14 20V10M18 20V10M3 10h18L12 4z" fill="none"/>`,
}

const DOMAIN_TAGS: Record<string, string[]> = {
  publish_legal_advice: ['political', 'legal'],
  pursue_quiet_diplomacy: ['political', 'diplomatic'],
  declare_emergency_powers: ['political', 'legal'],
}

function consequenceCard(d: ConsequenceDomain, trend: DerivedTrend | null): string {
  const values = trend?.recent ?? []
  return `<article class="ccard ccard--${d.id}" data-card-id="${escapeHtml(d.trend?.field ?? d.id)}"
      tabindex="0" role="button"
      aria-label="${escapeHtml(d.title)}: ${escapeHtml(d.statement)}. Select to inspect the underlying values in Analysis view.">
    <header class="ccard__head">
      <span class="ccard__icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" fill="currentColor">${ICONS[d.id]}</svg>
      </span>
      <span class="ccard__label">${escapeHtml(d.title)}</span>
      ${originBadge(d.origin)}
    </header>
    <p class="ccard__state">${escapeHtml(d.statement)}</p>
    <div class="ccard__trend">
      <span class="ccard__trend-k">Trend (last 5 days)</span>
      ${trendLine(values, d.id)}
    </div>
    <span class="ccard__inspect">INSPECT <span aria-hidden="true">›</span></span>
  </article>`
}

function decisionCard(o: OptionEntry, primary: boolean): string {
  const name = o.label.replace(/_/g, ' ')
  const tags = DOMAIN_TAGS[o.option_id] ?? ['political']
  /*
   * DERIVED, not copied from the mockup.
   *
   * The mockup's wording ("could reduce public and political pressure") is a CONSEQUENCE claim, and
   * this prototype computes no cost or effect for any option - the options panel says so in the
   * same breath. Asserting an outcome here would contradict that caveat. What IS true, and is what
   * the engine actually establishes, is why the option currently holds its status.
   */
  const field = o.driven_by.replace('chain.', '').replace(/_/g, ' ')
  const why =
    o.value === 'ENABLED'
      ? `Open because ${field} has passed the threshold this option declares.`
      : o.value === 'CONSTRAINED'
        ? `Constrained: ${field} has risen far enough to limit this option, but not to open it.`
        : `Available: ${field} is below every threshold this option declares.`
  return `<article class="dcard ${primary ? 'dcard--primary' : 'dcard--secondary'}"
      data-card-id="${escapeHtml(o.option_id)}" tabindex="0" role="button"
      aria-label="${primary ? 'Primary decision' : 'Secondary option'}: ${escapeHtml(name)}, ${escapeHtml(o.value)}. Select to inspect.">
    <span class="dcard__kicker">${primary ? 'PRIMARY DECISION' : 'SECONDARY OPTION'}</span>
    <h3 class="dcard__title">${escapeHtml(name)}</h3>
    <p class="dcard__why">${escapeHtml(why)}</p>
    <ul class="dcard__tags">${tags.map((t) => `<li class="tag tag--${t}">${t}</li>`).join('')}</ul>
    ${
      primary
        ? `<div class="dcard__acts">
             <button class="btn btn--ghost" type="button" data-open-analysis="${escapeHtml(o.option_id)}">
               <span aria-hidden="true">⌕</span> INSPECT
             </button>
             <button class="btn btn--solid" type="button" data-plan="${escapeHtml(o.option_id)}"
               aria-describedby="plan-note">DEVELOP PLAN <span aria-hidden="true">›</span></button>
           </div>`
        : ''
    }
  </article>`
}

export function briefingView(run: RunResult): string {
  const p = run.projection
  const summary = situationSummary(run)
  const domains = consequenceDomains(run)
  const primary = primaryDecision(p)
  const secondary = p.government_options.find(
    (o) => o.option_id !== primary?.option_id && o.value === 'CONSTRAINED',
  )
  const callouts = mapCallouts(run)
  const days = Math.max(1, Math.round(p.simulated_hours / 24))

  return `<div class="briefing">

    <!-- ── Crisis visual: dominant, ~two thirds of usable width ─────────── -->
    <section class="bviz" aria-labelledby="lbl-crisis">
      <h2 class="sect" id="lbl-crisis">CRISIS OVERVIEW</h2>
      ${briefingMap(run, callouts, days)}
    </section>

    <!-- ── Situation summary ───────────────────────────────────────────── -->
    <section class="bsum" aria-labelledby="lbl-sum">
      <h2 class="sect" id="lbl-sum">SITUATION SUMMARY</h2>
      <p class="bsum__head">${escapeHtml(summary.headline)}</p>
      <p class="bsum__text">${escapeHtml(summary.text)}</p>
    </section>

    <!-- ── NEEDS YOU: one dominant decision, one secondary ──────────────── -->
    <aside class="bneeds" aria-labelledby="lbl-needs">
      <h2 class="sect" id="lbl-needs">NEEDS YOU</h2>
      ${primary ? decisionCard(primary, true) : '<p class="dcard__none">No option has changed status.</p>'}
      ${secondary ? decisionCard(secondary, false) : ''}
      <button class="bneeds__all" type="button" data-mode="analysis">
        See all options in Analysis view <span aria-hidden="true">›</span>
      </button>
      <p class="bneeds__note" id="plan-note">Display only — no action is submitted, priced, validated
      or applied in this prototype.</p>
    </aside>

    <!-- ── Since yesterday ─────────────────────────────────────────────── -->
    <aside class="bsince" aria-labelledby="lbl-since">
      <h2 class="sect" id="lbl-since">SINCE YESTERDAY</h2>
      <div class="bsince__row">
        <span class="bsince__icon" aria-hidden="true">
          <svg viewBox="0 0 24 24" fill="currentColor"><rect x="4" y="13" width="3.4" height="7" rx="1"/>
          <rect x="10.3" y="9" width="3.4" height="11" rx="1"/><rect x="16.6" y="5" width="3.4" height="15" rx="1"/></svg>
        </span>
        <p class="bsince__text">${escapeHtml(sinceYesterday(run))}</p>
        ${originBadge(run.connection === 'unavailable' ? 'unavailable' : 'engine')}
      </div>
    </aside>

    <!-- ── Three consequence domains (scenario-defined) ─────────────────── -->
    <section class="ccards" aria-label="How society is being affected">
      ${domains.map((d) => consequenceCard(d, d.trend)).join('')}
    </section>

    <!-- ── Origin legend ───────────────────────────────────────────────── -->
    <footer class="blegend" aria-label="Origin key">
      ${originBadge('engine')}<span class="blegend__t">Engine-derived</span>
      ${originBadge('fixture')}<span class="blegend__t">Fixture input</span>
    </footer>
  </div>`
}
