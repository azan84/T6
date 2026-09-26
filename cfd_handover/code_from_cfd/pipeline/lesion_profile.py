"""Lesion profile: the location/severity constants of the lesion pipeline, selected by the environment variable LESION_PROFILE (default 'lesion80' = the audited proximal-LAD lesion;
every script that imports them behaves exactly as before under the default). 'lesion_mid' = an isolated lesion in the LAD segment between the D1 and D2 ostia (design: lesion_mid_design.md).
Arcs are mm along the smoothed root->LAD path (same convention as before). lesion_mid: D1 ostium at smoothed arc 32.04 mm, D2 ostium at 69.25 mm (measured by projecting the branches' first points on the smoothed path); the frames end at 74.13 mm, so analysis windows stop at 71 mm.
LABEL / JUNCTION_NAME: text of figure labels and outcome strings (the lesion name and the branch whose ostium censors the reattachment; JUNCTION is its proximal edge)."""
import os
PROFILES = {
    "lesion80": dict(DIR="lesion80", OPEN="lesion80_open.vtp", S_C=23.5, LEN=10.0, DS=0.80, SID=2, KEEP=60.0,
                     SEC_START=1.0, SEC_END=50.0, WSS_START=15.0, WSS_END=45.0, JUNCTION=30.0, JUNCTION_OSTIUM=32.05, S_UP=18.5, S_DOWN=29.5,
                     XLIM=(15, 40), TUBE_START=17.5, TUBE_END=36.0, D1_CHAIN=True, JET_END=32.0, LOCAL_LO=17.5, LOCAL_HI=32.0,
                     BL_STATIONS=(8.0, 18.5, 21.0, 22.5, "S_C", 24.5, 26.0, 28.5, 31.0), TUBE_LO=18.5, TUBE_HI=32.0,
                     LABEL="lesion80", JUNCTION_NAME="D1"),
    "lesion_mid": dict(DIR="lesion_mid", OPEN="lesion_mid_open.vtp", S_C=48.0, LEN=10.0, DS=0.72, SID=3, KEEP=76.0,
                       SEC_START=34.0, SEC_END=71.0, WSS_START=36.0, WSS_END=71.0, JUNCTION=67.0, JUNCTION_OSTIUM=69.25, S_UP=43.0, S_DOWN=54.0,
                       XLIM=(39, 72), TUBE_START=41.0, TUBE_END=68.0, D1_CHAIN=False, JET_END=64.0, LOCAL_LO=41.0, LOCAL_HI=64.0,
                       BL_STATIONS=(36.0, 43.0, 45.5, 47.0, "S_C", 49.0, 51.0, 54.0, 58.0), TUBE_LO=43.0, TUBE_HI=64.0,
                       LABEL="lesion_mid", JUNCTION_NAME="D2"),
}
NAME = os.environ.get("LESION_PROFILE", "lesion80")
if NAME not in PROFILES:
    raise SystemExit(f"unknown LESION_PROFILE {NAME!r}; expected one of {list(PROFILES)}")
PR = PROFILES[NAME]
