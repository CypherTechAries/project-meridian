"""Independently verify the two CRITICAL audit findings. Read-only."""
import json, sys
from pathlib import Path
ROOT = Path(r"C:/Users/daijo/Documents/Business/Project MERIDIAN/scaffold")
sys.path.insert(0, str(ROOT / "backend"))
from app.simulation.engine import MeridianModel

scenario = json.loads((ROOT / "scenarios" / "kestral-strait.json").read_text(encoding="utf-8"))
m = MeridianModel(scenario=scenario, seed=88213)

def flat(d, p=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict): out.update(flat(v, f"{p}{k}."))
        elif isinstance(v, (int, float)) and not isinstance(v, bool): out[f"{p}{k}"] = v
    return out

start = flat(m.macro_snapshot()["indicators"])
c_start = {c.cohort.cohort_id: c.cohort.beliefs.government_competence for c in m.cohorts}
m.run(100)
end = flat(m.macro_snapshot()["indicators"])
c_end = {c.cohort.cohort_id: c.cohort.beliefs.government_competence for c in m.cohorts}

print("=== CRITICAL 4.2: saturation and frozen scalars (100 ticks, seed 88213) ===")
frozen = [k for k in start if start[k] == end[k]]
moved  = [k for k in start if start[k] != end[k]]
print(f"macro scalars total={len(start)}  frozen={len(frozen)}  moved={len(moved)}")
for k in moved:
    print(f"  MOVED  {k:52} {start[k]:>8.4f} -> {end[k]:.4f}")
print(f"  frozen: {', '.join(frozen)}")

print("\n=== CRITICAL 4.1: tiers move in opposite directions ===")
print(f"macro government_approval : {start['government_approval']:.4f} -> {end['government_approval']:.4f}")
for cid in c_start:
    print(f"  cohort {cid:32} {c_start[cid]:.4f} -> {c_end[cid]:.4f}")

# find first tick military_readiness hits the clamp
m2 = MeridianModel(scenario=scenario, seed=88213)
peg = None
for t in range(1, 101):
    m2.step()
    if m2.macro_snapshot()["indicators"]["military_readiness"] >= 1.0:
        peg = t; break
print(f"\nmilitary_readiness first reaches clamp ceiling 1.0 at tick: {peg}")

print("\n=== CRITICAL 4.1: is the declared cross-tier channel actually dead? ===")
import subprocess
for sym in ["income_sensitivity_to_shipping_disruption", "represents_population", "narrative_adoption"]:
    r = subprocess.run(["grep","-rn",sym,str(ROOT/"backend"/"app")],capture_output=True,text=True)
    lines = [l for l in r.stdout.strip().split("\n") if l]
    print(f"\n  '{sym}' -> {len(lines)} reference(s) in backend/app:")
    for l in lines: print(f"      {l.split(chr(92))[-1] if chr(92) in l else l}")
