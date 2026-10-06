"""INDEX.csv of cfd_handover/returns/2026-10-03 (every file except INDEX.csv/desktop.ini): path, task, content, data rows (CSV), bytes, sha256 over LF-normalised
content for text files (CRLF -> LF, as the analysis side's check requires), raw bytes otherwise. usage: make_index_1003.py [returns_dir]"""
import csv, hashlib, os, re, sys
R = sys.argv[1] if len(sys.argv) > 1 else "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-03"
DESC = [(r"^NOTE\.md$", "status and narrative of this return (read first)"),
        (r"M1_D7_sensitivity\.csv$", "Task A: D7 sensitivity verdict per variant (A1, A2, A0), first issue"),
        (r"M1_D7_sensitivity_.*\.csv$", "Task A: D7 sensitivity, re-issue (A0 labelled control; overall M1 verdict column)"),
        (r"M1_geometry_gates_D7.*\.csv$", "Task A: geometry/mesh gates and D3/D4 distances of A1, A2, A0 (M1_geometry_gates.csv format)"),
        (r"M1_results\.csv$", "M1_results-format row(s): geometry, mesh, solve, gates, flags"),
        (r"M1_probes_", "probe sections: p/P_aorta, area, r_eq, flow, Re per package probe"),
        (r"M1_outlets_", "per outlet: R used, Q, p (lost outlets flagged)"),
        (r"M1_monitor_history_.*\.csv$", "every-iteration probe monitor history (measurementP, throatP, ...)"),
        (r"M1_monitor_history_.*\.json$", "provenance of the monitor history"),
        (r"as_meshed_radius_.*_inscribed\.csv$", "as-meshed lumen radius, inscribed circle (D10)"),
        (r"as_meshed_radius_.*_detail\.csv$", "as-meshed radius, per-section detail"),
        (r"as_meshed_radius_.*_provenance\.json$", "provenance of the as-meshed radius files"),
        (r"as_meshed_radius_.*\.csv$", "as-meshed lumen radius, area-equivalent (D10)"),
        (r"settle_.*_2026-10-06\.csv$", "B1 SETTLED rule on measurementP, re-issue with the contended column filled"),
        (r"settle_.*\.csv$", "B1 SETTLED rule on measurementP (information; full budget run per D8)"),
        (r"flow_state_.*\.csv$", "flow-state profile (jet centroid offset along the lesion vessel)"),
        (r"flow_state_.*\.json$", "flow-state summary / comparison verdict"),
        (r"fill_.*\.json$", "inputs used to fill the M1_results row"),
        (r"package_check_.*\.json$", "package hashes and E0 membership check"),
        (r"post_summary_.*_2026-10-06\.json$", "post-processing summary, re-issue (M1_results.csv entry updated to the current aggregate)"),
        (r"post_summary_.*\.json$", "post-processing summary with sha256 of every output"),
        (r"post_.*\.log$", "post-processing log"),
        (r"reconstruct_check_.*\.json$", "reconstructPar verification"),
        (r"run_completion_.*\.json$", "solver completion record"),
        (r"result_S.*\.json$", "Task B: jet-state re-run result and rule verdict per U3D level"),
        (r"jet_offset_S.*\.txt$", "Task B: jet centroid offset along x per U3D level"),
        (r"verdict_S.*\.txt$", "Task B: one-line verdict per U3D level"),
        (r"U3D_jet_state_check_.*\.csv$", "Task B: all five U3D levels, FFR reproduction, jet state, GCI21 -> U3D final"),
        (r"ROOT_CAUSE_272_.*\.md$", "P5 272: root cause of the lost outlet out_396 and of the self-intersection flag"),
        (r"neck272\.json$", "P5 272: neck measurements (mask EDT, MC/smoothed/final section radii)"),
        (r"selfint272_.*\.json$", "P5 272: edge-triangle crossing test around the surfaceCheck point"),
        (r"tritri272_.*\.json$", "P5 272: triangle-triangle distance / crossing / fold check around a surfaceCheck point"),
        (r"log\.surfaceCheck\.", "P5 272: surfaceCheck log on a sub-surface around the reported point (or the full surface)"),
        (r"selfInterPoints\..*\.points\.txt$", "P5 272: points surfaceCheck reported as self-intersections (OBJ vertex lines, renamed .txt)")]
def task(rel):
    top = rel.split("/")[0]
    return {"TaskA": "A", "TaskB": "B", "P5": "P5"}.get(top, "A" if rel.startswith("M1_D7") else "all")
rows = []
for d, _, fs in os.walk(R):
    for f in sorted(fs):
        if f in ("INDEX.csv", "desktop.ini"): continue
        p = os.path.join(d, f); rel = os.path.relpath(p, R).replace(os.sep, "/"); b = open(p, "rb").read()
        text = f.endswith((".csv", ".json", ".md", ".txt", ".log"))
        h = hashlib.sha256(b.replace(b"\r\n", b"\n") if text else b).hexdigest()
        n = sum(1 for _ in csv.reader(b.decode("utf-8", "replace").splitlines()) if _ and not _[0].startswith("#")) - 1 if f.endswith(".csv") else ""
        desc = next((t for pat, t in DESC if re.search(pat, f)), "")
        case = rel.split("/")[1] if rel.startswith("P5/") else ""
        rows.append(dict(file=rel, task=task(rel), scan=case, content=desc, csv_data_rows=n, bytes=len(b), sha256_lf=h))
rows.sort(key=lambda r: r["file"])
with open(os.path.join(R, "INDEX.csv"), "w", newline="\n") as fh:
    fh.write("# INDEX of returns/2026-10-03; sha256_lf = sha256 of the file with CRLF normalised to LF (text files) or of the raw bytes\n")
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(len(rows), "files;", sum(1 for r in rows if not r["content"]), "without description:", [r["file"] for r in rows if not r["content"]][:10])
