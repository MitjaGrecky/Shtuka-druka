"""M1 - module of the 8 screen knobs (Param 1-8). Single source of truth for the schematic,
the board and the 3D check: parts, nets, positions.

Panel coordinates come from panel v7 (layout_v7.json, R107): knob k at x = 122.75 + 28 k, y = 277 mm
(y grows from the front edge towards the screen). Board coordinates (KiCad, y down): origin at the
board's rear-left corner, x = panel_x - X0, y = Y1 - panel_y.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math

NAME = "m1-screen-knobs"
TITLE = "M1 - screen knobs module (8 encoders, touch, 13-LED RGB rings)"
REV = "0.1"

# ------------------------------------------------------------------ geometry (mm)
PITCH = 28.0
KNOB_Y = 277.0                       # panel y of the knob row
X0, X1 = 108.75, 332.75              # board edges in panel x (224 mm = 8 x 28)
Y0, Y1 = 263.0, 291.0                # board edges in panel y (28 mm): knob row +-14; P2 ends before 263
W, H = X1 - X0, Y1 - Y0
RING_R = 12.0                        # LED ring radius (ring 24 mm in layout_v7)
RING_N = 13                          # LEDs per ring (P76: 13 = one SW line of IS31FL3741A)
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


def parts():
    """List of parts: ref, lib_id, value, footprint, {pin: net}, extra fields."""
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    R0402, C0402, C0805 = "Resistor_SMD:R_0402_1005Metric", "Capacitor_SMD:C_0402_1005Metric", "Capacitor_SMD:C_0805_2012Metric"
    add("J1", "Connector_Generic:Conn_02x07_Odd_Even", "Module bus 2x7 1.27",
        "Connector_PinHeader_1.27mm:PinHeader_2x07_P1.27mm_Vertical", {str(p): n for p, n in CONN.items()},
        Side="bottom")
    # LED driver
    cs = {}
    for i in range(1, 40):
        cs[str(25 + i if i <= 10 else 26 + i if i <= 28 else 27 + i if i <= 33 else i - 33)] = f"CS{i}"
    u1 = {"14": "+5V", "15": "+5V", "25": "+5V", "9": "SDA", "10": "SCL", "7": "~{INT}", "11": "SDB",
          "8": "ADDR", "13": "REXT", "12": "GND", "36": "GND", "55": "GND", "61": "GND"}
    u1.update({str(15 + k): f"SW{k}" for k in range(1, 10)})
    u1.update(cs)
    u1["24"] = None                                        # SW9 unused
    add("U1", "ShtukaDruka:IS31FL3741A", "IS31FL3741A-QFLS4-TR",
        "ShtukaDruka:QFN-60-1EP_7x7mm_P0.4mm_EP5.25x5.25mm", u1, LCSC="C2940604")
    add("R1", "Device:R", "20k 1%", R0402, {"1": "REXT", "2": "GND"}, Note="I_peak = 383/20k = 19 mA max per CS")
    add("R2", "Device:R", "10k", R0402, {"1": "SDB", "2": "+3V3"})
    add("R3", "Device:R", "0", R0402, {"1": "ADDR", "2": "GND"}, Note="I2C address 0x30 (ADDR=GND)")
    add("R4", "Device:R", "0", R0402, {"1": "ADDR", "2": "SCL"}, DNP="yes", Note="0x31")
    add("R5", "Device:R", "0", R0402, {"1": "ADDR", "2": "SDA"}, DNP="yes", Note="0x32")
    add("R6", "Device:R", "0", R0402, {"1": "ADDR", "2": "+5V"}, DNP="yes", Note="0x33")
    add("C1", "Device:C", "4.7u", C0805, {"1": "+5V", "2": "GND"})
    add("C2", "Device:C", "1u", C0402, {"1": "+5V", "2": "GND"})
    add("C3", "Device:C", "100n", C0402, {"1": "+5V", "2": "GND"})
    add("C4", "Device:C", "100n", C0402, {"1": "+5V", "2": "GND"})
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
            "Rotary_Encoder:RotaryEncoder_Alps_EC11E-Switch_Vertical_H20mm",
            {"A": f"E{k}_A", "B": f"E{k}_B", "C": "GND", "S1": f"E{k}_SW", "S2": "GND", "MP": f"TOUCH{k}"},
            Note="Alps EC11E1834403 or another smooth EC11 with switch and metal shaft")
    # LED rings: ring k -> SW(k+1); LED i -> CS(3i+1) R, CS(3i+2) G, CS(3i+3) B
    n = 0
    for k in range(8):
        for i in range(RING_N):
            n += 1
            add(f"D{n}", "ShtukaDruka:XL-1615RGBC-RF", "XL-1615RGBC-RF",
                "ShtukaDruka:LED_RGB_XL-1615RGBC_1.6x1.5mm",
                {"2": f"SW{k + 1}", "1": f"CS{3 * i + 1}", "3": f"CS{3 * i + 2}", "4": f"CS{3 * i + 3}"},
                LCSC="C965840", Ring=str(k + 1), Dot=str(i + 1))
    for h in range(4):
        add(f"H{h + 1}", "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2", {})
    return P


# ------------------------------------------------------------------ placement on the board
# Top side: only the 8 encoders and the 104 LEDs (clean for the light guide under the panel).
# Bottom side: all ICs, passives and the bus connector, in the 11 mm gaps between encoders
# (gap g centre x = 28 g, g = 1..7), where no encoder pins are.
GAP = {g: PITCH * g for g in range(1, 8)}


def placement():
    """ref -> (x, y, rotation, side); board coordinates, rotation in degrees (KiCad)."""
    pl = {}
    for k in range(8):
        cx, cy = knob_xy(k)
        pl[f"ENC{k + 1}"] = (cx, cy, 0, "top")        # A/B/C on the left, switch on the right
        for i in range(RING_N):
            x, y, a = led_xy(k, i)
            pl[f"D{k * RING_N + i + 1}"] = (x, y, a, "top")
    c = H / 2
    b = "bottom"

    def col(x, refs, y0, dy, rot=90):
        for n, r in enumerate(refs):
            pl[r] = (x, y0 + n * dy, rot, b)

    # shift registers with their pull-up packs (gaps 1, 3, 6)
    for u, g, rn in (("U3", 1, ("RN1", "RN2")), ("U4", 3, ("RN3", "RN4")), ("U5", 6, ("RN5", "RN6"))):
        x = GAP[g]
        pl[u] = (x, c, 0, b)
        pl[rn[0]], pl[rn[1]] = (x, 4.0, 0, b), (x, H - 4.0, 0, b)
    pl["C9"], pl["C10"], pl["C11"] = (GAP[1], 7.6, 0, b), (GAP[3], 7.6, 0, b), (GAP[6], 7.6, 0, b)
    pl["R18"] = (GAP[6], H - 7.6, 0, b)
    # bus connector (gap 2), bulk capacitors, optional pull-ups
    # J1 lies along the front edge, below the waist between rings 2 and 3 (make_pcb centres its pads here)
    pl["J1"] = (GAP[2], H - 3.0, 90, b)
    pl["C12"], pl["C13"] = (GAP[2], 3.0, 0, b), (GAP[2], 6.0, 0, b)
    for n, r in enumerate(("R15", "R16", "R17")):
        pl[r] = (GAP[2] - 2.4 + 2.4 * n, 9.5, 90, b)
    # LED driver (gap 4)
    x = GAP[4]
    pl["U1"] = (x, c + 3.5, 0, b)                    # off the waist: its thermal vias clear the ring LEDs
    for n, r in enumerate(("R1", "R2", "R3", "R4")):
        pl[r] = (x - 3.6 + 2.4 * n, 2.2, 90, b)
    for n, r in enumerate(("R5", "R6", "C2", "C3")):
        pl[r] = (x - 3.6 + 2.4 * n, 5.0, 90, b)
    pl["C4"], pl["C1"] = (x - 2.4, H - 3.4, 90, b), (x + 1.2, H - 3.0, 90, b)
    # touch controller (gap 5)
    x = GAP[5]
    pl["U2"] = (x, c, 0, b)
    for n in range(4):
        pl[f"R{7 + n}"] = (x - 3.6 + 2.4 * n, 2.2, 90, b)
        pl[f"R{11 + n}"] = (x - 3.6 + 2.4 * n, H - 2.2, 90, b)
    for n, r in enumerate(("C5", "C6", "C7", "C8")):
        pl[r] = (x - 3.6 + 2.4 * n, 5.4, 90, b)
    for n, (hx, hy) in enumerate(((2.6, 2.6), (W - 2.6, 2.6), (2.6, H - 2.6), (W - 2.6, H - 2.6))):
        pl[f"H{n + 1}"] = (hx, hy, 0, "top")
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    missing = [p["ref"] for p in P if p["ref"] not in pl]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; unplaced:", missing)
