"""Macro state container — RETIRED by P0.4.

This class previously owned the live `MacroState` and applied deltas to it via `apply_deltas`,
which wrote indicator values with `setattr`. It was one of several scattered mutation paths.

Since P0.4, authoritative macro state lives in `AuthoritativeState.macro`
(`app/simulation/state.py`), and the ONLY way to change it is a validated transition through
`TransitionService` (`app/simulation/transitions.py`).

Nothing in the codebase constructs this class any more. It is kept as a **tripwire** rather than
deleted: a live-but-unused mutation method is a bypass waiting to be reintroduced by a future
change, and a loud failure is better than a silent second write path. Every method raises.

Two behaviours of the old implementation are worth recording, because the replacement changed them:

  * `apply_deltas` SILENTLY IGNORED unrecognised keys (`if not hasattr(ind, key): continue`).
    A misspelled or nested indicator name produced no error, no warning and no effect, so a rule
    pack could author an effect that never applied and nothing would report it. The transition
    boundary now REJECTS unknown keys.
  * Nested state such as `public_finances` was unreachable by the only delta path, so no engine
    action could touch fiscal state. That remains true — no fiscal path exists — but it is now an
    explicit rejection rather than a silent skip.

Remove this file once no documentation references `MacroStateHolder`. Tracked as compatibility
debt in `docs/delivery/P0-4-STATE-CONTRACT.md`.
"""

from __future__ import annotations

from typing import Any, NoReturn

_RETIRED = (
    "MacroStateHolder was retired by Phase 0 item P0.4. Authoritative macro state lives in "
    "AuthoritativeState.macro and may only be changed by submitting a Transition to "
    "TransitionService. See app/simulation/transitions.py."
)


class MacroStateHolder:
    """Retired. Constructing or using this raises — a deliberate tripwire, not a shim."""

    def __init__(self, initial: Any) -> None:  # noqa: ARG002 - signature preserved deliberately
        raise NotImplementedError(_RETIRED)

    def apply_deltas(self, deltas: dict[str, float]) -> NoReturn:  # noqa: ARG002
        raise NotImplementedError(_RETIRED)

    def snapshot(self) -> NoReturn:
        raise NotImplementedError(_RETIRED)
