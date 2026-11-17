#!/usr/bin/env python3
"""Lower-case study (docs/ru/37_lower_case_study.md): for each variant find the lowest front height FRONT_Z at which
fit_model.py reports no collision (overlap > 0.05 mm), and what collides first below it.
Variants are env settings of fit_model.py; nothing here changes the default model.
Run: python lower_case_study.py [variant ...]   (no argument = all)   Python: KiCad 10 python, never kicad-cli."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KEYS = ("FRONT_Z", "COMPUTER", "H5_STANDOFF", "H5_H", "H5_X", "H5_Y", "PANEL_GAP", "P2_GAP", "P2_PARTS", "WHEEL_TRACK", "F1_MODE",
        "F1_TOP", "REAR_JACK_TOP", "REAR_JACK_TOP_R", "R2_TALL_X1", "R1_TOP", "R2_TOP", "BACK_H", "WHEEL_Y", "DECK", "FRONT_LIP", "REAR_SHIFT", "H5T_X", "H5T_S0", "H5T_N", "H5_PORT", "H5_PORT_LEN", "BATT_LIPO", "LIPO_H", "PANEL_PARTS", "F1_SIDE_Z", "BATT_FLAT", "PW_X0", "A1_X0", "A1_Y0", "H5_REAR_X", "H5_REAR_Y", "H5_Z0", "BATT_BOXES", "FAN")


def run(env, z):
    for k in KEYS:
        os.environ.pop(k, None)
    os.environ.update({k: str(v) for k, v in env.items()})
    os.environ["FRONT_Z"] = str(z)
    spec = importlib.util.spec_from_file_location("fm_%s" % str(z).replace(".", "_"), os.path.join(HERE, "fit_model.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    res = m.check(m.parts())
    return [r for r in res if r[0] < -0.05]


def pairs(col):
    return "; ".join(f"{a} / {b} {abs(g):g}" for g, a, b, e in col)


def lowest_clear(env, hi=68.0, lo=30.0, step=0.25):
    """Walk down from hi; the lowest z with no collisions on the way (the first collision stops the walk)."""
    z, last = hi, None
    while z >= lo:
        col = run(env, z)
        if col:
            return last, z, col
        last, z = z, round(z - step, 2)
    return last, None, []


H5R = dict(COMPUTER="H5REAR")
VARIANTS = {
    "V0 base (H5 under P2)": {},
    "V1 wheel follows skin": dict(WHEEL_TRACK=1),
    "V2 + F1 horizontal (P94)": dict(WHEEL_TRACK=1, F1_MODE="H"),
    "V3 + P2 parts under 4 -> 2 mm": dict(WHEEL_TRACK=1, F1_MODE="H", P2_PARTS=2),
    "V4 + P2 gap 6.5 -> 4.5": dict(WHEEL_TRACK=1, F1_MODE="H", P2_GAP=4.5),
    "V5 + H5 standoff 0": dict(WHEEL_TRACK=1, F1_MODE="H", H5_STANDOFF=0),
    "V6 H5 rear (as before) + V2": dict(WHEEL_TRACK=1, F1_MODE="H", **H5R),
    "V7 H5 rear + flat battery": dict(WHEEL_TRACK=1, F1_MODE="H", BATT_FLAT=1, **H5R),
}

if __name__ == "__main__":
    want = sys.argv[1:]
    for name, env in VARIANTS.items():
        if want and not any(name.startswith(w) for w in want):
            continue
        ok, bad, col = lowest_clear(env)
        print(f"{name}: lowest clear FRONT_Z = {ok}; first collision at {bad}: {pairs(col)}", flush=True)
