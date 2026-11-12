"""Shared building blocks of the digital boards (SPEC_boards.md, 12.11.2026): module bus, LP5864 with its
parts, 74HC165 chain, encoder, LED ring geometry and matrix, mounting holes.

Every helper takes `add(ref, lib, value, fp, pins, **fields)` - the parts-list callback of a design.py -
so a board's design.py stays the single source of truth for its parts and nets.
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (hardware data).
"""
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
M1_LIB = os.path.abspath(os.path.join(HERE, "..", "..", "m1-screen-knobs", "lib"))   # shared project library

R0402, C0402, C0805 = "Resistor_SMD:R_0402_1005Metric", "Capacitor_SMD:C_0402_1005Metric", "Capacitor_SMD:C_0805_2012Metric"
# only numbers already used in the project (W1, M1); 4.7u 0805, 1n 0402, 560 0402 have none yet ("choose a part" in M1's BOM_notes)
LCSC = {"100n": "C1525", "1u": "C52923", "10u": "C15850", "10k": "C25744", "4.7k": "C25900", "1k": "C11702"}

# ------------------------------------------------------------------ module bus (R123), 2 x 7, 1.27 mm
CONN = {1: "+5V", 2: "+5V", 3: "GND", 4: "GND", 5: "+3V3", 6: "GND", 7: "SDA", 8: "SCL",
        9: "~{INT}", 10: "GND", 11: "~{SR_LOAD}", 12: "SR_CLK", 13: "SR_OUT", 14: "SR_IN"}
BUS_FP = "Connector_PinHeader_1.27mm:PinHeader_2x07_P1.27mm_Vertical"


def bus(add, ref, value, conn=CONN):
    add(ref, "Connector_Generic:Conn_02x07_Odd_Even", value, BUS_FP,
        {str(p): n for p, n in conn.items()}, LCSC="C3975190", Side="bottom")


def rc(add, ref, value, a, b, fp=None, **f):
    """Resistor or capacitor by its reference letter, 0402 unless fp is given."""
    lib = "Device:R" if ref.startswith("R") else "Device:C"
    if value in LCSC:
        f.setdefault("LCSC", LCSC[value])
    add(ref, lib, value, fp or (R0402 if lib == "Device:R" else C0402), {"1": a, "2": b}, **f)


# ------------------------------------------------------------------ LED driver TI LP5864 (4 SW x 18 CS = 24 RGB)
def lp5864(add, ref, cell, caps, addr=(0, 0)):
    """LP5864RSMR with its four capacitors (VCC 1u, VLED 4.7u, VCAP 1u, VIO_EN 1n). Nets <cell>_CS0..17,
    <cell>_SW0..3, <cell>_VCAP. addr = (ADDR1, ADDR0): I2C chip address 1 0 0 ADDR1 ADDR0."""
    a1, a0 = addr
    u = {"1": "+5V", "15": "+5V", "25": f"{cell}_VCAP", "26": "GND", "27": "GND", "28": "SCL", "29": "SDA",
         "30": "+3V3" if a0 else "GND", "31": "+3V3" if a1 else "GND", "32": "+3V3", "33": "GND"}
    u.update({str(2 + n): f"{cell}_CS{n}" for n in range(9)})            # CS0-8 -> pins 2-10
    u.update({str(16 + n): f"{cell}_CS{9 + n}" for n in range(9)})       # CS9-17 -> pins 16-24
    u.update({str(11 + n): f"{cell}_SW{n}" for n in range(4)})           # SW0-3 -> pins 11-14
    add(ref, "ShtukaDruka:LP5864", "LP5864RSMR", "ShtukaDruka:VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm", u,
        LCSC="C5220564", Cell=cell, Note=f"I2C chip address 1 0 0 {a1} {a0} (ADDR1 ADDR0 tied on the board); internal current set")
    cv, cvled, cvcap, cvio = caps
    rc(add, cv, "1u", "+5V", "GND", Note="VCC (pin 1)")
    rc(add, cvled, "4.7u", "+5V", "GND", C0805, Note="VLED (pin 15)")
    rc(add, cvcap, "1u", f"{cell}_VCAP", "GND", Note="internal LDO (pin 25)")
    rc(add, cvio, "1n", "+3V3", "GND", Note="VIO_EN (pin 32)")


def rgb(add, ref, sw, cs, **f):
    """XL-1615RGBC-RF: 2 common anode on an SW line, cathodes 1 R, 3 G, 4 B on the CS triple cs, cs+1, cs+2."""
    add(ref, "ShtukaDruka:XL-1615RGBC-RF", "XL-1615RGBC-RF", "ShtukaDruka:LED_RGB_XL-1615RGBC_1.6x1.5mm",
        {"2": sw, "1": cs[0], "3": cs[1], "4": cs[2]}, LCSC="C965840", **f)


def ring_matrix(cell, r, i):
    """(SW net, CS triple) of LED i of ring r (0 = left, 1 = right) of a ring pair on one LP5864, as M1 rev 0.5:
    left ring on CS9-17, right ring on CS0-8; runs of 4 dots share a CS triple, SW0-3 in a serpentine."""
    j, p = i // 4, i % 4
    sw = p if j % 2 == 0 else 3 - p
    c = 3 * ((3 if r == 0 else 0) + j)
    return f"{cell}_SW{sw}", (f"{cell}_CS{c}", f"{cell}_CS{c + 1}", f"{cell}_CS{c + 2}")


ARC_START, ARC_SPAN = 225.0, 270.0   # degrees, counter-clockwise from +x; value grows clockwise


def ring_xy(cx, cy, radius, n, i):
    """Board coordinates and rotation of LED i of an n-LED ring around (cx, cy) (KiCad, y down)."""
    a = ARC_START - ARC_SPAN * i / (n - 1)
    t = math.radians(a)
    return cx + radius * math.cos(t), cy - radius * math.sin(t), a - 90.0


# ------------------------------------------------------------------ inputs: 74HC165 chain, encoders
SR_D = ["6", "5", "4", "3", "14", "13", "12", "11"]       # D7..D0


def sr165(add, ref, bits, ds, q7, cap):
    """74HC165PW: bits[0] -> D7 ... bits[7] -> D0 (None or missing -> +3V3, reads 1). Serial in ds, out q7."""
    d = {"1": "~{SR_LOAD}", "2": "SR_CLK", "15": "GND", "8": "GND", "16": "+3V3", "10": ds, "9": q7, "7": None}
    for p, net in zip(SR_D, list(bits) + [None] * (8 - len(bits))):
        d[p] = net or "+3V3"
    add(ref, "74xx:74HC165", "74HC165PW", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm", d, LCSC="C80696")
    rc(add, cap, "100n", "+3V3", "GND")


def pullups(add, first, nets):
    """4 x 10k packs to +3V3 for the given nets; refs RN<first>, RN<first+1>, ...; unused resistors left open."""
    refs = []
    for n in range(0, len(nets), 4):
        grp = nets[n:n + 4]
        pins = {}
        for i in range(4):
            net = grp[i] if i < len(grp) else None
            pins[str(i + 1)] = net
            pins[str(8 - i)] = "+3V3" if net else None
        ref = f"RN{first + n // 4}"
        add(ref, "Device:R_Pack04", "4x10k", "Resistor_SMD:R_Array_Convex_4x0402", pins, LCSC="C25725")
        refs.append(ref)
    return refs


def encoder(add, ref, k, mp="GND", note=""):
    """Alps EC11E smooth with switch: A, B, push S1 -> E<k>_A, E<k>_B, E<k>_SW; C and S2 on GND; MP (frame) on mp."""
    add(ref, "ShtukaDruka:RotaryEncoder_Switch_Touch", "EC11E smooth, switch",
        "ShtukaDruka:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm_Ring",
        {"A": f"E{k}_A", "B": f"E{k}_B", "C": "GND", "S1": f"E{k}_SW", "S2": "GND", "MP": mp},
        Note=note or "Alps EC11E1834403 or another smooth EC11 with switch and metal shaft")


ENC_SHAFT = (7.5, 2.5)          # shaft relative to pad A in the encoder footprint


def hole(add, ref):
    add(ref, "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2", {})


def corner_holes(w, h, inset=2.6):
    return [(inset, inset), (w - inset, inset), (inset, h - inset), (w - inset, h - inset)]
