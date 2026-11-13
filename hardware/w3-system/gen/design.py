"""W3 - System (slope, right column): Save and Project buttons with 2 RGB each, the record light at the USB/SD pocket.
Single source of truth for the schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, section W3.

Panel (layout_v7.json): Save x 435 and Project x 483 at y 323 (44 x 16 mm), USB-A + SD pocket x 459, y 365 (92 x 24 in the
top view, a retail module, P105), Power x 459, y 407 (14 mm). The pocket is as wide as the whole column (x 413-505), so a
board through it would fall into two pieces: this board covers the front part of the slope, from the fold side up to the
pocket (s 12 to 60.2 mm). The Power button sits behind the pocket - off this board (question V9 in notes/handoff.md:
own small board W3b or a panel button on a cable). Power state is not read (spec: the executor decides) - the Mini-ITX
board handles it. Record light: the 5th RGB, at the rear edge facing the pocket (for a light pipe into the pocket wall).
One LP5864 (5 RGB on CS0-5), one 74HC165 (Save, Project). P102-style: nothing else.
Board (KiCad, y down): origin at the rear-left corner (high s), x = panel_x - X0, y = S1 - s.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "w3-system"
ID = "W3"
TITLE = "W3 - System (slope, right): Save, Project, record light"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = "Module bus (R123): J1 to P4 over the fold (I2C channel 1 of P4's TCA9546A, P99); chain: P4 buttons -> W3"

COS = math.cos(math.radians(30.0))
X0, X1 = 413.0, 505.0
POCKET = (459.0, 365.0, 92.0, 24.0)          # panel x, y, w, h (top view)


def s_of(py):
    return (py - 300.0) / COS


S0 = 12.0                                    # front edge along the slope, as W1 and W2
S1 = s_of(POCKET[1] - POCKET[3] / 2) - 1.0   # rear edge: 1 mm before the pocket (s 60.2)
W, H = X1 - X0, S1 - S0                      # 92 x 48.2
LAYERS = 2
BUTTONS = [("Save", 435.0, 323.0), ("Project", 483.0, 323.0)]
LED_DX = 6.5                                 # P84: 2 RGB left and right of the button centre
REC = (459.0, None)                          # record light: rear edge, x of the pocket centre


def panel_to_board(px, py):
    return px - X0, S1 - s_of(py)


HOLES = K.corner_holes(W, H) + [(40.0, 2.6), (30.0, H - 2.6)]   # long sides 92 mm: one more hole on each


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.bus(add, "J1", "Module bus 2x7 1.27")
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "4.7k", "SDA", "+3V3", DNP="yes")
    K.rc(add, "R2", "4.7k", "SCL", "+3V3", DNP="yes")
    K.rc(add, "R3", "10k", "SR_IN", "+3V3", Note="end of the chain reads 1s when nothing follows")
    K.lp5864(add, "U1", "A", ("C3", "C4", "C5", "C6"), addr=(0, 0), cs_used=6)
    leds = [("Save left", 0), ("Save right", 1), ("Project left", 2), ("Project right", 3), ("Record", 4)]
    for n, (note, i) in enumerate(leds):     # LED i: CS triple i div 4, SW i mod 4
        c = 3 * (i // 4)
        K.rgb(add, f"D{n + 1}", f"A_SW{i % 4}", (f"A_CS{c}", f"A_CS{c + 1}", f"A_CS{c + 2}"), Note=note)
    bits = ["BTN_SAVE", "BTN_PROJECT"]
    for n, (nm, _, _) in enumerate(BUTTONS):
        add(f"SW{n + 1}", "Switch:SW_Push", "TS-1187A-B-A-B", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A",
            {"1": bits[n], "2": "GND"}, LCSC="C318884", Note=nm)
    K.sr165(add, "U2", bits, "SR_IN", "SR_OUT", "C7")
    K.pullups(add, 1, bits)
    for h in range(len(HOLES)):
        K.hole(add, f"H{h + 1}")
    return P


def placement():
    pl, t, b = {}, "top", "bottom"
    for n, (_, px, py) in enumerate(BUTTONS):
        x, y = panel_to_board(px, py)
        pl[f"SW{n + 1}"] = (x, y, 0, t)
        pl[f"D{2 * n + 1}"] = (x - LED_DX, y, 0, t)
        pl[f"D{2 * n + 2}"] = (x + LED_DX, y, 0, t)
    pl["D5"] = (REC[0] - X0, 1.6, 0, t)          # rear edge, under the pocket wall
    mx = W / 2
    pl["U1"] = (mx, 14.0, 0, b)
    for n, c in enumerate(("C3", "C4", "C5", "C6")):
        pl[c] = (mx + 4.6, 11.0 + 2.0 * n, 0, b)
    pl["U2"] = (mx, 30.0, 90, b)
    pl["RN1"], pl["C7"], pl["R3"] = (mx - 5.0, 30.0, 90, b), (mx + 5.0, 29.0, 90, b), (mx + 5.0, 32.0, 0, b)
    jx = 60.0                                    # front edge, beside the front middle hole
    pl["J1"] = (jx, H - 3.0, 90, b)
    pl["C1"], pl["C2"] = (jx - 6.5, H - 3.0, 90, b), (jx + 6.5, H - 3.0, 90, b)
    pl["R1"], pl["R2"] = (mx - 4.6, 11.0, 0, b), (mx - 4.6, 13.0, 0, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    print(len(P), "parts,", len(nets), "nets; board", W, "x", round(H, 2), "mm; unplaced:", [p["ref"] for p in P if p["ref"] not in pl])
    for nm, px, py in BUTTONS:
        print(f"  {nm}: board {tuple(round(v, 2) for v in panel_to_board(px, py))}")
    print(f"  pocket front edge s {s_of(POCKET[1] - POCKET[3] / 2):.1f}; Power s {s_of(407):.1f} (off this board)")
