/**
 * Visual primitives: the fictional strategic map, trajectory charts and sparklines.
 *
 * All original SVG. NO real-world mapping data, no tile service, no third-party map assets, and
 * no coastline traced from a real place. The Kestral Strait is invented geometry — that is a
 * safety property, not an aesthetic one: a fictional world must not render a recognisable real
 * location.
 *
 * Charts are drawn from the run's own trajectory. They plot values the engine produced and add
 * nothing — no smoothing, no projection forward, no confidence band.
 */

import { escapeHtml } from './epistemic.ts'
import type { TrajectoryPoint } from '../engine/client.ts'

/* ─────────────────────────────────────────────────────────────────────────────
 * Fictional strategic situation map
 * ─────────────────────────────────────────────────────────────────────────── */

/**
 * @param reroutingLevel 0..1 — how strongly carriers have diverted. Drives the rerouted flow's
 *   prominence, so the map reads the crisis rather than decorating it.
 */
export function situationMap(reroutingLevel: number, blockadeActive: boolean): string {
  const r = Math.min(1, Math.max(0, reroutingLevel))
  const rerouteOpacity = 0.3 + r * 0.7
  const rerouteWidth = 1.8 + r * 2.6
  const directOpacity = 1 - r * 0.78

  return `<svg class="map" viewBox="0 0 800 560" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="Fictional strategic map of the Kestral Strait. Northshore lies north of the strait, Southport south of it, and the Vantaran Approaches to the east. A blockade zone closes the northern approach; commercial shipping is diverted south around it. Invented geography.">
    <defs>
      <linearGradient id="sea" x1="0" y1="0" x2="0" y2="1.5">
        <stop offset="0%" stop-color="#0a1622"/><stop offset="100%" stop-color="#071019"/>
      </linearGradient>
      <linearGradient id="land" x1="0" y1="0" x2="0" y2="1.5">
        <stop offset="0%" stop-color="#182531"/><stop offset="100%" stop-color="#111c28"/>
      </linearGradient>
      <radialGradient id="blockadeGlow">
        <stop offset="0%" stop-color="#ff5c6a" stop-opacity="0.30"/>
        <stop offset="100%" stop-color="#ff5c6a" stop-opacity="0"/>
      </radialGradient>
      <marker id="flowDirect" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">
        <path d="M0,1 L9,5 L0,9 z" class="map__arrow map__arrow--direct"/>
      </marker>
      <marker id="flowReroute" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse">
        <path d="M0,1 L9,5 L0,9 z" class="map__arrow map__arrow--reroute"/>
      </marker>
      <pattern id="restricted" width="11" height="11" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
        <line x1="0" y1="0" x2="0" y2="11" class="map__hatch"/>
      </pattern>
    </defs>

    <rect width="800" height="560" fill="url(#sea)"/>

    <!-- Bathymetric contours: depth suggestion only, invented, no survey data. -->
    <g class="map__bathy" aria-hidden="true">
      <path d="M0,236 C150,214 280,268 420,254 C540,242 660,286 800,268"/>
      <path d="M0,282 C150,262 280,314 420,300 C540,288 660,330 800,312"/>
      <path d="M0,328 C150,310 280,358 420,346 C540,334 660,372 800,356"/>
    </g>

    <!-- Meridian graticule: the navigation motif the project is named for. -->
    <g class="map__graticule" aria-hidden="true">
      ${[80, 200, 320, 440, 560, 680].map((x) => `<line x1="${x}" y1="0" x2="${x}" y2="560"/>`).join('')}
      ${[60, 130, 200, 270, 340, 410, 480].map((y) => `<line x1="0" y1="${y}" x2="800" y2="${y}"/>`).join('')}
      <line class="map__meridian" x1="400" y1="0" x2="400" y2="560"/>
    </g>

    <!-- Invented landmasses with inlet detail. Not derived from any real coastline. -->
    <path class="map__land" fill="url(#land)"
      d="M0,0 L800,0 L800,86 C742,96 706,128 664,132 C620,136 596,112 556,124
         C516,136 486,158 446,150 C404,142 386,110 344,116 C300,122 268,150 226,142
         C176,132 132,96 84,72 C56,58 28,54 0,50 Z"/>
    <path class="map__land" fill="url(#land)"
      d="M0,560 L800,560 L800,442 C742,424 700,442 656,440 C610,438 578,410 536,414
         C494,418 470,446 428,442 C384,438 360,404 316,412 C266,421 214,462 160,478
         C104,494 52,498 0,500 Z"/>
    <path class="map__coast" fill="none"
      d="M0,50 C56,54 84,72 84,72 C132,96 176,132 226,142 C268,150 300,122 344,116
         C386,110 404,142 446,150 C486,158 516,136 556,124 C596,112 620,136 664,132
         C706,128 742,96 800,86"/>
    <path class="map__coast" fill="none"
      d="M0,500 C52,498 104,494 160,478 C214,462 266,421 316,412 C360,404 384,438 428,442
         C470,446 494,418 536,414 C578,410 610,438 656,440 C700,442 742,424 800,442"/>

    <!-- Restricted waters: the closed northern approach. -->
    ${
      blockadeActive
        ? `<path class="map__restricted" fill="url(#restricted)"
             d="M338,168 C370,150 452,150 496,172 C528,188 532,240 500,258
                C452,282 372,280 340,258 C310,238 310,184 338,168 Z"/>`
        : ''
    }

    <!-- Commercial route, direct: fades as carriers divert. -->
    <path class="map__route map__route--direct" marker-end="url(#flowDirect)"
      d="M40,315 C190,289 300,221 420,206 C520,195 640,177 760,153"
      style="opacity:${directOpacity.toFixed(3)}"/>

    <!-- Commercial route, diverted south: strengthens with engine-computed rerouting. -->
    <path class="map__route map__route--reroute" marker-end="url(#flowReroute)"
      d="M40,327 C190,354 300,421 430,430 C560,439 660,380 760,304"
      style="opacity:${rerouteOpacity.toFixed(3)};stroke-width:${rerouteWidth.toFixed(2)}"/>

    ${
      blockadeActive
        ? `<g class="map__blockade">
             <circle cx="430" cy="215" r="76" fill="url(#blockadeGlow)"/>
             <circle class="map__blockade-ring" cx="430" cy="215" r="47"/>
             <text class="map__blockade-label" x="430" y="220">BLOCKADE ZONE</text>
             <line class="map__leader" x1="430" y1="262" x2="430" y2="300"/>
             <text class="map__annot" x="430" y="316">Northern approach closed</text>
             <text class="map__annot map__annot--sub" x="430" y="333">Commercial traffic diverting south</text>
           </g>`
        : ''
    }

    <!-- Three strategic points. Commerce and transport, deliberately not military symbology. -->
    <g class="map__points">
      <g class="map__pt" transform="translate(196,196)">
        <circle class="map__pt-ring" r="7"/><circle class="map__pt-dot" r="2.6"/>
        <text class="map__pt-label" x="13" y="4">Northshore Terminal</text>
      </g>
      <g class="map__pt" transform="translate(232,452)">
        <circle class="map__pt-ring" r="7"/><circle class="map__pt-dot" r="2.6"/>
        <text class="map__pt-label" x="13" y="4">Southport Docks</text>
      </g>
      <g class="map__pt" transform="translate(688,368)">
        <circle class="map__pt-ring" r="7"/><circle class="map__pt-dot" r="2.6"/>
        <text class="map__pt-label" x="-13" y="4" text-anchor="end">Vantaran Approaches</text>
      </g>
    </g>

    <text class="map__place" x="620" y="60">NORTHSHORE</text>
    <text class="map__place" x="568" y="520">SOUTHPORT</text>
    <text class="map__strait" x="150" y="292">Kestral Strait</text>
  </svg>`
}

export function mapLegend(): string {
  const items: [string, string][] = [
    ['direct', 'Shipping route'],
    ['reroute', 'Rerouted flow'],
    ['blockade', 'Blockade zone'],
    ['restricted', 'Restricted waters'],
  ]
  return `<ul class="maplegend">${items
    .map(([k, label]) => `<li><span class="maplegend__key maplegend__key--${k}" aria-hidden="true"></span>${label}</li>`)
    .join('')}</ul>`
}

/* ─────────────────────────────────────────────────────────────────────────────
 * Charts — drawn only from values the run produced
 * ─────────────────────────────────────────────────────────────────────────── */

function points(series: number[], w: number, h: number, pad = 2): string {
  if (series.length < 2) return ''
  const max = Math.max(...series, 0.0001)
  const step = (w - pad * 2) / (series.length - 1)
  return series
    .map((v, i) => `${(pad + i * step).toFixed(2)},${(h - pad - (v / max) * (h - pad * 2)).toFixed(2)}`)
    .join(' ')
}

/** Compact inline trend. Purely a shape — the number beside it carries the value. */
export function sparkline(series: number[], tone: string): string {
  if (series.length < 2) return '<span class="spark spark--empty" aria-hidden="true"></span>'
  return `<svg class="spark" viewBox="0 0 68 20" preserveAspectRatio="none" aria-hidden="true">
    <polyline class="spark__line spark__line--${tone}" points="${points(series, 68, 20)}"/>
  </svg>`
}

export interface TrajectorySeries {
  field: string
  label: string
  tone: string
}

/** Multi-series trajectory over the run. Axis labelled in ticks, the engine's own clock. */
export function trajectoryChart(
  trajectory: TrajectoryPoint[],
  series: TrajectorySeries[],
  height = 150,
): string {
  const w = 460
  const h = height
  if (!trajectory.length) {
    return `<p class="chart__empty">No trajectory available.</p>`
  }
  const lines = series
    .map((s) => {
      const values = trajectory.map((t) => Number(t[s.field] ?? 0))
      return `<polyline class="chart__line chart__line--${s.tone}" points="${points(values, w, h, 6)}"/>`
    })
    .join('')

  const first = trajectory[0]?.tick ?? 0
  const last = trajectory[trajectory.length - 1]?.tick ?? 0

  return `<div class="chart">
    <svg class="chart__svg" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none" role="img"
         aria-label="Trajectory of engine-derived indicators from tick ${first} to tick ${last}.">
      <g class="chart__grid" aria-hidden="true">
        ${[0.25, 0.5, 0.75].map((f) => `<line x1="0" y1="${(h * f).toFixed(1)}" x2="${w}" y2="${(h * f).toFixed(1)}"/>`).join('')}
      </g>
      ${lines}
    </svg>
    <div class="chart__axis"><span>t${first}</span><span>t${last}</span></div>
    ${series.length < 2 ? '' : `<ul class="chart__legend">${series
      .map((s) => `<li><span class="chart__swatch chart__swatch--${s.tone}" aria-hidden="true"></span>${escapeHtml(s.label)}</li>`)
      .join('')}</ul>`}
  </div>`
}

/** Horizontal bar for a bounded 0..1 value. Width AND the printed number carry the value. */
export function bar(value: number, tone: string): string {
  const pct = Math.max(0, Math.min(1, value)) * 100
  return `<span class="bar" aria-hidden="true"><span class="bar__fill bar__fill--${tone}" style="width:${pct.toFixed(1)}%"></span></span>`
}


