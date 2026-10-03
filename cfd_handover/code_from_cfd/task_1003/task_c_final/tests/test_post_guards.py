"""Solver-free tests of the attempt-3 guards of post_case_generic.sh (audit round 2, ../audit_AC/SOL_C2.md findings 1, 3, 4):
(1) package resolution (m1_package.resolve_pkg_root / resolve_pkg_dir): explicit root only when given, else Drive packages/M1, packages/P5, then the persistent zipcheck copy; no /tmp root; and
    post_helpers.package_check: a copy of a real package verifies against the hashes recorded at build time, a tampered / missing / extra file or a missing record is refused;
(3) post_helpers.run_completion on synthetic log.simpleFoam tails: a complete run, no End, End followed by an appended run (complete header + partial Time lines, or only a header), End before the last Time,
    an early stop (last Time != endTime), a restart whose LAST run completed (accepted), CRLF line ends, a FOAM FATAL after End; and analyze_case --require-finished is passed by the runner;
(4) post_helpers.radius_check / radius_commit: no provenance -> regenerate; committed provenance -> reuse; changed mesh file, changed package hash, edited radius file -> regenerate.
usage: python3 -B tests/test_post_guards.py"""
import os, sys, json, shutil, tempfile, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE); sys.path.insert(0, f"{TC}/pf")
import m1_package as M
import post_helpers as H

S14 = "14_left_LAD_prox_20mm_80ds__baseline__real"; P473 = "473_left_LCX_prox_20mm_60ds__baseline__real"

def head(n=1):
    return "".join(f"/*---*/\nBuild  : v2406\nExec   : simpleFoam -parallel\nCreate time\n\nStarting time loop\n\n" for _ in range(n))

def iters(a, b):
    return "".join(f"Time = {i}\n\nsmoothSolver: Solving for Ux\nExecutionTime = {i * 0.1:.1f} s  ClockTime = {i} s\n\n" for i in range(a, b + 1))

END = "End\n\nFinalising parallel run\n"

def case_with_log(root, name, text, end_time=50):
    d = f"{root}/{name}"; os.makedirs(f"{d}/system", exist_ok=True)
    open(f"{d}/system/controlDict", "w").write(f"application simpleFoam;\nstartFrom latestTime;\nendTime         {end_time};\nwriteInterval 50;\n")
    open(f"{d}/log.simpleFoam", "w", newline="").write(text); return d

def test_completion(tmp):
    cases = {
        "complete": (head() + iters(1, 50) + END, True),
        "no_end": (head() + iters(1, 37), False),
        "appended_partial_run": (head() + iters(1, 50) + END + head() + iters(51, 60), False),
        "appended_header_only": (head() + iters(1, 50) + END + "/*---*/\nBuild  : v2406\nExec   : simpleFoam -parallel\nCreate time\n", False),
        "end_before_last_time": (head() + iters(1, 30) + END + iters(31, 50), False),
        "early_stop_residualControl": (head() + iters(1, 42) + "\nSIMPLE solution converged in 42 iterations\n\n" + END, False),
        "restart_last_run_complete": (head() + iters(1, 20) + head() + iters(21, 50) + END, True),
        "complete_crlf": ((head() + iters(1, 50) + END).replace("\n", "\r\n"), True),
        "fatal_after_end": (head() + iters(1, 50) + END + "--> FOAM FATAL ERROR: something\n", False),
        "end_line_not_exact": (head() + iters(1, 50) + "End of run\n", False),
    }
    for name, (txt, exp) in cases.items():
        ok, d = H.run_completion(case_with_log(tmp, name, txt))
        assert ok == exp, (name, d); print(f"  run_completion {name:28s} -> {'COMPLETE' if ok else 'refused: ' + '; '.join(d['fails'])[:110]}")
    ok, d = H.run_completion(case_with_log(tmp, "budget_mismatch", head() + iters(1, 50) + END, end_time=3000)); assert not ok and "endTime" in d["fails"][0]
    r = subprocess.run([sys.executable, "-B", f"{TC}/pf/post_helpers.py", "finished", f"{tmp}/appended_partial_run", "--json", f"{tmp}/rc.json"], capture_output=True, text=True)
    assert r.returncode == 1 and not json.load(open(f"{tmp}/rc.json"))["ok"], r.stdout
    sh = open(f"{TC}/post_case_generic.sh").read(); assert "--require-finished" in sh and "post_helpers.py\" finished" in sh
    ac = open(f"{TC}/pf/analyze_case.py").read(); assert "EXIT_NOT_FINISHED = 4" in ac and '"--require-finished" in sys.argv' in ac
    print("  (3) finished guard: last run must complete with Time == endTime; analysis completion flag enforced by the runner (--require-finished)")

def test_resolution(tmp):
    src = open(M.__file__).read(); assert "/tmp/" not in src and "M1_PKG_ROOT" not in src
    roots = M.DRIVE_PKG_ROOTS + M.PERSISTENT_PKG_ROOTS
    assert roots == ("/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/M1", "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/packages/P5", "/home/azan/paper6_t6_work/scratchpad/zipcheck/cfd_handover/packages/M1")
    got14 = M.resolve_pkg_dir(S14); exp14 = next(os.path.join(r, S14) for r in roots if os.path.isdir(os.path.join(r, S14))); assert got14 == exp14, got14
    got473 = M.resolve_pkg_dir(P473); assert got473 == os.path.join(M.DRIVE_PKG_ROOTS[1], P473), got473
    os.makedirs(f"{tmp}/root_explicit"); shutil.copytree(got14, f"{tmp}/root_explicit/{S14}")
    assert M.resolve_pkg_dir(S14, f"{tmp}/root_explicit") == f"{tmp}/root_explicit/{S14}"
    try: M.resolve_pkg_dir(P473, f"{tmp}/root_explicit"); raise AssertionError("explicit root must not fall back")
    except SystemExit: pass
    print(f"  (1) resolution: {S14} -> {got14}; {P473} -> {got473}; explicit root used alone (no fallback)")
    return got14

def test_package_check(tmp, real):
    info = dict(package=S14, package_hashes=M.package_hashes(real)); case = f"{tmp}/pkcase"; os.makedirs(case); json.dump(info, open(f"{case}/build_info.json", "w"))
    assert H.package_check(case, S14, f"{tmp}/pk_ok.json") and json.load(open(f"{tmp}/pk_ok.json"))["ok"]
    assert H.package_check(case, f"{tmp}/root_explicit/{S14}", f"{tmp}/pk_ok2.json")
    tam = f"{tmp}/root_tamper/{S14}"; shutil.copytree(real, tam); open(f"{tam}/probes.csv", "a").write("\n")
    assert not H.package_check(case, S14, f"{tmp}/pk_bad.json", f"{tmp}/root_tamper") and any("probes.csv: sha256" in x for x in json.load(open(f"{tmp}/pk_bad.json"))["fails"])
    mis = f"{tmp}/root_missing/{S14}"; shutil.copytree(real, mis); os.remove(f"{mis}/mask_edit.json")
    assert not H.package_check(case, S14, f"{tmp}/pk_mis.json", f"{tmp}/root_missing")
    j = json.load(open(f"{case}/build_info.json")); j.pop("package_hashes"); json.dump(j, open(f"{tmp}/bi.json", "w")); c2 = f"{tmp}/pkcase2"; os.makedirs(c2); shutil.copy(f"{tmp}/bi.json", f"{c2}/build_info.json")
    assert not H.package_check(c2, S14, f"{tmp}/pk_norec.json")
    j = dict(info, package="other_name"); c3 = f"{tmp}/pkcase3"; os.makedirs(c3); json.dump(j, open(f"{c3}/build_info.json", "w"))
    assert not H.package_check(c3, S14, f"{tmp}/pk_name.json")
    sh = open(f"{TC}/post_case_generic.sh").read(); assert sh.index('PKGDIR=$(python3 "$PF/post_helpers.py" package-check') < sh.index('run $PY "$PF/analyze_case.py"') < sh.index('run $PY "$PF/m1_probes.py"')
    print("  (1) package check: verified copy OK; tampered probes.csv, missing mask_edit.json, no recorded hashes, other package name -> refused; runs before anything is generated")

def test_radius(tmp, real):
    case = f"{tmp}/radcase"; pm = f"{case}/constant/polyMesh"; os.makedirs(pm)
    for n in ("boundary", "owner", "neighbour", "points", "faces"): open(f"{pm}/{n}", "w").write(f"{n} 1 2 3\n")
    out = f"{tmp}/radout"; os.makedirs(out); pre = f"{out}/as_meshed_radius_X"
    write = lambda: [open(pre + s, "w").write(f"radius {s}\n") for s in H.RADIUS_SUFFIXES]
    write(); assert not H.radius_check(case, real, pre)                                    # files exist but no provenance -> regenerate
    write(); H.radius_commit(pre); assert H.radius_check(case, real, pre)                  # after a (re)generation + commit -> reusable
    open(f"{pm}/points", "a").write("4\n"); assert not H.radius_check(case, real, pre)      # mesh changed
    write(); H.radius_commit(pre); assert H.radius_check(case, real, pre)
    assert not H.radius_check(case, f"{tmp}/root_tamper/{S14}", pre)                        # package hashes differ
    open(pre + "_inscribed.csv", "a").write("edit\n"); assert not H.radius_check(case, real, pre)   # an output edited after generation
    sh = open(f"{TC}/post_case_generic.sh").read(); assert "POST_REUSE_UNCHECKED" in sh and "radius-commit" in sh and "POST_RADIUS_DECISION" in open(f"{TC}/pf/post_helpers.py").read()
    print("  (4) radius provenance: no record / mesh changed / package changed / output edited -> regenerate; same mesh+package -> reuse")

def main():
    tmp = tempfile.mkdtemp(prefix="post_guards_")
    try:
        test_completion(tmp); real = test_resolution(tmp); test_package_check(tmp, real); test_radius(tmp, real)
        print("PASS: post guards (package resolution + build_info hash verification, last-run completion, radius provenance)")
    finally: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
