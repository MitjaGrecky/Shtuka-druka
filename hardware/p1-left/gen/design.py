"""P1 - Left deck: 19 buttons of the time column with 2 RGB each, I2C mux, bus to P2 and to the modules M3 and W1.
Single source of truth for the schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, section P1.

Panel (layout_v7.json, group x <= 102, y <= 252): Rec, Play, Stop, Restart, Metronome, Tap, Capture, Resample, Undo, Redo,
Delete, Duplicate, Double, New, Quantize, Length, Automate, Repeat, Accent. Board x 10-102, y 4-262 (92 x 258).
Proposals (not decisions, constants below): P99 - TCA9546A at 0x70: channel 0 own LP5864s, 1 -> J2 (M3), 2 -> J3 (W1),
3 free; P100 - J1 2 x 8 to P2; P101 - 2 RGB per button, 38 RGB on two LP5864 (cell A 0x40: first 12 buttons, B 0x41: 7).
Chain: host reads P1 buttons (U3 first: Rec .. ), then M3, then W1 (W1 continues to M5): U5.DS <- SR_M3 (J2 pin 13),
J2 pin 14 (M3's SR_IN) <- SR_W1 (J3 pin 13), J3 pin 14 (W1's SR_IN) <- SR_END pulled up here. ~INT of the modules goes
straight through to J1. J1 pin 14 (SR_IN from P2's side) is not used: P1 ends the chain with its modules.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "p1-left"
ID = "P1"
TITLE = "P1 - Left deck: 19 buttons with 2 RGB, I2C mux, bus to P2, M3, W1"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = "J1 deck bus 2x8 to P2 (P100); TCA9546A 0x70 (P99): ch0 own LEDs, ch1 J2 -> M3, ch2 J3 -> W1; chain P1 -> M3 -> W1 -> M5"

X0, X1 = 10.0, 102.0
Y0, Y1 = 4.0, 262.0
W, H = X1 - X0, Y1 - Y0                      # 92 x 258
LAYERS = 2
MUX_ADDR = 0                                 # P99: 0x70 + 0
LED_DX, LED_DX_NARROW = 6.5, 5.5             # P84: LEDs left and right of the button centre (16 mm wide buttons: 5.5)

ORDER = ["Rec", "Play", "Stop", "Restart", "Metronome", "Tap", "Capture", "Resample", "Undo", "Redo", "Delete",
         "Duplicate", "Double", "New", "Quantize", "Length", "Automate", "Repeat", "Accent"]
# layout names carry a symbol before some labels ("<symbol> Rec"): match on the last word, ASCII only in this file
_EL = {n.split(" ")[-1]: e for n, e in K.layout_elements().items() if e["kind"] == "button" and e["x"] <= 102}
BUTTONS = [(n, _EL[n]["x"], _EL[n]["y"], _EL[n]["w"]) for n in ORDER]   # (label, x, y, width)


def panel_to_board(px, py):
    return px - X0, Y1 - py


# mounting holes: corners, short-side middles, long sides at free rows (no button above them), at most 60 mm apart
_SIDE_Y = (60.0, 97.5, 150.0, 197.5)
HOLES = K.corner_holes(W, H) + [(W / 2, 2.6), (W / 2, H - 2.6)] + [(x, y) for y in _SIDE_Y for x in (2.6, W - 2.6)]
CELLS = [("A", "U1", ("C3", "C4", "C5", "C6"), (0, 0)), ("B", "U2", ("C7", "C8", "C9", "C10"), (0, 1))]
SRS, SR_CAPS = ("U3", "U4", "U5"), ("C11", "C12", "C13")


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.deck_bus(add, "J1", "Deck bus to P2 2x8 1.27")
    mod = lambda sda, scl, sr_out, sr_in: {**K.CONN, 7: sda, 8: scl, 13: sr_out, 14: sr_in}  # noqa: E731
    K.bus(add, "J2", "Module bus to M3 2x7 1.27", mod("SD1", "SC1", "SR_M3", "SR_W1"))
    K.bus(add, "J3", "Module bus to W1 2x7 1.27", mod("SD2", "SC2", "SR_W1", "SR_END"))
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "10k", "SR_END", "+3V3", Note="end of the chain (W1 SR_IN) reads 1s")
    r = K.i2c_mux(add, "U6", MUX_ADDR, {0: ("SD0", "SC0"), 1: ("SD1", "SC1"), 2: ("SD2", "SC2"), 3: None}, "C14", 2)
    # own LED drivers sit on mux channel 0
    cells = [(c, u, caps, a) for c, u, caps, a in CELLS]
    K.deck_inputs(add, [b[0] for b in BUTTONS], cells, SRS, SR_CAPS, "SR_M3")
    for p in P:                                  # LP5864s on channel 0, not on the upstream bus
        if p["ref"] in ("U1", "U2"):
            p["pins"]["29"], p["pins"]["28"] = "SD0", "SC0"
    for h in range(len(HOLES)):
        K.hole(add, f"H{h + 1}")
    return P


def placement():
    pl, t, b = {}, "top", "bottom"
    for k, (_, px, py, w) in enumerate(BUTTONS):
        x, y = panel_to_board(px, py)
        dx = LED_DX_NARROW if w <= 16 else LED_DX
        pl[f"SW{k + 1}"] = (x, y, 0, t)
        pl[f"D{2 * k + 1}"] = (x - dx, y, 0, t)
        pl[f"D{2 * k + 2}"] = (x + dx, y, 0, t)
    mx = W / 2
    # bottom side. LED drivers in the middle of their button groups (A: Rec .. Duplicate, B: Double .. Accent)
    for (cell, u, caps, _), y in zip(CELLS, (172.0, 72.0)):
        pl[u] = (mx, y, 0, b)
        for n, c in enumerate(caps):
            pl[c] = (mx + 4.6, y - 3.0 + 2.0 * n, 0, b)
    for n, (u, cap, y) in enumerate(zip(SRS, SR_CAPS, (205.0, 140.0, 90.0))):       # registers near their buttons
        pl[u] = (mx - 14.0, y, 90, b)
        pl[cap] = (mx - 8.5, y, 90, b)
    for n in range(5):                                                               # pull-up packs RN1-RN5
        pl[f"RN{n + 1}"] = (mx - 20.0, 215.0 - 32.0 * n, 90, b)
    # mux and its resistors near J1 (right edge, middle) - the bus comes in there
    pl["U6"], pl["C14"] = (mx + 18.0, 120.0, 0, b), (mx + 18.0, 115.0, 0, b)
    for n in range(2, 13):
        pl[f"R{n}"] = (mx + 14.0 + 2.0 * ((n - 2) % 5), 126.0 + 2.0 * ((n - 2) // 5), 90, b)
    pl["J1"] = (W - 3.0, 124.0, 0, b)                                              # to P2 (the grid deck) on the right
    pl["C1"], pl["C2"] = (W - 3.0, 133.0, 0, b), (W - 3.0, 135.0, 0, b)
    pl["J2"], pl["J3"] = (30.0, 3.0, 90, b), (62.0, 3.0, 90, b)                    # rear edge: M3 behind, W1 over the fold
    pl["R1"] = (62.0, 7.5, 0, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", [p["ref"] for p in P if p["ref"] not in pl])
    refs = [p["ref"] for p in P]
    print("  R refs:", sorted((r for r in refs if r.startswith("R") and not r.startswith("RN")), key=lambda s: int(s[1:])))
    for (nm, px, py, w) in BUTTONS[:3]:
        print(f"  {nm}: board {panel_to_board(px, py)}")
