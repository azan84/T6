"""Probe 1b: is ln q_norm(v) just  ln G(v) + ln pi(v) - ln(C/C_clean)  where
   G(v)  = [sum_{u in subtree(v)} w(u) / r_ref(v)^3] / [sum_all w / r_ref(0)^3]     (pure anatomy: r_ref only)
   pi(v) = (P(v) - P_v)/(P_in - P_v)                                                (the pressure field the model solves)
If the remainder is small, S1 carries no information beyond {anatomy, pressure profile, C} — i.e. it is not 'free'.
Also computes the anatomy-only orphan-weight statistic at the deleted junction.  Usage: probe_s1_decomp.py <root>"""
import sys
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parents[2]; sys.path.insert(0, str(HERE / "code"))
from zerod_ffr import Tree, K_MURRAY, P_AORTA, P_VEN
from severity_sweep import load, plan, insert, HOSTS
from error_types import ERROR_TYPES
from ablation import node_map, bed_flow, territories
from scipy.optimize import minimize_scalar
root = Path(sys.argv[1])
st = pd.read_csv(Path(__file__).parent / "s1_stats.csv")
inst = st[st.case == "T1_missed_branch"].drop_duplicates(["scan", "side"])[["scan", "side", "vessel", "ds_pct"]]
coh = pd.read_csv(HERE / "protocol" / "COHORT-FROZEN-2026-09-18.csv")

def subtree_w(t):
    S = t.w.copy()
    for v in range(len(t.parent) - 1, 0, -1):
        if t.active[v]: S[t.parent[v]] += S[v]
    return S

rows = []
for _, r in inst.iterrows():
    cr = coh[(coh.scan == r.scan) & (coh.side == r.side) & (coh.vessel == r.vessel)].iloc[0]
    for bed in ("leaky", "discrete"):
        t = load(root, int(r.scan), r.side, bed); o = t.ffr(); C = o["C"]
        slots, _ = plan(t, r.side, t.last["ffr"].copy())
        sl = next(s for s in slots if s["vessel"] == cr.vessel and s["loc"] == cr["loc"] and abs(s["L"] * 1e3 - cr.L_mm) < 1e-6)
        path, s_arc, c, L = sl["path"], sl["s"], sl["c"], sl["L"]
        rc, _ = insert(t, path, s_arc, c, L, cr.ds_pct / 100)
        f, Q, info, _, _ = t.evaluate(C, rc); q = Q.copy(); q[0] = info["inflow"]
        S = subtree_w(t); G = (S / t.r_ref ** 3) / (S[0] / t.r_ref[0] ** 3)
        pi = (f * P_AORTA - P_VEN) / (P_AORTA - P_VEN)
        sel = path[t.resolved[path]]
        lnq = np.log(q[sel] / (K_MURRAY * t.r_ref[sel] ** 3)); rem = lnq - np.log(G[sel]) - np.log(pi[sel])
        rows.append(dict(scan=r.scan, side=r.side, bed=bed, case="clean_lesion", sd_lnq=lnq.std(), range_lnq=np.ptp(lnq),
                         sd_remainder=rem.std(), range_remainder=np.ptp(rem), mean_remainder=rem.mean(),
                         sd_lnG=np.log(G[sel]).std(), sd_lnpi=np.log(pi[sel]).std()))
        # corrupted T1 under Protocol C
        q0_all = bed_flow(t, C, f)
        segs2, info1 = ERROR_TYPES["T1_missed_branch"](list(t.segments), t, path, s_arc, c, L)
        t2 = Tree(segs2, "x", bed=bed); m = node_map(t, t2); p2, _ = t2.vessel_path(HOSTS[r.side][cr.vessel])
        s2 = t2.arc[p2] - t2.arc[p2[0]]; r2, _ = insert(t2, p2, s2, c, L, cr.ds_pct / 100)
        pairs = [(sub, float(q0_all[m[sub][m[sub] >= 0]].sum())) for sub in territories(t2) if (m[sub] >= 0).any()]
        if len(pairs) < 2: continue
        qt = np.array([x for _, x in pairs]); t2._C.clear(); Cs = t2.calibrate(t2.demand())
        def loss(lc):
            ff, _, _, _, _ = t2.evaluate(10 ** lc, r2); qq = bed_flow(t2, 10 ** lc, ff)
            return float(np.mean(((np.array([qq[s].sum() for s, _ in pairs]) - qt) / qt) ** 2))
        C2 = 10 ** minimize_scalar(loss, bounds=(np.log10(Cs) - 1.5, np.log10(Cs) + 1.5), method="bounded", options=dict(xatol=1e-7)).x
        f2, Q2, i2, _, _ = t2.evaluate(C2, r2); q2 = Q2.copy(); q2[0] = i2["inflow"]
        S2 = subtree_w(t2); G2 = (S2 / t2.r_ref ** 3) / (S2[0] / t2.r_ref[0] ** 3); pi2 = (f2 * P_AORTA - P_VEN) / (P_AORTA - P_VEN)
        sel2 = p2[t2.resolved[p2]]
        lnq2 = np.log(q2[sel2] / (K_MURRAY * t2.r_ref[sel2] ** 3)); rem2 = lnq2 - np.log(G2[sel2]) - np.log(pi2[sel2])
        # the K r0^3 normalisation: inflow/(K r0^3) = 1 in the clean tree by calibration; under C it is not
        rows.append(dict(scan=r.scan, side=r.side, bed=bed, case="T1_C", sd_lnq=lnq2.std(), range_lnq=np.ptp(lnq2),
                         sd_remainder=rem2.std(), range_remainder=np.ptp(rem2), mean_remainder=rem2.mean(),
                         sd_lnG=np.log(G2[sel2]).std(), sd_lnpi=np.log(pi2[sel2]).std(),
                         ln_inflow_over_Kr0=float(np.log(i2["inflow"] / (K_MURRAY * t2.r_ref[0] ** 3))), lnC_ratio=np.log(C2 / C)))
        # anatomy-only orphan weight at the deleted junction, clean vs corrupted:  (r_J^3 - sum_children r^3)/r_J^3
        sb = info1["branch_arc_mm"] * 1e-3; kJ = int(np.argmin(np.abs(s_arc - sb))); J = path[kJ]; J2 = p2[int(np.argmin(np.abs(s2 - sb)))]
        orph = lambda tt, v: (tt.r_ref[v] ** 3 - sum(tt.r_ref[cc] ** 3 for cc in tt.children[v])) / tt.r_ref[v] ** 3
        # distribution of the same statistic at every other resolved host-path node in the CLEAN tree (the null)
        null = np.array([orph(t, v) for v in path if t.resolved[v] and v != J and t.children[v]])
        rows.append(dict(scan=r.scan, side=r.side, bed=bed, case="orphan_stat", orphan_clean_J=orph(t, J), orphan_corrupt_J=orph(t2, J2),
                         null_p95=float(np.quantile(null, .95)), null_max=float(null.max()), n_null=len(null),
                         branch_r_mm=info1["branch_r_mm"], rJ_mm=t.r_ref[J] * 1e3))
df = pd.DataFrame(rows); df.to_csv(Path(__file__).parent / "s1_decomp.csv", index=False)
pd.set_option("display.width", 250)
print(df[df.case != "orphan_stat"].round(3).to_string()); print(); print(df[df.case == "orphan_stat"].round(3).to_string())
