"""
Briefing and Ask MERIDIAN must not carry separate factual versions of the same run.

WHY THESE TESTS EXIST. The two surfaces contradicted each other in the browser. The Briefing said
political pressure was low and falling; Ask MERIDIAN said it was "still high". Both were describing
the same deterministic 20-tick run. The Briefing derived its claim; Ask's was a hand-written string.

These tests assert the SHARED STATE, not the prose. Asserting exact sentences would fail on every
wording change while still permitting the actual defect — two surfaces reading different sources.
So the rule enforced here is: there is one factual source, both surfaces read it, and moving the
shared value moves both.
"""

from __future__ import annotations

import re

import pytest

from app.api.routes_demo import DemoRunRequest, packaged_run_state, run_demonstration
from app.simulation.ask.answer import answer_question
from app.simulation.scenario_state import (
    Direction,
    Level,
    classify_direction,
    classify_level,
    derive_field_state,
    scenario_state,
)


@pytest.fixture(scope="module")
def state():
    return packaged_run_state()


@pytest.fixture(scope="module")
def run():
    return run_demonstration(DemoRunRequest())


def ask(question: str):
    return answer_question(question)


# ── the shared source itself ──────────────────────────────────────────────────────────────────────


def test_run_response_carries_the_shared_state(run):
    """The Briefing's own request returns the authoritative state, so it need not re-derive it."""
    assert "fields" in run.state
    assert "political_pressure" in run.state["fields"]


def test_packaged_state_matches_the_default_run(run, state):
    """
    Ask reads the packaged state; the Briefing reads the state of its own default request. If those
    two ever diverge, every consistency guarantee below is worthless.
    """
    assert run.state == state.model_dump()


def test_level_and_direction_are_separate_measures(state):
    """
    The contradiction was made possible by conflating two true statements. Political pressure is LOW
    in absolute terms AND close to its own peak. Both facts must be present and independent, so a
    surface cannot state one while implying the other.
    """
    political = state.get("political_pressure")
    assert political is not None
    assert political.level is Level.low
    assert political.near_peak is True
    assert political.peak_retention > 0.9
    assert political.value < 0.33


def test_direction_is_falling_not_steady(state):
    """A value past its peak reads as falling even where the five-tick window is too narrow."""
    political = state.get("political_pressure")
    assert political.direction is Direction.falling
    assert political.post_peak is True


def test_unmeasured_direction_is_not_reported_as_steady(state):
    """
    A field the trajectory does not record has no measurable direction. NOT_ESTABLISHED is the
    honest answer; STEADY would claim we looked and found no movement.
    """
    port = state.get("port_activity_deficit")
    assert port is not None
    assert port.direction_measured is False
    assert port.direction is Direction.not_established


# ── agreement between the two surfaces ────────────────────────────────────────────────────────────


LEVEL_WORDS = {Level.high: "high", Level.moderate: "moderate", Level.low: "low"}
# Words that would assert a level the shared state does not support.
CONTRADICTING = {
    Level.low: ["high", "severe", "intense", "extreme"],
    Level.moderate: ["severe", "extreme"],
    Level.high: ["low", "negligible", "minimal"],
}


@pytest.mark.parametrize(
    "question",
    [
        "Brief me on the current situation.",
        "How are the economy and supply chains reacting?",
        "What is happening politically?",
        "Is political pressure rising or falling?",
    ],
)
def test_ask_never_contradicts_the_shared_political_level(question, state):
    """
    No Ask answer may assert a political-pressure level the shared state does not support.

    This is the exact defect: `_brief` hard-coded "political pressure is still high" while the
    shared state said LOW.
    """
    political = state.get("political_pressure")
    response = ask(question)
    if not response.supported:
        return
    text = response.short_answer.lower()
    if "pressure on the government" not in text and "political pressure" not in text:
        return
    for banned in CONTRADICTING[political.level]:
        # Whole words only. "highest it has been so far" is the near-peak fact and is TRUE;
        # "pressure is high" is the level claim and would be false. Substring matching cannot
        # tell them apart, and conflating them is how this defect started.
        assert not re.search(rf"\b{banned}\b", text), (
            f"Ask asserts '{banned}' for political pressure while the shared state says "
            f"{political.level.value}. Question: {question!r}"
        )


def test_ask_states_the_level_the_shared_state_holds(state):
    political = state.get("political_pressure")
    text = ask("Brief me on the current situation.").short_answer.lower()
    assert LEVEL_WORDS[political.level] in text


def test_ask_agrees_on_direction(state):
    political = state.get("political_pressure")
    text = ask("Brief me on the current situation.").short_answer.lower()
    if political.direction is Direction.falling:
        assert "coming down" in text or "come down" in text
        assert "still rising" not in text
    elif political.direction is Direction.rising:
        assert "rising" in text


def test_ask_carries_the_near_peak_fact_when_the_state_holds_it(state):
    """
    The near-peak fact is why the original hard-coded sentence *felt* right. It is true and must be
    stated — but as the second half of the sentence, not as the level.
    """
    political = state.get("political_pressure")
    assert political.near_peak is True
    text = ask("Brief me on the current situation.").short_answer.lower()
    assert "close to the highest it has been" in text


def test_economy_answer_does_not_contradict_the_shared_state(state):
    text = ask("How are the economy and supply chains reacting?").short_answer.lower()
    reroute = state.get("rerouting_level")
    assert LEVEL_WORDS[reroute.level] in text
    # The old prose asserted political pressure was "still near its peak" as the headline fact.
    assert "still high" not in text


# ── moving the shared value must move both surfaces ───────────────────────────────────────────────


def test_changing_the_shared_value_changes_the_description():
    """
    The load-bearing test. If a surface stopped reading the shared state and went back to prose,
    this is what would catch it: the same code path, given a different value, must describe it
    differently.
    """
    low = derive_field_state("political_pressure", 0.15, [0.1, 0.12, 0.14, 0.16, 0.155, 0.15])
    high = derive_field_state("political_pressure", 0.80, [0.1, 0.3, 0.5, 0.65, 0.75, 0.80])
    assert low.level is Level.low
    assert high.level is Level.high
    assert high.direction is Direction.rising


def test_a_rebuilt_state_from_a_different_run_differs(run):
    """A different tick count is a different state — the summary is computed, never authored."""
    short = run_demonstration(DemoRunRequest(ticks=6))
    assert short.state != run.state


# ── no independently hard-coded state values ──────────────────────────────────────────────────────


LEVEL_CLAIM = re.compile(
    r"(political pressure|pressure on the government)[^.]*\b(high|low|moderate|severe)\b",
    re.IGNORECASE,
)


def test_no_starter_answer_hard_codes_a_conflicting_level(state):
    """
    Every declared starter, checked against the shared state. A level word appearing next to
    political pressure must be the word the shared state supports.
    """
    from app.simulation.ask.catalogue import STARTERS

    political = state.get("political_pressure")
    expected = LEVEL_WORDS[political.level]
    for question in STARTERS:
        response = ask(question)
        for match in LEVEL_CLAIM.finditer(response.short_answer):
            assert match.group(2).lower() == expected, (
                f"starter {question!r} claims political pressure is '{match.group(2)}'; "
                f"the shared state says '{expected}'"
            )


def test_answer_module_contains_no_authored_level_claim():
    """
    A source-level guard. The defect was a literal string in the module, and the cheapest way to
    stop it coming back is to refuse to let one be written.
    """
    from pathlib import Path

    import app.simulation.ask.answer as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    # Strip the docstrings and comments that legitimately DISCUSS the defect.
    code = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    for banned in ["political pressure is still high", "still near its peak"]:
        assert banned not in code, f"authored state claim reintroduced: {banned!r}"


# ── the classifiers themselves ────────────────────────────────────────────────────────────────────


def test_classify_level_boundaries():
    assert classify_level(0.0) is Level.none
    assert classify_level(0.01) is Level.low
    assert classify_level(0.33) is Level.moderate
    assert classify_level(0.66) is Level.high


def test_classify_direction_needs_a_window():
    direction, measured = classify_direction([0.1, 0.2])
    assert measured is False
    assert direction is Direction.not_established


def test_scenario_state_skips_malformed_stages():
    """A stage without a numeric value is omitted, never coerced to zero."""
    built = scenario_state(
        "x", 1, {"stages": [{"field": "a", "value": "UNAVAILABLE"}], "simulated_hours": 24}, []
    )
    assert "a" not in built.fields


# ── the wording a cold reader actually meets ──────────────────────────────────────────────────────


# Internal vocabulary. Each of these is meaningful to the team and meaningless to a first-time
# reader, which is the specific failure the usability reset exists to prevent. A first user does
# not know what a "run" is, what "packaged" means, or what a "tick" or "snapshot" is.
TELEMETRY_WORDS = [
    "in this run",
    "packaged run",
    "packaged snapshot",
    "packaged fictional run",
    "per tick",
    "at every tick",
    "trajectory",
    "projection",
    "chain.",
]


@pytest.mark.parametrize(
    "question",
    [
        "Brief me on the current situation.",
        "How are the economy and supply chains reacting?",
        "How are people and groups reacting?",
        "What does MERIDIAN know — and what remains uncertain?",
    ],
)
def test_starter_answers_avoid_internal_vocabulary(question):
    """
    The ANSWER a reader meets must not read like internal telemetry.

    Scoped to `short_answer` deliberately. The `limitations` list is a technical disclosure and is
    allowed to use precise terms; the sentence the reader meets first is not.
    """
    text = answer_question(question).short_answer.lower()
    for word in TELEMETRY_WORDS:
        assert word not in text, f"{question!r} answer contains internal vocabulary {word!r}"


# ── scenario position: horizon and final-tick are derived, not asserted ────────────────────────────


def test_state_carries_the_declared_horizon(run, state):
    """
    The interface says "final recorded day of this scenario". That claim needs the horizon, and it
    must come from the same shared state both surfaces read — not from a second account.
    """
    assert state.horizon_ticks == run.projection["demonstration_horizon_ticks"]
    assert state.ticks == run.projection["demonstration_horizon_ticks"]
    assert state.is_final_recorded_tick is True


def test_a_shorter_run_does_not_claim_to_be_the_end(run):
    """A run stopped early must NOT report itself as the final recorded point."""
    short = run_demonstration(DemoRunRequest(ticks=12))
    assert short.state["ticks"] == 12
    assert short.state["horizon_ticks"] == 20
    assert short.state["is_final_recorded_tick"] is False


def test_the_peak_the_interface_reports_is_the_peak_the_run_produced(state, run):
    """
    The founder read the situation as halfway through. It is three ticks past the peak, and the
    sentence saying so must be checkable against the trajectory rather than trusted.
    """
    political = state.get("political_pressure")
    series = [p["political_pressure"] for p in run.trajectory]
    assert political.peak_tick == series.index(max(series)) + 1
    assert political.peak_tick < len(series), "the peak must genuinely be in the past"
    assert political.post_peak is True
