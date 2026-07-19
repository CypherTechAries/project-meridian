"""P0.4A — adversarial isolation tests for the keyed draw service.

These are the point of P0.4A. The old shared stream would have PASSED a naive "same seed, same
result" test while still allowing an unrelated change to shift every downstream value. The tests
below are written to fail on that failure mode specifically: they add draws, reorder work, insert
entities and reject transitions, then assert that unrelated results did not move.

Numbering follows the founder's required list.
"""

from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from app.simulation.draws import (
    ALGORITHM,
    KEY_ENCODING_VERSION,
    RANDOMNESS_ARCHITECTURE,
    DeterministicDrawService,
    DrawKey,
)
from app.simulation.engine import MeridianModel
from app.simulation.state import canonical_json
from app.simulation.transitions import Transition, TransitionOrigin, TransitionType

BACKEND = Path(__file__).resolve().parents[1]
SCENARIO_PATH = BACKEND.parent / "scenarios" / "kestral-strait.json"
AUTHORITATIVE_MODULES = [
    BACKEND / "app" / "simulation" / "engine.py",
    BACKEND / "app" / "simulation" / "diffusion.py",
    BACKEND / "app" / "simulation" / "transitions.py",
    BACKEND / "app" / "simulation" / "state.py",
    BACKEND / "app" / "simulation" / "draws.py",
    BACKEND / "app" / "simulation" / "agents" / "cohort_agent.py",
    BACKEND / "app" / "simulation" / "agents" / "institutional_agent.py",
]


@pytest.fixture()
def scenario() -> dict:
    return json.loads(SCENARIO_PATH.read_text())


@pytest.fixture()
def draws() -> DeterministicDrawService:
    return DeterministicDrawService(seed=88213, scenario="kestral-strait", rule_pack="rp-1")


# --------------------------------------------------------------------------- #
# 1. Same key and seed produce the same output
# --------------------------------------------------------------------------- #
def test_same_key_same_seed_is_stable(draws: DeterministicDrawService) -> None:
    values = {draws.unit_float("macro", "noise", context="7") for _ in range(50)}
    assert len(values) == 1


def test_two_services_same_seed_agree() -> None:
    a = DeterministicDrawService(seed=5, scenario="s", rule_pack="r")
    b = DeterministicDrawService(seed=5, scenario="s", rule_pack="r")
    assert a.uint64("sub", "purp", "ent", "ctx", 3) == b.uint64("sub", "purp", "ent", "ctx", 3)


# --------------------------------------------------------------------------- #
# 2 & 3. Purpose and entity isolation
# --------------------------------------------------------------------------- #
def test_different_purposes_are_isolated(draws: DeterministicDrawService) -> None:
    a = draws.unit_float("cohort", "grievance_drift", entity="c1", context="1")
    b = draws.unit_float("cohort", "media_exposure", entity="c1", context="1")
    assert a != b


def test_different_entities_are_isolated(draws: DeterministicDrawService) -> None:
    a = draws.unit_float("cohort", "grievance_drift", entity="c1", context="1")
    b = draws.unit_float("cohort", "grievance_drift", entity="c2", context="1")
    assert a != b


def test_different_subsystems_are_isolated(draws: DeterministicDrawService) -> None:
    a = draws.unit_float("macro", "p", entity="e", context="1")
    b = draws.unit_float("diffusion", "p", entity="e", context="1")
    assert a != b


def test_different_contexts_are_isolated(draws: DeterministicDrawService) -> None:
    assert draws.unit_float("s", "p", context="1") != draws.unit_float("s", "p", context="2")


# --------------------------------------------------------------------------- #
# 4. Different seeds diverge
# --------------------------------------------------------------------------- #
def test_different_seeds_produce_different_outputs() -> None:
    a = DeterministicDrawService(seed=1).unit_float("s", "p", context="c")
    b = DeterministicDrawService(seed=2).unit_float("s", "p", context="c")
    assert a != b


def test_scenario_and_rule_pack_participate_in_the_key() -> None:
    base = DeterministicDrawService(seed=1, scenario="a", rule_pack="r1")
    other_scenario = DeterministicDrawService(seed=1, scenario="b", rule_pack="r1")
    other_rules = DeterministicDrawService(seed=1, scenario="a", rule_pack="r2")
    v = base.unit_float("s", "p")
    assert v != other_scenario.unit_float("s", "p")
    assert v != other_rules.unit_float("s", "p")


# --------------------------------------------------------------------------- #
# 5. An extra unrelated draw does not shift another result
# --------------------------------------------------------------------------- #
def test_extra_unrelated_draw_does_not_shift_another_value(draws: DeterministicDrawService) -> None:
    """THE headline P0.4A property. A shared sequential stream fails this test."""
    target_before = draws.unit_float("macro", "shipping_noise", context="12")

    # Make many unrelated draws in other subsystems, purposes and entities.
    for i in range(500):
        draws.unit_float("diffusion", "adoption_jitter", entity=f"c{i}", context="12")
        draws.uint64("cohort", "grievance_drift", entity=f"x{i}", context=str(i))

    assert draws.unit_float("macro", "shipping_noise", context="12") == target_before


# --------------------------------------------------------------------------- #
# 6 & 7. Order independence, and adding an entity
# --------------------------------------------------------------------------- #
def test_reordering_independent_entity_draws_changes_nothing(
    draws: DeterministicDrawService,
) -> None:
    ids = [f"cohort-{i}" for i in range(12)]
    forward = {e: draws.unit_float("cohort", "grievance_drift", entity=e, context="3") for e in ids}
    backward = {
        e: draws.unit_float("cohort", "grievance_drift", entity=e, context="3")
        for e in reversed(ids)
    }
    assert forward == backward


def test_adding_an_unrelated_entity_does_not_change_existing_entities(
    draws: DeterministicDrawService,
) -> None:
    existing = [f"cohort-{i}" for i in range(5)]
    before = {e: draws.unit_float("cohort", "drift", entity=e, context="1") for e in existing}

    # A new entity appears — the exact case that shifted every later draw under the old stream.
    draws.unit_float("cohort", "drift", entity="newly-materialised-person", context="1")

    after = {e: draws.unit_float("cohort", "drift", entity=e, context="1") for e in existing}
    assert after == before


# --------------------------------------------------------------------------- #
# 8. A rejected transition does not affect future draws
# --------------------------------------------------------------------------- #
def test_rejected_transition_does_not_affect_future_draws(scenario: dict) -> None:
    clean = MeridianModel(scenario=scenario, seed=88213)
    poisoned = MeridianModel(scenario=scenario, seed=88213)

    for _ in range(6):
        poisoned.submit(
            Transition(
                type=TransitionType.APPLY_MACRO_DELTAS,
                origin=TransitionOrigin.ENGINE_RULE,
                payload={"deltas": {"nonexistent_indicator": 1.0}},
            )
        )
        poisoned.submit(
            Transition(
                type=TransitionType.APPLY_MACRO_DELTAS,
                origin=TransitionOrigin.PRESENTATION,
                payload={"deltas": {"government_approval": 0.5}},
            )
        )

    clean.run(6)
    poisoned.run(6)

    assert clean.state.macro.model_dump() == poisoned.state.macro.model_dump()
    assert clean.state.narrative_adoption == poisoned.state.narrative_adoption
    assert clean.state.cohorts == poisoned.state.cohorts


# --------------------------------------------------------------------------- #
# 9. Repeated draws require explicit distinct indices
# --------------------------------------------------------------------------- #
def test_repeated_draws_need_an_explicit_index(draws: DeterministicDrawService) -> None:
    """No implicit advancement: an identical key must return an identical value."""
    first = draws.unit_float("s", "p", entity="e", context="c")
    again = draws.unit_float("s", "p", entity="e", context="c")
    assert first == again, "a draw must not advance any hidden counter"

    indexed = draws.unit_float("s", "p", entity="e", context="c", index=1)
    assert indexed != first, "an explicit index must produce an independent value"


def test_index_sequence_produces_distinct_values(draws: DeterministicDrawService) -> None:
    values = [draws.unit_float("s", "p", context="c", index=i) for i in range(64)]
    assert len(set(values)) == 64


# --------------------------------------------------------------------------- #
# 10. Promotion-style draws do not disturb unrelated state
# --------------------------------------------------------------------------- #
def test_promotion_style_draw_does_not_alter_unrelated_results(
    draws: DeterministicDrawService,
) -> None:
    """Materialising an entity must not perturb anything else (world-model G1 constraint)."""
    macro_before = draws.unit_float("macro", "shipping_noise", context="41")
    cohort_before = draws.unit_float("cohort", "drift", entity="coastal", context="41")

    for i in range(50):
        draws.uint64("entity", "materialise", entity=f"person-{i}", context="41")
        draws.bounded_int(100, "entity", "trait_roll", entity=f"person-{i}", context="41")

    assert draws.unit_float("macro", "shipping_noise", context="41") == macro_before
    assert draws.unit_float("cohort", "drift", entity="coastal", context="41") == cohort_before


# --------------------------------------------------------------------------- #
# 11. Canonical key encoding is stable and injective
# --------------------------------------------------------------------------- #
def test_canonical_key_encoding_is_stable() -> None:
    key = DrawKey(
        subsystem="cohort", purpose="drift", entity="c1", context="7", index=2,
        scenario="kestral-strait", rule_pack="rp-1",
    )
    encoded = key.canonical()
    assert encoded.startswith(KEY_ENCODING_VERSION)
    assert key.canonical() == encoded  # repeat calls agree
    # Length-prefixed so the encoding is injective.
    assert re.search(r"\d+:subsystem=\d+:cohort;", encoded)


def test_canonical_key_encoding_is_injective_across_field_boundaries() -> None:
    """Values containing separators must not be able to imitate a different field split."""
    a = DrawKey(subsystem="a", purpose="b=c", entity="", context="", index=0)
    b = DrawKey(subsystem="a", purpose="b", entity="c", context="", index=0)
    assert a.canonical() != b.canonical()

    c = DrawKey(subsystem="ab", purpose="c", entity="", context="", index=0)
    d = DrawKey(subsystem="a", purpose="bc", entity="", context="", index=0)
    assert c.canonical() != d.canonical()


def test_key_field_order_is_fixed_not_dict_order() -> None:
    k1 = DrawKey(subsystem="s", purpose="p", entity="e", context="c", index=1)
    k2 = DrawKey(index=1, context="c", entity="e", purpose="p", subsystem="s")
    assert k1.canonical() == k2.canonical()


# --------------------------------------------------------------------------- #
# 12 & 13. Static enforcement: no hash(), no global random
# --------------------------------------------------------------------------- #
def test_python_hash_is_not_used_in_authoritative_modules() -> None:
    """`hash()` is randomised per process and would make keys unstable across runs.

    Checked on the parsed AST, not on source text: these modules DISCUSS `hash()` and `random` in
    their docstrings precisely because they explain why neither is used, and a text search would
    flag that prose as a violation.
    """
    offenders = []
    for path in AUTHORITATIVE_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "hash":
                offenders.append(f"{path.name}:{node.lineno}: call to hash()")
    assert not offenders, "Python hash() found in authoritative code:\n" + "\n".join(offenders)


def test_no_global_random_calls_in_authoritative_modules() -> None:
    """No `random` import, no `random.*` call, no module-level generator in authoritative code."""
    offenders = []
    for path in AUTHORITATIVE_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "random":
                        offenders.append(f"{path.name}:{node.lineno}: imports random")
            elif isinstance(node, ast.ImportFrom) and node.module == "random":
                offenders.append(f"{path.name}:{node.lineno}: from random import ...")
            elif isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id == "random":
                    offenders.append(f"{path.name}:{node.lineno}: random.{node.attr}")
    assert not offenders, "global random usage in authoritative code:\n" + "\n".join(offenders)


def test_engine_exposes_no_unrestricted_generator(scenario: dict) -> None:
    """Domain code must not be handed a stateful PRNG it can advance."""
    model = MeridianModel(scenario=scenario, seed=1)
    assert not hasattr(model, "rng"), "engine must not expose a shared mutable RNG"
    assert isinstance(model.draws, DeterministicDrawService)
    for forbidden in ("random", "getrandbits", "shuffle", "choice"):
        assert not hasattr(model.draws, forbidden)


# --------------------------------------------------------------------------- #
# 14. Two complete runs serialise identically
# --------------------------------------------------------------------------- #
def test_two_complete_runs_serialise_identically(scenario: dict) -> None:
    a = MeridianModel(scenario=scenario, seed=88213)
    b = MeridianModel(scenario=scenario, seed=88213)
    a.run(15)
    b.run(15)
    assert canonical_json(a.state) == canonical_json(b.state)


def test_determinism_survives_a_different_process_hash_seed(scenario: dict) -> None:
    """Subprocess check: results must not depend on process-local hash randomisation.

    This is the test that would catch an accidental reliance on `hash()` or on set/dict ordering
    derived from it. Two subprocesses run with deliberately different PYTHONHASHSEED values.
    """
    code = (
        "import json,sys;"
        "sys.path.insert(0, r'%s');"
        "from app.simulation.engine import MeridianModel;"
        "from app.simulation.state import canonical_json;"
        "sc=json.load(open(r'%s'));"
        "m=MeridianModel(scenario=sc, seed=88213); m.run(8);"
        "print(canonical_json(m.state))" % (BACKEND, SCENARIO_PATH)
    )
    outputs = []
    for hashseed in ("0", "1", "12345"):
        proc = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            # Inherit the real environment and override ONLY the hash seed. Blanking PATH
            # breaks Windows socket-provider loading and would fail for an unrelated reason.
            env={**os.environ, "PYTHONHASHSEED": hashseed},
        )
        assert proc.returncode == 0, proc.stderr
        outputs.append(proc.stdout.strip())
    assert len(set(outputs)) == 1, "authoritative state depends on process hash randomisation"


# --------------------------------------------------------------------------- #
# Numeric properties of the mapping
# --------------------------------------------------------------------------- #
def test_unit_float_is_in_range_and_well_distributed(draws: DeterministicDrawService) -> None:
    values = [draws.unit_float("s", "p", context=str(i)) for i in range(2000)]
    assert all(0.0 <= v < 1.0 for v in values)
    # A crude uniformity sanity check, not a statistical claim.
    buckets = [0] * 10
    for v in values:
        buckets[int(v * 10)] += 1
    assert all(b > 100 for b in buckets), f"suspicious bucket distribution: {buckets}"


def test_bounded_int_is_in_range_and_hits_every_value(draws: DeterministicDrawService) -> None:
    seen = {draws.bounded_int(7, "s", "p", context=str(i)) for i in range(400)}
    assert seen == set(range(7))


def test_bounded_int_rejects_non_positive_bound(draws: DeterministicDrawService) -> None:
    with pytest.raises(ValueError):
        draws.bounded_int(0, "s", "p")


def test_jitter_is_symmetric_and_bounded(draws: DeterministicDrawService) -> None:
    values = [draws.jitter(0.01, "s", "p", context=str(i)) for i in range(500)]
    assert all(-0.01 <= v < 0.01 for v in values)
    assert any(v < 0 for v in values) and any(v > 0 for v in values)


# --------------------------------------------------------------------------- #
# Draw references
# --------------------------------------------------------------------------- #
def test_draw_reference_identifies_the_draw(draws: DeterministicDrawService) -> None:
    ref = draws.reference("cohort", "grievance_drift", entity="c1", context="7", index=0)
    assert ref.algorithm == ALGORITHM
    assert ref.key_encoding == KEY_ENCODING_VERSION
    assert ref.subsystem == "cohort" and ref.purpose == "grievance_drift"
    assert ref.entity == "c1" and ref.context == "7"
    assert ref.digest
    # Same inputs ⇒ same reference and digest.
    assert draws.reference("cohort", "grievance_drift", entity="c1", context="7").digest == ref.digest


def test_reference_does_not_consume_anything(draws: DeterministicDrawService) -> None:
    before = draws.unit_float("macro", "noise", context="3")
    for _ in range(20):
        draws.reference("macro", "noise", context="3")
    assert draws.unit_float("macro", "noise", context="3") == before


def test_architecture_constant_is_recorded() -> None:
    assert RANDOMNESS_ARCHITECTURE == "keyed_counter_v1"
