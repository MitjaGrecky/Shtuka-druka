"""M5 - Gain 1 + 2 module (2 encoders on the slope, in the window of W1). Single source of truth for the schematic
and the board. Spec: hardware/for-routing/SPEC_boards.md, section M5; W1: hardware/w1-levels/gen/design.py.

Panel (layout_v7.json): knobs Gain 1 x 32 and Gain 2 x 80 at y 379 (slope), knob 16 mm; Clip 1 and Clip 2 LEDs
at x 48 and 96, y 386. The board is 82 x 34 mm and sits in W1's window (W1 board x M5_X = 5-87, i.e. panel x 15-97),
centred on the Gain row. P103: rings of 11 LEDs + the 2 Clip LEDs = 24 RGB on one LP5864 (each Clip LED is the
12th position of its ring's CS triples). P102: no touch. J1 faces W1's J2 (W1 board x 46 = M5 x 41, front edge).
Slope: s = (panel_y - 300) / cos 30 along the slope from the fold. Board (KiCad, y down): origin at the rear-left
corner (high s), x = panel_x - X0, y = S1 - s.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "m5-gain"
ID = "M5"
TITLE = "M5 - Gain 1 + 2 module on the slope (2 encoders, 11-LED rings, Clip LEDs)"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = "Module bus (R123): J1 to W1's J2 (W1 passes the bus on; chain: P1 -> M3 -> W1 -> M5)"

COS = math.cos(math.radians(30.0))
W1_X0, M5_X = 10.0, (5.0, 87.0)              # W1 board edge in panel x; M5 outline in W1 board x (w1-levels design.py)
X0, X1 = W1_X0 + M5_X[0], W1_X0 + M5_X[1]   # panel x 15-97
W, H = X1 - X0, 34.0                         # 82 x 34
LAYERS = 2
KNOBS = [("Gain 1", 32.0, 379.0), ("Gain 2", 80.0, 379.0)]
CLIPS = [("Clip 1", 48.0, 386.0), ("Clip 2", 96.0, 386.0)]
KNOB_D = 16.0
RING_R = KNOB_D / 2 + 3.0                    # 11 mm (spec formula; layout_v7 draws a 21 mm ring)
RING_N = 11                                  # P103
TOUCH = False                                # P102


def s_of(py):
    return (py - 300.0) / COS


S1 = s_of(KNOBS[0][2]) + H / 2               # rear edge along the slope: the board is centred on the Gain row


def panel_to_board(px, py):
    return px - X0, S1 - s_of(py)


def knob_xy(k):
    return panel_to_board(*KNOBS[k][1:])


HOLES = K.corner_holes(W, H) + [(41.0, 2.6)]   # 82 mm: one more hole between the knobs at the rear edge


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.knob_pair(add, [k[0] for k in KNOBS], RING_N, clips=[c[0] for c in CLIPS], holes=len(HOLES))
    return P


def placement():
    pl, t, b = {}, "top", "bottom"
    for k in range(2):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, t)
        for i in range(RING_N):
            x, y, a = K.ring_xy(cx, cy, RING_R, RING_N, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, t)
    for k, (_, px, py) in enumerate(CLIPS):
        x, y = panel_to_board(px, py)
        pl[f"D{2 * RING_N + k + 1}"] = (x, y, 0, t)
    mx = 41.0                                    # opposite W1's J2
    pl["U1"] = (mx, 9.5, 0, b)
    for n, c in enumerate(("C3", "C4", "C5", "C6")):
        pl[c] = (mx + 4.5, 6.5 + 2.0 * n, 0, b)
    pl["R1"], pl["R2"] = (mx - 4.5, 7.0, 0, b), (mx - 4.5, 9.0, 0, b)
    pl["U2"] = (mx, 19.5, 90, b)
    pl["RN1"], pl["RN2"] = (mx - 5.0, 18.0, 90, b), (mx - 5.0, 21.0, 90, b)
    pl["C7"], pl["R3"] = (mx + 5.0, 18.5, 90, b), (mx + 5.0, 21.5, 0, b)
    pl["J1"] = (mx, H - 3.0, 90, b)
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
        print(" ", KNOBS[k][0], "board", tuple(round(v, 2) for v in knob_xy(k)))
    for nm, px, py in CLIPS:
        print(" ", nm, "board", tuple(round(v, 2) for v in panel_to_board(px, py)))
