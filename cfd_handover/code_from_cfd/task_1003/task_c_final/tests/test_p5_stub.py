"""Case-file build (no mesh) for every P5 package with the Task C template: a stub polyMesh (boundary with inlet, wall and the package outlet_ids; empty owner) per package, build_m1_case.build(..., 'resistance',
mesh_check=False) into a temp dir, then: patches/BC blocks per outlet, bounded throat + measurement planes in controlDict (foamDictionary parses it), probe boxes sized from the centreline, NOT_FOR_PRODUCTION marker,
E0 MEMBER, strict measurement-section rule (473 relocated, others PASS). Also checks that the builder REFUSES a mesh whose patch list does not match the package. usage: python3 test_p5_stub.py [pkg_root]"""
import os, sys, json, re, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE); PILOT = os.path.dirname(TC)
sys.path[:0] = [f"{TC}/pf", f"{PILOT}/pf"]
import build_m1_case as B
import m1_package as M
ROOT = sys.argv[1] if len(sys.argv) > 1 else "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5"
FOAM = "source /usr/lib/openfoam/openfoam2406/etc/bashrc >/dev/null 2>&1; "

def stub_mesh(d, patches):
    os.makedirs(f"{d}/constant/polyMesh")
    body = "".join(f"{p}\n{{\n    type {'wall' if p == 'wall' else 'patch'};\n    nFaces 10;\n    startFace {100 + 10 * i};\n}}\n" for i, p in enumerate(patches))
    open(f"{d}/constant/polyMesh/boundary", "w").write("FoamFile { version 2.0; format ascii; class polyBoundaryMesh; object boundary; }\n\n" + f"{len(patches)}\n(\n{body})\n")
    open(f"{d}/constant/polyMesh/owner", "w").write("")

def main():
    tmp = tempfile.mkdtemp(prefix="p5stub_"); res = {}
    try:
        for name in sorted(os.listdir(ROOT)):
            pkg = M.load_package(name, ROOT); ids = [o["outlet_id"] for o in pkg["outlets"]]
            mesh = f"{tmp}/mesh_{name}"; stub_mesh(mesh, ["inlet"] + ids + ["wall"]); out = f"{tmp}/case_{name}"
            b = B.build(name, mesh, "resistance", out, 16, ROOT, mesh_check=False)
            cd = open(f"{out}/system/controlDict").read(); p0 = open(f"{out}/0/p").read(); u0 = open(f"{out}/0/U").read()
            assert [o["patch"] for o in b["outlets"]] == ids and b["closed_patches"] == []
            for i in ids: assert re.search(rf"^    {i}\n    {{\n        type            codedFixedValue;", p0, re.M) and f"    {i}   {{ type inletOutlet;" in u0, i
            for m in ("throatP", "throatFlux", "measurementP", "measurementFlux"): assert f"    {m}\n" in cd, m
            assert cd.count("bounds (") == 4 and cd.count("writeArea true;") == 4
            assert os.path.exists(f"{out}/NOT_FOR_PRODUCTION") and b["production_ready"] is False and b["e0_guard"]["status"] == "MEMBER"
            r = subprocess.run(["bash", "-c", FOAM + f"foamDictionary -entry functions -keywords {out}/system/controlDict"], capture_output=True, text=True)
            assert r.returncode == 0 and "measurementP" in r.stdout.split(), r.stderr[-500:]
            r2 = subprocess.run(["bash", "-c", FOAM + f"foamDictionary -entry functions/measurementP/sampledSurfaceDict/bounds {out}/system/controlDict"], capture_output=True, text=True)
            assert r2.returncode == 0 and r2.stdout.strip().startswith("bounds"), r2.stdout + r2.stderr[-300:]
            psc = b["probe_section_check"]
            # strict single-lumen measurement-section rule (no mesh: S1/S2 only): 473 must be FAILED_SECTION_RULE + relocated (no original monitor without a mesh), the other four PASS on the package probe
            if name.startswith("473_"):
                assert b["measurement_section_rule"]["status"] == "FAILED_SECTION_RULE" and b["measurement_probe_used"] == "p011_reloc" and b["measurement_probe_relocated"]["relocated"]["tree_node"] == 646, b["measurement_section_rule"]
                assert "measurementOrigP" not in cd and b["measurement_probe_relocated"]["original"]["original_monitor"] is None
            else: assert b["measurement_section_rule"]["status"] == "PASS" and b["measurement_probe_used"] == b["measurement_probe"] and b["measurement_probe_relocated"] is None
            res[name] = dict(outlets=ids, section_rule=b["measurement_section_rule"]["status"], measurement=(psc["measurement"]["probe_id"], round(psc["measurement"]["h_final_mm"], 3), psc["measurement"]["sizing"]["n_other_crossings_infinite_plane"]),
                             throat=(psc["throat"]["probe_id"], round(psc["throat"]["h_final_mm"], 3), psc["throat"]["sizing"]["n_other_crossings_infinite_plane"]), relax=[round(o["relax"], 5) for o in b["outlets"]],
                             extension_source=b["extension_source"])
            # a mesh that does not carry the package's outlet patches must be refused
            bad = f"{tmp}/bad_{name}"; stub_mesh(bad, ["inlet", "out_999", "wall"])
            try: B.build(name, bad, "resistance", f"{tmp}/badcase_{name}", 16, ROOT, mesh_check=False); raise AssertionError("mismatched mesh accepted")
            except SystemExit as e: assert "mesh patches" in str(e), e
        for k, v in res.items(): print(k, json.dumps(v))
        print(f"PASS: {len(res)} P5 packages built (case files, stub mesh)")
    finally: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
