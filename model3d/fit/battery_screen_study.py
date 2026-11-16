#!/usr/bin/env python3
"""Step case with the batteries under the screen instead of under the pads (user, 16.11.2026): one or two flat LiPo packs
170 x 100 x 12 on a 2 mm shelf above A1 / PW, a 92 mm exhaust fan on the right wall above the H5, H5 4 mm from R1.
Prints: where the packs fit, the lowest deck once nothing lies under P2, and the lowest fold.
Run: python battery_screen_study.py   (KiCad 10 python, never kicad-cli)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lower_case_study as L  # noqa: E402

RS = 20.0
H5Y = 413.4 + RS - 4.0 - 60          # H5 4 mm in front of R1 (was 0.9)
BASE = dict(WHEEL_TRACK=1, COMPUTER="H5REAR", BATT_LIPO=0, P2_PARTS=1.5, PANEL_PARTS=3, H5_REAR_X=410, H5_REAR_Y=H5Y, PW_X0=245,
            A1_X0=20, H5_PORT="E", F1_MODE="LIP", FRONT_LIP=28, REAR_SHIFT=RS, DECK=28)


def packs(n, y0, z0):
    xs = [(10, 180), (178, 348)][:n]
    return ";".join(f"{a},{b},{y0},{y0 + 100},{z0}" for a, b in xs)


def clear(env, fold):
    return L.run(env, fold)


if __name__ == "__main__":
    fold = 56.0
    print("0) base, no packs:", L.pairs(clear(BASE, fold)) or "clear", flush=True)
    found = {}
    for n in (1, 2):
        for z0 in (29, 30, 32, 34, 36, 38, 40):
            for y0 in (325, 330, 335, 340, 345):
                col = clear(dict(BASE, BATT_BOXES=packs(n, y0, z0)), fold)
                if not col:
                    found.setdefault(n, (y0, z0))
                    break
            if n in found:
                break
        print(f"{n} pack(s): first clear (y0, shelf z) = {found.get(n)}", flush=True)
        if n not in found:
            print("   collisions at y0 345, z0 30:", L.pairs(clear(dict(BASE, BATT_BOXES=packs(n, 345, 30)), fold)), flush=True)
    n = max(found) if found else 0
    if n:
        y0, z0 = found[n]
        env = dict(BASE, BATT_BOXES=packs(n, y0, z0))
        for fy, fz in ((H5Y, 30), (H5Y, 20), (H5Y + 20, 25)):
            col = clear(dict(env, FAN=f"{fy},{fz}"), fold)
            print(f"fan at y {fy:.0f}, z {fz}-{fz + 92}:", L.pairs(col) or "clear", flush=True)
            if not col:
                env["FAN"] = f"{fy},{fz}"
                break
        deck, last = 28.0, None
        while deck >= 14:
            col = clear(dict(env, DECK=deck), fold)
            if col:
                print(f"lowest deck = {last}; at {deck}: {L.pairs(col)}", flush=True)
                break
            last, deck = deck, round(deck - 0.5, 2)
        f, lastf = 56.0, None
        while f >= 36:
            col = clear(dict(env, DECK=last or 28), f)
            if col:
                print(f"lowest fold (deck {last}) = {lastf}; at {f}: {L.pairs(col)}", flush=True)
                break
            lastf, f = f, round(f - 1, 2)
