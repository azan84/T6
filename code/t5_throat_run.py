"""
t5_throat_run.py - runs the throat caliber error (T5) under Protocols A-C (ablation.run_instance) and D
(ablation_per_territory.run_instance) on the frozen cohort, both beds, by swapping the error-type set and the
insertion function through t5_throat_error_types.install(). The frozen modules are imported unchanged.

usage:
  t5_throat_run.py validate [--n 6]      zero-magnitude identity, clean-FFR reproduction, DS monotonicity
  t5_throat_run.py run [--workers 4]     full cohort, both beds
"""
from __future__ import annotations
import argparse, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import t5_throat_error_types as T5
import ablation as A
import ablation_per_territory as P

ROOT = T5.DATA_ROOT
PROJ = HERE.parent
COHORT = PROJ / "deposit-2026-10-08" / "protocol" / "COHORT-FROZEN-2026-09-18.csv"
OUT = PROJ / "results" / "t5_throat-2026-10-09"
FROZEN_ABL = PROJ / "results" / "ablation-2026-10-07.csv"
FROZEN_PER = PROJ / "results" / "ablation-perterritory-2026-10-08.csv"
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]


def build_types(spec):
    """spec: "t5" for the four variants, or a dict {name: dDS fraction} of constant-DS check types."""
    if spec == "t5": return T5.T5_TYPES
    return {k: T5.constant_ds_type(v) for k, v in spec.items()}


def one(args):
    row, bed, spec = args
    T5.install(build_types(spec))
    T5.LOG.clear()
    T5.reset(); abc, _, _, why = A.run_instance(ROOT, row, bed)
    T5.reset(); d, why_d = P.run_instance(A, ROOT, row, bed)
    T5.reset()
    log = [dict(m, bed=bed) for m in T5.LOG]
    return abc, d, log, why or why_d


PARTS = Path("/private/tmp/claude-501/t5_throat_parts")


def _part(args):
    row, bed, spec = args
    return PARTS / f"{int(row.scan)}_{row.side}_{row.vessel}_{row['loc']}_{int(row.L_mm)}_{int(row.ds_pct)}_{bed}.pkl"


def one_cached(args):
    import pickle
    f = _part(args)
    if f.exists(): return pickle.loads(f.read_bytes())
    res = one(args)
    tmp = f.with_suffix(".tmp"); tmp.write_bytes(pickle.dumps(res)); tmp.rename(f)
    return res


def run_all(coh, beds, types, workers, cache=False):
    tasks = [(r, bed, types) for _, r in coh.iterrows() for bed in beds]
    if cache: PARTS.mkdir(parents=True, exist_ok=True)
    abc, d, log, t0 = [], [], [], time.time()
    with Pool(workers) as pool:
        for n, (a_, d_, l_, why) in enumerate(pool.imap(one_cached if cache else one, tasks, chunksize=1), 1):
            abc += a_; d += d_; log += l_
            if n % 20 == 0: print(f"  {n}/{len(tasks)}  {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(abc), pd.DataFrame(d), pd.DataFrame(log), time.time() - t0


def frozen_clean():
    f = pd.read_csv(FROZEN_ABL, low_memory=False, float_precision="round_trip")
    return f[f.error_type == "clean"][KEY + ["bed", "ffr"]].rename(columns={"ffr": "ffr_frozen"})


def check_clean(abc, d):
    fc = frozen_clean()
    c = abc[abc.error_type == "clean"][KEY + ["bed", "ffr"]].merge(fc, on=KEY + ["bed"], how="outer", indicator=True)
    both = c[c._merge == "both"]
    dmax = float((both.ffr - both.ffr_frozen).abs().max())
    fp = pd.read_csv(FROZEN_PER, float_precision="round_trip")[KEY + ["bed", "ffr_clean"]].drop_duplicates()
    dd = d[KEY + ["bed", "ffr_clean"]].drop_duplicates().merge(fp, on=KEY + ["bed"], suffixes=("", "_frozen"))
    dmax_d = float((dd.ffr_clean - dd.ffr_clean_frozen).abs().max())
    return dict(n_clean_rows=len(both), only_new=int((c._merge == "left_only").sum()),
                only_frozen=int((c._merge == "right_only").sum()), max_abs_diff_clean_ffr=dmax,
                identical=bool(dmax == 0.0), n_D_instances=len(dd), max_abs_diff_D_ffr_clean=dmax_d)


def validate(n, workers):
    OUT.mkdir(parents=True, exist_ok=True)
    coh = pd.read_csv(COHORT)
    sub = pd.concat([coh[coh.side == "left"].head(n // 2 + 1), coh[coh.side == "right"].head(n // 2)]).head(n)
    lines = [f"validation on {len(sub)} instances: " + ", ".join(f"{r.scan}_{r.side}_{r.vessel}_{r['loc']}_{int(r.L_mm)}mm_{int(r.ds_pct)}"
                                                         for _, r in sub.iterrows())]
    # (1) zero magnitude: the T5 path with dDS = 0 must reproduce the clean model
    zero = {"T5_zero": 0.0}
    abc, d, log, _ = run_all(sub, ["leaky", "discrete"], zero, workers)
    ok = pd.concat([abc[(abc.error_type == "T5_zero") & (abc.status == "ok")], d[d.status == "ok"]])
    lines.append("(1) zero-magnitude T5 path, |dFFR| by protocol (max):")
    for p, g in ok.groupby("protocol"):
        lines.append(f"    {p:16} n={len(g):3}  max|dFFR|={g.dFFR.abs().max():.3e}  flips={int(g.flip.sum())}")
    lines.append(f"    insertions logged {len(log)}, all ds_applied == ds_orig: {bool((log.ds_applied == log.ds_orig).all())}")
    # (2) clean FFR reproduces the frozen run exactly
    cc = check_clean(abc, d)
    lines.append(f"(2) clean FFR vs frozen ablation-2026-10-07: {cc}")
    # (3) monotonicity of FFR in DS under Protocol A (and B)
    grid = [-0.20, -0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15]
    types = {f"T5_d{int(round(g*100)):+d}": g for g in grid}
    abc3, _, log3, _ = run_all(sub, ["leaky", "discrete"], types, workers)
    x = abc3[(abc3.status == "ok") & abc3.protocol.isin(["A_fixed", "B_rederived"])].copy()
    x["dds"] = x.error_type.str.extract(r"d([+-]\d+)").astype(float)
    x["ds_new"] = (x.ds_pct + x.dds).clip(5, 95)
    viol, steps = 0, 0
    mono_rows = []
    for k, g in x.groupby(KEY + ["bed", "protocol"]):
        g = g.sort_values("ds_new"); f = g.ffr.values; dif = np.diff(f)
        steps += len(dif); viol += int((dif >= 0).sum())
        mono_rows.append(dict(zip(KEY + ["bed", "protocol"], k), **{f"ffr_ds{int(a)}": b for a, b in zip(g.ds_new, f)}))
    lines.append(f"(3) FFR strictly decreasing in DS (Protocols A and B, DS change -20..+15 pp): "
                 f"{viol} violations in {steps} steps over {x.groupby(KEY + ['bed']).ngroups} instance-beds")
    pd.DataFrame(mono_rows).to_csv(OUT / "validation_monotonic.csv", index=False)
    txt = "\n".join(lines); print(txt); (OUT / "validation.txt").write_text(txt + "\n")


def run(workers):
    OUT.mkdir(parents=True, exist_ok=True)
    coh = pd.read_csv(COHORT)
    abc, d, log, dt = run_all(coh, ["leaky", "discrete"], "t5", workers, cache=True)
    abc.to_csv(OUT / "ablation_t5.csv", index=False)
    d.to_csv(OUT / "perterritory_t5.csv", index=False)
    log.to_csv(OUT / "t5_insert_log.csv", index=False)
    cc = check_clean(abc, d)
    txt = (f"rows A-C {len(abc)}, D {len(d)}, insertions {len(log)}, {dt:.0f}s\n"
           f"clean FFR vs frozen: {cc}\n"
           f"status A-C: {abc.status.value_counts().to_dict()}\nstatus D: {d.status.value_counts().to_dict()}\n")
    print(txt); (OUT / "run.txt").write_text(txt)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=("validate", "run"))
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    validate(a.n, a.workers) if a.mode == "validate" else run(a.workers)
