/**
 * Briefing crisis visual and trend lines.
 *
 * Original SVG throughout: atmospheric water, haze bands, dimensional invented landmasses with lit
 * coastal settlement points, a hatched blockade disc, and clearly differentiated original (blocked)
 * and rerouted flows with arrowheads.
 *
 * NOT a real coastline, not a tile service, not traced from any real place. That is a safety
 * property (B5), not an aesthetic one.
 *
 * Callouts are PASSED IN, already derived from engine state by `engine/presentation.ts`. This
 * module renders what it is given and invents nothing.
 */

import type { RunResult } from '../engine/client.ts'
import { stageByField } from '../engine/client.ts'
import { escapeHtml } from './epistemic.ts'

/**
 * Deterministic settlement lights.
 *
 * Seeded rather than random so the same run renders the same coastline every time — an unseeded
 * sprinkle would make screenshots differ between captures of identical state, which would quietly
 * contradict the project's determinism claim.
 */
function lights(count: number, seed: number, path: (t: number) => [number, number]): string {
  let x = seed
  const out: string[] = []
  for (let i = 0; i < count; i++) {
    x = (x * 1103515245 + 12345) % 2147483648
    const t = (x / 2147483648 + i / count) % 1
    const [cx, cy] = path(t)
    const r = 0.7 + ((x >> 7) % 10) / 12
    const o = 0.22 + ((x >> 11) % 10) / 18
    out.push(
      `<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r.toFixed(2)}" fill="#ffd9a0" opacity="${o.toFixed(2)}"/>`,
    )
  }
  return out.join('')
}

export function briefingMap(run: RunResult, callouts: string[], days: number): string {
  const p = run.projection
  const r = Math.min(1, Math.max(0, stageByField(p, 'rerouting_level')?.value ?? 0))
  const blockade = p.incident_active
  const rerouteOpacity = 0.6 + r * 0.4
  const rerouteWidth = 2.2 + r * 1.6
  const directOpacity = 0.25 + (1 - r) * 0.45

  const northCoast = (t: number): [number, number] => [40 + t * 880, 106 - Math.sin(t * 5.2) * 18 - t * 10]
  const southCoast = (t: number): [number, number] => [40 + t * 880, 328 + Math.sin(t * 4.4 + 1) * 16 + t * 6]

  const anchors = [
    { x: 214, y: 124, ax: 268, ay: 104 },
    { x: 706, y: 100, ax: 620, ay: 172 },
    { x: 470, y: 306, ax: 470, ay: 262 },
  ]
  const pills = callouts
    .map((c, i) => {
      const a = anchors[i]
      if (!a) return ''
      const w = 40 + c.length * 6.8
      return `<g class="cal">
        <line class="cal__lead" x1="${a.x}" y1="${a.y}" x2="${a.ax}" y2="${a.ay}"/>
        <g transform="translate(${(a.x - w / 2).toFixed(0)},${a.y - 15})">
          <rect class="cal__pill" width="${w.toFixed(0)}" height="30" rx="15"/>
          <circle class="cal__num-bg" cx="17" cy="15" r="10"/>
          <text class="cal__num" x="17" y="19.5" text-anchor="middle">${i + 1}</text>
          <text class="cal__txt" x="34" y="19.5">${escapeHtml(c)}</text>
        </g>
      </g>`
    })
    .join('')

  const swell = [176, 206, 236, 266]
    .map((y) => `<path d="M0,${y} C160,${y - 12} 320,${y + 12} 480,${y} C640,${y - 12} 800,${y + 12} 960,${y}"/>`)
    .join('')

  return `<svg class="bmap" viewBox="0 0 960 430" preserveAspectRatio="xMidYMid slice" role="img"
      aria-label="Fictional map of the Kestral Strait. ${
        blockade
          ? 'A blockade zone closes the centre of the strait and shipping is diverted south.'
          : 'No incident is active.'
      } Northshore lies to the north and Southport to the south. Invented geography, no real-world map data.">
    <defs>
      <linearGradient id="bw" x1="0" y1="0" x2="0.3" y2="1">
        <stop offset="0%" stop-color="#0d2236"/><stop offset="45%" stop-color="#0a1a2a"/>
        <stop offset="100%" stop-color="#071320"/>
      </linearGradient>
      <linearGradient id="bln" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#22394e"/><stop offset="100%" stop-color="#2d5271"/>
      </linearGradient>
      <linearGradient id="bls" x1="0" y1="1" x2="0" y2="0">
        <stop offset="0%" stop-color="#22394e"/><stop offset="100%" stop-color="#2d5271"/>
      </linearGradient>
      <radialGradient id="bhot">
        <stop offset="0%" stop-color="#ff5c6a" stop-opacity="0.40"/>
        <stop offset="100%" stop-color="#ff5c6a" stop-opacity="0"/>
      </radialGradient>
      <radialGradient id="bhaze" cx="0.5" cy="0.5">
        <stop offset="0%" stop-color="#5b86a8" stop-opacity="0.15"/>
        <stop offset="100%" stop-color="#5b86a8" stop-opacity="0"/>
      </radialGradient>
      <filter id="bsoft"><feGaussianBlur stdDeviation="10"/></filter>
      <marker id="bmA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">
        <path d="M0,1.5 L9,5 L0,8.5 z" fill="#3fd0e8"/>
      </marker>
      <marker id="bmB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
        <path d="M0,1.5 L9,5 L0,8.5 z" fill="#f0a742"/>
      </marker>
      <pattern id="bhatch" width="9" height="9" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="9" stroke="#ff5c6a" stroke-opacity="0.42" stroke-width="1.6"/>
      </pattern>
    </defs>

    <rect width="960" height="430" fill="url(#bw)"/>
    <g opacity="0.6" filter="url(#bsoft)" aria-hidden="true">
      <ellipse cx="250" cy="230" rx="270" ry="76" fill="url(#bhaze)"/>
      <ellipse cx="740" cy="196" rx="240" ry="70" fill="url(#bhaze)"/>
    </g>
    <g class="bmap__swell" aria-hidden="true">${swell}</g>

    <path fill="url(#bln)" d="M0,0 L960,0 L960,62 C880,76 830,104 770,110 C706,116 668,92 606,102
      C548,112 512,134 448,126 C388,118 366,88 306,96 C246,104 206,128 142,118
      C92,110 44,86 0,74 Z"/>
    <path fill="url(#bls)" d="M0,430 L960,430 L960,344 C880,326 820,344 756,340 C692,336 654,310 592,316
      C534,322 502,348 442,342 C382,336 350,306 288,314 C222,323 158,356 88,370 C56,376 26,378 0,380 Z"/>
    <path class="bmap__coast" fill="none" d="M0,74 C44,86 92,110 142,118 C206,128 246,104 306,96
      C366,88 388,118 448,126 C512,134 548,112 606,102 C668,92 706,116 770,110 C830,104 880,76 960,62"/>
    <path class="bmap__coast" fill="none" d="M0,380 C26,378 56,376 88,370 C158,356 222,323 288,314
      C350,306 382,336 442,342 C502,348 534,322 592,316 C654,310 692,336 756,340 C820,344 880,326 960,344"/>
    <g aria-hidden="true">${lights(46, 7919, northCoast)}${lights(38, 104729, southCoast)}</g>

    ${
      blockade
        ? `<g>
             <circle cx="470" cy="208" r="104" fill="url(#bhot)"/>
             <circle class="bmap__zone" cx="470" cy="208" r="64" fill="url(#bhatch)"/>
             <g transform="translate(470,192)" class="bmap__ship" aria-hidden="true">
               <path d="M-14,4 L14,4 L10,12 L-10,12 Z"/><path d="M-1,4 L-1,-7 L8,-2.5 L-1,-2.5 Z"/>
             </g>
             <text class="bmap__zone-t" x="470" y="234" text-anchor="middle">BLOCKADE ZONE</text>
             <text class="bmap__zone-s" x="470" y="250" text-anchor="middle">Active for ${days} day${days === 1 ? '' : 's'}</text>
           </g>`
        : ''
    }

    <path class="rt rt--blocked" marker-end="url(#bmB)" style="opacity:${directOpacity.toFixed(2)}"
      d="M150,286 C300,302 380,272 470,262 C580,250 700,282 830,296"/>
    <path class="rt rt--reroute" marker-end="url(#bmA)"
      style="opacity:${rerouteOpacity.toFixed(2)};stroke-width:${rerouteWidth.toFixed(2)}"
      d="M150,276 C300,244 380,190 470,182 C590,170 720,178 852,188"/>

    <text class="bmap__place" x="480" y="80" text-anchor="middle">NORTHSHORE</text>
    <text class="bmap__place" x="480" y="366" text-anchor="middle">SOUTHPORT</text>
    <text class="bmap__strait" x="150" y="222">KESTRAL STRAIT</text>

    ${pills}

    <g class="lgd" transform="translate(22,268)">
      <rect class="lgd__bg" width="246" height="82" rx="6"/>
      <rect x="16" y="16" width="17" height="10" fill="url(#bhatch)" stroke="#ff5c6a" stroke-opacity="0.5"/>
      <text class="lgd__t" x="42" y="25">Blockade zone</text>
      <line x1="16" y1="45" x2="33" y2="45" class="rt rt--blocked" stroke-dasharray="5 4"/>
      <text class="lgd__t" x="42" y="49">Original shipping route (blocked)</text>
      <line x1="16" y1="67" x2="33" y2="67" class="rt rt--reroute" stroke-dasharray="5 4"/>
      <text class="lgd__t" x="42" y="71">Rerouted shipping flow</text>
    </g>
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
