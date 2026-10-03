"""Helpers of post_case_generic.sh (Task C end-to-end post-solve runner, any Gate-M1-format package: scan-14 M1, P5). Reads only the case (monitors, logs, build_info, reconstructed time directory names), the mesh/geometry
gate json files and small csv files: no fields, no 0D code.
usage: post_helpers.py finished <case> [--json out.json]                exit 0 iff the LAST run of log.simpleFoam completed (run_completion: exact 'End' after the last 'Time = <t>' line, no later run header /
                                                                         'Starting time loop' / Time line, i.e. no appended partial run) AND that last Time equals the case's endTime (system/controlDict)
       post_helpers.py package-check <case> <package> [--pkg-root R] --json out.json    resolve the package (m1_package.resolve_pkg_dir) and verify its files against build_info.json package_hashes;
                                                                         prints the verified absolute package directory; exit 1 on any mismatch (nothing may be generated from an unverified package)
       post_helpers.py radius-check <case> <pkg_dir> <radius_prefix>    exit 0 iff <prefix>_provenance.json records the SAME mesh (sha256 of the case's constant/polyMesh files) and package hashes as now and the
                                                                         three radius files are unchanged; writes the current hashes to <prefix>_provenance.pending.json either way
       post_helpers.py radius-commit <radius_prefix>                    after a regeneration: the pending provenance + the sha256 of the new radius files -> <prefix>_provenance.json
       post_helpers.py reconstruct-check <case> <out.json>               after reconstructPar -latestTime: the reconstructed latest time equals processor0's latest time, holds U and p (non-empty), log ends with End;
                                                                         exit 1 otherwise (processor directories are NEVER touched by this runner)
       post_helpers.py fill <case> <package> <out.json> [--gates F] [--mesh-gates F] [--d34 F]     geometry/mesh columns of M1_results.csv (generic make_fill_json; sources recorded, missing values left empty) + the
                                                                         machine-readable 'flags' column and the D3/D4 columns (FLAGS below)
       post_helpers.py history <case> <out.csv> [--probes M1_probes.csv] [--json summary.json]   per-iteration measurement-probe history (D8 monitors measurementP/measurementFlux, throatP/throatFlux and
                                                                         measurementOrigP/measurementOrigFlux when present) + summary (last value, last-100 mean and band, cross-check against the probes csv)
       post_helpers.py cells <case>                                      number of cells (constant/polyMesh/owner header note nCells)
       post_helpers.py peak-ram <case>                                   peak RAM in GB when available (env PEAK_RAM_GB; else the memlog sampler $MEMLOG through u3d_make_csv.peak_ram_gb), else empty
       post_helpers.py summary <case> <out_dir> <label> <mode> <out.json> [file ...]       post_summary json: verdict, wall clock, cells, RAM, measurement probe used, sha256 of every output, and with
                                                                         $REF_FFR [$REF_TOL] the comparison of the package measurement-probe section value with a reference (Task A: 0.8697574904997768) file
Mesh-gate discovery (fill): --mesh-gates, else $MESH_GATES_JSON, else <build_info mesh_source_dir>/mesh_gates.json, else the mesh directory under $P/m1/mesh/* or $P/p5/mesh/* whose constant/polyMesh/owner is the SAME
inode as the case's (hard-linked mesh). Geometry gates: --gates, else $GATES_JSON, else the extension json the case was built with if it is a gates.json or names one ('source'), else $P/p5/out/<package>/gates.json,
else (scan 14 only) $P/m1/out/<error_type>/gates.json. D3/D4 json (d34_generic.py output): --d34, else $D34_JSON, else d34.json next to the mesh gates json, else <build_info mesh_source_dir>/d34.json, else the
hard-linked mesh directory's d34.json, else $P/p5/mesh/<scan>/d34.json. Every source used (or missing) is written into the json and the notes.
GEOMETRY STATUS (D10, audit P5 Sol finding 2): geometry_step_ok = all DECISIVE geometry gates pass (gates.json GATES_DECISIVE / ALL_GATES_PASS of the fixed builder; for an older gates.json: GATES minus the
reported-only literal absolute r_target check); geometry_all_gates_pass_including_reported = every gate (the absolute check included). Both are written.
FLAGS (audit P5 Sol findings 5, 6): 'flags' = ';'-joined, fixed order (FLAG_ORDER), 'NONE' if empty: D2_RELATIVE_THROAT_GATE_FAIL, LESION_PURITY_GATE_FAIL, POSITIVE_CONTROL_UNDETECTED, SELF_INTERSECTION,
GEOMETRY_GATE_FAIL:<gate> (any other decisive gate), D3_FAIL, D4_FAIL (strict checkMesh entity < 2 mm from the throat / measurement probe, d34.json), CHECKMESH_STANDARD_FAIL, MEASUREMENT_PROBE_RELOCATED (build_info),
OUTLET_LOST_IN_MESH (0-face outlet patch, build_info), MANUAL_REPAIR_NEEDED (only if a pipeline record says so: a truthy manual_repair_needed / manual_repair key in gates.json, mesh_gates.json or build_info),
NOT_CONVERGED (added by m1_results.py from the analysis verdict), and GEOMETRY_GATES_MISSING / MESH_GATES_MISSING / D34_MISSING when a source is not found."""
import sys, os, re, csv, json, glob, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pf_common as C

PILOT = os.environ.get("P") or "/home/azan/paper6_t6_work/scratchpad/item3_M1_pilot"
VMTK_ENV = os.environ.get("VMTK_ENV", "/home/azan/paper6_t6_work/scratchpad/micromamba/envs/vmtk")
AREA_TOL = 0.005        # monitor vs reconstructed-section area (same plane): scan 14 agreed to 6 digits
MONITORS = ("measurementP", "measurementFlux", "throatP", "throatFlux", "measurementOrigP", "measurementOrigFlux")

HEADER_RE = re.compile(r"^(Exec\s*:|Build\s*:|Starting time loop\b)")
TIME_RE = re.compile(r"^Time = (\S+)$")

def control_end_time(case):
    f = f"{case}/system/controlDict"
    m = re.search(r"^\s*endTime\s+([^\s;]+)\s*;", open(f).read(), re.M) if os.path.exists(f) else None
    try: return float(m.group(1)) if m else None
    except ValueError: return None

def run_completion(case):
    """completion of the LAST run of <case>/log.simpleFoam, defined on the log tail: the last run starts at the last header line (Build:/Exec:/'Starting time loop'); it is complete iff it has a 'Time = <t>'
    line, the last such line is followed by a line that is exactly 'End', nothing after that End is a header / 'Starting time loop' / Time / FOAM FATAL line (no appended run, partial or not), and
    <t> equals endTime of system/controlDict (a run stopped early, by residualControl or by hand, is not a finished budget run). Returns (ok, detail)."""
    f = f"{case}/log.simpleFoam"; d = dict(log=f, end_time_controlDict=control_end_time(case)); fails = []
    if not os.path.exists(f): return False, dict(d, fails=["no log.simpleFoam"])
    L = [ln.rstrip("\r\n") for ln in open(f, errors="replace")]
    hdr = [i for i, ln in enumerate(L) if HEADER_RE.match(ln)]; tim = [i for i, ln in enumerate(L) if TIME_RE.match(ln)]; end = [i for i, ln in enumerate(L) if ln == "End"]
    i_h = hdr[-1] if hdr else -1; i_t = tim[-1] if tim else None; i_e = end[-1] if end else None
    d.update(n_run_headers=sum(1 for i in hdr if L[i].startswith("Starting time loop")), last_header_line=i_h + 1, last_time_line=(i_t + 1 if i_t is not None else None), last_end_line=(i_e + 1 if i_e is not None else None),
             last_time=(TIME_RE.match(L[i_t]).group(1) if i_t is not None else None))
    if i_t is None or i_t < i_h: fails.append("the last run (from the last header line) has no 'Time = ' line")
    if i_e is None: fails.append("no line that is exactly 'End'")
    elif i_t is not None and i_e < i_t: fails.append(f"the last 'End' (line {i_e + 1}) precedes the last 'Time = ' line ({i_t + 1}): a later run is running or aborted")
    elif i_e < i_h: fails.append(f"the last 'End' (line {i_e + 1}) precedes the last run header (line {i_h + 1}): an appended run did not complete")
    if i_e is not None:
        late = [f"{i + 1}: {L[i][:60]}" for i in range(i_e + 1, len(L)) if HEADER_RE.match(L[i]) or TIME_RE.match(L[i]) or "FOAM FATAL" in L[i]]
        if late: fails.append(f"lines after the last End: {late[:3]}")
    if not fails:
        try: t = float(d["last_time"])
        except (TypeError, ValueError): t = None
        if d["end_time_controlDict"] is None: fails.append("endTime of system/controlDict not readable")
        elif t is None or abs(t - d["end_time_controlDict"]) > 1e-9 * max(1.0, abs(d["end_time_controlDict"])): fails.append(f"last Time {d['last_time']} != endTime {d['end_time_controlDict']} (run stopped before the budget)")
    d.update(fails=fails, ok=not fails)
    return not fails, d

def log_finished(case):
    return run_completion(case)[0]

def time_dirs(d):
    out = []
    for n in os.listdir(d) if os.path.isdir(d) else []:
        try: v = float(n)
        except ValueError: continue
        if os.path.isdir(os.path.join(d, n)): out.append((v, n))
    return sorted(out)

def reconstruct_check(case, out):
    r = dict(case=os.path.abspath(case)); t_case = time_dirs(case); t_p0 = time_dirs(f"{case}/processor0")
    r["processor_dirs"] = sorted(os.path.basename(p) for p in glob.glob(f"{case}/processor*"))
    r["latest_processor0"] = t_p0[-1][1] if t_p0 else None; r["latest_reconstructed"] = t_case[-1][1] if t_case else None
    fails = []
    if not t_p0: fails.append("no time directory in processor0")
    if not t_case or (t_p0 and t_case[-1][0] != t_p0[-1][0]): fails.append(f"latest reconstructed time {r['latest_reconstructed']} != processor0 latest {r['latest_processor0']}")
    if t_case and t_case[-1][0] > 0:
        d = f"{case}/{t_case[-1][1]}"; r["fields"] = {f: os.path.getsize(f"{d}/{f}") for f in ("U", "p") if os.path.exists(f"{d}/{f}")}
        fails += [f"field {f} missing or empty in {t_case[-1][1]}" for f in ("U", "p") if r["fields"].get(f, 0) <= 0]
    else: fails.append("no reconstructed solution time (> 0)")
    lg = f"{case}/log.reconstructPar"
    if not (os.path.exists(lg) and any(ln.strip() == "End" for ln in open(lg, errors="replace"))): fails.append("log.reconstructPar missing or without End")
    r.update(fails=fails, ok=not fails, note="processor directories are NOT removed by post_case_generic.sh; remove them only after this check is ok and the outputs are verified")
    json.dump(r, open(out, "w"), indent=1); print(("RECONSTRUCT OK: " if r["ok"] else "RECONSTRUCT FAILED: ") + (f"time {r['latest_reconstructed']}, fields {r.get('fields')}" if r["ok"] else "; ".join(fails)))
    return r["ok"]

def cells(case):
    f = f"{C.poly_dir(case)}/owner"
    with open(f, "rb") as fh: head = fh.read(4096).decode("latin-1")
    m = re.search(r"nCells:\s*(\d+)", head)
    if m: return int(m.group(1))
    lg = f"{case}/log.decomposePar"          # cfMesh owner files carry no nCells note: sum of the per-processor cell counts of decomposePar
    if os.path.exists(lg):
        n = [int(x) for x in re.findall(r"^\s+Processor \d+\s*\n\s+Number of cells = (\d+)\s*$", open(lg, errors="replace").read(), re.M)]
        if n: return sum(n)
    return None

def peak_ram(case):
    if os.environ.get("PEAK_RAM_GB"): return os.environ["PEAK_RAM_GB"], "env PEAK_RAM_GB"
    ml = os.environ.get("MEMLOG")
    if ml and os.path.exists(ml):
        sys.path.insert(0, f"{PILOT}/u3d")
        try:
            import u3d_make_csv as U
            t = U.timing(case); v = U.peak_ram_gb(t["start_clock"], t["end_clock"], ml)
            if v is not None: return str(v), f"memlog {ml} (sum of all simpleFoam RSS on the host inside the solve window){'; ' + U.ram_dating_warning if U.ram_dating_warning else ''}"
        except Exception as e: return "", f"memlog {ml} not usable: {e}"
    return "", "not available (no PEAK_RAM_GB, no MEMLOG sampler file)"

# ---------------- fill json (generic make_fill_json)
def vmtk_version():
    for f in sorted(glob.glob(f"{VMTK_ENV}/conda-meta/vmtk-[0-9]*.json")):
        try: return json.load(open(f))["version"]
        except (OSError, ValueError, KeyError): pass
    return "not recorded"

def same_inode_mesh(case):
    try: st = os.stat(f"{C.poly_dir(case)}/owner")
    except (OSError, SystemExit): return None
    for d in sorted(glob.glob(f"{PILOT}/m1/mesh/*") + glob.glob(f"{PILOT}/p5/mesh/*")):
        f = f"{d}/constant/polyMesh/owner"
        if os.path.exists(f) and os.stat(f).st_ino == st.st_ino and os.stat(f).st_dev == st.st_dev: return d
    return None

def find_mesh_gates(case, info, arg=None):
    for src, f in (("--mesh-gates", arg), ("$MESH_GATES_JSON", os.environ.get("MESH_GATES_JSON")),
                   ("build_info mesh_source_dir", f"{info['mesh_source_dir']}/mesh_gates.json" if info.get("mesh_source_dir") else None)):
        if f and os.path.exists(f): return f, src
    d = same_inode_mesh(case)
    if d and os.path.exists(f"{d}/mesh_gates.json"): return f"{d}/mesh_gates.json", "hard-linked mesh directory (same owner inode)"
    return None, "not found"

def find_gates(info, package, arg=None):
    cands = [("--gates", arg), ("$GATES_JSON", os.environ.get("GATES_JSON"))]
    es = info.get("extension_source", "")
    if es.startswith("as-built, from "):
        f = es[len("as-built, from "):]
        try:
            j = json.load(open(f))
            if "ALL_GATES_PASS" in j: cands.append(("extension json of the build (a gates.json)", f))
            elif isinstance(j.get("source"), str): cands.append(("'source' of the build's extension json", os.path.join(PILOT, j["source"].split()[0])))
        except (OSError, ValueError): pass
    cands.append(("p5/out/<package>/gates.json", f"{PILOT}/p5/out/{package}/gates.json"))
    if str((info.get("instance") or {}).get("scan")) == "14": cands.append(("m1/out/<error_type>/gates.json (scan 14)", f"{PILOT}/m1/out/{info.get('error_type')}/gates.json"))
    for src, f in cands:
        if f and os.path.exists(f): return f, src
    return None, "not found"

def find_d34(case, info, mesh_gates_file=None, arg=None):
    scan = str((info.get("instance") or {}).get("scan", ""))
    cands = [("--d34", arg), ("$D34_JSON", os.environ.get("D34_JSON")), ("next to the mesh gates json", os.path.join(os.path.dirname(mesh_gates_file), "d34.json") if mesh_gates_file else None),
             ("build_info mesh_source_dir", f"{info['mesh_source_dir']}/d34.json" if info.get("mesh_source_dir") else None)]
    d = same_inode_mesh(case); cands.append(("hard-linked mesh directory (same owner inode)", f"{d}/d34.json" if d else None))
    if scan: cands.append(("p5/mesh/<scan>/d34.json", f"{PILOT}/p5/mesh/{scan}/d34.json"))
    for src, f in cands:
        if f and os.path.exists(f): return f, src
    return None, "not found"

def d34_entry(d, scan):
    """the case entry of a d34_generic.py json ({label: {...}}; a bare entry is accepted)"""
    if "D3_verdict" in d: return d
    if str(scan) in d: return d[str(scan)]
    if len(d) == 1: return next(iter(d.values()))
    raise SystemExit(f"d34 json holds {sorted(d)}: no entry for scan {scan}")

REPORTED_NON_DECISIVE_GATES = ("lesion_literal_absolute_r_target_check",)       # D10: reported, not decisive (same list as p5/build_m1_geometry.py)
GATE_FLAGS = {"lesion_relative_throat_gate": "D2_RELATIVE_THROAT_GATE_FAIL", "lesion_purity_fold_window_edge_labels": "LESION_PURITY_GATE_FAIL",
              "self_intersection_positive_control_flagged": "POSITIVE_CONTROL_UNDETECTED", "surfaceCheck_not_self_intersecting": "SELF_INTERSECTION"}
FLAG_ORDER = ["GEOMETRY_GATES_MISSING", "D2_RELATIVE_THROAT_GATE_FAIL", "LESION_PURITY_GATE_FAIL", "POSITIVE_CONTROL_UNDETECTED", "SELF_INTERSECTION", "GEOMETRY_GATE_FAIL", "D34_MISSING", "D3_FAIL", "D4_FAIL",
              "MESH_GATES_MISSING", "CHECKMESH_STANDARD_FAIL", "MEASUREMENT_PROBE_RELOCATED", "OUTLET_LOST_IN_MESH", "MANUAL_REPAIR_NEEDED", "NOT_CONVERGED"]

def flag_key(f):
    b = f.split(":")[0]
    return (FLAG_ORDER.index(b) if b in FLAG_ORDER else len(FLAG_ORDER), f)

def merge_flags(*lists):
    """union of flag lists / ';'-strings, fixed order; 'NONE' and empty entries dropped"""
    out = set()
    for l in lists:
        for f in (l.split(";") if isinstance(l, str) else (l or [])):
            if f and f.strip() and f.strip() != "NONE": out.add(f.strip())
    return sorted(out, key=flag_key)

def flags_str(fl): return ";".join(fl) if fl else "NONE"

def geometry_gate_status(g):
    """(decisive gates, reported-only gates, all decisive pass, all pass incl. reported) of a gates.json; an older gates.json (no GATES_DECISIVE) is split here by REPORTED_NON_DECISIVE_GATES"""
    gs = g.get("GATES") or {}
    dec = g.get("GATES_DECISIVE") if isinstance(g.get("GATES_DECISIVE"), dict) else {k: v for k, v in gs.items() if k not in REPORTED_NON_DECISIVE_GATES}
    rpt = g.get("GATES_REPORTED_NON_DECISIVE") if isinstance(g.get("GATES_REPORTED_NON_DECISIVE"), dict) else {k: v for k, v in gs.items() if k in REPORTED_NON_DECISIVE_GATES}
    return dec, rpt, bool(dec) and all(bool(v) for v in dec.values()), bool(gs) and all(bool(v) for v in gs.values())

def manual_repair_record(*docs):
    """True only if a pipeline record says a manual repair was needed/done (a truthy 'manual_repair_needed' or 'manual_repair' key at the top level of a gates/mesh-gates/build_info json); (value, where)"""
    for name, d in docs:
        for k in ("manual_repair_needed", "manual_repair"):
            if isinstance(d, dict) and d.get(k): return True, f"{name}:{k}={d[k]}"
    return False, "no manual-repair record in " + ", ".join(n for n, d in docs if isinstance(d, dict))

def fill(case, package, out, gates_arg=None, mesh_arg=None, d34_arg=None):
    info = json.load(open(f"{case}/build_info.json")); notes = []; flags = []; o = dict(mesher="cfMesh cartesianMesh (OpenFOAM ESI v2406)", openfoam_version="ESI v2406", vmtk_version=vmtk_version(),
                                                                                              extension_lengths_mm=json.dumps(info.get("extension_lengths_mm", {})))
    gf, gsrc = find_gates(info, package, gates_arg); mf, msrc = find_mesh_gates(case, info, mesh_arg); df, dsrc = find_d34(case, info, mf, d34_arg)
    o["sources"] = dict(geometry_gates=gf, geometry_gates_source=gsrc, mesh_gates=mf, mesh_gates_source=msrc, d34=df, d34_source=dsrc)
    g = m = None
    if gf:
        g = json.load(open(gf)); dec, rpt, ok_dec, ok_all = geometry_gate_status(g)
        o.update(geometry_step_ok=ok_dec, geometry_all_gates_pass_including_reported=ok_all)
        fdec = [k for k, v in dec.items() if not v]; frpt = [k for k, v in rpt.items() if not v]
        flags += [GATE_FLAGS.get(k, f"GEOMETRY_GATE_FAIL:{k}") for k in fdec]
        o["geometry_gates_failed_decisive"] = fdec; o["geometry_gates_failed_reported_only"] = frpt
        try: o["n_surface_components"] = g["final_surface"]["topology"]["connected_components"]
        except (KeyError, TypeError): notes.append("n_surface_components not in the geometry gates")
        notes.append((f"failed DECISIVE geometry gates: {fdec}" if fdec else "all decisive geometry gates passed") + (f"; reported-only (D10, non-decisive) check failed: {frpt}" if frpt else ""))
        les = g.get("lesion") if isinstance(g.get("lesion"), dict) else {}
        th = les.get("throat") if isinstance(les.get("throat"), dict) else None
        if th:
            try:
                o.update(throat_radius_asbuilt_mm=th["asbuilt_mm"]["area_equiv"], throat_radius_target_mm=th["r_target_mm"], throat_pct_error=th["LITERAL_ABSOLUTE_vs_r_target"]["area_equiv_pct"], subdivision_edge_mm=les.get("h_max_mm"))
                notes.append(f"throat as-built radius is the area-equivalent one; relative gate {th['RELATIVE_GATE']['area_equiv_pct']} %")
            except (KeyError, TypeError) as e: notes.append(f"throat gate keys missing in {os.path.basename(gf)}: {e}")
        else: notes.append("no lesion throat block in the geometry gates")
    else: notes.append("geometry gates json NOT FOUND: geometry columns left empty"); flags.append("GEOMETRY_GATES_MISSING")
    if mf:
        m = json.load(open(mf))
        if not m.get("checkMesh_standard_OK"): flags.append("CHECKMESH_STANDARD_FAIL")
        o.update(n_cells=m.get("cells"), checkMesh_ok=bool(m.get("checkMesh_standard_OK")), max_nonortho_deg=m.get("max_nonortho"), max_skewness=m.get("max_skew"), neg_volumes=0, n_bl_layers=4)
        cats = m.get("cells_across_throat_diameter"); o["throat_cells_across"] = cats["min"] if isinstance(cats, dict) else cats
        o["throat_cell_um_p95"] = (m.get("cell_size_um_throat_pm2mm_arc") or {}).get("p95")
        notes.append(f"strict checkMesh failed checks: {m.get('strict_failed_checks')} (standard checkMesh {'OK' if m.get('checkMesh_standard_OK') else 'NOT OK'}); mesh GATES_PASS {m.get('GATES_PASS')}")
    else: notes.append("mesh gates json NOT FOUND: mesh columns left empty (n_cells from the polyMesh in post_summary.json)"); flags.append("MESH_GATES_MISSING")
    if df:
        e = d34_entry(json.load(open(df)), (info.get("instance") or {}).get("scan"))
        o.update(D3_verdict=e.get("D3_verdict"), D4_verdict=e.get("D4_verdict"), D34_min_dist_throat_mm=e.get("min_over_checks_throat_centre_mm"), D34_min_dist_measurement_mm=e.get("min_over_checks_measurement_centre_mm"),
                 D34_checks_within_2mm=";".join(e.get("checks_within_2mm") or []), D34_probes=f"throat {e.get('throat_probe')}, measurement {e.get('measurement_probe')}")
        flags += [f"{k}_FAIL" for k in ("D3", "D4") if e.get(f"{k}_verdict") != "PASS"]
        notes.append(f"D3 {e.get('D3_verdict')} / D4 {e.get('D4_verdict')}: nearest strict-checkMesh entity {e.get('min_over_checks_throat_centre_mm'):.3f} mm from the throat probe {e.get('throat_probe')}, "
                     f"{e.get('min_over_checks_measurement_centre_mm'):.3f} mm from the measurement probe {e.get('measurement_probe')} (limit 2 mm; checks within 2 mm: {e.get('checks_within_2mm')})")
    else: notes.append("d34.json NOT FOUND: D3/D4 columns left empty"); flags.append("D34_MISSING")
    rel = info.get("measurement_probe_relocated")
    if rel:
        flags.append("MEASUREMENT_PROBE_RELOCATED")
        if df and e.get("measurement_probe") == rel["original"]["probe_id"]: notes.append(f"D3/D4 measurement distance refers to the PACKAGE probe {rel['original']['probe_id']}; the measurementP monitor uses the relocated {rel['relocated']['probe_id']}")
    lost = C.lost_outlets(info); o["outlets_lost_in_mesh"] = ";".join(x["patch"] for x in lost)
    if lost:
        flags.append("OUTLET_LOST_IN_MESH")
        for x in lost: notes.append(f"OUTLET_LOST_IN_MESH {x['patch']}: 0 faces, Q = 0 reported, p N/A, territory CLOSED (bc_C target {x['Q_target_m3s'] * 1e6:.5f} mL/s not delivered, bc_A R {x.get('R_used')} not applied); BC-error criteria over the outlets in the mesh only")
    mr, mr_src = manual_repair_record(("gates.json", g), ("mesh_gates.json", m), ("build_info.json", info))
    o["manual_repair_needed"] = mr; o["sources"]["manual_repair_needed"] = mr_src
    if mr: flags.append("MANUAL_REPAIR_NEEDED")
    o["flags"] = flags_str(merge_flags(flags))
    e0 = info.get("e0_guard") or {}; notes.append(f"E0 guard {e0.get('status', 'not recorded')}" + (f" (waiver: {e0['waiver']})" if e0.get("waiver") else ""))
    notes.append(f"extension lengths: {info.get('extension_source', 'not recorded')}")
    notes.append("vmtk use: vmtksurfacesmoothing (Taubin, 30 it) only; no vmtksurfaceremeshing")
    o["notes"] = " | ".join(notes)
    json.dump(o, open(out, "w"), indent=1, default=str); print(f"wrote {out} (geometry gates: {gf} [{gsrc}]; mesh gates: {mf} [{msrc}]; d34: {df} [{dsrc}]): flags {o['flags']}")

# ---------------- measurement-probe history
def read_mon(case, name):
    f = f"{case}/postProcessing/{name}/0/surfaceFieldValue.dat"
    if not os.path.exists(f): return None
    hdr = None
    with open(f) as fh:
        for ln in fh:
            if not ln.startswith("#"): break
            if ln[1:].strip().startswith("Time"): hdr = ln[1:].split()
    d = np.loadtxt(f, comments="#", ndmin=2); vc = C.value_column(f); ac = hdr.index("Area") if hdr and "Area" in hdr else None
    return dict(it=d[:, 0].astype(int), v=d[:, vc], area=(d[:, ac] if ac is not None else None))

def history(case, out, probes=None, js=None):
    info = json.load(open(f"{case}/build_info.json")); mons = {m: read_mon(case, m) for m in MONITORS}; mons = {k: v for k, v in mons.items() if v is not None}
    if "measurementP" not in mons: print(f"{case}: no measurementP monitor (pre-D8 case): history has only the monitors present {sorted(mons)}")
    its = sorted(set().union(*[set(v["it"].tolist()) for v in mons.values()])) if mons else []
    cols = ["iteration"]
    for k, v in mons.items():
        if k.endswith("P"): cols += [f"{k}_area_m2", f"{k}_p_kin", f"{k}_p_Pa", f"{k}_p_over_Paorta"]
        else: cols += [f"{k}_area_m2", f"{k}_Q_m3s", f"{k}_Q_mls"]
    rows = []
    idx = {k: {int(i): j for j, i in enumerate(v["it"])} for k, v in mons.items()}
    for it in its:
        r = dict(iteration=it)
        for k, v in mons.items():
            j = idx[k].get(it)
            if j is None: continue
            r[f"{k}_area_m2"] = v["area"][j] if v["area"] is not None else ""
            if k.endswith("P"): r.update({f"{k}_p_kin": v["v"][j], f"{k}_p_Pa": v["v"][j] * C.RHO, f"{k}_p_over_Paorta": v["v"][j] * C.RHO / C.P_AORTA_PA})
            else: r.update({f"{k}_Q_m3s": v["v"][j], f"{k}_Q_mls": v["v"][j] * 1e6})
        rows.append(r)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    summ = dict(case=os.path.abspath(case), measurement_probe_used=info.get("measurement_probe_used") or info.get("measurement_probe"), measurement_probe_package=info.get("measurement_probe"),
                relocated=bool(info.get("measurement_probe_relocated")), monitors=sorted(mons), n_iterations=len(its), every_iteration={k: bool(len(v["it"]) == (v["it"][-1] - v["it"][0] + 1)) for k, v in mons.items()})
    for k, v in mons.items():
        w = v["v"][-100:]; s = dict(last_iteration=int(v["it"][-1]), last=float(v["v"][-1]), last100_mean=float(w.mean()), last100_band_rel=float((w.max() - w.min()) / abs(w.mean())) if w.mean() else None,
                                    area_last_m2=(float(v["area"][-1]) if v["area"] is not None else None))
        if k.endswith("P"): s.update(last_p_over_Paorta=s["last"] * C.RHO / C.P_AORTA_PA, last100_mean_p_over_Paorta=s["last100_mean"] * C.RHO / C.P_AORTA_PA)
        summ[k] = s
    if probes and os.path.exists(probes):
        pr = list(csv.DictReader(open(probes))); summ["cross_check_probes_csv"] = {}
        for mon_name, kind in (("measurementP", "measurement_relocated" if summ["relocated"] else "measurement"), ("measurementOrigP", "measurement"), ("throatP", "throat")):
            if mon_name not in mons: continue
            r = [x for x in pr if x["kind"] == kind]
            if not (len(r) == 1 and r[0].get("p_over_Paorta")): summ["cross_check_probes_csv"][mon_name] = f"no unique valid '{kind}' row with p in {os.path.basename(probes)}"; continue
            sec = float(r[0]["p_over_Paorta"]); mon = summ[mon_name]["last_p_over_Paorta"]; am = (summ[mon_name]["area_last_m2"] or 0) * 1e6; asec = float(r[0]["section_area_mm2"])
            cc = dict(probe_id=r[0]["probe_id"], kind=kind, section_p_over_Paorta=sec, section_area_mm2=asec, monitor_last_p_over_Paorta=mon, monitor_area_mm2=am, difference=mon - sec, area_rel_diff=am / asec - 1,
                      note="monitor = sampledPlane areaAverage on the bounded plane at the last iteration; section = connected-section pullback of the reconstructed fields (pf/m1_probes.py): same plane, different sampling (cell-centre cut vs pyvista slice)")
            cc["area_flag"] = ("OK" if abs(cc["area_rel_diff"]) <= AREA_TOL else
                               f"AREA MISMATCH > {AREA_TOL:.1%}: the monitor plane and the reconstructed section are not the same section (OpenFOAM cut of a plane lying on mesh faces, or a pyvista section with holes): check before using either value")
            summ["cross_check_probes_csv"][mon_name] = cc
            print(f"cross-check {mon_name} vs probes row {r[0]['probe_id']} ({kind}): p/P_aorta {mon:.6f} vs {sec:.6f} (diff {mon - sec:+.2e}); area {am:.5f} vs {asec:.5f} mm2: {cc['area_flag']}")
    if js: json.dump(summ, open(js, "w"), indent=1)
    print(f"wrote {out}: {len(rows)} iterations, monitors {sorted(mons)}" + (f"; measurementP last p/P_aorta {summ['measurementP']['last_p_over_Paorta']:.6f}" if "measurementP" in summ else ""))
    return summ

# ---------------- package verification, radius provenance
def package_check(case, package, out, pkg_root=None):
    import m1_package as M
    info = json.load(open(f"{case}/build_info.json")); r = dict(case=os.path.abspath(case), package_arg=package, pkg_root_arg=pkg_root)
    try: d = M.resolve_pkg_dir(package, pkg_root)
    except SystemExit as e: d = None; r["fails"] = [f"package not resolved: {e}"]
    if d:
        r.update(package_dir=d, recorded=info.get("package_hashes"), now=M.package_hashes(d)); r["fails"] = M.verify_against_build(d, info)
    r["ok"] = not r["fails"]
    if out: json.dump(r, open(out, "w"), indent=1)
    if r["ok"]: print(d); return True
    print(f"PACKAGE NOT VERIFIED against {case}/build_info.json package_hashes ({d}): " + "; ".join(r["fails"]), file=sys.stderr); return False

def mesh_hash(case):
    """sha256 over the case's polyMesh files (name + content, sorted; .gz variants included)"""
    pd = C.poly_dir(case); h = hashlib.sha256(); files = sorted(n for n in os.listdir(pd) if os.path.isfile(f"{pd}/{n}"))
    for n in files:
        h.update(n.encode() + b"\0")
        with open(f"{pd}/{n}", "rb") as fh:
            for b in iter(lambda: fh.read(1 << 22), b""): h.update(b)
    return dict(polyMesh=os.path.realpath(pd), files=files, sha256=h.hexdigest())

RADIUS_SUFFIXES = (".csv", "_inscribed.csv", "_detail.csv")

def radius_check(case, pkg_dir, prefix):
    import m1_package as M
    cur = dict(case=os.path.abspath(case), mesh=mesh_hash(case), package_dir=pkg_dir, package_hashes=M.package_hashes(pkg_dir))
    json.dump(cur, open(f"{prefix}_provenance.pending.json", "w"), indent=1)
    f = f"{prefix}_provenance.json"
    if not os.path.exists(f): print(f"no radius provenance {os.path.basename(f)}: regenerate"); return False
    old = json.load(open(f)); why = []
    if old.get("mesh", {}).get("sha256") != cur["mesh"]["sha256"]: why.append("mesh sha256 differs")
    if old.get("package_hashes") != cur["package_hashes"]: why.append("package hashes differ")
    for sfx in RADIUS_SUFFIXES:
        g = prefix + sfx; rec = (old.get("outputs") or {}).get(os.path.basename(g))
        if not os.path.exists(g) or os.path.getsize(g) == 0: why.append(f"{os.path.basename(g)} missing/empty")
        elif rec != sha256(g): why.append(f"{os.path.basename(g)} changed since it was generated")
    if why: print("radius outputs NOT reusable: " + "; ".join(why)); return False
    print(f"radius outputs reusable: provenance verified (mesh sha256 {cur['mesh']['sha256'][:12]}, package hashes equal)"); return True

def radius_commit(prefix):
    p = f"{prefix}_provenance.pending.json"; r = json.load(open(p)); r["outputs"] = {os.path.basename(prefix + s): sha256(prefix + s) for s in RADIUS_SUFFIXES}
    json.dump(r, open(f"{prefix}_provenance.json", "w"), indent=1); os.remove(p); print(f"wrote {prefix}_provenance.json")

# ---------------- summary
def sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def reference_comparison(probes, hist):
    """$REF_FFR (e.g. Task A: 0.8697574904997768, the returned p011 value of M1_probes_baseline_resistance.csv) against the SAME quantity of this solve: p_over_Paorta of the package 'measurement' row of the probes
    csv (connected-section pullback of the reconstructed final fields, pf/m1_probes.py; Sol finding A7: like with like); |DeltaFFR| < $REF_TOL (default U3D = 0.00055). The measurementP last-100 mean is reported
    separately (B1), never used for the comparison. Not set: 'not requested'."""
    ref = os.environ.get("REF_FFR")
    if not ref: return "not requested (set REF_FFR)"
    ref = float(ref); tol = float(os.environ.get("REF_TOL", 0.00055)); rows = [r for r in csv.DictReader(open(probes)) if r["kind"] == "measurement"] if os.path.exists(probes) else []
    if len(rows) != 1 or not rows[0].get("p_over_Paorta"): return f"REF_FFR given but no valid package 'measurement' row in {probes}"
    v = float(rows[0]["p_over_Paorta"]); d = v - ref; h = json.load(open(hist)) if os.path.exists(hist) else {}
    mp = (h.get("measurementP") or {}).get("last100_mean_p_over_Paorta")
    return dict(reference=ref, value=v, probe_id=rows[0]["probe_id"], time=rows[0]["time"], DeltaFFR=d, tol=tol, within=bool(abs(d) < tol), measurementP_last100_mean_p_over_Paorta_B1=mp,
                statement=f"FFR({rows[0]['probe_id']}, reconstructed time {rows[0]['time']}) = {v:.7f}; DeltaFFR vs reference {ref} = {d:+.7f}: |DeltaFFR| {'<' if abs(d) < tol else '>='} {tol}"
                          + (f"; measurementP last-100 mean {mp:.7f} (B1, reported separately)" if mp is not None else ""))

def summary(case, out_dir, label, mode, out, files):
    info = json.load(open(f"{case}/build_info.json")); an = json.load(open(f"{case}/analysis_pf.json")) if os.path.exists(f"{case}/analysis_pf.json") else {}
    txt = open(f"{case}/log.simpleFoam", errors="replace").read(); m = re.findall(r"ExecutionTime = ([0-9.]+) s\s+ClockTime = (\d+) s", txt)
    ram, ram_src = peak_ram(case)
    s = dict(case_dir=os.path.abspath(case), label=label, mode=mode, package=info.get("package"), verdict=an.get("verdict"), verdict_analyze_solve=an.get("verdict_analyze_solve"),
             failed_checks=[k for k, v in (an.get("checks") or {}).items() if not v], last_iteration=an.get("last_iteration"), log_finished=log_finished(case),
             analysis_log_finished=(an.get("strict") or {}).get("log_finished"), run_completion=run_completion(case)[1],
             package_check=(json.load(open(f"{out_dir}/package_check_{label}_{mode}.json")) if os.path.exists(f"{out_dir}/package_check_{label}_{mode}.json") else "not run"),
             radius_outputs=os.environ.get("POST_RADIUS_DECISION", "not recorded"),
             wall_clock_s=(int(m[-1][1]) if m else None), execution_time_s=(float(m[-1][0]) if m else None), cells=cells(case), nproc=info.get("nproc"), peak_ram_gb=ram, peak_ram_source=ram_src,
             measurement_probe_package=info.get("measurement_probe"), measurement_probe_used=info.get("measurement_probe_used") or info.get("measurement_probe"),
             measurement_section_rule=(info.get("measurement_section_rule") or {}).get("status", "not evaluated (pre-strict-rule build)"), measurement_probe_relocated=info.get("measurement_probe_relocated"),
             processor_dirs_kept=sorted(os.path.basename(p) for p in glob.glob(f"{case}/processor*")),
             outputs={os.path.relpath(f, out_dir) if f.startswith(os.path.abspath(out_dir)) else f: dict(size_bytes=os.path.getsize(f), sha256=sha256(f)) for f in map(os.path.abspath, files) if os.path.exists(f)},
             missing_outputs=[f for f in files if not os.path.exists(f)])
    rr = [r for r in csv.DictReader(open(f"{out_dir}/M1_results.csv")) if r.get("case") == label and r.get("bc_mode") == ("prescribed-flow" if mode == "prescribed" else "resistance")] if os.path.exists(f"{out_dir}/M1_results.csv") else []
    s["flags"] = rr[-1].get("flags") if rr else "M1_results row not found"; s["outlets_lost_in_mesh"] = [o["patch"] for o in C.lost_outlets(info)]
    s["reference_comparison"] = reference_comparison(f"{out_dir}/M1_probes_{label}_{mode}.csv", f"{out_dir}/M1_monitor_history_{label}_{mode}.json")
    json.dump(s, open(out, "w"), indent=1, default=str)
    if isinstance(s["reference_comparison"], dict): print("reference comparison: " + s["reference_comparison"]["statement"])
    print(f"wrote {out}: flags {s['flags']}, verdict {s['verdict']}, wall clock {s['wall_clock_s']} s, cells {s['cells']}, peak RAM {ram or 'n/a'} GB, measurement probe used {s['measurement_probe_used']} ({s['measurement_section_rule']})"
          + (f", MISSING {s['missing_outputs']}" if s["missing_outputs"] else ""))

def main(a):
    if not a: raise SystemExit(__doc__)
    g = lambda f: a[a.index(f) + 1] if f in a else None
    cmd = a[0]
    if cmd == "finished":
        ok, d = run_completion(a[1])
        if g("--json"): json.dump(d, open(g("--json"), "w"), indent=1)
        print(("RUN COMPLETE: " if ok else "RUN NOT COMPLETE: ") + (f"last Time {d['last_time']} = endTime, End at line {d['last_end_line']}" if ok else "; ".join(d["fails"]))); sys.exit(0 if ok else 1)
    if cmd == "package-check": sys.exit(0 if package_check(a[1], a[2], g("--json"), g("--pkg-root")) else 1)
    if cmd == "radius-check": sys.exit(0 if radius_check(a[1], a[2], a[3]) else 1)
    if cmd == "radius-commit": return radius_commit(a[1])
    if cmd == "reconstruct-check": sys.exit(0 if reconstruct_check(a[1], a[2]) else 1)
    if cmd == "fill": return fill(a[1], a[2], a[3], g("--gates"), g("--mesh-gates"), g("--d34"))
    if cmd == "history": return history(a[1], a[2], g("--probes"), g("--json"))
    if cmd == "cells": print(cells(a[1])); return
    if cmd == "peak-ram": print(peak_ram(a[1])[0]); return
    if cmd == "summary": return summary(a[1], a[2], a[3], a[4], a[5], a[6:])
    raise SystemExit(__doc__)

if __name__ == "__main__":
    main(sys.argv[1:])
