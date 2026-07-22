"""
Deterministic decision resolution — Kestral Consequence Slice v0.2, build step 1.

WHAT THIS CLOSES. A submitted action used to be appended to a list the tick loop never read, so
choosing an option changed nothing. This module is the rule that turns a selected option into a
consequence, and it is the ONLY place that decides what a decision does.

DETERMINISTIC BY CONSTRUCTION. No random draw is taken here, and the shared RNG is never touched.

    same scenario state + same selected action + same rule version
        = same consequence and the same explanation

Random variation stays blocked until named RNG substreams exist (P0.4A) and outcome dispersion has
been evaluated (issue #26). "Risk of partial failure" therefore means **resolved from the declared
state**, never sampled.

NO CLIFFS. Effectiveness is CONTINUOUS and the magnitude of every effect scales with it; only the
LABEL is banded. A run whose capacity is a hair under a band edge gets a slightly smaller effect and
a different word — not a different world. That is the difference between a band and a brittle
threshold, and it is the property `test_no_cliff_at_band_edges` exists to hold.

NOTHING HERE IS HIDDEN. Every input is a named field of authoritative state, every requirement is
declared below, and the explanation is generated from the same numbers the resolution used — so an
explanation cannot drift from the effect it describes.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

_FROZEN = ConfigDict(extra="forbid", frozen=True)

#: Versioned, and recorded on every transition and event this module produces. Changing any
#: declared number below REQUIRES bumping this, because a stored trace must identify the rule that
#: produced it.
RESOLUTION_RULE = "kestral-decision-resolution"
RESOLUTION_RULE_VERSION = "0.1.0"


class Outcome(str, Enum):
    """The closed set of resolutions. An unknown option resolves INVALID, never silently."""

    FULL_SUCCESS = "FULL_SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILURE = "FAILURE"
    INVALID_OR_UNAVAILABLE = "INVALID_OR_UNAVAILABLE"


#: Declared outcome bands, on effectiveness in [0,1]. Named and versioned so a trace can be read
#: years later. These are authored fictional values calibrated against nothing, like every other
#: coefficient in this project.
BAND_FULL = 0.85
BAND_PARTIAL = 0.40


def band_for(effectiveness: float) -> Outcome:
    """Effectiveness → declared band. The label is banded; the magnitude is not."""
    if effectiveness >= BAND_FULL:
        return Outcome.FULL_SUCCESS
    if effectiveness >= BAND_PARTIAL:
        return Outcome.PARTIAL_SUCCESS
    return Outcome.FAILURE


class OptionRequirement(BaseModel):
    """What an option needs, and what it costs. Declared, inspectable, scenario-independent."""

    model_config = _FROZEN

    option_id: str
    #: Plain-language name of the lever. Never an identifier on screen.
    label: str
    #: Which lever family this is — operational, economic or information.
    lever: str
    #: Implementation capacity required to deliver it in full, 0..1.
    required_capability: float
    #: Budget required to deliver it in full, in the scenario's declared millions.
    required_budget_m: float
    #: Political capital consumed, 0..1. Spent whether or not delivery succeeds.
    political_capital_cost: float
    #: Ticks between the decision being consumed and its delayed effect landing.
    implementation_delay_ticks: int
    #: The authoritative fields the resolution reads. Echoed into the trace.
    source_fields: tuple[str, ...]


#: THE FIRST VERTICAL SLICE — one option only.
#:
#: Economic, and deliberately not communications: it moves money to households whose income the
#: blockade has cut. The other two levers (operational, information) are declared in issue #44 and
#: are NOT implemented; adding them is the next step, not this one.
EMERGENCY_SUPPORT = OptionRequirement(
    option_id="emergency_support_fishing_households",
    label="Emergency support for fishing households and affected ports",
    lever="economic",
    required_capability=0.60,
    required_budget_m=180.0,
    political_capital_cost=0.10,
    implementation_delay_ticks=2,
    source_fields=(
        "government.implementation_capacity",
        "government.budget_reserve_m",
        "government.political_capital",
        "cohorts.coastal-creole-fishing.economic_concern",
        "chain.employment_pressure",
    ),
)

DECLARED_OPTIONS: dict[str, OptionRequirement] = {
    EMERGENCY_SUPPORT.option_id: EMERGENCY_SUPPORT,
}


class ResolutionInputs(BaseModel):
    """Exactly the state this rule reads. Explicit so an explanation cannot cite anything else."""

    model_config = _FROZEN

    implementation_capacity: float
    budget_reserve_m: float
    political_capital: float
    affected_population: int
    #: Present only when the scenario declares an adversary campaign targeting the affected cohort.
    adversary_targets_affected_cohort: bool = False


class Resolution(BaseModel):
    """The complete, inspectable result of resolving one decision."""

    model_config = _FROZEN

    option_id: str
    outcome: Outcome
    #: 0..1. The magnitude of every effect below is proportional to this.
    effectiveness: float
    #: What was actually spent — never more than was available.
    budget_spent_m: float
    political_capital_spent: float
    #: Immediate authoritative changes, as (field, new value) pairs the caller turns into
    #: transitions. This module proposes; the transition boundary remains the only writer.
    immediate_effects: list[dict[str, Any]] = Field(default_factory=list)
    #: Effects that land later, with the tick offset at which they become due.
    delayed_effects: list[dict[str, Any]] = Field(default_factory=list)
    #: The adversary's declared reaction, where the scenario supports one.
    adversary_response: Optional[dict[str, Any]] = None
    #: Ordinary language, generated from the same numbers used above.
    explanation: str
    #: Why it resolved as it did, in the rule's own terms.
    limiting_factor: str
    rule: str = RESOLUTION_RULE
    rule_version: str = RESOLUTION_RULE_VERSION
    inputs: ResolutionInputs
    source_fields: list[str] = Field(default_factory=list)


def _ratio(available: float, required: float) -> float:
    """Available against required, capped at 1. A zero requirement is met by definition."""
    if required <= 0:
        return 1.0
    return max(0.0, min(1.0, available / required))


def resolve(
    option_id: str,
    inputs: ResolutionInputs,
    *,
    current_concern: float,
    current_employment_pressure: float,
) -> Resolution:
    """
    Resolve one decision from declared state. Pure: reads its arguments, writes nothing.

    Effectiveness is the WEAKEST of the declared ratios — a plan you cannot staff is not rescued by
    money, and a plan you cannot fund is not rescued by capacity. That is a modelling choice, and it
    is declared here rather than buried.
    """
    requirement = DECLARED_OPTIONS.get(option_id)
    if requirement is None:
        return Resolution(
            option_id=option_id,
            outcome=Outcome.INVALID_OR_UNAVAILABLE,
            effectiveness=0.0,
            budget_spent_m=0.0,
            political_capital_spent=0.0,
            explanation=(
                f"'{option_id}' is not a declared option in this scenario, so nothing was "
                f"attempted and nothing was spent."
            ),
            limiting_factor="unknown_option",
            inputs=inputs,
            source_fields=[],
        )

    capacity_ratio = _ratio(inputs.implementation_capacity, requirement.required_capability)
    budget_ratio = _ratio(inputs.budget_reserve_m, requirement.required_budget_m)
    effectiveness = round(min(capacity_ratio, budget_ratio), 6)
    outcome = band_for(effectiveness)

    limiting = (
        "implementation_capacity" if capacity_ratio <= budget_ratio else "budget_reserve"
    )
    if effectiveness >= 1.0:
        limiting = "none — both requirements were met in full"

    # Spending is proportional to what was actually delivered, and never exceeds what was held.
    budget_spent = round(min(inputs.budget_reserve_m, requirement.required_budget_m * effectiveness), 4)
    # Political capital is spent on ATTEMPTING, not on succeeding. Announcing support and
    # delivering little costs more politically than not announcing it, which is why this is not
    # scaled by effectiveness.
    capital_spent = round(min(inputs.political_capital, requirement.political_capital_cost), 4)

    immediate: list[dict[str, Any]] = []
    delayed: list[dict[str, Any]] = []
    adversary: Optional[dict[str, Any]] = None

    if outcome is not Outcome.FAILURE:
        # Immediate: money reaching households eases their economic concern, in proportion.
        relief = round(0.18 * effectiveness, 6)
        immediate.append(
            {
                "kind": "cohort_concern",
                "cohort_id": "coastal-creole-fishing",
                "value": round(max(0.0, current_concern - relief), 6),
                "why": f"support reduced concern by {relief:.3f}",
            }
        )
        # Delayed: employment exposure eases only once the money has moved through the ports.
        ease = round(0.12 * effectiveness, 6)
        delayed.append(
            {
                "kind": "chain_scalar",
                "field": "employment_pressure",
                "value": round(max(0.0, current_employment_pressure - ease), 6),
                "due_in_ticks": requirement.implementation_delay_ticks,
                "why": f"port employment exposure eased by {ease:.3f} once payments cleared",
            }
        )
        if inputs.adversary_targets_affected_cohort:
            # The declared campaign reframes the payments. This is the SCENARIO'S declared
            # adversary reacting — not an invented consequence.
            lift = round(0.05 * effectiveness, 6)
            adversary = {
                "kind": "chain_scalar",
                "field": "narrative_attention",
                "delta": lift,
                "why": (
                    "the declared foreign campaign reframed the payments as evidence that the "
                    "blockade was working, raising attention"
                ),
            }

    explanation = _explain(requirement, outcome, effectiveness, budget_spent, capital_spent,
                           limiting, inputs, adversary is not None)

    return Resolution(
        option_id=option_id,
        outcome=outcome,
        effectiveness=effectiveness,
        budget_spent_m=budget_spent,
        political_capital_spent=capital_spent,
        immediate_effects=immediate,
        delayed_effects=delayed,
        adversary_response=adversary,
        explanation=explanation,
        limiting_factor=limiting,
        inputs=inputs,
        source_fields=list(requirement.source_fields),
    )


def _explain(
    requirement: OptionRequirement,
    outcome: Outcome,
    effectiveness: float,
    budget_spent: float,
    capital_spent: float,
    limiting: str,
    inputs: ResolutionInputs,
    adversary_reacted: bool,
) -> str:
    """
    Ordinary language, built from the same numbers the resolution used.

    Generated rather than authored, so an explanation cannot describe an effect that did not
    happen — the failure mode that made the Briefing and Ask contradict each other.
    """
    if outcome is Outcome.FULL_SUCCESS:
        head = (
            f"Support reached the affected households in full. The government had the capacity "
            f"({inputs.implementation_capacity:.2f} against {requirement.required_capability:.2f} "
            f"required) and the money ({inputs.budget_reserve_m:.0f}m against "
            f"{requirement.required_budget_m:.0f}m required)."
        )
    elif outcome is Outcome.PARTIAL_SUCCESS:
        short = (
            "capacity" if limiting == "implementation_capacity" else "money"
        )
        held = (
            f"{inputs.implementation_capacity:.2f} against "
            f"{requirement.required_capability:.2f} required"
            if limiting == "implementation_capacity"
            else f"{inputs.budget_reserve_m:.0f}m against {requirement.required_budget_m:.0f}m required"
        )
        head = (
            f"Support reached some households and not others — about "
            f"{effectiveness * 100:.0f}% of what was intended. The limit was {short} "
            f"({held})."
        )
    else:
        short = "capacity" if limiting == "implementation_capacity" else "money"
        head = (
            f"The support did not reach households. There was too little {short} to deliver it "
            f"— effectiveness resolved to {effectiveness * 100:.0f}%, below the {BAND_PARTIAL * 100:.0f}% "
            f"needed for partial delivery."
        )

    cost = (
        f" It used {budget_spent:.0f}m of the reserve and {capital_spent:.2f} of political capital."
    )
    reaction = (
        " The declared foreign campaign reframed the payments as evidence that the blockade was "
        "working."
        if adversary_reacted
        else ""
    )
    return head + cost + reaction
