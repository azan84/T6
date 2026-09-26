import pandas as pd, numpy as np
R = "/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 30)
B = np.arange(0.65, 0.9501, 0.05)
def bidx(f):
    if not np.isfinite(f) or f < B[0] or f >= B[-1]: return -1
    return int(np.searchsorted(B, f, "right") - 1)
d = pd.read_csv(R + "results/discrete_arm_eligibility.csv"); e = d[d.eligible].copy()
same = e.ffr_discrete.map(bidx) == e.ffr_leaky.map(bidx)
print("band holds (index):", same.sum(), "| eligible&deletable&same:", (e.deletable_branch & same).sum(), e[e.deletable_branch & same].vessel.value_counts().to_dict())
print("shift min/max:", (e.ffr_discrete - e.ffr_leaky).min().round(4), (e.ffr_discrete - e.ffr_leaky).max().round(4))
print("distinct trees that built under discrete (n_outlets notna):", d[d.n_outlets.notna()].groupby(["scan","side"]).ngroups, "| trees eligible:", e.groupby(["scan","side"]).ngroups)
cfd = pd.read_csv(R + "protocol/CFD-SUBSET-FROZEN-2026-09-18.csv"); print("subset L_mm:", cfd.L_mm.value_counts().to_dict(), "ds:", sorted(cfd.ds_pct.unique()))
c = pd.read_csv(R + "protocol/COHORT-FROZEN-2026-09-18.csv")
print(pd.crosstab(c.ds_pct, c.band).to_string())
for f in ["E0_prevalence_test_PRE-LESIONRULE.csv", "E0_prevalence_test_PRE-V9FIX.csv"]:
    e0 = pd.read_csv(R + "results/" + f)
    for mode in ["murray", "territory"]:
        x = e0[(e0["mode"] == mode) & np.isclose(e0.scale, 1.0)].min_ffr_main
        print(f, mode, "in[0.70,0.90)=", ((x >= .7) & (x < .9)).sum(), "in[0.75,0.85)=", ((x >= .75) & (x < .85)).sum(), "<=0.80=", (x <= .8).sum())
s = pd.read_csv(R + "results/ablation_smoke.csv")
print("T2 meas_same_point:", s[s.error_type == "T2_truncation"].meas_same_point.value_counts(dropna=False).to_dict())
print("T1 meas_same_point:", s[s.error_type == "T1_missed_branch"].meas_same_point.value_counts(dropna=False).to_dict())
print("has fit_n_basins col:", "fit_n_basins" in s.columns)
print("skipped reasons:", s[s.status != "ok"].status.value_counts().to_dict())
print("smoke instances:", s[["scan","side","vessel","loc","ds_pct"]].drop_duplicates().to_string())
