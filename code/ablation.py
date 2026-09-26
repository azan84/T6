"""
ablation.py — the primary experiment: 4 segmentation-error types x 3 boundary-condition protocols x 2 bed structures,
on the frozen cohort.

THE THESIS THIS TESTS. A reduced-order FFR model can be re-tuned after a segmentation error until it reproduces its
outlet flow targets — and still move the FFR <= 0.80 decision. "Error absorbed at calibration is error committed at
deployment."

THE THREE PROTOCOLS (CFD-ARM-SPEC v0.2 §2.2-2.3, STUDY-PLAN-v2 §E2 banner)
  A  fixed        outlet conductances keep their CLEAN values; deleted outlets simply vanish. The naive case.
  B  re-derived   the bed rule is re-applied to the corrupted geometry and C re-calibrated to the corrupted tree's
                  own Murray demand. This is what a deployed pipeline actually does to wrong anatomy.
  C  flow-matched ONE global bed scaling is tuned so the SURVIVING outlets reproduce the clean model's outlet FLOWS.
                  This is the "validated" model — it passes its own check.

  WHY FLOW ONLY, NOT PRESSURE. In a steady tree, if the outlets distal to a lesion reproduce the baseline's pressure
  AND flow, then the distal pressure — hence FFR — is the baseline's by construction and no decision can flip. The
  thesis is only testable, and only clinically meaningful, for FLOW (perfusion-type) targets; nobody measures
  coronary outlet pressure. Matching both was specified in an earlier draft and would have made H2 unfalsifiable.

  FOSSAN CONSTRAINTS, as far as this model supports them: exactly ONE free parameter against N >= 2 outlet targets
  (so the fit is over-determined, not "one equation, one unknown"); the bed rule and Murray exponent stay at their
  population values and are never re-fitted per case. NOT implemented: resting-state re-simulation with
  autoregulation-coupled resistance — this steady hyperaemic model has no autoregulation. Declared limitation.

OUTPUT one row per (instance, bed, error type, protocol) with the paired endpoints: dFFR against that instance's own
clean baseline IN THAT BED, the flip indicator, and the outlet-flow residual that makes absorption visible.

usage: ablation.py <data_root> [--cohort <csv>] [--beds leaky,discrete] [--limit N] [--out <csv>]
"""
from __future__ import annotations
import argparse, sys, time, traceback
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize_scalar

sys.path.insert(0, str(Path(__file__).parent))
from zerod_ffr import Tree, P_AORTA, P_VEN, R_TRUNC, R_TRUNC_DISCRETE, K_MURRAY
from severity_sweep import load, plan, insert, HOSTS, RUNOFF
from error_types import ERROR_TYPES, TOPOLOGICAL, T3_LENGTH_DELTA, T4_RADIUS_SCALE, T2_KEEP_BEYOND
import severity_sweep as ss

# DECISION B2's guard, 2026-09-19. T2 truncates the host vessel T2_KEEP_BEYOND past the lesion's distal edge, and the
# FFR endpoint is read RUNOFF past it. If KEEP <= RUNOFF the truncation deletes the measurement node -- which is
# exactly what happened (15 mm vs 20 mm), silently, in 0 of 30 frozen 3D instances did it survive, and
# error_types.t2_truncation's own docstring claimed the opposite. The two constants live in different modules, so
# nothing connected them. This assert connects them: it fires at import, not after a 12-minute run.
assert T2_KEEP_BEYOND > RUNOFF, (
    f"T2_KEEP_BEYOND ({T2_KEEP_BEYOND*1e3:.1f} mm) must EXCEED RUNOFF ({RUNOFF*1e3:.1f} mm), or T2 deletes the "
    f"measurement node it is defined to preserve and the endpoint is read at a boundary condition instead of a "
    f"computed interior pressure (decision B2)")

THRESHOLD = 0.80
# "The model matches its validation target" cannot mean an arbitrary number. It means: the predicted territory
# perfusion agrees with the measured value to within the precision of the measurement.
#
# CITATION RESOLVED 2026-09-19 (references/CITATION-VALIDATED-RESIDUAL-2026-09-19.md). The VALUE stands at 0.10; the
# JUSTIFICATION THAT STOOD HERE WAS WRONG and is replaced, because it conflated two statistics that differ by ~2.8x:
#   * within-subject COEFFICIENT OF VARIATION (wsCV) — the spread of one measurement about its own mean;
#   * REPEATABILITY COEFFICIENT (RC ~= 2.77 x within-subject SD) — the 95 % bound on the difference of TWO
#     independent measurements.
# The old comment quoted "10-15 %" (a wsCV figure, traceable to Schindler et al., JACC Cardiovasc Imaging 2023;
# 16(4):536-548, doi 10.1016/j.jcmg.2022.12.015: "coefficients of variation (CoV) of ~10% for same day ... 15% to
# 20% for different day") while PHRASING it as an agreement bound. Those are not the same quantity.
#
# WHY 0.10 IS NEVERTHELESS THE RIGHT NUMBER HERE, and it is not the RC:
# this residual compares a DETERMINISTIC model output against ONE noisy measurement — one noise draw, not two — so
# the RC's factor of sqrt(2) does not apply. The statistically correct 95 % bound for this comparison is ~0.13-0.16
# at the published per-territory hyperaemic wsCV. 0.10 sits just BELOW that band: it is a STRICTER check than the
# measurement precision strictly requires, and it is strict in the safe direction, because the headline proportion
# P(passes the check AND is materially wrong) is monotone non-decreasing in the threshold. A looser, equally
# defensible threshold could only INCREASE the absorption count, so 0.10 makes H2 conservative. That argument, not
# the citation, is the real defence of the number.
#
# PER-TERRITORY IS MATERIALLY WORSE THAN GLOBAL (~1.5x) and the check is per-territory: RC 15 % whole myocardium ->
# 23 % regional -> 27 % segmental in the one study measuring all three on the same subjects (Lubberink et al.,
# EHJCI 2024;25(Suppl 1):jeae142.093 — 15O-water, same-day, n=10; NOTE: conference abstract, small n, "regional"
# undefined). Independently, Brown et al., JCMR 2018;20:48, doi 10.1186/s12968-018-0462-y (open access) reports
# both statistics on one dataset: wsCV 11 % stress vs RC 29 % global / 30-37 % regional.
# "CT perfusion" has been dropped from this justification: the only human test-retest CTP MBF study has its two
# scans a median 795 days apart and reports neither CV nor RC. The claim is PET-based.
#
# Set BEFORE the ablation was run on more than 6 pilot instances, and BEFORE registration. An earlier draft used 1 %,
# which a pilot showed is unreachable with a single free parameter against 2-3 targets — i.e. it would have made H2
# fail for a reason about the tuning parameterisation rather than about physiology.
VALIDATED_RESIDUAL = 0.10
MATERIAL_DFFR = 0.05        # an FFR error large enough to matter clinically near the 0.80 cut

def node_map(clean: Tree, corrupt: Tree):
    """corrupted node -> clean node, by coordinate. Node INDICES are not stable across a topology change."""
    key = {tuple(np.round(x, 9)): i for i, x in enumerate(clean.xyz)}
    return np.array([key.get(tuple(np.round(x, 9)), -1) for x in corrupt.xyz])

def bed_flow(tree: Tree, C: float, ffr: np.ndarray) -> np.ndarray:
    """Flow leaving the network at each node through the microvascular bed (m^3/s)."""
    return tree.w / C * (ffr * P_AORTA - P_VEN)

CALIBRE_ONLY = ("T3_stenosis_length", "T4_taper")   # change no topology, so must not change the modelled node set

def protocol_c_targets(t: Tree, t2: Tree, m: np.ndarray, q0_all: np.ndarray):
    """Protocol C's targets: (corrupted member nodes, clean target flow) per territory. Decision B1.

    THE PARTITION IS THE CLEAN TREE'S, NOT THE CORRUPTED TREE'S. Taking territories from the corrupted tree looks
    right and fails two ways, both measured on a 25-instance probe: (i) if the error removes the tree's first
    bifurcation the corrupted partition roots DEEPER, and the clean subtree below that deeper point EXCLUDES the
    deleted branch -- 2 of 174 rows targeted as little as 33 % of the clean territory flow; (ii) if the corrupted
    tree stops branching at all there is no partition and Protocol C was skipped entirely -- 27 of 174 rows. The
    clean territories are a fixed anatomical partition the error cannot move, so the target is well defined however
    the topology is damaged, and each corrupted node is assigned to the territory its CLEAN counterpart belongs to.

    Lives here, not inline in run_instance, so that a check can exercise the REAL code path: the first version of
    the invariant test re-implemented this logic and therefore passed against a copy while the implementation went
    untested.
    """
    terr_clean = territories(t)
    owner = {int(v): j for j, sub in enumerate(terr_clean) for v in sub}
    pairs = []
    for j, sub_c in enumerate(terr_clean):
        q_clean = float(q0_all[sub_c].sum())                  # clean subtree = FULL territory, incl. deleted parts
        members = np.array([v for v in range(len(t2.parent))
                            if t2.active[v] and m[v] >= 0 and owner.get(int(m[v]), -1) == j], dtype=int)
        if q_clean > 0 and len(members): pairs.append((members, q_clean, sub_c))
    # TRIPLES, not pairs: the clean territory travels with its own target. Territories with no surviving member are
    # dropped, so an index into this list does NOT index territories(t) -- carrying sub_c removes that trap.
    return pairs

def trunc_for(bed: str, etype: str) -> float:
    """Truncation radius for a corrupted tree.

    DECISION B3, settled 2026-09-19. T4 scales every distal radius by 0.930, which drags r_ref down with it, which
    pushes leaves below a FIXED truncation radius and deletes them. That is a modelling artefact, not a consequence
    of the segmentation error: T4 says the lumen was read ~7 % narrow, and the vessels are still there. Left
    unfixed it was severe -- Protocol A wrote `closed` for 66 of 133 discrete outlets, 9 of 30 instances lost their
    bed entirely, and T4 x A came out at dFFR +0.13 WITH THE WRONG SIGN (against -0.02 with the territory
    preserved). STATISTICS-PLAN §P3 currently cites "taper under Protocol A: 6 flips leaky vs 43 discrete" as a
    headline structure-dependent interaction; that contrast is this artefact.

    The truncation radius encodes the RESOLUTION LIMIT of the reference anatomy, so under a uniform calibre error it
    must move with the anatomy. Scaling it by the same factor keeps the active node set identical between clean and
    corrupted trees, which makes T4 what error_types.t4_taper says it is: "purely the ~1/scale^4 rise in viscous
    resistance -- an under-read lumen, not a fabricated stenosis". No other error type is affected: T1 and T2 change
    topology by construction, and T3 does not touch radii at all.
    """
    base = R_TRUNC if bed == "leaky" else R_TRUNC_DISCRETE
    return base * T4_RADIUS_SCALE if etype == "T4_taper" else base

def subtree(tree: Tree, v: int) -> np.ndarray:
    """Every node at or below v, on the tree's ACTIVE children lists."""
    out, stack = [], [int(v)]
    while stack:
        u = stack.pop(); out.append(u); stack += [int(x) for x in tree.children[u]]
    return np.array(out, dtype=int)

def territories(tree: Tree):
    """Perfusion territories: the subtrees rooted at each child of the FIRST branching node.

    Protocol C's targets must mean the same thing in both bed structures. Leaf 'outlet flow' does not: in the
    discrete bed every unit of flow leaves at a leaf, but in the leaky bed most leaves the wall along the way, so
    matching leaf flows alone is matching a small and structurally different fraction of the bed — the smoke test
    showed residuals of 24.9 and 10.4 (i.e. the fit is ill-posed) in the leaky bed while behaving in the discrete one.
    TERRITORY flow — the total bed outflow of a subtree — is well defined in both, reduces to the sum of outlet flows
    in the discrete bed, and is the quantity a clinic can actually measure (CT perfusion / PET MBF per territory).
    Returns a list of node-index arrays, one per territory, or [] if the tree never branches."""
    br = next((v for v in np.where(tree.active)[0] if len(tree.children[v]) >= 2), None)
    if br is None: return []
    out = []
    for c in tree.children[br]:
        sub, stack = [], [int(c)]
        while stack:
            v = stack.pop(); sub.append(v); stack += [int(x) for x in tree.children[v]]
        out.append(np.array(sub, dtype=int))
    return out

PULLBACK_GRID_MM, PULLBACK_CAP, PULLBACK_MERGE_MM = 5.0, 40, 1.0

def run_id_of(row, bed: str, etype: str, proto: str) -> str:
    return (f"{int(row.scan)}_{row.side}_{row.vessel}_{row['loc']}_{int(row.L_mm)}mm_"
            f"{int(row.ds_pct)}ds_{bed}_{etype}_{proto or 'none'}")

def sc_covariates(tree: Tree) -> dict:
    """The anatomical covariates of DETECTOR-SPEC §3.1's closed form
    C_closed = (P_in - P_v) * sum(w) / (K * r_ref(root)^3), taken from the model being scored."""
    return dict(w_sum=float(tree.w.sum()), r_ref_root_mm=float(tree.r_ref[0] * 1e3),
                L_resolved_mm=float(tree.ds[tree.resolved].sum() * 1e3), n_outlets=int(len(tree.leaves)))

def pullback_rows(tree: Tree, path, s_arc, c, L, meas, ffr, Q, inflow, rid: str):
    """Per-station profile along the host vessel — DETECTOR-SPEC §7.2/§7.3.

    DEMOTED, and deliberately kept: no §3 detector statistic uses this (the reviewer showed every flow statistic
    along the tree is an exact function of anatomy x the model's own pressure solution). It exists for the mechanism
    figure, for the 0D-vs-3D pullback comparison, and so that the abandoned statistics stay checkable by a reviewer
    who asks. It must NEVER be shipped in a CFD package — it is a prediction.

    Stations are the same rule the exporter imposes on probes.csv so 0D and 3D sample the same places: a 5 mm grid
    to the last resolved node plus anchors at the lesion shoulders, throat and measurement node, anchors placed
    first so a grid point can never displace a named one.
    """
    res = tree.resolved[path]
    s_end = float(s_arc[res][-1]) if res.any() else float(s_arc[-1])
    anchors = [(float(c - L / 2), "lesion_prox"), (float(c), "throat"), (float(c + L / 2), "lesion_dist")]
    if meas in path: anchors.append((float(s_arc[int(np.argmin(np.abs(path - meas)))]), "measurement"))
    anchors = [(s, k) for s, k in anchors if 0.0 <= s <= s_end]
    for step in (PULLBACK_GRID_MM * 1e-3, 2 * PULLBACK_GRID_MM * 1e-3):
        merged = []
        for s, kind in sorted(anchors, key=lambda z: z[0]):
            if merged and abs(s - merged[-1][0]) < PULLBACK_MERGE_MM * 1e-3: continue
            merged.append((s, kind))
        for s in np.arange(0.0, s_end + 1e-12, step):
            if all(abs(float(s) - m0) >= PULLBACK_MERGE_MM * 1e-3 for m0, _ in merged):
                merged.append((float(s), "grid"))
        merged.sort(key=lambda z: z[0])
        if len(merged) <= PULLBACK_CAP: break
    rows = []
    for s, kind in merged:
        k = int(np.argmin(np.abs(s_arc - s))); v = int(path[k])
        # ROOT STATION: evaluate() returns Q[0] = 0 (the root has no parent element), so q_norm would be 0 and
        # ln q_norm -inf at the origin of every right tree. The inflow lives in info, and that is what belongs here.
        q = float(inflow) if v == 0 else float(Q[v])
        rref = float(tree.r_ref[v])
        # S_A ingredient (DETECTOR-SPEC §3.2), recorded raw at every junction so the statistic can be characterised
        # later WITHOUT re-running: Murray's books at a bifurcation. Not itself a pre-registered statistic yet.
        kids = tree.children[v]
        orphan = (float(rref ** 3 - sum(tree.r_ref[ch] ** 3 for ch in kids)) / rref ** 3) if (kids and rref > 0) else np.nan
        rows.append(dict(run_id=rid, station_mm=s * 1e3, s_from_lesion_mm=(s - c) * 1e3, kind=kind, node=v,
                         ffr=float(ffr[v]), Q_mls=q * 1e6, r_mm=float(tree.r[v] * 1e3), r_ref_mm=rref * 1e3,
                         r_fit_mm=float(tree.r_fit[v] * 1e3),
                         q_norm=q / (K_MURRAY * rref ** 3) if rref > 0 else np.nan,
                         n_children=len(kids), orphan_frac=orphan, resolved=int(tree.resolved[v])))
    return rows

def run_instance(root: Path, row, bed: str):
    """All error types x protocols for one cohort instance under one bed structure.

    Returns (main_rows, territory_rows, pullback_rows, why) — the three streams DETECTOR-SPEC §7 requires. The side
    files are long-format and keyed by run_id so the main table does not grow forty columns.
    """
    out, terr_out, pull_out = [], [], []
    t = load(root, int(row.scan), row.side, bed)
    o = t.ffr("murray", 1.0); C_clean = o["C"]
    slots, _ = plan(t, row.side, t.last["ffr"].copy())
    sl = next((s for s in slots if s["vessel"] == row.vessel and s["loc"] == row["loc"]
               and abs(s["L"] * 1e3 - row.L_mm) < 1e-6), None)
    if sl is None: return out, terr_out, pull_out, "slot not eligible under this bed"
    path, s_arc, c, L, mi = sl["path"], sl["s"], sl["c"], sl["L"], sl["mi"]
    meas_clean = int(path[mi]); ds = row.ds_pct / 100

    # --- the clean reference: correct anatomy, lesion present
    r_clean, _ = insert(t, path, s_arc, c, L, ds)
    ffr0, Q0, info0, _, _ = t.evaluate(C_clean, r_clean)
    if not info0["converged"]: return out, terr_out, pull_out, "clean solve did not converge"
    f0 = float(ffr0[meas_clean]); q0_all = bed_flow(t, C_clean, ffr0)
    base = dict(scan=int(row.scan), side=row.side, vessel=row.vessel, loc=row["loc"], L_mm=row.L_mm,
                ds_pct=int(row.ds_pct), bed=bed, band_cohort=row.band, ffr_clean=f0,
                flip_clean=int(f0 <= THRESHOLD), n_outlets_clean=len(t.leaves))

    # --- THE CLEAN ROW. DETECTOR-SPEC §7.4: the clean model needs its own row and its own run_id. Until now its
    # values were only ever copied into the corrupted rows as columns, so the uncorrupted model -- the thing every
    # dFFR is measured against, and the natural source of the detector's negative class -- had no record of its own.
    terr_clean = territories(t)
    rid0 = run_id_of(row, bed, "clean", "")
    out.append({**base, "run_id": rid0, "error_type": "clean", "protocol": "", "status": "ok",
                "meas_same_point": True, "n_outlets_shared": len(t.leaves), "n_territories": len(terr_clean),
                "C_clean": C_clean, "C": C_clean, "C_abs": C_clean, "C_ratio": 1.0,
                "ffr": f0, "dFFR": 0.0, "flip": 0, "flip_dir": "",
                "outlet_flow_residual": 0.0, "inflow_mls": info0["inflow"] * 1e6,
                "inflow_clean_mls": info0["inflow"] * 1e6, "converged": True,
                "iters": info0["iters"], "mass_err": info0["mass_err"], **sc_covariates(t)})
    pull_out += pullback_rows(t, path, s_arc, c, L, meas_clean, ffr0, Q0, info0["inflow"], rid0)
    for j, sub_c in enumerate(terr_clean):
        terr_out.append(dict(run_id=rid0, terr_id=j, root_node=int(sub_c[0]),
                             root_xyz_mm=";".join(f"{v:.4f}" for v in t.xyz[int(sub_c[0])] * 1e3),
                             Q_target_mls=float(q0_all[sub_c].sum()) * 1e6,
                             Q_achieved_mls=float(q0_all[sub_c].sum()) * 1e6, residual=0.0,
                             sum_w=float(t.w[sub_c].sum()), n_nodes=int(len(sub_c)),
                             n_outlets=int(sum(1 for v in sub_c if v in set(int(x) for x in t.leaves))),
                             contains_lesion=bool(meas_clean in sub_c), contains_error=False))

    for etype, fn in ERROR_TYPES.items():
        segs2, info = fn(list(t.segments), t, path, s_arc, c, L)
        if segs2 is None:
            out.append({**base, "run_id": run_id_of(row, bed, etype, ""), "error_type": etype, "protocol": "",
                        "status": f"skipped: {info}"}); continue
        try:
            t2 = Tree(segs2, f"{t.name}_{etype}", bed=bed, r_trunc=trunc_for(bed, etype),
                      trunc_ref=t if etype in CALIBRE_ONLY else None)
        except ValueError as e:
            out.append({**base, "run_id": run_id_of(row, bed, etype, ""), "error_type": etype, "protocol": "",
                        "status": f"skipped: {e}"}); continue
        m = node_map(t, t2)                                   # corrupted -> clean
        p2, _ = t2.vessel_path(HOSTS[row.side][row.vessel])
        if p2 is None or len(p2) < 3:
            out.append({**base, "run_id": run_id_of(row, bed, etype, ""), "error_type": etype, "protocol": "",
                        "status": "skipped: host vessel lost"}); continue
        s2 = t2.arc[p2] - t2.arc[p2[0]]
        L2 = L + T3_LENGTH_DELTA if etype == "T3_stenosis_length" else L
        if c + L2 / 2 >= s2[-1]:
            out.append({**base, "run_id": run_id_of(row, bed, etype, ""), "error_type": etype, "protocol": "",
                        "status": "skipped: lesion outside vessel"}); continue
        r2, _ = insert(t2, p2, s2, c, L2, ds)
        # measurement node: the SAME anatomical point as in the clean tree where it survives, else by arc
        cand = np.where(m == meas_clean)[0]
        meas2 = int(cand[0]) if len(cand) else int(p2[min(int(np.searchsorted(s2, c + L / 2 + RUNOFF)), len(p2) - 1)])
        meas_same_point = bool(len(cand))
        # Protocol C targets: TERRITORY PERFUSION, matched between clean and corrupted trees by the anatomical
        # identity of each territory's root node (coordinates).
        #
        # DECISION B1, settled 2026-09-19. The target is the clean tree's FULL territory outflow -- the whole clean
        # subtree below that anatomical point, INCLUDING any part the segmentation error deleted. Until now the code
        # summed only the SURVIVING nodes' clean flow, which is a different experiment and gave the opposite sign
        # (every T1 C_ratio > 1 instead of < 1).
        #
        # Why the full territory is the right target: the target represents what perfusion imaging measures IN THE
        # PATIENT. The patient's myocardium is perfused whether or not the segmentation saw the branch that feeds it,
        # so a missing branch does not reduce the measured territory flow -- it only means the model must deliver
        # that flow through the vessels it can see. The surviving-nodes alternative sets the target from the
        # corrupted anatomy itself, i.e. a validation target that has been contaminated by the very error it is
        # supposed to validate against, and one no clinic could produce without already knowing which branch was
        # missed. This also restores the thesis mechanism: the bed must draw harder through fewer vessels, C falls,
        # and the concealment is visible. Matches STATISTICS-PLAN §P2 ("total bed outflow of each subtree") as
        # written; the code, not the plan, was wrong.
        # THE PARTITION IS THE CLEAN TREE'S, NOT THE CORRUPTED TREE'S. Taking territories from the corrupted tree
        # looked right and fails in two ways, both measured: (i) if the error removes the tree's first bifurcation
        # the corrupted partition roots DEEPER, and the clean subtree below that deeper point EXCLUDES the deleted
        # branch -- 2 of 174 probe rows targeted as little as 33 % of the clean territory flow; (ii) if the corrupted
        # tree stops branching altogether there is no partition at all and Protocol C was skipped -- 27 of 174 rows.
        # The clean tree's territories are a fixed anatomical partition that the error cannot move, so the target is
        # well defined however the topology is damaged, and a corrupted node is assigned to the territory its CLEAN
        # counterpart belongs to.
        t_pairs = protocol_c_targets(t, t2, m, q0_all)
        q_target = np.array([q for _, q, _ in t_pairs])
        surv = [v for v in t2.leaves if m[v] >= 0]            # reported for provenance, not used as targets

        for proto in ("A_fixed", "B_rederived", "C_flowmatched"):
            rec = {**base, "run_id": run_id_of(row, bed, etype, proto),
                   "error_type": etype, "protocol": proto, "status": "ok",
                   "meas_same_point": meas_same_point, "n_outlets_shared": len(surv),
                   "n_territories": len(t_pairs), **sc_covariates(t2),
                   **{f"info_{k}": v for k, v in (info.items() if isinstance(info, dict) else [])}}
            try:
                if proto == "A_fixed":
                    # clean conductances on the surviving nodes; deleted nodes' demand is simply lost
                    w_saved = t2.w.copy()
                    t2.w = np.where(m >= 0, t.w[np.maximum(m, 0)], 0.0) * (t2.w > 0)
                    if t2.w.sum() <= 0: t2.w = w_saved; rec["status"] = "skipped: no bed left"; out.append(rec); continue
                    C2 = C_clean
                    ffr2, Q2, info2, _, _ = t2.evaluate(C2, r2); qb = bed_flow(t2, C2, ffr2)
                    t2.w = w_saved
                elif proto == "B_rederived":
                    t2._C.clear(); C2 = t2.calibrate(t2.demand("murray", 1.0))
                    ffr2, Q2, info2, _, _ = t2.evaluate(C2, r2); qb = bed_flow(t2, C2, ffr2)
                else:
                    # ONE free parameter (a global bed scaling) against n_territories >= 2 targets: over-determined
                    # by construction, which is the answer to "one equation, one unknown".
                    if len(t_pairs) < 2:
                        rec["status"] = "skipped: fewer than 2 shared territories to match"; out.append(rec); continue
                    t2._C.clear(); C_start = t2.calibrate(t2.demand("murray", 1.0))
                    lo_b, hi_b = np.log10(C_start) - 1.5, np.log10(C_start) + 1.5
                    def loss(lc):
                        f, _, _, _, _ = t2.evaluate(10 ** lc, r2)
                        q = bed_flow(t2, 10 ** lc, f)
                        pred = np.array([q[sub].sum() for sub, _, _ in t_pairs])
                        return float(np.mean(((pred - q_target) / q_target) ** 2))
                    # GLOBAL scan before local refinement. The loss is BIMODAL in log C: as C -> 0 the flows become
                    # epicardially limited and the RATIO of territory flows happens to match the target ratio again --
                    # a second basin with no physical meaning. minimize_scalar(method="bounded") is a LOCAL method and
                    # returned that basin for scan 341/RCA/leaky/T1: C_ratio 0.077, residual 0.050, FFR 0.158,
                    # dFFR -0.52, against a true optimum of C_ratio 1.00, residual 0.004, dFFR ~0. That row would have
                    # been recorded as "passes its validation check AND is materially wrong" -- a false absorption
                    # count in P2's headline number and a false positive for H5. 1 of 16 T1 fits in the reviewer's
                    # probe. The C_ratio values 9.3 and 33.3 are from that probe too, NOT from the smoke run: the
                    # smoke's largest is 10.1 (scan 335 / discrete / T2), and that one was checked and is unimodal,
                    # i.e. genuine and not this pathology. Post-fix the smoke changed 0 of 38 Protocol C rows, so the
                    # smoke set does not contain the pathology at all -- which is the argument for recording the fit
                    # diagnostics on every row of the full run rather than trusting a subset.
                    # Independent review 2026-09-19, references/FABLE-REVIEW-DETECTOR-2026-09-19.md §5 (MUST 2).
                    grid = np.linspace(lo_b, hi_b, 61)                      # 61 points = C_start is grid[30] exactly
                    lv = np.array([loss(x) for x in grid])
                    k = int(np.argmin(lv))
                    n_basins = int(sum(1 for i in range(1, len(lv) - 1) if lv[i] < lv[i - 1] and lv[i] < lv[i + 1]))
                    res = minimize_scalar(loss, bounds=(grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]),
                                          method="bounded", options=dict(xatol=1e-9))
                    lc_opt = float(res.x) if float(res.fun) <= lv[k] else float(grid[k])
                    at_bound = bool(min(abs(lc_opt - lo_b), abs(lc_opt - hi_b)) < 1e-6)
                    rec.update(fit_n_basins=n_basins, fit_loss_at_Cstart=float(lv[30]),
                               fit_loss=float(min(float(res.fun), lv[k])), fit_at_bound=at_bound)
                    # A fit sitting on a search bound is not an optimum, it is a search that ran out of room:
                    # a FAILED FIT, logged, never a result (STATISTICS-PLAN §9 -- non-converged solves are failures).
                    if at_bound:
                        rec["status"] = "failed fit: Protocol C optimum at search bound"; out.append(rec); continue
                    C2 = 10 ** lc_opt
                    ffr2, Q2, info2, _, _ = t2.evaluate(C2, r2); qb = bed_flow(t2, C2, ffr2)
                f2 = float(ffr2[meas2])
                if len(t_pairs):
                    pred = np.array([qb[sub].sum() for sub, _, _ in t_pairs])
                    resid = float(np.sqrt(np.mean(((pred - q_target) / q_target) ** 2)))
                else:
                    resid = np.nan
                rec.update(C_clean=C_clean, C=C2, C_abs=C2, C_ratio=C2 / C_clean, ffr=f2, dFFR=f2 - f0,
                           flip=int((f2 <= THRESHOLD) != (f0 <= THRESHOLD)),
                           flip_dir=("to_positive" if f2 <= THRESHOLD < f0 else
                                     "to_negative" if f0 <= THRESHOLD < f2 else ""),
                           outlet_flow_residual=resid, inflow_mls=info2["inflow"] * 1e6,
                           inflow_clean_mls=info0["inflow"] * 1e6, converged=bool(info2["converged"]),
                           iters=info2["iters"], mass_err=info2["mass_err"])
                # --- side files (DETECTOR-SPEC §7.2, §7.3), emitted only for a run that actually solved
                rid = rec["run_id"]
                pull_out += pullback_rows(t2, p2, s2, c, L2, meas2, ffr2, Q2, info2["inflow"], rid)
                covered = set(int(x) for x in m[m >= 0])
                for j, (members, q_tgt_j, sub_c) in enumerate(t_pairs):
                    terr_out.append(dict(
                        run_id=rid, terr_id=j, root_node=int(sub_c[0]),
                        root_xyz_mm=";".join(f"{v:.4f}" for v in t.xyz[int(sub_c[0])] * 1e3),
                        Q_target_mls=q_tgt_j * 1e6, Q_achieved_mls=float(qb[members].sum()) * 1e6,
                        residual=float((qb[members].sum() - q_tgt_j) / q_tgt_j) if q_tgt_j else np.nan,
                        sum_w=float(t2.w[members].sum()), n_nodes=int(len(members)),
                        n_outlets=int(sum(1 for v in members if v in set(int(x) for x in t2.leaves))),
                        contains_lesion=bool(meas_clean in sub_c),
                        # an EXPERIMENT-SIDE label for analysis — never a detector input
                        contains_error=bool(any(int(v) not in covered for v in sub_c))))
            except Exception as e:
                rec["status"] = f"error: {e.__class__.__name__}: {e}"
            out.append(rec)
    return out, terr_out, pull_out, ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root"); ap.add_argument("--cohort", default=None); ap.add_argument("--beds", default="leaky,discrete")
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", default=None)
    a = ap.parse_args(); root = Path(a.root); here = Path(__file__).parent.parent
    coh = pd.read_csv(a.cohort or here / "protocol" / "COHORT-FROZEN-2026-09-18.csv")
    if a.limit: coh = coh.head(a.limit)
    beds = a.beds.split(",")
    out_path = Path(a.out or here / "results" / "ablation.csv")
    rows, terrs, pulls, t0, fails = [], [], [], time.time(), 0
    print(f"cohort {len(coh)} instances x {len(beds)} beds x 4 error types x 3 protocols "
          f"= up to {len(coh)*len(beds)*12} rows\n")
    for n, (_, r) in enumerate(coh.iterrows(), 1):
        for bed in beds:
            try:
                res, tr, pl, why = run_instance(root, r, bed)
                if why: fails += 1; print(f"  SKIP {r.scan}_{r.side} {bed}: {why}", file=sys.stderr)
                rows += res; terrs += tr; pulls += pl
            except Exception as e:
                fails += 1; print(f"  FAIL {r.scan}_{r.side} {bed}: {e.__class__.__name__}: {e}", file=sys.stderr)
                if fails <= 3: traceback.print_exc()
        if n % 10 == 0:
            print(f"  {n}/{len(coh)} instances  {len(rows)} rows  {fails} failures  {time.time()-t0:.0f}s", flush=True)
    df = pd.DataFrame(rows); out_path.parent.mkdir(exist_ok=True); df.to_csv(out_path, index=False)
    # DETECTOR-SPEC §7.2/§7.3 side files, long-format and keyed by run_id. Written beside the main table with the
    # same stem so a run is one self-describing set. They exist so the detector NEVER requires a second ablation:
    # twelve minutes of compute now is cheap, a post-registration code change is a protocol deviation.
    terr_path = out_path.with_name(out_path.stem + "_territory.csv")
    pull_path = out_path.with_name(out_path.stem + "_pullback.csv")
    pd.DataFrame(terrs).to_csv(terr_path, index=False)
    pd.DataFrame(pulls).to_csv(pull_path, index=False)
    print(f"\nwrote {out_path}  ({len(df)} rows, {fails} instance failures, {time.time()-t0:.0f}s)")
    print(f"      {terr_path.name}  ({len(terrs)} territory rows)")
    print(f"      {pull_path.name}  ({len(pulls)} pullback stations)")
    summarise(df)

def summarise(df):
    ok = df[df.status == "ok"].copy()
    print(f"\n{'='*94}\nABLATION — {len(ok)}/{len(df)} rows solved"
          f"{'' if len(ok)==len(df) else '  (skips: ' + '; '.join(f'{k}: {v}' for k,v in df[df.status!='ok'].status.value_counts().head(4).items()) + ')'}"
          f"\n{'='*94}")
    if ok.empty: return
    # converged arrives as object dtype (skipped rows contribute NaN), and ~True on a Python bool is -2, not False
    nonconv = int((ok.converged.astype("boolean") != True).sum())
    print(f"non-converged {nonconv}  |  max mass error {ok.mass_err.max():.1e}  |  territories per row: "
          f"median {ok.n_territories.median():.0f}")
    for bed, g in ok.groupby("bed"):
        print(f"\n--- bed = {bed} ---")
        print(f"{'error type':<20}{'protocol':<16}{'n':>4}{'mean dFFR':>11}{'mean |dFFR|':>13}{'flips':>8}{'flip %':>8}{'flow resid':>12}")
        for (e, p), h in g.groupby(["error_type", "protocol"]):
            print(f"{e:<20}{p:<16}{len(h):>4}{h.dFFR.mean():>+11.4f}{h.dFFR.abs().mean():>13.4f}"
                  f"{int(h.flip.sum()):>8}{100*h.flip.mean():>7.1f}%{h.outlet_flow_residual.median():>12.4f}")
    print(f"\n--- THE THESIS: a model that passes its perfusion check (residual < {VALIDATED_RESIDUAL:.0%}) while the"
          f" FFR it reports is wrong by > {MATERIAL_DFFR:.2f} ---")
    print(f"{'bed':<10}{'protocol':<16}{'n':>4}{'median resid':>14}{'passes check':>14}{'…and wrong':>12}{'…and flips':>12}")
    for bed, g in ok.groupby("bed"):
        for p in ("A_fixed", "B_rederived", "C_flowmatched"):
            h = g[g.protocol == p]
            if h.empty: continue
            passes = h[h.outlet_flow_residual < VALIDATED_RESIDUAL]
            absorbed = passes[passes.dFFR.abs() > MATERIAL_DFFR]
            print(f"{bed:<10}{p:<16}{len(h):>4}{h.outlet_flow_residual.median():>14.4f}"
                  f"{len(passes):>8} ({100*len(passes)/len(h):>3.0f}%){len(absorbed):>8}"
                  f"{int(passes.flip.sum()):>12}")
    print("  (A keeps the CLEAN bed on surviving nodes — the reference arm, not a naive case. It does NOT pass the")
    print("   perfusion check by construction: since decision B1 the target is the FULL clean territory including")
    print("   the deleted branch's share, which A cannot deliver through the vessels it has left, so A's residual is")
    print("   the lost perfusion. B is the deployment case: the bed is re-derived from wrong anatomy. C is tuned.)")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--summarise":
        summarise(pd.read_csv(sys.argv[2]))
    else:
        main()
