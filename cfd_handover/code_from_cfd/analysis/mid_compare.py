"""Post-run comparison for the isolated-lesion pair (lesion_mid_design.md sections 5 and 8); written BEFORE the runs, read-only on the case outputs.
usage: LESION_PROFILE=lesion_mid python3 mid_compare.py <solve_lesion_mid> <solve_baseline_ref_mid> <out.json> [tube_end_mm]
exit code: 0 only for a VALID pair (result json 'valid_pair' True); 1 = required files missing (nothing compared); 2 = pair NOT valid (outputs written under *_UNCONVERGED_do_not_quote).
Validity (shared with the hyperaemic/E60 comparisons, hyp_compare.case_validity): strict verdict + stored verdict CONVERGED, finished log, freshness at the final iteration,
exact monitor equality, measurement-plane stability from two write times (needs sections_lesion80_tprev.* / sections_baseline_ref_tprev.*). If either case is not valid no single value is
printed: compare_lesion outputs go under *_UNCONVERGED_do_not_quote names and only the reasons and the primary-outcome STATUS are printed.
Realised fine-tube end (HYP4 finding 4): derived from the lesion case's own system/meshDict (last lad_<i> cone, p1 in metres, projected on the profile's smoothed centreline
= build_lesion80_surface.build_frames); the optional command-line value is only a cross-check (|difference| > 0.05 mm aborts); the reference meshDict must hold the same lad cones.
The analysed window ends are read from the files (last finite station of the WSS csv, last ok section of the section csv), never from the profile.
PRIMARY outcome (reattachment, audited f_rev rule of reattachment_wss, threshold 1 % reversed-wall fraction): assess_primary() gives ONE status, printed next to every raw number,
stored in values['primary_outcome_status'], the companion json ('mid_compare_status') and the pdf banner. Precedence: NOT ASSESSABLE (missing stations / json-csv mismatch)
> NOT MESH-SUPPORTED or NOT ASSESSABLE (within 2 mm of the realised tube end / the WSS window end) > PROVISIONAL (within 3 mm of the flagged mesh cluster at 60.65 mm; pending the
pre-registered mesh check, lesion_mid_design.md section 8) > ASSESSABLE (reattached before the junction edge) / CENSORED.
Secondary outputs (design section 5, no tolerances): distal_flow_reduction_pct (D2 + LAD outlets, with 0D EDT/area), peak_wall_shear_Pa and peak_axial_velocity_ms within +-3 mm
of the throat, throat Re, added static loss S_UP -> S_DOWN.
Output order (HYP4 finding 3): everything that does not need compare_lesion's output is computed BEFORE it runs; its files go to *_compare_UNFINISHED.* at once and get their final
names only after every wrapper calculation and write has succeeded (an exception leaves *_UNFINISHED)."""
import sys, os, re, json, io, contextlib, textwrap
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lesion_profile
if lesion_profile.NAME != "lesion_mid":
    raise SystemExit("mid_compare.py must be run with LESION_PROFILE=lesion_mid (the stations and junction of the profile are used)")
import numpy as np, pandas as pd
import hyp_compare as H
import compare_lesion as CL
PR = lesion_profile.PR
MESH_FLAG_ARC, MESH_FLAG_HALF = 60.65, 3.0     # cluster of 4 low-quality wall tet faces inside the fine tube (failed_sets_localisation.json of lesion_mid/mesh_M50); pre-registered provisional band
PRIMARY_THR, SUSTAIN_MM, EDGE_MM, PEAK_HALF = 0.01, 1.0, 2.0, 3.0   # primary rule's own threshold and sustain length (reattachment_wss), end-gap, +-throat window of the peak outputs
TUBE_END_TOL = 0.05                            # mm: derived vs command-line tube end
MESH_CHECK = "pending the pre-registered mesh check (25 um refinement zone over arcs 52-66 mm, lesion_mid_design.md section 8)"

_FRAMES = None
def frames():
    """Smoothed root->LAD centreline of the profile (mm; build_lesion80_surface.build_frames, the curve every arc of the pipeline refers to); built once."""
    global _FRAMES
    if _FRAMES is None:
        import build_lesion80_surface as G
        from outlets_837 import build_tree
        with contextlib.redirect_stdout(io.StringIO()):
            T = build_tree(); T.ffr(mode="murray"); _FRAMES = G.build_frames(T)
    return _FRAMES

def lad_cones(meshdict):
    """[(index, p0 (m), p1 (m))] of the lad_<i> cones of a cfMesh meshDict, sorted by index."""
    txt = open(meshdict).read()
    num = r"([-+0-9.eE]+)"
    pat = re.compile(rf"\blad_(\d+)\s*\{{[^}}]*?p0\s*\(\s*{num}\s+{num}\s+{num}\s*\)[^}}]*?p1\s*\(\s*{num}\s+{num}\s+{num}\s*\)")
    c = sorted((int(m.group(1)), np.array([float(x) for x in m.group(2, 3, 4)]), np.array([float(x) for x in m.group(5, 6, 7)])) for m in pat.finditer(txt))
    if not c: raise SystemExit(f"{meshdict}: no lad_<i> cone found: the realised fine-tube end cannot be derived")
    if [i for i, _, _ in c] != list(range(len(c))): raise SystemExit(f"{meshdict}: lad cone indices not contiguous from 0: {[i for i, _, _ in c]}")
    return c

def project_arc(p_mm, fr=None):
    """Arc (mm) of the orthogonal projection of p on the smoothed centreline polyline (segment-wise, not just the nearest frame point) and the distance to it."""
    fr = frames() if fr is None else fr
    c, s = np.asarray(fr["c"], float), np.asarray(fr["s"], float)
    a, b = c[:-1], c[1:]; ab = b - a; L2 = np.einsum("ij,ij->i", ab, ab)
    t = np.clip(np.einsum("ij,ij->i", p_mm - a, ab) / np.where(L2 > 0, L2, 1), 0, 1)
    q = a + t[:, None] * ab; d = np.linalg.norm(q - p_mm, axis=1); k = int(d.argmin())
    return float(s[k] + t[k] * (s[k + 1] - s[k])), float(d[k])

def realised_tube_end(les, ref=None, cli_mm=None, fr=None):
    """HYP4 finding 4: realised end of the fine LAD tube = projection of the last lad cone's p1 of <les>/system/meshDict; cross-checked with the reference meshDict
    (identical cylinder list required, design section 3) and the optional command-line value (|diff| <= TUBE_END_TOL)."""
    md = f"{les}/system/meshDict"
    c = lad_cones(md); last = c[-1]
    arc, dist = project_arc(last[2] * 1e3, fr)
    start, _ = project_arc(c[0][1] * 1e3, fr)
    r = dict(tube_end_mm=arc, tube_start_mm=start, source=md, last_cone=f"lad_{last[0]}", p1_m=last[2].tolist(), p1_axis_distance_mm=dist, n_lad_cones=len(c),
             requested_profile_TUBE_END_mm=PR["TUBE_END"], command_line_mm=cli_mm)
    if dist > 0.5: raise SystemExit(f"{md}: last lad cone p1 is {dist:.3f} mm from the smoothed centreline: not a centreline chain, tube end not derivable")
    if ref is not None and os.path.exists(f"{ref}/system/meshDict"):
        cr = lad_cones(f"{ref}/system/meshDict")
        same = len(cr) == len(c) and all(np.allclose(x[1], y[1], atol=1e-9) and np.allclose(x[2], y[2], atol=1e-9) for x, y in zip(c, cr))
        r["reference_meshDict_same_lad_cones"] = bool(same)
        if not same: raise SystemExit(f"{ref}/system/meshDict: lad cones differ from {md} (the pair must share the cylinder list)")
    if cli_mm is not None and abs(cli_mm - arc) > TUBE_END_TOL:
        raise SystemExit(f"command-line tube end {cli_mm} mm != realised {arc:.3f} mm from {md} (|diff| > {TUBE_END_TOL} mm)")
    return r

def _f(W):
    return np.asarray(W.s_mm, float), pd.to_numeric(W.f_rev, errors="coerce").astype(float).values

def assess_primary(W, Wj, tube_end_mm, s_c=None, junction=None, flag_arc=MESH_FLAG_ARC, flag_half=MESH_FLAG_HALF, S=None):
    """HYP4 finding 5: explicit status of the PRIMARY outcome (reattachment by the audited f_rev rule), with the rule's own threshold (f_rev >= 0.01) and actual coverage.
    W: wss csv (every station; NaN f_rev = missing), Wj: reattachment_wss json. Statuses in precedence order:
    (a) 'NOT ASSESSABLE (...)': reattachment_wss's missing_stations_in_window != 0 / absent, a NaN f_rev station between the throat and the reattachment's sustain window end
        (reattached) or the junction edge (not reattached), the json's reattachment not reproduced by the csv, or a 'no resolved separation' without complete coverage;
        json/csv contradiction (HYP6 FIXES(b)-1, checked station by station, before (b)-(c)): 'no separation' but ANY finite wss station from the throat to the window end
        (or any ok section station of S, the section csv) with f_rev / frac_reversed_area >= 1 %; a reversed station between the throat and the json's onset; a reversed
        station after the json's reattachment and before the junction edge beyond the json's own last_station_f_rev_ge_1pct_before_junction (unreported second patch);
    (b) 'NOT ASSESSABLE (...)' if the reattachment arc or the last f_rev >= 1 % station lies within 2 mm of the WSS window end (last finite station) and
        'NOT MESH-SUPPORTED (...)' if within 2 mm of (or beyond) the realised fine-tube end;
    (c) 'PROVISIONAL (mesh-flag-adjacent)': reattachment arc or last f_rev >= 1 % station within flag_half of the flagged cluster;
    (d) 'ASSESSABLE' (reattached before the junction edge, or no resolved separation with complete coverage) / 'CENSORED (not reattached before the junction edge)'.
    'last f_rev >= 1 % station': reattached -> the last finite reversed station before the reattachment and reattachment_wss's last_station_f_rev_ge_1pct_before_junction
    (conservative: both are tested); separated, not reattached -> the last finite reversed station of the whole csv (finite_extent, threshold 0.01); no separation -> none
    (any reversal contradicts the json and is NOT ASSESSABLE). With this mesh (tube end 66.5 < junction edge 67) a not-reattached outcome is always
    within 2 mm of the tube end, i.e. NOT MESH-SUPPORTED rather than CENSORED. Status strings carry no numbers
    (they are shown for a pair that is not valid); numbers are in 'reasons' and the other keys."""
    s_c = PR["S_C"] if s_c is None else s_c; junction = PR["JUNCTION"] if junction is None else junction
    s, f = _f(W); fin = np.isfinite(f)
    fe = H.finite_extent(s, f, PRIMARY_THR, s_c, gap_mm=EDGE_MM)
    win = fe["window_end_mm"]
    onset, reatt = Wj.get("separation_onset_s_mm"), Wj.get("reattachment_s_mm_f_rev_rule")
    reattached = bool(Wj.get("reattached_before_junction")) and reatt is not None and reatt < junction
    n_own = Wj.get("missing_stations_in_window")
    lim_tube = tube_end_mm - EDGE_MM
    r = dict(rule=f"reattachment_wss f_rev rule: onset f_rev >= {PRIMARY_THR}, reattachment = first station with f_rev < {PRIMARY_THR} sustained over >= {SUSTAIN_MM} mm, no missing station; "
                  f"uncensored only before the junction edge {junction:g} mm", threshold=PRIMARY_THR, separation_onset_s_mm=onset, reattachment_s_mm=reatt,
             distance_from_throat_mm=(reatt - s_c) if reattached else None, reattached_before_junction=reattached, junction_edge_mm=junction, throat_mm=s_c,
             realised_tube_end_mm=tube_end_mm, tube_end_limit_mm=lim_tube, wss_window_end_mm=win, wss_csv_end_mm=float(s.max()) if len(s) else None,
             mesh_flag_arc_mm=flag_arc, mesh_flag_band_mm=flag_half, missing_stations_in_window_reattachment_wss=n_own, reasons=[])
    NA, NMS, PROV = [], [], []
    # (a) coverage
    if n_own != 0: NA.append(f"reattachment_wss missing_stations_in_window={n_own} (must be 0)")
    end_a = (reatt + SUSTAIN_MM) if reattached else junction
    closed = reattached   # the sustain window end belongs to the reattachment claim; the junction edge is exclusive
    m = (s >= s_c - 1e-9) & ((s <= end_a + 1e-9) if closed else (s < end_a - 1e-9))
    miss = sorted(float(x) for x in s[m & ~fin])
    r["missing_stations_throat_to_claim_end"] = miss; r["claim_end_mm"] = end_a
    if miss: NA.append(f"missing (NaN) WSS stations between the throat {s_c:g} mm and {end_a:g} mm: {miss}")
    if reattached and not miss:   # the json's reattachment must be reproduced by the csv (onset reversed; sustain window finite and < threshold)
        sw = (s >= reatt - 1e-9) & (s <= reatt + SUSTAIN_MM + 1e-9)
        if sw.sum() < int(round(SUSTAIN_MM / 0.25)) + 1 or not (f[sw] < PRIMARY_THR).all(): NA.append(f"wss csv does not show f_rev < {PRIMARY_THR} over {reatt:g}-{reatt + SUSTAIN_MM:g} mm (json and csv disagree)")
    if onset is not None:
        o = np.abs(s - onset) < 1e-6
        if not (o.any() and np.isfinite(f[o]).all() and (f[o] >= PRIMARY_THR).all()): NA.append(f"wss csv does not show f_rev >= {PRIMARY_THR} at the onset {onset:g} mm (json and csv disagree)")
    # HYP6 FIXES(b)-1: EVERY finite station is checked against the json's claims (not only the last reversed one)
    revs = fin & (s >= s_c - 1e-9) & (f >= PRIMARY_THR)
    if onset is None:   # 'no resolved separation (f_rev < 1 % everywhere after the throat)': any reversed station from the throat to the window end contradicts it
        bad = sorted(float(x) for x in s[revs])
        if bad: NA.append(f"reattachment_wss reports no separation but the wss csv has f_rev >= {PRIMARY_THR} at {bad} mm (json and csv disagree)")
        if Wj.get("last_station_f_rev_ge_1pct_before_junction") is not None:
            NA.append(f"reattachment_wss reports no separation but its last_station_f_rev_ge_1pct_before_junction is {Wj['last_station_f_rev_ge_1pct_before_junction']:g} mm (json inconsistent: json and csv disagree)")
        if S is not None:   # the section stations (ok, finite) must not show reversed area either
            okv = S.ok.map(H.is_true).values if "ok" in S.columns else np.ones(len(S), bool)
            ss = np.asarray(S.s_mm, float); v = np.where(okv, pd.to_numeric(S.frac_reversed_area, errors="coerce").astype(float).values, np.nan)
            bad = sorted(float(x) for x in ss[np.isfinite(v) & (ss >= s_c - 1e-9) & (v >= PRIMARY_THR)])
            r["section_stations_reversed_mm"] = bad
            if bad: NA.append(f"reattachment_wss reports no separation but the section csv has frac_reversed_area >= {PRIMARY_THR} at {bad} mm (json and csv disagree)")
    else:
        bad = sorted(float(x) for x in s[revs & (s < onset - 1e-6)])
        if bad: NA.append(f"wss csv has f_rev >= {PRIMARY_THR} at {bad} mm, before the json's separation onset {onset:g} mm (json and csv disagree)")
    if reattached:   # a second reversed patch after the claimed reattachment that the json does not report (its last reversed station before the junction is earlier)
        last_own_ = Wj.get("last_station_f_rev_ge_1pct_before_junction")
        bad = sorted(float(x) for x in s[revs & (s > reatt + 1e-9) & (s < junction - 1e-9)] if last_own_ is None or x > last_own_ + 1e-6)
        if bad: NA.append(f"wss csv has f_rev >= {PRIMARY_THR} at {bad} mm after the json's reattachment {reatt:g} mm and before the junction edge, not reported by the json "
                          f"(last_station_f_rev_ge_1pct_before_junction={last_own_}): second reversed patch (json and csv disagree)")
    r["contradiction_checked"] = "every finite wss station from the throat (and, for 'no separation', every ok section station) against onset / reattachment / last reversed station of the json"
    if onset is None:
        cov = H.wss_outcome_assessment(W, Wj, s_c)
        r["no_separation_coverage"] = cov
        if not cov["coverage_complete"]: NA.append(f"'no resolved separation' needs every station finite: {cov['outcome_assessed']}")
    # the stations that bound the claimed recirculation
    if reattached:
        pre = fin & (s >= s_c - 1e-9) & (s < reatt - 1e-9) & (f >= PRIMARY_THR)
        last_rev = float(s[pre].max()) if pre.any() else None
    elif onset is not None:
        last_rev = fe["last_reversed_mm"]
    else:   # no separation claimed: any reversed station contradicts it (checked above)
        last_rev = None
    last_own = Wj.get("last_station_f_rev_ge_1pct_before_junction")
    r.update(last_f_rev_ge_1pct_mm=last_rev, last_station_f_rev_ge_1pct_before_junction_json=last_own, finite_extent_1pct=fe)
    tested = [("reattachment arc", reatt if reattached else None), ("last f_rev >= 1 % station", last_rev), ("last f_rev >= 1 % station before the junction (reattachment_wss)", last_own)]
    # (b) window end / realised tube end
    for nm, x in tested:
        if x is None: continue
        if win is not None and x >= win - EDGE_MM: NA.append(f"{nm} {x:g} mm within {EDGE_MM:g} mm of the WSS window end {win:g} mm")
        if x >= lim_tube: NMS.append(f"{nm} {x:g} mm within {EDGE_MM:g} mm of (or beyond) the realised fine-tube end {tube_end_mm:.3f} mm")
    # (c) flagged mesh cluster
    for nm, x in tested:
        if x is not None and abs(x - flag_arc) <= flag_half: PROV.append(f"{nm} {x:g} mm within {flag_half:g} mm of the flagged mesh cluster at {flag_arc:g} mm; {MESH_CHECK}")
    r["reasons"] = NA + NMS + PROV
    r["mesh_flag_adjacent"] = bool(PROV)
    if NA:
        cause = "missing stations" if any("missing" in x for x in NA) else "json and csv disagree" if any("disagree" in x for x in NA) else "recirculation reaches the analysed WSS window end"
        r["status"] = f"NOT ASSESSABLE ({cause})"
    elif NMS: r["status"] = "NOT MESH-SUPPORTED (recirculation within 2 mm of the realised fine-tube end)" + ("" if reattached else "; not reattached before the junction edge")
    elif PROV: r["status"] = "PROVISIONAL (mesh-flag-adjacent)"
    elif reattached: r["status"] = "ASSESSABLE"
    elif onset is None: r["status"] = "ASSESSABLE"; r["outcome_kind"] = "no resolved separation"
    else: r["status"] = "CENSORED (not reattached before the junction edge)"
    r.setdefault("outcome_kind", "reattached before the junction edge" if reattached else "separated, not reattached before the junction edge" if onset is not None else "no resolved separation")
    return r

def near_throat(df, col, s_c, half=PEAK_HALF, ok_col=False):
    """Max of col over the stations with |s - s_c| <= half (ok sections only if ok_col); value, station, and the stations missing in that range."""
    s = np.asarray(df.s_mm, float); v = pd.to_numeric(df[col], errors="coerce").astype(float).values
    ok = df.ok.map(H.is_true).values if ok_col else np.ones(len(df), bool)
    m = np.abs(s - s_c) <= half + 1e-9; good = m & ok & np.isfinite(v)
    miss = sorted(float(x) for x in s[m & ~good])
    if not good.any(): return dict(value=None, s_mm=None, n_stations=0, missing_stations=miss)
    k = np.where(good)[0][v[good].argmax()]
    return dict(value=float(v[k]), s_mm=float(s[k]), n_stations=int(good.sum()), window_mm=[s_c - half, s_c + half], missing_stations=miss)

def distal_flow(A_l, A_r, Z):
    """design section 5: 100 (1 - (Q_D2 + Q_LAD)_lesion / (Q_D2 + Q_LAD)_reference), 3D and the 0D EDT / area-variant equivalents (zerod_reference.json of the lesion case)."""
    outs = [f"outlet_{PR['JUNCTION_NAME']}", "outlet_LAD"]
    ql = sum(A_l["outlets"][p]["Q_mls"] for p in outs); qr = sum(A_r["outlets"][p]["Q_mls"] for p in outs)
    z = {k: sum(Z["outlets"][p][k] for p in outs) for k in ("Q0_mls", "Q0_areaVariant_mls", "Q0_healthy_mls")}
    return dict(outlets=outs, Q_lesion_mls=ql, Q_reference_mls=qr, distal_flow_reduction_pct=100 * (1 - ql / qr),
                distal_flow_reduction_0D_edt_pct=100 * (1 - z["Q0_mls"] / z["Q0_healthy_mls"]), distal_flow_reduction_0D_area_pct=100 * (1 - z["Q0_areaVariant_mls"] / z["Q0_healthy_mls"]),
                Q0_edt_mls=z["Q0_mls"], Q0_area_mls=z["Q0_areaVariant_mls"], Q0_healthy_mls=z["Q0_healthy_mls"])

def banner(valid, P):
    lines = ["VALID PAIR" if valid else "NOT A VALID PAIR: DO NOT QUOTE",
             f"profile {lesion_profile.NAME} | PRIMARY outcome (reattachment, f_rev >= 1 %): {P['status']}"]
    if P["status"] != "ASSESSABLE" and not P["status"].startswith("CENSORED"): lines.append("the primary outcome is not a supported measurement here" + (f"; {MESH_CHECK}" if P["mesh_flag_adjacent"] else ""))
    return "\n".join("\n".join(textwrap.wrap(l, 125)) for l in lines)

def main(les, ref, out, tube_end=None, need_plane=True):
    for f in H.output_names(out):
        if os.path.lexists(f): os.remove(f)
    val = {"lesion": H.case_validity(les, "lesion80", need_plane, tag=os.path.basename(les)), "reference": H.case_validity(ref, "baseline_ref", need_plane, tag=os.path.basename(ref))}
    valid = all(v["valid"] for v in val.values())
    reasons = [r for v in val.values() for r in v["reasons"]]
    res = dict(profile=lesion_profile.NAME, S_C=PR["S_C"], junction_mm=PR["JUNCTION"], valid_pair=valid, reasons=reasons, validity={k: {kk: v[kk] for kk in ("valid", "reasons", "strict_verdict", "stored_verdict", "log_finished", "final_iteration")} for k, v in val.items()})
    need = [f"{les}/analysis.json", f"{les}/sections_lesion80.csv", f"{les}/wss_lesion80.csv", f"{les}/wss_lesion80.json", f"{les}/zerod_reference.json", f"{les}/system/meshDict",
            f"{ref}/analysis.json", f"{ref}/sections_baseline_ref.csv", f"{ref}/wss_baseline_ref.csv", f"{ref}/wss_baseline_ref.json"]
    missing = [f for f in need if not os.path.exists(f)]
    if missing:                                       # nothing to compare yet (case not run / not post-processed): report and stop, no output that could be mistaken for a result
        res["missing_files"] = missing
        with open(out, "w") as f: json.dump(res, f, indent=1, default=float)
        print("NOT COMPARED: required files missing:", [os.path.relpath(m) for m in missing]); [print("  -", r) for r in reasons]; raise SystemExit(1)
    # ---- everything that does not need compare_lesion's output: BEFORE it runs (its pdf carries the banner)
    TE = realised_tube_end(les, ref, tube_end)
    te = TE["tube_end_mm"]
    S_l = pd.read_csv(f"{les}/sections_lesion80.csv"); S_r = pd.read_csv(f"{ref}/sections_baseline_ref.csv"); W_l = pd.read_csv(f"{les}/wss_lesion80.csv"); Wj = json.load(open(f"{les}/wss_lesion80.json"))
    PRI = assess_primary(W_l, Wj, te, S=S_l)
    ext, flag = H.recirculation_extent(S_l, W_l, te, s_lo=PR["S_C"])
    windows = dict(section_csv_range_mm=[float(S_l.s_mm.min()), float(S_l.s_mm.max())], section_window_end_mm=ext["section_window_end_mm"],
                   wss_csv_range_mm=ext["wss_csv_range_mm"], wss_window_end_mm=ext["wss_window_end_mm"], realised_tube_end_mm=te)
    bnr = banner(valid, PRI)
    tmp, unf = out + "_compare_TMP", out + "_compare_UNFINISHED"
    try:
        with contextlib.redirect_stdout(io.StringIO()): CL.main(les, ref, tmp, banner=bnr)
    finally:
        for e in ("json", "pdf"):
            if os.path.exists(f"{tmp}.{e}"): os.replace(f"{tmp}.{e}", f"{unf}.{e}")
    final = out + ("_compare" if valid else "_compare_UNCONVERGED_do_not_quote")
    C = json.load(open(unf + ".json")); res["compare_outputs"] = [final + ".json", final + ".pdf"]
    A_l = json.load(open(f"{les}/analysis.json")); A_r = json.load(open(f"{ref}/analysis.json")); Z = json.load(open(f"{les}/zerod_reference.json"))
    V = {}
    V["primary_outcome_status"] = PRI
    V["reattachment"] = dict(primary_outcome_status=PRI["status"], separation_onset_s_mm=Wj["separation_onset_s_mm"], reattachment_s_mm=Wj["reattachment_s_mm_f_rev_rule"],
                             distance_from_throat_mm=Wj["distance_from_throat_mm"], reattached_before_junction=Wj["reattached_before_junction"], outcome_reattachment_wss=Wj["outcome"],
                             peak_f_rev_before_junction=Wj["peak_f_rev_before_junction"], last_station_f_rev_ge_1pct_before_junction=Wj["last_station_f_rev_ge_1pct_before_junction"])
    V["flow_categories"] = {p: dict(d3D=d["delta_3D_pct"], d0D_edt=d["delta_0D_edt_pct"], d0D_area=d["delta_0D_area_pct"], category=H.category(d["delta_3D_pct"], d["delta_0D_area_pct"], d["delta_0D_edt_pct"])) for p, d in C["flow"].items()}
    V["pressure"] = C["pressure"]; V["throat"] = C["throat"]
    pd_ = C["pressure"]["prox_to_distal"]
    V["secondary_outputs"] = dict(
        distal_flow=distal_flow(A_l, A_r, Z),
        peak_wall_shear_Pa=dict(near_throat(W_l, "tau_mean_Pa", PR["S_C"]), definition="max circumferential-mean forward-positive axial WSS (tau_mean_Pa) over the WSS stations within +-3 mm of the throat"),
        peak_axial_velocity_ms=dict(near_throat(S_l, "umax_ms", PR["S_C"], ok_col=True), definition="max section umax_ms over the ok sections within +-3 mm of the throat"),
        Re_throat=C["throat"]["Re_area_eq"],
        added_static_loss=dict(s_from_mm=PR["S_UP"], s_to_mm=PR["S_DOWN"], added_3D_mmHg=pd_["added_by_lesion_3D_mmHg"], added_0D_edt_mmHg=pd_["added_by_lesion_0D_edt_mmHg"], added_0D_area_mmHg=pd_["added_by_lesion_0D_area_mmHg"]),
        note="pre-registered outputs, lesion_mid_design.md section 5; no tolerances")
    V["recirculation_extent"] = ext   # secondary (design 5b rule: sections >= 1 %, wall >= 5 %); the PRIMARY claim uses primary_outcome_status only
    V["analysis_windows"] = windows; V["realised_tube_end"] = TE
    V["flags"] = dict(primary_outcome_status=PRI["status"], recirculation_not_mesh_supported=bool(flag), recirculation_extent_not_assessable=bool(not ext["extent_end_established"]),
                      mesh_flag_adjacent=PRI["mesh_flag_adjacent"], mesh_flag_arc_mm=MESH_FLAG_ARC, mesh_flag_band_mm=MESH_FLAG_HALF,
                      mesh_flag_note=f"4 low-quality wall tet faces at arc ~60.65 mm inside the fine tube; a primary value within {MESH_FLAG_HALF:g} mm is PROVISIONAL {MESH_CHECK}",
                      tube_end_mm=te, Re_throat=C["throat"]["Re_area_eq"])
    p_stations = {}
    for st in H.STATIONS:
        try: p_stations[str(st)] = dict(lesion_3D=H.at(S_l, "p_over_Pao", st), ref_3D=H.at(S_r, "p_over_Pao", st), lesion_0D_edt=H.at(S_l, "p0D_edt_over_Pao", st), lesion_0D_area=H.at(S_l, "p0D_area_over_Pao", st))
        except SystemExit as e: p_stations[str(st)] = f"unavailable: {e}"
    V["p_over_Pao_at_stations"] = p_stations
    res["primary_outcome_status"] = PRI["status"]; res["realised_tube_end_mm"] = te; res["analysis_windows"] = windows
    res["values" if valid else "values_UNCONVERGED_do_not_quote"] = V
    C["mid_compare_status"] = dict(valid_pair=valid, profile=lesion_profile.NAME, primary_outcome_status=PRI["status"], primary_reasons=PRI["reasons"] if valid else "withheld (pair not valid)",
                                   flags={k: v for k, v in V["flags"].items() if k not in ("Re_throat",)} if valid else dict(primary_outcome_status=PRI["status"], mesh_flag_adjacent=PRI["mesh_flag_adjacent"]),
                                   realised_tube_end_mm=te, analysis_windows=windows, validity_reasons=reasons, banner=bnr)
    json.dump(C, open(unf + ".json", "w"), indent=1, default=float)
    json.dump(res, open(out + "_UNFINISHED", "w"), indent=1, default=float)
    os.replace(unf + ".json", final + ".json"); os.replace(unf + ".pdf", final + ".pdf"); os.replace(out + "_UNFINISHED", out)
    print("=" * 70); print("PAIR", "VALID" if valid else "NOT VALID: NOT A VALID PAIR: DO NOT QUOTE (no single value is printed)")
    print("PRIMARY OUTCOME STATUS:", PRI["status"]); print("=" * 70)
    if valid:
        print("primary-status reasons:", PRI["reasons"] or "none")
        print(json.dumps(V["reattachment"], indent=1)); print("analysis windows (from the files) and realised tube end:", windows)
        print(json.dumps(V["secondary_outputs"], indent=1, default=float)); print(json.dumps(V["flags"], indent=1)); print(json.dumps(V["flow_categories"], indent=1))
    else:
        [print("  -", r) for r in reasons]
    print("outputs:", out, res["compare_outputs"])
    return res

if __name__ == "__main__":
    if len(sys.argv) < 4: raise SystemExit("usage: LESION_PROFILE=lesion_mid mid_compare.py <lesion case> <reference case> <out.json> [tube_end_mm (cross-check only)]")
    r = main(sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4]) if len(sys.argv) > 4 else None)
    sys.exit(0 if r["valid_pair"] is True else 2)
