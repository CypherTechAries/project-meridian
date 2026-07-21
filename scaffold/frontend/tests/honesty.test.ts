/**
 * C0 honesty tests — carried forward through the visual redesign.
 *
 * Every property the previous suite enforced is preserved. The component names changed; the
 * guarantees did not. Nothing here was relaxed to accommodate the new layout — where the redesign
 * changed what is true (the screen is now MIXED engine and fixture, not fixture-only), the test
 * asserts the new truth rather than the old wording.
 */

import { beforeEach, describe, expect, it } from 'vitest'
import { FICTION_DISCLOSURE, MIXED_DISCLOSURE, mount } from '../src/main.ts'
import { initialSnapshot } from '../src/engine/client.ts'
import type { RunResult } from '../src/engine/client.ts'

const ALLOWED_STATUS = ['AUTHORITATIVE', 'ASSESSED', 'DISPUTED', 'UNKNOWN', 'PRESENTATION_ONLY']
const ALLOWED_CONF = ['HIGH', 'MEDIUM', 'LOW', 'NOT_APPLICABLE']

/*
 * These suites assert properties of the ANALYSIS view — the detailed dashboard that was the
 * default before Briefing View existed. Every assertion is unchanged; only the mode they mount is,
 * because the same guarantees now live one depth-level in. Briefing View has its own suite below,
 * with its own stricter rules about what may appear at all.
 */
function render(run: RunResult = initialSnapshot()): HTMLElement {
  const root = document.createElement('div')
  mount(root, run, 'analysis')
  return root
}

describe('disclosures', () => {
  let root: HTMLElement
  beforeEach(() => {
    root = render()
  })

  it('renders the fictional-simulation disclosure verbatim', () => {
    expect(root.textContent).toContain(FICTION_DISCLOSURE)
  })

  it('renders the MIXED-origin disclosure, because the screen is no longer fixture-only', () => {
    // The old "NOT CONNECTED TO THE SIMULATION ENGINE" wording would now be FALSE: part of this
    // screen genuinely is connected. Claiming otherwise would be a new dishonesty.
    expect(root.textContent).toContain(MIXED_DISCLOSURE)
    expect(root.textContent).not.toContain('NOT CONNECTED TO THE SIMULATION ENGINE')
  })

  it('provides no control that could dismiss a disclosure', () => {
    const band = root.querySelector('.disclosures')!
    expect(band.querySelector('button')).toBeNull()
    expect(band.querySelector('[aria-label*="close" i]')).toBeNull()
    expect(band.querySelector('[aria-label*="dismiss" i]')).toBeNull()
  })
})

describe('crop safety', () => {
  it('every panel carries its own fictional-world marker', () => {
    // A cropped screenshot of one panel must still declare that the world is fictional. The
    // treatment is now compact rather than a full-width word, but it is still present per panel.
    const root = render()
    const panels = Array.from(root.querySelectorAll('.panel'))
    expect(panels.length).toBeGreaterThan(4)
    for (const p of panels) {
      expect(p.querySelector('.fmark'), `panel missing fiction mark: ${p.className}`).not.toBeNull()
    }
  })

  it('every panel carries a compact origin badge with a letter, not colour alone', () => {
    const root = render()
    for (const p of Array.from(root.querySelectorAll('.panel'))) {
      const badge = p.querySelector('.ob')
      expect(badge, `panel missing origin badge: ${p.className}`).not.toBeNull()
      expect(badge!.querySelector('.ob__code')?.textContent?.trim()).toBeTruthy()
      // Screen-reader text spells the origin out; the letter is not the only signal.
      expect(badge!.querySelector('.u-sr')?.textContent?.trim()).toBeTruthy()
    }
  })

  it('the fiction mark carries text, not only an icon', () => {
    const root = render()
    for (const m of Array.from(root.querySelectorAll('.fmark'))) {
      expect(m.textContent?.trim()).toContain('FICTIONAL')
    }
  })
})

describe('engine versus fixture', () => {
  it('engine and fixture panels are visibly distinguished', () => {
    const root = render()
    const engine = root.querySelectorAll('.ob--engine')
    const fixture = root.querySelectorAll('.ob--fixture')
    expect(engine.length).toBeGreaterThan(0)
    expect(fixture.length).toBeGreaterThan(0)
    // Different letters, not merely different colours.
    expect(engine.item(0)?.querySelector('.ob__code')?.textContent).toBe('E')
    expect(fixture.item(0)?.querySelector('.ob__code')?.textContent).toBe('F')
  })

  it('the fixture panel says plainly that the engine does not model its content', () => {
    const root = render()
    const intel = root.querySelector('.panel--intel')!
    expect(intel.querySelector('.ob--fixture')).not.toBeNull()
    expect(intel.textContent).toMatch(/engine models no/i)
  })

  it('marks the connection state so a recorded snapshot is not shown as live', () => {
    const snap = render(initialSnapshot())
    expect(snap.querySelector('.tb__v--stale')?.textContent).toBe('SNAPSHOT')

    const live = render({ ...initialSnapshot(), connection: 'live' })
    expect(live.querySelector('.tb__v--live')?.textContent).toBe('LIVE')
  })

  it('renders an honest unavailable state when the backend cannot be reached', () => {
    const root = render({ ...initialSnapshot(), connection: 'unavailable', error: 'refused' })
    expect(root.querySelector('.tb__v--stale')?.textContent).toBe('UNAVAILABLE')
    expect(root.querySelector('.sysrow__v--warn')?.textContent).toBe('OFFLINE')
    // Engine-sourced panels must not still claim engine origin when the engine is unreachable.
    expect(root.querySelector('.panel--crisis .ob--unavailable')).not.toBeNull()
  })
})

describe('no fabricated precision', () => {
  it('displays no numeric confidence percentage anywhere', () => {
    const text = render().textContent ?? ''
    expect(text).not.toMatch(/\d+\s?%\s*(confidence|certain)/i)
  })

  it('reports confidence as not-applicable rather than inventing one', () => {
    const root = render()
    expect(root.textContent).toMatch(/the engine computes, it does not estimate/i)
  })

  it('only uses the approved epistemic and confidence vocabulary', () => {
    const p = initialSnapshot().projection
    for (const group of [p.stages, p.cohorts, p.government_options]) {
      for (const entry of group as Array<{ epistemic_status: string; confidence?: string }>) {
        expect(ALLOWED_STATUS).toContain(entry.epistemic_status)
        if (entry.confidence) expect(ALLOWED_CONF).toContain(entry.confidence)
      }
    }
  })
})

describe('absence handling', () => {
  it('the decision rail distinguishes "nothing changed" from an empty list', () => {
    // Zero decisions is a RESULT, not a blank. It must say why.
    const run = initialSnapshot()
    const quiet: RunResult = {
      ...run,
      projection: {
        ...run.projection,
        government_options: run.projection.government_options.map((o) => ({ ...o, value: 'AVAILABLE' })),
      },
    }
    const root = render(quiet)
    expect(root.querySelector('.ditem--none')).not.toBeNull()
    expect(root.querySelector('.ditem--none')?.textContent).toMatch(/below every declared threshold/i)
    expect(root.querySelector('.rail__count')?.textContent).toBe('0')
  })

  it('does not render an unavailable capability as a zero', () => {
    const root = render()
    const text = root.textContent ?? ''
    // The options panel states the absence of cost/effect rather than printing 0.
    expect(text).toMatch(/computes no cost or effect/i)
  })
})

describe('honest scope', () => {
  it('marks unbuilt screens as not built', () => {
    const root = render()
    const disabled = Array.from(root.querySelectorAll('.nav__item.is-disabled'))
    expect(disabled.length).toBe(4)
    for (const d of disabled) expect(d.textContent).toContain('not built')
  })

  it('states that the run is ephemeral and not a replay', () => {
    expect(render().textContent).toMatch(/not persisted, not a replay/i)
  })

  it('does not claim replay, event sourcing or persistence anywhere on screen', () => {
    const text = (render().textContent ?? '').toLowerCase()
    expect(text).not.toMatch(/\breplay(ing|able)?\b(?!\s*[.,]?\s*$)(?![^.]*not)/)
    expect(text).not.toContain('event sourcing')
    expect(text).not.toContain('event-sourced')
  })

  it('states that population affects magnitude only', () => {
    const root = render()
    expect(root.textContent).toMatch(/population affects aggregate magnitude only/i)
  })

  it('says the map is invented geography', () => {
    expect(render().textContent).toMatch(/invented geography|no real-world map data/i)
  })
})

describe('structure and accessibility basics', () => {
  it('renders the landmark regions', () => {
    const root = render()
    expect(root.querySelector('nav[aria-label="Primary"]')).not.toBeNull()
    expect(root.querySelector('main#main')).not.toBeNull()
    expect(root.querySelector('aside[aria-label="Decisions and inspector"]')).not.toBeNull()
    expect(root.querySelector('[aria-label="Scenario and run status"]')).not.toBeNull()
    expect(root.querySelector('[aria-label="Prototype disclosures"]')).not.toBeNull()
  })

  it('gives the map a descriptive text alternative', () => {
    const label = render().querySelector('.map')?.getAttribute('aria-label') ?? ''
    expect(label).toMatch(/fictional/i)
    expect(label.length).toBeGreaterThan(40)
  })

  it('gives every selectable element an accessible name', () => {
    const root = render()
    const selectable = Array.from(root.querySelectorAll('[data-card-id][role="button"]'))
    expect(selectable.length).toBeGreaterThan(6)
    for (const el of selectable) {
      expect(el.getAttribute('aria-label')?.trim(), el.className).toBeTruthy()
      expect(el.getAttribute('tabindex')).toBe('0')
    }
  })

  it('uses headings rather than styled text for panel titles', () => {
    const root = render()
    const titles = Array.from(root.querySelectorAll('.panel__title'))
    expect(titles.length).toBeGreaterThan(4)
    for (const t of titles) expect(t.tagName).toBe('H2')
  })

  it('does not communicate option status by colour alone', () => {
    const root = render()
    for (const s of Array.from(root.querySelectorAll('.opt__state'))) {
      // The status word itself is present, not just a coloured dot.
      expect(s.textContent?.trim()).toMatch(/AVAILABLE|CONSTRAINED|ENABLED/)
    }
  })

  it('opens with the inspector populated rather than empty', () => {
    const root = render()
    expect(root.querySelector('#inspector-body .insp__title')).not.toBeNull()
  })
})

describe('engine values reach the screen', () => {
  it('renders the political pressure the run actually produced', () => {
    const run = initialSnapshot()
    const political = run.projection.stages.find((s) => s.field === 'political_pressure')!
    const root = render(run)
    expect(root.querySelector('.bignum__value')?.textContent).toBe(political.value.toFixed(4))
  })

  it('renders every cohort from the projection', () => {
    const run = initialSnapshot()
    const root = render(run)
    expect(root.querySelectorAll('.cohort').length).toBe(run.projection.cohorts.length)
  })

  it('shows the population-weighted aggregate, not a plain mean', () => {
    const run = initialSnapshot()
    const p = run.projection
    const total = p.cohorts.reduce((n, c) => n + c.represents_population, 0)
    const weighted = p.cohorts.reduce((n, c) => n + c.value * c.represents_population, 0) / total
    const root = render(run)
    expect(root.querySelector('.cohorts__agg-val')?.textContent).toBe(weighted.toFixed(4))
  })

  it('shows the real rule-pack version', () => {
    expect(render().textContent).toContain('kestral-causal-slice@1.0.0')
  })
})

describe('crop safety is visual, not merely textual', () => {
  it('the fictional-world marker text is not screen-reader-only', () => {
    // Regression guard. A shared screenshot shows pixels, not textContent: hiding the word behind
    // a .u-sr clip would keep the earlier assertion green while defeating what it protects.
    const root = render()
    const marks = Array.from(root.querySelectorAll('.fmark__txt'))
    expect(marks.length).toBeGreaterThan(4)
    for (const m of marks) {
      expect(m.classList.contains('u-sr'), 'fiction text must be visible').toBe(false)
      expect((m as HTMLElement).style.position).not.toBe('absolute')
    }
  })
})

describe('bounded defect-correction pass', () => {
  it('renders all seven propagation rows, including political pressure', () => {
    // The political-pressure row was the one clipped at 1440x900. It must never be dropped to
    // make the panel fit — the fix belongs in layout, not in removing a chain value.
    const root = render()
    const rows = Array.from(root.querySelectorAll('.chainsum__step'))
    expect(rows.length).toBe(7)
    expect(rows.map((r) => r.querySelector('.chainsum__name')?.textContent)).toContain('Politics')
  })

  it('keeps narrow-panel subtitles to short, single-line copy', () => {
    // jsdom cannot measure wrapping, so this guards the input to it: short copy plus the
    // nowrap/ellipsis treatment in styles.css is what keeps these to one line.
    const root = render()
    for (const sub of Array.from(root.querySelectorAll('.panel__sub'))) {
      expect(sub.textContent!.trim().length, sub.textContent!).toBeLessThanOrEqual(46)
    }
  })

  it('puts the title and origin markers on their own header row', () => {
    // The markers previously shared the subtitle line and forced it to wrap.
    const root = render()
    for (const p of Array.from(root.querySelectorAll('.panel'))) {
      const row = p.querySelector('.panel__headrow')
      expect(row, p.className).not.toBeNull()
      expect(row!.querySelector('.panel__title')).not.toBeNull()
      expect(row!.querySelector('.ob')).not.toBeNull()
      expect(row!.querySelector('.fmark')).not.toBeNull()
      // The subtitle is a sibling of that row, never inside it.
      expect(row!.querySelector('.panel__sub')).toBeNull()
    }
  })

  it('never renders unknown or unavailable as a zero', () => {
    const root = document.createElement('div')
    mount(root, { ...initialSnapshot(), connection: 'unavailable', error: 'refused' }, 'analysis')
    const unavailable = Array.from(root.querySelectorAll('.ob--unavailable'))
    expect(unavailable.length).toBeGreaterThan(0)
    for (const el of unavailable) {
      expect(el.closest('.panel')?.textContent).not.toMatch(/\b0\.000\b/)
    }
  })

  it('drops the chart legend only when a single series makes it redundant', () => {
    // One-series legends repeat the panel title and subtitle. Multi-series charts still need one.
    const root = render()
    const crisis = root.querySelector('.panel--crisis')!
    expect(crisis.querySelector('.chart__svg')).not.toBeNull()
    expect(crisis.querySelector('.chart__legend')).toBeNull()
    // The series is still named, so nothing became unlabelled.
    expect(crisis.querySelector('.panel__sub')?.textContent).toContain('Political pressure')
  })
})

describe('polish pass keeps disclosures out of collapsed regions', () => {
  it('shows confidence status in the default provenance view, not only inside a disclosure', () => {
    // Moving explanatory PROSE into <details> is fine; moving the STATUS itself would hide an
    // honesty property behind a click. The status must be visible without interaction.
    const root = render()
    const grid = root.querySelector('.panel--prov .provgrid')!
    expect(grid.textContent).toContain('NOT_APPLICABLE')
    expect(grid.closest('details')).toBeNull()
  })

  it('keeps the canonical confidence sentence verbatim', () => {
    expect(render().textContent).toMatch(/the engine computes, it does not estimate/i)
  })

  it('states urgency without inventing a deadline the engine cannot support', () => {
    // The engine has no clock. Any countdown, due time or expiry would be fabricated.
    const text = (render().textContent ?? '').toLowerCase()
    expect(text).not.toMatch(/\b\d+\s*(h|hr|hrs|hours|min|mins|minutes)\s*(left|remaining|to go)\b/)
    expect(text).not.toMatch(/deadline|expires|due (in|by)|countdown|time remaining/)
  })

  it('derives decision domains from the option driven_by field', () => {
    const root = render()
    const primary = root.querySelector('.ditem--primary')!
    expect(primary.querySelectorAll('.dom__chip').length).toBeGreaterThan(0)
    // The affordance inspects; it must never read as execution.
    expect(primary.querySelector('.ditem__act')?.textContent).toBe('Inspect')
    expect(root.querySelector('.rail__foot')?.textContent).toMatch(/nothing can be\s+submitted, priced, validated or executed/i)
  })

  it('labels metric direction only as description of ticks already produced', () => {
    const root = render()
    const dirs = Array.from(root.querySelectorAll('.krow__dir')).map((d) => d.textContent?.trim())
    for (const d of dirs) expect(['RISING', 'STABLE', 'EASING', 'UPSTREAMEASING', '—']).toContain(d)
    // No rate, no forecast, no per-tick extrapolation.
    expect(root.querySelector('.panel--metrics')?.textContent).not.toMatch(/\/tick|per tick|forecast|projected/i)
  })
})

describe('lagged-response explanation is derived, not narrated', () => {
  const rising = (n: number, from = 0.02, to = 0.15): number[] =>
    Array.from({ length: n }, (_, i) => from + ((to - from) * i) / (n - 1))
  const falling = (n: number, from = 0.6, to = 0.3): number[] =>
    Array.from({ length: n }, (_, i) => from + ((to - from) * i) / (n - 1))

  /** Builds a run whose trajectory we control, leaving projection metadata untouched. */
  function withTrajectory(political: number[], upstream: number[]): RunResult {
    const base = initialSnapshot()
    const n = political.length
    return {
      ...base,
      trajectory: Array.from({ length: n }, (_, i) => ({
        tick: i + 1,
        political_pressure: political[i] ?? 0,
        insurer_risk: upstream[i] ?? 0,
        rerouting_level: upstream[i] ?? 0,
        employment_pressure: upstream[i] ?? 0,
        household_expectation_pressure: upstream[i] ?? 0,
        incident_severity: upstream[i] ?? 0,
        narrative_attention: political[i] ?? 0,
        collective_activity: political[i] ?? 0,
      })),
    }
  }

  it('shows the explanation when political rises while upstream indicators ease', () => {
    const root = render(withTrajectory(rising(20), falling(20)))
    expect(root.querySelector('.lagnote__chip')?.textContent).toBe('LAGGED RESPONSE')
    expect(root.querySelector('.lagnote')?.textContent).toMatch(
      /upstream disruption is easing, but political pressure is\s+still rising/i,
    )
    expect(root.querySelector('.bignum__dir')?.textContent).toBe('STILL RISING')
  })

  it('does NOT show it when upstream indicators are also rising', () => {
    // Same rising political pressure — but nothing is easing, so there is no lag story to tell.
    const root = render(withTrajectory(rising(20), rising(20, 0.1, 0.6)))
    expect(root.querySelector('.lagnote')).toBeNull()
    expect(root.querySelector('.bignum__dir')).toBeNull()
  })

  /** Rises to a late peak, then declines slowly — the shape the real Kestral run produces. */
  const latePeak = (n: number): number[] =>
    Array.from({ length: n }, (_, i) => {
      const peak = Math.floor(n * 0.6)
      return i <= peak ? 0.02 + (0.13 * i) / peak : 0.15 - 0.0008 * (i - peak)
    })
  /** Peaks early, then falls steeply. */
  const earlyPeak = (n: number): number[] =>
    Array.from({ length: n }, (_, i) => {
      const peak = Math.floor(n * 0.2)
      return i <= peak ? 0.2 + (0.6 * i) / peak : 0.8 - 0.03 * (i - peak)
    })

  it('shows the peak-lag variant when political peaked later than every upstream indicator', () => {
    // This is what the real run shows at tick 20: political pressure has already turned over, but
    // it peaked AFTER its causes and is holding nearer its peak. Claiming "still rising" here
    // would be false, so the copy must adapt rather than the gate loosening.
    const root = render(withTrajectory(latePeak(20), earlyPeak(20)))
    expect(root.querySelector('.lagnote__chip')?.textContent).toBe('LAGGED RESPONSE')
    expect(root.querySelector('.lagnote')?.textContent).toMatch(/peaked \d+\s+ticks later, at tick \d+/i)
    expect(root.querySelector('.lagnote')?.textContent).not.toMatch(/still rising/i)
    expect(root.querySelector('.bignum__dir')?.textContent).toMatch(/^PEAKED t\d+ · LAGGED$/)
  })

  it('does NOT show it when political peaked no later than upstream', () => {
    // Both peak early: there is no propagation delay to demonstrate.
    const root = render(withTrajectory(earlyPeak(20), earlyPeak(20)))
    expect(root.querySelector('.lagnote')).toBeNull()
  })

  it('does NOT show it when political has given up more of its peak than upstream', () => {
    const collapsing = Array.from({ length: 20 }, (_, i) => (i <= 17 ? 0.02 + 0.13 * (i / 17) : 0.01))
    const root = render(withTrajectory(collapsing, falling(20, 0.6, 0.58)))
    expect(root.querySelector('.lagnote')).toBeNull()
  })

  it('does NOT show it when the trajectory is too short to establish direction', () => {
    const root = render(withTrajectory(rising(3), falling(3)))
    expect(root.querySelector('.lagnote')).toBeNull()
  })

  it('requires the mechanism to declare a lag, not just the numbers to look right', () => {
    // The claim is about declared lag. With lag_ticks stripped to 0 the numbers are unchanged,
    // so a story-driven implementation would still render it. This one must not.
    const run = withTrajectory(rising(20), falling(20))
    const noLag: RunResult = {
      ...run,
      projection: {
        ...run.projection,
        stages: run.projection.stages.map((s) =>
          s.field === 'political_pressure' ? { ...s, lag_ticks: 0 } : s,
        ),
      },
    }
    expect(render(noLag).querySelector('.lagnote')).toBeNull()
  })

  it('qualifies upstream easing labels only while the lagged state holds', () => {
    const lagged = render(withTrajectory(rising(20), falling(20)))
    expect(lagged.querySelector('.krow__dir-q')?.textContent).toBe('UPSTREAM')

    const plain = render(withTrajectory(falling(20, 0.5, 0.1), falling(20)))
    expect(plain.querySelector('.krow__dir-q')).toBeNull()
  })

  it('builds the inspector explanation from mechanism metadata, not fixed prose', () => {
    const root = render(withTrajectory(rising(20), falling(20)))
    const lagBlock = root.querySelector('.insp__lag')!
    expect(lagBlock).not.toBeNull()
    const political = initialSnapshot().projection.stages.find((s) => s.field === 'political_pressure')!
    // The declared lag and lifecycle come from the projection, not from a literal in the view.
    expect(lagBlock.textContent).toContain(`${political.lag_ticks} tick(s)`)
    expect(lagBlock.textContent).toContain(political.lifecycle)
    for (const f of political.source_fields) {
      expect(lagBlock.textContent).toContain(f.replace('chain.', '').replace(/_/g, ' '))
    }
  })

  it('keeps the full semantic metric name available despite the short visible label', () => {
    const root = render()
    const labels = Array.from(root.querySelectorAll('.krow__label'))
    expect(labels.length).toBe(4)
    for (const el of labels) {
      const full = el.getAttribute('title') ?? ''
      expect(full.length).toBeGreaterThan((el.textContent ?? '').length - 1)
      expect(full.trim()).toBeTruthy()
    }
    // And the row's accessible name still carries the projection's own label.
    const rows = Array.from(root.querySelectorAll('.krow'))
    for (const r of rows) expect(r.getAttribute('aria-label')).toBeTruthy()
  })

  it('does not describe the lag as a prediction', () => {
    // Scoped to the lag content: the global disclosure legitimately contains the word
    // "prediction" (it denies making one), so a whole-document match would be meaningless.
    const root = render(withTrajectory(rising(20), falling(20)))
    const scoped = [
      ...Array.from(root.querySelectorAll('.lagnote')),
      ...Array.from(root.querySelectorAll('.insp__lag')),
    ]
      .map((el) => el.textContent ?? '')
      .join(' ')
      .toLowerCase()
    expect(scoped.length).toBeGreaterThan(80)
    expect(scoped).not.toMatch(/will (rise|continue|peak|fall)|expected to|forecast|projected|predict/)
  })
})
