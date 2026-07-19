"""Deterministic keyed draw service — Phase 0 item P0.4A, implementing ADR-010.

THE PROBLEM THIS REPLACES
-------------------------
The engine previously drew every random value from one shared `random.Random` stream, in call
order. A3 demonstrated the consequence: `CohortAgent.step` draws only when a cohort has
grievances, so changing how many cohorts have grievances changed how many draws were consumed,
which shifted every later draw in the stream, which moved macro indicators. That looked like
meso→macro causality and was not — it was stream displacement. Any future change adding or
removing a draw anywhere would silently perturb unrelated results, and the existing determinism
test would absorb it as expected divergence.

THE CONTRACT THIS ESTABLISHES
-----------------------------
A draw is a pure function of a KEY, not of position in a sequence. Nothing accumulates, nothing
advances, and no subsystem can displace another. Requesting a draw twice with the same key yields
the same value; requesting one that never existed before changes nothing else.

WHAT THIS IS NOT
----------------
This is **not** replay. It is the determinism that replay will later depend on. No inputs are
recorded, no history is kept, and no run can be reconstructed. That is P0.6.

ALGORITHM — documented precisely because an under-specified key encoding is the most likely
source of a silent reproducibility break.

  algorithm            : HMAC-SHA-256 (stdlib `hmac` + `hashlib`; no new dependency)
  algorithm version    : "hmac-sha256-v1"
  key encoding version : "meridian-key-v1"
  HMAC key             : b"meridian-rng-v1|seed=<run_seed>"      (UTF-8)
  HMAC message         : the canonical key encoding below         (UTF-8)
  byte→integer         : int.from_bytes(digest[0:8], "big")       → unsigned 64-bit
  float mapping        : (u64 >> 11) / 2**53                      → [0.0, 1.0), 53-bit exact
  bounded integer      : rejection sampling (see `bounded_int`), never modulo
  repeated draws       : an explicit `index` field in the key; never implicit advancement

CANONICAL KEY ENCODING ("meridian-key-v1")
------------------------------------------
Fields are emitted in a FIXED order, each length-prefixed so the encoding is injective — two
different field sets cannot produce the same byte string:

    meridian-key-v1
    <len>:<field-name>=<len>:<value>;   ... for each field, in fixed order

Values are `str()` of the supplied value, UTF-8 encoded, with lengths measured in BYTES. Field
order is fixed by `_KEY_FIELDS`, not by dict iteration order. Python's `hash()` is never used —
it is randomised per process and would make keys unstable across runs.

REPRODUCIBILITY CLAIM — read before widening it
-----------------------------------------------
Deterministic on the tested CPython implementation, verified in-process and across a subprocess
with a different `PYTHONHASHSEED`. Cross-language and cross-version reproducibility is **NOT**
claimed: the published test vectors have not been reproduced outside Python. Do not describe this
as cross-language reproducible until they have been.
"""

from __future__ import annotations

import hashlib
import hmac
from typing import Optional

from pydantic import BaseModel, Field

ALGORITHM = "hmac-sha256-v1"
KEY_ENCODING_VERSION = "meridian-key-v1"
RANDOMNESS_ARCHITECTURE = "keyed_counter_v1"

# Fixed field order for the canonical key. Appending a NEW field changes every derived value, so
# it is a breaking change requiring a KEY_ENCODING_VERSION bump.
_KEY_FIELDS = (
    "scenario",
    "rule_pack",
    "subsystem",
    "entity",
    "purpose",
    "context",
    "index",
)


class DrawKey(BaseModel):
    """The complete identity of a draw. Same key ⇒ same value, always."""

    subsystem: str
    purpose: str
    # Entity, cohort or interaction identifier. Empty for run-wide draws.
    entity: str = ""
    # Tick or transition context. Empty for context-free draws.
    context: str = ""
    # Explicit index for repeated draws with otherwise identical keys. NEVER implicit.
    index: int = 0
    scenario: str = ""
    rule_pack: str = ""

    def canonical(self) -> str:
        """Injective, length-prefixed, fixed-order encoding. See module docstring."""
        parts = [KEY_ENCODING_VERSION]
        for field in _KEY_FIELDS:
            name = field
            value = str(getattr(self, field))
            nb = len(name.encode("utf-8"))
            vb = len(value.encode("utf-8"))
            parts.append(f"{nb}:{name}={vb}:{value};")
        return "".join(parts)


class DrawReference(BaseModel):
    """A citable record of one draw, suitable for `Transition.draw_refs`.

    Recording a reference is NOT replay. It identifies which draw produced a value so a reader can
    reproduce it independently; it does not reconstruct a run.
    """

    ref: str
    algorithm: str = ALGORITHM
    key_encoding: str = KEY_ENCODING_VERSION
    subsystem: str
    purpose: str
    entity: str = ""
    context: str = ""
    index: int = 0
    # First 8 hex chars of the digest — enough to distinguish draws, not a security claim.
    digest: str = ""


class DeterministicDrawService:
    """Keyed draw service. The ONLY source of authoritative randomness.

    Holds no mutable stream state. Every method is a pure function of (seed, key) — so a draw
    cannot displace another draw, and a rejected transition cannot consume anything, because
    nothing is consumed at all.
    """

    def __init__(self, seed: int, scenario: str = "", rule_pack: str = "") -> None:
        self._seed = seed
        self._scenario = scenario
        self._rule_pack = rule_pack
        self._hmac_key = f"meridian-rng-v1|seed={seed}".encode("utf-8")

    # -------------------------------------------------------------- #
    # Core derivation
    # -------------------------------------------------------------- #
    def _digest(self, key: DrawKey) -> bytes:
        key = key.model_copy(update={"scenario": self._scenario, "rule_pack": self._rule_pack})
        return hmac.new(self._hmac_key, key.canonical().encode("utf-8"), hashlib.sha256).digest()

    def _key(
        self, subsystem: str, purpose: str, entity: str, context: str, index: int
    ) -> DrawKey:
        return DrawKey(
            subsystem=subsystem,
            purpose=purpose,
            entity=entity,
            context=context,
            index=index,
            scenario=self._scenario,
            rule_pack=self._rule_pack,
        )

    def reference(
        self, subsystem: str, purpose: str, entity: str = "", context: str = "", index: int = 0
    ) -> DrawReference:
        """Build the citable reference for a draw without consuming anything."""
        key = self._key(subsystem, purpose, entity, context, index)
        digest = self._digest(key)
        return DrawReference(
            ref=f"{ALGORITHM}:{subsystem}/{purpose}/{entity or '-'}/{context or '-'}#{index}",
            subsystem=subsystem,
            purpose=purpose,
            entity=entity,
            context=context,
            index=index,
            digest=digest[:4].hex(),
        )

    # -------------------------------------------------------------- #
    # Draw operations — only what current behaviour and P0.5 need.
    # -------------------------------------------------------------- #
    def uint64(
        self, subsystem: str, purpose: str, entity: str = "", context: str = "", index: int = 0
    ) -> int:
        """Deterministic unsigned 64-bit integer."""
        digest = self._digest(self._key(subsystem, purpose, entity, context, index))
        return int.from_bytes(digest[0:8], "big")

    def unit_float(
        self, subsystem: str, purpose: str, entity: str = "", context: str = "", index: int = 0
    ) -> float:
        """Deterministic float in [0.0, 1.0).

        Uses the top 53 bits so every representable double in the range is reachable and the
        mapping is exact — the standard construction, not a modulo of the full 64 bits.
        """
        return (self.uint64(subsystem, purpose, entity, context, index) >> 11) / float(1 << 53)

    def uniform(
        self,
        low: float,
        high: float,
        subsystem: str,
        purpose: str,
        entity: str = "",
        context: str = "",
        index: int = 0,
    ) -> float:
        """Deterministic uniform float in [low, high)."""
        return low + (high - low) * self.unit_float(subsystem, purpose, entity, context, index)

    def jitter(
        self,
        magnitude: float,
        subsystem: str,
        purpose: str,
        entity: str = "",
        context: str = "",
        index: int = 0,
    ) -> float:
        """Deterministic symmetric jitter in [-magnitude, +magnitude)."""
        return self.uniform(-magnitude, magnitude, subsystem, purpose, entity, context, index)

    def bounded_int(
        self,
        bound: int,
        subsystem: str,
        purpose: str,
        entity: str = "",
        context: str = "",
        index: int = 0,
    ) -> int:
        """Deterministic integer in [0, bound), free of modulo bias.

        Rejection sampling: 2**64 is not generally divisible by `bound`, so plain `% bound` would
        favour the low residues. Values at or above the largest exact multiple of `bound` are
        rejected and the draw is retried at a derived sub-index. Retry is bounded and derived —
        it consumes nothing and cannot displace another draw.
        """
        if bound <= 0:
            raise ValueError("bound must be positive")
        limit = (1 << 64) - ((1 << 64) % bound)  # largest exact multiple of `bound`
        for attempt in range(64):
            # Sub-index keeps each retry a distinct, reproducible key.
            value = self.uint64(subsystem, purpose, entity, context, index * 1000 + attempt)
            if value < limit:
                return value % bound
        # Astronomically unlikely; fail loudly rather than silently biasing.
        raise RuntimeError(f"bounded_int rejection sampling failed after 64 attempts (bound={bound})")


def make_run_metadata_fields() -> dict[str, str]:
    """The randomness fields recorded in authoritative run metadata."""
    return {
        "randomness_architecture": RANDOMNESS_ARCHITECTURE,
        "rng_algorithm": ALGORITHM,
        "rng_algorithm_version": ALGORITHM,
        "key_encoding_version": KEY_ENCODING_VERSION,
    }
