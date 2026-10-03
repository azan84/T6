"""Flags / D3-D4 / decisive-geometry columns of the M1_results row (audit P5 Sol findings 2, 5, 6) on the five REAL P5 cases, read-only: post_helpers.py fill on p5/cases/<scan>_resistance (build_info.json) with the
automatic discovery of p5/out/<scan>/gates.json, p5/mesh/<scan>/mesh_gates.json and p5/mesh/<scan>/d34.json; outputs in a temp dir. Then the M1_results merge (m1_results.py: fill flags + build_info + NOT_CONVERGED)
for a converged and an unconverged verdict. usage: python3 tests/test_flags_p5.py [extra_case_dir:scan ...]   (e.g. the temp rebuild of 272 with the new builder)"""
import os, sys, json, subprocess, tempfile, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); TC = os.path.dirname(HERE); PILOT = os.path.dirname(TC)
sys.path.insert(0, f"{TC}/pf")
import post_helpers as PH

EXPECTED = {   # brief OPUS_BRIEF_37 item 3
    "138": dict(flags="D3_FAIL;D4_FAIL;CHECKMESH_STANDARD_FAIL", geometry_step_ok=True),          # its only failed gate is the reported-only absolute check (D10)
    "69": dict(flags="LESION_PURITY_GATE_FAIL;POSITIVE_CONTROL_UNDETECTED", geometry_step_ok=False, D3_verdict="PASS", D4_verdict="PASS"),
    "473": dict(flags="D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL;MEASUREMENT_PROBE_RELOCATED", geometry_step_ok=False),
    "272": dict(flags="SELF_INTERSECTION;D3_FAIL;D4_FAIL;OUTLET_LOST_IN_MESH", geometry_step_ok=False, outlets_lost_in_mesh="out_396"),
    "139": dict(flags="D2_RELATIVE_THROAT_GATE_FAIL;D3_FAIL;D4_FAIL", geometry_step_ok=False),
}

def main():
    tmp = tempfile.mkdtemp(prefix="flags37_"); cases = [(f"{PILOT}/p5/cases/{s}_resistance", s) for s in EXPECTED] + [tuple(a.rsplit(":", 1)) for a in sys.argv[1:]]
    try:
        for case, scan in cases:
            info = json.load(open(f"{case}/build_info.json")); out = f"{tmp}/fill_{scan}_{os.path.basename(case)}.json"
            r = subprocess.run([sys.executable, f"{TC}/pf/post_helpers.py", "fill", case, info["package"], out], capture_output=True, text=True); assert r.returncode == 0, r.stdout + r.stderr
            f = json.load(open(out)); exp = EXPECTED[scan]
            for k, v in exp.items(): assert f.get(k) == v, (scan, k, f.get(k), v)
            assert f["geometry_all_gates_pass_including_reported"] is False and f["manual_repair_needed"] is False
            assert f["geometry_gates_failed_reported_only"] == ["lesion_literal_absolute_r_target_check"], f["geometry_gates_failed_reported_only"]
            for k in ("D3_verdict", "D4_verdict", "D34_min_dist_throat_mm", "D34_min_dist_measurement_mm"): assert f.get(k) not in (None, ""), (scan, k)
            # the M1_results merge of m1_results.py: fill flags + build_info flags (+ NOT_CONVERGED)
            lost = ["OUTLET_LOST_IN_MESH"] if PH.C.lost_outlets(info) else []; rel = ["MEASUREMENT_PROBE_RELOCATED"] if info.get("measurement_probe_relocated") else []
            row_conv = PH.flags_str(PH.merge_flags(f["flags"], rel, lost, [])); row_unconv = PH.flags_str(PH.merge_flags(f["flags"], rel, lost, ["NOT_CONVERGED"]))
            assert row_conv == exp["flags"] and row_unconv == exp["flags"] + ";NOT_CONVERGED"
            print(f"{scan:>4s} {os.path.relpath(case, PILOT)}: flags {f['flags']} | geometry_step_ok {f['geometry_step_ok']} (incl. reported {f['geometry_all_gates_pass_including_reported']}) | "
                  f"D3 {f['D3_verdict']} D4 {f['D4_verdict']} thr {f['D34_min_dist_throat_mm']:.3f} mm meas {f['D34_min_dist_measurement_mm']:.3f} mm ({f['D34_probes']}; within 2 mm: {f['D34_checks_within_2mm'] or '-'}) | "
                  f"decisive failed {f['geometry_gates_failed_decisive']} | lost {f['outlets_lost_in_mesh'] or '-'} | manual repair {f['manual_repair_needed']} ({f['sources']['manual_repair_needed']}) | unconverged row: {row_unconv}")
        # the flag order is fixed and 'NONE' is the empty value
        assert PH.flags_str(PH.merge_flags("NONE", [])) == "NONE" and PH.flags_str(PH.merge_flags("NOT_CONVERGED;D3_FAIL", ["GEOMETRY_GATE_FAIL:frame_check"])) == "GEOMETRY_GATE_FAIL:frame_check;D3_FAIL;NOT_CONVERGED"
        print(f"PASS: {len(cases)} cases, expected flag sets reproduced")
    finally: shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
