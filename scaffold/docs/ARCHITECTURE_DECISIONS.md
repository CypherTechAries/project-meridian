# Architecture Decision Record (ADR) — MERIDIAN

Short ADR-style log of the stack choices made during the research phase (see
`research_architecture.md`, `research_licensing.md` in the workspace root). Each decision is
recorded here so future contributors — human or AI — inherit the *why*, not just the *what*.

Status legend: **Accepted** = committed for v1; do not re-litigate without a new ADR.

---

## ADR-001 — Backend: Python 3.11+ / FastAPI / Pydantic v2
**Status:** Accepted.
The simulation core, ABM libraries, and LLM tooling are all strongest in Python. FastAPI gives
async REST + native WebSocket support and auto-generated OpenAPI docs with minimal ceremony.
Pydantic v2 is the schema source of truth — its models generate the JSON Schema mirrors in
`/schemas` and validate every object crossing the API and LLM boundaries.

## ADR-002 — Simulation engine: Mesa (Apache-2.0)
**Status:** Accepted.
Mesa is a mature, permissively licensed (Apache-2.0) agent-based-modelling framework. It gives
us a `Model`/`Agent` structure and scheduling without inventing our own. We use it for the
meso (cohort) and micro (institutional) tiers; the macro tier is a plain seeded rules object,
not an agent, because national aggregates are not usefully modelled as a stepped agent.
Rationale for permissive licence: the product may be commercialised — GPL engines were ruled
out in `research_licensing.md`.

## ADR-003 — Database: PostgreSQL via SQLAlchemy 2.0
**Status:** Accepted.
We persist three things: `simulation_run` (seed + scenario), immutable `state_snapshot` per
tick, and an append-only `event_log`. JSON columns store schema objects verbatim so the DB is
generic across nation archetypes (data, not code — see ADR-007). Snapshots make scenario
branching and Monte-Carlo batch runs cheap: fork from any tick. SQLAlchemy chosen over raw SQL
for typed models that mirror the Pydantic schemas.

## ADR-004 — LLM gateway: LiteLLM-ready, stubbed by default (MIT)
**Status:** Accepted.
`llm_gateway.py` is an interface, not an implementation, in the scaffold: it returns canned
text so the system runs with **no API keys**. LiteLLM (MIT) is the intended router because it
exposes one interface over local *and* frontier models — micro-agent reasoning can go to a
cheap/local model while briefings go to a frontier model, tuned per call. Swapping the stub for
real calls is a localized change to one module.

## ADR-005 — Real-time: FastAPI WebSocket now, Socket.IO-ready
**Status:** Accepted.
Tick broadcast uses a plain FastAPI WebSocket endpoint for the scaffold (zero extra infra).
`python-socketio` is already a dependency so a full build can move to rooms/namespaces for
multi-player shared runs without changing the engine. The engine is transport-agnostic: it
exposes `step()` and `macro_snapshot()`; the transport layer decides how to broadcast.

## ADR-006 — The determinism boundary (the load-bearing decision)
**Status:** Accepted. **Do not weaken.**
**The LLM never mutates macro or meso numeric state directly.** It only returns structured
*proposals* (`ActionProposal`) and interpretive text (briefings). `engine.py` is the sole
writer of numeric state: it validates a proposal's legality/feasibility and computes magnitude
itself (`_validate_and_price`), deliberately treating the proposal's numeric parameters as
advisory. This is enforced *structurally* — `llm_gateway.py` imports no state object, and
`test_engine.py::test_llm_gateway_cannot_write_state` guards it. Rationale: reproducibility and
explainability are core product promises; letting an LLM write numbers would destroy both.

## ADR-007 — Reproducibility: one seed, threaded everywhere
**Status:** Accepted.
Every run has a `seed`, threaded into `MeridianModel.__init__` → `self.rng`
(`random.Random`). All engine, agent, and diffusion randomness draws from that one RNG — never
the global `random` or unseeded `numpy`. Same seed + scenario + decisions ⇒ identical
macro/meso numbers, proven by `test_same_seed_is_deterministic`. LLM text is explicitly *not*
part of reproducible state; it is versioned separately by `model_id + prompt_version +
temperature` and treated as an interpretive layer.

## ADR-008 — Nation types are data, not code
**Status:** Accepted.
Per `design_nation_expansion.md`, a nation archetype is a scenario-template JSON (starting
macro values, institutional roster, relationship-graph seed, crisis hooks, win/loss set). The
engine contains **no** archetype-specific branches. If the engine appears to need a special
case, that is a signal the schema is incomplete — extend the schema, not the engine. Adding an
eighth archetype must require only a new `scenarios/*.json`.

## ADR-009 — Diffusion model for narrative spread
**Status:** Accepted.
Information-campaign effectiveness is computed by a seeded Linear Threshold diffusion over a
`networkx` cohort graph (`diffusion.py`), against each cohort's `influence_susceptibility` and
`network_position` — **not** authored by the LLM. The LLM may compose campaign *content*
(channel, messenger framing) constrained to the `Campaign` schema; the engine decides whether
and how far it spreads. Consistent with ADR-006.
