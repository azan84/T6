"""Build the hyperaemic pair: solve_baseline_ref_hyp (healthy, mesh_base_ref) and solve_lesion80_hyp (lesion80, mesh_case2).
Same meshes, numerics, BC formulation and 0D twin as the audited resting pair; ONLY the bed constant C changes, because the demand
is raised from the study's Murray demand on the 0D EDT inlet radius (0.6636 mL/s) to the same Murray law (k = 562 1/s) on the 3D
area-equivalent radius of the inlet patch (r = sqrt(A_inlet/pi)). See hyperaemia_design.md. Refuses to overwrite a case holding run output.
usage: build_hyp_cases.py            (no arguments; both cases are always built together so that R_out/relax are provably identical)"""
import sys, os, re, shutil, json
import re as _re
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from zerod_ffr import RHO, MU, P_AORTA, P_VEN, K_MURRAY
from outlets_837 import build_tree, node_xyz_and_tangent
import build_solve_cases as B
import build_lesion80_case as L
from hyp_probe import inlet_area_mm2

BASE = B.BASE
REF_MESH, LES_MESH = "lesion80/mesh_base_ref", "lesion80/mesh_case2"
REF_NAME, LES_NAME = "baseline_ref_hyp", "lesion80_hyp"
_PAT = _re.compile(r"// No residualControl in fvSolution \(see there for why\).*?laminar assumption\)\.\n", _re.S)
_NEW = ('// No residualControl in fvSolution: fixed iteration count, judged from the monitors. Hyperaemic demand: throat Re of the lesion case is estimated 300-600 (computed from the solved section flux\n'
        '// after the run); the steady solver may stall on the post-stenotic jet - if so report the last-500-iteration band and label the case UNCONVERGED, never a converged value.\n')

def guard(name):
    dst = f"{BASE}/solve_{name}"
    if os.path.exists(dst):
        done = [d for d in os.listdir(dst) if (d.isdigit() and int(d) > 0) or d.startswith("processor") or d in ("log.simpleFoam", "log.smoke")]
        if done:
            raise SystemExit(f"refusing to overwrite {dst}: it holds run output {done[:4]}")

def finish_controls(dst, functions_extra=True):
    cd = open(f"{dst}/system/controlDict").read()
    if functions_extra and "wallShearStress" not in cd:
        cd = cd.rstrip()[:-1] + ("    wallShearStress\n    {\n        type wallShearStress;\n        libs (\"libfieldFunctionObjects.so\");\n"
                                 "        writeControl writeTime; patches (wall);\n    }\n}\n")
    new = _PAT.sub(_NEW, cd)
    assert new != cd, "residualControl comment block not found: controlDict comment not updated"
    open(f"{dst}/system/controlDict", "w").write(new)
    c = open(f"{dst}/system/controlDict").read()
    assert re.search(r"stopAt\s+endTime;", c) and re.search(r"startFrom\s+startTime;", c) and re.search(r"endTime\s+3000;", c) and "wallShearStress" in c, "run controls not as required"

def main():
    guard(REF_NAME); guard(LES_NAME)
    a_ref = inlet_area_mm2(f"{BASE}/solve_baseline_ref")["inlet"]; a_les = inlet_area_mm2(f"{BASE}/solve_lesion80")["inlet"]
    assert abs(a_ref / a_les - 1) < 5e-4, f"inlet areas differ: {a_ref} vs {a_les}"
    r_in = np.sqrt(a_ref * 1e-6 / np.pi)
    T = build_tree()
    Q_rest = T.demand("murray"); Q_hyp = K_MURRAY * r_in ** 3
    alpha = Q_hyp / Q_rest
    assert 3.0 < alpha < 3.3, f"alpha {alpha} outside the pre-registered 3.0-3.3 window"
    C = T.calibrate(Q_hyp)
    print(f"A_inlet(ref mesh) {a_ref:.4f} mm2 (lesion mesh {a_les:.4f}); r_in,3D {r_in*1e3:.4f} mm; Q_rest {Q_rest*1e6:.4f} mL/s -> Q_hyp {Q_hyp*1e6:.4f} mL/s (alpha {alpha:.4f}); C {C:.5e}")
    # ---------------- healthy reference (audited builder, only the demand differs)
    dst_r = B.build_case(REF_NAME, f"{BASE}/{REF_MESH}", T, Q_hyp)
    shutil.rmtree(f"{dst_r}/constant/polyMesh/sets", ignore_errors=True)
    finish_controls(dst_r)
    zr = json.load(open(f"{dst_r}/zerod_reference.json")); zr.update(dict(demand_rule="Q = K_MURRAY * r_in3D^3", K_MURRAY=K_MURRAY, A_inlet_mm2=a_ref, r_in3D_mm=r_in * 1e3,
                                                                       Q_rest_mls=Q_rest * 1e6, alpha=alpha))
    healthy_ffr_hyp = float(T.ffr(mode="murray", scale=alpha)["min_ffr_main"])   # build_case writes the RESTING-demand value (T.ffr(mode="murray")); the hyperaemic demand is Q_rest * alpha
    zr["healthy_main_ffr"] = healthy_ffr_hyp
    json.dump(zr, open(f"{dst_r}/zerod_reference.json", "w"), indent=1)
    # ---------------- lesion case (same procedure as build_lesion80_case.main, demand replaced, reference R_out from the hyp reference)
    Qd = Q_hyp
    ffr_h, Qn_h, info_h, sten_h, K_h = T.evaluate(C)
    r_ov, idx = L.lesion_r_override(T)
    ffr_l, Qn_l, info_l, sten_l, K_l = T.evaluate(C, r_override=r_ov)
    r_ov_a, idx_a = L.lesion_r_override(T, "area")
    ffr_a, Qn_a, info_a, sten_a, K_a = T.evaluate(C, r_override=r_ov_a)
    assert info_h["converged"] and info_l["converged"] and info_a["converged"], "0D solve did not converge"
    ref_h = json.load(open(f"{dst_r}/zerod_reference.json"))
    dst = f"{BASE}/solve_{LES_NAME}"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for sub in ("constant", "system"):
        shutil.copytree(f"{BASE}/{LES_MESH}/{sub}", f"{dst}/{sub}")
    shutil.rmtree(f"{dst}/constant/polyMesh/sets", ignore_errors=True)
    for f in ("log.checkMesh", "log.cartesianMesh"):
        shutil.copy(f"{BASE}/{LES_MESH}/{f}", dst)
    cent = B.patch_centroids(dst)
    rows = {}
    for v in T.leaves:
        lab = T.label[v]; patch = f"outlet_{lab}"
        p_xyz, tan = node_xyz_and_tangent(T, v)
        dist = float(np.linalg.norm(p_xyz + B.EXT_MM * tan - cent[patch]))
        assert dist < B.TOL_MM, (patch, dist)
        R_out = C / T.w[v]
        assert abs(R_out / ref_h["outlets"][patch]["R_out"] - 1) < 1e-9, f"{patch}: R_out differs from {REF_NAME}"
        R_own, L_own = B.terminal_R_own(T, v)
        G = R_out / R_own; relax = min(0.5, 1.0 / (1.0 + G))
        assert abs(relax / ref_h["outlets"][patch]["relax"] - 1) < 1e-9, f"{patch}: relax differs from {REF_NAME}"
        Q0h, Q0l, Q0a = float(Qn_h[v]), float(Qn_l[v]), float(Qn_a[v])
        rows[patch] = dict(leaf=int(v), label=lab, r_ref_mm=float(T.r_ref[v] * 1e3), R_out=float(R_out), R_own=float(R_own),
                           G=float(G), relax=float(relax), Q0_healthy_mls=Q0h * 1e6, Q0_mls=Q0l * 1e6, Q0_areaVariant_mls=Q0a * 1e6,
                           p_init_kin=float((P_VEN + R_out * Q0l) / RHO), match_mm=dist)
    assert set(rows) == set(ref_h["outlets"]), "outlet sets differ between the pair"
    outlets_U = "".join(f"    {p} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}\n" for p in rows)
    outlets_P = "".join(B.P_OUT.format(patch=p, cname=p.split('_')[1], p_init=d["p_init_kin"], R=d["R_out"], Pv=P_VEN,
                                       rho=RHO, relax=d["relax"]) for p, d in rows.items())
    os.makedirs(f"{dst}/0")
    open(f"{dst}/0/U", "w").write(B.U_T.format(outlets=outlets_U))
    open(f"{dst}/0/p", "w").write(B.P_T.format(p0=B.P0_KIN, outlets=outlets_P))
    cd = open(f"{dst}/system/controlDict").read()
    head = re.sub(r"writeInterval\s+100;", "writeInterval   250;", cd[:cd.index("functions")])
    open(f"{dst}/system/controlDict", "w").write(head + B.functions_block(list(rows)))
    finish_controls(dst)
    open(f"{dst}/system/decomposeParDict", "w").write(
        f"FoamFile {{ version 2.0; format ascii; class dictionary; object decomposeParDict; }}\nnumberOfSubdomains {L.NPROC};\nmethod scotch;\n")
    win = np.array(idx); sten_w = 100 * sten_l[win]
    json.dump(dict(case=LES_NAME, mesh_dir=LES_MESH, Q_demand_mls=Qd * 1e6, C=float(C), inflow_healthy_mls=info_h["inflow"] * 1e6,
                   inflow_mls=info_l["inflow"] * 1e6, healthy_main_ffr=healthy_ffr_hyp,
                   demand_rule="Q = K_MURRAY * r_in3D^3", K_MURRAY=K_MURRAY, A_inlet_mm2=a_ref, r_in3D_mm=r_in * 1e3, Q_rest_mls=Q_rest * 1e6, alpha=alpha,
                   lesion_nodes=idx, lesion_0D_max_DS_pct=float(sten_w.max()), lesion_0D_r_throat_mm=float(r_ov[win].min() * 1e3),
                   lesion_0D_r_pre_mm=float(T.r[win[np.argmin(r_ov[win])]] * 1e3), inflow_areaVariant_mls=info_a['inflow'] * 1e6,
                   lesion_0D_areaVariant_max_DS_pct=float(100 * sten_a[np.array(idx_a)].max()), lesion_0D_areaVariant_r_throat_mm=float(r_ov_a[np.array(idx_a)].min() * 1e3),
                   K_nodes=[int(k) for k in np.where(K_l > 0)[0]], K_values=[float(K_l[k]) for k in np.where(K_l > 0)[0]],
                   zerod_converged=bool(info_l['converged']), zerod_mass_err=float(info_l['mass_err']), outlets=rows,
                   patch_centroids_mm={k: v.tolist() for k, v in cent.items()}),
              open(f"{dst}/zerod_reference.json", "w"), indent=1)
    print(f"0D healthy inflow {info_h['inflow']*1e6:.4f} mL/s -> lesion (EDT) {info_l['inflow']*1e6:.4f} mL/s ({100*(info_l['inflow']/info_h['inflow']-1):+.1f}%), "
          f"area variant {info_a['inflow']*1e6:.4f} ({100*(info_a['inflow']/info_h['inflow']-1):+.1f}%)")
    print("outlet         R_out       relax    Q healthy -> Q lesion (0D edt) | area-variant")
    for p, d in rows.items():
        print(f"  {p:11s} {d['R_out']:.4e} {d['relax']:.5f}  {d['Q0_healthy_mls']:.5f} -> {d['Q0_mls']:.5f} ({100*(d['Q0_mls']/d['Q0_healthy_mls']-1):+.1f}%) | {d['Q0_areaVariant_mls']:.5f} ({100*(d['Q0_areaVariant_mls']/d['Q0_healthy_mls']-1):+.1f}%)")
    h_r = json.load(open(f"{dst_r}/zerod_reference.json"))["healthy_main_ffr"]; h_l = json.load(open(f"{dst}/zerod_reference.json"))["healthy_main_ffr"]
    assert h_r == h_l == healthy_ffr_hyp, f"healthy_main_ffr differs between the pair: {h_r} vs {h_l}"
    print(f"healthy_main_ffr (hyperaemic demand) {h_r:.8f} in both zerod_reference.json")
    print(f"built {dst_r} and {dst}")

if __name__ == "__main__":
    main()
