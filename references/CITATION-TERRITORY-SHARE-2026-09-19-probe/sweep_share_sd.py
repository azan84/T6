"""PROBE (read-only w.r.t. the project): how does the negative class move with SD_TERRITORY_SHARE?

Monkeypatches negatives.SD_TERRITORY_SHARE over a sweep and re-runs the SAME instances with the SAME
seed, so the only thing that changes between arms is the constant under review. Writes a CSV next to
this file. Changes nothing in code/ or results/.

usage: python sweep_share_sd.py <data_root> [--limit N] [--draws N]
"""
import argparse, sys, time
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent                      # Paper6-T6
sys.path.insert(0, str(ROOT / "code"))
import negatives as N

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--draws", type=int, default=3); ap.add_argument("--seed", type=int, default=20260919)
    ap.add_argument("--sds", default="0.00,0.05,0.10,0.15,0.20,0.25")
    a = ap.parse_args()
    coh = pd.read_csv(ROOT / "protocol" / "COHORT-FROZEN-2026-09-18.csv").head(a.limit)
    rows = []
    for sd in [float(x) for x in a.sds.split(",")]:
        N.SD_TERRITORY_SHARE = sd
        rng = np.random.default_rng(a.seed)     # same seed every arm
        t0, got = time.time(), []
        for _, r in coh.iterrows():
            try:
                res, _, why = N.run_instance(Path(a.root), r, "leaky", a.draws, rng)
                got += res
            except Exception as e:
                print(f"  fail {r.scan}_{r.side}: {e.__class__.__name__}: {e}", file=sys.stderr)
        df = pd.DataFrame(got)
        ok = df[df.status == "ok"] if len(df) else df
        if not len(ok):
            print(f"sd={sd}: no ok rows"); continue
        rows.append(dict(sd=sd, n=len(ok),
                         resid_median=ok.outlet_flow_residual.median(),
                         resid_p10=ok.outlet_flow_residual.quantile(.1),
                         resid_p90=ok.outlet_flow_residual.quantile(.9),
                         pass_rate=ok.passes_check.mean(),
                         dffr_abs_median=ok.dFFR.abs().median(),
                         dffr_abs_p90=ok.dFFR.abs().quantile(.9),
                         flips=int(ok.flip.sum()),
                         C_ratio_iqr=ok.C_ratio.quantile(.75) - ok.C_ratio.quantile(.25)))
        print(f"sd={sd:.2f}  n={len(ok):4d}  resid med {rows[-1]['resid_median']:.4f}  "
              f"pass {rows[-1]['pass_rate']:.0%}  |dFFR| med {rows[-1]['dffr_abs_median']:.4f}  "
              f"({time.time()-t0:.0f}s)", flush=True)
    out = pd.DataFrame(rows); out.to_csv(HERE / "sweep_share_sd.csv", index=False)
    print("\n", out.to_string(index=False))

if __name__ == "__main__":
    main()
