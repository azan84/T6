# Resistance outlet BC, TRANSIENT (`pimpleFoam`) - what was used, what has NOT been run

## A. Direct-impose version (Item 6, pulsatile cost pilot) - used
File: `item6_pulsatile_pilot/sten60_pulsatile/0/p` (scratchpad; template reproduced below). Case: sten60, 8 ranks, Co 3-5 and Co 1 runs (cost timing only; the runs
were stopped, see report section 11.4/11.7). Same law as the steady BC, applied directly, no `prevIter()`:
```cpp
outlet
{
    type            codedFixedValue;
    value           uniform 9.5265;
    name            resistanceOutletS60pulsatile;
    code
    #{
        const scalar R     = 6.975221e9;
        const scalar Pv    = 666.61;
        const scalar rho   = 1060.0;
        const fvsPatchField<scalar>& phip =
            patch().lookupPatchField<surfaceScalarField, scalar>("phi");
        const scalar Q = gSum(phip);
        const scalar pTarget = (Pv + R*Q)/rho;
        operator==(pTarget);        // NO relaxation against p.prevIter()
    #};
}
```
Numerics used with it (`stageA/caseTemplate_transient/system/`): `ddtSchemes Euler`, `PIMPLE { nOuterCorrectors 3; nCorrectors 2; nNonOrthogonalCorrectors 1; momentumPredictor no; }`,
adjustable time step (`adjustTimeStep on; maxCo 5`), **no `relaxationFactors` block**, and solver entries for BOTH `"(p|pFinal)"` and `"(U|UFinal)"`
(`pimpleFoam` looks up `UFinal`/`pFinal` on the last outer corrector; a missing entry aborts the run). Inlet: `flowRateInletVelocity` with a `Function1::table` waveform.

## B. Explicit-lag version for the lesion80 steady-solution check (`pipeline/`-side: `build_pimple_case.py`, scratchpad `item3_M1_pilot/`) - NOT RUN
Same law and same `operator==((Pv + R*Q)/rho)` with `Q = gSum(phi)` of the current call (block `P_OUT` in `build_pimple_case.py`, `name resX`). It was BUILT and audited
(design `transient_design.md`, launcher `run_pimple.sh`, analysis `pimple_analyse.py` in the scratchpad) but **no solver has been run on `pimple_lesion80`**: treat it as untested.
Its numerics: `ddt backward`, `PIMPLE { nOuterCorrectors 2; nCorrectors 2; nNonOrthogonalCorrectors 1; momentumPredictor yes }`, `linearUpwind grad(U)` (unbounded), dt 2.5e-5 s, maxCo 0.8.
Stability of the explicit coupling is only ESTIMATED for one outlet (time-step limit about 2 rho L/(A R) = 1.7e-3 s >> dt); it is not proven for the multi-outlet PIMPLE loop.
The copied steady solution is not an exact fixed point of the transient discretisation (patch-value mismatch up to 5e-6 relative, unbounded vs bounded convection).

## C. Which is which
| | steady BC | Item 6 (A) | pimple_lesion80 (B) |
|---|---|---|---|
| solver | simpleFoam | pimpleFoam | pimpleFoam |
| relaxation vs prevIter() | yes, needs `p` in relaxationFactors | none | none |
| status | confirmed on real runs | ran (cost pilot) | built + audited, NOT run |
