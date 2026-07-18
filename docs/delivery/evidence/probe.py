import json, copy, sys
sys.path.insert(0, r"[REPOSITORY ROOT]/scaffold/backend")
from app.simulation.engine import MeridianModel

p = r"[REPOSITORY ROOT]/scaffold/scenarios/kestral-strait.json"
base = json.load(open(p, encoding="utf-8"))

m = MeridianModel(copy.deepcopy(base), seed=42); m.run(10)
print("ORIG events:", len(m.event_log), "approval:", m.macro.state.indicators.government_approval)

alt = copy.deepcopy(base)
rename = {"head_of_government":"chancellor","minister_of_defence":"secretary_minister_of_defence",
          "minister_of_finance":"treasury_secretary","minister_of_foreign_affairs":"foreign_secretary",
          "intelligence_lead":"spy_chief","strategic_comms":"press_office"}
for a in alt["institutional_agents"]:
    a["role"] = rename[a["role"]]
try:
    m2 = MeridianModel(alt, seed=42); m2.run(10)
    print("RENAMED events:", len(m2.event_log), "approval:", m2.macro.state.indicators.government_approval)
except Exception as e:
    print("RENAMED raised:", type(e).__name__, e)

land = copy.deepcopy(base)
del land["initial_macro_state"]["indicators"]["shipping_throughput_pct_of_baseline"]
try:
    m3 = MeridianModel(land, seed=42); m3.run(3)
    print("LANDLOCKED ok")
except Exception as e:
    print("LANDLOCKED raised:", type(e).__name__, e)
