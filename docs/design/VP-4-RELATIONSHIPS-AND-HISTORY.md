# VP-4 — relationships and ordered history

VP-4 records what a fictional person is connected to, what information they received, and what belief
state was observed — in a deterministic, ordered, append-only form. **It records; it does not cause.**

Code: `scaffold/backend/app/simulation/person/history.py`, `vp4_fixtures.py` ·
Tests: `tests/test_virtual_person_vp4.py`

## Claim boundary

> Virtual Person History v0.1 records declared fictional relationships, information exposure and
> belief observations in a deterministic, ordered and inspectable form. It does not model a complete
> life history, social network or psychological trajectory.

## What a relationship edge means

A `RelationshipEdge` is a **declared connection** — "member of the national government", "represents
affected families". It is **not** a numerical measure of one person's power over another. There is no
influence, trustworthiness, strength, closeness, susceptibility, persuadability, loyalty or emotional
dependency score of any kind. Kinds: family, colleague, reports_to, member_of, represents,
trusts_for, receives_from.

**Direction** is documented: reports_to, member_of, represents, receives_from and trusts_for are
directional; colleague is symmetric via a documented normalisation; family carries no implied
direction or role. Reverse edges are never silently invented; if a normalised reverse edge is ever
produced it is marked `ENGINE`, never `FIXTURE`.

**`trusts_for`** must always be scoped to a declared proposition, subject, domain, verification or
source process — *"trusts the verification process for corroboration of a factual allegation before
publication"*, never *"Person A trusts Person B"*. No numeric trust value is added, and it is not
connected to the belief update rule.

**`receives_from`** records a declared information path. It does **not** mean the source is believed,
the source is influential, every message was received, or that information automatically changes
belief. Receipt is only ever an explicit `InformationRecord`; the edge does not generate it.

## What `NOT_RECEIVED_THROUGH_TICK` means

Information exposure is time-bounded. "Not received through tick 5" says only that the available
record shows the person had not received it *by that point* — a later record can show subsequent
receipt. It is **not** rejected, ignored, disbelieved, opposed or unavailable-in-the-world. Absence
is first-class: missing exposure is never silently turned into NOT_RECEIVED, and no negative belief
is ever inferred from missing exposure. Where nothing reliable is known, the status is `UNKNOWN` or
`UNAVAILABLE`.

## Why not receiving is different from rejection

They live in different vocabularies. Exposure is `RECEIVED` / `NOT_RECEIVED_THROUGH_TICK` / `UNKNOWN`
/ `UNAVAILABLE` / `NOT_MODELLED`. Belief outcome is `RECEIVED_AND_REJECTED` and its siblings. A person
who never received a claim has **not rejected it** — that distinction is the belief slice's core
honesty property, carried up to the person's history.

## What a belief-history entry records

A `BeliefHistoryEntry` is one observation of belief state, **reusing the existing belief slice's
values and vocabulary** — VP-4 computes no belief of its own and changes no frozen value. It keeps the
`value_origin` (where the number came from) separate from the `decision_origin` (who decided to keep
or change it), classifies the outcome using existing proposition-level semantics
(`RECEIVED_AND_ACCEPTED` / `RECEIVED_AND_REJECTED` / `RECEIVED_BUT_UNSURE` / `RETAINED_PRIOR` / …), and
discloses on every entry that the result is a `packaged-belief-snapshot` with
`connected_to_authoritative_run: false`.

## Why one entry is not a trajectory

When only one belief update exists, the history reports `observation_count: 1` and
`trajectory_available: false`, and says so in plain language:

> MERIDIAN has one recorded belief update for this proposition. It does not yet have enough history
> to describe a longer-term pattern.

One entry is never labelled a trend, trajectory, long-term movement, persistent tendency or
behavioural pattern. The model refuses `trajectory_available: true` below two observations.

## Why engine history is not human memory

The history is an **engine audit record**, not cognition. VP-4 does not claim the person remembers
anything, and implements no recall, forgetting, salience decay, retrieval, summarisation or LLM
memory. It is a record of what happened, kept so it can be inspected.

## Why relationships do not affect decisions yet

VP-4 is recording, not causal integration. Relationship and history data cannot alter VP-2 situation
transitions, VP-3 option comparison, the VP-3 selected action, or any belief output — proven by
mutation tests. There is no social transmission (no person-to-person propagation, delivery rules,
cascades, feed ranking, influence spread or coordinated-account modelling) and no changing trust (no
updates, decay, reputation or source-learning). Existing contextual source trust in the belief rule
is untouched and is never derived from a relationship edge.

## Append-only history

Three pure append functions (relationship, information, belief). A valid append preserves every prior
entry byte-for-byte, rejects duplicate ids, enforces stable ordering (tick, event_order, id), rejects
conflicting same-tick information records (no reconciliation rule is invented to hide a conflict),
validates typed fictional references, and returns a new immutable history plus a trace of the
decision. There is **no update or delete**; correction, if ever needed, would be a future explicit
correction entry.

## Boundaries held

No relationship effects · no social transmission · no changing trust · no memory model · no VP-3
action executed (all decisions remain `NOT_EXECUTED`) · no consequences appended to histories · no
API route (VP-5, `main.py` untouched) · no LLM or UI. VP-1 schema, VP-2 transitions, VP-3 decision
rule, belief update rule, read-model API, fictional registry, B5 controls and the scenario-id
disclosure are unchanged; the packaged belief snapshot is not connected to authoritative run state
(issue #16 remains open).

## What VP-5 will add

A read-only Virtual Person API exposing identity, current situation, decisions and this history, with
the same origin, absence and disclosure semantics — the concrete surface the Ask MERIDIAN interface
(VP-6) will read.
