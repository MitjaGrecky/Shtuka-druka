"""P2 - Grid deck, the main board of the panel (x 110-334, y 4-262, 224 x 258 mm): the panel's RP2350 (R85), 64 pad sensors read through
8 x 74HC4051 and one ADC128S102 (V17, option a), 8 scene buttons and the two grid arrows, 109 RGB LEDs on 5 x LP5864, the strip of 25 lights,
connectors for two Bela Trill Bars, the module bus of M1 (R123), three deck buses (R130) and the cables to PW (power, INA226) and the R2 hub (USB).
Single source of truth for the schematic. Research: docs/ru/09_controls_research.md, docs/ru/29_board_map.md; decisions R85, R86, R106, R113,
R119, R123, R124, R129, R130, R146; proposal V17 (answer 14.11.2026: 74HC4051 + ADC128S102).

Pads: each pad is an FSR - two interdigitated copper electrodes on this board under a Velostat / force-sensing sheet. Per pad: electrode 1 to
the analog 3.3 V (+3V3A), electrode 2 to the node PAD<r>.<c> with a 10k pull-down; 8 pads of a row go into one 74HC4051 (address S0-S2 shared),
its COM into one input of the ADC128S102 (row = ADC channel). A full scan = 8 addresses x 8 channels = 64 conversions (about 130 us at 500 ksps).
Electrode footprints are drawn with the board (placeholder: a 2-pad test point).

I2C: main bus SDA/SCL (pull-ups here, 4.7k) -> deck muxes P1 0x70, P3 0x71, P4 0x72 and the local TCA9546A 0x73: channel 0 = LP5864 A-D (addresses
0-3), 1 = M1 module bus, 2 = LP5864 E + Trill Bar A, 3 = Trill Bar B + the INA226 of PW (R146; separate from the LED drivers: address 0x40 may meet
an LP5864 - check). Chain of registers (R123): ~SR_LOAD and SR_CLK shared, data back on SR_P1, SR_P3, SR_P4 (deck buses) and SR_P2 (local registers
-> M1 through the module bus).
Rev 0.1 (14.11.2026, PC) = schematic only. Rev 0.8 (19.11.2026): green LED NCD0603G1 C84267 (BOM only).
Rev 0.7 (19.11.2026): placement only (DRC): the cable header row moved 3 mm away from the strip LEDs.
Rev 0.6 (18.11.2026): PW harness widened to PH 8 (CHG_INT, FAN_PWM, FAN_TACH, CHG_EN on GP14, GP11, GP13, GP12). License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "p2-grid"
ID = "P2"
TITLE = "P2 - Grid deck: RP2350 panel controller, 64 FSR pads, 109 RGB, scene buttons, Trill Bars, deck and module buses"
REV = "0.10"
RA_ROT = 270        # right-angle 1.27 mm bus headers: rotation that opens them towards the rear edge (checked on the built board)
M1_LIB = K.M1_LIB
BUS_NOTE = ("RP2350 (panel): USB to the R2 hub; I2C + TCA9546A 0x73; 64 pads = 8 x 74HC4051 + ADC128S102 (SPI0); 5 x LP5864 for 109 RGB; "
            "buses to P1, P3, P4 (2x8) and M1 (2x7); power and INA226 from PW")
EXTRA_POWER_NETS = ("/+5V_PANEL",)     # netclass Power for the local-label rail
PWR_FLAG_NETS = ("+5V_PANEL", "DVDD", "VREG_AVDD", "ADC_AVDD", "+3V3A", "VAP")
NO_PWR_FLAG = ("+3V3", "+5V")     # no "+5V" net on P2: the only 5 V input is +5V_PANEL (J1)
W, H = 224.0, 258.0          # 16.11.2026: panel y 4-262 (was 290: it ran under M1, whose knob row is at y 263-297; fit model)
Y0 = 4.0                     # panel y of the board's front edge
HOLES = [(4.0, 4.0), (220.0, 4.0), (4.0, 254.0), (220.0, 254.0), (112.0, 254.0), (190.0, 4.0)]   # M3, board coordinates (KiCad, y down); 15.11.2026
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
SOT235, SOT236 = "Package_TO_SOT_SMD:SOT-23-5", "Package_TO_SOT_SMD:SOT-23-6"
TSSOP16 = "Package_SO:TSSOP-16_4.4x5mm_P0.65mm"
PH = "Connector_JST:JST_PH_S{n}B-PH-K_1x0{n}_P2.00mm_Horizontal"   # R168 (16.11.2026): side entry, 4.8 mm high (JST ePH), cable along the board - 7.9 mm to the floor under P2 in the low case
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"

# GPIO -> RP2350A QFN-60 pin (same package as on R2)
GPIO_PIN = {0: "2", 1: "3", 2: "4", 3: "5", 4: "7", 5: "8", 6: "9", 7: "10", 8: "12", 9: "13", 10: "14", 11: "15",
            12: "16", 13: "17", 14: "18", 15: "19", 16: "27", 17: "28", 18: "29", 19: "31", 20: "32", 21: "33",
            22: "34", 23: "35", 24: "36", 25: "37", 26: "40", 27: "41", 28: "42", 29: "43"}
GPIO = {0: "SDA", 1: "SCL", 2: "~{SR_LOAD}", 3: "SR_CLK", 4: "SR_P1", 5: "SR_P3", 6: "SR_P4", 7: "SR_P2", 8: "~{INT}", 9: "PM_ALERT",
        10: "STATUS_LED", 11: "FAN_PWM", 12: "CHG_EN", 13: "FAN_TACH", 14: "CHG_INT", 16: "ADC_DOUT", 17: "ADC_CS", 18: "ADC_SCK", 19: "ADC_DIN", 20: "MUX_S0", 21: "MUX_S1", 22: "MUX_S2"}


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Y": 0, "L": 0, "FB": 0, "SW": 0, "FSR": 0, "RN": 0}
    sdl = {}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    def R(value, a, b, fp=R0402, **f):
        K.rc(add, ref("R"), value, a, b, fp if fp != R0402 else None, **f)

    def C(value, a, b="GND", fp=None, **f):
        K.rc(add, ref("C"), value, a, b, fp, **f)

    # ================================================================ power in, 3.3 V
    # R168: single-row right-angle Micro-Fit 43650-0600 (mated height 6.98 mm by the Molex listing; the 2 x 3 header is about 10 mm high
    # and does not fit under P2 in the low case). Cable: 2 x 3 plug on PW -> 1 x 6 plug here, pin for pin by net.
    add(ref("J"), "Connector_Generic:Conn_01x06", "+5V from PW", "Connector_Molex:Molex_Micro-Fit_3.0_43650-0600_1x06_P3.00mm_Horizontal",
        {"1": "+5V_PANEL", "2": "+5V_PANEL", "3": "+5V_PANEL", "4": "GND", "5": "GND", "6": "GND"}, LCSC="C492352",
        Note="PW '+5V panel': the whole panel (all decks, modules and LEDs) is fed from here through the deck buses - worst case in the README")
    for _ in range(2):
        C("100u 16V", "+5V_PANEL", fp="Capacitor_SMD:CP_Elec_6.3x5.4", LCSC="C7469977",
          Note="R168: 5.4 mm high FVH016ADA101M0654 instead of the 7.7 mm can (low case)")
    C("10u", "+5V_PANEL", fp=C0805)
    add(ref("U"), "Regulator_Linear:AP2112K-3.3", "AP2112K-3.3", SOT235, {"1": "+5V_PANEL", "2": "GND", "3": "+5V_PANEL", "4": None, "5": "+3V3"},
        LCSC="C51118", Note="3.3 V for the RP2350, the muxes' logic and the buses (modules and decks use it for logic only)")
    C("1u", "+5V_PANEL", fp=C0603)
    C("1u", "+3V3", fp=C0603)
    C("10u", "+3V3", fp=C0805)
    # analog 3.3 V for the pad divider and the ADC: filtered
    add(ref("FB"), "Device:FerriteBead_Small", "600R", "Resistor_SMD:R_0603_1608Metric", {"1": "+3V3", "2": "+3V3A"}, LCSC="C14709",
        Note="analog 3.3 V for the 64 pad dividers, the muxes and the ADC (VA = reference)")
    C("10u", "+3V3A", fp=C0805)
    C("100n", "+3V3A")

    # ================================================================ RP2350A (panel controller, as on R2) + flash, crystal, USB
    u = ref("U")
    mcu = {"1": "+3V3", "11": "+3V3", "20": "+3V3", "30": "+3V3", "38": "+3V3", "45": "+3V3", "6": "DVDD", "23": "DVDD", "39": "DVDD",
           "44": "ADC_AVDD", "46": "VREG_AVDD", "47": "GND", "48": "VREG_LX", "49": "+3V3", "50": "DVDD", "51": "MCU_DM_R", "52": "MCU_DP_R",
           "53": "+3V3", "54": "+3V3", "55": "QSPI_SD3", "56": "QSPI_SCLK", "57": "QSPI_SD0", "58": "QSPI_SD2", "59": "QSPI_SD1", "60": "QSPI_SS",
           "21": "XIN", "22": "XOUT", "24": "SWCLK", "25": "SWDIO", "26": "RUN", "61": "GND"}
    for g, pin in GPIO_PIN.items():
        mcu[pin] = GPIO.get(g)
    add(u, "MCU_RaspberryPi:RP2350A", "RP2350A", "Package_DFN_QFN:QFN-60-1EP_7x7mm_P0.4mm_EP3.4x3.4mm", mcu, LCSC="C42411118",
        Note="panel controller (R85): pads, buttons, LEDs, deck buses; SDP over USB to the R2 hub (R86)")
    add(ref("L"), "Device:L", "3.3uH", "Inductor_SMD:L_Abracon_AOTA-B201610S", {"1": "VREG_LX", "2": "DVDD"}, LCSC="C42411119",
        Note="as on R2 (Raspberry Pi minimal design)")
    R("33", "+3V3", "VREG_AVDD")
    C("4.7u", "VREG_AVDD", fp=C0805)
    R("33", "+3V3", "ADC_AVDD")
    C("1u", "ADC_AVDD")
    C("4.7u", "DVDD", fp=C0805)
    C("4.7u", "+3V3", fp=C0805)
    for _ in range(7):
        C("100n", "+3V3")
    for _ in range(3):
        C("100n", "DVDD")
    R("10k", "RUN", "+3V3")
    C("100n", "RUN")
    add(ref("Y"), "Device:Crystal_GND24", "12MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
        {"1": "XIN", "3": "XTAL_O", "2": "GND", "4": "GND"}, LCSC="C20625731", Note="ABM8-272-T3 as on R2")
    R("1k", "XOUT", "XTAL_O")
    C("15p", "XIN")
    C("15p", "XTAL_O")
    add(ref("U"), "Memory_Flash:W25Q16JVSS", "W25Q128JVSIQ", "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
        {"1": "QSPI_SS", "2": "QSPI_SD1", "3": "QSPI_SD2", "4": "GND", "5": "QSPI_SD0", "6": "QSPI_SCLK", "7": "QSPI_SD3", "8": "+3V3"},
        LCSC="C97521", Note="16 MB QSPI flash")
    C("100n", "+3V3")
    R("10k", "QSPI_SS", "+3V3")
    R("1k", "QSPI_SS", "BOOTSEL")
    add(ref("SW"), "Switch:SW_Push", "BOOTSEL", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", {"1": "BOOTSEL", "2": "GND"}, LCSC="C318884")
    R("27", "MCU_DM_R", "MCU_DM")
    R("27", "MCU_DP_R", "MCU_DP")
    add(ref("J"), "Connector_Generic:Conn_01x03", "SWD", PH.format(n=3), {"1": "SWCLK", "2": "SWDIO", "3": "GND"})
    add(ref("J"), "Connector_Generic:Conn_01x04", "USB to R2 hub", PH.format(n=4), {"1": "+5V_PANEL_S", "2": "MCU_DM", "3": "MCU_DP", "4": "GND"},
        Note="cable to the R2 hub 'USB down: panel P2' (R86): USB MIDI + SDP; VBUS pin only senses (the panel has its own +5 V)")
    R("10k", "+5V_PANEL_S", "VBUS_SENSE", Note="not used by firmware; keeps the net from floating")
    R("20k", "VBUS_SENSE", "GND")
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", SOT236,
        {"1": "MCU_DP", "6": "MCU_DP", "3": "MCU_DM", "4": "MCU_DM", "2": "GND", "5": "+5V_PANEL_S"}, LCSC="C7519")
    R("1k", "STATUS_LED", "STATUS_K")
    add(ref("D"), "Device:LED", "green", "LED_SMD:LED_0603_1608Metric", {"2": "STATUS_K", "1": "GND"}, LCSC="C84267")

    # ================================================================ pads: 8 x 74HC4051 + ADC128S102
    add(ref("U"), "ShtukaDruka:ADC128S102", "ADC128S102", TSSOP16,
        {"1": "ADC_CS", "16": "ADC_SCK", "14": "ADC_DIN", "15": "ADC_DOUT", "2": "VAP", "13": "VAP", "3": "GND", "12": "GND",
         **{str(4 + k): f"ROW{k + 1}" for k in range(8)}}, LCSC="C206503",
        Note="12-bit, 8 channels, SPI mode 0/3: channel = pad row; VA = reference = 3.3 V analog")
    add(ref("FB"), "Device:FerriteBead_Small", "600R", "Resistor_SMD:R_0603_1608Metric", {"1": "+3V3A", "2": "VAP"}, LCSC="C14709",
        Note="reference / ADC supply filter")
    C("10u", "VAP", fp=C0805)
    C("1u", "VAP", Note="ADC128S102 datasheet: VA bypass 1 uF + 0.1 uF at the pins")
    C("100n", "VAP")
    for row in range(1, 9):
        m = ref("U")
        pins = {"16": "+3V3A", "8": "GND", "7": "GND", "6": "GND", "9": "MUX_S2", "10": "MUX_S1", "11": "MUX_S0", "3": f"ROW{row}_C"}
        for c, pin in enumerate(("13", "14", "15", "12", "1", "5", "2", "4")):
            pins[pin] = f"PAD{row}.{c + 1}"
        add(m, "74xx:74HC4051", "74HC4051", TSSOP16, pins, LCSC="C5645",
            Note=f"row {row}: pads {row}.1-{row}.8, address S0-S2 shared, COM -> ADC channel {row}; Nexperia 74HC4051PW,118 (TSSOP-16, LCSC C5645; C2943042 from rev 0.1 not confirmed)")
        C("100n", "+3V3A")
        R("1k", f"ROW{row}_C", f"ROW{row}", Note="series + 1n below: anti-alias")
        C("1n", f"ROW{row}")
        for col in range(1, 9):
            net = f"PAD{row}.{col}"
            add(ref("FSR"), "Connector_Generic:Conn_01x02", f"FSR {row}.{col}", "TestPoint:TestPoint_2Pads_Pitch2.54mm_Drill0.8mm",
                {"1": "+3V3A", "2": net}, Note=f"pad row {row} column {col}: interdigitated electrodes on the board (drawn with the board), electrode 1 to +3V3A")
            R("10k", net, "GND", Note="divider pull-down: node = 3.3 V x 10k / (10k + FSR)")

    # ================================================================ I2C: pull-ups, local TCA9546A 0x73, local channels
    R("4.7k", "SDA", "+3V3", Note="main bus pull-up (decks and modules have none: R123)")
    R("4.7k", "SCL", "+3V3")
    R("4.7k", "~{INT}", "+3V3", Note="shared interrupt line of the modules")
    chans = {0: ("L_SDA", "L_SCL"), 1: ("M1_SDA", "M1_SCL"), 2: ("T_SDA", "T_SCL"), 3: ("X_SDA", "X_SCL")}
    # kit.i2c_mux expects explicit R refs from res_first; keep our own counter in step
    res_first = n["R"] + 1
    nxt = K.i2c_mux(add, ref("U"), 3, chans, ref("C"), res_first)
    n["R"] = nxt - 1

    # ================================================================ LEDs: 109 RGB on 5 x LP5864
    leds = []
    for k in range(1, 9):
        leds += [f"Scene {k} left", f"Scene {k} right"]
    for nm in ("Arrow left", "Arrow right"):
        leds += [f"{nm} left", f"{nm} right"]
    for r in range(1, 9):
        for c in range(1, 9):
            leds.append(f"Pad {r}.{c}")
    leds += [f"Strip {k}" for k in range(1, 26)]
    cells = [("A", (0, 0), "L"), ("B", (0, 1), "L"), ("C", (1, 0), "L"), ("D", (1, 1), "L"), ("E", (0, 0), "T")]
    for cell, addr, seg in cells:
        u = ref("U")
        base = len(P)
        K.lp5864(add, u, cell, (ref("C"), ref("C"), ref("C"), ref("C")), addr=addr, cs_used=12 if cell == "E" else 18)
        for part in P[base:]:                                            # LP5864 on its mux channel
            if part["ref"] == u:
                part["pins"]["28"], part["pins"]["29"] = f"{seg}_SCL", f"{seg}_SDA"
    for j, nm in enumerate(leds):
        cell = cells[j // 24][0]
        i = j % 24
        c = 3 * (i // 4)
        K.rgb(add, ref("D"), f"{cell}_SW{i % 4}", (f"{cell}_CS{c}", f"{cell}_CS{c + 1}", f"{cell}_CS{c + 2}"), Note=nm)

    # ================================================================ buttons: 8 scenes + 2 arrows on local 74HC165s
    names = [f"Scene {k}" for k in range(1, 9)] + ["Arrow left", "Arrow right"]
    bits = []
    for k, nm in enumerate(names):
        add(ref("SW"), "Switch:SW_Push", "TS-1187A-B-A-B", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", {"1": f"BTN{k + 1}", "2": "GND"},
            LCSC="C318884", Note=nm)
        bits.append(f"BTN{k + 1}")
    srs = [("SR_P2", "SR_Q1", 0), ("SR_Q1", "SR_M1", 1)]
    for s, (q7, ds, idx) in enumerate(srs):
        K.sr165(add, ref("U"), bits[8 * idx:8 * idx + 8], ds, q7, ref("C"))
    K.pullups(add, 1, bits)
    R("10k", "SR_END", "+3V3", Note="end of the chain: M1's SR_IN reads 1s")

    # ================================================================ buses: M1 (2x7), P1, P3, P4 (2x8), Trill Bars, PW monitor
    m1 = {**K.CONN, 7: "M1_SDA", 8: "M1_SCL", 13: "SR_M1", 14: "SR_END", 5: "+3V3", 1: "+5V_PANEL", 2: "+5V_PANEL"}
    K.bus(add, ref("J"), "Module bus M1 (2x7)", conn=m1, lying=True)
    for deck, sr in (("P1", "SR_P1"), ("P3", "SR_P3"), ("P4", "SR_P4")):
        conn = {**K.DECK_CONN}
        conn[1] = conn[2] = "+5V_PANEL"
        conn[13], conn[14] = sr, None
        add(ref("J"), "Connector_Generic:Conn_02x08_Odd_Even", f"Deck bus to {deck}", K.DECK_FP_RA, {str(p): v for p, v in conn.items()},
            LCSC=K.DECK_LCSC_RA, Note=f"R130: bus to {deck}; SR_OUT of the deck back to the controller, SR_IN (14) not used, AUX (15) reserved")
    for tag, (sd, sc) in (("A", ("T_SDA", "T_SCL")), ("B", ("X_SDA", "X_SCL"))):
        add(ref("J"), "Connector_Generic:Conn_01x04", f"Trill Bar {tag}", PH.format(n=4), {"1": "GND", "2": "+3V3", "3": sd, "4": sc},
            Note=f"Bela Trill Bar {tag} (R113), I2C on mux channel {'2' if tag == 'A' else '3'}; Qwiic order GND, 3.3 V, SDA, SCL (SH 1.0 on the sensor: cable SH-PH); address 0x20, no pull-ups on the sensor")
    # rev 0.6 (18.11.2026, audit + docs/ru/45): the PW harness is PH 8, pin for pin as PW 'Power telemetry to P2'. GP11 FAN_PWM (25 kHz, PWM5B), GP12 CHG_EN,
    # GP13 FAN_TACH (counted on channel B = 6B), GP14 CHG_INT. Pull-ups of CHG_INT / tach and the pull-down of CHG_EN are on PW; all 3.3 V.
    add(ref("J"), "Connector_Generic:Conn_01x08", "Power telemetry (PW)", PH.format(n=8),
        {"1": "X_SDA", "2": "X_SCL", "3": "PM_ALERT", "4": "CHG_INT", "5": "FAN_PWM", "6": "FAN_TACH", "7": "GND", "8": "CHG_EN"},
        Note="cable from PW 'Power telemetry to P2' (INA226 R146, BQ25798 chargers via TCA9546A 0x70, fan, charge enable): SDA, SCL on mux channel 3, ALERT GP9, CHG_INT GP14, FAN_PWM GP11, FAN_TACH GP13, CHG_EN GP12")
    R("100k", "PM_ALERT", "+3V3", Note="ALERT is open drain")
    K.mount_holes(add, ref, HOLES, "M3 standoff (Codex review 15.11.2026): corners first; the final positions come with the enclosure")
    # rev 0.10: the shared kit blocks (LP5864 and its capacitors) name their rail "+5V", which has no source on this board
    for part in P:
        part["pins"] = {n: ("+5V_PANEL" if v == "+5V" else v) for n, v in part["pins"].items()}
    return P


def placement():
    """Rev 0.3: pads, scene buttons, arrows, strip and their LEDs on the panel v7 grid (doc 27: columns every 28 mm from x 14,
    rows every 25 mm from y 52, strip y 22, scenes y 252; the pad LED sits in the gap below its pad), cable headers in a row along the
    bottom edge, the rest by hardware/common/gen/autoplace.py. y is counted from the front edge."""
    import autoplace
    fixed = {}
    for p in parts():
        r, note, val = p["ref"], p["fields"].get("Note", ""), p["value"]
        if val.startswith("FSR "):
            row, col = (int(v) for v in val[4:].split("."))
            fixed[r] = (14.0 + 28 * (col - 1), 52.0 + 25 * (row - 1), 0, "top")
        elif r.startswith("D") and note.startswith("Pad "):
            row, col = (int(v) for v in note[4:].split("."))
            fixed[r] = (14.0 + 28 * (col - 1), 52.0 + 25 * (row - 1) + 12.5, 0, "top")
        elif r.startswith("D") and note.startswith("Strip "):
            k = int(note[6:])
            fixed[r] = (20.75 + 7.26 * (k - 0.5), 22.0, 0, "top")
        elif r.startswith("SW") and note.startswith("Scene "):
            fixed[r] = (14.0 + 28 * (int(note[6:]) - 1), 252.0, 0, "top")
        elif r.startswith("D") and note.startswith("Scene "):
            k = int(note.split()[1])
            fixed[r] = (14.0 + 28 * (k - 1) + (-9.0 if note.endswith("left") else 9.0), 252.0, 0, "top")
        elif r.startswith("SW") and note.startswith("Arrow "):
            fixed[r] = (12.0 if "left" in note else 211.5, 22.0, 0, "top")
        elif r.startswith("D") and note.startswith("Arrow "):
            x0 = 12.0 if note.startswith("Arrow left") else 211.5
            fixed[r] = (x0 + (-8.5 if note.endswith("left") else 8.5), 22.0, 0, "top")
    # Rev 0.4 (15.11.2026): the y above is counted from the front edge (panel v7), but KiCad's y grows downwards in the top view.
    # Rev 0.3 used it directly, so the strip and the arrows sat at the far edge and turning the board by 180 deg would also reverse
    # the columns (Codex review 15.11.2026). Now board y = H - panel y, as P1, P3 and P4 do: front edge (strip, arrows) at the bottom
    # of the KiCad view, scenes towards the screen at the top; column 1 stays on the musician's left.
    fixed = {r: (x, round(Y0 + H - y, 2), a, s) for r, (x, y, a, s) in fixed.items()}   # y above = panel y
    # cable headers in a row along the far (rear) edge, BOTTOM side (the cables go down to PW and R2; the top side there has the
    # scene buttons, 16.11.2026)
    import packer
    byref = {p["ref"]: p for p in parts()}
    x, y, rowh, margin = 12.0, 11.0, 0.0, 6.0      # rev 0.7 (DRC): row 3 mm further from the strip LEDs (D79, D80, D83 sat in the pads of J2, J4, J10)
    for r in [p["ref"] for p in parts() if p["ref"].startswith("J")]:
        # R168: lying connectors must open towards the rear edge (cables run on under M1 to PW and R2). The JST side-entry
        # footprints do at 0 deg; the right-angle Micro-Fit opens the other way, so it is turned by 180 deg.
        rot = {"Micro-Fit": 180, "P1.27mm_Horizontal": RA_ROT}.get(next((k for k in ("Micro-Fit", "P1.27mm_Horizontal") if k in byref[r]["fp"]), ""), 0)
        box, _ = packer._bbox(sys.modules[__name__], byref[r], rot, "bottom")
        w, h = box[2] - box[0], box[3] - box[1]
        if x + w > W - margin:
            x, y, rowh = margin, y + rowh + 2, 0.0
        fixed[r] = (round(x - box[0], 1), round(y - box[1], 1), rot, "bottom")
        x += w + 2
        rowh = max(rowh, h)
    fixed.update(K.hole_fixed(parts(), HOLES))
    return autoplace.fit(sys.modules[__name__], lambda g, ic: autoplace.place(sys.modules[__name__], fixed=fixed, gap=g, ic_gap=ic))


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
    single = {}
    for p in P:
        for pin, nn in p["pins"].items():
            if nn:
                single.setdefault(nn, []).append(f"{p['ref']}.{pin}")
    print("single-pin nets:", sorted(k for k, v in single.items() if len(v) == 1))
