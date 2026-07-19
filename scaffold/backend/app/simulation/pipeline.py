"""The deterministic staged mechanism runner — Phase 0 item P0.5.

Runs the declared causal chain once per tick, in fixed stage order, routing every accepted change
through `TransitionService`.

THE STAGE CONTRACT
------------------
For each mechanism, in declared order:

  1. read an immutable authoritative-state view;
  2. evaluate the rule-pack conditions;
  3. request keyed draws only where the mechanism explicitly needs one;
  4. emit typed PROPOSED transitions;
  5. pass them through validation;
  6. apply accepted ones via `TransitionService` — still the only writer;
  7. record mechanism id, version, source fields, draw references and causal parents.

No mechanism mutates state itself, and no mechanism writes another tier directly. A later stage
may read an earlier stage's output from the SAME tick; anything feeding backwards reads the
previous tick's recorded value via the lag mechanism. There are therefore no same-tick causal
cycles.

At the end of every tick a bookkeeping transition snapshots the chain scalars into
`chain.previous`, which is what lagged mechanisms read next tick.

NOT REPLAY. Causal parents are recorded so a reader can see which transition a later one followed
from. Nothing replays from them, nothing persists, and no state can be rebuilt. That is P0.6.
"""

from __future__ import annotations

from typing import Iterable, Optional

from .mechanisms import CHAIN, Mechanism
from .transitions import Transition, TransitionOrigin, TransitionRecord, TransitionType


class ChainRunner:
    """Executes the declared mechanism chain against a model, one tick at a time."""

    def __init__(self, model, enabled: Optional[Iterable[str]] = None) -> None:
        """`enabled` restricts which mechanisms run — the counterfactual switch.

        Disabling a mechanism is how the project demonstrates that a link MATTERS: run with it,
        run without it, and attribute the downstream difference to that link alone. `None` means
        every declared mechanism runs.
        """
        self.model = model
        self.enabled: Optional[set[str]] = set(enabled) if enabled is not None else None

    def is_enabled(self, mech: Mechanism) -> bool:
        return self.enabled is None or mech.id in self.enabled

    def run_tick(self) -> list[TransitionRecord]:
        """Run every enabled mechanism once, in stage order, then snapshot for next tick's lags."""
        records: list[TransitionRecord] = []
        # Causal parents within a tick: a mechanism's transitions follow from the transitions the
        # previous stage applied. This is deliberately shallow - it records adjacency, not a graph.
        previous_stage_ids: list[str] = []

        for mech in CHAIN:
            if not self.is_enabled(mech):
                continue

            proposals = mech.fn(self.model.state, self.model.draws)
            applied_here: list[str] = []

            for proposal in proposals:
                if previous_stage_ids and not proposal.causal_parents:
                    proposal = proposal.model_copy(
                        update={"causal_parents": list(previous_stage_ids)}
                    )
                record = self.model.submit(proposal)
                records.append(record)
                if record.applied:
                    applied_here.append(record.transition_id)

            if applied_here:
                previous_stage_ids = applied_here

        # End-of-tick bookkeeping: record this tick's chain values for next tick's lagged reads.
        records.append(
            self.model.submit(
                Transition(
                    type=TransitionType.SNAPSHOT_CHAIN_PREVIOUS,
                    origin=TransitionOrigin.ENGINE_RULE,
                    mechanism="chain_lag_bookkeeping",
                    mechanism_version="1.0.0",
                )
            )
        )
        return records

    def apply_incident(self, severity: float, label: str = "") -> TransitionRecord:
        """Inject the scenario's maritime incident as an explicit EXTERNAL input.

        Deliberately not hard-coded inside the tick loop. A run can therefore execute as a
        baseline with no incident at all, which is what makes "the chain does not start on its
        own" a testable property rather than an assurance.
        """
        return self.model.submit(
            Transition(
                type=TransitionType.APPLY_INCIDENT,
                origin=TransitionOrigin.EXTERNAL_INPUT,
                payload={"severity": severity, "label": label},
                mechanism="scenario_incident_input",
                mechanism_version="1.0.0",
                source_fields=["scenario.incidents"],
            )
        )
