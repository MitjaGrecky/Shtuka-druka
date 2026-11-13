"""M2 - Level 1-8 module: 8 encoders with 12-LED rings and touch on the knob frames. Single source of truth for the
schematic and the board: parts, nets, positions. Spec: hardware/for-routing/SPEC_boards.md, section M2.

Panel (layout_v7.json): knobs Level 8 ... Level 1 at x 394.5, y 52 + 25k (k = 0..7, Level 8 at y 52), knob 14 mm,
rings of 12 LEDs at r = 14/2 + 3 = 10 mm. Strip x 382.5-406.5, y 40-245 (24 x 205 mm); it sits in the notch of P3
(P3 rev 0.1, question V5) and plugs into P3's J2 (I2C channel 1 of P3's TCA9546A, chain P3 -> M2 -> M4).
Four LP5864, one per pair of rings (cells A-D, I2C 0x40-0x43, ADDR1 ADDR0 = 00, 01, 10, 11), CY8CMBR3108 touch
(the frame MP of each encoder through 560 R, as M1), three 74HC165 (A, B, push x 8, Level 8 first, as M1). 4 layers, as M1.
Board (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
Bottom side: the encoders' through-hole pins sit at x 4.5 and 19 and their frame lugs at y +-5.6 around each shaft,
so there is an 11.8 mm band between two encoders and a free column x 6-17 under each encoder.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "m2-levels"
ID = "M2"
TITLE = "M2 - Level 1-8 module (8 encoders, 12-LED RGB rings, touch)"
REV = "0.2"                                  # 0.2: rings r = 10.5 from the layout (V2)
M1_LIB = K.M1_LIB
BUS_NOTE = ("Module bus (R123): J1 to P3's J2 (I2C channel 1 of P3's TCA9546A); chain P3 -> M2 -> M4: SR_OUT to P3, "
            "SR_IN from M4. LP5864 0x40-0x43, touch CY8CMBR3108 0x37")

X0, X1 = 382.5, 406.5
Y0, Y1 = 40.0, 245.0
W, H = X1 - X0, Y1 - Y0                      # 24 x 205
LAYERS = 4                                   # 96 LEDs and 4 drivers in a 24 mm strip, as M1
KNOB_X, KNOB_D = 394.5, 14.0
KNOBS = [(f"Level {8 - k}", KNOB_X, 52.0 + 25.0 * k) for k in range(8)]
RING_R = K.ring_r(KNOBS[0][0])                 # 10.5 mm: layout ring 21 (V2: layout over the spec formula, was 10)
RING_N = 12
CELLS = [("A", "U1", ("C3", "C4", "C5", "C6"), (0, 0)), ("B", "U2", ("C7", "C8", "C9", "C10"), (0, 1)),
         ("C", "U3", ("C11", "C12", "C13", "C14"), (1, 0)), ("D", "U4", ("C15", "C16", "C17", "C18"), (1, 1))]


def panel_to_board(px, py):
    return px - X0, Y1 - py


def knob_xy(k):
    return panel_to_board(*KNOBS[k][1:])


def band_y(k):
    """Centre of the bottom-side band between encoder k and k + 1 (11.8 mm free between the frame lugs)."""
    return knob_xy(k)[1] - 12.5


BITS = [f"E{k}_{s}" for k in range(8) for s in ("A", "B", "SW")]   # host reads Level 8 A, B, push, Level 7 ... (24 bits)
SRS, SR_CAPS = ("U6", "U7", "U8"), ("C23", "C24", "C25")
# corners + both long sides in bands 1/2, 3/4, 5/6 (y 155.5, 105.5, 55.5): no more than 53 mm apart along the strip
HOLES = K.corner_holes(W, H) + [(x, band_y(k)) for k in (1, 3, 5) for x in (2.6, W - 2.6)]


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.bus(add, "J1", "Module bus 2x7 1.27")
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "4.7k", "SDA", "+3V3", DNP="yes")           # bus and INT pull-ups live on the host (P2), as M1
    K.rc(add, "R2", "4.7k", "SCL", "+3V3", DNP="yes")
    K.rc(add, "R3", "10k", "SR_IN", "+3V3", Note="end of the chain reads 1s when nothing follows")
    K.rc(add, "R4", "10k", "~{INT}", "+3V3", DNP="yes")
    # LEDs: ring pair (2c, 2c + 1) on LP5864 of cell c; the upper ring of a pair (Level 8, 6, 4, 2) is "left" (CS9-17)
    n = 0
    for c, (cell, u, caps, addr) in enumerate(CELLS):
        K.lp5864(add, u, cell, caps, addr=addr)
        for r in range(2):
            k = 2 * c + r
            for i in range(RING_N):
                n += 1
                sw, cs = K.ring_matrix(cell, r, i)
                K.rgb(add, f"D{n}", sw, cs, Ring=KNOBS[k][0], Dot=str(i + 1))
    # touch controller, as M1: sensor k = frame of encoder k through 560 R
    u5 = {"1": "TR0", "2": "TR1", "12": "TR2", "13": "TR3", "8": "TR4", "9": "TR5", "10": "TR6", "11": "TR7",
          "3": "CMOD", "4": "VREG", "5": "+3V3", "6": "+3V3", "7": "GND", "14": "SDA", "15": "SCL", "16": "~{INT}", "17": "GND"}
    add("U5", "Sensor_Touch:CY8CMBR3108", "CY8CMBR3108-LQXIT", "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm", u5,
        LCSC="C462528", Note="I2C 0x37; Infineon CY8CMBR3108-LQXIT (EasyEDA library, Extended)")
    for k in range(8):
        K.rc(add, f"R{5 + k}", "560", f"TR{k}", f"TOUCH{k}", Note=f"touch {KNOBS[k][0]}")
    K.rc(add, "C19", "2.2n", "CMOD", "GND", LCSC="C1531", Note="CMOD; 0402B222K500NT X7R 50V (Extended)")
    K.rc(add, "C20", "100n", "VREG", "GND")
    K.rc(add, "C21", "1u", "+3V3", "GND")
    K.rc(add, "C22", "100n", "+3V3", "GND")
    # inputs: three 74HC165, U6 first (Q7 -> SR_OUT, Level 8 ... Level 6 A B), U8 last (DS <- SR_IN)
    for s, (u, cap) in enumerate(zip(SRS, SR_CAPS)):
        q7 = "SR_OUT" if s == 0 else f"SR_Q{s}"
        ds = "SR_IN" if s == len(SRS) - 1 else f"SR_Q{s + 1}"
        K.sr165(add, u, BITS[8 * s:8 * s + 8], ds, q7, cap)
    K.pullups(add, 1, BITS)                                         # RN1-RN6
    for k in range(8):
        K.encoder(add, f"ENC{k + 1}", k, mp=f"TOUCH{k}",
                  note=f"{KNOBS[k][0]}: Alps EC11E1834403 or another smooth EC11 with switch and metal shaft (touch)")
    for h in range(len(HOLES)):
        K.hole(add, f"H{h + 1}")
    return P


def placement():
    """ref -> (x, y, rotation, side). Top: encoders and ring LEDs (locked). Bottom: the rest - drivers in the band
    between the two rings of their pair, J1 in band 3/4 (opposite P3's J2), touch and its resistors in bands 1/2 and 5/6,
    shift registers and pull-up packs in the free column under the encoders."""
    pl, t, b = {}, "top", "bottom"
    mx = W / 2
    for k in range(8):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, t)
        for i in range(RING_N):
            x, y, a = K.ring_xy(cx, cy, RING_R, RING_N, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, t)
    for c, (cell, u, caps, addr) in enumerate(CELLS):              # band between ring 2c and 2c + 1
        y = band_y(2 * c)
        pl[u] = (mx - 2.5, y, 0, b)
        for n, cap in enumerate(caps):
            pl[cap] = (mx + 3.5 + 3.0 * (n // 2), y - 1.5 + 3.0 * (n % 2), 90, b)
    yj = band_y(3)                                                  # 105.5 = panel y 139.5, P3's J2 is at panel y 139
    pl["J1"] = (mx, yj, 90, b)
    pl["C1"], pl["C2"] = (mx - 4.0, yj - 3.8, 0, b), (mx + 4.0, yj - 3.8, 0, b)
    pl["R1"], pl["R2"] = (mx - 3.0, yj + 3.0, 0, b), (mx, yj + 3.0, 0, b)
    pl["R3"], pl["R4"] = (mx + 3.0, yj + 3.0, 0, b), (mx + 6.0, yj + 2.5, 90, b)
    yt = band_y(1)                                                  # touch controller between Level 7 and Level 6
    pl["U5"] = (mx, yt, 0, b)
    for n, cap in enumerate(("C19", "C20", "C21", "C22")):
        pl[cap] = (mx - 5.5 + 11.0 * (n // 2), yt - 1.2 + 2.4 * (n % 2), 90, b)
    for k in range(8):                                              # 560 R: TR0-3 in band 1/2, TR4-7 in band 5/6
        y = band_y(1 if k < 4 else 5)
        pl[f"R{5 + k}"] = (mx - 4.5 + 3.0 * (k % 4), y + (3.5 if k < 4 else 0.0), 0, b)
    for s, (u, cap) in enumerate(zip(SRS, SR_CAPS)):                # under encoders Level 7, 5, 3 (k 1, 3, 5)
        cx, cy = knob_xy(2 * s + 1)
        pl[u] = (cx, cy, 0, b)
        pl[cap] = (cx + 5.0, cy, 90, b)
    for n in range(6):                                              # under encoders Level 8, 6, 4 (k 0, 2, 4), two per encoder
        cx, cy = knob_xy(2 * (n // 2))
        pl[f"RN{n + 1}"] = (cx, cy - 1.6 + 3.2 * (n % 2), 0, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", [p["ref"] for p in P if p["ref"] not in pl])
    for k in range(8):
        print(" ", KNOBS[k][0], "board", knob_xy(k), "band below", band_y(k) if k < 7 else "-")
