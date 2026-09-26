# Resistance outlet boundary condition — template

> **UNTESTED.** Written on a machine without OpenFOAM. Stage A check **A3** (p_outlet = P_v + R·Q to 0.1 %) is its
> acceptance test. Please send back whatever had to change, with the OpenFOAM version.

## What it does
Steady lumped microvascular bed at an outlet: **p = P_venous + R · Q**, with Q the volumetric outflow through the patch.
OpenFOAM's incompressible solvers carry **kinematic** pressure, so the value set on the patch is (P_v + R·Q)/ρ.
Under-relaxed, because p depends on the flux the solver is still converging.

## `0/p`
```
outlet                      // one block per outlet patch: outlet_1, outlet_2, ...
{
    type            codedFixedValue;
    value           uniform 0.62888;          // P_venous / rho, initial guess
    name            resistanceOutlet;         // must be unique per patch if R differs: resistanceOutlet_1, _2, ...

    code
    #{
        const scalar R     = 6.975e9;         // Pa s m^-3   <- R_out_SI from expected_0D.csv / outlets.csv
        const scalar Pv    = 666.61;          // Pa
        const scalar rho   = 1060.0;          // kg m^-3
        const scalar relax = 0.05;            // SEE THE STABILITY BOUND BELOW. 0.2 diverges on sten00.

        const fvsPatchField<scalar>& phip =
            patch().lookupPatchField<surfaceScalarField, scalar>("phi");   // m^3 s^-1 per face, + = outflow
        const scalar Q = gSum(phip);                                       // gSum: correct in parallel

        const scalar pTarget = (Pv + R*Q)/rho;                             // kinematic
        const scalarField pOld(*this);
        operator==((1.0 - relax)*pOld + relax*pTarget);
    #};
}
```
## The under-relaxation is a STABILITY BOUND, not a knob — read before running A3

The coupling p ← P_v + R·Q is a fixed-point iteration whose linear gain is −R/R_epicardial, so the update is stable
only for

    relax  <  2 / (1 + R_outlet/R_epicardial)

**On the Stage A `sten00` case that bound is 0.134, so the template's original 0.2 diverges** (gain −1.99). On the
real lumens the bound is ≈ 0.10. The counter-intuitive part, and the reason this is called out rather than left to
be discovered: **the MILDEST cases fail first.** A mild case has little epicardial resistance, so R_outlet/R_epi is
largest and the bound is tightest — `sten00` is the hardest case for this BC, not the easiest.

**Therefore: run A3 on `sten00` FIRST, at relax = 0.05.** If that is stable, everything else is. If a case still
oscillates, halve it rather than hunting; the cost is iterations, not accuracy, because the converged answer is
independent of `relax`.

## `0/U`
```
outlet  { type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }
inlet   { type pressureInletOutletVelocity; value uniform (0 0 0); }
wall    { type noSlip; }
```
`0/p` inlet: `type totalPressure; p0 uniform 11.3198;`  (= 11 998.98 Pa / 1060)

## Known version differences
- **ESI (.com) v2xxx:** as above. Newer releases prefer `patch().lookupPatchField<surfaceScalarField>("phi")`
  (single template argument) — if the two-argument form fails to compile, drop `, scalar`.
- **Foundation (.org) 9+:** same idea; `codedFixedValue` is supported, `lookupPatchField` signature as per that release.
- `system/controlDict` may need `libs ("libutilityFunctionObjects.so");` only if you add function objects; the coded BC
  itself compiles on first run (needs a working compiler and write access to `dynamicCode/`).

## Prescribed-flow mode (the first Protocol C solve, and check A4)
Replace the outlet's velocity BC with
```
outlet { type flowRateInletVelocity; volumetricFlowRate -1.1308e-6; value uniform (0 0 0); }   // negative = outflow
```
and set `0/p` on that patch to `zeroGradient`. Read the converged area-averaged patch pressure p̄ (kinematic) and derive
**R = (ρ·p̄ − P_v) / Q**. Re-solving with that R in resistance mode must reproduce Q (check A4, 0.5 %).
**With several outlets, prescribe EVERY outlet.** An earlier version of this file said to prescribe all but one and
leave the last as a pressure outlet "or the system is over-constrained against the total-pressure inlet". **That is
wrong.** The inlet is a `totalPressure` condition, so the inlet flow is an outcome, not a constraint: prescribing all
outlets fixes the total inflow and leaves the inlet pressure to satisfy it. Nothing is over-constrained.

It also matters more than it looks. Leaving one outlet free would make the first Protocol C solve match every outlet
flow **except one** — and on a corrupted geometry the free outlet absorbs the whole discrepancy, which is precisely
the effect this study exists to measure. **Flow-matched Protocol C is invalid on any multi-outlet case run that way.**

## Monitoring (add to `system/controlDict` functions)
A `surfaceFieldValue` with `operation sum` on `phi` for every outlet and the inlet, and `areaAverage` of `p` on each
probe plane (`sampledSurface` plane at the x positions in START-HERE). Convergence per the spec: residuals < 1e-5 **and**
inlet flow, each outlet flow and the measurement-plane pressure stable to < 0.1 % over 200 iterations.
