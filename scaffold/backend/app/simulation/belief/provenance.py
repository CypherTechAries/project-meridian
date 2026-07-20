"""
First-class typed provenance and calculation traces.

The point is not tidier typing. It is that every displayed value can answer, without re-running the
engine: what does this represent, where did it come from, which inputs affected it, which rule
produced it, what was unavailable, and over what denominator.

TWO RULES THAT SHAPE EVERYTHING HERE.

  1. ORIGIN DESCRIBES WHO PRODUCED THE VALUE, NOT WHO TOUCHED IT. A retained prior copied through
     by engine code is not ENGINE-derived — the number came from a fixture. `RetainedPrior` records
     the prior's own origin alongside the fact that the engine produced the no-update decision, so
     the two cannot be conflated.
  2. ABSENCE IS TEXTUAL. `UNKNOWN` and `UNAVAILABLE` are enum states, and an absent number
     serialises as `null`. Neither ever becomes `0`.

Every record is immutable and forbids unknown fields. No composite field exists that could be read
as "how influenceable this entity is".
"""

from __future__ import annotations

import json
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ...safety.controls import ORIGIN_VOCABULARY, TARGET_PREFIX, B5Violation
from .schemas import PropositionKind

_FROZEN = ConfigDict(extra="forbid", frozen=True)

#: Belief-slice outputs use these kinds only. The legacy `agent` kind is not permitted here.
BELIEF_ENTITY_KINDS = frozenset({"person", "organisation", "cohort"})


class Origin(str, Enum):
    engine = "ENGINE"
    fixture = "FIXTURE"
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"


class ResultStatus(str, Enum):
    updated = "UPDATED"
    no_update = "NO_UPDATE"
    unexposed = "UNEXPOSED"
    unavailable = "UNAVAILABLE"


class EntityRef(BaseModel):
    """A typed reference. Cross-world and wrong-kind references are refused at construction."""

    model_config = _FROZEN

    scenario_id: str
    entity_kind: str
    entity_id: str

    @model_validator(mode="after")
    def _valid(self) -> "EntityRef":
        if self.entity_kind not in BELIEF_ENTITY_KINDS:
            raise ValueError(
                f"'{self.entity_kind}' is not a belief-slice entity kind "
                f"{sorted(BELIEF_ENTITY_KINDS)}; the legacy 'agent' kind is not permitted here"
            )
        return self

    def typed_id(self) -> str:
        return f"{TARGET_PREFIX}:{self.scenario_id}:{self.entity_kind}:{self.entity_id}"


class Provenance(BaseModel):
    """Common to every belief-slice output."""

    model_config = _FROZEN

    scenario_id: str
    scenario_version: str
    entity: EntityRef
    proposition_id: str
    proposition_kind: PropositionKind
    tick: int = Field(..., ge=0)
    origin: Origin
    result_status: ResultStatus
    rule_id: str
    rule_version: str
    created_from: tuple[str, ...] = ()

    @model_validator(mode="after")
    def _world_and_origin(self) -> "Provenance":
        if self.entity.scenario_id != self.scenario_id:
            raise ValueError(
                f"cross-world reference: entity belongs to '{self.entity.scenario_id}' but the "
                f"provenance names '{self.scenario_id}'"
            )
        if self.origin.value not in ORIGIN_VOCABULARY:
            raise ValueError(f"origin '{self.origin}' is outside the approved vocabulary")
        return self


class RetainedPrior(BaseModel):
    """
    A prior carried forward unchanged.

    Kept as its own type because "the engine decided not to update this" and "this number is
    engine-derived" are different claims. `prior_origin` records where the number came from;
    `decision_origin` records that the engine made the no-update decision.
    """

    model_config = _FROZEN

    value: Optional[float]
    prior_origin: Origin
    decision_origin: Origin = Origin.engine
    reason: str


class PersonUpdateTrace(BaseModel):
    """Every declared input, every intermediate, and the bounded output."""

    model_config = _FROZEN

    provenance: Provenance

    prior_state_reference: str
    information_event_reference: Optional[str]
    exposure_reference: Optional[str]
    contextual_threshold_reference: Optional[str]
    source_trust_reference: Optional[str]

    prior_credence: Optional[float]
    prior_confidence: Optional[float]
    source_trust: Optional[float]
    contextual_threshold: Optional[float]
    evidence_strength: Optional[float]
    exposure_intensity: Optional[float]
    relay_factor: Optional[float]
    relevance: Optional[float]
    evidence_status: str

    update_weight: Optional[float]
    target_value: Optional[float]
    raw_credence_delta: Optional[float]
    raw_confidence_delta: Optional[float]
    clamped: bool

    final_credence: Optional[float]
    final_confidence: Optional[float]
    result_classification: Optional[str]
    uncertainty_status: Optional[str]
    no_update_reason: Optional[str] = None

    @model_validator(mode="after")
    def _person_only_and_no_update_explained(self) -> "PersonUpdateTrace":
        if self.provenance.entity.entity_kind != "person":
            raise ValueError(
                f"a person trace cannot describe a {self.provenance.entity.entity_kind}"
            )
        if self.provenance.result_status in (ResultStatus.no_update, ResultStatus.unexposed):
            if not self.no_update_reason:
                raise ValueError("a no-update result must state why no update occurred")
        return self


class OrganisationTrace(BaseModel):
    model_config = _FROZEN

    provenance: Provenance
    exposure_references: tuple[str, ...] = ()

    prior_official_alignment: Optional[float]
    update_weight: Optional[float]
    target_alignment: Optional[float]
    cohesion: Optional[float]
    cohesion_contribution: Optional[float]
    raw_alignment_delta: Optional[float]
    resulting_alignment: Optional[float]

    internal_distribution: Optional[dict[str, float]]
    uncertain_bloc_share: Optional[float]
    decisive_margin: Optional[float]

    governance_rule: str
    official_position: Optional[str]
    official_position_derivation: str
    official_position_equals_weighted_mean: bool = False

    action_direction: Optional[str]
    action_intensity: Optional[float]
    action_intensity_derivation: str

    objectives: tuple[str, ...] = ()
    unavailable_reason: Optional[str] = None

    @model_validator(mode="after")
    def _organisation_only(self) -> "OrganisationTrace":
        if self.provenance.entity.entity_kind != "organisation":
            raise ValueError(
                f"an organisation trace cannot describe a {self.provenance.entity.entity_kind}"
            )
        return self


class CohortTrace(BaseModel):
    model_config = _FROZEN

    provenance: Provenance

    population_weight: int
    total_denominator: int
    exposed_denominator: int
    unexposed_denominator: int
    exposure_missing_denominator: int
    belief_known_denominator: int

    exposure_status: str
    retained_prior: Optional[RetainedPrior]
    event_driven_delta: Optional[float]

    aggregate_value: Optional[float]
    #: Names the denominator in prose so an exposed-only figure cannot be read as society-wide.
    aggregate_basis: str

    distribution_status: str
    distribution_unavailable_reason: Optional[str]
    state_mass_references: tuple[str, ...] = ()
    reconciliation_tolerance: float

    @model_validator(mode="after")
    def _cohort_only_and_denominators_reconcile(self) -> "CohortTrace":
        if self.provenance.entity.entity_kind != "cohort":
            raise ValueError(f"a cohort trace cannot describe a {self.provenance.entity.entity_kind}")
        parts = (
            self.exposed_denominator
            + self.unexposed_denominator
            + self.exposure_missing_denominator
        )
        if parts != self.total_denominator:
            raise ValueError(
                f"exposure denominators {parts} do not reconcile with total "
                f"{self.total_denominator}"
            )
        if self.distribution_status == "unavailable" and not self.distribution_unavailable_reason:
            raise ValueError("an unavailable distribution must state why")
        if self.state_mass_references and self.distribution_status == "unavailable":
            raise ValueError("state mass references imply an available distribution")
        return self


def canonical_json(record: BaseModel) -> str:
    """
    Deterministic serialisation.

    Keys sorted, so identical inputs always produce byte-identical output. Absent numbers become
    `null` — never `0` — and status values stay textual.
    """
    return json.dumps(record.model_dump(mode="json"), sort_keys=True, separators=(",", ":"))


def assert_no_zero_for_absence(record: BaseModel) -> None:
    """
    Guard the specific failure B5-08 exists to prevent.

    Anything the record reports as UNKNOWN or UNAVAILABLE must not be carrying a numeric value.
    """
    data = record.model_dump(mode="json")

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            # Any key ENDING in origin/status, not just the exact names. RetainedPrior uses
            # `prior_origin`, and a guard that missed it would have been silently narrow.
            status = "".join(
                str(v) for k, v in node.items()
                if isinstance(v, str) and (k.endswith("origin") or k.endswith("status"))
            )
            if "UNAVAILABLE" in status or "UNKNOWN" in status:
                for key, value in node.items():
                    if isinstance(value, (int, float)) and not isinstance(value, bool):
                        if key not in ("tick",) and value == 0:
                            raise B5Violation(
                                "B5-08",
                                f"{path}.{key} is 0 on a record whose status is an absence; "
                                f"absence must serialise as null",
                            )
            for key, value in node.items():
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                walk(item, f"{path}[{idx}]")

    walk(data, "record")
