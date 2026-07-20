# VP-3 — deterministic action selection and decision trace

VP-3 gives a Virtual Person a **decision**: given a declared current situation and a declared set of
fictional options, the engine selects one available option and explains why. It **selects; it never
executes.**

Code: `scaffold/backend/app/simulation/person/decision.py`, `vp3_decisions.py` ·
Tests: `tests/test_virtual_person_vp3.py`

## Claim boundary

> Virtual Person Decision Rule v0.1 is a deterministic mechanism for comparing declared fictional
> options against declared goals, responsibilities, pressures and constraints. It is not a complete
> model or prediction of human decision-making.

A selected option means *"the declared rule ranked this option highest under these declared inputs."*
It does not mean the option is objectively best, that every similar person would choose it, or
anything about intelligence, competence, morality, strategy or free will. Both the claim boundary and
a "what this is not" list travel inside every result.

## What an option is

An `ActionOption` is authored fictional content — a label, a description, and **declared
contributions**: how it aligns with each named goal, each named responsibility, how it responds to
each named pressure, and which constraints it requires. Those contributions are **comparison inputs,
not predicted consequences**. An option is never an executable instruction, and unrestricted prose is
never accepted as one.

## How constraints affect availability

Availability is decided **before** ranking. If an option declares it is blocked while a constraint is
active, and that constraint is active, the option is **UNAVAILABLE** — it is not scored, and
unavailable is never represented as a score of zero. If every option is unavailable, the result is
`NO_AVAILABLE_ACTION` with no selected action and a trace explaining each block; the engine never
invents a fallback or quietly picks the least-blocked option.

Soft constraints, where an option declares an explicit bounded `soft_penalty`, subtract that named,
visible penalty from the score. Hard blocking and soft penalty are mutually exclusive on one
requirement.

## How the rule compares available options

One small versioned formula (`vp3-decision-rule-v0.1`), shown in the trace:

```
goal component          = Σ (goal.priority        × declared option alignment)
responsibility component= Σ (responsibility.urgency × declared option alignment)
pressure component      = Σ (pressure.intensity    × declared option response)
soft-penalty total      = Σ (declared soft penalty for active soft constraints)
total                   = goal + responsibility + pressure − soft-penalty
```

Only **declared** contributions are summed; a contribution the option does not declare is absent, not
a fabricated zero. Nothing is multiplied by role, prestige, education, occupation, wealth,
intelligence, competence, personality, appearance or biography — none of which can reach the kernel.

## What an option score means, and does not

It is local to one decision, comparative only within that option set, and derived from explicit
contributions. It is **not** a probability of choosing, a likelihood of success, a moral or policy
judgement, a measure of intelligence or competence, or an overall person score. Raw scores are never
compared across unrelated decisions, and there is no permanent person-wide decision score.

## Ties

Deterministic and visible: compare totals; on an exact tie, select the **lowest `action_id`**
(documented, stable); record that a tie occurred and which rule broke it. Never input order,
dictionary order, filesystem order or randomness.

## Why selection is not execution

`execution_status` is always `NOT_EXECUTED`, enforced by the result model. VP-3 applies no world
state, belief, relationship or run consequence, emits no event, and reduces no pressure as a "result"
of a decision. Reducing a pressure never causes a decision, because VP-3 makes no change to anything
but the returned decision record.

## The input boundary, and a reported gap

VP-1 defined `DecisionInputs` carrying string *refs*. The formula needs the magnitudes those refs
point at, plus each option's contributions. Rather than reach around the boundary by passing a whole
`VirtualPerson`, VP-3 takes a `DecisionRequest` carrying the concrete VP-2 engine-state items (Goals,
Responsibilities, Pressures, Constraints) and the ActionOptions. **It has no field for name,
portrait, biography, role, occupation, education, socioeconomic description, life stage, community or
prestige.** `subject_ref` exists only to stamp the returned record and is never read by scoring — two
different people with identical requests get identical results. VP-1's `DecisionInputs` is left
unchanged.

## Example

> The journalist has a deadline, but publishing immediately is unavailable because the required
> corroboration is missing. The rule selects seeking another source because it best supports the
> declared accuracy goal and verification responsibility. Nothing is published or executed.

The explanation is generated deterministically from the structured result, uses at most three
reasons, and never references personality, profession-as-capability, intelligence or emotion.

## Boundaries held

No execution or consequences · no relationship effects · no history (VP-4) · no API route (VP-5,
`main.py` untouched) · no LLM, dialogue or UI · no people ranking, audience selection, persuasion
optimisation or real-person target. Belief update rule, read-model API, VP-1 schema, VP-2
transitions, fictional registry, B5 controls and the scenario-id disclosure are unchanged; the
packaged belief snapshot is not connected to authoritative run state (issue #16 remains open).

## What VP-4 will add

Ordered relationship, information and belief histories — turning a single decision record into an
inspectable sequence, without describing one decision as a behavioural pattern.
