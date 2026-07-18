"""Decisive test: is meso->macro influence CAUSAL, or shared-RNG contamination?"""
import json, copy, sys, hashlib
from pathlib import Path
ROOT = Path(r"C:/Users/daijo/Documents/Business/Project MERIDIAN/scaffold")
sys.path.insert(0, str(ROOT / "backend"))
from app.simulation.engine import MeridianModel

BASE = json.loads((ROOT / "scenarios" / "kestral-strait.json").read_text(encoding="utf-8"))
SEED = 88213
def sc(): return copy.deepcopy(BASE)

def run(scn, n=40):
    m = MeridianModel(scenario=scn, seed=SEED); m.run(n)
    return (m.macro_snapshot(),
            {c.cohort.cohort_id: c.cohort.beliefs.model_dump() for c in m.cohorts})

print("Grievance counts per cohort in the baseline scenario:")
for ch in BASE["cohorts"]:
    print(f"   {ch['cohort_id']:34} grievances={len(ch.get('grievances',[]))}")
print("\ncohort_agent.step() draws from rng ONLY IF the cohort has grievances.")
print("So changing WHICH cohorts have grievances changes how many draws are consumed per tick.\n")

mac0, coh0 = run(sc())

# TEST A: change belief VALUES only. Grievance lists untouched => identical number of rng draws.
sA = sc()
for ch in sA["cohorts"]:
    ch["beliefs"]["government_competence"] = 0.01   # was 0.31-0.58
    ch["beliefs"]["threat_perception_external"] = 0.99
macA, cohA = run(sA)
print("TEST A  belief VALUES changed drastically; grievance list lengths UNCHANGED")
print(f"        cohort beliefs differ? {coh0 != cohA}")
print(f"        macro differs?         {mac0 != macA}   <-- if False, meso->macro is NOT causal")

# TEST B: add a grievance to the one cohort that has none => +1 rng draw per tick.
sB = sc()
for ch in sB["cohorts"]:
    if not ch.get("grievances"):
        ch["grievances"] = ["synthetic_extra_grievance"]
        print(f"\nTEST B  added a grievance to '{ch['cohort_id']}' (it had none)")
macB, cohB = run(sB)
print(f"        macro differs? {mac0 != macB}   <-- if True, it is RNG-STREAM contamination")
if mac0 != macB:
    a = mac0["indicators"]; b = macB["indicators"]
    for k in a:
        if isinstance(a[k], float) and a[k] != b[k]:
            print(f"          {k}: {a[k]!r} -> {b[k]!r}")

# TEST C: remove ALL grievances everywhere => cohort step makes zero draws.
sC = sc()
for ch in sC["cohorts"]: ch["grievances"] = []
macC, cohC = run(sC)
print(f"\nTEST C  all grievances removed (cohort step consumes zero rng draws)")
print(f"        macro differs? {mac0 != macC}")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
causal = (mac0 != macA)
contamination = (mac0 != macB)
if not causal and contamination:
    print("  meso -> macro is NOT a causal channel.")
    print("  The apparent coupling is SHARED-RNG CONTAMINATION: cohort code and macro code")
    print("  draw from the same random.Random stream, so changing the NUMBER of cohort draws")
    print("  shifts every later macro draw. Changing cohort VALUES changes nothing at all.")
    print("  => Critical finding 4.1 stands, and this is a SECOND defect: no named RNG substreams.")
elif causal:
    print("  meso -> macro IS causal. Critical finding 4.1 must be modified or refuted.")
else:
    print("  Neither effect observed. Investigate further.")
