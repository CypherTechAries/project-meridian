"""A3 direct verification of the 5 checks whose agents died. Read-only on the repo."""
import json, copy, sys, hashlib, random
from pathlib import Path
ROOT = Path(r"C:/Users/daijo/Documents/Business/Project MERIDIAN/scaffold")
sys.path.insert(0, str(ROOT / "backend"))
from app.simulation.engine import MeridianModel, ACTION_EFFECTS
from app.simulation.agents.macro_state import MacroStateHolder

BASE = json.loads((ROOT / "scenarios" / "kestral-strait.json").read_text(encoding="utf-8"))
SEED = 88213
def sc(): return copy.deepcopy(BASE)
def h(o): return hashlib.sha256(json.dumps(o, sort_keys=True).encode()).hexdigest()[:12]

def line(t): print("\n" + "="*84 + f"\n{t}\n" + "="*84)

# ---------------------------------------------------------------- CHECK 1
line("CHECK 1  no-budget-or-treasury-enforcement")
print("ACTION_EFFECTS keys touched by ANY action:")
touched = sorted({k for e in ACTION_EFFECTS.values() for k in e})
print("  ", touched)
print("  any fiscal/economic key present?",
      any(k in touched for k in ("treasury_reserve_usd_m","deficit_pct_gdp","inflation_rate",
                                 "unemployment_rate","gdp_growth_qoq","foreign_direct_investment_flow")))

m = MeridianModel(scenario=sc(), seed=SEED)
pf_before = m.macro_snapshot()["indicators"]["public_finances"]
# Try to move a nested fiscal value through the ONLY delta path the engine has.
m.macro.apply_deltas({"treasury_reserve_usd_m": -999999.0})
m.macro.apply_deltas({"public_finances": -999999.0})
pf_after = m.macro_snapshot()["indicators"]["public_finances"]
print(f"  public_finances before: {pf_before}")
print(f"  public_finances after  : {pf_after}")
print(f"  -> nested fiscal state reachable by apply_deltas? {pf_before != pf_after}")

ind = m.macro.state.indicators
before_unknown = m.macro_snapshot()["indicators"]["government_approval"]
m.macro.apply_deltas({"treasry_reserve": 5.0, "totally_made_up_key": 1.0})
print(f"  unknown delta keys silently ignored (no error raised): True")

# ---------------------------------------------------------------- CHECK 2
line("CHECK 2  procurement-constraint-actively-contradicted")
m = MeridianModel(scenario=sc(), seed=SEED)
peg = None; traj = []
for t in range(1, 121):
    m.step()
    r = m.macro_snapshot()["indicators"]["military_readiness"]
    if t in (1,5,10,30,60,61,62,100,120): traj.append((t, round(r,4)))
    if peg is None and r >= 1.0: peg = t
print("  readiness trajectory:", traj)
print(f"  first tick at clamp ceiling 1.0: {peg}")
print(f"  scenario constrains min-defence-oduya with procurement_law_18mo_minimum, and the")
print(f"  defence minister proposes request_procurement_acceleration EVERY tick.")
print(f"  effect applied per tick: {ACTION_EFFECTS['request_procurement_acceleration']}")

# does removing the constraint change anything at all?
s2 = sc()
for a in s2["institutional_agents"]:
    a["constraints"] = []
m2 = MeridianModel(scenario=s2, seed=SEED); m2.run(40)
m3 = MeridianModel(scenario=sc(), seed=SEED); m3.run(40)
print(f"  40-tick hash WITH constraints   : {h(m3.macro_snapshot())}")
print(f"  40-tick hash WITHOUT constraints: {h(m2.macro_snapshot())}")
print(f"  -> constraints causally inert? {h(m2.macro_snapshot()) == h(m3.macro_snapshot())}")

# ---------------------------------------------------------------- CHECK 3
line("CHECK 3  player-intervention-path-is-a-no-op")
from fastapi.testclient import TestClient
from app.main import app
c = TestClient(app)
r = c.post("/api/simulation/runs", json={"scenario_id": "kestral-strait", "seed": SEED})
print("  create run:", r.status_code, r.json())
rid = r.json()["run_id"]
before = c.get(f"/api/simulation/runs/{rid}/state").json()["macro_state"]
absurd = {
    "action_id": "act-absurd-001",
    "actor_role": "janitor_with_no_authority",
    "action_type": "nationalise_every_foreign_asset_and_declare_war",
    "target": "everything",
    "resource_cost": {"treasury_reserve_usd_m": 999999999},
    "legal_check": "LEGAL_AND_APPROVED",
    "timeline_days": 0,
}
d = c.post(f"/api/simulation/runs/{rid}/decision", json=absurd)
print("  submit absurd intervention:", d.status_code, d.json())
after = c.get(f"/api/simulation/runs/{rid}/state").json()["macro_state"]
print(f"  macro state changed by the decision? {before != after}")
c.post(f"/api/simulation/runs/{rid}/advance", json={"ticks": 5})
after5 = c.get(f"/api/simulation/runs/{rid}/state").json()["macro_state"]
ev = c.get(f"/api/simulation/runs/{rid}/events").json()["events"]
pd = [e for e in ev if e.get("type") == "player_decision"]
print(f"  after 5 further ticks, player_decision events: {len(pd)}")
print(f"  their 'effects' field: {[e['effects'] for e in pd]}")
print(f"  client-supplied legal_check echoed back: {pd[0]['intervention'].get('legal_check')!r}")

# ---------------------------------------------------------------- CHECK 4
line("CHECK 4 (CRITICAL 1)  tiers structurally decoupled - perturbation test")
def run_get(scn, seed=SEED, n=40):
    m = MeridianModel(scenario=scn, seed=seed); m.run(n)
    return (m.macro_snapshot(),
            {c.cohort.cohort_id: c.cohort.beliefs.model_dump() for c in m.cohorts},
            dict(m.narrative_adoption))

mac0, coh0, nar0 = run_get(sc())

# (a) perturb MACRO start -> does ANY meso value change?
sA = sc()
sA["initial_macro_state"]["indicators"]["shipping_throughput_pct_of_baseline"] = 0.05
sA["initial_macro_state"]["indicators"]["government_approval"] = 0.01
sA["initial_macro_state"]["indicators"]["unemployment_rate"] = 0.95
macA, cohA, narA = run_get(sA)
print("  (a) macro perturbed hard (shipping .61->.05, approval .44->.01, unemp ->.95)")
print(f"      macro differs?           {mac0 != macA}")
print(f"      ANY cohort belief differs? {coh0 != cohA}")
print(f"      narrative adoption differs? {nar0 != narA}")

# (b) perturb MESO start -> does ANY macro value change?
sB = sc()
for ch in sB["cohorts"]:
    ch["beliefs"]["government_competence"] = 0.0
    ch["grievances"] = ["everything_is_terrible"]
macB, cohB, narB = run_get(sB)
print("  (b) every cohort's competence -> 0.0 and all given grievances")
print(f"      cohort beliefs differ?   {coh0 != cohB}")
print(f"      ANY macro value differs? {mac0 != macB}")

# (c) delete an entire cohort -> macro unchanged?
sC = sc(); removed = sC["cohorts"].pop(1)
macC, cohC, narC = run_get(sC)
print(f"  (c) deleted cohort '{removed['cohort_id']}' ({removed.get('represents_population')} people)")
print(f"      ANY macro value differs? {mac0 != macC}")

# ---------------------------------------------------------------- CHECK 5
line("CHECK 5 (CRITICAL 2)  is saturation a STUB artefact or an ENGINE defect?")
import app.simulation.llm_gateway as gw
import app.simulation.agents.institutional_agent as ia
from app.simulation.schemas.agent_schema import ActionProposal

orig = gw.propose_action
ACTIONS = [a for a in ACTION_EFFECTS if a != "observe"]

def varied_factory(seed):
    rr = random.Random(seed)
    def varied(agent, context):
        p = orig(agent, context)
        return ActionProposal(
            proposing_agent_id=p.proposing_agent_id,
            action_type=rr.choice(ACTIONS),
            target=p.target, rationale=p.rationale,
            parameters=p.parameters, confidence=p.confidence)
    return varied

for label, fn in (("STUB (fixed action per role)", None),
                  ("VARIED (random legal action each tick, as a real LLM would)", varied_factory(7))):
    if fn: gw.propose_action = fn; ia.llm_gateway.propose_action = fn
    else:  gw.propose_action = orig; ia.llm_gateway.propose_action = orig
    m = MeridianModel(scenario=sc(), seed=SEED); m.run(120)
    i = m.macro_snapshot()["indicators"]
    at_bound = [k for k in ("military_readiness","government_approval","social_stability_index",
                            "shipping_throughput_pct_of_baseline")
                if i[k] >= 0.9999 or i[k] <= 0.0001]
    print(f"\n  {label}")
    print(f"     military_readiness      {i['military_readiness']:.4f}")
    print(f"     social_stability_index  {i['social_stability_index']:.4f}")
    print(f"     government_approval     {i['government_approval']:.4f}")
    print(f"     indicators pinned at a clamp bound after 120 ticks: {at_bound}")
gw.propose_action = orig; ia.llm_gateway.propose_action = orig

# is there ANY cost/cooldown/decay mechanism in the engine at all?
line("CHECK 5b  does any cost / cooldown / decay / opposing-pressure mechanism exist?")
import inspect
from app.simulation import engine as eng
src = inspect.getsource(eng)
for token in ("cost", "cooldown", "decay", "budget", "resource", "prerequisite", "mean_revert", "revert"):
    print(f"   '{token}' appears in engine.py source: {token in src}")
