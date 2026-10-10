import sys, warnings; warnings.filterwarnings("ignore")
sys.path.insert(0, "code")
from summarise_revision import load
from statsmodels.stats.proportion import proportion_confint
import pandas as pd
R = "results/"
x = load(R+"ablation-2026-10-07.csv", R+"ablation-perterritory-2026-10-08.csv", R+"discrete_arm_eligibility.csv")
d = x.dropna(subset=["outlet_flow_residual"]).copy()
def ci(k,n):
    lo,hi = proportion_confint(k,n,method="wilson"); return f"{100*k/n:.0f} ({100*lo:.0f}--{100*hi:.0f})"
PR={"A_fixed":"A","B_rederived":"B","C_flowmatched":"C","D_perterritory":"D"}
rows=[]
for bed in ("discrete","leaky"):
    for grp,gl in (("topo","T1+T2"),("all","All")):
        for p,pl in PR.items():
            g=d[(d.bed==bed)&(d.protocol==p)]
            if grp=="topo": g=g[g.cls=="topo"]
            out={}
            for thr in (0.10,0.13,0.16):
                ps=g.outlet_flow_residual<thr; pw=int((ps&(g.dFFR.abs()>0.05)).sum()); out[thr]=ci(pw,len(g))
            ps=g.outlet_flow_residual<0.10; npass=int(ps.sum()); pw=int((ps&(g.dFFR.abs()>0.05)).sum())
            wp=ci(pw,npass) if npass else "--"
            rows.append(f"{bed.capitalize()} & {gl} & {pl} & {len(g)} & {out[0.10]} & {out[0.13]} & {out[0.16]} & {npass} & {wp} \\\\")
open("drafts/manuscript/supplement_tables/tab_thresholds.tex","w").write("\n".join(rows)+"\n")
