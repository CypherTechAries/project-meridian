"""
VP-2 fixture slice — a minimal, explicit current-situation for the three existing fictional people.

Only enough state to demonstrate the mechanism. No biographies are invented, and NOTHING here is
derived from a role label — each item is authored fixture content grounded in existing scenario
facts (the Kestral Strait incident, the belief-slice claim, the declared processes). Everything is
marked FIXTURE.

These are the situations, in plain terms:

  Family spokesperson — wants a credible explanation for affected families; responsible for
    representing them accurately; under pressure from continuing uncertainty; constrained by lack of
    access to official records.
  Government minister — wants to maintain continuity and public order; responsible for following the
    cabinet verification process; under pressure from political scrutiny; constrained from making an
    unsupported public attribution.
  Broadcast journalist — wants to publish an accurate report; responsible for meeting the
    broadcaster's verification standard; under an approaching-deadline pressure; constrained by
    insufficient corroboration.
"""

from __future__ import annotations

from ..belief.provenance import Origin
from .current_state import (
    Constraint,
    ConstraintKind,
    CurrentSituation,
    Goal,
    Pressure,
    PressureSource,
    Responsibility,
)

CLAIM = "P-WARNINGS-IGNORED"


def _sit(goals, responsibilities, pressures, constraints) -> CurrentSituation:
    return CurrentSituation(
        goals=tuple(goals), responsibilities=tuple(responsibilities),
        pressures=tuple(pressures), constraints=tuple(constraints),
    )


VP2_FIXTURES: dict[str, CurrentSituation] = {
    "family-spokesperson": _sit(
        goals=[Goal(goal_id="g-explanation", description="obtain a credible explanation for affected families",
                    desired_condition="a verified account of what happened is available to families",
                    priority=0.7, origin=Origin.fixture, supporting_refs=(CLAIM,))],
        responsibilities=[Responsibility(responsibility_id="r-represent",
                    obligation="represent affected families accurately", owed_to="Strait Families Group",
                    subject="public representation", urgency=0.6, origin=Origin.fixture)],
        pressures=[Pressure(pressure_id="p-uncertainty", description="continuing uncertainty about the closure",
                    source_kind=PressureSource.missing_information, source_ref="incident:kestral-blockade",
                    intensity=0.6, onset_tick=1, origin=Origin.fixture)],
        constraints=[Constraint(constraint_id="c-records", limitation="no access to official records",
                    constraint_kind=ConstraintKind.lacks_record_access, subject="verifying the account",
                    origin=Origin.fixture)],
    ),
    "government-minister": _sit(
        goals=[Goal(goal_id="g-continuity", description="maintain continuity of government and public order",
                    desired_condition="the strait situation is managed without loss of continuity",
                    priority=0.65, origin=Origin.fixture)],
        responsibilities=[Responsibility(responsibility_id="r-verify",
                    obligation="follow the declared cabinet verification process", owed_to="the cabinet",
                    subject="official factual position", urgency=0.7, origin=Origin.fixture, supporting_refs=(CLAIM,))],
        pressures=[Pressure(pressure_id="p-scrutiny", description="political scrutiny of the response",
                    source_kind=PressureSource.public_scrutiny, source_ref="incident:kestral-blockade",
                    intensity=0.55, onset_tick=1, origin=Origin.fixture)],
        constraints=[Constraint(constraint_id="c-attribution",
                    limitation="cannot make an unsupported public attribution",
                    constraint_kind=ConstraintKind.verification_incomplete, subject="public statement on the claim",
                    hardness="hard", origin=Origin.fixture, source_ref=CLAIM)],
    ),
    "broadcast-journalist": _sit(
        goals=[Goal(goal_id="g-report", description="publish an accurate report",
                    desired_condition="a corroborated report can be published",
                    priority=0.6, origin=Origin.fixture, supporting_refs=(CLAIM,))],
        responsibilities=[Responsibility(responsibility_id="r-standard",
                    obligation="meet the broadcaster's verification standard", owed_to="Northshore Public Broadcast",
                    subject="publication", urgency=0.6, origin=Origin.fixture)],
        pressures=[Pressure(pressure_id="p-deadline", description="an approaching publication deadline",
                    source_kind=PressureSource.approaching_deadline, source_ref="broadcast-window:day6",
                    intensity=0.5, onset_tick=6, origin=Origin.fixture)],
        constraints=[Constraint(constraint_id="c-corroboration", limitation="insufficient corroboration to report as established",
                    constraint_kind=ConstraintKind.verification_incomplete, subject="reporting the claim",
                    hardness="hard", origin=Origin.fixture, source_ref=CLAIM)],
    ),
}


def fixture_for(person_id: str) -> CurrentSituation:
    if person_id not in VP2_FIXTURES:
        raise ValueError(f"no VP-2 fixture for '{person_id}'")
    return VP2_FIXTURES[person_id]
