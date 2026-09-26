"""Build pimple_lesion80: transient steadiness check of the converged resting lesion80 solution (transient_design.md).
Mesh = solve_lesion80's (symlinked constant/polyMesh), initial fields = its converged steady time (U, p, phi copied as time 0), boundary conditions = the same inlet
totalPressure and the same five resistance outlets (R_out from solve_lesion80/zerod_reference.json, identical values) but WITHOUT the steady-state relaxation device:
p_out = (Pv + R Q)/rho with Q the current patch flux (explicit lag, see the design), pimpleFoam, backward Euler-2 time integration.
usage: build_pimple_case.py [time_dir_of_steady_solution]   (default: the latest numeric directory of solve_lesion80)
Refuses to overwrite a case that has run output.
MESH IS SHARED: constant/polyMesh is a SYMLINK to solve_lesion80/constant/polyMesh (the resting steady case). NOTHING may write into pimple_lesion80/constant/polyMesh
(no topoSet/setSet/setsToZones/refineMesh/renumberMesh/checkMesh -writeSets/-writeFields, no mesh-changing utility run in the serial case): it would silently modify the steady case.
decomposePar only reads it (processor*/constant/polyMesh are private copies). The symlink target must stay exactly P/solve_lesion80/constant/polyMesh.
Monitors (names recorded in build_info.json 'monitors' and read from there by pimple_analyse.py / pimple_gate.py): inletFlux, inletPressure, outlet_<X>Flux/Pressure for the five outlets
(surfaceFieldValue on the patches), throatFlux (surfaceFieldValue regionType sampledSurface: a cutting plane through lesion80_open_info.json throat_xyz_mm with normal throat_axis,
trimmed by a bounding box of +-THROAT_BOX_MM so that only the throat lumen is cut; operation areaNormalIntegrate of U = cell-value-sampled flux, approximate, NOT the conservative phi;
a time-variation monitor only) and jetProbes (probes: U, p at six points)."""
import sys, os, re, json, shutil, glob
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from zerod_ffr import RHO, P_VEN, P_AORTA
from outlets_837 import build_tree
import build_lesion80_surface as G

BASE = os.path.dirname(os.path.abspath(__file__)); SRC = f"{BASE}/solve_lesion80"; DST = f"{BASE}/pimple_lesion80"
NPROC = int(os.environ.get("PIMPLE_NPROC", "32"))
DT0, DTMAX, MAXCO, T_END, T_WRITE = 2.5e-5, 4.0e-5, 0.8, 0.08, 0.01
THROAT_BOX_MM = 1.0                                  # half-width of the bounding box trimming the throat cutting plane (throat radius 0.377 mm)
PROBE_ARCS = (25.5, 28.5, 31.5)                      # 2, 5 and 8 mm past the throat (arc 23.5), before the D1 ostium influence

P_OUT = """    {patch}
    {{
        type            codedFixedValue;
        value           uniform {p0:.8f};
        name            res{cname};
        code
        #{{
            // explicit-lag resistance outlet: p = (Pv + R Q)/rho with Q the current flux of the patch (no p.prevIter() relaxation: that device belongs to SIMPLE)
            const scalar R     = {R:.8e};
            const scalar Pv    = {Pv};
            const scalar rho   = {rho};
            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            operator==((Pv + R*Q)/rho);
        #}};
    }}
"""
HEAD = "FoamFile {{ version 2.0; format ascii; class {cls}; object {obj}; }}\n"

def latest_time():
    ts = [(float(os.path.basename(d)), d) for d in glob.glob(f"{SRC}/[0-9]*") if os.path.isdir(d) and float(os.path.basename(d)) > 0]
    return max(ts)[1]

def main(tdir=None):
    if os.path.exists(DST):
        done = [d for d in os.listdir(DST) if (re.match(r"^[0-9.eE+-]+$", d) and d != "0") or d.startswith("processor") or d in ("log.pimpleFoam", "log.smoke", "log.decomposePar", "log.gate", "postProcessing", "dynamicCode", "GATE_OK", "GATE_FAILED", "mpirun.rc")]
        done += [f"system/{f}" for f in ("controlDict.production",) if os.path.exists(f"{DST}/system/{f}")]
        if done: raise SystemExit(f"refusing to overwrite {DST}: it holds run output {done[:4]}")
        shutil.rmtree(DST)
    tdir = tdir or latest_time()
    for f in ("U", "p", "phi"):
        assert os.path.exists(f"{tdir}/{f}"), f"{tdir}/{f} missing (reconstructed steady solution needed)"
    os.makedirs(f"{DST}/constant"); os.makedirs(f"{DST}/system"); os.makedirs(f"{DST}/0")
    os.symlink(f"{SRC}/constant/polyMesh", f"{DST}/constant/polyMesh")
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{SRC}/constant/{f}", f"{DST}/constant/{f}")
    shutil.copy(f"{tdir}/U", f"{DST}/0/U"); shutil.copy(f"{tdir}/phi", f"{DST}/0/phi");     # ---- p: internal field and the inlet from the converged steady solution, outlets replaced by the explicit-lag coded BC
    z = json.load(open(f"{SRC}/zerod_reference.json"))["outlets"]; an = json.load(open(f"{SRC}/analysis.json"))["outlets"]
    ptxt = open(f"{tdir}/p").read()
    m = re.search(r"boundaryField\s*\{", ptxt); head = ptxt[:m.start()]
    # the outlet 'value' entry only initialises the boundary field: the area-averaged steady patch pressure (analysis.json) is used; step 1 re-evaluates it from the copied flux phi
    outs = "".join(P_OUT.format(patch=p, cname=p.split("_")[1], p0=an[p]["P_Pa"] / RHO, R=d["R_out"], Pv=P_VEN, rho=RHO) for p, d in z.items())
    open(f"{DST}/0/p", "w").write(head + "boundaryField\n{\n    inlet   { type totalPressure; p0 uniform %.6f; value uniform %.6f; }\n%s    wall    { type zeroGradient; }\n}\n" % (P_AORTA / RHO, P_AORTA / RHO, outs))
    # ---- system
    open(f"{DST}/system/fvSchemes", "w").write(HEAD.format(cls="dictionary", obj="fvSchemes") + """ddtSchemes { default backward; }
gradSchemes { default Gauss linear; }
divSchemes { default none; div(phi,U) Gauss linearUpwind grad(U); div((nuEff*dev2(T(grad(U))))) Gauss linear; }
laplacianSchemes { default Gauss linear corrected; }
interpolationSchemes { default linear; }
snGradSchemes { default corrected; }
""")
    open(f"{DST}/system/fvSolution", "w").write(HEAD.format(cls="dictionary", obj="fvSolution") + """solvers
{
    p      { solver GAMG; smoother GaussSeidel; tolerance 1e-08; relTol 0.01; }
    pFinal { $p; relTol 0; }
    "(U)"      { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-09; relTol 0.1; }
    "(U)Final" { $U; relTol 0; }
}
PIMPLE { momentumPredictor yes; nOuterCorrectors 2; nCorrectors 2; nNonOrthogonalCorrectors 1; }
""")
    open(f"{DST}/system/decomposeParDict", "w").write(HEAD.format(cls="dictionary", obj="decomposeParDict") + f"numberOfSubdomains {NPROC};\nmethod scotch;\n")
    # ---- monitors: same surfaceFieldValue objects as the steady runs + velocity/pressure probes in the jet
    T = build_tree(); T.ffr(mode="murray"); dfm = G.Deformer(T); fr = dfm.fr
    pts = []
    for s in PROBE_ARCS:
        k = int(np.argmin(np.abs(fr["s"] - s))); c = fr["c"][k]; t = fr["t"][k]
        n = np.cross(t, [0.0, 0.0, 1.0]); n = n / np.linalg.norm(n)
        pts += [c, c + 0.4 * n]                                 # axis and 0.4 mm off axis (shear layer of the 0.34 mm throat jet widening downstream)
    plist = " ".join("({:.7f} {:.7f} {:.7f})".format(*(p * 1e-3)) for p in pts)
    blk = lambda name, patch, op, fld: (f"    {name}\n    {{\n        type surfaceFieldValue;\n        libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log true;\n"
                                        f"        regionType patch; name {patch}; operation {op}; fields ({fld});\n    }}\n")
    fo = blk("inletFlux", "inlet", "sum", "phi") + blk("inletPressure", "inlet", "areaAverage", "p")
    for p in z: fo += blk(f"{p}Flux", p, "sum", "phi") + blk(f"{p}Pressure", p, "areaAverage", "p")
    # throat-plane flux (transient_design.md sec. 2 'throat-section flux'); syntax checked against the installed v2406 sources: surfaceFieldValue.C (regionType sampledSurface ->
    # sampledSurface::New(sampledSurfaceDict), cell-value sampling, areaNormalIntegrate -> vector (sum(U & Sf), 0, 0)), sampledPlane.H (type plane, bounds) , plane.C (planeType pointAndNormal) and boundBox.C (bounds = two points without outer parentheses, as in tutorials .../squareBend/system/sampling)
    th = json.load(open(f"{BASE}/lesion80/lesion80_open_info.json")); tp = np.array(th["throat_xyz_mm"], float); tn = np.array(th["throat_axis"], float); tn = tn / np.linalg.norm(tn)
    v3 = lambda a: "({:.9g} {:.9g} {:.9g})".format(*a)
    fo += (f"    throatFlux\n    {{\n        type surfaceFieldValue;\n        libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log true;\n"
           f"        regionType sampledSurface; name throatPlane;\n        sampledSurfaceDict\n        {{\n            type plane; planeType pointAndNormal;\n"
           f"            pointAndNormalDict {{ point {v3(tp * 1e-3)}; normal {v3(tn)}; }}\n            bounds {v3((tp - THROAT_BOX_MM) * 1e-3)} {v3((tp + THROAT_BOX_MM) * 1e-3)};\n        }}\n"
           f"        operation areaNormalIntegrate; fields (U);\n    }}\n")
    fo += f"    jetProbes\n    {{\n        type probes;\n        libs (\"libsampling.so\");\n        writeControl timeStep; writeInterval 1;\n        fields (U p);\n        probeLocations ( {plist} );\n    }}\n"
    open(f"{DST}/system/controlDict", "w").write(HEAD.format(cls="dictionary", obj="controlDict") + f"""application pimpleFoam;
startFrom startTime; startTime 0; stopAt endTime; endTime {T_END};
deltaT {DT0}; adjustTimeStep yes; maxCo {MAXCO}; maxDeltaT {DTMAX};
writeControl adjustableRunTime; writeInterval {T_WRITE}; purgeWrite 3; writeFormat ascii; writePrecision 8; timeFormat general; timePrecision 8; runTimeModifiable no;
functions
{{
{fo}}}
""")
    json.dump(dict(source_case="solve_lesion80", steady_time=os.path.basename(tdir), dt0=DT0, dt_max=DTMAX, max_co=MAXCO, end_time=T_END, write_interval=T_WRITE, nproc=NPROC,
                   probe_arcs_mm=list(PROBE_ARCS), probe_points_mm=[list(map(float, p)) for p in pts],
                   rho=RHO, throat_plane=dict(point_mm=list(map(float, tp)), normal=list(map(float, tn)), box_half_mm=THROAT_BOX_MM),
                   monitors=dict(surface=["inletFlux", "inletPressure"] + [f"{p}{k}" for p in z for k in ("Flux", "Pressure")] + ["throatFlux"],
                                 gate_flux=["inletFlux"] + [f"{p}Flux" for p in z], gate_pressure=[f"{p}Pressure" for p in z],
                                 probes=dict(name="jetProbes", fields=["U", "p"], n=len(pts)))), open(f"{DST}/build_info.json", "w"), indent=1)
    open(f"{DST}/case.foam", "w").close()
    print("built", DST, "from steady time", os.path.basename(tdir), "| probes:", len(pts))

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
