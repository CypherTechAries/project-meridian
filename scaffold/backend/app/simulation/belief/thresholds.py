"""
Contextual thresholds.

STRUCTURAL CORRECTION. A threshold was previously a scalar on the person, which made it read as a
permanent disposition — "this person is more rigorous". It is not. A threshold belongs to a
**proposition and a process**: the evidence a particular claim requires under a particular
procedure, for a particular entity. The same person legitimately holds different thresholds for
different propositions.

FACTUAL AND EVALUATIVE ARE DIFFERENT KINDS, NOT DIFFERENT VALUES. A factual claim can be verified,
so it takes a `verification` threshold. An evaluative claim cannot be verified at all, so attaching
a verification threshold to one would quietly assert that "emergency powers are legitimate" has a
truth value. It takes a `deliberation` or `commitment` threshold instead — how much reasoning or
confidence is required before a stance becomes firm, which says nothing about correctness.

That separation is enforced at construction, not by convention.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ...safety.controls import B5Violation
from .schemas import PropositionKind


class ThresholdKind(str, Enum):
    """Closed set. An unknown kind fails at construction."""

    verification = "verification"
    deliberation = "deliberation"
    commitment = "commitment"


#: Which threshold kinds are admissible for which proposition kinds.
_ADMISSIBLE: dict[PropositionKind, frozenset[ThresholdKind]] = {
    PropositionKind.fact: frozenset({ThresholdKind.verification}),
    PropositionKind.attribution: frozenset({ThresholdKind.verification}),
    PropositionKind.disposition: frozenset({ThresholdKind.verification}),
    PropositionKind.evaluative: frozenset({ThresholdKind.deliberation, ThresholdKind.commitment}),
}


class ContextualThreshold(BaseModel):
    """
    One threshold, scoped to an entity, a proposition and the process that set it.

    Note what is NOT here: no occupation, education, wealth, class, seniority, intelligence or
    competence field. A threshold cannot be derived from any of them because none is available to
    derive it from. `setting_process` and `rationale` record *why* the value is what it is, in
    situational terms, so the justification is auditable rather than assumed.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    entity_id: str
    proposition_id: str
    proposition_kind: PropositionKind
    threshold_kind: ThresholdKind
    value: float = Field(..., ge=0.0, le=1.0)
    scenario_id: str
    scenario_version: str
    setting_process: str = Field(..., min_length=1)
    rationale: str = Field(..., min_length=1)
    origin: str = "FIXTURE"
    source_reference: str

    @model_validator(mode="after")
    def _kind_matches_proposition(self) -> "ContextualThreshold":
        """
        A verification threshold on an evaluative proposition is a construction error.

        This is the clause that keeps factual and evaluative semantics apart. If it were a warning
        rather than a failure, an evaluative claim could acquire verification semantics by accident
        and be treated as truth-apt downstream.
        """
        admissible = _ADMISSIBLE[self.proposition_kind]
        if self.threshold_kind not in admissible:
            raise ValueError(
                f"threshold kind '{self.threshold_kind.value}' is not admissible for a "
                f"{self.proposition_kind.value} proposition; expected one of "
                f"{sorted(k.value for k in admissible)}. A factual claim takes a verification "
                f"threshold; an evaluative claim cannot be verified and takes deliberation or "
                f"commitment."
            )
        return self


class ThresholdRegistry:
    """
    Resolution for (entity, proposition).

    Fails closed on an unknown proposition; returns None — never 0.0 — when a proposition is known
    but the entity has no declared threshold for it. Those are different situations and must not
    collapse: an unknown proposition is a lookup error, a missing threshold is an absence.
    """

    def __init__(self, records: list[ContextualThreshold], known_propositions: set[str]) -> None:
        self._known = set(known_propositions)
        self._by_key: dict[tuple[str, str], ContextualThreshold] = {}
        for r in records:
            if r.proposition_id not in self._known:
                raise B5Violation(
                    "B5-03",
                    f"threshold references unknown proposition '{r.proposition_id}'",
                )
            self._by_key[(r.entity_id, r.proposition_id)] = r

    def resolve(
        self, entity_id: str, proposition_id: str, *, expect: Optional[ThresholdKind] = None
    ) -> Optional[ContextualThreshold]:
        if proposition_id not in self._known:
            raise B5Violation(
                "B5-03",
                f"unknown proposition '{proposition_id}' — threshold resolution fails closed",
            )
        record = self._by_key.get((entity_id, proposition_id))
        if record is None:
            return None  # Unavailable. Never 0.0.
        if expect is not None and record.threshold_kind is not expect:
            raise ValueError(
                f"expected a '{expect.value}' threshold for {entity_id} / {proposition_id} but the "
                f"declared record is '{record.threshold_kind.value}'; kinds are not interchangeable"
            )
        return record

    def value_for(
        self, entity_id: str, proposition_id: str, *, expect: Optional[ThresholdKind] = None
    ) -> Optional[float]:
        record = self.resolve(entity_id, proposition_id, expect=expect)
        return None if record is None else record.value

    def all_for_entity(self, entity_id: str) -> list[ContextualThreshold]:
        return [r for (e, _), r in self._by_key.items() if e == entity_id]
