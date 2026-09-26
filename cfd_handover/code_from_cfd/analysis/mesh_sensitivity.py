"""Mesh-sensitivity arithmetic for the lesion80 throat (design: mesh_sensitivity_design.md, v3). Rules and tolerances are FIXED in the design before any of these solves and are constants here.
usage: mesh_sensitivity.py <out.json> [M50=<case> T25a=<case> T25b=<case> W100=<case> REF=<case>]     (case = solve_* directory name in the pilot dir)
Each case dir must contain analysis.json (analyze_solve.py), sections_<mode>.csv/.json (lesion_sections.py), wss_<mode>.csv/.json (reattachment_wss.py), all from the SAME reconstructed time.
Missing, invalid or non-finite data NEVER shrink a window: the quantity becomes NaN and its label UNASSESSABLE. No GCI / order of accuracy is computed (the level set is not a systematic refinement family)."""
import sys, os, io, re, json, csv
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code"); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from zerod_ffr import P_AORTA, MMHG
from build_lesion80_surface import S_C
BASE = os.path.dirname(os.path.abspath(__file__))
DEFAULT = dict(M50="solve_lesion80", T25a="solve_lesion80_T25a", T25b="solve_lesion80_T25b", W100="solve_lesion80_W100", REF="solve_baseline_ref")
S_UP, S_DOWN = 18.5, 29.5                   # pressure-loss stations; 29.5 is the last validated section before the 1.5 mm-spaced sections (there is no section at 30.0)
# pre-registered tolerances: ("abs", x) = absolute change in the quantity's own unit, ("rel", x) = fraction of |M50 value|; |change| <= tolerance counts as within tolerance
TOL = {"flow_red_distal_pct": ("abs", 0.5), "flow_red_total_pct": ("abs", 0.5), "added_static_loss_mmHg": ("rel", 0.03), "p_min_over_Pao": ("abs", 0.0033),
       "umax_ms": ("rel", 0.05), "tau_peak_throat_Pa": ("rel", 0.05), "onset_arc_mm": ("abs", 0.25), "recovery_arc_wss_mm": ("abs", 1.0),
       "max_reversed_wall_fraction": ("abs", 0.05), "max_reversed_area_fraction": ("abs", 0.05)}
# expected station grids (lesion_sections.py: 0.25 mm within +-6 mm of the throat incl. 23.5, 1.5 mm elsewhere; reattachment_wss.py: 0.25 mm from 15 to 45)
SEC_GRID = lambda lo, hi: [round(x, 2) for x in np.concatenate([np.arange(17.5, 29.5 + 1e-9, 0.25), [31.0, 32.5, 34.0, 35.5, 37.0, 38.5, 40.0, 41.5]]) if lo - 1e-9 <= x <= hi + 1e-9]
WSS_GRID = lambda lo, hi: [round(x, 2) for x in np.arange(lo, hi + 1e-9, 0.25)]

def _no_dups(pairs):
    keys = [k for k, _ in pairs]
    if len(set(keys)) != len(keys): raise Bad(f"duplicate JSON object keys: {sorted({k for k in keys if keys.count(k) > 1})}")
    return dict(pairs)
def read_bytes(path):
    """Whole file as bytes; a NUL byte anywhere is Bad BEFORE any parser sees it (pandas reads e.g. '0\\x00.9' silently as 0.0)."""
    with open(path, "rb") as f: raw = f.read()
    if b"\x00" in raw: raise Bad(f"{os.path.basename(path)}: contains a NUL byte (corrupted/binary file)")
    return raw
def load_json(path):
    return json.loads(read_bytes(path).decode("utf-8"), object_pairs_hook=_no_dups)      # str, not bytes: a UTF-8 BOM stays an error as with open()

class Missing(Exception): pass          # a needed station/value is absent or invalid -> the quantity is UNASSESSABLE
class Bad(Exception): pass              # a file's structure/types are wrong -> the whole LEVEL is UNREADABLE
NEVER = 50.0            # sentinel arc (mm), beyond the 45 mm WSS grid, for the PHYSICAL outcomes "no separation" / "not recovered within 45 mm" (distinct from missing data)
OUTLETS = ("outlet_LCX", "outlet_IM", "outlet_D1", "outlet_D2", "outlet_LAD")
FLOW_RANGE, PRATIO_RANGE = (0.01, 10.0), (0.5, 1.2)           # mL/s per outlet and total (real 0.108-0.19 / 0.64-0.66); P/P_aorta at an outlet (real 0.88-0.99)
CAT_QUANTITIES = ("onset_arc_mm", "recovery_arc_wss_mm")

def num(x, what, lo=None, hi=None):
    """Strict number: rejects bool/str/None/list, non-finite and out-of-range values (Bad -> the level is unreadable)."""
    if isinstance(x, (bool, np.bool_)) or not isinstance(x, (int, float, np.integer, np.floating)): raise Bad(f"{what} is not a number: {x!r}")
    x = float(x)
    if not np.isfinite(x): raise Bad(f"{what} is not finite")
    if (lo is not None and x < lo) or (hi is not None and x > hi): raise Bad(f"{what}={x} outside [{lo}, {hi}]")
    return x

def validate_analysis(A):
    if not isinstance(A, dict): raise Bad("analysis.json is not an object")
    v = A.get("verdict")
    if not isinstance(v, str) or v not in ("CONVERGED", "UNCONVERGED"): raise Bad(f"verdict {v!r} is not CONVERGED/UNCONVERGED")
    o = A.get("outlets")
    if not isinstance(o, dict): raise Bad("outlets missing or not an object")
    Q, P = {}, {}
    for p in OUTLETS:
        d = o.get(p)
        if not isinstance(d, dict): raise Bad(f"outlet {p} missing or not an object")
        Q[p] = num(d.get("Q_mls"), f"{p}.Q_mls", *FLOW_RANGE); P[p] = num(d.get("P_over_Paorta"), f"{p}.P_over_Paorta", *PRATIO_RANGE)
    total = num(A.get("sum_outlets_mls"), "sum_outlets_mls", *FLOW_RANGE)
    if abs(total - sum(Q.values())) > 1e-6 * total: raise Bad(f"sum_outlets_mls={total} disagrees with the sum of the five outlet flows {sum(Q.values())}")
    return dict(verdict=v, last_iteration=num(A.get("last_iteration"), "last_iteration", 1, 1e7), total=total, Q=Q, P=P)

_FLOAT_TOKEN = re.compile(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
def read_csv_strict(path, numeric, boolean=()):
    """Strict reader for the pandas-written (to_csv(index=False)) section/WSS tables. pandas' parser is NOT used: it coerces malformed tokens silently (e.g. '"0".9' -> 0.9).
    csv.reader(strict=True) splits the rows; every row must have exactly len(header) fields (one trailing blank line tolerated); numeric cells must be empty (NaN),
    a plain decimal/scientific token, or nan/inf/-inf; boolean cells must be exactly True/False; other columns are kept as strings. Anything else is Bad (file, column, row)."""
    fn = os.path.basename(path); raw = read_bytes(path)
    try: text = raw.decode("utf-8")
    except UnicodeDecodeError as e: raise Bad(f"{fn}: not valid UTF-8 ({e})")
    try: rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as e: raise Bad(f"{fn}: malformed CSV (quoting/structure): {e}")
    if not rows or not rows[0]: raise Bad(f"{fn}: empty file or empty header line")
    header, data = rows[0], rows[1:]
    if data and data[-1] == []: data = data[:-1]                        # a single trailing blank line
    if len({h.strip() for h in header}) != len(header): raise Bad(f"{fn}: duplicate column names")
    if any("\ufeff" in h or h != h.strip() or not h for h in header): raise Bad(f"{fn}: header not read as written (BOM/whitespace/empty column name): {header}")
    for c in list(numeric) + list(boolean):
        if c not in header: raise Bad(f"{fn}: column {c!r} absent")
    if not data: raise Bad(f"{fn}: no data rows")
    for i, r in enumerate(data, start=2):
        if len(r) != len(header): raise Bad(f"{fn}: line {i} has {len(r)} fields, header has {len(header)}" + (" (blank line inside the data)" if r == [] else ""))
    cols = {}
    for j, c in enumerate(header):
        cells = [r[j] for r in data]
        if c in numeric:
            v = np.empty(len(cells))
            for i, t in enumerate(cells):
                if t == "": v[i] = np.nan
                elif t in ("nan", "inf", "-inf"): v[i] = float(t)
                elif _FLOAT_TOKEN.fullmatch(t) and np.isfinite(float(t)): v[i] = float(t)
                else: raise Bad(f"{fn}: column {c!r} line {i + 2}: {t!r} is not a plain number" + (" (overflows to inf)" if _FLOAT_TOKEN.fullmatch(t) else ""))
            cols[c] = v
        elif c in boolean:
            bad = [(i + 2, t) for i, t in enumerate(cells) if t not in ("True", "False")]
            if bad: raise Bad(f"{fn}: column {c!r} line {bad[0][0]}: {bad[0][1]!r} is not an explicit True/False")
            cols[c] = np.array([t == "True" for t in cells], dtype=bool)
        else: cols[c] = pd.Series(cells, dtype=object)                 # unused columns: kept verbatim as strings
    return pd.DataFrame(cols, columns=header)

def read_time(path):
    J = load_json(path)
    if not isinstance(J, dict): raise Bad(f"{os.path.basename(path)} is not an object")
    return num(J.get("time"), f"{os.path.basename(path)}: time", 1e-9, 1e7)

def load(c, mode):
    """Strict loader. Returns a level dict: kind = 'ok' (converged, post-processed), 'unconverged' (valid analysis.json saying UNCONVERGED; post-processing files are not read).
    Raises SystemExit for a missing analysis.json or for a CONVERGED level whose post-processing is missing; Bad for structurally wrong files."""
    d = os.path.join(BASE, c)
    if not os.path.exists(f"{d}/analysis.json"): raise SystemExit(f"{c}: analysis.json not found")
    A = validate_analysis(load_json(f"{d}/analysis.json"))
    if A["verdict"] != "CONVERGED": return dict(kind="unconverged", A=A, name=c, time_consistent=False)
    need = [f"sections_{mode}.csv", f"sections_{mode}.json", f"wss_{mode}.csv", f"wss_{mode}.json"]
    miss = [f for f in need if not os.path.exists(f"{d}/{f}")]
    if miss: raise SystemExit(f"{c}: CONVERGED but post-processing files missing: {miss} - post-process it first")
    S = read_csv_strict(f"{d}/sections_{mode}.csv", ["s_mm", "p_over_Pao", "umax_ms", "frac_reversed_area"], ["ok"])
    W = read_csv_strict(f"{d}/wss_{mode}.csv", ["s_mm", "tau_mean_Pa", "f_rev"])
    t = [A["last_iteration"], read_time(f"{d}/sections_{mode}.json"), read_time(f"{d}/wss_{mode}.json")]
    return dict(kind="ok", A=A, S=S, W=W, name=c, time_consistent=bool(len(set(t)) == 1))     # analysis final iteration == the reconstructed time read by both post-processors

def load_safe(c, mode):
    try: return load(c, mode)
    except SystemExit: raise
    except Exception as e:                                             # Bad, malformed JSON/CSV, anything else: the level is unusable, say so and why
        return dict(kind="unreadable", A=dict(verdict="UNREADABLE"), name=c, time_consistent=False, load_error=f"{type(e).__name__}: {e}")

def stations(df, col, grid, ok_col=None, lo=None, hi=None):
    """Values of `col` at EVERY station of `grid` (exact match, 1e-6); raise Missing if any station is absent, invalid, non-finite or outside the physical bounds [lo, hi]."""
    v = []
    sm = df["s_mm"]
    for s in grid:
        r = df[(sm - s).abs() < 1e-6]
        if len(r) != 1: raise Missing(f"station {s} absent or duplicated")
        r = r.iloc[0]
        if ok_col is not None and not bool(r[ok_col]): raise Missing(f"station {s} failed validation ({ok_col} False)")
        x = float(r[col])
        if not np.isfinite(x): raise Missing(f"station {s} non-finite {col}")
        if (lo is not None and x < lo) or (hi is not None and x > hi): raise Missing(f"station {s} {col}={x} outside the physical range [{lo}, {hi}]")
        v.append(x)
    return np.array(v)

def quantities(c, ref):
    if c["kind"] != "ok":
        q = {k: float("nan") for k in TOL}; q.update(verdict=c["A"]["verdict"], iterations=c["A"].get("last_iteration"), time_consistent=False, physical_outcome_notes={}, outcome_category={},
                                                       missing={"all": c.get("load_error", "not post-processed (level not converged)")})
        return q
    A, S, W = c["A"], c["S"], c["W"]; q = {}; why = {}; notes = {}; cats = {}
    def put(name, fn):
        try:
            x = float(fn())
            if not np.isfinite(x): raise Missing("non-finite result")
            q[name] = x
        except Missing as e: q[name] = float("nan"); why[name] = str(e)
        except Exception as e: q[name] = float("nan"); why[name] = f"unexpected {type(e).__name__}: {e}"      # nothing malformed becomes a value or a crash
    put("flow_red_distal_pct", lambda: 100 * (1 - sum(A["Q"][p] for p in ("outlet_D1", "outlet_D2", "outlet_LAD")) / sum(ref["A"]["Q"][p] for p in ("outlet_D1", "outlet_D2", "outlet_LAD"))))
    put("flow_red_total_pct", lambda: 100 * (1 - A["total"] / ref["A"]["total"]))
    def loss(X):
        p = stations(X["S"], "p_over_Pao", [S_UP, S_DOWN], "ok", lo=0.5, hi=1.2); return p[0] - p[1]
    put("added_static_loss_mmHg", lambda: (loss(c) - loss(ref)) * P_AORTA / MMHG)
    put("p_min_over_Pao", lambda: stations(S, "p_over_Pao", SEC_GRID(22.0, 29.5), "ok", lo=0.5, hi=1.2).min())
    put("umax_ms", lambda: stations(S, "umax_ms", SEC_GRID(22.0, 26.0), "ok", lo=0.0, hi=20.0).max())
    put("tau_peak_throat_Pa", lambda: stations(W, "tau_mean_Pa", WSS_GRID(22.0, 25.0), lo=-1e4, hi=1e4).max())
    f_on = lambda: stations(W, "f_rev", WSS_GRID(S_C, 45.0), lo=0.0, hi=1.0)        # needs EVERY station from the throat to 45 mm
    def onset(record=False):
        f = f_on(); g = WSS_GRID(S_C, 45.0); k = np.where(f >= 0.01)[0]
        if len(k): return g[k[0]]
        if record: notes["onset_arc_mm"] = f"physical outcome: no separation (reversed-wall fraction < 1 % at every station to 45 mm); sentinel {NEVER}"
        return NEVER
    put("onset_arc_mm", lambda: onset(True))
    cats["onset_arc_mm"] = "none" if q.get("onset_arc_mm") == NEVER else ("separated" if np.isfinite(q.get("onset_arc_mm", float("nan"))) else "unassessable")
    def recovery():
        f = f_on(); g = np.array(WSS_GRID(S_C, 45.0)); on = onset()
        if on == NEVER: notes["recovery_arc_wss_mm"] = f"physical outcome: no separation, nothing to recover from; sentinel {NEVER}"; return NEVER
        for k in range(len(g)):
            if g[k] > on and (f[k:] < 0.01).all(): return g[k]
        notes["recovery_arc_wss_mm"] = f"physical outcome: not recovered within 45 mm (reversed-wall fraction >= 1 % at the last station); sentinel {NEVER}"
        return NEVER
    put("recovery_arc_wss_mm", recovery)
    rv = q.get("recovery_arc_wss_mm", float("nan"))
    cats["recovery_arc_wss_mm"] = "unassessable" if not np.isfinite(rv) else ("recovered" if rv != NEVER else ("no_separation" if cats["onset_arc_mm"] == "none" else "not_recovered"))
    put("max_reversed_wall_fraction", lambda: stations(W, "f_rev", WSS_GRID(24.0, 39.0), lo=0.0, hi=1.0).max())
    put("max_reversed_area_fraction", lambda: stations(S, "frac_reversed_area", SEC_GRID(24.0, 38.5), "ok", lo=0.0, hi=1.0).max())
    for p in OUTLETS: q[f"P_over_Pao_{p}"] = A["P"][p]
    q["verdict"] = A["verdict"]; q["iterations"] = A["last_iteration"]; q["time_consistent"] = c["time_consistent"]; q["missing"] = why; q["physical_outcome_notes"] = notes; q["outcome_category"] = cats
    return q

def exceeds(x, t): return abs(x) > t * (1 + 1e-9) + 1e-15               # equality at the threshold counts as within tolerance (floating-point safe)

def label(name, m50, a, b, w100, w_converged=True):
    """Precedence: UNASSESSABLE > SENSITIVE > INTERFACE-CONTAMINATED > NON-MONOTONE > INSENSITIVE. m50 = audited mesh, a = T25a, b = T25b, w100 = W100."""
    kind, tol = TOL[name]; t = tol * (abs(m50) if kind == "rel" and np.isfinite(m50) else 1.0)
    vals = [m50, a, b] + ([w100] if w_converged else [])
    if not all(np.isfinite(x) for x in vals): return "UNASSESSABLE (missing, invalid or non-finite data)", t
    if exceeds(a - m50, t) or exceeds(b - m50, t): return "SENSITIVE", t
    if exceeds(a - b, t): return "INTERFACE-CONTAMINATED", t
    if not w_converged: return "INSENSITIVE on the fine side (monotonicity not assessed: W100 unconverged)", t
    dc, df_ = w100 - m50, m50 - a                                      # series W100 -> M50 -> T25a (increasing resolution); monotone = same sign
    if exceeds(dc, t) and abs(df_) > 0.2 * t and np.sign(dc) != np.sign(df_): return "NON-MONOTONE", t
    return "INSENSITIVE", t

def main(out, args):
    if not isinstance(out, str) or "=" in out or not out.endswith(".json"):   # checked before anything is opened: a forgotten output argument must not become a file named 'T25a=...'
        raise SystemExit(f"bad output path {out!r}: the first argument must be the output file ending in .json (no '='); usage: mesh_sensitivity.py <out.json> [TAG=<case dir> ...]")
    cases = dict(DEFAULT); seen = set()
    for a in args:
        if not isinstance(a, str) or a.count("=") != 1 or not a.split("=")[0] or not a.split("=")[1]: raise SystemExit(f"bad argument {a!r}: expected TAG=<case dir>, e.g. T25a=solve_lesion80_T25a")
        k, v = a.split("=")
        if k in seen: raise SystemExit(f"level tag {k!r} given more than once; give each tag at most once")
        seen.add(k); cases[k] = v
    unknown = [k for k in cases if k not in DEFAULT]
    if unknown: raise SystemExit(f"unknown level tag(s) {unknown}; expected {list(DEFAULT)}")
    real = {k: os.path.realpath(os.path.join(BASE, v)) for k, v in cases.items()}
    if len(set(real.values())) != len(real): raise SystemExit(f"two level tags resolve to the same directory: {real}")
    try: outf = open(out, "w")                                            # open the output first: an unwritable path must stop the analysis BEFORE anything is computed
    except OSError as e: raise SystemExit(f"cannot write the output file {out!r}: {e}")
    for k, v in cases.items(): print(f"dir: {k:5s} -> {real[k]}" + ("  (override)" if k in seen else "  (default)"))   # always show which directory each tag used
    C = {k: load_safe(v, "baseline_ref" if k == "REF" else "lesion80") for k, v in cases.items()}; ref = C.pop("REF")
    if ref["kind"] == "unreadable": raise SystemExit(f"REF must be readable ({ref['load_error']})")
    for k in ("M50", "T25a", "T25b"):
        if C[k]["kind"] == "unreadable": raise SystemExit(f"{k} must be readable ({C[k]['load_error']})")
    if ref["kind"] != "ok": bad_ref = ["REF"]
    else: bad_ref = [] if ref["time_consistent"] else ["REF"]
    if ref["kind"] != "ok":                                            # unconverged REF: nothing can be assessed; report it plainly
        Q = {k: quantities(c, ref) if c["kind"] != "ok" else dict(quantities({**c, "kind": "unconverged"}, ref), verdict=c["A"]["verdict"]) for k, c in C.items()}
    else:
        Q = {k: quantities(c, ref) for k, c in C.items()}
    bad = bad_ref + [k for k in ("M50", "T25a", "T25b") if C[k]["kind"] != "ok" or not C[k]["time_consistent"]]
    w_kind = C["W100"]["kind"]; w_ok = (w_kind == "ok")
    if w_kind == "ok" and not C["W100"]["time_consistent"]: bad.append("W100(time-inconsistent)")     # bookkeeping error: never excused as "unconverged"
    if w_kind == "unreadable": bad.append(f"W100(unreadable: {C['W100']['load_error']})")                # never excused either
    res = dict(cases=cases, quantities=Q, labels={}, unconverged_or_inconsistent=bad, W100_kind=w_kind)
    print("runs:", {k: (q["verdict"], q["iterations"], "time-consistent" if q["time_consistent"] else "TIME MISMATCH/none") for k, q in Q.items()}, "| REF:", ref["A"]["verdict"])
    print(f"{'quantity':30s} {'W100':>10s} {'M50':>10s} {'T25a':>10s} {'T25b':>10s} {'tol':>8s}  label")
    for name in TOL:
        v = {k: Q[k][name] for k in Q}
        if bad: lab, t = f"UNASSESSABLE (unconverged, unreadable or time-inconsistent: {','.join(bad)})", float("nan")
        else:
            lab, t = label(name, v["M50"], v["T25a"], v["T25b"], v["W100"], w_ok)
            if name in CAT_QUANTITIES and not lab.startswith("UNASSESSABLE"):
                cat = {k: Q[k]["outcome_category"].get(name) for k in ("M50", "T25a", "T25b")}
                if len(set(cat.values())) > 1: lab = f"SENSITIVE (outcome category differs among M50/T25a/T25b: {cat})"
                elif w_ok and Q["W100"]["outcome_category"].get(name) != cat["M50"]:
                    lab2, t = label(name, v["M50"], v["T25a"], v["T25b"], float("nan"), False)      # sentinel arithmetic must not enter the monotonicity test: fine side only
                    lab = (f"INSENSITIVE on the fine side; W100 outcome category differs ({Q['W100']['outcome_category'].get(name)} vs {cat['M50']}): coarse-side dependence, reported"
                           if lab2.startswith("INSENSITIVE") else lab2)
        res["labels"][name] = dict(label=lab, tolerance=t, **v)
        print(f"{name:30s} {v['W100']:10.4f} {v['M50']:10.4f} {v['T25a']:10.4f} {v['T25b']:10.4f} {t:8.4f}  {lab}")
    for k in Q:
        if Q[k]["missing"]: print(f"  missing data in {k}: {Q[k]['missing']}")
        if Q[k].get("physical_outcome_notes"): print(f"  physical outcome in {k}: {Q[k]['physical_outcome_notes']}")
    for name in sorted({k for L_ in Q.values() for k in L_ if k.startswith("P_over_Pao_")}):
        print(f"{name:30s} " + " ".join(f"{Q[k].get(name, float('nan')):10.5f}" for k in ("W100", "M50", "T25a", "T25b")) + "   (reported, no rule)")
    try: json.dump(res, outf, indent=1, default=float); outf.flush(); outf.close()     # write, flush AND close can fail (e.g. ENOSPC on close): stop cleanly, no traceback
    except OSError as e:
        try: outf.close()
        except (OSError, ValueError): pass                          # the underlying fd is released even when this second close fails
        raise SystemExit(f"cannot write the output file {out!r}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2: raise SystemExit("usage: mesh_sensitivity.py <out.json> [TAG=<case dir> ...]")
    main(sys.argv[1], sys.argv[2:])
