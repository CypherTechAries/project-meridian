"""Macro state container.

This is a plain state object, NOT a Mesa Agent — the macro tier is national aggregate state
updated once per tick by deterministic rules (see `engine.py`), never stepped like an agent
and never written by the LLM.
"""

from __future__ import annotations

from ..schemas.macro_schema import MacroState


class MacroStateHolder:
    """Owns the live `MacroState` and applies validated deltas.

    Only `engine.py` calls `apply_deltas`. The LLM has no reference to this object — that is
    the determinism boundary enforced structurally.
    """

    def __init__(self, initial: MacroState) -> None:
        self.state: MacroState = initial

    def apply_deltas(self, deltas: dict[str, float]) -> None:
        """Apply additive changes to top-level scalar indicators, clamping bounded ones.

        Keys are indicator names on `MacroIndicators`. Nested blocks (e.g. institutional
        trust) are handled explicitly by the engine, not here.
        """
        ind = self.state.indicators
        bounded = {
            "government_approval",
            "military_readiness",
            "social_stability_index",
            "shipping_throughput_pct_of_baseline",
        }
        for key, delta in deltas.items():
            if not hasattr(ind, key):
                continue
            current = getattr(ind, key)
            if not isinstance(current, (int, float)):
                continue
            updated = current + delta
            if key in bounded:
                updated = max(0.0, min(1.0, updated))
            elif key == "fuel_reserve_days":
                updated = max(0.0, updated)
            setattr(ind, key, updated)

    def snapshot(self) -> dict:
        """Return an immutable serializable snapshot of the current macro state."""
        return self.state.model_dump()
