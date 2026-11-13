"""P3 - Tracks deck: 21 buttons of the track column with 2 RGB each, I2C mux, buses to P2, M2, M4 and W2.
Single source of truth for the schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, section P3.

Panel (layout_v7.json, x 339-405, y <= 252): Solo, Arm, Arrow down, Mute 8..1, Select 8..1, Stop All, Arrow up.
Board x 339-405 (66 mm; question V5: 409 would cover M2's strip), y 4-262. The Level knobs (module M2, x 394.5, y 52-227)
need a window: M2's strip x 382.5-406.5, y 40-245 runs past this board's right edge, so the window is a notch open to the
right edge (board x 43.5-66, y 16.5-222.5); the arrows down (y 22) and up (y 252) sit on the board parts in front of and
behind it.
Proposals (constants below): P99 - TCA9546A at 0x71: ch 0 own LP5864s, ch 1 J2 -> M2, ch 2 J3 -> M4, ch 3 J4 -> W2 (over the
fold); P100 - J1 2 x 8 to P2; P101 - 2 RGB per button (42 RGB: cell A 0x40 buttons 1-12, B 0x41 buttons 13-21).
Chain: P3 buttons (U3 first: Solo ...), then M2 (J2), then M4 (J3): U5.DS <- SR_M2, J2 pin 14 <- SR_M4, J3 pin 14 <- SR_END
(pulled up here). W2 has no buttons and is not in the chain (its J4 pins 13/14 open). ~INT of M2, M4, W2 straight to J1.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "p3-tracks"
ID = "P3"
TITLE = "P3 - Tracks deck: 21 buttons with 2 RGB, window for M2, I2C mux, buses to P2, M2, M4, W2"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("J1 deck bus 2x8 to P2 (P100); TCA9546A 0x71 (P99): ch0 own LEDs, ch1 J2 -> M2, ch2 J3 -> M4, ch3 J4 -> W2; "
            "chain P3 -> M2 -> M4")

X0, X1 = 339.0, 405.0                        # V5: X1 = 409 would make the notch narrower on the right
Y0, Y1 = 4.0, 262.0
W, H = X1 - X0, Y1 - Y0                      # 66 x 258
LAYERS = 2
MUX_ADDR = 1                                 # P99: 0x71
LED_DX, LED_DX_NARROW = 6.5, 5.5
M2_STRIP = (382.5, 406.5, 40.0, 245.0)       # panel x0, x1, y0, y1 of module M2 (spec)
GAP = 0.5


def panel_to_board(px, py):
    return px - X0, Y1 - py


NX0 = panel_to_board(M2_STRIP[0], 0)[0] - GAP                     # notch: board x 43.5 .. right edge
NY0, NY1 = Y1 - M2_STRIP[3] - GAP, Y1 - M2_STRIP[2] + GAP         # board y 16.5 .. 222.5
OUTLINE = [(0, 0), (W, 0), (W, NY0), (NX0, NY0), (NX0, NY1), (W, NY1), (W, H), (0, H)]

_EL = K.layout_elements()
BUTTONS = sorted(((e["name"], e["x"], e["y"], e["w"]) for e in _EL.values()
                  if e["kind"] == "button" and X0 <= e["x"] <= X1 and e["y"] <= 252), key=lambda b: (b[2], b[1]))

_ROW_GAPS = (47.5, 97.5, 147.5, 197.5)       # board y between button rows
HOLES = ([(2.6, 2.6), (W - 2.6, 2.6), (2.6, H - 2.6), (W - 2.6, H - 2.6), (16.0, 2.6), (W / 2, H - 2.6)]
         + [(2.6, y) for y in _ROW_GAPS] + [(NX0 - 2.6, y) for y in _ROW_GAPS])
CELLS = [("A", "U1", ("C3", "C4", "C5", "C6"), (0, 0)), ("B", "U2", ("C7", "C8", "C9", "C10"), (0, 1))]
SRS, SR_CAPS = ("U3", "U4", "U5"), ("C11", "C12", "C13")


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.deck_bus(add, "J1", "Deck bus to P2 2x8 1.27")
    mod = lambda sda, scl, sr_out, sr_in: {**K.CONN, 7: sda, 8: scl, 13: sr_out, 14: sr_in}  # noqa: E731
    K.bus(add, "J2", "Module bus to M2 2x7 1.27", mod("SD1", "SC1", "SR_M2", "SR_M4"))
    K.bus(add, "J3", "Module bus to M4 2x7 1.27", mod("SD2", "SC2", "SR_M4", "SR_END"))
    K.bus(add, "J4", "Module bus to W2 2x7 1.27", mod("SD3", "SC3", None, None))
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "10k", "SR_END", "+3V3", Note="end of the chain (M4 SR_IN) reads 1s")
    K.i2c_mux(add, "U6", MUX_ADDR, {0: ("SD0", "SC0"), 1: ("SD1", "SC1"), 2: ("SD2", "SC2"), 3: ("SD3", "SC3")}, "C14", 2)
    K.deck_inputs(add, [b[0] for b in BUTTONS], CELLS, SRS, SR_CAPS, "SR_M2")
    for p in P:
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
    # bottom side, left of the notch (x 0-43.5)
    for (cell, u, caps, _), y in zip(CELLS, (200.0, 80.0)):
        pl[u] = (21.0, y, 0, b)
        for n, c in enumerate(caps):
            pl[c] = (25.6, y - 3.0 + 2.0 * n, 0, b)
    for u, cap, y in zip(SRS, SR_CAPS, (215.0, 150.0, 60.0)):
        pl[u] = (9.0, y, 90, b)
        pl[cap] = (14.5, y, 90, b)
    for n in range(6):
        pl[f"RN{n + 1}"] = (36.0, 230.0 - 36.0 * n, 90, b)
    pl["J1"] = (3.0, 123.0, 0, b)                                   # left edge: P2 (the grid) is to the left
    pl["C1"], pl["C2"] = (3.0, 132.0, 0, b), (3.0, 134.0, 0, b)
    pl["U6"], pl["C14"] = (14.0, 123.0, 0, b), (14.0, 118.0, 0, b)
    rs = sorted((p["ref"] for p in parts() if p["ref"].startswith("R") and p["ref"][1:].isdigit() and p["ref"] != "R1"),
                key=lambda s: int(s[1:]))
    for n, ref in enumerate(rs):
        pl[ref] = (10.0 + 2.0 * (n % 6), 128.0 + 2.0 * (n // 6), 90, b)
    pl["J2"] = (NX0 - 4.0, 123.0, 0, b)                               # at the notch edge: M2 sits in the notch
    pl["J3"], pl["R1"] = (26.0, 3.0, 90, b), (26.0, 7.5, 0, b)      # rear edge: M4 right behind P3
    pl["J4"] = (52.0, 3.0, 90, b)                                    # rear edge, behind the notch: W2 over the fold
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; notch x", NX0, "y", NY0, "-", NY1,
          "; unplaced:", [r for r in refs if r not in pl], "; placed, no part:", [r for r in pl if r not in refs])
    print("  buttons:", len(BUTTONS), [b[0].encode("ascii", "replace").decode() for b in BUTTONS])
