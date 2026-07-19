"""The Kestral Strait societal-response mechanisms — Phase 0 item P0.5.

MERIDIAN's first real cross-tier causal channel. Before this, the three tiers did not causally
influence one another at all: the apparent meso→macro movement A3 found was shared-RNG stream
displacement, not causality. These mechanisms are the first genuine propagation path.

WHAT THIS IS
------------
ONE chain, in a fictional scenario:

    maritime incident → insurer risk → insurance-cost pressure → carrier rerouting
    → port and employment exposure → household/cohort expectations → narrative and family
    activity → political pressure → government options

WHAT THIS IS NOT
----------------
Not a society model, not comprehensive, not validated, not predictive, and not a claim about the
real world. Every coefficient is an authored fictional value (see `rules/kestral_v1.py`). One
chain existing does not make MERIDIAN a simulated society; it makes the claim
"MERIDIAN currently implements one cross-tier societal-response mechanism in a fictional scenario"
true, and nothing broader.

HOW A MECHANISM WORKS
---------------------
Each is a PURE FUNCTION of (immutable state view, draw service) returning PROPOSED transitions.
No mechanism mutates anything. The runner passes proposals through `TransitionService`, which is
still the only writer. No LLM and no network call is reachable from here.

LAG. A mechanism declaring `lag_ticks=1` reads `state.chain.previous[field]` — a value recorded by
a bookkeeping transition at the end of the prior tick — never the live value. That makes a lag an
explicit read of a recorded past, not an accident of stage ordering, and it is what prevents
same-tick causal cycles: a later stage may read an earlier stage's output from THIS tick, but
feedback to an earlier stage always waits for the next one.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

from .draws import DeterministicDrawService
from .rules import kestral_v1 as R
from .state import AuthoritativeState
from .transitions import Transition, TransitionOrigin, TransitionType


@dataclass(frozen=True)
class Mechanism:
    """One declared causal link."""

    id: str
    version: str
    stage: int
    stage_name: str
    source_fields: tuple[str, ...]
    target_fields: tuple[str, ...]
    lag_ticks: int
    lifecycle: str
    fn: Callable[[AuthoritativeState, DeterministicDrawService], list[Transition]]


def _lagged(state: AuthoritativeState, field: str, lag: int) -> float:
    """Read a source value honouring the declared lag.

    lag 0 → this tick's live value (a later stage reading an earlier stage's output).
    lag ≥1 → the value recorded at the end of the previous tick.
    """
    if lag == 0:
        return float(getattr(state.chain, field))
    return float(state.chain.previous.get(field, 0.0))


def _set(
    field: str,
    value: float,
    mech: "Mechanism",
    sources: tuple[str, ...] | None = None,
    draw_refs: list[str] | None = None,
) -> Transition:
    return Transition(
        type=TransitionType.SET_CHAIN_SCALAR,
        origin=TransitionOrigin.ENGINE_RULE,
        payload={"field": field, "value": R.clamp(value)},
        mechanism=mech.id,
        mechanism_version=mech.version,
        source_fields=list(sources if sources is not None else mech.source_fields),
        draw_refs=draw_refs or [],
    )


# --------------------------------------------------------------------------- #
# Stage 1 — incident observation
# --------------------------------------------------------------------------- #
def m_incident(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Incident salience decays only because it is no longer being reinforced.

    Legitimate here because incident severity is an OBSERVATION quantity. It is not licence to
    decay economic or institutional state on "time passed" — those recover only when their own
    inputs improve.
    """
    c = state.chain
    if not c.incident_active:
        return []
    decayed = max(0.0, c.incident_severity - R.INCIDENT_DECAY_PER_TICK)
    out = [_set("incident_severity", decayed, M_INCIDENT)]
    if decayed < R.INCIDENT_ACTIVE_THRESHOLD:
        # Below threshold the incident stops being an active stimulus. Downstream state does NOT
        # reset — it recovers through its own mechanisms, at its own pace.
        out.append(
            Transition(
                type=TransitionType.SET_CHAIN_SCALAR,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"field": "incident_severity", "value": 0.0},
                mechanism=M_INCIDENT.id,
                mechanism_version=M_INCIDENT.version,
                source_fields=["chain.incident_severity"],
            )
        )
    return out


# --------------------------------------------------------------------------- #
# Stage 2 — institutional risk assessment
# --------------------------------------------------------------------------- #
def m_insurer(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Underwriters reprice against the incident, one tick behind it.

    Recovery reason: risk posture relaxes ONLY while no incident is active. It is not a timer — a
    persisting incident holds the posture up indefinitely.
    """
    severity = _lagged(state, "incident_severity", R.INSURER_LAG_TICKS)
    current = state.chain.insurer_risk
    if severity > 0.0:
        target = severity
        value = R.approach(current, target, R.INSURER_GAIN)
    else:
        value = max(0.0, current - R.INSURER_DECAY_PER_TICK)
    return [_set("insurer_risk", min(value, R.INSURER_MAX), M_INSURER)]


# --------------------------------------------------------------------------- #
# Stage 3 — market and logistics response
# --------------------------------------------------------------------------- #
def m_premium(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Insurance-cost pressure tracks the insurer's risk posture within the same tick."""
    risk = _lagged(state, "insurer_risk", R.PREMIUM_LAG_TICKS)
    value = R.approach(state.chain.premium_pressure, risk, R.PREMIUM_GAIN)
    return [_set("premium_pressure", min(value, R.PREMIUM_MAX), M_PREMIUM)]


def m_reroute(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Carriers divert once cost pressure crosses a threshold, and stay diverted.

    Lifecycle: a genuine COOLDOWN, not decay. A diverted vessel is committed, so rerouting cannot
    unwind until the minimum commitment has elapsed AND pressure has fallen below the release
    threshold. Time alone is not sufficient, and neither is a pressure drop alone.
    """
    c = state.chain
    pressure = c.premium_pressure
    committed = c.rerouting_ticks_committed
    out: list[Transition] = []

    if pressure >= R.REROUTE_TRIGGER_THRESHOLD:
        value = R.approach(c.rerouting_level, pressure, R.REROUTE_GAIN)
        out.append(_set("rerouting_level", min(value, R.REROUTE_MAX), M_REROUTE))
        out.append(
            Transition(
                type=TransitionType.SET_CHAIN_SCALAR,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"field": "rerouting_ticks_committed", "value": R.REROUTE_MIN_DURATION_TICKS},
                mechanism=M_REROUTE.id,
                mechanism_version=M_REROUTE.version,
                source_fields=["chain.premium_pressure"],
            )
        )
    elif committed > 0:
        # Still committed: hold the routing posture and burn down the commitment.
        out.append(
            Transition(
                type=TransitionType.SET_CHAIN_SCALAR,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"field": "rerouting_ticks_committed", "value": committed - 1},
                mechanism=M_REROUTE.id,
                mechanism_version=M_REROUTE.version,
                source_fields=["chain.rerouting_ticks_committed"],
            )
        )
    elif pressure < R.REROUTE_RELEASE_THRESHOLD and c.rerouting_level > 0.0:
        # Commitment elapsed AND pressure released: unwind gradually.
        out.append(
            _set("rerouting_level", max(0.0, c.rerouting_level - R.REROUTE_UNWIND_PER_TICK), M_REROUTE)
        )
    return out


# --------------------------------------------------------------------------- #
# Stage 4 — port and employment exposure
# --------------------------------------------------------------------------- #
def m_port(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Port activity follows routing state; employment follows port activity, asymmetrically.

    Recovery reason is entirely "rerouting reduced" — there is NO random recovery and no timer. If
    carriers are still diverted the port stays quiet. Employment restores more slowly than it is
    cut, because rosters are easier to cancel than to rebuild.
    """
    rerouting = _lagged(state, "rerouting_level", R.PORT_LAG_TICKS)
    c = state.chain

    deficit_target = rerouting * R.PORT_DEFICIT_GAIN
    deficit = R.approach(c.port_activity_deficit, deficit_target, R.PORT_DEFICIT_GAIN)

    employment_target = deficit * R.EMPLOYMENT_GAIN
    if employment_target >= c.employment_pressure:
        employment = R.approach(c.employment_pressure, employment_target, R.EMPLOYMENT_GAIN)
    else:
        employment = R.approach(c.employment_pressure, employment_target, R.EMPLOYMENT_RECOVERY_FRACTION)

    return [
        _set("port_activity_deficit", min(deficit, R.PORT_DEFICIT_MAX), M_PORT,
             sources=("chain.rerouting_level",)),
        _set("employment_pressure", min(employment, R.EMPLOYMENT_MAX), M_PORT,
             sources=("chain.port_activity_deficit",)),
    ]


# --------------------------------------------------------------------------- #
# Stage 5 — household and cohort response (POPULATION-WEIGHTED)
# --------------------------------------------------------------------------- #
def m_household(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Per-cohort concern, then the population-weighted society-wide aggregate.

    Each cohort's concern is employment pressure scaled by that cohort's OWN declared exposure
    (`income_sensitivity`, from the scenario). This is why the fishing cohort and the urban
    professional cohort respond differently to the same shock — intensity is a property of the
    cohort, not of its size.

    The AGGREGATE is weighted by `represents_population` and normalised by the total represented
    population. Size affects aggregate magnitude ONLY. It says nothing about whether a cohort is
    right, and nothing about what any individual does.

    Recovery reason: household expectations improve only when employment pressure improves, and
    more slowly than they worsen. They do not fade because time passed.
    """
    employment = _lagged(state, "employment_pressure", R.CONCERN_LAG_TICKS)
    out: list[Transition] = []

    total_population = sum(c.represents_population for c in state.cohorts.values())
    weighted_sum = 0.0

    # Sorted so the result cannot depend on dict iteration order.
    for cid in sorted(state.cohorts):
        cohort = state.cohorts[cid]
        target = R.clamp(employment * cohort.income_sensitivity)
        gain = R.CONCERN_GAIN if target >= cohort.economic_concern else R.CONCERN_RECOVERY_FRACTION
        concern = R.clamp(R.approach(cohort.economic_concern, target, gain), high=R.CONCERN_MAX)

        out.append(
            Transition(
                type=TransitionType.SET_COHORT_CONCERN,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"cohort_id": cid, "value": concern},
                mechanism=M_HOUSEHOLD.id,
                mechanism_version=M_HOUSEHOLD.version,
                actor=cid,
                source_fields=["chain.employment_pressure", f"cohorts.{cid}.income_sensitivity"],
            )
        )
        weighted_sum += concern * cohort.represents_population

    aggregate = (weighted_sum / total_population) if total_population > 0 else 0.0
    out.append(
        _set("household_expectation_pressure", aggregate, M_HOUSEHOLD,
             sources=("cohorts.*.economic_concern", "cohorts.*.represents_population"))
    )
    return out


# --------------------------------------------------------------------------- #
# Stage 6 — narrative and collective activity
# --------------------------------------------------------------------------- #
def m_narrative(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Attention and collective activity.

    These are the ONLY quantities in the slice permitted to decay on "no new stimulus" alone —
    that is what attention is. Collective activity carries a small keyed stochastic component
    because turnout genuinely varies; the draw is keyed so it cannot displace any other draw.
    """
    household = _lagged(state, "household_expectation_pressure", R.NARRATIVE_LAG_TICKS)
    c = state.chain
    out: list[Transition] = []

    if household > 0.0:
        attention = R.approach(c.narrative_attention, household, R.NARRATIVE_GAIN)
    else:
        attention = max(0.0, c.narrative_attention - R.NARRATIVE_DECAY_PER_TICK)
    out.append(_set("narrative_attention", min(attention, R.NARRATIVE_MAX), M_NARRATIVE,
                    sources=("chain.household_expectation_pressure",)))

    # Turnout jitter is SCALED BY CURRENT ACTIVITY, so it cannot manufacture activity from
    # nothing. An earlier version added unscaled jitter every tick, which made collective activity
    # drift upward from zero in a run with no incident at all - the chain appearing to start on its
    # own. Bounded noise on a live quantity is modelling; noise on a dead one is a false positive.
    ref = draws.reference("chain", "collective_turnout", context=str(state.tick))
    if household > 0.0:
        base = R.approach(c.collective_activity, attention, R.COLLECTIVE_GAIN)
    else:
        base = max(0.0, c.collective_activity - R.COLLECTIVE_DECAY_PER_TICK)
    jitter = draws.jitter(R.COLLECTIVE_JITTER, subsystem="chain",
                          purpose="collective_turnout", context=str(state.tick)) * base
    collective = min(max(base + jitter, 0.0), R.COLLECTIVE_MAX)
    out.append(_set("collective_activity", collective, M_NARRATIVE,
                    sources=("chain.narrative_attention",), draw_refs=[ref.ref]))
    return out


# --------------------------------------------------------------------------- #
# Stage 7 — political pressure and government options
# --------------------------------------------------------------------------- #
def m_political(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Political pressure accumulates from attention AND collective activity, and persists longer.

    Deliberately decays more slowly than narrative attention: a tabled question or a coalition
    demand does not evaporate when coverage moves on. That asymmetry is the point of separating
    the two quantities.
    """
    attention = _lagged(state, "narrative_attention", R.POLITICAL_LAG_TICKS)
    collective = _lagged(state, "collective_activity", R.POLITICAL_LAG_TICKS)
    drive = attention * R.POLITICAL_NARRATIVE_WEIGHT + collective * R.POLITICAL_COLLECTIVE_WEIGHT
    c = state.chain

    if drive > 0.0:
        value = R.approach(c.political_pressure, drive, R.POLITICAL_GAIN)
    else:
        value = max(0.0, c.political_pressure - R.POLITICAL_DECAY_PER_TICK)
    return [_set("political_pressure", min(value, R.POLITICAL_MAX), M_POLITICAL,
                 sources=("chain.narrative_attention", "chain.collective_activity"))]


def m_options(state: AuthoritativeState, draws: DeterministicDrawService) -> list[Transition]:
    """Government options open, close and become constrained as pressure crosses thresholds.

    Options move in BOTH directions — pressure falling reopens quiet diplomacy and withdraws
    emergency powers. A one-way ratchet would be the saturation defect in a new costume.
    """
    p = state.chain.political_pressure
    desired = {
        "declare_emergency_powers": (
            R.OPTION_STATUS_ENABLED if p >= R.OPTION_EMERGENCY_POWERS_THRESHOLD
            else R.OPTION_STATUS_AVAILABLE
        ),
        "pursue_quiet_diplomacy": (
            R.OPTION_STATUS_CONSTRAINED if p >= R.OPTION_QUIET_DIPLOMACY_CONSTRAINED_ABOVE
            else R.OPTION_STATUS_AVAILABLE
        ),
        "publish_legal_advice": (
            R.OPTION_STATUS_ENABLED if p >= R.OPTION_PUBLISH_ADVICE_THRESHOLD
            else R.OPTION_STATUS_AVAILABLE
        ),
    }
    out: list[Transition] = []
    for oid, status in desired.items():
        if state.chain.government_options.get(oid) != status:
            out.append(
                Transition(
                    type=TransitionType.SET_OPTION_STATUS,
                    origin=TransitionOrigin.ENGINE_RULE,
                    payload={"option_id": oid, "status": status},
                    mechanism=M_OPTIONS.id,
                    mechanism_version=M_OPTIONS.version,
                    source_fields=["chain.political_pressure"],
                )
            )
    return out


# --------------------------------------------------------------------------- #
# The declared chain, in stage order.
# --------------------------------------------------------------------------- #
M_INCIDENT = Mechanism(
    id="M-INCIDENT-OBS", version="1.0.0", stage=1, stage_name="incident observation",
    source_fields=("chain.incident_severity",), target_fields=("chain.incident_severity",),
    lag_ticks=0, lifecycle="salience decay while unreinforced (attention-like)", fn=m_incident,
)
M_INSURER = Mechanism(
    id="M-INSURER-RISK", version="1.0.0", stage=2, stage_name="institutional risk assessment",
    source_fields=("chain.incident_severity",), target_fields=("chain.insurer_risk",),
    lag_ticks=R.INSURER_LAG_TICKS,
    lifecycle="decays ONLY while no incident is active; a live incident holds it up", fn=m_insurer,
)
M_PREMIUM = Mechanism(
    id="M-PREMIUM-PRESSURE", version="1.0.0", stage=3, stage_name="market response",
    source_fields=("chain.insurer_risk",), target_fields=("chain.premium_pressure",),
    lag_ticks=R.PREMIUM_LAG_TICKS, lifecycle="tracks insurer risk; no independent decay",
    fn=m_premium,
)
M_REROUTE = Mechanism(
    id="M-CARRIER-REROUTE", version="1.0.0", stage=3, stage_name="logistics response",
    source_fields=("chain.premium_pressure",),
    target_fields=("chain.rerouting_level", "chain.rerouting_ticks_committed"),
    lag_ticks=0,
    lifecycle=f"cooldown: minimum {R.REROUTE_MIN_DURATION_TICKS}-tick commitment, then unwinds "
              f"only if pressure < {R.REROUTE_RELEASE_THRESHOLD}",
    fn=m_reroute,
)
M_PORT = Mechanism(
    id="M-PORT-EXPOSURE", version="1.0.0", stage=4, stage_name="port and employment exposure",
    source_fields=("chain.rerouting_level",),
    target_fields=("chain.port_activity_deficit", "chain.employment_pressure"),
    lag_ticks=R.PORT_LAG_TICKS,
    lifecycle="follows routing state only; no random recovery; employment restores slower than it cuts",
    fn=m_port,
)
M_HOUSEHOLD = Mechanism(
    id="M-HOUSEHOLD-EXPECT", version="1.0.0", stage=5, stage_name="household and cohort response",
    source_fields=("chain.employment_pressure", "cohorts.*.income_sensitivity",
                   "cohorts.*.represents_population"),
    target_fields=("cohorts.*.economic_concern", "chain.household_expectation_pressure"),
    lag_ticks=R.CONCERN_LAG_TICKS,
    lifecycle="improves only when employment pressure improves, and more slowly than it worsens",
    fn=m_household,
)
M_NARRATIVE = Mechanism(
    id="M-NARRATIVE-ACTIVITY", version="1.0.0", stage=6, stage_name="narrative and family activity",
    source_fields=("chain.household_expectation_pressure",),
    target_fields=("chain.narrative_attention", "chain.collective_activity"),
    lag_ticks=R.NARRATIVE_LAG_TICKS,
    lifecycle="attention-like: MAY decay on absence of stimulus alone", fn=m_narrative,
)
M_POLITICAL = Mechanism(
    id="M-POLITICAL-PRESSURE", version="1.0.0", stage=7, stage_name="political pressure",
    source_fields=("chain.narrative_attention", "chain.collective_activity"),
    target_fields=("chain.political_pressure",), lag_ticks=R.POLITICAL_LAG_TICKS,
    lifecycle="persists longer than media attention; decays more slowly", fn=m_political,
)
M_OPTIONS = Mechanism(
    id="M-GOV-OPTIONS", version="1.0.0", stage=7, stage_name="government options",
    source_fields=("chain.political_pressure",), target_fields=("chain.government_options",),
    lag_ticks=0, lifecycle="threshold-driven, bidirectional: options open AND close", fn=m_options,
)

# Stage order is explicit and fixed. A later stage may read an earlier stage's output from THIS
# tick; feedback to an earlier stage always waits for the next tick, so no same-tick cycle exists.
CHAIN: tuple[Mechanism, ...] = (
    M_INCIDENT, M_INSURER, M_PREMIUM, M_REROUTE, M_PORT, M_HOUSEHOLD, M_NARRATIVE,
    M_POLITICAL, M_OPTIONS,
)


def mechanism_by_id(mid: str) -> Optional[Mechanism]:
    return next((m for m in CHAIN if m.id == mid), None)
