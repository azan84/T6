"""Flow-state diagnostic of Task A (pre-registered in taskA/TASK_A_DESIGN.md, 'Flow-state diagnostic'; audit 2026-10-03 Sol finding 8). Reconstructed fields only (pyvista); no 0D code.
PROFILE: on the reconstructed (latest, or --time) fields, sections of the lesion vessel every STEP_MM = 1 mm of centreline arc from throat + START_MM = 2 mm to the measurement probe (the last station is the probe itself),
each normal to the local centreline tangent (chord of the vessel path over +-0.5 mm of arc), BOUNDED (cells within 3 r_ref + 1.5 mm of the station) and CONNECTED (the component of the cut nearest the station point:
pf/sections.py Sectioner(robust=True): the connected set is taken on the 3D cells straddling the plane). Per section: area A, area-equivalent radius r_eq = sqrt(A/pi), area centroid c_A, axial velocity u_a = U . t per section polygon (cell value),
flux-weighted centroid c_Q = sum(u_a A c) / sum(u_a A) (signed flux weights: the centroid of the through-flow; |u_a|- and forward-only-weighted variants are extra columns, not used by the rule),
offset vector d = (c_Q - c_A) projected on the section plane, and offset/r_eq in the local (normal, binormal) frame: o_N = d.N / r_eq, o_B = d.B / r_eq, |o|, direction angle atan2(o_B, o_N).
Frame (N, B): rotation-minimising (double-reflection) frame carried along the stations; N at the first station = the Frenet curvature normal there if the centreline curvature (from the tangents at +-1 mm) exceeds
KAPPA_MIN = 0.02 /mm, else the projection of the global axis least aligned with the tangent (x, y, z order on ties). The frame depends only on the centreline, so two solves of the same package share it. The Frenet
curvature normal of every station is reported as an angle in this frame (kappa_per_mm, curvature_normal_angle_deg) for the inner/outer-bend reading. Section validity: area centroid within 0.5 r_eq of the station
(as pf/sections.py) AND a section without holes (holes >= 0.5 % of the filled section area, measured by rasterising: a cut with holes, seen through cfMesh transition polyhedra at one sten70 station, is not a valid
lumen section); invalid sections are reported (n_boundary_loops, hole_area_fraction) and make the comparison INDETERMINATE (see COMPARE).
Path: the package centreline (--package): root -> the measurement node (the package probe, or the RELOCATED probe the case's measurementP uses when build_info records one); the throat probe's node must lie on it.
Straight tubes (--straight-x X_THROAT_MM X_MEAS_MM [--axis-yz Y Z] [--r-ref MM]): the x axis is the centreline (sten70; mesh in metres, positions in mm).
COMPARE (the pre-registered classification of two solves on the same centreline): stations matched by arc from the throat. The pre-registered statistic is the max over the FULL specified profile (every station
from throat + 2 mm to the measurement probe) of |o(A) - o(B)| (vector difference in the (N, B) frame, which bounds the difference of the magnitudes). It exists only if every specified station is present and valid
in BOTH profiles; otherwise (an invalid section, a missing or unmatched station) the comparison is INDETERMINATE: the verdict is 'STATES INDETERMINATE', the excluded/unmatched/missing stations are listed, and the
maximum over the stations valid in both is reported for information only (never turned into AGREE; no replacement rule is pre-registered, so none is applied). With a complete profile: STATES AGREE iff
that max <= OFFSET_TOL = 0.03 AND |DeltaFFR_A - DeltaFFR_B| < U3D = 0.00055 (DeltaFFR = FFR at the measurement probe minus the returned reference; the reference cancels, so FFR_A - FFR_B is used: --ffr A B);
otherwise STATES DIFFER. Without --ffr only the profile criterion is evaluated and the verdict says so. No claim of bistability is made (design).
usage: flow_state_profile.py profile <case_dir> (--package NAME [--pkg-root R] | --straight-x X_THROAT_MM X_MEAS_MM [--axis-yz Y_MM Z_MM] [--r-ref MM]) [--time T] [--label L] [--out profile.csv] [--json summary.json]
       flow_state_profile.py compare <profileA.csv> <profileB.csv> [--ffr FFR_A FFR_B] [--json out.json]"""
import sys, os, csv, json
HERE = os.path.dirname(os.path.abspath(__file__))
for _d in (os.path.join(os.environ.get("P", "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot"), "pf"), os.path.join(HERE, "pf")):
    if os.path.isdir(_d): sys.path.insert(0, _d)
import numpy as np

START_MM, STEP_MM, TANGENT_HALF_MM, KAPPA_MIN, OFFSET_TOL, U3D = 2.0, 1.0, 0.5, 0.02, 0.03, 0.00055

# ---------------- path
def polyline_point(X, arc, s): return np.array([np.interp(s, arc, X[:, d]) for d in range(3)])

def polyline_tangent(X, arc, s, half=TANGENT_HALF_MM):
    a, b = max(s - half, arc[0]), min(s + half, arc[-1]); t = polyline_point(X, arc, b) - polyline_point(X, arc, a); return t / np.linalg.norm(t)

def package_path(case, name, pkg_root=None):
    """(X_mm path points root -> measurement node, arc_mm, r_ref_mm along it, s_throat, s_meas, info)"""
    import m1_package as M
    pkg = M.load_package(name, pkg_root); cl = pkg["centreline"]; par, _ = M.graph(cl)
    th = M.probe_row(pkg, "throat"); me = M.probe_row(pkg, "measurement"); meas_node, meas_src = int(me["tree_node"]), f"package probe {me['probe_id']}"
    bi = os.path.join(case, "build_info.json") if case else None
    if bi and os.path.exists(bi):
        rel = json.load(open(bi)).get("measurement_probe_relocated")
        if rel: meas_node, meas_src = int(rel["relocated"]["tree_node"]), f"RELOCATED probe {rel['relocated']['probe_id']} (package probe {me['probe_id']} failed the strict section rule; build_info)"
    i_m = M.point_of_tree_node(cl, meas_node); i_t = M.point_of_tree_node(cl, th["tree_node"])
    path = [i_m]
    while path[-1] in par: path.append(par[path[-1]])
    path = path[::-1]
    if i_t not in path: raise SystemExit(f"throat node {th['tree_node']} is not on the root -> measurement path (node {meas_node})")
    X = np.asarray(cl.points, float)[path]; arc = np.r_[0.0, np.cumsum(np.linalg.norm(np.diff(X, axis=0), axis=1))]
    rr = np.asarray(cl.point_data["r_ref_mm"], float)[path]
    info = dict(package=pkg["name"], throat_probe=th["probe_id"], throat_tree_node=int(th["tree_node"]), measurement=meas_src, measurement_tree_node=meas_node, path_nodes=len(path))
    return X, arc, rr, float(arc[path.index(i_t)]), float(arc[-1]), info

def straight_path(x_t, x_m, y=0.0, z=0.0, r_ref=2.0):
    x = np.linspace(x_t - 5.0, x_m + 5.0, 2001); X = np.c_[x, np.full_like(x, y), np.full_like(x, z)]; arc = x - x[0]
    return X, arc, np.full_like(x, r_ref), float(x_t - x[0]), float(x_m - x[0]), dict(straight_x=dict(x_throat_mm=x_t, x_meas_mm=x_m, y_mm=y, z_mm=z), r_ref_mm=r_ref)

def stations(s_t, s_m):
    s = list(np.arange(s_t + START_MM, s_m + 1e-9, STEP_MM))
    if not s or s_m - s[-1] > 1e-6: s.append(s_m)
    return np.array(s)

def least_aligned_axis(t):
    e = np.eye(3); k = int(np.argmin(np.round(np.abs(e @ t), 12))); v = e[k] - (e[k] @ t) * t; return v / np.linalg.norm(v)

def frames(X, arc, ss):
    """tangents, rotation-minimising normals N, binormals B at the stations, curvature (1/mm) and the Frenet normal per station"""
    T = np.array([polyline_tangent(X, arc, s) for s in ss]); K = []
    for s in ss:
        a, b = max(s - 1.0, arc[0]), min(s + 1.0, arc[-1]); K.append((polyline_tangent(X, arc, b) - polyline_tangent(X, arc, a)) / max(b - a, 1e-9))
    K = np.array(K); K = K - (K * T).sum(1)[:, None] * T; kap = np.linalg.norm(K, axis=1)
    N = np.zeros_like(T); N[0] = K[0] / kap[0] if kap[0] > KAPPA_MIN else least_aligned_axis(T[0])
    P_ = np.array([polyline_point(X, arc, s) for s in ss])
    for i in range(1, len(ss)):                    # double reflection (Wang et al. 2008)
        v1 = P_[i] - P_[i - 1]; c1 = v1 @ v1
        if c1 < 1e-18: N[i] = N[i - 1]; continue
        rL = N[i - 1] - (2 / c1) * (v1 @ N[i - 1]) * v1; tL = T[i - 1] - (2 / c1) * (v1 @ T[i - 1]) * v1
        v2 = T[i] - tL; c2 = v2 @ v2; N[i] = rL - (2 / c2) * (v2 @ rL) * v2 if c2 > 1e-18 else rL
        N[i] -= (N[i] @ T[i]) * T[i]; N[i] /= np.linalg.norm(N[i])
    B = np.cross(T, N)
    return P_, T, N, B, kap, K

# ---------------- sections
def profile_mesh(mesh, X, arc, rr, s_t, s_m, unit=1e-3, label=""):
    """rows of the profile for a pyvista internal mesh with cell data U (and p if present); X/arc in mm, mesh coordinates in metres (unit = 1e-3)"""
    import sections as S
    sec = S.Sectioner(mesh, robust=True); ss = stations(s_t, s_m); P_, T, N, B, kap, K = frames(X, arc, ss); rows = []
    for i, s in enumerate(ss):
        r_hint = float(np.interp(s, arc, rr)) * unit
        o = sec.section(P_[i] * unit, T[i], r_hint, need_fields=False)
        row = dict(label=label, station=i, s_mm=float(s), s_from_throat_mm=float(s - s_t), s_to_measurement_mm=float(s_m - s), x_mm=P_[i][0], y_mm=P_[i][1], z_mm=P_[i][2], t_x=T[i][0], t_y=T[i][1], t_z=T[i][2],
                   N_x=N[i][0], N_y=N[i][1], N_z=N[i][2], kappa_per_mm=float(kap[i]),
                   curvature_normal_angle_deg=(float(np.degrees(np.arctan2(K[i] @ B[i], K[i] @ N[i]))) if kap[i] > KAPPA_MIN else ""), section_ok=0)
        if o is None: rows.append(row); continue
        part = o["surface"]; A = np.asarray(part.cell_data["Area"]); C = np.asarray(part.cell_centers().points); U = np.asarray(part.cell_data["U"]); t = T[i]
        ua = U @ t; Atot = A.sum(); cA = (A[:, None] * C).sum(0) / Atot; req = np.sqrt(Atot / np.pi)
        def cen(w):
            sw = (w * A).sum(); return None if abs(sw) < 1e-300 else (w[:, None] * A[:, None] * C).sum(0) / sw
        res = {}
        for tag, w in (("", ua), ("_absw", np.abs(ua)), ("_fwd", np.clip(ua, 0, None))):
            c = cen(w)
            if c is None: res.update({f"oN{tag}": "", f"oB{tag}": "", f"offset_over_req{tag}": ""}); continue
            d = c - cA; d -= (d @ t) * t
            res.update({f"oN{tag}": float(d @ N[i] / req), f"oB{tag}": float(d @ B[i] / req), f"offset_over_req{tag}": float(np.linalg.norm(d) / req)})
        Q = float((ua * A).sum()); Qr = float((np.clip(ua, None, 0) * A).sum())
        row.update(section_ok=int(o["section_ok"]), area_mm2=Atot / unit ** 2, r_eq_mm=req / unit, station_centroid_offset_over_req=o["centroid_offset_over_req"], Q_through_mls=Q * 1e6, Q_reverse_mls=Qr * 1e6,
                   reverse_flow_fraction=(-Qr / (Q - Qr) if Q - Qr > 0 else ""), u_axial_max=float(ua.max()), n_polyhedra_cut=o["n_polyhedra_in_section"], n_boundary_loops=o["n_boundary_loops"], hole_area_fraction=o["hole_area_fraction"], **res,
                   direction_deg=(float(np.degrees(np.arctan2(res["oB"], res["oN"]))) if res["oN"] != "" else ""))
        if "p" in part.cell_data.keys(): row["p_mean_kin"] = float((np.asarray(part.cell_data["p"]) * A).sum() / Atot)
        rows.append(row)
    return rows

COLS = ["label", "station", "s_mm", "s_from_throat_mm", "s_to_measurement_mm", "x_mm", "y_mm", "z_mm", "section_ok", "area_mm2", "r_eq_mm", "station_centroid_offset_over_req", "offset_over_req", "oN", "oB", "direction_deg",
        "offset_over_req_absw", "oN_absw", "oB_absw", "offset_over_req_fwd", "oN_fwd", "oB_fwd", "Q_through_mls", "Q_reverse_mls", "reverse_flow_fraction", "u_axial_max", "p_mean_kin", "n_polyhedra_cut", "n_boundary_loops", "hole_area_fraction", "kappa_per_mm",
        "curvature_normal_angle_deg", "t_x", "t_y", "t_z", "N_x", "N_y", "N_z"]

def summarise(rows):
    v = [r for r in rows if r["section_ok"] == 1 and r.get("oN", "") != ""]
    if not v: return dict(n_stations=len(rows), n_valid=0)
    o = np.array([[r["oN"], r["oB"]] for r in v]); mag = np.linalg.norm(o, axis=1); ang = np.arctan2(o[:, 1], o[:, 0])
    R_ = float(np.abs(np.mean(np.exp(1j * ang))))         # mean resultant length of the directions: 1 = one persistent direction
    return dict(n_stations=len(rows), n_valid=len(v), max_offset_over_req=float(mag.max()), mean_offset_over_req=float(mag.mean()), s_from_throat_at_max_mm=float(v[int(mag.argmax())]["s_from_throat_mm"]),
                mean_oN=float(o[:, 0].mean()), mean_oB=float(o[:, 1].mean()), direction_persistence_R=R_, mean_direction_deg=float(np.degrees(np.angle(np.mean(np.exp(1j * ang))))),
                invalid_stations=[r["station"] for r in rows if r["section_ok"] != 1])

def write_rows(rows, out):
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

def profile(a):
    g = lambda f, k=1: a[a.index(f) + k] if f in a else None
    case = a[1]; label = g("--label") or os.path.basename(os.path.abspath(case))
    if "--package" in a: X, arc, rr, s_t, s_m, info = package_path(case, g("--package"), g("--pkg-root"))
    elif "--straight-x" in a:
        yz = (float(g("--axis-yz")), float(g("--axis-yz", 2))) if "--axis-yz" in a else (0.0, 0.0)
        X, arc, rr, s_t, s_m, info = straight_path(float(g("--straight-x")), float(g("--straight-x", 2)), *yz, r_ref=float(g("--r-ref") or 2.0))
    else: raise SystemExit(__doc__)
    import sections as S
    mesh, t = S.load_internal_mesh(case, g("--time"), fields=True)
    rows = profile_mesh(mesh, X, arc, rr, s_t, s_m, label=label)
    out = g("--out") or f"flow_state_{label}.csv"; write_rows(rows, out)
    summ = dict(case=os.path.abspath(case), label=label, time=t, cells=mesh.n_cells, path=info, start_mm=START_MM, step_mm=STEP_MM, **summarise(rows))
    json.dump(summ, open(g("--json") or os.path.splitext(out)[0] + ".json", "w"), indent=1, default=str)
    print(f"wrote {out}: {summ['n_valid']}/{summ['n_stations']} valid sections, time {t}; max offset/r_eq {summ.get('max_offset_over_req', float('nan')):.4f} at s-s_throat {summ.get('s_from_throat_at_max_mm')} mm, "
          f"direction persistence {summ.get('direction_persistence_R', float('nan')):.3f}")
    return rows, summ

def read_profile(f):
    rows = list(csv.DictReader(open(f)))
    for r in rows:
        for k in ("s_from_throat_mm", "s_to_measurement_mm", "oN", "oB", "offset_over_req"): r[k] = float(r[k]) if r.get(k) not in ("", None) else None
        r["section_ok"] = int(r["section_ok"])
    return rows

def specified_stations(rows):
    """the station keys (arc from the throat, mm, rounded) the pre-registered rule specifies for this profile: stations(0, L) with L = throat -> measurement arc (s_from_throat + s_to_measurement of the rows)"""
    Ls = {round(r["s_from_throat_mm"] + r["s_to_measurement_mm"], 6) for r in rows if r["s_from_throat_mm"] is not None and r["s_to_measurement_mm"] is not None}
    if len(Ls) != 1: return None, sorted(Ls)
    L = Ls.pop(); return [round(float(x), 6) for x in stations(0.0, L)], L

def compare(fa, fb, ffr=None):
    A, B = read_profile(fa), read_profile(fb); ka = {round(r["s_from_throat_mm"], 6): r for r in A}; kb = {round(r["s_from_throat_mm"], 6): r for r in B}
    diffs, excluded, missing, extra = [], [], {}, {}
    unmatched = sorted(set(ka) ^ set(kb))
    for tag, rows, k in (("A", A, ka), ("B", B, kb)):
        spec, L = specified_stations(rows)
        if spec is None: missing[tag] = f"throat -> measurement arc not unique in the profile rows: {L}"
        else:
            m = [x for x in spec if x not in k]; e = sorted(x for x in k if x not in spec)
            if m: missing[tag] = m
            if e: extra[tag] = e
    for key in sorted(set(ka) & set(kb)):
        r, q = ka[key], kb[key]
        if not (r["section_ok"] and q["section_ok"] and r["oN"] is not None and q["oN"] is not None):
            excluded.append(dict(s_from_throat_mm=key, invalid_in=[t for t, x in (("A", r), ("B", q)) if not (x["section_ok"] and x["oN"] is not None)])); continue
        d = float(np.hypot(r["oN"] - q["oN"], r["oB"] - q["oB"])); diffs.append(dict(s_from_throat_mm=key, vector_diff=d, magnitude_diff=abs(r["offset_over_req"] - q["offset_over_req"]),
                                                                                    offset_A=r["offset_over_req"], offset_B=q["offset_over_req"]))
    complete = bool(diffs) and not (excluded or unmatched or missing or extra)
    mx = max(diffs, key=lambda d: d["vector_diff"]) if diffs else None
    res = dict(profile_A=os.path.abspath(fa), profile_B=os.path.abspath(fb), n_specified=len(set(ka) | set(kb)), n_compared=len(diffs), complete_profile=complete,
               stations_excluded_invalid=excluded, stations_unmatched=unmatched, stations_missing=missing, stations_not_specified=extra, offset_tol=OFFSET_TOL, per_station=diffs)
    if complete:
        prof_ok = mx["vector_diff"] <= OFFSET_TOL
        res.update(max_vector_diff_offset_over_req=mx["vector_diff"], at_s_from_throat_mm=mx["s_from_throat_mm"], max_magnitude_diff=max(d["magnitude_diff"] for d in diffs), profile_criterion=("AGREE" if prof_ok else "DIFFER"))
    else:
        res.update(max_vector_diff_offset_over_req=None, at_s_from_throat_mm=None, profile_criterion="INDETERMINATE",
                   indeterminate_reason=("pre-registered statistic = max over the FULL specified profile; not available: " + "; ".join(
                       ([f"invalid section at s-s_throat {[e['s_from_throat_mm'] for e in excluded]} mm"] if excluded else []) + ([f"unmatched stations {unmatched}"] if unmatched else [])
                       + ([f"missing stations {missing}"] if missing else []) + ([f"stations outside the specified profile {extra}"] if extra else []) + ([] if diffs else ["no station valid in both"]))),
                   subset_max_vector_diff_INFORMATION_ONLY=(mx["vector_diff"] if mx else None), subset_at_s_from_throat_mm=(mx["s_from_throat_mm"] if mx else None),
                   subset_max_magnitude_diff_INFORMATION_ONLY=(max(d["magnitude_diff"] for d in diffs) if diffs else None),
                   subset_note=("max over the stations valid in both, NOT the pre-registered statistic. The full-profile max is >= this value, so a subset max above the tolerance bounds the full statistic "
                                "above it as well, while a subset max below it says nothing about the excluded stations; no replacement rule is pre-registered, so the verdict stays INDETERMINATE either way."),
                   subset_max_exceeds_tol=(bool(mx["vector_diff"] > OFFSET_TOL) if mx else None))
    if ffr is not None:
        dffr = abs(ffr[0] - ffr[1]); res.update(FFR_A=ffr[0], FFR_B=ffr[1], abs_dFFR_A_minus_dFFR_B=dffr, U3D=U3D, ffr_criterion=("AGREE" if dffr < U3D else "DIFFER"))
        res["verdict"] = "STATES INDETERMINATE" if not complete else ("STATES AGREE" if (res["profile_criterion"] == "AGREE" and dffr < U3D) else "STATES DIFFER")
    else: res["verdict"] = ("STATES INDETERMINATE" if not complete else "STATES AGREE" if res["profile_criterion"] == "AGREE" else "STATES DIFFER") + " (profile criterion only: FFR criterion not evaluated, no --ffr)"
    return res

def main(a):
    if len(a) < 2: raise SystemExit(__doc__)
    if a[0] == "profile": profile(a)
    elif a[0] == "compare":
        ffr = (float(a[a.index("--ffr") + 1]), float(a[a.index("--ffr") + 2])) if "--ffr" in a else None
        r = compare(a[1], a[2], ffr)
        if "--json" in a: json.dump(r, open(a[a.index("--json") + 1], "w"), indent=1)
        tail = f"; |FFR_A - FFR_B| = {r['abs_dFFR_A_minus_dFFR_B']:.6f} (tol {U3D}, ffr criterion {r['ffr_criterion']})" if ffr else ""
        if r["complete_profile"]:
            print(f"{r['verdict']}: max |o_A - o_B| over the full profile = {r['max_vector_diff_offset_over_req']:.4f} at s-s_throat {r['at_s_from_throat_mm']} mm (tol {OFFSET_TOL}; all {r['n_compared']} stations valid in both){tail}")
        else:
            sm = r["subset_max_vector_diff_INFORMATION_ONLY"]
            print(f"{r['verdict']}: {r['indeterminate_reason']}. Information only: max |o_A - o_B| over the {r['n_compared']}/{r['n_specified']} stations valid in both = "
                  + (f"{sm:.4f} at s-s_throat {r['subset_at_s_from_throat_mm']} mm ({'above' if r['subset_max_exceeds_tol'] else 'not above'} tol {OFFSET_TOL})" if sm is not None else "n/a") + tail)
    else: raise SystemExit(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
