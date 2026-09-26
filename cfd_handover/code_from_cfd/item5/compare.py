"""Item 5 verification: compare pimpleFoam's own outlet-pressure monitor against an independent
scipy RK45 solve of the same RCR ODE, over the second cycle only."""
import numpy as np
from scipy.integrate import solve_ivp
from pathlib import Path

R1, R2, C, Pv, rho = 5e8, 5e9, 1e-10, 0.0, 1060.0

def Qfun(t):
    return 0.5e-6 + 1.0e-6 * np.sin(2 * np.pi * 1.0 * t)

def rhs(t, y):
    pc = y[0]
    return [(Qfun(t) - (pc - Pv) / R2) / C]

sol = solve_ivp(rhs, [0, 2.0], [0.0], max_step=1e-4, dense_output=True, rtol=1e-10, atol=1e-12)

CASE = Path("/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item5_rcr_verify/case")
pp_dirs = sorted((CASE / "postProcessing" / "outletPatchPressure").glob("*"))
assert pp_dirs, "no outletPatchPressure postProcessing output found"
t_of, p_of_kin = [], []
for d in pp_dirs:
    # OpenFOAM appended "_0" to avoid clobbering the pre-existing serial-smoke-test file at the
    # same path - glob for any surfaceFieldValue*.dat, not just the un-suffixed name, and use the
    # largest one (the real 17k+ timestep run, not the 7-line smoke-test leftover).
    candidates = sorted(d.glob("surfaceFieldValue*.dat"), key=lambda p: p.stat().st_size)
    if not candidates:
        continue
    f = candidates[-1]
    for line in f.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        t_of.append(float(parts[0])); p_of_kin.append(float(parts[1]))
t_of = np.array(t_of); p_of_kin = np.array(p_of_kin)
order = np.argsort(t_of); t_of = t_of[order]; p_of_kin = p_of_kin[order]
p_of = p_of_kin * rho   # back to Pa

flux_dirs = sorted((CASE / "postProcessing" / "outletFlux").glob("*"))
t_q, q_of = [], []
for d in flux_dirs:
    candidates = sorted(d.glob("surfaceFieldValue*.dat"), key=lambda p: p.stat().st_size)
    if not candidates:
        continue
    f = candidates[-1]
    for line in f.read_text().splitlines():
        if line.startswith("#") or not line.strip():
            continue
        parts = line.split()
        t_q.append(float(parts[0])); q_of.append(float(parts[1]))
t_q = np.array(t_q); q_of = np.array(q_of)
oq = np.argsort(t_q); t_q = t_q[oq]; q_of = q_of[oq]

mask2 = t_of >= 1.0
t2 = t_of[mask2]; p_of2 = p_of[mask2]
pc_ref2 = sol.sol(t2)[0]
p_ref2 = R1 * Qfun(t2) + pc_ref2

err = np.abs(p_of2 - p_ref2)
rel_err = err / np.max(np.abs(p_ref2))
print(f"n samples in cycle 2: {len(t2)}")
print(f"max relative error over cycle 2: {rel_err.max()*100:.4f}%")
print(f"mean relative error over cycle 2: {rel_err.mean()*100:.4f}%")
print(f"pass (<0.5%): {rel_err.max() < 0.005}")

# backflow window check (Q<0, roughly t mod 1 in [210/360,330/360)*1s i.e. ~[0.583,0.917) each cycle)
backflow_mask = Qfun(t2) < 0
print(f"\nbackflow samples in cycle 2: {backflow_mask.sum()} / {len(t2)}")
if backflow_mask.sum() > 0:
    print(f"  max |p_OF| during backflow: {np.abs(p_of2[backflow_mask]).max():.2f} Pa")
    print(f"  max rel error during backflow: {rel_err[backflow_mask].max()*100:.4f}%")
    print(f"  any NaN/inf in p_OF during backflow: {not np.all(np.isfinite(p_of2[backflow_mask]))}")

print(f"\noverall p_OF range: [{p_of.min():.2f}, {p_of.max():.2f}] Pa")
print(f"any NaN/inf anywhere in p_OF: {not np.all(np.isfinite(p_of))}")
print(f"total simulated time reached: {t_of.max():.4f} s (target 2.0 s)")

# flow-Q cross-check: does the CFD's own outlet flux track the prescribed Q(t)? (mass conservation
# through a rigid incompressible pipe means it should, independent of the outlet BC)
q_ref_at_tq = Qfun(t_q)
q_err = np.abs(q_of - q_ref_at_tq) / np.max(np.abs(q_ref_at_tq))
print(f"\noutlet flux vs prescribed Q(t): max rel diff = {q_err.max()*100:.4f}% (sanity check, not the pass criterion)")
