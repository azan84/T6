"""Cohort-wide GEOMETRY census for the final pre-flight (no ablation results are produced: one clean solve per
instance, then only tree construction and node-set bookkeeping for each error type).

Per (instance, bed, error type):
  n_terr_clean   Protocol C territory count under the CURRENT code (clean partition, protocol_c_targets)
  n_terr_corr    territory count under the corrupted-tree partition (what export_cfd_case.py still uses)
  tgt_clean_sum  sum of Protocol C targets, clean partition   (mL/s)
  tgt_corr_sum   sum of exporter-style full-territory targets (corrupted partition, subtree(t, root_clean))
  only_t2 / only_t   active nodes present only in the corrupted / only in the clean tree (node-set identity)
  T4 extra: node-set deltas for trunc_ref-with-base-radius (is trunc_for redundant?) and trunc_for-only (old B3)
  meas_survives  the clean measurement node exists in the corrupted tree
"""
import sys, time, traceback
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "code"))
from zerod_ffr import Tree, R_TRUNC, R_TRUNC_DISCRETE
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES
from ablation import node_map, bed_flow, territories, subtree, trunc_for, CALIBRE_ONLY, protocol_c_targets

ROOT = Path.home() / "Datasets/imagecas-x/ImageCAS-X_dataset"
coh = pd.read_csv(HERE / "protocol" / "COHORT-FROZEN-2026-09-18.csv").sort_values(["scan", "side"])
sub = pd.read_csv(HERE / "protocol" / "CFD-SUBSET-FROZEN-2026-09-18.csv")
in3d = set(zip(sub.scan, sub.side, sub.vessel, sub["loc"], sub.L_mm, sub.ds_pct))
keyset = lambda t: set(map(tuple, np.round(t.xyz[t.active], 9)))
rows, t0 = [], time.time()
for bed in ("leaky", "discrete"):
    for n, (_, r) in enumerate(coh.iterrows(), 1):
        base = dict(bed=bed, scan=int(r.scan), side=r.side, vessel=r.vessel, loc=r["loc"], L_mm=r.L_mm, ds_pct=int(r.ds_pct),
                    in_3d_subset=(r.scan, r.side, r.vessel, r["loc"], r.L_mm, r.ds_pct) in in3d)
        try:
            t = load(ROOT, int(r.scan), r.side, bed)
            o = t.ffr("murray", 1.0); C = o["C"]
            slots, _ = plan(t, r.side, t.last["ffr"].copy())
            sl = next((s for s in slots if s["vessel"] == r.vessel and s["loc"] == r["loc"] and abs(s["L"] * 1e3 - r.L_mm) < 1e-6), None)
            if sl is None:
                rows.append({**base, "error_type": "", "status": "slot not eligible"}); continue
            path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
            meas_clean = int(path[mi])
            r_clean, _ = insert(t, path, s_arc, c, L, r.ds_pct / 100)
            ffr0, _, info0, _, _ = t.evaluate(C, r_clean); q0_all = bed_flow(t, C, ffr0)
            kt = keyset(t); n_terr_t = len(territories(t))
            for etype, fn in ERROR_TYPES.items():
                rec = {**base, "error_type": etype, "n_leaves_clean": len(t.leaves), "n_terr_cleantree": n_terr_t,
                       "n_active_clean": int(t.active.sum())}
                segs2, info = fn(list(t.segments), t, path, s_arc, c, L)
                if segs2 is None:
                    rec["status"] = f"skipped: {info}"; rows.append(rec); continue
                try:
                    t2 = Tree(segs2, f"{t.name}_{etype}", bed=bed, r_trunc=trunc_for(bed, etype),
                              trunc_ref=t if etype in CALIBRE_ONLY else None)
                except ValueError as e:
                    rec["status"] = f"skipped: {str(e)[:50]}"; rows.append(rec); continue
                m = node_map(t, t2)
                p2, _ = t2.vessel_path(HOSTS[r.side][r.vessel])
                if p2 is None or len(p2) < 3:
                    rec["status"] = "skipped: host vessel lost"; rows.append(rec); continue
                pairs = protocol_c_targets(t, t2, m, q0_all)
                terr2 = territories(t2)
                corr = []
                for s_ in terr2:
                    rc = int(m[int(s_[0])])
                    corr.append(float(q0_all[subtree(t, rc)].sum()) if rc >= 0 else np.nan)
                k2 = keyset(t2)
                rec.update(status="ok", n_terr_clean=len(pairs), n_terr_corr=len(terr2),
                           tgt_clean_sum=sum(q for _, q in pairs) * 1e6, tgt_corr_sum=float(np.nansum(corr)) * 1e6,
                           corr_root_unmapped=int(sum(1 for x in corr if np.isnan(x))),
                           only_t2=len(k2 - kt), only_t=len(kt - k2), n_active_corr=int(t2.active.sum()),
                           n_leaves_corr=len(t2.leaves), meas_survives=bool((m == meas_clean).any()),
                           terr_min_members=min((len(mem) for mem, _ in pairs), default=0))
                if etype == "T4_taper":
                    try:
                        tb = Tree(segs2, "b", bed=bed, trunc_ref=t)                       # trunc_ref, base radius
                        kb = keyset(tb); rec.update(T4_ref_only_only_t=len(kt - kb), T4_ref_only_only_t2=len(kb - kt))
                    except ValueError as e:
                        rec.update(T4_ref_only_err=str(e)[:40])
                    try:
                        tc = Tree(segs2, "c", bed=bed, r_trunc=trunc_for(bed, etype))    # old B3: trunc_for only
                        kc = keyset(tc); rec.update(T4_for_only_only_t=len(kt - kc), T4_for_only_only_t2=len(kc - kt))
                    except ValueError as e:
                        rec.update(T4_for_only_err=str(e)[:40])
                rows.append(rec)
        except Exception as e:
            rows.append({**base, "error_type": "", "status": f"FAIL {e.__class__.__name__}: {str(e)[:60]}"})
            traceback.print_exc()
        if n % 25 == 0: print(f"  {bed} {n}/{len(coh)}  {time.time()-t0:.0f}s", flush=True)
df = pd.DataFrame(rows); df.to_csv(sys.argv[1], index=False)
print(f"wrote {sys.argv[1]} {df.shape} in {time.time()-t0:.0f}s")
