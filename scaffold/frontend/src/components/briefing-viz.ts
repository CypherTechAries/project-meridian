/**
 * Briefing situation diagram and trend lines.
 *
 * THIS IS NOT A MAP, AND DELIBERATELY SO (issue #33).
 *
 * MERIDIAN's engine has no spatial model: no coordinates, no geometry, no port entities, and
 * political pressure is a single scalar with no location. A map would have to invent placement for
 * facts the scenario does not hold. The previous version did exactly that — invented coastlines,
 * decorative settlement lights, and two place names ("Northshore", "Southport") that were
 * hard-coded in this file and are not scenario entities. It failed its first cold usability test.
 *
 * What replaces it shows STRUCTURE: the causal chain the engine actually models, arranged by
 * relationship. One thing led to another. Nothing is anywhere.
 *
 * The model is built by `engine/presentation.ts`. This module renders what it is given and invents
 * nothing — no value, no group, no place, and no magnitude that is not in the model.
 */

import type { SituationModel, SituationStage } from '../engine/presentation.ts'
import { escapeHtml } from './epistemic.ts'

const W = 960
const BAND_H = 92
const PAD_X = 26

/** Magnitude bar. Length is the value; the level word beside it carries the meaning in text. */
function bar(value: number, x: number, y: number, w: number): string {
  const fill = Math.max(2, Math.round(w * value))
  return `<g aria-hidden="true">
    <rect class="sd__bar-bg" x="${x}" y="${y}" width="${w}" height="8" rx="4"/>
    <rect class="sd__bar" x="${x}" y="${y}" width="${fill}" height="8" rx="4"/>
  </g>`
}

/**
 * The recorded values over time. No smoothing, no extrapolation, no forward projection.
 * Absent rather than flat where the value is not recorded — a flat line would be a claim.
 *
 * THE PEAK IS MARKED, and that is not decoration. The line covers the whole scenario, while the
 * direction word beside it describes the recent window. For political pressure those disagree on
 * sight: the line climbs steeply and the label reads "falling", because the value rose for
 * seventeen steps and has edged down since. Marking the turn is what makes both true statements
 * legible at once — the same problem as reporting a level without its distance from its own peak.
 */
function spark(values: number[], x: number, y: number, w: number, h: number): string {
  if (values.length < 2) return ''
  const lo = Math.min(...values)
  const hi = Math.max(...values)
  const span = hi - lo || 1
  const at = (v: number, i: number): [number, number] => [
    x + (i / (values.length - 1)) * w,
    y + h - ((v - lo) / span) * h,
  ]
  const pts = values.map((v, i) => at(v, i).map((n) => n.toFixed(1)).join(',')).join(' ')

  const peakIndex = values.indexOf(hi)
  const [px, py] = at(hi, peakIndex)
  const [lx, ly] = at(values[values.length - 1] ?? 0, values.length - 1)
  // Only worth marking when the peak is genuinely behind us; otherwise the peak IS the last point.
  const turned = peakIndex < values.length - 1

  return `<g aria-hidden="true">
    <polyline class="sd__spark" points="${pts}"/>
    ${
      turned
        ? `<circle class="sd__spark-peak" cx="${px.toFixed(1)}" cy="${py.toFixed(1)}" r="2.8"/>
           <text class="sd__spark-peakl" x="${px.toFixed(1)}" y="${(py - 7).toFixed(1)}" text-anchor="middle">highest</text>`
        : ''
    }
    <circle class="sd__spark-end" cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="2.6"/>
  </g>`
}

const ARROWS: Record<string, string> = { rising: '↑', falling: '↓', steady: '→' }

function stageBand(s: SituationStage, y: number): string {
  // The sentence needs room. At 470 the pressure sentence ran under the bar.
  const barX = 520
  const barW = 170
  const sparkX = 726
  return `<g class="sd__band" data-stage="${escapeHtml(s.id)}">
    <rect class="sd__band-bg" x="${PAD_X}" y="${y}" width="${W - PAD_X * 2}" height="${BAND_H - 14}" rx="8"/>
    <text class="sd__band-t" x="${PAD_X + 20}" y="${y + 30}">${escapeHtml(s.title)}</text>
    <text class="sd__band-s" x="${PAD_X + 20}" y="${y + 54}">${escapeHtml(s.sentence)}</text>
    ${
      s.level !== null && s.magnitude !== null
        ? `<text class="sd__lvl" x="${barX}" y="${y + 30}">${escapeHtml(s.level)}${
            s.direction
              ? ` <tspan class="sd__dir sd__dir--${s.direction}">${ARROWS[s.direction] ?? ''} ${escapeHtml(s.direction)}</tspan>`
              : ''
          }</text>
           ${bar(s.magnitude, barX, y + 42, barW)}`
        : `<text class="sd__lvl sd__lvl--none" x="${barX}" y="${y + 30}">not established</text>`
    }
    ${
      s.series.length >= 2
        ? `${spark(s.series, sparkX, y + 22, 170, 26)}
           <text class="sd__sparkl" x="${sparkX}" y="${y + 64}">start of the scenario to now</text>`
        : `<text class="sd__sparkl sd__sparkl--none" x="${sparkX}" y="${y + 36}">no change line —</text>
           <text class="sd__sparkl sd__sparkl--none" x="${sparkX}" y="${y + 52}">not recorded each step</text>`
    }
  </g>`
}

function connector(y: number): string {
  return `<g aria-hidden="true">
    <line class="sd__flow" x1="${W / 2}" y1="${y}" x2="${W / 2}" y2="${y + 12}"/>
    <path class="sd__flow-head" d="M${W / 2 - 5},${y + 10} L${W / 2},${y + 18} L${W / 2 + 5},${y + 10} Z"/>
  </g>`
}

/**
 * The situation diagram.
 *
 * Reads top to bottom: what closed, what followed from it, who it reached, what pressure built, and
 * what choice is open. **Position carries CONSEQUENCE, never location.**
 */
export function situationDiagram(m: SituationModel): string {
  const gap = 20
  let y = 66
  const parts: string[] = []

  // 1 · what is blocked
  parts.push(`<g data-stage="origin">
    <rect class="sd__origin" x="${PAD_X}" y="${y}" width="${W - PAD_X * 2}" height="${BAND_H - 14}" rx="8"/>
    <text class="sd__origin-t" x="${PAD_X + 20}" y="${y + 32}">${
      m.blockadeActive ? 'THE STRAIT IS CLOSED' : 'NO INCIDENT IS ACTIVE'
    }</text>
    <text class="sd__origin-s" x="${PAD_X + 20}" y="${y + 58}">${
      m.blockadeActive
        ? `A blockade has closed it for ${m.days} day${m.days === 1 ? '' : 's'}. Everything below follows from that.`
        : 'Nothing below is being driven by an incident.'
    }</text>
  </g>`)
  y += BAND_H - 14

  // 2–4 · the chain the engine actually models
  for (const s of m.stages) {
    parts.push(connector(y))
    y += gap
    parts.push(stageBand(s, y))
    y += BAND_H - 14
  }

  // 5 · who is affected
  parts.push(connector(y))
  y += gap
  // TWO LABELLED FACTS, never one bar for both. A single bar cannot carry "how many people" and
  // "how badly hit"; readers reasonably assume the longest bar is the biggest group, and here the
  // hardest-hit group is the SMALLEST. The columns are headed so the two cannot be confused.
  const gh = 92 + m.groups.length * 32
  parts.push(`<g class="sd__band" data-stage="groups">
    <rect class="sd__band-bg" x="${PAD_X}" y="${y}" width="${W - PAD_X * 2}" height="${gh}" rx="8"/>
    <text class="sd__band-t" x="${PAD_X + 20}" y="${y + 30}">Who this reaches</text>
    <text class="sd__colh" x="420" y="${y + 52}" text-anchor="end">Share of population</text>
    <text class="sd__colh" x="440" y="${y + 52}">Impact on this group</text>
    ${m.groups
      .map((g, i) => {
        const gy = y + 78 + i * 32
        return `<g data-group-row="${escapeHtml(g.name)}">
          <text class="sd__grp" x="${PAD_X + 20}" y="${gy + 8}">${escapeHtml(g.name)}</text>
          <text class="sd__grp-share" x="420" y="${gy + 8}" text-anchor="end">${g.sharePercent}%</text>
          ${bar(g.value, 440, gy + 1, 130)}
          <text class="sd__grp-lvl" x="582" y="${gy + 8}">${escapeHtml(g.level)}${
            g.mostAffected
              // "most affected" could be read as "badly affected". Naming the comparison set makes
              // it impossible to mistake "highest here" for "high in absolute terms".
              ? '<tspan class="sd__grp-top"> · highest impact among the groups shown</tspan>'
              : ''
          }</text>
        </g>`
      })
      .join('')}
    <text class="sd__note" x="${PAD_X + 20}" y="${y + gh - 12}">${escapeHtml(m.groupsNote)}</text>
  </g>`)
  y += gh

  // 6 · what trade-offs are visible
  if (m.decision) {
    parts.push(connector(y))
    y += gap
    const dh = 124
    parts.push(`<g class="sd__band" data-stage="decision">
      <rect class="sd__decision" x="${PAD_X}" y="${y}" width="${W - PAD_X * 2}" height="${dh}" rx="8"/>
      <text class="sd__band-t" x="${PAD_X + 20}" y="${y + 30}">The choice in front of the government</text>
      <text class="sd__band-s" x="${PAD_X + 20}" y="${y + 56}">${escapeHtml(m.decision.question)}</text>
      <text class="sd__choice" x="${PAD_X + 20}" y="${y + 84}">${escapeHtml(m.decision.choices[0])}</text>
      <text class="sd__choice" x="${PAD_X + 300}" y="${y + 84}">${escapeHtml(m.decision.choices[1])}</text>
      ${
        m.otherChoices > 0
          ? `<text class="sd__note" x="${PAD_X + 600}" y="${y + 84}">and ${m.otherChoices} other${m.otherChoices === 1 ? '' : 's'}</text>`
          : ''
      }
      <text class="sd__exec" x="${PAD_X + 20}" y="${y + dh - 14}">${escapeHtml(m.executionNote)}</text>
    </g>`)
    y += dh
  }

  const H = y + 56

  return `<svg class="bmap sd" viewBox="0 0 ${W} ${H}" preserveAspectRatio="xMidYMin meet" role="img"
      aria-label="Situation diagram for the fictional Kestral Strait scenario. ${escapeHtml(m.kindNote)} ${
        m.blockadeActive
          ? `A blockade closed the strait ${m.days} days ago. Shipping reroutes, port work falls, population groups are affected, and pressure builds on the government, which has a choice open that has not been executed.`
          : 'No incident is active.'
      }">
    <text class="sd__title" x="${PAD_X}" y="30">HOW THIS SITUATION FITS TOGETHER</text>
    <text class="sd__kind" x="${PAD_X}" y="52">${escapeHtml(m.kindNote)}</text>
    ${parts.join('')}
    <text class="sd__foot" x="${PAD_X}" y="${H - 18}">Fictional scenario. Read top to bottom — each row follows from the one above it.</text>
  </svg>`
}

/** Five-point trend line from values the run produced. No smoothing, no projection forward. */
export function trendLine(values: number[], tone: string): string {
  if (values.length < 2) return '<span class="tline tline--empty" aria-hidden="true"></span>'
  const w = 210
  const h = 34
  const max = Math.max(...values)
  const min = Math.min(...values)
  const span = max - min || 1
  const at = (v: number, i: number): [number, number] => [
    3 + (i * (w - 6)) / (values.length - 1),
    h - 5 - ((v - min) / span) * (h - 13),
  ]
  const pts = values.map((v, i) => at(v, i).map((n) => n.toFixed(1)).join(',')).join(' ')
  const dots = values
    .map((v, i) => {
      const [x, y] = at(v, i)
      return `<circle cx="${x.toFixed(1)}" cy="${y.toFixed(1)}" r="2.3"/>`
    })
    .join('')
  return `<svg class="tline tline--${tone}" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" aria-hidden="true">
    <polyline points="${pts}" fill="none"/>${dots}
  </svg>`
}
