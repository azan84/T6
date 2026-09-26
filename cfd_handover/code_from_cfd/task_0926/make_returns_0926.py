"""Assembles /mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-09-26/ (work order 2026-09-26, Task 0 + Task A + B1): the 2026-09-24 returns (never overwritten), the new files (M1_geometry_gates.csv, settle_iterations.csv,
as_meshed_radius_<case>.csv in the contract format, lesion80_hyperaemic.csv, lesion80_E60.csv), U3D_sten70.csv with the GCI columns, INDEX.csv and the one-page NOTE.md. Idempotent (rewrites the target files).
usage: make_returns_0926.py"""
import os, sys, csv, json, shutil, hashlib, glob
import numpy as np
P = os.path.dirname(os.path.abspath(__file__)); RET = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns"; OLD = f"{RET}/2026-09-24"; NEW = f"{RET}/2026-09-26"
os.makedirs(NEW, exist_ok=True)
def rd(f): return list(csv.DictReader(open(f)))
def wr(f, rows, cols=None):
    cols = cols or list(rows[0].keys())
    with open(f, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
# 1. carry over the 2026-09-24 files (numbers unchanged) except those regenerated below
SKIP = {"INDEX.md", "NOTE.md", "pilot837_hyperaemia_flow.csv", "pilot837_E60_extended_tube.csv", "U3D_sten70.csv"} | {os.path.basename(f) for f in glob.glob(f"{OLD}/as_meshed_radius_*.csv")}
for n in sorted(os.listdir(OLD)):
    if n in SKIP or n == "desktop.ini": continue
    s = f"{OLD}/{n}"
    if os.path.isdir(s): shutil.copytree(s, f"{NEW}/{n}", dirs_exist_ok=True)
    else: shutil.copy2(s, f"{NEW}/{n}")
shutil.copy2(f"{OLD}/NOTE.md", f"{NEW}/NOTE_long.md")
APP = f"{P}/returns_0926_status_appendix.md"
if os.path.exists(APP): open(f"{NEW}/NOTE_long.md", "a").write("\n\n" + open(APP).read())      # status of the 2026-09-26 tasks (B1, B2, B3, audits), maintained by hand      # the living detailed note of the 2026-09-24 folder (updated to 2026-09-26), kept next to the one-page NOTE.md
# 2. the pilot follow-ups under the names of the 2026-09-26 table
shutil.copy2(f"{OLD}/pilot837_hyperaemia_flow.csv", f"{NEW}/lesion80_hyperaemic.csv"); shutil.copy2(f"{OLD}/pilot837_E60_extended_tube.csv", f"{NEW}/lesion80_E60.csv")
# 3. as_meshed_radius_<case>.csv in the contract format: tree_node, s_mm, r_asmeshed_mm, r_area_equiv_mm, r_max_inscribed_mm, section_area_mm2, covered ; one row per node of the package centreline.vtp
#    covered = 1 iff the planar section at the node is valid (section_ok = 1: one connected section of the LAD/branch lumen); covered = 0 -> radii blank (no interpolation). The richer table is kept as *_detail.csv.
cov = {}
for case in ("baseline", "T1_missed_branch", "clean_nolesion"):
    rows = rd(f"{OLD}/as_meshed_radius_{case}.csv"); out = []
    for r in rows:
        ok = r["section_ok"] == "1" and r["r_eq3D_mm"] not in ("", "nan")
        out.append(dict(tree_node=int(r["node"]), s_mm=r["arc_s_mm"], r_asmeshed_mm=r["r_eq3D_mm"] if ok else "", r_area_equiv_mm=r["r_eq3D_mm"] if ok else "", r_max_inscribed_mm=r["r_maxinscribed_mm"] if ok else "",
                        section_area_mm2=r["section_area_mm2"] if ok else "", covered=1 if ok else 0))
    wr(f"{NEW}/as_meshed_radius_{case}.csv", out, ["tree_node", "s_mm", "r_asmeshed_mm", "r_area_equiv_mm", "r_max_inscribed_mm", "section_area_mm2", "covered"]); shutil.copy2(f"{OLD}/as_meshed_radius_{case}.csv", f"{NEW}/as_meshed_radius_{case}_detail.csv")
    # inscribed variant: the same contract, r_asmeshed_mm = the maximum-inscribed-circle radius of the section (ingest_cfd_radius.py reads only tree_node and r_asmeshed_mm; blank/non-positive = uncovered -> requested radius)
    ins = []
    for r in rows:
        ok = r["section_ok"] == "1" and r["r_maxinscribed_mm"] not in ("", "nan") and r["r_eq3D_mm"] not in ("", "nan")
        ins.append(dict(tree_node=int(r["node"]), s_mm=r["arc_s_mm"], r_asmeshed_mm=r["r_maxinscribed_mm"] if ok else "", r_area_equiv_mm=r["r_eq3D_mm"] if ok else "", r_max_inscribed_mm=r["r_maxinscribed_mm"] if ok else "", section_area_mm2=r["section_area_mm2"] if ok else "", covered=1 if ok else 0))
    wr(f"{NEW}/as_meshed_radius_{case}_inscribed.csv", ins, ["tree_node", "s_mm", "r_asmeshed_mm", "r_area_equiv_mm", "r_max_inscribed_mm", "section_area_mm2", "covered"])
    cov[case] = (len(out), sum(o["covered"] for o in out))
# 4. U3D_sten70.csv with GCI columns per family
fin = json.load(open(f"{P}/u3d/u3d_final.json")); fam = fin["classification"]["families"]; wed = fin["wedge"]["celik"]
rows = rd(f"{P}/u3d/U3D_sten70_work.csv")
for r in rows:
    l = r["level"]; z = [k for k in ("A", "B") if l in fam[k]["levels"]] if l in ("S50", "S25A", "S12A", "S25B", "S12B") else []
    r["zone_family"] = "+".join(z) if z else ("wedge" if l in fin["wedge"]["levels"] else "not classified (kept for transparency)")
    for k in ("A", "B"):
        r[f"GCI21_absolute_zone{k}"] = fam[k]["celik"].get("GCI21_absolute") if k in z else ""; r[f"observed_order_zone{k}"] = fam[k]["celik"].get("observed_order") if k in z else ""
    inw = l in fin["wedge"]["levels"][-3:]
    r["GCI21_absolute_wedge"] = wed.get("GCI21_absolute") if inw else ""; r["observed_order_wedge"] = wed.get("observed_order") if inw else ""
    r["U3D_final"] = fin["classification"].get("U3D") if l == "S50" else ""
wr(f"{NEW}/U3D_sten70.csv", rows)
# 5. new tables built by their own scripts (read-only on the solves)
shutil.copy2(f"{P}/m1/out_returns/M1_geometry_gates.csv", f"{NEW}/M1_geometry_gates.csv"); shutil.copy2(f"{P}/m1/out_returns/d34_distances.json", f"{NEW}/M1_D3_D4_distances_detail.json")
# 6. INDEX.csv
REF = {"stageA_summary.csv": ("0b", "Stage A running summary (sec 2-9)", ""), "stageA_A2_sweep.csv": ("0b", "A2 sweep / Item 2 severity sweep (sec 6, 11.3)", ""), "stageA_A5_ladders.csv": ("0b", "A5 ladders (Table 3, sec 9, 11.3)", ""),
       "stageA_NOTES_partial.md": ("0b", "caveats of the Stage A / Item tables", ""), "item1_tree.csv": ("0b", "Item 1 branched tree (sec 11.2)", ""), "item1_prescribed_flow_roundtrip_ds00.csv": ("3", "Table 5 (sec 11.2)", ""),
       "item1_prescribed_flow_roundtrip_ds60.csv": ("3", "Table 5 (sec 11.2)", ""), "item3_837_outlets.csv": ("0b", "Item 3 converged results (sec 11.5)", "PILOT_OUT_OF_COHORT"), "item3_837_timing.csv": ("0b", "timing of the scan-837 solves (sec 11.5, 11.10)", "PILOT_OUT_OF_COHORT"),
       "item3_837_lesion80_wss.csv": ("0b", "lesion80 WSS (sec 11.5)", "PILOT_OUT_OF_COHORT"), "item5_rcr.csv": ("0b", "Item 5 RCR (sec 11.9)", ""), "item6_cost.csv": ("0b", "Item 6 cost (sec 11.4)", ""), "failures.csv": ("0b", "failures and own mistakes (sec 10)", "PILOT_OUT_OF_COHORT on the scan-837 rows (cohort_label column)"),
       "failures_NOTES.md": ("0b", "notes to failures.csv", ""), "lesion80_sensitivity.csv": ("2", "Table 13 (sec 11.5)", "PILOT_OUT_OF_COHORT"), "lesion80_hyperaemic.csv": ("extra", "Table 14 (sec 11.6)", "PILOT_OUT_OF_COHORT"), "lesion80_E60.csv": ("extra", "Table 15 (sec 11.6)", "PILOT_OUT_OF_COHORT"),
       "U3D_sten70.csv": ("1", "Table 16 + wedge levels (sec 11.7)", ""), "U3D_sten70_summary.csv": ("1", "differences, Celik GCI per family, rule, U3D (sec 11.7)", ""), "M1_results.csv": ("3", "Table 18 (sec 11.8)", "scan 14 = frozen cohort"),
       "M1_geometry_gates.csv": ("3", "Table 17 + D2/D3/D4 (sec 11.8)", "scan 14"), "M1_D3_D4_distances_detail.json": ("3", "distances behind Table 17 (D3/D4)", "scan 14"), "settle_iterations.csv": ("B1", "settle iteration of every real-lumen steady solve (sec 11.8, new)", "scan 14 and PILOT_OUT_OF_COHORT (837)"),
       "NOTE.md": ("0b", "one-page caveats, M1 status line first", ""), "NOTE_long.md": ("0b", "detailed living note (2026-09-24 folder, updated 2026-09-26)", ""), "M1_scan14_build": ("3", "geometry/mesh gate json and READMEs of the scan-14 build", "scan 14")}
idx = []
def nrows(f):
    try: return sum(1 for _ in open(f)) - 1 if f.endswith(".csv") else ""
    except Exception: return ""
for n in sorted(os.listdir(NEW)):
    if n in ("INDEX.csv", "INDEX.md", "desktop.ini"): continue
    fp = f"{NEW}/{n}"
    for f in ([fp] if not os.path.isdir(fp) else sorted(os.path.join(dp, x) for dp, _, xs in os.walk(fp) for x in xs)):
        rel = os.path.relpath(f, NEW); key = n if not os.path.isdir(fp) else n
        if n.startswith("M1_outlets_"): ref = ("3", "Tables 19 and 20 (sec 11.8): per outlet R used or derived, Q, p-bar", "scan 14")
        elif n.startswith("M1_probes_"): ref = ("3", "area-averaged p and through-plane flux at every probe of probes.csv (sec 11.8)", "scan 14")
        elif n.startswith("M1_roundtrip_"): ref = ("A", "Table 20 (sec 11.8): prescribed-flow round trip", "scan 14")
        elif n.startswith("as_meshed_radius_"): ref = ("D2", "as-meshed radius per package centreline node (contract of code/ingest_cfd_radius.py)" + (" - richer detail table" if n.endswith("_detail.csv") else (" - INSCRIBED variant (r_asmeshed_mm = maximum inscribed radius)" if n.endswith("_inscribed.csv") else " - area-equivalent variant (r_asmeshed_mm = r_area_equiv_mm)")), "scan 14")
        elif n.startswith("item3_837_pullback_"): ref = ("0b", "Item 3 pullback tables (sec 11.5)", "PILOT_OUT_OF_COHORT")
        else: ref = REF.get(key, ("", "", ""))
        idx.append(dict(file=rel, task=ref[0], report_section_or_table=ref[1], rows=nrows(f), cohort_label=ref[2]))
wr(f"{NEW}/INDEX.csv", idx)
print("returns/2026-09-26:", len(idx), "files indexed; as-meshed coverage", cov)
