"""Build and mesh wedge_W<k> of the U3D 2D-axisymmetric cross-check family (u3d_design.md section 7): blockMesh of the SAME analytic sten70 geometry as the 3D family (radius law of make_stageA_geometry.py imported, not copied),
2 degree wedge about the x axis (collapsed axis), structured, every block count doubling with the level k (cell size ratio exactly 2 in x and r). Same BCs/numerics/monitors as build_sten70_case.py except that the coded resistance uses
R_wedge = R * 360/theta so that p = Pv + R*Q_full is enforced from the wedge flux Q_full*theta/360; throat/outlet/inlet fluxes in the monitors are WEDGE fluxes (u3d_analyse.py multiplies by 360/theta).
usage: build_wedge_case.py <k 0..4> [nproc]      (default nproc: 2,2,4,8,16 for k = 0..4)     Output dir u3d/wedge_W<k> (must not exist). Runs blockMesh + checkMesh only (no solver).
Axial layout (mm): Z1 [-15, 11.5] graded 8a -> a; Z2a [11.5, 26.5] uniform a; ten 1 mm lesion sub-blocks [26.5, 36.5] uniform a (a block boundary resets the wall-arc / axis-x drift of blockMesh's polyLine edges); Z2b [36.5, 51.5] uniform a;
Z3 [51.5, 100] graded a -> 8a. a = 50 um / 2^k. Radial: N_r = 9 * 2^k cells from the axis to the wall, wall cell = 1/3 of the axis cell (simpleGrading 1/3), one cell in azimuth."""
import sys, os, re, shutil, json, subprocess, importlib.util
import numpy as np
U = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(U); TEMPLATE = f"{P}/../A5_sten70_fine"
G = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/stageA/make_stageA_geometry.py"
spec = importlib.util.spec_from_file_location("stageA_geo", G); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
THETA_DEG = 2.0; HALF = np.radians(THETA_DEG / 2); WEDGE_SCALE = 360.0 / THETA_DEG
R_SI, PV, RHO, RELAX, P_INIT, P_AORTA_KIN = 6.974826e9, 666.61, 1060.0, 0.2, 8.0694, 11.3198
R_WEDGE = R_SI * WEDGE_SCALE
END = int(os.environ.get("U3D_END", "3000"))      # fixed per-level budget (design v2.4); the launcher must be told with RUN_SET_END_MAP when it is not 3000
NX0 = dict(Z1=160, Z2a=300, LES=20, Z2b=300, Z3=288)      # cells per block at level 0 (a0 = 50 um): 160 + 300 + 10*20 + 300 + 288 = 1248
NR0, GRAD_R = 9, 1.0 / 3.0
POLY_DX = {"lesion": 0.01, "other": 0.2}                   # polyLine node spacing (mm) on the wall edges
RATIO_END = 8.0

def radius_m(x_mm): return float(g.radius_sten(x_mm, 70)) * 1e-3

def block_layout(k):
    f = 2 ** k; blocks = [("Z1", -15.0, 11.5, NX0["Z1"] * f, 1.0 / RATIO_END), ("Z2a", 11.5, 26.5, NX0["Z2a"] * f, 1.0)]
    for i in range(10): blocks.append((f"L{i}", 26.5 + i, 27.5 + i, NX0["LES"] * f, 1.0))
    blocks += [("Z2b", 36.5, 51.5, NX0["Z2b"] * f, 1.0), ("Z3", 51.5, 100.0, NX0["Z3"] * f, RATIO_END)]
    return blocks

def edge_points(x0, x1, sign):
    dx = POLY_DX["lesion"] if 26.5 <= x0 < 36.5 else POLY_DX["other"]
    n = max(int(round((x1 - x0) / dx)), 1); xs = np.linspace(x0, x1, n + 1)[1:-1]
    xs = np.array(sorted(set(np.round(np.concatenate([xs, [k for k in (0.0, 90.0) if x0 < k < x1]]), 9))))      # the radius law has slope kinks at x = 0 and 90 mm: put a polyLine node exactly on them
    return [(x * 1e-3, radius_m(x) * np.cos(HALF), sign * radius_m(x) * np.sin(HALF)) for x in xs]

def blockmesh_dict(k):
    bl = block_layout(k); xs = [bl[0][1]] + [b[2] for b in bl]; nst = len(xs)
    vert, lines = [], []      # per station i: A_i (axis), F_i (front wall z<0), B_i (back wall z>0): labels 3i, 3i+1, 3i+2
    for x in xs:
        r = radius_m(x); vert += [(x * 1e-3, 0.0, 0.0), (x * 1e-3, r * np.cos(HALF), -r * np.sin(HALF)), (x * 1e-3, r * np.cos(HALF), r * np.sin(HALF))]
    A = lambda i: 3 * i; F = lambda i: 3 * i + 1; B = lambda i: 3 * i + 2
    s = "FoamFile { version 2.0; format ascii; class dictionary; object blockMeshDict; }\nconvertToMeters 1;\nvertices\n(\n" + "".join(f"    ({a:.9e} {b:.9e} {c:.9e})\n" for a, b, c in vert) + ");\nblocks\n(\n"
    for i, (name, x0, x1, n, rho) in enumerate(bl):
        s += f"    hex ({A(i)} {A(i+1)} {F(i+1)} {F(i)} {A(i)} {A(i+1)} {B(i+1)} {B(i)}) ({n} {NR0 * 2 ** k} 1) simpleGrading ({rho:.10g} {GRAD_R:.10g} 1)   // {name}\n"
    s += ");\nedges\n(\n"
    for i, (name, x0, x1, n, rho) in enumerate(bl):
        for lab, sg in ((F, -1.0), (B, 1.0)):
            pts = edge_points(x0, x1, sg); s += f"    polyLine {lab(i)} {lab(i+1)} (" + " ".join(f"({a:.9e} {b:.9e} {c:.9e})" for a, b, c in pts) + ")\n"
    s += ");\nboundary\n(\n"
    s += f"    inlet {{ type patch; faces (({A(0)} {B(0)} {F(0)} {A(0)})); }}\n"          # collapsed quad (A A B F): a triangle per axis cell; blockMesh collapses it
    s += f"    outlet {{ type patch; faces (({A(nst-1)} {F(nst-1)} {B(nst-1)} {A(nst-1)})); }}\n"
    s += "    wall { type wall; faces (" + " ".join(f"({F(i)} {F(i+1)} {B(i+1)} {B(i)})" for i in range(len(bl))) + "); }\n"
    s += "    front { type wedge; faces (" + " ".join(f"({A(i)} {A(i+1)} {F(i+1)} {F(i)})" for i in range(len(bl))) + "); }\n"
    s += "    back { type wedge; faces (" + " ".join(f"({A(i)} {B(i)} {B(i+1)} {A(i+1)})" for i in range(len(bl))) + "); }\n"
    s += ");\nmergePatchPairs ();\n"
    return s

P_TXT = """FoamFile { version 2.0; format ascii; class volScalarField; object p; }
dimensions      [0 2 -2 0 0 0 0];
internalField   uniform %(pi)s;

boundaryField
{
    inlet   { type totalPressure; p0 uniform %(pa)s; value uniform %(pa)s; }
    wall    { type zeroGradient; }
    front   { type wedge; }
    back    { type wedge; }

    outlet
    {
        type            codedFixedValue;
        value           uniform %(pi)s;
        name            resOut;
        code
        #{
            const scalar R     = %(R).8e;
            const scalar Pv    = %(Pv)s;
            const scalar rho   = %(rho)s;
            const scalar relax = %(relax).8f;
            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            const scalar pTarget = (Pv + R*Q)/rho;
            const volScalarField& pFld = db().lookupObject<volScalarField>("p");
            const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);
            operator==((1.0 - relax)*pOld + relax*pTarget);
        #};
    }
}
"""
U_TXT = """FoamFile { version 2.0; format ascii; class volVectorField; object U; }
dimensions      [0 1 -1 0 0 0 0];
internalField   uniform (0.2 0 0);

boundaryField
{
    inlet   { type pressureInletOutletVelocity; value uniform (0 0 0); }
    outlet  { type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }
    wall    { type noSlip; }
    front   { type wedge; }
    back    { type wedge; }
}
"""
def fo(name, patch=None, op=None, fld=None, plane=None):
    hd = f"    {name}\n    {{\n        type surfaceFieldValue; libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log true;\n"
    if plane is None: return hd + f"        regionType patch; name {patch}; operation {op}; fields ({fld});\n    }}\n"
    return hd + (f"        regionType sampledSurface; name {name}Plane;\n        sampledSurfaceDict\n        {{\n            type plane; planeType pointAndNormal;\n            pointAndNormalDict {{ point ({plane:.6f} 0 0); normal (1 0 0); }}\n            interpolate false;\n        }}\n"
                 f"        operation {op}; fields ({fld});\n    }}\n")

def main(k, nproc=None):
    if k not in range(5): raise SystemExit("k must be 0..4")
    nproc = nproc or (2, 2, 4, 8, 16)[k]; case = f"{U}/wedge_W{k}"
    if os.path.exists(case): raise SystemExit(f"{case} exists")
    os.makedirs(f"{case}/constant"); os.makedirs(f"{case}/system"); os.makedirs(f"{case}/0")
    open(f"{case}/system/blockMeshDict", "w").write(blockmesh_dict(k))
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{TEMPLATE}/constant/{f}", f"{case}/constant/{f}")
    for f in ("fvSchemes", "fvSolution"): shutil.copy(f"{TEMPLATE}/system/{f}", f"{case}/system/{f}")
    open(f"{case}/0/U", "w").write(U_TXT); open(f"{case}/0/p", "w").write(P_TXT % dict(pi=P_INIT, pa=P_AORTA_KIN, R=R_WEDGE, Pv=PV, rho=RHO, relax=RELAX))
    open(f"{case}/system/decomposeParDict", "w").write(f"FoamFile {{ version 2.0; format ascii; class dictionary; object decomposeParDict; }}\nnumberOfSubdomains {nproc};\nmethod simple;\nsimpleCoeffs {{ n ({nproc} 1 1); }}\n")
    fns = fo("inletFlux", "inlet", "sum", "phi") + fo("outletFlux", "outlet", "sum", "phi") + fo("outletPressure", "outlet", "areaAverage", "p") + fo("inletPressure", "inlet", "areaAverage", "p") + fo("measurementP", op="areaAverage", fld="p", plane=0.0565) + \
          fo("throatFlux", op="areaNormalIntegrate", fld="U", plane=0.031503) + fo("throatP", op="areaAverage", fld="p", plane=0.031503)
    open(f"{case}/system/controlDict", "w").write("FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }\n"
        f"application     simpleFoam;\nstartFrom       startTime;\nstartTime       0;\nstopAt          endTime;\nendTime         {END};\ndeltaT          1;\nwriteControl    timeStep;\nwriteInterval   250;\npurgeWrite      2;\nwriteFormat     ascii;\n"
        "writePrecision  8;\nwriteCompression off;\ntimeFormat      general;\ntimePrecision   8;\nrunTimeModifiable true;\n\nfunctions\n{\n" + fns + "}\n")
    json.dump(dict(case=f"wedge_W{k}", Q_demand_mls=None, outlets={"outlet": dict(R_out=R_WEDGE, relax=RELAX, Q0_mls=None)}), open(f"{case}/zerod_reference.json", "w"), indent=1)
    open(f"{case}/case.foam", "w").close()
    env = "source /usr/lib/openfoam/openfoam2406/etc/bashrc; cd " + case + "; "
    subprocess.run(["bash", "-c", env + "blockMesh > log.blockMesh 2>&1; checkMesh > log.checkMesh.standard 2>&1; checkMesh -allGeometry -allTopology > log.checkMesh.strict 2>&1"], check=True)
    gates = mesh_gates(case, k, nproc); subprocess.run(["sed", "-i", "s/^writeFormat .*/writeFormat     binary;/", f"{case}/system/controlDict"], check=True)   # ascii for the mesh build/gates parse, binary fields for the run (disk)
    json.dump(gates, open(f"{case}/mesh_gates.json", "w"), indent=1); print(json.dumps(gates, indent=1))
    json.dump(dict(level=f"W{k}", family="wedge", theta_deg=THETA_DEG, wedge_scale=WEDGE_SCALE, endTime=END, R_SI_full=R_SI, R_wedge=R_WEDGE, relax=RELAX, nproc=nproc, mesh_gates=gates), open(f"{case}/build_info.json", "w"), indent=1)
    if not gates["GATES_PASS"]: raise SystemExit("mesh gates failed: see mesh_gates.json (the mesh is NOT to be used)")

def mesh_gates(case, k, nproc):
    bm = open(f"{case}/log.blockMesh").read(); std = open(f"{case}/log.checkMesh.standard").read(); strict = open(f"{case}/log.checkMesh.strict").read()
    gg = dict(level=f"W{k}", blockMesh_finished=("End" in bm), checkMesh_standard_OK=("Mesh OK" in std))
    m = re.search(r"cells:\s+(\d+)", strict); gg["cells"] = int(m.group(1)) if m else None
    gg["strict_failed_checks"] = int(re.search(r"Failed (\d+) mesh checks", strict).group(1)) if "Failed" in strict else 0
    for kk, pat in (("max_nonortho", r"Mesh non-orthogonality Max: ([\d.]+)"), ("max_skew", r"Max skewness = ([\d.]+)"), ("max_aspect", r"Max aspect ratio = ([\d.]+)")):
        mm = re.search(pat, strict); gg[kk] = float(mm.group(1)) if mm else None
    bt = open(f"{case}/constant/polyMesh/boundary").read(); gg["patch_faces"] = {n: int(f) for n, f in re.findall(r"(\w+)\s*\{[^}]*?nFaces\s+(\d+);", bt)}
    pm = f"{case}/constant/polyMesh"; txt = open(f"{pm}/points").read(); body = txt[txt.index("(\n") + 2: txt.rindex(")")]
    pts = np.array([[float(v) for v in ln.strip()[1:-1].split()] for ln in body.strip().split("\n")])
    ftxt = open(f"{pm}/faces").read(); fl = [list(map(int, ln[ln.index("(") + 1: ln.rindex(")")].split())) for ln in ftxt.split("\n") if re.match(r"^\d+\(", ln)]
    bt2 = open(f"{pm}/boundary").read(); mw = re.search(r"wall\s*\{[^}]*?nFaces\s+(\d+);\s*startFace\s+(\d+);", bt2)
    nf, sf = int(mw.group(1)), int(mw.group(2)); widx = sorted({i for f in fl[sf:sf + nf] for i in f}); pts = pts[widx]
    x = pts[:, 0] * 1e3; r = np.hypot(pts[:, 1], pts[:, 2]) * 1e3
    r_law = np.asarray(g.radius_sten(x, 70), float)
    gg["wall_radius_max_abs_err_um"] = float(np.abs(r - r_law).max() * 1e3); gg["wall_r_min_mm"] = float(r.min()); gg["wall_r_min_at_x_mm"] = float(x[np.argmin(r)])
    vm = float(re.search(r"Total volume = ([0-9.]+e[+-][0-9]+)", strict).group(1)); xx = np.linspace(-15, 100, 230001); rr = np.asarray(g.radius_sten(xx, 70), float) * 1e-3
    v_an = float(np.trapz(0.5 * np.radians(THETA_DEG) * rr ** 2, xx * 1e-3)); v_flat = v_an * np.sin(np.radians(THETA_DEG)) / np.radians(THETA_DEG)
    gg["volume_mesh_over_flat_facet_analytic"] = vm / v_flat; gg["volume_note"] = "flat-facet wedge (chord at the wall) has sin(theta)/theta = 0.99980 of the circular sector"
    gg["axial_cell_um_at_throat"] = float(50.0 / 2 ** k); gg["radial_cells"] = NR0 * 2 ** k
    fine_ends = {}
    for name, L, N in (("Z1", 26.5, NX0["Z1"] * 2 ** k), ("Z3", 48.5, NX0["Z3"] * 2 ** k)):
        q = RATIO_END ** (1.0 / (N - 1)); fine_ends[name + "_fine_end_um"] = float(L * (q - 1) / (q ** N - 1) * 1e3)
    gg.update(fine_ends)
    gg["GATES_PASS"] = bool(gg["blockMesh_finished"] and gg["checkMesh_standard_OK"] and all(v > 0 for kk, v in gg["patch_faces"].items() if kk != "defaultFaces") and gg["patch_faces"].get("defaultFaces", 0) == 0 and abs(gg["wall_r_min_mm"] - 0.4455) < 2e-4 * 1 and gg["wall_radius_max_abs_err_um"] < 0.05 and abs(gg["volume_mesh_over_flat_facet_analytic"] - 1) < 2e-3)
    return gg

if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    main(int(sys.argv[1]), int(sys.argv[2]) if len(sys.argv) > 2 else None)
