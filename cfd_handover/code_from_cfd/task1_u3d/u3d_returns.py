"""Writes returns/2026-09-24/U3D_sten70.csv (one row per level = the work CSV) and U3D_sten70_summary.csv (differences, Celik GCI, rule, U3D, defining sentence) from U3D_sten70_work.csv and u3d_analyse json."""
import sys, os, json, csv, shutil, subprocess
U = os.path.dirname(os.path.abspath(__file__)); R = os.environ.get("U3D_RETURNS_DIR", "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-24")
# U3D_RETURNS_DIR (optional) redirects the two CSVs AND u3d_final.json into that directory (dry run); U3D_WORK_CSV (optional) replaces U/U3D_sten70_work.csv as input
J = f"{R}/u3d_final.json" if "U3D_RETURNS_DIR" in os.environ else f"{U}/u3d_final.json"; WORK = os.environ.get("U3D_WORK_CSV", f"{U}/U3D_sten70_work.csv")
levels = [r["level"] for r in csv.DictReader(open(WORK))]
order = [l for l in ("S50", "S25A", "S12A", "S25B", "S12B", "W0", "W1", "W2", "W3", "W4") if l in levels and os.path.exists(f"{U}/{'wedge_' if l.startswith('W') else 'case_'}{l}/analysis.json")]
transient = [l for l in levels if l == "W3_3000it"]      # the first 3000-iteration W3 run (still drifting): kept in the table for transparency, never used in the classification
subprocess.run(["python3", f"{U}/u3d_analyse.py", J] + order, check=True, stdout=subprocess.DEVNULL)
d = json.load(open(J)); c = d["classification"]
rows = {r["level"]: r for r in csv.DictReader(open(WORK))}
cols = list(next(iter(rows.values())).keys())
with open(f"{R}/U3D_sten70.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader()
    for l in order + transient: w.writerow(rows[l])
S = []
def add(k, v, note=""): S.append(dict(item=k, value=v, note=note))
add("U3D", c.get("U3D"), c.get("sentence")); add("rule", c["rule"], "classification rules (design v2.1-v2.2) and SETTLED criterion (v2.4) fixed before the first 3D result; iteration budgets v2.5-v2.7 set with earlier results in view (settling behaviour only)")
for z, f in c["families"].items():
    add(f"zone{z}_levels", " ".join(f["levels"])); add(f"zone{z}_e21_f25_minus_f12", f["celik"].get("e21")); add(f"zone{z}_e32_f50_minus_f25", f["celik"].get("e32"))
    add(f"zone{z}_finest_pair_abs", f["finest_pair_abs"], "< 0.005 required for PASS"); add(f"zone{z}_observed_order", f["celik"].get("observed_order")); add(f"zone{z}_GCI21_absolute", f["celik"].get("GCI21_absolute"), "1.25 |e21| / (2^p - 1), FFR units")
    add(f"zone{z}_GCI21_relative", f["celik"].get("GCI21")); add(f"zone{z}_shrinks_noise_limited", f"{f['shrinks']} {f['noise_limited']}")
if "S25A" in rows and "S25B" in rows: add("interface_effect_S25B_minus_S25A", float(rows["S25B"]["FFR_last100_mean"]) - float(rows["S25A"]["FFR_last100_mean"]), "shifted-zone (B) vs zone A interfaces, 25 um")
if "S12A" in rows and "S12B" in rows: add("interface_effect_S12B_minus_S12A", float(rows["S12B"]["FFR_last100_mean"]) - float(rows["S12A"]["FFR_last100_mean"]), "12.5 um")
if "wedge" in d:
    wd = d["wedge"]; add("wedge_levels", " ".join(wd["levels"])); add("wedge_successive_differences", json.dumps(wd["diffs_successive"])); add("wedge_finest_pair_abs", wd["finest_pair_abs"]); add("wedge_differences_shrink", wd["differences_shrink"]); add("wedge_celik", json.dumps(wd["celik"])); add("wedge_clean", c.get("wedge_clean"), "only used by rules 2 and 3")
with open(f"{R}/U3D_sten70_summary.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["item", "value", "note"]); w.writeheader(); w.writerows(S)
print("wrote", len(order), "levels; rule", c["rule"], "U3D", c.get("U3D"))
