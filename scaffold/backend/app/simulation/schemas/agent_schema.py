"""Pydantic v2 schemas for meso/micro agents and the supporting object graph.

Mirrors `design_simulation_schemas.md`. These models are the source of truth; the JSON
Schema files in `/schemas` and the SQLAlchemy models in `app/db/models.py` are derived
from them and must be kept in sync.

Determinism note: none of these objects are ever mutated by the LLM. The LLM only produces
`ActionProposal` (see `llm_gateway.py`); the engine validates and applies effects.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------- #
# MESO tier — cohorts
# --------------------------------------------------------------------------- #
class Demographics(BaseModel):
    """Coarse demographic profile of a cohort."""

    median_age: int = Field(..., description="Median age of the cohort in years.")
    urban_rural: str = Field(..., description="Dominant settlement type, e.g. 'urban' or 'rural'.")
    primary_language: str = Field(..., description="Primary language of the cohort.")
    religion_majority: str = Field(..., description="Majority religious identity label.")


class EconomicProfile(BaseModel):
    """Economic exposure of a cohort."""

    median_income_usd: float = Field(..., description="Median annual income in USD.")
    employment_sector: str = Field(..., description="Dominant employment sector.")
    income_sensitivity_to_shipping_disruption: float = Field(
        ..., ge=0, le=1,
        description="How strongly cohort income reacts to shipping disruption, 0..1.",
    )


class MediaExposure(BaseModel):
    """Fraction of the cohort reached by each channel, 0..1 per channel."""

    state_tv: float = Field(0.0, ge=0, le=1, description="Reach of state TV, 0..1.")
    local_radio: float = Field(0.0, ge=0, le=1, description="Reach of local radio, 0..1.")
    social_video_short_form: float = Field(
        0.0, ge=0, le=1, description="Reach of short-form social video, 0..1."
    )
    messaging_apps: float = Field(0.0, ge=0, le=1, description="Reach of messaging apps, 0..1.")
    foreign_language_channels: float = Field(
        0.0, ge=0, le=1, description="Reach of foreign-language channels, 0..1."
    )


class CohortBeliefs(BaseModel):
    """Belief levels for a cohort, each 0..1. Updated by the diffusion model, not the LLM."""

    government_competence: float = Field(..., ge=0, le=1, description="Belief in government competence.")
    foreign_interference_probability: float = Field(
        ..., ge=0, le=1, description="Believed probability of foreign interference."
    )
    trust_in_military: float = Field(..., ge=0, le=1, description="Trust in the military.")
    support_for_western_alignment: float = Field(
        ..., ge=0, le=1, description="Support for aligning with the Western bloc."
    )
    support_for_eastern_alignment: float = Field(
        0.0, ge=0, le=1, description="Support for aligning with the Eastern bloc."
    )


class InfluenceSusceptibility(BaseModel):
    """How persuadable the cohort is by each appeal type, 0..1. Feeds the diffusion model."""

    authority_appeal: float = Field(..., ge=0, le=1, description="Susceptibility to authority framing.")
    identity_appeal: float = Field(..., ge=0, le=1, description="Susceptibility to identity framing.")
    economic_appeal: float = Field(..., ge=0, le=1, description="Susceptibility to economic framing.")


class NetworkPosition(BaseModel):
    """Cohort's position in the social graph."""

    internal_cohesion: float = Field(
        ..., ge=0, le=1, description="Internal cohesion of the cohort, 0..1."
    )
    bridges_to: list[str] = Field(
        default_factory=list, description="IDs of cohorts/institutions this cohort bridges to."
    )


class Cohort(BaseModel):
    """MESO-tier representative agent. One record stands for `represents_population` citizens."""

    cohort_id: str = Field(..., description="Stable unique identifier for the cohort.")
    represents_population: int = Field(
        ..., ge=0, description="Number of real citizens this single agent represents."
    )
    region: str = Field(..., description="Region label the cohort is concentrated in.")
    demographics: Demographics = Field(..., description="Demographic profile.")
    economic_profile: EconomicProfile = Field(..., description="Economic exposure profile.")
    media_exposure: MediaExposure = Field(..., description="Per-channel media reach.")
    beliefs: CohortBeliefs = Field(..., description="Current belief levels (mutated by diffusion).")
    grievances: list[str] = Field(
        default_factory=list, description="Active grievance tags driving susceptibility."
    )
    influence_susceptibility: InfluenceSusceptibility = Field(
        ..., description="Per-appeal persuadability."
    )
    network_position: NetworkPosition = Field(..., description="Position in the social graph.")


# --------------------------------------------------------------------------- #
# MICRO tier — institutional agents
# --------------------------------------------------------------------------- #
class Objective(BaseModel):
    """A weighted goal an agent pursues."""

    goal: str = Field(..., description="Machine-readable goal tag.")
    priority: float = Field(..., ge=0, le=1, description="Relative priority of the goal, 0..1.")


class AgentTraits(BaseModel):
    """Stable behavioural traits influencing action selection, each 0..1."""

    risk_tolerance: float = Field(..., ge=0, le=1, description="Willingness to take risky actions.")
    status_seeking: float = Field(..., ge=0, le=1, description="Drive for status/visibility.")
    institutional_trust: float = Field(..., ge=0, le=1, description="Trust in institutions.")
    corruption_susceptibility: float = Field(
        ..., ge=0, le=1, description="Susceptibility to corrupt inducements."
    )


class AgentResources(BaseModel):
    """Resources an agent controls."""

    budget_control_usd_m: float = Field(..., description="Budget the agent controls, millions USD.")
    political_capital: float = Field(..., ge=0, le=1, description="Spendable political capital, 0..1.")
    personal_network_reach: float = Field(
        ..., ge=0, le=1, description="Reach of the agent's personal network, 0..1."
    )


class AgentMemory(BaseModel):
    """Bounded memory of recent events with decay."""

    recent_events: list[str] = Field(
        default_factory=list, description="Event IDs the agent currently remembers."
    )
    decay_rate: float = Field(
        0.08, ge=0, le=1, description="Per-tick memory decay rate, 0..1."
    )


class MicroAgent(BaseModel):
    """MICRO-tier individually simulated institutional agent (minister, commander, …).

    The LLM may *reason* about which action this agent should take, but the engine decides
    whether the action is legal and computes its numeric effect.
    """

    agent_id: str = Field(..., description="Stable unique identifier for the agent.")
    role: str = Field(..., description="Institutional role, e.g. 'minister_of_defence'.")
    agent_class: str = Field(
        default="micro_institutional", description="Agent class tag for the engine."
    )
    biography_ref: Optional[str] = Field(
        default=None, description="Path/ref to the agent's biography document."
    )
    objectives: list[Objective] = Field(default_factory=list, description="Weighted goals.")
    beliefs: dict[str, float] = Field(
        default_factory=dict, description="Free-form belief map, each value 0..1."
    )
    traits: AgentTraits = Field(..., description="Behavioural traits.")
    resources: AgentResources = Field(..., description="Controlled resources.")
    relationships: dict[str, float] = Field(
        default_factory=dict, description="Valence toward other agents/roles, -1..1."
    )
    information_access: list[str] = Field(
        default_factory=list, description="Information channels the agent can see."
    )
    constraints: list[str] = Field(
        default_factory=list, description="Hard legal/procedural constraints on the agent."
    )
    memory: AgentMemory = Field(default_factory=AgentMemory, description="Bounded event memory.")


# --------------------------------------------------------------------------- #
# Supporting schemas
# --------------------------------------------------------------------------- #
class Relationship(BaseModel):
    """An edge in the social/institutional graph."""

    agent_a: str = Field(..., description="Source agent/cohort id.")
    agent_b: str = Field(..., description="Target agent/cohort id.")
    valence: float = Field(..., ge=-1, le=1, description="Affective valence, -1..1.")
    trust: float = Field(..., ge=0, le=1, description="Trust level, 0..1.")
    dependency: float = Field(..., ge=0, le=1, description="Dependency of a on b, 0..1.")
    last_interaction_tick: int = Field(
        ..., ge=0, description="Tick of the most recent interaction."
    )


class EventVisibility(str, Enum):
    """Who can observe an event."""

    public = "public"
    classified = "classified"
    leaked = "leaked"


class Event(BaseModel):
    """A recorded occurrence. `causal_parents` preserves the chain for explainability."""

    event_id: str = Field(..., description="Stable unique identifier for the event.")
    tick: int = Field(..., ge=0, description="Tick at which the event occurred.")
    type: str = Field(..., description="Event type tag.")
    actors_involved: list[str] = Field(
        default_factory=list, description="IDs of actors involved."
    )
    location: Optional[str] = Field(default=None, description="Location label, if any.")
    visibility: EventVisibility = Field(
        default=EventVisibility.public, description="Observability of the event."
    )
    causal_parents: list[str] = Field(
        default_factory=list, description="Event IDs that caused this event."
    )
    effects: list[dict] = Field(
        default_factory=list, description="Structured effect records applied by the engine."
    )


class Intervention(BaseModel):
    """A player action, parsed by the LLM but validated and priced by the engine."""

    action_id: str = Field(..., description="Stable unique identifier for the action.")
    actor_role: str = Field(..., description="Role initiating the action.")
    action_type: str = Field(..., description="Type of action.")
    target: Optional[str] = Field(default=None, description="Target entity id, if any.")
    resource_cost: dict[str, float] = Field(
        default_factory=dict, description="Resource costs keyed by resource name."
    )
    legal_check: Optional[str] = Field(
        default=None,
        description=(
            "INTENDED to hold a legal-check outcome set by the engine. P0.1 correction "
            "(19 July 2026): no engine legality check exists, so nothing ever sets this. On the "
            "player-decision path the client supplies this value and the endpoint stores and "
            "echoes it unexamined — it is client-controlled, not engine-owned. Treat as a "
            "target field; do not rely on it as an authority."
        ),
    )
    timeline_days: int = Field(
        default=0, ge=0, description="Days until the action takes effect."
    )
    second_order_hooks: list[str] = Field(
        default_factory=list, description="Tags of downstream consequences to schedule."
    )


class TruthStatus(str, Enum):
    """Ground-truth status of a narrative claim."""

    true = "true"
    false = "false"
    unverified = "unverified"


class Narrative(BaseModel):
    """A claim spreading through the information environment."""

    narrative_id: str = Field(..., description="Stable unique identifier for the narrative.")
    claim_text: str = Field(..., description="Human-readable claim.")
    originating_campaign_id: Optional[str] = Field(
        default=None, description="Campaign that seeded this narrative, if any."
    )
    truth_status: TruthStatus = Field(
        default=TruthStatus.unverified, description="Ground-truth status of the claim."
    )
    adoption_by_cohort: dict[str, float] = Field(
        default_factory=dict, description="Per-cohort adoption fraction, 0..1."
    )
    resistance_by_cohort: dict[str, float] = Field(
        default_factory=dict, description="Per-cohort resistance fraction, 0..1."
    )


class CampaignNarrative(BaseModel):
    """The core claim of an information campaign."""

    claim: str = Field(..., description="The claim the campaign pushes.")
    truth_status: TruthStatus = Field(..., description="Ground-truth status of the claim.")


class CampaignMessenger(BaseModel):
    """The apparent source used to carry the campaign."""

    agent_id: str = Field(..., description="Messenger agent id.")
    perceived_independence: float = Field(
        ..., ge=0, le=1, description="How independent the messenger appears, 0..1."
    )


class AmplificationNetwork(BaseModel):
    """Amplification assets behind a campaign."""

    coordinated_accounts: int = Field(..., ge=0, description="Number of coordinated accounts.")
    sympathetic_commentators: int = Field(
        ..., ge=0, description="Number of organic sympathetic commentators."
    )
    estimated_reach: int = Field(..., ge=0, description="Estimated raw reach (people).")


class CampaignMetrics(BaseModel):
    """Live campaign metrics, all computed by the diffusion model — never by the LLM."""

    exposure: float = Field(0.0, ge=0, le=1, description="Fraction of targets exposed, 0..1.")
    belief_adoption: float = Field(0.0, ge=0, le=1, description="Fraction adopting the belief, 0..1.")
    resistance: float = Field(0.0, ge=0, le=1, description="Fraction resisting, 0..1.")
    detection_probability: float = Field(
        0.0, ge=0, le=1, description="Probability the campaign is detected, 0..1."
    )
    attribution_probability: float = Field(
        0.0, ge=0, le=1, description="Probability the campaign is correctly attributed, 0..1."
    )


class Campaign(BaseModel):
    """An information operation. The LLM may compose content; the engine computes spread."""

    campaign_id: str = Field(..., description="Stable unique identifier for the campaign.")
    sponsor: str = Field(..., description="Sponsoring actor id.")
    strategic_objective: str = Field(..., description="High-level objective tag.")
    target_cohorts: list[str] = Field(
        default_factory=list, description="Cohort ids targeted."
    )
    existing_grievance: Optional[str] = Field(
        default=None, description="Pre-existing grievance the campaign exploits."
    )
    narrative: CampaignNarrative = Field(..., description="Core claim.")
    messenger: CampaignMessenger = Field(..., description="Apparent source.")
    channels: list[str] = Field(default_factory=list, description="Channels used.")
    amplification_network: AmplificationNetwork = Field(
        ..., description="Amplification assets."
    )
    trigger_event_id: Optional[str] = Field(
        default=None, description="Event that triggers/times the campaign."
    )
    desired_behaviour: Optional[str] = Field(
        default=None, description="Behaviour the campaign aims to produce."
    )
    metrics: CampaignMetrics = Field(
        default_factory=CampaignMetrics, description="Live campaign metrics (engine-computed)."
    )


class Outcome(BaseModel):
    """The resolved result of a decision, with an explanation trace for the 'why' system."""

    outcome_id: str = Field(..., description="Stable unique identifier for the outcome.")
    decision_id: str = Field(..., description="Id of the decision/intervention resolved.")
    macro_deltas: dict[str, float] = Field(
        default_factory=dict, description="Changes applied to macro indicators."
    )
    meso_deltas: dict[str, float] = Field(
        default_factory=dict, description="Changes applied to cohort/meso values."
    )
    micro_reactions: list[str] = Field(
        default_factory=list, description="Micro-agent reactions triggered."
    )
    explanation_trace: list[str] = Field(
        default_factory=list, description="Ordered causal steps (data, not LLM prose)."
    )
    confidence: float = Field(
        1.0, ge=0, le=1, description="Engine confidence in the outcome, 0..1."
    )


# --------------------------------------------------------------------------- #
# LLM boundary object — the ONLY thing the LLM gateway may return
# --------------------------------------------------------------------------- #
class ActionProposal(BaseModel):
    """A proposal returned by the LLM gateway.

    This is deliberately NOT a state object. It carries *no authority* to change numbers —
    `engine.py` reads it, runs a legality/feasibility check, and only then computes and
    applies effects. This type is the structural enforcement of the determinism boundary.
    """

    proposing_agent_id: str = Field(..., description="Agent the proposal is on behalf of.")
    action_type: str = Field(..., description="Proposed action type tag.")
    target: Optional[str] = Field(default=None, description="Proposed target entity id.")
    rationale: str = Field(
        ..., description="LLM-generated natural-language rationale (interpretive layer only)."
    )
    parameters: dict[str, float] = Field(
        default_factory=dict, description="Proposed numeric parameters (advisory; engine may scale/reject)."
    )
    confidence: float = Field(
        0.5, ge=0, le=1, description="LLM self-reported confidence, 0..1 (advisory only)."
    )
