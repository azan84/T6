"""Every 120 s evaluate the predefined convergence criteria (analyze_solve.py, which itself requires >= 200 iterations for the 200-iteration bands) on the running cases; a case is stopped gracefully
(stopAt writeNow) only after TWO consecutive CONVERGED checks at least 20 iterations apart and >= 300 iterations. A case whose log has not changed for 20 min and has no 'Finalising parallel run'
is reported as STALLED/TERMINATED (never treated as converged). Never stops a case for any other reason. Cases MUST be given as arguments (no defaults).
usage: watch_converge.py [--strict] solve_lesion80_T25a solve_lesion80_T25b solve_lesion80_W100      log: stdout
--strict (optional, first argument only): the verdict is analyze_solve.main(case, strict=True) (adds the strict checks); otherwise unchanged."""
import sys, os, time, io, contextlib, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analyze_solve as A
BASE = os.path.dirname(os.path.abspath(__file__))
STRICT = len(sys.argv) > 1 and sys.argv[1] == "--strict"
cases = sys.argv[2:] if STRICT else sys.argv[1:]
if not cases: raise SystemExit("usage: watch_converge.py <case_dir_name> ...   (no default cases)")
ok_count = {c: 0 for c in cases}; last_ok_iter = {c: None for c in cases}; done = set()
env = "source /usr/lib/openfoam/openfoam2406/etc/bashrc; "
def log(m): print(time.strftime("%H:%M:%S"), m, flush=True)
while len(done) < len(cases):
    for c in cases:
        if c in done: continue
        d = f"{BASE}/{c}"; lf = f"{d}/log.simpleFoam"
        if os.path.exists(lf):
            txt = open(lf).read()
            if "Finalising parallel run" in txt[-400:]:
                log(f"{c}: run finished on its own or after writeNow"); done.add(c); continue
            if time.time() - os.path.getmtime(lf) > 1200:
                log(f"{c}: STALLED/TERMINATED (log unchanged for > 20 min, no 'Finalising parallel run') - not converged, needs attention"); done.add(c); continue
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r = A.main(d, strict=True) if STRICT else A.main(d)
        except Exception as e:
            log(f"{c}: analysis not ready ({type(e).__name__}: {e})"); ok_count[c] = 0; continue
        it = r["last_iteration"]; failed = [k for k, v in r["checks"].items() if not v]
        log(f"{c}: iter {it} verdict {r['verdict']} p_res {r['residuals_last']['p']:.1e} failed {failed}")
        if r["verdict"] == "CONVERGED" and it >= 300:
            if last_ok_iter[c] is None or it - last_ok_iter[c] >= 20:
                ok_count[c] += 1; last_ok_iter[c] = it
        else:
            ok_count[c] = 0; last_ok_iter[c] = None
        if ok_count[c] >= 2:
            try:
                subprocess.run(["bash", "-c", env + f"cd {d} && foamDictionary system/controlDict -entry stopAt -set writeNow"], check=True, capture_output=True)
                if "writeNow" not in open(f"{d}/system/controlDict").read(): raise RuntimeError("stopAt not set to writeNow")
                log(f"{c}: CONVERGED at two consecutive checks (iter {it}) -> stopAt writeNow"); done.add(c)
            except Exception as e:
                log(f"{c}: stop command failed ({type(e).__name__}: {e}); will retry"); ok_count[c] = 1
    time.sleep(120)
log("all cases stopped/finished")
