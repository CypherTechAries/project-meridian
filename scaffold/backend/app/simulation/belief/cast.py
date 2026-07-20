"""
The fictional cast, propositions, source trust, priors and exposure records.

FROZEN BEFORE OUTCOME INSPECTION. Every value here was chosen from the entity's declared situation
— what it can access, who it trusts, what it already believed, how relevant the claim is to it —
and NOT by running the model and adjusting until three desired labels appeared. The commit that
introduced this file precedes any outcome assertion, deliberately, so that ordering is checkable in
history rather than merely asserted.

SEPARATION OF CONCERNS. `bio` fields are descriptive fixture content for the interface. They are
never read by the update rule; `test_belief_genericity` asserts that the update input contains no
biography field at all.

ROLE IS NOT CAPABILITY. Thresholds live in `THRESHOLDS` as contextual records keyed by
(entity, proposition), each carrying the process that set it — never on the person as a scalar,
which would read as a permanent disposition. A prestigious role grants access, authority and
constraints; it does not grant competence or rationality.

B5: every identifier is a `fict:` typed target that must resolve in the active world's registry.
There is no susceptibility, persuadability or ranking value anywhere in this module.
"""

from __future__ import annotations

from typing import Any

SCENARIO_ID = "kestral-strait"
SCENARIO_VERSION = "1.0.0"
RULE_VERSION = "belief-update-v1"


# ── Propositions ─────────────────────────────────────────────────────────────────────────────────

PROPOSITIONS: list[dict[str, Any]] = [
    {
        "proposition_id": "P-WARNINGS-IGNORED",
        "kind": "attribution",
        "topic": "government-conduct",
        "truth_value": "indeterminate",
        "claim_text": (
            "The government ignored advance warnings about the closure of the Kestral Strait."
        ),
        "scenario_authored": True,
    },
    {
        "proposition_id": "P-EMERGENCY-LEGITIMATE",
        "kind": "evaluative",
        "topic": "government-conduct",
        # Evaluative claims are structurally not truth-apt. No holder is ever recorded as factually
        # wrong for holding one.
        "truth_value": "not_truth_apt",
        "claim_text": "Emergency powers would be a legitimate response to the closure.",
        "scenario_authored": True,
    },
]


# ── People ───────────────────────────────────────────────────────────────────────────────────────
#
# Three declared SITUATIONS, not three scripted outcomes. What differs is only evidentiary
# threshold, source trust, relevance and prior state — each justified by access, obligation or
# procedure, never by occupation, credentials or presumed capability.

PEOPLE: list[dict[str, Any]] = [
    {
        "person_id": "family-spokesperson",
        "display_name": "Spokesperson, Strait Families Group",
        "bio": "Speaks for families of crew held by the closure.",
    },
    {
        "person_id": "government-minister",
        "display_name": "Minister for Maritime Affairs",
        "bio": "Holds the maritime brief in the governing coalition.",
    },
    {
        "person_id": "broadcast-journalist",
        "display_name": "Correspondent, Northshore Broadcast",
        "bio": "Covers the strait for the public broadcaster.",
    },
]

ORGANISATIONS: list[dict[str, Any]] = [
    {
        "organisation_id": "national-government",
        "display_name": "National Government",
        "cohesion": 0.72,
        "official_alignment": 0.15,
        "internal_blocs": {"support": 0.15, "oppose": 0.55, "uncertain": 0.30},
        "objectives": ["maintain continuity of government", "restore strait access"],
        "bio": "The governing coalition.",
    },
    {
        "organisation_id": "public-broadcaster",
        "display_name": "Northshore Public Broadcast",
        "cohesion": 0.55,
        "official_alignment": 0.40,
        "internal_blocs": {"support": 0.30, "oppose": 0.20, "uncertain": 0.50},
        "objectives": ["report verified information", "maintain editorial independence"],
        "bio": "The public service broadcaster.",
    },
    {
        "organisation_id": "coastal-workers-union",
        "display_name": "Coastal Workers' Union",
        "cohesion": 0.81,
        "official_alignment": 0.62,
        "internal_blocs": {"support": 0.70, "oppose": 0.10, "uncertain": 0.20},
        "objectives": ["protect member employment", "secure hardship support"],
        "bio": "Represents port and coastal workers.",
    },
]

# Cohort ids match the shipped P0.5 scenario where they already exist, so population weighting comes
# from scenario data rather than being re-declared here.
COHORTS: list[dict[str, Any]] = [
    {"cohort_id": "port-workers", "display_name": "Port workers", "represents_population": 41_000},
    {"cohort_id": "coastal-households", "display_name": "Coastal households", "represents_population": 96_000},
    {"cohort_id": "governing-party-supporters", "display_name": "Governing-party supporters", "represents_population": 210_000},
    {"cohort_id": "opposition-supporters", "display_name": "Opposition supporters", "represents_population": 188_000},
    {"cohort_id": "inland-households", "display_name": "Inland households", "represents_population": 402_000},
    {"cohort_id": "small-business-owners", "display_name": "Small-business owners", "represents_population": 64_000},
]


# ── Contextual thresholds ────────────────────────────────────────────────────────────────────────
#
# Keyed by (entity, proposition). The three factual values are EXACTLY those previously held as
# person scalars - 0.20 / 0.75 / 0.55 - so the frozen first run is preserved. Only their scoping,
# kind and provenance changed. This is a semantic correction, not tuning.
#
# The evaluative proposition carries DELIBERATION thresholds, a different kind: an evaluative claim
# cannot be verified, so it has no verification threshold at all.

THRESHOLD_RECORDS: list[dict[str, Any]] = [
    {
        "entity_id": "family-spokesperson",
        "proposition_id": "P-WARNINGS-IGNORED",
        "proposition_kind": "attribution",
        "threshold_kind": "verification",
        "value": 0.20,
        "setting_process": "first-hand testimony already held",
        "rationale": (
            "The person already holds the first-hand testimony on which the factual claim is "
            "based, reducing the additional corroboration required for this proposition."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
    {
        "entity_id": "government-minister",
        "proposition_id": "P-WARNINGS-IGNORED",
        "proposition_kind": "attribution",
        "threshold_kind": "verification",
        "value": 0.75,
        "setting_process": "departmental verification requirement",
        "rationale": (
            "The relevant governmental process requires formal verification against institutional "
            "records before changing the official factual position."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
    {
        "entity_id": "broadcast-journalist",
        "proposition_id": "P-WARNINGS-IGNORED",
        "proposition_kind": "attribution",
        "threshold_kind": "verification",
        "value": 0.55,
        "setting_process": "broadcaster publication standard",
        "rationale": (
            "The broadcaster's publication process requires corroboration before reporting this "
            "factual allegation as established."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
    # Evaluative proposition: DELIBERATION, not verification. Declared for schema completeness; the
    # evaluative update path is not exercised by the frozen factual run.
    {
        "entity_id": "family-spokesperson",
        "proposition_id": "P-EMERGENCY-LEGITIMATE",
        "proposition_kind": "evaluative",
        "threshold_kind": "deliberation",
        "value": 0.35,
        "setting_process": "campaign group internal consultation",
        "rationale": (
            "The group consults affected families before adopting a firm public position on a "
            "measure that would affect them."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
    {
        "entity_id": "government-minister",
        "proposition_id": "P-EMERGENCY-LEGITIMATE",
        "proposition_kind": "evaluative",
        "threshold_kind": "commitment",
        "value": 0.70,
        "setting_process": "collective responsibility",
        "rationale": (
            "A firm public stance commits the whole coalition, so the position is not advanced "
            "until it is agreed collectively."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
    {
        "entity_id": "broadcast-journalist",
        "proposition_id": "P-EMERGENCY-LEGITIMATE",
        "proposition_kind": "evaluative",
        "threshold_kind": "deliberation",
        "value": 0.60,
        "setting_process": "editorial impartiality standard",
        "rationale": (
            "The broadcaster's impartiality standard restricts correspondents from advancing a "
            "firm position on a contested policy question."
        ),
        "source_reference": "cast.THRESHOLD_RECORDS",
    },
]


def threshold_registry():
    """Build the typed registry from the declared records."""
    from .thresholds import ContextualThreshold, ThresholdRegistry

    records = [
        ContextualThreshold(
            **r, scenario_id=SCENARIO_ID, scenario_version=SCENARIO_VERSION, origin="FIXTURE"
        )
        for r in THRESHOLD_RECORDS
    ]
    return ThresholdRegistry(records, {p["proposition_id"] for p in PROPOSITIONS})


# ── Source trust ─────────────────────────────────────────────────────────────────────────────────
#
# Trust is per SOURCE CATEGORY, not a global "trustfulness" score, and not per individual — an
# entity may trust the broadcaster and distrust the government simultaneously.

SOURCE_CATEGORIES = ("family-group", "government", "broadcaster", "union")

SOURCE_TRUST: dict[str, dict[str, float]] = {
    "family-spokesperson": {"family-group": 0.90, "government": 0.20, "broadcaster": 0.60, "union": 0.75},
    "government-minister": {"family-group": 0.30, "government": 0.90, "broadcaster": 0.50, "union": 0.35},
    "broadcast-journalist": {"family-group": 0.55, "government": 0.55, "broadcaster": 0.80, "union": 0.55},
    "national-government": {"family-group": 0.25, "government": 0.85, "broadcaster": 0.45, "union": 0.35},
    "public-broadcaster": {"family-group": 0.55, "government": 0.55, "broadcaster": 0.85, "union": 0.55},
    "coastal-workers-union": {"family-group": 0.80, "government": 0.30, "broadcaster": 0.55, "union": 0.90},
    "port-workers": {"family-group": 0.75, "government": 0.35, "broadcaster": 0.55, "union": 0.85},
    "coastal-households": {"family-group": 0.70, "government": 0.40, "broadcaster": 0.60, "union": 0.65},
    "governing-party-supporters": {"family-group": 0.35, "government": 0.80, "broadcaster": 0.50, "union": 0.35},
    "opposition-supporters": {"family-group": 0.65, "government": 0.25, "broadcaster": 0.60, "union": 0.60},
    "inland-households": {"family-group": 0.50, "government": 0.50, "broadcaster": 0.55, "union": 0.45},
    "small-business-owners": {"family-group": 0.55, "government": 0.45, "broadcaster": 0.55, "union": 0.50},
}


# ── Priors ───────────────────────────────────────────────────────────────────────────────────────
#
# (entity_id, proposition_id) -> prior state. Declared from the entity's situation.

PRIORS: dict[tuple[str, str], dict[str, float]] = {
    ("family-spokesperson", "P-WARNINGS-IGNORED"): {"credence": 0.55, "confidence": 0.40, "salience": 0.90},
    ("government-minister", "P-WARNINGS-IGNORED"): {"credence": 0.15, "confidence": 0.70, "salience": 0.80},
    ("broadcast-journalist", "P-WARNINGS-IGNORED"): {"credence": 0.35, "confidence": 0.25, "salience": 0.70},
    ("national-government", "P-WARNINGS-IGNORED"): {"credence": 0.15, "confidence": 0.65, "salience": 0.75},
    ("public-broadcaster", "P-WARNINGS-IGNORED"): {"credence": 0.40, "confidence": 0.30, "salience": 0.65},
    ("coastal-workers-union", "P-WARNINGS-IGNORED"): {"credence": 0.60, "confidence": 0.45, "salience": 0.85},
    ("port-workers", "P-WARNINGS-IGNORED"): {"credence": 0.50, "confidence": 0.35, "salience": 0.80},
    ("coastal-households", "P-WARNINGS-IGNORED"): {"credence": 0.45, "confidence": 0.30, "salience": 0.70},
    ("governing-party-supporters", "P-WARNINGS-IGNORED"): {"credence": 0.25, "confidence": 0.45, "salience": 0.40},
    ("opposition-supporters", "P-WARNINGS-IGNORED"): {"credence": 0.55, "confidence": 0.40, "salience": 0.55},
    ("inland-households", "P-WARNINGS-IGNORED"): {"credence": 0.35, "confidence": 0.20, "salience": 0.25},
    ("small-business-owners", "P-WARNINGS-IGNORED"): {"credence": 0.40, "confidence": 0.25, "salience": 0.45},
    # Evaluative proposition: stance, never credence.
    ("family-spokesperson", "P-EMERGENCY-LEGITIMATE"): {"stance_intensity": 0.30, "confidence": 0.35, "salience": 0.60},
    ("government-minister", "P-EMERGENCY-LEGITIMATE"): {"stance_intensity": 0.70, "confidence": 0.65, "salience": 0.85},
    ("broadcast-journalist", "P-EMERGENCY-LEGITIMATE"): {"stance_intensity": 0.40, "confidence": 0.30, "salience": 0.55},
}


# ── Relevance ────────────────────────────────────────────────────────────────────────────────────
#
# How much the claim's topic bears on the entity's own situation. Not a susceptibility score:
# relevance says the subject matters to them, not that they are easy to move.

RELEVANCE: dict[str, float] = {
    "family-spokesperson": 0.95,
    "government-minister": 0.90,
    "broadcast-journalist": 0.85,
    "national-government": 0.90,
    "public-broadcaster": 0.80,
    "coastal-workers-union": 0.88,
    "port-workers": 0.90,
    "coastal-households": 0.75,
    "governing-party-supporters": 0.45,
    "opposition-supporters": 0.60,
    "inland-households": 0.25,
    "small-business-owners": 0.55,
}


# ── The single shared information event ──────────────────────────────────────────────────────────
#
# ONE event. Same source, same wording, same claimed evidence, same timestamp, same id, for every
# recipient. Divergence may come only from declared prior, trust, exposure and threshold.

SHARED_EVENT: dict[str, Any] = {
    "event_id": "E-ALLEGATION-01",
    "proposition_id": "P-WARNINGS-IGNORED",
    "source_entity": f"fict:{SCENARIO_ID}:person:family-spokesperson",
    "source_category": "family-group",
    "channels": ["broadcast", "workplace", "community", "official_briefing", "union_network"],
    # Deliberately mid-strength: an allegation with partial supporting material. Strong enough to
    # move a receptive prior, not strong enough to resolve a professional's uncertainty.
    "evidence_strength": 0.45,
    "claim_direction": 1,
    "introduced_at_tick": 6,
}


# ── Exposure ─────────────────────────────────────────────────────────────────────────────────────
#
# Who encounters the event, through which channel, how directly. Exposure intensity describes
# CONTACT WITH THE INFORMATION, not how easily an entity can be influenced.
#
# `inland-households` is deliberately UNEXPOSED — an unexposed population is a first-class result
# and must not be reported as zero belief.

EXPOSURES: list[dict[str, Any]] = [
    {"entity_id": "family-spokesperson", "channel": "community", "intensity": 1.00, "relay": 1.00, "path": "originator"},
    {"entity_id": "government-minister", "channel": "official_briefing", "intensity": 0.85, "relay": 1.00, "path": "departmental briefing"},
    {"entity_id": "broadcast-journalist", "channel": "broadcast", "intensity": 0.95, "relay": 1.00, "path": "newsroom wire"},
    {"entity_id": "national-government", "channel": "official_briefing", "intensity": 0.80, "relay": 1.00, "path": "departmental briefing"},
    {"entity_id": "public-broadcaster", "channel": "broadcast", "intensity": 0.90, "relay": 1.00, "path": "newsroom wire"},
    {"entity_id": "coastal-workers-union", "channel": "union_network", "intensity": 0.85, "relay": 1.00, "path": "branch network"},
    {"entity_id": "port-workers", "channel": "workplace", "intensity": 0.80, "relay": 0.85, "path": "union relay"},
    {"entity_id": "coastal-households", "channel": "community", "intensity": 0.70, "relay": 0.85, "path": "community relay"},
    {"entity_id": "governing-party-supporters", "channel": "broadcast", "intensity": 0.55, "relay": 0.70, "path": "broadcast relay"},
    {"entity_id": "opposition-supporters", "channel": "broadcast", "intensity": 0.65, "relay": 0.70, "path": "broadcast relay"},
    {"entity_id": "small-business-owners", "channel": "community", "intensity": 0.45, "relay": 0.70, "path": "community relay"},
    # inland-households: no record. Unexposed, not zero.
]

UNEXPOSED = ("inland-households",)


def entity_kind(entity_id: str) -> str:
    if any(p["person_id"] == entity_id for p in PEOPLE):
        return "person"
    if any(o["organisation_id"] == entity_id for o in ORGANISATIONS):
        return "organisation"
    if any(c["cohort_id"] == entity_id for c in COHORTS):
        return "cohort"
    raise KeyError(f"'{entity_id}' is not in the belief-slice cast")


def target_id(entity_id: str) -> str:
    """Typed fictional identifier for an entity in the active world."""
    return f"fict:{SCENARIO_ID}:{entity_kind(entity_id)}:{entity_id}"
