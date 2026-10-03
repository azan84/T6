#!/bin/bash
# End-to-end test of post_case_generic.sh on a SYNTHETIC finished solve (no real case is solved): tests/synthetic_tube.py writes a Gate-M1-format package (straight stenosed tube, measurement probe normal tilted
# 30 deg so that the strict section rule S1 fails) and a 41k-cell blockMesh mesh; pf/build_m1_case.py builds the production case (mesh-checked probe planes; the measurement probe must be RELOCATED, with the
# original-probe monitor kept); the solve runs 1000 iterations on 2 ranks (nice); then:
#   (a) post_case_generic.sh refuses the case before the solve (no 'End');  (b) it runs end to end after the solve and writes every output;  (c) the outputs are checked (probes csv incl. the relocated row,
#   contract radius files, results row + notes naming the probe used, REF_FFR comparison in the summary (package measurement row vs a reference), history with every iteration of measurementP AND measurementOrigP, settle csv, flow-state profile, summary with sha256, reconstruct check);
#   (d) a second run reuses the reconstruction, the cached analysis and the radius files (provenance verified);  (e) processor directories are still there;
#   attempt 3 (audit round 2): (f) an appended partial run in log.simpleFoam -> refused before anything is generated;  (g) a package whose probes.csv differs from the build_info hashes -> refused before
#   anything is generated;  (h) a log without 'Finalising parallel run' (analysis completion flag false) -> stop, exit 4;  (i) radius provenance recording another mesh -> regenerated; POST_REUSE_UNCHECKED=1 -> reused
#   and recorded as unchecked in the summary.
# Evidence (kB files) is copied to test_output/post_case_generic_synthetic/; the test root is removed at the end. usage: bash tests/test_post_case_generic.sh
set -e -o pipefail
TC=$(dirname "$(dirname "$(readlink -f "$0")")"); ROOT=$TC/.post_test_tmp; EV=$TC/test_output/post_case_generic_synthetic
rm -rf "$ROOT"; mkdir -p "$ROOT"; cd "$ROOT"
nice -n 10 python3 "$TC/tests/synthetic_tube.py" "$ROOT" --tilt-measurement 30
printf 'scan,side\n99999,left\n' > subset_synthetic.csv            # the synthetic 'scan' is not a cohort case: a test-only E0 subset file
nice -n 10 python3 "$TC/pf/build_m1_case.py" pkg/SYN_tube_test__baseline__real mesh resistance case_syn 2 --pkg-root pkg --csv-subset subset_synthetic.csv | tail -2
grep -q "^    measurementP$" case_syn/system/controlDict && grep -q "^    measurementOrigP$" case_syn/system/controlDict
sed -i 's/^endTime         3000;/endTime         1000;/' case_syn/system/controlDict          # test copy only (the template budget stays 3000)
echo "(a) refusal before the solve:"; if bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > refuse.txt 2>&1; then echo "FAIL: unfinished case accepted"; exit 1; fi; tail -1 refuse.txt
( source /usr/lib/openfoam/openfoam2406/etc/bashrc >/dev/null 2>&1 || true; cd case_syn && nice -n 10 decomposePar > log.decomposePar 2>&1 && nice -n 10 mpirun -np 2 simpleFoam -parallel > log.simpleFoam 2>&1 ); tail -1 case_syn/log.simpleFoam
echo "(b) post-processing:"; REF_FFR=0.9796 PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post1.txt 2>&1; grep -E "POSTDONE|RUN COMPLETE|package verified|as-meshed radius:|cross-check|RECONSTRUCT|FAILED_SECTION|wrote .*(flow_state|post_summary)" post1.txt | cut -c1-250
echo "(c) output checks:"; python3 - "$ROOT" <<'PY'
import sys, csv, json, os
R = sys.argv[1]; O = f"{R}/out"; rd = lambda f: list(csv.DictReader(open(f"{O}/{f}")))
NC = json.load(open(f"{R}/mesh/mesh_gates.json"))["cells"]; bi = json.load(open(f"{R}/case_syn/build_info.json")); rel = bi["measurement_probe_relocated"]
assert bi["measurement_section_rule"]["status"] == "FAILED_SECTION_RULE" and bi["measurement_probe_used"] == "p004_reloc" and rel["original"]["original_monitor"] == "measurementOrigFlux/measurementOrigP"
assert abs(rel["relocated"]["arc_from_original_mm"] - 0.5) < 1e-9 and rel["relocated"]["tree_node"] == 33, rel["relocated"]          # nearest node, ties distal first
pr = rd("M1_probes_syn_resistance.csv"); k = {r["kind"]: r for r in pr}
assert set(k) >= {"inlet", "throat", "measurement", "measurement_relocated", "outlet"} and k["measurement_relocated"]["probe_id"] == "p004_reloc" and k["measurement_relocated"]["section_ok"] == "1"
for f in ("as_meshed_radius_syn.csv", "as_meshed_radius_syn_inscribed.csv"):
    r = rd(f); assert list(r[0]) == ["tree_node", "s_mm", "r_asmeshed_mm", "r_area_equiv_mm", "r_max_inscribed_mm", "section_area_mm2", "covered"] and len(r) == 41 and sum(int(x["covered"]) for x in r) >= 38
res = rd("M1_results.csv"); assert len(res) == 1 and res[0]["converged"] == "CONVERGED" and res[0]["iterations"] == "1000" and "measurement probe USED: p004_reloc (RELOCATED" in res[0]["notes"] and res[0]["n_cells"] == str(NC)
assert len(rd("M1_outlets_syn_resistance.csv")) == 1
h = json.load(open(f"{O}/M1_monitor_history_syn_resistance.json")); assert all(h["every_iteration"].values()) and {"measurementP", "measurementOrigP"} <= set(h["monitors"]) and h["n_iterations"] == 1000
cc = h["cross_check_probes_csv"]; assert cc["measurementP"]["area_flag"] == "OK" and cc["measurementOrigP"]["area_flag"] == "OK" and abs(cc["measurementP"]["difference"]) < 1e-4, cc
s = rd("settle_syn_resistance.csv"); assert s[0]["b1_label"] == "B1" and "RUN THE FULL BUDGET" in s[0]["stop_recommendation"]
fs = rd("flow_state_syn_resistance.csv"); assert len(fs) >= 9 and all(r["section_ok"] == "1" for r in fs) and max(float(r["offset_over_req"]) for r in fs) < 0.01
sm = json.load(open(f"{O}/post_summary_syn_resistance.json")); rc = sm["reference_comparison"]; assert rc["probe_id"] == "p004" and rc["within"] and abs(rc["DeltaFFR"]) < 1e-3, rc
assert sm["verdict"] == "CONVERGED" and sm["cells"] == NC and not sm["missing_outputs"] and len(sm["outputs"]) == 15 and sm["measurement_probe_used"] == "p004_reloc", (len(sm["outputs"]), sm["missing_outputs"])
assert sm["run_completion"]["ok"] and sm["analysis_log_finished"] and sm["package_check"]["ok"] and sm["package_check"]["package_dir"] == f"{R}/pkg/SYN_tube_test__baseline__real" and sm["radius_outputs"].startswith("regenerated"), sm["radius_outputs"]
assert json.load(open(f"{O}/as_meshed_radius_syn_provenance.json"))["mesh"]["sha256"]
assert json.load(open(f"{O}/reconstruct_check_syn_resistance.json"))["ok"]
print(f"outputs OK: probes {len(pr)} rows (relocated row valid), radius 41 nodes, results row CONVERGED, history {h['n_iterations']} it (measurementP {cc['measurementP']['monitor_last_p_over_Paorta']:.6f} vs section {cc['measurementP']['section_p_over_Paorta']:.6f}; "
      f"measurementOrigP {cc['measurementOrigP']['monitor_last_p_over_Paorta']:.6f}), B1 first settled {s[0]['iter_first_settled']}, flow-state max offset/r_eq {max(float(r['offset_over_req']) for r in fs):.2e}, wall clock {sm['wall_clock_s']} s")
PY
echo "(d) second run:"; PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post2.txt 2>&1
grep -q "reconstructPar not re-run" post2.txt && grep -q "as-meshed radius: reused (provenance verified" post2.txt && grep -q "cached analysis reused" post2.txt && grep -q POSTDONE post2.txt && echo "second run reused the reconstruction, the radius files and the cached analysis"
echo "(e) processor directories kept:"; ls -d case_syn/processor* | tr '\n' ' '; echo
stamp() { stat -c %Y out/M1_probes_syn_resistance.csv out/post_summary_syn_resistance.json | tr '\n' ' '; }
cp case_syn/log.simpleFoam log.keep
echo "(f) appended partial run:"; printf 'Build  : v2406\nExec   : simpleFoam -parallel\nStarting time loop\n\nTime = 1001\n\n' >> case_syn/log.simpleFoam; S0=$(stamp); sleep 1
if PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_f.txt 2>&1; then echo "FAIL: appended run accepted"; exit 1; fi
[ "$(stamp)" = "$S0" ] || { echo "FAIL: outputs touched"; exit 1; }; grep "RUN NOT COMPLETE" post_f.txt | cut -c1-200; cp log.keep case_syn/log.simpleFoam
echo "(g) package not matching build_info hashes:"; mkdir -p pkg_t; cp -r pkg/SYN_tube_test__baseline__real pkg_t/; echo "" >> pkg_t/SYN_tube_test__baseline__real/probes.csv; S0=$(stamp)
if PKG_ROOT=$ROOT/pkg_t bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_g.txt 2>&1; then echo "FAIL: tampered package accepted"; exit 1; fi
[ "$(stamp)" = "$S0" ] || { echo "FAIL: outputs touched"; exit 1; }; grep "PACKAGE NOT VERIFIED" post_g.txt | cut -c1-250
echo "(h) analysis completion flag false (no 'Finalising parallel run'):"; grep -v "^Finalising parallel run" log.keep > case_syn/log.simpleFoam
set +e; PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_h.txt 2>&1; rc=$?; set -e
[ $rc -eq 4 ] || { echo "FAIL: exit $rc (expected 4)"; exit 1; }; grep -- "--require-finished:" post_h.txt | cut -c1-200; cp log.keep case_syn/log.simpleFoam
echo "(i) radius provenance of another mesh / unchecked reuse:"; python3 -c "import json,sys; f=sys.argv[1]; j=json.load(open(f)); j['mesh']['sha256']='0'*64; json.dump(j,open(f,'w'))" out/as_meshed_radius_syn_provenance.json
PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_i1.txt 2>&1; grep -E "NOT reusable|as-meshed radius:" post_i1.txt | cut -c1-200
grep -q "as-meshed radius: regenerated" post_i1.txt && python3 -c "import json; assert json.load(open('out/post_summary_syn_resistance.json'))['radius_outputs'].startswith('regenerated')"
POST_REUSE_UNCHECKED=1 PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_i2.txt 2>&1; grep "as-meshed radius:" post_i2.txt | cut -c1-200
python3 -c "import json; s=json.load(open('out/post_summary_syn_resistance.json')); assert s['radius_outputs'].startswith('REUSED UNCHECKED'), s['radius_outputs']"
PKG_ROOT=$ROOT/pkg bash "$TC/post_case_generic.sh" case_syn SYN_tube_test__baseline__real syn resistance out > post_i3.txt 2>&1; grep -q "as-meshed radius: reused (provenance verified" post_i3.txt && echo "guards (f)-(i) OK; final run reuses with verified provenance"
rm -rf "$EV"; mkdir -p "$EV"; cp out/*.csv out/*.json out/*.log post*.txt refuse.txt "$EV/"; cp case_syn/build_info.json case_syn/system/controlDict case_syn/log.simpleFoam case_syn/log.reconstructPar "$EV/"
cd /; rm -rf "$ROOT"
echo "PASS: post_case_generic.sh end to end on a synthetic finished solve (evidence in test_output/post_case_generic_synthetic/)"
