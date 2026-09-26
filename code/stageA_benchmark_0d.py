"""
stageA_benchmark_0d.py — 0D-DISCRETE benchmark values for the Stage A test geometries (CFD-ARM-SPEC v0.2 §8).

Same radius law as the STL generator (imported from cfd_handover/stageA/make_stageA_geometry.py), single outlet, NO
distributed leakage (a 3D tube cannot leak), hyperaemic demand fixed at 1.5 mL/s on the healthy vessel. Writes
cfd_handover/stageA/expected_0D.csv with the BC values to impose in 3D and the pressures to compare against.
The 0D-vs-3D gap on these cases is a RESULT about the lumped stenosis model, not a pass/fail.
"""
import sys
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent; HAND = HERE.parent / "cfd_handover" / "stageA"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(HAND))
from zerod_ffr import Tree, Segment, MU, RHO, P_AORTA, P_VEN
from make_stageA_geometry import radius_sten, PROBES_STEN, X_IN, X_OUT

Q_DEMAND = 1.5e-6                          # m^3/s, LAD-like hyperaemic flow; keeps throat Re to a few hundred

def vessel(ds):
    """Three chained segments (inlet extension | tapering vessel | outlet extension) so each gets its own taper fit."""
    segs = []
    for sid, (a, b) in enumerate(((X_IN, 0.0), (0.0, 90.0), (90.0, X_OUT))):
        x = np.arange(a, b + 1e-9, 0.25)
        segs.append(Segment(sid, None if sid == 0 else sid - 1, np.stack([x, 0 * x, 0 * x], 1) * 1e-3,
                            radius_sten(x, ds) * 1e-3, "LAD"))
    return segs

def discrete(tree):
    """Single-outlet bed: all conductance at the leaf, none along the wall."""
    leaf = max(np.where(tree.active)[0], key=lambda v: tree.arc[v])
    tree.w[:] = 0.0; tree.w[leaf] = tree.r_ref[leaf] ** 3; tree._C.clear()
    return leaf

rows = []
for ds in (0, 50, 70, 80):
    t = Tree(vessel(ds), f"sten{ds:02d}"); leaf = discrete(t)
    C = t.calibrate(Q_DEMAND); R_out = C / t.w[leaf]
    ffr, Q, info, sten, K = t.evaluate(C)
    x_node = t.arc * 1e3 + X_IN                                   # node x-coordinate, mm
    row = dict(case=f"sten{ds:02d}", P_in_Pa=P_AORTA, P_v_Pa=P_VEN, R_out_SI=R_out, R_out_kinematic=R_out / RHO,
               Q_mls=info["inflow"] * 1e6, detected_DS_pct=100 * sten.max(), iters=info["iters"], converged=info["converged"])
    for name, xp in PROBES_STEN.items():
        v = int(np.argmin(np.abs(x_node - xp))); row[f"p_{name}_Pa"] = ffr[v] * P_AORTA
    row["FFR_measurement"] = row["p_measurement_Pa"] / P_AORTA
    r_th = radius_sten(31.5, ds) * 1e-3
    row["Re_throat"] = 2 * RHO * info["inflow"] / (np.pi * MU * r_th)
    rows.append(row)

# straight pipe: analytic Poiseuille at the prescribed flow
r, L = 1.5e-3, 30e-3
rows.append(dict(case="pipe", P_in_Pa=P_AORTA, P_v_Pa=P_VEN, Q_mls=Q_DEMAND * 1e6,
                 dP_60_to_90mm_Pa=8 * MU * L * Q_DEMAND / (np.pi * r ** 4),
                 Re_throat=2 * RHO * Q_DEMAND / (np.pi * MU * r)))
df = pd.DataFrame(rows); df.to_csv(HAND / "expected_0D.csv", index=False)
pd.set_option("display.width", 220); print(df.round(4).to_string(index=False)); print("\nwrote", HAND / "expected_0D.csv")
