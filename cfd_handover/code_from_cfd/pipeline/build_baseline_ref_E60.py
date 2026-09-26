"""solve_baseline_ref_E60: healthy baseline surface meshed with the lesion80 refinement extended to arc 60 mm (mesh_base_ref_E60), resting baseline BCs (identical R_out/relax to
solve_baseline), plus wallShearStress. Reference for solve_lesion80_E60. Refuses to overwrite a case holding run output. Derived from the audited build_baseline_ref.py."""
import sys, os, re, json
import re as _re
_PAT = _re.compile(r"// No residualControl in fvSolution \(see there for why\).*?laminar assumption\)\.\n", _re.S)
_NEW = '// No residualControl in fvSolution: fixed iteration count, judged from the monitors. Throat Re of the lesion80 case is estimated 110-210 (computed from the solved section flux\n// after the run); a slow limit cycle is possible - if so report the last-500-iteration band and label the case UNCONVERGED, never a converged value.\n'
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_solve_cases as B
from outlets_837 import build_tree

BASE = B.BASE
T = build_tree(); Qd = T.demand("murray")
import shutil
chk = f"{BASE}/solve_baseline_ref_E60"
if os.path.exists(chk):
    done = [d for d in os.listdir(chk) if (d.isdigit() and int(d) > 0) or d.startswith("processor") or d in ("log.simpleFoam", "log.smoke")]
    if done: raise SystemExit(f"refusing to overwrite {chk}: it holds run output {done[:4]}")
dst = B.build_case("baseline_ref_E60", f"{BASE}/lesion80/mesh_base_ref_E60", T, Qd)
shutil.rmtree(f"{dst}/constant/polyMesh/sets", ignore_errors=True)
ref = json.load(open(f"{BASE}/solve_baseline/zerod_reference.json"))["outlets"]
new = json.load(open(f"{dst}/zerod_reference.json"))["outlets"]
for p in ref:
    assert abs(new[p]["R_out"] / ref[p]["R_out"] - 1) < 1e-9 and abs(new[p]["relax"] / ref[p]["relax"] - 1) < 1e-9, p
cd = open(f"{dst}/system/controlDict").read()
fn = cd.rstrip()[:-1] + ("    wallShearStress\n    {\n        type wallShearStress;\n        libs (\"libfieldFunctionObjects.so\");\n"
                         "        writeControl writeTime; patches (wall);\n    }\n}\n")
open(f"{dst}/system/controlDict", "w").write(_PAT.sub(_NEW, fn))
cdict = open(f"{dst}/system/controlDict").read()
assert re.search(r"stopAt\s+endTime;", cdict) and re.search(r"startFrom\s+startTime;", cdict) and re.search(r"endTime\s+3000;", cdict)
print("baseline_ref_E60 built; R_out/relax identical to solve_baseline; run controls asserted")
