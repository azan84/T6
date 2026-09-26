"""Lesion-minus-reference analysis for Item 3 case 2 (needs, in each case dir: analysis.json [analyze_solve.py], sections_<mode>.csv [lesion_sections.py],
wss_<mode>.csv/json [reattachment_wss.py]; lesion case also zerod_reference.json).
usage: compare_lesion.py <solve_lesion80> <solve_baseline_ref> <out_prefix>   -> <out_prefix>.json and <out_prefix>.pdf, prints the tables.
main(les, ref, out, banner=None): banner (a short string, used by hyp_compare) is drawn in red as the figure suptitle; with banner=None json and pdf are unchanged."""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from zerod_ffr import P_AORTA, MMHG
from build_lesion80_surface import S_C, PR

def at(df, col, s):
    d = df.dropna(subset=[col]); d = d[(d.s_mm - s).abs() < 1e-6]
    if len(d) != 1: raise SystemExit(f"no valid section at s={s} mm for {col}: refusing to substitute a neighbouring station")
    return float(d.iloc[0][col]), float(d.iloc[0].s_mm)

def main(les, ref, out, banner=None):
    A_l = json.load(open(f"{les}/analysis.json")); A_r = json.load(open(f"{ref}/analysis.json"))
    Z = json.load(open(f"{les}/zerod_reference.json"))
    S_l = pd.read_csv(f"{les}/sections_lesion80.csv"); S_r = pd.read_csv(f"{ref}/sections_baseline_ref.csv")
    W_l = pd.read_csv(f"{les}/wss_lesion80.csv"); W_r = pd.read_csv(f"{ref}/wss_baseline_ref.csv")
    Wj_l = json.load(open(f"{les}/wss_lesion80.json")); Wj_r = json.load(open(f"{ref}/wss_baseline_ref.json"))
    R = dict(verdicts=dict(lesion=A_l["verdict"], reference=A_r["verdict"]))
    # ---- flow split
    fl = {}
    for p, d in A_l["outlets"].items():
        q_l, q_r = d["Q_mls"], A_r["outlets"][p]["Q_mls"]
        z = Z["outlets"][p]
        fl[p] = dict(Q_lesion=q_l, Q_ref=q_r, delta_3D_pct=100 * (q_l / q_r - 1), delta_0D_edt_pct=100 * (z["Q0_mls"] / z["Q0_healthy_mls"] - 1),
                     delta_0D_area_pct=100 * (z["Q0_areaVariant_mls"] / z["Q0_healthy_mls"] - 1))
    tin_l, tin_r = A_l["sum_outlets_mls"], A_r["sum_outlets_mls"]
    fl["total"] = dict(Q_lesion=tin_l, Q_ref=tin_r, delta_3D_pct=100 * (tin_l / tin_r - 1), delta_0D_edt_pct=100 * (Z["inflow_mls"] / Z["inflow_healthy_mls"] - 1),
                       delta_0D_area_pct=100 * (Z["inflow_areaVariant_mls"] / Z["inflow_healthy_mls"] - 1))
    R["flow"] = fl
    # ---- pressure across the lesion (valid stations only), per model
    ok_l, ok_r = S_l[S_l.ok.astype(bool)], S_r[S_r.ok.astype(bool)]
    pr = {}
    for name, (s_from, s_to) in dict(prox_to_throat=(PR["S_UP"], S_C), throat_to_distal=(S_C, PR["S_DOWN"]), prox_to_distal=(PR["S_UP"], PR["S_DOWN"])).items():
        row = {}
        for tag, df, col in (("3D_lesion", ok_l, "p_over_Pao"), ("3D_ref", ok_r, "p_over_Pao"), ("0D_edt", ok_l, "p0D_edt_over_Pao"), ("0D_area", ok_l, "p0D_area_over_Pao"), ("0D_healthy", ok_r, "p0D_healthy_over_Pao")):
            if col not in df.columns: continue
            a, sa = at(df, col, s_from); b, sb = at(df, col, s_to); row[tag] = dict(drop_over_Pao=a - b, drop_mmHg=(a - b) * P_AORTA / MMHG, s_from=sa, s_to=sb)
        row["added_by_lesion_3D_mmHg"] = row["3D_lesion"]["drop_mmHg"] - row["3D_ref"]["drop_mmHg"]
        row["added_by_lesion_0D_edt_mmHg"] = row["0D_edt"]["drop_mmHg"] - row["0D_healthy"]["drop_mmHg"]
        row["added_by_lesion_0D_area_mmHg"] = row["0D_area"]["drop_mmHg"] - row["0D_healthy"]["drop_mmHg"]
        pr[name] = row
    R["pressure"] = pr
    thr = S_l.iloc[(S_l.s_mm - S_C).abs().argmin()]
    R["throat"] = dict(Q_mls=float(thr.Q_mls), Re_area_eq=float(thr.Re_area_eq), umax_ms=float(thr.umax_ms), area_mm2=float(thr.area_mm2), area_expected_mm2=float(thr.area_expected_mm2),
                       frac_reversed_area_at_throat=float(thr.frac_reversed_area))
    post = ok_l[(ok_l.s_mm > S_C) & (ok_l.s_mm < PR["JUNCTION"])]
    rev = post[post.frac_reversed_area >= 0.01]
    R["reversed_axial_velocity_sections"] = dict(max_fraction=float(post.frac_reversed_area.max()) if len(post) else None,
                                                  s_of_max=float(post.s_mm.values[post.frac_reversed_area.values.argmax()]) if len(post) else None,
                                                  last_section_ge_1pct=float(rev.s_mm.max()) if len(rev) else None, n_valid_sections=int(len(post)))
    R["wss"] = dict(lesion=Wj_l, reference=Wj_r)
    json.dump(R, open(out + ".json", "w"), indent=1, default=float)
    # ---- print
    print(f"verdicts: {R['verdicts']}")
    print(f"{'outlet':11s} {'Q_les':>9s} {'Q_ref':>9s} {'d3D %':>8s} {'d0D edt':>8s} {'d0D area':>9s}")
    for p, d in fl.items():
        print(f"{p:11s} {d['Q_lesion']:9.5f} {d['Q_ref']:9.5f} {d['delta_3D_pct']:+8.2f} {d['delta_0D_edt_pct']:+8.2f} {d['delta_0D_area_pct']:+9.2f}")
    for name, row in pr.items():
        print(f"{name:16s} 3D lesion {row['3D_lesion']['drop_mmHg']:7.3f} mmHg  3D ref {row['3D_ref']['drop_mmHg']:7.3f}  added(3D) {row['added_by_lesion_3D_mmHg']:7.3f}  | 0D edt {row['added_by_lesion_0D_edt_mmHg']:7.3f}  0D area {row['added_by_lesion_0D_area_mmHg']:7.3f}")
    print("throat:", R["throat"]); print("reversed-velocity sections:", R["reversed_axial_velocity_sections"]); print("WSS lesion:", Wj_l["outcome"], "| reference:", Wj_r["outcome"])
    # ---- figure
    fig, ax = plt.subplots(2, 2, figsize=(11, 8))
    a = ax[0, 0]
    a.plot(ok_r.s_mm, ok_r.p_over_Pao, "k-", label="3D reference"); a.plot(ok_l.s_mm, ok_l.p_over_Pao, "r-", label=f"3D {PR['LABEL']}")
    a.plot(ok_r.s_mm, ok_r.p0D_healthy_over_Pao, "k--", label="0D healthy"); a.plot(ok_l.s_mm, ok_l.p0D_edt_over_Pao, "r--", label="0D lesion (EDT r)")
    a.plot(ok_l.s_mm, ok_l.p0D_area_over_Pao, "m:", label="0D lesion (area r)")
    a.axvline(S_C, color="gray", lw=0.5); a.axvline(PR["JUNCTION_OSTIUM"], color="gray", ls=":", lw=0.7); a.set_xlim(*PR["XLIM"]); a.set_xlabel("arc s (mm)"); a.set_ylabel(r"section-mean static p / $P_{aorta}$"); a.legend(fontsize=7)
    a.set_title(f"(a) pressure along the LAD (dotted vertical: {PR['JUNCTION_NAME']} ostium)", fontsize=9)
    a = ax[0, 1]; a.plot(ok_l.s_mm, ok_l.area_mm2, "r-", label="lesion area"); a.plot(ok_r.s_mm, ok_r.area_mm2, "k-", label="reference area"); a.set_yscale("log"); a.set_xlim(*PR["XLIM"])
    a2 = a.twinx(); a2.plot(ok_l.s_mm, ok_l.Q_mls, "b.-", ms=3, label="lesion Q"); a2.set_ylabel("Q (mL/s)", color="b"); a.set_xlabel("arc s (mm)"); a.set_ylabel("section area (mm$^2$)"); a.legend(fontsize=7, loc="lower left")
    a.set_title("(b) section area and flux", fontsize=9)
    a = ax[1, 0]; a.plot(W_l.s_mm, W_l.tau_mean_Pa, "r-", label="lesion mean"); a.plot(W_l.s_mm, W_l.tau_min_Pa, "r:", label="lesion min"); a.plot(W_r.s_mm, W_r.tau_mean_Pa, "k-", label="reference mean")
    a.axhline(0, color="gray", lw=0.5); a.axvline(PR["JUNCTION_OSTIUM"], color="gray", ls=":", lw=0.7); a.set_yscale("symlog", linthresh=0.1); a.set_xlabel("arc s (mm)"); a.set_ylabel("forward-positive axial WSS (Pa)"); a.legend(fontsize=7); a.set_title("(c) axial WSS", fontsize=9)
    a = ax[1, 1]; a.plot(W_l.s_mm, W_l.f_rev, "r-", label="lesion: reversed-WSS wall fraction"); a.plot(ok_l.s_mm, ok_l.frac_reversed_area, "b--", label="lesion: reversed-velocity section-area fraction")
    a.plot(W_r.s_mm, W_r.f_rev, "k-", label="reference: reversed-WSS wall fraction"); a.axvline(PR["JUNCTION_OSTIUM"], color="gray", ls=":", lw=0.7); a.axvline(PR["JUNCTION"], color="gray", lw=0.5)
    a.set_xlim(*PR["XLIM"]); a.set_xlabel("arc s (mm)"); a.set_ylabel("fraction"); a.legend(fontsize=7); a.set_title(f"(d) recirculation indicators (solid vertical: junction-censoring edge s={PR['JUNCTION']:g})", fontsize=9)
    if banner is not None:   # hyp_compare (HYP4 finding 3): pair validity / 5b mesh support / not-assessable statements in red on top of the figure; banner=None: figure unchanged
        fig.suptitle(banner, color="red", fontsize=8, fontweight="bold", va="top", y=0.995); fig.tight_layout(rect=(0, 0, 1, 1 - 0.022 * (banner.count("\n") + 1) - 0.01))
    else: fig.tight_layout()
    fig.savefig(out + ".pdf"); print("wrote", out + ".json", out + ".pdf")

if __name__ == "__main__":
    main(*sys.argv[1:4])
