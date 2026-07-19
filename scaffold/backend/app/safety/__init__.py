"""
B5 technical controls.

Canonical baseline: `docs/safety/B5-TECHNICAL-CONTROLS.md`. This package implements it. Where the
two disagree, the document governs and this package is wrong.

  B5-01 fail-closed fictional manifest        -> scenarios.assert_fictional_manifest
  B5-02 packaged scenarios only               -> scenarios.assert_packaged_scenario / load_packaged_scenario
  B5-03 fictional target registry             -> targets.FictionalTargetRegistry
  B5-04 protected-trait exclusion             -> targets.assert_no_protected_traits
  B5-05 no persuadability optimisation        -> targets.assert_no_persuasion_optimisation
  B5-06 no real-population recommendations    -> targets.assert_not_real_population
  B5-07 persistent fictional disclosure       -> controls.FICTION_DISCLOSURE, scenarios.fictional_world_metadata
  B5-08 per-element provenance and origin     -> provenance.*
"""

from .controls import (
    FICTION_DISCLOSURE,
    ORIGIN_ENGINE,
    ORIGIN_FIXTURE,
    ORIGIN_UNAVAILABLE,
    ORIGIN_UNKNOWN,
    ORIGIN_VOCABULARY,
    PACKAGED_SCENARIOS,
    B5Violation,
)
from .provenance import (
    ProvenancedValue,
    absent_value,
    assert_origin,
    assert_projection_provenance,
    engine_value,
    fixture_value,
)
from .scenarios import (
    assert_fictional_manifest,
    assert_packaged_scenario,
    fictional_world_metadata,
    load_packaged_scenario,
)
from .targets import (
    FictionalTargetRegistry,
    TargetRef,
    assert_no_persuasion_optimisation,
    assert_no_protected_traits,
    assert_not_real_population,
    assert_request_permitted,
)

__all__ = [
    "B5Violation",
    "FICTION_DISCLOSURE",
    "FictionalTargetRegistry",
    "ORIGIN_ENGINE",
    "ORIGIN_FIXTURE",
    "ORIGIN_UNAVAILABLE",
    "ORIGIN_UNKNOWN",
    "ORIGIN_VOCABULARY",
    "PACKAGED_SCENARIOS",
    "ProvenancedValue",
    "TargetRef",
    "absent_value",
    "assert_fictional_manifest",
    "assert_no_persuasion_optimisation",
    "assert_no_protected_traits",
    "assert_not_real_population",
    "assert_origin",
    "assert_packaged_scenario",
    "assert_projection_provenance",
    "assert_request_permitted",
    "engine_value",
    "fictional_world_metadata",
    "fixture_value",
    "load_packaged_scenario",
]
