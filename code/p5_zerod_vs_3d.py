"""P5 pilot: 3D (resistance, bc_A) vs 0D on requested / as-meshed area / inscribed radius, at the 3D measurement node."""
import sys, json
from pathlib import Path
import numpy as np, pandas as pd, pyvista as pv
P6 = Path(sys.argv[1]); ROOT = Path(sys.argv[2]); OUT = Path(sys.argv[3])
sys.path.insert(0, str(P6 / "code"))
from ingest_cfd_radius import rebuild
from zerod_ffr import P_AORTA, P_VEN
PK = P6 / "cfd_handover/packages/P5"; RET = P6 / "cfd_handover/returns/2026-10-03/P5"
ZD = {138: .802, 69: .810, 473: .850, 272: .811, 139: .773}
rows = []
for pkg in sorted(PK.iterdir()):
    s = int(pkg.name.split("_")[0]); r = RET / str(s)
    pr = pd.read_csv(r / f"M1_probes_{s}_resistance.csv")
    m = (pr[pr.kind == "measurement_relocated"] if (pr.kind == "measurement_relocated").any() else pr[pr.kind == "measurement"]).iloc[0]; meas = int(m.tree_node)
    ol = pd.read_csv(pkg / "outlets.csv"); bcA = pd.read_csv(pkg / "bc_A.csv")
    node_of = dict(zip(ol.outlet_id, ol.tree_node))
    R_by = {int(node_of[o]): R for o, R, md in zip(bcA.outlet_id, bcA.R_SI, bcA["mode"]) if md == "resistance"}
    vtp = pv.read(pkg / "centreline.vtp")
    req = pd.DataFrame(dict(tree_node=np.asarray(vtp.point_data["tree_node"]).astype(int),
                            r_asmeshed_mm=np.asarray(vtp.point_data["r_target_mm"])))
    tmp = OUT / f"_req_{s}.csv"; req.to_csv(tmp, index=False)
    row = dict(scan=s, meas_node=meas, probe=m.probe_id, ffr3d=float(m.p_over_Paorta), ffr0d_cohort=ZD[s])
    for vn, csv in {"req": tmp, "area": r / f"as_meshed_radius_{s}.csv", "insc": r / f"as_meshed_radius_{s}_inscribed.csv"}.items():
        try:
            tw, *_ = rebuild(ROOT, pkg, csv)
            w = np.zeros_like(tw.w)
            for v, R in R_by.items(): w[v] = 1.0 / R
            tw.w = w
            P, Q, _ = tw._solve(1.0, P_AORTA, P_VEN, healthy=False)
            row[f"ffr0d_{vn}"] = P[meas] / P_AORTA
        except Exception as e:
            row[f"ffr0d_{vn}"] = np.nan; print(s, vn, "ERR", repr(e)[:200])
    rows.append(row)
df = pd.DataFrame(rows)
df["d_def"] = df.ffr3d - df.ffr0d_req; df["d_phys_area"] = df.ffr3d - df.ffr0d_area; df["d_phys_insc"] = df.ffr3d - df.ffr0d_insc
df.to_csv(OUT / "p5_0d_vs_3d.csv", index=False)
pd.set_option("display.width", 250); print(df.round(4).to_string(index=False))
