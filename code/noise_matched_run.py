"""
noise_matched_run.py - segmentation-error models tuned to the same noisy perfusion targets as the correct-anatomy
floor, under Protocols A-D, with a Protocol D floor.

For each cohort instance, bed and recorded noise draw, the territory targets of Protocols C and D are the clean
territory flows scaled by the ratio noisy / nominal recorded for that draw in
results/a7_detector-2026-10-09/negatives_pretune.csv (terr_target_mls / terr_pred_start_mls). The corrupted model
itself stays nominal, as in negatives.py. Error types: an identity type (correct anatomy, the floor), T1-T4 from
error_types.py, and the two half-voxel throat variants from t5_throat_error_types.py. Draw -1 is the nominal
(noise-free) case, which must reproduce the frozen runs exactly.

The frozen modules are imported unchanged and patched in memory only: ablation.protocol_c_targets is replaced by a
version that applies the per-territory ratio, and the error-type set is swapped as in t5_throat_run.py.

usage:
  noise_matched_run.py validate [--n 6] [--workers 5]
  noise_matched_run.py run [--workers 5] [--max-draw 19]   draws 0..max-draw plus the nominal case
  noise_matched_run.py assemble
"""
from __future__ import annotations
import argparse, pickle, sys, time
from pathlib import Path
from multiprocessing import Pool
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ablation as A
import ablation_per_territory as P
import error_types as ET
import t5_throat_error_types as T5

PROJ = HERE.parent
ROOT = T5.DATA_ROOT
COHORT = PROJ / "deposit-2026-10-08" / "protocol" / "COHORT-FROZEN-2026-09-18.csv"
ELIG = PROJ / "results" / "discrete_arm_eligibility.csv"
NEG = PROJ / "results" / "a7_detector-2026-10-09" / "negatives_pretune.csv"
FROZEN_ABL = PROJ / "results" / "ablation-2026-10-07.csv"
FROZEN_PER = PROJ / "results" / "ablation-perterritory-2026-10-08.csv"
FROZEN_T5_ABL = PROJ / "results" / "t5_throat-2026-10-09" / "ablation_t5.csv"
FROZEN_T5_PER = PROJ / "results" / "t5_throat-2026-10-09" / "perterritory_t5.csv"
OUT = PROJ / "results" / "noise_matched-2026-10-09"
PARTS = Path("/private/tmp/claude-501/noise_matched_parts")
KEY = ["scan", "side", "vessel", "loc", "L_mm", "ds_pct"]
IDENTITY = "T0_identity"
T5_TYPES = {k: T5.T5_TYPES[k] for k in ("T5_vox_narrow", "T5_vox_wide")}

RATIO = {"v": None}


def noisy_targets(t, t2, m, q0_all):
    """Protocol C/D targets: the clean territory flow of each territory, scaled by the draw's noisy/nominal ratio."""
    terr_clean = A.territories(t)
    owner = {int(v): j for j, sub in enumerate(terr_clean) for v in sub}
    ratio = RATIO["v"]
    pairs = []
    for j, sub_c in enumerate(terr_clean):
        q_clean = float(q0_all[sub_c].sum())
        if ratio is not None:
            q_clean *= float(ratio[j])
        members = np.array([v for v in range(len(t2.parent))
                            if t2.active[v] and m[v] >= 0 and owner.get(int(m[v]), -1) == j], dtype=int)
        if q_clean > 0 and len(members):
            pairs.append((members, q_clean, sub_c))
    return pairs


def t0_identity(segs, tree, path, s_arc, c, L):
    return list(segs), {}


# Patches, applied at import so that spawned workers carry them.
A.protocol_c_targets = noisy_targets
BASE_TYPES = {k: v for k, v in ET.ERROR_TYPES.items() if k.startswith(("T1", "T2", "T3", "T4"))}
assert len(BASE_TYPES) == 4, sorted(BASE_TYPES)
T5.install(T5_TYPES)
TYPES = {IDENTITY: t0_identity, **BASE_TYPES, **T5_TYPES}
ET.ERROR_TYPES = TYPES
A.ERROR_TYPES = TYPES
A.CALIBRE_ONLY = ("T3_stenosis_length", "T4_taper", IDENTITY, "T5_vox_narrow", "T5_vox_wide")


def one(args):
    row, bed, draw, ratio = args
    RATIO["v"] = ratio
    T5.reset(); abc, _, _, why = A.run_instance(ROOT, row, bed)
    T5.reset(); d, why_d = P.run_instance(A, ROOT, row, bed)
    T5.reset(); RATIO["v"] = None
    rows = [dict(r, draw=draw) for r in abc] + [dict(r, draw=draw) for r in d]
    return rows, why or why_d


def part_path(args):
    row, bed, draw, _ = args
    return PARTS / f"{int(row.scan)}_{row.side}_{row.vessel}_{row['loc']}_{int(row.L_mm)}_{int(row.ds_pct)}_{bed}_d{draw}.pkl"


def one_cached(args):
    f = part_path(args)
    if f.exists():
        return pickle.loads(f.read_bytes())
    res = one(args)
    tmp = f.with_suffix(".tmp"); tmp.write_bytes(pickle.dumps(res)); tmp.rename(f)
    return res


def load_inputs():
    coh = pd.read_csv(COHORT)
    el = pd.read_csv(ELIG); el = el[el.eligible.astype(bool)][KEY]
    neg = pd.read_csv(NEG, low_memory=False)
    return coh, el, neg


def build_tasks(coh, el, neg, n_draws=20):
    """One task per instance, bed and draw (-1 = nominal), the draws of one instance-bed consecutive so that a
    worker reuses the scan's cached distance transform. Discrete bed: eligible instances only."""
    elig = set(map(tuple, el[KEY].astype(str).values))
    tasks = []
    for _, r in coh.iterrows():
        k = tuple(str(r[c]) for c in KEY)
        for bed in ("leaky", "discrete"):
            if bed == "discrete" and k not in elig:
                continue
            g = neg[(neg.scan == r.scan) & (neg.side == r.side) & (neg.vessel == r.vessel) & (neg["loc"] == r["loc"])
                    & np.isclose(neg.L_mm, r.L_mm) & (neg.ds_pct == r.ds_pct) & (neg.bed == bed)].sort_values("draw")
            tasks.append((r, bed, -1, None))
            for _, n in g.head(n_draws).iterrows():
                tgt = np.array([float(x) for x in str(n.terr_target_mls).split(";")])
                nom = np.array([float(x) for x in str(n.terr_pred_start_mls).split(";")])
                tasks.append((r, bed, int(n.draw), tgt / nom))
    return tasks


def n_per_group(tasks):
    """Tasks per instance-bed (nominal + draws), the chunk handed to one worker."""
    first = (int(tasks[0][0].scan), tasks[0][1])
    return sum(1 for t in tasks if (int(t[0].scan), t[1]) == first and t[0].vessel == tasks[0][0].vessel
               and t[0]["loc"] == tasks[0][0]["loc"] and t[0].L_mm == tasks[0][0].L_mm and t[0].ds_pct == tasks[0][0].ds_pct)


def run_tasks(tasks, workers, cache):
    if cache:
        PARTS.mkdir(parents=True, exist_ok=True)
    rows, fails, t0 = [], [], time.time()
    group = n_per_group(tasks)
    with Pool(workers, maxtasksperchild=4 * group) as pool:
        for n, (rr, why) in enumerate(pool.imap_unordered(one_cached if cache else one, tasks, chunksize=group), 1):
            rows += rr
            if why:
                fails.append(why)
            if n % 50 == 0 or n == len(tasks):
                print(f"  {n}/{len(tasks)}  {time.time() - t0:.0f}s", flush=True)
    return pd.DataFrame(rows), fails, time.time() - t0


def frozen_rows():
    cols = KEY + ["bed", "error_type", "protocol", "ffr", "dFFR", "outlet_flow_residual"]
    fr = []
    for f in (FROZEN_ABL, FROZEN_T5_ABL):
        x = pd.read_csv(f, low_memory=False, float_precision="round_trip")
        fr.append(x[(x.status == "ok") & (x.error_type != "clean")][cols])
    for f in (FROZEN_PER, FROZEN_T5_PER):
        x = pd.read_csv(f, low_memory=False, float_precision="round_trip")
        fr.append(x[x.status == "ok"][cols])
    return pd.concat(fr, ignore_index=True).rename(columns={"ffr": "ffr_frozen", "dFFR": "dFFR_frozen",
                                                            "outlet_flow_residual": "resid_frozen"})


def check(df, neg):
    """Nominal rows against the frozen runs; identity rows against the recorded floor draws."""
    ok = df[df.status == "ok"].copy()
    lines = ["error types (ok rows): " + str(ok.error_type.value_counts().to_dict())]
    nom = ok[(ok.draw == -1) & (ok.error_type != "clean") & (ok.error_type != IDENTITY)]
    m = nom.merge(frozen_rows(), on=KEY + ["bed", "error_type", "protocol"], how="left")
    miss = int(m.ffr_frozen.isna().sum())
    dmax = float((m.ffr - m.ffr_frozen).abs().max()); rmax = float((m.outlet_flow_residual - m.resid_frozen).abs().max())
    lines.append(f"nominal vs frozen (T1-T4 and half-voxel throat, A-D): n={len(m)} unmatched={miss} "
                 f"max|FFR diff|={dmax:.3e} max|residual diff|={rmax:.3e} identical={bool(dmax == 0.0 and rmax == 0.0)}")
    per = {p: float((g.ffr - g.ffr_frozen).abs().max()) for p, g in m.groupby("protocol")}
    lines.append("  by protocol: " + ", ".join(f"{p} {v:.1e}" for p, v in per.items()))
    nom0 = ok[(ok.draw == -1) & (ok.error_type == IDENTITY)]
    lines.append(f"nominal identity: n={len(nom0)} max|dFFR|={float(nom0.dFFR.abs().max()):.2e} "
                 f"max residual={float(nom0.outlet_flow_residual.max()):.2e}")
    ncols = KEY + ["bed", "draw", "dFFR", "outlet_flow_residual", "pretune_resid", "C_ratio"]
    v = ok[(ok.error_type == IDENTITY) & (ok.protocol == "C_flowmatched") & (ok.draw >= 0)]
    v = v.merge(neg[neg.status == "ok"][ncols], on=KEY + ["bed", "draw"], suffixes=("", "_a7"))
    lines.append(f"identity under C vs recorded floor draws: n={len(v)} max|dFFR diff|={float((v.dFFR - v.dFFR_a7).abs().max()):.2e} "
                 f"max|residual diff|={float((v.outlet_flow_residual - v.outlet_flow_residual_a7).abs().max()):.2e} "
                 f"max|C_ratio diff|={float((v.C_ratio - v.C_ratio_a7).abs().max()):.2e}")
    vb = ok[(ok.error_type == IDENTITY) & (ok.protocol == "B_rederived") & (ok.draw >= 0)]
    vb = vb.merge(neg[ncols], on=KEY + ["bed", "draw"], suffixes=("", "_a7"))
    lines.append(f"identity under B vs recorded pre-tuning residual: n={len(vb)} "
                 f"max diff={float((vb.outlet_flow_residual - vb.pretune_resid).abs().max()):.2e}")
    return "\n".join(lines)


def validate(n, workers):
    OUT.mkdir(parents=True, exist_ok=True)
    coh, el, neg = load_inputs()
    abl = pd.read_csv(FROZEN_ABL, low_memory=False)
    okd = abl[(abl.error_type == "T1_missed_branch") & (abl.protocol == "C_flowmatched") & (abl.status == "ok")
              & (abl.bed == "discrete")][KEY].drop_duplicates()
    sel = coh.merge(okd, on=KEY).merge(el, on=KEY)
    sel = sel.iloc[np.linspace(0, len(sel) - 1, n).astype(int)]
    tasks = build_tasks(sel, el, neg)
    df, fails, dt = run_tasks(tasks, workers, cache=True)
    df.to_csv(OUT / "validation_rows.csv", index=False)
    txt = (f"validation on {len(sel)} instances (bands {sorted(sel.band.unique())}): "
           + ", ".join(f"{r.scan}_{r.side}_{r.vessel}_{r['loc']}_{int(r.L_mm)}mm_{int(r.ds_pct)}" for _, r in sel.iterrows())
           + f"\n{len(tasks)} tasks (instance x bed x draw), {len(df)} rows, {dt:.0f}s on {workers} workers; failures: {fails}\n"
           + check(df, neg) + "\n" + f"status: {df.status.value_counts().to_dict()}\n")
    print(txt); (OUT / "validation.txt").write_text(txt)


def run(workers, max_draw):
    OUT.mkdir(parents=True, exist_ok=True)
    coh, el, neg = load_inputs()
    tasks = build_tasks(coh, el, neg, n_draws=max_draw + 1)
    print(f"{len(tasks)} tasks on {workers} workers", flush=True)
    df, fails, dt = run_tasks(tasks, workers, cache=True)
    write(df, fails, dt, neg)


def assemble():
    coh, el, neg = load_inputs()
    rows, fails = [], []
    for f in sorted(PARTS.glob("*.pkl")):
        rr, why = pickle.loads(f.read_bytes()); rows += rr
        if why: fails.append(why)
    write(pd.DataFrame(rows), fails, float("nan"), neg)


def write(df, fails, dt, neg):
    df.to_csv(OUT / "matched_rows.csv", index=False)
    txt = (f"rows {len(df)}, instance-bed-draws {df[KEY + ['bed', 'draw']].drop_duplicates().shape[0]}, {dt:.0f}s; failures: {fails}\n"
           + check(df, neg) + "\n" + f"status: {df.status.value_counts().to_dict()}\n")
    print(txt); (OUT / "run.txt").write_text(txt)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("mode", choices=("validate", "run", "assemble"))
    ap.add_argument("--n", type=int, default=6); ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--max-draw", type=int, default=19)
    a = ap.parse_args()
    {"validate": lambda: validate(a.n, a.workers), "run": lambda: run(a.workers, a.max_draw), "assemble": assemble}[a.mode]()
