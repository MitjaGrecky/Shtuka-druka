"""W1 - Levels board on the slope (left column). Single source of truth for the schematic,
the board and the 3D check: parts, nets, positions.

What sits here (panel v7, layout_v7.json, R107): 4 volume pots with end stops (Main, Cue Mix,
Phones 1, Phones 2; R13, R87), 2 P48 buttons (phantom power, lit amber), and a window for the
encoder module M5 (Gain 1 + 2, R119). W1 has no microcontroller: it speaks the same 2 x 7 module
bus as the encoder modules (R123) - I2C for the pot ADC and the LED driver, the shift-register
chain for the buttons - and passes the bus on to M5.

Coordinates. Panel: x from the left side; on the slope the panel y is the top-view projection
(fold y 300, shelf y 430, slope 30 degrees). Slope coordinate s = (y - 300) / cos 30, measured
along the slope from the fold. Board (KiCad, y down, looking at the top side): origin at the
board's rear-left corner (high s), x = panel_x - X0, y = S1 - s.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import math
import os

NAME = "w1-levels"
TITLE = "W1 - Levels (slope, left): 4 volume pots, 2 P48 buttons, window for M5 Gain"
REV = "0.1"

HERE = os.path.dirname(os.path.abspath(__file__))
M1_LIB = os.path.join(HERE, "..", "..", "m1-screen-knobs", "lib")   # shared project library (LED 1615)

# ------------------------------------------------------------------ geometry (mm)
COS = math.cos(math.radians(30.0))
X0, X1 = 10.0, 102.0                 # board edges in panel x (left column, R107)
S0, S1 = 12.0, 138.0                 # board edges along the slope (slope length 150.1)
W, H = X1 - X0, S1 - S0              # 92 x 126
LAYERS = 2
BELOW_SKIN = 8.5                     # board top face under the skin's inner face: pot body <= 7.4 + 1 mm air
# window for the M5 module (its own board in the plane of the encoder modules, 6.5 mm under the skin)
M5_X = (5.0, 87.0)                   # board x of the module outline (82 mm: 2 encoders 48 apart, rings, Clip LEDs)
WIN_GAP = 0.5


def s_of(py):
    return (py - 300.0) / COS


def panel_to_board(px, py):
    return px - X0, S1 - s_of(py)


POTS = [("Main", 32, 323), ("Cue Mix", 80, 323), ("Phones 1", 32, 351), ("Phones 2", 80, 351)]
BUTTONS = [("P48 1", 32, 407), ("P48 2", 80, 407)]
GAIN = [("Gain 1", 32, 379), ("Gain 2", 80, 379)]          # on M5, not on this board


def window():
    """Board-coordinate rectangle of the M5 window (x0, y0, x1, y1)."""
    gy = panel_to_board(*GAIN[0][1:])[1]
    return M5_X[0] - WIN_GAP, gy - 17.0 - WIN_GAP, M5_X[1] + WIN_GAP, gy + 17.0 + WIN_GAP


# ------------------------------------------------------------------ module bus (R123), same pinout as M1
CONN = {1: "+5V", 2: "+5V", 3: "GND", 4: "GND", 5: "+3V3", 6: "GND", 7: "SDA", 8: "SCL",
        9: "~{INT}", 10: "GND", 11: "~{SR_LOAD}", 12: "SR_CLK", 13: "SR_OUT", 14: "SR_IN"}
# J2 to M5: same, except that M5 drives SR_M5 (its SR_OUT) into our register's serial input
CONN_M5 = {**CONN, 13: "SR_M5"}

R0402, C0402, C0805 = "Resistor_SMD:R_0402_1005Metric", "Capacitor_SMD:C_0402_1005Metric", "Capacitor_SMD:C_0805_2012Metric"
LCSC = {"100n": "C1525", "1u": "C52923", "10u": "C15850", "10k": "C25744", "4.7k": "C25900", "1k": "C11702"}


def parts():
    """List of parts: ref, lib_id, value, footprint, {pin: net}, extra fields."""
    P = []

    def add(ref, lib, value, fp, pins, **f):
        P.append(dict(ref=ref, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def rc(ref, value, a, b, fp=None):
        lib = "Device:R" if ref.startswith("R") else "Device:C"
        add(ref, lib, value, fp or (R0402 if lib == "Device:R" else C0402), {"1": a, "2": b}, LCSC=LCSC[value])

    hdr = "Connector_PinHeader_1.27mm:PinHeader_2x07_P1.27mm_Vertical"
    add("J1", "Connector_Generic:Conn_02x07_Odd_Even", "Bus to P1 2x7 1.27", hdr,
        {str(p): n for p, n in CONN.items()}, LCSC="C3975190", Side="bottom")
    add("J2", "Connector_Generic:Conn_02x07_Odd_Even", "Bus to M5 2x7 1.27", hdr,
        {str(p): n for p, n in CONN_M5.items()}, LCSC="C3975190", Side="bottom")
    rc("C1", "10u", "+5V", "GND", C0805)
    rc("C2", "1u", "+3V3", "GND")

    # pots -> ADS1115 (16 bit, I2C 0x48): wiper through 1k / 100n, ends on GND and +3V3
    for n, (nm, _, _) in enumerate(POTS):
        add(f"RV{n + 1}", "Device:R_Potentiometer", "10k lin, end stops",
            "Potentiometer_THT:Potentiometer_Alps_RK09K_Single_Vertical",
            {"1": "GND", "2": f"POT{n + 1}", "3": "+3V3"}, LCSC="C209770", Note=nm,
            Part="Alps RK09K1130A6S or another RK09K 10k with linear (B) taper")
        rc(f"R{1 + n}", "1k", f"POT{n + 1}", f"AIN{n}")
        rc(f"C{3 + n}", "100n", f"AIN{n}", "GND")
    add("U1", "Analog_ADC:ADS1115IDGS", "ADS1115IDGSR", "Package_SO:TSSOP-10_3x3mm_P0.5mm",
        {"1": "GND", "2": None, "3": "GND", "4": "AIN0", "5": "AIN1", "6": "AIN2", "7": "AIN3",
         "8": "+3V3", "9": "SDA", "10": "SCL"}, LCSC="C37593", Note="I2C 0x48 (ADDR=GND)")
    rc("C7", "100n", "+3V3", "GND")

    # P48 buttons: tact switch to GND, 10k pull-up, read by one 74HC165 in the module chain
    for n in range(2):
        add(f"SW{n + 1}", "Switch:SW_Push", "TS-1187A-B-A-B", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A",
            {"1": f"BTN{n + 1}", "2": "GND"}, LCSC="C318884", Note=BUTTONS[n][0])
    add("RN1", "Device:R_Pack04", "4x10k", "Resistor_SMD:R_Array_Convex_4x0402",
        {"1": "BTN1", "2": "BTN2", "3": "SR_M5", "4": None, "8": "+3V3", "7": "+3V3", "6": "+3V3", "5": None},
        LCSC="C25725", Note="SR_M5 pull-up: the chain still reads 1s without M5")
    sr = {"1": "~{SR_LOAD}", "2": "SR_CLK", "15": "GND", "8": "GND", "16": "+3V3", "10": "SR_M5", "9": "SR_OUT",
          "7": None}
    # D7..D0 = pins 6 5 4 3 14 13 12 11: host reads P48 1, P48 2, then six 1s, then M5
    for p, net in zip(["6", "5", "4", "3", "14", "13", "12", "11"], ["BTN1", "BTN2"] + ["+3V3"] * 6):
        sr[p] = net
    add("U2", "74xx:74HC165", "74HC165PW", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm", sr, LCSC="C80696")
    rc("C8", "100n", "+3V3", "GND")

    # button lights: 2 RGB per button (left and right of the switch), IS31FL3218 (18 PWM sinks, I2C 0x54)
    u3 = {"1": None, "2": "REXT", "3": "+5V", "4": "GND", "25": "GND", "5": "SDA", "6": "SCL", "24": "SDB"}
    out = [str(p) for p in range(7, 24)] + ["1"]                 # OUT1..OUT17 = pins 7..23, OUT18 = pin 1
    for i, p in enumerate(out):
        u3[p] = f"OUT{i + 1}" if i < 12 else None
    add("U3", "Driver_LED:IS31FL3218-QF", "IS31FL3218-QFLS2-TR",
        "Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.7x2.7mm", u3, LCSC="C2940546",
        Note="I2C 0x54 (fixed); write only")
    rc("R5", "4.7k", "REXT", "GND")          # I_max = 76.05 / 4.7k = 16 mA per channel (datasheet)
    rc("R6", "10k", "SDB", "+5V")
    rc("C9", "1u", "+5V", "GND")
    rc("C10", "100n", "+5V", "GND")
    for n in range(4):                       # D1 = P48 1 left, D2 = P48 1 right, D3, D4 = P48 2
        o = 3 * n
        add(f"D{n + 1}", "ShtukaDruka:XL-1615RGBC-RF", "XL-1615RGBC-RF", "ShtukaDruka:LED_RGB_XL-1615RGBC_1.6x1.5mm",
            {"2": "+5V", "1": f"OUT{o + 1}", "3": f"OUT{o + 2}", "4": f"OUT{o + 3}"}, LCSC="C965840")
    for h in range(6):
        add(f"H{h + 1}", "Mechanical:MountingHole", "M2", "MountingHole:MountingHole_2.2mm_M2", {})
    return P


U3_ROT = 0          # LED driver rotation (W1_U3_ROT overrides it for routing experiments)


def placement():
    """ref -> (x, y, rotation, side); board coordinates. Top: pots, switches, LEDs. Bottom: the rest."""
    pl = {}
    t, b = "top", "bottom"
    for n, (_, px, py) in enumerate(POTS):
        x, y = panel_to_board(px, py)
        pl[f"RV{n + 1}"] = (x, y, 0, t)                  # make_pcb puts the shaft at (x, y)
    for n, (_, px, py) in enumerate(BUTTONS):
        x, y = panel_to_board(px, py)
        pl[f"SW{n + 1}"] = (x, y, 0, t)
        pl[f"D{2 * n + 1}"] = (x - 6.5, y, 0, t)
        pl[f"D{2 * n + 2}"] = (x + 6.5, y, 0, t)
    # bottom, rear part (behind the window): LED driver between the buttons
    pl["U3"] = (46.0, 16.0, float(os.environ.get("W1_U3_ROT", U3_ROT)), b)
    for n, r in enumerate(("R5", "R6", "C9", "C10")):        # in a row in front of it, pins stay free to fan out
        pl[r] = (43.0 + 2.0 * n, 22.5, 90, b)
    # bottom, front part: ADC between the pots, shift register and connectors
    pl["U1"] = (46.0, 100.0, 0, b)
    for n in range(4):
        pl[f"R{1 + n}"] = (40.0 + 4.0 * n, 94.5, 90, b)
        pl[f"C{3 + n}"] = (40.0 + 4.0 * n, 105.5, 90, b)
    pl["C7"] = (52.0, 100.0, 90, b)
    pl["U2"] = (46.0, 82.0, 90, b)
    pl["RN1"], pl["C8"] = (39.0, 82.0, 90, b), (53.0, 82.0, 90, b)
    w = window()
    pl["J2"] = (46.0, w[3] + 3.0, 90, b)                # just in front of the window: short ribbon to M5
    pl["J1"] = (46.0, H - 3.0, 90, b)                   # front edge, towards the fold and P1
    pl["C1"], pl["C2"] = (37.0, H - 3.0, 90, b), (55.0, H - 3.0, 90, b)
    for n, (hx, hy) in enumerate(((2.6, 2.6), (W - 2.6, 2.6), (2.6, H - 2.6), (W - 2.6, H - 2.6),
                                  (46.0, 5.0), (46.0, 113.0))):
        pl[f"H{n + 1}"] = (hx, hy, 0, t)
    return pl


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    pl = placement()
    missing = [p["ref"] for p in P if p["ref"] not in pl]
    print(len(P), "parts,", len(nets), "nets; board", W, "x", H, "mm; window", window(), "; unplaced:", missing)
    for nm, px, py in POTS + BUTTONS + GAIN:
        print(f"  {nm:9s} board {panel_to_board(px, py)}")
