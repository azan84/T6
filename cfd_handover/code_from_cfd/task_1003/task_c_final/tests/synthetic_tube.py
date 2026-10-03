"""Synthetic Gate-M1-format package + blockMesh mesh for the end-to-end test of post_case_generic.sh (tests/test_post_case_generic.sh): a straight tube along x (L = 20 mm, R = 1 mm) with a smooth stenosis
(radius x (1 - 0.4 exp(-((x - 6)/1.5)^2)), throat 0.6 mm at x = 6 mm), one outlet. Package files in the M1 format (centreline.vtp with the package point arrays, probes.csv with inlet/throat/measurement/outlet
probes, outlets.csv, bc_A.csv, bc_C_flows.csv, inlet.json, meta.json, territories.csv), mesh = O-grid blockMesh (about 42k hexahedra) with patches inlet, out_40, wall, stenosis applied by moving the points.
Frame: package mm, mesh m (as the real packages). nx = 97 axial cells (0.206 mm): no probe plane coincides with a layer of mesh faces (with nx = 100 the planes at whole mm did, and the OpenFOAM
sampledPlane monitors then reported an area 8 % too large: 3.388 vs 3.129 mm2, recorded in FIX30_REPORT attempt 2).
--tilt-measurement DEG: the measurement probe normal is tilted by DEG in the x-y plane (30 -> fails the strict section rule S1, so the builder must relocate it and keep the original monitor).
usage: synthetic_tube.py <root> [--tilt-measurement DEG]   (writes <root>/pkg/SYN_tube_test__baseline__real and <root>/mesh)"""
import os, sys, json, csv, subprocess
import numpy as np, pyvista as pv

L, R, XT, DEPTH, WID = 20.0, 1.0, 6.0, 0.4, 1.5
NAME = "SYN_tube_test__baseline__real"
P_AORTA, PV, RHO, MU = 11998.98, 666.61, 1060.0, 0.004
R_OUT = 2.0e10
TEMPLATE = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/stageA/caseTemplate_real_lumen_steady"      # read-only (fvSchemes/fvSolution for checkMesh)
FOAM = "source /usr/lib/openfoam/openfoam2406/etc/bashrc >/dev/null 2>&1; "

def rad(x): return R * (1 - DEPTH * np.exp(-((x - XT) / WID) ** 2))

def package(d, tilt=0.0):
    os.makedirs(d, exist_ok=True); x = np.arange(0, L + 1e-9, 0.5); n = len(x); X = np.c_[x, np.zeros(n), np.zeros(n)]
    cl = pv.PolyData(X, lines=np.hstack([[2, i, i + 1] for i in range(n - 1)]))
    r = rad(x)
    for k, v in dict(MaximumInscribedSphereRadius=r, r_target_mm=r, r_source_mm=np.full(n, R), radial_scale=r / R, r_ref_mm=np.full(n, R), r_fit_mm=np.full(n, R)).items(): cl.point_data[k] = v
    cl.point_data["segment_name"] = np.array(["LAD"] * n); cl.point_data["branch_id"] = np.zeros(n, int); cl.point_data["tree_node"] = np.arange(n); cl.point_data["resolved"] = np.ones(n, int)
    cl.save(f"{d}/centreline.vtp")
    it, im, io = 12, 32, n - 1
    pr = [dict(probe_id="inlet", kind="inlet", tree_node=0), dict(probe_id="p001", kind="grid", tree_node=4), dict(probe_id="p002", kind="throat", tree_node=it),
          dict(probe_id="p003", kind="grid", tree_node=24), dict(probe_id="p004", kind="measurement", tree_node=im), dict(probe_id=f"out_{io}", kind="outlet", tree_node=io)]
    with open(f"{d}/probes.csv", "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(["probe_id", "kind", "s_mm", "s_node_mm", "s_from_lesion_mm", "tree_node", "x", "y", "z", "normal_x", "normal_y", "normal_z", "r_ref_mm", "resolved"])
        for p in pr:
            k = p["tree_node"]; nrm = [np.cos(np.radians(tilt)), np.sin(np.radians(tilt)), 0.0] if p["kind"] == "measurement" else [1.0, 0.0, 0.0]
            w.writerow([p["probe_id"], p["kind"], x[k] if p["kind"] != "outlet" else "", x[k], (x[k] - XT) if p["kind"] != "outlet" else "", k, x[k], 0.0, 0.0, *nrm, R, 1 if p["kind"] != "outlet" else 0])
    Q = (P_AORTA - PV) / (R_OUT + 1e9)
    open(f"{d}/outlets.csv", "w").write(f"outlet_id,tree_node,x,y,z,normal_x,normal_y,normal_z,r_ref_mm,r_mm,territory_id\nout_{io},{io},{L},0,0,1,0,0,{R},{R},0\n")
    open(f"{d}/bc_A.csv", "w").write(f"outlet_id,mode,R_SI,R_kinematic\nout_{io},resistance,{R_OUT!r},{R_OUT / RHO!r}\n")
    open(f"{d}/bc_C_flows.csv", "w").write(f"outlet_id,mode,territory_id,Q_target_m3s,Q_target_mls\nout_{io},prescribed,0,{Q!r},{Q * 1e6!r}\n")
    open(f"{d}/territories.csv", "w").write(f"territory_id,root_tree_node,root_clean_node,Q_clean_surviving_mls,Q_clean_full_territory_mls,n_outlets\n0,0,0,{Q * 1e6},{Q * 1e6},1\n")
    json.dump(dict(P_aorta_Pa=P_AORTA, P_venous_Pa=PV, P_aorta_kinematic=P_AORTA / RHO, P_venous_kinematic=PV / RHO, rho=RHO, mu=MU, nu=MU / RHO, inlet=dict(x=0.0, y=0.0, z=0.0, r_mm=R, normal=[1.0, 0.0, 0.0])), open(f"{d}/inlet.json", "w"), indent=1)
    json.dump(dict(frame="mm (synthetic test tube, not a patient)", instance=dict(scan=99999, side="left", vessel="LAD", loc="prox", L_mm=6.0, ds_pct=40, c_mm=XT), error_type="baseline", tier="synthetic",
                   measurement=dict(tree_node=im, s_mm=float(x[im]))), open(f"{d}/meta.json", "w"), indent=1)

def mesh(d, nx=97, nc=10, nr=8):
    os.makedirs(f"{d}/system", exist_ok=True); os.makedirs(f"{d}/constant", exist_ok=True)
    a, Rm, Lm = 0.4e-3, R * 1e-3, L * 1e-3; c45 = Rm / np.sqrt(2)
    v = []
    for xx in (0.0, Lm): v += [(xx, -a, -a), (xx, a, -a), (xx, a, a), (xx, -a, a), (xx, -c45, -c45), (xx, c45, -c45), (xx, c45, c45), (xx, -c45, c45)]
    V = lambda i, side: i + 8 * side
    def hexb(q, n1, n2): return f"    hex ({' '.join(str(V(i, 0)) for i in q)} {' '.join(str(V(i, 1)) for i in q)}) ({n1} {n2} {nx}) simpleGrading (1 1 1)\n"
    # blocks in the y-z plane, extruded along x (local third direction = x)
    blocks = hexb([0, 1, 2, 3], nc, nc) + hexb([4, 5, 1, 0], nc, nr) + hexb([5, 6, 2, 1], nc, nr) + hexb([6, 7, 3, 2], nc, nr) + hexb([7, 4, 0, 3], nc, nr)
    edges = ""
    for side, xx in ((0, 0.0), (1, Lm)):
        for i, j, (yy, zz) in ((4, 5, (0, -Rm)), (5, 6, (Rm, 0)), (6, 7, (0, Rm)), (7, 4, (-Rm, 0))): edges += f"    arc {V(i, side)} {V(j, side)} ({xx} {yy} {zz})\n"
    face = lambda q, side: "(" + " ".join(str(V(i, side)) for i in q) + ")"
    quads = ([0, 1, 2, 3], [4, 5, 1, 0], [5, 6, 2, 1], [6, 7, 3, 2], [7, 4, 0, 3])
    inlet = " ".join(face(q[::-1], 0) for q in quads); outlet = " ".join(face(q, 1) for q in quads)
    wall = " ".join(f"({V(i, 0)} {V(j, 0)} {V(j, 1)} {V(i, 1)})" for i, j in ((4, 5), (5, 6), (6, 7), (7, 4)))
    open(f"{d}/system/blockMeshDict", "w").write("FoamFile { version 2.0; format ascii; class dictionary; object blockMeshDict; }\nscale 1;\nvertices\n(\n" + "".join(f"    ({p[0]} {p[1]} {p[2]})\n" for p in v)
        + ");\nblocks\n(\n" + blocks + ");\nedges\n(\n" + edges + ");\nboundary\n(\n" + f"    inlet {{ type patch; faces ({inlet}); }}\n    out_40 {{ type patch; faces ({outlet}); }}\n    wall {{ type wall; faces ({wall}); }}\n);\n")
    open(f"{d}/system/controlDict", "w").write("FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }\napplication blockMesh; startFrom startTime; startTime 0; stopAt endTime; endTime 1; deltaT 1; writeControl timeStep; writeInterval 1; writeFormat ascii;\n")
    r = subprocess.run(["bash", "-c", FOAM + f"cd {d} && blockMesh > log.blockMesh 2>&1"]); assert r.returncode == 0, "blockMesh failed"
    f = f"{d}/constant/polyMesh/points"; txt = open(f).read(); k = txt.index("\n(\n") + 3; head, body = txt[:k], txt[k:]
    lines = body.split("\n"); n_pts = int(head.rstrip().split("\n")[-2].strip())
    pts = np.array([list(map(float, ln.strip()[1:-1].split())) for ln in lines[:n_pts]]); assert lines[n_pts].strip() == ")", lines[n_pts]
    s = rad(pts[:, 0] * 1e3) / R; pts[:, 1] *= s; pts[:, 2] *= s
    open(f, "w").write(head + "".join(f"({p[0]:.12g} {p[1]:.12g} {p[2]:.12g})\n" for p in pts) + ")\n")
    for k in ("fvSchemes", "fvSolution"): open(f"{d}/system/{k}", "w").write(open(f"{TEMPLATE}/system/{k}").read())
    r = subprocess.run(["bash", "-c", FOAM + f"cd {d} && checkMesh > log.checkMesh 2>&1"]); ok = "Mesh OK" in open(f"{d}/log.checkMesh").read()
    nc_ = int(open(f"{d}/log.checkMesh").read().split("cells:")[1].split()[0])
    json.dump(dict(case="synthetic", cells=nc_, checkMesh_standard_OK=ok, max_nonortho=None, max_skew=None, strict_failed_checks=0, GATES_PASS=ok, note="synthetic test tube (blockMesh)"), open(f"{d}/mesh_gates.json", "w"), indent=1)
    return nc_, ok

if __name__ == "__main__":
    root = sys.argv[1]; tilt = float(sys.argv[sys.argv.index("--tilt-measurement") + 1]) if "--tilt-measurement" in sys.argv else 0.0
    package(f"{root}/pkg/{NAME}", tilt); n, ok = mesh(f"{root}/mesh"); print(f"synthetic package {root}/pkg/{NAME}, mesh {root}/mesh: {n} cells, checkMesh OK {ok}")
