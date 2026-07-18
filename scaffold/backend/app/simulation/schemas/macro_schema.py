"""Pydantic v2 schema for the MACRO tier — national/system state.

Mirrors the `macro_state` object in `design_simulation_schemas.md`. Updated once per tick
by deterministic rules + seeded stochastic draws. NO LLM ever writes to this object.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class InstitutionalTrust(BaseModel):
    """Public trust in each institution, 0..1."""

    military: float = Field(..., ge=0, le=1, description="Trust in the military, 0..1.")
    judiciary: float = Field(..., ge=0, le=1, description="Trust in the judiciary, 0..1.")
    media: float = Field(..., ge=0, le=1, description="Trust in the media, 0..1.")
    central_bank: float = Field(..., ge=0, le=1, description="Trust in the central bank, 0..1.")


class AllianceConfidence(BaseModel):
    """Confidence of each external bloc in the nation, 0..1."""

    western_bloc: float = Field(..., ge=0, le=1, description="Western bloc confidence, 0..1.")
    eastern_bloc: float = Field(..., ge=0, le=1, description="Eastern bloc confidence, 0..1.")


class PublicFinances(BaseModel):
    """Fiscal position of the state."""

    treasury_reserve_usd_m: float = Field(
        ..., description="Treasury cash reserve in millions USD."
    )
    deficit_pct_gdp: float = Field(..., description="Budget deficit as a fraction of GDP.")
    debt_service_pct_revenue: float = Field(
        ..., description="Debt service cost as a fraction of government revenue."
    )


class MacroIndicators(BaseModel):
    """The scalar national indicators updated each tick by the rules engine."""

    inflation_rate: float = Field(..., description="Annualised inflation rate, e.g. 0.041.")
    unemployment_rate: float = Field(..., description="Unemployment rate, fraction of labour force.")
    gdp_growth_qoq: float = Field(..., description="Quarter-on-quarter GDP growth, signed fraction.")
    shipping_throughput_pct_of_baseline: float = Field(
        ..., ge=0, description="Strait shipping throughput as a fraction of pre-crisis baseline."
    )
    government_approval: float = Field(
        ..., ge=0, le=1, description="Overall government approval, 0..1."
    )
    institutional_trust: InstitutionalTrust = Field(
        ..., description="Per-institution public trust."
    )
    military_readiness: float = Field(
        ..., ge=0, le=1, description="Aggregate military readiness, 0..1."
    )
    alliance_confidence: AllianceConfidence = Field(
        ..., description="Per-bloc external confidence."
    )
    social_stability_index: float = Field(
        ..., ge=0, le=1, description="Composite social stability, 0..1 (higher = calmer)."
    )
    foreign_direct_investment_flow: float = Field(
        ..., description="Net FDI flow in millions USD (can be negative)."
    )
    fuel_reserve_days: float = Field(
        ..., ge=0, description="Days of national fuel reserve remaining at current burn."
    )
    public_finances: PublicFinances = Field(..., description="Fiscal position block.")


class MacroState(BaseModel):
    """Top-level MACRO state object, snapshotted immutably each tick.

    The `seed` and `scenario_id` pin reproducibility: same seed + scenario + decisions
    produce an identical sequence of `MacroState` values.
    """

    tick: int = Field(..., ge=0, description="Simulation tick index.")
    scenario_id: str = Field(..., description="Identifier of the scenario being run.")
    seed: int = Field(..., description="Deterministic RNG seed for the run.")
    indicators: MacroIndicators = Field(..., description="Scalar national indicators.")
    derivation: str = Field(
        default="rules_engine_v1",
        description="Provenance string describing how this state was derived.",
    )
