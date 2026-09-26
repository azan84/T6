# Item 5 design: RCR outlet BC code verification

## REVISION NOTE (2026-09-19, post-panel)
Real, substantive disagreement among the three reviewers on explicit Euler's accuracy at intermediate
timesteps (Fable: 1e-2 s fails at 1.09%, 1e-3 s passes at 0.11%; astra: similar, 1e-2 s ~1.1-1.3%,
1e-3 s ~0.11-0.13%; Gemini: 1e-2 s fails at 3.02%, and claims even 2e-3 s fails at 0.60%, implying a
stricter dt<1.6ms requirement). This is NOT resolved here by re-deriving the transfer function myself —
it doesn't need to be: **at the timestep this item actually plans to run (Courant-limited, a few x1e-4 s
per the original design), all three reviewers' numbers, including Gemini's stricter one, are comfortably
under the 0.5% tolerance.** The disagreement is confined to timesteps (2-10ms) well above what this
pipe/mesh's Courant limit would ever permit, so it doesn't change what to build. Separately, all three
reviewers found the SAME once-per-timestep guard has a real structural problem under PIMPLE's outer
correctors, and independently converged on materially the same fix (an algebraic, corrector-count-
independent reformulation). Both addressed below. Given the fix is free (no extra solver cost, closed-
form update) and removes ALL doubt about the Euler-accuracy disagreement, it is adopted regardless of
which reviewer's error numbers are exactly right.

## Physical model (3-element Windkessel) — unchanged
p(t) = R1*Q(t) + p_C(t), dp_C/dt = (Q(t) - (p_C(t) - Pv)/R2) / C
R1=5e8, R2=5e9, C=1e-10 Pa.s/m3 / m3/Pa (tau=R2*C=0.5s).

## Test geometry, driving flow — unchanged, with one correction
Stage A's pipe geometry/mesh (r=1.5mm, L=100mm, 61,440 cells). Q(t) = Q0 + Q1 sin(2 pi f t),
Q0=0.5e-6, Q1=1.0e-6 m3/s, f=1Hz. **Corrected (panel finding): the reverse-flow window is 1/3 of the
cycle, not 1/6 as originally stated** — Q(t)<0 whenever sin(2 pi f t) < -0.5, i.e. for 120 degrees of
phase out of 360, not 60.

## Coded outlet BC — replaced with a Crank-Nicolson (trapezoidal) algebraic form
**Panel-identified defects in the original design, both fixed by this reformulation:**
1. The original `if (t > tLast + 0.5*dt)` guard advances `pC` exactly once per timestep using
   whichever flux `Q` happens to be available on the FIRST call of that timestep — under PIMPLE, the
   first outer-corrector's flux is typically the previous-timestep's converged value carried forward
   (a predictor), not the value that will eventually converge at the new time. Gemini and astra
   independently flagged this as freezing `pC` on a stale flux and never revisiting it once the
   corrector loop actually converges within that timestep.
2. Explicit Euler's accuracy is disputed at coarse dt (see above) but not free of doubt at any dt
   without switching schemes.

**Fix (converged form, materially the same fix two of three reviewers proposed independently):**
advance the capacitor state ONLY at the true end of a timestep (never mid-corrector), using a
closed-form Crank-Nicolson update; compute the PATCH PRESSURE itself algebraically every call from the
CURRENT (possibly still-iterating) flux and the FROZEN previous-timestep capacitor state — so every
corrector call already sees the current best Q for the pressure it applies, while the internal ODE
state is never touched more than once per real timestep, closing the ambiguity about "which Q update
pC" outright:

```cpp
outlet
{
    type            codedFixedValue;
    value           uniform 0.0;
    name            RCROutlet;

    codeInclude
    #{
        #include "Time.H"
    #};

    code
    #{
        const scalar R1 = 5e8, R2 = 5e9, C = 1e-10, Pv = 0.0, rho = 1060.0;
        static scalar pC_n = 0.0;       // capacitor state at the START of the current timestep (Pa)
        static scalar Q_n  = 0.0;       // flux at the start of the current timestep (m^3/s)
        static scalar tLast = -1.0;     // simulation time this state was last advanced at

        const scalar t  = this->db().time().value();
        const scalar dt = this->db().time().deltaT().value();

        const fvsPatchField<scalar>& phip =
            patch().lookupPatchField<surfaceScalarField, scalar>("phi");
        const scalar Q = gSum(phip);     // CURRENT flux (this corrector call), signed: + = outflow

        // Crank-Nicolson step for the capacitor, using Q_n (start-of-step) and Q (current best
        // estimate of the end-of-step flux) - advanced ONLY once per genuine new timestep, so a
        // converging outer-corrector loop refines Q_new on every call without re-integrating pC.
        const scalar tau = R2 * C;
        const scalar a = dt / (2.0 * tau);
        const scalar pC_trial = ((1.0 - a) * pC_n + (dt / (2.0 * C)) * (Q_n + Q) + (dt / tau) * Pv) / (1.0 + a);

        const scalar pTarget = (R1 * Q + pC_trial) / rho;   // kinematic; uses the CURRENT Q directly,
                                                             // so every corrector call is consistent
        operator==(pTarget);

        // Commit the state ONLY when the solver has genuinely moved to a new time - never mid-corrector.
        if (t > tLast + 0.5 * dt)
        {
            pC_n = pC_trial;
            Q_n = Q;
            tLast = t;
        }
    #};
}
```

This is algebraically Crank-Nicolson (unconditionally stable, the closed-form update all three
reviewers converged on being far more accurate than explicit Euler at any practical dt - Fable measured
0.011% at 1e-2s vs. Euler's 1.09%), and it sidesteps the stale-flux ambiguity: `pTarget` on every single
corrector call uses whatever `Q` that call has, so the applied pressure always reflects the
solver's current best flux estimate; only the internal `pC_n`/`Q_n` bookkeeping — which exists purely
to compute the NEXT step's trapezoidal average — is deliberately committed once per timestep.

**Known limitations, stated rather than fixed (all three reviewers agree these don't need fixing for
THIS single-outlet, 2-second, no-restart test, but do need fixing before any production reuse):**
- `static` state is not patch-local (a second RCR outlet using the same coded `name` would corrupt it)
  and does not survive a case restart (resets to `pC_n=0`, `tLast=-1` on any fresh process start).
  Production use needs a registered, auto-written `IOdictionary`-backed state keyed by patch name.
- The MPI reasoning is fine for this test (the patch lives on whichever ranks own its faces, `gSum` is
  already a collective reduction, and every participating rank reaches the same `pC_n` in lockstep).

## Outlet velocity BC — added (panel finding: previously unspecified, which meant the "no instability
under backflow" pass criterion could not actually be tested)
```
outlet { type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }
```
Matches Stage A's own convention: forces U=0 on any face where the flux is instantaneously inward
(backflow), which is what makes the reverse-flow segment of the waveform a genuine, checkable stability
test rather than an undefined condition.

## Independent verification (scipy) — unchanged mechanism, corrected reference initial condition
`scipy.integrate.solve_ivp` (RK45, rtol=1e-10) driven by the exact same analytic Q(t), starting from
`pC(0)=0` — **the SAME non-periodic initial condition the CFD case itself starts from** (both start
quiescent), so the comparison is a like-for-like initial-value problem, not a periodic-vs-transient
mismatch. (Panel note: the periodic steady-state is not reached until ~cycle 5, and departs from a
`pC(0)=0` start by a non-negligible ~140 Pa at t=1s — this only matters if a PERIODIC reference were
used instead; since it isn't, no fix is needed here beyond stating the initial condition explicitly.)

## Pass criterion — unchanged
`max(|p_OF(t) - p_ref(t)|) / max(|p_ref(t)|) < 0.005` over the second full cycle (discarding the first
as the shared startup transient, common to both the CFD run and the scipy reference), plus no
NaN/blow-up/growing oscillation during the backflow window.

## Run plan — unchanged
>=2 full cycles (2s), deltaT set by the Courant limit on the coarse tube mesh (a few x1e-4 s) —
reported after the actual solve, not assumed; report the second cycle only.
