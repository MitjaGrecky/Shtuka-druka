"""P3 - Tracks deck with the Level knobs (rev 0.2: P3 and M2 on one board, R128): 21 buttons of the track column with
2 RGB each, 8 Level encoders with 12-LED rings and touch, I2C mux, buses to P2, M4 and W2.
Single source of truth for the schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, sections P3 and M2.

Panel (layout_v7.json): Solo, Arm, Arrow down, Mute 8..1, Select 8..1, Stop All, Arrow up (x 339-405, y <= 252) and the
Level knobs 8..1 (x 394.5, y 52-227). Board x 339-406.5 (67.5 mm: the right edge of M2's former strip), y 4-262, 4 layers.
R128 (user, 13.11.2026): one 4-layer board instead of P3 + module M2 - no notch, no M2 connector and cable.
The Level part is hardware/m2-levels/gen/design.py (rev 0.1, kept as the source of the block): its parts and positions are
taken over with refs renumbered after P3's own, board offset (43.5, 17), its I2C on mux channel 1 (SD1/SC1), its cells
A-D renamed LA-LD and its chain nets SR_Q1/2 renamed SR_L1/2 so they do not clash with P3's.
Proposals: P99 - TCA9546A at 0x71: ch 0 own LP5864s (0x40, 0x41), ch 1 the Level block (LP5864 0x40-0x43, touch 0x37),
ch 2 J3 -> M4, ch 3 J4 -> W2 (over the fold); P100 - J1 2 x 8 to P2; P101 - 2 RGB per button (42 RGB).
Chain: P3 buttons (U3 first: Solo ...), then the Level registers (Level 8 first), then M4 (J3): U5.DS <- SR_M2,
Level chain SR_M2 ... DS of its last register <- SR_M4 (pulled up, R of the Level block), J3 pin 14 <- SR_END (R1).
W2 has no buttons and is not in the chain (its J4 pins 13/14 open). ~INT of the touch controller, M4, W2 to J1.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "p3-tracks"
ID = "P3"
TITLE = "P3 - Tracks deck + Level knobs: 21 buttons with 2 RGB, 8 encoders with rings and touch, I2C mux, buses to P2, M4, W2"
REV = "0.4"                                  # 0.2: Level knobs on this board (R128); 0.3: Level rings r 10.5 (V2); 0.4: LED drivers U7-U10 centred in the gap between rings (EasyEDA DRC: vias at ring LEDs)
M1_LIB = K.M1_LIB
BUS_NOTE = ("J1 deck bus 2x8 to P2 (P100); TCA9546A 0x71 (P99): ch0 own LEDs, ch1 Level block (4 LP5864, touch), "
            "ch2 J3 -> M4, ch3 J4 -> W2; chain P3 buttons -> Level knobs -> M4")

X0, X1 = 339.0, 406.5                        # R128: right edge = right edge of the former M2 strip (V5 closed)
Y0, Y1 = 4.0, 262.0
W, H = X1 - X0, Y1 - Y0                      # 67.5 x 258
LAYERS = 4                                   # R128: 4 layers, as M1/M2
MUX_ADDR = 1                                 # P99: 0x71
LED_DX, LED_DX_NARROW = 6.5, 5.5


def panel_to_board(px, py):
    return px - X0, Y1 - py


# ------------------------------------------------------------------ the Level block (former module M2)
_spec = importlib.util.spec_from_file_location("m2_design", os.path.join(K.HERE, "..", "..", "m2-levels", "gen", "design.py"))  # via kit: works from a temp copy too
M2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(M2)
M2_DX, M2_DY = panel_to_board(M2.X0, M2.Y1)                       # (43.5, 17): M2 board origin on this board
M2_DROP = {"J1", "R1", "R2", "R4"}                                # its bus connector, DNP bus and INT pull-ups (P2 has them)
M2_NETS = {"SDA": "SD1", "SCL": "SC1", "SR_OUT": "SR_M2", "SR_IN": "SR_M4", "SR_Q1": "SR_L1", "SR_Q2": "SR_L2"}


def _m2_net(n):
    if n is None or n in M2_NETS:
        return M2_NETS.get(n) if n else n
    m = re.match(r"^([A-D])_(.+)$", n)                             # LED cells A-D -> LA-LD
    return f"L{m.group(1)}_{m.group(2)}" if m else n


_EL = K.layout_elements()
BUTTONS = sorted(((e["name"], e["x"], e["y"], e["w"]) for e in _EL.values()
                  if e["kind"] == "button" and X0 <= e["x"] <= 405.0 and e["y"] <= 252), key=lambda b: (b[2], b[1]))

_ROW_GAPS = (47.5, 97.5, 147.5, 197.5)       # board y between button rows
# corners, rear x 16, front middle, left edge and the column between Select and Level at the row gaps, right edge at the
# Level block's bands (y 17 + 55.5, 105.5, 155.5) and next to its first and last ring: no more than 53 mm apart
HOLES = ([(2.6, 2.6), (W - 2.6, 2.6), (2.6, H - 2.6), (W - 2.6, H - 2.6), (16.0, 2.6), (W / 2, H - 2.6)]
         + [(2.6, y) for y in _ROW_GAPS] + [(40.9, y) for y in _ROW_GAPS]
         + [(W - 2.6, M2_DY + y) for y in (2.6, 55.5, 105.5, 155.5, 206.5)])   # 206.5: 6 mm from the Level 8 ring (r 10.5)
CELLS = [("A", "U1", ("C3", "C4", "C5", "C6"), (0, 0)), ("B", "U2", ("C7", "C8", "C9", "C10"), (0, 1))]
SRS, SR_CAPS = ("U3", "U4", "U5"), ("C11", "C12", "C13")


def _own_parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.deck_bus(add, "J1", "Deck bus to P2 2x8 1.27")
    mod = lambda sda, scl, sr_out, sr_in: {**K.CONN, 7: sda, 8: scl, 13: sr_out, 14: sr_in}  # noqa: E731
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
    return P


def _m2_refs(own):
    """M2 ref -> ref on this board: numbered after P3's own parts of the same prefix (U, C, R, RN, D); ENC keep theirs."""
    top = {}
    for p in own:
        m = re.match(r"^([A-Z]+)(\d+)$", p["ref"])
        top[m.group(1)] = max(top.get(m.group(1), 0), int(m.group(2)))
    out = {}
    for p in M2.parts():
        m = re.match(r"^([A-Z]+)(\d+)$", p["ref"])
        if p["ref"] in M2_DROP or m.group(1) == "H":
            continue
        out[p["ref"]] = p["ref"] if m.group(1) == "ENC" else f"{m.group(1)}{top.get(m.group(1), 0) + int(m.group(2))}"
    return out


def parts():
    P = _own_parts()
    refs = _m2_refs(P)
    own_nets = {n for p in P for n in p["pins"].values() if n}
    shared = {"+5V", "+3V3", "GND", "~{INT}", "~{SR_LOAD}", "SR_CLK"} | set(M2_NETS.values())
    for p in M2.parts():
        if p["ref"] not in refs:
            continue
        pins = {k: _m2_net(v) for k, v in p["pins"].items()}
        clash = {n for n in pins.values() if n} & own_nets - shared
        assert not clash, (p["ref"], clash)
        P.append(dict(p, ref=refs[p["ref"]], pins=pins, fields=dict(p["fields"], Block="Level")))
    for h in range(len(HOLES)):
        P.append(dict(ref=f"H{h + 1}", lib="Mechanical:MountingHole", value="M2", fp="MountingHole:MountingHole_2.2mm_M2",
                      pins={}, fields={}))
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
    own = _own_parts()
    rs = sorted((p["ref"] for p in own if p["ref"].startswith("R") and p["ref"][1:].isdigit() and p["ref"] != "R1"),
                key=lambda s: int(s[1:]))
    for n, ref in enumerate(rs):
        pl[ref] = (10.0 + 2.0 * (n % 6), 128.0 + 2.0 * (n // 6), 90, b)
    pl["J3"], pl["R1"] = (26.0, 3.0, 90, b), (26.0, 7.5, 0, b)      # rear edge: M4 right behind P3
    pl["J4"] = (52.0, 3.0, 90, b)                                    # rear edge, behind the Level knobs: W2 over the fold
    m2pl = M2.placement()
    for old, new in _m2_refs(own).items():                          # the Level block where it was on M2, shifted
        x, y, r, side = m2pl[old]
        pl[new] = (x + M2_DX, y + M2_DY, r, side)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm, Level block at", (M2_DX, M2_DY),
          "; unplaced:", [r for r in refs if r not in pl], "; placed, no part:", [r for r in pl if r not in refs],
          "; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
    print("  buttons:", len(BUTTONS), [b[0].encode("ascii", "replace").decode() for b in BUTTONS])
