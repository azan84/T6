"""
negatives.py — the detector's NEGATIVE class (DETECTOR-SPEC v0.2 §5).

WHAT A NEGATIVE IS. The positives (from ablation.py) are models built on CORRUPTED anatomy that pass their own
perfusion check and are still materially wrong. A negative is the opposite case a deployed pipeline must not be
flagged for: **correct anatomy, whose validation targets are noisy** — because the patient varies and the
measurement varies. The detector's job is to separate those two, and it is only a real job if the negatives are
themselves imperfect.

WHY THE OBVIOUS NEGATIVE IS USELESS. An unperturbed clean model matches its own targets to ~1e-9, so
"residual > 0.001" would separate the classes perfectly and mean nothing at deployment (measured: AUC 0.82-0.90 in
the reviewer's probe). The negatives must carry noise the single tuning parameter CANNOT absorb.

WHICH NOISE, AND WHERE IT GOES. All of it lands on the TRUTH side: the model stays nominal and deterministic, and
the targets it is asked to match are drawn from a perturbed patient and measured imperfectly. That is the
deployment situation exactly.

  cardiac output      truth   Tree.demand(scale=)      absorbed by a global scaling -- on its own it is degenerate
  mean arterial P     truth   P_in argument            mostly absorbed
  haematocrit -> mu   truth   Tree.mu (parameterised 2026-09-19 for this)
  heart rate          --      NOT REPRESENTED: this is a steady model. Stated, not silently omitted.
  territory share     truth   built here               NOT absorbable by one global parameter -- this is the point
  measurement noise   truth   built here               NOT absorbable -- and it is what makes the 10 % check an
                                                       operating characteristic rather than an arbitrary constant

THE STATISTIC TO INJECT AT IS THE WITHIN-SUBJECT SD, NOT THE REPEATABILITY COEFFICIENT, and getting this wrong
inflates the negatives' residuals by ~2.8x and makes the detector look far better than it is. RC = 2.77 x within-
subject SD is the 95 % bound on the difference between TWO measurements; here the model is deterministic and only
the target is measured, so one SD is the correct dispersion
(references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md).

usage: negatives.py <data_root> [--cohort <csv>] [--beds leaky,discrete] [--draws N] [--seed S] [--out <csv>]
"""
from __future__ import annotations
import argparse, sys, time, traceback
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree, P_AORTA, P_VEN, MU
from severity_sweep import load, plan, insert, HOSTS
from ablation import (THRESHOLD, VALIDATED_RESIDUAL, bed_flow, territories, subtree,
                      run_id_of, sc_covariates, pullback_rows)

# ----------------------------------------------------------------------------------------------- the noise model
# CITATIONS RESOLVED 2026-09-19 — references/CITATION-PHYSIOLOGICAL-SDS-2026-09-19.md. Every value below moved, and
# the earlier placeholders were wrong by factors of 2 to 8. What the lookup established:
#
#   Tanade C, Chen SJ, Leopold JA, Randles A. Front Med Technol 2022;4:1034801, doi 10.3389/fmedt.2022.1034801
#   publishes only TWO of the four SDs STATISTICS-PLAN §6 asks for: cardiac output N(1, 0.153) and MAP N(1, 0.056),
#   both RELATIVE. Heart rate and haematocrit have no SD anywhere in that paper -- both were fixed to cohort
#   constants because its Sobol analysis found they did not matter. §6 as written could not be executed.
#
#   THE DECISIVE POINT ABOUT WHICH STATISTIC TO USE. Tanade's CoVs are literature-derived and the cardiac-output
#   one traces to Dubin 1990, a Doppler-vs-thermodilution METHOD-COMPARISON study (+/-0.69 L/min over 4.5 = 0.153).
#   That is inter-instrument disagreement, not the same patient varying between occasions. A negative draw here
#   represents ONE patient measured again, so the right quantity is the WITHIN-SUBJECT SD. The gap is not subtle:
#   population CV of cardiac index is ~30.9 % against a within-subject 5.44 % (Taeger 2015) -- a factor of 5.7, and
#   exactly the trap the old SD_MAP_MMHG = 10.0 had fallen into by sitting near the population SD.
SD_CO = 0.05            # cardiac output, relative, WITHIN-SUBJECT. Taeger 2015 doi 10.1002/ehf2.12040 (CV_I 5.44 %,
                        # weekly, in patients); Lassen 2023 doi 10.1007/s12350-023-03308-1 (5.0 % rest / 3.1 %
                        # adenosine). Use 0.10 instead ONLY if this constant is meant to absorb measurement error
                        # too -- it is not: measurement lives in WSCV_TARGET below.
SD_MAP_REL = 0.056      # mean arterial pressure, RELATIVE. Tanade Table 1, and independently consistent with
                        # propagating Stergiou/Muntner within-subject figures (4.1-5.7 mmHg at a 90 mmHg mean).
SD_MU = 0.02            # viscosity via haematocrit, relative. Coskun 2018 doi 10.1515/cclm-2017-1155 (Hct CV_I
                        # 2.82 %) propagated through mu = mu0/(1 - phi). Defensible band 0.02-0.04. The previous
                        # 0.15 was 7-8x too large.
# HEART RATE IS NOT REPRESENTED. No SD exists to use, and this is a steady model with no handle for it. Stated in
# STATISTICS-PLAN §6 as a limitation rather than quietly dropped.

# These two are NOT physiological scatter — they are what makes the class non-degenerate, and they are the terms a
# single global bed scaling cannot remove.
# CITATION SEARCHED 2026-09-19 — references/CITATION-TERRITORY-SHARE-2026-09-19.md. Verdict: NO SINGLE VALUE IS
# SUPPORTABLE, so 0.10 stays as the pre-registered primary and is declared a CHOSEN value, not a cited one, with
# the detector's specificity reported across a band (see SHARE_SENSITIVITY below).
#
# THE CONSTANT SPANS TWO LEGS AND ONLY ONE IS MEASURED.
#   mass -> flow  (does each gram of myocardium get equal flow?) -- well measured at 0.07-0.15 by an independent
#                 method family: Chareonthaitawee 2001 within-subject between-region CV 17 +/- 10 % at hyperaemia;
#                 Bassingthwaighte 1989's fractal scale law ~7 % at territory scale; Choy & Kassab 2008 15.2 %.
#   calibre -> mass  (does vessel size predict the mass it feeds?) -- NOT cleanly isolated anywhere in the
#                 literature. The model needs BOTH legs, so a figure for the first alone under-states it.
#
# THE CLOSEST DIRECT MEASUREMENT: Keulards et al., Heart 2020;106:1489-94, doi 10.1136/heartjnl-2020-316689.
# 35 near-normal patients; compares an anatomical downstream-vascular-volume prediction of each territory's share
# against invasively measured hyperaemic flow share. SD of the paired difference 6.2 / 7.4 / 3.4 percentage points
# (LAD / LCx / RCA) -> 0.147 / 0.273 / 0.111 relative; after removing measurement error and undoing this model's
# renormalisation, 0.170 / 0.281 / 0.051, RMS 0.192.
#
# SO 0.10 IS DEFENSIBLE BUT SITS AT THE LOW END, AND LOW IS THE UNSAFE DIRECTION: under-setting it makes the
# negative class too easy and INFLATES the specificity DETECTOR-SPEC §5 reports. Kept at 0.10 because it is what was
# pre-specified and the sensitivity band carries the uncertainty honestly; a reader who prefers 0.19 can read the
# specificity straight off the band.
SD_TERRITORY_SHARE = 0.10
# Pre-registered sensitivity: the detector's specificity is reported at every one of these, not at 0.10 alone.
# Do NOT extend past 0.20 -- above it the Gaussian share draw starts producing fits at the search bound (3/100).
SHARE_SENSITIVITY = (0.05, 0.10, 0.15, 0.20)
#
# SYSTEMATIC COMPONENT — DECLARED, NOT MODELLED. The departure is not purely random: LAD territories run ~5 pp
# over-perfused and RCA/inferior lowest, replicated across Keulards 2020, Fournier 2021, Brown 2023 (CMR, n=150,
# p<0.001) and Kamani 2025 (n=138). But it weakens or vanishes at HYPERAEMIA (Brown 2018 null at stress;
# Lyu 2022 P=0.399), LAD-vs-LCx does not replicate (Piccinelli 2020 has LCx highest), and three modalities each
# carry a septum-specific artefact pointing the same way. This model's territories are not vessel-identified, so a
# per-vessel bias could not be applied faithfully even if it were wanted. Declared in the limitations.
#
# Per-territory hyperaemic MBF within-subject CoV. The one figure here with a source: RC 23 % regional
# (Lubberink 2024, 15O-water, same-day, n=10) -> wsCV = 23 / 2.77 = 8.3 %. Conference abstract; see the citation doc.
WSCV_TARGET = 0.083
# ⚠ CONTESTED 2026-09-19, and in the same direction as SD_TERRITORY_SHARE: Kaufmann 1999 reports a REGIONAL
# hyperaemic within-subject CV of 15-21 %, roughly DOUBLE this. Our 0.083 derives from Lubberink 2024's regional
# RC of 23 % (/2.77), a conference abstract with n = 10. Both noise terms in this file therefore sit at the low end
# of their plausible ranges, and both err toward making the negative class EASY -- which inflates the detector's
# specificity. Resolve before the detector's numbers are reported; until then the specificity is an upper bound.

def perturbed_targets(t: Tree, C_clean: float, r_clean: np.ndarray, terr, rng: np.random.Generator):
    """One draw of a noisy truth for a CLEAN tree. Returns (targets, the draw's parameters).

    Step 1 perturbs the patient and re-solves, so the true territory flows move together and physiologically.
    Steps 2-3 then break the Murray proportions and measure the result imperfectly — neither of which a single
    global scaling can undo, which is the whole reason the negatives are not trivially separable.
    """
    co = float(rng.normal(1.0, SD_CO))
    map_pa = P_AORTA * float(rng.normal(1.0, SD_MAP_REL))     # RELATIVE, per Tanade Table 1
    mu = float(rng.normal(MU, SD_MU * MU))
    co, mu, map_pa = max(co, 0.2), max(mu, 0.2 * MU), max(map_pa, 40 * 133.322)

    mu_saved, C_saved = t.mu, dict(t._C)
    t.mu = mu; t._C.clear()                       # a cached C was calibrated at the old viscosity
    try:
        C_true = t.calibrate(t.demand("murray", co), map_pa, P_VEN)
        ffr_t, _, info_t, _, _ = t.evaluate(C_true, r_clean, map_pa, P_VEN)
        q_true = bed_flow(t, C_true, ffr_t) * (map_pa / P_AORTA)   # bed_flow assumes P_AORTA; rescale to this draw
        tgt = np.array([float(q_true[sub].sum()) for sub in terr])
    finally:
        t.mu = mu_saved; t._C.clear(); t._C.update(C_saved)

    share = rng.normal(1.0, SD_TERRITORY_SHARE, size=len(tgt))
    tgt_shared = tgt * share
    if tgt_shared.sum() > 0:                      # renormalise: the share noise REDISTRIBUTES, it does not create flow
        tgt_shared *= tgt.sum() / tgt_shared.sum()
    measured = tgt_shared * rng.normal(1.0, WSCV_TARGET, size=len(tgt))
    return np.maximum(measured, 1e-12), dict(draw_co=co, draw_map_mmhg=map_pa / 133.322, draw_mu=mu,
                                             draw_share_sd=SD_TERRITORY_SHARE, draw_wscv=WSCV_TARGET)

def fit_global_scaling(t: Tree, r: np.ndarray, terr, targets):
    """Protocol C's fit, identical in form to ablation.py: ONE global bed scaling, global grid scan then Brent."""
    t._C.clear(); C_start = t.calibrate(t.demand("murray", 1.0))
    lo_b, hi_b = np.log10(C_start) - 1.5, np.log10(C_start) + 1.5
    def loss(lc):
        f, _, _, _, _ = t.evaluate(10 ** lc, r)
        q = bed_flow(t, 10 ** lc, f)
        pred = np.array([q[sub].sum() for sub in terr])
        return float(np.mean(((pred - targets) / targets) ** 2))
    grid = np.linspace(lo_b, hi_b, 61); lv = np.array([loss(x) for x in grid]); k = int(np.argmin(lv))
    res = minimize_scalar(loss, bounds=(grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]),
                          method="bounded", options=dict(xatol=1e-9))
    lc = float(res.x) if float(res.fun) <= lv[k] else float(grid[k])
    n_basins = int(sum(1 for i in range(1, len(lv) - 1) if lv[i] < lv[i - 1] and lv[i] < lv[i + 1]))
    at_bound = bool(min(abs(lc - lo_b), abs(lc - hi_b)) < 1e-6)
    return 10 ** lc, C_start, n_basins, at_bound

def run_instance(root: Path, row, bed: str, draws: int, rng):
    out, pull = [], []
    t = load(root, int(row.scan), row.side, bed)
    o = t.ffr("murray", 1.0); C_clean = o["C"]
    sl = next((s for s in plan(t, row.side, t.last["ffr"].copy())[0]
               if s["vessel"] == row.vessel and s["loc"] == row["loc"] and abs(s["L"] * 1e3 - row.L_mm) < 1e-6), None)
    if sl is None: return out, pull, "slot not eligible under this bed"
    path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
    meas = int(path[mi])
    r_clean, _ = insert(t, path, s_arc, c, L, row.ds_pct / 100)
    ffr0, _, info0, _, _ = t.evaluate(C_clean, r_clean)
    f0 = float(ffr0[meas])
    terr = [sub for sub in territories(t)]
    if len(terr) < 2: return out, pull, "fewer than 2 territories — Protocol C not applicable"

    base = dict(scan=int(row.scan), side=row.side, vessel=row.vessel, loc=row["loc"], L_mm=row.L_mm,
                ds_pct=int(row.ds_pct), bed=bed, band_cohort=row.band, ffr_clean=f0,
                error_type="negative", protocol="C_flowmatched", n_territories=len(terr), **sc_covariates(t))
    for d in range(draws):
        rid = run_id_of(row, bed, "negative", f"draw{d}")
        rec = {**base, "run_id": rid, "draw": d, "status": "ok"}
        try:
            targets, params = perturbed_targets(t, C_clean, r_clean, terr, rng)
            rec.update(params)
            C2, C_start, nb, at_bound = fit_global_scaling(t, r_clean, terr, targets)
            ffr2, Q2, info2, _, _ = t.evaluate(C2, r_clean)
            qb = bed_flow(t, C2, ffr2)
            pred = np.array([qb[sub].sum() for sub in terr])
            resid = float(np.sqrt(np.mean(((pred - targets) / targets) ** 2)))
            f2 = float(ffr2[meas])
            rec.update(C_clean=C_clean, C=C2, C_abs=C2, C_ratio=C2 / C_clean, ffr=f2, dFFR=f2 - f0,
                       flip=int((f2 <= THRESHOLD) != (f0 <= THRESHOLD)),
                       outlet_flow_residual=resid, passes_check=int(resid < VALIDATED_RESIDUAL),
                       fit_n_basins=nb, fit_at_bound=at_bound,
                       inflow_mls=info2["inflow"] * 1e6, converged=bool(info2["converged"]))
            if at_bound: rec["status"] = "failed fit: optimum at search bound"
            else: pull += pullback_rows(t, path, s_arc, c, L, meas, ffr2, Q2, info2["inflow"], rid)
        except Exception as e:
            rec["status"] = f"error: {e.__class__.__name__}: {e}"
        out.append(rec)
    return out, pull, ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--cohort", default=None)
    ap.add_argument("--beds", default="leaky,discrete"); ap.add_argument("--draws", type=int, default=1)
    ap.add_argument("--seed", type=int, default=20260919); ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default=None)
    a = ap.parse_args(); root = Path(a.root); here = Path(__file__).parent.parent
    coh = pd.read_csv(a.cohort or here / "protocol" / "COHORT-FROZEN-2026-09-18.csv")
    if a.limit: coh = coh.head(a.limit)
    out_path = Path(a.out or here / "results" / "negatives.csv")
    rng = np.random.default_rng(a.seed)
    rows, pulls, t0, fails = [], [], time.time(), 0
    # ONE draw per instance per replicate, NOT 1,000 draws against ~60 positives: DeLong's variance assumes
    # independent negatives, and a 1,000:1 imbalance with within-instance correlation violates it (DETECTOR-SPEC §5).
    print(f"{len(coh)} instances x {len(a.beds.split(','))} beds x {a.draws} draw(s), seed {a.seed}\n")
    for n, (_, r) in enumerate(coh.iterrows(), 1):
        for bed in a.beds.split(","):
            try:
                res, pl, why = run_instance(root, r, bed, a.draws, rng)
                if why: fails += 1; print(f"  SKIP {r.scan}_{r.side} {bed}: {why}", file=sys.stderr)
                rows += res; pulls += pl
            except Exception as e:
                fails += 1; print(f"  FAIL {r.scan}_{r.side} {bed}: {e.__class__.__name__}: {e}", file=sys.stderr)
                if fails <= 3: traceback.print_exc()
        if n % 10 == 0: print(f"  {n}/{len(coh)}  {len(rows)} rows  {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows); out_path.parent.mkdir(exist_ok=True); df.to_csv(out_path, index=False)
    pd.DataFrame(pulls).to_csv(out_path.with_name(out_path.stem + "_pullback.csv"), index=False)
    print(f"\nwrote {out_path}  ({len(df)} rows, {fails} skips, {time.time()-t0:.0f}s)")
    ok = df[df.status == "ok"]
    if len(ok):
        print(f"\nNEGATIVE CLASS — the check that matters: are these non-degenerate?")
        print(f"  residual: median {ok.outlet_flow_residual.median():.4f}  "
              f"p10 {ok.outlet_flow_residual.quantile(.1):.4f}  p90 {ok.outlet_flow_residual.quantile(.9):.4f}")
        print(f"  passes the {VALIDATED_RESIDUAL:.0%} check: {int(ok.passes_check.sum())}/{len(ok)} "
              f"({100*ok.passes_check.mean():.0f}%)  <- DETECTOR-SPEC §5 predicts ~77 %")
        print(f"  |dFFR| median {ok.dFFR.abs().median():.4f}  flips {int(ok.flip.sum())}")
        print(f"     ^ NOT expected to be ~0, and this is the single most useful number here: the anatomy is")
        print(f"       CORRECT, so this is the FFR error a perfectly-segmented model still makes when it is tuned")
        print(f"       to a noisy measurement. It is the irreducible noise floor on dFFR, and it must be reported")
        print(f"       beside every injected-error effect (STATISTICS-PLAN §6). Compare it with MATERIAL_DFFR =")
        print(f"       {0.05:.2f}: if the floor approaches the material threshold, the positives are only modestly")
        print(f"       separated from correct models and H5's ceiling is set by physiology, not by the detector.")
        print(f"  C_ratio: median {ok.C_ratio.median():.4f}  IQR "
              f"[{ok.C_ratio.quantile(.25):.4f}, {ok.C_ratio.quantile(.75):.4f}]  <- S_C's null spread")

if __name__ == "__main__":
    main()
