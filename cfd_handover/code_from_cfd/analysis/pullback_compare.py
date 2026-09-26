"""Item 4 pullback comparison: per-node 0D pressure vs AREA-AVERAGED 3D cross-section pressure along each
root->outlet centreline path, both normalised by the prescribed P_aorta (design.md Item 4 step 6 / spec 6.2).
0D-3D difference is LOGGED as data, not judged (no stated tolerance for this item).

usage: pullback_compare.py <solve_case_dir> <baseline|missedbranch> [time]
"""
import sys, os, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pyvista as pv
from zerod_ffr import RHO, P_AORTA
from outlets_837 import build_tree
from build_solve_cases import drop_branch

STEP_MM = 1.5

def node_xyz(T, v):
    sid = T.seg[v]
    seg = [s for s in T.segments if s.sid == sid][0]
    seg_nodes = np.where(T.seg == sid)[0]
    li = int(np.where(seg_nodes == v)[0][0])
    # root segment: node 0 IS pts[0]; every other segment skips its first point (shared with the parent end node)
    return seg.pts[li if seg.parent is None else li + 1] * 1e3

def path_to(T, v):
    p = [v]
    while T.parent[p[-1]] >= 0 and p[-1] != 0:
        p.append(int(T.parent[p[-1]]))
    return p[::-1]

def section_pressure(mesh, origin_m, normal):
    sl = mesh.slice(normal=normal, origin=origin_m)
    if sl.n_cells == 0:
        return np.nan, 0.0
    part = sl.connectivity(extraction_mode="closest", closest_point=origin_m)
    part = part.compute_cell_sizes(length=False, area=True, volume=False)
    a = part.cell_data["Area"]
    p = part.cell_data["p"]
    return float(np.sum(a * p) / np.sum(a)), float(np.sum(a))

def main(case_dir, which, time=None):
    T = build_tree()
    Qd = T.demand("murray")
    if which == "missedbranch":
        T, _ = drop_branch(T, "D2")
    C = T.calibrate(Qd)
    ffr0, Qn, info, _, _ = T.evaluate(C)            # ffr0[node] = P/P_aorta (0D)
    open(f"{case_dir}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{case_dir}/case.foam")
    rd.set_active_time_value(float(time) if time else rd.time_values[-1])
    rd.disable_all_patch_arrays(); rd.enable_patch_array("internalMesh")
    mb = rd.read()
    mesh = mb["internalMesh"] if "internalMesh" in mb.keys() else mb[0]
    print(f"3D time = {rd.active_time_value}, cells = {mesh.n_cells}")
    rows = []
    fig_data = {}
    for leaf in T.leaves:
        lab = str(T.label[leaf])
        nodes = path_to(T, int(leaf))
        xyz = np.array([node_xyz(T, n) for n in nodes])
        arc = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(xyz, axis=0), axis=1))])
        st = np.arange(0, arc[-1], STEP_MM); st = np.append(st, arc[-1])
        curve = []
        for s in st:
            i = min(int(np.searchsorted(arc, s)), len(arc) - 1)
            j = max(i - 1, 0)
            t = 0 if arc[i] == arc[j] else (s - arc[j]) / (arc[i] - arc[j])
            pt = xyz[j] + t * (xyz[i] - xyz[j])
            lo, hi = max(0, i - 3), min(len(xyz) - 1, i + 3)
            tan = xyz[hi] - xyz[lo]; tan = tan / np.linalg.norm(tan)
            p_kin, area = section_pressure(mesh, pt * 1e-3, tan)
            n_near = nodes[i]
            p3 = p_kin * RHO / P_AORTA
            p0 = float(ffr0[n_near])
            curve.append((float(s), p0, p3, area * 1e6))
            rows.append(dict(path=lab, arc_mm=float(s), P0D_over_Pa=p0, P3D_over_Pa=p3, section_area_mm2=area * 1e6))
        fig_data[lab] = np.array(curve)
        c = fig_data[lab]
        print(f"  {lab:4s} outlet station: 0D={c[-1,1]:.4f} 3D={c[-1,2]:.4f}  diff(3D-0D)={c[-1,2]-c[-1,1]:+.4f}   "
              f"max|diff| along path={np.nanmax(np.abs(c[:,2]-c[:,1])):.4f}")
    import csv
    out = f"{case_dir}/pullback_{which}.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 5))
    for k, (lab, c) in enumerate(fig_data.items()):
        col = f"C{k}"
        ax.plot(c[:, 0], c[:, 1], "-", color=col, label=f"{lab} 0D")
        ax.plot(c[:, 0], c[:, 2], "--", color=col, label=f"{lab} 3D")
    ax.set_xlabel("arclength along centreline path from ostium (mm)"); ax.set_ylabel("P / P_aorta")
    ax.set_title(f"Item 4 pullback, {which}: 0D (solid) vs 3D area-averaged section (dashed)")
    ax.legend(ncol=2, fontsize=8); fig.tight_layout(); fig.savefig(f"{case_dir}/pullback_{which}.pdf")
    print("wrote", out)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
