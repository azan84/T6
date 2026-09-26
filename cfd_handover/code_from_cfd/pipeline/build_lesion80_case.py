"""Build solve_lesion80: lesion80 mesh + multi-outlet resistance BCs from the HEALTHY 0D tree (frozen physiology; identical
R_out/relax to solve_baseline) + 0D lesion prediction via Tree.evaluate(C, r_override). See lesion80_design.md.
"""
import sys, os, re, shutil, json
import re as _re
_PAT = _re.compile(r"// No residualControl in fvSolution \(see there for why\).*?laminar assumption\)\.\n", _re.S)
_NEW = '// No residualControl in fvSolution: fixed iteration count, judged from the monitors. Throat Re of the lesion80 case is estimated 110-210 (computed from the solved section flux\n// after the run); a slow limit cycle is possible - if so report the last-500-iteration band and label the case UNCONVERGED, never a converged value.\n'
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from zerod_ffr import RHO, MU, P_AORTA, P_VEN
from outlets_837 import build_tree, node_xyz_and_tangent
import build_solve_cases as B
from build_lesion80_surface import build_frames, f_of_s, S_C, LEN, LAD_SID, PR

BASE = B.BASE
NPROC = int(os.environ.get("NPROC", "16"))

def node_stations(fr):
    """Arc (on the SAME smoothed curve the 3D deformation uses) of each 0D path node, by position (nearest curve sample).
    The polyline arc of the raw centreline nodes differs by up to ~0.7 mm in the window (point jitter inflates it)."""
    from scipy.spatial import cKDTree
    d, j = cKDTree(fr["c"]).query(fr["xyz"])
    return fr["s"][j], d

def lesion_r_override(T, variant="edt"):
    """Radii of the LAD-window nodes scaled by f(s_node); everything else (r_ref, r_fit, leaf weights, C) stays frozen at its
    healthy value inside Tree.evaluate. variant='edt': r_node*f (design; r_node = 0D EDT radius). variant='area': r_eq3D(s)*f,
    with r_eq3D the area-equivalent radius of the BASELINE 3D section at that station (diagnostic: separates the EDT-radius bias)."""
    fr = build_frames(T)
    s_node, _ = node_stations(fr)
    r_ov = T.r.copy()
    idx = []
    if variant == "area":
        ver = json.load(open(f"{BASE}/{PR['DIR']}/geometry_verification.json"))
        st = np.array([r["s"] for r in ver["sections"]]); req = np.array([r["base"]["r_eq"] for r in ver["sections"]]) * 1e-3
    for n, s in zip(fr["nodes"], s_node):
        if T.seg[n] != LAD_SID:
            continue
        f, w = f_of_s(np.array([s]))
        if w[0] > 0:
            r_base = T.r[n] if variant == "edt" else float(np.interp(s, st, req))
            r_ov[n] = r_base * f[0]
            idx.append(int(n))
    return r_ov, idx

def main():
    T = build_tree()
    Qd = T.demand("murray")
    C = T.calibrate(Qd)
    ffr_h, Qn_h, info_h, sten_h, K_h = T.evaluate(C)
    r_ov, idx = lesion_r_override(T)
    ffr_l, Qn_l, info_l, sten_l, K_l = T.evaluate(C, r_override=r_ov)
    r_ov_a, idx_a = lesion_r_override(T, "area")
    ffr_a, Qn_a, info_a, sten_a, K_a = T.evaluate(C, r_override=r_ov_a)
    ref_base = json.load(open(f"{BASE}/solve_baseline/zerod_reference.json"))
    name, mesh = os.environ.get("LESION_CASE_NAME"), os.environ.get("LESION_MESH_DIR")
    if not name or not mesh:
        raise SystemExit("set LESION_CASE_NAME (case dir will be solve_<name>) and LESION_MESH_DIR (relative to the pilot dir) explicitly; there is no default so a finished case can never be rebuilt by accident")
    dst = f"{BASE}/solve_{name}"
    if os.path.exists(dst):
        done = [d for d in os.listdir(dst) if (d.isdigit() and int(d) > 0) or d.startswith("processor") or d in ("log.simpleFoam", "log.smoke")]
        if done:
            raise SystemExit(f"refusing to overwrite {dst}: it holds run output {done[:4]}")
        shutil.rmtree(dst)
    os.makedirs(dst)
    for sub in ("constant", "system"):
        shutil.copytree(f"{BASE}/{mesh}/{sub}", f"{dst}/{sub}")
    shutil.rmtree(f"{dst}/constant/polyMesh/sets", ignore_errors=True)         # checkMesh -writeSets output is not part of the case
    for f in ("log.checkMesh", "log.cartesianMesh"):
        shutil.copy(f"{BASE}/{mesh}/{f}", dst)
    cent = B.patch_centroids(dst)
    rows = {}
    for v in T.leaves:
        lab = T.label[v]; patch = f"outlet_{lab}"
        p_xyz, tan = node_xyz_and_tangent(T, v)
        dist = float(np.linalg.norm(p_xyz + B.EXT_MM * tan - cent[patch]))
        assert dist < B.TOL_MM, (patch, dist)
        R_out = C / T.w[v]
        assert abs(R_out / ref_base["outlets"][patch]["R_out"] - 1) < 1e-9, f"{patch}: R_out differs from solve_baseline"
        R_own, L_own = B.terminal_R_own(T, v)
        G = R_out / R_own; relax = min(0.5, 1.0 / (1.0 + G))
        Q0h, Q0l, Q0a = float(Qn_h[v]), float(Qn_l[v]), float(Qn_a[v])
        rows[patch] = dict(leaf=int(v), label=lab, r_ref_mm=float(T.r_ref[v] * 1e3), R_out=float(R_out), R_own=float(R_own),
                           G=float(G), relax=float(relax), Q0_healthy_mls=Q0h * 1e6, Q0_mls=Q0l * 1e6, Q0_areaVariant_mls=Q0a * 1e6,
                           p_init_kin=float((P_VEN + R_out * Q0l) / RHO), match_mm=dist)
    outlets_U = "".join(f"    {p} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}\n" for p in rows)
    outlets_P = "".join(B.P_OUT.format(patch=p, cname=p.split('_')[1], p_init=d["p_init_kin"], R=d["R_out"], Pv=P_VEN,
                                       rho=RHO, relax=d["relax"]) for p, d in rows.items())
    os.makedirs(f"{dst}/0")
    open(f"{dst}/0/U", "w").write(B.U_T.format(outlets=outlets_U))
    open(f"{dst}/0/p", "w").write(B.P_T.format(p0=B.P0_KIN, outlets=outlets_P))
    cd = open(f"{dst}/system/controlDict").read()
    head = re.sub(r"writeInterval\s+100;", "writeInterval   250;", cd[:cd.index("functions")])
    fn = B.functions_block(list(rows))
    # wall shear stress for the reattachment metric (written at the end of the run only)
    fn = fn.rstrip()[:-1] + ("    wallShearStress\n    {\n        type wallShearStress;\n        libs (\"libfieldFunctionObjects.so\");\n"
                             "        writeControl writeTime; patches (wall);\n    }\n}\n")
    open(f"{dst}/system/controlDict", "w").write(_PAT.sub(_NEW, head + fn))
    cdict = open(f"{dst}/system/controlDict").read()
    assert re.search(r"stopAt\s+endTime;", cdict) and re.search(r"startFrom\s+startTime;", cdict) and re.search(r"endTime\s+3000;", cdict), "run controls not reset"
    open(f"{dst}/system/decomposeParDict", "w").write(
        f"FoamFile {{ version 2.0; format ascii; class dictionary; object decomposeParDict; }}\nnumberOfSubdomains {NPROC};\nmethod scotch;\n")
    win = np.array(idx)
    sten_w = 100 * sten_l[win]
    json.dump(dict(case=name, mesh_dir=mesh, Q_demand_mls=Qd * 1e6, C=float(C), inflow_healthy_mls=info_h["inflow"] * 1e6,
                   inflow_mls=info_l["inflow"] * 1e6, healthy_main_ffr=float(T.ffr(mode="murray")["min_ffr_main"]),
                   lesion_nodes=idx, lesion_0D_max_DS_pct=float(sten_w.max()), lesion_0D_r_throat_mm=float(r_ov[win].min() * 1e3),
                   lesion_0D_r_pre_mm=float(T.r[win[np.argmin(r_ov[win])]] * 1e3), inflow_areaVariant_mls=info_a['inflow'] * 1e6,
                   lesion_0D_areaVariant_max_DS_pct=float(100 * sten_a[np.array(idx_a)].max()), lesion_0D_areaVariant_r_throat_mm=float(r_ov_a[np.array(idx_a)].min() * 1e3),
                   K_nodes=[int(k) for k in np.where(K_l > 0)[0]], K_values=[float(K_l[k]) for k in np.where(K_l > 0)[0]],
                   zerod_converged=bool(info_l['converged']), zerod_mass_err=float(info_l['mass_err']), outlets=rows,
                   patch_centroids_mm={k: v.tolist() for k, v in cent.items()}),
              open(f"{dst}/zerod_reference.json", "w"), indent=1)
    print(f"0D healthy inflow {info_h['inflow']*1e6:.4f} mL/s -> with lesion {info_l['inflow']*1e6:.4f} mL/s "
          f"({100*(info_l['inflow']/info_h['inflow']-1):+.1f}%); 0D-detected max DS in window {sten_w.max():.1f}% "
          f"(nominal 80%), 0D throat radius {r_ov[win].min()*1e3:.3f} mm (pre-lesion node r {T.r[win[np.argmin(r_ov[win])]]*1e3:.3f} mm)")
    print(f"area-equivalent 0D variant: max DS {100*sten_a[np.array(idx_a)].max():.1f}%, throat r {r_ov_a[np.array(idx_a)].min()*1e3:.3f} mm, inflow {info_a['inflow']*1e6:.4f} mL/s")
    print("outlet         R_out       relax    Q healthy -> Q lesion (0D edt) | area-variant")
    for p, d in rows.items():
        print(f"  {p:11s} {d['R_out']:.4e} {d['relax']:.5f}  {d['Q0_healthy_mls']:.5f} -> {d['Q0_mls']:.5f} ({100*(d['Q0_mls']/d['Q0_healthy_mls']-1):+.1f}%) | {d['Q0_areaVariant_mls']:.5f} ({100*(d['Q0_areaVariant_mls']/d['Q0_healthy_mls']-1):+.1f}%)")
    return dst

if __name__ == "__main__":
    main()
