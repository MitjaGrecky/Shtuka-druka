"""P4 - Right deck: 20 buttons of the value column with 2 RGB each, crossfader (ADS1115), wheel (AS5600), I2C mux, buses.
Single source of truth for the schematic and the board. Spec: hardware/for-routing/SPEC_boards.md, section P4.

Panel (layout_v7.json, x 413-505, y <= 252): Scene A, Scene B, Chords, Touch FX, Scale, Clips, Steps, Notes, Sound, Effects,
Mod, Mixer, Song, Browser, Sampler, Inputs, Settings, Page <, Back, Page >; crossfader x 459, y 22 (travel about 45 mm,
part not chosen - P90: Bourns PTA4543 footprint as a placeholder); wheel x 459, y 277, 38 mm. Board x 413-505, y 4-297
(92 x 293: no cut-out for the M modules on this side).
Proposals (constants below): P99 - TCA9546A at 0x72: channel 0 own LP5864s, ADS1115 0x48 and AS5600 0x36, 1 -> J3 (W3),
2 and 3 free; P100 - J1 2 x 8 to P2; P101 - 2 RGB per button (40 RGB: cell A 0x40 buttons 1-12, B 0x41 buttons 13-20);
P104 - the crossfader is digitised here (wiper -> 1k / 100n -> ADS1115 AIN0), no analogue signal on the ribbon.
Wheel: AS5600 on the top side right under the wheel's magnet (3.3 V mode: VDD5V = VDD3V3 = +3V3, DIR to GND).
The wheel push ("OK" in the panel description) is not in the spec: its input is reserved (WHEEL_PUSH, bit 21, J4 2-pin
JST PH for a switch in the wheel mechanism) - question V10. Chain: host reads P4 (U3 first: Scene A ...), then W3 (J3):
U5.DS <- SR_W3 (J3 pin 13); J3 pin 14 (W3's SR_IN) <- SR_END pulled up here.
Board coordinates (KiCad, y down): origin at the rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "p4-right"
ID = "P4"
TITLE = "P4 - Right deck: 20 buttons with 2 RGB, crossfader, wheel, I2C mux, bus to P2 and W3"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("J1 deck bus 2x8 to P2 (P100); TCA9546A 0x72 (P99): ch0 own LEDs + ADS1115 0x48 + AS5600 0x36, ch1 J3 -> W3; "
            "chain P4 -> W3")

X0, X1 = 413.0, 505.0
Y0, Y1 = 4.0, 297.0
W, H = X1 - X0, Y1 - Y0                      # 92 x 293
LAYERS = 2
MUX_ADDR = 2                                 # P99: 0x70 + 2 = 0x72
LED_DX, LED_DX_NARROW = 6.5, 5.5             # P84 (buttons up to 16 mm wide: 5.5)
WHEEL_PUSH = True                            # V10: reserve an input and a connector for a push switch in the wheel

_EL = K.layout_elements()
# the 20 buttons of the column, in reading order: rows from the front (low y), left to right
BUTTONS = sorted(((e["name"], e["x"], e["y"], e["w"]) for e in _EL.values()
                  if e["kind"] == "button" and X0 <= e["x"] <= X1 and e["y"] <= 252), key=lambda b: (b[2], b[1]))
XFADER = (_EL["Crossfader"]["x"], _EL["Crossfader"]["y"])
WHEEL = (_EL["Wheel"]["x"], _EL["Wheel"]["y"], _EL["Wheel"]["w"])


def panel_to_board(px, py):
    return px - X0, Y1 - py


# holes: corners; rear edge clear of the wheel (x 27-65); front middle; long sides at rows without buttons, <= 60 mm apart
_SIDE_Y = (50.0, 95.0, 132.5, 185.0, 232.5)
HOLES = (K.corner_holes(W, H) + [(20.0, 2.6), (72.0, 2.6), (W / 2, H - 2.6)]
         + [(x, y) for y in _SIDE_Y for x in (2.6, W - 2.6)])
CELLS = [("A", "U1", ("C3", "C4", "C5", "C6"), (0, 0)), ("B", "U2", ("C7", "C8", "C9", "C10"), (0, 1))]
SRS, SR_CAPS = ("U3", "U4", "U5"), ("C11", "C12", "C13")


def parts():
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    K.deck_bus(add, "J1", "Deck bus to P2 2x8 1.27")
    K.bus(add, "J3", "Module bus to W3 2x7 1.27", {**K.CONN, 7: "SD1", 8: "SC1", 13: "SR_W3", 14: "SR_END"})
    K.rc(add, "C1", "10u", "+5V", "GND", K.C0805)
    K.rc(add, "C2", "1u", "+3V3", "GND")
    K.rc(add, "R1", "10k", "SR_END", "+3V3", Note="end of the chain (W3 SR_IN) reads 1s")
    r = K.i2c_mux(add, "U6", MUX_ADDR, {0: ("SD0", "SC0"), 1: ("SD1", "SC1"), 2: None, 3: None}, "C14", 2)
    names = [b[0] for b in BUTTONS]
    bits = K.deck_inputs(add, names, CELLS, SRS, SR_CAPS, "SR_W3")
    for p in P:                                  # LED drivers on mux channel 0
        if p["ref"] in ("U1", "U2"):
            p["pins"]["29"], p["pins"]["28"] = "SD0", "SC0"
    if WHEEL_PUSH:                               # bit 21 (U5 D3): wheel push, pull-up in the 6th pack slot
        u5 = next(p for p in P if p["ref"] == "U5")
        u5["pins"][K.SR_D[len(bits) - 16]] = "WHEEL_PUSH"
        K.pullups(add, 1 + (len(bits) + 3) // 4, ["WHEEL_PUSH"])
        add("J4", "Connector_Generic:Conn_01x02", "Wheel push", "Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical",
            {"1": "WHEEL_PUSH", "2": "GND"}, LCSC="C20504437", Side="bottom", Note="V10: switch in the wheel mechanism (to confirm)")
    # crossfader (P104): slide pot -> 1k / 100n -> ADS1115 AIN0; AIN1-3 unused (to GND)
    add("RV1", "Device:R_Potentiometer", "10k lin, 45 mm travel", "Potentiometer_THT:Potentiometer_Bourns_PTA4543_Single_Slide",
        {"1": "GND", "2": "XFADER", "3": "+3V3"}, LCSC="C17444183",
        Note="crossfader - part not chosen (P90): Bourns PTA4543-2015DPB103 as a placeholder")
    K.rc(add, f"R{r}", "1k", "XFADER", "AIN0"); r += 1
    K.rc(add, "C15", "100n", "AIN0", "GND")
    add("U7", "Analog_ADC:ADS1115IDGS", "ADS1115IDGSR", "Package_SO:TSSOP-10_3x3mm_P0.5mm",
        {"1": "GND", "2": None, "3": "GND", "4": "AIN0", "5": "GND", "6": "GND", "7": "GND", "8": "+3V3", "9": "SD0", "10": "SC0"},
        LCSC="C37593", Note="I2C 0x48 (ADDR = GND), crossfader on AIN0 (P104)")
    K.rc(add, "C16", "100n", "+3V3", "GND")
    # wheel: AS5600 under the magnet, 3.3 V mode
    add("U8", "Common:AS5600", "AS5600-ASOM", "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",
        {"1": "+3V3", "2": "+3V3", "3": None, "4": "GND", "5": None, "6": "SD0", "7": "SC0", "8": "GND"},
        LCSC="C79815", Note="I2C 0x36; centred under the wheel magnet; DIR = GND (angle grows clockwise from the top)")
    K.rc(add, "C17", "100n", "+3V3", "GND", Note="AS5600 VDD")
    K.rc(add, "C18", "1u", "+3V3", "GND", Note="AS5600 VDD3V3")
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
    xf = panel_to_board(*XFADER)
    pl["RV1"] = (xf[0], xf[1], 0, t)                       # travel along x, centred on the panel slot
    wx, wy = panel_to_board(*WHEEL[:2])
    pl["U8"] = (wx, wy, 0, t)                              # exactly under the wheel axis
    pl["C17"], pl["C18"] = (wx - 3.0, wy, 90, b), (wx + 3.0, wy, 90, b)
    for (cell, u, caps, _), y in zip(CELLS, (225.0, 125.0)):
        pl[u] = (mx, y, 0, b)
        for n, c in enumerate(caps):
            pl[c] = (mx + 4.6, y - 3.0 + 2.0 * n, 0, b)
    for u, cap, y in zip(SRS, SR_CAPS, (258.0, 195.0, 100.0)):
        pl[u] = (mx - 14.0, y, 90, b)
        pl[cap] = (mx - 8.5, y, 90, b)
    for n in range(6):
        pl[f"RN{n + 1}"] = (mx - 20.0, 262.0 - 34.0 * n, 90, b)
    # crossfader ADC near the fader, mux and its resistors near J1 (left edge: P2 is to the left)
    pl["U7"], pl["C15"], pl["C16"] = (mx + 16.0, 262.0, 0, b), (mx + 12.0, 258.0, 90, b), (mx + 20.0, 258.0, 90, b)
    pl["U6"], pl["C14"] = (14.0, 150.0, 0, b), (14.0, 145.0, 0, b)
    rs = sorted((p["ref"] for p in parts() if p["ref"].startswith("R") and p["ref"][1:].isdigit()), key=lambda s: int(s[1:]))
    rx = next(p["ref"] for p in parts() if p["pins"].get("1") == "XFADER" and p["ref"].startswith("R"))
    for n, ref in enumerate(r for r in rs if r not in ("R1", rx)):   # mux reset, address, channel pull-ups
        pl[ref] = (10.0 + 2.0 * (n % 5), 156.0 + 2.0 * (n // 5), 90, b)
    pl[rx] = (mx + 16.0, 267.0, 0, b)                                # crossfader RC, at the ADC
    pl["J1"] = (3.0, 150.0, 0, b)
    pl["C1"], pl["C2"] = (3.0, 159.0, 0, b), (3.0, 161.0, 0, b)
    pl["J3"], pl["R1"] = (60.0, 3.0, 90, b), (60.0, 7.5, 0, b)  # rear edge, over the fold to W3 (W3's J1 at panel x 473)
    pl["J4"] = (34.0, 6.0, 0, b)                                 # beside the wheel
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", [r for r in refs if r not in pl],
          "; placed but no part:", [r for r in pl if r not in refs])
    print("  buttons:", len(BUTTONS), "; crossfader", panel_to_board(*XFADER), "; wheel", panel_to_board(*WHEEL[:2]))
