"""
throat_demand_run.py - the half-voxel throat caliber error (T5_vox_narrow, T5_vox_wide) under Protocols A-D on the
cohorts re-selected at a scaled hyperaemic demand (demand_replication.py). The frozen modules and the T5 wrapper
(t5_throat_error_types, t5_throat_run.one) are imported unchanged; each worker sets zerod_ffr.K_MURRAY = 562 * scale
before any tree is built, exactly as demand_replication.py and ablation_per_territory.py --kscale do.

usage:
  throat_demand_run.py validate <scale> [--n 6] [--workers 3]   zero-magnitude identity and clean-FFR reproduction
  throat_demand_run.py run <scale> [--workers 3]                full re-selected cohort
Beds: leaky and discrete at scale 2; leaky only at scale 3.
"""
from __future__ import annotations
import argparse, pickle, sys, time
from pathlib import Path
from multiprocessing import Pool
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
PROJ = HERE.parent
VOX = ("T5_vox_narrow", "T5_vox_wide")
BEDS = {2: ["leaky", "discrete"], 3: ["leaky"]}
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]


def rep_dir(scale):
    return PROJ / "results" / f"demand-replication-x{scale}-2026-10-08"


def out_dir(scale):
    return PROJ / "results" / "throat_demand-2026-10-09" / f"x{scale}"


def parts_dir(scale):
    return Path(f"/private/tmp/claude-501/throat_demand_parts_x{scale}")


_SCALE = None


def init(scale):
    global _SCALE
    _SCALE = scale
    import zerod_ffr
    zerod_ffr.K_MURRAY = 562.0 * scale
    import ablation
    ablation.K_MURRAY = zerod_ffr.K_MURRAY


def types_for(spec):
    import t5_throat_error_types as T5
    if spec == "vox":
        return {k: T5.T5_TYPES[k] for k in VOX}
    return {k: T5.constant_ds_type(v) for k, v in spec.items()}


def one(args):
    row, bed, spec = args
    import zerod_ffr
    assert zerod_ffr.K_MURRAY == 562.0 * _SCALE
    import t5_throat_error_types as T5, ablation as A, ablation_per_territory as P
    T5.install(types_for(spec))
    T5.LOG.clear()
    T5.reset(); abc, _, _, why = A.run_instance(T5.DATA_ROOT, row, bed)
    T5.reset(); d, why_d = P.run_instance(A, T5.DATA_ROOT, row, bed)
    T5.reset()
    return abc, d, [dict(m, bed=bed) for m in T5.LOG], why or why_d


def one_cached(args):
    row, bed, spec = args
    f = parts_dir(_SCALE) / f"{int(row.scan)}_{row.side}_{row.vessel}_{row['loc']}_{int(row.L_mm)}_{int(row.ds_pct)}_{bed}.pkl"
    if f.exists(): return pickle.loads(f.read_bytes())
    res = one(args)
    tmp = f.with_suffix(".tmp"); tmp.write_bytes(pickle.dumps(res)); tmp.rename(f)
    return res


def run_all(scale, coh, beds, spec, workers, cache=False):
    tasks = [(r, bed, spec) for _, r in coh.iterrows() for bed in beds]
    if cache: parts_dir(scale).mkdir(parents=True, exist_ok=True)
    abc, d, log, t0 = [], [], [], time.time()
    with Pool(workers, initializer=init, initargs=(scale,)) as pool:
        for n, (a_, d_, l_, why) in enumerate(pool.imap(one_cached if cache else one, tasks, chunksize=1), 1):
            abc += a_; d += d_; log += l_
            if n % 20 == 0: print(f"  {n}/{len(tasks)}  {time.time()-t0:.0f}s", flush=True)
    return pd.DataFrame(abc), pd.DataFrame(d), pd.DataFrame(log), time.time() - t0


def check_clean(scale, abc, d, beds):
    rd = rep_dir(scale)
    f = pd.read_csv(rd / "ablation.csv", low_memory=False, float_precision="round_trip")
    fc = f[(f.error_type == "clean") & f.bed.isin(beds)][KEY + ["bed", "ffr"]].rename(columns={"ffr": "ffr_frozen"})
    c = abc[abc.error_type == "clean"][KEY + ["bed", "ffr"]].merge(fc, on=KEY + ["bed"], how="outer", indicator=True)
    both = c[c._merge == "both"]
    dmax = float((both.ffr - both.ffr_frozen).abs().max()) if len(both) else float("nan")
    fp = pd.read_csv(rd / "ablation-perterritory.csv", float_precision="round_trip")
    fp = fp[fp.bed.isin(beds)][KEY + ["bed", "ffr_clean"]].drop_duplicates()
    dd = d[KEY + ["bed", "ffr_clean"]].drop_duplicates().merge(fp, on=KEY + ["bed"], suffixes=("", "_frozen"))
    dmax_d = float((dd.ffr_clean - dd.ffr_clean_frozen).abs().max()) if len(dd) else float("nan")
    return dict(n_clean_rows=len(both), only_new=int((c._merge == "left_only").sum()),
                only_frozen=int((c._merge == "right_only").sum()), max_abs_diff_clean_ffr=dmax,
                n_D_instances=len(dd), max_abs_diff_D_ffr_clean=dmax_d,
                identical=bool(dmax == 0.0 and dmax_d == 0.0))


def validate(scale, n, workers):
    out = out_dir(scale); out.mkdir(parents=True, exist_ok=True)
    coh = pd.read_csv(rep_dir(scale) / "sweep_test_selected.csv")
    el = pd.read_csv(rep_dir(scale) / "discrete_arm_eligibility.csv")
    coh = coh.merge(el[KEY + ["eligible"]], on=KEY, how="left")
    # include discrete-eligible instances on both sides so that both beds are exercised
    left = coh[(coh.side == "left") & coh.eligible.astype(bool)].head(n // 2 + 1)
    right = coh[(coh.side == "right")].head(n // 2)
    sub = pd.concat([left, right]).head(n).drop(columns="eligible")
    beds = BEDS[scale]
    lines = [f"scale {scale} (K_MURRAY = {562.0*scale:.1f} s^-1), beds {beds}, validation on {len(sub)} instances: "
             + ", ".join(f"{r.scan}_{r.side}_{r.vessel}_{r['loc']}_{int(r.L_mm)}mm_{int(r.ds_pct)}" for _, r in sub.iterrows())]
    abc, d, log, dt = run_all(scale, sub, beds, {"T5_zero": 0.0}, workers)
    ok = pd.concat([abc[(abc.error_type == "T5_zero") & (abc.status == "ok")], d[d.status == "ok"]])
    lines.append("(1) zero-magnitude T5 path, |dFFR| by protocol (max):")
    for p, g in ok.groupby("protocol"):
        lines.append(f"    {p:16} n={len(g):3}  max|dFFR|={g.dFFR.abs().max():.3e}  flips={int(g.flip.sum())}")
    lines.append(f"    insertions logged {len(log)}, all ds_applied == ds_orig: {bool((log.ds_applied == log.ds_orig).all())}")
    cc = check_clean(scale, abc, d, beds)
    lines.append(f"(2) clean FFR vs {rep_dir(scale).name}/ablation.csv and ablation-perterritory.csv: {cc}")
    lines.append(f"    {dt:.0f}s")
    txt = "\n".join(lines); print(txt); (out / "validation.txt").write_text(txt + "\n")
    if not cc["identical"]: sys.exit("clean FFR does not reproduce the replication run")


def run(scale, workers):
    out = out_dir(scale); out.mkdir(parents=True, exist_ok=True)
    coh = pd.read_csv(rep_dir(scale) / "sweep_test_selected.csv")
    beds = BEDS[scale]
    abc, d, log, dt = run_all(scale, coh, beds, "vox", workers, cache=True)
    abc.to_csv(out / "ablation_t5vox.csv", index=False)
    d.to_csv(out / "perterritory_t5vox.csv", index=False)
    log.to_csv(out / "t5vox_insert_log.csv", index=False)
    cc = check_clean(scale, abc, d, beds)
    txt = (f"scale {scale}, beds {beds}: rows A-C {len(abc)}, D {len(d)}, insertions {len(log)}, {dt:.0f}s\n"
           f"clean FFR vs replication run: {cc}\n"
           f"status A-C: {abc.status.value_counts().to_dict()}\nstatus D: {d.status.value_counts().to_dict()}\n")
    print(txt); (out / "run.txt").write_text(txt)
    if not cc["identical"]: sys.exit("clean FFR does not reproduce the replication run")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=("validate", "run"))
    ap.add_argument("scale", type=int, choices=(2, 3))
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    validate(a.scale, a.n, a.workers) if a.mode == "validate" else run(a.scale, a.workers)
