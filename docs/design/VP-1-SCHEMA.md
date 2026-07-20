# VP-1 — Virtual Person schema, identity boundary and invariants

VP-1 is the foundation of the Virtual Person model: it defines **what a fictional person is in the
data**, before anything decides how that person thinks or acts.

Code: `scaffold/backend/app/simulation/person/` · Tests:
`scaffold/backend/tests/test_virtual_person_vp1.py` · Design: [`VIRTUAL-PERSON-V0.1.md`](VIRTUAL-PERSON-V0.1.md)

## What VP-1 implements

A versioned root model `virtual-person@0.1` with four structurally separate sections:

| Section | VP-1 contents |
|---|---|
| `identity` | Fixture-authored descriptive context. Display only. |
| `state` | The **typed shape** of future engine state. Populated with nothing; every collection empty, status `NOT_MODELLED`. |
| `explanations` | The typed container for future engine-grounded explanations. Empty. |
| `model_boundary` | What MERIDIAN does not model, as typed values. |

Plus: a typed person-id resolver, the `DecisionInputs` shape that structurally excludes identity, the
`trusts_for` scope invariant, and a `from_cast` fixture adapter.

## What VP-1 deliberately does NOT implement

No goals that change · no pressure transitions · no action selection · no decision scoring · no
relationship effects · no information transmission · no belief transitions · no memory · no social
interaction · no cumulative stress · no changing trust · no LLM · no conversational UI · **no API
routes** · no portraits or image infrastructure. Those are VP-2 through VP-6.

Reserved state is empty tuples with a documented meaning. **An empty collection is not zero and is
not an engine result.**

## Identity versus engine state

`identity` is authored fictional context — a role label, a null portrait, an optional biography. It
is **display only**. It is never an input to a belief calculation, a decision, competence,
intelligence, morality, trust or action availability. Two tests prove belief output is byte-identical
regardless of biography or portrait.

`state` is the shape the engine will later fill. In VP-1 it is inert and reports `NOT_MODELLED`. A
validator forbids it reporting `ENGINE` before the engine produces a value.

## Origin and absence semantics

Reused, not reinvented. Field origins use the belief slice's `Origin`
(`FIXTURE` / `ENGINE` / `UNKNOWN` / `UNAVAILABLE`). Layer status uses `LayerStatus`, which mirrors
those four and adds **one documented member, `NOT_MODELLED`** — because "the engine does not model
this yet" is a distinct claim from "unavailable", and no existing enum carried all five together.

- Identity reports `FIXTURE`.
- A reserved state layer reports `NOT_MODELLED`, never `ENGINE`.
- Missing descriptive fields are `null`. **Missing is never numeric zero** — asserted by a walker.

## Why portrait and biography do not control behaviour

Appearance and background identify a person; they must never decide how the person behaves. This is
the belief slice's standing rule (background is not a proxy for capability) carried up to the person.
It is enforced two ways:

1. `DecisionInputs` — the shape a future decision function may receive — has **no** field for
   portrait, biography, display name, occupation, education, socioeconomic description or life stage.
   A decision cannot receive them even by accident. A test asserts the exact field set.
2. Tests mutate biography and portrait across wide ranges and assert the belief projection is
   unchanged.

## trusts_for is always scoped

Relationships are typed edges with **no strength or score field of any kind**. The design invariant is
enforced now even though relationship *effects* are VP-4: a `trusts_for` edge is invalid unless it
names a subject/proposition/domain/process. There is never an unscoped "A trusts B: 0.8". There is no
universal influence, susceptibility, persuadability or general-trust score anywhere in the schema —
prohibited field-name fragments are rejected by a test that walks every model.

## Migration and compatibility

`from_cast(person_id)` is the only bridge from the existing belief cast to Virtual Person. It reuses
existing fictional ids and cast descriptions, keeps `display_name` as the existing role label, leaves
`portrait_ref` null, and invents nothing to fill the schema. **No public entity id is renamed and no
identity is duplicated.** The belief snapshot and read-model API are untouched, and the belief
snapshot is **not** connected to authoritative run state in VP-1 — that remains gated on
[issue #16](https://github.com/CypherTechAries/project-meridian/issues/16).

## How later milestones extend this

- **VP-2** populates goals, responsibilities, pressures and constraints (real values, ENGINE origin).
- **VP-3** implements deterministic action selection and the decision trace, reading only
  `DecisionInputs`.
- **VP-4** implements relationships-with-effect and ordered information/belief history.
- **VP-5** exposes a read-only Virtual Person API.
- **VP-6** builds Ask MERIDIAN Phase 1 on deterministic structured answers, no LLM.

Each is a separate PR and a separate review.

## Known limitations

- Every state and explanation layer is a reserved, empty shape — VP-1 answers "what is a person",
  not "how does a person act".
- Only the three existing cast people adapt; no new people are authored.
- No API route exists yet (VP-5).
- The belief-cast / packaged-scenario id collision remains open (issue #16); VP-1 does not touch it.
