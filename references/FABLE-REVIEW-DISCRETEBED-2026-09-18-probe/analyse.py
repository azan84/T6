"""Summarise cohort_*.csv from bedprobe.py. Prints everything; writes nothing but this stdout (redirect to analyse.txt)."""
import numpy as np, pandas as pd, sys
from pathlib import Path
HERE = Path(__file__).parent; pre = sys.argv[1] if len(sys.argv) > 1 else "cohort"
pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
tr = pd.read_csv(HERE / f"{pre}_tree.csv"); lf = pd.read_csv(HERE / f"{pre}_leaf.csv"); sl = pd.read_csv(HERE / f"{pre}_slot.csv"); er = pd.read_csv(HERE / f"{pre}_err.csv")
SCH = ["share", "leaf3", "leaf266", "apport", "origin", "length"]
print(f"trees {len(tr)}  leaves(0.75,share) {len(lf)}  slot rows {len(sl)}  err rows {len(er)}")
print(f"inlet r_ref mm: median {tr.r_in.median():.2f} IQR {tr.r_in.quantile(.25):.2f}-{tr.r_in.quantile(.75):.2f}")

print("\n=== A. Leaf r_ref spread at 0.75 mm truncation (all trees) ===")
q = lf.r_leaf.quantile([0, .1, .25, .5, .75, .9, .95, 1]).round(3); print("r_leaf mm quantiles:", q.to_dict())
print(f"fraction of leaves with r_leaf < 0.80 mm: {(lf.r_leaf < 0.80).mean():.3f};  < 0.85: {(lf.r_leaf < 0.85).mean():.3f};  >= 1.0: {(lf.r_leaf >= 1.0).mean():.3f}")
g = lf.groupby(["scan", "side"])
cv = g.apply(lambda d: (d.r_leaf ** 3).std() / (d.r_leaf ** 3).mean() if len(d) > 1 else np.nan, include_groups=False)
ratio = g.apply(lambda d: (d.r_leaf ** 3).max() / (d.r_leaf ** 3).min() if len(d) > 1 else np.nan, include_groups=False)
print(f"per-tree CV of leaf r^3 (trees with >=2 outlets, n={cv.notna().sum()}): median {cv.median():.3f}, IQR {cv.quantile(.25):.3f}-{cv.quantile(.75):.3f}")
print(f"per-tree max/min leaf r^3 ratio: median {ratio.median():.2f}, p90 {ratio.quantile(.9):.2f}")
sr = g.apply(lambda d: (d.w_share.max() / d.w_share.min()) if len(d) > 1 else np.nan, include_groups=False)
print(f"per-tree max/min SHARE weight ratio: median {sr.median():.2f}, p90 {sr.quantile(.9):.2f}")
print(f"main-vessel leaves: mean share weight {lf[lf.is_main].w_share.mean():.3f} vs leaf3-normalised {lf[lf.is_main].w_leaf3.mean():.3f}; side-branch leaves {lf[~lf.is_main].w_share.mean():.3f} vs {lf[~lf.is_main].w_leaf3.mean():.3f}")

print("\n=== B. Tree level, 0.75 mm, per scheme (min FFR over resolved main vessels; offset vs leaky) ===")
print(f"leaky: minFFR median {tr.leaky_minffr.median():.3f}; healthy-network outlet FFR min: median {tr.leaky_healthy_outlet_ffr_min.median():.3f}, <0.90 in {(tr.leaky_healthy_outlet_ffr_min < .9).sum()}; outlets median {tr.leaky_nout.median():.0f}; leaf weight fraction median {tr.leaky_leafw_frac.median():.3f}")
for sc in SCH:
    k = f"0.75_{sc}"; d = tr[f"minffr_{k}"] - tr.leaky_minffr; dis = ((tr[f"minffr_{k}"] <= .8) != (tr.leaky_minffr <= .8))
    print(f"{sc:8s} minFFR median {tr[f'minffr_{k}'].median():.3f}; offset mean {d.mean():+.3f} sd {d.std():.3f} min {d.min():+.3f}; decision disagreement {dis.sum()}/{len(tr)}; "
          f"healthy outlet FFR min median {tr[f'hout_{k}'].median():.3f} (<0.90: {(tr[f'hout_{k}'] < .9).sum()}); healthy main FFR min <0.90: {(tr[f'hmain_{k}'] < .9).sum()}; "
          f"non-conv {(~tr[f'conv_{k}'].astype(bool)).sum()}; nan {tr[f'minffr_{k}'].isna().sum()}")
k = "0.75_share"
print(f"outlets at 0.75: median {tr[f'nout_{k}'].median():.0f}; single-outlet trees {(tr[f'nout_{k}'] == 1).sum()}/{len(tr)}; by side:", tr.groupby("side")[f"nout_{k}"].apply(lambda x: int((x == 1).sum())).to_dict())
one = tr[f"nout_{k}"] == 1
print(f"single-outlet trees: leaky minFFR median {tr[one].leaky_minffr.median():.3f} vs discrete {tr[one][f'minffr_{k}'].median():.3f}; offset mean {(tr[one][f'minffr_{k}'] - tr[one].leaky_minffr).mean():+.3f}; healthy main FFR min median {tr[one][f'hmain_{k}'].median():.3f}")
print(f"multi-outlet trees: offset mean share {(tr[~one]['minffr_0.75_share'] - tr[~one].leaky_minffr).mean():+.3f}, leaf3 {(tr[~one]['minffr_0.75_leaf3'] - tr[~one].leaky_minffr).mean():+.3f}, apport {(tr[~one]['minffr_0.75_apport'] - tr[~one].leaky_minffr).mean():+.3f}")
# represented-capacity ratio
tr["cap_ratio"] = np.nan
capr = lf.groupby(["scan", "side"]).w_leaf3.sum().rename("cap_ratio")
tr = tr.drop(columns="cap_ratio").merge(capr, on=["scan", "side"], how="left")
print(f"represented capacity sum(r_leaf^3)/r_in^3 at 0.75: median {tr.cap_ratio.median():.3f} IQR {tr.cap_ratio.quantile(.25):.3f}-{tr.cap_ratio.quantile(.75):.3f}")
print("corr(healthy main FFR min, cap_ratio) share:", round(tr["hmain_0.75_share"].corr(tr.cap_ratio), 3), " corr(offset, hmain):", round((tr["minffr_0.75_share"] - tr.leaky_minffr).corr(tr["hmain_0.75_share"]), 3))
# Q5: calibration pathology
for T in ("0.50", "0.60", "0.75", "0.90", "1.00"):
    k = f"{T}_share"; bad = tr[f"C_{k}"] < 1e-2; nanq = tr[f"Qin_{k}"].isna() & tr[f"nout_{k}"].gt(0)
    print(f"  T={T}: C<1e-2 in {bad.sum()}, Qin nan in {nanq.sum()}, C median {tr[f'C_{k}'].median():.2f} (leaky C median n/a)")

print("\n=== C. Slot level (one 65 %DS lesion per host vessel), 0.75 mm, per scheme ===")
s75 = sl[(sl["T"] == 0.75) & sl.meas_active]
for sc in SCH:
    d = s75[s75.scheme == sc]
    lq = np.log(d.Qh_meas / d.Qh_meas_leaky); ll = np.log(d.Qh_les / d.Qh_les_leaky)
    db = d.base_meas - d.base_meas_leaky; dl = d.les65_meas - d.les65_meas_leaky
    fl = (d.les65_meas <= .8) != (d.les65_meas_leaky <= .8)
    print(f"{sc:8s} n={len(d)}: healthy Q at meas node / leaky: median x{np.exp(lq.median()):.2f} IQR x{np.exp(lq.quantile(.25)):.2f}-x{np.exp(lq.quantile(.75)):.2f}, |log| mean {lq.abs().mean():.3f}; at lesion node x{np.exp(ll.median()):.2f} (|log| mean {ll.abs().mean():.3f}); "
          f"baseline FFR_meas offset {db.mean():+.3f} (sd {db.std():.3f}); 65%DS FFR_meas offset {dl.mean():+.3f} (sd {dl.std():.3f}); decision disagreement at 65%DS {fl.sum()}/{len(d)}; healthy FFR_meas median {d.hffr_meas.median():.3f}, <0.90 {(d.hffr_meas < .9).sum()}")
d = s75[s75.scheme == "share"]
print(f"leaky 65%DS FFR_meas: median {d.les65_meas_leaky.median():.3f}, <=0.80 in {(d.les65_meas_leaky <= .8).mean():.2f};  share: median {d.les65_meas.median():.3f}, <=0.80 in {(d.les65_meas <= .8).mean():.2f}")
for sc in ("share", "leaf3", "apport"):
    d = s75[s75.scheme == sc]
    for lab, m in (("single-outlet", d.nout == 1), ("multi-outlet", d.nout > 1)):
        dd = d[m]; lq = np.log(dd.Qh_meas / dd.Qh_meas_leaky)
        print(f"   {sc} {lab} n={len(dd)}: Q ratio median x{np.exp(lq.median()):.2f}; 65%DS offset {(dd.les65_meas - dd.les65_meas_leaky).mean():+.3f}; healthy FFR_meas<0.90: {(dd.hffr_meas < .9).sum()}")

print("\n=== D. Truncation sweep (share and leaf3) ===")
for T in (0.5, 0.6, 0.75, 0.9, 1.0):
    kT = f"{T:.2f}"; s = sl[(sl["T"] == T) & (sl.scheme == "share")]
    sa = s[s.meas_active]
    print(f"T={kT}: outlets median {tr[f'nout_{kT}_share'].median():.0f}, single {(tr[f'nout_{kT}_share'] == 1).sum()}, zero {(tr[f'nout_{kT}_share'] == 0).sum()} | slots: meas node retained {s.meas_active.mean():.2f}; >=1 downstream branch retained {(sa.n_dn_br_ret >= 1).mean():.2f} (of slots with any: {(sa[sa.n_dn_br_all >= 1].n_dn_br_ret >= 1).mean():.2f}); "
          f"run-off retained median {sa.runoff_ret_mm.median():.0f} mm | healthy FFR_meas median {sa.hffr_meas.median():.3f}, <0.90 {(sa.hffr_meas < .9).mean():.2f} | "
          f"minFFR offset vs leaky: share {(tr[f'minffr_{kT}_share'] - tr.leaky_minffr).mean():+.3f}, leaf3 {(tr[f'minffr_{kT}_leaf3'] - tr.leaky_minffr).mean():+.3f} | 65%DS offset share {(sa.les65_meas - sa.les65_meas_leaky).mean():+.3f}")
    s3 = sl[(sl["T"] == T) & (sl.scheme == "leaf3") & sl.meas_active]
    print(f"        leaf3: 65%DS offset {(s3.les65_meas - s3.les65_meas_leaky).mean():+.3f}, disagreement {((s3.les65_meas <= .8) != (s3.les65_meas_leaky <= .8)).sum()}/{len(s3)}; healthy Q ratio at meas median x{np.exp(np.log(s3.Qh_meas / s3.Qh_meas_leaky).median()):.2f}")

print("\n=== E. Error-induced dFFR at the measurement node (65 %DS lesion), leaky vs discrete schemes ===")
er = er[er.error.isna()] if "error" in er.columns else er
er = er[~er.meas_lost.astype(bool)]
for etype in ("T1", "T4"):
    e = er[er.err == etype]
    piv = {}
    for bed in ("leaky", "share", "leaf3", "apport"):
        d = e[e.bed == bed].set_index(["scan", "side", "vessel"])
        for p in "ABC": piv[(bed, p)] = d[p] - d.clean
        piv[(bed, "clean")] = d.clean
    piv = pd.DataFrame(piv)
    print(f"\n-- {etype}: n instances {len(piv)}")
    for p in "ABC":
        line = f"  protocol {p}: mean|d| "
        for bed in ("leaky", "share", "leaf3", "apport"):
            x = piv[(bed, p)]; fl = ((piv[(bed, 'clean')] + x <= .8) != (piv[(bed, 'clean')] <= .8))
            line += f"{bed} {x.abs().mean():.3f} (flips {fl.sum()}) | "
        print(line)
        for a, b in (("leaky", "share"), ("leaky", "leaf3"), ("leaky", "apport"), ("share", "leaf3")):
            x, y = piv[(a, p)], piv[(b, p)]; ok = x.notna() & y.notna()
            sgn = (np.sign(x[ok]) == np.sign(y[ok])).mean()
            fa = ((piv[(a, 'clean')] + x <= .8) != (piv[(a, 'clean')] <= .8)); fb = ((piv[(b, 'clean')] + y <= .8) != (piv[(b, 'clean')] <= .8))
            print(f"      {a} vs {b}: r={x[ok].corr(y[ok]):.2f} spearman={x[ok].corr(y[ok], method='spearman'):.2f} sign-agree {sgn:.2f}; flips both {int((fa & fb).sum())} / either {int((fa | fb).sum())} / a-only {int((fa & ~fb).sum())} / b-only {int((~fa & fb).sum())}")
    # cohort-level claim test: does B reduce |d| relative to A, and C relative to A, in each bed?
    for bed in ("leaky", "share", "leaf3", "apport"):
        a, b, c = piv[(bed, "A")].abs(), piv[(bed, "B")].abs(), piv[(bed, "C")].abs()
        print(f"  cohort claim in {bed}: mean|dA| {a.mean():.3f}  mean|dB| {b.mean():.3f}  mean|dC| {c.mean():.3f}  ->  B<A in {(b < a).mean():.2f} of instances, C<A in {(c < a).mean():.2f}")
    # near-threshold subset under each bed
    for bed in ("leaky", "share", "leaf3"):
        c = piv[(bed, "clean")]; near = c.between(.7, .9)
        print(f"  near-threshold (0.70-0.90 clean) under {bed}: {near.sum()} instances; flips A/B/C: {[int(((c[near] + piv[(bed, p)][near] <= .8) != (c[near] <= .8)).sum()) for p in 'ABC']}")

print("\n=== F. Exclusion-rule test on the share / leaf3 schemes (0.75 mm) ===")
for rule, m in (("none", np.ones(len(tr), bool)), ("nout>=2", tr["nout_0.75_share"] >= 2), ("healthy main FFR>=0.90", tr["hmain_0.75_share"] >= .9), ("healthy main FFR>=0.92", tr["hmain_0.75_share"] >= .92), ("cap_ratio>=0.25", tr.cap_ratio >= .25)):
    for sc in ("share", "leaf3"):
        d = tr[m][f"minffr_0.75_{sc}"] - tr[m].leaky_minffr; dis = ((tr[m][f"minffr_0.75_{sc}"] <= .8) != (tr[m].leaky_minffr <= .8))
        print(f"  {rule:24s} {sc:6s} keeps {m.sum()}/{len(tr)}: offset mean {d.mean():+.3f} sd {d.std():.3f} min {d.min():+.3f}; disagreement {dis.sum()}; r={tr[m][f'minffr_0.75_{sc}'].corr(tr[m].leaky_minffr):.2f}")
