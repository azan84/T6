"""
throat_demand_summarise.py - endpoints for the half-voxel throat error on the re-selected demand cohorts (x2, x3), in
the conventions of summarise_revision.py and t5_throat_summarise.py: discrete arm restricted to the eligible instances
of that demand, Wilson 95% intervals, passes-and-wrong over models with a defined residual, grey-zone flips, and the
paired sign test on per-instance flip proportions against T1+T2 of the replication run at the same demand.

usage: throat_demand_summarise.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from summarise_revision import load, ci, KEY
from t5_throat_summarise import grey, cell, sign_test, PROTOS, PL

PROJ = HERE.parent
R = PROJ / "results"
OUT = R / "throat_demand-2026-10-09"
VOX = ("T5_vox_narrow", "T5_vox_wide")
TOPO = ("T1_missed_branch", "T2_truncation")
CAL = ("T3_stenosis_length", "T4_taper")
BEDS = {2: ("discrete", "leaky"), 3: ("leaky",)}


def main():
    rows, st, tex, extra = [], [], [], []
    # primary demand, from the frozen T5 run (for the side-by-side table)
    p1 = pd.read_csv(R / "t5_throat-2026-10-09" / "t5_cells.csv")
    for _, r in p1[p1.error_type.isin(VOX + ("T5_vox_pooled", "T1T2_topo", "T3T4_cal"))].iterrows():
        rows.append(dict(scale=1, **r.to_dict()))
    s1 = pd.read_csv(R / "t5_throat-2026-10-09" / "t5_sign_tests.csv")
    s1 = s1[s1.comparison.isin(["T1T2 vs T5_vox_narrow", "T1T2 vs T5_vox_wide", "T1T2 vs T5_vox_pooled"])]
    for _, r in s1.iterrows(): st.append(dict(scale=1, **r.to_dict()))

    for scale, beds in BEDS.items():
        rd = R / f"demand-replication-x{scale}-2026-10-08"; od = OUT / f"x{scale}"
        el = rd / "discrete_arm_eligibility.csv"
        t5 = grey(load(od / "ablation_t5vox.csv", od / "perterritory_t5vox.csv", el))
        fr = grey(load(rd / "ablation.csv", rd / "ablation-perterritory.csv", el))
        fr = fr[fr.bed.isin(beds)]
        x = pd.concat([fr, t5], ignore_index=True)
        for bed in beds:
            for e, members in [(v, (v,)) for v in VOX] + [("T5_vox_pooled", VOX), ("T1T2_topo", TOPO), ("T3T4_cal", CAL)]:
                src = fr if e in ("T1T2_topo", "T3T4_cal") else t5
                for p in PROTOS:
                    g = src[(src.bed == bed) & src.error_type.isin(members) & (src.protocol == p)]
                    rows.append(dict(scale=scale, bed=bed, error_type=e, protocol=p, **cell(g)))
            for p in PROTOS:
                for name, b_ in (("T1T2 vs T5_vox_narrow", ("T5_vox_narrow",)), ("T1T2 vs T5_vox_wide", ("T5_vox_wide",)),
                                 ("T1T2 vs T5_vox_pooled", VOX)):
                    st.append(dict(scale=scale, bed=bed, protocol=p, comparison=name, **sign_test(x, TOPO, b_, bed, p)))
            # direction of flips, clean FFR and voxel magnitude at this demand
            a = t5[(t5.bed == bed) & (t5.protocol == "A_fixed")]
            fl = a[a.flip == 1]
            wrong_dir = int(((fl.error_type == "T5_vox_narrow") & (fl.to_neg == 1)).sum()
                            + ((fl.error_type == "T5_vox_wide") & (fl.to_pos == 1)).sum())
            inst = a.drop_duplicates(KEY)
            extra.append(f"x{scale} {bed}: instances {len(inst)}; clean FFR median {inst.ffr_clean.median():.3f} "
                         f"(IQR {inst.ffr_clean.quantile(.25):.3f}-{inst.ffr_clean.quantile(.75):.3f}); "
                         f"DS median {inst.ds_pct.median():.0f}%; |dDS| pp median "
                         f"{a[a.error_type == 'T5_vox_narrow'].info_dDS_requested_pp.abs().median():.2f} "
                         f"(range {a[a.error_type == 'T5_vox_narrow'].info_dDS_requested_pp.abs().min():.2f}-"
                         f"{a[a.error_type == 'T5_vox_narrow'].info_dDS_requested_pp.abs().max():.2f}); "
                         f"Protocol A flips against the sign of the error: {wrong_dir} of {len(fl)}; "
                         f"median |dFFR| A {a.dFFR.abs().median():.3f}")
        raw = pd.concat([pd.read_csv(od / "ablation_t5vox.csv", low_memory=False), pd.read_csv(od / "perterritory_t5vox.csv")])
        raw = raw[raw.error_type.isin(VOX)]
        extra.append(f"x{scale} status by protocol: " + raw.groupby(["bed", "protocol"]).status.value_counts().to_dict().__repr__())
        if "fit_at_bound" in raw:
            extra.append(f"x{scale} Protocol D fits at bound: " + raw[raw.protocol == "D_perterritory"].groupby(["bed", "error_type"]).fit_at_bound.sum().to_dict().__repr__())
        log = pd.read_csv(od / "t5vox_insert_log.csv")
        extra.append(f"x{scale} insertions {len(log)}, clipped {int(log.clipped.sum())}, realised != applied "
                     f"{int(((log.ds_realised - log.ds_applied).abs() > 1e-9).sum())}")

    tab = pd.DataFrame(rows); tab.to_csv(OUT / "throat_demand_cells.csv", index=False)
    st = pd.DataFrame(st); st.to_csv(OUT / "throat_demand_sign_tests.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
    print(tab[["scale", "bed", "error_type", "protocol", "n", "flips", "flip_ci", "n_resid", "pw", "pw_ci",
               "med_abs_dffr", "beyond", "beyond_ci", "to_pos", "to_neg"]].to_string(index=False))
    print("\npaired sign test on per-instance flip proportions, T1+T2 (a) against the throat error (b)")
    print(st[["scale", "bed", "protocol", "comparison", "n_inst", "rate_a", "rate_b", "a_gt_b", "b_gt_a", "p"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3g}"))
    txt = "\n".join(extra); print("\n" + txt); (OUT / "throat_demand_notes.txt").write_text(txt + "\n")

    # LaTeX rows for the pooled half-voxel error at x2 and x3, in the layout of Table tab:throat
    def c(scale, bed, p):
        r = tab[(tab.scale == scale) & (tab.bed == bed) & (tab.error_type == "T5_vox_pooled") & (tab.protocol == p)]
        if r.empty: return "-- & -- & -- & --"
        r = r.iloc[0]; return f"{r.n} & {r.flip_ci} & {r.pw_ci} & {r.beyond_ci}"
    for scale in (2, 3):
        for i, (lab, p) in enumerate((("A, B", "A_fixed"), ("C", "C_flowmatched"), ("D", "D_perterritory"))):
            head = f"$\\pm\\tfrac12$ voxel, $k\\times{scale}$" if i == 0 else ""
            tex.append(f"{head} & {lab} & {c(scale, 'discrete', p)} & {c(scale, 'leaky', p)} \\\\")
        tex.append("\\addlinespace[2pt]")
    (OUT / "tab_throat_demand.tex").write_text("\n".join(tex[:-1]) + "\n")
    print("\n" + "\n".join(tex[:-1]))


if __name__ == "__main__":
    main()
