#!/usr/bin/env python3
"""The low case as agreed on 16.11.2026 (docs/ru/39_low_case_plan.md): step case, deck 22, lip 28 with Cliff S1 jacks, H5 rear right
(ports to the right, 4 mm to R1, 8 mm under it for RAM / M.2), one LiPo pack on the floor hatch under A1, A1 on a tray,
60 mm fan on the right wall. For each shelf lengthening: the lowest fold without collisions and what stops it.
Run: python low_case_final.py   (KiCad 10 python, never kicad-cli)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lower_case_study as L  # noqa: E402

L.KEYS = tuple(dict.fromkeys(L.KEYS + ("JACK_H", "JACK_W", "F1_STAND", "M1_J1_H", "A1_Z0", "BATT_BOXES", "FAN")))


def config(rs, deck=22.0, h5_stand=8.0):
    a1y = 305 + rs
    return dict(WHEEL_TRACK=1, COMPUTER="H5REAR", BATT_LIPO=0, P2_PARTS=1.5, PANEL_PARTS=3, PW_X0=245, A1_X0=20, H5_PORT="E",
                F1_MODE="LIP", FRONT_LIP=28, REAR_SHIFT=rs, DECK=deck, H5_REAR_X=410, H5_REAR_Y=413.4 + rs - 4.0 - 60,
                H5_STANDOFF=h5_stand, JACK_H=12.7, JACK_W=15.9, F1_STAND=1, M1_J1_H=5, A1_Z0=20,
                BATT_BOXES=f"40,210,{a1y},{a1y + 100},3", FAN=f"{400 + rs - 20},4,60")


def lowest_fold(env, hi=70.0, lo=36.0):
    f, last = hi, None
    while f >= lo:
        col = L.run(env, f)
        if col:
            return last, f, col
        last, f = f, round(f - 1, 2)
    return last, None, []


if __name__ == "__main__":
    for rs in (20, 40, 60):
        for st in (3, 8):
            ok, bad, col = lowest_fold(config(rs, h5_stand=st))
            print(f"shelf +{rs}, H5 standoff {st}: lowest fold {ok} (rear {ok + 75 if ok else None}, depth {460 + 28 + rs}); "
                  f"at {bad}: {L.pairs(col)[:170]}", flush=True)
