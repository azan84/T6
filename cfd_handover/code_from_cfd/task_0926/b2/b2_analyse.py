"""Task B2 analysis (work order 2026-09-26): solves per hour of the layouts L16 (one 16-rank job) and L8x2 (two 8-rank jobs side by side), both stopped at the B1 rule.
Reads b2/results_<layout>/{run_status.json,isolation_evidence.json} and each job's log.simpleFoam + monitors (b1_settle.analyse: the B1 criterion on the LAD-outlet pressure proxy, outlet-flow bands < 0.1 %, BC errors < 0.1 %).
Per job: iteration first settled (B1), wall clock to it = ClockTime printed after that step (includes process start-up: mesh read, field read) and the time-loop wall (ClockTime at that step minus ClockTime after step 1).
Throughput: L16 = 3600 / W (one solve per W s); L8x2 = 3600 / W_A + 3600 / W_B (two jobs run side by side, each repeated: the sum of their rates); 'paired' = 2 x 3600 / max(W_A, W_B).
Validity (audit 0926-SETUPS finding 4): layout_status VALID (layout_valid=True) only if run_status.json says controlled_end and isolation_evidence.json says contended == 'no' (strict; bindings are part of it).
layout_status CONDITIONALLY_COMPARABLE (layout_valid=False, valid_with_windows_background=True): the WSL2 Windows-background rule of audit 0926 finding 3 holds: controlled_end, bindings_verified,
no SMT sibling / bound CPU busy with non-owned work, every contended reason is Windows-side (WINDOWS_REASONS: pre-run load, its override, pre-run check unavailable, Windows non-WSL CPU over the run),
the Windows non-WSL CPU mean over the run is < WIN_BG_MAX (1.0) core and the two layouts' means differ by < WIN_SYM_MAX (0.3) core. Such a run is sensitivity evidence only (similar mean Windows load does not prove equal
temporal contention or Hyper-V core placement). Any Linux-side reason (non-owned Linux CPU, bound-CPU occupancy, no samples, bindings) or asymmetry: INVALID. The numbers are always written.
Ratio row: ratio_status VALID (valid=True) if both layouts are VALID; CONDITIONALLY_COMPARABLE (valid=False, sensitivity evidence only) if both are at least conditionally comparable; else NOT CLAIMED.
Order and host state (finding 6): every job row carries run_order (1/2 by launch_epoch of run_status.json), launch_time and host_load_at_start (host_before.txt); one replicate in one fixed order, see b2_design.md.
A job that does not settle within its budget is reported (settled=False, iterations_run = its last iteration); its layout's throughput is then empty with the note 'job X did not settle within N iterations'.
usage: b2_analyse.py <out.csv>"""
import os, sys, json, csv, re, time
P = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, P)
import b1_settle as B1
B = os.environ.get("B2_ROOT", f"{P}/b2")
WIN_BG_MAX, WIN_SYM_MAX = 1.0, 0.3            # cores: Windows non-WSL background tolerated over the run (mean) / max difference of the two layouts' means
WINDOWS_REASONS = ("Windows non-WSL CPU over the run over threshold", "windows pre-run load", "windows pre-run check ")     # prefixes of b2_isolation.py contended_reasons that are Windows-side only
LAYOUTS = {"L16": [("L16", f"{B}/L16/case")], "L8x2": [("L8x2_A", f"{B}/L8/caseA"), ("L8x2_B", f"{B}/L8/caseB")]}
def job(label, case):
    r = B1.analyse(label, "14", case, "out_600", "resistance", "B2 throughput measurement, scan 14 baseline")
    r["settled"] = r.get("status") == "ok" and r.get("iter_first_settled") is not None
    if r.get("status") != "ok": return r
    clk = B1.clock_table(case); n1 = clk.get(1, min(clk) if clk else None); ns = r.get("iter_first_settled")
    r["clock_after_step1_s"] = n1
    if ns is not None:
        r["wall_to_first_settled_incl_startup_s"] = r["wall_clock_to_first_settled_s"]; r["wall_to_first_settled_time_loop_s"] = clk[ns] - n1
    end = int(r["iterations_run"]); r["mean_s_per_iteration_101_to_end"] = (clk[end] - clk[101]) / (end - 101) if 101 in clk and end in clk else None
    return r
def win_mean(ev): return (((ev or {}).get("run_windows_nonwsl_cores")) or {}).get("mean")
def valid(layout):
    """(verdict, why, ev): verdict 'valid' (strict: contended no), 'windows_background' (candidate: only Windows-side reasons, mean < WIN_BG_MAX; symmetry decided in validity()), or 'invalid'."""
    d = f"{B}/results_{layout}"
    try: st = json.load(open(f"{d}/run_status.json")); ev = json.load(open(f"{d}/isolation_evidence.json"))
    except Exception as e: return "invalid", f"no run_status/isolation_evidence ({e})", None
    why = []
    if st.get("controlled_end") is not True: why.append(f"run did not end normally ({st.get('end_reason')}, bounded stop {st.get('bounded_stop')})")
    if ev.get("contended") == "no" and not why: return "valid", "", ev
    if ev.get("contended") == "no": return "invalid", "; ".join(why), ev
    rs = ev.get("contended_reasons") or []; other = [x for x in rs if not x.startswith(WINDOWS_REASONS)]; wm = win_mean(ev)
    why.append(f"contended={ev.get('contended')}: {rs}")
    if ev.get("bindings_verified") is not True: why.append("bindings not verified")
    if ev.get("sibling_of_bound_cpu_busy_with_nonowned_work") is not False: why.append(f"bound CPUs / SMT siblings busy or not measured ({ev.get('sibling_of_bound_cpu_busy_with_nonowned_work')})")
    if other or not rs: why.append(f"non-Windows reason(s): {other or 'none stated'}")
    if wm is None: why.append("Windows non-WSL CPU over the run not measured")
    elif wm >= WIN_BG_MAX: why.append(f"Windows non-WSL CPU mean over the run {wm} >= {WIN_BG_MAX} core")
    if len(why) == 1 and st.get("controlled_end") is True: return "windows_background", why[0], ev
    return "invalid", "; ".join(why), ev
CC = "CONDITIONALLY_COMPARABLE"
RATIO_CC = CC + " (sensitivity evidence only: Windows background load {w1}/{w2} cores, symmetric; for a batch-layout decision stop the Windows-side background or run an order-reversed replicate)"
def validity(res):
    """res: {layout: (verdict, why, ev)} -> {layout: (layout_valid, valid_with_windows_background, layout_status, note)}; the Windows-background rule needs both layouts' means within WIN_SYM_MAX."""
    ms = {l: win_mean(ev) for l, (_, _, ev) in res.items()}; out = {}
    for l, (v, why, ev) in res.items():
        if v == "valid": out[l] = (True, False, "VALID", "uncontended per isolation_evidence.json"); continue
        if v == "invalid": out[l] = (False, False, "INVALID", why); continue
        o = [ms.get(k) for k in res if k != l]
        if len(o) != 1 or o[0] is None: out[l] = (False, False, "INVALID", f"{why}; Windows background symmetry not verifiable (other layout's Windows mean missing)")
        elif abs(ms[l] - o[0]) >= WIN_SYM_MAX: out[l] = (False, False, "INVALID", f"{why}; Windows background asymmetric ({ms[l]} vs {o[0]} cores, difference >= {WIN_SYM_MAX})")
        else: out[l] = (False, True, CC, f"conditionally comparable (not VALID: contended={ev.get('contended')}): {why}; Windows non-WSL mean {ms[l]} core < {WIN_BG_MAX}, other layout {o[0]} (difference < {WIN_SYM_MAX})")
    return out, ms
def run_meta():
    """{layout: dict(run_order, launch_time, host_load_at_start)} from results_<layout>/run_status.json (launch_epoch) and host_before.txt ('load at start X')"""
    ep, out = {}, {}
    for l in LAYOUTS:
        d = f"{B}/results_{l}"; m = dict(run_order="", launch_time="", host_load_at_start="")
        try: ep[l] = int(json.load(open(f"{d}/run_status.json")).get("launch_epoch") or 0) or None
        except Exception: ep[l] = None
        if ep[l]: m["launch_time"] = time.strftime("%Y-%m-%d %H:%M:%S %z", time.localtime(ep[l]))
        try: x = re.search(r"load at start ([0-9.]+)", open(f"{d}/host_before.txt").read()); m["host_load_at_start"] = float(x.group(1)) if x else ""
        except Exception: pass
        out[l] = m
    for i, l in enumerate(sorted((l for l in ep if ep[l]), key=lambda l: ep[l])): out[l]["run_order"] = i + 1
    return out
if __name__ == "__main__":
    rows, per = [], {}
    res = {lay: valid(lay) for lay in LAYOUTS}; vd, wms = validity(res); meta = run_meta()
    for lay, jobs in LAYOUTS.items():
        ok, wbg, stat, why = vd[lay]; ev = res[lay][2]; js = [job(l, c) for l, c in jobs]; per[lay] = (ok, why, js)
        for r in js:
            r.update(layout=lay, ranks_per_job=(16 if lay == "L16" else 8), layout_status=stat, layout_valid=ok, valid_with_windows_background=wbg, layout_note=why, **meta[lay])
            if ev: r.update(windows_nonwsl_cores_mean=(ev.get("run_windows_nonwsl_cores") or {}).get("mean"), linux_nonowned_cores_mean=(ev.get("run_linux_nonowned_cores") or {}).get("mean"), contended_evidence=ev.get("contended"))
            rows.append(r)
    def W(js): return [j.get("wall_to_first_settled_incl_startup_s") for j in js]
    s, miss = {}, {}
    for lay, (ok, why, js) in per.items():
        w = W(js)
        miss[lay] = [f"job {j['case']} did not settle within {j.get('iterations_run', '?')} iterations" if j.get("status") == "ok" else f"job {j['case']}: {j.get('status')}" for j in js if not j.get("settled")]
        if any(x is None for x in w) or not w: s[lay] = None; miss[lay] = miss[lay] or ["no wall clock to the settle iteration"]; continue
        s[lay] = dict(rate=sum(3600.0 / x for x in w), paired=len(w) * 3600.0 / max(w), wall=w)
    out = []
    for lay in ("L16", "L8x2"):
        ok, wbg, stat, why = vd[lay]; base = dict(layout=lay, jobs=len(per[lay][2]), layout_status=stat, valid=ok, valid_with_windows_background=wbg, run_order=meta[lay]["run_order"])
        if s.get(lay): out.append(dict(base, wall_to_settle_s_each=" / ".join(str(x) for x in s[lay]["wall"]), solves_per_hour_sum_of_rates=round(s[lay]["rate"], 4), solves_per_hour_paired=round(s[lay]["paired"], 4), note=why))
        else: out.append(dict(base, wall_to_settle_s_each="", solves_per_hour_sum_of_rates="", solves_per_hour_paired="", note="; ".join(miss[lay] + [why])))
    st = [vd[l][2] for l in ("L16", "L8x2")]; w1, w2 = wms["L16"], wms["L8x2"]
    if st == ["VALID", "VALID"]:
        rstat = "VALID"; wnote = f"Windows background load {w1}/{w2} cores, symmetric" if None not in (w1, w2) else f"Windows background load {w1}/{w2} cores (not measured in both layouts)"
    elif all(x in ("VALID", CC) for x in st): rstat = RATIO_CC.format(w1=w1, w2=w2); wnote = "not VALID: " + "; ".join(f"{l} {vd[l][2]}" for l in ("L16", "L8x2") if vd[l][2] != "VALID")
    else: rstat = "NOT CLAIMED"; wnote = "not claimed: " + "; ".join(f"{l} {vd[l][2]} ({vd[l][3]})" for l in ("L16", "L8x2") if vd[l][2] == "INVALID")
    if s.get("L16") and s.get("L8x2"): out.append(dict(layout="ratio L8x2 / L16", solves_per_hour_sum_of_rates=round(s["L8x2"]["rate"] / s["L16"]["rate"], 4), solves_per_hour_paired=round(s["L8x2"]["paired"] / s["L16"]["paired"], 4),
                                                          valid=(rstat == "VALID"), ratio_status=rstat, note=wnote + ("" if rstat == "VALID" else " (VALID only if both layouts are VALID)")))
    else: out.append(dict(layout="ratio L8x2 / L16", solves_per_hour_sum_of_rates="", solves_per_hour_paired="", valid=False, ratio_status="NOT CLAIMED", note="not computed: " + "; ".join(miss["L16"] + miss["L8x2"])))
    cols = []
    for r in rows + out:
        for k in r:
            if k not in cols: cols.append(k)
    with open(sys.argv[1], "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows); w.writerows(out)
    for r in out: print(r)
