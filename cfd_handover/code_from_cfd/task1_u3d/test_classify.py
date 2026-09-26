import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import u3d_analyse as A
def wedge(vals):
    f = {f"W{i}": v for i, v in enumerate(vals)}; w = sorted(f, key=lambda s: int(s[1:])); f3 = [f[x] for x in w[-3:]]
    return dict(levels=w, finest_pair_abs=abs(f[w[-1]] - f[w[-2]]), differences_shrink=all(abs(f[w[i + 1]] - f[w[i]]) < abs(f[w[i]] - f[w[i - 1]]) for i in range(1, len(w) - 1)), celik=A.gci(f3[2], f3[1], f3[0]))
b = {k: 1e-5 for k in ("S50", "S25A", "S12A", "S25B", "S12B")}
fails = 0
def chk(name, cond):
    global fails
    print(("PASS " if cond else "FAIL ") + name); fails += (not cond)
# 1 monotone, shrinking, finest 0.002 -> RULE1, U3D = GCI = 1.25*0.002/(2^1-1)
f = dict(S50=0.800, S25A=0.796, S12A=0.794); c = A.classify(f, b, None)
chk("RULE1 monotone, zone A only -> PROVISIONAL", c["rule"] == "RULE1_PROVISIONAL" and abs(c["U3D"] - 0.0025) < 1e-9 and "PROVISIONAL" in c["sentence"] and "would be a PASS" in c["sentence"] and "PASS, these settings" not in c["sentence"])
chk("RULE1 value", abs(c["U3D"] - 0.0025) < 1e-9); chk("zoneB required by the work order, not yet complete", c["zoneB_required_by_work_order"] and c["zoneB_complete"] is False)
# 2 shrinking but finest 0.0062 -> RULE1b, plain statement
f = dict(S50=0.830, S25A=0.812, S12A=0.8058); c = A.classify(f, b, None); chk("RULE1b, zone A only -> PROVISIONAL", c["rule"] == "RULE1b_PROVISIONAL" and "NO PASS" in c["sentence"] and "PROVISIONAL" in c["sentence"] and "PASS, these settings" not in c["sentence"])
# 3 non-monotone (oscillating) but shrinking in magnitude: e32 = +0.004, e21 = -0.002 -> shrinks, GCI not applicable -> finest pair used, still RULE1
f = dict(S50=0.800, S25A=0.796, S12A=0.798); c = A.classify(f, b, None); chk("RULE1 with GCI n/a uses finest", c["rule"] == "RULE1_PROVISIONAL" and abs(c["U3D"] - 0.002) < 1e-9 and "not applicable" in c["U3D_basis"])
# 4 flat 3D (finest = coarse pair), wedge clean -> RULE2 with the 3D finest pair
f = dict(S50=0.7960, S25A=0.7910, S12A=0.7860); w = wedge([0.79, 0.7930, 0.7938, 0.79405]); c = A.classify(f, b, w)
chk("RULE2, zone A only -> PROVISIONAL", c["rule"] == "RULE2_PROVISIONAL" and abs(c["U3D"] - 0.005) < 1e-9 and c["U3D_basis"] == "3D finest-pair difference" and c["wedge_clean"] is True and c["zoneB_required_by_work_order"] and "U3D >= 0.005" in c["sentence"] and "PROVISIONAL" in c["sentence"] and "PASS, these settings" not in c["sentence"])
# 5 flat 3D, wedge flat -> RULE3
w = wedge([0.79, 0.7930, 0.7900, 0.7935]); c = A.classify(f, b, w); chk("RULE3", c["rule"] == "RULE3" and c["U3D"] is None)
# 6 flat 3D, no wedge yet -> PENDING
c = A.classify(f, b, None); chk("PENDING_WEDGE", c["rule"] == "PENDING_WEDGE")
# 7 noise-limited: band 0.001 > 0.25*0.002 -> flat
bb = dict(b); bb["S12A"] = 0.001; f = dict(S50=0.800, S25A=0.796, S12A=0.794); c = A.classify(f, bb, wedge([0.79, 0.7930, 0.7938, 0.79405])); chk("noise-limited -> flat -> RULE2", c["rule"] == "RULE2_PROVISIONAL" and c["families"]["A"]["noise_limited"])
# 8 incomplete
c = A.classify(dict(S50=0.8, S25A=0.79), b, None); chk("INCOMPLETE", c["rule"] == "INCOMPLETE")
# 9 two families, both monotone shrinking; zone B has the larger finest pair (e21 = 0.0025, e32 = 0.005, e32/e21 = 2 > 1 -> p = 1) -> RULE1, U3D = zone B GCI21 = 1.25*0.0025/(2^1-1) = 0.003125 > zone A 0.0025
f = dict(S50=0.800, S25A=0.796, S12A=0.794, S25B=0.795, S12B=0.7925); c = A.classify(f, b, None); fB = c["families"]["B"]
eB21, eB32 = f["S25B"] - f["S12B"], f["S50"] - f["S25B"]; pB = abs(A.np.log(abs(eB32 / eB21))) / A.np.log(2); gB = 1.25 * abs(eB21) / (2 ** pB - 1)
chk("two families both monotone (e32/e21 > 1)", eB32 / eB21 > 1 and fB["celik"]["applicable"] and c["families"]["A"]["celik"]["applicable"] and fB["shrinks"] and not fB["noise_limited"])
chk("two families: max GCI from zone B, RULE1", c["rule"] == "RULE1" and c["U3D_zone"] == "B" and abs(c["U3D"] - gB) < 1e-12 and abs(gB - 0.003125) < 1e-12 and c["U3D_basis"] == "Celik GCI21")
chk("zone B complete -> plain RULE1 with PASS", c["zoneB_complete"] is True and "PASS, these settings become the study recipe." in c["sentence"] and "PROVISIONAL" not in c["sentence"])
# 10 E3: family() e21/e32 carry the Celik signs of gci()
chk("family e21/e32 signs = celik", abs(fB["e21"] - fB["celik"]["e21"]) < 1e-15 and abs(fB["e32"] - fB["celik"]["e32"]) < 1e-15 and abs(c["families"]["A"]["e21"] - 0.002) < 1e-12)
# 11 zone B complete, RULE1b and RULE2 stay plain (no PROVISIONAL)
f = dict(S50=0.830, S25A=0.812, S12A=0.8058, S25B=0.812, S12B=0.8058); c = A.classify(f, b, None); chk("RULE1b with zone B", c["rule"] == "RULE1b" and "PROVISIONAL" not in c["sentence"])
f = dict(S50=0.7960, S25A=0.7910, S12A=0.7860, S25B=0.7910, S12B=0.7860); c = A.classify(f, b, wedge([0.79, 0.7930, 0.7938, 0.79405])); chk("RULE2 with zone B", c["rule"] == "RULE2" and "PROVISIONAL" not in c["sentence"])
# 12 RULE3 / PENDING_WEDGE unchanged without zone B
f = dict(S50=0.7960, S25A=0.7910, S12A=0.7860); chk("RULE3 unchanged", A.classify(f, b, wedge([0.79, 0.7930, 0.7900, 0.7935]))["rule"] == "RULE3"); chk("PENDING unchanged", A.classify(f, b, None)["rule"] == "PENDING_WEDGE")

# --- settled gating (design v2.4)
f = dict(S50=0.800, S25A=0.796, S12A=0.794); b = {k: 1e-5 for k in ("S50", "S25A", "S12A", "S25B", "S12B")}
c = A.classify(f, b, None, {"S50": True, "S25A": True, "S12A": False}); chk("UNSETTLED 3D level -> rule UNSETTLED", c["rule"] == "UNSETTLED" and c["U3D"] is None and c["unsettled_levels"] == ["S12A"])
c = A.classify(f, b, None, {"S50": True, "S25A": True, "S12A": True}); chk("all settled -> normal classification", c["rule"].startswith("RULE1"))
fl = dict(S50=0.7960, S25A=0.7910, S12A=0.7860)
w = wedge([0.79, 0.7930, 0.7938, 0.79405]); c = A.classify(fl, b, w, {"S50": True, "S25A": True, "S12A": True, "W0": True, "W1": True, "W2": True, "W3": False})
chk("wedge finest three not settled -> undecided (PENDING_WEDGE), not RULE3", c["rule"] == "PENDING_WEDGE" and c["wedge_finest_three_settled"] is False)
c = A.classify(fl, b, w, {"S50": True, "S25A": True, "S12A": True, "W0": True, "W1": True, "W2": True, "W3": True}); chk("wedge settled and clean -> RULE2", c["rule"].startswith("RULE2"))

# --- audit opus_fix16 item 3: a level missing from settled is NOT settled; settled=None -> criterion not applied
f = dict(S50=0.800, S25A=0.796, S12A=0.794, S25B=0.795, S12B=0.7925)
c = A.classify(f, b, None, {"S50": True, "S25A": True, "S12A": True}); chk("zone B levels absent from settled -> UNSETTLED", c["rule"] == "UNSETTLED" and c["unsettled_levels"] == ["S12B", "S25B"])
chk("[control] settled=None -> criterion not applied (RULE1)", A.classify(f, b, None)["rule"] == "RULE1")
c = A.classify(fl, b, w, {"S50": True, "S25A": True, "S12A": True, "W0": True, "W1": True, "W2": True}); chk("wedge W3 absent from settled -> PENDING_WEDGE, not RULE2", c["rule"] == "PENDING_WEDGE" and c["wedge_finest_three_settled"] is False)

# --- audit opus_fix16 items 1, 2: level() on a synthetic case (A.U redirected to a temp dir)
import json, tempfile, numpy as np
def fake_case(root, n=600, end=None, t_out=None, nan_q=False, t_all=None):
    c = f"{root}/case_S50"; t = np.arange(1, n + 1, dtype=float) if t_all is None else t_all
    for name, col in (("measurementP", np.full(n, 9.0)), ("outletFlux", np.full(n, 1e-6)), ("throatFlux", np.full(n, 1e-6))):
        tc = t_out if (t_out is not None and name == "outletFlux") else t
        if nan_q and name == "throatFlux": col = col.copy(); col[-1] = np.nan
        os.makedirs(f"{c}/postProcessing/{name}/0", exist_ok=True); np.savetxt(f"{c}/postProcessing/{name}/0/surfaceFieldValue.dat", np.c_[tc, col], header="Time value")
    g = dict(cells=1000, strict_failed_checks=[], cells_across_throat_diameter=dict(median=40, min=30), **{"cell_size_um_x31.5_pm2mm": dict(p95=12.5)}, boundary_layer_um=dict(first_cell_median=5, first4_stack_median=25))
    json.dump(dict(mesh_gates=g, endTime=end if end is not None else n), open(f"{c}/build_info.json", "w"))
    json.dump(dict(verdict="CONVERGED", checks={}, mass_imbalance_pct=0.0, outlets=dict(outlet=dict(bc_err_pct=0.0))), open(f"{c}/analysis.json", "w"))
def try_level(**kw):
    root = tempfile.mkdtemp(); fake_case(root, **kw); U0 = A.U; A.U = root
    try: return A.level("S50")
    except SystemExit as e: return e
    finally: A.U = U0
r = try_level(t_out=np.arange(1, 601, dtype=float) * 2); chk("monitor iteration columns differ -> SystemExit naming level and files", isinstance(r, SystemExit) and "S50" in str(r) and "outletFlux" in str(r))
r = try_level(t_all=np.r_[np.arange(1, 600, dtype=float), 599.0]); chk("repeated iteration (same column in all monitors) -> SystemExit", isinstance(r, SystemExit) and "strictly increasing" in str(r))
r = try_level(nan_q=True); chk("NaN in the last 100 throat fluxes -> SystemExit", isinstance(r, SystemExit) and "non-finite" in str(r))
r = try_level(end=5000); chk("budget_iterations = build_info endTime, last_iteration = observed, budget_reached False", isinstance(r, dict) and r.get("budget_iterations") == 5000 and r.get("last_iteration") == 600 and r.get("budget_reached") is False and r["iterations"] == 600)
r = try_level(); chk("budget reached", isinstance(r, dict) and r.get("budget_reached") is True and r.get("budget_iterations") == 600)

# --- audit opus_fix16 item 4: main() wedge Celik only on consecutive W-levels with cell ratio ~4 (A.level stubbed)
def run_main(wl, cells, vals=(0.79, 0.7930, 0.7938, 0.79405)):
    fz = dict(S50=0.7960, S25A=0.7910, S12A=0.7860)
    stub = {l: dict(FFR_last100_mean=v, FFR_last100_band=1e-5, cells=1, verdict="CONVERGED", settled=True) for l, v in fz.items()}
    stub.update({l: dict(FFR_last100_mean=v, FFR_last100_band=1e-5, cells=n, verdict="CONVERGED", settled=True) for l, v, n in zip(wl, vals, cells)})
    L0 = A.level; A.level = lambda l: stub[l]; out = tempfile.mkstemp(suffix=".json")[1]
    try:
        import contextlib, io
        with contextlib.redirect_stdout(io.StringIO()): A.main(out, list(stub))
        return json.load(open(out))
    finally: A.level = L0
d = run_main(["W0", "W1", "W2", "W3"], [100, 400, 1600, 6400]); chk("[control] consecutive wedge x4 -> Celik applicable, RULE2", d["wedge"]["celik"]["applicable"] and d["classification"]["rule"] == "RULE2_PROVISIONAL")
d = run_main(["W0", "W1", "W3"], [100, 400, 6400], (0.79, 0.7930, 0.7938)); chk("non-consecutive wedge W1, W3 -> Celik not applicable, not wedge_clean", d["wedge"]["celik"]["applicable"] is False and "consecutive" in d["wedge"]["celik"]["reason"] and d["classification"]["wedge_clean"] is False)
d = run_main(["W0", "W1", "W2", "W3"], [100, 400, 1600, 3200]); chk("wedge cell ratio 2 -> Celik not applicable, not wedge_clean", d["wedge"]["celik"]["applicable"] is False and "ratio" in d["wedge"]["celik"]["reason"] and d["classification"]["wedge_clean"] is False)
print("FAILS", fails); sys.exit(fails)
