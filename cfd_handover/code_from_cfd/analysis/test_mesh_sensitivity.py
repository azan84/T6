"""Asymmetric arithmetic tests for mesh_sensitivity.py (identical-input self-tests cannot establish correctness)."""
import sys, os, copy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import mesh_sensitivity as M
L = M.label
def lab(name, m50, a, b, w, wc=True): return L(name, m50, a, b, w, wc)[0]
F = "flow_red_distal_pct"                                             # abs tolerance 0.5
n = 0
def check(cond, msg):
    global n; n += 1
    assert cond, "FAILED: " + msg
    print("ok  ", msg)
# monotonicity direction (the round-1 audit example)
check(lab(F, 10, 10.3, 10.3, 12) == "NON-MONOTONE", "W100=12, M50=10, T25=10.3 -> series 12,10,10.3 turns -> NON-MONOTONE")
check(lab(F, 10, 9.7, 9.7, 12) == "INSENSITIVE", "W100=12, M50=10, T25=9.7 -> series 12,10,9.7 monotone -> INSENSITIVE")
# threshold equality is inside the tolerance, just beyond is outside
check(lab(F, 10, 10.5, 10.5, 10.5) == "INSENSITIVE", "change exactly equal to the tolerance is within tolerance")
check(lab(F, 10, 10.5000001, 10.5000001, 10.5) == "SENSITIVE", "change just above the tolerance -> SENSITIVE")
# T25b alone beyond the tolerance from M50
check(lab(F, 10, 10.4, 9.4, 10) == "SENSITIVE", "T25b 0.6 from M50 while T25a is within -> SENSITIVE (precedence over interface)")
# interface disagreement while both are within tolerance of M50
check(lab(F, 10, 10.4, 9.6, 10) == "INTERFACE-CONTAMINATED", "T25a vs T25b differ by 0.8 (>0.5), each within 0.5 of M50 -> INTERFACE-CONTAMINATED")
# precedence: sensitive beats non-monotone beats insensitive
check(lab(F, 10, 11, 11, 13) == "SENSITIVE", "SENSITIVE takes precedence over NON-MONOTONE")
# invalid numbers
for bad in (float("nan"), float("inf"), -float("inf")):
    check(lab(F, 10, bad, 10, 10).startswith("UNASSESSABLE"), f"{bad} in T25a -> UNASSESSABLE")
    check(lab(F, bad, 10, 10, 10).startswith("UNASSESSABLE"), f"{bad} in M50 -> UNASSESSABLE")
    check(lab(F, 10, 10, 10, bad).startswith("UNASSESSABLE"), f"{bad} in W100 -> UNASSESSABLE (converged coarse level)")
# unconverged W100: fine side only, non-finite W100 ignored
check(lab(F, 10, 10.1, 10.2, float("nan"), wc=False).startswith("INSENSITIVE on the fine side"), "W100 unconverged -> fine-side label only")
check(lab(F, 10, 12, 12, float("nan"), wc=False) == "SENSITIVE", "W100 unconverged does not hide a fine-side SENSITIVE")
# relative tolerance and a zero reference value
R = "umax_ms"                                                          # rel 5 %
check(lab(R, 1.0, 1.05, 1.05, 1.0) == "INSENSITIVE", "5 % relative change equals tolerance -> within")
check(lab(R, 1.0, 1.051, 1.051, 1.0) == "SENSITIVE", "5.1 % relative change -> SENSITIVE")
check(lab(R, 0.0, 0.0, 0.0, 0.0) == "INSENSITIVE", "zero reference with zero change")
check(lab(R, 0.0, 0.001, 0.001, 0.0) == "SENSITIVE", "zero reference, any change -> SENSITIVE (tolerance 0)")
# missing data must not shrink windows: mutate real M50 data
c = M.load("solve_lesion80", "lesion80"); ref = M.load("solve_baseline_ref", "baseline_ref")
q0 = M.quantities(c, ref)
check(q0["recovery_arc_wss_mm"] == 39.0 and q0["missing"] == {}, "real M50 data: recovery 39.0 with no missing stations")
c1 = copy.deepcopy(c); c1["W"].loc[c1["W"].s_mm > 39.0, "f_rev"] = np.nan
q1 = M.quantities(c1, ref); check(np.isnan(q1["recovery_arc_wss_mm"]) and "recovery_arc_wss_mm" in q1["missing"], "WSS NaN after 39 mm -> recovery NaN (not 39)")
c1b = copy.deepcopy(c); c1b["W"].loc[c1b["W"].s_mm > 39.0, "f_rev"] = 0.5
q1b = M.quantities(c1b, ref); check(q1b["recovery_arc_wss_mm"] == M.NEVER and q1b["missing"] == {} and "recovery_arc_wss_mm" in q1b["physical_outcome_notes"], "reversed fraction 0.5 beyond 39 mm -> recovery = NEVER sentinel with a physical-outcome note (not NaN/missing)")
c1c = copy.deepcopy(c); c1c["W"].loc[c1c["W"].s_mm >= 23.5, "f_rev"] = 0.0
q1c = M.quantities(c1c, ref); check(q1c["onset_arc_mm"] == M.NEVER and q1c["recovery_arc_wss_mm"] == M.NEVER and q1c["missing"] == {}, "no separation anywhere -> onset and recovery = NEVER sentinel with notes (distinct from missing data)")
check(L("onset_arc_mm", 24.25, 24.25, 24.25, 24.25)[0] == "INSENSITIVE" and L("onset_arc_mm", 24.25, M.NEVER, M.NEVER, 24.25)[0] == "SENSITIVE", "a level with no separation is SENSITIVE against one with separation (not hidden as UNASSESSABLE)")
c2 = copy.deepcopy(c); c2["W"] = c2["W"][~((c2["W"].s_mm > 30.0) & (c2["W"].s_mm < 30.6))]
q2 = M.quantities(c2, ref); check(np.isnan(q2["recovery_arc_wss_mm"]) and np.isnan(q2["onset_arc_mm"]), "dropped WSS stations -> onset/recovery NaN, gap not bridged")
c3 = copy.deepcopy(c); c3["W"].loc[c3["W"].s_mm == 31.0, "f_rev"] = np.inf
q3 = M.quantities(c3, ref); check(np.isnan(q3["max_reversed_wall_fraction"]) or np.isfinite(q3["max_reversed_wall_fraction"]) and "recovery_arc_wss_mm" in q3["missing"], "inf f_rev -> recovery NaN")
c4 = copy.deepcopy(c); c4["S"].loc[(c4["S"].s_mm - 29.5).abs() < 1e-6, "ok"] = False
q4 = M.quantities(c4, ref); check(np.isnan(q4["added_static_loss_mmHg"]) and np.isnan(q4["p_min_over_Pao"]), "invalid 29.5 section -> loss and p_min NaN (no silent substitution)")
c5 = copy.deepcopy(c); c5["S"] = c5["S"][(c5["S"].s_mm - 29.5).abs() > 1e-6]
q5 = M.quantities(c5, ref); check(np.isnan(q5["added_static_loss_mmHg"]), "absent 29.5 section -> loss NaN (does not take 31.0)")
c6 = copy.deepcopy(c); c6["S"] = c6["S"][(c6["S"].s_mm - 38.5).abs() > 1e-6]
q6 = M.quantities(c6, ref); check(np.isnan(q6["max_reversed_area_fraction"]), "missing far section -> max reversed area NaN (window not shrunk)")
# convergence / time consistency gate through main(): mutate and write temp analysis is out of scope here; label() gate covered above
print(f"\nALL {n} CHECKS PASSED")

# ---------------- main()-level tests on copied case directories ----------------
import shutil, json, tempfile, io, contextlib
W = tempfile.mkdtemp(prefix="sens_test_")
def mk(name, src, mode):
    d = os.path.join(W, name); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for f in ("analysis.json", f"sections_{mode}.csv", f"sections_{mode}.json", f"wss_{mode}.csv", f"wss_{mode}.json"):
        shutil.copy(os.path.join(M.BASE, src, f), d)
    return d
def edit(d, f, fn):
    p = os.path.join(d, f); x = json.load(open(p)); fn(x); json.dump(x, open(p, "w"))
def run(**over):
    cases = {k: os.path.join(W, v) for k, v in over.items()}
    out = os.path.join(W, "out.json"); buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf): M.main(out, [f"{k}={v}" for k, v in cases.items()])
    except SystemExit as e: return "EXIT:" + str(e), None
    return None, json.load(open(out))
def fresh(*names):
    for nm in names: mk(nm, "solve_baseline_ref" if nm.startswith("ref") else "solve_lesion80", "baseline_ref" if nm.startswith("ref") else "lesion80")
base = dict(M50="m50", T25a="a", T25b="b", W100="w", REF="ref")
def all_unassessable(r): return all(v["label"].startswith("UNASSESSABLE") for v in r["labels"].values())
fresh("m50", "a", "b", "w", "ref")
err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "main(): identical real inputs -> all INSENSITIVE")
# ---- W100 policy
fresh("w"); edit(os.path.join(W, "w"), "wss_lesion80.json", lambda x: x.update(time=1363.0))
err, r = run(**base); check(all_unassessable(r) and any("time-inconsistent" in b for b in r["unconverged_or_inconsistent"]), "W100 converged but time-inconsistent -> every label UNASSESSABLE")
fresh("w"); edit(os.path.join(W, "w"), "analysis.json", lambda x: x.update(verdict="UNCONVERGED"))
for f in ("sections_lesion80.csv", "sections_lesion80.json", "wss_lesion80.csv", "wss_lesion80.json"): os.remove(os.path.join(W, "w", f))
err, r = run(**base); check(err is None and all(v["label"].startswith("INSENSITIVE on the fine side") for v in r["labels"].values()), "W100 genuinely unconverged (valid analysis.json, no post-processing) -> fine-side labels only")
fresh("w")
for f in ("sections_lesion80.csv",): os.remove(os.path.join(W, "w", f))
err, r = run(**base); check(err is not None and "post-processing files missing" in err, "converged W100 without post-processing -> hard stop, not excused")
for label_, corrupt in (("wss json time 'abc'", lambda d: edit(d, "wss_lesion80.json", lambda x: x.update(time="abc"))), ("empty wss csv", lambda d: open(os.path.join(d, "wss_lesion80.csv"), "w").write("")),
                        ("sections json is a list", lambda d: json.dump([1], open(os.path.join(d, "sections_lesion80.json"), "w"))), ("last_iteration null", lambda d: edit(d, "analysis.json", lambda x: x.update(last_iteration=None))),
                        ("verdict is a dict", lambda d: edit(d, "analysis.json", lambda x: x.update(verdict={"a": 1}))), ("verdict is a list", lambda d: edit(d, "analysis.json", lambda x: x.update(verdict=["UNCONVERGED"]))),
                        ("verdict absent", lambda d: edit(d, "analysis.json", lambda x: x.pop("verdict"))), ("analysis.json malformed", lambda d: open(os.path.join(d, "analysis.json"), "w").write("{not json")),
                        ("outlets null", lambda d: edit(d, "analysis.json", lambda x: x.update(outlets=None))), ("outlet_D1 null", lambda d: edit(d, "analysis.json", lambda x: x["outlets"].update(outlet_D1=None))),
                        ("P_over_Paorta null", lambda d: edit(d, "analysis.json", lambda x: x["outlets"]["outlet_D2"].update(P_over_Paorta=None))), ("Q_mls true", lambda d: edit(d, "analysis.json", lambda x: x["outlets"]["outlet_D1"].update(Q_mls=True))),
                        ("Q_mls 1e6", lambda d: edit(d, "analysis.json", lambda x: x["outlets"]["outlet_D1"].update(Q_mls=1e6))), ("sum true", lambda d: edit(d, "analysis.json", lambda x: x.update(sum_outlets_mls=True))),
                        ("last_iteration true", lambda d: edit(d, "analysis.json", lambda x: x.update(last_iteration=True)))):
    fresh("w"); corrupt(os.path.join(W, "w")); err, r = run(**base)
    check(err is None and all_unassessable(r) and any("unreadable" in b for b in r["unconverged_or_inconsistent"]) and not any(v["label"].startswith("INSENSITIVE on the fine side") for v in r["labels"].values()), f"W100 {label_} -> UNREADABLE, every label UNASSESSABLE (no unconverged exemption)")
for pos in ("m50", "a", "b", "ref"):
    for label_, corrupt in (("outlet_D1 removed", lambda d: edit(d, "analysis.json", lambda x: x["outlets"].pop("outlet_D1"))), ("verdict absent", lambda d: edit(d, "analysis.json", lambda x: x.pop("verdict"))),
                            ("P_over_Paorta null", lambda d: edit(d, "analysis.json", lambda x: x["outlets"]["outlet_D1"].update(P_over_Paorta=None))), ("reference infinite total", lambda d: edit(d, "analysis.json", lambda x: x.update(sum_outlets_mls=float("inf")))),
                            ("zero total", lambda d: edit(d, "analysis.json", lambda x: x.update(sum_outlets_mls=0.0))), ("D2 flow 1e308", lambda d: edit(d, "analysis.json", lambda x: x["outlets"]["outlet_D2"].update(Q_mls=1e308)))):
        fresh("m50", "a", "b", "w", "ref"); corrupt(os.path.join(W, pos)); err, r = run(**base)
        check(err is not None and "must be readable" in err, f"{pos}: {label_} -> clear stop message (no traceback, no label)")
# ---- booleans / duplicate headers / bad columns in the CSVs
fresh("m50", "a", "b", "w", "ref")
pp = os.path.join(W, "a", "wss_lesion80.csv"); d = pd.read_csv(pp); d["f_rev"] = False; d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "must be readable" in err, "boolean f_rev column in T25a -> stop (booleans are not physical numbers)")
fresh("a"); pp = os.path.join(W, "a", "wss_lesion80.csv"); d = pd.read_csv(pp); d["f_rev.1"] = -0.001; d = d.rename(columns={"f_rev.1": "f_rev"}); d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "duplicate column" in err, "duplicate f_rev header in T25a -> stop")
fresh("a"); pp = os.path.join(W, "a", "sections_lesion80.csv"); d = pd.read_csv(pp); d["p_over_Pao"] = d["p_over_Pao"].astype(object); d.loc[(d.s_mm - 24.0).abs() < 1e-6, "p_over_Pao"] = "abc"; d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "must be readable" in err, "string in a pressure cell -> stop")
fresh("a"); pp = os.path.join(W, "a", "sections_lesion80.csv"); d = pd.read_csv(pp).drop(columns=["umax_ms"]); d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "must be readable" in err, "missing column -> stop")
fresh("a"); pp = os.path.join(W, "a", "sections_lesion80.csv"); d = pd.read_csv(pp); d["s_mm"] = d["s_mm"].astype(object); d.loc[3, "s_mm"] = "x"; d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "must be readable" in err, "string in s_mm -> stop")
fresh("a"); pp = os.path.join(W, "a", "sections_lesion80.csv"); d = pd.read_csv(pp); d["ok"] = d["ok"].astype(object); d.loc[(d.s_mm - 29.5).abs() < 1e-6, "ok"] = np.nan; d.to_csv(pp, index=False)
err, r = run(**base); check(err is not None and "must be readable" in err, "ok flag NaN (not an explicit True/False column) -> stop")
fresh("a"); edit(os.path.join(W, "a"), "wss_lesion80.json", lambda x: x.update(time=True))
err, r = run(**base); check(err is not None and "must be readable" in err, "boolean time in T25a -> stop")
err, r = run(M50="m50", T25a="a", T25b="b", W100="w", REF="ref", BOGUS="x"); check(err is not None and "unknown level tag" in err, "unknown level tag -> clear stop message")
err, r = run(**dict(base, T25a="does_not_exist")); check(err is not None and "analysis.json not found" in err, "absent case directory -> clear stop message")
# ---- unconverged levels
fresh("a"); edit(os.path.join(W, "a"), "analysis.json", lambda x: x.update(verdict="UNCONVERGED"))
err, r = run(**base); check(err is None and all_unassessable(r), "T25a unconverged -> all UNASSESSABLE")
fresh("a"); fresh("ref"); edit(os.path.join(W, "ref"), "analysis.json", lambda x: x.update(verdict="UNCONVERGED"))
err, r = run(**base); check(err is None and all_unassessable(r), "REF unconverged -> all UNASSESSABLE")
fresh("m50", "a", "b", "w", "ref")
for f, k in (("analysis.json", "last_iteration"), ("sections_lesion80.json", "time"), ("wss_lesion80.json", "time")): edit(os.path.join(W, "a"), f, lambda x, k=k: x.update({k: 0.0}))
err, r = run(**base); check(err is not None and "must be readable" in err, "all times zero (non-positive) -> not readable")
# ---- values that are readable but nonsense at the station level stay per-quantity UNASSESSABLE
fresh("a"); pp = os.path.join(W, "a", "wss_lesion80.csv"); d = pd.read_csv(pp); d.loc[d.s_mm >= 23.5, "f_rev"] = -0.001; d.to_csv(pp, index=False)
err, r = run(**base); check(err is None and r["labels"]["onset_arc_mm"]["label"].startswith("UNASSESSABLE") and "outside the physical range" in json.dumps(r["quantities"]["T25a"]["missing"]), "f_rev = -0.001 -> onset/recovery UNASSESSABLE with an out-of-range reason")
fresh("a"); pp = os.path.join(W, "a", "wss_lesion80.csv"); d = pd.read_csv(pp); d.loc[d.s_mm >= 23.5, "f_rev"] = 1.0001; d.to_csv(pp, index=False)
err, r = run(**base); check(err is None and r["labels"]["max_reversed_wall_fraction"]["label"].startswith("UNASSESSABLE"), "f_rev = 1.0001 -> max reversed wall fraction UNASSESSABLE")
fresh("a"); pp = os.path.join(W, "a", "sections_lesion80.csv"); d = pd.read_csv(pp); d.loc[(d.s_mm - 29.5).abs() < 1e-6, "ok"] = False; d.to_csv(pp, index=False)
err, r = run(**base); check(err is None and r["labels"]["added_static_loss_mmHg"]["label"].startswith("UNASSESSABLE"), "invalid 29.5 section -> loss UNASSESSABLE (no substitution)")
# ---- physical-outcome categories through main(), every level position, incl. the W100 sentinel interplay
def setf(name, val):
    p = os.path.join(W, name, "wss_lesion80.csv"); d = pd.read_csv(p); d.loc[d.s_mm >= 23.5, "f_rev"] = val; d.to_csv(p, index=False)
for pos in ("m50", "a", "b"):
    fresh("m50", "a", "b", "w")
    for nm in ("m50", "a", "b", "w"): setf(nm, 0.5)
    setf(pos, 0.0); err, r = run(**base)
    check(r["labels"]["recovery_arc_wss_mm"]["label"].startswith("SENSITIVE (outcome category differs") and r["labels"]["onset_arc_mm"]["label"].startswith("SENSITIVE"), f"no-separation at {pos} vs never-recovering elsewhere -> recovery AND onset SENSITIVE")
fresh("m50", "a", "b", "w")
for nm in ("m50", "a", "b"): setf(nm, 0.5)
setf("w", 0.0); err, r = run(**base); check(r["labels"]["recovery_arc_wss_mm"]["label"].startswith("INSENSITIVE on the fine side; W100 outcome category differs"), "W100-only category change -> fine-side INSENSITIVE with the coarse-side dependence stated")
# round-5 counterexample: recovery arcs 39 / 39.25 / 39 with W100 never recovering must NOT become NON-MONOTONE through the sentinel
def setrec(name, last_rev):                                        # f_rev = 0.5 up to last_rev, 0 afterwards (recovery just after last_rev)
    p = os.path.join(W, name, "wss_lesion80.csv"); d = pd.read_csv(p); d.loc[d.s_mm >= 23.5, "f_rev"] = 0.5; d.loc[d.s_mm > last_rev, "f_rev"] = 0.0; d.to_csv(p, index=False)
fresh("m50", "a", "b", "w"); setrec("m50", 38.75); setrec("a", 39.0); setrec("b", 38.75); setf("w", 0.5)
err, r = run(**base); lab = r["labels"]["recovery_arc_wss_mm"]["label"]
check(lab.startswith("INSENSITIVE on the fine side; W100 outcome category differs") and "NON-MONOTONE" not in lab, "recovery 39/39.25/39 with W100 not recovered -> fine-side label naming the W100 category (no sentinel NON-MONOTONE)")
fresh("m50", "a", "b", "w"); setrec("m50", 38.75); setrec("a", 41.0); setrec("b", 38.75); setf("w", 0.5)
err, r = run(**base); check(r["labels"]["recovery_arc_wss_mm"]["label"] == "SENSITIVE", "fine-side numeric change beyond tolerance still SENSITIVE when W100 category differs")
fresh("m50", "a", "b", "w")
err, r = run(**base); check(all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "restored inputs -> all INSENSITIVE again")
# ---- round-6 audit counterexamples
fresh("m50", "a", "b", "w", "ref")
pp = os.path.join(W, "a", "wss_lesion80.csv"); lines = open(pp).read().split("\n"); lines[0] += ',"f_rev"'; lines[1:] = [l + ",-0.001" if l else l for l in lines[1:]]; open(pp, "w").write("\n".join(lines))
err, r = run(**base); check(err is not None and "duplicate column" in err, "quoted duplicate CSV header ('f_rev' and \"f_rev\") -> stop")
fresh("a", "w"); pp = os.path.join(W, "w", "analysis.json"); txt = open(pp).read().rstrip(); txt = txt[:txt.rfind("}")] + ', "verdict": "UNCONVERGED"}'; open(pp, "w").write(txt)
pp2 = os.path.join(W, "w", "wss_lesion80.csv"); open(pp2, "w").write("garbage")
err, r = run(**base); check(all_unassessable(r) and any("unreadable" in b for b in r["unconverged_or_inconsistent"]), "duplicate JSON key 'verdict' (CONVERGED then UNCONVERGED) in W100 -> UNREADABLE, not the unconverged exemption")
fresh("a"); edit(os.path.join(W, "a"), "analysis.json", lambda x: x.update(sum_outlets_mls=9.0))
err, r = run(**base); check(err is not None and "must be readable" in err and "disagrees" in err, "sum_outlets_mls contradicting the outlet flows -> stop")
err, r = M.main(os.path.join(W, "o.json"), ["T25a"]) if False else (None, None)
for bad_arg in ("T25a", "T25a=a=b", "=x", "T25a="):
    try: M.main(os.path.join(W, "o.json"), [bad_arg]); check(False, f"bad argument {bad_arg!r} must stop")
    except SystemExit as e: check("bad argument" in str(e), f"malformed argument {bad_arg!r} -> clear stop message")
fresh("a", "w"); err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "restored inputs -> all INSENSITIVE again (final)")
# ---- round-7 audit counterexamples
fresh("m50", "a", "b", "w", "ref")
for nm in ("m50", "a", "b", "w"):
    pp = os.path.join(W, nm, "wss_lesion80.csv"); txt = open(pp, encoding="utf-8").read().split("\n"); txt[0] = "\ufefff_rev,z," + txt[0]; txt[1:] = ["0.0,0," + l if l else l for l in txt[1:]]; open(pp, "w", encoding="utf-8").write("\n".join(txt))
err, r = run(**base); check(err is not None and "header not read as written" in err, "BOM-prefixed duplicate f_rev column in every lesion level -> stop (no all-INSENSITIVE on the wrong column)")
fresh("m50", "a", "b", "w")
err, r = run(**dict(base, T25a="m50")); check(err is not None and "same directory" in err, "two tags pointing at the same directory -> stop")
os.symlink(os.path.join(W, "m50"), os.path.join(W, "w_link")); err, r = run(**dict(base, W100="w_link")); check(err is not None and "same directory" in err, "a tag pointing at a symlink to another level's directory -> stop")
os.mkdir(os.path.join(W, "outdir.json"))
for bad_out in ("/nonexistent_dir_xyz/o.json", os.path.join(W, "outdir.json")):
    try: M.main(bad_out, ["M50=" + os.path.join(W, "m50")]); check(False, "unwritable output must stop")
    except SystemExit as e: check("cannot write the output file" in str(e), f"unwritable output {bad_out!r} -> clear stop message before any analysis")
# ---- round-8 audit counterexamples: forgotten output argument, repeated tag, visible tag -> directory mapping
cwd0 = os.getcwd(); os.chdir(W); before_w, before_cwd = set(os.listdir(W)), set(os.listdir(cwd0))
for argv in (["T25a=solve_lesion80_T25a_v2"], ["T25a=a", "T25b=" + os.path.join(W, "b")]):   # relative name: the old code created a file literally named 'T25a=...' in the cwd
    try: M.main(argv[0], argv[1:]); check(False, "forgotten output argument must stop")
    except SystemExit as e: check("bad output path" in str(e) and ".json" in str(e), f"output argument omitted ({len(argv)} TAG args) -> clear stop message")
    check(set(os.listdir(W)) == before_w and set(os.listdir(cwd0)) == before_cwd and not any("=" in f for f in os.listdir(W) + os.listdir(cwd0)), f"output argument omitted ({len(argv)} TAG args) -> no file created in the temp dir or the script dir")
os.chdir(cwd0)
for bad_out in (os.path.join(W, "o.txt"), os.path.join(W, "o"), os.path.join(W, "o.json.bak"), os.path.join(W, "x=o.json")):
    try: M.main(bad_out, ["M50=" + os.path.join(W, "m50")]); check(False, f"output {bad_out!r} must stop")
    except SystemExit as e: check("bad output path" in str(e) and not os.path.exists(bad_out), f"output {os.path.basename(bad_out)!r} (not *.json or contains '=') -> stop, nothing created")
fresh("m50", "a", "b", "w", "ref")
try: M.main(os.path.join(W, "rep.json"), [f"{k}={os.path.join(W, v)}" for k, v in base.items()] + ["T25a=" + os.path.join(W, "b")]); check(False, "repeated tag must stop")
except SystemExit as e: check("more than once" in str(e) and "T25a" in str(e), "repeated tag T25a=a ... T25a=b -> stop (no silent last-wins)")
try: M.main(os.path.join(W, "rep.json"), ["W100=" + os.path.join(W, "w"), "W100=" + os.path.join(W, "w")]); check(False, "repeated identical tag must stop")
except SystemExit as e: check("more than once" in str(e), "repeated identical tag W100=w W100=w -> stop")
buf = io.StringIO()
with contextlib.redirect_stdout(buf): M.main(os.path.join(W, "out.json"), [f"{k}={os.path.join(W, v)}" for k, v in base.items() if k != "REF"])
lines = buf.getvalue().splitlines(); first_runs = next(i for i, l in enumerate(lines) if l.startswith("runs:"))
dirl = [l for l in lines[:first_runs] if l.startswith("dir:")]
check(len(dirl) == 5 and all(any(l.split()[1] == k and l.split()[3] == os.path.realpath(os.path.join(W, v)) and "(override)" in l for l in dirl) for k, v in base.items() if k != "REF"), "console lists tag -> directory for the four overridden tags before the 'runs:' line, marked (override)")
check(any(l.split()[1] == "REF" and l.split()[3] == os.path.realpath(os.path.join(M.BASE, M.DEFAULT["REF"])) and "(default)" in l for l in dirl), "console lists REF -> its default directory, marked (default): all five tag -> directory pairs shown")
# ---- round-9 audit counterexamples: NUL bytes inside numeric tokens / JSON; output write, flush or close failing
def put_nul(nm, f, fn):
    p = os.path.join(W, nm, f); b = open(p, "rb").read(); new = fn(b); assert new != b; open(p, "wb").write(new)
def nul_frev(b):                                                   # every f_rev cell -> b"0\x00.9" (pandas parsed this silently as 0.0)
    lines = b.split(b"\n"); i = [h.strip() for h in lines[0].decode().split(",")].index("f_rev")
    return b"\n".join([lines[0]] + [b",".join(c if j != i else b"0\x00.9" for j, c in enumerate(l.split(b","))) if l else l for l in lines[1:]])
fresh("m50", "a", "b", "w", "ref"); put_nul("a", "wss_lesion80.csv", nul_frev)
err, r = run(**base); check(err is not None and "T25a must be readable" in err and "NUL" in err and "wss_lesion80.csv" in err, "wss csv f_rev cells '0\\x00.9' in T25a -> stop naming the NUL byte (no SENSITIVE labels from 0.0)")
for nm, f, fn, what in (("w", "wss_lesion80.csv", nul_frev, "W100 wss csv f_rev"), ("w", "wss_lesion80.json", lambda b: b.replace(b'"time"', b'"ti\x00me"', 1), "W100 wss json key"),
                        ("w", "sections_lesion80.json", lambda b: b + b"\x00", "W100 sections json trailing NUL"), ("w", "analysis.json", lambda b: b"\x00" + b, "W100 analysis.json leading NUL")):
    fresh("a", "w"); put_nul(nm, f, fn); err, r = run(**base)
    check(err is None and all_unassessable(r) and any("unreadable" in b and "NUL" in b and f in b for b in r["unconverged_or_inconsistent"]), f"{what} -> W100 UNREADABLE (NUL byte named), every label UNASSESSABLE")
fresh("w"); put_nul("b", "sections_lesion80.csv", lambda b: b.replace(b",", b",\x00", 1))
err, r = run(**base); check(err is not None and "T25b must be readable" in err and "NUL" in err and "sections_lesion80.csv" in err, "NUL inside a sections csv of T25b -> stop naming the NUL byte")
fresh("b"); put_nul("ref", "sections_baseline_ref.json", lambda b: b.replace(b":", b":\x00", 1))
err, r = run(**base); check(err is not None and "REF must be readable" in err and "NUL" in err, "NUL inside the REF sections json -> stop naming the NUL byte")
fresh("ref"); err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "genuine files after the NUL cases -> all INSENSITIVE (reader unchanged for real data)")
for f in ("analysis.json", "sections_lesion80.csv", "sections_lesion80.json", "wss_lesion80.csv", "wss_lesion80.json"):
    check(b"\x00" not in open(os.path.join(W, "m50", f), "rb").read(), f"genuine {f} has no NUL byte and is accepted")
class FailingOut(io.StringIO):                                         # output stream failing on write or on close (ENOSPC), like a full disk
    def __init__(self, on): super().__init__(); self.on = on; self.closed_ok = False
    def write(self, x):
        if self.on == "write": raise OSError(28, "No space left on device")
        return super().write(x)
    def close(self):
        if self.on == "close" and not self.closed_ok: self.closed_ok = True; raise OSError(28, "No space left on device")
        super().close()
real_open = open
for on in ("write", "close"):
    outp = os.path.join(W, f"full_{on}.json"); holder = []
    def fake_open(p, *a, **k):
        if p == outp: holder.append(FailingOut(on)); return holder[-1]
        return real_open(p, *a, **k)
    M.open = fake_open                                                  # module global shadows the builtin inside mesh_sensitivity only
    try:
        with contextlib.redirect_stdout(io.StringIO()): M.main(outp, [f"{k}={os.path.join(W, v)}" for k, v in base.items()])
        check(False, f"output {on} failure must stop")
    except SystemExit as e: check("cannot write the output file" in str(e) and "No space left on device" in str(e) and holder and holder[-1].closed, f"OSError(ENOSPC) on output {on} -> clear stop message, stream closed")
    finally: del M.open
if os.path.exists("/dev/full"):                                        # the real thing: /dev/full accepts open() and fails with ENOSPC on flush/close
    os.symlink("/dev/full", os.path.join(W, "devfull.json"))
    try:
        with contextlib.redirect_stdout(io.StringIO()): M.main(os.path.join(W, "devfull.json"), [f"{k}={os.path.join(W, v)}" for k, v in base.items()])
        check(False, "/dev/full output must stop")
    except SystemExit as e: check("cannot write the output file" in str(e) and "No space left" in str(e), "output on /dev/full (ENOSPC at flush/close) -> clear stop message, no traceback")
# ---- round-10 audit counterexamples: pandas' lenient parser replaced by a strict reader (malformed quoting / odd tokens / ragged rows must never become numbers)
def put_txt(nm, f, fn):
    p = os.path.join(W, nm, f); b = open(p, "rb").read(); new = fn(b.decode()); assert new != b.decode(); open(p, "wb").write(new.encode())
def cell(col, tok, rows=None):                                     # replace column `col` in data rows (all, or the given 0-based data-row indices) by the raw token `tok`
    def fn(t):
        lines = t.split("\n"); i = lines[0].split(",").index(col)
        return "\n".join([lines[0]] + [",".join(c if j != i else tok for j, c in enumerate(l.split(","))) if l and (rows is None or k in rows) else l for k, l in enumerate(lines[1:])])
    return fn
def line_edit(fn_lines):
    def fn(t): lines = t.split("\n"); fn_lines(lines); return "\n".join(lines)
    return fn
S_CSV, W_CSV = "sections_lesion80.csv", "wss_lesion80.csv"
R10 = (("f_rev cells '\"0\".9'", W_CSV, cell("f_rev", '"0".9'), "malformed CSV"), ("unbalanced quote in an f_rev cell", W_CSV, cell("f_rev", '"0.9', [5]), "malformed CSV"),
       ("a row with one field too many", W_CSV, line_edit(lambda L: L.__setitem__(4, L[4] + ",0.0")), "fields"), ("a row with one field too few", S_CSV, line_edit(lambda L: L.__setitem__(4, L[4].rsplit(",", 1)[0])), "fields"),
       ("a blank line in the middle of the data", W_CSV, line_edit(lambda L: L.insert(30, "")), "blank line"), ("an f_rev cell with a leading space", W_CSV, cell("f_rev", " 0.0", [40]), "not a plain number"),
       ("a pressure cell '1,5' (quoted thousands/decimal comma)", S_CSV, cell("p_over_Pao", '"1,5"', [30]), "not a plain number"), ("a tau cell '0x1p3'", W_CSV, cell("tau_mean_Pa", "0x1p3", [30]), "not a plain number"),
       ("an overflowing token '1e400' in tau", W_CSV, cell("tau_mean_Pa", "1e400", [30]), "overflows"), ("an ok cell 'true' (lower case)", S_CSV, cell("ok", "true", [30]), "True/False"),
       ("an ok cell '1'", S_CSV, cell("ok", "1", [30]), "True/False"), ("an s_mm cell '1_0'", W_CSV, cell("s_mm", "1_0", [30]), "not a plain number"))
fresh("m50", "a", "b", "w", "ref")
for what, f, fn, why in R10:
    fresh("a"); put_txt("a", f, fn); err, r = run(**base)
    check(err is not None and "T25a must be readable" in err and f in err and why in err, f"T25a {what} -> stop naming the file and the defect ({why})")
for what, f, fn, why in R10[:6]:
    fresh("a", "w"); put_txt("w", f, fn); err, r = run(**base)
    check(err is None and all_unassessable(r) and any("unreadable" in b and f in b and why in b for b in r["unconverged_or_inconsistent"]), f"W100 {what} -> UNREADABLE, every label UNASSESSABLE")
fresh("w"); pp = os.path.join(W, "a", W_CSV); b0 = open(pp, "rb").read(); assert b"\r" not in b0; open(pp, "wb").write(b0.replace(b"\n", b"\r\n"))
err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "genuine CRLF wss csv in T25a -> accepted, all INSENSITIVE")
fresh("a"); pp = os.path.join(W, "a", S_CSV); open(pp, "a").write("\n")
err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "genuine file with a single trailing blank line -> accepted")
fresh("a"); pp = os.path.join(W, "a", W_CSV); d = pd.read_csv(pp); d.loc[d.s_mm > 39.0, "f_rev"] = np.nan; d.to_csv(pp, index=False)
err, r = run(**base); check(err is None and r["labels"]["recovery_arc_wss_mm"]["label"].startswith("UNASSESSABLE") and r["labels"]["tau_peak_throat_Pa"]["label"] == "INSENSITIVE", "genuine file with empty (NaN) cells -> read, recovery UNASSESSABLE, others unaffected")
Sa = M.read_csv_strict(os.path.join(W, "m50", S_CSV), ["s_mm", "p_over_Pao", "umax_ms", "frac_reversed_area"], ["ok"]); Wa = M.read_csv_strict(pp, ["s_mm", "tau_mean_Pa", "f_rev"])
check(all(Sa[c].dtype == np.float64 for c in ("s_mm", "p_over_Pao", "umax_ms", "frac_reversed_area")) and Sa["ok"].dtype == bool and Wa["f_rev"].dtype == np.float64 and Wa["f_rev"].isna().sum() == (Wa.s_mm > 39.0).sum() > 0, "strict reader: float64 numeric columns (empty -> NaN), bool ok column")
fresh("a"); pp = os.path.join(W, "a", W_CSV); d = pd.read_csv(pp); d.loc[d.s_mm >= 44.0, "f_rev"] = np.inf; d.loc[d.s_mm == 43.75, "f_rev"] = -np.inf; d.to_csv(pp, index=False)
err, r = run(**base); check(err is None and r["labels"]["recovery_arc_wss_mm"]["label"].startswith("UNASSESSABLE") and "non-finite" in json.dumps(r["quantities"]["T25a"]["missing"]), "pandas-written inf/-inf tokens -> read as non-finite, recovery UNASSESSABLE (not a stop)")
fresh("a"); err, r = run(**base); check(err is None and all(v["label"] == "INSENSITIVE" for v in r["labels"].values()), "restored inputs after the strict-reader cases -> all INSENSITIVE")
shutil.rmtree(W)
print(f"\nALL {n} CHECKS PASSED (incl. main()-level)")
