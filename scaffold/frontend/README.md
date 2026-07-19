# MERIDIAN — C0 interactive prototype

> ## ⚠ FIXTURE DATA ONLY — NOT CONNECTED TO THE SIMULATION ENGINE
>
> Every value in this application is hand-authored fixture data. Nothing here is produced by the
> MERIDIAN engine. There is **no** live model call, **no** authoritative validation, **no** real
> cross-tier propagation, **no** event sourcing, **no** replay, **no** state hashing, **no**
> persistence, **no** role-based access enforcement and **no** tier promotion.
>
> The Republic of Vantara is fictional. No real nation, organisation or person is depicted.

**Status:** C0 gate, Strategic Command Centre only. Four of the five slice screens are specified
but **not built**, and are shown disabled in the navigation so the shell's shape is honest.

---

## Run it

```bash
cd scaffold/frontend
npm install
npm run dev            # http://localhost:5173
```

Other commands:

```bash
npm test               # 21 honesty + rendering tests (vitest + jsdom)
npm run build          # tsc --noEmit && vite build
npm run screenshot     # full-viewport capture + crop-invariance check (needs the dev server running)
```

`npm run screenshot` requires a one-off `npx playwright install chromium`.

**Verified 19 July 2026** — Node v24.15.0, npm 11.12.1, Windows 10. `npm install` added 98
packages in 22s; `tsc --noEmit` clean; 21/21 tests pass; screenshot captured with zero console
errors.

---

## What the screen demonstrates

The **societal propagation chain is the visual spine**. That is the deliberate design decision that
stops this reading as a military map, a chatbot, a metrics dashboard or a cabinet-only interface:
the centre of the screen is a crisis moving through insurers, carriers, port workers, households,
media, families and politics — people and institutions, not units on terrain.

The chain is **hand-authored** (founder decision G3). MERIDIAN's three simulation tiers do not
causally influence one another today, so no computed propagation exists to render. The screen says
so, in the interface, next to the chain: *"Hand-authored fixture trace — not computed, not
simulated, not live."*

## Honesty mechanisms

These are load-bearing, not decoration. The visual encoding **is** the honesty guarantee.

| Mechanism | Where |
|---|---|
| Two persistent disclosures, verbatim, non-dismissible, repeated top **and** bottom | `components/disclosure.ts` |
| `FICTIONAL` + `FIXTURE` markers on **every card**, so any crop still declares itself | `components/provenance.ts` |
| Epistemic status as glyph **+** text **+** colour — never colour alone | `components/epistemic.ts` |
| Structural left-gutter rule coloured by status — survives cropping and forced-colors | `styles.css` |
| Unknown / unavailable / zero render **distinctly** | `absenceValue()` |
| No numeric confidence percentages anywhere — asserted by test | `tests/honesty.test.ts` |
| Every chain hop names the **mechanism** behind each contributor | `strategic-command-centre.ts` |
| Non-materialised entities marked `AGGREGATE`; never given invented individual detail | founder decision G1 |
| Build-time assertion that every record carries a full fixture envelope | `assertEnvelope()` |
| A queue item with no affordance throws — a status indicator is not a decision | `verifyFixtureHonesty()` |

Hop 8, *Government options*, renders as `UNKNOWN` with an explicit note that no engine evaluates
outcomes. The gap is shown rather than hidden — that is the point.

## Known limitations

- **Dark theme only. No accessibility conformance is claimed.** Research finding C3 records that
  dark-only cannot be shipped and called accessible; light and high-contrast themes are required
  before any such claim, and do not exist.
- **Screenshot viewport is 1600×1400.** The screen is dense — ten content categories plus per-claim
  provenance. At 1600×1000 the reaction panels and event stream require scrolling. Content was not
  hidden to hit a height target.
- Keyboard reachable with visible focus, but **no full keyboard model** — no F6 region cycling, no
  roving tabindex, no skip links.
- Screen-reader behaviour is **untested**. Landmarks and `role="log"` are present but unverified.
- No light/high-contrast theme, no reduced-motion testing beyond the token-level media query.
- Selection state is DOM-only. There is no router and no persisted state.

## Layout

```
FICTIONAL SIMULATION …   |  INTERACTIVE PROTOTYPE — FIXTURE DATA …     ← both, non-dismissible
MERIDIAN · Vantara · scenario · tick · clock · role · EXPLORE
┌──────────┬────────────────────────────────────┬──────────────────┐
│ nav      │ crisis header                      │ decisions        │
│ (4 shown │ propagation chain (8 hops, 2 cols) │ awaiting you     │
│  as NOT  │ reaction panels (4)                │ inspector        │
│  BUILT)  │                                    │                  │
└──────────┴────────────────────────────────────┴──────────────────┘
event stream (low-relevance rows dimmed, never removed)
FICTIONAL SIMULATION …   |  INTERACTIVE PROTOTYPE — FIXTURE DATA …     ← repeated for crop safety
```

## Files

| Path | Purpose |
|---|---|
| `src/fixtures/types.ts` | Fixture envelope contract + `assertEnvelope` honesty gate |
| `src/fixtures/kestral-strait.v1.ts` | Versioned scenario fixture (`kestral-strait` v1.0.0) |
| `src/tokens.css` | Design tokens — original visual language, no trade dress |
| `src/components/` | `disclosure`, `epistemic`, `provenance` |
| `src/screens/strategic-command-centre.ts` | The screen |
| `src/main.ts` | Shell, navigation, inspector wiring |
| `tests/honesty.test.ts` | 21 tests, mostly asserting honesty properties |
| `scripts/screenshot.mjs` | Viewport capture + crop-invariance check |
| `legacy-dev-stub.html` | The previous minimal dev harness, preserved |

Nothing here is committed, pushed or published.
