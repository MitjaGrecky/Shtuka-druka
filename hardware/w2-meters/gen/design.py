"""W2 - Meters (slope): two columns of 14 RGB LEDs (L and R level meters). Single source of truth for the
schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, section W2.

Panel (layout_v7.json): Meter L at x 364, Meter R at x 380, centre y 365, 104 mm long in the top view, i.e.
120.1 mm along the slope (s 15.0-135.1). 14 LEDs per column at equal steps of 8.58 mm along the slope (7.43 mm in
the top view - the "about 7.4 mm" of the spec). Board x 355-390 (35 mm); along the slope s 12-138 like W1 (126 mm,
the meters alone are 120). Two LP5864 (L: ADDR 00 = 0x40, R: ADDR 01 = 0x41), 14 of 24 places each.
No buttons: J1's SR_IN and SR_OUT are tied (SR_THRU) so a chain through W2 would not break; P3 does not route its chain here.
Board (KiCad, y down): origin at the rear-left corner (high s), x = panel_x - X0, y = S1 - s.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "w2-meters"
ID = "W2"
TITLE = "W2 - Meters (slope): 2 x 14 RGB LED level meters"
REV = "0.1b"                                 # 0.1b: drivers under their columns (placement only, same netlist)
M1_LIB = K.M1_LIB
BUS_NOTE = "Module bus (R123): J1 to P3 over the fold (I2C channel 3 of P3's TCA9546A, P99); SR_IN tied to SR_OUT (no buttons)"

COS = math.cos(math.radians(30.0))
X0, X1 = 355.0, 390.0
S0, S1 = 12.0, 138.0
W, H = X1 - X0, S1 - S0                      # 35 x 126
LAYERS = 2
METERS = [("L", 364.0), ("R", 380.0)]
METER_Y, METER_LEN = 365.0, 104.0            # top view
N = 14


def s_of(py):
    return (py - 300.0) / COS


def panel_to_board(px, py):
    return px - X0, S1 - s_of(py)


S_LO, S_HI = s_of(METER_Y - METER_LEN / 2), s_of(METER_Y + METER_LEN / 2)
STEP = (S_HI - S_LO) / N


def led_xy(m, i):
    """LED i of meter m (i = 0 at the bottom of the meter, nearest the fold)."""
    s = S_LO + STEP * (i + 0.5)
    return METERS[m][1] - X0, S1 - s


HOLES = K.corner_holes(W, H) + [(2.6, H / 2), (W - 2.6, H / 2)]   # 126 mm sides: one more hole in the middle of each


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.bus(add, "J1", "Module bus 2x7 1.27", {**K.CONN, 13: "SR_THRU", 14: "SR_THRU"})
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "4.7k", "SDA", "+3V3", DNP="yes")
    K.rc(add, "R2", "4.7k", "SCL", "+3V3", DNP="yes")
    for m, (cell, u, caps, addr) in enumerate((("L", "U1", ("C3", "C4", "C5", "C6"), (0, 0)),
                                                ("R", "U2", ("C7", "C8", "C9", "C10"), (0, 1)))):
        K.lp5864(add, u, cell, caps, addr=addr, cs_used=12)
        for i in range(N):                     # LED i: CS triple i // 4, SW i % 4 (4 triples x 4 SW = 16 places, 14 used)
            c = 3 * (i // 4)
            K.rgb(add, f"D{m * N + i + 1}", f"{cell}_SW{i % 4}", (f"{cell}_CS{c}", f"{cell}_CS{c + 1}", f"{cell}_CS{c + 2}"),
                  Meter=cell, Step=str(i + 1))
    for h in range(len(HOLES)):
        K.hole(add, f"H{h + 1}")
    return P


def placement():
    pl, t, b = {}, "top", "bottom"
    for m in range(2):
        for i in range(N):
            x, y = led_xy(m, i)
            pl[f"D{m * N + i + 1}"] = (x, y, 0, t)
    mx = W / 2                                   # 17.5, between the two columns
    # rev 0.1b (13.11): each driver right under its own column on the bottom side, at mid-height, its capacitors towards
    # the board centre. Each column is then a self-contained bus (no crossings between L and R), the same pattern twice.
    ymid = H / 2 - 6.0                           # 57: clear of the middle mounting holes (y 63) and between LED rows
    for u, m, caps, side in (("U1", 0, ("C3", "C4", "C5", "C6"), +1), ("U2", 1, ("C7", "C8", "C9", "C10"), -1)):
        cx = METERS[m][1] - X0                   # under the column: x 9 (L) and 25 (R)
        pl[u] = (cx, ymid, 0, b)
        for n, c in enumerate(caps):
            pl[c] = (cx + side * 4.6, ymid - 3.0 + 2.0 * n, 0, b)
    pl["J1"] = (mx, H - 3.0, 90, b)              # front edge, towards the fold and P3
    pl["C1"], pl["C2"] = (mx - 6.5, H - 3.0, 90, b), (mx + 6.5, H - 3.0, 90, b)
    pl["R1"], pl["R2"] = (mx - 2.0, H - 7.0, 0, b), (mx + 2.0, H - 7.0, 0, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", [p["ref"] for p in P if p["ref"] not in pl])
    print(f"  meters s {S_LO:.1f}-{S_HI:.1f}, step {STEP:.2f} mm along the slope; LED 1 y {led_xy(0, 0)[1]:.1f}, LED 14 y {led_xy(0, 13)[1]:.1f}")
