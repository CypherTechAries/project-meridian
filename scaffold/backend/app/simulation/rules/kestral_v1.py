"""Kestral Strait causal-slice rule pack — Phase 0 item P0.5.

THE ONLY HOME FOR BEHAVIOURAL CONSTANTS in this slice. Coefficients, thresholds, caps, lags,
decay rates and cooldowns live here and nowhere else — not in the engine, not in route handlers,
not in the UI, not in agent prose.

WHAT THIS IS NOT
----------------
Not a behavioural-science framework and not a validated model. Every coefficient below is an
**authored fictional value chosen for demonstration**. None is calibrated against real data, none
is empirically defensible, and nothing here supports a claim about real-world behaviour. The
mechanisms are *plausible in shape*, which is what the charter asks of a fictional world; they are
not predictive.

LIFECYCLE DOCTRINE (founder decision, 19 July 2026)
--------------------------------------------------
There is no arbitrary global mean reversion. Each mechanism declares its own lifecycle, and every
recovery rule names the causal reason recovery happens. "No new stimulus" is accepted as a
sufficient reason ONLY for attention-like quantities — narrative attention and collective
activity. Economic and institutional states recover only when their own inputs improve.
"""

from __future__ import annotations

from typing import Final

RULE_PACK_ID: Final[str] = "kestral-causal-slice"
RULE_PACK_VERSION: Final[str] = "1.0.0"
RULE_PACK: Final[str] = f"{RULE_PACK_ID}@{RULE_PACK_VERSION}"

# --------------------------------------------------------------------------- #
# Stage 1 — incident observation
# --------------------------------------------------------------------------- #
# An incident is an EXTERNAL INPUT. It never spontaneously arises and never spontaneously
# repeats. Severity decays only because the incident itself is no longer being reinforced —
# this is an observation/salience quantity, so "no new stimulus" is a legitimate reason.
# 0.015/tick over 6-hour ticks: a sustained closure still reads as ~65% severity after five
# simulated days. An earlier 0.04 made the incident fade to nothing inside the 20-tick
# demonstration horizon, so the whole chain fizzled and the horizon carried no information. This
# is a scenario-fidelity fix - the Kestral incident is a continuing blockade, not a one-off event.
INCIDENT_DECAY_PER_TICK: Final[float] = 0.015
INCIDENT_ACTIVE_THRESHOLD: Final[float] = 0.05

# --------------------------------------------------------------------------- #
# Stage 2 — institutional risk assessment (insurers)
# --------------------------------------------------------------------------- #
# Lag: underwriters do not reprice within six hours of an incident.
INSURER_LAG_TICKS: Final[int] = 1
INSURER_GAIN: Final[float] = 0.55
INSURER_MAX: Final[float] = 1.0
# Recovery reason: risk posture relaxes only while NO incident is active. It is not a timer —
# a persisting incident holds the posture up indefinitely.
INSURER_DECAY_PER_TICK: Final[float] = 0.03

# --------------------------------------------------------------------------- #
# Stage 3 — market and logistics response
# --------------------------------------------------------------------------- #
PREMIUM_LAG_TICKS: Final[int] = 0
PREMIUM_GAIN: Final[float] = 0.80
PREMIUM_MAX: Final[float] = 1.0

# Carriers reroute once premium pressure crosses a threshold, and having rerouted they cannot
# instantly un-reroute: a diverted vessel is committed. This is a genuine cooldown, not decay.
REROUTE_TRIGGER_THRESHOLD: Final[float] = 0.30
REROUTE_GAIN: Final[float] = 0.70
REROUTE_MAX: Final[float] = 1.0
REROUTE_MIN_DURATION_TICKS: Final[int] = 8  # 48 simulated hours at 6h ticks
# Recovery reason: rerouting unwinds only when premium pressure has fallen below the release
# threshold AND the minimum commitment has elapsed.
REROUTE_RELEASE_THRESHOLD: Final[float] = 0.20
REROUTE_UNWIND_PER_TICK: Final[float] = 0.10

# --------------------------------------------------------------------------- #
# Stage 4 — port and employment exposure
# --------------------------------------------------------------------------- #
# Port activity FOLLOWS routing state. There is no random recovery: if carriers are still
# rerouted, the port stays quiet. Recovery reason is entirely "rerouting reduced".
PORT_LAG_TICKS: Final[int] = 1
PORT_DEFICIT_GAIN: Final[float] = 0.85
PORT_DEFICIT_MAX: Final[float] = 1.0
# Employment exposure tracks the port deficit with additional inertia: rosters are cut faster
# than they are restored.
EMPLOYMENT_GAIN: Final[float] = 0.70
EMPLOYMENT_MAX: Final[float] = 1.0
EMPLOYMENT_RECOVERY_FRACTION: Final[float] = 0.35  # restoration is slower than the cut

# --------------------------------------------------------------------------- #
# Stage 5 — household and cohort response
# --------------------------------------------------------------------------- #
# Per-cohort concern is driven by employment pressure scaled by that cohort's OWN declared
# exposure (`economic_profile.income_sensitivity_to_shipping_disruption` from the scenario).
# This is what makes the fishing cohort respond differently from the urban professional cohort.
CONCERN_LAG_TICKS: Final[int] = 1
CONCERN_GAIN: Final[float] = 0.90
CONCERN_MAX: Final[float] = 1.0
# Recovery reason: household expectations improve only when the economic input improves. They do
# not fade merely because time passed.
CONCERN_RECOVERY_FRACTION: Final[float] = 0.25

# --------------------------------------------------------------------------- #
# Stage 6 — narrative and collective activity
# --------------------------------------------------------------------------- #
# Attention-like quantities. These MAY decay on "no new stimulus" alone — that is the whole
# point of attention, and it is the only category where the founder permits it.
NARRATIVE_LAG_TICKS: Final[int] = 1
NARRATIVE_GAIN: Final[float] = 0.65
NARRATIVE_MAX: Final[float] = 1.0
NARRATIVE_DECAY_PER_TICK: Final[float] = 0.07

COLLECTIVE_GAIN: Final[float] = 0.50
COLLECTIVE_MAX: Final[float] = 1.0
COLLECTIVE_DECAY_PER_TICK: Final[float] = 0.05
# Small keyed stochastic component so collective activity is not perfectly smooth. Bounded, and
# drawn from the keyed service — it cannot displace any other draw.
COLLECTIVE_JITTER: Final[float] = 0.01

# --------------------------------------------------------------------------- #
# Stage 7 — political pressure and government options
# --------------------------------------------------------------------------- #
# Political pressure persists DIFFERENTLY from media attention: it accumulates from both
# narrative attention and collective activity, and decays more slowly, because a tabled question
# or a coalition demand does not evaporate when coverage moves on.
POLITICAL_LAG_TICKS: Final[int] = 1
POLITICAL_NARRATIVE_WEIGHT: Final[float] = 0.45
POLITICAL_COLLECTIVE_WEIGHT: Final[float] = 0.55
POLITICAL_GAIN: Final[float] = 0.60
POLITICAL_MAX: Final[float] = 1.0
POLITICAL_DECAY_PER_TICK: Final[float] = 0.02  # slower than narrative decay, deliberately

# Government options. Status is a function of political pressure crossing declared thresholds.
# Options may both open and close — pressure is not one-way.
# Thresholds are calibrated to the scale political_pressure actually occupies, which was
# established by running the chain rather than guessed in advance. A regional shipping crisis
# drives pressure into roughly 0.10-0.20 over the 20-tick horizon; pressure near 1.0 would mean a
# national existential crisis. The first draft set these at 0.30/0.45/0.55, which no reachable
# state could cross - the mechanism existed but could never demonstrably fire, and the
# demonstration horizon carried no information.
#
# The ordering is also a modelling statement, not a convenience. Publishing legal advice is a low
# bar: a routine act a government takes under modest scrutiny. Constraining quiet diplomacy needs
# more - it means the political cost of being seen to negotiate has become real. Emergency powers
# sit deliberately ABOVE anything this scenario reaches, because a five-day shipping disruption
# should NOT unlock them. That option staying AVAILABLE is a correct result, not a gap.
OPTION_EMERGENCY_POWERS_THRESHOLD: Final[float] = 0.20
OPTION_QUIET_DIPLOMACY_CONSTRAINED_ABOVE: Final[float] = 0.14
OPTION_PUBLISH_ADVICE_THRESHOLD: Final[float] = 0.10

OPTION_STATUS_AVAILABLE: Final[str] = "AVAILABLE"
OPTION_STATUS_CONSTRAINED: Final[str] = "CONSTRAINED"
OPTION_STATUS_ENABLED: Final[str] = "ENABLED"

GOVERNMENT_OPTIONS: Final[tuple[str, ...]] = (
    "declare_emergency_powers",
    "pursue_quiet_diplomacy",
    "publish_legal_advice",
)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Every scalar this rule pack produces is bounded. No unbounded accumulation is possible."""
    return max(low, min(high, value))


def approach(current: float, target: float, gain: float) -> float:
    """Move `current` a `gain` fraction of the way toward `target`.

    A bounded transformation: the output can never exceed `max(current, target)`, so repeated
    identical shocks converge rather than accumulating without limit. This is the primary
    saturation control for the slice.
    """
    return current + (target - current) * gain
