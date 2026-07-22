"""
The single authoritative description of what the packaged scenario currently shows.

WHY THIS EXISTS. The Briefing and Ask MERIDIAN contradicted each other about the same run. The
Briefing said political pressure was low and falling; Ask said it was "still high". Both surfaces
were describing the same 20-tick deterministic run, and only one of them was reading it.

The Briefing derived its claim from the run. Ask did not derive its claim from anything — the
sentence was authored by hand and shipped as prose. A hand-written sentence cannot drift back
towards the truth when the engine's output moves, so it was wrong the moment the numbers changed,
and nothing could detect it.

WHAT THIS MODULE OWNS. Facts about the packaged run: the value of each chain field, how large it is,
which way it is moving, and where it sits relative to its own peak. That is all.

WHAT IT DOES NOT OWN. Wording. Every surface writes its own sentences — the Briefing in plain
English for a first-time reader, Ask in its own register, the technical view in engine vocabulary.
They may describe this state differently. They may not carry separate versions of it.

NO ENGINE CHANGE. This module reads the engine's output. It computes no simulation value, defines
no mechanism, and changes no coefficient. Removing it would change nothing about any run.

TWO MEASURES, NOT ONE. The contradiction was made possible by conflating two different true
statements. Political pressure at the end of the packaged run is 0.1495 on a 0-1 scale, which is
LOW in absolute terms, and 97% of the highest it has ever been in this run, which is NEAR ITS PEAK.
Both are facts. Reported as if they were the same measure, they read as a contradiction. This
module therefore reports `level` and `near_peak` as SEPARATE fields, and any surface that mentions
one without the other is choosing to tell half the story.
"""

from __future__ import annotations

from enum import Enum
from functools import lru_cache
from typing import Any, Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

_FROZEN = ConfigDict(extra="forbid", frozen=True)


class Level(str, Enum):
    """How much of something there is, in absolute terms on the field's own 0-1 scale."""

    none = "NONE"
    low = "LOW"
    moderate = "MODERATE"
    high = "HIGH"


class Direction(str, Enum):
    """Which way the value has moved. A description of the run, never a forecast."""

    rising = "RISING"
    falling = "FALLING"
    steady = "STEADY"
    not_established = "NOT_ESTABLISHED"


# Declared thresholds. Authored, fictional, and calibrated against nothing — like every other
# coefficient in this project. They are here, once, so two surfaces cannot pick different ones.
LEVEL_HIGH = 0.66
LEVEL_MODERATE = 0.33

# A direction needs a window to be read over. Below this many points, nothing truthful can be said.
DIRECTION_WINDOW = 6
# Movement smaller than this is not reported as movement.
DIRECTION_FLOOR = 0.004
DIRECTION_RELATIVE = 0.02
# A value holding at least this share of its own peak is still near it.
NEAR_PEAK_RETENTION = 0.9
# A value must fall by more than this share of its peak before the peak counts as past.
POST_PEAK_MARGIN = 0.005


class FieldState(BaseModel):
    """The complete authoritative state of one chain field. Every surface reads this."""

    model_config = _FROZEN

    field: str
    value: float
    level: Level
    direction: Direction
    peak_value: float
    peak_tick: int
    #: Share of its own peak the value still holds, 0-1.
    peak_retention: float
    #: True when the value has turned over but still holds most of its peak.
    near_peak: bool
    #: True when the peak is in the past and the value has measurably fallen from it.
    post_peak: bool
    #: False when no trajectory was available, so `direction` is NOT_ESTABLISHED rather than STEADY.
    #: An unmeasured direction must never be reported as a measured absence of movement.
    direction_measured: bool


class ScenarioState(BaseModel):
    """What the packaged scenario shows. The one factual representation both surfaces read."""

    model_config = _FROZEN

    scenario_id: str
    seed: int
    ticks: int
    #: The horizon the scenario DECLARES. Held here so a surface can say where in the arc a reader
    #: is without re-reading the projection, and so both surfaces cannot disagree about it.
    horizon_ticks: int
    #: True when the run has reached its declared horizon — i.e. this is the last recorded point.
    #: Derived, never asserted: a shorter run must not claim to be the end of the scenario.
    is_final_recorded_tick: bool
    simulated_hours: float
    fields: dict[str, FieldState] = Field(default_factory=dict)

    def get(self, field: str) -> Optional[FieldState]:
        return self.fields.get(field)

    @property
    def days(self) -> int:
        return max(1, round(self.simulated_hours / 24))


def classify_level(value: float) -> Level:
    if value >= LEVEL_HIGH:
        return Level.high
    if value >= LEVEL_MODERATE:
        return Level.moderate
    if value > 0:
        return Level.low
    return Level.none


def classify_direction(values: Sequence[float]) -> tuple[Direction, bool]:
    """
    Direction over the last `DIRECTION_WINDOW` recorded values.

    Returns `(direction, measured)`. Too short a series returns NOT_ESTABLISHED with
    `measured=False` — deliberately not STEADY, because "we did not look" and "it did not move"
    are different claims and only one of them is honest here.
    """
    if len(values) < DIRECTION_WINDOW:
        return Direction.not_established, False
    now = values[-1]
    then = values[-DIRECTION_WINDOW]
    delta = now - then
    if abs(delta) < max(DIRECTION_FLOOR, abs(now) * DIRECTION_RELATIVE):
        return Direction.steady, True
    return (Direction.rising if delta > 0 else Direction.falling), True


def derive_field_state(field: str, value: float, values: Sequence[float]) -> FieldState:
    """
    One declared rule, applied to every field. `value` is the authoritative current value from the
    projection; `values` is the recorded per-tick history, which may be empty.
    """
    direction, measured = classify_direction(values)

    peak_value = max(values) if values else value
    peak_tick = (list(values).index(peak_value) + 1) if values else 0
    retention = (value / peak_value) if peak_value > 0 else 0.0
    last_tick = len(values)

    near_peak = (
        direction is not Direction.rising
        and retention >= NEAR_PEAK_RETENTION
        and peak_tick > 0
    )
    post_peak = (
        peak_tick > 0
        and peak_tick < last_tick
        and (peak_value - value) > peak_value * POST_PEAK_MARGIN
    )

    # A value that has turned over reads as FALLING even where the window is too narrow to call it.
    # At the packaged state political pressure has dropped 0.0033 over five ticks, under the 0.004
    # floor, while sitting 0.004 below a peak it passed three ticks ago. "Steady" would hide a turn
    # the run genuinely shows.
    if measured and direction is Direction.steady and post_peak:
        direction = Direction.falling

    return FieldState(
        field=field,
        value=value,
        level=classify_level(value),
        direction=direction,
        peak_value=peak_value,
        peak_tick=peak_tick,
        peak_retention=retention,
        near_peak=near_peak,
        post_peak=post_peak,
        direction_measured=measured,
    )


def scenario_state(
    scenario_id: str,
    seed: int,
    projection: dict[str, Any],
    trajectory: Sequence[dict[str, Any]],
) -> ScenarioState:
    """
    Build the authoritative state from a run's own projection and trajectory.

    The projection supplies the current value of every stage — it is the authority for "what is it
    now". The trajectory supplies the history, and covers fewer fields; a field absent from the
    trajectory gets an honestly unmeasured direction rather than a fabricated one.
    """
    fields: dict[str, FieldState] = {}
    for stage in projection.get("stages", []):
        field = stage.get("field")
        raw = stage.get("value")
        if not isinstance(field, str) or not isinstance(raw, (int, float)):
            continue
        history = [
            float(point[field])
            for point in trajectory
            if isinstance(point.get(field), (int, float))
        ]
        fields[field] = derive_field_state(field, float(raw), history)

    horizon = int(projection.get("demonstration_horizon_ticks") or 0)
    executed = len(trajectory)
    return ScenarioState(
        scenario_id=scenario_id,
        seed=seed,
        ticks=executed,
        horizon_ticks=horizon,
        is_final_recorded_tick=bool(horizon) and executed >= horizon,
        simulated_hours=float(projection.get("simulated_hours") or 0.0),
        fields=fields,
    )


@lru_cache(maxsize=1)
def packaged_scenario_state() -> ScenarioState:
    """
    The state of the DEFAULT packaged run — the same scenario, seed and tick count the demonstration
    endpoint executes for its default request, and therefore the same state the Briefing displays.

    Cached because the run is deterministic: the same inputs produce the same output every time, so
    a cached result is the result. It is not a stored history and nothing can write to it.

    Imported lazily to keep this module free of any dependency on the API layer.
    """
    from ..api.routes_demo import packaged_run_state

    return packaged_run_state()
