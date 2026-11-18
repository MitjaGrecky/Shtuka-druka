#!/usr/bin/env python3
"""Step case (git history (docs/ru/38_low_case_rework.md, deleted 18.11.2026), section 3b): the deck is DECK mm high in front of the fold, the riser wall goes up to the old
68 mm, behind it the slope as before. H5 on the right behind the riser, ports to the right wall, R1 / R2 / A1 / PW moved back by REAR_SHIFT
(longer shelf), flat LiPo under P2 (R155), F1 on the left wall behind the riser.
Run: python step_case_study.py   (KiCad 10 python, never kicad-cli). Uses lower_case_study.run()."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lower_case_study as L

BASE = dict(WHEEL_TRACK=1, COMPUTER="H5REAR", BATT_LIPO=1, P2_PARTS=1.5, PANEL_PARTS=3,
            H5_REAR_X=410, PW_X0=245, A1_X0=20, H5_PORT="E", F1_MODE="LIP", FRONT_LIP=28)

def lowest_deck(env, hi=40.0, lo=22.0, step=0.5):
    # H5 is pushed against R1 / R2 (front edge of R1 = 413.4 + REAR_SHIFT), 0.9 mm clear
    env = dict(env, H5_REAR_Y=413.4 + env.get("REAR_SHIFT", 0) - 0.9 - 60)
    z, last = hi, None
    while z >= lo:
        col = L.run(dict(env, DECK=z), 68)
        if col:
            return last, z, col
        last, z = z, round(z - step, 2)
    return last, None, []

if __name__ == "__main__":
    for name, env in {"RS 12, pack 12": dict(BASE, REAR_SHIFT=12), "RS 20, pack 12": dict(BASE, REAR_SHIFT=20),
                      "RS 20, pack 10, P2 parts 1": dict(BASE, REAR_SHIFT=20, LIPO_H=10, P2_PARTS=1.0),
                      "RS 0 (no shelf change)": dict(BASE, REAR_SHIFT=0)}.items():
        ok, bad, col = lowest_deck(env)
        print(f"{name}: lowest clear DECK = {ok}; next at {bad}: {L.pairs(col)}", flush=True)
