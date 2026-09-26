# RCR (3-element Windkessel) outlet BC, Crank-Nicolson form - Item 5, PASS (OpenFOAM ESI v2406, `pimpleFoam`)

Source: `item5_rcr_verify/design.md` and `item5_rcr_verify/case/0/p` (scratchpad); reference check `item5_rcr_verify/compare.py` (scipy RK45 of the same ODE).
Model: `p(t) = R1 Q(t) + pC(t)`, `dpC/dt = (Q - (pC - Pv)/R2)/C`; test values `R1 = 5e8`, `R2 = 5e9` Pa s/m^3, `C = 1e-10` m^3/Pa (tau = 0.5 s), `Pv = 0`.
The pressure applied on every corrector call is algebraic from the CURRENT flux and the state frozen at the start of the step; the internal state (`pC_n`, `Q_n`) is
advanced ONCE per real time step (a Crank-Nicolson closed form), never mid-corrector:
```cpp
outlet
{
    type            codedFixedValue;
    value           uniform 0.0;
    name            RCROutlet;
    codeInclude #{ #include "Time.H" #};
    code
    #{
        const scalar R1 = 5e8, R2 = 5e9, C = 1e-10, Pv = 0.0, rho = 1060.0;
        static scalar pC_n = 0.0;       // capacitor state at the START of the current step (Pa)
        static scalar Q_n  = 0.0;       // flux at the start of the step (m^3/s)
        static scalar tLast = -1.0;     // time the state was last advanced
        const scalar t  = this->db().time().value();
        const scalar dt = this->db().time().deltaT().value();
        const fvsPatchField<scalar>& phip = patch().lookupPatchField<surfaceScalarField, scalar>("phi");
        const scalar Q = gSum(phip);    // + = outflow
        const scalar tau = R2 * C;
        const scalar a = dt / (2.0 * tau);
        const scalar pC_trial = ((1.0 - a) * pC_n + (dt / (2.0 * C)) * (Q_n + Q) + (dt / tau) * Pv) / (1.0 + a);
        const scalar pTarget = (R1 * Q + pC_trial) / rho;      // kinematic
        operator==(pTarget);
        if (t > tLast + 0.5 * dt) { pC_n = pC_trial; Q_n = Q; tLast = t; }   // commit only at a genuinely new time
    #};
}
```
Companion: outlet `U` = `inletOutlet` (`inletValue (0 0 0)`), forcing U = 0 on inward-flux faces (backflow); inlet `flowRateInletVelocity` with `Q(t) = Q0 + Q1 sin(2 pi f t)`, `Q0 = 0.5e-6`, `Q1 = 1e-6` m^3/s, `f = 1` Hz.
Numerics: `PIMPLE { nOuterCorrectors 1; nCorrectors 2; nNonOrthogonalCorrectors 0; momentumPredictor yes }`, `ddt Euler`, adjustable step (Courant target 0.5), solver entries `"(p|pFinal)"`, `"(U|UFinal)"`.
Result (report section 11.x, Item 5): 2 cycles on the Stage A pipe (61,440 cells), 17,316 steps, cycle-2 max relative error against scipy 0.2827 % (mean 0.042 %; tolerance 0.5 %),
1,195 of 8,656 cycle-2 samples with Q < 0 (backflow), no instability. Independent check: analytic scipy vs the 10 ms-step CN form 0.011 %.
Known limits (stated, not fixed): the `static` state is not patch-local (a second RCR outlet with the same coded name would corrupt it) and does not survive a restart; production use needs an
`IOdictionary`-backed state keyed by patch name. Operational note: a stale `postProcessing` file from a serial compile smoke test was picked up by a glob - use the largest matching file.
