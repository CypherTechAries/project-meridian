"""
Virtual Person — VP-1: schema, fixture-identity boundary, origins and invariants.

VP-1 defines what a fictional person IS in the data. It implements NO behaviour: no goals that
change, no pressures, no action selection, no decisions, no relationships-with-effect, no
information transmission, no belief transitions, no memory, no trust change, no LLM, no API routes
and no portraits. Those are VP-2 onwards.

See `schema.py` for the models and `docs/design/VP-1-SCHEMA.md` for the boundary.
"""

from __future__ import annotations

from .schema import (
    DecisionInputs,
    Explanations,
    FixtureIdentity,
    PersonState,
    Relationship,
    RelationshipType,
    VirtualPerson,
    from_cast,
    resolve_person_ref,
)

__all__ = [
    "DecisionInputs",
    "Explanations",
    "FixtureIdentity",
    "PersonState",
    "Relationship",
    "RelationshipType",
    "VirtualPerson",
    "from_cast",
    "resolve_person_ref",
]
