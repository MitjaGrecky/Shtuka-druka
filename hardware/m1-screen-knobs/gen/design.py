"""M1 - module of the 8 screen knobs (Param 1-8). Single source of truth for the schematic,
the board and the 3D check: parts, nets, positions.

Panel coordinates come from panel v7 (layout_v7.json, R107): knob k at x = 122.75 + 28 k, y = 277 mm
(y grows from the front edge towards the screen). Board coordinates (KiCad, y down): origin at the
board's rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math
import os

NAME = "m1-screen-knobs"
LP = os.environ.get("M1_LP", "1") == "1"               # rev 0.5 is the default since 14.11.2026 (R148); M1_LP=0 builds the old rev 0.3. Rev 0.5 (job L, 11.11): one TI LP5864 (24 RGB) per pair of rings, 12 LEDs per ring
REV = "0.5" if LP else "0.3"
TITLE = "M1 - screen knobs module (8 encoders, touch, %d-LED RGB rings)" % (12 if LP else 13)

# ------------------------------------------------------------------ geometry (mm)
PITCH = 28.0
KNOB_Y = 277.0                       # panel y of the knob row
X0, X1 = 108.75, 332.75              # board edges in panel x (224 mm = 8 x 28)
Y0, Y1 = 263.0, 297.0                # board edges in panel y (34 mm): P2 ends before 263, the fold is at 300;
                                     # the 6 mm behind the rings give the LED driver room to fan out
W, H = X1 - X0, Y1 - Y0
RING_R = 12.0                        # LED ring radius (ring 24 mm in layout_v7)
RING_N = 12 if LP else 13            # LEDs per ring (P76: 13 = one SW line of IS31FL3741A; rev 0.5: 12 = 24 RGB per LP5864 for a pair)
ARC_START, ARC_SPAN = 225.0, 270.0   # degrees, counter-clockwise from +x, as in the 3D model
BOARD_THICK = 1.6
LAYERS = 4


def panel_to_board(px, py):
    return px - X0, Y1 - py


def knob_xy(k):
    """Board coordinates of the shaft of knob k (0..7)."""
    return panel_to_board(122.75 + PITCH * k, KNOB_Y)


def led_xy(k, i):
    """Board coordinates and rotation of LED i (0..12, value grows clockwise) of ring k."""
    cx, cy = knob_xy(k)
    a = ARC_START - ARC_SPAN * i / (RING_N - 1)
    r = math.radians(a)
    return cx + RING_R * math.cos(r), cy - RING_R * math.sin(r), a - 90.0


# ------------------------------------------------------------------ connector (P77)
# 2 x 7, 1.27 mm, same on every encoder module. Odd pins one row, even pins the other.
CONN = {1: "+5V", 2: "+5V", 3: "GND", 4: "GND", 5: "+3V3", 6: "GND", 7: "SDA", 8: "SCL",
        9: "~{INT}", 10: "GND", 11: "~{SR_LOAD}", 12: "SR_CLK", 13: "SR_OUT", 14: "SR_IN"}

# ------------------------------------------------------------------ shift registers
# 24 inputs: A, B and push of 8 encoders. Host reads U3 D7..D0, then U4, then U5 (U3.Q7 -> SR_OUT).
SR = {"U3": [], "U4": [], "U5": []}
_bits = [f"E{k}_{s}" for k in range(8) for s in ("A", "B", "SW")]
for n, u in enumerate(("U3", "U4", "U5")):
    SR[u] = _bits[8 * n:8 * n + 8]          # SR[u][0] -> D7, SR[u][7] -> D0


def cs_pin(i):
    """IS31FL3741A pin number of CS i (datasheet pin table)."""
    return str(25 + i if i <= 10 else 26 + i if i <= 28 else 27 + i if i <= 33 else i - 33)


ONE_CHIP = os.environ.get("M1_ONE_CHIP") == "1"   # experiment (job J, 07.11): one driver for all 8 rings
FOUR = os.environ.get("M1_FOUR") == "1" or LP     # rev 0.4 experiment (job K, 11.11): one driver per pair of rings
if FOUR:
    CELLS = ("A", "B", "C", "D")    # cell = 2 rings; driver in the rear gap between its two rings (gaps 1, 3, 5, 7)
    DRIVER = {"A": "U1", "B": "U6", "C": "U7", "D": "U8"}
    FAN_ROT = 180 if LP else 225     # IS31FL3741A: side 2 (SW1-7, CS1-5) faces the right ring, side 3 (CS6-12) the left ring
                                    # LP5864 (bottom side, KiCad orientation 180 = pin 1 bottom left in the board view): side 0 (CS0-6) faces the right ring, side 2 (CS10-17) the left ring,
                                    # side 1 (SW0-3) the front, side 3 (control pins) the rear edge
elif ONE_CHIP:
    CELLS = ("A",)
    DRIVER = {"A": "U1"}
    FAN_ROT = 315                   # sides 2+3 (CS1-19) face the right half, sides 4+1 (CS20-39) the left half
else:
    CELLS = ("A", "B")              # P98: two identical cells of 4 knobs, each with its own LED driver
    DRIVER = {"A": "U1", "B": "U6"}
    FAN_ROT = 225                   # side 2 (SW, CS1-5) faces the right pair, side 3 (CS6-18) the left pair


# reference designators of the passives of each LED driver cell
CELL_REFS = {"A": dict(rext="R1", sdb="R2", addr=("R3", "R4", "R5", "R6"), caps=("C1", "C2", "C3", "C4"), fit=0),
             "B": dict(rext="R19", sdb="R20", addr=("R21", "R22", "R23", "R24"), caps=("C14", "C15", "C16", "C17"), fit=1),
             "C": dict(rext="R25", sdb="R26", addr=("R27", "R28", "R29", "R30"), caps=("C18", "C19", "C20", "C21"), fit=2),
             "D": dict(rext="R31", sdb="R32", addr=("R33", "R34", "R35", "R36"), caps=("C22", "C23", "C24", "C25"), fit=3)}


def led_matrix(k, i):
    """(cell, SW, first CS) of LED i of ring k. Ring k belongs to cell k // 4; its driver serves 52 RGB
    on SW1-9 and CS1-18. Inside a cell the rings go in pairs (k % 4 // 2); a pair has three CS triples
    and every triple stays on the rings it lights (cathode arcs drawn by the generator, doc 33):
      first ring:  dots 0-8  -> triple 0, SW1-9;  dots 9-12 -> triple 2, SW1-4
      second ring: dots 0-3  -> triple 2, SW5-8;  dots 4-12 -> triple 1, SW1-9"""
    if LP:            # rev 0.5: LP5864 = 4 SW x 18 CS. Left ring (r 0) on CS9-17 (side 2 of the flipped chip), right ring (r 1) on CS0-8.
        # runs of 4 consecutive dots share a CS triple (cathode arcs drawn by make_pcb); inside a run SW0-3 in turn,
        # every second run reversed (serpentine): dots 3|4 and 7|8 share an SW and sit next to each other
        cell, r = CELLS[k // 2], k % 2
        j, p = i // 4, i % 4
        sw = p if j % 2 == 0 else 3 - p
        return cell, sw, 3 * ((3 if r == 0 else 0) + j)
    if FOUR:          # rev 0.4: model in doc 34 - matrix copper 4250 -> 3600 mm, 27 -> 19 lines per driver
        cell, r = CELLS[k // 2], k % 2
        t = (0 if r else 2) + (i >= 7)          # right ring CS1-6 (side 2), left ring CS7-12 (side 3); runs of 7 and 6 dots
        sw = i + 1 if i < 7 else i - 6          # SW1-7, each SW joins 2 dots of each ring of the pair
        return cell, sw, 3 * t + 1
    if ONE_CHIP:      # one driver: right half (pairs 2, 3) on CS1-18, left half (pairs 1, 0) on CS20-37 (CS19 unused)
        cell, t0 = "A", {0: 9, 1: 6, 2: 0, 3: 3}[k // 2]
    else:
        cell = CELLS[k // 4]
        t0 = 3 * (1 - (k % 4) // 2)    # rev 0.3: right pair on CS1-9 (driver side 2 faces it), left pair on CS10-18
    if k % 2 == 0:
        t, sw = (t0, i + 1) if i <= 8 else (t0 + 2, i - 8)
    else:
        t, sw = (t0 + 2, i + 5) if i <= 3 else (t0 + 1, i - 3)
    return cell, sw, 3 * t + 1 + (t >= 6)


def parts():
    """List of parts: ref, lib_id, value, footprint, {pin: net}, extra fields."""
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    R0402, C0402, C0805 = "Resistor_SMD:R_0402_1005Metric", "Capacitor_SMD:C_0402_1005Metric", "Capacitor_SMD:C_0805_2012Metric"
    add("J1", "Connector_Generic:Conn_02x07_Odd_Even", "Module bus 2x7 1.27",
        "Connector_PinHeader_1.27mm:PinHeader_2x07_P1.27mm_Vertical", {str(p): n for p, n in CONN.items()},
        Side="bottom")
    # LED drivers, one per cell (P98); cell B repeats cell A with its own references and address
    cell_refs = CELL_REFS
    for cell in CELLS:
        c = cell_refs[cell]
        if LP:
            cv, cvled, cvcap, cvio = c["caps"]
            a1, a0 = divmod(CELLS.index(cell), 2)         # I2C address: A = 0 0, B = 0 1, C = 1 0, D = 1 1 (ADDR1 ADDR0)
            u = {"1": "+5V", "15": "+5V", "25": f"{cell}_VCAP", "26": "GND", "27": "GND", "28": "SCL", "29": "SDA",
                 "30": "+3V3" if a0 else "GND", "31": "+3V3" if a1 else "GND", "32": "+3V3", "33": "GND"}
            u.update({str(2 + n): f"{cell}_CS{n}" for n in range(9)})            # CS0-8 -> pins 2-10
            u.update({str(16 + n): f"{cell}_CS{9 + n}" for n in range(9)})       # CS9-17 -> pins 16-24
            u.update({str(11 + n): f"{cell}_SW{n}" for n in range(4)})           # SW0-3 -> pins 11-14
            add(DRIVER[cell], "ShtukaDruka:LP5864", "LP5864RSMR", "ShtukaDruka:VQFN-32-1EP_4x4mm_P0.4mm_EP2.8x2.8mm", u,
                LCSC="C5220564", Cell=cell, Note=f"I2C chip address 10 0 {a1} {a0} (ADDR1 ADDR0 tied on the board); internal current set, no REXT")
            add(cv, "Device:C", "1u", C0402, {"1": "+5V", "2": "GND"}, Note="VCC (pin 1)")
            add(cvled, "Device:C", "4.7u", C0805, {"1": "+5V", "2": "GND"}, Note="VLED (pin 15), SW lines up to ~0.3 A")
            add(cvcap, "Device:C", "1u", C0402, {"1": f"{cell}_VCAP", "2": "GND"}, Note="internal LDO (pin 25)")
            add(cvio, "Device:C", "1n", C0402, {"1": "+3V3", "2": "GND"}, Note="VIO_EN (pin 32)")
            continue
        u = {"14": "+5V", "15": "+5V", "25": "+5V", "9": "SDA", "10": "SCL", "7": "~{INT}", "11": f"{cell}_SDB",
             "8": f"{cell}_ADDR", "13": f"{cell}_REXT", "12": "GND", "36": "GND", "55": "GND", "61": "GND"}
        nsw = 7 if FOUR else 9
        u.update({str(15 + k): (f"{cell}_SW{k}" if k <= nsw else None) for k in range(1, 10)})
        used = set(range(1, 13)) if FOUR else set(range(1, 19)) | (set(range(20, 38)) if ONE_CHIP else set())   # one chip: 12 triples, CS19 skipped
        u.update({cs_pin(i): (f"{cell}_CS{i}" if i in used else None) for i in range(1, 40)})
        add(DRIVER[cell], "ShtukaDruka:IS31FL3741A", "IS31FL3741A-QFLS4-TR",
            "ShtukaDruka:QFN-60-1EP_7x7mm_P0.4mm_EP5.25x5.25mm", u, LCSC="C2940604", Cell=cell)
        add(c["rext"], "Device:R", "20k 1%", R0402, {"1": f"{cell}_REXT", "2": "GND"}, Note="I_peak = 383/20k = 19 mA max per CS")
        add(c["sdb"], "Device:R", "10k", R0402, {"1": f"{cell}_SDB", "2": "+3V3"})
        for n, (to, adr) in enumerate((("GND", "0x30"), ("SCL", "0x31"), ("SDA", "0x32"), ("+5V", "0x33"))):
            f = dict(Note=f"I2C address {adr}")
            if n != c["fit"]:
                f["DNP"] = "yes"
            add(c["addr"][n], "Device:R", "0", R0402, {"1": f"{cell}_ADDR", "2": to}, **f)
        for ref, val, fp in zip(c["caps"], ("4.7u", "1u", "100n", "100n"), (C0805, C0402, C0402, C0402)):
            add(ref, "Device:C", val, fp, {"1": "+5V", "2": "GND"})
    # touch controller
    u2 = {"1": "TR0", "2": "TR1", "12": "TR2", "13": "TR3", "8": "TR4", "9": "TR5", "10": "TR6", "11": "TR7",
          "3": "CMOD", "4": "VREG", "5": "+3V3", "6": "+3V3", "7": "GND", "14": "SDA", "15": "SCL",
          "16": "~{INT}", "17": "GND"}
    add("U2", "Sensor_Touch:CY8CMBR3108", "CY8CMBR3108-LQXIT",
        "Package_DFN_QFN:QFN-16-1EP_3x3mm_P0.5mm_EP1.7x1.7mm", u2, LCSC="C462528")
    for k in range(8):
        add(f"R{7 + k}", "Device:R", "560", R0402, {"1": f"TR{k}", "2": f"TOUCH{k}"})
    add("C5", "Device:C", "2.2n", C0402, {"1": "CMOD", "2": "GND"})
    add("C6", "Device:C", "100n", C0402, {"1": "VREG", "2": "GND"})
    add("C7", "Device:C", "1u", C0402, {"1": "+3V3", "2": "GND"})
    add("C8", "Device:C", "100n", C0402, {"1": "+3V3", "2": "GND"})
    # bus pull-ups (normally on the host board), pull-up of the chain input
    add("R15", "Device:R", "4.7k", R0402, {"1": "SDA", "2": "+3V3"}, DNP="yes")
    add("R16", "Device:R", "4.7k", R0402, {"1": "SCL", "2": "+3V3"}, DNP="yes")
    add("R17", "Device:R", "10k", R0402, {"1": "~{INT}", "2": "+3V3"}, DNP="yes")
    add("R18", "Device:R", "10k", R0402, {"1": "SR_IN", "2": "+3V3"})
    # shift registers
    chain = {"U3": ("SR_Q3", "SR_OUT"), "U4": ("SR_Q4", "SR_Q3"), "U5": ("SR_IN", "SR_Q4")}
    for n, u in enumerate(("U3", "U4", "U5")):
        ds, q7 = chain[u]
        d = {"1": "~{SR_LOAD}", "2": "SR_CLK", "15": "GND", "8": "GND", "16": "+3V3", "10": ds, "9": q7, "7": None}
        dpins = ["6", "5", "4", "3", "14", "13", "12", "11"]        # D7..D0
        for p, net in zip(dpins, SR[u]):
            d[p] = net
        add(u, "74xx:74HC165", "74HC165PW", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm", d)
        add(f"C{9 + n}", "Device:C", "100n", C0402, {"1": "+3V3", "2": "GND"})
    for n in range(6):                                           # 24 pull-ups, 4 per pack
        nets = _bits[4 * n:4 * n + 4]
        pins = {str(i + 1): nets[i] for i in range(4)}
        pins.update({str(8 - i): "+3V3" for i in range(4)})
        add(f"RN{n + 1}", "Device:R_Pack04", "4x10k", "Resistor_SMD:R_Array_Convex_4x0402", pins)
    add("C12", "Device:C", "10u", C0805, {"1": "+5V", "2": "GND"})
    add("C13", "Device:C", "1u", C0402, {"1": "+3V3", "2": "GND"})
    # encoders
    for k in range(8):
        add(f"ENC{k + 1}", "ShtukaDruka:RotaryEncoder_Switch_Touch", "EC11E smooth, switch",
            "ShtukaDruka:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm_Ring",
            {"A": f"E{k}_A", "B": f"E{k}_B", "C": "GND", "S1": f"E{k}_SW", "S2": "GND", "MP": f"TOUCH{k}"},
            Note="Alps EC11E1834403 or another smooth EC11 with switch and metal shaft")
    # LED rings: see led_matrix()
    n = 0
    for k in range(8):
        for i in range(RING_N):
            n += 1
            cell, sw, cs = led_matrix(k, i)
            add(f"D{n}", "ShtukaDruka:XL-1615RGBC-RF", "XL-1615RGBC-RF",
                "ShtukaDruka:LED_RGB_XL-1615RGBC_1.6x1.5mm",
                {"2": f"{cell}_SW{sw}", "1": f"{cell}_CS{cs}", "3": f"{cell}_CS{cs + 1}", "4": f"{cell}_CS{cs + 2}"},
                LCSC="C965840", Ring=str(k + 1), Dot=str(i + 1))
    for h in range(len(HOLES)):
        add(f"H{h + 1}", "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2", {})
    return P


# ------------------------------------------------------------------ placement on the board
# Top side: only the 8 encoders and the 104 LEDs (clean for the light guide under the panel).
# Bottom side: everything else in the rear strip (y 0-7), where no ring via can land (ring vias sit at
# r 11.5-12.5 around y 20, the top of a ring is at y 7.5), plus the two drivers in gaps 2 and 6 and J1
# with its bulk capacitors in gap 2 at the front. Gap g centre x = 28 g.
GAP = {g: PITCH * g for g in range(1, 8)}
# Mounting (P97, adjusted): M2 heat-set inserts in the light guide, screws from below. Corners plus one
# hole every second knob in the rear strip: gaps 1, 3, 5, 7 (gaps 2 and 6 hold the LED drivers).
HOLES = [(2.6, 2.6), (W - 2.6, 2.6), (2.6, H - 2.6), (W - 2.6, H - 2.6)] + [(GAP[g], 2.6) for g in ((2, 4, 6) if FOUR else (1, 3, 5, 7))]
# rev 0.4 (FOUR): drivers take gaps 1, 3, 5, 7, so the holes go to gaps 2, 4, 6 (P97 as first proposed)
DRIVER_Y = 6.6 if ONE_CHIP else 6.0   # one chip: its SW side faces the rear edge
STRIP_Y = 4.2                        # centre line of the rear strip parts
# Bulk capacitors C1, C14 (4.7u) stay beside the driver; decoupling capacitors that make_pcb puts right at their pins: (cap, ic, pin, row); row 1, 2 sit
# further out than row 0. Pins: IS31FL3741A VCC 14, 15, 25; CY8CMBR3108 CMOD 3, VREG 4, VDD 5, 6;
# 74HC165 VCC 16.
# Rev 0.3: the LED drivers stand as a diamond (45 deg) with a scripted fan-out, their capacitors are left to the placer.
HUG = [("C5", "U2", "3", 0), ("C6", "U2", "4", 1), ("C8", "U2", "6", 0), ("C7", "U2", "5", 1),
       ("C9", "U3", "16", 0), ("C10", "U4", "16", 0), ("C11", "U5", "16", 0)]


def placement():
    """ref -> (x, y, rotation, side); board coordinates, rotation in degrees (KiCad).
    Capacitors listed in HUG get a provisional spot here; make_pcb moves them to their pins."""
    pl = {}
    for k in range(8):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, "top")        # A/B/C on the left, switch on the right
        for i in range(RING_N):
            x, y, a = led_xy(k, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, "top")
    b, y = "bottom", STRIP_Y
    # shift registers with their pull-up packs, rear strip
    for u, x, rn in (("U3", 15.0, ("RN1", "RN2")), ("U4", 95.0, ("RN3", "RN4")), ("U5", 209.0, ("RN5", "RN6"))):
        pl[u] = (x, y, 0, b)
        pl[rn[0]], pl[rn[1]] = (x - 6.0, y, 90, b), (x + 6.0, y, 90, b)
    pl["R18"] = (215.0, 6.3, 0, b)
    # bus connector at the front of gap 2, its bulk capacitors just behind it
    pl["J1"] = (GAP[2], H - 3.0, 90, b)
    pl["C12"], pl["C13"] = (GAP[2], H - 6.7, 0, b), (GAP[2], H - 8.8, 0, b)
    for n, r in enumerate(("R15", "R16", "R17")):      # optional bus pull-ups (normally on the host)
        pl[r] = (124.0, 1.6 + 2.0 * n, 0, b)
    # LED drivers in gaps 2 and 6, rear strip; their resistors on the left, capacitors at the pins
    drv = (("U1", 4 if ONE_CHIP else 2, ("R1", "R2", "R3", "R4", "R5", "R6"), ("C1", "C2", "C3", "C4")),
           ("U6", 6, ("R19", "R20", "R21", "R22", "R23", "R24"), ("C14", "C15", "C16", "C17")))[:len(CELLS)]
    if FOUR:
        drv = tuple((DRIVER[c], g, () if LP else (CELL_REFS[c]["rext"], CELL_REFS[c]["sdb"]) + CELL_REFS[c]["addr"], CELL_REFS[c]["caps"])
                    for c, g in zip(CELLS, (1, 3, 5, 7)))
    for u, g, rs, cs in drv:
        x = GAP[g]
        pl[u] = (x, DRIVER_Y, 0, b)            # make_pcb.driver_fanout() turns it to the diamond and fans out
        for n, r in enumerate(rs):
            pl[r] = (x - 7.4 - 2.2 * (n // 3), 2.0 + 2.2 * (n % 3), 0, b)
        for n, c in enumerate(cs):
            pl[c] = (x + (6.6 if LP else 7.4), 2.0 + 2.2 * n, 0, b)
    # touch controller near the middle (gap 4), its series resistors in a row beside it
    pl["U2"] = (118.0, 4.0, 0, b)
    for n in range(8):
        pl[f"R{7 + n}"] = (104.5 + 1.2 * n, 4.0, 90, b)
    for n, c in enumerate(("C5", "C6", "C7", "C8")):
        pl[c] = (121.5, 1.6 + 1.6 * n, 0, b)
    pl["C9"], pl["C10"], pl["C11"] = (15.0, 6.5, 0, b), (95.0, 6.5, 0, b), (209.0, 6.5, 0, b)
    for n, (hx, hy) in enumerate(HOLES):
        pl[f"H{n + 1}"] = (hx, hy, 0, "top")
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    missing = [p["ref"] for p in P if p["ref"] not in pl]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", missing)
