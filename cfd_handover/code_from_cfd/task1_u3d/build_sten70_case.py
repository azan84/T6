"""Build case_<level> of the U3D family from mesh_<level>: sten70 BCs of the Stage A ladder (inlet totalPressure 11.3198, outlet coded resistance R = 6.974826e9 Pa s/m3, Pv 666.61 Pa, relax 0.20,
initial 8.0694), the audited stageA caseTemplate numerics (A5_sten70_fine/system, fvSchemes/fvSolution unchanged), fixed iteration budget endTime 3000 (the value asserted by run_set.sh), monitors as in the earlier ladder
(inlet/outlet flux, outlet-patch and inlet-patch pressure, measurement plane x = 56.5 mm areaAverage p) plus the throat plane x = 31.503 mm (3 um past the throat centre: 31.5 mm is a cell-face plane) flux and pressure. polyMesh is HARD-LINKED from the mesh directory (same filesystem, no extra disk, never modified).
usage: build_sten70_case.py <level> [nproc=16]     Refuses to overwrite a case that holds run output."""
import sys, os, re, shutil, json, subprocess
U = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(U); TEMPLATE = f"{P}/../A5_sten70_fine"
R_SI, PV, RHO, RELAX, P_INIT, P_AORTA_KIN = 6.974826e9, 666.61, 1060.0, 0.2, 8.0694, 11.3198
END = int(os.environ.get("U3D_END", "3000"))      # fixed per-level budget (design v2.4); the launcher must be told with RUN_SET_END_MAP when it is not 3000
P_TXT = """FoamFile { version 2.0; format ascii; class volScalarField; object p; }
dimensions      [0 2 -2 0 0 0 0];
internalField   uniform %(pi)s;

boundaryField
{
    inlet   { type totalPressure; p0 uniform %(pa)s; value uniform %(pa)s; }
    wall    { type zeroGradient; }

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
def fo(name, patch=None, op=None, fld=None, plane=None):
    hd = f"    {name}\n    {{\n        type surfaceFieldValue; libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log true;\n"
    if plane is None: return hd + f"        regionType patch; name {patch}; operation {op}; fields ({fld});\n    }}\n"
    return hd + (f"        regionType sampledSurface; name {name}Plane;\n        sampledSurfaceDict\n        {{\n            type plane; planeType pointAndNormal;\n            pointAndNormalDict {{ point ({plane:.6f} 0 0); normal (1 0 0); }}\n            interpolate false;\n        }}\n"
                 f"        operation {op}; fields ({fld});\n    }}\n")
def main(level, nproc=16):
    mesh, case = f"{U}/mesh_{level}", f"{U}/case_{level}"
    if not os.path.exists(f"{mesh}/mesh_gates.json") or not json.load(open(f"{mesh}/mesh_gates.json"))["GATES_PASS"]: raise SystemExit(f"{mesh}: mesh gates missing or failed")
    if os.path.exists(case):
        done = [d for d in os.listdir(case) if (re.match(r"^[-+.0-9eE]+$", d) and d != "0") or d.startswith("processor") or d in ("log.simpleFoam", "log.smoke", "postProcessing", "dynamicCode")]
        if done: raise SystemExit(f"refusing to overwrite {case}: run output {done[:4]}")
        shutil.rmtree(case)
    os.makedirs(f"{case}/constant"); os.makedirs(f"{case}/system"); os.makedirs(f"{case}/0")
    subprocess.run(["cp", "-al", f"{mesh}/constant/polyMesh", f"{case}/constant/polyMesh"], check=True)
    shutil.rmtree(f"{case}/constant/polyMesh/sets", ignore_errors=True)
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{TEMPLATE}/constant/{f}", f"{case}/constant/{f}")
    for f in ("fvSchemes", "fvSolution"): shutil.copy(f"{TEMPLATE}/system/{f}", f"{case}/system/{f}")
    shutil.copy(f"{TEMPLATE}/0/U", f"{case}/0/U")
    open(f"{case}/0/p", "w").write(P_TXT % dict(pi=P_INIT, pa=P_AORTA_KIN, R=R_SI, Pv=PV, rho=RHO, relax=RELAX))
    open(f"{case}/system/decomposeParDict", "w").write(f"FoamFile {{ version 2.0; format ascii; class dictionary; object decomposeParDict; }}\nnumberOfSubdomains {nproc};\nmethod scotch;\n")
    fns = fo("inletFlux", "inlet", "sum", "phi") + fo("outletFlux", "outlet", "sum", "phi") + fo("outletPressure", "outlet", "areaAverage", "p") + fo("inletPressure", "inlet", "areaAverage", "p") + fo("measurementP", op="areaAverage", fld="p", plane=0.0565) + \
          fo("throatFlux", op="areaNormalIntegrate", fld="U", plane=0.031503) + fo("throatP", op="areaAverage", fld="p", plane=0.031503)
    open(f"{case}/system/controlDict", "w").write("FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }\n"
        f"application     simpleFoam;\nstartFrom       startTime;\nstartTime       0;\nstopAt          endTime;\nendTime         {END};\ndeltaT          1;\nwriteControl    timeStep;\nwriteInterval   250;\npurgeWrite      2;\nwriteFormat     binary;\n"
        "writePrecision  8;\nwriteCompression off;\ntimeFormat      general;\ntimePrecision   8;\nrunTimeModifiable true;\n\nfunctions\n{\n" + fns + "}\n")
    # minimal 'zerod_reference.json' so that analyze_solve.py (BC accuracy = p_outlet vs Pv + R Q, convergence bands, --strict) works unchanged: single outlet 'outlet', no 0D prediction
    json.dump(dict(case=f"sten70_{level}", Q_demand_mls=None, outlets={"outlet": dict(R_out=R_SI, relax=RELAX, Q0_mls=None)}), open(f"{case}/zerod_reference.json", "w"), indent=1)
    open(f"{case}/case.foam", "w").close()
    json.dump(dict(level=level, mesh=os.path.basename(mesh), endTime=END, R_SI=R_SI, relax=RELAX, nproc=nproc, mesh_gates=json.load(open(f"{mesh}/mesh_gates.json"))), open(f"{case}/build_info.json", "w"), indent=1)
    print("built", case)
if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 16)
