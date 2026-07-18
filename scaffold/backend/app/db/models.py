"""SQLAlchemy models mirroring the Pydantic schemas for persistence.

Three tables capture the reproducibility contract: a `simulation_run` (seed + scenario),
an immutable `state_snapshot` per tick, and an append-only `event_log`. JSON columns hold the
schema objects verbatim so the DB stays generic across nation archetypes (data, not code).
Keep these in sync with `app/simulation/schemas/`.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .session import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class SimulationRun(Base):
    """One simulation run. `seed` + `scenario_id` pin reproducibility."""

    __tablename__ = "simulation_run"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    scenario_id: Mapped[str] = mapped_column(String, index=True)
    seed: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow)
    current_tick: Mapped[int] = mapped_column(Integer, default=0)

    snapshots: Mapped[list["StateSnapshot"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )
    events: Mapped[list["EventLog"]] = relationship(
        back_populates="run", cascade="all, delete-orphan"
    )


class StateSnapshot(Base):
    """Immutable macro (and optionally meso) state at a given tick — enables branching."""

    __tablename__ = "state_snapshot"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("simulation_run.id"), index=True)
    tick: Mapped[int] = mapped_column(Integer, index=True)
    macro_state: Mapped[dict] = mapped_column(JSON)
    meso_state: Mapped[dict] = mapped_column(JSON, default=dict)

    run: Mapped[SimulationRun] = relationship(back_populates="snapshots")


class EventLog(Base):
    """Append-only causal event log for the explanation system."""

    __tablename__ = "event_log"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(ForeignKey("simulation_run.id"), index=True)
    tick: Mapped[int] = mapped_column(Integer, index=True)
    event: Mapped[dict] = mapped_column(JSON)

    run: Mapped[SimulationRun] = relationship(back_populates="events")
