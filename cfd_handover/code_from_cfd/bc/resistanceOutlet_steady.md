# Resistance outlet BC, STEADY (`simpleFoam`) - the version actually used (OpenFOAM ESI v2406)

Source: `pipeline/build_solve_cases.py` (`P_OUT`, `P_T`, `U_T`, `terminal_R_own`, `build_case`). Confirmed on real hardware:
Stage A (sten00/50/70/80, A3/A4), Item 1 (3 outlets), Item 3 scan 837 (5 outlets; baseline, missed branch, lesion80 and follow-ups),
BC error of the patch pressure against `(P_v + R Q)/rho` <= 0.0011 % in every converged case of the 2026-09-24 work.
This supersedes `bc/resistanceOutlet.md` (which is still the pre-fix, never-compiled template).

## The BC (one `codedFixedValue` per outlet patch; one block per outlet in `0/p`)
```cpp
outlet_LAD                      // patch name from the mesh; every outlet has its own block
{
    type            codedFixedValue;
    value           uniform 9.9917414;          // INITIAL value = (Pv + R*Q0)/rho with Q0 from the 0D twin (or any sensible pressure)
    name            resLAD;                     // MUST be unique per outlet (see below)
    code
    #{
        const scalar R     = 9.17500181e+10;    // Pa s / m^3, LITERAL in the code string (see 'recompilation' below)
        const scalar Pv    = 666.61;            // Pa (venous pressure)
        const scalar rho   = 1060.0;
        const scalar relax = 0.07451627;        // per-outlet, from the rule below
        const fvsPatchField<scalar>& phip =
            patch().lookupPatchField<surfaceScalarField, scalar>("phi");
        const scalar Q = gSum(phip);            // outflow through the patch, + = out
        const scalar pTarget = (Pv + R*Q)/rho;  // kinematic pressure
        const volScalarField& pFld = db().lookupObject<volScalarField>("p");
        const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);
        operator==((1.0 - relax)*pOld + relax*pTarget);     // under-relaxation against the PREVIOUS ITERATION value
    #};
}
```
Companion entries used with it: inlet `p` = `totalPressure` (`p0 = P_aorta/rho = 11.319792`), inlet `U` = `pressureInletOutletVelocity`, outlets
`U` = `inletOutlet` (`inletValue (0 0 0)`), wall `U` = `noSlip`, wall `p` = `zeroGradient`. `nu = 3.773585e-6` (mu 0.004, rho 1060), laminar.

## Relaxation rule (audit-derived, measured, NOT a preference)
Per outlet i: `G_i = R_out,i / R_own,i`, `relax_i = min(0.5, 1/(1 + G_i))`, where `R_own,i` is the Poiseuille resistance of the outlet's own terminal vessel
(actual radii along its centreline, nodes of the segment up to the leaf) PLUS the resistance of the flow extension at the leaf radius
(`R = 8 mu L/(pi r^4)`, `terminal_R_own` in `build_solve_cases.py`). This is the practical form of the stability bound
`alpha < 2/(1 + R_outlet/R_epicardial)` - the MILDEST case (largest R_out/R_epi) is the hardest.
Values used: Stage A single outlet 0.05 (sten00) / 0.08 (sten50) / 0.20 (sten70) / 0.25 (sten80); Item 1 tree 0.0058 / 0.0064 / 0.0070 (the original hand
values 0.05 and 0.2 would diverge on a branched tree); scan 837 (5 outlets) 0.015-0.075 at the protocol demand and 0.05-0.21 at 3.16x that demand
(R_out falls, G falls, relax rises). Range seen in practice: 0.006 .. 0.25; the cap 0.5 was never reached. Default when in doubt: 0.05.

## Things that bite (all met on real runs)
1. **`p.prevIter()` needs `p` under `relaxationFactors`.** In `system/fvSolution` `relaxationFactors { fields { p 0.3; } equations { U 0.7; } }` MUST be
   present; without a `p` entry `storePrevIter()` is never called and `prevIter()` is a FatalError (this is also why the steady BC cannot be reused under
   `pimpleFoam` - see `resistanceOutlet_transient.md`).
2. **Unique `name` per outlet** (`resLCX`, `resIM`, ...). Two coded BCs with the same name collide in `dynamicCode/`.
3. **Compile once, serially, before `mpirun`.** The literal `R`/`relax` are in the code string, so each distinct set of numbers is a distinct library
   (SHA1 of the code). Run a 2-iteration serial `simpleFoam` first (`run_set.sh` does this and asserts one `libres<X>_*.so` per outlet and 6 entries in
   `dynamicCode`), then decompose and launch; otherwise the ranks race to `wmake` the same library.
4. **Initial value matters little but must exist**; `p_init = (Pv + R Q0)/rho` is used so that the first iterations do not see a huge mismatch.
5. **Flow extensions are NOT compensated**: the outlet patch sits 20 mm beyond the 0D leaf; the extension's own Poiseuille resistance is in series with `R_out`
   (about 1.7 % of `R_out` at protocol demand, about 6 % at 3.16x). A diagnostic (`solve_baseline_extcomp`, `R_out - R_ext`) showed it is not the cause of
   the 0D-3D differences at protocol demand.
6. Fixed iteration budget (3000), NO `residualControl`; convergence is judged from residuals < 1e-5 (all components) AND flux/pressure bands < 0.1 % over 200 iterations
   (`analysis/analyze_solve.py`, `launch/watch_converge.py`); stop a converged run with `foamDictionary system/controlDict -entry stopAt -set writeNow`.
7. Leaf-to-patch matching: each 0D leaf (plus 20 mm extension along its tangent) must lie within **3 mm** of its mesh patch centroid (`build_case` asserts this);
   `mode = closed` outlets of the analysis-side packages are WALLS (zero conductance), not outlets.
