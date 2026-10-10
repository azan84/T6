#!/usr/bin/env python3
"""WO 2026-10-10 D15: pimpleFoam time-average fallback for a production steady solve that did NOT settle within the 3000-iteration budget.

README
------
TRIGGER (decided from the B1/D8 settle analysis, never from the FFR value): settle_<label>_<mode>.csv written by post_case_generic.sh step 7 (b1_settle.py --case, the B1 rule on measurementP; prescribed-flow:
the D8 variant with the 800-iteration floor). The steady solve is SETTLED iff that row has status ok, iterations_run equal to the budget (build_info endTime, 3000) and a non-empty iter_permanently_settled
(the full criterion (a)+(b)+(c) holds from some iteration up to the END of the run, so the returned end-of-budget value is a settled value). Otherwise it is NOT SETTLED and the fallback is run:
`pimple_fallback.py check <settle.csv> <steady_case>` prints the decision (exit 0 = fallback needed, 3 = settled, 2 = no decision possible); `build` refuses a settled solve unless --force-untriggered TEXT
is given (recorded in build_info.json, case marked NOT_FOR_PRODUCTION, never COMPLETE; used only by the smoke test).

usage: pimple_fallback.py check    <settle.csv> <steady_case>
       pimple_fallback.py build    <steady_case> <out_case> --settle <settle.csv> [--nproc N<=16] [--force-untriggered TEXT [--window-override-s T] [--zone-test id,id]]
       pimple_fallback.py resume-point <case> <nproc>   (wrapper step) consistency of processor*/ times, partial latest times moved aside, controlDict endTime = T_run of window_state.json, startFrom latestTime;
                                                         exit 0 = run needed (prints the start time), 10 = the run already stands at T_run, 1 = inconsistent (refused)
       pimple_fallback.py window   <case>               (wrapper step, after a run that reached T_run) stationarity decision: exit 0 STATIONARY, 10 EXTENDED (T_run += 25 % of T_decl, written to window_state.json
                                                         and controlDict), 11 NOT_STATIONARY_AT_CAP (final), 1 refused (run not at T_run)
       pimple_fallback.py analyse  <case> <out_dir> [--label L] [--steady-results M1_results.csv]      exit 0 = status COMPLETE, 6 = INCOMPLETE
       pimple_fallback.py make-job <steady_case> <Task> <name> [--priority P] [--ranks 16] [--jobs-dir D] [--ret-root R] (tests)  pool job jobs/<name>.json (atomic; no .audited marker) running fallback_job.sh
The run itself is ONLY done by the pool wrapper wo1010/fallback_job.sh <steady_case> <Task> <name> [ranks] (lock, disk gate, stale refusal, build, decomposePar, mpirun pimpleFoam, resume, window
extensions, analyse, purge); see its header. There is no direct `run` command any more (audit 2026-10-10 R2 Sol finding 4).

BUILD (from the FINISHED steady case; the steady case is only read):
  * mesh: constant/polyMesh hard-linked (cp -al; copy across filesystems), except `boundary`, which is COPIED (1 kB) so that no tool run in the transient case can rewrite the steady case's mesh files,
    and nothing is ever written into it; the section surfaces of PROBE MONITORS (B) go to the case's own constant/triSurface/;
  * initial fields: U, p, phi of the steady case's reconstructed latest time (== endTime, run_completion of log.simpleFoam ok) copied (not linked) as time 0;
  * inlet: unchanged totalPressure (the same p0) + pressureInletOutletVelocity, walls unchanged;
  * outlets, RESISTANCE mode: every outlet's p BC (lost 0-face outlets included, inert) replaced by the explicit-lag coded BC p = (Pv + R Q)/rho with Q = gSum(phi) of the patch at the moment the BC is
    evaluated and R = build_info R_used (= the R of the steady coded BC, cross-checked to 1e-8; Task G cases carry k*bc_A), WITHOUT the steady relaxation device (relax/prevIter belong to SIMPLE; the old
    ../build_pimple_case.py design; no code is imported from it). U outlets stay inletOutlet.
    PRESCRIBED mode: every live outlet keeps flowRateOutletVelocity with volumetricFlowRate = build_info Q_target_m3s written as a CONSTANT (a steady iteration ramp would be meaningless in physical time),
    p zeroGradient. The BC rewrite is done by OpenFOAM's changeDictionary (binary fields handled natively) and verified afterwards on the written 0/p, 0/U (binary-aware reader below).
  * numerics: pimpleFoam, ddt backward (2nd order), div(phi,U) Gauss linearUpwind grad(U) (the steady scheme without the steady-only 'bounded' wrapper), other schemes as the steady case; PIMPLE in PISO
    mode (nOuterCorrectors 1, nCorrectors 2, nNonOrthogonalCorrectors 1 = the steady value); p GAMG 1e-8/0.01, pFinal relTol 0; U smoothSolver 1e-9/0.1, UFinal relTol 0; adjustTimeStep yes, maxCo 0.8.
    The explicit lag is stable here: the inertial impedance of the outlet segment over one step, rho L/(A dt) ~ 1e12 Pa s/m3 at dt ~ 1e-5 s, exceeds every bc_A R (1e10-5e10) by > 10x.
  * controlDict: startFrom latestTime (a restart continues from the latest written time), endTime = T_run (window_state.json), writeInterval = T_decl/64 (adjustableRunTime: every T_run of the extension
    rule is a multiple of T_decl/8, hence a write time, and the run ends exactly on it), purgeWrite 2, binary.
  * monitors: the steady controlDict's `functions` block copied VERBATIM (inlet/outlet flux + area-average p, the BOUNDED throat and measurement planes throatFlux/throatP, measurementFlux/measurementP
    [, measurementOrig*], every time step, writeArea) PLUS the PROBE MONITORS below.

PROBE MONITORS (FFR at EVERY probe of the package's probes.csv, plus the relocated measurement probe <id>_reloc when the steady build relocated it): pr_<probe_id>P (areaAverage p) and pr_<probe_id>Flux
(areaNormalIntegrate U, sign along the probe normal), every time step, writeArea, on a plane through the probe point with the probes.csv normal, restricted to the probe's own lumen section by
  (A) bounded_box: the SAME sizing and mesh-check code as the steady builder (pf/probe_sections.py size_box + fit_and_check: axis-aligned box sized from r_ref_mm and the centreline, checked on the actual
      polyMesh: one connected section in the box, not clipped, no other vessel, area within [0.4, 2.5] pi r_own^2, centroid within 0.5 r_eq; shrink/grow rule) -> sampledPlane `bounds`; the lenient rule
      (the strict single-lumen rule S1/S2/S4 belongs to the measurement-probe choice, which the steady build already made: measurementP is copied verbatim); else, when the box cannot be sized (another
      vessel closer than h_min to the section: size_box ok = False) or fails the mesh check for every box tried,
  (B) section_surface: the connected section of the plane NEAREST the probe point (pyvista slice of the cells within max(3 mm, 6 r_own), the crop sphere grown until the section lies inside it;
      = the production M1_probes.py / sections.py definition of a probe section) is triangulated (triangles oriented along the probe normal, triangulated area == section area to 1e-6) and written
      as constant/triSurface/ps_<probe_id>.stl; the monitor samples it as a meshedSurface with source insideCells, interpolate false (every triangle takes the value of the cell containing its
      centre, i.e. of the cut cell, as the production section's cell data). Accepted only if the section is not clipped by the crop sphere and its area centroid is within 0.5 r_eq of the probe
      point = the validity rule of the production probe sections (sections.py section_ok); the area ratio to pi r_own^2 is recorded (area_outside_0p4_2p5), not judged: outlet probe sections are
      oblique/flared (14 out_826: 2.58 pi r_own^2, the SAME section as the production M1_probes row, 5.047 mm2). A `zone`-restricted sampledPlane is NOT used: in ESI v2406 a processor that holds
      no cell of the zone gets an empty selection and cuts its whole sub-mesh (cuttingPlane::performCut `if (cellCuts.size())`; seen in the R3B 4-rank smoke: 10.7 instead of 4.34 mm2).
      analyse refuses (reports missing) any monitored probe whose time-mean sampled area differs from the build-time checked section area by more than 1 %;
  (C) neither -> the probe is NOT monitored; build_info probe_monitors[<id>] records method 'none' and the reasons, and analyse reports it in FFR_probes_missing (never silently dropped).
  Measured feasibility (2026-10-10, real meshes): box (A) passes for 27/29 probes of 14_T1regen (p000: size_box clearance -1.8 mm, another vessel crosses the plane next to the proximal grid probe;
  out_826: area/clip at every box), 28/31 of 14_T5w (p000, p010 bif_dist clearance 1.33 < h_min 1.51 mm, out_868), 28/31 of 14_T5n (same three), 32/32 of P5 139 (+ none relocated); those go to (B).
  (B) takes out_826 / out_868 / p010; p000 of scan 14 (proximal grid probe, 2.3 mm from the inlet probe) stays (C): its plane cuts the merged lumen at the left-main bifurcation, the unclipped connected
  section (32.9 mm2, 3.2 pi r_own^2) has its centroid 0.96 r_eq off the probe, i.e. there is no single-lumen section there. The production M1_probes value of p000 (23.2 mm2, offset 0.48) is a section
  truncated by sections.py's crop sphere (3 r + 1.5 mm, no clip test), which this monitor does not reproduce. p000 FFR is ~0.998 (proximal; the steady value is in M1_probes); it is reported missing.

WINDOW (pre-declared, fixed at build time from the steady solve, recorded in build_info.json 'window' and window_state.json; extended ONLY by the stationarity rule below, never shortened):
  tau_jet  = L / U_t: L = distance between the throat-plane and the (used) measurement-plane centres (build_info planes), U_t = |throatFlux| / throat area (steady last-100 means of the bounded throat
             monitor): one flow-through of the post-stenotic region at the throat jet velocity (P5 baselines 17-25 ms); the shear layer / jet time scale.
  tau_slow = V_post / Q_post: the bulk turnover (residence) time of the post-stenotic region, the slow recirculation time scale. V_post = as-meshed lumen volume between the throat probe and the
             (used) measurement probe = integral of pi r(s)^2 ds along the package centreline path (probe_sections.vessel_path of the measurement node, from the throat node to the measurement node;
             r = r_target_mm, i.e. the lesioned lumen, where the package has it, else r_ref_mm) times the as-meshed area factor f_A = (steady bounded measurement-plane area) / (pi r(measurement)^2)
             (D10: the meshed lumen is wider than the package radius); Q_post = min(|throatFlux|, |measurementFlux|) (steady last-100 means; the smaller flow when a side branch leaves in between, i.e.
             the longer, conservative residence time). Why this definition: the recirculation zone downstream of the jet fills the post-stenotic segment and is renewed by the through-flow; V/Q is the
             time the through-flow needs to replace that volume once, it is computable from the package and the steady monitors alone, and it agrees with L / U_measurement (the 'tau_bulk' of the 1st
             version) within 5 % for P5 139 (179 vs 170 ms), while it also accounts for a non-uniform lumen. If the throat node is not on the measurement node's path (never seen), tau_slow falls back to
             L / U_measurement and the window records it.
  T_decl   = max(6 tau_jet, 1.5 tau_slow): at least six jet flow-throughs and one and a half slow turnovers. The FIRST HALF is wash-out of the steady initial state (>= 0.75 slow turnovers, >= 3 jet
             flow-throughs), the time average is taken over the SECOND HALF [T_run/2, T_run] (step-length weighted), T_run = T_decl at first.
  ACCEPTANCE (status COMPLETE) only if the window is STATIONARY: with Q3 = [T_run/2, 3 T_run/4] and Q4 = [3 T_run/4, T_run], |mean FFR_measurement(Q3) - mean FFR_measurement(Q4)| < U3D = 0.00055 AND for
             EVERY live outlet |mean Q(Q3) - mean Q(Q4)| < 0.5 % of |mean Q over [T_run/2, T_run]|.
  EXTENSION: not stationary -> T_run += 0.25 T_decl (the run continues from T_run; the averaging window becomes the second half of the new T_run, the quarters move with it), re-tested at the new T_run,
             up to the hard cap T_run = 2 T_decl. Still not stationary at the cap -> status INCOMPLETE (never COMPLETE), flag WINDOW_NOT_STATIONARY. Every test is logged in window_state.json 'history'.
  COST: dt = 0.8 dx / U_c with U_c ~ 4 U_t (R3B 4-rank smoke on P5 139: Courant-limited dt 3.94e-6 s, dx 25.5 um, U_t 1.30 m/s), hence
             steps(6 tau_jet) = 30 L / dx and steps(1.5 tau_slow) = 7.5 V_post / (A_throat dx): both independent of the flow, the second scales with 1/A_throat.
             Measured: 11.3 s/step on 4 ranks (P5 139, 4.14 M cells, all 33+2x2 probe monitors; median of steps 10-24). 16 ranks (not run: work-order cap 4 for tests): 2.8-3.3 s/step assuming
             4->16 efficiency 1.0-0.85 (returned steady runs scale linearly 8->16 ranks: 1.50 -> 0.74 s/iteration/M cells).
               P5 139 / 139_T1 (same lesion): 6 tau_jet 101.6 ms, 1.5 tau_slow 268 ms (binding) -> 68 k steps, ~54-63 h at 16 ranks; cap 2 T_decl: 137 k steps, ~105-126 h.
               scan 14 T5 narrow (throat r_target 0.151 mm, bounded throat section 0.102 mm2, V_post 88.7 mm3, L 29.8 mm, 3.52 M cells): 1.5 tau_slow = 44 tau_jet (binding) ->
               253 k steps (dx 25.8 um, throat-zone p95) to 470 k steps (13.9 um, median), i.e. ~170-370 h (7-15 days) at 16 ranks; cap 2 T_decl: 14-31 days.
  The build prints its estimate; `analyse` of any run prints projected_total_steps (T_decl and cap, from the rule value even under a test override) and the projected wall clock at the run's rank
  count from the measured dt and s/step. maxDeltaT = tau_jet/200, deltaT0 = maxDeltaT (pimpleFoam's setInitialDeltaT lowers it to maxCo at the start).
  TEST OVERRIDE: --window-override-s T (only together with --force-untriggered) replaces T_decl by T and writeInterval by T/8: NOT_FOR_PRODUCTION (resume/extension smoke tests only).

RESUME: a run stopped at any point (signal, crash, pool restart, reboot) is continued by re-running the same wrapper: `resume-point` keeps the latest time that is complete (U, p, phi, uniform/time
non-empty) in EVERY processor dir, moves later (partial) time dirs to <case>/_partial_<stamp>/processorN/ (outside the time search, nothing deleted), and pimpleFoam starts from it (startFrom latestTime);
the monitors of the new start write postProcessing/<name>/<t_start>/ and `analyse` lets a later start override the earlier samples of the same times; logs are rotated to log.pimpleFoam.<k>.
At most the time since the last write (<= T_decl/64) is recomputed.

ANALYSE: monitors of every postProcessing/<name>/<t0>/ (restarts: a later start overrides earlier samples of the same time), time averages WEIGHTED BY THE STEP LENGTH over [T_run/2, T_run]
(T_run from window_state.json), min/max band, std, the Q3/Q4 stationarity numbers, of: measurement FFR = measurementP rho / P_aorta (the used, possibly relocated, measurement plane; measurementOrigP too when
present), throat FFR = throatP rho / P_aorta, the FFR at every monitored probe, every outlet flow (and p, and the BC residual |p rho - (Pv + R Q)|/(Pv + R Q) in resistance mode), inlet flow and mass
imbalance, throat Reynolds number 4 rho |Q| / (pi mu D), D = 2 sqrt(A/pi) of the bounded throat monitor, max Courant number in the window (logs). Writes into <out_dir> (never overwriting: a differing file of
the same name gets a dated suffix, work order section 5):
  pimple_result_<L>_<M>.json  (the machine interface used by task_gate.py / taskG.py / finalise_task.py): status "COMPLETE" | "INCOMPLETE", steady_case (abs path), settle_decision, production_ready,
      outlets {outlet_id: time-averaged Q mL/s}, FFR {probe_id: time-averaged p rho / P_aorta}, FFR_Q_mls {probe_id: time-averaged through-plane flux}, FFR_probes_missing {probe_id: reason},
      FFR_measurement_mean, FFR_throat_mean, Re_throat_mean, flags, window, stationarity, analysed;
  pimple_result_<L>_<M>.csv (one row, flags column starts with PIMPLE_FALLBACK), pimple_outlets_<L>_<M>.csv, pimple_probes_<L>_<M>.csv, pimple_history_<L>_<M>.csv (every step),
  pimple_summary_<L>_<M>.json and, with --steady-results (the steady M1_results.csv of the same return), M1_results_pimple_<L>_<M>.csv = that row with converged 'PIMPLE_FALLBACK', flags + PIMPLE_FALLBACK,
  Re_throat and Q_inlet_mls replaced by the time averages and the window recorded in notes.
  status COMPLETE iff: window_state final == STATIONARY, the last log ends with End at T_run, production_ready (no forced trigger / window override), the recorded build trigger is NOT_SETTLED and
  every live outlet is monitored. Otherwise INCOMPLETE with flags: WINDOW_NOT_STATIONARY (cap reached), RUN_NOT_AT_T_RUN (stopped / still running), WINDOW_NOT_DECIDED, NOT_FOR_PRODUCTION,
  TRIGGER_NOT_MET, OUTLET_MONITOR_MISSING; PROBE_MONITOR_MISSING marks probes without FFR (FFR_probes_missing) without changing the status.
Blinding: constants from pf_common (RHO, MU, PV, P_AORTA_PA); no zerod_ffr / outlets_837 / 0D import anywhere in this code path."""
import sys, os, re, csv, json, glob, shutil, subprocess, math, datetime, hashlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(HERE); sys.path.insert(0, f"{P}/pf")
import pf_common as C
import post_helpers as H
S_AREA = (0.4, 2.5)      # probe_sections AREA_FACTOR (criterion (4)), also for the cell-zone sections

FOAM_ENV = "/usr/lib/openfoam/openfoam2406/etc/bashrc"
N_FT, MAXCO, SAMPLES_PER_TAU, MAX_RANKS, U3D = 6, 0.8, 200, 16, 0.00055
N_SLOW, EXT_FRAC, CAP_FRAC, Q_STAT_REL, WRITES_PER_DECL = 1.5, 0.25, 2.0, 0.005, 64      # window rule (README): T_decl = max(N_FT tau_jet, N_SLOW tau_slow); +25 % steps up to 2 T_decl; outlets 0.5 %
POOL_JOBS = "/home/azan/paper6_t6_work/wo1010_pool/jobs"; RET_ROOT = "/mnt/e/Paper6-T6/Paper6-T6/cfd_handover/returns/2026-10-10"; WRAPPER = os.path.join(HERE, "fallback_job.sh")
FLAG = "PIMPLE_FALLBACK"
HEAD = "FoamFile {{ version 2.0; format ascii; class {cls}; object {obj}; }}\n"

P_LAG = """    {patch}
    {{
        type            codedFixedValue;
        name            {cname};
        code
        #{{
            // D15 PIMPLE fallback: explicit-lag resistance outlet p = (Pv + R Q)/rho, Q = current patch flux; NO prevIter relaxation (that device belongs to SIMPLE)
            const scalar R     = {R:.8e};
            const scalar Pv    = {Pv};
            const scalar rho   = {rho};
            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            operator==((Pv + R*Q)/rho);
        #}};
    }}
"""
U_FLOW = "    {patch}\n    {{\n        type            flowRateOutletVelocity;\n        volumetricFlowRate constant {Q:.10e};\n    }}\n"

def foam(cmd, cwd, log):
    """run an OpenFOAM command line in cwd with the v2406 environment, output to cwd/log; returns the exit code"""
    r = subprocess.run(["bash", "-c", f"source {FOAM_ENV} >/dev/null 2>&1; [ \"$WM_PROJECT_VERSION\" = v2406 ] || exit 97; {cmd} > {log} 2>&1"], cwd=cwd)
    return r.returncode

# ---------------------------------------------------------------- settle decision
def settle_decision(settle_csv, steady_case):
    """(decision, detail): decision NOT_SETTLED (fallback needed), SETTLED, or NO_DECISION"""
    rows = list(csv.DictReader(open(settle_csv)))
    info = json.load(open(f"{steady_case}/build_info.json")); budget = int(float(info.get("endTime") or C.END_TIME))
    want = os.path.basename(os.path.normpath(steady_case)); r = [x for x in rows if x.get("case") == want] or (rows if len(rows) == 1 else [])
    if len(r) != 1: return "NO_DECISION", dict(reason=f"{settle_csv}: {len(rows)} rows, none/several for case {want}")
    r = r[0]; d = dict(settle_csv=os.path.abspath(settle_csv), case=r.get("case"), b1_label=r.get("b1_label"), status=r.get("status"), iterations_run=r.get("iterations_run"), budget=budget,
                       iter_first_settled=r.get("iter_first_settled"), iter_permanently_settled=r.get("iter_permanently_settled"), min_iterations_floor=r.get("min_iterations_floor"))
    if r.get("status") != "ok": return "NO_DECISION", dict(d, reason=f"settle row status {r.get('status')!r}")
    if not str(r.get("b1_label", "")).startswith("B1"): return "NO_DECISION", dict(d, reason=f"b1_label {r.get('b1_label')!r}: not the B1/D8 rule (no measurementP monitor)")
    if int(float(r["iterations_run"])) != budget: return "NO_DECISION", dict(d, reason=f"iterations_run {r['iterations_run']} != budget {budget}")
    if r.get("iter_permanently_settled"): return "SETTLED", dict(d, reason=f"B1 holds from iteration {r['iter_permanently_settled']} to the end of the budget")
    return "NOT_SETTLED", dict(d, reason=("B1 never held within the budget" if not r.get("iter_first_settled") else f"B1 first held at {r['iter_first_settled']} but does not hold at the end of the budget"))

# ---------------------------------------------------------------- binary-aware OpenFOAM field reader (dictionary text with the List<> blobs elided)
_LIST = re.compile(rb"List<(scalar|vector|symmTensor|tensor|sphericalTensor)>\s*(\d+)\s*\(")
_WIDTH = dict(scalar=1, vector=3, symmTensor=6, tensor=9, sphericalTensor=1)
def field_text(path):
    """ascii text of an OpenFOAM field file with every nonuniform List<...> body replaced by '<N values>'; binary bodies are skipped by length (N * width * 8 bytes), ascii bodies by parenthesis matching"""
    b = open(path, "rb").read(); binary = re.search(rb"format\s+binary\s*;", b[:2000]) is not None; out = []; i = 0
    while True:
        m = _LIST.search(b, i)
        if not m: out.append(b[i:]); break
        out.append(b[i:m.start()]); n = int(m.group(2)); j = m.end()
        if binary: j += n * _WIDTH[m.group(1).decode()] * 8
        else:
            depth = 1
            while depth: c = b[j:j + 1]; depth += (c == b"(") - (c == b")"); j += 1
            j -= 1
        if b[j:j + 1] != b")": raise SystemExit(f"{path}: List body of {n} values not closed at byte {j}")
        out.append(f"List<{m.group(1).decode()}> <{n} values>".encode()); i = j + 1
    return b"".join(out).decode("latin-1")

def patch_dicts(text):
    """{patch: body text} of boundaryField (brace matching)"""
    i = text.index("boundaryField"); i = text.index("{", i) + 1; out = {}
    while True:
        m = re.compile(r"\s*([A-Za-z0-9_\"().*|]+)\s*\{").match(text, i)
        if not m: break
        j = m.end(); depth = 1; k = j
        while depth:
            if text.startswith("#{", k): k = text.index("#}", k) + 2; continue
            depth += (text[k] == "{") - (text[k] == "}"); k += 1
        out[m.group(1)] = text[j:k - 1]; i = k
    return out

# ---------------------------------------------------------------- monitors
def load_mon(case, name):
    """(t, area or None, value) of postProcessing/<name>/*/surfaceFieldValue.dat, all start times; a later start overrides earlier samples of the same time"""
    def t0_of(f):
        try: return float(os.path.basename(os.path.dirname(f)))
        except ValueError: return None
    fs = sorted((f for f in glob.glob(f"{case}/postProcessing/{name}/*/surfaceFieldValue*.dat") if t0_of(f) is not None), key=lambda f: (t0_of(f), os.path.getmtime(f)))      # two starts at the same time: the later file wins
    T, A, V = [], [], []
    for f in fs:
        d = np.loadtxt(f, comments="#", ndmin=2)
        if not len(d): continue
        c = C.value_column(f); hdr = open(f).read(4000); has_area = re.search(r"^#\s*Time\s+Area", hdr, re.M) is not None
        t0 = float(os.path.basename(os.path.dirname(f)))
        if T: keep = [k for k in range(len(T)) if T[k] < t0]; T, A, V = [T[k] for k in keep], [A[k] for k in keep], [V[k] for k in keep]
        T += list(d[:, 0]); V += list(d[:, c]); A += list(d[:, 1]) if has_area else [np.nan] * len(d)
    if not T: return None
    return np.array(T), np.array(A), np.array(V)

def last_mean(case, name, n=100):
    m = load_mon(case, name)
    if m is None: raise SystemExit(f"{case}: monitor {name} missing")
    t, a, v = m; return float(np.mean(a[-n:])), float(np.mean(v[-n:]))

# ---------------------------------------------------------------- build
def latest_time(case):
    td = [x for x in H.time_dirs(case) if x[0] > 0]
    return td[-1] if td else None

def functions_block(control_text):
    i = re.search(r"^functions\s*\n?\s*\{", control_text, re.M)
    if not i: raise SystemExit("steady controlDict has no functions block")
    j = i.end(); depth = 1; k = j
    while depth: depth += (control_text[k] == "{") - (control_text[k] == "}"); k += 1
    return control_text[j:k - 1].strip("\n") + "\n"

def slow_time(pkg, info, Qt, Qm, Am, L, Um):
    """tau_slow = V_post / Q_post (README WINDOW): V_post = f_A * integral pi r(s)^2 ds along the measurement node's vessel path from the throat node to the measurement node, f_A = steady measurement-plane
    area / (pi r_meas^2), Q_post = min(|Q_throat|, |Q_measurement|). Returns a dict (falls back to L / U_measurement, recorded, if the throat node is not on that path)."""
    import probe_sections as S
    cl = pkg["centreline"]; tn = np.asarray(cl.point_data["tree_node"]); rf = S._radius_field(cl); r = np.asarray(cl.point_data[rf], float)
    pr = {p["probe_id"]: p for p in pkg["probes"]}
    mrow = pr.get(info.get("measurement_probe")); trow = pr.get(info.get("throat_probe"))
    if (info.get("measurement_probe_used") or "") != (info.get("measurement_probe") or ""):     # relocated measurement plane: its node from build_info
        rel = (info.get("measurement_probe_relocated") or {}).get("relocated") or {}; mnode = int(rel["tree_node"])
    else: mnode = int(mrow["tree_node"])
    mi = np.where(tn == mnode)[0]; ti = np.where(tn == int(trow["tree_node"]))[0]
    Qp = min(abs(Qt), abs(Qm)); d = dict(radius_field=rf, Q_post_m3s=Qp, measurement_tree_node=mnode, throat_tree_node=int(trow["tree_node"]))
    if len(mi) == 1 and len(ti) == 1:
        path, arc, k = S.vessel_path(cl, int(mi[0]))
        if int(ti[0]) in path[:k + 1]:
            j = path.index(int(ti[0])); seg = path[j:k + 1]; X = np.asarray(cl.points, float)[seg]; ds = np.linalg.norm(np.diff(X, axis=0), axis=1)
            A = np.pi * r[seg] ** 2; Vpkg = float(np.sum(0.5 * (A[1:] + A[:-1]) * ds)) * 1e-9; fA = Am / (np.pi * (r[int(mi[0])] * 1e-3) ** 2)
            V = Vpkg * fA
            return dict(d, tau_slow_s=V / Qp, definition="V_post / Q_post", V_post_m3=V, V_post_package_m3=Vpkg, area_factor_as_meshed=fA, path_arc_m=float(ds.sum()) * 1e-3, n_centreline_points=len(seg),
                        tau_slow_check_L_over_Umeas_s=L / Um)
    return dict(d, tau_slow_s=L / Um, definition="FALLBACK L / U_measurement (throat node not on the measurement node's centreline path)", tau_slow_check_L_over_Umeas_s=L / Um)

def window(steady, info, pkg, override=None):
    tp, mp = info.get("throat_plane"), info.get("measurement_plane")
    if not (tp and mp): raise SystemExit("steady build_info lacks throat_plane / measurement_plane (D8 template needed)")
    L = float(np.linalg.norm(np.array(tp["point_m"]) - np.array(mp["point_m"])))
    At, Qt = last_mean(steady, "throatFlux"); Am, Qm = last_mean(steady, "measurementFlux")
    Ut, Um = abs(Qt) / At, abs(Qm) / Am; tau = L / Ut
    sl = slow_time(pkg, info, Qt, Qm, Am, L, Um); ts = sl["tau_slow_s"]
    T = max(N_FT * tau, N_SLOW * ts); Tdecl = float(override) if override else T
    w = dict(L_throat_to_measurement_m=L, throat_area_m2=At, throat_Q_m3s=Qt, U_throat_ms=Ut, measurement_area_m2=Am, measurement_Q_m3s=Qm, U_measurement_ms=Um, tau_jet_s=tau, tau_slow_s=ts, tau_slow=sl,
             N_flowthrough=N_FT, N_slow=N_SLOW, T_rule_s=T, T_rule_binding=("6 tau_jet" if N_FT * tau >= N_SLOW * ts else "1.5 tau_slow"), T_decl_s=Tdecl, T_window_s=Tdecl,
             average="second half [T_run/2, T_run], step-length weighted", extension_step_s=EXT_FRAC * Tdecl, T_cap_s=CAP_FRAC * Tdecl,
             stationarity=f"|mean FFR_measurement(Q3) - mean(Q4)| < U3D {U3D} and every live outlet |mean Q(Q3) - mean Q(Q4)| < {Q_STAT_REL * 100:g} % of its second-half mean; Q3 = [T_run/2, 3T_run/4], Q4 = [3T_run/4, T_run]",
             maxDeltaT_s=tau / SAMPLES_PER_TAU, deltaT0_s=tau / SAMPLES_PER_TAU, writeInterval_s=Tdecl / (8 if override else WRITES_PER_DECL), maxCo=MAXCO,
             window_override_s=(float(override) if override else None), override_note=("NOT_FOR_PRODUCTION: T_decl replaced by --window-override-s (resume/extension smoke test)" if override else None),
             source="steady last-100 means of the bounded throatFlux / measurementFlux monitors (writeArea), plane centres from build_info, package centreline for V_post",
             rule=f"T_decl = max({N_FT} tau_jet, {N_SLOW} tau_slow), tau_jet = L/U_t, tau_slow = V_post/Q_post; average over the second half; COMPLETE only if stationary (Q3 vs Q4); else +{EXT_FRAC:g} T_decl up to {CAP_FRAC:g} T_decl, then INCOMPLETE WINDOW_NOT_STATIONARY; declared before the transient is run")
    dx = None
    mg = os.path.join(info.get("mesh_source_dir") or "", "mesh_gates.json")
    if os.path.exists(mg):
        g = json.load(open(mg)); v = g.get("cell_size_um_throat_pm2mm_arc")
        if isinstance(v, dict): v = v.get("p95") or v.get("median") or v.get("max")
        try: dx = float(v) * 1e-6
        except (TypeError, ValueError): dx = None
    w["throat_cell_m_for_estimate"] = dx
    w["estimated_steps_T_decl"] = (int(Tdecl * 4 * Ut / (MAXCO * dx)) if dx else None)
    w["estimated_steps_cap"] = (int(CAP_FRAC * Tdecl * 4 * Ut / (MAXCO * dx)) if dx else None)
    w["estimate_note"] = ("steps ~ T * U_c / (maxCo dx) with U_c = 4 U_t (calibrated on the 139 smoke run: dt 3.94e-6 s at maxCo 0.8, dx 25.5 um, U_t 1.30 m/s), dx = throat-zone cell size of the steady mesh "
                          "(mesh_gates.json); a rough estimate: `analyse` of a short run gives projected_total_steps from the measured dt")
    return w

# ---------------------------------------------------------------- probe monitors (README PROBE MONITORS)
def section_surface(checker, point_mm, normal, r_own_mm):
    """(B) the connected section of the plane nearest the probe (the production sections.py section, not clipped by the crop sphere), triangulated with every triangle oriented along the probe
    normal; returns dict(ok, tri=(points (n,3), triangles (m,3)), section_area_mm2, ..., fails)"""
    p = np.asarray(point_mm, float) * 1e-3; n = np.asarray(normal, float); n = n / np.linalg.norm(n)
    R = max(3e-3, 6 * r_own_mm * 1e-3); r = None
    for _ in range(4):
        ids = np.sort(np.asarray(checker.tree.query_ball_point(p, R), dtype=np.int64)); sub = checker.mesh.extract_cells(ids)
        sub.cell_data["oid"] = ids
        sl = sub.slice(normal=n, origin=p)
        if sl.n_cells == 0: return dict(ok=False, fails=["no_cut"], crop_radius_mm=R * 1e3)
        cn = sl.connectivity(extraction_mode="all"); rid = np.array(cn.cell_data["RegionId"], dtype=np.int64, copy=True)
        con = cn.compute_cell_sizes(length=False, area=True, volume=False); A = np.asarray(con.cell_data["Area"]); oid = np.asarray(con.cell_data["oid"], dtype=np.int64)
        own = int(rid[con.find_closest_cell(p)]); m = rid == own; ctr = np.asarray(con.cell_centers().points)
        far = float(np.max(np.linalg.norm(ctr[m] - p, axis=1)))
        hmax = float(np.cbrt(np.max(np.abs(np.asarray(checker.mesh.extract_cells(np.unique(oid[m])).compute_cell_sizes(length=False, area=False, volume=True).cell_data["Volume"])))))
        if far <= R - 2 * hmax: break
        R = max(R * 1.5, 1.5 * far + 2 * hmax)                       # clipped by the crop sphere: crop wider
    else: return dict(ok=False, fails=["clip"], crop_radius_mm=R * 1e3)
    Ab = float(A[m].sum()); cen = (ctr[m] * A[m, None]).sum(0) / Ab; req = np.sqrt(Ab / np.pi)
    r = dict(crop_radius_mm=R * 1e3, own_max_dist_mm=far * 1e3, section_area_mm2=Ab * 1e6, area_over_pi_r_own2=Ab / (np.pi * (r_own_mm * 1e-3) ** 2), r_eq_mm=req * 1e3,
             centroid_offset_over_req=float(np.linalg.norm(cen - p) / req), n_regions_local=int(rid.max() + 1))
    fails = []      # the production validity rule of sections.py / M1_probes (centroid within 0.5 r_eq) + not clipped; the area ratio is recorded, not judged (outlet sections are oblique/flared)
    r["area_outside_0p4_2p5"] = not (S_AREA[0] <= r["area_over_pi_r_own2"] <= S_AREA[1])
    if r["centroid_offset_over_req"] >= 0.5: fails.append("centroid")
    own_s = con.extract_cells(np.where(m)[0]).extract_surface(algorithm=None).triangulate().clean()
    P = np.asarray(own_s.points, float); F = np.asarray(own_s.faces).reshape(-1, 4)[:, 1:].copy()
    nt = np.cross(P[F[:, 1]] - P[F[:, 0]], P[F[:, 2]] - P[F[:, 0]]); flip = (nt @ n) < 0; F[flip] = F[flip][:, ::-1]
    At = 0.5 * np.linalg.norm(nt, axis=1); r["triangles"] = int(len(F)); r["triangulated_area_mm2"] = float(At.sum() * 1e6); r["n_cells_cut"] = int(len(np.unique(oid[m])))
    if abs(At.sum() - Ab) > 1e-6 * Ab: fails.append("triangulation_area")
    r.update(fails=fails, ok=not fails, tri=(P, F))
    return r

def write_stl(path, P, F, name):
    """ASCII STL (metres) of a triangulated section"""
    with open(path, "w") as fh:
        fh.write(f"solid {name}\n")
        for a, b, c in F:
            nn = np.cross(P[b] - P[a], P[c] - P[a]); nn = nn / (np.linalg.norm(nn) or 1.0)
            fh.write(f" facet normal {nn[0]:.9e} {nn[1]:.9e} {nn[2]:.9e}\n  outer loop\n" + "".join(f"   vertex {P[k][0]:.12e} {P[k][1]:.12e} {P[k][2]:.12e}\n" for k in (a, b, c)) + "  endloop\n endfacet\n")
        fh.write(f"endsolid {name}\n")

def probe_monitor_plan(pkg, info, poly, zone_force=()):
    """{probe_id: record} for every probes.csv probe (+ the relocated measurement probe): method bounded_box / section_surface / none (README PROBE MONITORS). zone_force: probe ids that get (B) IN ADDITION
    to (A) (test of the section-surface method against the box on the same plane; monitor names pz_<id>*)."""
    import probe_sections as S
    rows = [dict(p) for p in pkg["probes"]]
    rel = info.get("measurement_probe_relocated")
    if rel:
        rr = rel["relocated"]; rows.append(dict(probe_id=rr["probe_id"], kind="measurement_relocated", tree_node=str(rr["tree_node"]), x=rr["point_mm"][0], y=rr["point_mm"][1], z=rr["point_mm"][2],
                                                normal_x=rr["normal"][0], normal_y=rr["normal"][1], normal_z=rr["normal"][2], r_ref_mm=rr["r_ref_mm"]))
    ids = [r["probe_id"] for r in rows]
    if len(set(ids)) != len(ids) or not all(re.fullmatch(r"[A-Za-z0-9_]+", i) for i in ids): raise SystemExit(f"probe ids not unique / not OpenFOAM words: {ids}")
    checker = S.MeshChecker(S.load_mesh(poly)); cl = pkg["centreline"]; tn = np.asarray(cl.point_data["tree_node"]); rad = np.asarray(cl.point_data[S._radius_field(cl)], float); out = {}
    for row in rows:
        pid = row["probe_id"]; pt = [float(row["x"]), float(row["y"]), float(row["z"])]; nv = np.array([float(row[k]) for k in ("normal_x", "normal_y", "normal_z")]); nv = (nv / np.linalg.norm(nv)).tolist()
        rec = dict(probe_id=pid, kind=row["kind"], tree_node=row.get("tree_node"), point_m=(np.asarray(pt) * 1e-3).tolist(), normal=nv, r_ref_mm=float(row["r_ref_mm"]), reasons=[])
        try:
            sb = S.size_box(cl, row)
            if sb["ok"]:
                h, att = S.fit_and_check(checker, sb)
                if h is not None: rec.update(method="bounded_box", bounds_m=S.box_m(sb["point_mm"], h), h_mm=h, mesh_check={k: att[-1][k] for k in ("bounded_section_area_mm2", "bounded_area_over_pi_r_own2", "centroid_offset_over_req", "fails")})
                else: rec["reasons"].append(f"box mesh check failed for every box: {[(round(a['h_mm'], 3), a['fails']) for a in att]}")
            else: rec["reasons"].append(f"box sizing: {sb['reason']}")
        except SystemExit as e: rec["reasons"].append(f"box sizing: {e}")
        if rec.get("method") != "bounded_box" or pid in zone_force:
            i = np.where(tn == int(row["tree_node"]))[0] if str(row.get("tree_node", "")).lstrip("-").isdigit() else []
            r_own = float(rad[int(i[0])]) if len(i) == 1 else float(row["r_ref_mm"])
            z = section_surface(checker, pt, nv, r_own); zrec = {k: v for k, v in z.items() if k != "tri"}; zrec.update(r_own_mm=r_own)
            if pid in zone_force and rec.get("method") == "bounded_box":
                rec["zone_test"] = dict(zrec, surface=f"pz_{pid}.stl", tri=z.get("tri") if z["ok"] else None, monitors=[f"pz_{pid}P", f"pz_{pid}Flux"])
            elif z["ok"]: rec.update(method="section_surface", surface=f"ps_{pid}.stl", section_check=zrec, tri=z["tri"])
            else: rec.update(method="none"); rec["reasons"].append(f"section surface: {z['fails']} {zrec}")
        out[pid] = rec
    return out

def plane_fo(name, pt, nv, op, fld, bounds=None, surface=None):
    """surfaceFieldValue every time step, writeArea: on a bounded sampledPlane (as pf_common.surface_fo), or (surface = a constant/triSurface file) on the meshedSurface of a triangulated
    section sampled with source insideCells (each triangle takes the value of the cell containing its centre = the cut cell, as in the production sections). NOT a `zone`-restricted plane: in ESI
    v2406 an empty zone selection on a processor (cuttingPlane::performCut: `if (cellCuts.size())`) cuts that processor's whole sub-mesh (found by the R3B smoke, 10.7 instead of 4.34 mm2)."""
    if surface is not None:
        sd = f"            type meshedSurface; surface {surface}; source insideCells; interpolate false;\n"
    else:
        bl = f"            bounds ({bounds[0][0]:.9e} {bounds[0][1]:.9e} {bounds[0][2]:.9e}) ({bounds[1][0]:.9e} {bounds[1][1]:.9e} {bounds[1][2]:.9e});\n"
        sd = (f"            type plane; planeType pointAndNormal;\n            pointAndNormalDict {{ point ({pt[0]:.9e} {pt[1]:.9e} {pt[2]:.9e}); normal ({nv[0]:.9e} {nv[1]:.9e} {nv[2]:.9e}); }}\n{bl}"
              "            interpolate false;\n")
    return (f"    {name}\n    {{\n        type surfaceFieldValue; libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log false; writeArea true;\n"
            f"        regionType sampledSurface; name {name}Surf;\n        sampledSurfaceDict\n        {{\n{sd}        }}\n        operation {op}; fields ({fld});\n    }}\n")

def probe_functions(plan):
    """(functions text, {stl file name: (points, triangles)}) for the probe monitors"""
    s, zones = "", {}
    for pid, r in plan.items():
        pt = r["point_m"]; nv = r["normal"]
        if r["method"] == "bounded_box": s += plane_fo(f"pr_{pid}P", pt, nv, "areaAverage", "p", bounds=r["bounds_m"]) + plane_fo(f"pr_{pid}Flux", pt, nv, "areaNormalIntegrate", "U", bounds=r["bounds_m"])
        elif r["method"] == "section_surface":
            zones[r["surface"]] = r["tri"]; s += plane_fo(f"pr_{pid}P", pt, nv, "areaAverage", "p", surface=r["surface"]) + plane_fo(f"pr_{pid}Flux", pt, nv, "areaNormalIntegrate", "U", surface=r["surface"])
        zt = r.get("zone_test")
        if zt and zt.get("tri") is not None:
            zones[zt["surface"]] = zt["tri"]; s += plane_fo(f"pz_{pid}P", pt, nv, "areaAverage", "p", surface=zt["surface"]) + plane_fo(f"pz_{pid}Flux", pt, nv, "areaNormalIntegrate", "U", surface=zt["surface"])
    return s, zones

def build(steady, out, settle_csv=None, nproc=16, force=None, override=None, zone_force=()):
    steady = os.path.abspath(steady); out = os.path.abspath(out)
    if override and not force: raise SystemExit("--window-override-s is a test option: only together with --force-untriggered (NOT_FOR_PRODUCTION)")
    if zone_force and not force: raise SystemExit("--zone-test is a test option: only together with --force-untriggered (NOT_FOR_PRODUCTION)")
    if not 1 <= nproc <= MAX_RANKS: raise SystemExit(f"nproc {nproc}: 1..{MAX_RANKS} (work order rank cap)")
    if os.path.exists(out): raise SystemExit(f"{out} exists (never overwritten)")
    info = json.load(open(f"{steady}/build_info.json")); mode = info.get("mode")
    if mode not in ("resistance", "prescribed"): raise SystemExit(f"steady mode {mode!r}: resistance or prescribed only")
    ok, rc = H.run_completion(steady)
    if not ok: raise SystemExit(f"steady solve not finished (run_completion of log.simpleFoam): {rc['fails']}")
    lt = latest_time(steady); end = float(info.get("endTime") or C.END_TIME)
    if not lt or abs(lt[0] - end) > 1e-9: raise SystemExit(f"latest reconstructed time {lt} != endTime {end}: run reconstructPar -latestTime first (post_case_generic step 2)")
    src_t = f"{steady}/{lt[1]}"
    for f in ("U", "p", "phi"):
        if not (os.path.exists(f"{src_t}/{f}") and os.path.getsize(f"{src_t}/{f}") > 0): raise SystemExit(f"{src_t}/{f} missing or empty")
    if settle_csv:
        dec, det = settle_decision(settle_csv, steady)
    else: dec, det = "NO_DECISION", dict(reason="no --settle csv given")
    if dec != "NOT_SETTLED" and not force: raise SystemExit(f"trigger not met: settle decision {dec} ({det.get('reason')}); the fallback runs only for a NOT SETTLED steady solve (--force-untriggered TEXT for tests)")
    # steady p BCs: R of every coded outlet (cross-check with build_info)
    pt = patch_dicts(field_text(f"{src_t}/p")); ut = patch_dicts(field_text(f"{src_t}/U"))
    live, lost = list(info.get("outlets", [])), list(C.lost_outlets(info))
    outs = live + [o for o in lost if o["patch"] not in {x["patch"] for x in live}]
    for o in outs:
        if o["patch"] not in pt: raise SystemExit(f"outlet {o['patch']} not in the steady p boundaryField")
        if mode == "resistance":
            m = re.search(r"const scalar R\s*=\s*([0-9.eE+-]+);", pt[o["patch"]])
            if not m or abs(float(m.group(1)) - o["R_used"]) > 1e-8 * o["R_used"]: raise SystemExit(f"{o['patch']}: steady coded R {m and m.group(1)} != build_info R_used {o['R_used']}")
    import m1_package as M
    pkg = M.load_package(info["package"]); mis = M.verify_against_build(pkg["dir"], info)
    if mis: raise SystemExit(f"package {pkg['dir']} differs from the one the steady case was built with: {mis}")
    w = window(steady, info, pkg, override)
    plan = probe_monitor_plan(pkg, info, f"{steady}/constant/polyMesh", zone_force)
    # ---- case
    os.makedirs(f"{out}/constant"); os.makedirs(f"{out}/system"); os.makedirs(f"{out}/0")
    how = C.link_or_copy(f"{steady}/constant/polyMesh", f"{out}/constant/polyMesh")
    b = f"{out}/constant/polyMesh/boundary"; os.unlink(b); shutil.copy2(f"{steady}/constant/polyMesh/boundary", b)       # private copy: never rewrite the steady mesh through a link
    pfo, zones = probe_functions(plan)
    if zones:
        os.makedirs(f"{out}/constant/triSurface")
        for fn, (Pt, Ft) in zones.items(): write_stl(f"{out}/constant/triSurface/{fn}", Pt, Ft, fn[:-4])
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy2(f"{steady}/constant/{f}", f"{out}/constant/{f}")
    for f in ("U", "p", "phi"): shutil.copy2(f"{src_t}/{f}", f"{out}/0/{f}")
    for f in ("U", "p", "phi"):
        if os.path.samefile(f"{src_t}/{f}", f"{out}/0/{f}"): raise SystemExit("field copy is a link")
    fs = open(f"{steady}/system/fvSchemes").read()
    fs2, n1 = re.subn(r"(ddtSchemes\s*\{\s*default\s+)steadyState\s*;", r"\1backward;", fs); fs2, n2 = re.subn(r"(?m)^(\s*div\([^\n/]*?)bounded\s+Gauss", r"\1Gauss", fs2)      # scheme lines only, not comments
    if n1 != 1 or n2 < 1: raise SystemExit(f"steady fvSchemes not in the expected form (ddt steadyState: {n1}, bounded Gauss: {n2})")
    open(f"{out}/system/fvSchemes", "w").write(fs2)
    open(f"{out}/system/fvSolution", "w").write(HEAD.format(cls="dictionary", obj="fvSolution") + """solvers
{
    p      { solver GAMG; smoother GaussSeidel; tolerance 1e-08; relTol 0.01; }
    pFinal { $p; relTol 0; }
    U      { solver smoothSolver; smoother symGaussSeidel; tolerance 1e-09; relTol 0.1; }
    UFinal { $U; relTol 0; }
}
PIMPLE { momentumPredictor yes; nOuterCorrectors 1; nCorrectors 2; nNonOrthogonalCorrectors 1; }
""")
    fo = functions_block(open(f"{steady}/system/controlDict").read())
    ctl = (HEAD.format(cls="dictionary", obj="controlDict") + f"application     pimpleFoam;\nstartFrom       latestTime;\nstartTime       0;\nstopAt          endTime;\nendTime         {w['T_decl_s']:.12g};\n"
           f"deltaT          {w['deltaT0_s']:.6g};\nadjustTimeStep  yes;\nmaxCo           {MAXCO};\nmaxDeltaT       {w['maxDeltaT_s']:.6g};\nwriteControl    adjustableRunTime;\nwriteInterval   {w['writeInterval_s']:.12g};\n"
           "purgeWrite      2;\nwriteFormat     binary;\nwritePrecision  12;\nwriteCompression off;\ntimeFormat      general;\ntimePrecision   12;\nrunTimeModifiable false;\n\nfunctions\n{\n" + fo + pfo + "}\n")
    open(f"{out}/system/controlDict", "w").write(ctl)
    open(f"{out}/system/decomposeParDict", "w").write(HEAD.format(cls="dictionary", obj="decomposeParDict") + f"numberOfSubdomains {nproc};\nmethod scotch;\n")
    # ---- outlet BCs through changeDictionary
    if mode == "resistance":
        ent = "".join(P_LAG.format(patch=o["patch"], cname=o.get("code_name") or "res" + o["patch"].split("_", 1)[1], R=o["R_used"], Pv=C.PV, rho=C.RHO) for o in outs)
        cd = "p\n{\n    boundaryField\n    {\n" + ent + "    }\n}\n"
    else:
        cd = "U\n{\n    boundaryField\n    {\n" + "".join(U_FLOW.format(patch=o["patch"], Q=o["Q_target_m3s"]) for o in live) + "    }\n}\n"
    open(f"{out}/system/changeDictionaryDict", "w").write(HEAD.format(cls="dictionary", obj="changeDictionaryDict") + cd)
    if foam("changeDictionary -time 0", out, "log.changeDictionary") != 0: raise SystemExit(f"changeDictionary failed (see {out}/log.changeDictionary)")
    if not filecmp_same(f"{out}/constant/polyMesh/boundary", f"{steady}/constant/polyMesh/boundary"): raise SystemExit("constant/polyMesh/boundary changed by changeDictionary (private copy; steady mesh untouched)")
    ver = verify_bcs(out, mode, live, outs, info)
    if os.path.exists(f"{steady}/zerod_reference.json"): shutil.copy2(f"{steady}/zerod_reference.json", f"{out}/zerod_reference.json")
    open(f"{out}/case.foam", "w").close()
    pm = {k: {x: y for x, y in v.items() if x != "tri"} for k, v in plan.items()}
    for v in pm.values():
        if v.get("zone_test"): v["zone_test"] = {x: y for x, y in v["zone_test"].items() if x != "tri"}
    binfo = dict(case=os.path.basename(out), family="m1_pimple_fallback", flag=FLAG, mode=mode, stage=mode, steady_case=steady, steady_time=lt[1], steady_build_info=info, endTime=w["T_decl_s"],
                 probe_monitors=pm, probe_monitor_counts={m: sum(v["method"] == m for v in plan.values()) for m in ("bounded_box", "section_surface", "none")}, zone_test=list(zone_force) or None,
                 nproc=nproc, mesh_link=how + " (boundary copied)", window=w, trigger=dict(decision=dec, **det), forced_untriggered=force, production_ready=not (force or override),
                 outlets=live, outlets_lost_in_mesh=lost, throat_plane=info.get("throat_plane"), measurement_plane=info.get("measurement_plane"), extra_planes=info.get("extra_planes"),
                 measurement_probe=info.get("measurement_probe"), measurement_probe_used=info.get("measurement_probe_used") or info.get("measurement_probe"), throat_probe=info.get("throat_probe"),
                 package=info.get("package"), instance=info.get("instance"), error_type=info.get("error_type"), label=info.get("label"), r_scale_k=info.get("r_scale_k", 1.0),
                 numerics=dict(solver="pimpleFoam", ddt="backward", divU="Gauss linearUpwind grad(U)", pimple="nOuterCorrectors 1, nCorrectors 2, nNonOrthogonalCorrectors 1", maxCo=MAXCO),
                 bc=("explicit-lag coded p = (Pv + R Q)/rho on every outlet (no relaxation), R = build_info R_used" if mode == "resistance" else "flowRateOutletVelocity constant Q_target_m3s on every live outlet, p zeroGradient"),
                 bc_verification=ver, blinding="pf_common constants only; no zerod_ffr / outlets_837 / 0D import", built=datetime.datetime.now().isoformat(timespec="seconds"),
                 builder_sha256=hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest())
    write_state(out, dict(T_decl_s=w["T_decl_s"], T_run_s=w["T_decl_s"], extension_step_s=w["extension_step_s"], T_cap_s=w["T_cap_s"], final=None, history=[], created=binfo["built"]))
    if force: open(f"{out}/NOT_FOR_PRODUCTION", "w").write(f"built with --force-untriggered: {force}\nsettle decision: {dec} ({det.get('reason')})\n" + (f"window override: T_decl = {override} s\n" if override else ""))
    json.dump(binfo, open(f"{out}/build_info.json.tmp", "w"), indent=1, default=str); os.replace(f"{out}/build_info.json.tmp", f"{out}/build_info.json")      # last: build_info.json marks a finished build
    print(f"built {out} ({mode}) from {steady} time {lt[1]}: trigger {dec} ({det.get('reason')}){' FORCED: ' + force if force else ''}; T_decl = {w['T_decl_s']*1e3:.2f} ms = max({N_FT} x tau_jet "
          f"{w['tau_jet_s']*1e3:.2f} ms (L {w['L_throat_to_measurement_m']*1e3:.2f} mm, U_t {w['U_throat_ms']:.3f} m/s), tau_slow {w['tau_slow_s']*1e3:.1f} ms ({w['tau_slow']['definition']}); binding {w['T_rule_binding']}"
          f"{'; OVERRIDE T_decl ' + str(override) + ' s (NOT_FOR_PRODUCTION)' if override else ''}; cap {w['T_cap_s']*1e3:.2f} ms, writeInterval {w['writeInterval_s']:.4g} s, maxDeltaT {w['maxDeltaT_s']:.3g} s, "
          f"est. steps {w['estimated_steps_T_decl']} (cap {w['estimated_steps_cap']}); probe monitors {binfo['probe_monitor_counts']}; BCs verified: {ver['summary']}")
    return binfo

def filecmp_same(a, b): return open(a, "rb").read() == open(b, "rb").read()

def verify_bcs(case, mode, live, outs, info):
    pt = patch_dicts(field_text(f"{case}/0/p")); ut = patch_dicts(field_text(f"{case}/0/U")); fails = []; rec = {}
    st = info["p0_kin"]
    inl = pt.get("inlet", "")
    if "totalPressure" not in inl or not re.search(r"p0\s+uniform\s+([0-9.eE+-]+)", inl) or abs(float(re.search(r"p0\s+uniform\s+([0-9.eE+-]+)", inl).group(1)) - st) > 1e-5 * st: fails.append("inlet not totalPressure with the steady p0")
    if "pressureInletOutletVelocity" not in ut.get("inlet", ""): fails.append("inlet U not pressureInletOutletVelocity")
    for o in outs:
        p_, u_ = (re.sub(r"//[^\n]*", "", x) for x in (pt.get(o["patch"], ""), ut.get(o["patch"], "")))      # code comments are not code
        if mode == "resistance":
            m = re.search(r"const scalar R\s*=\s*([0-9.eE+-]+);", p_)
            okp = "codedFixedValue" in p_ and m and abs(float(m.group(1)) - o["R_used"]) <= 1e-8 * o["R_used"] and "relax" not in p_ and "prevIter" not in p_ and "operator==((Pv + R*Q)/rho)" in p_
            oku = "inletOutlet" in u_
            rec[o["patch"]] = dict(p="explicit-lag coded" if okp else "WRONG", R=float(m.group(1)) if m else None, U="inletOutlet" if oku else "WRONG")
            if not (okp and oku): fails.append(f"{o['patch']}: p/U BC not as specified")
        else:
            if o in live:
                m = re.search(r"volumetricFlowRate\s+constant\s+([0-9.eE+-]+);", u_)
                oku = "flowRateOutletVelocity" in u_ and m and abs(float(m.group(1)) - o["Q_target_m3s"]) <= 1e-9 * abs(o["Q_target_m3s"])
                okp = "zeroGradient" in p_
                rec[o["patch"]] = dict(U="flowRateOutletVelocity constant" if oku else "WRONG", Q=float(m.group(1)) if m else None, p="zeroGradient" if okp else "WRONG")
                if not (oku and okp): fails.append(f"{o['patch']}: U/p BC not as specified")
    if fails: raise SystemExit(f"BC verification FAILED in {case}/0: {fails}")
    return dict(ok=True, patches=rec, summary=f"{len(rec)} outlet(s) {'explicit-lag coded p' if mode == 'resistance' else 'flowRateOutletVelocity constant'}, inlet totalPressure p0 {st:.6f}")

# ---------------------------------------------------------------- window state, resume point, stationarity decision (wrapper steps)
def read_state(case):
    return json.load(open(f"{case}/window_state.json"))

def write_state(case, st):
    tmp = f"{case}/.window_state.json.tmp"
    with open(tmp, "w") as fh: json.dump(st, fh, indent=1, default=str); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, f"{case}/window_state.json")

def set_control(case, T_run):
    """controlDict: endTime = T_run, startFrom latestTime (atomic rewrite; verified)"""
    f = f"{case}/system/controlDict"; t = open(f).read()
    t2, n1 = re.subn(r"(?m)^endTime\s+[^;\n]+;", f"endTime         {T_run:.12g};", t); t2, n2 = re.subn(r"(?m)^startFrom\s+[^;\n]+;", "startFrom       latestTime;", t2)
    if n1 != 1 or n2 != 1: raise SystemExit(f"{f}: endTime/startFrom lines not found exactly once ({n1}, {n2})")
    if t2 != t: open(f + ".tmp", "w").write(t2); os.replace(f + ".tmp", f)
    m = re.search(r"(?m)^endTime\s+([^;\n]+);", open(f).read())
    if not m or abs(float(m.group(1)) - T_run) > 1e-9 * T_run: raise SystemExit(f"{f}: endTime not set to {T_run}")

def same_time(a, b): return abs(a - b) <= 1e-6 * max(abs(a), abs(b), 1e-30)

def resume_point(case, nproc):
    """README RESUME. Returns (code, info): 0 run needed from info['start'], 10 latest == T_run (nothing to run). Raises SystemExit (exit 1) on an inconsistent case."""
    case = os.path.abspath(case); st = read_state(case); T = float(st["T_run_s"])
    procs = sorted(glob.glob(f"{case}/processor[0-9]*"), key=lambda d: int(re.sub(r"\D", "", os.path.basename(d))))
    if len(procs) != nproc or [os.path.basename(d) for d in procs] != [f"processor{i}" for i in range(nproc)]: raise SystemExit(f"{case}: {len(procs)} processor dirs, expected processor0..{nproc - 1}")
    def complete(d, t):
        need = ("U", "p", "phi") + (() if t[0] == 0 else ("uniform/time",))
        return all(os.path.isfile(f"{d}/{t[1]}/{f}") and os.path.getsize(f"{d}/{t[1]}/{f}") > 0 for f in need)
    per = [H.time_dirs(d) for d in procs]
    common = None
    for t in sorted({x[0] for x in per[0]}, reverse=True):
        names = [[y for y in pt if same_time(y[0], t)] for pt in per]
        if all(len(n) == 1 and complete(d, n[0]) for d, n in zip(procs, names)): common = t; break
    if common is None: raise SystemExit(f"{case}: no time is complete in every processor dir (not even 0): decomposition broken, refused")
    if common > T * (1 + 1e-6): raise SystemExit(f"{case}: latest complete time {common} is beyond T_run {T} of window_state.json: inconsistent, refused")
    moved = []
    later = [(d, x) for d, pt in zip(procs, per) for x in pt if x[0] > common and not same_time(x[0], common)]
    if later:
        dst = f"{case}/_partial_{datetime.datetime.now().strftime('%Y%m%dT%H%M%S')}"
        for d, x in later:
            os.makedirs(f"{dst}/{os.path.basename(d)}", exist_ok=True); shutil.move(f"{d}/{x[1]}", f"{dst}/{os.path.basename(d)}/{x[1]}"); moved.append(f"{os.path.basename(d)}/{x[1]}")
    # disk: purgeWrite only purges the times written by the CURRENT segment; older checkpoints of earlier segments are pruned here, keeping 0 and the two latest times complete in every processor
    full = sorted(t for t in {x[0] for x in per[0]} if t <= common and all(any(same_time(y[0], t) and complete(d, y) for y in pt) for d, pt in zip(procs, per)))
    keep = set(full[-2:]) | {0.0}; pruned = []
    for d, pt in zip(procs, per):
        for x in pt:
            if x[0] > 0 and x[0] < min(full[-2:]) and not any(same_time(x[0], k) for k in keep) and x[0] in full:
                shutil.rmtree(f"{d}/{x[1]}"); pruned.append(f"{os.path.basename(d)}/{x[1]}")
    set_control(case, T)
    info = dict(start=common, T_run=T, moved_aside=moved, pruned_old_checkpoints=sorted(set(p.split("/")[1] for p in pruned), key=float), final=st.get("final"))
    return (10 if same_time(common, T) else 0), info

def stationarity(case, T):
    """Q3/Q4 test over the second half of [0, T] (README ACCEPTANCE); returns dict(ok, ...)"""
    bi = json.load(open(f"{case}/build_info.json")); lo, q, hi = T / 2, 3 * T / 4, T; pa = C.P_AORTA_PA; r = dict(T_run_s=T, Q3=[lo, q], Q4=[q, hi]); fails = []
    m = load_mon(case, "measurementP")
    if m is None: raise SystemExit(f"{case}: no measurementP history")
    a3, a4 = tavg(m[0], m[2] * C.RHO / pa, lo, q), tavg(m[0], m[2] * C.RHO / pa, q, hi)
    if not (a3["n"] and a4["n"]): raise SystemExit(f"{case}: no measurementP samples in a quarter of [{lo}, {hi}]")
    d = a4["mean"] - a3["mean"]; r.update(FFR_measurement_Q3=a3["mean"], FFR_measurement_Q4=a4["mean"], FFR_measurement_diff=d, FFR_ok=abs(d) < U3D)
    if not abs(d) < U3D: fails.append(f"FFR_measurement |Q4 - Q3| = {abs(d):.6f} >= U3D {U3D}")
    ro = {}
    for o in bi["outlets"]:
        mo = load_mon(case, f"{o['patch']}Flux")
        if mo is None: fails.append(f"{o['patch']}: no flux monitor"); continue
        b3, b4, bh = tavg(mo[0], mo[2], lo, q), tavg(mo[0], mo[2], q, hi), tavg(mo[0], mo[2], lo, hi)
        rel = abs(b4["mean"] - b3["mean"]) / abs(bh["mean"]) if bh["mean"] else float("inf")
        ro[o["patch"]] = dict(Q3_mls=b3["mean"] * 1e6, Q4_mls=b4["mean"] * 1e6, rel_diff=rel, ok=rel < Q_STAT_REL)
        if not rel < Q_STAT_REL: fails.append(f"{o['patch']} |Q4 - Q3| / Q = {rel * 100:.3f} % >= {Q_STAT_REL * 100:g} %")
    r.update(outlets=ro, fails=fails, ok=not fails); return r

def window_decide(case):
    """after a run that reached T_run: 0 STATIONARY, 10 EXTENDED (state + controlDict updated), 11 NOT_STATIONARY_AT_CAP; SystemExit if the run is not at T_run"""
    case = os.path.abspath(case); st = read_state(case)
    if st.get("final"): return {"STATIONARY": 0, "NOT_STATIONARY_AT_CAP": 11}[st["final"]], st
    T = float(st["T_run_s"]); p0 = H.time_dirs(f"{case}/processor0") if os.path.isdir(f"{case}/processor0") else H.time_dirs(case)
    if not p0 or not same_time(p0[-1][0], T): raise SystemExit(f"{case}: latest time {p0[-1][1] if p0 else None} != T_run {T}: the run has not reached T_run")
    lg = log_info(case)
    if not lg["complete"]: raise SystemExit(f"{case}: the last log.pimpleFoam does not end with End after its last Time line")
    r = stationarity(case, T); r["decided"] = datetime.datetime.now().isoformat(timespec="seconds"); st["history"].append(r)
    cap = float(st["T_cap_s"]); step = float(st["extension_step_s"])
    if r["ok"]: st["final"] = "STATIONARY"; code = 0
    elif T + step <= cap * (1 + 1e-9): r["decision"] = f"EXTEND to {T + step:.12g} s"; st["T_run_s"] = T + step; code = 10
    else: st["final"] = "NOT_STATIONARY_AT_CAP"; code = 11
    r.setdefault("decision", st["final"]); write_state(case, st)
    if code == 10: set_control(case, st["T_run_s"])
    return code, st

# ---------------------------------------------------------------- analyse
def tavg(t, v, a, b):
    """step-length weighted mean over samples with a < t <= b (each sample = the state at the end of its step); also min, max, std, n"""
    dt = np.diff(np.concatenate([[t[0] - (t[1] - t[0]) if len(t) > 1 else 0.0], t]))
    k = (t > a) & (t <= b)
    if not k.any(): return dict(mean=None, min=None, max=None, std=None, n=0)
    w = dt[k]; x = v[k]; m = float(np.sum(w * x) / np.sum(w))
    return dict(mean=m, min=float(x.min()), max=float(x.max()), std=float(np.sqrt(np.sum(w * (x - m) ** 2) / np.sum(w))), n=int(k.sum()))

def pimple_logs(case):
    """rotated logs log.pimpleFoam.<k> (k ascending) then the current log.pimpleFoam"""
    rot = sorted(glob.glob(f"{case}/log.pimpleFoam.[0-9]*"), key=lambda f: int(f.rsplit(".", 1)[1]))
    return rot + ([f"{case}/log.pimpleFoam"] if os.path.exists(f"{case}/log.pimpleFoam") else [])

def log_info(case):
    """Courant numbers / s per step over ALL run segments (rotated logs); completion (End after the last Time line, no FOAM FATAL) of the CURRENT log.pimpleFoam"""
    fs = pimple_logs(case)
    if not fs or not fs[-1].endswith("log.pimpleFoam"): return dict(complete=False, fatal=False, courant=[], host=None, build=None, n_time_lines=0, s_per_step=None, execution_time_s=None, n_segments=len(fs))
    co, spp_all, host, build, ex_tot = [], [], None, None, 0.0
    for f in fs:
        L = [ln.rstrip("\r") for ln in open(f, errors="replace").read().splitlines()]; t_cur = None
        for ln in L:
            m = re.match(r"^Time = (\S+)$", ln)
            if m: t_cur = float(m.group(1)); continue
            m = re.match(r"^Courant Number mean: (\S+) max: (\S+)", ln)
            if m: co.append((t_cur, float(m.group(2))))
        host = next((re.sub(r'^Host\s*:\s*"?([^"]*)"?.*$', r"\1", ln) for ln in L if ln.startswith("Host")), host)
        build = next((ln.split(":", 1)[1].strip() for ln in L if ln.startswith("Build")), build)
        ex = [float(m.group(1)) for m in (re.match(r"^ExecutionTime = (\S+) s", ln) for ln in L) if m]
        if len(ex) > 2: spp_all += list(np.diff(ex)[1:])      # the first step of a segment carries the coded-BC compile / restart reads
        ex_tot += ex[-1] if ex else 0.0
    tl = [i for i, ln in enumerate(L) if re.match(r"^Time = ", ln)]; en = [i for i, ln in enumerate(L) if ln == "End"]
    fatal = any("FOAM FATAL" in ln for ln in L)
    return dict(complete=bool(tl and en and en[-1] > tl[-1] and not fatal), fatal=fatal, courant=co, host=host, build=build, n_time_lines=len(tl),
                s_per_step=(float(np.median(spp_all)) if spp_all else None), execution_time_s=ex_tot, n_segments=len(fs))

def issue(path, text, date=None):
    """write text to path unless an identical file exists; a DIFFERENT existing file is never overwritten: <stem>_<date><ext>, then _<date>_r2, ... (work order section 5). Returns the path holding the text."""
    date = date or datetime.date.today().isoformat(); stem, ext = os.path.splitext(path)
    for cand in [path, f"{stem}_{date}{ext}"] + [f"{stem}_{date}_r{i}{ext}" for i in range(2, 100)]:
        if os.path.exists(cand):
            if open(cand, newline="").read() == text: return cand
            continue
        with open(cand, "w", newline="") as fh: fh.write(text)
        return cand
    raise SystemExit(f"too many re-issues of {path}")

def csv_text(rows, cols=None):
    import io
    cols = cols or list(dict.fromkeys(k for r in rows for k in r)); s = io.StringIO()
    w = csv.DictWriter(s, cols, extrasaction="ignore", lineterminator="\n"); w.writeheader(); [w.writerow(r) for r in rows]; return s.getvalue()

def analyse(case, out_dir, label=None, steady_results=None):
    case = os.path.abspath(case); os.makedirs(out_dir, exist_ok=True)
    bi = json.load(open(f"{case}/build_info.json"))
    if bi.get("flag") != FLAG: raise SystemExit(f"{case} is not a {FLAG} case")
    mode = bi["mode"]; w = bi["window"]; ws = read_state(case); T = float(ws["T_run_s"]); Tdecl = float(ws["T_decl_s"])
    label = label or re.sub(r"_(resistance|prescribed)$", "", os.path.basename(bi["steady_case"].rstrip("/")))
    lg = log_info(case)
    mm = {k: load_mon(case, k) for k in ["measurementP", "throatP", "throatFlux", "measurementFlux", "inletFlux", "measurementOrigP"]}
    if mm["measurementP"] is None or mm["throatP"] is None: raise SystemExit(f"{case}: no measurementP/throatP history (has the run started?)")
    t = mm["measurementP"][0]; t_last = float(t[-1])
    at_T = bool(lg["complete"] and same_time(t_last, T))
    if at_T: lo, hi = T / 2, T
    elif t_last > T / 2: lo, hi = T / 2, t_last
    else: lo, hi = t_last / 2, t_last
    flags = []
    if not at_T: flags.append("RUN_NOT_AT_T_RUN")
    elif ws.get("final") is None: flags.append("WINDOW_NOT_DECIDED")
    if ws.get("final") == "NOT_STATIONARY_AT_CAP": flags.append("WINDOW_NOT_STATIONARY")
    if not bi.get("production_ready"): flags.append("NOT_FOR_PRODUCTION")
    missing_outlets = [o["patch"] for o in bi["outlets"] if load_mon(case, f"{o['patch']}Flux") is None]
    if missing_outlets: flags.append("OUTLET_MONITOR_MISSING")
    trig = bi["trigger"]["decision"]
    if trig != "NOT_SETTLED": flags.append("TRIGGER_NOT_MET")
    status = "COMPLETE" if (at_T and ws.get("final") == "STATIONARY" and bi.get("production_ready") and not bi.get("forced_untriggered") and trig == "NOT_SETTLED" and not missing_outlets) else "INCOMPLETE"
    pa = C.P_AORTA_PA; assert abs(bi["steady_build_info"]["p0_kin"] * C.RHO - pa) < 1e-2 * pa
    def series(name, scale=1.0):
        m = mm.get(name) if name in mm else load_mon(case, name)
        return None if m is None else (m[0], m[2] * scale, m[1])
    res = dict(case=label, mode=mode, bc_mode="prescribed-flow" if mode == "prescribed" else "resistance", flags=";".join([FLAG] + flags), status=status, pimple_case=case, steady_case=bi["steady_case"],
               trigger=bi["trigger"]["decision"], trigger_reason=bi["trigger"].get("reason"), forced_untriggered=bi.get("forced_untriggered") or "", production_ready=bool(bi.get("production_ready")),
               measurement_probe_used=bi.get("measurement_probe_used"), throat_probe=bi.get("throat_probe"), T_decl_s=Tdecl, T_run_s=T, T_cap_s=float(ws["T_cap_s"]), window_final=ws.get("final") or "",
               n_window_tests=len(ws.get("history", [])), average_from_s=lo, average_to_s=hi, tau_jet_s=w["tau_jet_s"], tau_slow_s=w.get("tau_slow_s"), T_rule_binding=w.get("T_rule_binding"),
               t_last_s=t_last, n_steps=len(t))
    hist = dict(time=t)
    for key, name in (("FFR_measurement", "measurementP"), ("FFR_throat", "throatP"), ("FFR_measurement_orig", "measurementOrigP")):
        s = series(name, C.RHO / pa)
        if s is None: continue
        st = tavg(s[0], s[1], lo, hi); hist[key] = s[1]
        q = (lo + hi) / 2; d1, d2 = tavg(s[0], s[1], lo, q), tavg(s[0], s[1], q, hi)
        res.update({f"{key}_mean": st["mean"], f"{key}_min": st["min"], f"{key}_max": st["max"], f"{key}_band": (st["max"] - st["min"]) if st["n"] else None, f"{key}_std": st["std"],
                    f"{key}_drift_q4_minus_q3": (d2["mean"] - d1["mean"]) if d1["n"] and d2["n"] else None})
        try:
            sa, sv = last_mean(bi["steady_case"], name)
            res[f"{key}_steady_mon_last100"] = sv * C.RHO / pa; res[f"{key}_mean_minus_steady"] = (st["mean"] - sv * C.RHO / pa) if st["mean"] is not None else None
        except SystemExit: pass
    res["n_samples_in_average"] = tavg(t, hist["FFR_measurement"], lo, hi)["n"]
    tf = mm["throatFlux"]
    if tf is not None:
        D = 2 * np.sqrt(tf[1] / np.pi); Re = 4 * C.RHO * np.abs(tf[2]) / (np.pi * C.MU * D); st = tavg(tf[0], Re, lo, hi); hist["Re_throat"] = Re
        res.update(Re_throat_mean=st["mean"], Re_throat_min=st["min"], Re_throat_max=st["max"], Re_throat_source="bounded throatFlux monitor: 4 rho |Q| / (pi mu 2 sqrt(A/pi)), step-weighted")
    qi = mm["inletFlux"]
    orow = []
    qsum = 0.0
    for o in bi["outlets"]:
        q = series(f"{o['patch']}Flux"); p_ = series(f"{o['patch']}Pressure")
        if q is None: continue
        sq = tavg(q[0], q[1], lo, hi); sp = tavg(p_[0], p_[1], lo, hi) if p_ is not None else dict(mean=None, min=None, max=None)
        hist[f"Q_{o['patch']}_mls"] = q[1] * 1e6; qsum += sq["mean"] or 0.0
        r = dict(case=label, mode=mode, outlet_id=o["patch"], Q_mean_mls=sq["mean"] * 1e6, Q_min_mls=sq["min"] * 1e6, Q_max_mls=sq["max"] * 1e6, Q_band_pct=(sq["max"] - sq["min"]) / abs(sq["mean"]) * 100,
                 Q_target_bcC_mls=o["Q_target_m3s"] * 1e6, p_mean_Pa=(sp["mean"] * C.RHO if sp["mean"] is not None else None), p_min_Pa=(sp["min"] * C.RHO if sp["min"] is not None else None),
                 p_max_Pa=(sp["max"] * C.RHO if sp["max"] is not None else None), R_SI=o.get("R_used") if mode == "resistance" else None)
        if mode == "resistance" and p_ is not None:
            n = min(len(q[1]), len(p_[1])); k = (q[0][:n] > lo) & (q[0][:n] <= hi); tgt = C.PV + o["R_used"] * q[1][:n]
            r["bc_err_max_pct"] = float(np.max(np.abs(p_[1][:n] * C.RHO - tgt)[k] / tgt[k]) * 100) if k.any() else None
        orow.append(r)
    if qi is not None:
        si = tavg(qi[0], -qi[2], lo, hi); hist["Q_inlet_mls"] = -qi[2] * 1e6
        res.update(Q_inlet_mean_mls=si["mean"] * 1e6, Q_inlet_min_mls=si["min"] * 1e6, Q_inlet_max_mls=si["max"] * 1e6, mass_imbalance_pct=(si["mean"] - qsum) / si["mean"] * 100)
    for r in orow: res[f"Q_{r['outlet_id']}_mean_mls"] = r["Q_mean_mls"]; res[f"Q_{r['outlet_id']}_min_mls"] = r["Q_min_mls"]; res[f"Q_{r['outlet_id']}_max_mls"] = r["Q_max_mls"]
    co = [c for tt, c in lg["courant"] if tt is not None and lo < tt <= hi]
    dts = np.diff(t)
    res.update(max_courant_in_average=max(co) if co else None, dt_min_s=float(dts.min()) if len(dts) else None, dt_mean_s=float(dts.mean()) if len(dts) else None, dt_max_s=float(dts.max()) if len(dts) else None,
               log_complete=lg["complete"], host=lg["host"], openfoam_build=lg["build"], execution_time_s=lg["execution_time_s"], s_per_step_median=lg["s_per_step"])
    if len(dts):      # cost projection of the declared window and of the cap from the measured step (smoke runs: decide whether the fallback is affordable before committing ranks)
        dtm = float(np.median(dts[-min(len(dts), 50):])); wt = w.get("window_override_s") and bi["window"].get("T_rule_s") or Tdecl
        res.update(dt_recent_median_s=dtm, projected_total_steps=int(math.ceil(wt / dtm)), projected_total_steps_cap=int(math.ceil(CAP_FRAC * wt / dtm)), projection_window_s=wt,
                   projection_note="production T_decl (the rule value even when a test override was used) / recent median dt; wall clock = steps x median s/step of this run's rank count")
        res["projected_wallclock_h_at_this_rank_count"] = (res["projected_total_steps"] * lg["s_per_step"] / 3600) if lg["s_per_step"] else None
        res["projected_wallclock_h_cap_at_this_rank_count"] = (res["projected_total_steps_cap"] * lg["s_per_step"] / 3600) if lg["s_per_step"] else None
    # ---- FFR at every monitored probe (README PROBE MONITORS)
    prow, FFR, FQ, missing = [], {}, {}, {}
    for pid, rec in (bi.get("probe_monitors") or {}).items():
        r = dict(case=label, mode=mode, probe_id=pid, kind=rec.get("kind"), tree_node=rec.get("tree_node"), method=rec.get("method"))
        sp_, sq_ = series(f"pr_{pid}P", C.RHO / pa), series(f"pr_{pid}Flux")
        if rec.get("method") in ("bounded_box", "section_surface") and sp_ is not None and sq_ is not None:
            a1, a2 = tavg(sp_[0], sp_[1], lo, hi), tavg(sq_[0], sq_[2], lo, hi); a3 = tavg(sp_[0], sp_[2], lo, hi)
            r.update(FFR_mean=a1["mean"], FFR_min=a1["min"], FFR_max=a1["max"], FFR_std=a1["std"], Q_mean_mls=a2["mean"] * 1e6 if a2["mean"] is not None else None, area_mean_mm2=a3["mean"] * 1e6 if a3["mean"] is not None else None)
            exp_a = (rec.get("mesh_check") or {}).get("bounded_section_area_mm2") or (rec.get("section_check") or {}).get("section_area_mm2")
            r["area_expected_mm2"] = exp_a; r["area_rel_diff"] = (abs(r["area_mean_mm2"] - exp_a) / exp_a) if (exp_a and r["area_mean_mm2"] is not None) else None
            if r["area_rel_diff"] is None or r["area_rel_diff"] > 0.01:      # the monitor does not sample the section checked at build time: not used
                missing[pid] = f"monitor area {r['area_mean_mm2']} mm2 differs from the checked section {exp_a} mm2 by more than 1 %"; r["missing_reason"] = missing[pid]
            else: FFR[pid] = a1["mean"]; FQ[pid] = r["Q_mean_mls"]; hist[f"FFR_{pid}"] = sp_[1]
        else: missing[pid] = "; ".join(rec.get("reasons") or []) or f"monitor pr_{pid}P/Flux has no samples"; r["missing_reason"] = missing[pid]
        zt = rec.get("zone_test")
        if zt:
            zp, zq = series(f"pz_{pid}P", C.RHO / pa), series(f"pz_{pid}Flux")
            if zp is not None and zq is not None:
                b1, b2 = tavg(zp[0], zp[1], lo, hi), tavg(zp[0], zp[2], lo, hi)
                r.update(zone_test_FFR_mean=b1["mean"], zone_test_area_mean_mm2=b2["mean"] * 1e6, zone_test_minus_box_FFR=(b1["mean"] - r.get("FFR_mean")) if r.get("FFR_mean") is not None else None,
                         zone_test_expected_area_mm2=zt.get("section_area_mm2"))
        prow.append(r)
    if missing: res["flags"] += ";PROBE_MONITOR_MISSING"
    res["n_probes_monitored"] = len(FFR); res["n_probes_missing"] = len(missing)
    # history csv (every step), aligned on the measurementP times
    n = len(t); cols = list(hist)
    rows_h = [{c: (float(hist[c][i]) if i < len(hist[c]) else None) for c in cols} for i in range(n)]
    tag = f"{label}_{mode}"; written = {}
    written["result"] = issue(f"{out_dir}/pimple_result_{tag}.csv", csv_text([res]))
    written["outlets"] = issue(f"{out_dir}/pimple_outlets_{tag}.csv", csv_text(orow))
    written["history"] = issue(f"{out_dir}/pimple_history_{tag}.csv", csv_text(rows_h, cols))
    written["probes"] = issue(f"{out_dir}/pimple_probes_{tag}.csv", csv_text(prow))
    if steady_results:
        rr = [r for r in csv.DictReader(open(steady_results)) if r.get("case") == label and r.get("bc_mode") == res["bc_mode"]]
        if len(rr) == 1:
            r = dict(rr[0]); r["converged"] = FLAG; r["flags"] = (r.get("flags") if r.get("flags") not in (None, "", "NONE") else "") ; r["flags"] = ";".join(x for x in [FLAG] + r["flags"].split(";") + res["flags"].split(";")[1:] if x)
            r["Re_throat"] = res.get("Re_throat_mean", ""); r["Q_inlet_mls"] = res.get("Q_inlet_mean_mls", ""); r["iterations"] = f"{len(t)} time steps"
            r["notes"] = (r.get("notes") or "") + (f" | {FLAG} (D15): steady B1 {bi['trigger']['decision']}; pimpleFoam time average over [{lo*1e3:.3f}, {hi*1e3:.3f}] ms of a {T*1e3:.3f} ms run (T_decl {Tdecl*1e3:.3f} ms = max(6 tau_jet {w['tau_jet_s']*1e3:.3f}, 1.5 tau_slow {(w.get('tau_slow_s') or 0)*1e3:.3f}) ms, "
                                                   f"window {ws.get('final')}), status {status}; FFR_measurement {res.get('FFR_measurement_mean')} [{res.get('FFR_measurement_min')}, {res.get('FFR_measurement_max')}], "
                                                   f"FFR_throat {res.get('FFR_throat_mean')} [{res.get('FFR_throat_min')}, {res.get('FFR_throat_max')}]; Re_throat = time-mean of the bounded throat monitor")
            written["m1_row"] = issue(f"{out_dir}/M1_results_pimple_{tag}.csv", csv_text([r], list(rr[0].keys())))
        else: print(f"note: {len(rr)} rows for ({label}, {res['bc_mode']}) in {steady_results}: M1_results_pimple not written", file=sys.stderr)
    hs = ws.get("history") or []
    pj = dict(status=status, steady_case=bi["steady_case"], settle_decision=bi["trigger"]["decision"], production_ready=bool(bi.get("production_ready")), case=label, mode=mode, pimple_case=case,
              outlets={r["outlet_id"]: r["Q_mean_mls"] for r in orow}, outlets_unit="mL/s, time average over [average_from_s, average_to_s]", FFR=FFR, FFR_Q_mls=FQ, FFR_probes_missing=missing,
              FFR_measurement_mean=res.get("FFR_measurement_mean"), FFR_throat_mean=res.get("FFR_throat_mean"), Re_throat_mean=res.get("Re_throat_mean"), measurement_probe_used=bi.get("measurement_probe_used"),
              flags=res["flags"], average_from_s=lo, average_to_s=hi, T_decl_s=Tdecl, T_run_s=T, window=dict(final=ws.get("final"), history=hs, rule=w.get("rule")),
              stationarity=(hs[-1] if hs else None), analysed=(hs[-1].get("decided") if hs else None), mass_imbalance_pct=res.get("mass_imbalance_pct"), host=lg["host"], openfoam_build=lg["build"],
              pimple_fallback_sha256=bi.get("builder_sha256"))
    written["result_json"] = issue(f"{out_dir}/pimple_result_{tag}.json", json.dumps(pj, indent=1, default=str) + "\n")
    summ = dict(result=res, outlets=orow, probes=prow, window=w, window_state=ws, build_trigger=bi["trigger"], files={k: dict(file=os.path.basename(v), sha256=hashlib.sha256(open(v, "rb").read()).hexdigest()) for k, v in written.items()})
    written["summary"] = issue(f"{out_dir}/pimple_summary_{tag}.json", json.dumps(summ, indent=1, default=str) + "\n")
    print(f"{tag}: {status}, {len(t)} steps to t = {t_last:.6g} s (T_run {T:.6g} s, final {ws.get('final')}, average ({lo:.6g}, {hi:.6g}]): FFR_measurement {res.get('FFR_measurement_mean')} [{res.get('FFR_measurement_min')}, "
          f"{res.get('FFR_measurement_max')}], FFR_throat {res.get('FFR_throat_mean')}, Re_throat {res.get('Re_throat_mean')}, mass imbalance {res.get('mass_imbalance_pct')} %, probes {len(FFR)} monitored / {len(missing)} missing, flags {res['flags']}")
    for k, v in written.items(): print(f"  {k}: {v}")
    return res

# ---------------------------------------------------------------- pool job
def make_job(steady, task, name, priority=1, ranks=16, jobs_dir=POOL_JOBS, ret_root=RET_ROOT):
    """jobs/<name>.json for the pool (atomic write; never a .audited marker). RAM 1.7 GB per million cells + 1.5 (simpleFoam jobs: 1.4/M + 1.5; pimpleFoam keeps U_0, U_0_0, phi_0 and the PISO
    work arrays), disk max(6, 1.5 GB per million cells) (decomposed mesh + two purgeWrite time levels + monitors), ranks 16, after [] (the operator creates the job after its own audit of the trigger).
    FAIL-CLOSED: refuses unless the steady solve's return RET/<Task>/<steady>/ holds exactly one settle_*.csv whose decision is NOT_SETTLED (the same rule as `check`/build)."""
    steady = os.path.abspath(steady)
    if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or not re.fullmatch(r"Task[A-Za-z0-9]+", task): raise SystemExit(f"bad name {name!r} / task {task!r}")
    if not 1 <= ranks <= MAX_RANKS: raise SystemExit(f"ranks 1..{MAX_RANKS}")
    info = json.load(open(f"{steady}/build_info.json"))
    if info.get("mode") not in ("resistance", "prescribed"): raise SystemExit(f"{steady}: not a steady M1 case (mode {info.get('mode')!r})")
    mg = os.path.join(info.get("mesh_source_dir") or "", "mesh_gates.json"); cells = json.load(open(mg)).get("cells") if os.path.exists(mg) else None
    if not isinstance(cells, int) or cells <= 0: raise SystemExit(f"{mg}: no cell count")
    sl = glob.glob(f"{ret_root}/{task}/{os.path.basename(steady)}/settle_*.csv")
    if len(sl) != 1: raise SystemExit(f"REFUSED: expected exactly one settle_*.csv in {ret_root}/{task}/{os.path.basename(steady)}/, found {sl}")
    dec, det = settle_decision(sl[0], steady)
    if dec != "NOT_SETTLED": raise SystemExit(f"REFUSED: settle decision {dec} ({det.get('reason')}): no fallback job for this solve")
    ram = round(1.7 * cells / 1e6 + 1.5, 1); disk = max(6, int(math.ceil(1.5 * cells / 1e6)))
    cmd = f"DISK_NEED_GB={disk} bash {WRAPPER} {steady} {task} {name} {ranks}"
    job = dict(name=name, ranks=ranks, ram_gb=ram, disk_gb=disk, priority=priority, cmd=cmd, after=[])
    os.makedirs(jobs_dir, exist_ok=True); f = f"{jobs_dir}/{name}.json"
    if os.path.exists(f) and json.load(open(f)) != job: raise SystemExit(f"{f} exists with a different content: not overwritten (remove it first if intended)")
    tmp = f"{jobs_dir}/.{name}.json.tmp{os.getpid()}"
    with open(tmp, "w") as fh: json.dump(job, fh, indent=1); fh.flush(); os.fsync(fh.fileno())
    os.replace(tmp, f)
    print(f"{f}: cells {cells}, ranks {ranks}, ram {ram} GB, disk {disk} GB, priority {priority}, after []; NO .audited marker written")
    return job

def main(a):
    cmds = ("check", "build", "resume-point", "window", "analyse", "make-job")
    if not a or a[0] not in cmds:
        if a and a[0] == "run": raise SystemExit("`run` was removed (audit R2 Sol finding 4): runs go through the pool wrapper wo1010/fallback_job.sh <steady_case> <Task> <name> [ranks]")
        raise SystemExit(__doc__)
    def opt(f, d=None):
        if f in a: i = a.index(f); v = a[i + 1]; del a[i:i + 2]; return v
        return d
    cmd = a.pop(0)
    if cmd == "check":
        dec, det = settle_decision(a[0], a[1]); print(dec, json.dumps(det, default=str)); sys.exit({"NOT_SETTLED": 0, "SETTLED": 3}.get(dec, 2))
    if cmd == "build":
        s, n, f, w = opt("--settle"), int(opt("--nproc", 16)), opt("--force-untriggered"), opt("--window-override-s"); zt = tuple(x for x in (opt("--zone-test") or "").split(",") if x)
        existed = os.path.exists(a[1])
        try: build(a[0], a[1], s, n, f, float(w) if w else None, zt)
        except SystemExit as e:
            if not existed and os.path.isdir(a[1]) and not os.path.exists(f"{a[1]}/build_info.json"):
                open(f"{a[1]}/BUILD_FAILED", "w").write(f"{e}\n")      # a half-built case is marked, not removed
            raise
    elif cmd == "resume-point":
        code, info = resume_point(a[0], int(a[1])); print(json.dumps(info, default=str)); sys.exit(code)
    elif cmd == "window":
        code, st = window_decide(a[0]); h = st["history"][-1] if st["history"] else {}
        print(f"window: {['STATIONARY', 'EXTENDED', 'NOT_STATIONARY_AT_CAP'][{0: 0, 10: 1, 11: 2}[code]]} at T_run {h.get('T_run_s')} -> T_run {st['T_run_s']} (cap {st['T_cap_s']}); "
              f"FFR_meas Q3 {h.get('FFR_measurement_Q3')} Q4 {h.get('FFR_measurement_Q4')}; fails {h.get('fails')}"); sys.exit(code)
    elif cmd == "make-job":
        pr, rk, jd, rr = int(opt("--priority", 1)), int(opt("--ranks", 16)), opt("--jobs-dir", POOL_JOBS), opt("--ret-root", RET_ROOT); make_job(a[0], a[1], a[2], pr, rk, jd, rr)
    else:
        l, sr = opt("--label"), opt("--steady-results"); res = analyse(a[0], a[1], l, sr); sys.exit(0 if res["status"] == "COMPLETE" else 6)      # 6 = INCOMPLETE (fallback_job.sh)

if __name__ == "__main__":
    main(sys.argv[1:])
