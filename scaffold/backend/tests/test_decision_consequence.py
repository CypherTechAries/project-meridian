"""
Kestral Consequence Slice v0.2, build step 1 — decisions reach the tick loop and change the world.

WHAT THIS CLOSES. A submitted action used to be appended to a list `step()` never read, so choosing
an option changed nothing. These tests hold the loop that replaced it:

    submitted decision → validate → queue → consume exactly once → resolve through the versioned
    deterministic rule → mutate authoritative state → append events → next situation

DETERMINISTIC. No random draw is taken in decision resolution and the shared RNG is not touched.
`same state + same action + same rule version = same consequence and explanation` is asserted
directly, not assumed.
"""

from __future__ import annotations

import inspect

import pytest

from app.safety import load_packaged_scenario
from app.simulation import decisions as decisions_module
from app.simulation.decisions import (
    BAND_FULL,
    BAND_PARTIAL,
    DECLARED_OPTIONS,
    RESOLUTION_RULE_VERSION,
    Outcome,
    ResolutionInputs,
    band_for,
    resolve,
)
from app.simulation.engine import MeridianModel
from app.simulation.transitions import Transition, TransitionOrigin, TransitionType

OPTION = "emergency_support_fishing_households"
COHORT = "coastal-creole-fishing"


def build() -> MeridianModel:
    return MeridianModel(scenario=load_packaged_scenario("kestral-strait"), seed=88213)


def queue(model: MeridianModel, submission_id: str = "sub-001", option_id: str = OPTION):
    return model.submit(
        Transition(
            type=TransitionType.QUEUE_PLAYER_DECISION,
            origin=TransitionOrigin.PLAYER_DECISION,
            payload={
                "submission_id": submission_id,
                "option_id": option_id,
                "apply_at_tick": model.tick + 1,
            },
        )
    )


def run(decide_at: int | None = None, ticks: int = 12, submission_id: str = "sub-001"):
    m = build()
    for _ in range(ticks):
        if decide_at is not None and m.tick == decide_at:
            queue(m, submission_id)
        m.step()
    return m


# ── 1-2 · the decision reaches the loop, and is consumed exactly once ─────────────────────────────


def test_01_a_valid_decision_reaches_the_tick_loop():
    m = run(decide_at=6)
    assert len(m.state.decision_log) == 1
    entry = m.state.decision_log[0]
    assert entry["option_id"] == OPTION
    assert entry["consumed_tick"] > entry["submitted_tick"]


def test_02_consumed_exactly_once():
    m = run(decide_at=6)
    assert m.state.consumed_submissions == ["sub-001"]
    assert m.state.decision_queue == []
    # And the log holds one entry, not one per subsequent tick.
    assert len(m.state.decision_log) == 1


# ── 3 · reproducibility ──────────────────────────────────────────────────────────────────────────


def test_03_same_state_and_decision_reproduce_the_same_result():
    a, b = run(decide_at=6), run(decide_at=6)
    assert a.state.decision_log == b.state.decision_log
    assert a.state.government.model_dump() == b.state.government.model_dump()
    assert a.state.chain.model_dump() == b.state.chain.model_dump()
    assert a.state.cohorts[COHORT].economic_concern == b.state.cohorts[COHORT].economic_concern


# ── 4 · no decision means no decision-caused change ──────────────────────────────────────────────


def test_04_no_decision_means_no_decision_caused_change():
    m = run()
    assert m.state.decision_log == []
    assert m.state.consumed_submissions == []
    assert m.state.delayed_effects == []
    # Resources are untouched: nothing spent them.
    scenario = load_packaged_scenario("kestral-strait")["government_resources"]
    assert m.state.government.budget_reserve_m == scenario["budget_reserve_m"]
    assert m.state.government.political_capital == scenario["political_capital"]


# ── 5-6 · idempotency and availability ───────────────────────────────────────────────────────────


def test_05_duplicate_submission_does_not_duplicate_effects():
    m = build()
    for _ in range(6):
        m.step()
    first = queue(m, "sub-001")
    assert first.applied is True

    # Same id again while queued — refused.
    again = queue(m, "sub-001")
    assert again.applied is False
    assert any("already queued" in e for e in again.validation.errors)

    m.step()  # consumed here
    spent_once = m.state.government.budget_reserve_m

    # Same id again after consumption — still refused, and nothing is spent twice.
    after = queue(m, "sub-001")
    assert after.applied is False
    assert any("already been consumed" in e for e in after.validation.errors)
    m.step()
    assert m.state.government.budget_reserve_m == spent_once
    assert len(m.state.decision_log) == 1


def test_06_an_unavailable_decision_cannot_mutate_state():
    m = build()
    for _ in range(6):
        m.step()
    before = m.state.model_dump_json()
    rec = queue(m, "sub-bad", option_id="nationalise_the_fishing_fleet")
    assert rec.applied is False
    assert any("unknown or unavailable option" in e for e in rec.validation.errors)
    assert m.state.model_dump_json() == before


# ── 7 · every outcome is reachable from declared counterfactual state ────────────────────────────


@pytest.mark.parametrize(
    "capacity,budget,expected",
    [
        (0.72, 240.0, Outcome.FULL_SUCCESS),      # the packaged state
        (0.40, 240.0, Outcome.PARTIAL_SUCCESS),   # capacity-limited
        (0.72, 90.0, Outcome.PARTIAL_SUCCESS),    # budget-limited
        (0.10, 240.0, Outcome.FAILURE),           # far too little capacity
    ],
)
def test_07_outcomes_are_reachable_from_declared_state(capacity, budget, expected):
    r = resolve(
        OPTION,
        ResolutionInputs(
            implementation_capacity=capacity,
            budget_reserve_m=budget,
            political_capital=0.7,
            affected_population=14200,
        ),
        current_concern=0.36,
        current_employment_pressure=0.44,
    )
    assert r.outcome is expected


def test_07a_an_unknown_option_resolves_invalid_and_spends_nothing():
    r = resolve(
        "not_a_real_option",
        ResolutionInputs(
            implementation_capacity=0.9, budget_reserve_m=999.0,
            political_capital=0.9, affected_population=1,
        ),
        current_concern=0.3, current_employment_pressure=0.4,
    )
    assert r.outcome is Outcome.INVALID_OR_UNAVAILABLE
    assert r.budget_spent_m == 0.0
    assert r.political_capital_spent == 0.0
    assert r.immediate_effects == [] and r.delayed_effects == []


def test_07b_no_cliff_at_band_edges():
    """
    The label is banded; the MAGNITUDE is continuous. An insignificant numerical change must not
    produce a completely different world — only a different word.
    """
    req = DECLARED_OPTIONS[OPTION].required_capability

    def at(capacity: float):
        return resolve(
            OPTION,
            ResolutionInputs(implementation_capacity=capacity, budget_reserve_m=240.0,
                             political_capital=0.7, affected_population=14200),
            current_concern=0.36, current_employment_pressure=0.44,
        )

    just_under = at(req * (BAND_PARTIAL - 0.001))
    just_over = at(req * (BAND_PARTIAL + 0.001))
    assert just_under.outcome is Outcome.FAILURE
    assert just_over.outcome is Outcome.PARTIAL_SUCCESS
    # The world barely moves across the edge: spending differs by well under 1% of the requirement.
    assert abs(just_over.budget_spent_m - just_under.budget_spent_m) < 2.0


def test_07c_bands_are_declared_and_ordered():
    assert 0.0 < BAND_PARTIAL < BAND_FULL <= 1.0
    assert band_for(1.0) is Outcome.FULL_SUCCESS
    assert band_for(BAND_PARTIAL) is Outcome.PARTIAL_SUCCESS
    assert band_for(0.0) is Outcome.FAILURE


# ── 8 · the explanation matches the inputs and the changes ───────────────────────────────────────


def test_08_the_explanation_matches_the_exact_inputs_and_state_changes():
    m = run(decide_at=6)
    entry = m.state.decision_log[0]
    text = entry["explanation"]

    # The numbers it cites are the numbers it used.
    assert f"{entry['inputs']['implementation_capacity']:.2f}" in text
    assert f"{entry['budget_spent_m']:.0f}m" in text
    assert f"{entry['political_capital_spent']:.2f}" in text
    # And the trace identifies the rule that produced it.
    assert entry["rule_version"] == RESOLUTION_RULE_VERSION
    assert entry["limiting_factor"]


def test_08a_the_trace_records_everything_required():
    m = run(decide_at=6)
    e = m.state.decision_log[0]
    for key in (
        "submission_id", "option_id", "submitted_tick", "consumed_tick", "rule", "rule_version",
        "inputs", "outcome", "effectiveness", "limiting_factor", "budget_spent_m",
        "political_capital_spent", "immediate_effects", "delayed_effects", "explanation",
    ):
        assert key in e, key


# ── 9 · the choice changes the next situation ────────────────────────────────────────────────────


def test_09_the_selected_action_changes_the_world():
    base, decided = run(), run(decide_at=6)

    # Cost paid.
    assert decided.state.government.budget_reserve_m < base.state.government.budget_reserve_m
    assert decided.state.government.political_capital < base.state.government.political_capital
    # Immediate effect: the affected cohort is less concerned.
    assert decided.state.cohorts[COHORT].economic_concern < base.state.cohorts[COHORT].economic_concern
    # Delayed effect landed: employment exposure eased.
    assert decided.state.chain.employment_pressure < base.state.chain.employment_pressure


def test_09a_the_delayed_effect_lands_later_than_the_decision():
    m = build()
    for _ in range(6):
        m.step()
    queue(m)
    m.step()  # consumed
    assert m.state.delayed_effects, "a delayed effect must be scheduled, not applied immediately"
    due = m.state.delayed_effects[0].due_tick
    assert due > m.tick
    while m.tick < due:
        m.step()
    assert m.state.delayed_effects == [], "the delayed effect must be applied and retired"


def test_09b_the_declared_adversary_responds():
    m = run(decide_at=6)
    entry = m.state.decision_log[0]
    assert entry["adversary_response"] is not None
    # It is the SCENARIO'S declared campaign, not an invented actor.
    assert any(
        r.actor and "camp" in str(r.actor) and r.applied
        for r in m.transition_log
    )


# ── 10-11 · no undeclared channel, and no new randomness ─────────────────────────────────────────


def test_10_unrelated_state_does_not_change_through_an_undeclared_channel():
    base, decided = run(), run(decide_at=6)
    # A cohort the option does not touch, and which sits outside the affected chain path.
    # `inland-highland-minority` declares NO bridges in the diffusion graph, so nothing the
    # decision touches can legitimately reach it.
    untouched = "inland-highland-minority"
    assert (
        decided.state.cohorts[untouched].beliefs
        == base.state.cohorts[untouched].beliefs
    ), "a decision must not move an unbridged cohort's beliefs through an undeclared channel"
    # Its `economic_concern` DOES move, and that is correct rather than a leak: concern is
    # computed from the shared `employment_pressure`, which the decision genuinely eased
    # nationally. Easing port employment eases everyone's exposure a little. The declared channel
    # is chain.employment_pressure -> household pressure -> cohort concern, and the movement is
    # in the direction the chain implies.
    assert (
        decided.state.cohorts[untouched].economic_concern
        < base.state.cohorts[untouched].economic_concern
    ), "support eased national employment pressure, so concern should fall, not rise"
    assert decided.state.chain.employment_pressure < base.state.chain.employment_pressure

    # Every RESOLUTION transition names the fields it read and the rule version that produced it.
    # Queueing is excluded deliberately: it reads no state, it only records an intent, so it has
    # no inputs to declare. Requiring them there would be a false guarantee.
    for record in decided.transition_log:
        if (
            record.origin is TransitionOrigin.PLAYER_DECISION
            and record.applied
            and record.type is not TransitionType.QUEUE_PLAYER_DECISION
        ):
            assert record.source_fields, f"{record.type} applied without declaring its inputs"
            assert record.mechanism_version, f"{record.type} applied without a rule version"


def test_11_no_new_random_draw_was_introduced():
    """
    Decision resolution must not sample.

    NOTE, corrected: P0.4A **is** implemented. `DeterministicDrawService` gives keyed draws that
    are a pure function of (run seed, canonical key), so there is no shared stream to displace and
    a draw here would still be reproducible. `scaffold/CLAUDE.md` still says otherwise and is
    stale.

    The rule still takes no draw, for a different and better reason: this milestone has no
    modelled probability, and an outcome that cannot be explained from declared state cannot be
    explained at all.
    """
    source = inspect.getsource(decisions_module)
    code_lines = []
    in_doc = False
    for line in source.splitlines():
        stripped = line.strip()
        if stripped.startswith('"""') or stripped.endswith('"""'):
            in_doc = not in_doc if stripped.count('"""') == 1 else in_doc
            continue
        if in_doc or stripped.startswith("#"):
            continue
        code_lines.append(line)
    code = "\n".join(code_lines)

    for banned in ("random.", "randint", "uniform(", "choice(", "shuffle(", "gauss("):
        assert banned not in code, "decision resolution must not use " + banned

    # It does not request a keyed draw either.
    assert ".draws" not in code, "decision resolution must not request a keyed draw"


def test_11a_no_probability_language_in_the_rule_or_its_output():
    source = inspect.getsource(decisions_module)
    m = run(decide_at=6)
    text = m.state.decision_log[0]["explanation"].lower()
    for banned in ("probability", "% chance", "likelihood", "odds of"):
        assert banned not in text, f"explanation must not use probability language: {banned}"
    assert "probability" not in source.lower().replace("no probability", "")


# ── 12 · determinism, including the new clause ───────────────────────────────────────────────────


def test_12_determinism_now_includes_ordered_decisions():
    """
    The determinism claim gains a clause: same scenario, seed, ticks AND ordered decisions.
    A DIFFERENT decision tick must produce a different world — otherwise the loop is inert.
    """
    same_a, same_b = run(decide_at=6), run(decide_at=6)
    assert same_a.state.chain.model_dump() == same_b.state.chain.model_dump()

    earlier = run(decide_at=3)
    assert earlier.state.chain.model_dump() != same_a.state.chain.model_dump(), (
        "deciding at a different tick must change the outcome, or decisions are not consequential"
    )
