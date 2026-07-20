"""
Descriptive metadata is inert.

Background describes the world someone has moved through. It must never act as a proxy for
intelligence, competence, judgement or gullibility, and it must not reach the calculation at all.

These tests prove inertness by MUTATION rather than by assertion of absence: change the metadata,
re-run, and require the numbers not to move. A structural check alone would pass even if a future
change quietly wired the layer in.
"""

from __future__ import annotations

import ast
import inspect
import io
import tokenize
from contextlib import contextmanager

import pytest

from app.simulation.belief import cast
from app.simulation.belief import thresholds as th
from app.simulation.belief import update as upd
from app.simulation.belief.thresholds import ThresholdKind
from app.simulation.belief.update import UpdateInput, apply_update

FACTUAL = "P-WARNINGS-IGNORED"
PEOPLE_IDS = ["family-spokesperson", "government-minister", "broadcast-journalist"]

DESCRIPTIVE_FIELDS = (
    "occupation_description",
    "education_history",
    "socioeconomic_description",
    "public_biography",
    "role_narrative",
)


def _result(eid: str):
    reg = cast.threshold_registry()
    ex = {e["entity_id"]: e for e in cast.EXPOSURES}[eid]
    prior = cast.PRIORS[(eid, FACTUAL)]
    return apply_update(
        UpdateInput(
            prior_credence=prior["credence"],
            prior_confidence=prior["confidence"],
            prior_salience=prior["salience"],
            evidentiary_threshold=reg.value_for(eid, FACTUAL, expect=ThresholdKind.verification),
            source_trust=cast.SOURCE_TRUST[eid][cast.SHARED_EVENT["source_category"]],
            evidence_strength=cast.SHARED_EVENT["evidence_strength"],
            exposure_intensity=ex["intensity"],
            relay_factor=ex["relay"],
            relevance=cast.RELEVANCE[eid],
            claim_direction=cast.SHARED_EVENT["claim_direction"],
        )
    )


def snapshot() -> dict:
    return {e: (_result(e).credence, _result(e).confidence, _result(e).signal_weight)
            for e in PEOPLE_IDS}


@contextmanager
def descriptive_restored():
    """Mutate freely; the original metadata is always put back."""
    original = {k: dict(v) for k, v in cast.DESCRIPTIVE.items()}
    try:
        yield
    finally:
        cast.DESCRIPTIVE.clear()
        cast.DESCRIPTIVE.update(original)


def executable_source(module) -> str:
    """Source with comments and docstrings stripped — the prohibition is on code, not on prose."""
    src = inspect.getsource(module)
    toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type != tokenize.COMMENT]
    tree = ast.parse(tokenize.untokenize(toks))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                body.pop(0)
    return ast.unparse(tree)


# ── 1-3: changing a single descriptive field moves nothing ───────────────────────────────────────


@pytest.mark.parametrize(
    "field", ["education_history", "occupation_description", "socioeconomic_description"]
)
def test_01_03_changing_a_descriptive_field_changes_no_result(field: str) -> None:
    before = snapshot()
    with descriptive_restored():
        for eid in PEOPLE_IDS:
            cast.DESCRIPTIVE[eid][field] = "Entirely different fictional description."
        assert snapshot() == before, f"changing {field} altered a calculation"


# ── 4: swapping whole profiles ───────────────────────────────────────────────────────────────────


def test_04_swapping_complete_descriptive_profiles_changes_nothing() -> None:
    """
    The strongest form: give the minister the journalist's entire background and vice versa. If any
    result moves, biography is doing work the declared inputs should be doing.
    """
    before = snapshot()
    with descriptive_restored():
        a, b = "government-minister", "broadcast-journalist"
        cast.DESCRIPTIVE[a], cast.DESCRIPTIVE[b] = cast.DESCRIPTIVE[b], cast.DESCRIPTIVE[a]
        assert snapshot() == before, "swapping descriptive profiles altered a calculation"


# ── 5: removing it entirely ──────────────────────────────────────────────────────────────────────


def test_05_removing_descriptive_metadata_changes_nothing() -> None:
    before = snapshot()
    with descriptive_restored():
        cast.DESCRIPTIVE.clear()
        assert snapshot() == before, "removing descriptive metadata altered a calculation"


# ── 6-8: the resolution paths cannot consume it ──────────────────────────────────────────────────


def test_06_update_input_cannot_accept_descriptive_fields() -> None:
    fields = set(UpdateInput.__dataclass_fields__)
    for f in DESCRIPTIVE_FIELDS:
        assert f not in fields
    for f in DESCRIPTIVE_FIELDS:
        with pytest.raises(TypeError):
            UpdateInput(
                prior_credence=0.5, prior_confidence=0.5, prior_salience=0.5,
                evidentiary_threshold=0.5, source_trust=0.5, evidence_strength=0.5,
                exposure_intensity=0.5, relay_factor=1.0, relevance=0.5, claim_direction=1,
                **{f: "x"},
            )


def test_07_threshold_resolution_cannot_consume_descriptive_fields() -> None:
    from app.simulation.belief.thresholds import ContextualThreshold

    for f in DESCRIPTIVE_FIELDS:
        assert f not in ContextualThreshold.model_fields
    src = executable_source(th)
    for f in DESCRIPTIVE_FIELDS:
        assert f not in src


def test_08_source_trust_resolution_cannot_consume_descriptive_fields() -> None:
    """Trust is keyed by source CATEGORY only — no descriptive dimension exists to key on."""
    for entity, by_category in cast.SOURCE_TRUST.items():
        assert set(by_category).issubset(set(cast.SOURCE_CATEGORIES))
        for f in DESCRIPTIVE_FIELDS:
            assert f not in by_category


# ── 9: no executable branch on background ────────────────────────────────────────────────────────


def test_09_no_executable_update_branch_refers_to_background() -> None:
    src = executable_source(upd).lower()
    for term in (
        "education", "occupation", "wealth", "socioeconomic", "biography", "bio",
        "intelligence", "competence", "prestige", "sophistication", "rationality",
    ):
        assert term not in src, f"update module refers to '{term}'"


# ── 10: never in a trace ─────────────────────────────────────────────────────────────────────────


def test_10_descriptive_metadata_never_appears_in_a_calculation_trace() -> None:
    for eid in PEOPLE_IDS:
        trace = _result(eid).trace
        flat = " ".join(str(v) for v in trace.values()).lower()
        for f in DESCRIPTIVE_FIELDS:
            assert f not in trace
        for value in cast.DESCRIPTIVE[eid].values():
            assert value.lower() not in flat, "descriptive text leaked into a calculation trace"


# ── No implicit capability scale ─────────────────────────────────────────────────────────────────


def test_11_descriptive_layer_contains_no_scores_only_text() -> None:
    """
    Every descriptive value is a string. A numeric field here would be the beginning of a
    socioeconomic or prestige scale, which is exactly what must not exist.
    """
    for eid, record in cast.DESCRIPTIVE.items():
        for key, value in record.items():
            assert isinstance(value, str), f"{eid}.{key} is not text"
            assert key in DESCRIPTIVE_FIELDS
    for banned in ("rank", "score", "level", "tier", "class_index", "prestige"):
        for record in cast.DESCRIPTIVE.values():
            assert not any(banned in k for k in record)
