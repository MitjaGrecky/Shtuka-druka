"""M4 - FX Mix + Filter module (2 encoders with 12-LED rings). Single source of truth for the schematic
and the board. Spec: hardware/for-routing/SPEC_boards.md, section M4 ("as M3").

Panel (layout_v7.json): knobs FX Mix x 355 and Filter x 389, y 277, knob 22 mm; board x 339-405, y 263-297 (66 x 34).
The knobs are only 34 mm apart, so the rings (r 14) leave 6 mm between them: the ICs sit on the bottom side
between the encoder pins (x 26-40), J1 at the front edge in the gap under the two ring openings.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "m4-fx-filter"
ID = "M4"
TITLE = "M4 - FX Mix + Filter module (2 encoders, 12-LED RGB rings)"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = "Module bus (R123): J1 to P3 (I2C channel 2 of P3's TCA9546A); chain: P3 buttons -> M2 -> M4"

X0, X1 = 339.0, 405.0
Y0, Y1 = 263.0, 297.0
W, H = X1 - X0, Y1 - Y0                      # 66 x 34
LAYERS = 2
KNOBS = [("FX Mix", 355.0, 277.0), ("Filter", 389.0, 277.0)]
KNOB_D = 22.0
RING_R = KNOB_D / 2 + 3.0                    # 14 mm (spec)
RING_N = 12
TOUCH = False                                # P102
HOLES = K.corner_holes(W, H) + [(W / 2, 2.6)]   # 66 mm: corners alone would be 60.8 apart (> 60), one more in the middle


def panel_to_board(px, py):
    return px - X0, Y1 - py


def knob_xy(k):
    return panel_to_board(*KNOBS[k][1:])


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.knob_pair(add, [k[0] for k in KNOBS], RING_N, holes=len(HOLES))
    return P


def placement():
    pl, t, b = {}, "top", "bottom"
    for k in range(2):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, t)
        for i in range(RING_N):
            x, y, a = K.ring_xy(cx, cy, RING_R, RING_N, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, t)
    mx = W / 2                                   # 33: between the switch pins of ENC1 (x 23) and pad A of ENC2 (x 42.5)
    pl["U1"] = (mx, 9.5, 0, b)
    for n, c in enumerate(("C3", "C4", "C5", "C6")):
        pl[c] = (mx + 4.5, 6.5 + 2.0 * n, 0, b)
    pl["R1"], pl["R2"] = (mx - 4.5, 7.0, 0, b), (mx - 4.5, 9.0, 0, b)
    pl["U2"] = (mx, 19.5, 90, b)
    pl["RN1"], pl["RN2"] = (mx - 5.0, 18.0, 90, b), (mx - 5.0, 21.0, 90, b)
    pl["C7"], pl["R3"] = (mx + 5.0, 18.5, 90, b), (mx + 5.0, 21.5, 0, b)
    pl["J1"] = (mx, H - 3.0, 90, b)              # front edge, in the gap of both ring openings
    pl["C1"], pl["C2"] = (mx - 6.5, H - 3.0, 90, b), (mx + 6.5, H - 3.0, 90, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", [p["ref"] for p in P if p["ref"] not in pl])
    for k in range(2):
        print(" ", KNOBS[k][0], "board", knob_xy(k))
