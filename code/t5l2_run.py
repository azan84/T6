"""
t5l2_run.py - throat caliber error (T5) with the level-2 perfusion-territory partition.

Combines two existing modules without editing either:
  t5_throat_error_types.install()   swaps the error-type set to the T5 variants and patches the lesion insertion
  a6_territory_run.setup(config)     patches ablation.protocol_c_targets with the level-1 or level-2 partition and
                                     the unperfused-territory rule; a6_territory_run.run_d is the Protocol D fit
Protocols A-C come from the frozen ablation.run_instance, which uses protocol_c_targets for the residual of every
protocol, so A and B residuals follow the configured partition while their FFR does not change.

usage:
  t5l2_run.py check-a6 [--n 6]                 frozen T1-T4 at L2keep through this wrapper vs the stored L2keep rows
  t5l2_run.py check-zero [--n 6]               T5 path with dDS = 0 at L2keep: dFFR = 0, residual as for the clean tree
  t5l2_run.py run --config L1drop|L2keep       T5 variants, full cohort, both beds
  t5l2_run.py check-t5                         L1drop T5 run vs results/t5_throat-2026-10-09, every row
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

PROJ = HERE.parent
ROOT = Path.home() / "Documents" / "Datasets" / "imagecas-x" / "ImageCAS-X_dataset"
COHORT = PROJ / "deposit-2026-10-08" / "protocol" / "COHORT-FROZEN-2026-09-18.csv"
OUT = PROJ / "results" / "t5l2-2026-10-09"
T5_DIR = PROJ / "results" / "t5_throat-2026-10-09"
A6_DIR = PROJ / "results" / "a6_territory-2026-10-09"
COLS = ["status", "ffr", "dFFR", "flip", "outlet_flow_residual"]


def setup(config: str, types: str):
    import severity_sweep, ablation
    import t5_throat_error_types as T5
    import a6_territory_run as A6
    if types == "t5":
        T5.install(T5.T5_TYPES)
    elif types == "zero":
        T5.install({"T5_zero": T5.constant_ds_type(0.0)})
    else:  # frozen T1-T4; the insertion patch is installed but has no pending transform
        if T5._ORIG_INSERT is None:
            T5._ORIG_INSERT = severity_sweep.insert
        severity_sweep.insert = T5.patched_insert
        ablation.insert = T5.patched_insert
    A6.setup(config)


def job(args):
    root, row, bed = args
    import ablation as A
    import t5_throat_error_types as T5
    import a6_territory_run as A6
    T5.LOG.clear()
    T5.reset(); abc, terr, _, why1 = A.run_instance(root, row, bed)
    T5.reset(); d, tinfo, why2 = A6.run_d(A, root, row, bed)
    T5.reset()
    empty = {}
    for x in terr:
        if x["n_nodes"] == 0: empty[x["run_id"]] = empty.get(x["run_id"], 0) + 1
    for r in abc:
        if r.get("status") == "ok" and r.get("protocol"):
            r["n_empty"] = empty.get(r["run_id"], 0)
    log = [dict(m, bed=bed) for m in T5.LOG]
    return abc, d, tinfo, log, (why1 or why2)


def run_all(coh, config, types, workers, beds=("leaky", "discrete")):
    jobs = [(ROOT, r, bed) for _, r in coh.iterrows() for bed in beds]
    abc_all, d_all, ti_all, log_all, t0 = [], [], [], [], time.time()
    with Pool(workers, initializer=setup, initargs=(config, types)) as pool:
        for n, (abc, d, ti, log, why) in enumerate(pool.imap(job, jobs, chunksize=1), 1):
            abc_all += abc; d_all += d; log_all += log
            if ti: ti_all.append(ti)
            if why: print(f"  skip job {n}: {why}", file=sys.stderr)
            if n % 20 == 0: print(f"  {n}/{len(jobs)}  {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(abc_all), pd.DataFrame(d_all), pd.DataFrame(ti_all), pd.DataFrame(log_all), time.time() - t0


def sample(n):
    coh = pd.read_csv(COHORT)
    return pd.concat([coh[coh.side == "left"].head(n // 2 + 1), coh[coh.side == "right"].head(n // 2)]).head(n)


def compare(new, ref, label):
    """Row-by-row comparison on run_id: status equal, numeric columns bit-identical (NaN = NaN)."""
    j = new.set_index("run_id")[COLS].join(ref.set_index("run_id")[COLS], how="left", rsuffix="_ref")
    lines = [f"{label}: {len(new)} rows, {int(j.status_ref.isna().sum())} without a reference row, "
             f"status differs in {int((j.status != j.status_ref).sum())}"]
    for c in COLS[1:]:
        a, b = j[c].astype(float), j[c + "_ref"].astype(float)
        diff = ~((a == b) | (a.isna() & b.isna()))
        lines.append(f"    {c:22} rows differing {int(diff.sum()):4}  max|diff| "
                     f"{float(np.nanmax(np.abs(a - b))) if len(a) else 0:.3g}")
    return lines


def rd(f):
    return pd.read_csv(f, low_memory=False, float_precision="round_trip")


def check_a6(n, workers):
    sub = sample(n)
    abc, d, _, _, dt = run_all(sub, "L2keep", "frozen", workers)
    ref_a, ref_d = rd(A6_DIR / "ablation_L2keep.csv"), rd(A6_DIR / "perterritory_L2keep.csv")
    lines = [f"check-a6: frozen T1-T4 at L2keep through t5l2_run on {len(sub)} instances x 2 beds ({dt:.0f}s): "
             + ", ".join(f"{r.scan}_{r.side}_{r.vessel}_{r['loc']}_{int(r.L_mm)}_{int(r.ds_pct)}" for _, r in sub.iterrows())]
    lines += compare(abc, ref_a, "  A-C (incl. clean rows) vs a6 ablation_L2keep")
    lines += compare(d, ref_d, "  D vs a6 perterritory_L2keep")
    return lines


def check_zero(n, workers):
    sub = sample(n)
    abc, d, _, log, dt = run_all(sub, "L2keep", "zero", workers)
    ok = pd.concat([abc[(abc.error_type == "T5_zero") & (abc.status == "ok")], d[d.status == "ok"]])
    lines = [f"check-zero: T5 path with dDS = 0 at L2keep, {len(sub)} instances x 2 beds ({dt:.0f}s); "
             f"insertions {len(log)}, all ds_applied == ds_orig: {bool((log.ds_applied == log.ds_orig).all())}"]
    for p, g in ok.groupby("protocol"):
        lines.append(f"    {p:16} n={len(g):3} max|dFFR|={g.dFFR.abs().max():.3e} flips={int(g.flip.sum())} "
                     f"max residual={g.outlet_flow_residual.max():.3e}")
    return lines


def run(config, workers):
    OUT.mkdir(parents=True, exist_ok=True)
    coh = pd.read_csv(COHORT)
    abc, d, ti, log, dt = run_all(coh, config, "t5", workers)
    abc.to_csv(OUT / f"ablation_t5_{config}.csv", index=False)
    d.to_csv(OUT / f"perterritory_t5_{config}.csv", index=False)
    ti.to_csv(OUT / f"territory_counts_{config}.csv", index=False)
    log.to_csv(OUT / f"t5_insert_log_{config}.csv", index=False)
    txt = (f"{config}: rows A-C {len(abc)}, D {len(d)}, insertions {len(log)}, {dt:.0f}s\n"
           f"status A-C: {abc.status.value_counts().to_dict()}\nstatus D: {d.status.value_counts().to_dict()}\n")
    print(txt); (OUT / f"run_{config}.txt").write_text(txt)


def check_t5():
    abc, d = rd(OUT / "ablation_t5_L1drop.csv"), rd(OUT / "perterritory_t5_L1drop.csv")
    lines = ["check-t5: L1drop T5 run through t5l2_run vs results/t5_throat-2026-10-09 (every row)"]
    lines += compare(abc, rd(T5_DIR / "ablation_t5.csv"), "  A-C (incl. clean rows) vs ablation_t5")
    lines += compare(d, rd(T5_DIR / "perterritory_t5.csv"), "  D vs perterritory_t5")
    ref = rd(T5_DIR / "perterritory_t5.csv").set_index("run_id").fit_at_bound
    j = d.set_index("run_id").fit_at_bound
    lines.append(f"    D fit_at_bound: here {int(j.sum())}, frozen T5 {int(ref.sum())}, "
                 f"rows differing {int((j != ref.reindex(j.index)).sum())}")
    return lines


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("check-a6", "check-zero", "run", "check-t5"))
    ap.add_argument("--config", default="L2keep", choices=("L1drop", "L2keep"))
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--workers", type=int, default=6)
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if a.mode == "run":
        run(a.config, a.workers)
    else:
        lines = {"check-a6": lambda: check_a6(a.n, a.workers), "check-zero": lambda: check_zero(a.n, a.workers),
                 "check-t5": check_t5}[a.mode]()
        txt = "\n".join(lines); print(txt)
        with open(OUT / "validation.txt", "a") as fh: fh.write(txt + "\n")
