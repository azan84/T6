import sys, pandas as pd, numpy as np
d = pd.read_csv(sys.argv[1])
ok = d[d.status == "ok"].copy()
print("rows", d.shape, "| status:", d.status.value_counts().to_dict())
print("\n=== B1: Protocol C territory count under the CURRENT code (clean partition) vs the exporter's corrupted partition")
for et in ("T1_missed_branch", "T2_truncation", "T3_stenosis_length", "T4_taper"):
    for bed in ("leaky", "discrete"):
        g = ok[(ok.error_type == et) & (ok.bed == bed)]
        if g.empty: continue
        skipped = d[(d.error_type == et) & (d.bed == bed) & (d.status != "ok")]
        lt2 = g[g.n_terr_clean < 2]
        print(f"  {et:20s} {bed:9s} n_ok={len(g):3d} skipped={len(skipped):3d} | clean-partition n_terr: {g.n_terr_clean.value_counts().sort_index().to_dict()}"
              f" -> Protocol C lost (<2): {len(lt2)} ({100*len(lt2)/max(len(g),1):.0f}% of ok rows; by side {lt2.side.value_counts().to_dict()})"
              f" | corrupted-partition n_terr: {g.n_terr_corr.value_counts().sort_index().to_dict()}")
print("\n=== B1 exporter mismatch: exporter (corrupted partition) target sum vs ablation (clean partition) target sum, T1/T2 only")
for et in ("T1_missed_branch", "T2_truncation"):
    for bed in ("leaky", "discrete"):
        g = ok[(ok.error_type == et) & (ok.bed == bed) & (ok.n_terr_clean >= 2)].copy()
        g["ratio"] = g.tgt_corr_sum / g.tgt_clean_sum
        mism = g[(np.abs(g.ratio - 1) > 1e-6) | (g.n_terr_corr != g.n_terr_clean) | (g.corr_root_unmapped > 0)]
        print(f"  {et:20s} {bed:9s} n={len(g):3d} | rows where exporter partition != ablation partition or target differs: {len(mism)}"
              f" | min target ratio {g.ratio.min():.3f} | n_terr differs {int((g.n_terr_corr != g.n_terr_clean).sum())} | unmapped roots {int((g.corr_root_unmapped>0).sum())}")
        if bed == "discrete":
            s = mism[mism.in_3d_subset]
            print(f"      of which in the frozen 3D subset: {len(s)}  scans {sorted(s.scan.tolist())}")
print("\n=== B3: node-set identity, calibre-only errors (should be 0 / 0)")
for et in ("T3_stenosis_length", "T4_taper"):
    for bed in ("leaky", "discrete"):
        g = ok[(ok.error_type == et) & (ok.bed == bed)]
        print(f"  {et:20s} {bed:9s} n={len(g):3d} | current code: rows with only_t2>0: {int((g.only_t2>0).sum())}, only_t>0: {int((g.only_t>0).sum())}, max only_t {int(g.only_t.max())}"
              f" | leaves differ: {int((g.n_leaves_corr != g.n_leaves_clean).sum())}")
        if et == "T4_taper":
            print(f"      trunc_ref ALONE (base radius): rows dropping nodes {int((g.T4_ref_only_only_t>0).sum())}, max dropped {int(g.T4_ref_only_only_t.max())}, added {int((g.T4_ref_only_only_t2>0).sum())}, build errors {int(g.get('T4_ref_only_err', pd.Series(dtype=object)).notna().sum()) if 'T4_ref_only_err' in g else 0}")
            print(f"      trunc_for ALONE (old B3):      rows dropping nodes {int((g.T4_for_only_only_t>0).sum())}, added nodes {int((g.T4_for_only_only_t2>0).sum())}, max added {int(g.T4_for_only_only_t2.max())}, max dropped {int(g.T4_for_only_only_t.max())}")
print("\n=== B2: T2 measurement node survives; leaves after T2")
for bed in ("leaky", "discrete"):
    g = ok[(ok.error_type == "T2_truncation") & (ok.bed == bed)]
    print(f"  {bed:9s} n={len(g):3d} meas_survives {int(g.meas_survives.sum())}/{len(g)} | n_leaves_corr==1: {int((g.n_leaves_corr==1).sum())} (by side {g[g.n_leaves_corr==1].side.value_counts().to_dict()})")
print("\n=== T1 applicability")
for bed in ("leaky", "discrete"):
    g = d[(d.error_type == "T1_missed_branch") & (d.bed == bed)]
    print(f"  {bed:9s} {g.status.value_counts().to_dict()}")
print("\n=== per-instance failures / ineligible")
print(d[d.error_type == ""].groupby(["bed", "status"]).size().to_string())
