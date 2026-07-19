# PERSON-MODEL

> # ⚠ SPECIFICATION — NOT IMPLEMENTED
>
> **Nothing in this document exists in code.** No field, table, mechanism, test, portrait
> pipeline or generation step described here has been built. Every statement about behaviour is
> written in the future or imperative mood deliberately: it describes what a future architecture
> **must** do, never what MERIDIAN does.
>
> MERIDIAN's defining defect, and the reason its repository is private, is documentation that
> claimed properties the code did not have. A reader must not be able to mistake any sentence
> below for a description of working software. Where this document refers to something that
> **does** exist today, it says so explicitly and cites `file:line`.

**Status:** DRAFT — pending owner review.
**Date:** 18 July 2026.
**Amended:** 19 July 2026 — founder ownership rulings **1A** (observation), **1B** (role authority)
and **1C** (faction alignment) applied from the consuming side. Nothing is deleted: superseded
statements are marked superseded and dated, and the text they replaced is retained on the record.
The amendment record is at Part 3.0a, immediately below the mechanism register.
**Derived from:** [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md). That
record is the authority. Where this document and the source record disagree, the source record is
right and this document is wrong. **One carve-out, stated so this rule does not void Part 7:** where
the source record and the **founder decision of 18 July 2026 on dual-use influence targeting (B5)**
differ *on the subject of that decision*, the decision governs, because it is the later instruction.
Part 7 applies that decision — including a not-permitted identity list wider than the source
record's — on that basis and on no other. The carve-out is confined to the decision's own subject;
everywhere else the source record governs without qualification.

**Disposition: BACKLOG. This work does not interrupt Phase 0 remediation.** The founder was
explicit ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):5-6, :340-341;
[`../../HANDOFF.md`](../../HANDOFF.md) § Backlog (`:107-120`)) that the world model must be captured before the
replacement simulation architecture is designed, and equally explicit that capturing it must not
displace P0.1–P0.8. Nothing in this document is a proposal to begin work now. It is a specification
to be held until the foundation is honest and testable.

**Terminology.** Public-facing language is **simulated society**. "Synthetic society" and
"artificial society" are not used, because they imply the world is merely generated content.
Internal and technical language retains **synthetic population**, **synthetic agent** and
**synthetic data**, which remain correct.

---

## Part 0 — Plain English

### What this document is for

MERIDIAN is meant to model a fictional society whose people behave for reasons. A defence minister
should oppose an operation because of who she is, where she came from, who she owes, what she has
survived and what she currently fears — and the system should be able to show its working.

The obvious way to build that is to write rich biographies for everyone. That is also the way it
fails. A biography that reads beautifully and changes nothing is **fake depth**: it makes the
product look deep in a demonstration and adds nothing to the simulation. The founder named this as
the single largest risk to the whole idea
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):241-254).

So this document is not primarily a list of things a person has. It is a list of things a person
has **paired with the specific machinery each one is required to drive**. Any attribute that cannot
be paired with machinery is either labelled PRESENTATION-ONLY and forbidden from touching the
simulation, or struck out entirely.

This project has already proved to itself why that discipline matters. The cohort field
`represents_population` is declared in the schema, is described in two READMEs as the thing that
weights population influence, and is read by no code at all. Because nothing read it, nobody
noticed that one demo cohort's population was wrong by a factor of about sixty-three
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.10). An attribute
that feeds no mechanism produces no error when it is wrong. That is the empirical case for the rule
this document is built around.

### The four things this document decides

1. **Every person attribute names the mechanism it feeds.** If it feeds nothing, it is presentation
   or it is deleted. There is a test obligation attached, so this cannot quietly rot.
2. **Biography shifts the odds; it never picks the answer.** A religious person must not have a
   political behaviour attached to them. A wealthy person must not be automatically calm. The
   document specifies the arithmetic that makes this structurally impossible rather than merely
   promising it as good practice.
3. **A person's changing state is separated from their fixed history**, with a stated rule for what
   may change every tick and what may change only when something actually happens to them.
4. **Portraits are decoration with rules.** They must be stable, deterministic, provenance-tagged
   and clearly fictional — and they must never influence a simulation outcome.

### What a reader should not take away

That any of this is close. The prerequisites listed in Part 1 are not met, and several are not yet
even scheduled. This document is a target, written down while the reasoning is fresh.

---

## Part 1 — Where this attaches, and what is in the way

### 1.1 What exists today

This section describes real code. Everything outside it does not exist.

| Structure | Location | What it actually is |
|---|---|---|
| `MicroAgent` | `scaffold/backend/app/simulation/schemas/agent_schema.py:154-184` | The only individual-actor record in the project. It has `agent_id`, `role`, free-form `beliefs`, four traits, three resources and a valence map. It has no name, no age, no birthplace, no identity, no family, no history and no health. |
| `AgentTraits` | `.../agent_schema.py:122-130` | Four scalars: `risk_tolerance`, `status_seeking`, `institutional_trust`, `corruption_susceptibility`. |
| `AgentResources` | `.../agent_schema.py:133-140` | Three scalars: `budget_control_usd_m`, `political_capital`, `personal_network_reach`. |
| `AgentMemory` | `.../agent_schema.py:143-151` | `recent_events` (a list of event ids) and `decay_rate`. Memory is modelled as decay only. |
| `MicroAgent.relationships` | `.../agent_schema.py:175-177` | `dict[str, float]` — one signed scalar per counterpart. |
| `MicroAgent.biography_ref` | `.../agent_schema.py:166-168` | An optional path to a prose biography. Set once, to `"bios/oduya.md"`, at `scaffold/scenarios/kestral-strait.json:268`. That file does not exist anywhere in the repository. |
| `MicroAgent.constraints` | `.../agent_schema.py:181-183` | Documented as "Hard legal/procedural constraints". Verified causally inert: a 40-tick run with and without constraints produces the identical state hash `1af9170525db` ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) §3). |
| `InstitutionalAgent` | `scaffold/backend/app/simulation/agents/institutional_agent.py:18-41` | The runtime wrapper. One role produces one action proposal per tick, from a three-key context stub. |
| `ActionProposal` | `.../agent_schema.py:374-393` | The LLM boundary object. The determinism boundary it enforces is real today: `llm_gateway.py:35` imports only this type and no state object, and `_validate_and_price` (`engine.py:128-130`) never reads `proposal.parameters` or `proposal.confidence` ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §3). Note that its own docstring (`:377-379`) additionally claims the engine "runs a legality/feasibility check", which audit §5.4 records as false — `_validate_and_price` (`engine.py:121-130`) is a dict lookup with no legality check, no feasibility check, no resource debit and no scaling — and that the gateway is a stub making no model call (`llm_gateway.py:1-4`). This specification depends only on the boundary property, not on the docstring. |

Six institutional agents exist in the demo scenario. Their identifiers carry surnames —
`head-of-government-varo` (`kestral-strait.json:243`), `min-defence-oduya` (`:266`),
`min-finance-serel` (`:298`), `min-foreign-affairs-lind` (`:320`), `intel-lead-navarro` (`:345`),
`strat-comms-adeyemi` (`:366`) — but there is no person record behind any of them. Today a person's
identity is encoded in a string primary key. That cannot satisfy the requirement that identity and
history remain stable once materialised
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):236-237).

None of the person-level fields specified in Part 3 have any equivalent today.

### 1.2 Person and role are currently one record. They must be separated

`MicroAgent` fuses two different things: the **person** (who they are, what they have lived
through, what they are like) and the **role occupancy** (the institutional seat they hold, the
authority it carries, the information it grants, the constraints it imposes).

This specification separates them. A person must be able to lose a role, gain a role, hold two
roles, or be replaced in a role while their identity, history and relationships persist unchanged.
Role occupancy must be a time-bounded association between a person entity and an organisation
entity, owned by [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md). **Confirmed 19 July 2026 by
founder ruling 1B**, which assigns that document roles and offices, the authority attached to a role,
jurisdiction, delegation, appointment and removal, acting authority, conflict between formal and
practical authority, command chains, and authority expiry and suspension. This document may
reference a person's current role; it must not own the mechanism (Part 3.0a).

**This is an owner decision, not a decision this document may take.** The two candidate routes —
person as a new first-class entity, versus extending `MicroAgent` in place — have materially
different migration costs and give different answers to "what happens when a minister is sacked".
Recorded in Part 8.

### 1.3 Prerequisites that are not met

| Prerequisite | State | Consequence for this document |
|---|---|---|
| **Deterministic randomness isolation** (called "named RNG substreams" elsewhere in this document; the mechanism is not yet chosen) | **Does not exist. Owned by P0.4A**, a Phase 0 workstream created by founder decision of 18 July 2026 and placed between P0.4 and P0.5 ([`../delivery/PHASE-0-REMEDIATION-PLAN.md`](../delivery/PHASE-0-REMEDIATION-PLAN.md) §P0.4A). Isolation is required by subsystem, entity, relationship or interaction, purpose, and tick or event context — **per-entity streams alone are insufficient**, so this document's per-person framing understates the requirement. A single shared `random.Random` is created at `scaffold/backend/app/simulation/engine.py:83`. [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) §6 demonstrated that adding one draw in one subsystem shifts every later draw everywhere: adding a grievance to a single cohort moved `shipping_throughput_pct_of_baseline` from `0.6080711379477878` to `0.5973599412373322`. | **Hard blocker on two things this document specifies.** Deterministic profile generation and portrait generation both consume draws. On a shared stream, materialising a person would silently perturb national indicators — national numbers would move because a player opened a dossier. And an entity generated at a different tick would receive a different biography, breaking the stable-identity requirement outright. Additionally, the single-RNG design is a **recorded architecture decision (ADR-007)**, so substreams require superseding an ADR, which [`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`) reserves to the owner. |
| **P0.4 — authoritative-state contract** | Not started. Today the contract is implicitly macro-only: `macro_snapshot()` returns `MacroState.model_dump()` and nothing else (`scaffold/backend/app/simulation/agents/macro_state.py:49-51`). | The person record's **authoritative reality** view cannot be defined until P0.4 says whether micro-tier state is authoritative or derived. This document takes the position that only authoritative reality is authoritative state and the other three views are derived — but that is a claim *about* the P0.4 contract, not a substitute for it. P0.4 must decide. |
| **P0.6 — event, snapshot, replay foundations** | Not started. `Event` (`.../agent_schema.py:211-229`) is never instantiated; `engine.py:165-173` appends raw unvalidated dicts; `causal_parents` (`:224`) is assigned nowhere; no RNG state is ever captured; nothing is persisted at all. | Event-sourced life history and the entity timeline are **unbuildable** before P0.6. Every "recorded event" reference in this document is a forward reference to machinery P0.6 must deliver. |
| **P0.7 — simulation time and horizon** | Not started. P0.7 requires time and horizon to be defined **before** saturation is touched, and forbids arbitrary mean reversion ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.7 (`:89`)). | **"Per tick" currently has no defined meaning to specify against.** The whole per-tick/per-event cadence split in Part 5.2 presupposes tick semantics P0.7 has not settled, and every per-tick rule specified there — stress decaying to a baseline, confidence decaying to a baseline, age-conditioned health drift — is mean reversion. Those rules must be re-derived once P0.7 lands, not implemented as written. Part 5.2 carries this warning at its head. |
| **P0.5 — cross-tier causal channels** | Not started. | The influence a person exerts on aggregate outcomes (M11) sits on top of the aggregation channel P0.5 delivers. This document must not redesign it. See [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md). |
| **B5 / P0.8 — dual-use targeting** | **DECIDED** (founder decision, 18 July 2026). **Not an open decision, and must not be recorded as one.** The eight controls it requires are, however, **entirely unbuilt.** | The decision converts B5 from a policy question into an engineering prerequisite: it clears only when technical enforcement is implemented and verified, because disclosure and acceptable-use wording were ruled **supplementary**. The person record still refines targetable audience attributes from five aggregate cohorts down to named individuals with portraits, so this document sits **inside** the envelope the decision fixes rather than waiting on it. Part 7 states the controls and the permitted / not-permitted line. |
| **Any auth or role layer** | Does not exist ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §7). | "What the player's role knows about this person" has nothing to resolve against today. **Amended 19 July 2026 (ruling 1A).** The superseded text read: "Owned by [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md)." That single assignment conflated four separable things, which now separate as: what an entity is in a position to observe at all — [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md); view production — [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2; presentation of the resulting dossier — [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md); and **which human player may open which record, which is the future access and role-authorisation layer that no document specifies and no code implements** ([`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §4). The prerequisite is therefore *more* unmet than this row previously implied: the layer is not merely unbuilt, it is unowned. Recorded as open question 13. |
| **Schema mirror generator** | Does not exist. Nine JSON Schema mirrors under `scaffold/schemas/` and the SQLAlchemy models in `scaffold/backend/app/db/models.py` are hand-maintained, with no generator and no sync test ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.13). | A person record of this size would need a third hand-maintained copy. This document records the cost; whether to build the generator first is an owner sequencing decision. |
| **Mesa as the agent substrate** | Open owner decision ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §8 decision 3). | The person record is specified **substrate-neutral**: it is a data record with named mechanisms operating on it, not a subclass of any framework's agent type. Assuming `mesa.Agent` would prejudge an open decision. |

**Ordering.** Named RNG substreams sit underneath everything. P0.4 precedes P0.6. P0.6 precedes
event-sourced life history. **P0.7 precedes every per-tick rule in Part 5.2, because until tick
semantics and horizon exist there is nothing for "per tick" to mean and any equilibrium chosen is
the arbitrary mean reversion P0.7 forbids.** P0.5 precedes population-weighted influence. B5 no
longer *gates* the sensitive-identity fields by leaving their permitted detail undecided — it
**bounds** them: the permitted / not-permitted line in Part 7 is now fixed, and the eight controls
must be built and verified before any of this may be published. None of this is a reason to start
building; it is a reason to write the specification carefully now and hold it.

---

## Part 2 — The two rules that govern everything below

### 2.1 The causal-value rule (the fake-depth guard)

> **Rule P-1.** Every attribute of a person record must name at least one mechanism that reads it
> and changes simulation behaviour as a result. An attribute that names no such mechanism must be
> labelled PRESENTATION-ONLY. A PRESENTATION-ONLY attribute must never be read by any mechanism
> that can change authoritative state.

> **Rule P-1a (the null-effect obligation).** Rule P-1's prohibition must be **tested, not trusted.**
> For every PRESENTATION-ONLY attribute a *null-effect test* must exist that perturbs only that
> attribute, holds seed and world state fixed, and asserts the run's state hash is **byte-identical**.
> Without it, the prohibition side of the guard is enforced by reviewer diligence alone — and this
> project's own evidence is that declarations no test enforces rot silently.
>
> This is directly buildable on a method the project has already used: A3 §3 proved `constraints`
> causally inert by showing the identical 40-tick hash `1af9170525db` with and without it
> ([`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) §3). That is
> exactly this test, performed by hand once. It must become a suite.
>
> The null-effect suite must run in CI alongside Rule P-4. **A PRESENTATION-ONLY attribute whose
> null-effect test starts failing must fail the build**, because that means a mechanism has begun
> reading it. It must never be silently reclassified as mapped — reclassification requires the
> attribute to earn a named mechanism and a Rule P-3 sensitivity test on the record.
>
> This applies with particular force to portraits, where Part 6.1 states "no portrait may influence
> any simulation outcome, ever", and to the conditional attributes in 9.2 whose free-text variants
> must have no reader. Today, a contributor wiring `identity.name` or a portrait field into a
> mechanism would break nothing and fail no build.

> **Rule P-2.** An attribute that is neither mapped to a mechanism nor justified as
> PRESENTATION-ONLY must be **struck, not deferred.** "We will wire it up later" is how
> `represents_population` came to sit in the schema, be described in two READMEs, and hide a 63×
> data error indefinitely ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
> §5.10).

> **Rule P-3 (the test obligation).** For every attribute mapped to a mechanism, a **sensitivity
> test** must exist that perturbs only that attribute and asserts that at least one recorded
> outcome changes. If such a test cannot be written, the attribute has no causal value and Rule P-2
> applies. There are no invariant tests of any kind in the project today
> ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §6.34), so this
> obligation is entirely new work.

> **Rule P-4 (drift guard).** Both suites must run in CI: the Rule P-3 sensitivity tests for mapped
> attributes, and the Rule P-1a null-effect tests for PRESENTATION-ONLY attributes. An attribute
> whose sensitivity test starts passing vacuously — because the mechanism that reads it was removed
> — must fail the build, not degrade silently. A PRESENTATION-ONLY attribute whose null-effect test
> starts failing must likewise fail the build, because a mechanism has begun reading something
> forbidden to it. The two suites guard opposite directions of the same rule, and only running both
> makes Rule P-1 enforceable.

Rule P-3 is what distinguishes this specification from a wish list. Every row in Part 3's tables
carries an implied test, and the "if absent" column exists so the test author knows what the null
behaviour is supposed to be.

### 2.2 The probabilistic-influence rule, and how it is enforced

The founder's requirement
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):87-91):

> A person's biography should influence their behaviour, but it should not mechanically determine
> it. […] Identity changes probabilities, social connections and lived experience — it should not
> become a stereotype switch.

Asserting this as a principle is not enough. It must be structurally impossible to violate.
Six enforcement mechanisms are specified.

#### E-1. Option-set generation must be identity-blind at decision time

At every decision point, the set of options a person may consider must be produced by
**M2 FEASIBILITY-GATE**. M2's read set must be a **closed whitelist**, and nothing outside it may be
consulted when a decision point is evaluated:

```text
M2 may read, and may read nothing else:
    capabilities.*                       # what the person is recorded as able to do
    state.current_role  → M13 authority  # the powers of the seat currently held
    state.available_resources            # what is currently affordable
    state.health, state.fatigue          # physical possibility
    state.location                       # physical reachability
    state.knowledge                      # an option unknown to the person is not available
    legal_status.*                       # scenario-authored, enumerable law (see below)
    world_state                          # physical and situational possibility

M2 must NOT read, at a decision point:
    identity.*        life_history.*        psychology.*
```

Every entry on the whitelist is a fact about **what is presently possible for this person**, not
about who they are or where they came from. `state.knowledge` is included because an option a person
does not know exists is genuinely unavailable to them; note that knowledge is itself downstream of
M3 exposure, which identity *does* legitimately shape — a further instance of the transitive path
E-1c makes explicit rather than denying.

> **Amended 19 July 2026 (rulings 1A and 1B).** Two whitelist entries now read against mechanisms
> owned elsewhere, and the whitelist is unchanged by that. `state.current_role → M13 authority` is a
> read of a **time-bounded reference** to a role-occupancy record owned by
> [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md), which ruling 1B confirms as the owner of role
> authority; M2 reads the powers the seat presently carries, never a mechanism specified here.
> `state.knowledge` is populated from `Observation` records whose sole writer is `M-OBS-ACQ`, owned by
> [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md), and whose consumption
> is owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). Neither ruling
> loosens E-1: the whitelist is closed, and M2 still may not read `identity.*`, `life_history.*` or
> `psychology.*` at a decision point. What changed is only which document must specify the two
> whitelist entries — and neither is specified yet.

Identity, history and psychology may then only **reweight** options that M2 has already admitted.
They may never add an option and never remove one. This makes "religion X ⇒ always chooses Y"
inexpressible: religion cannot reach the branch structure at all.

**Biography reaches feasibility only by having been recorded as a capability or a legal-status
fact.** Life history must not be read by M2 directly. It must reach M2 only through a materialised,
dated, event-referenced record that M2 then reads as a present fact:

| Biography fact | Must reach M2 as | Not as |
|---|---|---|
| Education and qualification | `capabilities.expertise[].credential_ref` | `life_history.education[]` |
| Military or public service | `capabilities.security_clearance` | `life_history.service_record` |
| Criminal or disciplinary finding | `legal_status.disqualifications[]`, each with an originating event reference | `life_history.criminal_or_disciplinary[]` |
| Prior employment and sector experience | `capabilities.expertise[]` | `life_history.employment_history[]` |
| Political involvement | Nothing in M2. It is a weighting input to M14/M6/M1 only. | — |
| Family wealth and class | Nothing in M2. It is a weight on capability *acquisition* over time, never a gate. | — |
| Immediate objectives | Nothing in M2. A want is not a permission. | — |

**The `legal_status` group.** M2 needs somewhere to read lawful eligibility from without reading
identity. `legal_status` is that place: a small, scenario-authored, enumerable, auditable record of
legal facts about a person — citizenship and residency status, held clearances, formal
disqualifications, licence and office eligibility. The governing rule:

> **Rule E-1a.** Every `legal_status` entry must be scenario-authored law: enumerable, inspectable,
> attributable to a stated rule of the fictional legal system, and carrying the event that
> established it. No `legal_status` entry may be keyed on ethnic, cultural or religious identity.

**Citizenship and nationality are the one hard case, and this document does not settle it.**
Nationality is named by the source record
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):300) as a sensitive
identity attribute, and E-3 therefore forbids it a *bounded weight* in `score(o)`. Yet legal systems
really do condition office, clearance and asset ownership on citizenship, and a model that cannot
express that cannot express a dual-national minister — which is one of the more interesting cases
the product exists to produce. The result is an inconsistency this document must not resolve on its
own authority: the weaker use is forbidden while the stronger use, deleting options outright, would
be permitted. **Recorded as an open question in Part 8.** Until the owner decides, the conservative
default applies: a citizenship-conditioned gate must exist only as an explicit `legal_status` entry
derived from a stated scenario law, never as M2 reading `identity.citizenship` directly.

> **Invariant E-1b.** No attribute subject to E-3 — ethnicity, religion, nationality, class, gender
> or language — may reduce the cardinality of the feasible set `O` **at a decision point**.
> Sensitive identity may change the *probability* of an option under E-2's bounds; it may never
> remove the option. This invariant is in scope for the E-4 lint.

**E-1c. Identity-blind at decision time is not identity-blind over a lifetime, and the document must
not pretend otherwise.** E-3 blesses the chain `ethnic_identity → M17 DISCRIMINATION-EXPOSURE →
recorded life events`. M17's outputs are exclusion and restriction events — education not completed,
clearance refused, access withdrawn — and those events change **capabilities**, which are M2's
primary input. Sensitive identity therefore *does* reach the option set transitively, along a path
this specification deliberately permits.

That path is not a defect. It is the founder's requirement: "historical exclusion; unequal access to
education" ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):311-313) is
precisely a model in which identity has, over a life, changed what a person can do. A model that
forbade it could not represent discrimination at all. What would be a defect is claiming the path
does not exist, because then the E-4 lint would pass a build in which identity systematically
removes options and no one would be looking.

The claim this document makes is therefore the narrower and true one:

> **M2 must not consult identity or life-history fields when evaluating a decision point.**
> Historical, identity-driven differences in *accumulated capability* are permitted and required.

Admitting the path creates an audit obligation, which is the price of admitting it:

> **Rule E-1d (gate-refusal provenance).** Every option M2 removes must record the specific
> capability or `legal_status` record that caused the removal. Where that record originated in an
> M17 event, the full chain — identity → M17 event → capability change → gate refusal — must be
> retrievable. Modelled historical exclusion and an unintended identity gate look identical in
> aggregate; only the chain distinguishes them, so the chain must be inspectable rather than
> assumed away.

#### E-2. Composition is additive in log-odds, over many bounded terms

Weighting must be specified as a sum of small contributions, never a lookup that selects a branch.

```text
For each option o in the feasible set O (produced by M2, identity-blind):

    score(o) = base_utility(o, world_state)
             + Σ_a  w(a, o)            # attribute contributions
             + Σ_e  r(e, o)            # recalled-experience contributions, via M8
             + Σ_t  n(t, o)            # relationship/obligation contributions, via M6/M7/M16
             + pressure_term(o)        # via M9

    P(o) = softmax over all o in O of ( score(o) / temperature )
```

Constraints that must hold and must be tested:

- **Bounded term.** `|w(a, o)| ≤ λ_max` for every attribute `a` and option `o`, with `λ_max`
  declared in the rule pack, not in code. No single attribute may dominate the sum.
- **Additive only.** No term may multiply another term to zero, and no term may be `-∞`. Vetoes are
  the exclusive business of M2, which is identity-blind.
- **Full support.** `P(o) > ε` for every `o ∈ O`, with `ε` declared. Every feasible option must
  retain non-zero probability under every combination of attribute values. This is the formal
  statement of "not a stereotype switch", and it is a testable invariant.

#### E-3. The indirection rule for sensitive identity

Ethnicity, religion, nationality, class, gender and language must **never appear as a term `w(a, o)`
in any decision score.** They may enter the simulation only through intermediate social variables:

```text
permitted:    religious_identity → M6 TIE-FORMATION      → network composition → M3 exposure → M5 belief → M1 decision
permitted:    ethnic_identity    → M17 DISCRIMINATION-EXPOSURE → recorded life events → M8 recall → M1 decision
permitted:    language           → M19 LANGUAGE-ACCESS   → which channels are intelligible → M3 exposure

forbidden:    religious_identity → M1 decision weight     (direct term)
forbidden:    ethnic_identity    → any capability, trait, competence or morality field
forbidden:    any sensitive identity → state.loyalty / psychology.loyalty seed
forbidden:    any sensitive identity → psychology.attitude_to_violence
forbidden:    any sensitive identity → psychology.susceptibility_to_pressure,
                                       or any other manipulability or persuadability term
forbidden:    any sensitive identity → an optimisation criterion for persuasion or manipulation
```

This is the mechanical form of the founder's design rule
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):305-306): sensitive
identity affects social experience, networks, exposure, discrimination, solidarity and cultural
interpretation — never inherent competence, morality or intelligence.

**E-3a. The indirection layer must itself be bounded.** E-2 bounds every attribute's decision
contribution at `λ_max`; E-5 bounds the residual. M17 is the compulsory channel through which *all*
sensitive identity reaches behaviour, and left unbounded it is where the stereotype switch would
reappear one layer below the guard: the option set stays formally open while the person's entire
experience history is determined by their ethnicity. Bounding only the visible path and leaving the
laundering path open would be a guard in name only.

> **Rule E-3a.** M17's identity-conditioned rate multipliers must be **bounded, scenario-authored,
> versioned and reviewable**. The bound must be declared in the rule pack, not in code, exactly as
> `λ_max` is. **No identity value may drive any exclusion-event category's rate to a certainty or to
> zero** — this is E-2's full-support principle applied at the event-generation layer rather than
> only at the decision layer. An identity that guarantees an experience is a stereotype switch with
> a delay.

M17's rate table is itself an attribute of the model and is subject to **Rule P-3**: a sensitivity
test must exist over the rate table, and it must be run and reported as part of the bias suite. The
numeric bound, its failing threshold and its review cadence are owned by
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) — recorded
here explicitly so the bound is not left ownerless between the two documents, which is how it would
otherwise go missing.

**E-3b. The not-permitted list is wider than the source record's, and the last four forbidden lines
in E-3 are why.** The settled B5 decision (Part 7) states the line as: identity must never act as an
inherent **competence, morality, loyalty, violence or manipulability** coefficient. That is three
categories more than the source record enumerates, and each of the three has a named landing site in
this document — `state.loyalty` and its `psychology.loyalty` seed (3.4, 3.7),
`psychology.attitude_to_violence` (3.4), and `psychology.susceptibility_to_pressure` (3.4), whose
cohort-level analogue `InfluenceSusceptibility` (`.../agent_schema.py:72-77`) is half of the audit's
dual-use finding. Without those lines a build could satisfy E-3 as originally written while keying
persuadability on ethnicity, which is precisely the construction control B5-5 prohibits. **The E-4
lint must cover all six forbidden lines, not the first two, and E-3a's bound applies to any
identity-conditioned rate feeding them.**

**The permitted list is also wider, and it needs no new path.** The decision names lived experience,
relationships, discrimination, **institutional access**, **media exposure** and cultural
interpretation as permitted effects. Institutional access and media exposure are already reachable
under this specification, and must stay reachable **only** by the routes already specified: identity
→ M17 → recorded exclusion or restriction events → `capabilities.institutional_access` (the E-1c
chain, with its Rule E-1d provenance obligation), and identity → M19/M6 → reachable channel set →
M3. Neither may become a direct term. Cultural interpretation remains **struck** under Rule P-2
(3.2) for want of a mechanism, not for want of permission; open question 6b covers it.

#### E-4. A static rule: no conditionals on identity in decision paths

Sensitive identity fields must be forbidden from appearing in any conditional expression on a
decision path. They may appear only as arguments to a declared, bounded, reviewable weight table
that feeds the permitted intermediate mechanisms in E-3. This must be enforced by a lint check in
CI, not by reviewer diligence.

#### E-5. The swap tests — two of them, with different intents

A single swap test cannot work, and specifying one would give false assurance. The point in a
person's life at which the sensitive value is varied changes the test completely, and both readings
of a single test are degenerate:

- Swapped **at the decision point** with all other state held fixed, the answer is exactly zero by
  construction, because E-3 already forbids direct terms. The test would pass any build, including
  one in which identity had determined everything upstream.
- Swapped **at materialisation** and re-run, the distribution *must* shift, because M6 network
  composition and M17 exposure rates are specified to differ. A total-variation bound would flag the
  model's intended and founder-required mechanism as bias, and any bound loose enough not to would
  detect nothing.

Two separate tests are therefore specified.

**E-5a. Decision-time invariance.** Swap the sensitive identity value at the decision point only,
holding network, life events, capabilities and world state fixed. **Assert exactly zero change** in
the outcome distribution. This is the direct-term check — the mechanical form of E-3 — and a failure
must be a hard build failure, not a threshold judgement.

**E-5b. Lifetime differential, with mandatory attribution.** Swap at materialisation and re-run.
**Do not bound the magnitude of the shift.** Instead require that it be **fully attributable**: every
unit of divergence must decompose into named contributions from permitted intermediate mechanisms —
M6 tie composition, M17 event rates, M19 channel access — and the **residual, meaning divergence not
attributable to any permitted intermediate mechanism, must be zero**.

> The residual is the bias signal, not the magnitude. A large but fully attributed divergence is the
> model working as specified. A small unattributable one is a leak, and is the more dangerous
> finding of the two.

The residual threshold, the failing criteria, the decomposition method and the reporting format are
owned by [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md);
this document states only that the person model must be built so both tests are runnable, and that
E-5b is unbuildable without the named RNG substreams of Part 1.3 — re-running with one attribute
varied requires that every other subsystem's draw sequence be unchanged, which a shared stream
cannot provide.

#### E-6. The LLM narrates, never authors

Biographies, dossier prose, briefings and in-character conversation must be generated from the
structured record and must never write back to it. This is the CHARTER's determinism boundary
([`../../CHARTER.md`](../../CHARTER.md):37-44, ADR-006) applied to the entity layer.

The existing implementation of that boundary holds in the narrow, verified sense and must be reused
rather than paralleled: `ActionProposal` (`.../agent_schema.py:374-393`) is the only simulation type
the gateway imports (`scaffold/backend/app/simulation/llm_gateway.py:35`), and it carries no
authority to change numbers ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
§3). Two qualifications must be carried with that statement. First, the gateway is a **stub that
makes no model call at all** (`llm_gateway.py:1-4`: "in this scaffold every function returns canned
output"), so the boundary has never been exercised against a real model. Second, the wider claim
that the engine validates legality and feasibility is **false** (audit §5.4). What is reused here is
the structural property — the narrating component cannot write state — not the validation the
docstrings describe. Generated biography text must be treated the same way — an interpretive artefact, logged
separately, never an input to any mechanism in Part 3, and carrying a visible provenance tag at the
interface per [`../../CHARTER.md`](../../CHARTER.md):141.

**Corollary.** If a fact appears in a generated biography and nowhere in the structured record, it
is not true in the simulation and nothing may act on it.

---

## Part 3 — The person record

### 3.0 Mechanism register

Every mapping in the tables below cites one of these. **All twenty were named here on 18 July 2026;
none exists.** As amended on 19 July 2026, **M12 is superseded** and its successors `M-OBS-SURF`,
`M-OBS-ATTR` and `M-OBS-EXP` are specified in
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5; nineteen numbered
mechanisms remain in this register, and none of the successors exists in code either. Mechanisms
marked *(owned elsewhere)* are specified — or, in several cases, only **assigned** — in a sibling
document, and are referenced here only as readers of person attributes. **Ownership is not
specification**, and the amendment record immediately below distinguishes the two, because a
citation to an owned-but-unwritten mechanism is the same defect as a citation to an ownerless one,
merely one step further along.

| ID | Mechanism | What it must do |
|---|---|---|
| **M1** | DECISION-WEIGHTING | Produce a probability distribution over the feasible option set at a decision point, per the composition in E-2. |
| **M2** | FEASIBILITY-GATE | Determine which options exist at all: authority, resources, skills, legality, physical possibility, from the closed read-whitelist in E-1. **Identity-blind at decision time (E-1)** — not identity-blind over a lifetime, and the difference is stated in E-1c. Succeeds the currently inert `constraints` field (`.../agent_schema.py:181-183`). |
| **M3** | INFORMATION-EXPOSURE | Determine which events and claims a person observes, at what fidelity, with what delay. |
| **M4** | SOURCE-CREDIBILITY | Weight how strongly an observed claim updates belief, given who carried it. |
| **M5** | BELIEF-UPDATE | Apply weighted evidence to belief state. *(Owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md).)* |
| **M6** | TIE-FORMATION | Probability that a directed relationship edge forms, and its opening dimension values. *(Owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).)* |
| **M7** | TIE-UPDATE | How an interaction changes an existing directed edge. *(Owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).)* |
| **M8** | EXPERIENCE-RECALL | Select which recorded life events are retrieved when a new event is interpreted, and how strongly they weight. Answers the founder's "which prior experiences shaped the reaction". |
| **M9** | PRESSURE-ACCUMULATION | Accumulate stress, fatigue and financial pressure, and apply their effect on decision quality, volatility and time horizon. |
| **M10** | REACH | Determine the size and composition of the audience a person's utterance reaches. |
| **M11** | INFLUENCE-WEIGHT | Determine a person's contribution to aggregate outcomes, including disproportionate influence via wealth, organisation, position or access. *(Owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md), downstream of P0.5.)* |
| **M12** | OBSERVABILITY — **SUPERSEDED 19 July 2026 (ruling 1A)** | **M12 is superseded.** Its function is now owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5 and split: the observable surface is `M-OBS-SURF`, alias and concealed-identity resolution is `M-OBS-ATTR`, and clearance-gated event observability is `M-OBS-EXP`. M12's clause assigning production of the public profile and the player intelligence profile to [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) is withdrawn: view production is [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2 and presentation is that design document; neither is a simulation mechanism. **The superseded text read:** "Determine what other entities, and the player's role, can learn about this person; produces the public profile and the player intelligence profile. *(Owned by `../design/ENTITY-PROFILE-EXPERIENCE.md`.)*" The identifier `M12` is retired and must not be reissued to a different mechanism. |
| **M13** | ROLE-AUTHORITY | Resolve the legal and institutional powers available through current role occupancy. *(Owned by [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) — **confirmed by founder ruling 1B, 19 July 2026**, which assigns that document roles and offices, authority attached to a role, jurisdiction, delegation, appointment and removal, acting authority, conflict between formal and practical authority, organisational command chains, and authority expiry and suspension.)* **This document may reference a person's current role occupancy; it must not own the mechanism.** Ownership is now settled. Specification is not: see the amendment record below. |
| **M14** | FACTION-ALIGNMENT — **SPLIT 19 July 2026 (ruling 1C)** | Faction definitions, membership rules, formal positions and faction structure are owned by [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md). The **directional, historied person-to-faction alignment and loyalty relationship, and its changing strength**, is owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) (which records the gain at its :15-19). **This document consumes the resulting relationship projection and must not duplicate the mechanism.** Every M14 citation in Parts 3.3–3.7 is therefore a *consumption* citation and confers no ownership here. **The superseded text read:** "Determine which internal faction a person aligns with, and their dissent or defection probability. *(Owned by `ORGANISATION-MODEL.md`.)*" Per-person dissent and defection probability is the one clause of that sentence the split does not unambiguously place — recorded below. |
| **M15** | PROMOTION-SALIENCE | Determine whether a background person becomes eligible for promotion to a named fidelity tier. *(Owned by [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md).)* |
| **M16** | OBLIGATION-LEDGER | Record favours owed and owned as callable obligations with expiry and cost. |
| **M17** | DISCRIMINATION-EXPOSURE | Determine the rate at which a person experiences exclusion, suspicion or restriction events given identity and setting. The mandatory indirection layer for sensitive identity (E-3), and therefore **the mechanism most in need of its own bound — see E-3a.** |
| **M18** | SUCCESSION | Determine what happens to role, obligations, relationships and knowledge when a person exits a role or the simulation. |
| **M19** | LANGUAGE-ACCESS | Determine which channels, documents and conversations are intelligible to a person. |
| **M20** | THREAT-SALIENCE | Determine how strongly a perceived hazard weights into the decision distribution. |

### 3.0a Amendment record — founder ownership rulings, 19 July 2026

Three ownership rulings were taken by the founder on 19 July 2026. This document is a **consumer** of
all three: it holds person-side fields that the mechanisms read, and it must not own the mechanisms.
Nothing below is a decision this document has taken. Superseded text is retained in the register rows
above and in the field tables, marked and dated, because the record of what was previously believed
is itself evidence.

**Ownership is not specification.** Every mechanism named here is now attributed to a document. Not
one of them is specified to a buildable standard, and none exists in code. A citation to an
owned-but-unwritten mechanism is the same defect as a citation to an ownerless one, one step further
along. The distinction is stated in each row below and must not be collapsed.

| Ruling | Subject | Owner after the ruling | State of the specification |
|---|---|---|---|
| **1A** | Observation and evidence emission | [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) (DRAFT, 19 July 2026) | Drafted, not approved, not implemented. |
| **1B** | Role authority (M13) | [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) | Owner settled; mechanism not specified. |
| **1C** | Faction alignment (M14) | Split: structure to [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md), the person-to-faction edge to [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | Owners settled; neither half specified. |

#### Ruling 1A — observation. Every M12 citation in this document is repointed

The previous assignment of M12 OBSERVABILITY to
[`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) was wrong, and the
reason it was wrong is worth stating rather than merely correcting: **a user-interface specification
cannot own a simulation mechanism because it displays that mechanism's output.** Observation
determines what is true of the world's information state; a dossier is a rendering of what
observation has already produced. Assigning the mechanism to the surface that renders it is the same
category error as `biography_ref` — a description standing in for the machinery it describes.

The chain, per the ruling, is: world event → observation opportunity → entity-specific observation →
belief or knowledge update → role-filtered projection → dossier presentation. This document supplies
person-side inputs to the second and third steps and holds the state written by the fourth. It owns
none of them.

The identifier **`M12` is retired**. It must not be reissued. Every citation of it in Parts 3.2–3.7
and Part 9 has been repointed to the successor named below, and each repointed cell carries an
inline supersession note:

| Former M12 use | Successor | Owning document |
|---|---|---|
| What an entity exposes to a given observer class — public identity, publicly stated position, visible role, contact pattern, achievements, reputation evidence base | `M-OBS-SURF` | [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5 |
| Alias non-resolution, concealed identity, mistaken and deliberate misattribution | `M-OBS-ATTR` | as above |
| Clearance-gated event observability | `M-OBS-EXP` | as above |
| Production of the public profile and the player intelligence profile | **No successor mechanism.** View production is [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2; presentation is [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md). Neither is a simulation mechanism, and the clause is withdrawn. | — |

Two consequences for this document specifically. First, `capabilities.security_clearance` (3.5) is
no longer an input to a mechanism this document owns: it is read by `M-OBS-EXP`, which the owning
document names as the sole future reader of `EventVisibility` (`.../agent_schema.py:203-208`).
Second, the four-view model this document sits inside is unchanged, but the boundary is now drawn in
mechanism terms rather than by document: `state.exposure_to_danger` remains authoritative reality,
`state.perceived_threat` remains the entity's self-understanding, and what a *different* entity comes
to hold about this person is produced by `M-OBS-*` and stored by
[`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md), not by any field in Part 3.

**Not resolved by ruling 1A, and recorded rather than assumed away:**

- **M3 INFORMATION-EXPOSURE is now duplicative on its face.** M3 is defined in the register above as
  "determine which events and claims a person observes, at what fidelity, with what delay". That is
  coextensive with `M-OBS-EXP` (which entities are in a position to observe an event) and
  `M-OBS-ACQ` (directness, latency, fidelity, degradation on relay), which ruling 1A assigns
  elsewhere and names as the sole writer of `Observation`. The ruling did not name M3, so **M3 is
  not retired here** — retiring or re-scoping a mechanism this document currently owns is an owner
  decision. Recorded as open question 14. Until it is taken, every M3 citation in Parts 3.2–3.7
  should be read as naming a function whose ownership is contested, not settled.
- **M4 SOURCE-CREDIBILITY is adjacent to `M-OBS-ATTR` but is not the same mechanism.** `M-OBS-ATTR`
  determines who the holder *takes* the source to be, and may fail. M4 determines how strongly a
  claim attributed to that source weights when it updates belief. The division is clean and is
  stated here so it is not later collapsed in either direction; M4 remains owned by this document.
- **`ViewKind` has no kind for entity B's view of entity A.** The owning document records this as
  blocking `M-OBS-SURF` and defers it to owner decision Q-R in
  [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md). Every `M-OBS-SURF` citation added below therefore rests
  on a view kind that does not yet exist.
- **`state.private_reputation` remains conditional.** The owning document records `reputation_private`
  as conditional pending its own open question Q2. It is no longer unowned; it is not yet settled.
- **The access and role-authorisation layer is unowned entirely.** Which human player may open which
  record is neither observation, nor view production, nor presentation. No document specifies it and
  no code implements it (Part 1.3; open question 13).

#### Ruling 1B — role authority

M13 ROLE-AUTHORITY is confirmed to [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md), which owns roles
and offices, authority attached to a role, jurisdiction, delegation, appointment and removal, acting
authority, conflict between formal and practical authority, organisational command chains, and
authority expiry and suspension.

**This document may reference a person's current role occupancy. It must not own the mechanism.**
`state.current_role` (3.7) is a time-bounded reference to a role-occupancy record held elsewhere, and
the E-1 whitelist entry `state.current_role → M13 authority` is a read of that reference, not of a
mechanism specified here. Part 1.2's separation of person from role occupancy is the counterpart of
this ruling and is unchanged by it.

The ruling settles ownership and nothing else. M13 is not specified anywhere: no authority model, no
delegation rule, no expiry semantics and no conflict rule between formal and practical authority
exist in any document. Before the ruling `state.current_role` cited a mechanism whose owner was
asserted but whose specification existed nowhere; after it, the owner is settled and the
specification still exists nowhere. The 3.7 row states this in place rather than implying a
resolution the ruling did not deliver.

#### Ruling 1C — faction alignment

M14 is split and **must not be duplicated here**:

- Faction definitions, membership rules, formal positions and faction structure —
  [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md).
- The directional, historied person-to-faction alignment and loyalty relationship, and its changing
  strength — [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).
- **This document consumes the resulting relationship projection.**

Every M14 citation in Parts 3.3, 3.4, 3.5 and 3.7 is therefore a **consumption** citation. It records
that a person-side field feeds, or is read alongside, an alignment edge owned elsewhere; it confers
no ownership here and must not be read as licence to specify faction behaviour in this document. The
citations are left in place rather than rewritten one by one, because they correctly name the
mechanism a reader must follow; this paragraph governs how they are read.

One clause of the superseded M14 definition is **not unambiguously placed by the split**: *per-person
dissent and defection probability*. It is a probability attached to a person, computed from an
alignment edge, against an organisational position — so it plausibly belongs to any of the three
documents. It is cited in this document at `psychology.values[]` (3.4, "value conflict with an
organisational position must raise dissent probability"), `psychology.attitude_to_authority` (3.4)
and `state.loyalty` (3.7). Recorded as open question 15. Until it is placed, no document should
assume it holds it.

### 3.1 Field-naming convention

`person.<group>.<field>`. Groups: `identity`, `life_history`, `psychology`, `capabilities`,
`relationships`, `state`. Every person must carry a stable `person_id` from a namespace shared with all
other entity types — [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) owns that namespace. Note that no
shared identifier namespace exists today: `cohort_id` (`.../agent_schema.py:94`) and `agent_id`
(`:161`) are unrelated and nothing binds them.

### 3.2 Identity

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):54-57. Identity is
**stable**: once a person is materialised, these fields must never be regenerated differently
(:236-237). Corrections are permitted only as recorded, audited amendments, never as silent
regeneration.

| Field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `identity.name` | structured (given / family / honorific / display) | — | **PRESENTATION-ONLY.** A display label. Must not be read by any state-changing mechanism. | Dossier shows the `person_id`. No simulation effect. |
| `identity.aliases[]` | list of `{alias, context, known_to[]}` | `M-OBS-ATTR`, M4 — **repointed 19 July 2026 (ruling 1A); was M12, M4** | Each alias must be a separate identity surface. An observer holding only the alias must not resolve it to the person, so attribution of an act must fail or mis-resolve. Alias non-resolution and misattribution are `M-OBS-ATTR`, owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, which states that attribution **may fail**. M4 then weights the claim as attributed, correctly or not. | Every act would be attributable to the true person on observation; concealment would become impossible. |
| `identity.age` | int, derived from `date_of_birth` and current sim date | M1, M6, M9, M15 | Must weight health-decline priors, retirement and succession risk, generational tie-formation affinity, and fatigue recovery rate. | Age-conditioned priors would fall back to a population median; only cohort-typical behaviour would remain. |
| `identity.date_of_birth` | date | — | **PRESENTATION-ONLY** unless a records-matching or document-verification mechanism is built. `age` carries all specified causal load. | No effect. Age is derived from a stored age plus elapsed sim time instead. |
| `identity.place_of_birth` | reference to a place entity | M6, M3, M17 | Must seed origin-community ties (M6), which must determine which local information channels reach the person (M3), and must set the baseline discrimination-exposure setting (M17). This is the entry point of the port-town chain in Part 4.1. | The person would begin with no origin community: no home-town tie bonus, no local channel, no origin-linked solidarity. |
| `identity.current_residence` | reference to a place entity | M3, M6, M9, M17 | Must determine local channel reach, physical co-location for tie formation and interaction, exposure to local hazard, and the applicable discrimination setting. | The person would be unlocated; local events could not reach them and proximity-based tie formation could not run. |
| `identity.citizenship[]`, `identity.nationality` | list of state-entity references | M13, M3 — **and M2 only indirectly, via `legal_status`** | Must determine which state's protection and obligations apply. Legal eligibility for offices, clearances, travel and asset ownership must be gated by a `legal_status` entry derived from a stated scenario law (Rule E-1a) — **M2 must not read this field directly.** Nationality is sensitive identity under E-3; the carve-out is unresolved and recorded as an open question. | Legal eligibility would default to the scenario's resident-citizen assumption; dual-nationality conflicts would become inexpressible. |
| `identity.ethnic_identity`, `identity.cultural_identity`, `identity.religious_identity` | fictional identity-entity references, each with `salience 0..1` and `publicly_known bool` | M6, M17, M19, M3 — **and nothing else** | **Subject to E-3.** Permitted effects, exhaustively: composition of the social network (M6), rate of exclusion and suspicion events (M17, bounded by Rule E-3a), and channel intelligibility (M19) with its exposure consequence (M3). Must never touch competence, morality, intelligence, **loyalty, violence propensity or manipulability** (E-3b), nor any decision weight directly, and must never be used as an **optimisation criterion for persuasion or manipulation** (control B5-5, Part 7). **"Cultural interpretation of ambiguous events" is deliberately absent — see the note below.** | Network composition and discrimination exposure would default to setting-average. All decision behaviour would be unchanged, by design — because these attributes are forbidden from reaching decisions directly in any case. |
| `identity.languages[]` | list of `{language, proficiency 0..1, register}` | M19, M3, M6, M10 | Must determine which channels, documents and conversations are intelligible; must bound the audience a person can address (M10); must gate tie formation with non-shared-language counterparts. | All content would be universally intelligible; language barriers, mistranslation and interpreter dependency would become inexpressible. |
| `identity.household[]`, `identity.family[]` | typed directed edges to person entities | M6, M7, M9, M16, M18, M20 | Family ties must be pre-existing edges with high default trust and dependency. Dependents must create financial and safety pressure (M9) and hostage or exposure salience (M20). Inheritance and succession must run over them (M18). | The person would have no dependents and no default trusted circle; family-based pressure and leverage could not exist. |
| `identity.physical_appearance` | structured descriptors | — | **PRESENTATION-ONLY.** See Part 6 and the conditional promotion note below. | No simulation effect. |
| `identity.portrait_ref` | asset reference (see Part 6) | — | **PRESENTATION-ONLY.** Stated explicitly by the founder ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):208). | Dossier renders a placeholder. No simulation effect. |
| `identity.public_identity` vs `identity.concealed_identity` | two selections over the fields above, plus `concealment_strength 0..1` | `M-OBS-SURF`, `M-OBS-ATTR`, `M-OBS-EXP`, M17 — **repointed 19 July 2026 (ruling 1A); was M12, M3, M17** | Must define which identity facts are visible to which observer classes (`M-OBS-SURF`) and which the observer can resolve to this person (`M-OBS-ATTR`). A concealed identity must not raise discrimination exposure while concealed, and must be discoverable by a specified exposure mechanism (`M-OBS-EXP`) — at which point the consequences must apply retroactively as new events. All three are owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5. **The `M-OBS-SURF` citation rests on a `ViewKind` that does not exist** — no kind expresses entity B's view of entity A (3.0a; owner decision Q-R in [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md)). | Every identity fact would be universally visible; passing, exposure, outing and covert identity would become inexpressible, and the public profile would collapse into authoritative reality. |

**Struck under Rule P-2 — "cultural interpretation of ambiguous events".** An earlier draft listed
this among the permitted effects of ethnic, cultural and religious identity, with **no mechanism
identifier attached**. Rule P-1 requires every attribute to name a mechanism that reads it, and Rule
P-2 requires anything unmapped to be **struck, not deferred**. Filing it under "at risk" while
leaving it in the permitted list would exempt the single most safety-sensitive row in this document
from the rule enforced everywhere else.

It is struck for a second and stronger reason. A "cultural interpretation" hook attached to
ethnicity and religion, with no defined reader, no stated inputs and no stated bound, is a blank
cheque — and it is precisely where essentialism would enter without anyone noticing, because
"members of culture X read ambiguity as hostile" is exactly the kind of claim it would silently
license.

The source record does name cultural interpretation as a permitted effect
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):305-306), and the source
record is the authority. Striking the *unmapped clause* is therefore not a rejection of the founder's
intent; it is a refusal to carry the intent as an unbounded hook. **Whether to allocate a mechanism —
provisionally `M21 AMBIGUITY-INTERPRETATION`, with stated inputs, stated outputs, and explicit bounds
under E-2, E-3a and E-5b — is an owner decision, recorded as an open question in Part 8.** Until it
is specified to that standard, the effect must not appear in any permitted-effects list.

**Conditional promotion — `physical_appearance`.** If, and only if, a witness-identification or
disguise mechanism is later built, a narrow structured subset (`distinctive_features[]`) may be
promoted from PRESENTATION-ONLY to a mapped attribute feeding **`M-OBS-ATTR`** — **repointed
19 July 2026 (ruling 1A); this previously read "feeding M12".** Witness identification is an observer
resolving who they saw, which is identity resolution and may fail; `M-OBS-SURF` supplies the features
exposed to that observer. Both are owned by
[`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, and neither the
promotion condition nor its successor mechanism exists. Until that mechanism exists, Rule P-1 applies
to the whole field. It must not be read by anything.

### 3.3 Life history

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):59-62.

**Structural requirement.** Life history must be stored as a list of typed, dated, structured
**life-event records**, not as prose. Each record must carry `{event_type, period, place,
counterparts[], magnitude, valence, evidence_visibility}`. Prose biography must be generated from
these records at read time and must never be the source of truth. The existing `biography_ref`
pattern (`.../agent_schema.py:166-168`, pointing at a file that does not exist) is exactly the
failure mode the founder rejects, and must not be built upon.

**Dependency.** Life-event records at simulation start are seeded history. Life-event records
created during a run must be produced by the central transition mechanism P0.6 is required to
deliver. Until P0.6 lands, the second half of this group is unbuildable.

**Memory rule.** Formative life events must **not** decay. The existing `AgentMemory` model
(`.../agent_schema.py:143-151`) treats memory purely as a decaying list of event ids, which
contradicts stable life history directly. Recency must modulate *retrieval probability* in M8; it
must never delete the record.

| Field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `life_history.childhood_environment` | structured: place ref, settlement type, economic condition, security condition | M6, M8, M20, M17 | Must seed origin-community ties and their strength; must supply the recalled experiences M8 retrieves when a structurally similar event occurs; must set baseline threat salience for hazard classes present in childhood. | There would be no origin identification and no childhood recall set; the person would react to a home-region shock exactly as a stranger would. |
| `life_history.family_wealth_and_class` | `{origin_class, origin_wealth_band, trajectory}` | M6, M9 — **not M2** | Must determine starting network reach into elite or non-elite circles (M6) and the financial-pressure floor (M9), and must act as a **weight on the rate of capability acquisition over time** — never as a gate. **Class must not weight any decision directly (E-3) and must not be read by M2 (E-1): it is a prior, not a permission.** | Network reach and pressure floor would default to setting-average. Class mobility narratives would become unrepresentable. |
| `life_history.education[]` | list of `{institution_ref, level, field, country, cohort_peers[]}` | M6, M3, M4 — **M2 only via `capabilities.expertise[].credential_ref`** | Institutions must be entities and alumni must be ties (M6). Foreign institutions must produce foreign professional ties, hence foreign information sources (M3) and different source-credibility weighting (M4). Where a qualification gates a role, **M2 must read the recorded credential, not the education history** (E-1). This is the entry point of the elite-education chain in Part 4.2. | No alumni network and no foreign-source channel would exist. The person's information diet would be domestic by default. |
| `life_history.service_record` | list of `{organisation_ref, period, rank, theatre, discharge_type}` | M6, M4, M8, M14 — **M2 only via `capabilities.security_clearance`** | Must create durable ties into the security establishment (M6), raise credibility weighting for military-sourced claims (M4), and supply recall material for security-related events (M8). Clearance eligibility must reach M2 as a **granted, recorded clearance**, not as service history (E-1). | No security-establishment ties and no service-derived credibility asymmetry would exist. |
| `life_history.employment_history[]` | list of `{organisation_ref, period, role, seniority, exit_reason}` | M6, M14, M16 — **M2 only via `capabilities.expertise[]`** | Prior employers must be tie sources; exit reason must set edge valence sign; sector experience must set faction affinity (M14). Where sector experience gates an option, **M2 must read the recorded expertise entry, not the employment history** (E-1). | The professional network would be limited to the current role. Career-derived loyalties and grudges would be inexpressible. |
| `life_history.migration_and_travel[]` | list of `{from, to, period, reason, status}` | M6, M17, M19, M3 | Must create diaspora and destination ties; migration status must be a discrimination-exposure input (M17); residence abroad must raise language proficiency and foreign-channel exposure. | There would be no transnational ties, and diaspora dynamics could not be modelled. |
| `life_history.achievements[]` | list of `{achievement_type, verifying_organisation_ref, public bool, date}` | `M-OBS-SURF`, M4, M10 — **conditional; repointed 19 July 2026 (ruling 1A), was M12, M4, M10** | **Mapped only when structured with a verifying entity.** A publicly known, verified achievement must raise credibility (M4) and audience reach (M10) and must form part of the observable surface this person exposes (`M-OBS-SURF`, owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5). It is the surface that is the mechanism; the public profile is a **view** produced per [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2, not a mechanism this row may cite. **Free-text achievements with no verifier are PRESENTATION-ONLY** and must not be read. | The person would carry no reputational credit; credibility would rest on role and relationships alone. |
| `life_history.traumatic_experiences[]` | list of `{event_ref, category, severity, age_at, resolved bool}` | M8, M20, M9 | Must be the primary input to threat salience. When a new event matches a trauma's category, M8 must retrieve it and M20 must raise the weight on hazard-avoiding options. Severity must modulate the magnitude; it must never force a choice (E-2 bound applies). Entry point of the political-violence chain in Part 4.3. | Threat response would be baseline; two people with identical roles would react identically to a violent event. |
| `life_history.criminal_or_disciplinary[]` | list of `{organisation_ref, finding, period, public bool, spent bool}` | `M-OBS-SURF`, M16 — **M2 only via `legal_status.disqualifications[]`; repointed 19 July 2026 (ruling 1A), was M12, M16** | A finding that bars office or clearance must be materialised as a `legal_status.disqualifications[]` record carrying its originating event; **M2 must read that record, not the history** (E-1, Rule E-1a). A non-public record must be exploitable leverage that another entity may hold (M16); the `public` flag must determine whether the finding is on the observable surface (`M-OBS-SURF`), which is what makes a concealed finding leverage rather than common knowledge. | No legal-history eligibility bar and no blackmail surface would exist. |
| `life_history.political_involvement[]` | list of `{organisation_ref, period, role, public bool, current bool}` | M14 *(consumption — ruling 1C)*, M6, `M-OBS-SURF` — **not M2; repointed 19 July 2026 (ruling 1A), was M14, M6, M12** | Must set faction affinity priors and political ties (M6). **Faction affinity is not owned here:** per ruling 1C the person-to-faction alignment edge is owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) and faction structure by [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md); this row supplies a prior to that edge and consumes its projection. A concealed past affiliation must be a leverage and exposure surface (`M-OBS-SURF`, `M-OBS-ATTR`). **Political history must never gate the option set:** a person's politics may change what they are inclined to do, never what they are permitted to do. | The person would have no political history; faction alignment would rest on current position only. |
| `life_history.previous_crises[]` | list of `{crisis_ref, role_held, outcome, lesson_tag}` | M8, M1, M20 | Must be the specific recall set M8 draws on when the current crisis matches a recorded crisis type. `lesson_tag` must bias the option class the person favours — as a weighted term, never a selection. | Every crisis would be the person's first; there would be no experience-derived differentiation between veterans and novices. |

### 3.4 Psychology and worldview

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):64-67. Seventeen
attributes, against the four that exist today in `AgentTraits` (`.../agent_schema.py:122-130`).

**Vocabulary requirement.** `values`, `political_beliefs`, `fears` and `aspirations` must be drawn
from bounded, scenario-authored, machine-readable vocabularies. As free text they are prose, and
Rule P-1 strikes them. The existing `MicroAgent.beliefs` field is `dict[str, float]` with free-form
keys (`.../agent_schema.py:170-172`), which is exactly the shape that permits this to rot.

| Field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `psychology.values[]` | list of `{value_tag, weight 0..1}` from a closed vocabulary | M1, M14 *(consumption — ruling 1C)* | Each option must carry value-implication tags, and matching tags must contribute a bounded term to `score(o)`. Value conflict with an organisational position must raise dissent probability. **Dissent and defection probability is the one clause of the superseded M14 definition that ruling 1C does not unambiguously place** (3.0a, open question 15); this row states the required effect and does not claim to own the mechanism producing it. | Options would be weighted on interest alone; principled and unprincipled actors would become indistinguishable. |
| `psychology.political_beliefs[]` | list of `{position_tag, strength 0..1, publicly_stated bool}` | M1, M14 *(consumption — ruling 1C)*, M4, `M-OBS-SURF` — **repointed 19 July 2026 (ruling 1A), was M1, M14, M4, M12** | Must weight policy options, supply a prior to the faction-alignment edge owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md), and modulate credibility of politically coded sources (M4). The `publicly_stated` flag must place a position on the observable surface; **privately held and publicly stated positions must be able to diverge**, which is a property of `M-OBS-SURF` and not of any view or dossier. | There would be no policy preference; every actor would be a pure office-holder. |
| `psychology.religious_commitment` | `{intensity 0..1, participation_frequency}` | M6, M3, M17 — **subject to E-3** | **Commitment is separated from religious identity.** Permitted effects, exhaustively: participation in religious-institution networks (M6), exposure to claims carried by those networks (M3), and discrimination-exposure interaction (M17, bounded by Rule E-3a). Must not weight any political option directly. | The religious-institution channel would not be available to this person. There would be no decision effect, by design. |
| `psychology.risk_tolerance` | float 0..1 | M1, M20 | Must scale the weight applied to outcome variance in `score(o)`. High tolerance must flatten the penalty on high-variance options; it must not select them. *Exists today* at `.../agent_schema.py:125`. It is serialised into the mapping passed to the stub gateway (`institutional_agent.py:38-41`) and read by nothing: `llm_gateway.propose_action` (`llm_gateway.py:70-73`) reads only `role` and `agent_id`, and returns a canned proposal from a hardcoded role→action table (`:41-51`). It drives no mechanism. | Risk weighting would be population-median; bold and cautious actors would be indistinguishable. |
| `psychology.need_for_status` | float 0..1 | M1, M10, M14 | Must weight options by visibility and credit-claiming potential; must raise propensity to make public statements (M10). *Exists today* as `status_seeking` (`:126`), and like `risk_tolerance` is serialised into the stub gateway mapping (`institutional_agent.py:38-41`) and read by nothing (`llm_gateway.py:70-73`). It drives no mechanism. | There would be no preference for visible action over effective action. |
| `psychology.empathy` | float 0..1 | M1, M7 | Must weight the civilian-harm and counterpart-cost terms of an option, and must modulate how strongly harm caused to a tied counterpart degrades the edge (M7). | Human cost would carry no weight beyond its instrumental effect. |
| `psychology.loyalty` | `{target_ref, strength 0..1}[]` — **materialisation-time seed only** | *(none — see note)* | **Seed value, not a parallel input.** It must set the initial value of `state.loyalty` at materialisation and must then have **no reader of its own**. All mechanisms must read `state.loyalty`. Retaining both as live inputs would double-count allegiance and let each field's Rule P-3 test pass for the wrong reason. | Allegiance would start at a setting-default rather than an authored value. No mechanism would lose an input. |
| `psychology.ambition` | float 0..1 | M1, M14, M15 | Must weight options that improve future role prospects, including against present interest, and must raise promotion salience for background persons (M15). | There would be no forward-looking positioning, and career-motivated behaviour would be inexpressible. |
| `psychology.patience` | float 0..1 | M1 | Must set the temporal discount rate applied to delayed outcomes in `score(o)`, and is therefore the term that must decide whether slow lawful routes outweigh fast damaging ones. | All actors would share one discount rate, and time-preference conflict between actors would vanish. |
| `psychology.susceptibility_to_pressure` | float 0..1 | M9, M1 | Must scale how strongly accumulated stress and financial pressure distort the decision distribution, by widening temperature and shortening horizon. **This is a manipulability term, and E-3b forbids any sensitive identity attribute from writing, seeding or conditioning it.** It must also never be an optimisation criterion for persuasion (control B5-5, Part 7). | Pressure would have a uniform effect on everyone, and coercion and stress-testing would lose differentiation. |
| `psychology.attitude_to_authority` | float −1..1 | M4, M1, M14 | Must weight credibility of official sources (M4) and compliance-shaped options, and must raise or lower dissent probability. Related to the existing `institutional_trust` scalar (`:127`), which is populated but read by no mechanism. | Official instruction would be weighted like any other input. |
| `psychology.attitude_to_violence` | float 0..1 with `context_qualifiers[]` | M1 | Must weight the coercive-option class. **Must be bounded by `λ_max`.** No value may drive the probability of any non-violent feasible option to zero (E-2 full support). | Coercive and non-coercive options would be weighted alike. |
| `psychology.institutional_trust` | per-institution map, not a scalar | M4, M1 — **not M2** | Must determine how strongly this person credits information and instruction from each named institution. **Not mapped to M2:** trust is psychology, and E-1 forbids M2 from reading it — distrusting an institution must change how a person weights its instructions, never whether an option is available to them. *A single scalar exists today* (`:127`), populated but read by no mechanism; per-institution resolution is new. | Trust would be uniform across institutions; an actor could not trust the army and distrust the ministry. |
| `psychology.perceived_grievances[]` | list of `{grievance_tag, target_ref, onset_event_ref, intensity, resolution_condition}` | M1, M5, M17, M10 | **Grievance must be event-sourced and resolvable.** Onset must reference a recorded event; intensity must be able to fall as well as rise; a resolution condition must exist. Grievances must weight options against the target and must raise receptivity to claims that name the target (M5). | There would be no accumulated resentment; a person who had been repeatedly wronged would behave like one who had not. |
| `psychology.personal_fears[]` | list of `{fear_referent_ref, intensity}` — **structured referent required** | M20, M1 | Must raise threat salience for events involving the referent. **Free-text fears are PRESENTATION-ONLY**, because there is nothing for M20 to match against. | Threat salience would be generic; personal vulnerabilities could not be targeted or protected. |
| `psychology.long_term_aspirations[]` | list of `{aspiration_tag, target_ref, horizon}` from a closed vocabulary | M1, M14, M16 | Must weight options that advance the aspiration, on a horizon set by `patience`, and must provide the currency for offers and inducements from other entities. | There would be no long-horizon motive; actors could not be bought or persuaded with future prospects. |
| `psychology.immediate_objectives[]` | list of `{goal_tag, priority 0..1}` | M1 | Must be the dominant near-term weighting term in `score(o)`. **Not mapped to M2** — an objective is something a person wants, never a fact about what they may lawfully do, so it must not gate the option set (E-1). *Exists today* as `Objective` (`.../agent_schema.py:115-119`) and is populated in the demo scenario. It is serialised into the stub gateway mapping (`institutional_agent.py:38-41`) and read by nothing (`llm_gateway.py:70-73`); it drives no mechanism. | Behaviour would be driven by long-run disposition only; actors could not respond to the current situation. |

**Note on the existing four traits.** `risk_tolerance`, `status_seeking`, `institutional_trust` and
`corruption_susceptibility` exist and are populated in `kestral-strait.json`. They are not read by
any engine mechanism. They must be re-homed under this group and given real readers, or Rule P-2
applies to them as it applies to new fields. `corruption_susceptibility` is not carried forward as
a named field in this specification: it must be re-expressed as a bounded term over
`psychology.values` and `state.financial_pressure`, so that susceptibility to inducement is a
consequence of circumstances rather than a fixed personal constant.

### 3.5 Capabilities

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):69-71. Twelve
attributes against the three that exist today in `AgentResources`
(`.../agent_schema.py:133-140`).

Capabilities feed **M2 FEASIBILITY-GATE** primarily. This is the identity-blind half of the model:
what a person *can* do, as distinct from what they are *inclined* to do.

| Field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `capabilities.expertise[]` | list of `{domain_tag, level 0..1, credential_ref}` | M2, M4, M1 | Must gate options requiring the domain (M2 reads `credential_ref`, never `life_history.education[]`); must raise this person's credibility as a source within it (M4); must raise the accuracy of their private assessments. | Options requiring expertise would be either unavailable or available to everyone equally — whichever default is chosen must be declared, not implicit. |
| `capabilities.leadership` | float 0..1 | M14, M10, M2 | Must determine how much of an organisation's internal disagreement this person can override, and how reliably subordinates execute. | Organisational action would not depend on who leads it. |
| `capabilities.negotiation` | float 0..1 | M7, M16 | Must scale the achieved value of bilateral agreements and the probability an obligation is successfully called in. | All negotiated outcomes would be personnel-independent. |
| `capabilities.languages` | *reference to* `identity.languages[]` | M19 | Must not be duplicated. The capability must read the identity field. | See `identity.languages`. |
| `capabilities.social_influence` | derived from the relationship graph, not stored | M10, M11, M6 | Must be **computed** from out-edges and their strength, never authored as a free scalar. A stored scalar would be unfalsifiable and would drift from the graph. Supersedes `personal_network_reach` (`.../agent_schema.py:138-140`). | Influence would be authored rather than earned, and the relationship graph would stop mattering. |
| `capabilities.financial_resources` | `{personal_wealth, liquid, controlled_budget_ref}` | M2, M11, M9, M16 | Must gate options with a cost; must contribute to disproportionate influence weighting (M11); must set the financial-pressure floor. Must distinguish personal wealth from institutionally controlled budget, which today's `budget_control_usd_m` (`:136`) conflates. | Cost would not be a constraint on individual action, and wealth-based influence would be inexpressible. |
| `capabilities.institutional_access[]` | list of `{organisation_ref, access_level, via_relationship_ref}` | M2, M3, M11 | Must determine which rooms, meetings and processes the person can reach, and hence what they learn (M3). Access held *via a relationship* must lapse when that edge degrades. This is the recorded capability through which the Part 4.2 education chain reaches M2 — M2 reads this record, never the education history. | Access would be determined by role title alone; informal access, which is most real access, would disappear. |
| `capabilities.security_clearance` | `{level, issuing_state_ref, granted_event_ref, suspended bool}` | `M-OBS-EXP`, M2 — **repointed 19 July 2026 (ruling 1A), was M3, M2, M12** | Must determine which classified events are observable, and must be the record M2 reads when clearance gates an option — never `life_history.service_record`. **Clearance-gated event observability is `M-OBS-EXP`**, owned by [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) §5, which names `M-OBS-EXP` the sole future reader of `EventVisibility` (`.../agent_schema.py:203-208`) — a construct that exists, is the project's only visibility construct, and is never populated. This field is therefore a person-side **input** to a mechanism owned elsewhere; this document must not specify the gating rule. | All events would be equally observable, and the intelligence asymmetry the product depends on would collapse. |
| `capabilities.military_or_technical_skills[]` | list of `{skill_tag, level}` | M2 | Must gate options requiring the skill. | Skill-gated options would be open to all or to none. |
| `capabilities.media_reach` | `{owned_channels[], habitual_platforms[], estimated_audience}` | M10, M11 | Must bound the audience a public statement reaches, by channel and by cohort composition. **Bounded by the settled B5 decision — see Part 7.** Media consumption is an expressly *permitted* non-sensitive factor for a campaign model, so this field may inform reach and audience composition; it must not carry, proxy or be combined with a protected trait to form a targeting criterion (control B5-5). | Public statements would reach a default audience regardless of who makes them. |
| `capabilities.physical_health` | `{baseline 0..1, chronic_conditions[], age_decline_curve}` | M9, M2, M18 | Must set fatigue recovery rate and the ceiling on sustained activity; must gate physically demanding options; must drive incapacity and succession risk (M18). | Everyone would be equally durable, and illness, exhaustion and death-in-office would be inexpressible. |
| `capabilities.dependents_and_obligations[]` | list of `{person_ref or organisation_ref, obligation_type, severity}` | M9, M16, M20, M1 | Must be a standing pressure and leverage surface: dependents must raise the cost of risk-taking and must provide targets that raise threat salience. | Nobody would have anything to lose, and coercion, protection and personal cost would vanish. |

### 3.6 Relationships

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):73-80.

**Ownership.** The edge structure, its dimensions, its history and its update rules are specified in
[`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md), not here. This section specifies only what the
person record must hold and which mechanisms read it.

> **Amended 19 July 2026 (ruling 1C).** That document additionally owns **the directional, historied
> person-to-faction alignment and loyalty relationship and its changing strength**, with faction
> definitions, membership rules, formal positions and faction structure owned by
> [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md). This document **consumes the resulting projection
> and must not duplicate the mechanism.** One consequence worth stating: the alignment edge runs from
> a **person to an organisation**, and none of the thirteen founder-named relationship kinds below is
> person-to-organisation — twelve are person-to-person and "employers" is ambiguous. Whether the
> alignment edge is a new kind on the common directed edge, or a distinct edge class, is for
> [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) to settle. This document only requires that it not
> be materialised twice.

**Requirements this document restates because they bear on the person record:**

- Edges must be **directional**. "A trusts B" must not imply "B trusts A"
  ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):77).
- Edges must carry **history**, not only a current value.
- The founder's thirteen relationship *kinds* — family, friends, rivals, mentors, employers,
  political patrons, financial dependencies, romantic relationships, professional contacts, trusted
  sources, people they distrust, people to whom they owe favours, people who owe them favours
  (:73-75) — must be modelled as **edge types over a common directed edge**, not as thirteen
  separate fields on the person. Several are the same edge viewed from different sides: "owes a
  favour to" and "is owed a favour by" are one obligation record read in two directions, and
  duplicating them guarantees they will disagree.
- The founder's twelve edge *dimensions* — trust, affection, fear, respect, dependency, ideological
  alignment, resentment, familiarity, leverage, shared history, last interaction, important
  unresolved events (:79-80) — are dimensions of the edge, owned by
  [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md).

| Person-side field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `relationships.out_edges[]` | directed edges to entity references, typed and dimensioned per [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) | M1, M3, M4, M6, M7, M10, M11, M16 | Must be the single largest input to behaviour. Must determine who this person hears from and believes (M3, M4), whose interests weight into their decisions (M1), how far their statements travel (M10), and what they can call in (M16). | The person would be socially isolated, and almost every mechanism in this document would degrade to a default. |
| `relationships.obligation_ledger[]` | list of `{counterpart_ref, direction, magnitude, origin_event_ref, expiry, discharged bool}` | M16, M1, M7 | Must record favours owed and owed-to as **callable, expiring, discharge-tracked** entries. Calling one must consume it and must alter the edge. | Favours would be sentiment rather than currency, and patronage and reciprocity would become inexpressible. |
| `relationships.trusted_sources[]` | derived view over out-edges with high trust and information-carrying type | M3, M4 | Must not be stored separately. A derived projection; storing it independently would drift from the graph. | See `out_edges`. |

**Contradiction to record.** The two existing relationship structures cannot be extended into this;
they must be **replaced**. `MicroAgent.relationships` is one signed float per counterpart
(`.../agent_schema.py:175-177`), and the standalone `Relationship` model
(`.../agent_schema.py:190-200`) carries a single shared trust, valence and dependency with only
`last_interaction_tick` as history. Both are unread and unpopulated — `Relationship` is instantiated
nowhere, and no institutional agent in `kestral-strait.json` carries a `relationships` key at all —
so **replacement costs nothing to make now** and will cost a great deal later. Note also that the
only social graph running code actually uses is undirected (`nx.Graph()` at
`scaffold/backend/app/simulation/diffusion.py:24`), which symmetrises asymmetric ties silently.

### 3.7 Current state

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):82-85. Cadence is
specified separately in Part 5.

| Field | Type sketch | Mechanism(s) | How it must change behaviour | If absent (specified null behaviour) |
|---|---|---|---|---|
| `state.location` | place-entity reference + `since_event_ref` | M3, M6, M2, M20 | Must determine which events are physically observable, who is available for interaction, which options are reachable, and exposure to local hazard. | The person would be everywhere and nowhere; presence, absence, travel time and evacuation could not be modelled. |
| `state.health` | float 0..1 + `conditions[]` | M2, M9, M18 | Must gate demanding options, set the recovery rate for fatigue, and drive incapacity and succession (M18). | There would be no incapacity path. |
| `state.stress` | float 0..1 | M9, M1 | Must raise the softmax temperature, producing more erratic selection, and must shorten the effective time horizon. Must be bounded so that stress **degrades judgement without determining a choice** (E-2). | Judgement quality would be constant regardless of circumstance. |
| `state.fatigue` | float 0..1 | M9, M1, M2 | Must accrue with activity load and recover with rest; must degrade assessment accuracy and gate sustained operations. | Actors would be tireless, and tempo would have no cost. |
| `state.financial_pressure` | float 0..1 | M9, M1, M16 | Must raise the weight on options that relieve pressure, including inducements. This is where susceptibility to corruption must live, as circumstance rather than as a personal constant. | Money troubles would not affect behaviour, and inducement would have no purchase. |
| `state.confidence` | float 0..1 | M1, M10 | Must modulate willingness to act on incomplete information and to make public commitments. Must be updated by recorded outcomes: success must raise it and public failure must lower it. | Confidence would be static, and success and humiliation would have no behavioural consequence. |
| `state.loyalty` | per-target map — **the single loyalty value; seeded once from `psychology.loyalty`** | M14 *(consumption — ruling 1C)*, M1, M16 | The **only** loyalty field any mechanism reads. Must lower defection probability toward the target, weight options that protect them, and raise willingness to discharge obligations to them (M16). **Ruling 1C bears directly on this row:** where the target is a faction, the directional, historied alignment and loyalty relationship and its changing strength are owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md), and this field must consume that edge's projection rather than hold a second, independently updated value — which would be the duplication ruling 1C forbids, and would reproduce at the faction level the double-counting Rule P-6 caught between `psychology.loyalty` and this field. **Whether defection probability itself is computed here, on the edge, or in [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) is open question 15.** Must be able to fall **and recover**, and every change must be event-sourced per 5.2. | Allegiance would be fixed at scenario authoring; betrayal and reconciliation would be impossible. |
| `state.current_intentions[]` | list of `{intent_tag, target_ref, formed_event_ref, horizon}` | M1, `M-OBS-SURF` — **repointed 19 July 2026 (ruling 1A), was M1, M12** | Must hold multi-tick plans that survive between decision points, so behaviour is not re-derived from scratch each tick. Must be **partially** observable to others — the intention itself is authoritative state held here; what another entity can learn of it is `M-OBS-SURF`, and what that entity then holds is a belief owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). Partial and fallible observation of intent is what makes intelligence work meaningful. | Every tick would be independent: no plan, no persistence, no anticipation. |
| `state.knowledge[]` | propositions with source, evidence and confidence | M1, M2, M5, `M-OBS-SURF` — **repointed 19 July 2026 (ruling 1A), was M1, M2, M5, M12** | Must hold what the person actually knows, distinct from what is true. *(Structure owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md).)* What **another** entity can learn about this person's knowledge is `M-OBS-SURF`, not a property of this field. Note the division fixed by ruling 1A: the `Observation` records that populate this field are written solely by `M-OBS-ACQ`, and their consumption — belief updating, storage, confidence labelling — is owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md). This document owns neither side. | The person would be omniscient or ignorant by fiat, and incomplete intelligence — a CHARTER commitment ([`../../CHARTER.md`](../../CHARTER.md):23) — would be unrepresentable. |
| `state.beliefs[]` | propositions with strength, source and provenance | M1, M5, M20 | Must hold what the person believes true, including things that are false, so as to answer the founder's question "what does this person believe that is factually wrong?" *(Structure owned by [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md).)* | Belief and truth would collapse into one another. |
| `state.rumours_heard[]` | list of `{narrative_ref, heard_via_ref, tick, credited 0..1}` | M5, M4, M10 | Must act as the pre-belief buffer: a claim received but not yet credited. Must determine what this person can repeat, and to whom. | Claims would be either believed or unheard, and the transmission stage would vanish. |
| `state.recent_contacts[]` | list of `{person_ref, tick, channel, subject_ref}` | M7, `M-OBS-SURF`, M3 — **repointed 19 July 2026 (ruling 1A), was M7, M12, M3** | Must record interaction for edge update (M7) and must produce the observable contact pattern that intelligence work reads (`M-OBS-SURF`). Contact analysis is the clearest case for the ruling: whether a meeting was observed at all is a simulation fact, and no dossier may display a contact no entity observed. | There would be no interaction history; edges could not be updated from behaviour, and contact analysis would be impossible. |
| `state.current_role` | role-occupancy reference, time-bounded | M13 *(reference only — ruling 1B)*, M2, M3, `M-OBS-SURF` and `M-OBS-EXP` — **repointed 19 July 2026 (rulings 1A and 1B); was M13, M2, M3, M12** | Must be a **time-bounded reference** to a role-occupancy record owned by [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md), never a copy of one. Through that reference the role must supply authority (M13), information access (`M-OBS-EXP`, since a seat is one route to clearance-gated observability) and public visibility (`M-OBS-SURF`) — all of which must be **lost on exit** while identity and relationships persist. **Ruling 1B settles ownership of M13 on `ORGANISATION-MODEL.md` and this document must not own it:** authority attached to a role, jurisdiction, delegation, appointment and removal, acting authority, conflict between formal and practical authority, command chains, and authority expiry and suspension all sit there. **Ownership is settled; specification is not.** Before the rulings this row cited two mechanisms that were specified in no document at all — M13, asserted to an owner but written nowhere, and M12, assigned to a user-interface specification that cannot own a simulation mechanism. Both now have a named owner. Neither is yet specified, and this row must not be read as though they were. | Person and office would remain fused, as in `MicroAgent` today, and replacing a minister would remain inexpressible. |
| `state.available_resources` | current draw against `capabilities.financial_resources` and role budget | M2, M16 | Spending must deplete it. This is the person-level half of the missing cost mechanism: A3 §7 verified that the words `cost`, `cooldown`, `decay`, `budget`, `resource` and `prerequisite` appear nowhere in `engine.py`. | Action would be free and repeatable, which is precisely the mechanism whose absence produced the macro-saturation critical finding. |
| `state.public_reputation` | per-audience map: cohort or organisation → sentiment | M10, M4, `M-OBS-SURF`, M11 — **repointed 19 July 2026 (ruling 1A), was M10, M4, M12, M11** | Must hold what different audiences think of this person. Must be per-audience: a figure trusted by one community and despised by another must be representable. **`M-OBS-SURF` supplies the evidence base that separates public from private reputation** — the owning document states this explicitly — so the difference between the two fields must follow from what each observer class could actually observe, never from authorial assignment. | Reputation would be a single number or absent, and audience-differentiated standing would be lost. |
| `state.private_reputation` | per-observer-class map | M6, M7, M14 *(consumption — ruling 1C)*, `M-OBS-SURF` — **repointed 19 July 2026 (ruling 1A), was M6, M7, M14, M12** | Must hold standing among peers and insiders, which must be able to invert public standing entirely. Must feed the faction-alignment edge owned by [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) and elite tie formation (M6). **Conditional, not settled:** the owning document records `reputation_private` as conditional pending its own open question Q2 (3.0a). It is no longer unowned; it is not yet resolved, and this row must not be built against until it is. | Elite and public opinion could not diverge, removing one of the model's most useful dynamics. |
| `state.exposure_to_danger` | float 0..1 — **authoritative reality.** Derived per tick from location, role, affiliations and active threats | M20 (as input), **"harm-event resolution" — no mechanism identifier, no owner** | **The objective hazard, and a world fact.** Must be derived per tick from world state and **must never be written by any psychological mechanism.** Reserved for the probability of harm events actually befalling this person. **Defect recorded 19 July 2026:** the second reader named in this row is a prose phrase, not a register entry. It has no identifier, appears in no document, and was not addressed by any of the three rulings, so this is the only remaining row in 3.7 whose mapping does not resolve to a mechanism with a named owner. Rule P-1 requires a named mechanism; allocating one is an owner decision, recorded as open question 16. | Personal risk would not exist; nobody would have a reason to take cover. |
| `state.perceived_threat` | float 0..1 — **the entity's self-understanding view** | M20 (as output), M9, M1 | **What this person believes their risk to be.** Must be produced by M20 from the authoritative `exposure_to_danger` plus recall (M8), trauma and salience. M9 stress and M1 decision weighting must read **this** value, never the authoritative one. | Perceived and actual risk would collapse into one number, and the divergence Part 4.3 depends on would be inexpressible. |

**Why these are two fields and not one.** An earlier draft of this specification had a single
`state.exposure_to_danger` both derived from world facts each tick *and* raised by trauma recall.
That cannot work, and the reason is the document's own four-view model: objective hazard belongs to
**authoritative reality**, perceived hazard to the **entity's self-understanding**. One field
carrying both would let a person's psychology silently contaminate a quantity other mechanisms treat
as a world fact, and the per-tick derivation in 5.2 would overwrite the perceptual component every
tick — so the Part 4.3 chain would not run at all. The divergence between the two is, as Part 4.3
says, the point, which is exactly why they cannot be one number.

---

## Part 4 — Worked causal chains

Each chain is taken from the source record and expanded into the full path: attribute → mechanism →
state touched → behavioural change. Every step is **specified, not implemented**. Numeric values are
illustrative placeholders for parameters the rule pack would own; they are not calibrated and must
not be read as such.

Each chain closes with a **negative clause** stating what the chain must *not* do. The negative
clauses are the substance of this document. Without them, each chain is a stereotype with extra
steps.

### 4.1 Childhood in an economically marginalised port town

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):248-254.

**Seeded attributes**

```text
identity.place_of_birth              → place:eastern-wharf-district
life_history.childhood_environment   → {settlement: port_town, economic_condition: declining,
                                        period: age 0-17}
life_history.family_wealth_and_class → {origin_class: maritime_labour, origin_wealth_band: low}
```

**Step 1 — M6 TIE-FORMATION.** Birthplace and childhood environment must raise the prior
probability of directed out-edges to entities rooted in that place: the port workers' association,
the district community organisation, individual persons of the same origin cohort. Edges are created
with an origin-affinity bonus on the `familiarity` and `shared_history` dimensions.

> State touched: `relationships.out_edges[]` gains typed edges. Nothing else yet.

**Step 2 — M3 INFORMATION-EXPOSURE.** Those edges determine reachability. Claims circulating in the
port-labour network must reach this person earlier and more often than they reach an unconnected
person of the same role.

> State touched: `state.rumours_heard[]` receives port-network claims sooner.

**Step 3 — M4 SOURCE-CREDIBILITY.** A claim arriving via a high-`trust` origin-community edge must
receive a higher credibility weight than the same claim from an unconnected source. **The claim is
not accepted; its weight is raised.**

> State touched: the evidence weight passed to M5.

**Step 4 — M5 BELIEF-UPDATE.** Higher-weighted evidence about shipping-sector harm shifts
`state.beliefs` on the relevant propositions further per observation than it would for an
unconnected person.

> State touched: `state.beliefs[]`.

**Step 5 — M8 EXPERIENCE-RECALL.** When a blockade event is evaluated, M8 must retrieve the
childhood-environment record because the event's category (`maritime_livelihood_disruption`)
matches. The recalled record contributes a bounded term.

**Step 6 — M1 DECISION-WEIGHTING.** The contributions compose:

```text
Feasible option set from M2 (identity-blind):
    { impose_blockade, delay_blockade_pending_review, impose_with_compensation_package,
      refer_to_cabinet, oppose_publicly, abstain }

Illustrative contributions to score(impose_blockade):
    base_utility (national security framing)            +0.90
    w(origin-community tie salience → harm to tied)     −0.35   (bounded, |w| ≤ λ_max)
    r(recalled childhood environment, via M8)           −0.25
    n(port association out-edge, dependency)            −0.20
                                                        ------
                                                        +0.10

score(impose_with_compensation_package)                 +0.55
score(delay_blockade_pending_review)                    +0.40
… all remaining feasible options retain P(o) > ε
```

**Required behavioural change.** The specified composition must lower the probability of the
unmitigated blockade and must raise the probability of the compensated and delayed variants. Across
many runs, a person specified this way must oppose unmitigated blockades more often than an
otherwise identical person from a different background — while remaining able to impose one in any
single run.

**Negative clause.** This chain must **not** produce "person from port town ⇒ opposes blockade".
`impose_blockade` remains in the option set with non-zero probability throughout, because M2 never
saw the biography. If a build produces a person who never selects a feasible option under any world
state, E-2's full-support invariant has been violated and the build must fail.

**Test obligation (Rule P-3).** Perturb `place_of_birth` alone, hold seed and world state fixed, run
the decision point *N* times, and assert the option distribution shifts measurably. If it does not,
`place_of_birth` has no causal value and Rule P-2 applies.

### 4.2 Elite foreign education

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):256-262.

**Seeded attributes**

```text
life_history.education[]        → {institution_ref: org:meridian-school-of-governance,
                                   country: state:aveline, level: postgraduate,
                                   cohort_peers: [person:…, person:…]}
identity.languages[]            → {language: avelinian, proficiency: 0.85}
life_history.migration_and_travel[] → {to: state:aveline, period: 4 years, reason: study}
```

**Step 1 — M6 TIE-FORMATION.** Named cohort peers become directed out-edges. Where a peer later
holds a foreign official or investor role, the edge persists into that role. Edges are person-to-
person and must survive the peer's role changes.

> State touched: `relationships.out_edges[]` now crosses a state boundary.

**Step 2 — M19 LANGUAGE-ACCESS and M3 INFORMATION-EXPOSURE.** Proficiency admits foreign-language
channels to this person's reachable channel set. Foreign professional edges admit private
foreign-sourced claims. This person's information diet must differ **in content**, not merely in
weighting, from a domestically educated peer.

> State touched: `state.knowledge[]` and `state.rumours_heard[]` acquire propositions a domestic-
> only person does not hold at all.

**Step 3 — M4 SOURCE-CREDIBILITY.** Foreign-sourced claims arriving through a personal edge are
weighted by that edge's `trust`, not by generic foreign-source discount. A foreign claim from a
trusted classmate must outweigh a domestic claim from an untrusted ministry.

**Step 4 — M5 BELIEF-UPDATE and M2 FEASIBILITY-GATE.** Two distinct effects, and the distinction
matters:

- **Belief:** the person's assessment of sanctions risk differs because their evidence differs. They
  may be more accurate or less accurate — the model must not assume foreign education confers
  correctness.
- **Feasibility:** `capabilities.institutional_access` via those edges must admit options no other
  actor has, such as `open_informal_channel_to_foreign_ministry`. **Access established by a recorded
  relationship is one of the enumerated capability routes by which biography may reach the option
  set; the complete closed list is the table in E-1.** E-1 is not breached, because M2 does not
  consult the person's education, origin or nationality — it reads the `capabilities.institutional_access`
  record that education *caused to exist*. The distinction is the whole safety argument: M2 reads a
  materialised present fact with a recorded provenance, never the biography that produced it.

**Step 5 — M1 DECISION-WEIGHTING.** Because the belief state differs, the same score function
produces a different distribution — a first-order effect of different evidence, not a personality
term.

**Required behavioural change.** A person specified this way must be able to propose informal foreign
channels that others cannot propose, and must price sanctions risk from a different evidence base. If
their foreign sources are wrong, they must be able to be confidently wrong — which is the interesting
case, and the model must be able to produce it.

**Negative clause.** Foreign education must **not** be modelled as a competence bonus, a
cosmopolitanism score, or a disposition toward accommodation. It changes network, channels and
access. It must not add a term to any decision score directly. A build in which foreign-educated
persons are systematically more accurate has smuggled competence into an identity-adjacent
attribute and violates E-3.

### 4.3 Previous experience surviving political violence

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):264-269.

**Seeded attributes**

```text
life_history.traumatic_experiences[] → {event_ref: event:harbour-square-dispersal-year-11,
                                        category: political_violence, severity: 0.8,
                                        age_at: 24, resolved: false}
life_history.previous_crises[]       → {crisis_ref: …, role_held: bystander,
                                        outcome: personal_injury, lesson_tag: delay_is_dangerous}
```

**Step 1 — M8 EXPERIENCE-RECALL.** When a current event carries the category
`political_violence` or a specified adjacent category, M8 must retrieve the trauma record.
Retrieval probability rises with severity and with category match, and falls with elapsed sim time
— but the record must **never be deleted**, because the founder requires that formative experience
persist. This is a direct contradiction of the existing `AgentMemory` decay model
(`.../agent_schema.py:143-151`) and displaces it.

**Step 2 — M20 THREAT-SALIENCE.** Recall raises the weight on the hazard dimension of the current
assessment.

> State touched: `state.perceived_threat` must rise for this person **while the authoritative
> `state.exposure_to_danger` is unchanged**, because the objective hazard has not moved. Perceived
> and actual risk must be able to diverge, per person. That divergence is the point, and it is why
> 3.7 specifies the two as separate fields: M20 writes the perceived value only, and must never
> write the authoritative one.

**Step 3 — M9 PRESSURE-ACCUMULATION.** Elevated threat salience raises `state.stress`, which raises
the softmax temperature and shortens the effective time horizon.

**Step 4 — M1 DECISION-WEIGHTING.** Three composing effects:

```text
Feasible option set from M2 (identity-blind):
    { deploy_security_immediately, await_further_intelligence,
      deploy_with_restrictive_rules_of_engagement, negotiate_with_organisers, take_no_action }

    +  raised threat salience  → weight on rapid security options rises
    +  shortened time horizon  → discount on await_further_intelligence deepens
    +  recalled lesson_tag     → bounded negative term on delay-shaped options
```

**Required behavioural change.** The specified composition must produce lower tolerance for uncertain
intelligence and a raised probability of rapid security measures — exactly the founder's stated
chain. It must not make the person braver or more authoritarian: what must differ is their
perception of an identical situation, and their patience under perceived threat.

**Negative clause.** Trauma must **not** be modelled as a trait or a personality type, and must
never gate an option. `await_further_intelligence` must retain non-zero probability at every trauma
severity. Nor may trauma be modelled as degraded competence: it changes salience and horizon, not
capability. Note also that this specification requires trauma to be **resolvable** — the record
carries `resolved`, and a recorded resolution must be able to reduce retrieval weighting. A model
in which harm accumulates permanently and never abates would repeat the belief-ratchet defect the
audit found at the cohort tier ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
§5.9), where four of five demo cohorts fall to 0.0 and remain there with no recovery path in
existence.

---

## Part 5 — Current-state cadence

### 5.1 The three classes of change

| Class | Definition | Examples | Cadence |
|---|---|---|---|
| **Fixed** | Set at materialisation. May be corrected only by a recorded, audited amendment; never regenerated. | All of `identity` except `age`; all seeded `life_history` records. | Never, during a run. |
| **Accreting** | Append-only. Records are added; existing records are never rewritten. | New `life_history` entries; `psychology.perceived_grievances` onsets; `relationships.obligation_ledger` entries. | On event. |
| **Mutable** | Numeric or referential state that changes during the run. | All of `state.*`. | Per tick or per event — see 5.2. |

> **Rule P-6 (no parallel inputs).** Where a `psychology` attribute has a mutable `state`
> counterpart, **mechanisms must read the `state` field only**, and the `psychology` field is a
> materialisation-time **seed with no reader of its own**. Two live fields for one quantity would
> double-count it, and would let each field's Rule P-3 sensitivity test pass for the wrong reason —
> each appearing causal while the effect actually came from the other. A seed that acquires its own
> reader has become a duplicate and must be struck under Rule P-2.
>
> `psychology.loyalty` / `state.loyalty` is the instance this specification found in its own tables
> and has resolved (3.4, 3.7). Any further psychology/state pair introduced later is subject to the
> same rule, and the pairing must be declared explicitly rather than left to the reader to infer
> from a phrase like "mirroring its mutable counterpart", which is what concealed this one.

### 5.2 Per-tick versus per-event

> **⚠ Constrained by P0.7, and not resolvable until P0.7 lands.** P0.7 requires simulation time and
> horizon to be defined **before** saturation is touched, and forbids **arbitrary mean reversion**
> ([`../../HANDOFF.md`](../../HANDOFF.md) § Phase 0 priority order, P0.7 (`:89`)). Every rule in the per-tick table below is a
> decay-toward-baseline rule, which is mean reversion; and "per tick" has no defined meaning to
> specify against until P0.7 settles tick semantics. **These rules must therefore be re-derived from
> whatever P0.7 decides, not implemented as written.** They are recorded here to state the *shape* of
> the requirement — bidirectionality and a defined equilibrium — not its parameters or its cadence.
> Any baseline or decay constant in this table that is not derived from P0.7's time semantics is
> precisely the arbitrary mean reversion P0.7 exists to prevent.

**Per-tick (continuous processes).** These must be recomputed each tick by a declared rule, with no
triggering event. Every per-tick rule must be **bidirectional**: it must be able to move the value
in both directions and must have a defined equilibrium — where "defined" means derived from P0.7's
time and horizon semantics, never chosen to make a curve look plausible.

| Field | Per-tick rule (specified, subject to P0.7) |
|---|---|
| `state.fatigue` | Must accrue with activity load and must recover at a rate set by `capabilities.physical_health` and rest. |
| `state.stress` | Must decay toward a personal baseline, and must be raised by events, by `state.perceived_threat` and by unresolved pressure. Baseline and decay rate must come from P0.7. |
| `state.health` | Must apply age-conditioned drift and condition-specific progression. |
| `state.financial_pressure` | Must be recomputed from obligations, income and `state.available_resources`. |
| `state.exposure_to_danger` | Must be derived each tick from location, role, affiliations and active threats — **authoritative only. No psychological mechanism may write it.** |
| `state.perceived_threat` | Must be recomputed by M20 from `state.exposure_to_danger` plus recall, trauma and salience. It may diverge from the authoritative value and must not be reconciled to it. |
| `state.confidence` | Must decay slightly toward baseline between outcomes and must be stepped by recorded outcomes. Baseline and rate must come from P0.7. |

**Per-event (discrete, caused).** These must change **only** as the recorded effect of an event, and
each change must carry a causal reference to the event that produced it.

| Field | Changes on |
|---|---|
| `state.location` | Movement event. |
| `state.knowledge`, `state.beliefs` | Observation or communication event, via M3 → M4 → M5. |
| `state.rumours_heard` | Transmission event. |
| `state.recent_contacts` | Interaction event. |
| `state.current_intentions` | Decision event, or an event that invalidates the plan. |
| `state.current_role` | Appointment, dismissal, resignation or incapacity event. |
| `state.available_resources` | Expenditure, allocation or seizure event. |
| `state.public_reputation`, `state.private_reputation` | Publication, disclosure or outcome event. |
| `state.loyalty` | Betrayal, support, reward or humiliation event. |
| All `life_history` and `obligation_ledger` appends | The originating event. |

### 5.3 The write-path rule

> **Rule P-5.** No mechanism may mutate a person record in place. Every change to a mutable field
> must pass through the central transition mechanism and must emit an event carrying the full
> payload enumerated below. This is the CHARTER's eight-question standard
> ([`../../CHARTER.md`](../../CHARTER.md):118-130) applied to entity state — and a record that
> answers only "what changed, when, and which rule" would **not** meet that standard while claiming
> to, which is this project's characteristic defect reproduced at the specification layer.

**The required payload, against all eight charter questions and the founder's six.** The mapping is
set out explicitly because the gap is otherwise easy to miss:

| Charter question (`CHARTER.md:118-130`) | Required field on the entity-transition event |
|---|---|
| 1. What happened? | The field changed, its prior value and its new value. |
| 2. What caused it? | Reference to the causing event, and to the person or mechanism that initiated it. |
| 3. Which rule or mechanism applied? | Mechanism ID (M1–M20) and the specific rule within it. |
| 4. Which actors reacted? | Entity references for every person or organisation whose state changed in the same transition. |
| 5. What assumptions were used? | The **parameter set and rule-pack version in force**, by version identifier. |
| 6. What uncertainty existed? | The distribution drawn from, the `temperature` and `ε` in force, and the **named RNG substream and index consumed** (Part 1.3). |
| 7. What alternative outcomes were possible? | **The feasible set `O` considered, with each option's `score(o)` and resulting `P(o)` at decision time.** |
| 8. What future options changed? | Options opened or closed by this change, including any M2 gate refusal with its E-1d provenance chain. |

Two further fields are required by the source record
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):289-291) and are not
covered by the charter's eight:

| Founder question | Required field |
|---|---|
| What evidence did the entity observe? | The M3 observation records that supplied the evidence, by reference. |
| Which prior experiences shaped the reaction? | The life-event records M8 retrieved, and the weight each contributed. |

**None of this is expensive to capture, which is why omitting it would be indefensible.** E-2 already
computes the feasible set and a score per option at every decision point; M3 already determines what
the person observed; M8 already selects the retrieved experiences. Alternatives and observed
evidence are **in hand at write time**. The requirement is only that they be persisted rather than
discarded.

**This requirement lands on P0.6, not beside it.** These fields are the entity-layer payload that
P0.6's central transition mechanism must be able to carry. They must be specified as a requirement
*on* P0.6 rather than invented as a parallel entity-only event format, which would produce a second
event path and guarantee the two disagree.

**This displaces the current write path rather than extending it.** Today `cohort_agent.py:38`
writes `b.government_competence` directly on a live Pydantic object, with no event, no cause and no
recovery path. `engine.py:164` applies deltas and logs the *requested* effect rather than the
realised one — over 120 ticks at seed 88213, summed `military_readiness` effects imply 1.59 against
an actual 1.0 ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §6.15).
Person-level event sourcing built on that path would inherit both defects.

**Two further dependencies.**

1. **The only existing delta path cannot reach nested state.** `apply_deltas`
   (`scaffold/backend/app/simulation/agents/macro_state.py:23-47`) applies top-level scalars only:
   it skips nested blocks (`:40-41`) and unknown keys (`:37-38`) in silence. A person record is
   inherently nested, so a person-affecting effect written through that path would produce no error,
   no warning and no symptom. The person model must use a different write path, and P0.6 must
   supply it.
2. **The event log is currently client-forgeable.** `routes_simulation.py:81` binds the whole
   `Intervention` model from the request body and `:91-100` writes `model_dump()` verbatim into the
   event log; A3 §5 drove this through the real API and confirmed a client can assert its own
   `legal_check` and mint the event identifier. An entity history built on that log would inherit
   forgeable provenance. Splitting the wire model from the state model is a precondition.

### 5.4 Snapshot placement

`StateSnapshot` (`scaffold/backend/app/db/models.py:42-53`) already reserves a `meso_state` JSON
column (`:51`) that nothing writes. That is the natural landing site for entity-tier state, and this
specification should extend it rather than introduce a parallel store. Note that nothing is ever
written to any of the three persistence tables today
([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.14), and that no RNG
state is captured in any snapshot — so a fork from a snapshot, as ADR-003 describes, would resume
the generator at position 0 and diverge from its parent silently.

---

## Part 6 — Portraits and visual identity

Source: [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):194-208.

### 6.1 The governing statement

> **Portraits are PRESENTATION-ONLY.** No mechanism in Part 3 may read `identity.portrait_ref` or
> any portrait metadata. No portrait may influence any simulation outcome, ever. The founder is
> explicit: "Portraits are presentation. The underlying identity must still be structured data."
> ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):208.)

The portrait is a **rendering of** the structured record. The record must never be a rendering of
the portrait. If a portrait shows a detail absent from the record, that detail is not true in the
simulation and nothing may act on it.

### 6.2 Progression

The founder's staged progression (:196-199) is adopted as the intended order of work: abstract
avatars during early development; consistent illustrated portraits; generated fictional faces with
multiple expressions or context states; later, visual variation for age, injury, role and
circumstance. **No stage is scheduled.** Stage one is the correct target if any of this is ever
started, because it satisfies stable visual identity at negligible cost and creates no
likeness risk.

### 6.3 Requirements on the asset

| Requirement | Specification |
|---|---|
| **Stable visual identity** | A person's portrait must not change between sessions, between runs of the same scenario, or on reload. This must be guaranteed by construction — generation is one-time and the result is stored — never by re-running a generator and hoping for the same output. |
| **One-time deterministic generation** | The portrait must be generated once from a **stable entity specification**: a declared, ordered, versioned projection of specific person fields. The projection must be explicit, so that it is knowable which record changes could ever alter a portrait. |
| **Regeneration is forbidden by default** | Once generated and stored, a portrait must not be regenerated. Changes to fields outside the stable specification must not affect it. Regeneration must require an explicit, recorded, audited action. |
| **Versioning** | Every portrait asset must carry a version. Expression variants, context states and age progressions must be **new versions with a common lineage**, never in-place replacements. The historical asset must remain retrievable, so a dossier viewed at an earlier tick can render correctly. |
| **Provenance and generation metadata** | Each asset must record: generator identity and version, prompt or parameter set, the stable entity specification hash it was generated from, the substream name and index consumed, generation timestamp, and the human review status. Without this the asset's origin is unauditable. |
| **Clearly fictional** | The asset must be clearly fictional and must not be derived from, or intentionally resemble, a real person. See the enforcement gap below. |
| **Consistency** | The portrait must be consistent with `identity.age`, geography implied by `place_of_birth` and `current_residence`, family resemblance across `identity.family` edges, and visible life-history facts. Consistency must be a checkable property of the stable specification, not a matter of taste. |
| **Provenance tag at the interface** | Every generated asset must carry a visible provenance tag distinguishing it from engine-computed fact, at the interface and not merely in documentation ([`../../CHARTER.md`](../../CHARTER.md):141). |

### 6.4 The RNG substream dependency

Deterministic one-time generation is **not currently possible**, for two separate reasons, both
stemming from the single shared RNG at `engine.py:83`:

1. **Generation would perturb the simulation.** Portrait generation consumes draws. On a shared
   stream, those draws shift every subsequent draw in every subsystem. A3 §6 demonstrated the effect
   with a single added draw. National indicators would move because a portrait was generated.
2. **The portrait would not be stable.** Draws taken from a shared stream depend on global draw
   order, which depends on everything that happened before. The same person materialised at a
   different tick, or after a branch, would receive a different face — violating the stable-visual-
   identity requirement outright.

The specification is therefore that portrait generation must draw from a **named substream keyed on
stable inputs only**: run seed, `person_id`, and a purpose tag such as `portrait.v1`. Generation must
be independent of global draw order and must consume nothing from any other subsystem's stream.

Adopting named substreams supersedes ADR-007's recorded single-RNG decision and affects determinism
and authoritative state, so it requires owner approval per
[`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:139-140`). It is not a decision this document may take. It is
recorded as an open question in Part 8.

### 6.5 The enforcement gap

"Clearly fictional, not derived from or intentionally resembling a real person" is currently a
**stated intention with no enforcement mechanism specified anywhere**. This document does not
resolve it, and flags it plainly:

- No asset store exists in the project.
- No asset reference field exists in any schema.
- Nothing validates entity names against real people; `CHARTER.md:137` forbids real individuals and
  nothing checks it ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
  §5.12).
- The scenario's own `fiction_disclaimer` (`kestral-strait.json:7`) is read by nothing and appears in
  no API response or interface.

Portrait generation adds a **new likeness risk** that the current codebase does not have, because it
does not generate images at all. What enforces the fictional-likeness requirement — a review gate, a
similarity check, a restriction on generator choice, a prohibition on reference images, or a
combination — is an owner decision that **remains open**, and the settled B5 decision raises its
priority rather than answering it: control **B5-4** requires that real persons cannot be entities in
the first place, and a portrait that resembles a real person is a route by which a nominally
fictional entity acquires a real likeness. Because B5-8 makes technical enforcement mandatory, this
cannot be discharged by a stated intention. It should be settled before any portrait pipeline is
designed, not after.

---

## Part 7 — Safety coupling: B5 / P0.8 (DECIDED)

**B5 is decided.** The founder settled it on 18 July 2026, and it must not appear anywhere in this
document, or any sibling, as an unresolved owner decision. What this section records is therefore a
**constraint this specification is already bound by**, not a question it is waiting on.

**The important consequence, stated first.** B5 no longer clears by an owner decision. It clears
only when the eight controls below are **implemented and verified**, because the founder ruled that
disclosure and any future acceptable-use language are **supplementary** and that **technical
enforcement is mandatory**. The publication gate is therefore **larger** than it was, not smaller,
and the earlier framing in
[`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md):245-248 — four
blockers clearing by text correction, only B5 needing a decision — is superseded.

**None of the eight exists.** Every row below is a requirement on a future architecture. There is
no `world_mode` field, no scenario schema (audit §5.13), no scenario-load validation, no entity
validation, no targeting gate, and no interface of any kind on which a disclosure could appear.

| # | Required control | Where it bears on the person model |
|---|---|---|
| B5-1 | Influence mechanics operate **only** in explicitly fictional worlds | A person may be an audience or a messenger only within a fictional world. |
| B5-2 | The scenario loader **requires** `world_mode: fictional` and **fails closed** without it | Seeded person records arrive through scenario load; the check must precede their construction. |
| B5-3 | Real-world scenario import remains **disabled** | No import path may create person entities. |
| B5-4 | Real persons, organisations and political populations may **not** be influence-target entities | Directly binding: this document specifies named individuals with structured identity, media reach and social graphs. Every one must be fictional. |
| B5-5 | Protected characteristics may **not** be optimisation criteria for persuasion or manipulation | The binding constraint on 3.2's sensitive-identity fields and on `psychology.susceptibility_to_pressure`. Mechanised as E-3, E-3b and the E-4 lint. |
| B5-6 | Fictional **aggregate** narrative diffusion, exposure, adoption and counter-messaging **remain allowed** | A permission. The M3 / M10 / M19 exposure and reach chains are not in question; what is prohibited is optimising them against protected traits. |
| B5-7 | API and UI **disclose** that the active world is fictional | Owned by [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md), which is where a person dossier would be served. |
| B5-8 | Technical enforcement is mandatory; disclosure and acceptable-use wording are supplementary | No control above may be discharged by writing a document. Including this one. |

*(B5-1 to B5-8 is a label adopted so the controls can be cited precisely across the world-model set.
The founder's decision text is the authority; the numbering is not.)*

### 7.1 The permitted / not-permitted line, as it binds this document

> **Permitted:** identity affects lived experience, relationships, discrimination, institutional
> access, media exposure and cultural interpretation.
>
> **Not permitted:** identity acts as an inherent competence, morality, loyalty, violence or
> manipulability coefficient.

The not-permitted list adds three categories to the source record's "competence, morality or
intelligence" (:305-306) — loyalty, violence and manipulability — and E-3b is where this document
mechanises the widening. **It is an addition, not a replacement.** The decision's phrasing does not
repeat *intelligence*, and that omission must not be read as a permission: the source record's
prohibition on identity acting as an inherent **intelligence** coefficient stands undisturbed,
because the decision does not contradict it and the source record governs wherever the decision is
silent. The operative prohibited set is therefore all six — competence, morality, intelligence,
loyalty, violence and manipulability — and E-3's second forbidden line ("any capability, trait,
competence or morality field") is the line that carries intelligence. The campaign model **may** use non-sensitive factors — geography,
institutional affiliation, economic exposure, political behaviour, media consumption — where the
fictional scenario justifies them; it **must not** optimise against protected traits. Those
permitted factors correspond to `identity.current_residence`, role occupancy and
`capabilities.institutional_access`, `state.financial_pressure` and
`capabilities.financial_resources`, `life_history.political_involvement`, and
`capabilities.media_reach` respectively. The protected traits correspond to
`identity.ethnic_identity`, `identity.cultural_identity`, `identity.religious_identity`,
`identity.nationality`, `identity.languages` and the class field in
`life_history.family_wealth_and_class`.

**A boundary this document cannot police on its own.** Several permitted factors are *correlated*
with protected traits by construction — residence with ethnicity where segregation is modelled
(M17), media consumption with language (M19). A campaign model optimising on the permitted proxy
can therefore approximate optimisation on the protected trait without ever reading it, and the E-4
lint, which is a static check on field references, would not see it. Detecting proxy optimisation is
a measurement problem of the same family as E-5b's residual, and it belongs to
[`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md). It is
recorded here so the gap is visible rather than assumed closed, and raised in Part 8.

### 7.2 What the person model contributes to the surface

The person model refines targetable audience attributes from five aggregate cohorts to named
individuals with structured identity, media reach, social graphs and portraits. Concretely, the
audit's dual-use finding (§5.12) rests on `InfluenceSusceptibility`
(`.../agent_schema.py:72-78`), `MediaExposure` (`:42-53`) and `Demographics` including
`religion_majority` and `primary_language` (`:22-28`), paired with campaign design fields at
`:312-346`. This document specifies:

- Per-person ethnic, cultural and religious identity, with salience and concealment
  (`identity.ethnic_identity`, `identity.cultural_identity`, `identity.religious_identity`).
- Per-person media reach and habitual platforms (`capabilities.media_reach`).
- Per-person grievance records with named targets (`psychology.perceived_grievances`).
- Per-person structured fears with named referents (`psychology.personal_fears`).
- A directed social graph with leverage and obligation dimensions.
- A stable portrait per person.

**The dual-use surface this creates is strictly larger than the one B5 was originally raised on**,
and the decision does not shrink it. Each item above must sit inside the envelope of 7.1 and behind
the controls of the table above.

**The earlier recommendation is spent.** A previous revision of this section recommended holding
identity-attribute detail deliberately coarse *until B5 is decided*. B5 is decided, so that
holding pattern no longer applies — and it must not be replaced with a licence to specify freely.
The constraint that replaces it: identity attributes may be specified in whatever detail the
permitted list of 7.1 supports, and must not be specified in any form that serves the
not-permitted list or supplies an optimisation criterion under B5-5. The level of detail is no
longer the safety control; **the eight controls and the E-3/E-3b/E-4/E-5 machinery are**, and none
of them is built.

**Consistent with the charter.** The founder's preference for fictional cultural, ethnic and
religious identities in the default scenario
([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):315-316) is consistent
with [`../../CHARTER.md`](../../CHARTER.md):137, which forbids real nations, organisations and named
individuals. Note that the existing demo scenario mixes a real-world religious label,
`"sunni-mixed"`, into four of five cohorts (`kestral-strait.json:45, :85, :168, :208`) alongside
fictional ones such as `"highland-traditional"` (`:128`). Whether that is replaced is an owner
decision on existing scenario data, recorded in Part 8, and not resolved here.

**Also note:** the founder's design rule at :305-306 is a *design rule*, not enforcement. E-3, E-3b,
E-4 and E-5 in Part 2 are this document's proposed mechanical form of it. **They do not exist** —
and under control B5-8 that gap is now the thing standing between this specification and
publication, not a refinement to be scheduled later.

---

## Part 8 — Open questions for the owner

AI agents may draft records but may not approve decisions
([`../../HANDOFF.md`](../../HANDOFF.md) § Standing constraints (`:138`)). Every item below requires a human choice and is
deliberately left unresolved.

> **Amended 19 July 2026.** Three questions this document had not raised as numbered items — who owns
> observation, who owns role authority, who owns faction alignment — were **answered** by founder
> rulings 1A, 1B and 1C. They are recorded in the amendment record at Part 3.0a rather than added
> here as resolved items, because they were never numbered questions in this list. Four questions are
> **added** below (13, 14, 15, 16). Three of the four are consequences of the rulings: applying them
> made visible what they did not cover. No existing item 1–12 is removed or renumbered.

1. **Person as a first-class entity, or `MicroAgent` extended in place?** These have different
   migration costs and give different answers to "what happens when a minister is replaced". This
   document assumes separation of person from role occupancy; that assumption needs confirmation.
2. **Deterministic randomness — narrowed 19 July 2026; the placement sub-question is answered.**
   The founder decision of 18 July 2026 added this to Phase 0 as a new item, **P0.4A**, between P0.4
   and P0.5, and ruled out folding it into P0.6 or deferring it to the replacement architecture.
   Deterministic profile generation, stable identity, portrait stability and tier promotion remain
   unbuildable until P0.4A passes, and A3 §6 establishes the shared stream as a latent
   reproducibility hazard independent of any entity work. **Still for the owner:** the mechanism —
   stateful named substreams or keyed / counter-based deterministic draws
   ([`../adr/ADR-010-deterministic-randomness-architecture.md`](../adr/ADR-010-deterministic-randomness-architecture.md)
   is drafted, *Proposed* and unapproved) — the key scheme's ownership, and whether the ADR
   supersedes or narrows ADR-007. Note that the old sub-question "per entity, per entity type, or
   per subsystem" understates the requirement: isolation is required by subsystem, entity,
   relationship or interaction, purpose, and tick or event context, and **per-entity streams alone
   are insufficient**. Determinism-affecting; owner approval required.
3. **Does P0.4 treat micro-tier entity state as authoritative, or as derived from macro?** This
   document's position — that only authoritative reality is authoritative state, and
   self-understanding, public profile and player intelligence profile are derived — needs explicit
   confirmation, because it constrains snapshot shape and replay. A sub-question: is the entity's
   self-understanding authoritative in its own right, since it is a fact about what the entity
   believes?
4. **Is the rejection rule (P-2) adopted?** That is: any specified attribute with no named reading
   mechanism is **struck, not deferred**. Audit §5.10 is the empirical case for it. This is a
   specification-process decision, not a technical one.
5. **Is the sensitivity-test obligation (P-3) and its CI enforcement (P-4) accepted as a cost?** It
   is roughly one test per attribute, against a project that currently has five tests in total and
   no invariant tests at all.
6. **B5 / P0.8 is DECIDED and is not re-opened here.** The residual question is a measurement one,
   and this document cannot answer it: **what detects a campaign model optimising on a permitted
   non-sensitive factor that is a close proxy for a protected trait?** (Part 7.1.) Residence
   correlates with ethnicity wherever M17 models segregation; media consumption correlates with
   language through M19. The E-4 lint is a static check on field references and would pass such a
   build. Who owns the detection method — the residual decomposition of E-5b, a separate proxy
   audit, or a restriction on which factors a campaign may optimise over at all — is an owner
   decision. **Do not read this as re-opening B5.**
6a. **May a legal-status gate be conditioned on citizenship or nationality?** This is the one
   unresolved inconsistency inside the safety model, and it is stated plainly rather than papered
   over. Nationality is named as a sensitive identity attribute by the source record
   ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):300), so E-3 forbids it
   the *weaker* use of a bounded term in `score(o)`. But real legal systems condition office,
   clearance and asset ownership on citizenship, and forbidding that outright makes a dual-national
   minister — an interesting and legitimate scenario — inexpressible. Granting it means permitting a
   sensitive identity attribute the *stronger* use of removing options outright. Options: (a) permit
   it only via a `legal_status` entry derived from an enumerable scenario law, as E-1a currently
   provides as the conservative default; (b) forbid it entirely and model such exclusions as M17
   discrimination events instead, which keeps E-1b clean at the cost of expressiveness; (c) permit
   it and explicitly except it from E-1b, which weakens the invariant. **Owner decision. Not taken
   here.**
6b. **Is a mechanism allocated for "cultural interpretation of ambiguous events" (provisionally
   `M21 AMBIGUITY-INTERPRETATION`), or does it remain struck?** The source record names it as a
   permitted effect of cultural identity (:305-306), and the settled B5 decision **restates cultural
   interpretation on the permitted side of the line** (Part 7.1) — so the question is no longer
   whether the effect is allowed. It arrived with no mechanism, no stated inputs and no bound, so
   Rule P-2 struck it from the permitted-effects list (Part 3.2) for want of a reader, not for want
   of permission. Permission does not supply a mechanism, and the strike stands until one is
   specified. Specifying
   it means specifying what it reads, what it writes, and how it is bounded under E-2, E-3a and
   E-5b — on the most safety-sensitive row in the document. Leaving it struck means declining a
   named founder requirement. **Owner decision.**
7. **What enforces "clearly fictional, not resembling a real person"** for generated portraits, and
   who reviews? No asset store, no asset reference field and no name validation exist. **Still
   open, and now load-bearing:** it is a component of control B5-4, and B5-8 forbids discharging it
   with a stated intention (Parts 6.5 and 7).
8. **Is `"sunni-mixed"` (`kestral-strait.json:45, :85, :168, :208`) replaced with a fictional
   identity?** The founder's stated preference and `CHARTER.md:137` point one way; it is existing
   scenario data and the choice is the owner's. **The settled B5 decision sharpens this rather than
   settling it:** the label is a real-world religious identity carried by cohorts in a scenario that
   also contains a hidden influence campaign with `target_cohorts` (`:389-418`). Whether that
   arrangement is compatible with control B5-5 depends on whether the campaign's targeting ever
   reads the identity field — which nothing currently checks, because no such check exists. Owner
   decision on the data; the check itself is required work under B5-5 regardless of the answer.
9. **Is `"bios/oduya.md"` (`kestral-strait.json:268`) an intended future artefact, or a dangling
   reference to be removed** once structured identity replaces prose biography?
10. **How much of the ~80 attributes above survives the causal-value test in the owner's judgement?**
    This document proposes a rejection list in Part 9. Accepting, extending or overriding it is an
    owner decision.
11. **Does the size of this record justify building the schema-mirror generator first?** Nine JSON
    Schema mirrors and the SQLAlchemy models are hand-maintained with no generator and no sync test.
    A sequencing decision outside Phase 0.
12. **Does Mesa remain the agent substrate?** This document is deliberately substrate-neutral, which
    keeps the decision open but defers it.
13. **Who owns the access and role-authorisation layer — which human player may open which record?**
    **Raised 19 July 2026 while applying ruling 1A.** The ruling separated four things that Part 1.3
    previously treated as one: observation opportunity
    ([`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md)), view production
    ([`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2), dossier presentation
    ([`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md)), and player
    access control. The first three now have owners. **The fourth has none: no document specifies it
    and no code implements it** ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md)
    §7). The prerequisite is therefore worse than Part 1.3 previously recorded — not merely unbuilt,
    but unowned. Note that founder decision 4 of 19 July 2026 **retains** the standing position and
    takes no new decision: authoritative reality exists internally; players ordinarily receive role-,
    access-, evidence- and confidence-filtered projections; there is no automatic omniscient
    browsing; whether any privileged role may receive fields equivalent to authoritative reality
    remains an explicit later owner decision; and **a clearance-gated projection must not be
    described as a raw ground-truth read.** This item asks only who owns the layer, and must not be
    read as re-opening any of that.
14. **Is M3 INFORMATION-EXPOSURE retired, re-scoped, or retained alongside `M-OBS-EXP` and
    `M-OBS-ACQ`?** **Raised 19 July 2026 while applying ruling 1A.** M3 is defined in this document's
    register as "determine which events and claims a person observes, at what fidelity, with what
    delay". That is coextensive with `M-OBS-EXP` (who is in a position to observe) and `M-OBS-ACQ`
    (directness, latency, fidelity, degradation), which ruling 1A assigns to
    [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) and names the sole
    writer of `Observation`. The ruling did not mention M3, so **this document has not retired it**:
    withdrawing a mechanism this document owns is an owner decision, and the standing rule against
    duplicating a mechanism across documents cuts both ways. M3 is cited at `identity.place_of_birth`,
    `identity.current_residence`, `identity.languages`, `life_history.education[]`,
    `life_history.migration_and_travel[]`, `psychology.religious_commitment`,
    `capabilities.institutional_access[]`, `state.location`, `state.recent_contacts[]` and
    `state.current_role`, and throughout the Part 4 chains. Options: (a) retire M3 and repoint every
    citation to `M-OBS-EXP` / `M-OBS-ACQ`; (b) re-scope M3 to the person-side inputs only —
    residence, language, network position, access — with the observation itself owned elsewhere;
    (c) retain both and state the boundary, which risks exactly the duplication ruling 1C forbade for
    M14. **Owner decision. Not taken here.**
15. **Where does per-person dissent and defection probability sit after the M14 split?** **Raised
    19 July 2026 while applying ruling 1C.** The ruling places faction structure with
    [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) and the directional person-to-faction alignment
    edge with [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md). The superseded M14 definition also
    carried "and their dissent or defection probability", which the split does not unambiguously
    place: it is a probability attached to a **person**, computed from an **edge**, against an
    **organisational** position. It is cited here at `psychology.values[]`,
    `psychology.attitude_to_authority` and `state.loyalty`. **The risk is not that it lands in the
    wrong document but that all three assume another holds it**, which is how
    `represents_population` came to be read by nothing at all
    ([`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) §5.10). **Owner
    decision.**
16. **What mechanism resolves harm events?** **Raised 19 July 2026 while checking the Part 3.7
    mapping.** `state.exposure_to_danger` names two readers: M20, and the prose phrase "harm-event
    resolution". The second has no identifier, appears in no register, and is owned by no document.
    After rulings 1A, 1B and 1C it is the **only** row in 3.7 whose mapping does not resolve to a
    mechanism with a named owner. Rule P-1 requires every mapped attribute to name a mechanism that
    reads it, and Rule P-2 strikes anything unmapped — so on this document's own rules the phrase
    must either become a specified mechanism with an owner or the mapping must be struck. Allocating
    an identifier is an owner decision; note that `M21` is already provisionally reserved for
    `AMBIGUITY-INTERPRETATION` under open question 6b, and `M12` is retired and must not be reissued.
    **Owner decision.**

---

## Part 9 — Consolidated PRESENTATION-ONLY and unmapped register

This is the fake-depth guard made explicit. Everything listed here is either forbidden from touching
the simulation, or conditional on structure or on a mechanism that does not exist.

### 9.1 PRESENTATION-ONLY — must never be read by any state-changing mechanism

| Attribute | Why it is presentation-only |
|---|---|
| `identity.name` | A display label. No mechanism reads a person's name; every mechanism keys on `person_id`. |
| `identity.date_of_birth` | `identity.age` carries all specified causal load. Exact date has no reader unless a records-matching or document-verification mechanism is later built. |
| `identity.physical_appearance` | No mechanism reads appearance. Conditionally promotable (see 9.2). |
| `identity.portrait_ref` and all portrait metadata | Stated by the founder ([`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md):208). Part 6 forbids any mechanism from reading it. |
| Generated biography prose, dossier narrative, in-character dialogue | Rendered from the structured record; never an input. E-6. If a fact appears only in prose, it is not true in the simulation. |

### 9.2 CONDITIONAL — mapped only under a stated condition, otherwise presentation-only

| Attribute | Condition |
|---|---|
| `life_history.achievements[]` | Mapped **only** when structured with a verifying organisation reference and a public flag, feeding M4, M10 and `M-OBS-SURF` (**repointed 19 July 2026, ruling 1A; was M12**). Free-text achievements have no reader and are presentation-only. |
| `psychology.personal_fears[]` | Mapped **only** with a structured referent that M20 can match against a current event. Free-text fears are presentation-only. |
| `identity.physical_appearance.distinctive_features[]` | Promotable to feed `M-OBS-ATTR` (**repointed 19 July 2026, ruling 1A; was M12**) **only if** a witness-identification or disguise mechanism is built. Until then, presentation-only. |
| `psychology.values[]`, `psychology.political_beliefs[]`, `psychology.long_term_aspirations[]` | Mapped **only** against bounded, scenario-authored, machine-readable vocabularies. As free text they are prose and Rule P-1 strikes them. |
| `life_history.childhood_environment` | Mapped **only** as structured fields. As a prose paragraph it has no reader. |

### 9.3 Attributes at risk — mapped, but on thin mechanisms

Flagged for owner attention because their mapping depends on machinery that is itself only
specified, or because the mapping is weak enough that Rule P-3's sensitivity test may fail:

- `psychology.empathy` — mapped to M1 and M7, but its distinct contribution beyond
  `psychology.values` needs demonstrating.
- `psychology.religious_commitment` — permitted effects are indirect only (E-3), so its sensitivity
  test must measure network and exposure change, not decision change. Easy to build wrongly.
- `identity.cultural_identity` — its permitted effects are now M6, M17 and M19/M3 only. The
  "cultural interpretation of ambiguous events" effect named in the source record has been **struck
  under Rule P-2** (Part 3.2) because it arrived with no mechanism identifier and no bound. Listing
  it here as merely "at risk", as an earlier draft did, would have exempted the most
  safety-sensitive row in the document from the rule enforced everywhere else. Whether to specify
  it properly as `M21` is open question 6b.
- `life_history.migration_and_travel[]` — real causal load, but it overlaps heavily with `education`
  and `employment_history`. May not survive a distinct sensitivity test.

### 9.4 Fields deliberately not carried forward

- `corruption_susceptibility` (exists at `.../agent_schema.py:128-130`) — re-expressed as a bounded
  term over `psychology.values` and `state.financial_pressure`, so susceptibility to inducement is a
  consequence of circumstance rather than a fixed personal constant. A standing "corruptibility"
  scalar invites exactly the essentialism E-3 forbids.
- `AgentMemory.decay_rate` (exists at `.../agent_schema.py:149-151`) — displaced. Recency modulates
  M8 retrieval probability; it must never delete a formative record.
- `capabilities.social_influence` as a stored scalar — computed from the relationship graph instead.
  A stored value would be unfalsifiable and would drift from the graph.
- `relationships.trusted_sources[]` as stored state — a derived view over out-edges.
- `psychology.loyalty` as a **live input** — retained only as the materialisation-time seed for
  `state.loyalty`, with no reader of its own (Rule P-6). An earlier draft specified both at the same
  resolution with overlapping readers and no composition rule, which would have double-counted
  allegiance in M1 and M14.
- `state.exposure_to_danger` as a **single field carrying both objective and perceived hazard** —
  split into the authoritative `state.exposure_to_danger` and the self-understanding
  `state.perceived_threat` (3.7). One field could not be both derived from world facts each tick and
  raised by trauma recall.
- "Cultural interpretation of ambiguous events" as an **unmapped permitted effect** of ethnic,
  cultural and religious identity — struck under Rule P-2 (3.2). Open question 6b covers whether it
  returns as a specified, bounded mechanism.

---

## Cross-references

**Source record and governance**

- [`FOUNDER-REQUIREMENT-2026-07-18.md`](FOUNDER-REQUIREMENT-2026-07-18.md) — the authority for this
  document.
- [`../../CHARTER.md`](../../CHARTER.md) — the eight-question standard and the determinism boundary.
- [`../../HANDOFF.md`](../../HANDOFF.md) — Phase 0 order, standing constraints, approval boundaries.
- [`../delivery/CURRENT-STATE-AUDIT.md`](../delivery/CURRENT-STATE-AUDIT.md) and
  [`../delivery/A3-VERIFICATION-RESULTS.md`](../delivery/A3-VERIFICATION-RESULTS.md) — the closed
  audit. Cited throughout for what exists and what does not.

**Sibling world-model documents**

- [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) — the common entity ontology, the shared identifier
  namespace, and the four-view model this document's fields sit inside. This document assumes its
  entity-reference conventions.
- [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md) — **added 19 July 2026
  (ruling 1A).** Owns observation and evidence emission: `M-OBS-EXP` (exposure and observation
  opportunity), `M-OBS-ACQ` (acquisition, relay and degradation, and sole writer of `Observation`),
  `M-OBS-ATTR` (source attribution and identity resolution) and `M-OBS-SURF` (observable surface).
  The successors to this document's retired M12. It does **not** own belief updating, knowledge
  storage, dossier rendering or player access control.
- [`ORGANISATION-MODEL.md`](ORGANISATION-MODEL.md) — role occupancy and institutional authority
  (M13, **confirmed by ruling 1B**); faction definitions, membership rules, formal positions and
  faction structure (**the structural half of the M14 split, ruling 1C**). Also owns `InstitutionState`
  and institution lifecycle, an institution being a specialised organisation for current scope. The
  counterpart to Part 1.2's separation of person from role.
- [`RELATIONSHIP-GRAPH.md`](RELATIONSHIP-GRAPH.md) — owns the directed edge, its twelve dimensions,
  its history and M6/M7, and — **per ruling 1C** — the directional, historied person-to-faction
  alignment and loyalty relationship and its changing strength. Part 3.6 defers to it, and Parts 3.3,
  3.4, 3.5 and 3.7 **consume** the alignment projection without owning it.
- [`BELIEF-AND-KNOWLEDGE-MODEL.md`](BELIEF-AND-KNOWLEDGE-MODEL.md) — owns `state.knowledge`,
  `state.beliefs` and M5. Depends on P0.6 exactly as this document does.
- [`POPULATION-FIDELITY.md`](POPULATION-FIDELITY.md) — owns the fidelity tiers, promotion and
  demotion (M15) and influence weighting (M11). The successor to P0.5; this document must not
  duplicate it.
- [`../design/ENTITY-PROFILE-EXPERIENCE.md`](../design/ENTITY-PROFILE-EXPERIENCE.md) — the ten-tab
  dossier. **Amended 19 July 2026 (ruling 1A):** this entry previously read "the ten-tab dossier and
  the player intelligence profile (M12)". That document specifies **presentation only**. Observation
  is a simulation mechanism owned by
  [`OBSERVATION-AND-PERCEPTION-MODEL.md`](OBSERVATION-AND-PERCEPTION-MODEL.md); the design document
  neither owns nor implies it, and any assignment of an observation mechanism to it is a defect. View
  production is [`ENTITY-ONTOLOGY.md`](ENTITY-ONTOLOGY.md) §9.2. It remains the read surface over
  this record, and Part 7's control B5-7 still lands on it.
- [`../safety/IDENTITY-AND-BIAS-GUIDELINES.md`](../safety/IDENTITY-AND-BIAS-GUIDELINES.md) — owns
  the swap test (E-5), the bias thresholds, and the settled B5 envelope stated in Part 7 — including
  the widened not-permitted list mechanised as E-3b and the unresolved proxy-optimisation question
  (Part 7.1, open question 6).

---

**END — SPECIFICATION, NOT IMPLEMENTED. BACKLOG. Does not interrupt Phase 0.**
