#!/usr/bin/env python3
"""WO 2026-10-10 section 5: finalise one task folder returns/2026-10-10/<Task>/ (Task = TaskT, TaskG, TaskM, TaskT2, TaskN) after its solves were post-processed (post_case_generic.sh, one sub-folder per
solve <label>_<mode>[_G<n>] holding M1_results.csv, M1_probes_*, M1_outlets_*, settle_*, post_summary_*, ...; D15 solves also pimple_result_*).
usage: finalise_task.py <Task> [--returns-root R] [--ref-root R] [--date YYYY-MM-DD] [--cases-dir C] [--state-dir S]
  --returns-root  root holding 2026-10-10/<Task>/ (default: the Drive returns folder; tests: a fake tree in audit_tmp)
  --ref-root      root of the earlier returns used as references (default: the Drive returns folder; only READ)
  --cases-dir / --state-dir   wo1010/cases and wo1010/state (tests only)
FAIL CLOSED (Sol R2 finding 6): nothing is written (exit 1) unless
  * task_gate.py <Task> passes (same function): every expected solve of wo_common.EXPECTED (Task G: G2..Gn of the ledger state/taskG_ledger.json, whose final record must be exit 0, and the published
    taskG_iterations csv lists exactly those iterations) has an accepted steady return that B1-SETTLED, or a NOT_SETTLED steady run with exactly one usable COMPLETE D15 fallback result, and a
    provenance.json (provenance.py, written at job start);
  * every solve's provenance.json is consistent: case_name = the solve, build_info_sha256 = the case's build_info.json when the case dir still exists; all solves of the task share ONE OpenFOAM build and
    ONE template_sha256 (work order section 6); code hashes that differ between solves are listed in the NOTE;
  * every reference file named for a comparison exists (a solve without a defined reference is allowed only where the work order says none exists, e.g. prescribed-flow rows of P5 instances);
  and after writing, verify_manifest.sh passes on the folder (else exit 1, reported). PIMPLE results enter only through the gate: status COMPLETE and the steady solve NOT_SETTLED.
Writes into the task folder, in this order (never overwriting: a differing file of the same name gets _<date>, then _<date>_r2 ...; identical content is left as is):
  1. summary_<Task>.csv: one row per (solve, reference) pair: FFR at the measurement probe actually used (relocated or package probe) and at the package measurement probe, FFR at the throat probe
     (all from the M1_probes csv: reconstructed end-of-budget sections), Delta vs the reference baseline of the same instance and mode ON THE SAME PROBE ID, Delta/U3D, throat Re, cells, settle label
     (B1/D8: SETTLED from n / FIRST_SETTLED_ONLY / NOT_SETTLED), converged, gate/flag columns (geometry_step_ok, checkMesh_ok, D3/D4 verdicts and distances, flags, lost outlets), host, OpenFOAM version,
     template commit and template_sha256 FROM THE SOLVE-TIME provenance.json, and for D15 solves the PIMPLE_FALLBACK time averages (mean, band) with Delta_pimple = Delta_steady + (pimple mean - steady monitor), the like-with-like correction.
     References: Task T: the returned scan-14 M1 baseline of the same mode (2026-09-26, resistance and prescribed); D14 extra (label with 12p5): A1 (2026-10-03 TaskA baseline_D7_12p5) AND the production
     narrow solve of this return (14_T5n_resistance); Task T2 / Task M: the P5 baseline (2026-10-03 P5/<scan>, resistance only; prescribed rows say that no prescribed-flow baseline exists); Task N: the 306
     baseline solved in this work order (TaskN/306_base_resistance, resistance only); Task G: the k1 = 1 solve (2026-09-26 T1_missed_branch resistance) and the taskG_iterations table.
  2. code_provenance_<Task>.csv: one row per solve copied from its solve-time provenance.json (host, date, OpenFOAM version/build, template path + template_sha256 + commit, sha256 of every recorded
     code file, build_info/system/0 hashes of the case as built, built_in_job). Nothing is reconstructed at finalisation time.
  3. NOTE.md: one dated paragraph for the task appended (earlier paragraphs are never changed; an identical paragraph is not appended twice).
  4. INDEX.csv: one row per file of the task folder (format of returns/2026-10-03/INDEX.csv: file,task,scan,content,csv_data_rows,bytes,sha256_lf; '#' header line).
  5. MANIFEST.sha256 + MANIFEST.README with ../taskFinal/make_manifest.sh itself (LF-normalised hashes, no comment lines); a previous, different MANIFEST.sha256 is kept as MANIFEST_superseded_<date>[_rN].sha256.
No CFD, no 0D code: reads csv/json files only."""
import sys, os, re, csv, json, glob, hashlib, subprocess, datetime, io
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import wo_common as W
import task_gate
from wo_common import DRIVE_RETURNS, WO, TASKS, latest

U3D = 0.00055
class Refused(SystemExit): pass
def refuse(msg): raise Refused(f"FINALISE REFUSED: {msg}")
def issue(path, text, date=None): return W.issue_atomic(path, text, date)
def csv_text(rows, cols=None):
    cols = cols or list(dict.fromkeys(k for r in rows for k in r)); s = io.StringIO()
    w = csv.DictWriter(s, cols, extrasaction="ignore", lineterminator="\n"); w.writeheader(); [w.writerow(r) for r in rows]; return s.getvalue()
P5_SCANS = ("138", "69", "473", "139", "272")
CONTENT = [(r"^NOTE\.md$", "status and narrative of this return (read first)"), (r"^summary_Task", "task summary: FFR at measurement and throat probes vs the reference baseline, Re, cells, settle, gates (finalise_task.py)"),
           (r"^code_provenance_", "sha256 of the production template and code at finalisation (finalise_task.py)"), (r"^taskG_iterations", "Task G: k iterations, territory flows, J, max |Q/T-1|"),
           (r"^M1_results_pimple_", "D15: M1_results row of a PIMPLE_FALLBACK solve (time averages)"), (r"^M1_results\.csv$", "M1_results-format row(s): geometry, mesh, solve, gates, flags"),
           (r"^M1_probes_", "probe sections: p/P_aorta, area, r_eq, flow, Re per package probe"), (r"^M1_outlets_", "per outlet: R used, Q, p (lost outlets flagged)"),
           (r"^M1_monitor_history_.*\.csv$", "every-iteration probe monitor history (measurementP, throatP, ...)"), (r"^M1_monitor_history_.*\.json$", "provenance of the monitor history"),
           (r"^as_meshed_radius_.*_detail\.csv$", "as-meshed radius, per-section detail"), (r"^as_meshed_radius_.*_inscribed\.csv$", "as-meshed lumen radius, inscribed circle (D10)"),
           (r"^as_meshed_radius_.*_provenance\.json$", "provenance of the as-meshed radius files"), (r"^as_meshed_radius_.*\.csv$", "as-meshed lumen radius, area-equivalent (D10)"),
           (r"^fill_", "inputs used to fill the M1_results row"), (r"^flow_state_.*\.csv$", "flow-state profile (jet centroid offset along the lesion vessel)"), (r"^flow_state_.*\.json$", "flow-state summary / comparison verdict"),
           (r"^package_check_", "package hashes and E0 membership check"), (r"^post_summary_", "post-processing summary with sha256 of every output"), (r"^post_.*\.log$", "post-processing log"),
           (r"^reconstruct_check_", "reconstructPar verification"), (r"^run_completion_", "solver completion record"), (r"^settle_", "B1 SETTLED rule on measurementP (information; full budget run per D8)"),
           (r"^pimple_result_", "D15 PIMPLE_FALLBACK: time averages (second half of the window) and min/max band of FFR, flows, Re"), (r"^pimple_outlets_", "D15 PIMPLE_FALLBACK: per outlet time-averaged flow and pressure"),
           (r"^pimple_history_", "D15 PIMPLE_FALLBACK: every time step of the transient monitors"), (r"^pimple_summary_", "D15 PIMPLE_FALLBACK: summary json with window and sha256"),
           (r"^MANIFEST_superseded_", "previous MANIFEST.sha256 of this folder (superseded)"), (r"^provenance.*\.json$", "solve-time provenance: host, OpenFOAM build, code + template sha256, as-built case hashes (provenance.py)")]
VARIANTS = ("baseline", "T1_missed_branch", "T5_vox_narrow", "T5_vox_wide", "clean_nolesion")

def sha256_lf(path):
    b = open(path, "rb").read()
    return hashlib.sha256(b if b"\0" in b else b.replace(b"\r", b"")).hexdigest()

def rows(path): return list(csv.DictReader(open(path))) if path and os.path.exists(path) else []

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def na(x): return "n/a" if x in (None, "") else x

def fmt(x, n=5, sign=False):
    return "n/a" if x is None else (f"{x:+.{n}f}" if sign else f"{x:.{n}f}")

# ------------------------------------------------------------------ probes
def probe_rows(path):
    r = rows(path); by_id = {x["probe_id"]: x for x in r}
    used = next((x for x in r if x["kind"] == "measurement_relocated"), None) or next((x for x in r if x["kind"] == "measurement"), None)
    pkg = next((x for x in r if x["kind"] == "measurement"), None); thr = next((x for x in r if x["kind"] == "throat"), None)
    return dict(by_id=by_id, used=used, pkg=pkg, throat=thr)

def ffr(row): return num(row.get("p_over_Paorta")) if row else None

# ------------------------------------------------------------------ solves
def solve_records(task_dir, states):
    """one record per EXPECTED solve (states = task_gate solve states, all ok); the solve's own M1_results row (tag match), its provenance and, for a D15 solve, its fallback json"""
    out = []
    for st in states:
        d, tag = st["out"], st["tag"]
        mr = [r for r in rows(f"{d}/M1_results.csv") if f"{r['case']}_{'prescribed' if r['bc_mode'].startswith('prescribed') else 'resistance'}" == tag]
        if len(mr) != 1: refuse(f"{d}/M1_results.csv: {len(mr)} rows for {tag} (need exactly one)")
        r = mr[0]; label = r["case"]; mode = "prescribed" if r["bc_mode"].startswith("prescribed") else "resistance"
        ps = latest(d, f"post_summary_{tag}*.json"); ps = json.load(open(ps)) if ps else {}
        pc = latest(d, f"package_check_{tag}*.json"); pc = json.load(open(pc)) if pc else {}
        pkg = ps.get("package") or os.path.basename(str(pc.get("package_dir") or "")) or ""
        m = re.match(r"^(\d+)_.*__(" + "|".join(VARIANTS) + r")__", os.path.basename(str(pkg)))
        scan = m.group(1) if m else (re.match(r"^(\d+)", label).group(1) if re.match(r"^(\d+)", label) else "")
        pp, prov = W.provenance_of(d)
        if not prov: refuse(f"{d}: provenance.json missing/unreadable")
        out.append(dict(dir=d, solve=st["solve"], label=label, mode=mode, tag=tag, row=r, post_summary=ps, package=os.path.basename(str(pkg)), scan=scan,
                        variant=(m.group(2) if m else ""), probes=f"{d}/M1_probes_{tag}.csv", outlets=f"{d}/M1_outlets_{tag}.csv", settle=latest(d, f"settle_{tag}*.csv"),
                        settle_decision=st["settle"], source=st["source"], pimple=st["fallback"], provenance=prov, provenance_file=pp, case=st["case"]))
    return out

def references(task, s, task_dir, ref_root, solves):
    """[(ref_name, probes_csv, outlets_csv, note)]; probes_csv None = no reference (note says why)"""
    r26, r03 = f"{ref_root}/2026-09-26", f"{ref_root}/2026-10-03"; mode, scan, label = s["mode"], s["scan"], s["label"]
    if task == "TaskG" or re.search(r"_G\d+$", label):
        return [("k1 = 1: scan-14 T1_missed_branch resistance solve returned 2026-09-26 (not re-solved)", f"{r26}/M1_probes_T1_missed_branch_resistance.csv", f"{r26}/M1_outlets_T1_missed_branch_resistance.csv", "")]
    if scan == "14":
        if "12p5" in label:
            nar = next((x for x in solves if x["label"] == "14_T5n" and x["mode"] == "resistance"), None)
            return [("A1: scan-14 baseline, 12.5 um throat zone (2026-10-03 TaskA baseline_D7_12p5, resistance)", f"{r03}/TaskA/M1_probes_baseline_D7_12p5_resistance.csv", f"{r03}/TaskA/M1_outlets_baseline_D7_12p5_resistance.csv", "D14 pair (both 12.5 um)"),
                    ("production narrow solve 14_T5n resistance (25 um throat zone, this return)", nar["probes"] if nar else None, nar["outlets"] if nar else None,
                     "" if nar else "the production narrow resistance solve 14_T5n_resistance is not (yet) in this task folder")]
        return [(f"scan-14 M1 baseline, {mode} (returned 2026-09-26)", f"{r26}/M1_probes_baseline_{mode}.csv", f"{r26}/M1_outlets_baseline_{mode}.csv", "")]
    if scan in P5_SCANS:
        if mode == "prescribed": return [("none", None, None, f"no prescribed-flow baseline exists for scan {scan} (P5 returned the baseline in resistance mode only): absolute values only")]
        return [(f"P5 baseline scan {scan}, resistance (2026-10-03 P5/{scan})", f"{r03}/P5/{scan}/M1_probes_{scan}_resistance.csv", f"{r03}/P5/{scan}/M1_outlets_{scan}_resistance.csv", "")]
    if scan == "306":
        if s["variant"] == "baseline" or label.endswith("_base"): return [("none", None, None, "this IS the scan-306 baseline (resistance), the reference of the Task N solves")]
        if mode == "prescribed": return [("none", None, None, "no prescribed-flow baseline exists for scan 306 (the work order solves the 306 baseline in resistance mode only): absolute values only")]
        b = next((x for x in solves if x["scan"] == "306" and x["mode"] == "resistance" and (x["variant"] == "baseline" or x["label"].endswith("_base"))), None)
        if b is None:     # Task N folder of the same return when finalising another task
            for d in glob.glob(f"{os.path.dirname(task_dir)}/TaskN/306_base*_resistance"):
                b = dict(probes=glob.glob(f"{d}/M1_probes_*_resistance.csv")[0], outlets=glob.glob(f"{d}/M1_outlets_*_resistance.csv")[0])
        return [("scan-306 baseline, resistance (solved in this work order, TaskN/306_base_resistance)", b["probes"] if b else None, b["outlets"] if b else None, "" if b else "the 306 baseline solve is not (yet) returned")]
    return [("none", None, None, f"no reference defined for scan {scan}")]

def settle_label(path):
    r = rows(path)
    if not r: return "settle csv missing", None, None
    r = r[0]; f, p_ = r.get("iter_first_settled"), r.get("iter_permanently_settled")
    lab = r.get("b1_label") or ""
    if p_: return f"{lab}: SETTLED from {p_} (first {f}) of {r.get('iterations_run')}", f, p_
    if f: return f"{lab}: FIRST_SETTLED_ONLY at {f}, NOT settled at the end of {r.get('iterations_run')}", f, None
    return f"{lab}: NOT_SETTLED within {r.get('iterations_run')}", None, None

def outlet_delta(new_csv, ref_csv):
    a = {x["outlet_id"]: num(x["Q_mls"]) for x in rows(new_csv)}; b = {x["outlet_id"]: num(x["Q_mls"]) for x in rows(ref_csv)}
    c = [abs(a[k] / b[k] - 1) * 100 for k in a if k in b and a[k] is not None and b[k]]
    return (max(c) if c else None), sorted(set(a) ^ set(b))

# ------------------------------------------------------------------ solve-time provenance (provenance.py), never reconstructed here
def check_provenance(solves):
    """-> (rows of code_provenance_<Task>.csv, NOTE text on the code); refuses on an inconsistent provenance or a mixed OpenFOAM build / template within the task"""
    pr = []
    for s in solves:
        p = s["provenance"]
        if p.get("case_name") != s["solve"]: refuse(f"{s['provenance_file']}: case_name {p.get('case_name')!r} != solve {s['solve']!r}")
        for k in ("host", "template_sha256", "build_info_sha256"):
            if not p.get(k): refuse(f"{s['provenance_file']}: {k} empty")
        if not (p.get("openfoam") or {}).get("build"): refuse(f"{s['provenance_file']}: OpenFOAM build empty")
        bi = f"{s['case']}/build_info.json"
        if os.path.isfile(bi) and W.sha256(bi) != p["build_info_sha256"]: refuse(f"{bi} is not the build_info.json recorded at solve start in {s['provenance_file']} (case rebuilt after the solve?)")
        row = dict(solve=s["solve"], host=p["host"], date=p.get("date"), job=p.get("job"), built_in_job=p.get("built_in_job"), openfoam_version=p["openfoam"].get("WM_PROJECT_VERSION"),
                   openfoam_build=p["openfoam"]["build"], openfoam_dir=p["openfoam"].get("WM_PROJECT_DIR"), template=p.get("template"), template_sha256=p["template_sha256"],
                   template_commit=p.get("template_commit"), build_info_sha256=p["build_info_sha256"], case_system_sha256=p.get("case_system_sha256"), case_0_sha256=p.get("case_0_sha256"),
                   case_built_at=p.get("case_built_at"), r_scale_k=p.get("r_scale_k"), provenance_file=os.path.relpath(s["provenance_file"], os.path.dirname(s["dir"])))
        row.update({f"sha256:{os.path.relpath(f, P)}": h for f, h in sorted((p.get("code") or {}).items())})
        pr.append(row)
    for k in ("openfoam_build", "template_sha256"):
        v = sorted({r[k] for r in pr})
        if len(v) > 1: refuse(f"the solves of this task do not share one {k} (work order section 6): {v}")
    code_cols = sorted({c for r in pr for c in r if c.startswith("sha256:")})
    differ = [c[7:] for c in code_cols if len({r.get(c) for r in pr}) > 1]
    note = (f"Provenance (solve-time, `provenance.json` of every solve, provenance.py): host(s) {', '.join(sorted({r['host'] for r in pr}))}; OpenFOAM {pr[0]['openfoam_version']} build {pr[0]['openfoam_build']}; "
            f"template {pr[0]['template']} content sha256 {pr[0]['template_sha256']} (commit: {pr[0]['template_commit']}); "
            + ("the same code sha256 for every solve." if not differ else f"code files whose sha256 differs between solves: {', '.join(differ)} (see the code_provenance table)."))
    return pr, note

# ------------------------------------------------------------------ main
def finalise(task, returns_root, ref_root, date, cases=W.CASES, state=W.STATE):
    if task not in TASKS: refuse(f"task must be one of {TASKS}")
    td = os.path.join(returns_root, WO, task)
    if not os.path.isdir(td): refuse(f"{td}: no such task folder")
    ok, rep = task_gate.gate(task, returns_root, cases, state)
    if not ok:
        refuse(f"task_gate {task}: {rep.get('verdict')} " + (rep.get("reason") or "; ".join([f"{x['solve']}: {' | '.join(x['reasons'])}" for x in rep["solves"] if not x["ok"]] + rep.get("problems", []))))
    solves = solve_records(td, rep["solves"])
    prov, prov_note = check_provenance(solves)
    extra = sorted(os.path.basename(d.rstrip("/")) for d in glob.glob(f"{td}/*/") if os.path.basename(d.rstrip("/")) not in {s["solve"] for s in solves} and not os.path.basename(d.rstrip("/")).startswith("_")
                   and not any(s["pimple"] and os.path.dirname(s["pimple"]) == d.rstrip("/") for s in solves))
    out, bullets, notes = [], [], set()
    for s in solves:
        pr = probe_rows(s["probes"]); r = s["row"]; pv = s["provenance"]; host, build = pv["host"], pv["openfoam"]["build"]
        sl, s_first, s_perm = settle_label(s["settle"])
        pim = json.load(open(s["pimple"])) if s["source"] == "pimple" else None
        base = dict(task=task, solve=s["solve"], label=s["label"], scan=s["scan"], variant=s["variant"] or ("D14 12.5 um" if "12p5" in s["label"] else ""), mode=s["mode"], package=s["package"],
                    measurement_probe_used=(pr["used"] or {}).get("probe_id"), FFR_measurement_used=ffr(pr["used"]), measurement_probe_package=(pr["pkg"] or {}).get("probe_id"), FFR_measurement_package_probe=ffr(pr["pkg"]),
                    throat_probe=(pr["throat"] or {}).get("probe_id"), FFR_throat=ffr(pr["throat"]), Re_throat=num(r.get("Re_throat")), n_cells=r.get("n_cells"),
                    settle=sl, iter_first_settled=s_first, iter_permanently_settled=s_perm, converged=r.get("converged"), flags=r.get("flags"),
                    geometry_step_ok=r.get("geometry_step_ok"), checkMesh_ok=r.get("checkMesh_ok"), throat_pct_error=r.get("throat_pct_error"), D3_verdict=r.get("D3_verdict"), D4_verdict=r.get("D4_verdict"),
                    D34_min_dist_throat_mm=r.get("D34_min_dist_throat_mm"), D34_min_dist_measurement_mm=r.get("D34_min_dist_measurement_mm"), outlets_lost_in_mesh=r.get("outlets_lost_in_mesh"),
                    host=host, openfoam_version=pv["openfoam"].get("WM_PROJECT_VERSION"), openfoam_build=build, template_commit=pv.get("template_commit"), template_sha256=pv["template_sha256"],
                    settle_decision=s["settle_decision"], result_source=("D15 pimple fallback " + os.path.relpath(s["pimple"], td) if pim else "steady (B1 settled)"))
        if pim:
            base.update(pimple_flag="PIMPLE_FALLBACK", pimple_status=pim.get("status"), pimple_FFR_measurement_mean=num(pim.get("FFR_measurement_mean")), pimple_FFR_measurement_min=num(pim.get("FFR_measurement_min")),
                        pimple_FFR_measurement_max=num(pim.get("FFR_measurement_max")), pimple_FFR_throat_mean=num(pim.get("FFR_throat_mean")), pimple_FFR_throat_min=num(pim.get("FFR_throat_min")),
                        pimple_FFR_throat_max=num(pim.get("FFR_throat_max")), pimple_minus_steady_monitor_measurement=num(pim.get("FFR_measurement_mean_minus_steady")),
                        pimple_minus_steady_monitor_throat=num(pim.get("FFR_throat_mean_minus_steady")), pimple_Re_throat_mean=num(pim.get("Re_throat_mean")), pimple_window=json.dumps(pim.get("window"), sort_keys=True, default=str) if pim.get("window") is not None else "n/a",
                        pimple_FFR_at_measurement_probe_used=num((pim.get("FFR") or {}).get(base["measurement_probe_used"])), pimple_FFR_at_throat_probe=num((pim.get("FFR") or {}).get(base["throat_probe"])),
                        pimple_flags=pim.get("flags"))
            base["flags"] = ";".join(x for x in ["PIMPLE_FALLBACK"] + str(base["flags"] or "").split(";") if x and x != "NONE")
        for name, rp, ro, note in references(task, s, td, ref_root, solves):
            row = dict(base, reference=name, reference_probes=rp or "", reference_note=note)
            if rp is None and name != "none": refuse(f"{s['solve']}: reference '{name}' has no file ({note})")
            if rp and not (os.path.exists(rp) and ro and os.path.exists(ro)): refuse(f"{s['solve']}: reference file(s) missing: {rp} / {ro}")
            if rp and os.path.exists(rp):
                rf = probe_rows(rp); uid = base["measurement_probe_used"]
                ref_used = rf["by_id"].get(uid) or rf["used"]
                if ref_used is not rf["by_id"].get(uid): row["reference_note"] = (note + "; " if note else "") + f"probe ids differ: new {uid}, reference {(rf['used'] or {}).get('probe_id')} (compared as the measurement probe of each)"
                d_used = (base["FFR_measurement_used"] - ffr(ref_used)) if base["FFR_measurement_used"] is not None and ffr(ref_used) is not None else None
                ref_pkg = rf["by_id"].get(base["measurement_probe_package"]) if base["measurement_probe_package"] else None
                d_pkg = (base["FFR_measurement_package_probe"] - ffr(ref_pkg)) if ref_pkg and base["FFR_measurement_package_probe"] is not None else None
                ref_thr = rf["by_id"].get(base["throat_probe"]) or rf["throat"]
                d_thr = (base["FFR_throat"] - ffr(ref_thr)) if ref_thr and base["FFR_throat"] is not None else None
                dq, odiff = outlet_delta(s["outlets"], ro)
                row.update(reference_measurement_probe=(ref_used or {}).get("probe_id"), reference_FFR_measurement=ffr(ref_used), Delta_FFR_measurement=d_used, Delta_over_U3D=(d_used / U3D if d_used is not None else None),
                           reference_FFR_measurement_package_probe=ffr(ref_pkg), Delta_FFR_measurement_package_probe=d_pkg, reference_throat_probe=(ref_thr or {}).get("probe_id"), reference_FFR_throat=ffr(ref_thr),
                           Delta_FFR_throat=d_thr, max_abs_outlet_Q_change_pct=dq, outlets_not_in_both=";".join(odiff))
                if pim and d_used is not None and base.get("pimple_minus_steady_monitor_measurement") is not None:
                    row["Delta_FFR_measurement_pimple"] = d_used + base["pimple_minus_steady_monitor_measurement"]
            elif rp: row["reference_note"] = (note + "; " if note else "") + f"reference file missing: {rp}"
            out.append(row)
        notes.update(n for n in [out[-1]["reference_note"]] if n and n.startswith("no prescribed"))
    # 1. summary csv
    cols = list(dict.fromkeys(k for r in out for k in r))
    p_sum = issue(f"{td}/summary_{task}.csv", csv_text(out, cols), date)
    p_prov = issue(f"{td}/code_provenance_{task}.csv", csv_text(prov), date)
    # 2. NOTE paragraph
    hosts = sorted({r["host"] for r in out}); vers = sorted({str(r["openfoam_version"]) + (f" (build {r['openfoam_build']})" if r["openfoam_build"] else "") for r in out})
    L = [f"## {task}: finalised {date} (finalise_task.py; facts filled from the returned files)", "",
         f"Expected solves: {len(solves)}, all present and complete (task_gate.py {task} PASS: B1 settled, or D15 COMPLETE fallback for "
         + (", ".join(s["solve"] for s in solves if s["source"] == "pimple") or "none") + f"): {', '.join(s['solve'] for s in solves)}."
         + (f" Other sub-folders (not part of this task's result): {', '.join(extra)}." if extra else ""),
         f"Host(s): {', '.join(hosts)}. OpenFOAM: {', '.join(vers)}. {prov_note} Table: `{os.path.basename(p_prov)}`.",
         f"FFR = p/P_aorta of the reconstructed end-of-budget section at the probe (M1_probes); Delta = solve - reference on the SAME probe id; U3D = {U3D} (final, 2026-10-03 Task B). Table: `{os.path.basename(p_sum)}`.", ""]
    for r in out:
        ref = r["reference"]
        if r.get("reference_FFR_measurement") is not None:
            cmp_m = f"vs {ref}: {fmt(r['reference_FFR_measurement'])}, Delta {fmt(r['Delta_FFR_measurement'], sign=True)} ({fmt(r['Delta_over_U3D'], 1, True)} x U3D)"
            cmp_t = f"(ref {fmt(r['reference_FFR_throat'])}, Delta {fmt(r['Delta_FFR_throat'], sign=True)})"
            cmp_q = f"; outlet flows change by at most {fmt(r['max_abs_outlet_Q_change_pct'], 2)} %" if r.get("max_abs_outlet_Q_change_pct") is not None else ""
        else: cmp_m, cmp_t, cmp_q = f"reference: {r['reference_note'] or ref}", "", ""
        reloc = f" (relocated; package probe {r['measurement_probe_package']}: {fmt(r['FFR_measurement_package_probe'])})" if r["measurement_probe_used"] != r["measurement_probe_package"] else ""
        b = (f"- `{r['solve']}` ({r['variant'] or 'n/a'}, {r['mode']}): FFR at measurement probe {r['measurement_probe_used']}{reloc} = {fmt(r['FFR_measurement_used'])}, {cmp_m}; throat probe {r['throat_probe']} = "
             f"{fmt(r['FFR_throat'])} {cmp_t}{cmp_q}. Re_throat {fmt(r['Re_throat'], 1)}, cells {r['n_cells']}, settle {r['settle']}, {na(r['converged'])}; flags {na(r['flags'])}; geometry_step_ok {na(r['geometry_step_ok'])}, "
             f"D3 {na(r['D3_verdict'])} / D4 {na(r['D4_verdict'])} (nearest flagged entity {fmt(num(r['D34_min_dist_throat_mm']), 3)} mm from the throat, {fmt(num(r['D34_min_dist_measurement_mm']), 3)} mm from the measurement probe); host {r['host']}.")
        if r.get("pimple_flag"):
            b += (f" **PIMPLE_FALLBACK** ({r['pimple_status']}): time mean over {r['pimple_window']}: measurement {fmt(r['pimple_FFR_measurement_mean'])} [{fmt(r['pimple_FFR_measurement_min'])}, {fmt(r['pimple_FFR_measurement_max'])}], "
                  f"throat {fmt(r['pimple_FFR_throat_mean'])} [{fmt(r['pimple_FFR_throat_min'])}, {fmt(r['pimple_FFR_throat_max'])}]" + (f", Delta_pimple {fmt(r.get('Delta_FFR_measurement_pimple'), sign=True)}" if r.get("Delta_FFR_measurement_pimple") is not None else "") + ".")
        if r["reference_note"] and r.get("reference_FFR_measurement") is not None: b += f" Note: {r['reference_note']}."
        L.append(b)
    if task in ("TaskT2", "TaskM"): L += ["", "Baselines of scans 138, 69, 473 and 139 are the P5 solves (2026-10-03), resistance mode only: NO prescribed-flow baseline exists for these instances, so the prescribed-flow solves are reported as absolute values without a Delta."]
    if task == "TaskN": L += ["", "Reference: the scan-306 baseline solved in this work order (resistance mode only); no prescribed-flow baseline exists for scan 306."]
    if task == "TaskT": L += ["", "Reference: the returned scan-14 M1 baseline of the same mode (2026-09-26, resistance and prescribed-flow). D14 extra (12.5 um): compared with A1 (2026-10-03 TaskA, also 12.5 um) and with the production narrow solve (25 um)."]
    if task == "TaskG":
        it = latest(td, "taskG_iterations*.csv")
        if it:
            ir = rows(it); qc = [c for c in ir[0] if c.startswith("Q_terr")]; tc = [c for c in ir[0] if c.startswith("T_terr")]
            L += ["", f"Task G iterations (`{os.path.basename(it)}`; targets T_j = CLEAN full territory flows, Decision B1; J = sum_j (Q_j/T_j - 1)^2):", "",
                  "| n | k | settle / source | J | max abs(Q/T-1) | " + " | ".join(qc) + " | " + " | ".join(tc) + " | k_next | dlogk | stop |", "|" + "---|" * (8 + len(qc) + len(tc))]
            for x in ir:
                L.append(f"| {x['n']} | {fmt(num(x['k']), 6)} | {x.get('settle') or ''}{' (D15 fallback)' if str(x.get('source', '')).startswith('D15') else ''} | {fmt(num(x['J']), 6)} | {fmt(num(x['max_abs_Q_over_T_minus_1']), 4)} | " + " | ".join(fmt(num(x[c]), 5) for c in qc) + " | " + " | ".join(fmt(num(x[c]), 5) for c in tc)
                         + f" | {fmt(num(x.get('k_next')), 6)} | {fmt(num(x.get('dlogk')), 4)} | {x.get('stop') or ''} |")
        else: refuse(f"Task G: taskG_iterations csv not found in {td}")
    para = "\n".join(L) + "\n"
    nf = f"{td}/NOTE.md"; old = open(nf).read() if os.path.exists(nf) else ""
    if para not in old:          # append only: earlier paragraphs are never changed
        head = (("\n" if not old.endswith("\n\n") else "") if old else f"# NOTE, CFD machine returns {WO}/{task} (answers WORK-ORDER-{WO})\n\n")
        with open(nf, "a", newline="") as fh: fh.write(head + para)
    # 3. INDEX
    p_idx = write_index(td, task, date)
    # 4. MANIFEST, then its verification (fail closed: a manifest that does not verify is reported, exit 1)
    write_manifest(td, date)
    v = subprocess.run(["bash", f"{P}/taskFinal/verify_manifest.sh", td], capture_output=True, text=True)
    if v.returncode != 0: refuse(f"verify_manifest.sh {td} FAILED after writing (rc {v.returncode}): " + " | ".join(ln for ln in v.stdout.splitlines() if not ln.endswith(": OK"))[-1500:])
    print(f"{task}: FINALISED: {len(solves)} solve(s) ({sum(s['source'] == 'pimple' for s in solves)} D15), {len(out)} summary row(s) -> {os.path.basename(p_sum)}; {os.path.basename(p_prov)}; NOTE.md; "
          f"{os.path.basename(p_idx)}; MANIFEST.sha256 verified ({v.stdout.strip().splitlines()[-1]})")
    return out

def write_index(td, task, date):
    fs = []
    for root, dirs, files in os.walk(td):
        dirs.sort()
        for f in sorted(files):
            rel = os.path.relpath(os.path.join(root, f), td)
            if re.match(r"^(INDEX(_\d{4}-\d\d-\d\d(_r\d+)?)?\.csv|MANIFEST\.(sha256|README))$", rel): continue
            fs.append(rel)
    ir = []
    for rel in sorted(fs):
        p = os.path.join(td, rel); b = os.path.basename(rel); top = rel.split(os.sep)[0]
        m = re.match(r"^(\d+)_", top); scan = m.group(1) if m and os.sep in rel else ""
        if not scan and task == "TaskG": scan = "14"
        content = next((c for pat, c in CONTENT if re.search(pat, b)), "")
        n = None
        if b.endswith(".csv"):
            with open(p, newline="") as fh: n = max(0, sum(1 for ln in fh if ln.strip() and not ln.startswith("#")) - 1)
        ir.append(dict(file=rel.replace(os.sep, "/"), task=task, scan=scan, content=content, csv_data_rows="" if n is None else n, bytes=os.path.getsize(p), sha256_lf=sha256_lf(p)))
    txt = f"# INDEX of returns/{WO}/{task}; sha256_lf = sha256 of the file with CRLF normalised to LF (text files) or of the raw bytes\n" + csv_text(ir, ["file", "task", "scan", "content", "csv_data_rows", "bytes", "sha256_lf"])
    return issue(f"{td}/INDEX.csv", txt, date)

def write_manifest(td, date):
    mk = f"{P}/taskFinal/make_manifest.sh"; m, rd = f"{td}/MANIFEST.sha256", f"{td}/MANIFEST.README"
    old = open(m, "rb").read() if os.path.exists(m) else None; old_rd = open(rd, "rb").read() if os.path.exists(rd) else None
    mm = lambda: subprocess.run(["bash", mk, td], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
    r = mm()
    if r.returncode != 0: refuse(f"make_manifest.sh {td} failed (rc {r.returncode}): {r.stderr.strip()[-500:]}")
    if old is None or open(m, "rb").read() == old:
        if old_rd is not None and old is not None: open(rd, "wb").write(old_rd)          # unchanged content: keep the original README (its timestamp)
        return m
    for k in [""] + [f"_r{i}" for i in range(2, 100)]:                                   # different: keep the previous manifest, then regenerate (the kept copy is itself listed)
        sup = f"{td}/MANIFEST_superseded_{date}{k}.sha256"
        if not os.path.exists(sup): open(sup, "wb").write(old); break
    r = mm()
    if r.returncode != 0: refuse(f"make_manifest.sh {td} failed (rc {r.returncode}): {r.stderr.strip()[-500:]}")
    return m

def main(a):
    if not a or a[0] in ("-h", "--help"): raise SystemExit(__doc__)
    def opt(f, d=None):
        if f in a: i = a.index(f); v = a[i + 1]; del a[i:i + 2]; return v
        return d
    rr, ref, date = opt("--returns-root", DRIVE_RETURNS), opt("--ref-root", DRIVE_RETURNS), opt("--date", datetime.date.today().isoformat())
    cs, sd = opt("--cases-dir", W.CASES), opt("--state-dir", W.STATE)
    if len(a) != 1: raise SystemExit(__doc__)
    try: finalise(a[0], rr, ref, date, cs, sd)
    except Refused as e: print(e, file=sys.stderr); sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])
