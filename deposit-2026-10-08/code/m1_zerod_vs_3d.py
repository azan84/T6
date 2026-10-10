import sys, json
from pathlib import Path
import numpy as np, pandas as pd
import pyvista as pv

P6 = Path(sys.argv[1]); ROOT = Path(sys.argv[2]); OUT = Path(sys.argv[3])
sys.path.insert(0, str(P6 / "code"))
from ingest_cfd_radius import rebuild
from zerod_ffr import R_FLOOR, P_AORTA, P_VEN

PK = P6 / "cfd_handover/packages/M1"; RET = P6 / "cfd_handover/returns/2026-09-26"
CASES = ["clean_nolesion", "baseline", "T1_missed_branch"]

def solve_resistance(tw, R_by_node):
    w = np.zeros_like(tw.w)
    for v, R in R_by_node.items(): w[v] = 1.0 / R
    assert set(R_by_node) == set(int(x) for x in tw.leaves), "outlet set != twin leaves"
    tw.w = w
    P, Q, inflow = tw._solve(1.0, P_AORTA, P_VEN, healthy=False)
    assert tw.info["converged"], tw.info
    return P, Q

def solve_prescribed(tw, Q_by_node):
    n = len(tw.r); Q = np.zeros(n)
    order = sorted(np.where(tw.active)[0], key=lambda v: -tw.arc[v])
    for v, q in Q_by_node.items(): Q[v] = q
    for v in order:
        if v != 0 and tw.parent[v] >= 0 and tw.children[v]: Q[v] = sum(Q[c] for c in tw.children[v])
    P = np.full(n, np.nan); P[0] = P_AORTA
    for v in sorted(np.where(tw.active)[0], key=lambda v: tw.arc[v]):
        if v == 0: continue
        p = tw.parent[v]
        r_mid = max(0.5 * (tw.r[v] + tw.r[p]), R_FLOOR)
        Rl = 8 * tw.mu * tw.ds[v] / (np.pi * r_mid ** 4)
        P[v] = P[p] - Q[v] * (Rl + tw.K[v] * abs(Q[v]))
    return P, Q

rows, outl = [], []
for c in CASES:
    pkg = PK / f"14_left_LAD_prox_20mm_80ds__{c}__real"
    meta = json.loads((pkg / "meta.json").read_text())
    meas = meta["measurement"]["tree_node"]
    probes = pd.read_csv(pkg / "probes.csv"); throat = int(probes.loc[probes.kind == "throat", "tree_node"].iloc[0])
    bcA = pd.read_csv(pkg / "bc_A.csv"); bcC = pd.read_csv(pkg / "bc_C_flows.csv"); ol = pd.read_csv(pkg / "outlets.csv")
    node_of = dict(zip(ol.outlet_id, ol.tree_node))
    R_by = {int(node_of[o]): R for o, R, m in zip(bcA.outlet_id, bcA.R_SI, bcA["mode"]) if m == "resistance"}
    Q_by = {int(node_of[o]): q for o, q, m in zip(bcC.outlet_id, bcC.Q_target_m3s, bcC["mode"]) if m == "prescribed"}
    vtp = pv.read(pkg / "centreline.vtp")
    req = pd.DataFrame(dict(tree_node=np.asarray(vtp.point_data["tree_node"]).astype(int),
                            r_asmeshed_mm=np.asarray(vtp.point_data["r_target_mm"])))
    tmp = OUT / f"_req_{c}.csv"; req.to_csv(tmp, index=False)
    variants = {"requested": tmp,
                "asmeshed_area": RET / f"as_meshed_radius_{c}.csv",
                "asmeshed_inscribed": RET / f"as_meshed_radius_{c}_inscribed.csv"}

    for mode, f3 in (("resistance", "resistance"), ("prescribed", "prescribed")):
        pr = pd.read_csv(RET / f"M1_probes_{c}_{f3}.csv"); o3 = pd.read_csv(RET / f"M1_outlets_{c}_{f3}.csv")
        rows.append(dict(case=c, mode=mode, model="3D",
                         ffr_meas=float(pr.loc[pr.kind == "measurement", "p_over_Paorta"].iloc[0]),
                         ffr_throat=float(pr.loc[pr.kind == "throat", "p_over_Paorta"].iloc[0]),
                         Q_meas_mls=float(pr.loc[pr.kind == "measurement", "Q_through_mls"].iloc[0]),
                         Q_in_mls=float(o3.Q_mls.sum())))
        for r in o3.itertuples(): outl.append(dict(case=c, mode=mode, model="3D", outlet=r.outlet_id, Q_mls=r.Q_mls,
                                                   p_over_Pa=r.p_bar_over_Paorta))
    for vname, csv in variants.items():
        tw, base, t, sl, diag = rebuild(ROOT, pkg, csv)
        for mode in ("resistance", "prescribed"):
            P, Q = solve_resistance(tw, R_by) if mode == "resistance" else solve_prescribed(tw, Q_by)
            leaves = [int(x) for x in tw.leaves]
            rows.append(dict(case=c, mode=mode, model=f"0D_{vname}", ffr_meas=P[meas] / P_AORTA,
                             ffr_throat=P[throat] / P_AORTA, Q_meas_mls=Q[meas] * 1e6,
                             Q_in_mls=sum(Q[v] for v in leaves) * 1e6, coverage=diag["coverage"],
                             throat_r_mm=tw.r[throat] * 1e3, throat_DS=float(tw.stenosis[throat])))
            inv = {v: o for o, v in node_of.items()}
            for v in leaves: outl.append(dict(case=c, mode=mode, model=f"0D_{vname}", outlet=inv[v], Q_mls=Q[v] * 1e6,
                                             p_over_Pa=P[v] / P_AORTA))

        P1, Q1 = solve_resistance(tw, R_by)
        P2, _ = solve_prescribed(tw, {v: Q1[v] for v in (int(x) for x in tw.leaves)})
        act = tw.active
        err = np.nanmax(np.abs(P1[act] - P2[act])) / P_AORTA
        print(f"{c:18s} {vname:20s} cross-check max |dP|/Pa = {err:.2e}")
        assert err < 1e-6
df = pd.DataFrame(rows); df.to_csv(OUT / "m1_0d_vs_3d.csv", index=False)
pd.DataFrame(outl).to_csv(OUT / "m1_0d_vs_3d_outlets.csv", index=False)
pd.set_option("display.width", 200); pd.set_option("display.precision", 4)
print(df.drop(columns=["coverage"]).to_string(index=False))

piv = df.pivot_table(index=["mode", "model"], columns="case", values="ffr_meas")
piv["dFFR_T1_minus_base"] = piv["T1_missed_branch"] - piv["baseline"]
print("\n", piv.to_string())
