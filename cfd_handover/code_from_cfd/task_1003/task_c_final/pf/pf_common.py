"""Shared pieces of the Task-3 case builders (Item 1 prescribed-flow round trip, scan-14 M1 packages). No 0D code, no zerod_ffr import.
Case anatomy (all written here so that every case of the Task-3 family is identical except its BCs):
  constant/polyMesh (hard-linked from a mesh or the prescribed case when on the same filesystem, else copied), constant/{transportProperties,turbulenceProperties} + system/{fvSchemes,fvSolution} copied from the
  audited source case/template, system/controlDict (fixed budget endTime 3000, no residualControl, binary fields, per-patch flux + area-average p monitors, optional BOUNDED throat and measurement planes (D8: measurementP every iteration)),
  system/decomposeParDict (scotch), 0/U, 0/p, zerod_reference.json (a stub for analyze_solve.py: R_out, Q0_mls = the TARGET flow, NOT a 0D prediction), build_info.json, case.foam.
Modes: 'resistance' (audited codedFixedValue p per outlet, U inletOutlet), 'prescribed' (U flowRateOutletVelocity per outlet, p zeroGradient; inlet totalPressure in both).
OUTLET LOST IN MESH (P5 scan 272, out_396; audit P5 Sol finding 1): an outlet patch with ZERO faces in the polyMesh gets NO surfaceFieldValue monitor (a selected patch yielding zero faces is fatal in v2406,
surfaceFieldValue.C) and no zerod_reference entry; its 0/p, 0/U entries stay (resistance: the coded BC, inert on an empty patch, verified by tests/test_empty_patch_coded_bc.sh; prescribed: zeroGradient / noSlip,
no flow can be imposed on it); build_info.json 'outlets' lists the outlets WITH faces only, 'outlets_lost_in_mesh' the lost ones (reason, bc_A R, bc_C target), 'bc_bookkeeping' the territory accounting
(the lost outlet's territory is CLOSED: no flow, its bc_C target not delivered, its bc_A R not applied).
flowRateOutletVelocity (OpenFOAM ESI v2406, src/finiteVolume/.../flowRateOutletVelocity): volumetricFlowRate is POSITIVE OUT of the domain, fixedValue patch velocity = extrapolated interior velocity with its
normal component rescaled (if the estimated flow exceeds half the target) or offset (otherwise) so that gSum(magSf*nUp) equals the target exactly; reverse flow is removed (nUp >= 0)."""
import os, re, json, shutil, subprocess, types
import numpy as np

RHO, MU, PV = 1060.0, 0.004, 666.61
P_AORTA_PA = 11998.98
END_TIME = 3000
WRITE_INTERVAL, PURGE_WRITE = 250, 3

P_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__)); P = os.path.dirname(P_SCRIPT_DIR)

def relax_from_G(R, R_own):
    """audited rule: G = R/R_own, relax = min(0.5, 1/(1+G)) (bc/resistanceOutlet_steady.md)"""
    G = R / R_own
    return G, min(0.5, 1.0 / (1.0 + G))

def read_boundary(polymesh):
    txt = open(f"{polymesh}/boundary").read()
    out = {}
    start = re.search(r"^\d+\s*\n\(", txt, re.M).start()      # the patch count line followed by the opening parenthesis (after the FoamFile header)
    for m in re.finditer(r"(\w+)\s*\{([^}]*)\}", txt[start:]):
        body = m.group(2); ty = re.search(r"type\s+(\w+);", body); nf = re.search(r"nFaces\s+(\d+);", body)
        if ty and nf: out[m.group(1)] = dict(type=ty.group(1), nFaces=int(nf.group(1)))
    return out

def poly_dir(case_or_mesh):
    """accepts a case dir (constant/polyMesh below it) or a polyMesh dir itself"""
    for c in (f"{case_or_mesh}/constant/polyMesh", case_or_mesh):
        if os.path.exists(f"{c}/boundary") and os.path.exists(f"{c}/owner"): return c
    raise SystemExit(f"no polyMesh (boundary + owner) in {case_or_mesh}")

def link_or_copy(src, dst):
    """hard-link a polyMesh (same filesystem, never modified by the solver or decomposePar) else copy"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run(["cp", "-al", src, dst], capture_output=True)
    if r.returncode != 0:
        shutil.rmtree(dst, ignore_errors=True); shutil.copytree(src, dst); return "copied"
    return "hard-linked"

def fmt(x): return f"{x:.10e}"

def p_coded_block(patch, code_name, R, relax, p_init_kin):
    return (f"    {patch}\n    {{\n        type            codedFixedValue;\n        value           uniform {p_init_kin:.8f};\n        name            {code_name};\n        code\n        #{{\n"
            f"            const scalar R     = {R:.8e};\n            const scalar Pv    = {PV};\n            const scalar rho   = {RHO};\n            const scalar relax = {relax:.8f};\n"
            "            const fvsPatchField<scalar>& phip =\n                patch().lookupPatchField<surfaceScalarField, scalar>(\"phi\");\n"
            "            const scalar Q = gSum(phip);\n            const scalar pTarget = (Pv + R*Q)/rho;\n"
            "            const volScalarField& pFld = db().lookupObject<volScalarField>(\"p\");\n"
            "            const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);\n"
            "            operator==((1.0 - relax)*pOld + relax*pTarget);\n        #};\n    }\n")

def flow_function(Q, ramp_iters):
    """Function1 text for the flow rate: a constant, or a linear ramp over the first ramp_iters iterations (time = iteration number, deltaT 1)"""
    if ramp_iters and ramp_iters > 0: return f"table ((0 0) ({int(ramp_iters)} {Q:.10e}))"
    return f"{Q:.10e}"

def plane_spec(plane):
    """a probe plane as (point_m, normal) or (point_m, normal, bounds) with bounds = (lo_m, hi_m) or None, or a dict(point_m, normal, bounds_m); returns (pt, nrm, bounds)"""
    if plane is None: return None
    if isinstance(plane, dict): return plane["point_m"], plane["normal"], plane.get("bounds_m")
    return (plane[0], plane[1], plane[2] if len(plane) > 2 else None)

def surface_fo(name, patch=None, op=None, fld=None, plane=None, surf=None, write_area=False):
    """surfaceFieldValue written every iteration on a patch or on a sampled plane. plane: see plane_spec; bounds -> sampledPlane `bounds (lo) (hi);` (ESI v2406: only cells with centres in the box are cut,
    sampledPlane.C / cuttingSurfaceBaseSelection.C). An UNBOUNDED plane cuts every vessel crossing it (the 09-26 throat-monitor defect): the M1/P5 builders always pass checked bounds."""
    hd = f"    {name}\n    {{\n        type surfaceFieldValue; libs (\"libfieldFunctionObjects.so\");\n        writeControl timeStep; writeInterval 1; writeFields false; log true;{' writeArea true;' if write_area else ''}\n"
    if plane is None: return hd + f"        regionType patch; name {patch}; operation {op}; fields ({fld});\n    }}\n"
    pt, nrm, bnd = plane_spec(plane)
    bl = "" if bnd is None else f"            bounds ({bnd[0][0]:.9e} {bnd[0][1]:.9e} {bnd[0][2]:.9e}) ({bnd[1][0]:.9e} {bnd[1][1]:.9e} {bnd[1][2]:.9e});\n"
    return hd + (f"        regionType sampledSurface; name {surf or name + 'Plane'};\n        sampledSurfaceDict\n        {{\n            type plane; planeType pointAndNormal;\n"
                 f"            pointAndNormalDict {{ point ({pt[0]:.9e} {pt[1]:.9e} {pt[2]:.9e}); normal ({nrm[0]:.9e} {nrm[1]:.9e} {nrm[2]:.9e}); }}\n{bl}            interpolate false;\n        }}\n"
                 f"        operation {op}; fields ({fld});\n    }}\n")

def monitors(outlet_patches, throat_plane=None, measurement_plane=None, extra_planes=None):
    """per-patch flux + area-average p; throatFlux/throatP and (D8) measurementFlux/measurementP on the bounded probe planes, every iteration, with the sampled area written (writeArea) for the section check.
    extra_planes: {tag: plane} written as <tag>Flux/<tag>P the same way (e.g. measurementOrig: the package measurement probe when the strict section rule relocated measurementP, probe_sections.py)"""
    s = surface_fo("inletFlux", "inlet", "sum", "phi") + surface_fo("inletPressure", "inlet", "areaAverage", "p")
    for p in outlet_patches: s += surface_fo(f"{p}Flux", p, "sum", "phi") + surface_fo(f"{p}Pressure", p, "areaAverage", "p")
    for tag, pl in (("throat", throat_plane), ("measurement", measurement_plane)) + tuple(sorted((extra_planes or {}).items())):
        if pl is not None:
            s += (surface_fo(f"{tag}Flux", op="areaNormalIntegrate", fld="U", plane=pl, write_area=True)
                  + surface_fo(f"{tag}P", op="areaAverage", fld="p", plane=pl, write_area=True))
    return s

def plane_info(plane):
    if plane is None: return None
    pt, nrm, bnd = plane_spec(plane)
    return dict(point_m=list(map(float, pt)), normal=list(map(float, nrm)), bounds_m=None if bnd is None else [list(map(float, bnd[0])), list(map(float, bnd[1]))])

CONTROL_HEAD = ("FoamFile { version 2.0; format ascii; class dictionary; object controlDict; }\napplication     simpleFoam;\nstartFrom       startTime;\nstartTime       0;\nstopAt          endTime;\n"
                f"endTime         {END_TIME};\ndeltaT          1;\nwriteControl    timeStep;\nwriteInterval   {WRITE_INTERVAL};\npurgeWrite      {PURGE_WRITE};\nwriteFormat     binary;\n"
                "writePrecision  8;\nwriteCompression off;\ntimeFormat      general;\ntimePrecision   8;\nrunTimeModifiable true;\n\nfunctions\n{\n")

LOST_REASON_DEFAULT = "outlet patch has 0 faces in the polyMesh (the mesher removed the region holding it)"

def lost_outlets(info):
    """the outlets lost in the mesh of a built case: build_info 'outlets_lost_in_mesh' (this builder), else (cases built before it) the outlets of build_info 'outlets' whose patch has nFaces 0 in 'mesh_patches'"""
    if "outlets_lost_in_mesh" in info: return list(info["outlets_lost_in_mesh"])
    mp = info.get("mesh_patches") or {}
    return [dict(o, reason=LOST_REASON_DEFAULT + " (derived from build_info mesh_patches: case built before the lost-outlet handling)") for o in info.get("outlets", []) if (mp.get(o["patch"]) or {}).get("nFaces") == 0]

def live_outlets(info):
    """build_info 'outlets' minus any outlet lost in the mesh (identical to 'outlets' for cases built with the lost-outlet handling)"""
    lost = {o["patch"] for o in lost_outlets(info)}
    return [o for o in info.get("outlets", []) if o["patch"] not in lost]

def write_case(case, mode, polymesh_src, sys_src, const_src, outlets, p0_kin, nproc, closed_patches=(), throat_plane=None, ramp_iters=0, info=None, measurement_plane=None, extra_planes=None, lost_reasons=None):
    """outlets: list of dict(patch, code_name, R (resistance mode), relax, Q_target_m3s, p_init_kin, R_ref (reference resistance for the zerod_reference stub)). An outlet whose mesh patch has 0 faces is LOST
    (module docstring): BC entries kept, no monitor, not in zerod_reference / build_info 'outlets'; lost_reasons: {patch: text} from the mesh stage (default LOST_REASON_DEFAULT)."""
    assert mode in ("resistance", "prescribed"); assert 1 <= nproc <= 16, "rank cap 16 (work order section 6)"
    if os.path.exists(case): raise SystemExit(f"{case} exists")
    bnd = read_boundary(polymesh_src)
    want = {"inlet", "wall"} | {o["patch"] for o in outlets}
    got = set(bnd); extra_closed = set(closed_patches) & got
    if got - extra_closed != want: raise SystemExit(f"mesh patches {sorted(got)} != expected {sorted(want | extra_closed)}")
    for o in outlets:
        if bnd[o["patch"]]["type"] != "patch": raise SystemExit(f"{o['patch']} has type {bnd[o['patch']]['type']}, expected patch")
    lost = [o for o in outlets if bnd[o["patch"]]["nFaces"] == 0]; live = [o for o in outlets if bnd[o["patch"]]["nFaces"] > 0]
    if not live: raise SystemExit(f"every outlet patch has 0 faces: {[o['patch'] for o in outlets]}")
    names = [o["code_name"] for o in outlets]
    if mode == "resistance" and (len(set(names)) != len(names) or not all(re.fullmatch(r"res[A-Za-z0-9_]+", n) for n in names)): raise SystemExit(f"coded BC names not unique/res<...>: {names}")
    for d in ("constant", "system", "0"): os.makedirs(f"{case}/{d}")
    how = link_or_copy(polymesh_src, f"{case}/constant/polyMesh")
    for f in ("transportProperties", "turbulenceProperties"): shutil.copy(f"{const_src}/{f}", f"{case}/constant/{f}")
    for f in ("fvSchemes", "fvSolution"): shutil.copy(f"{sys_src}/{f}", f"{case}/system/{f}")
    # 0/p
    ptxt = ("FoamFile { version 2.0; format ascii; class volScalarField; object p; }\ndimensions      [0 2 -2 0 0 0 0];\n"
            f"internalField   uniform {p0_kin:.8f};\n\nboundaryField\n{{\n    inlet   {{ type totalPressure; p0 uniform {p0_kin:.8f}; value uniform {p0_kin:.8f}; }}\n    wall    {{ type zeroGradient; }}\n")
    for c in extra_closed: ptxt += f"    {c}   {{ type zeroGradient; }}\n"
    for o in outlets:
        ptxt += (p_coded_block(o["patch"], o["code_name"], o["R"], o["relax"], o["p_init_kin"]) if mode == "resistance" else f"    {o['patch']}   {{ type zeroGradient; }}\n")     # lost outlets too (inert on 0 faces)
    open(f"{case}/0/p", "w").write(ptxt + "}\n")
    # 0/U
    utxt = ("FoamFile { version 2.0; format ascii; class volVectorField; object U; }\ndimensions      [0 1 -1 0 0 0 0];\ninternalField   uniform (0 0 0);\n\nboundaryField\n{\n"
            "    inlet   { type pressureInletOutletVelocity; value uniform (0 0 0); }\n    wall    { type noSlip; }\n")
    for c in extra_closed: utxt += f"    {c}   {{ type noSlip; }}\n"
    for o in outlets:
        utxt += (f"    {o['patch']}   {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}\n" if mode == "resistance"
                 else f"    {o['patch']}   {{ type noSlip; }}\n" if o in lost       # a lost outlet carries no flow: no flow rate is imposed on its empty patch
                 else f"    {o['patch']}   {{ type flowRateOutletVelocity; volumetricFlowRate {flow_function(o['Q_target_m3s'], ramp_iters)}; value uniform (0 0 0); }}\n")
    open(f"{case}/0/U", "w").write(utxt + "}\n")
    open(f"{case}/system/controlDict", "w").write(CONTROL_HEAD + monitors([o["patch"] for o in live], throat_plane, measurement_plane, extra_planes) + "}\n")
    open(f"{case}/system/decomposeParDict", "w").write(f"FoamFile {{ version 2.0; format ascii; class dictionary; object decomposeParDict; }}\nnumberOfSubdomains {nproc};\nmethod scotch;\n")
    ref = {o["patch"]: dict(R_out=float(o["R"] if mode == "resistance" else o["R_ref"]), Q0_mls=float(o["Q_target_m3s"]) * 1e6, relax=o.get("relax")) for o in live}
    json.dump(dict(case=os.path.basename(case), mode=mode, note="stub for analyze_solve.py: Q0_mls is the TARGET flow (prescribed/bc_C), R_out the reference resistance law; NO 0D prediction", outlets=ref), open(f"{case}/zerod_reference.json", "w"), indent=1)
    open(f"{case}/case.foam", "w").close()
    binfo = dict(case=os.path.basename(case), mode=mode, nproc=nproc, endTime=END_TIME, writeInterval=WRITE_INTERVAL, purgeWrite=PURGE_WRITE, ramp_iters=ramp_iters, mesh_link=how, p0_kin=p0_kin, P_aorta_Pa=p0_kin * RHO,
                 closed_patches=sorted(extra_closed), throat_plane=plane_info(throat_plane), measurement_plane=plane_info(measurement_plane), extra_planes={k: plane_info(v) for k, v in sorted((extra_planes or {}).items())},
                 outlets=[outlet_record(o) for o in live],
                 outlets_lost_in_mesh=[dict(outlet_record(o), nFaces=0, reason=(lost_reasons or {}).get(o["patch"], LOST_REASON_DEFAULT), flag="OUTLET_LOST_IN_MESH",
                                            bc_written=("codedFixedValue p (inert on 0 faces) + inletOutlet U" if mode == "resistance" else "zeroGradient p + noSlip U (no flow imposed)"), monitors="none (0 faces: fatal in v2406)")
                                       for o in lost],
                 bc_bookkeeping=bc_bookkeeping(live, lost, mode), mesh_patches=bnd)
    binfo.update(info or {}); json.dump(binfo, open(f"{case}/build_info.json", "w"), indent=1)
    return binfo

def outlet_record(o):
    return dict(patch=o["patch"], code_name=o["code_name"], R_used=o.get("R"), R_ref=o.get("R_ref"), relax=o.get("relax"), Q_target_m3s=o["Q_target_m3s"], R_own=o.get("R_own"), G=o.get("G"),
                **{k: o[k] for k in ("tree_node", "territory_id", "p_init_kin") if k in o})

def bc_bookkeeping(live, lost, mode):
    """territory accounting of bc_C / bc_A over the outlets that exist in the mesh; a lost outlet's territory is CLOSED (no flow), so the sum of the bc_C targets of the existing outlets is what the case can deliver"""
    qa, ql = sum(o["Q_target_m3s"] for o in live), sum(o["Q_target_m3s"] for o in lost)
    return dict(n_outlets_package=len(live) + len(lost), n_outlets_in_mesh=len(live), outlets_in_mesh=[o["patch"] for o in live], outlets_lost_in_mesh=[o["patch"] for o in lost],
                bcC_Q_target_total_mls=(qa + ql) * 1e6, bcC_Q_target_in_mesh_mls=qa * 1e6, bcC_Q_target_lost_mls=ql * 1e6,
                bc_error_criteria_over="the outlets in the mesh only" + (f" ({len(live)} of {len(live) + len(lost)})" if lost else ""),
                lost_territory=("CLOSED: the territory of " + ", ".join(o["patch"] for o in lost) + " receives no flow (Q = 0 reported, flag OUTLET_LOST_IN_MESH); its bc_C target is not delivered and its bc_A R"
                                + (" is not applied (the coded BC on an empty patch does nothing)" if mode == "resistance" else " is not used (no flow imposed)")) if lost else None)

# ---------------- reading results (monitors are the source of truth)
def value_column(path):
    """index of the value column of a surfaceFieldValue .dat: the header '# Time <Area> <op(field)>' is parsed; with writeArea (the D8 plane monitors) column 1 is the sampled Area and the value is column 2"""
    hdr = None
    with open(path) as fh:
        for ln in fh:
            if not ln.startswith("#"): break
            if ln[1:].strip().startswith("Time"): hdr = ln[1:].split()
    if hdr is None: return 1
    cols = [i for i, h in enumerate(hdr) if h not in ("Time", "Area")]
    if len(cols) != 1: raise SystemExit(f"{path}: expected one value column, header {hdr}")
    return cols[0]

def series(case, name, col=None):
    f = f"{case}/postProcessing/{name}/0/surfaceFieldValue.dat"; d = np.loadtxt(f, comments="#", ndmin=2)
    return d[:, 0], d[:, value_column(f) if col is None else col]

def last_mean(case, name, n=100):
    t, v = series(case, name); w = v[-n:]
    return float(w.mean()), float((w.max() - w.min()) / abs(w.mean()) * 100 if w.mean() != 0 else np.nan), int(t[-1])

def derive_R(case, patches, n=100):
    """R_i = (pbar_i*rho - Pv)/Q_i from the last-n means of the outlet-patch area-average p (kinematic) and flux monitors; returns dict patch -> dict"""
    out = {}
    for p in patches:
        pbar, pband, it = last_mean(case, f"{p}Pressure", n); Q, qband, it2 = last_mean(case, f"{p}Flux", n)
        assert it == it2, "monitor length mismatch"
        if not Q > 0: raise SystemExit(f"{p}: mean outlet flux {Q} not positive (outflow +)")
        out[p] = dict(p_bar_kin=pbar, p_bar_Pa=pbar * RHO, p_band_pct=pband, Q_m3s=Q, Q_band_pct=qband, R_derived=(pbar * RHO - PV) / Q, last_iteration=it)
    return out

def zerod_stub():
    """analyze_solve.py imports RHO, P_VEN, P_AORTA from zerod_ffr. The scan-14 code path must never import the 0D twin: register a constants-only stand-in BEFORE importing analyze_solve."""
    m = types.ModuleType("zerod_ffr"); m.RHO, m.P_VEN, m.P_AORTA = RHO, PV, P_AORTA_PA; m.IS_CONSTANTS_STUB = True
    return m
