"""M3 - Tempo + Swing module (2 encoders with 12-LED rings). Single source of truth for the schematic
and the board: parts, nets, positions. Spec: hardware/for-routing/SPEC_boards.md, section M3.

Panel (layout_v7.json): knobs Tempo x 32 and Swing x 80, y 277, knob 22 mm; board x 10-102, y 263-297
(92 x 34, the same strip as M1). One TI LP5864 drives both rings (24 RGB), one 74HC165 reads A, B and
push of both encoders. P102 (proposal): no touch sensing, the encoder frames (MP) go to GND.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "m3-tempo-swing"
ID = "M3"
TITLE = "M3 - Tempo + Swing module (2 encoders, 12-LED RGB rings)"
REV = "0.1"
M1_LIB = K.M1_LIB

# ------------------------------------------------------------------ geometry (mm)
X0, X1 = 10.0, 102.0
Y0, Y1 = 263.0, 297.0
W, H = X1 - X0, Y1 - Y0                      # 92 x 34
LAYERS = 2                                   # 24 LEDs, one driver: 2 layers are expected to do (M1 needs 4 for 96 LEDs)
KNOBS = [("Tempo", 32.0, 277.0), ("Swing", 80.0, 277.0)]
KNOB_D = 22.0
RING_R = KNOB_D / 2 + 3.0                    # 14 mm (spec: r = knob diameter / 2 + 3)
RING_N = 12
TOUCH = False                                # P102: no touch on M3; True would need a touch controller like M1


def panel_to_board(px, py):
    return px - X0, Y1 - py


def knob_xy(k):
    return panel_to_board(*KNOBS[k][1:])


BITS = [f"E{k}_{s}" for k in range(2) for s in ("A", "B", "SW")]   # host reads Tempo A, B, push, Swing A, B, push, 1, 1
HOLES = K.corner_holes(W, H) + [(W / 2, 2.6)]                       # corners + one between the knobs (long side < 60 mm apart)


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.bus(add, "J1", "Module bus 2x7 1.27")
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    # bus pull-ups live on the host (P2); places here, not fitted, as on M1
    K.rc(add, "R1", "4.7k", "SDA", "+3V3", DNP="yes")
    K.rc(add, "R2", "4.7k", "SCL", "+3V3", DNP="yes")
    K.rc(add, "R3", "10k", "SR_IN", "+3V3", Note="end of the chain reads 1s when nothing follows")
    # LEDs: one LP5864 for the pair of rings (left = Tempo on CS9-17, right = Swing on CS0-8)
    K.lp5864(add, "U1", "A", ("C3", "C4", "C5", "C6"), addr=(0, 0))
    n = 0
    for k in range(2):
        for i in range(RING_N):
            n += 1
            sw, cs = K.ring_matrix("A", k, i)
            K.rgb(add, f"D{n}", sw, cs, Ring=KNOBS[k][0], Dot=str(i + 1))
    # inputs: one 74HC165, Q7 -> SR_OUT (towards the host), DS <- SR_IN
    K.sr165(add, "U2", BITS, "SR_IN", "SR_OUT", "C7")
    K.pullups(add, 1, BITS)
    for k in range(2):
        K.encoder(add, f"ENC{k + 1}", k, mp="GND", note=f"{KNOBS[k][0]}: Alps EC11E1834403 or another smooth EC11 with switch")
    for h in range(len(HOLES)):
        K.hole(add, f"H{h + 1}")
    return P


def placement():
    """ref -> (x, y, rotation, side). Top: encoders and ring LEDs (locked, set by the panel). Bottom: the rest,
    in the 20 mm band between the two rings (x 36-56) and behind them."""
    pl, t, b = {}, "top", "bottom"
    for k in range(2):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, t)                       # make_pcb puts the shaft at (x, y)
        for i in range(RING_N):
            x, y, a = K.ring_xy(cx, cy, RING_R, RING_N, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, t)
    mx = W / 2
    pl["U1"] = (mx, 11.0, 0, b)
    for n, c in enumerate(("C3", "C4", "C5", "C6")):
        pl[c] = (mx + 4.5, 8.0 + 2.0 * n, 0, b)
    pl["U2"] = (mx, 20.5, 90, b)
    pl["RN1"], pl["RN2"], pl["C7"] = (mx - 5.0, 19.5, 90, b), (mx - 5.0, 22.5, 90, b), (mx + 5.0, 20.5, 90, b)
    pl["R3"] = (mx + 5.0, 23.5, 0, b)
    pl["J1"] = (mx, H - 3.0, 90, b)                              # front edge: towards P1's J2 (rear edge of P1)
    pl["C1"], pl["C2"] = (mx - 6.5, H - 3.0, 90, b), (mx + 6.5, H - 3.0, 90, b)
    pl["R1"], pl["R2"] = (mx - 4.5, 6.0, 0, b), (mx - 4.5, 8.0, 0, b)
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
