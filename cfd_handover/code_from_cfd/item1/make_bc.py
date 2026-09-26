"""Generate 0/U and 0/p for item1's branched-tree case, both BC variants (hand-relax constants vs
the formula-based G=R/R_own relax rule - numerically identical per design.md's resolution of the
panel's start-up-instability finding, but exercising a different code path each time)."""
import sys, os
sys.path.insert(0, "/mnt/e/Paper6-T6/Paper6-T6/code")
from zerod_ffr import RHO, P_AORTA, P_VEN, MU
from build_0d import build_healthy_tree, Q_DEMAND
import numpy as np

T0, paths = build_healthy_tree()
C = T0.calibrate(Q_DEMAND)
ffr0, Q0, info0, sten0, K0 = T0.evaluate(C)

OUTLETS = {}
for v in T0.leaves:
    name = "outlet" + T0.label[v]
    R = C / T0.w[v]
    seg_mask = (T0.seg == T0.seg[v])
    L = T0.ds[seg_mask].sum(); r = T0.r_ref[v]
    R_own = 8 * MU * L / (np.pi * r ** 4)
    p_outlet_kin = (P_VEN + R * Q0[v]) / RHO
    OUTLETS[name] = dict(R=R, R_own=R_own, p_init=p_outlet_kin)

P0_KIN = P_AORTA / RHO

U_TEMPLATE = """FoamFile {{ version 2.0; format ascii; class volVectorField; object U; }}
dimensions [0 1 -1 0 0 0 0];
internalField uniform (0 0 0);
boundaryField
{{
    inlet   {{ type pressureInletOutletVelocity; value uniform (0 0 0); }}
{outlets}
    wall    {{ type noSlip; }}
}}
"""

U_OUTLET_BLOCK = "    {name} {{ type inletOutlet; inletValue uniform (0 0 0); value uniform (0 0 0); }}\n"

P_TEMPLATE = """FoamFile {{ version 2.0; format ascii; class volScalarField; object p; }}
dimensions [0 2 -2 0 0 0 0];
internalField uniform {p0};
boundaryField
{{
    inlet   {{ type totalPressure; p0 uniform {p0}; value uniform {p0}; }}
{outlets}
    wall    {{ type zeroGradient; }}
}}
"""

P_OUTLET_HAND = """    {name}
    {{
        type            codedFixedValue;
        value           uniform {p_init:.6f};
        name            hand{cname};
        code
        #{{
            const scalar R     = {R:.8e};
            const scalar Pv    = {Pv};
            const scalar rho   = {rho};
            const scalar relax = {relax:.8f};

            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            const scalar pTarget = (Pv + R*Q)/rho;

            const volScalarField& pFld = db().lookupObject<volScalarField>("p");
            const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);
            operator==((1.0 - relax)*pOld + relax*pTarget);
        #}};
    }}
"""

P_OUTLET_AUTO = """    {name}
    {{
        type            codedFixedValue;
        value           uniform {p_init:.6f};
        name            auto{cname};
        code
        #{{
            const scalar R     = {R:.8e};
            const scalar R_own = {R_own:.8e};
            const scalar Pv    = {Pv};
            const scalar rho   = {rho};
            const scalar G     = R / R_own;
            const scalar relax = min(0.5, 1.0/(1.0+G));

            const fvsPatchField<scalar>& phip =
                patch().lookupPatchField<surfaceScalarField, scalar>("phi");
            const scalar Q = gSum(phip);
            const scalar pTarget = (Pv + R*Q)/rho;

            const volScalarField& pFld = db().lookupObject<volScalarField>("p");
            const scalarField pOld(pFld.prevIter().boundaryField()[patch().index()]);
            operator==((1.0 - relax)*pOld + relax*pTarget);
        #}};
    }}
"""

def write_case(case_dir, variant):
    zpath = os.path.join(case_dir, "0")
    os.makedirs(zpath, exist_ok=True)
    u_outlets = "".join(U_OUTLET_BLOCK.format(name=n) for n in OUTLETS)
    with open(os.path.join(zpath, "U"), "w") as f:
        f.write(U_TEMPLATE.format(outlets=u_outlets))
    tmpl = P_OUTLET_HAND if variant == "hand" else P_OUTLET_AUTO
    p_outlets = "".join(
        tmpl.format(name=n, cname=n[6:].capitalize(), p_init=d["p_init"], R=d["R"], R_own=d["R_own"],
                    relax=min(0.5, 1.0 / (1.0 + d["R"] / d["R_own"])), Pv=P_VEN, rho=RHO)
        for n, d in OUTLETS.items()
    )
    with open(os.path.join(zpath, "p"), "w") as f:
        f.write(P_TEMPLATE.format(p0=f"{P0_KIN:.6f}", outlets=p_outlets))
    print(f"wrote {zpath}/U, {zpath}/p  (variant={variant})")

if __name__ == "__main__":
    for name, d in OUTLETS.items():
        print(f"{name}: R={d['R']:.6e} R_own={d['R_own']:.6e} relax={min(0.5,1/(1+d['R']/d['R_own'])):.6f} p_init={d['p_init']:.6f}")
    for ds in ("ds00", "ds60"):
        base = f"/tmp/claude-1000/-mnt-e-Paper6-T6/d3d689cf-6b0f-4d2a-a7a7-6e02a27b7588/scratchpad/item1_branched_tree/case_{ds}"
        write_case(base, "hand")
        write_case(base + "_auto", "auto")
