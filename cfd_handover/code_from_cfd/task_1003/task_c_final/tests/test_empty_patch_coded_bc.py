"""Real OpenFOAM test of an outlet patch with ZERO faces (P5 scan 272, out_396; audit P5 Sol finding 1). Serial, niced, temp dir, removed afterwards.
1. blockMesh: a 10 x 1 x 1 mm channel, patches inlet (x = 0), out_1 (x = 10 mm), out_2 (declared with NO faces: nFaces 0, like out_396) and wall.
2. pf_common.write_case (the production writer) builds the resistance case with the audited coded BC on BOTH outlets: the 0-face out_2 keeps its codedFixedValue p / inletOutlet U entries, gets NO
   surfaceFieldValue monitor and no zerod_reference entry; build_info lists it in outlets_lost_in_mesh with the territory bookkeeping.
3. simpleFoam, endTime 2 (test copy only), serially: must end with 'End', no FOAM FATAL; the coded BC of out_2 (res2) must be compiled and constructed on the empty patch.
4. Negative control: the same case with the two monitors the old builder wrote for the empty patch (out_2Flux, out_2Pressure) must stop with a FOAM FATAL error from surfaceFieldValue (v2406: a selected patch
   yielding zero faces is fatal by default), i.e. the omission is what makes the case runnable.
5. Post path on the 2-iteration case: analyze_case.analyse (BC-error criteria over out_1 only; outlets_lost_in_mesh), m1_results.py (M1_outlets row out_2 Q 0 / p N/A / closed 1 / lost_in_mesh 1 / flag OUTLET_LOST_IN_MESH;
   M1_results flags OUTLET_LOST_IN_MESH;NOT_CONVERGED, outlets_lost_in_mesh out_2).
usage: python3 tests/test_empty_patch_coded_bc.py [--keep DIR]"""
import os, sys, re, json, csv, shutil, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE)
sys.path.insert(0, f"{TC}/pf")
import pf_common as C
TEMPLATE = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/code_from_cfd/stageA/caseTemplate_real_lumen_steady"
FOAM = "source /usr/lib/openfoam/openfoam2406/etc/bashrc >/dev/null 2>&1; export OMP_NUM_THREADS=1; "

BLOCKMESH = """FoamFile { version 2.0; format ascii; class dictionary; object blockMeshDict; }
scale 0.001;
vertices ( (0 0 0) (10 0 0) (10 1 0) (0 1 0) (0 0 1) (10 0 1) (10 1 1) (0 1 1) );
blocks ( hex (0 1 2 3 4 5 6 7) (40 6 6) simpleGrading (1 1 1) );
boundary
(
    inlet { type patch; faces ( (0 4 7 3) ); }
    out_1 { type patch; faces ( (1 2 6 5) ); }
    out_2 { type patch; faces ( ); }
    wall  { type wall;  faces ( (0 1 5 4) (3 7 6 2) (0 3 2 1) (4 5 6 7) ); }
);
"""

def sh(cmd, cwd, log):
    r = subprocess.run(["bash", "-c", FOAM + f"nice -n 10 {cmd} > {log} 2>&1"], cwd=cwd)
    return r.returncode, open(os.path.join(cwd, log), errors="replace").read()

def main():
    keep = sys.argv[sys.argv.index("--keep") + 1] if "--keep" in sys.argv else None
    tmp = keep or tempfile.mkdtemp(prefix="emptypatch_")
    try:
        mesh = f"{tmp}/mesh"; os.makedirs(f"{mesh}/system")
        open(f"{mesh}/system/blockMeshDict", "w").write(BLOCKMESH)
        shutil.copy(f"{TEMPLATE}/system/controlDict", f"{mesh}/system/controlDict")
        rc, lg = sh("blockMesh", mesh, "log.blockMesh"); assert rc == 0 and "End" in lg, lg[-1500:]
        bnd = C.read_boundary(f"{mesh}/constant/polyMesh"); print("blockMesh boundary:", bnd)
        assert bnd["out_2"]["nFaces"] == 0 and bnd["out_1"]["nFaces"] == 36
        p0 = 11.319792452830189; R = 1.3e10
        outlets = [dict(patch=p, code_name=f"res{p[-1]}", R=R, R_ref=R, R_own=1e9, G=13.0, relax=C.relax_from_G(R, 1e9)[1], Q_target_m3s=q, p_init_kin=(C.PV + R * q) / C.RHO, tree_node=int(p[-1]), territory_id=f"T{p[-1]}")
                   for p, q in (("out_1", 5e-7), ("out_2", 2e-7))]
        case = f"{tmp}/case"
        b = C.write_case(case, "resistance", f"{mesh}/constant/polyMesh", f"{TEMPLATE}/system", f"{TEMPLATE}/constant", outlets, p0, 1, info=dict(package="stub", instance=dict(scan="stub")),
                         lost_reasons={"out_2": "stub: declared with no faces in blockMeshDict"})
        cd = open(f"{case}/system/controlDict").read(); p0txt = open(f"{case}/0/p").read(); u0 = open(f"{case}/0/U").read(); zr = json.load(open(f"{case}/zerod_reference.json"))
        assert "out_1Flux" in cd and "out_1Pressure" in cd and "out_2" not in cd, "controlDict monitors"
        assert re.search(r"^    out_2\n    \{\n        type            codedFixedValue;", p0txt, re.M) and "name            res2;" in p0txt and "    out_2   { type inletOutlet;" in u0, "out_2 BC entries kept"
        assert list(zr["outlets"]) == ["out_1"], zr
        assert [o["patch"] for o in b["outlets"]] == ["out_1"] and [o["patch"] for o in b["outlets_lost_in_mesh"]] == ["out_2"] and b["outlets_lost_in_mesh"][0]["flag"] == "OUTLET_LOST_IN_MESH"
        bk = b["bc_bookkeeping"]; assert abs(bk["bcC_Q_target_lost_mls"] - 0.2) < 1e-12 and abs(bk["bcC_Q_target_in_mesh_mls"] - 0.5) < 1e-12 and bk["outlets_lost_in_mesh"] == ["out_2"]
        print("build_info outlets_lost_in_mesh:", json.dumps(b["outlets_lost_in_mesh"][0])); print("build_info bc_bookkeeping:", json.dumps(bk))
        # negative control: the old builder's monitors on the empty patch (copy of the case, 1 iteration)
        neg = f"{tmp}/case_old_monitors"; shutil.copytree(case, neg, symlinks=True)
        open(f"{neg}/system/controlDict", "w").write(C.CONTROL_HEAD.replace(f"endTime         {C.END_TIME};", "endTime         1;") + C.monitors(["out_1", "out_2"]) + "}\n")
        rcn, lgn = sh("simpleFoam", neg, "log.simpleFoam")
        fat = lgn[lgn.find("FOAM FATAL"):][:600] if "FOAM FATAL" in lgn else ""
        print(f"NEGATIVE CONTROL (old monitors on the 0-face patch): simpleFoam rc={rcn}; FATAL excerpt:\n{fat}")
        assert rcn != 0 and "FOAM FATAL" in lgn and "out_2" in fat, lgn[-2000:]
        # the fixed case: 2 iterations, serial
        c = open(f"{case}/system/controlDict").read().replace(f"endTime         {C.END_TIME};", "endTime         2;"); open(f"{case}/system/controlDict", "w").write(c)
        rc, lg = sh("simpleFoam", case, "log.simpleFoam")
        tail = "\n".join(lg.strip().splitlines()[-12:])
        assert rc == 0 and re.search(r"^End\s*$", lg, re.M) and "FOAM FATAL" not in lg, lg[-3000:]
        assert re.search(r"^Time = 2$", lg, re.M), "2 iterations"
        assert "res2" in lg and "res1" in lg, "both coded BCs compiled/constructed"       # dynamicCode 'Using dynamicCode for codedFixedValue res2'
        print("simpleFoam (fixed case) rc=0, log tail:\n" + tail)
        print("dynamicCode lines:", [ln.strip() for ln in lg.splitlines() if "dynamicCode" in ln])
        assert sorted(os.listdir(f"{case}/postProcessing")) == sorted(["inletFlux", "inletPressure", "out_1Flux", "out_1Pressure"]), os.listdir(f"{case}/postProcessing")
        q1 = C.series(case, "out_1Flux")[1]; pr1 = C.series(case, "out_1Pressure")[1]; print(f"out_1 flux per iteration {q1.tolist()}, area-average p {pr1.tolist()}")
        # post path
        import analyze_case as AC
        an = AC.analyse(case, f"{case}/analysis_pf.json")
        assert list(an["outlets"]) == ["out_1"] and an["bc_error_criteria_over_outlets"] == ["out_1"] and an["outlets_lost_in_mesh"]["out_2"]["Q_mls"] == 0.0 and an["outlets_lost_in_mesh"]["out_2"]["p_Pa"] == "N/A"
        assert an["bc_bookkeeping"]["outlets_lost_in_mesh"] == ["out_2"]
        out = f"{tmp}/returns"
        r = subprocess.run([sys.executable, f"{TC}/pf/m1_results.py", case, "stub", "resistance", "--analysis", f"{case}/analysis_pf.json", "--outdir", out], capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
        oc = list(csv.DictReader(open(f"{out}/M1_outlets_stub_resistance.csv"))); rr = list(csv.DictReader(open(f"{out}/M1_results.csv")))
        o2 = [x for x in oc if x["outlet_id"] == "out_2"][0]; o1 = [x for x in oc if x["outlet_id"] == "out_1"][0]
        assert o2["Q_mls"] == "0.0" and o2["p_bar_Pa"] == "N/A" and o2["closed"] == "1" and o2["lost_in_mesh"] == "1" and o2["flag"] == "OUTLET_LOST_IN_MESH" and o1["lost_in_mesh"] == "0"
        assert rr[0]["flags"] == "OUTLET_LOST_IN_MESH;NOT_CONVERGED" and rr[0]["outlets_lost_in_mesh"] == "out_2" and "territory closed" in rr[0]["notes"], rr[0]
        print("M1_outlets rows:"); [print("  ", {k: x[k] for k in ("outlet_id", "Q_mls", "Q_target_bcC_mls", "p_bar_Pa", "closed", "lost_in_mesh", "flag", "R_source")}) for x in oc]
        print("M1_results flags:", rr[0]["flags"], "| outlets_lost_in_mesh:", rr[0]["outlets_lost_in_mesh"], "| converged:", rr[0]["converged"])
        print("PASS: 0-face outlet patch: coded BC accepted on the empty patch (2 serial simpleFoam iterations, End), its monitors omitted (they are fatal: negative control), post path reports Q 0 / p N/A / OUTLET_LOST_IN_MESH")
    finally:
        if not keep: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
