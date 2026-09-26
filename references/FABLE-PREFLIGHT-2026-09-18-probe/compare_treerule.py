"""Tree-wide-rule sweep vs current-code sweep; supply per band; re-selection; overlap with the on-disk cohort."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; sys.path.insert(0, str(ROOT / "code"))
import severity_sweep as ss
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]
cur = pd.read_csv(HERE / "sweep_current.csv"); tr = pd.read_csv(HERE / "sweep_treerule.csv"); old = pd.read_csv(ROOT / "results" / "sweep_test.csv")
m = cur.merge(tr, on=KEY, suffixes=("_c", "_t")); assert len(m) == len(cur) == len(tr)
d = m.ffr_meas_t - m.ffr_meas_c
band = lambda x: pd.cut(x, np.arange(0.65, 0.9501, 0.05), right=False).apply(lambda v: "out" if pd.isna(v) else str(v))
print(f"tree rule vs current, whole sweep ({len(m)}): changed {(d.abs()>1e-12).sum()}; mean {d.mean():+.4f}; max {d.max():+.4f}; min {d.min():+.4f}; |d|>0.005: {(d.abs()>0.005).sum()}; |d|>0.01: {(d.abs()>0.01).sum()}; |d|>0.02: {(d.abs()>0.02).sum()}")
print("  base_ffr_meas max |d|:", float((m.base_ffr_meas_t - m.base_ffr_meas_c).abs().max()), " Q_in_pre max |d|:", float((m.Q_in_pre_t - m.Q_in_pre_c).abs().max()))
bc, bt = band(m.ffr_meas_c), band(m.ffr_meas_t)
print("  band changed:", int((bc != bt).sum()), "; decision changed:", int(((m.ffr_meas_c <= 0.8) != (m.ffr_meas_t <= 0.8)).sum()))
print("  supply per band (current -> tree rule):", {b: (int((bc == b).sum()), int((bt == b).sum())) for b in sorted(set(bt)) if b != "out"})
print("  K terms added per instance (tree rule) value counts:", (tr.n_K - tr.n_K_base).value_counts().sort_index().to_dict())
print("  bif_in_window instances: n =", int(tr.bif_in_window.sum()), "; mean dFFR on them:", round(float(d[m.bif_in_window_c].mean()), 4), "max", round(float(d[m.bif_in_window_c].max()), 4))
print("  non-converged:", int((~tr.converged).sum()), " max mass err:", float(tr.mass_err.max()))
print("\n=== selection on the tree-rule sweep (seed 20260918) ===")
ss.select(str(HERE / "sweep_treerule.csv"))
ns = pd.read_csv(HERE / "sweep_treerule_selected.csv"); sel = pd.read_csv(ROOT / "results" / "sweep_test_selected.csv")
a = set(map(tuple, sel[KEY].values)); b = set(map(tuple, ns[KEY].values))
print(f"overlap with on-disk selection: {len(a & b)}/150 instances; trees {len(set(zip(sel.scan, sel.side)) & set(zip(ns.scan, ns.side)))}/107")
print("new selection: loc", ns["loc"].value_counts().to_dict(), " L", ns.L_mm.value_counts().to_dict(), " bif_in_window", int(ns.bif_in_window.sum()), " no downstream bif", int(ns.d_dn_bif_mm.isna().sum()))
slot = ns.groupby(["scan", "side", "vessel", "loc", "L_mm"]).size(); print("doubled slots:", int((slot > 1).sum()), " scans with both trees:", int((ns.groupby("scan").side.nunique() == 2).sum()))
