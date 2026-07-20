"""
VP-3 fixture decision slice — one small declared decision for each of the three fictional people.

Options are authored fictional content, NOT inferred from roles. Every contribution references a
declared VP-2 goal/responsibility/pressure/constraint from `vp2_fixtures`. The blocked options are
blocked by genuinely-active hard constraints in that slice.
"""

from __future__ import annotations

from ..belief.provenance import Origin
from .decision import (
    ActionOption,
    ConstraintRequirement,
    DecisionRequest,
    GoalContribution,
    PressureResponse,
    ResponsibilityContribution,
)
from .vp2_fixtures import fixture_for


def _request(person_id: str, decision_id: str, options) -> DecisionRequest:
    s = fixture_for(person_id)
    return DecisionRequest(
        decision_id=decision_id, subject_ref=f"fict:kestral-strait:person:{person_id}",
        goals=s.goals, responsibilities=s.responsibilities, pressures=s.pressures,
        constraints=s.constraints, options=tuple(options),
    )


def spokesperson_decision() -> DecisionRequest:
    """Communication decision. Repeating an unverified account conflicts with representing accurately."""
    return _request("family-spokesperson", "d-spokesperson-communication", [
        ActionOption(action_id="a-repeat-unverified", label="repeat the strongest unverified account",
            description="restate the strongest account without confirmation",
            goal_contributions=(GoalContribution(goal_id="g-explanation", alignment=0.2,
                rationale="offers families an explanation, but an unverified one"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-represent",
                alignment=-0.6, rationale="an unverified account risks misrepresenting the families"),),
            pressure_responses=(PressureResponse(pressure_id="p-uncertainty", response=0.3,
                rationale="fills the silence but does not resolve the uncertainty"),)),
        ActionOption(action_id="a-request-records", label="request official records, communicate only confirmed facts",
            description="ask for records and speak only to what is confirmed",
            goal_contributions=(GoalContribution(goal_id="g-explanation", alignment=0.7,
                rationale="pursues a credible, verifiable explanation"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-represent",
                alignment=0.8, rationale="represents families accurately"),),
            pressure_responses=(PressureResponse(pressure_id="p-uncertainty", response=0.4,
                rationale="reduces uncertainty by seeking confirmation"),)),
        ActionOption(action_id="a-no-statement", label="make no statement",
            description="say nothing for now",
            goal_contributions=(GoalContribution(goal_id="g-explanation", alignment=-0.2,
                rationale="does not advance an explanation"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-represent",
                alignment=0.1, rationale="avoids inaccuracy but offers nothing"),),
            pressure_responses=(PressureResponse(pressure_id="p-uncertainty", response=-0.1,
                rationale="leaves the uncertainty in place"),)),
    ])


def minister_decision() -> DecisionRequest:
    """Public-response decision. Immediate attribution is blocked while the verification constraint is active."""
    return _request("government-minister", "d-minister-public-response", [
        ActionOption(action_id="a-attribute-now", label="publicly attribute responsibility immediately",
            description="name a responsible party now",
            constraint_requirements=(ConstraintRequirement(constraint_id="c-attribution",
                blocked_while_active=True, rationale="an unsupported public attribution is not permitted "
                "while verification is incomplete"),),
            goal_contributions=(GoalContribution(goal_id="g-continuity", alignment=-0.3,
                rationale="a premature attribution risks continuity if it proves wrong"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-verify",
                alignment=-0.7, rationale="bypasses the verification process"),)),
        ActionOption(action_id="a-cautious-statement", label="issue a cautious statement and continue verification",
            description="acknowledge the situation and keep verifying",
            goal_contributions=(GoalContribution(goal_id="g-continuity", alignment=0.6,
                rationale="maintains order without overcommitting"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-verify",
                alignment=0.8, rationale="honours the verification process"),),
            pressure_responses=(PressureResponse(pressure_id="p-scrutiny", response=0.5,
                rationale="answers scrutiny without a premature claim"),)),
        ActionOption(action_id="a-no-statement", label="make no public statement",
            description="stay silent for now",
            goal_contributions=(GoalContribution(goal_id="g-continuity", alignment=0.2,
                rationale="avoids error but may read as evasive"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-verify",
                alignment=0.3, rationale="does not breach the process"),),
            pressure_responses=(PressureResponse(pressure_id="p-scrutiny", response=-0.3,
                rationale="silence increases scrutiny"),)),
    ])


def journalist_decision() -> DecisionRequest:
    """Publication decision. Publishing immediately is blocked while the corroboration constraint is active."""
    return _request("broadcast-journalist", "d-journalist-publication", [
        ActionOption(action_id="a-publish-now", label="publish the claim immediately",
            description="report the claim as established now",
            constraint_requirements=(ConstraintRequirement(constraint_id="c-corroboration",
                blocked_while_active=True, rationale="the broadcaster's standard forbids reporting as "
                "established without corroboration"),),
            goal_contributions=(GoalContribution(goal_id="g-report", alignment=0.3,
                rationale="publishes, but not an accurate corroborated report"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-standard",
                alignment=-0.8, rationale="fails the verification standard"),)),
        ActionOption(action_id="a-seek-corroboration", label="seek additional corroboration",
            description="pursue a second source before reporting",
            goal_contributions=(GoalContribution(goal_id="g-report", alignment=0.7,
                rationale="works toward an accurate, publishable report"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-standard",
                alignment=0.8, rationale="meets the verification standard"),),
            pressure_responses=(PressureResponse(pressure_id="p-deadline", response=-0.2,
                rationale="takes time against the deadline"),)),
        ActionOption(action_id="a-hold", label="hold the report without further investigation",
            description="shelve it and do nothing further",
            goal_contributions=(GoalContribution(goal_id="g-report", alignment=-0.3,
                rationale="abandons the report"),),
            responsibility_contributions=(ResponsibilityContribution(responsibility_id="r-standard",
                alignment=0.2, rationale="does not breach the standard, but reports nothing"),),
            pressure_responses=(PressureResponse(pressure_id="p-deadline", response=0.1,
                rationale="removes deadline pressure by giving up"),)),
    ])


FIXTURE_DECISIONS = {
    "family-spokesperson": spokesperson_decision,
    "government-minister": minister_decision,
    "broadcast-journalist": journalist_decision,
}
