# P0.5 — the first cross-tier societal-response mechanism

**Status:** DRAFT, pending owner review · **Date:** 19 July 2026 · **Rule pack:** `kestral-causal-slice@1.0.0`

---

## The claim this licenses, and its exact limit

> **MERIDIAN currently implements one cross-tier societal-response mechanism in a fictional scenario.**

Nothing broader. One chain existing does **not** make MERIDIAN a simulated society, and does not
license "crises propagate through populations, media, markets and institutions" as a general
statement. It licenses precisely the sentence above.

Before P0.5 the three tiers did not causally influence one another at all — the apparent meso→macro
movement A3 found was shared-RNG stream displacement, not causality. **This is the first genuine
propagation path in the project.**

---

## Stage order and mechanisms

| Stage | Mechanism | Version | Source → target | Lag | Lifecycle |
|---|---|---|---|---|---|
| 1 | `M-INCIDENT-OBS` | 1.0.0 | `incident_severity` → itself | 0 | salience decay while unreinforced *(attention-like)* |
| 2 | `M-INSURER-RISK` | 1.0.0 | `incident_severity` → `insurer_risk` | **1** | decays **only** while no incident is active |
| 3 | `M-PREMIUM-PRESSURE` | 1.0.0 | `insurer_risk` → `premium_pressure` | 0 | tracks source; no independent decay |
| 3 | `M-CARRIER-REROUTE` | 1.0.0 | `premium_pressure` → `rerouting_level` | 0 | **cooldown**: 8-tick minimum commitment, then unwinds only if pressure < 0.20 |
| 4 | `M-PORT-EXPOSURE` | 1.0.0 | `rerouting_level` → `port_activity_deficit`, `employment_pressure` | **1** | follows routing only; **no random recovery**; employment restores slower than it cuts |
| 5 | `M-HOUSEHOLD-EXPECT` | 1.0.0 | `employment_pressure` + cohort exposure → `economic_concern`, `household_expectation_pressure` | **1** | improves only when employment improves, and more slowly |
| 6 | `M-NARRATIVE-ACTIVITY` | 1.0.0 | `household_expectation_pressure` → `narrative_attention`, `collective_activity` | **1** | attention-like: **may** decay on absence of stimulus alone |
| 7 | `M-POLITICAL-PRESSURE` | 1.0.0 | `narrative_attention` + `collective_activity` → `political_pressure` | **1** | persists longer than media attention |
| 7 | `M-GOV-OPTIONS` | 1.0.0 | `political_pressure` → `government_options` | 0 | threshold-driven, **bidirectional** |

**Every recovery rule names its causal reason.** "No new stimulus" is accepted **only** for the two
attention-like quantities. Economic and institutional state recovers when its own inputs improve,
never because time passed.

**Lag is an explicit read of a recorded past.** A mechanism with `lag_ticks=1` reads
`chain.previous[field]`, snapshotted by a bookkeeping transition at the end of the prior tick.
Stage numbers are non-decreasing, so a later stage may read an earlier stage's output from the
same tick while feedback always waits for the next — **no same-tick causal cycles**.

---

## Measured evidence

**Counterfactual verification.** A counterfactual disables a MECHANISM, never the incident. In
both counterfactuals below the incident is still present and active at severity 0.5500 —
identical to the full run — while the baseline never had one (0.0000, `incident_active=False`).
Disabling `M-CARRIER-REROUTE` shows this most sharply: `insurer_risk` (0.5773) and
`premium_pressure` (0.5810) are preserved *bit-identically*, `rerouting_level` — the disabled
mechanism's own target — is prevented at 0.0000, and everything downstream collapses to zero.

Seed `88213`, 20 ticks (**one tick = 6 simulated hours for this scenario only**; 20 ticks = 5
simulated days). Tick durations are scenario-scoped — nothing in the engine assumes six hours.

| Run | insurer | reroute | employ | household | political | options |
|---|---|---|---|---|---|---|
| **Baseline** (no incident) | 0.0000 | 0.0000 | 0.0000 | 0.0000 | **0.0000** | all AVAILABLE |
| **Incident** | 0.5773 | 0.5875 | 0.3763 | 0.1416 | **0.1495** | publish ENABLED, quiet CONSTRAINED |
| **CF: `M-INSURER-RISK` disabled** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | **0.0000** | all AVAILABLE |
| **CF: `M-CARRIER-REROUTE` disabled** | 0.5773 | 0.0000 | 0.0000 | 0.0000 | **0.0000** | all AVAILABLE |

*(Incident severity is 0.5500 in the incident run and in **both** counterfactuals; 0.0000 in the
baseline. That column is what makes a disabled mechanism distinguishable from a removed incident.)*

Propagation is visible tick by tick: incident at t1 → insurer reprices t2 (the declared lag) →
rerouting t3 → employment t4 → household t4-6 → narrative t6 → political t8 → `publish_legal_advice`
ENABLED at t10 → `pursue_quiet_diplomacy` CONSTRAINED at t14.

**`declare_emergency_powers` correctly stays AVAILABLE.** A five-day shipping disruption should not
unlock emergency powers. An option that never fires in this scenario is a correct result, and it is
what distinguishes a causal model from a one-way ratchet.

**Extended no-new-input stability and recovery test:** political pressure peaks at 0.1495 (t20)
and returns to **0.000000** by t520. Nothing accumulates indefinitely.

**520 ticks is a stability test, not the demonstration horizon.** The Kestral Strait
demonstration horizon remains **20 ticks — six simulated hours per tick, five simulated days**.
The long run exists only to prove the chain returns to rest rather than plateauing upward.

---

## Population weighting

`represents_population` was declared in the schema but **read by no code** before P0.5, with the
demo data wrong by 63× and nothing detecting it. It now weights every society-wide aggregate:

```
household_expectation_pressure = Σ(concern_c × population_c) / Σ(population_c)
```

Verified to 1e-9 against a directly computed weighted mean.

**Size affects aggregate magnitude only.** It says nothing about whether a cohort is right, and
nothing about what any individual does. Two tests enforce the distinction: the smallest cohort
(coastal fishing, 14,200 people, exposure 0.81) carries the **highest** individual concern
(0.3299) while contributing only 0.95% of the aggregate; and concern ranks by declared exposure,
never by population.

Making that cohort the demographic majority raises society-wide pressure — tested.

---

## Determinism and boundary

Every chain mutation passes through `TransitionService`; mechanisms are pure functions returning
*proposed* transitions and mutate nothing themselves. Each applied transition records mechanism id,
mechanism version, source fields, draw references and causal parents.

Verified inside the chain, not merely in the abstract: adding an unrelated cohort does not move any
existing cohort's result; reversing cohort order changes nothing; repeated runs serialise
byte-identically. **No LLM or network call is reachable from the authoritative path** — enforced by
a test that patches `socket.connect` to raise and asserts the gateway is never called.

---

## Two defects found and fixed during implementation

**The chain started on its own.** Unscaled turnout jitter made `collective_activity` drift upward
from zero in a run with *no incident at all* — 0.0058 at t20. Bounded noise on a live quantity is
modelling; noise on a dead one manufactures activity. Jitter is now scaled by current activity, so
zero activity yields zero noise. Baseline is now exactly 0.0000 across every field.

**The demonstration horizon carried no information.** With incident decay at 0.04/tick the incident
faded to nothing inside 20 ticks, the chain fizzled, and no option ever changed. Decay is now
0.015/tick — a sustained blockade, which is what the scenario describes, rather than a one-off
event. Option thresholds were recalibrated to the scale political pressure actually occupies,
established by running the chain rather than guessed in advance.

Also corrected: `rule_pack_version` reported `unversioned-inline-0` while
`kestral-causal-slice@1.0.0` was running. A version field that misreports its own rules is worse
than no field.

---

## Honest limits

- **Every coefficient is an authored fictional value.** None is calibrated against data, none is
  empirically defensible, and nothing here supports any claim about real-world behaviour.
- **One chain is not a society.** No media model, no market model, no institutional decision-making,
  no individual households — household effects are represented through weighted cohorts only.
- The legacy `ACTION_EFFECTS` table remains unversioned inline code, and the **macro saturation
  critical is untouched** — P0.5 deliberately did not repair unrelated legacy macro variables.
- No legality, authority, resource or feasibility validation exists (blocker B1 stands).
- `entities` and `relationships` remain empty. No persistent entity model exists.

## Still not implemented, and not claimed

Replay · event sourcing · state hashing · persistence · causal reconstruction · live model
integration · role-based access enforcement. Causal parents record adjacency within a tick; nothing
replays from them and no state can be rebuilt. That is P0.6.

---

## Read-only projection

`app/simulation/projection.py` produces a derived view for a later UI-integration block. It never
writes, never draws randomness and never calls a model — asserted by a test that renders it 25
times and compares canonical serialisation.

Every entry carries `origin: "engine"` because it genuinely came from the engine. That matters
because C0 renders fixtures marked `origin: "fixture"`: when both appear together the distinction
must be **per-record, never per-page**, or a live build silently launders fixture values into
apparent engine output. Confidence is `NOT_APPLICABLE` throughout — the engine computes values, it
does not estimate them, and inventing a confidence would be fabricated precision.

The payload states its own `not_implemented` list so a consumer cannot infer capabilities from its
shape.

**C0 remains fixture-only.** Nothing was connected to the frontend in this block.

---

## Test evidence

**100 passed** — 62 pre-existing (unchanged) + 38 new. Covering all 20 required properties: chain
triggering, no spontaneous start, each link's effect, three counterfactuals, population weighting,
order independence, unrelated-entity isolation, byte-identical repeats, boundary enforcement,
bounds, cooldown, lag, no-cycle, no network, saturation recovery, and projection read-only-ness.
