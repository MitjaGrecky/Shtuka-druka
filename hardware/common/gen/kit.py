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
LAYOUT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "mockup", "layout", "layout_v7.json"))  # panel v7


def layout_elements():
    """{name: element} of the panel layout (x, y = centre, w, h in mm, top view)."""
    import json
    return {e["name"]: e for e in json.load(open(LAYOUT, encoding="utf-8"))["elements"]}

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
def lp5864(add, ref, cell, caps, addr=(0, 0), cs_used=18):
    """LP5864RSMR with its four capacitors (VCC 1u, VLED 4.7u, VCAP 1u, VIO_EN 1n). Nets <cell>_CS0..17,
    <cell>_SW0..3, <cell>_VCAP. addr = (ADDR1, ADDR0): I2C chip address 1 0 0 ADDR1 ADDR0.
    CS lines from cs_used on are left open (no-connect)."""
    a1, a0 = addr
    u = {"1": "+5V", "15": "+5V", "25": f"{cell}_VCAP", "26": "GND", "27": "GND", "28": "SCL", "29": "SDA",
         "30": "+3V3" if a0 else "GND", "31": "+3V3" if a1 else "GND", "32": "+3V3", "33": "GND"}
    u.update({str(2 + n): f"{cell}_CS{n}" if n < cs_used else None for n in range(9)})            # CS0-8 -> pins 2-10
    u.update({str(16 + n): f"{cell}_CS{9 + n}" if 9 + n < cs_used else None for n in range(9)})   # CS9-17 -> pins 16-24
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


def knob_pair(add, names, ring_n=12, clips=(), holes=5):
    """Parts of a two-encoder module on the module bus (M3, M4, M5): J1, bulk caps C1 C2, bus pull-ups R1 R2 (DNP),
    chain-end pull-up R3, LP5864 U1 with C3-C6, LEDs D1.. (left ring on CS9-17, right ring on CS0-8; a ring with
    11 LEDs takes its clip LED as 12th dot), 74HC165 U2 + C7, pull-up packs RN1 RN2, ENC1 ENC2 (MP on GND), holes.
    Returns the shift-register bit list (host reads D7..D0)."""
    bus(add, "J1", "Module bus 2x7 1.27")
    rc(add, "C1", "10u", "+5V", "GND", C0805)
    rc(add, "C2", "1u", "+3V3", "GND")
    rc(add, "R1", "4.7k", "SDA", "+3V3", DNP="yes")           # bus pull-ups live on the host (P2)
    rc(add, "R2", "4.7k", "SCL", "+3V3", DNP="yes")
    rc(add, "R3", "10k", "SR_IN", "+3V3", Note="end of the chain reads 1s when nothing follows")
    lp5864(add, "U1", "A", ("C3", "C4", "C5", "C6"), addr=(0, 0))
    n = 0
    for k in range(2):
        for i in range(ring_n):
            n += 1
            sw, cs = ring_matrix("A", k, i)
            rgb(add, f"D{n}", sw, cs, Ring=names[k], Dot=str(i + 1))
    for k, clip in enumerate(clips):                       # 12th position of ring k's CS triples
        n += 1
        sw, cs = ring_matrix("A", k, ring_n)
        rgb(add, f"D{n}", sw, cs, Note=clip)
    bits = [f"E{k}_{s}" for k in range(2) for s in ("A", "B", "SW")]
    sr165(add, "U2", bits, "SR_IN", "SR_OUT", "C7")
    pullups(add, 1, bits)
    for k in range(2):
        encoder(add, f"ENC{k + 1}", k, mp="GND", note=f"{names[k]}: Alps EC11E1834403 or another smooth EC11 with switch")
    for h in range(holes):
        hole(add, f"H{h + 1}")
    return bits


# ------------------------------------------------------------------ decks (P1, P3, P4)
DECK_FP = "Connector_PinHeader_1.27mm:PinHeader_2x08_P1.27mm_Vertical"
# P100 (proposal): deck bus 2 x 8, 1.27 mm to P2 - pins 1-14 as the module bus, 15 AUX (reserve), 16 GND
DECK_CONN = {**CONN, 15: None, 16: "GND"}


def deck_bus(add, ref, value):
    add(ref, "Connector_Generic:Conn_02x08_Odd_Even", value, DECK_FP,
        {str(p): n for p, n in DECK_CONN.items()}, Side="bottom", Note="P100: deck bus to P2, pin 15 AUX not used")


def i2c_mux(add, ref, addr, chans, caps, res_first):
    """TCA9546A (P99): upstream SDA/SCL from P2; chans = {0: (sd, sc) or None, ...}; 4.7k pull-ups on every used channel;
    ~RESET pulled up; A2 A1 A0 through 0R to GND or +3V3 (addr = 3 bits, 0x70 + addr). Returns the next free R number."""
    u = {"16": "+3V3", "8": "GND", "15": "SDA", "14": "SCL", "3": "MUX_RST"}
    pins = {0: ("4", "5"), 1: ("6", "7"), 2: ("9", "10"), 3: ("11", "12")}
    for ch, (pd, pc) in pins.items():
        nets = chans.get(ch)
        u[pd], u[pc] = (nets if nets else (None, None))
    a = [(addr >> b) & 1 for b in range(3)]
    for b, pin in zip(range(3), ("1", "2", "13")):
        u[pin] = f"MUX_A{b}"
    add(ref, "Interface_Expansion:TCA9546APW", "TCA9546APWR", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm", u,
        Note=f"P99: I2C address 0x{0x70 + addr:02X} (A2 A1 A0 = {a[2]} {a[1]} {a[0]}); LCSC number to choose")
    rc(add, caps, "100n", "+3V3", "GND")
    r = res_first
    rc(add, f"R{r}", "10k", "MUX_RST", "+3V3"); r += 1
    for b in range(3):
        rc(add, f"R{r}", "0", f"MUX_A{b}", "+3V3" if a[b] else "GND", Note="address jumper"); r += 1
    for ch, nets in sorted(chans.items()):
        if nets:
            for n in nets:
                rc(add, f"R{r}", "4.7k", n, "+3V3", Note=f"pull-up of mux channel {ch}"); r += 1
    return r


def deck_inputs(add, names, cells, sr_refs, sr_caps, chain_in, rn_first=1):
    """Buttons with 2 RGB each (P101) read by a 74HC165 chain. names: button names in reading order.
    cells: [(cell, U ref, (4 caps), (ADDR1, ADDR0)), ...] - 12 buttons (24 RGB) per LP5864.
    Q7 of the first register -> SR_OUT; DS of the last <- chain_in. Returns the bit list."""
    for cell, u, caps, addr in cells:
        lp5864(add, u, cell, caps, addr=addr)
    for k, nm in enumerate(names):
        add(f"SW{k + 1}", "Switch:SW_Push", "TS-1187A-B-A-B", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A",
            {"1": f"BTN{k + 1}", "2": "GND"}, LCSC="C318884", Note=nm)
        for side in range(2):
            j = 2 * k + side                       # LED index over the deck
            cell = cells[j // 24][0]
            i = j % 24                             # 24 places per LP5864: CS triple i div 4, SW i mod 4
            c = 3 * (i // 4)
            rgb(add, f"D{j + 1}", f"{cell}_SW{i % 4}", (f"{cell}_CS{c}", f"{cell}_CS{c + 1}", f"{cell}_CS{c + 2}"),
                Note=f"{nm} {'left' if side == 0 else 'right'}")
    bits = [f"BTN{k + 1}" for k in range(len(names))]
    n = len(sr_refs)
    for s, (u, cap) in enumerate(zip(sr_refs, sr_caps)):
        q7 = "SR_OUT" if s == 0 else f"SR_Q{s}"
        ds = chain_in if s == n - 1 else f"SR_Q{s + 1}"
        sr165(add, u, bits[8 * s:8 * s + 8], ds, q7, cap)
    pullups(add, rn_first, bits)
    return bits


def hole(add, ref):
    add(ref, "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2", {})


def corner_holes(w, h, inset=2.6):
    return [(inset, inset), (w - inset, inset), (inset, h - inset), (w - inset, h - inset)]
