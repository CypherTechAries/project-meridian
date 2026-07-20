"""
B5 technical controls — the constants the enforcement code reads.

CANONICAL SOURCE: `docs/safety/B5-TECHNICAL-CONTROLS.md`. That document is the founder-approved
baseline; this module implements it and must not diverge from it. If a control here disagrees with
the document, this module is wrong.

Every value in this file is deliberately a CLOSED set. B5 is enforced by constraining what can be
expressed to the engine, not by inspecting content for suspicious names — an allowlist cannot be
talked around, and a heuristic can.
"""

from __future__ import annotations

from typing import Final

# ── B5-01 ────────────────────────────────────────────────────────────────────────────────────────
# The only accepted world mode. There is no default: a scenario that omits the field is invalid,
# not assumed safe.
WORLD_MODE_KEY: Final = "world_mode"
FICTIONAL_WORLD_MODE: Final = "fictional"

# ── B5-02 ────────────────────────────────────────────────────────────────────────────────────────
# Repository-bundled scenarios that public v0.1 may run. Membership is the whole check: an id that
# is not in this frozenset never reaches the filesystem, which also closes path traversal.
PACKAGED_SCENARIOS: Final[frozenset[str]] = frozenset({"kestral-strait"})

# ── B5-03 ────────────────────────────────────────────────────────────────────────────────────────
# Typed target identifiers: fict:<scenario_id>:<kind>:<entity_id>. The prefix and scenario segment
# make a cross-world or real-world reference structurally inexpressible rather than merely refused.
TARGET_PREFIX: Final = "fict"

# Entity kinds a target may name. CLOSED SET, and each kind means one specific thing.
#
#   person        a fictional individual with STABLE IDENTITY WITHIN THE ACTIVE SCENARIO AND RUN,
#                 carrying beliefs, attitudes, bounded emotions, stance and behaviour propensities.
#                 Persistence across saved sessions or runs is NOT implemented and is not claimed.
#   organisation  a fictional formal collective actor with membership, official position, internal
#                 position distribution, objectives, cohesion and posture. NO emotion vector.
#   cohort        an aggregate fictional population group used for population-weighted modelling.
#                 Not a person and not a list of persons.
#   agent         LEGACY P0.5 scenario-actor type, resolving only to the existing
#                 `institutional_agents` registry. NOT a generic target kind and NOT used for
#                 belief-slice entities.
#
# The six legacy agent records are role-scoped - identified by office, not by person, and none
# carries a personal name. Four are singular offices; two (intelligence_lead, strategic_comms)
# denote a lead function that may be a post or a team. They are heterogeneous and are deliberately
# NOT folded into `person` or `organisation`.
#
# CHANGED 20 July 2026 for the Belief Formation and Divergence Slice:
#   + person, + organisation  - that milestone models named fictional people and organisations,
#                               which the previous vocabulary could not express at all.
#   - institution             - REMOVED. No scenario declared an `institutions` collection, so the
#                               kind resolved to nothing and could never appear in a valid target.
#                               A kind that cannot resolve is surface area with no purpose.
#
# Net effect is a widening of two and a tightening of one. It does not weaken fictional-only
# resolution: a target must still carry the 'fict:' prefix, name the ACTIVE world, and RESOLVE in
# that world's registry, which is built solely from scenario data. No real person or organisation
# becomes addressable, whatever its kind.
TARGET_KINDS: Final[frozenset[str]] = frozenset({"cohort", "agent", "person", "organisation"})

# ── B5-04 ────────────────────────────────────────────────────────────────────────────────────────
# Protected/sensitive traits and project-declared proxies. Rejected as targeting, ranking,
# optimisation, intervention-selection, susceptibility or segmentation inputs.
#
# NOTE THE BOUNDARY: identity may still affect lived experience, relationships, discrimination,
# institutional access, media exposure and cultural interpretation. This tuple governs what may be
# used to SELECT or RANK an audience, not what the world model may represent.
PROTECTED_TRAITS: Final[tuple[str, ...]] = (
    "race",
    "ethnicity",
    "ethnic_group",
    "national_origin",
    "religion",
    "faith",
    "sex",
    "gender",
    "gender_identity",
    "sexual_orientation",
    "disability",
    "health_status",
    "medical_condition",
    "pregnancy",
    "age_group",
    "caste",
    "immigration_status",
    "political_affiliation",
    "union_membership",
    "genetic_data",
    "biometric_data",
)

# Declared proxies. Listed separately so the reason for each is auditable rather than folded in.
PROTECTED_TRAIT_PROXIES: Final[tuple[str, ...]] = (
    "postcode",
    "zip_code",
    "neighbourhood",
    "neighborhood",
    "surname",
    "family_name",
    "language_spoken",
    "mother_tongue",
    "dialect",
    "school_attended",
    "place_of_worship",
    "diaspora",
)

# Identity may never encode these as inherent properties (B5-04, second clause).
PROHIBITED_IDENTITY_INFERENCES: Final[tuple[str, ...]] = (
    "competence",
    "morality",
    "loyalty",
    "violence",
    "truthfulness",
    "manipulability",
)

# ── B5-05 ────────────────────────────────────────────────────────────────────────────────────────
# Persuadability/susceptibility optimisation vocabulary. Rejected as request fields and forbidden as
# response fields. Applies to fictional and real audiences alike for public v0.1.
PERSUASION_OPTIMISATION_TERMS: Final[tuple[str, ...]] = (
    "susceptibility",
    "susceptible",
    "persuadability",
    "persuadable",
    "influenceability",
    "influenceable",
    "most_influenceable",
    "gullibility",
    "vulnerability_score",
    "manipulability",
    "optimal_audience",
    "optimal_target",
    "best_target",
    "target_ranking",
    "audience_ranking",
    "audience_optimisation",
    "audience_optimization",
    "message_optimisation",
    "message_optimization",
    "maximise_belief_change",
    "maximize_belief_change",
    "conversion_likelihood",
)

# ── B5-06 ────────────────────────────────────────────────────────────────────────────────────────
# A request whose target scope is a real population is REJECTED, never rewritten into a fictional
# analogue: silent transformation would teach the caller the request was acceptable.
REAL_POPULATION_SCOPES: Final[tuple[str, ...]] = (
    "real",
    "real_world",
    "real-world",
    "realworld",
    "actual",
    "live_population",
    "production",
)

# ── B5-07 ────────────────────────────────────────────────────────────────────────────────────────
# Approved disclosure wording. Exact string; UI and API must not paraphrase it.
FICTION_DISCLOSURE: Final = "FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION"

# ── B5-08 ────────────────────────────────────────────────────────────────────────────────────────
# Closed origin vocabulary. UNKNOWN and UNAVAILABLE are absences, never zero.
ORIGIN_ENGINE: Final = "ENGINE"
ORIGIN_FIXTURE: Final = "FIXTURE"
ORIGIN_UNKNOWN: Final = "UNKNOWN"
ORIGIN_UNAVAILABLE: Final = "UNAVAILABLE"
ORIGIN_VOCABULARY: Final[frozenset[str]] = frozenset(
    {ORIGIN_ENGINE, ORIGIN_FIXTURE, ORIGIN_UNKNOWN, ORIGIN_UNAVAILABLE}
)
ABSENCE_ORIGINS: Final[frozenset[str]] = frozenset({ORIGIN_UNKNOWN, ORIGIN_UNAVAILABLE})


class B5Violation(ValueError):
    """
    Raised when a B5 control refuses an input.

    Carries the control id so a refusal can always be traced to the clause that caused it, rather
    than surfacing as an anonymous validation error.
    """

    def __init__(self, control: str, message: str) -> None:
        self.control = control
        super().__init__(f"{control}: {message}")
