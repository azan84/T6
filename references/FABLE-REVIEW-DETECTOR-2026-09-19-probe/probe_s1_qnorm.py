"""Probe 1 (DETECTOR-SPEC review): is S1 = q_norm(v) = Q(v)/(K r_ref^3) ~1 in clean trees, and does it step distal
to a deleted branch under Protocol C?  Mirrors ablation.run_instance's Protocol C block exactly; nothing is written
into results/ or protocol/.  Usage: probe_s1_qnorm.py <data_root> [n_instances]"""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd
HERE = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(HERE / "code"))
import zerod_ffr
from zerod_ffr import Tree, K_MURRAY, P_AORTA, P_VEN
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES
from ablation import node_map, bed_flow, territories
from scipy.optimize import minimize_scalar

root = Path(sys.argv[1]); N = int(sys.argv[2]) if len(sys.argv) > 2 else 8
coh = pd.read_csv(HERE / "protocol" / "COHORT-FROZEN-2026-09-18.csv")
el = pd.read_csv(HERE / "results" / "discrete_arm_eligibility.csv")
# instances where T1 exists in the discrete bed AND the discrete arm is eligible, one per tree, spread over vessels
ok = el[el.eligible & el.deletable_branch].drop_duplicates(["scan", "side"])
pick = pd.concat([ok[ok.vessel == v].head(int(np.ceil(N / 3))) for v in ("LAD", "LCX", "RCA")]).head(N)
rows = pick.merge(coh, on=["scan", "side", "vessel", "loc", "L_mm", "ds_pct"])

def qnorm(t, Q, inflow):
    q = Q.copy(); q[0] = inflow                      # Qf[0] is 0 (root eliminated); the root carries the inflow
    return q / (K_MURRAY * t.r_ref ** 3)

def protocol_c(t2, r2, t_pairs, C_start):
    q_target = np.array([q for _, q in t_pairs])
    def loss(lc):
        f, _, _, _, _ = t2.evaluate(10 ** lc, r2); q = bed_flow(t2, 10 ** lc, f)
        return float(np.mean(((np.array([q[s].sum() for s, _ in t_pairs]) - q_target) / q_target) ** 2))
    res = minimize_scalar(loss, bounds=(np.log10(C_start) - 1.5, np.log10(C_start) + 1.5), method="bounded",
                          options=dict(xatol=1e-7))
    C2 = 10 ** res.x; f, Q, info, _, _ = t2.evaluate(C2, r2); qb = bed_flow(t2, C2, f)
    pred = np.array([qb[s].sum() for s, _ in t_pairs]); rho = (pred - q_target) / q_target
    return C2, f, Q, info, rho

def s1_stats(t, path, s_arc, c, L, lnq):
    """S1 as in DETECTOR-SPEC §3: resolved host-path nodes from the lesion's proximal shoulder to the last resolved."""
    k0 = int(np.searchsorted(s_arc, c - L / 2)); sel = [k for k in range(k0, len(path)) if t.resolved[path[k]]]
    v = lnq[path[sel]]; steps = np.abs(np.diff(v))
    # 5 mm grid version of the step (spec §7.2 stations): sample nearest node every 5 mm
    grid = np.arange(s_arc[sel[0]], s_arc[sel[-1]] + 1e-9, 5e-3)
    gk = [sel[int(np.argmin(np.abs(s_arc[sel] - g)))] for g in grid]
    vg = lnq[path[sorted(set(gk))]]
    return dict(S1_max=float(np.abs(v).max()), S1_step_node=float(steps.max()) if len(steps) else np.nan,
                S1_step_5mm=float(np.abs(np.diff(vg)).max()) if len(vg) > 1 else np.nan,
                S1_range=float(v.max() - v.min()), lnq_prox=float(v[0]), lnq_last=float(v[-1]))

out, prof = [], []
for _, row in rows.iterrows():
    for bed in ("leaky", "discrete"):
        try:
            t = load(root, int(row.scan), row.side, bed)
        except ValueError as e:
            print("skip", row.scan, row.side, bed, e); continue
        o = t.ffr("murray", 1.0); C_clean = o["C"]
        slots, _ = plan(t, row.side, t.last["ffr"].copy())
        sl = next((s for s in slots if s["vessel"] == row.vessel and s["loc"] == row["loc"]
                   and abs(s["L"] * 1e3 - row.L_mm) < 1e-6), None)
        if sl is None: print("skip slot", row.scan, row.side, bed); continue
        path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
        meas_clean = int(path[mi]); ds = row.ds_pct / 100
        # ---- healthy (no lesion) and clean (lesion) profiles
        Ph, Qh, inh = t._solve(C_clean, P_AORTA, P_VEN, healthy=True)
        lnq_h = np.log(qnorm(t, Qh, inh))
        r_clean, _ = insert(t, path, s_arc, c, L, ds)
        ffr0, Q0, info0, _, _ = t.evaluate(C_clean, r_clean); q0_all = bed_flow(t, C_clean, ffr0)
        lnq_0 = np.log(qnorm(t, Q0, info0["inflow"]))
        base = dict(scan=int(row.scan), side=row.side, vessel=row.vessel, ds_pct=int(row.ds_pct), bed=bed,
                    ffr_clean=float(ffr0[meas_clean]), n_bif_on_path=int(sum(len(t.children[v]) >= 2 for v in path)),
                    n_terr=len(territories(t)), n_outlets=len(t.leaves), path_len_mm=float(s_arc[-1] * 1e3))
        out.append({**base, "case": "healthy_nolesion", **s1_stats(t, path, s_arc, c, L, lnq_h),
                    "lnq_path_sd": float(np.std(lnq_h[path[t.resolved[path]]]))})
        out.append({**base, "case": "clean_lesion", **s1_stats(t, path, s_arc, c, L, lnq_0), "C_ratio": 1.0})
        for k, v in enumerate(path):
            prof.append({**base, "case": "clean_lesion", "k": k, "s_mm": s_arc[k] * 1e3, "node": int(v),
                         "r_ref_mm": t.r_ref[v] * 1e3, "Q_mls": Q0[v] * 1e6 if v else info0["inflow"] * 1e6,
                         "lnq": lnq_0[v], "lnq_healthy": lnq_h[v], "ffr": ffr0[v], "resolved": bool(t.resolved[v]),
                         "bif": len(t.children[v]) >= 2})
        # ---- NEGATIVES: clean anatomy, physiology perturbed in the TRUTH, model at nominal, Protocol C tuned
        terr = territories(t); t_pairs_self = [(sub, 1.0) for sub in terr]
        for tag, kw in (("neg_CO+20%", dict(scale=1.2)), ("neg_CO-20%", dict(scale=0.8)),
                        ("neg_mu+15%", dict(mu=1.15)), ("neg_MAP+10", dict(pin=P_AORTA + 10 * zerod_ffr.MMHG))):
            if len(terr) < 2: continue
            mu0 = zerod_ffr.MU
            if "mu" in kw: zerod_ffr.MU = mu0 * kw["mu"]
            pin = kw.get("pin", P_AORTA)
            t._C.clear(); Ct = t.calibrate(t.demand("murray", kw.get("scale", 1.0)), P_in=pin)
            ft, Qt, it, _, _ = t.evaluate(Ct, r_clean, P_in=pin); qt = bed_flow(t, Ct, ft) if pin == P_AORTA else \
                t.w / Ct * (ft * pin - P_VEN)
            zerod_ffr.MU = mu0
            pairs = [(sub, float(qt[sub].sum())) for sub in terr if qt[sub].sum() > 0]
            t._C.clear(); C2, f2, Q2, i2, rho = protocol_c(t, r_clean, pairs, C_clean)
            lnq = np.log(qnorm(t, Q2, i2["inflow"]))
            out.append({**base, "case": tag, **s1_stats(t, path, s_arc, c, L, lnq), "C_ratio": C2 / C_clean,
                        "resid": float(np.sqrt(np.mean(rho ** 2))), "S3_conc": float(np.abs(rho).max() / np.sqrt(np.mean(rho ** 2))) if np.sqrt(np.mean(rho ** 2)) > 0 else np.nan,
                        "dFFR": float(f2[meas_clean] - ffr0[meas_clean])})
        # ---- POSITIVES: T1 and T4 under Protocol C, exactly as ablation.py
        for etype in ("T1_missed_branch", "T4_taper", "T2_truncation"):
            segs2, info = ERROR_TYPES[etype](list(t.segments), t, path, s_arc, c, L)
            if segs2 is None: out.append({**base, "case": etype, "status": info}); continue
            try: t2 = Tree(segs2, f"{t.name}_{etype}", bed=bed)
            except ValueError as e: out.append({**base, "case": etype, "status": str(e)}); continue
            m = node_map(t, t2); p2, _ = t2.vessel_path(HOSTS[row.side][row.vessel])
            s2 = t2.arc[p2] - t2.arc[p2[0]]
            if c + L / 2 >= s2[-1]: out.append({**base, "case": etype, "status": "lesion outside"}); continue
            r2, _ = insert(t2, p2, s2, c, L, ds)
            cand = np.where(m == meas_clean)[0]
            meas2 = int(cand[0]) if len(cand) else int(p2[min(int(np.searchsorted(s2, c + L / 2 + RUNOFF)), len(p2) - 1)])
            t_pairs = []
            for sub in territories(t2):
                mc = m[sub][m[sub] >= 0]
                if len(mc) and q0_all[mc].sum() > 0: t_pairs.append((sub, float(q0_all[mc].sum())))
            if len(t_pairs) < 2: out.append({**base, "case": etype, "status": "<2 territories"}); continue
            t2._C.clear(); C_start = t2.calibrate(t2.demand("murray", 1.0))
            C2, f2, Q2, i2, rho = protocol_c(t2, r2, t_pairs, C_start)
            lnq = np.log(qnorm(t2, Q2, i2["inflow"]))
            st = s1_stats(t2, p2, s2, c, L, lnq)
            rec = {**base, "case": etype, **st, "C_ratio": C2 / C_clean, "resid": float(np.sqrt(np.mean(rho ** 2))),
                   "S3_conc": float(np.abs(rho).max() / np.sqrt(np.mean(rho ** 2))), "dFFR": float(f2[meas2] - ffr0[meas_clean]),
                   "n_terr_c": len(t_pairs), "status": "ok"}
            if etype == "T1_missed_branch":
                # the jump in ln q_norm across the deleted branch point, corrupted minus clean, at the same nodes
                sb = info["branch_arc_mm"] * 1e-3; kb = int(np.argmin(np.abs(s2 - sb)))
                kk = [k for k in (kb - 1, kb + 1) if 0 <= k < len(p2)]
                vc = [int(m[p2[k]]) for k in kk]
                rec.update(branch_r_mm=info["branch_r_mm"], branch_arc_mm=info["branch_arc_mm"],
                           dlnq_prox_of_branch=float(lnq[p2[kk[0]]] - lnq_0[vc[0]]),
                           dlnq_dist_of_branch=float(lnq[p2[kk[-1]]] - lnq_0[vc[-1]]),
                           step_at_branch_corrupt=float(lnq[p2[kk[-1]]] - lnq[p2[kk[0]]]),
                           step_at_branch_clean=float(lnq_0[vc[-1]] - lnq_0[vc[0]]))
            out.append(rec)
            for k, v in enumerate(p2):
                prof.append({**base, "case": etype, "k": k, "s_mm": s2[k] * 1e3, "node": int(v), "r_ref_mm": t2.r_ref[v] * 1e3,
                             "Q_mls": Q2[v] * 1e6 if v else i2["inflow"] * 1e6, "lnq": lnq[v], "ffr": f2[v],
                             "resolved": bool(t2.resolved[v]), "bif": len(t2.children[v]) >= 2,
                             "lnq_clean_same_node": lnq_0[m[v]] if m[v] >= 0 else np.nan})
        print(f"done {row.scan} {row.side} {row.vessel} {bed}", flush=True)

pd.DataFrame(out).to_csv(Path(__file__).parent / "s1_stats.csv", index=False)
pd.DataFrame(prof).to_csv(Path(__file__).parent / "s1_profiles.csv", index=False)
print("wrote s1_stats.csv / s1_profiles.csv")
