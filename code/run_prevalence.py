"""
run_prevalence.py — Gate E0: baseline 0D FFR distribution over ImageCAS-X trees.

Decision rule (STUDY-PLAN-v2 §E0): if fewer than ~40 trees have a main-vessel FFR in 0.70-0.90, add the
virtual-stenosis severity-sweep cohort. Two demand models x three flow scales, so the verdict is not an artefact of
one hyperaemic-flow assumption:
  murray    : Q = k r_inlet^3            (self-scales with vessel size; primary)
  territory : fixed 6.5 mL/s total, split LCA/RCA by dominance   (check)

usage: run_prevalence.py <data_root> [--split test|val|train|all] [--limit N]
       run_prevalence.py --summarise <csv>
"""
from __future__ import annotations
import argparse, sys, time, traceback
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from imagecasx_loader import load_tree

TOTAL_HYP_FLOW = 6.5e-6                                   # m^3/s, whole heart at maximal vasodilation
SHARE = {"r": (0.70, 0.30), "l": (0.82, 0.18), "c": (0.76, 0.24)}   # (LCA, RCA) by dominance R / L / Co

def territory_flow(dominance, side):
    lca, rca = SHARE.get(str(dominance).strip().lower()[:1], SHARE["r"])
    return TOTAL_HYP_FLOW * (lca if side == "left" else rca)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--split", default="test")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", default=None)
    a = ap.parse_args(); root = Path(a.root)
    desc = pd.read_excel(root / "Descriptors.xlsx"); desc.columns = [c.strip() for c in desc.columns]
    desc["Scan ID"] = desc["Scan ID"].astype(int)
    desc = desc[desc["Image Quality"] > 0]                # quality 0 == excluded scans
    ids = desc["Scan ID"].tolist()
    if a.split != "all":
        keep = {int(l.strip()) for l in (root / "filelist" / f"{a.split}.txt").read_text().splitlines() if l.strip()}
        ids = [i for i in ids if i in keep]
    if a.limit: ids = ids[: a.limit]
    out = Path(a.out or (Path(__file__).parent.parent / "results" / f"E0_prevalence_{a.split}.csv"))
    out.parent.mkdir(parents=True, exist_ok=True)
    rows, fails, t0 = [], 0, time.time()
    for n, sid in enumerate(ids, 1):
        meta = desc[desc["Scan ID"] == sid].iloc[0]
        mask = root / "segmentations" / f"{sid}.coronary.nii.gz"
        for side in ("left", "right"):
            vtk = root / "centerlines" / f"{sid}.coronary_{side}_centerline.vtk"
            if not vtk.exists(): continue
            try:
                tree = load_tree(str(vtk), str(mask), name=f"{sid}_{side}")
                for mode in ("murray", "territory"):
                    for scale in (0.7, 1.0, 1.3):
                        o = tree.ffr(mode=mode, scale=scale, Q_territory=territory_flow(meta["Dominance"], side))
                        o.update(scan=sid, side=side, dominance=meta["Dominance"], disease=meta["Disease"],
                                 quality=int(meta["Image Quality"]))
                        rows.append(o)
            except Exception as e:
                fails += 1
                print(f"  FAIL {sid} {side}: {e.__class__.__name__}: {e}", file=sys.stderr)
                if fails <= 3: traceback.print_exc()
        if n % 20 == 0:
            print(f"  {n}/{len(ids)} scans  {len(rows)} rows  {fails} failures  {time.time()-t0:.0f}s", flush=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"\nwrote {out}  ({len(rows)} rows, {fails} tree failures, {time.time()-t0:.0f}s)")
    summarise(out)

def summarise(csv_path):
    df = pd.read_csv(csv_path)
    bands = [(0, 0.70), (0.70, 0.75), (0.75, 0.80), (0.80, 0.85), (0.85, 0.90), (0.90, 1.01)]
    trees = df[(df["mode"] == "murray") & (df["scale"] == 1.0)]
    print(f"\n=== E0 PREVALENCE — {len(trees)} trees from {trees.scan.nunique()} scans "
          f"({int((trees.groupby('scan').disease.first()=='yes').sum())} disease-labelled) ===")
    print(f"inlet radius mm: median {trees.r_in_mm.median():.2f} (IQR {trees.r_in_mm.quantile(.25):.2f}-{trees.r_in_mm.quantile(.75):.2f});"
          f"  demand mL/s median {trees.Q_demand_mls.median():.2f};  trees with >=1 resolved lesion: {int((trees.n_lesions>0).sum())}")
    for metric, title in (("min_ffr_main", "MIN FFR over resolved main vessels (LM/LAD/LCx/RCA)"),
                          ("lesion_ffr20", "FFR 20 mm distal to the tightest resolved main-vessel lesion")):
        print(f"\n--- {title} ---")
        print(f"{'model':<10}{'scale':>6} {'n':>5} {'median':>7} | " + " ".join(f"[{lo:.2f},{hi:.2f})" for lo, hi in bands) + " | in[0.70,0.90)")
        for (mode, scale), g in df.groupby(["mode", "scale"]):
            x = g[metric].dropna(); n = len(x)
            cnt = [int(((x >= lo) & (x < hi)).sum()) for lo, hi in bands]
            near = int(((x >= 0.70) & (x < 0.90)).sum())
            print(f"{mode:<10}{scale:>6.1f} {n:>5} {x.median():>7.3f} | " + " ".join(f"{c:>11d}" for c in cnt) + f" | {near:>5d}")
    prim = trees["min_ffr_main"].dropna()
    near = int(((prim >= 0.70) & (prim < 0.90)).sum()); flip = int(((prim >= 0.75) & (prim < 0.85)).sum())
    print(f"\nPRIMARY (murray x1.0): trees in [0.70,0.90) = {near};  in the flip-prone band [0.75,0.85) = {flip};  <= 0.80 = {int((prim<=0.80).sum())}")
    print("VERDICT: " + ("natural cohort sufficient near threshold" if near >= 40
                         else "BELOW 40 -> add the virtual-stenosis severity sweep (decision rule)"))

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--summarise":
        summarise(sys.argv[2])
    else:
        main()
