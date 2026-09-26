"""Build the Item-3 solve cases (baseline + missed-branch) on the REBUILT surfaces/meshes.

Adopts opus_debug/CF_{baseline,missedbranch}_fixedsurf (valid cfMesh meshes built from the rebuilt STLs) into
solve_{baseline,missedbranch}/, adds 0/U, 0/p (multi-outlet resistance BC, literal R/relax per outlet as in
Item 1's validated template, unique coded-BC names) and system/ monitors + decomposeParDict.

0D twin: scan 837/left, bed='discrete' (explicit - the loader defaults to leaky), Q_demand from the healthy
tree's own Murray demand (an inlet property, unchanged for the missed-branch case). Missed-branch: D2's segment
(and descendants) deleted from the 0D tree, tree re-calibrated to the SAME Q_demand, so the remaining outlets'
R values reflect the redistributed flow (design.md, Item 3 step 5).
Leaf -> patch matching is by vessel label AND verified by coordinate (leaf xyz + 20 mm extension along the leaf
tangent must land within TOL of the patch centroid) - labels alone are not trusted (design.md, Item 4).
"""
import sys, os, re, shutil, json
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
import numpy as np
import pyvista as pv
from zerod_ffr import Tree, RHO, MU, P_AORTA, P_VEN
from outlets_837 import build_tree, node_xyz_and_tangent

BASE = "/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item3_M1_pilot"
EXT_MM = 20.0          # flow-extension length used by the rebuilt surfaces (opus_debug/rebuild_surface.py)
TOL_MM = 3.0           # leaf->patch coordinate-match tolerance
NPROC = int(os.environ.get("NPROC", "16"))
P0_KIN = P_AORTA / RHO

def drop_branch(T, label):
    kill = {s.sid for s in T.segments if s.label == label}
    changed = True
    while changed:
        changed = False
        for s in T.segments:
            if s.parent in kill and s.sid not in kill:
                kill.add(s.sid); changed = True
    keep = [s for s in T.segments if s.sid not in kill]
    T2 = Tree(keep, f"{T.name}_no{label}", bed="discrete")
    T2.segments = keep
    return T2, sorted(kill)

def terminal_R_own(T, v):
    """Poiseuille resistance of the leaf's own terminal vessel (active nodes of its segment up to v, actual r_ref)
    plus the flow extension at the leaf radius (panel-mandated static G_i = R_i/R_own,i, Item 1 resolution)."""
    sid = T.seg[v]
    nodes = [n for n in np.where(T.seg == sid)[0] if T.active[n] and n <= v]
    R = 0.0
    for n in nodes:
        rm = 0.5 * (T.r_ref[n] + T.r_ref[T.parent[n]])
        R += 8 * MU * T.ds[n] / (np.pi * rm ** 4)
    r_leaf = T.r_ref[v]
    R_ext = 8 * MU * (EXT_MM * 1e-3) / (np.pi * r_leaf ** 4)
    return R + R_ext, sum(T.ds[n] for n in nodes)

def patch_centroids(case_dir):
    open(f"{case_dir}/case.foam", "w").close()
    rd = pv.OpenFOAMReader(f"{case_dir}/case.foam")
    rd.disable_all_cell_arrays(); rd.disable_all_point_arrays()
    rd.enable_all_patch_arrays()
    mb = rd.read()
    out = {}
    def walk(b, prefix=""):
        for i in range(b.n_blocks):
            name = b.get_block_name(i)
            blk = b[i]
            if isinstance(blk, pv.MultiBlock):
                walk(blk, prefix + name + "/")
            elif blk is not None and blk.n_points:
                out[prefix + name] = np.asarray(blk.points).mean(axis=0) * 1e3   # metres -> mm
    walk(mb)
    return {k.split("/")[-1]: v for k, v in out.items() if "outlet" in k or k.split("/")[-1] == "inlet"}

U_T = """FoamFile {{ version 2.0; format ascii; class volVectorField; object U; }}
dimensions [0 1 -1 0 0 0 0];
internalField uniform (0 0 0);
boundaryField
{{
    inlet   {{ type pressureInletOutletVelocity; value uniform (0 0 0); }}
{outlets}
    wall    {{ type noSlip; }}
}}
"""
P_T = """FoamFile {{ version 2.0; format ascii; class volScalarField; object p; }}
dimensions [0 2 -2 0 0 0 0];
internalField uniform {p0:.6f};
boundaryField
{{
    inlet   {{ type totalPressure; p0 uniform {p0:.6f}; value uniform {p0:.6f}; }}
{outlets}
    wall    {{ type zeroGradient; }}
}}
"""
P_OUT = """    {patch}
    {{
        type            codedFixedValue;
        value           uniform {p_init:.6f};
        name            res{cname};
        code
        #{{
            const scalar R     = {R:.8e};
            const scalar Pv    = {Pv};
            const scalar rho   = {rho};
            const scalar relax = {relax:.8f};
            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            const scalar pTarget = (Pv + R*Q)/rho;
            const volScalarField& pFld = db().lookupObject<volScalarField>("p");
            const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);
            operator==((1.0 - relax)*pOld + relax*pTarget);
        #}};
    }}
"""

def functions_block(patches):
    s = "functions\n{\n"
    def blk(name, patch, op, field):
        return (f"    {name}\n    {{\n        type surfaceFieldValue;\n        libs (\"libfieldFunctionObjects.so\");\n"
                f"        writeControl timeStep; writeInterval 1; writeFields false; log true;\n"
                f"        regionType patch; name {patch}; operation {op}; fields ({field});\n    }}\n")
    s += blk("inletFlux", "inlet", "sum", "phi")
    s += blk("inletPressure", "inlet", "areaAverage", "p")
    for p in patches:
        s += blk(f"{p}Flux", p, "sum", "phi")
        s += blk(f"{p}Pressure", p, "areaAverage", "p")
    return s + "}\n"

def build_case(name, src_case, T, Q_demand):
    dst = f"{BASE}/solve_{name}"
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    for sub in ("constant", "system"):
        shutil.copytree(f"{src_case}/{sub}", f"{dst}/{sub}")
    for f in ("log.checkMesh", "log.cartesianMesh"):
        if os.path.exists(f"{src_case}/{f}"):
            shutil.copy(f"{src_case}/{f}", dst)
    # ---- 0D characterisation
    C = T.calibrate(Q_demand)
    ffr, Qn, info, sten, K = T.evaluate(C)
    cent = patch_centroids(dst)
    rows = {}
    for v in T.leaves:
        lab = T.label[v]
        patch = f"outlet_{lab}"
        if patch not in cent:
            raise SystemExit(f"leaf {v} ({lab}) has no mesh patch {patch}; patches: {list(cent)}")
        p_xyz, tan = node_xyz_and_tangent(T, v)
        expect = p_xyz + EXT_MM * tan
        dist = float(np.linalg.norm(expect - cent[patch]))
        assert dist < TOL_MM, f"{patch}: leaf+extension {np.round(expect,1)} vs patch centroid {np.round(cent[patch],1)} = {dist:.2f} mm > {TOL_MM}"
        R_bed = C / T.w[v]
        R_ext = 8 * MU * (EXT_MM * 1e-3) / (np.pi * T.r_ref[v] ** 4)
        # diagnostic variant: the 3D outlet patch sits EXT_MM beyond the 0D leaf, so the extension's own Poiseuille
        # resistance is in series; '_extcomp' subtracts it so leaf->bed total matches the 0D twin
        R_out = R_bed - R_ext if name.endswith("_extcomp") else R_bed
        R_own, L_own = terminal_R_own(T, v)
        G = R_out / R_own
        relax = min(0.5, 1.0 / (1.0 + G))
        Q0 = float(Qn[v])
        p_init = (P_VEN + R_out * Q0) / RHO
        rows[patch] = dict(leaf=int(v), label=lab, r_ref_mm=float(T.r_ref[v] * 1e3), R_out=float(R_out), R_bed=float(R_bed),
                           R_ext=float(R_ext), R_own=float(R_own),
                           L_own_mm=float(L_own * 1e3), G=float(G), relax=float(relax), Q0_mls=Q0 * 1e6,
                           p_init_kin=float(p_init), match_mm=dist)
    missing = [p for p in cent if p.startswith("outlet") and p not in rows]
    assert not missing, f"mesh patches without a 0D leaf: {missing}"
    outlets_U = "".join(f"    {p} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}\n" for p in rows)
    outlets_P = "".join(P_OUT.format(patch=p, cname=p.split('_')[1], p_init=d["p_init_kin"], R=d["R_out"], Pv=P_VEN,
                                     rho=RHO, relax=d["relax"]) for p, d in rows.items())
    os.makedirs(f"{dst}/0")
    open(f"{dst}/0/U", "w").write(U_T.format(outlets=outlets_U))
    open(f"{dst}/0/p", "w").write(P_T.format(p0=P0_KIN, outlets=outlets_P))
    # ---- system: monitors + decomposition
    cd = open(f"{dst}/system/controlDict").read()
    head = cd[:cd.index("functions")]
    head = re.sub(r"writeInterval\s+100;", "writeInterval   250;", head)
    open(f"{dst}/system/controlDict", "w").write(head + functions_block(list(rows)))
    open(f"{dst}/system/decomposeParDict", "w").write(
        "FoamFile { version 2.0; format ascii; class dictionary; object decomposeParDict; }\n"
        f"numberOfSubdomains {NPROC};\nmethod scotch;\n")
    json.dump(dict(case=name, Q_demand_mls=Q_demand * 1e6, C=float(C), inflow_mls=info["inflow"] * 1e6,
                   healthy_main_ffr=float(T.ffr(mode="murray")["min_ffr_main"]), outlets=rows,
                   patch_centroids_mm={k: v.tolist() for k, v in cent.items()}),
              open(f"{dst}/zerod_reference.json", "w"), indent=1)
    print(f"\n=== {name}: {len(rows)} outlets, Q_demand={Q_demand*1e6:.4f} mL/s, 0D inflow={info['inflow']*1e6:.4f} mL/s ===")
    for p, d in rows.items():
        print(f"  {p:12s} r={d['r_ref_mm']:.3f}mm R_out={d['R_out']:.4e} R_own={d['R_own']:.3e} (L={d['L_own_mm']:.1f}mm) "
              f"G={d['G']:.1f} relax={d['relax']:.5f} Q0={d['Q0_mls']:.4f}mL/s coord-match={d['match_mm']:.2f}mm")
    return dst

if __name__ == "__main__":
    T = build_tree()
    Qd = T.demand("murray")
    if len(sys.argv) > 1 and sys.argv[1] == "extcomp":
        build_case("baseline_extcomp", f"{BASE}/opus_debug/CF_baseline_fixedsurf", T, Qd)
        sys.exit(0)
    build_case("baseline", f"{BASE}/opus_debug/CF_baseline_fixedsurf", T, Qd)
    T2, killed = drop_branch(T, "D2")
    print(f"\nmissed-branch 0D tree: deleted segment sids {killed}; leaves now {[T2.label[v] for v in T2.leaves]}")
    build_case("missedbranch", f"{BASE}/opus_debug/CF_missedbranch_fixedsurf", T2, Qd)
