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
  const rerouteOpacity = 0.25 + Math.min(1, reroutingLevel) * 0.75
  const rerouteWidth = 1.5 + Math.min(1, reroutingLevel) * 2.5
  const directOpacity = 1 - Math.min(1, reroutingLevel) * 0.75

  return `<svg class="map" viewBox="0 0 800 560" preserveAspectRatio="xMidYMid meet" role="img"
      aria-label="Fictional strategic map of the Kestral Strait. Northshore lies north of the strait and Southport south of it. A blockade zone sits on the northern approach; shipping is rerouted south around it.">
    <defs>
      <linearGradient id="sea" x1="0" y1="0.0" x2="0" y2="1.5">
        <stop offset="0%" stop-color="#0a1622"/><stop offset="100%" stop-color="#071019"/>
      </linearGradient>
      <linearGradient id="land" x1="0" y1="0.0" x2="0" y2="1.5">
        <stop offset="0%" stop-color="#152131"/><stop offset="100%" stop-color="#101a26"/>
      </linearGradient>
      <radialGradient id="blockadeGlow">
        <stop offset="0%" stop-color="#ff5c6a" stop-opacity="0.30"/>
        <stop offset="100%" stop-color="#ff5c6a" stop-opacity="0"/>
      </radialGradient>
    </defs>

    <rect width="800" height="560.0" fill="url(#sea)"/>

    <!-- Meridian graticule: the navigation motif the project is named for. -->
    <g class="map__graticule" aria-hidden="true">
      ${[80, 200, 320, 440, 560, 680].map((x) => `<line x1="${x}" y1="0.0" x2="${x}" y2="560.0"/>`).join('')}
      ${[60, 130, 200, 270, 340].map((y) => `<line x1="0" y1="${y}" x2="800" y2="${y}"/>`).join('')}
      <line class="map__meridian" x1="400" y1="0.0" x2="400" y2="560.0"/>
    </g>

    <!-- Invented landmasses. Not derived from any real coastline. -->
    <path class="map__land" fill="url(#land)"
      d="M0,0.0 L800,0.0 L800,85.5 C700,97.3 640,135.6 560,141.5 C470,148.8 400,109.1 310,117.9 C220,126.7 140,85.5 60,58.9 L0,50.1 Z"/>
    <path class="map__land" fill="url(#land)"
      d="M0,560.0 L800,560.0 L800,442.1 C720,421.5 660,450.9 580,442.1 C500,433.3 452,386.1 372,397.9 C280,411.2 190,468.6 96,486.3 L0,498.1 Z"/>

    <text class="map__place" x="612" y="76.6">Northshore</text>
    <text class="map__place" x="560" y="504.0">Southport</text>
    <text class="map__strait" x="196" y="259.4">Kestral Strait</text>

    <!-- Direct route: fades as rerouting rises. -->
    <path class="map__route map__route--direct" d="M40,315.4 C190,288.8 300,221.1 420,206.3 C520,194.5 640,176.8 772,153.3"
      style="opacity:${directOpacity.toFixed(3)}"/>

    <!-- Rerouted flow: strengthens as rerouting rises. Driven by engine output. -->
    <path class="map__route map__route--reroute"
      d="M40,327.2 C190,353.7 300,421.5 430,430.3 C560,439.2 660,380.2 772,303.6"
      style="opacity:${rerouteOpacity.toFixed(3)};stroke-width:${rerouteWidth.toFixed(2)}"/>

    ${
      blockadeActive
        ? `<g class="map__blockade">
             <circle cx="430" cy="215.2" r="74" fill="url(#blockadeGlow)"/>
             <circle class="map__blockade-ring" cx="430" cy="215.2" r="46"/>
             <text class="map__blockade-label" x="430" y="221.1">BLOCKADE ZONE</text>
           </g>`
        : ''
    }

    <g class="map__marker" transform="translate(430,146)">
      <circle r="4.5"/><circle class="map__marker-halo" r="11"/>
    </g>
  </svg>`
}

export function mapLegend(): string {
  const items: [string, string][] = [
    ['direct', 'Shipping route'],
    ['reroute', 'Rerouted flow'],
    ['blockade', 'Blockade zone'],
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
