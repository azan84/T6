"""
t5l2_summarise.py - endpoints of the throat caliber error (T5) at level-1 and level-2 perfusion territories.

Conventions of summarise_revision.py: discrete arm restricted to eligible instances, rows with status ok, pass =
residual < 0.10, wrong = |dFFR| > 0.05, passes-and-wrong = both, Wilson 95% intervals. Level 2 is paired with
level 1 by model (rows ok at both levels); exact McNemar on discordant pairs.

usage: t5l2_summarise.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import binomtest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from summarise_revision import load, ci

PROJ = HERE.parent
R = PROJ / "results"
OUT = R / "t5l2-2026-10-09"
ELIG = R / "discrete_arm_eligibility.csv"
PL = {"A_fixed": "A", "B_rederived": "B", "C_flowmatched": "C", "D_perterritory": "D"}
VARIANTS = ("T5_ds_plus10", "T5_ds_minus10", "T5_vox_narrow", "T5_vox_wide")
POOLS = {"T5_ds_pooled": ("T5_ds_plus10", "T5_ds_minus10"), "T5_vox_pooled": ("T5_vox_narrow", "T5_vox_wide")}
V = ["pw", "pass_", "flip", "wrong", "outlet_flow_residual", "ffr", "fit_at_bound", "n_empty"]


def level(cfg):
    x = load(OUT / f"ablation_t5_{cfg}.csv", OUT / f"perterritory_t5_{cfg}.csv", ELIG)
    x["pass_"] = (x.outlet_flow_residual < 0.10).astype(int)
    for c in ("fit_at_bound", "n_empty"):
        x[c] = x[c] if c in x else np.nan
    x["fit_at_bound"] = x.fit_at_bound.astype(object).map({True: 1, False: 0, "True": 1, "False": 0}).fillna(0).astype(int)
    return x


def mcn(a, b):
    n01 = int(((a == 0) & (b == 1)).sum()); n10 = int(((a == 1) & (b == 0)).sum())
    return n01, n10, float(binomtest(n01, n01 + n10).pvalue) if n01 + n10 else 1.0


def main():
    l1, l2 = level("L1drop"), level("L2keep")
    j = l1.set_index("run_id")[["bed", "error_type", "protocol"] + V].join(
        l2.set_index("run_id")[V], how="inner", rsuffix="_2").reset_index()
    only = len(set(l1.run_id) ^ set(l2.run_id))
    rows = []
    for bed in ("discrete", "leaky"):
        for e in VARIANTS + tuple(POOLS):
            for p in PL:
                g = j[(j.bed == bed) & j.error_type.isin(POOLS.get(e, (e,))) & (j.protocol == p)]
                n = len(g); r = dict(bed=bed, error_type=e, protocol=PL[p], n=n)
                for lv, s in (("L1", ""), ("L2", "_2")):
                    k_p, k_pw, k_f = int(g["pass_" + s].sum()), int(g["pw" + s].sum()), int(g["flip" + s].sum())
                    nb = int(g["fit_at_bound" + s].sum()); h = g[g["fit_at_bound" + s] == 0]
                    r.update({f"{lv}_pass": k_p, f"{lv}_pw": k_pw, f"{lv}_flip": k_f,
                              f"{lv}_pw_ci": ci(k_pw, n), f"{lv}_wgp_ci": ci(k_pw, k_p), f"{lv}_flip_ci": ci(k_f, n),
                              f"{lv}_pass_ci": ci(k_p, n), f"{lv}_bound": nb,
                              f"{lv}_pw_exbound_ci": ci(int(h["pw" + s].sum()), len(h)),
                              f"{lv}_med_resid": float(g["outlet_flow_residual" + s].median()),
                              f"{lv}_n_empty": int((g["n_empty" + s].fillna(0) > 0).sum())})
                for ep in ("pw", "flip", "pass_"):
                    n01, n10, pv = mcn(g[ep], g[ep + "_2"])
                    r.update({f"{ep}_new": n01, f"{ep}_lost": n10, f"{ep}_p": pv})
                r["max_abs_ffr_diff"] = float((g.ffr - g.ffr_2).abs().max()) if n else np.nan
                rows.append(r)
    t = pd.DataFrame(rows); t.to_csv(OUT / "t5l2_cells.csv", index=False)

    n1 = {b: len(l1[(l1.bed == b)]) for b in ("discrete", "leaky")}
    lines = [f"paired rows {len(j)}; run_ids in only one level {only}; L1 ok rows {n1}",
             "",
             "bed       error           P  n   | pass L1 -> L2      | P&W L1 -> L2 (+new/-lost, p)            | "
             "P(wrong|pass) L1 -> L2           | flip L1 -> L2 (+/-, p)                | D bound L1/L2"]
    for _, r in t.iterrows():
        lines.append(
            f"{r.bed:9} {r.error_type:15} {r.protocol} {r.n:3} | {r.L1_pass:3} -> {r.L2_pass:3} (p {r.pass__p:.2g}) | "
            f"{r.L1_pw_ci:13} -> {r.L2_pw_ci:13} (+{r.pw_new}/-{r.pw_lost}, p {r.pw_p:.2g}) | "
            f"{r.L1_pw}/{r.L1_pass} {r.L1_wgp_ci:13} -> {r.L2_pw}/{r.L2_pass} {r.L2_wgp_ci:13} | "
            f"{r.L1_flip_ci:13} -> {r.L2_flip_ci:13} (+{r.flip_new}/-{r.flip_lost}, p {r.flip_p:.2g}) | "
            f"{r.L1_bound}/{r.L2_bound}  max|dffr L1-L2| {r.max_abs_ffr_diff:.2g}  empty {r.L1_n_empty}/{r.L2_n_empty}")
    lines += ["", "D passes-and-wrong excluding fits on the parameter bound (L1 -> L2):"]
    for _, r in t[t.protocol == "D"].iterrows():
        lines.append(f"  {r.bed:9} {r.error_type:15} bound {r.L1_bound:3}/{r.L2_bound:3}  "
                     f"{r.L1_pw_exbound_ci} -> {r.L2_pw_exbound_ci}")

    # failed Protocol C fits and D bound fits over all rows (before eligibility pairing)
    lines += ["", "status counts by level (all rows, both beds, before eligibility):"]
    for cfg in ("L1drop", "L2keep"):
        a = pd.read_csv(OUT / f"ablation_t5_{cfg}.csv", low_memory=False)
        d = pd.read_csv(OUT / f"perterritory_t5_{cfg}.csv")
        lines.append(f"  {cfg}: A-C {a.status.value_counts().to_dict()}; D {d.status.value_counts().to_dict()}; "
                     f"D fit_at_bound {int(d.fit_at_bound.astype(str).eq('True').sum())} of {int(d.status.eq('ok').sum())}")
    tc = pd.read_csv(OUT / "territory_counts_L2keep.csv")
    el = pd.read_csv(ELIG); el = el[el.eligible.astype(bool)][["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]].assign(_e=1)
    tc = tc.merge(el, on=["scan", "side", "vessel", "loc", "L_mm", "ds_pct"], how="left")
    tc = tc[(tc.bed == "leaky") | (tc._e == 1)]
    for bed, g in tc.groupby("bed"):
        lines.append(f"  territories per tree, {bed}: L1 {g.n_terr_l1.value_counts().sort_index().to_dict()}, "
                     f"L2 {g.n_terr_pos.value_counts().sort_index().to_dict()} (median {g.n_terr_pos.median():.0f})")
    txt = "\n".join(lines); print(txt); (OUT / "summary.txt").write_text(txt + "\n")

    # LaTeX body: pooled magnitudes, protocols A/B, C, D; P&W L1 -> L2 per bed with McNemar p
    def pf(p): return "$<0.001$" if p < 0.001 else "1.0" if p >= 0.995 else f"{p:.2g}"
    names = {"T5_ds_pooled": "DS $\\pm10$", "T5_vox_pooled": "Throat $\\pm\\tfrac12$ voxel"}
    body = []
    for e in POOLS:
        for i, p in enumerate(("A", "C", "D")):
            dr = t[(t.bed == "discrete") & (t.error_type == e) & (t.protocol == p)].iloc[0]
            lr = t[(t.bed == "leaky") & (t.error_type == e) & (t.protocol == p)].iloc[0]
            body.append(f"{names[e] if i == 0 else ''} & {'A, B' if p == 'A' else p} & "
                        f"{dr.L1_pw_ci} & {dr.L2_pw_ci} & {pf(dr.pw_p)} & "
                        f"{lr.L1_pw_ci} & {lr.L2_pw_ci} & {pf(lr.pw_p)} \\\\")
        body.append("\\addlinespace[2pt]")
    (OUT / "tab_t5l2.tex").write_text("\n".join(body[:-1]) + "\n")


if __name__ == "__main__":
    main()
