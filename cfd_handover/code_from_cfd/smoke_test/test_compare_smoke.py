"""fix26 tests of compare_smoke.py (branch-aware verdict, schema-2 reference, --write-reference governance). usage: python3 test_compare_smoke.py   (no network, no OpenFOAM)
Synthetic work dirs: monitors 1..3000, log.simpleFoam with 'Time =' lines and 'End', controlDict, smoke_checks.json and the retained mesh files the re-verification reads (a dummy STL whose
sha256 replaces compare_smoke.STL_SHA256 for the in-process synthetic tests; boundary, log.checkMesh, points, log.decomposePar, decomposeParDict). The real smoke_ref run is checked in a
subprocess with nothing patched (read-only). The shipped reference_result.json is only read; the in-process tests use temp copies whose stl_sha256 is the dummy hash (load_reference checks
it against the patched constant; fix26 attempt 2) and write tests write only into temp copies.
fix26 attempt 2: combined Q-and-FFR branch identification (audit SOL 1), common-field validation of the reference (SOL 3 / AGY 4), preflight of run_smoke_test.sh's WRITE_REFERENCE /
SMOKE_REPLACE_BRANCH governance in a temp copy of the script (exits before OpenFOAM is sourced: FOAM_BASHRC points nowhere; SOL 4 / AGY 2, 3), temp directory from TMPDIR (tempfile) with a
fallback next to this file when the system temp is not writable (SOL: read-only sandbox).
fix26 attempt 3: shell preflight refuses a reference lacking a branch in compare mode (AGY R2-2); if neither the system temp nor the fallback is writable, one clear message and exit (SOL R2-1)."""
import os, sys, io, json, shutil, hashlib, tempfile, subprocess, contextlib, unittest
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.dont_write_bytecode = True
import compare_smoke as cs
REF = os.path.join(HERE, "reference_result.json"); SMOKE_REF = "/home/azan/paper6_t6_work/smoke_ref"
P_OF_FFR = lambda f: f * cs.P_AORTA / cs.RHO
DEFL = dict(q=1.17390297e-06, pm=8.87434)              # a5_arch8 re-run on the archived mesh
SYMM = dict(q=1.17825059e-06, pm=8.85754493)           # smoke_ref
BOUNDARY = "3\n(\nwall\n{\n    type wall;\n    nFaces 1;\n    startFace 0;\n}\ninlet\n{\n    type patch;\n    nFaces 1;\n    startFace 1;\n}\noutlet\n{\n    type patch;\n    nFaces 1;\n    startFace 2;\n}\n)\n"
def make_run(root, name, q, pm, n=cs.N_ITER, end=True, drift_pct=0.0, cells=cs.CELLS_A5):
    """synthetic work dir: Q and p_meas approach their final values (decaying transient), plus a linear drift of drift_pct % over the last 200 iterations"""
    d = os.path.join(root, name); it = np.arange(1, n + 1, dtype=float)
    tr = np.exp(-it / 300.0); dr = np.where(it > n - 200, (it - (n - 200)) / 200.0 * drift_pct / 100, 0.0) - (drift_pct / 100 if drift_pct else 0.0)
    cols = dict(outletFlux=q * (1 + 0.05 * tr + dr), measurementP=pm * (1 + 0.05 * tr + dr), outletPatchP=8.37 * (1 + 0.05 * tr))
    for k, v in cols.items():
        os.makedirs(f"{d}/postProcessing/{k}/0"); np.savetxt(f"{d}/postProcessing/{k}/0/surfaceFieldValue.dat", np.c_[it, v], fmt=["%d", "%.8e"], header="Time value", comments="# ")
    with open(f"{d}/log.simpleFoam", "w") as f:
        for i in range(1, n + 1): f.write(f"Time = {i}\n\nExecutionTime = {i * 0.1:.2f} s  ClockTime = {i // 10} s\n\n")
        if end: f.write("End\n")
    os.makedirs(f"{d}/system"); open(f"{d}/system/controlDict", "w").write(f"endTime         {cs.N_ITER};\n")
    open(f"{d}/system/decomposeParDict", "w").write("numberOfSubdomains  8;\nmethod              scotch;\n")
    os.makedirs(f"{d}/constant/triSurface"); os.makedirs(f"{d}/constant/polyMesh")
    open(f"{d}/constant/triSurface/sten70.stl", "w").write("solid dummy\nendsolid dummy\n"); open(f"{d}/constant/polyMesh/boundary", "w").write(BOUNDARY)
    open(f"{d}/constant/polyMesh/points", "w").write(f"(0 0 0) {name}\n")
    open(f"{d}/log.checkMesh", "w").write(f"    cells:            {cells}\n\nMesh OK.\n\nEnd\n")
    open(f"{d}/log.decomposePar", "w").write("".join(f"Processor {i}\n    Number of processor faces = 700\n" for i in range(8)) + "\nNumber of processor faces = 2899\n")
    json.dump(dict(stl_sha256=DUMMY_SHA, checkMesh_ok=True, cells=cells, inlet_rewrites=1, outlet_rewrites=1, omp_num_threads="8"), open(f"{d}/smoke_checks.json", "w"))
    return d
DUMMY_SHA = hashlib.sha256(b"solid dummy\nendsolid dummy\n").hexdigest()
def run(*argv):
    """in-process compare_smoke.main with the dummy STL hash: (exit code, stdout)"""
    o, keep = io.StringIO(), cs.STL_SHA256; cs.STL_SHA256 = DUMMY_SHA
    try:
        with contextlib.redirect_stdout(o): rc = cs.main(["compare_smoke.py", *argv])
    finally: cs.STL_SHA256 = keep
    return rc, o.getvalue()
def lref(path):
    """cs.load_reference with the dummy STL hash"""
    keep = cs.STL_SHA256; cs.STL_SHA256 = DUMMY_SHA
    try: return cs.load_reference(path)
    finally: cs.STL_SHA256 = keep
def mktmp():
    """temp dir from TMPDIR/TEMP/TMP//tmp (tempfile); if none is writable, next to this file (never the shipped reference itself); if that is not writable either, the module
    stops at once with one message naming the directories tried (fix26 attempt 3, audit SOL R2-1: no raw OSError traceback in setUpClass; nothing is skipped)"""
    try: return tempfile.mkdtemp(prefix="fix26_test_")
    except OSError as e1:
        try: return tempfile.mkdtemp(prefix="fix26_test_", dir=HERE)
        except OSError as e2:
            tried = [tempfile.tempdir] if tempfile.tempdir else getattr(tempfile, "_candidate_tempdir_list", lambda: [os.environ.get(v) for v in ("TMPDIR", "TEMP", "TMP")] + ["/tmp", "/var/tmp", "/usr/tmp", os.getcwd()])()
            sys.exit(f"test_compare_smoke.py: no writable temporary directory, 0 tests run. Tried the system temp {[d for d in tried if d]} ({e1.strerror or e1}) and the fallback {HERE} ({e2.strerror or e2}). "
                     "Set TMPDIR to a writable directory, e.g. TMPDIR=/path/to/writable/dir python3 test_compare_smoke.py")
class T(unittest.TestCase):
    @classmethod
    def setUpClass(c):
        c.tmp = mktmp(); c.ref_sha = hashlib.sha256(open(REF, "rb").read()).hexdigest()
        c.dref = os.path.join(c.tmp, "ref_dummy_stl.json"); j = json.load(open(REF)); j["stl_sha256"] = DUMMY_SHA; json.dump(j, open(c.dref, "w"), indent=1)
    @classmethod
    def tearDownClass(c):
        shutil.rmtree(c.tmp); assert hashlib.sha256(open(REF, "rb").read()).hexdigest() == c.ref_sha, "shipped reference_result.json was modified"
    def ref_copy(self, name, **common):
        """temp copy of the shipped reference with the dummy STL hash (and common fields overridden; None deletes)"""
        p = os.path.join(self.tmp, name); j = json.load(open(self.dref))
        for k, v in common.items():
            if v is None: j.pop(k)
            else: j[k] = v
        json.dump(j, open(p, "w"), indent=1); return p
    def test_deflected_pass(self):
        rc, o = run(make_run(self.tmp, "defl", **DEFL), self.dref); self.assertEqual(rc, 0, o); self.assertIn("SMOKE TEST PASS (deflected-jet branch = the returned A5 coarse value)", o)
    def test_symmetric_pass(self):
        rc, o = run(make_run(self.tmp, "symm", **SYMM), self.dref); self.assertEqual(rc, 0, o); self.assertIn("SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)", o)
    def test_between_branches_fail(self):
        rc, o = run(make_run(self.tmp, "betw", q=1.1761e-06, pm=P_OF_FFR(0.7832)), self.dref)
        self.assertEqual(rc, 1, o); self.assertIn("in no branch window", o); self.assertIn("vs deflected branch", o); self.assertIn("vs symmetric branch", o); self.assertIn("SMOKE TEST FAIL", o)
    def test_q_in_window_ffr_out_fail(self):
        rc, o = run(make_run(self.tmp, "qffr", q=SYMM["q"], pm=DEFL["pm"]), self.dref); self.assertEqual(rc, 1, o); self.assertIn("in the symmetric window but FFR_x56p5", o)
    def test_unstable_window_fail(self):
        rc, o = run(make_run(self.tmp, "drift", **DEFL, drift_pct=0.03), self.dref)   # Q and FFR still inside the deflected window, but drifting 0.03 % over the last 200 iterations
        self.assertEqual(rc, 1, o); self.assertIn("unstable final window: Q band", o); self.assertNotIn("PASS", o)
    def test_incomplete_run_3(self):
        rc, o = run(make_run(self.tmp, "noend", **DEFL, end=False), self.dref); self.assertEqual(rc, 3, o); self.assertIn("no exact line 'End'", o)
        rc, o = run(make_run(self.tmp, "short", **DEFL, n=2999), self.dref); self.assertEqual(rc, 3, o)
    def test_other_cell_count_3(self):
        rc, o = run(make_run(self.tmp, "cells", **DEFL, cells=198250), self.dref); self.assertEqual(rc, 3, o); self.assertIn("different cell count", o)
    def test_write_reference_replacement(self):
        d, r = make_run(self.tmp, "wdefl", **DEFL), self.ref_copy("ref_w.json"); before = json.load(open(r))
        rc, o = run(d, r, "--write-reference", r); self.assertEqual(rc, 2, o); self.assertIn("pass --replace-branch deflected", o); self.assertEqual(json.load(open(r)), before)
        rc, o = run(d, r, "--write-reference", r, "--replace-branch", "symmetric"); self.assertEqual(rc, 2, o); self.assertEqual(json.load(open(r)), before)
        rc, o = run(d, r, "--wall", "300", "--write-reference", r, "--replace-branch", "deflected"); self.assertEqual(rc, 0, o)
        after = json.load(open(r)); self.assertEqual(after["branches"]["symmetric"], before["branches"]["symmetric"])
        e = after["branches"]["deflected"]; self.assertAlmostEqual(e["Q_out_m3s"], DEFL["q"], delta=1e-11)   # final value incl. the decayed transient (2e-6 relative)
        pv = e["provenance"]; self.assertEqual(pv["processor_faces"], 2899); self.assertEqual(pv["nprocs"], 8); self.assertEqual(pv["decomposition_method"], "scotch")
        self.assertEqual(pv["mesh_points_sha256"], hashlib.sha256(open(f"{d}/constant/polyMesh/points", "rb").read()).hexdigest()); self.assertEqual(pv["wall_clock_total_s"], 300)
        rc, o = run(make_run(self.tmp, "symm2", **SYMM), r); self.assertEqual(rc, 0, o)     # the rewritten reference is still a valid compare reference
    def test_write_reference_refuses_off_branch_and_unstable(self):
        r = self.ref_copy("ref_off.json"); before = open(r).read()
        rc, o = run(make_run(self.tmp, "woff", q=1.1761e-06, pm=P_OF_FFR(0.7832)), r, "--write-reference", r, "--replace-branch", "deflected"); self.assertEqual(rc, 1, o)
        rc, o = run(make_run(self.tmp, "wdrift", **DEFL, drift_pct=0.03), r, "--write-reference", r, "--replace-branch", "deflected"); self.assertEqual(rc, 1, o)
        self.assertEqual(open(r).read(), before)
    def test_write_reference_new_file(self):
        r = os.path.join(self.tmp, "new_ref.json"); rc, o = run(make_run(self.tmp, "wnew", **SYMM), r, "--write-reference", r); self.assertEqual(rc, 0, o)
        j = json.load(open(r)); self.assertEqual(j["schema"], 2); self.assertEqual(list(j["branches"]), ["symmetric"])
        rc, o = run(make_run(self.tmp, "wnew2", **SYMM), r); self.assertEqual(rc, 2, o); self.assertIn("lacks the deflected branch", o)
    def test_schema1_reference_clear_error(self):
        r = os.path.join(self.tmp, "schema1.json")
        json.dump(dict(iterations=3000, finished=True, Q_out_m3s=1.17825059e-06, FFR_x56p5=0.78248298, cells=198252, returned_value_stageA_A5_ladders_Q_out_m3s=1.17392231e-06), open(r, "w"))
        d = make_run(self.tmp, "s1", **SYMM)
        rc, o = run(d, r); self.assertEqual(rc, 2, o); self.assertIn("not schema 2", o)
        rc, o = run(d, r, "--write-reference", r); self.assertEqual(rc, 2, o); self.assertIn("not schema 2", o)
    def test_reference_cannot_redefine_branch(self):
        r = self.ref_copy("ref_bad.json"); j = json.load(open(r)); j["branches"]["deflected"]["Q_out_m3s"] = 1.1761e-06; json.dump(j, open(r, "w"))
        rc, o = run(make_run(self.tmp, "redef", q=1.1761e-06, pm=DEFL["pm"]), r); self.assertEqual(rc, 2, o); self.assertIn("outside the window of its constant", o)
    def test_overlapping_q_windows_ffr_separates_pass(self):
        # audit SOL 1: reference Q values moved within their allowed 0.1 % towards each other -> Q windows overlap; FFR identifies the branch
        r = self.ref_copy("ref_overlap.json"); j = json.load(open(r))
        j["branches"]["deflected"]["Q_out_m3s"] = cs.BRANCHES["deflected"]["Q_out_m3s"] * 1.00099; j["branches"]["symmetric"]["Q_out_m3s"] = cs.BRANCHES["symmetric"]["Q_out_m3s"] * 0.99901
        json.dump(j, open(r, "w")); self.assertIsNone(lref(r)[1])
        q = 1.17608e-06   # inside both Q windows
        for k in ("deflected", "symmetric"): self.assertTrue(cs.in_window(dict(Q_out_m3s=q, FFR_x56p5=0), j["branches"][k])[0])
        rc, o = run(make_run(self.tmp, "ovl_d", q=q, pm=P_OF_FFR(cs.BRANCHES["deflected"]["FFR_x56p5"])), r); self.assertEqual(rc, 0, o); self.assertIn("SMOKE TEST PASS (deflected-jet branch", o)
        rc, o = run(make_run(self.tmp, "ovl_s", q=q, pm=P_OF_FFR(cs.BRANCHES["symmetric"]["FFR_x56p5"])), r); self.assertEqual(rc, 0, o); self.assertIn("SMOKE TEST PASS (symmetric-jet branch", o)
        rc, o = run(make_run(self.tmp, "ovl_x", q=q, pm=P_OF_FFR(0.7832)), r); self.assertEqual(rc, 1, o)   # Q in both windows, FFR in neither
        self.assertIn("in the deflected window but FFR_x56p5", o); self.assertIn("in the symmetric window but FFR_x56p5", o)
    def test_two_branches_both_in_window_ambiguous_fail(self):
        # Q and FFR entries both moved to the edge of their constants' windows: a run can be in both combined windows -> FAIL (ambiguous)
        r = self.ref_copy("ref_ambig.json"); j = json.load(open(r)); d, sy = j["branches"]["deflected"], j["branches"]["symmetric"]
        d["Q_out_m3s"] = cs.BRANCHES["deflected"]["Q_out_m3s"] * 1.00099; sy["Q_out_m3s"] = cs.BRANCHES["symmetric"]["Q_out_m3s"] * 0.99901
        d["FFR_x56p5"] = cs.BRANCHES["deflected"]["FFR_x56p5"] - 0.00049; sy["FFR_x56p5"] = cs.BRANCHES["symmetric"]["FFR_x56p5"] + 0.00049
        json.dump(j, open(r, "w")); self.assertIsNone(lref(r)[1])
        rc, o = run(make_run(self.tmp, "ambig", q=1.17608e-06, pm=P_OF_FFR(0.78322)), r); self.assertEqual(rc, 1, o); self.assertIn("ambiguous", o); self.assertNotIn("PASS", o)
    def test_reference_common_fields_validated(self):
        d = make_run(self.tmp, "common", **SYMM)
        for name, kw, msg in (("c_cells", dict(cells=999), "'cells' = 999"), ("c_cells_missing", dict(cells=None), "'cells' missing"),
                              ("c_stl", dict(stl_sha256="0" * 64), "'stl_sha256'"), ("c_niter", dict(n_iter=2000), "'n_iter' = 2000"),
                              ("c_ret", dict(returned_value_stageA_A5_ladders_Q_out_m3s=1.1739e-06), "'returned_value_stageA_A5_ladders_Q_out_m3s'"),
                              ("c_ret_missing", dict(returned_value_stageA_A5_ladders_Q_out_m3s=None), "missing"), ("c_schema", dict(schema=3), "not schema 2")):
            r = self.ref_copy(name + ".json", **kw); before = open(r).read()
            rc, o = run(d, r); self.assertEqual(rc, 2, (name, o)); self.assertIn(msg, o, name)
            rc, o = run(d, r, "--write-reference", r, "--replace-branch", "symmetric"); self.assertEqual(rc, 2, (name, o)); self.assertIn(msg, o, name); self.assertEqual(open(r).read(), before)
    def shell(self, name, ref=None, **env):
        """temp copy of run_smoke_test.sh + compare_smoke.py + reference + controlDict; FOAM_BASHRC points nowhere, so the script can never get past the preflight: (rc, output)"""
        d = os.path.join(self.tmp, "sh_" + name); os.makedirs(f"{d}/case_files/system")
        for f in ("run_smoke_test.sh", "compare_smoke.py"): shutil.copy(os.path.join(HERE, f), d)
        shutil.copy(os.path.join(HERE, "case_files/system/controlDict"), f"{d}/case_files/system/"); shutil.copy(ref or REF, f"{d}/reference_result.json")
        open(f"{d}/gen.py", "w").write("raise SystemExit(99)\n")
        e = {k: v for k, v in os.environ.items() if k not in ("WRITE_REFERENCE", "SMOKE_REPLACE_BRANCH")}
        e.update(GEN=f"{d}/gen.py", FOAM_BASHRC=f"{d}/no_such_bashrc", PYTHONDONTWRITEBYTECODE="1", **env)
        p = subprocess.run(["bash", f"{d}/run_smoke_test.sh", "8", f"{d}/work"], capture_output=True, text=True, env=e, timeout=60)
        self.assertFalse(os.path.exists(f"{d}/work")); self.assertEqual(open(f"{d}/reference_result.json", "rb").read(), open(ref or REF, "rb").read())
        return p.returncode, p.stdout + p.stderr
    def test_shell_preflight_reference_governance(self):
        rc, o = self.shell("both"); self.assertEqual(rc, 2, o); self.assertIn("OpenFOAM v2406 bashrc not found", o)   # plain compare passes governance
        rc, o = self.shell("wr_both", WRITE_REFERENCE="1"); self.assertEqual(rc, 2, o); self.assertIn("already holds both branch entries (deflected, symmetric)", o); self.assertNotIn("bashrc not found", o)
        rc, o = self.shell("wr_bad", WRITE_REFERENCE="1", SMOKE_REPLACE_BRANCH="foo"); self.assertEqual(rc, 2, o); self.assertIn("must be deflected or symmetric", o); self.assertNotIn("bashrc not found", o)
        rc, o = self.shell("rb_only", SMOKE_REPLACE_BRANCH="deflected"); self.assertEqual(rc, 2, o); self.assertIn("only valid with WRITE_REFERENCE=1", o)
        rc, o = self.shell("wr_repl", WRITE_REFERENCE="1", SMOKE_REPLACE_BRANCH="deflected"); self.assertEqual(rc, 2, o)
        self.assertIn("Step 6 replaces the deflected entry IF the run lands on the deflected branch", o); self.assertIn("bashrc not found", o)   # governance passed, stopped at the OpenFOAM check
        one = os.path.join(self.tmp, "ref_one.json"); j = json.load(open(REF)); del j["branches"]["deflected"]; json.dump(j, open(one, "w"), indent=1)
        rc, o = self.shell("wr_one", ref=one, WRITE_REFERENCE="1"); self.assertEqual(rc, 2, o); self.assertIn("entries in", o); self.assertIn("symmetric. Step 6 adds this run", o); self.assertIn("bashrc not found", o)
        rc, o = self.shell("cmp_one", ref=one); self.assertEqual(rc, 2, o); self.assertIn("compare mode needs both branch entries (deflected, symmetric)", o); self.assertIn("it holds: symmetric.", o); self.assertNotIn("bashrc not found", o)   # fix26 attempt 3 (AGY R2-2)
        none = os.path.join(self.tmp, "ref_none.json"); j = json.load(open(REF)); j["branches"] = {}; json.dump(j, open(none, "w"), indent=1)
        rc, o = self.shell("cmp_none", ref=none); self.assertEqual(rc, 2, o); self.assertIn("compare mode needs both branch entries", o); self.assertNotIn("bashrc not found", o)
        s1 = os.path.join(self.tmp, "ref_s1.json"); json.dump(dict(Q_out_m3s=1.17825059e-06, cells=198252), open(s1, "w"))
        rc, o = self.shell("s1", ref=s1); self.assertEqual(rc, 2, o); self.assertIn("preflight: reference", o); self.assertIn("not schema 2", o); self.assertNotIn("bashrc not found", o)
    def test_shipped_reference_consistent(self):
        r, err = cs.load_reference(REF); self.assertIsNone(err); self.assertEqual(set(r["branches"]), {"deflected", "symmetric"}); self.assertEqual(r["cells"], cs.CELLS_A5)
        self.assertEqual(r["stl_sha256"], cs.STL_SHA256); self.assertEqual(r["n_iter"], cs.N_ITER); self.assertEqual(r["returned_value_stageA_A5_ladders_Q_out_m3s"], cs.RETURNED_Q)
    @unittest.skipUnless(os.path.isdir(SMOKE_REF), "real smoke_ref not present")
    def test_real_smoke_ref_symmetric(self):
        p = subprocess.run([sys.executable, "-B", os.path.join(HERE, "compare_smoke.py"), SMOKE_REF, REF, "--wall", "318"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr); self.assertIn("SMOKE TEST PASS (symmetric-jet branch; not the returned value, see SETUP.md section 4)", p.stdout)
if __name__ == "__main__":
    unittest.main(verbosity=2, warnings="ignore")   # ResourceWarnings of the open(...).read() idiom (files are read-only, closed by refcount) are not shown
