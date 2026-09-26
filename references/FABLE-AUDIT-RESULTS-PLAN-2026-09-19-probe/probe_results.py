import pandas as pd, numpy as np, sys
R = "/Users/mzpi/Library/CloudStorage/GoogleDrive-Mohd.Zulhilmi@monash.edu/My Drive/Research/01 CollabProject-MonashIIUM/Imaging-Medical/Paper6-T6/"
pd.set_option("display.width", 200)

print("=== E0 ===")
e0 = pd.read_csv(R + "results/E0_prevalence_test.csv")
print("rows", len(e0), "trees", e0["name"].nunique(), "scans", e0["scan"].nunique(), "disease yes scans", e0.drop_duplicates("scan")["disease"].eq("yes").sum())
for mode, sc in [("murray", 1.0), ("territory", 1.0), ("murray", 0.7), ("murray", 1.3), ("territory", 0.7), ("territory", 1.3)]:
    d = e0[(e0["mode"] == mode) & (np.isclose(e0["scale"], sc))]
    f = d["min_ffr_main"]
    n = f.notna().sum()
    print(f"{mode:9s} {sc}: n={n} median={f.median():.3f} in[0.70,0.90)={((f>=0.70)&(f<0.90)).sum()} "
          f"in[0.75,0.85)={((f>=0.75)&(f<0.85)).sum()} <=0.80={(f<=0.80).sum()} <0.70={(f<0.70).sum()} conv_all={d['converged'].all()}")
d = e0[(e0["mode"] == "murray") & np.isclose(e0["scale"], 1.0)]
ds = d["lesion_ds_pct"]
print("trees with tightest lesion ds>=30:", (ds >= 30).sum(), "of", len(d), "| median", ds[ds>=30].median(), "p90", ds[ds>=30].quantile(0.9), "max", ds.max())
print("bands 30-40/40-50/50-60/60-70/>=70:", [((ds>=a)&(ds<b)).sum() for a,b in [(30,40),(40,50),(50,60),(60,70),(70,999)]])
print("trees with n_lesions>=1:", (d["n_lesions"] >= 1).sum())
print("median r_in_mm:", d["r_in_mm"].median(), "IQR", d["r_in_mm"].quantile([.25,.75]).values)
print("median FFR disease yes/no:", d.groupby("disease")["min_ffr_main"].median().to_dict())
print("demand ratio Q_in/Q_demand > 1.0 rows:", (e0["Q_in_mls"]/e0["Q_demand_mls"] > 1.0).sum(), "max ratio", (e0["Q_in_mls"]/e0["Q_demand_mls"]).max())
print("rows with Q_in/Q_demand > 1.0 all modes n=", len(e0))

print("\n=== COHORT ===")
c = pd.read_csv(R + "protocol/COHORT-FROZEN-2026-09-18.csv")
sel = pd.read_csv(R + "results/sweep_test_selected.csv")
print("rows", len(c), "selected rows", len(sel))
key = ["scan","side","vessel","loc","L_mm","ds_pct"]
m = c.merge(sel, on=key, how="outer", indicator=True, suffixes=("_c","_s"))
print("cohort vs selected merge:", m["_merge"].value_counts().to_dict())
print("ffr agree:", np.allclose(m["ffr_meas_c"], m["ffr_meas_s"]))
print("per band:", c["band"].value_counts().sort_index().to_dict())
print("per vessel:", c["vessel"].value_counts().to_dict())
print(pd.crosstab(c["band"], c["vessel"]))
c["tree"] = c["scan"].astype(str) + "_" + c["side"]
c["slot"] = c["scan"].astype(str) + "_" + c["side"] + "_" + c["vessel"] + "_" + c["loc"] + "_" + c["L_mm"].astype(str)
print("trees", c["tree"].nunique(), "patients", c["scan"].nunique(), "slots", c["slot"].nunique(), "slots with 2:", (c["slot"].value_counts()==2).sum(), "slots >2:", (c["slot"].value_counts()>2).sum())
pp = c.groupby("scan")["side"].nunique(); print("patients with both sides:", (pp==2).sum())
pi = c["scan"].value_counts(); print("patients with 1/2/>=3 instances:", (pi==1).sum(), (pi==2).sum(), (pi>=3).sum(), "max", pi.max())
print("L_mm:", c["L_mm"].value_counts().to_dict(), "bif_in_window:", c["bif_in_window"].sum(), "quality:", c["quality"].value_counts().sort_index().to_dict())
print(pd.crosstab(c["ds_pct"], c["band"]))
print("band derived from ffr_meas consistent:", all(((c.ffr_meas>=0.65)&(c.ffr_meas<0.95))), "ffr range", c.ffr_meas.min(), c.ffr_meas.max())
print("loc:", c["loc"].value_counts().to_dict())

print("\n=== DISCRETE ARM ===")
d = pd.read_csv(R + "results/discrete_arm_eligibility.csv")
print("rows", len(d), "eligible", d["eligible"].sum())
print("reasons:", d.loc[~d.eligible, "reason"].str.split(" ").str[0].value_counts().to_dict())
print(d.loc[~d.eligible, "reason"].str.replace(r"[0-9.]+", "#", regex=True).value_counts().to_dict())
e = d[d.eligible].copy()
shift = e["ffr_discrete"] - e["ffr_leaky"]
print(f"shift mean {shift.mean():.4f} sd {shift.std(ddof=1):.4f} sd0 {shift.std(ddof=0):.4f} median {shift.median():.4f}")
dis = ((e.ffr_discrete <= 0.80) != (e.ffr_leaky <= 0.80)).sum(); print("decision disagreement (<=0.80):", dis, " (<0.80):", ((e.ffr_discrete < 0.80) != (e.ffr_leaky < 0.80)).sum())
print("band_discrete values:", e["band_discrete"].value_counts().to_dict())
keep = (e["band_discrete"] == e["band_leaky"]).sum(); print("keep leaky band:", keep, "out of range:", (e["band_discrete"]=="out").sum())
print("inside 0.65-0.95 by value:", ((e.ffr_discrete>=0.65)&(e.ffr_discrete<0.95)).sum())
print("deletable_branch among eligible:", e["deletable_branch"].sum(), "n_branch_ge_cut>=1:", (e["n_branch_ge_cut"]>=1).sum())
print("eligible & deletable & in-band:", (e.deletable_branch & (e.band_discrete!="out")).sum())
print("eligible & in-band:", (e.band_discrete!="out").sum())
print("eligible & keep band:", keep)
# base_discrete healthy check
print("base_discrete<0.9 among eligible:", (e.base_discrete<0.9).sum(), "healthy_main<0.9 among eligible:", (e.healthy_main<0.9).sum())
print("n_outlets<2 rows:", (d.n_outlets<2).sum(), "reason strings for those:", d.loc[d.n_outlets<2,"reason"].unique())
cfd = pd.read_csv(R + "protocol/CFD-SUBSET-FROZEN-2026-09-18.csv")
print("CFD subset rows", len(cfd), "vessels", cfd.vessel.value_counts().to_dict(), "trees", (cfd.scan.astype(str)+cfd.side).nunique(), "patients", cfd.scan.nunique())
mm = cfd.merge(d, on=["scan","side","vessel","loc","L_mm","ds_pct"], how="left", suffixes=("","_e"))
print("subset all eligible:", mm.eligible.all(), "all deletable:", mm.deletable_branch.all(), "band_discrete:", mm.band_discrete.value_counts().to_dict())
print("subset in cohort:", cfd.merge(c, on=["scan","side","vessel","loc","L_mm","ds_pct"], how="inner").shape[0])
# pool: eligible & deletable ?
pool = e[e.deletable_branch]; print("pool eligible&deletable:", len(pool), "of which in-band:", (pool.band_discrete!="out").sum())
# what discrete bands the subset spans
print("subset ffr_discrete range", cfd.ffr_discrete.min(), cfd.ffr_discrete.max())
bins=[0.65,0.70,0.75,0.80,0.85,0.90,0.95]; print("subset band counts:", pd.cut(cfd.ffr_discrete,bins,right=False).value_counts().sort_index().to_dict())
print("pool band counts:", pd.cut(pool.ffr_discrete,bins,right=False).value_counts().sort_index().to_dict(), "out:", ((pool.ffr_discrete<0.65)|(pool.ffr_discrete>=0.95)).sum())

print("\n=== SMOKE ===")
s = pd.read_csv(R + "results/ablation_smoke.csv")
print("rows", len(s), "instances", s[["scan","side","vessel","loc","L_mm","ds_pct"]].drop_duplicates().shape[0])
print(s.groupby(["protocol","status"]).size())
print("status values:", s.status.str.split(":").str[0].value_counts().to_dict())
ok = s[s.status=="ok"]
print("C rows ok:", (ok.protocol=="C_matched").sum(), "protocols:", ok.protocol.unique())
print(ok.groupby(["bed","error_type","protocol"]).agg(n=("dFFR","size"), mean_abs=("dFFR", lambda x: np.abs(x).mean()), flips=("flip","sum")).round(4))
cc = ok[ok.protocol.str.startswith("C")]
print("C_ratio range", cc.C_ratio.min(), cc.C_ratio.max()); print(cc[["scan","side","vessel","bed","error_type","C_ratio","dFFR","outlet_flow_residual","flip"]].sort_values("C_ratio").to_string())
print("C rows: residual<0.10 & |dFFR|>0.05:", ((cc.outlet_flow_residual<0.10)&(cc.dFFR.abs()>0.05)).sum(), "of", len(cc))
print("columns:", list(s.columns))
