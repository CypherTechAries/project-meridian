"""
Virtual Person VP-1 — schema, fixture-identity boundary, origins and invariants.

VP-1 establishes what a fictional person IS in the data. These tests prove the boundary holds:
identity is inert, reserved state never claims to be an engine result, missing is never zero,
prohibited ranking fields cannot exist, trust is always scoped, and identity can never reach a
decision.
"""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

from app.simulation.belief import cast
from app.simulation.belief.organisations import OrganisationInput, aggregate
from app.simulation.belief.projection import person_projection
from app.simulation.person.schema import (
    DECISION_INPUT_FIELDS,
    EXCLUDED_FROM_DECISIONS,
    PROHIBITED_FIELD_FRAGMENTS,
    DecisionInputs,
    Explanations,
    FixtureIdentity,
    LayerStatus,
    ModelBoundary,
    PersonRef,
    PersonState,
    Relationship,
    RelationshipType,
    VirtualPerson,
    from_cast,
    resolve_person_ref,
)

JOURNALIST = "broadcast-journalist"
TYPED = f"fict:{cast.SCENARIO_ID}:person:{JOURNALIST}"

ALL_MODELS = (VirtualPerson, FixtureIdentity, PersonState, Explanations, ModelBoundary,
              Relationship, DecisionInputs, PersonRef)


def all_field_names() -> set[str]:
    names: set[str] = set()
    for m in ALL_MODELS:
        names |= set(m.model_fields)
    return names


# ══ 1–4 · SCHEMA LOADS, REJECTS UNKNOWN AND BAD IDS ═══════════════════════════════════════════════


def test_01_valid_fictional_person_schema_loads() -> None:
    vp = from_cast(JOURNALIST)
    assert vp.schema_version == "virtual-person@0.1"
    assert vp.identity.person_ref.typed_id() == TYPED
    VirtualPerson.model_validate(vp.model_dump(mode="json"))


def test_02_unknown_fields_are_rejected() -> None:
    good = from_cast(JOURNALIST).model_dump(mode="json")
    good["identity"]["susceptibility"] = 0.8            # hostile injection
    with pytest.raises(ValidationError):
        VirtualPerson.model_validate(good)
    with pytest.raises(ValidationError):
        FixtureIdentity(person_ref=PersonRef(scenario_id=cast.SCENARIO_ID, entity_id=JOURNALIST),
                        display_name="x", intelligence=9)  # type: ignore[call-arg]


def test_03_cross_world_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="cross-world"):
        resolve_person_ref("fict:some-other-world:person:broadcast-journalist")
    with pytest.raises(ValueError, match="cross-world"):
        PersonRef(scenario_id="elsewhere", entity_id=JOURNALIST)


def test_04_wrong_entity_kinds_are_rejected() -> None:
    with pytest.raises(ValueError):
        resolve_person_ref(f"fict:{cast.SCENARIO_ID}:organisation:{JOURNALIST}")
    with pytest.raises(ValueError):
        resolve_person_ref(f"fict:{cast.SCENARIO_ID}:agent:{JOURNALIST}")
    with pytest.raises(ValueError):
        PersonRef(scenario_id=cast.SCENARIO_ID, entity_id=JOURNALIST, entity_kind="cohort")


def test_04b_free_text_and_unknown_people_are_rejected() -> None:
    for bad in ("BBC News", "a real journalist", JOURNALIST, "Reuters"):
        with pytest.raises(ValueError):
            resolve_person_ref(bad)
    with pytest.raises(ValueError, match="no person"):
        PersonRef(scenario_id=cast.SCENARIO_ID, entity_id="nobody")


# ══ 5–6 · ORIGINS ═════════════════════════════════════════════════════════════════════════════════


def test_05_fixture_identity_reports_fixture_origin() -> None:
    vp = from_cast(JOURNALIST)
    assert vp.identity.origin.value == "FIXTURE"
    with pytest.raises(ValueError, match="FIXTURE"):
        FixtureIdentity(person_ref=vp.identity.person_ref, display_name="x",
                        origin=vp.identity.origin.__class__.engine)


def test_06_unimplemented_engine_layers_do_not_report_engine() -> None:
    vp = from_cast(JOURNALIST)
    assert vp.state.status is LayerStatus.not_modelled
    assert vp.explanations.status is LayerStatus.not_modelled
    assert vp.state.status is not LayerStatus.engine
    with pytest.raises(ValueError, match="must not report ENGINE"):
        PersonState(status=LayerStatus.engine)
    with pytest.raises(ValueError, match="must not report ENGINE"):
        Explanations(status=LayerStatus.engine)


# ══ 7–9 · PORTRAIT NULL, MISSING NEVER ZERO ═══════════════════════════════════════════════════════


def test_07_portrait_ref_may_be_null() -> None:
    vp = from_cast(JOURNALIST)
    assert vp.identity.portrait_ref is None


def test_08_null_portrait_does_not_invalidate_a_person() -> None:
    vp = from_cast(JOURNALIST)
    assert vp.identity.portrait_ref is None
    VirtualPerson.model_validate(vp.model_dump(mode="json"))  # round-trips fine


def test_09_missing_values_never_serialise_as_zero() -> None:
    data = from_cast(JOURNALIST).model_dump(mode="json")

    def walk(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                # a missing descriptive/state value must be null or an empty collection, never 0
                if v == 0 and not isinstance(v, bool):
                    raise AssertionError(f"{path}.{k} serialised as numeric zero")
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, item in enumerate(node):
                walk(item, f"{path}[{i}]")

    walk(data)
    # missing descriptive fields are explicitly null, not empty invented prose
    for f in ("portrait_ref", "life_stage", "organisation_ref", "community_ref"):
        assert data["identity"][f] is None


# ══ 10 · DECISION INPUT EXCLUSION ═════════════════════════════════════════════════════════════════


def test_10_identity_fields_are_absent_from_the_decision_input_shape() -> None:
    fields = set(DecisionInputs.model_fields)
    assert fields == set(DECISION_INPUT_FIELDS)
    for excluded in EXCLUDED_FROM_DECISIONS:
        assert excluded not in fields, f"a decision must never receive '{excluded}'"
    # portrait / biography / display_name / occupation / education / socioeconomic / life_stage
    for name in ("portrait", "biograph", "display_name", "occupation", "education",
                 "socioeconomic", "life_stage"):
        assert not any(name in f for f in fields)


# ══ 11 · PROHIBITED FIELDS ════════════════════════════════════════════════════════════════════════


def test_11_no_ranking_or_profiling_field_exists() -> None:
    for field in all_field_names():
        low = field.lower()
        for banned in PROHIBITED_FIELD_FRAGMENTS:
            assert banned not in low, f"prohibited field '{field}' (matched '{banned}')"


def test_11b_prohibited_fields_are_rejected_if_injected() -> None:
    base = from_cast(JOURNALIST).model_dump(mode="json")
    for bad in ("influence_rank", "susceptibility", "competence_score", "universal_trust"):
        hostile = json.loads(json.dumps(base))
        hostile["identity"][bad] = 1
        with pytest.raises(ValidationError):
            VirtualPerson.model_validate(hostile)


# ══ 12–13 · IMMUTABILITY AND DETERMINISM ══════════════════════════════════════════════════════════


def test_12_public_models_are_immutable() -> None:
    vp = from_cast(JOURNALIST)
    with pytest.raises(ValidationError):
        vp.identity.display_name = "changed"  # type: ignore[misc]
    with pytest.raises(ValidationError):
        vp.state.status = LayerStatus.engine    # type: ignore[misc]


def test_13_serialisation_is_deterministic() -> None:
    a = json.dumps(from_cast(JOURNALIST).model_dump(mode="json"), sort_keys=True)
    b = json.dumps(from_cast(JOURNALIST).model_dump(mode="json"), sort_keys=True)
    assert a == b


# ══ 14 · STRUCTURALLY DISTINCT KINDS ══════════════════════════════════════════════════════════════


def test_14_a_person_cannot_be_parsed_as_an_organisation_or_cohort() -> None:
    with pytest.raises(ValueError):
        PersonRef(scenario_id=cast.SCENARIO_ID, entity_id="public-broadcaster")  # an org id
    with pytest.raises(ValueError):
        PersonRef(scenario_id=cast.SCENARIO_ID, entity_id="port-workers")        # a cohort id
    # a person id is not in the org or cohort registries
    assert JOURNALIST not in {o["organisation_id"] for o in cast.ORGANISATIONS}
    assert JOURNALIST not in {c["cohort_id"] for c in cast.COHORTS}


# ══ 15 · NOT_MODELLED IS DISTINCT ═════════════════════════════════════════════════════════════════


def test_15_not_modelled_is_distinct_from_unknown_and_unavailable() -> None:
    vals = {s.value for s in LayerStatus}
    assert {"NOT_MODELLED", "UNKNOWN", "UNAVAILABLE"} <= vals
    assert LayerStatus.not_modelled is not LayerStatus.unknown
    assert LayerStatus.not_modelled is not LayerStatus.unavailable
    assert len({LayerStatus.not_modelled, LayerStatus.unknown, LayerStatus.unavailable}) == 3


# ══ 16 · TRUSTS_FOR SCOPE ═════════════════════════════════════════════════════════════════════════


def test_16_an_unscoped_trusts_for_relationship_is_invalid() -> None:
    with pytest.raises(ValueError, match="subject"):
        Relationship(relationship_type=RelationshipType.trusts_for, target="fict:x:person:y")
    with pytest.raises(ValueError, match="subject"):
        Relationship(relationship_type=RelationshipType.trusts_for, target="y", subject="   ")
    ok = Relationship(relationship_type=RelationshipType.trusts_for, target="y",
                      subject="P-WARNINGS-IGNORED")
    assert ok.subject == "P-WARNINGS-IGNORED"
    # non-trust edges do not require a subject
    Relationship(relationship_type=RelationshipType.reports_to, target="org")


def test_16b_no_relationship_carries_a_strength_or_score() -> None:
    for f in Relationship.model_fields:
        for banned in ("strength", "score", "weight", "influence", "trust_value"):
            assert banned not in f.lower()


# ══ 17–18 · IDENTITY DOES NOT AFFECT BELIEF OUTPUT ════════════════════════════════════════════════


def test_17_biography_does_not_alter_belief_output() -> None:
    before = person_projection(JOURNALIST).model_dump(mode="json")
    # building Virtual Persons with wildly different biographies changes nothing downstream
    for bio in (None, "a", "an utterly different fictional life story " * 5):
        vp = FixtureIdentity(
            person_ref=PersonRef(scenario_id=cast.SCENARIO_ID, entity_id=JOURNALIST),
            display_name="Correspondent", biography=bio)
        assert vp.biography == bio
    after = person_projection(JOURNALIST).model_dump(mode="json")
    assert before == after, "belief output must not depend on biography"


def test_18_portrait_reference_does_not_alter_belief_output() -> None:
    before = person_projection(JOURNALIST).model_dump(mode="json")
    for portrait in (None, "assets/people/x.png", "assets/people/COMPLETELY-DIFFERENT.png"):
        vp = FixtureIdentity(
            person_ref=PersonRef(scenario_id=cast.SCENARIO_ID, entity_id=JOURNALIST),
            display_name="Correspondent", portrait_ref=portrait)
        assert vp.portrait_ref == portrait
    after = person_projection(JOURNALIST).model_dump(mode="json")
    assert before == after, "belief output must not depend on portrait"


# ══ 19 · COVERAGE OF ALL THREE PEOPLE + THE ADAPTER ═══════════════════════════════════════════════


def test_19_every_cast_person_adapts_cleanly() -> None:
    for p in cast.PEOPLE:
        vp = from_cast(p["person_id"])
        assert vp.identity.origin.value == "FIXTURE"
        assert vp.identity.portrait_ref is None
        assert vp.identity.display_name == p["display_name"]   # existing label, not invented
        assert vp.state.status is LayerStatus.not_modelled
    with pytest.raises(ValueError, match="no person"):
        from_cast("not-in-the-cast")


def test_20_boundary_names_the_never_modelled_traits() -> None:
    boundary = from_cast(JOURNALIST).model_boundary.not_modelled
    for trait in ("intelligence", "competence", "moral worth", "susceptibility", "persuadability"):
        assert trait in boundary
