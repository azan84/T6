"""supplement_tables.py — LaTeX tables for the Supplementary Material from the analysis folder and CFD returns.
usage: supplement_tables.py <analysis_dir> <out_dir>"""
import sys
from pathlib import Path
import pandas as pd
an, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
P6 = Path(__file__).parent.parent
ET = {"T1_missed_branch": "T1", "T2_truncation": "T2", "T3_stenosis_length": "T3", "T4_taper": "T4"}
PR = {"A_fixed": "A", "B_rederived": "B", "C_flowmatched": "C"}

def term(t):
    t = t.replace("C(error_type)[T.", "").replace("C(protocol)[T.", "").replace("]", "")
    for k, v in {**ET, **PR, "B_rederived": "B", "C_flowmatched": "C"}.items(): t = t.replace(k, v)
    return t.replace(":", r" $\times$ ").replace("ds_pct", "Severity (\\% DS)").replace("L_mm", "Length (mm)")

# S-Table 1: VB mixed model, both beds
d = pd.read_csv(an / "P1_glmm_vb_discrete.csv", index_col=0); l = pd.read_csv(an / "P1_glmm_vb_leaky.csv", index_col=0)
rows = [r for r in d.index if not r.startswith("C(band_c)")]
with open(out / "tab_glmm.tex", "w") as f:
    for r in rows:
        a, b = d.loc[r], l.loc[r]
        fm = ".3f" if r == "ds_pct" else ".2f"
        f.write(f"{term(r)} & {a.post_mean:{fm}} ({a.lo95:{fm}}, {a.hi95:{fm}}) & {b.post_mean:{fm}} ({b.lo95:{fm}}, {b.hi95:{fm}}) \\\\\n")

# S-Table 2: absorption at thresholds 0.10/0.13/0.16, protocol x {topological, all}
p = pd.read_csv(an / "P2_absorption.csv")
with open(out / "tab_thresholds.tex", "w") as f:
    for bed in ("discrete", "leaky"):
        for grp, gl in (("TOPOLOGICAL", "T1+T2"), ("ALL", "All")):
            for pr, ps in PR.items():
                cells = []
                for thr in (0.10, 0.13, 0.16):
                    x = p[(p.threshold == thr) & (p.bed == bed) & (p.protocol == pr) & (p.error_type == grp)].iloc[0]
                    cells.append(f"{x.pct:.0f} ({x.lo:.0f}--{x.hi:.0f})")
                f.write(f"{bed.capitalize()} & {gl} & {ps} & {int(x.n)} & " + " & ".join(cells) + " \\\\\n")

# S-Table 3: exclusions (nonzero cells only), incl. error-type applicability rows that carry no protocol
REASON = {"skipped: fewer than 2 shared territories to match": "fewer than two territories with surviving vessels",
          "skipped: no bed left": "no node with bed outflow remains",
          "skipped: no deletable downstream branch": "no side branch distal to the lesion",
          "skipped: truncation point falls at the start of its segment": "truncation point at a segment start"}
raw = pd.read_csv(P6 / "results/ablation-2026-10-07.csv")
el = pd.read_csv(P6 / "results/discrete_arm_eligibility.csv")
key = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]
el = el[el.eligible.astype(bool)][key].assign(_e=True)
raw = raw.merge(el, on=key, how="left"); raw = raw[(raw.bed != "discrete") | raw._e.fillna(False).astype(bool)]
raw = raw[raw.error_type != "clean"]
with open(out / "tab_exclusions_nz.tex", "w") as f:
    for bed in ("discrete", "leaky"):
        for e in ET:
            g = raw[(raw.bed == bed) & (raw.error_type == e)]
            na = g[g.protocol.isna() | (g.protocol == "")]
            if len(na):
                n_inst = g[key].drop_duplicates().shape[0]
                f.write(f"{bed.capitalize()} & {ET[e]} & all & {n_inst - len(na)} of {n_inst} & "
                        + "; ".join(f"{REASON.get(k, k)}: {v}" for k, v in na.status.value_counts().items()) + " \\\\\n")
            for pr, ps in PR.items():
                h = g[g.protocol == pr]; ex = h[h.status != "ok"]
                if len(ex):
                    f.write(f"{bed.capitalize()} & {ET[e]} & {ps} & {int((h.status == 'ok').sum())} & "
                            + "; ".join(f"{REASON.get(k, k)}: {v}" for k, v in ex.status.value_counts().items()) + " \\\\\n")

# S-Table 4: simulated floor
fb = pd.read_csv(an / "floor6b.csv")
with open(out / "tab_floor.tex", "w") as f:
    for _, r in fb.iterrows():
        f.write(f"{r.bed.capitalize()} & {int(r.instances)} & {int(r.n)} & {r.flip_pct:.1f} ({r.flip_lo:.1f}--{r.flip_hi:.1f}) & "
                f"{r.median_abs_dFFR:.3f} & {r.p95_abs_dFFR:.3f} & {r.pass_pct:.0f} & {r.pass_and_wrong_pct:.1f} ({r.pw_lo:.1f}--{r.pw_hi:.1f}) \\\\\n")

# S-Table 5: 3D mesh-resolution test (D7)
m = pd.read_csv(P6 / "cfd_handover/returns/2026-10-03/M1_D7_sensitivity_2026-10-06.csv")
lab = {"A0": "Control: 25~\\textmu m, regenerated", "A1": "12.5~\\textmu m, $\\pm$4~mm", "A2": "12.5~\\textmu m, interfaces +1~mm"}
with open(out / "tab_d7.tex", "w") as f:
    for _, r in m.sort_values("variant").iterrows():
        f.write(f"{lab[r.variant]} & {r.cells/1e6:.2f} & {r.p011_over_Paorta:.4f} & {r.delta_FFR_vs_returned:+.4f} & "
                f"{r.max_outlet_flow_change_pct:.2f} & {r.D34_min_dist_throat_mm:.2f} \\\\\n")
print("wrote", sorted(x.name for x in out.iterdir()))
