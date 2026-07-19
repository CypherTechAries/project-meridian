"""
B5-08 — per-element provenance and origin.

Two properties this module exists to guarantee, both of which are dishonesty failures rather than
formatting failures:

  1. Fixture content must never be presented as computed engine output.
  2. UNKNOWN and UNAVAILABLE must never render as zero. Zero is a number the engine produced;
     absence is not. Collapsing the two is the specific lie this control prevents.

`ProvenancedValue.render()` therefore returns `None` for an absent value rather than a number, so a
caller cannot accidentally format an absence as `0`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from .controls import (
    ABSENCE_ORIGINS,
    ORIGIN_ENGINE,
    ORIGIN_FIXTURE,
    ORIGIN_UNAVAILABLE,
    ORIGIN_UNKNOWN,
    ORIGIN_VOCABULARY,
    B5Violation,
)


def assert_origin(origin: Any) -> str:
    """The origin vocabulary is closed. Anything outside it fails closed."""
    if origin not in ORIGIN_VOCABULARY:
        raise B5Violation(
            "B5-08",
            f"origin '{origin}' is not in the approved vocabulary {sorted(ORIGIN_VOCABULARY)}",
        )
    return str(origin)


@dataclass(frozen=True)
class ProvenancedValue:
    """
    A user-visible value carrying its own provenance.

    `value` MUST be None whenever origin is an absence. That invariant is enforced in __post_init__
    rather than left to callers, because the failure it prevents is silent.
    """

    value: Optional[float]
    origin: str
    epistemic_status: str
    scenario_id: str
    scenario_version: str
    last_updated_tick: Optional[int] = None
    confidence: str = "NOT_APPLICABLE"

    def __post_init__(self) -> None:
        assert_origin(self.origin)
        if self.origin in ABSENCE_ORIGINS and self.value is not None:
            raise B5Violation(
                "B5-08",
                f"origin '{self.origin}' declares an absence but a value ({self.value!r}) was "
                f"supplied. An absent value must not carry a number - that is how absences become "
                f"zeros.",
            )
        if self.origin not in ABSENCE_ORIGINS and self.value is None:
            raise B5Violation(
                "B5-08",
                f"origin '{self.origin}' asserts a real value but none was supplied. Use "
                f"{ORIGIN_UNKNOWN} or {ORIGIN_UNAVAILABLE} instead of a null.",
            )

    @property
    def is_absent(self) -> bool:
        return self.origin in ABSENCE_ORIGINS

    def render(self) -> Optional[float]:
        """Return the number, or None for an absence. Never 0 as a stand-in for 'no value'."""
        return None if self.is_absent else self.value

    def as_dict(self) -> dict:
        return {
            "value": self.render(),
            "origin": self.origin,
            "epistemic_status": self.epistemic_status,
            "confidence": self.confidence,
            "scenario_id": self.scenario_id,
            "scenario_version": self.scenario_version,
            "last_updated_tick": self.last_updated_tick,
            "absent": self.is_absent,
        }


def engine_value(
    value: float,
    *,
    scenario_id: str,
    scenario_version: str,
    tick: Optional[int] = None,
    epistemic_status: str = "AUTHORITATIVE",
) -> ProvenancedValue:
    return ProvenancedValue(
        value=float(value),
        origin=ORIGIN_ENGINE,
        epistemic_status=epistemic_status,
        scenario_id=scenario_id,
        scenario_version=scenario_version,
        last_updated_tick=tick,
    )


def fixture_value(
    value: float,
    *,
    scenario_id: str,
    scenario_version: str,
    epistemic_status: str = "PRESENTATION_ONLY",
) -> ProvenancedValue:
    """Hand-authored content. Never labelled ENGINE — that is the B5-08 falsehood."""
    return ProvenancedValue(
        value=float(value),
        origin=ORIGIN_FIXTURE,
        epistemic_status=epistemic_status,
        scenario_id=scenario_id,
        scenario_version=scenario_version,
    )


def absent_value(
    origin: str,
    *,
    scenario_id: str,
    scenario_version: str,
    epistemic_status: str = "UNKNOWN",
) -> ProvenancedValue:
    if origin not in ABSENCE_ORIGINS:
        raise B5Violation("B5-08", f"'{origin}' is not an absence origin")
    return ProvenancedValue(
        value=None,
        origin=origin,
        epistemic_status=epistemic_status,
        scenario_id=scenario_id,
        scenario_version=scenario_version,
    )


def assert_projection_provenance(projection: dict) -> None:
    """
    B5-08 over a whole projection: every user-visible record must carry a valid origin, and no
    fixture record may claim ENGINE.
    """
    groups = ("stages", "cohorts", "government_options", "recent_transitions")
    for group in groups:
        for i, entry in enumerate(projection.get(group, []) or []):
            if "origin" not in entry:
                raise B5Violation(
                    "B5-08", f"{group}[{i}] has no origin; every visible record must carry one"
                )
            assert_origin(entry["origin"])
            if entry["origin"] in ABSENCE_ORIGINS and entry.get("value") not in (None,):
                raise B5Violation(
                    "B5-08",
                    f"{group}[{i}] declares origin '{entry['origin']}' but carries value "
                    f"{entry.get('value')!r}; absences must not render as numbers",
                )
