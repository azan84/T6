"""Compare results/sweep_test.csv (15:55, pre-fix) with the probe re-runs; re-select under the current code."""
import sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]; sys.path.insert(0, str(ROOT / "code"))
import severity_sweep as ss
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]
old = pd.read_csv(ROOT / "results" / "sweep_test.csv"); cur = pd.read_csv(HERE / "sweep_current.csv"); cap = pd.read_csv(HERE / "sweep_cap3.csv")
print(f"rows: on-disk {len(old)}  current {len(cur)}  cap3 {len(cap)}")
for nm, d in (("cap3", cap), ("current", cur)):
    m = old.merge(d, on=KEY, suffixes=("_o", "_n")); assert len(m) == len(old) == len(d), (len(m), len(old), len(d))
    df = m.ffr_meas_n - m.ffr_meas_o; db = m.base_ffr_meas_n - m.base_ffr_meas_o
    print(f"\n[{nm}] vs on-disk: ffr_meas identical rows {(df == 0).sum()}/{len(m)}; max|d| {df.abs().max():.2e}; moved(>1e-12) {(df.abs() > 1e-12).sum()}; "
          f"down {(df < -1e-12).sum()} up {(df > 1e-12).sum()}; base_ffr max|d| {db.abs().max():.2e}; Q_in_pre max|d| {(m.Q_in_pre_n - m.Q_in_pre_o).abs().max():.2e}; "
          f"c_mm identical {(m.c_mm_n == m.c_mm_o).all()}  r_fit_c identical {(m.r_fit_c_mm_n == m.r_fit_c_mm_o).all()}")
    if nm == "current":
        print("  |dFFR_meas| quantiles: p50 %.5f p90 %.5f p99 %.5f max %.5f" % tuple(df.abs().quantile([.5, .9, .99, 1.0])))
        print("  by ds_pct, max |d|:", m.groupby("ds_pct").apply(lambda g: (g.ffr_meas_n - g.ffr_meas_o).abs().max(), include_groups=False).round(4).to_dict())
        edges = np.arange(0.65, 0.9501, 0.05)
        bo = pd.cut(m.ffr_meas_o, edges, right=False).apply(lambda v: "out" if pd.isna(v) else str(v)); bn = pd.cut(m.ffr_meas_n, edges, right=False).apply(lambda v: "out" if pd.isna(v) else str(v))
        print("  whole sweep: band changed in", int((bo != bn).sum()), "of", len(m), "instances (in-range either side:", int(((bo != "out") | (bn != "out")).sum()), ")")
        print("  supply per band, on-disk vs current:", {b: (int((bo == b).sum()), int((bn == b).sum())) for b in sorted(set(bo)) if b != "out"})
        # selected 150
        sel = pd.read_csv(ROOT / "results" / "sweep_test_selected.csv")
        s = sel.merge(m, on=KEY)
        assert len(s) == 150
        sb_o = pd.cut(s.ffr_meas_o, edges, right=False).apply(lambda v: "out" if pd.isna(v) else str(v)); sb_n = pd.cut(s.ffr_meas_n, edges, right=False).apply(lambda v: "out" if pd.isna(v) else str(v))
        assert (sb_o == s.band.astype(str)).all()
        ch = s[sb_o != sb_n]
        print(f"\n  SELECTED 150: band changes under current code = {len(ch)}; max |dFFR_meas| = {(s.ffr_meas_n - s.ffr_meas_o).abs().max():.4f}; "
              f"n with |d|>0.001: {int(((s.ffr_meas_n - s.ffr_meas_o).abs() > 0.001).sum())}; decision (<=0.80) changes: {int(((s.ffr_meas_o <= 0.80) != (s.ffr_meas_n <= 0.80)).sum())}")
        if len(ch): print(ch[KEY + ["ffr_meas_o", "ffr_meas_n"]].assign(band_o=sb_o[ch.index], band_n=sb_n[ch.index]).round(4).to_string())
        print("  per-band count after the shift (target 25):", sb_n.value_counts().sort_index().to_dict())
        # spurious shoulder K terms on the current run
        cur["dK"] = cur.n_K - cur.n_K_base
        print("\n  K-term census (current code): n_K - n_K_base value counts:", cur.dK.value_counts().sort_index().to_dict())
        print("  instances with >=2 extra K terms (spurious shoulder terms), by L_mm x ds_pct:")
        print(pd.crosstab(cur.L_mm, cur.ds_pct, values=(cur.dK >= 2).astype(int), aggfunc="sum").to_string())
        print("  share of L=20, DS>=65 instances with >=2 extra K:", round(float((cur[(cur.L_mm == 20) & (cur.ds_pct >= 65)].dK >= 2).mean()), 3))
        s2 = sel.merge(cur, on=KEY); print("  SELECTED 150 with spurious shoulder K terms (dK>=2):", int((s2.n_K - s2.n_K_base >= 2).sum()), "; dK<=0 (native term suppressed by insertion):", int((s2.n_K - s2.n_K_base <= 0).sum()))
# re-select from the current sweep (writes sweep_current_selected.csv in the probe dir)
print("\n=== re-selection under the current code (same seed) ===")
ss.select(str(HERE / "sweep_current.csv"))
new_sel = pd.read_csv(HERE / "sweep_current_selected.csv"); sel = pd.read_csv(ROOT / "results" / "sweep_test_selected.csv")
a = set(map(tuple, sel[KEY].values)); b = set(map(tuple, new_sel[KEY].values))
print(f"overlap with the on-disk selection: {len(a & b)} of 150 instances; same trees: {len(set(zip(sel.scan, sel.side)) & set(zip(new_sel.scan, new_sel.side)))}")
