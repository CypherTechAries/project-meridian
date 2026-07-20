# VP-2 — the current-situation model

VP-2 gives a fictional person a **changing current situation**: what they are trying to achieve, what
they are responsible for, what pressure they are under, and what limits their choices — plus a
deterministic record of what changed those conditions.

It is the first milestone where a Virtual Person's situation moves. It is deliberately **not** the
milestone where the person decides anything.

Code: `scaffold/backend/app/simulation/person/current_state.py`,
`vp2_fixtures.py` · Tests: `tests/test_virtual_person_vp2.py`

## The four things VP-2 models

**A goal** is what the person is trying to achieve *now* — "publish an accurate report". It is a
current objective, not a personality trait, not a moral judgement, not proof of what they will do.

**A responsibility** is a declared obligation — "meet the broadcaster's verification standard", owed
to someone or some process. It must be authored or activated; it is never auto-derived from a job
title.

**A pressure** is an active circumstance with a named source — "an approaching publication deadline".
It always points at the event or obligation it comes from.

**A constraint** is a current limitation — "insufficient corroboration to report as established".
VP-2 *records* constraints; it does not yet let them remove options.

## How the situation changes

A small, typed set of declared events changes state: activate/change/satisfy a goal, activate/change
a responsibility, activate/change/resolve a pressure, activate/resolve a constraint. Unrestricted
prose is never an authoritative input. Every event names the item it targets, a declared magnitude
or status change, a reason and an origin.

`apply_events(situation, events, rule_version)` is a **pure function**: the same situation, the same
ordered events and the same rule version always produce the same result and the same trace. Events
are applied in a declared stable order — tick, then event order, then event id — never dictionary or
filesystem order. No language model, no randomness, no clock, no network, no hidden global state.

Every event produces a **trace entry**, including one that changed nothing: **no-change is a real
result**, recorded with a reason, not represented by a missing entry. The trace keeps the value's
*fixture* origin separate from the *engine* decision that acted (or chose not to act) on it.

### Example

> An approaching deadline increases the journalist's deadline pressure from moderate to high.

That is all it means. **It does not mean the journalist is generally anxious**, it says nothing about
her as a person, and **it does not decide what she will do**.

## Why this is not a personality model

Every value is current-situation data grounded in a declared fixture, a declared event or a
deterministic transition. Nothing is inferred from role, biography, portrait, education, wealth,
socioeconomic description, apparent age, gender presentation or occupation. A pressure is an active
circumstance, never a diagnosis; a goal is what someone wants now, never "what this type of person
always wants".

**Current pressure is not susceptibility.** "This deadline pressure is high" is a reading of one
named pressure. It is never combined with anything into a person-wide score, and there is no
susceptibility, persuadability, resilience, stability, vulnerability, motivation, risk or influence
field anywhere. Numbers are bounded [0,1], contextual to one named item, and shown as plain-language
bands (low / moderate / high) — a measure of the circumstance, never of the person.

## Why no decision is selected yet

The kernel's inputs are *only* the current state, the ordered events and the rule version. Its
signature structurally excludes name, portrait, biography, life stage, education, occupation,
socioeconomic description, organisation prestige and every intelligence/competence/personality field
— a person cannot be profiled through it, and two different people given the same situation and
events get the same result. The reserved selected-action field stays `NOT_MODELLED`. Reducing a
pressure never "causes" a decision, because VP-2 makes no decision at all.

## What VP-3 will add

VP-3 implements deterministic **action selection and the decision trace**: available actions, how
constraints remove options, which action is selected and why. It reads only the engine-state
references defined in VP-1's `DecisionInputs` — identity still cannot reach it.

## Boundaries held

No action selection · no relationship effects · no information/belief history (VP-4) · no API route
(VP-5, `main.py` untouched) · no portrait or image work · belief update rule, read-model API, VP-1
schema, fictional registry, B5 controls and the scenario-id disclosure all unchanged · the packaged
belief snapshot is not connected to authoritative run state.
