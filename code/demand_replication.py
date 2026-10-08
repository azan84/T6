"""
demand_replication.py — the whole reduced-order pipeline re-run at a scaled hyperaemic demand, with the cohort
RE-SELECTED at that demand. Added 2026-10-08 after the blind ARS review (domain W1, methodology W6): at k = 562 s^-1
the segmented ImageCAS-X radii (median reference radius 1.26 mm at the LAD lesion slot, against ~1.85 mm normal)
give hyperaemic flows well below the thermodilution values, and an 80 %DS lesion reads FFR ~0.87.

Unlike ablation_demand_scale.py (frozen cohort, demand x0.7/x1.3), this re-runs every stage with K_MURRAY scaled, so
that the baseline FFR bands again span 0.80 at the higher flow:
  1. severity sweep on the test split            -> <outdir>/sweep_test.csv
  2. stratified selection (same rule and seed)   -> <outdir>/sweep_test_selected.csv   (= this replication's cohort)
  3. discrete-arm eligibility                    -> <outdir>/discrete_arm_eligibility.csv
  4. ablation A/B/C                              -> <outdir>/ablation.csv
  5. per-territory Protocol D                    -> <outdir>/ablation-perterritory.csv
Frozen modules are imported unchanged; only K_MURRAY and output paths differ.

usage: demand_replication.py <kscale> <data_root> <outdir>
"""
import sys, subprocess
from pathlib import Path

HERE = Path(__file__).parent
scale, root, outdir = float(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)
PY = sys.executable

PATCH = (f"import sys; sys.path.insert(0, {str(HERE)!r}); import zerod_ffr; zerod_ffr.K_MURRAY = 562.0 * {scale}; ")


def run(code, log):
    with open(outdir / log, "w") as fh:
        r = subprocess.run([PY, "-c", PATCH + code], stdout=fh, stderr=subprocess.STDOUT)
    if r.returncode: sys.exit(f"stage failed, see {outdir / log}")


# 1. sweep: severity_sweep.run writes to <module dir>/../results; point its __file__ at outdir/code/
run("import severity_sweep as ss; from pathlib import Path; "
    f"ss.__file__ = {str(outdir / 'code' / 'severity_sweep.py')!r}; ss.run(Path({root!r}), 'test')", "1_sweep.log")
(outdir / "results" / "sweep_test.csv").rename(outdir / "sweep_test.csv")
(outdir / "results" / "sweep_test_rejections.csv").rename(outdir / "sweep_test_rejections.csv")
(outdir / "results").rmdir()
# 2. selection
run(f"import severity_sweep as ss; ss.select({str(outdir / 'sweep_test.csv')!r})", "2_select.log")
coh = str(outdir / "sweep_test_selected.csv")
# 3. discrete eligibility
run(f"import discrete_arm as d; sys.argv = ['x', {root!r}, '--cohort', {coh!r}, '--out', "
    f"{str(outdir / 'discrete_arm_eligibility.csv')!r}]; d.main()", "3_discrete.log")
# 4. ablation A/B/C
run(f"import ablation as A; A.K_MURRAY = zerod_ffr.K_MURRAY; sys.argv = ['x', {root!r}, '--cohort', {coh!r}, "
    f"'--out', {str(outdir / 'ablation.csv')!r}]; A.main()", "4_ablation.log")
# 5. per-territory D
r = subprocess.run([PY, str(HERE / "ablation_per_territory.py"), root, "--cohort", coh, "--kscale", str(scale),
                    "--out", str(outdir / "ablation-perterritory.csv")],
                   stdout=open(outdir / "5_perterritory.log", "w"), stderr=subprocess.STDOUT)
print("done" if r.returncode == 0 else "stage 5 failed")
