"""
The canonical belief-outcome classifier — ONE mapping from a belief result to a named outcome.

WHY THIS EXISTS. The uncertain band (0.35–0.65) had drifted into four separate definitions:
`update.py` (the canonical home, used by `UpdateResult.is_uncertain`), `cohorts.py`, `projection.py`
and a set of hard-coded literals in the VP-4 history fixtures. Four copies of one threshold is a
defect waiting to happen: change one and the same person is "unsure" in one surface and "accepted"
in another. This module is the single classifier every surface must call, and it imports the band
from `update.py` rather than restating it.

It does not introduce a new threshold system. It reads the existing frozen semantics:

    not exposed                      -> RETAINED_PRIOR      (no update happened)
    exposed and `is_uncertain`       -> RECEIVED_BUT_UNSURE (the engine's own uncertainty reading)
    exposed and credence > HIGH      -> RECEIVED_AND_ACCEPTED
    exposed and credence < LOW       -> RECEIVED_AND_REJECTED
    exposed and inside the band      -> RECEIVED_BUT_UNSURE

No frozen belief value changes. This only names a result that already existed.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from .update import UNCERTAIN_HIGH, UNCERTAIN_LOW


class BeliefOutcome(str, Enum):
    """The canonical outcome vocabulary. Every surface reuses these names."""

    never_received_through_tick = "NEVER_RECEIVED_THROUGH_TICK"
    received_but_unsure = "RECEIVED_BUT_UNSURE"
    received_and_rejected = "RECEIVED_AND_REJECTED"
    received_and_accepted = "RECEIVED_AND_ACCEPTED"
    retained_prior = "RETAINED_PRIOR"
    unknown = "UNKNOWN"
    unavailable = "UNAVAILABLE"
    not_modelled = "NOT_MODELLED"


def classify_belief_outcome(
    *,
    received: bool,
    credence: Optional[float],
    is_uncertain: bool,
) -> tuple[BeliefOutcome, str]:
    """
    The single canonical classification. Returns the outcome and a short reason.

    `is_uncertain` is the engine's own reading (credence in band AND confidence below its line) and
    takes precedence, so a surface can never call "unsure" something the engine settled, or settle
    something the engine called uncertain.
    """
    if credence is None:
        return BeliefOutcome.unavailable, "no belief value is available"
    if not received:
        return BeliefOutcome.retained_prior, "prior carried forward; not exposed to this event"
    if is_uncertain:
        return BeliefOutcome.received_but_unsure, "in the uncertain band with low confidence"
    if credence > UNCERTAIN_HIGH:
        return BeliefOutcome.received_and_accepted, "moved above the uncertain band"
    if credence < UNCERTAIN_LOW:
        return BeliefOutcome.received_and_rejected, "moved below the uncertain band"
    return BeliefOutcome.received_but_unsure, "remained within the uncertain band"
