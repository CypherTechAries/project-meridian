"""
B5-03 / B5-05 / B5-06 — direct evidence for the target-kind vocabulary.

WHY THIS FILE EXISTS. `person` and `organisation` were added to the B5 closed vocabulary for the
Belief Formation and Divergence Slice, and `institution` was removed. The pre-existing 70-test suite
passing is NOT evidence for kinds that were not previously representable — it never exercised them.
This file supplies that evidence directly.

Numbering follows the founder's required list so the mapping is auditable.
"""

from __future__ import annotations

import pytest

from app.safety import B5Violation, FictionalTargetRegistry, load_packaged_scenario
from app.safety.controls import TARGET_KINDS
from app.simulation.belief.schemas import MessageTarget

SCENARIO_ID = "kestral-strait"
OTHER_WORLD = "vantaran-basin"


@pytest.fixture(scope="module")
def scenario() -> dict:
    return load_packaged_scenario(SCENARIO_ID)


@pytest.fixture(scope="module")
def registry(scenario: dict) -> FictionalTargetRegistry:
    """
    The packaged scenario carries no `people` or `organisations` yet — the belief-slice cast lands
    in the next step. Registering them here proves the REGISTRY mechanism for the new kinds without
    waiting for the fixtures, which is exactly what this hardening pass is for.
    """
    enriched = {
        **scenario,
        "people": [
            {"person_id": "family-spokesperson"},
            {"person_id": "government-minister"},
            {"person_id": "broadcast-journalist"},
        ],
        "organisations": [
            {"organisation_id": "national-government"},
            {"organisation_id": "public-broadcaster"},
            {"organisation_id": "coastal-workers-union"},
        ],
    }
    return FictionalTargetRegistry(enriched, SCENARIO_ID)


# ── 1-2: registered entities of the new kinds resolve ────────────────────────────────────────────


def test_01_registered_fictional_person_is_accepted(registry: FictionalTargetRegistry) -> None:
    ref = registry.resolve(f"fict:{SCENARIO_ID}:person:family-spokesperson")
    assert ref.kind == "person"
    assert ref.entity_id == "family-spokesperson"
    assert ref.scenario_id == SCENARIO_ID


def test_02_registered_fictional_organisation_is_accepted(registry: FictionalTargetRegistry) -> None:
    ref = registry.resolve(f"fict:{SCENARIO_ID}:organisation:coastal-workers-union")
    assert ref.kind == "organisation"
    assert ref.entity_id == "coastal-workers-union"


# ── 3-4: unregistered entities of the new kinds fail closed ──────────────────────────────────────


@pytest.mark.parametrize(
    "unregistered",
    ["someone-else", "prime-minister", "family-spokesperson-2", "Family-Spokesperson"],
)
def test_03_unregistered_fictional_person_is_rejected(
    registry: FictionalTargetRegistry, unregistered: str
) -> None:
    """A kind existing does not make an entity reachable. The registry is the authority."""
    with pytest.raises(B5Violation) as exc:
        registry.resolve(f"fict:{SCENARIO_ID}:person:{unregistered}")
    assert exc.value.control == "B5-03"


@pytest.mark.parametrize("unregistered", ["some-ministry", "acme-corp", "national-government-2"])
def test_04_unregistered_fictional_organisation_is_rejected(
    registry: FictionalTargetRegistry, unregistered: str
) -> None:
    with pytest.raises(B5Violation) as exc:
        registry.resolve(f"fict:{SCENARIO_ID}:organisation:{unregistered}")
    assert exc.value.control == "B5-03"


# ── 5-6: cross-world references of the new kinds fail closed ─────────────────────────────────────


def test_05_person_from_another_fictional_world_is_rejected(registry: FictionalTargetRegistry) -> None:
    """The entity id is valid HERE; the world segment is what refuses it."""
    with pytest.raises(B5Violation) as exc:
        registry.resolve(f"fict:{OTHER_WORLD}:person:family-spokesperson")
    assert exc.value.control == "B5-03"
    assert "Cross-world" in str(exc.value) or "active world" in str(exc.value)


def test_06_organisation_from_another_fictional_world_is_rejected(
    registry: FictionalTargetRegistry,
) -> None:
    with pytest.raises(B5Violation) as exc:
        registry.resolve(f"fict:{OTHER_WORLD}:organisation:coastal-workers-union")
    assert exc.value.control == "B5-03"


# ── 7-8: identifying fields cannot be attached to a target ───────────────────────────────────────


@pytest.mark.parametrize(
    "extra",
    ["name", "description", "external_id", "real_name", "social_handle", "email", "url"],
)
@pytest.mark.parametrize("kind", ["person", "organisation"])
def test_07_08_target_rejects_identifying_extra_fields(kind: str, extra: str) -> None:
    """
    B5-06 structurally. A target that could carry a name could carry a REAL name; the model forbids
    extras so the field does not exist to be filled.
    """
    with pytest.raises(Exception) as exc:
        MessageTarget(
            scenario_id=SCENARIO_ID, kind=kind, entity_id="family-spokesperson", **{extra: "x"}
        )
    assert "extra" in str(exc.value).lower() or "forbidden" in str(exc.value).lower()


# ── 9-11: free text, unknown kinds, malformed identifiers ────────────────────────────────────────


@pytest.mark.parametrize(
    "free_text",
    ["the family spokesperson", "National Government", "coastal workers", "a journalist", ""],
)
def test_09_free_text_target_is_rejected(
    registry: FictionalTargetRegistry, free_text: str
) -> None:
    with pytest.raises(B5Violation):
        registry.resolve(free_text)


@pytest.mark.parametrize(
    "unknown_kind", ["institution", "company", "state", "population", "individual", "user"]
)
def test_10_unknown_target_kind_is_rejected(
    registry: FictionalTargetRegistry, unknown_kind: str
) -> None:
    """
    'institution' is included on purpose: it was REMOVED from the vocabulary because no scenario
    declared one, so it must now fail like any other unknown kind.
    """
    assert unknown_kind not in TARGET_KINDS
    with pytest.raises(B5Violation) as exc:
        registry.resolve(f"fict:{SCENARIO_ID}:{unknown_kind}:family-spokesperson")
    assert exc.value.control == "B5-03"


@pytest.mark.parametrize(
    "malformed",
    [
        "kestral-strait:person:family-spokesperson",
        "real:kestral-strait:person:family-spokesperson",
        "fict:kestral-strait:person",
        "fict:kestral-strait:person:a:b",
        "FICT:kestral-strait:person:family-spokesperson",
        "://person/family-spokesperson",
        None,
        42,
    ],
)
def test_11_malformed_or_unprefixed_identifier_is_rejected(
    registry: FictionalTargetRegistry, malformed: object
) -> None:
    with pytest.raises(B5Violation):
        registry.resolve(malformed)


# ── 12: canonical resolution cannot be bypassed by case, whitespace or Unicode ───────────────────


@pytest.mark.parametrize(
    "variant",
    [
        "fict:kestral-strait:person:FAMILY-SPOKESPERSON",
        "fict:kestral-strait:person:Family-Spokesperson",
        "fict:kestral-strait:person: family-spokesperson",
        "fict:kestral-strait:person:family-spokesperson ",
        "fict:kestral-strait:PERSON:family-spokesperson",
        "fict:KESTRAL-STRAIT:person:family-spokesperson",
        "fict:kestral-strait:person:family‐spokesperson",  # U+2010 hyphen, not ASCII '-'
        "fict:kestral-strait:person:famіly-spokesperson",  # Cyrillic 'і' homoglyph
        "fict:kestral-strait:person:family-spokesperson​",  # zero-width space
    ],
)
def test_12_case_whitespace_unicode_cannot_bypass_resolution(
    registry: FictionalTargetRegistry, variant: str
) -> None:
    """
    Exact match only.

    Deliberately NOT normalised: fuzzy matching is how a near-miss identifier quietly resolves to
    something it was not. Homoglyph and zero-width variants must fail, not be helpfully corrected.
    """
    with pytest.raises(B5Violation):
        registry.resolve(variant)


# ── 13: no collisions across kinds ───────────────────────────────────────────────────────────────


def test_13_registry_entries_do_not_collide_across_kinds(scenario: dict) -> None:
    """
    A shared id must not make an entity reachable under the wrong kind.

    If `port-workers` exists as both a cohort and an organisation, resolving it as an organisation
    must not silently return the cohort — kind is part of identity, not a hint.
    """
    colliding = {
        **scenario,
        "people": [{"person_id": "shared-id"}],
        "organisations": [{"organisation_id": "shared-id"}],
    }
    reg = FictionalTargetRegistry(colliding, SCENARIO_ID)

    as_person = reg.resolve(f"fict:{SCENARIO_ID}:person:shared-id")
    as_org = reg.resolve(f"fict:{SCENARIO_ID}:organisation:shared-id")
    assert as_person.kind == "person" and as_org.kind == "organisation"
    assert as_person != as_org

    # A cohort id must not be reachable as a person.
    cohort_id = sorted(reg.known("cohort"))[0]
    with pytest.raises(B5Violation):
        reg.resolve(f"fict:{SCENARIO_ID}:person:{cohort_id}")

    # Namespaces are disjoint.
    assert not (reg.known("person") & reg.known("cohort"))


# ── 14: audience ranking is inexpressible ────────────────────────────────────────────────────────


def test_14_no_audience_ranking_concept_exists() -> None:
    """
    B5-05, proven by ABSENCE rather than by refusal.

    "Most persuadable person", "easiest organisation to influence", "highest-conversion cohort" and
    "optimal audience" cannot be requested because no field, model or function supports the notion.
    A keyword filter would only refuse the phrasing; this asserts the capability is not there.
    """
    import app.simulation.belief.schemas as bs
    from app.safety import targets as tg

    banned = (
        "susceptib",
        "persuad",
        "influenceab",
        "conversion",
        "optimal_audience",
        "rank_audience",
        "most_",
        "easiest",
        "highest_conversion",
        "gullib",
        "manipulab",
    )

    for module in (bs, tg):
        for attr in dir(module):
            assert not any(b in attr.lower() for b in banned), f"{module.__name__}.{attr}"

    # No model in the belief schema carries a rankable score field.
    for name in dir(bs):
        obj = getattr(bs, name)
        fields = getattr(obj, "model_fields", None)
        if not fields:
            continue
        for field_name in fields:
            assert not any(b in field_name.lower() for b in banned), f"{name}.{field_name}"

    # And the registry offers retrieval and membership only — no ordering operation.
    assert not any(
        op in dir(tg.FictionalTargetRegistry) for op in ("rank", "sort_by", "top", "best", "score")
    )
