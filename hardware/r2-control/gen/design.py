"""R2 - Control board at the rear wall (right part): RP2350 of the control board (R85), MIDI DIN 2 in / 4 out and
TRS 1 in / 2 out (R32, R34), 8 CV/Gate outputs +-10 V (R35), 4 CV inputs, sync block 5 jacks (R33), internal USB hub
(R82, doc 29), rear USB-C (to the PC, passed to A1's port B), rear USB-A (passed to the Mini-ITX), power jacks
(DC and USB-C PD, passed to PW), the control lines to the audio boards (phantom 48 V x 2, phono/line, mute relays; R118, R137).
Single source of truth for the schematic. Research and decisions: docs/ru/34_rear_boards_research.md, R135-R138.

Rev 0.1 = schematic. The board outline and the jack positions follow the rear panel layout (doc 13, 3.5), which is
not drawn yet; the 5-pin DIN footprint (CUI SDS-50J) and the locking DC jack are chosen with it.
Rev 0.2 (14.11.2026, cloud, task #20): checked against the datasheets - RP2350 minimal design (inductor, crystal, BOOTSEL,
shared 100 nF of pins 53/54), DAC80504 REFDIV high (2.5 V ref needs VDD >= 5.0 V undivided: the +5 V rail is not enough),
CV difference amps x8.06 around REF/2, USB2514B straps left to the internal pull-downs, CRFILT/PLLFILT 100 nF, VBUS_DET 100k/100k.
Rev 0.3 (14.11.2026, PC, R139): the right-angle jacks (MIDI DIN x 6, USB-C PC, USB-A, USB-C PD, DC) moved to the shelf
board R2b (hardware/r2b-jacks) with their ESD and cables; R2 keeps the MIDI parts and gets a 2x7 comb to R2b.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "r2-control"
ID = "R2"
TITLE = "R2 - Control board (rear wall): RP2350, USB hub, MIDI, CV/Gate, sync; DIN, USB and power jacks on R2b"
REV = "0.3"
M1_LIB = K.M1_LIB
BUS_NOTE = ("RP2350 (R85): MIDI DIN 2 in / 4 out, TRS 1 in / 2 out (A/B in firmware), 8 CV/Gate +-10 V (2 x DAC80504), "
            "4 CV in, sync 3 out / 2 in; USB2514B hub: up = Mini-ITX, down = RP2350, panel P2, A1 port A, spare")
PWR_FLAG_NETS = ("+12V", "-12V", "DVDD", "VREG_AVDD", "ADC_AVDD")   # ERC: rails from a connector, inductor or RC filter
NO_PWR_FLAG = ("+3V3",)                                               # +3V3 is driven by the AP2112K (power output pin)
W, H = 258.0, 100.0         # rough: rear wall right part x 252-510, height up to ~104 mm (doc 29); refined with the panel layout
LAYERS = 4

R0402, C0402, C0805 = K.R0402, K.C0402, K.C0805
SOT23, SOD123 = "Package_TO_SOT_SMD:SOT-23", "Diode_SMD:D_SOD-123"
JACK35 = "Connector_Audio:Jack_3.5mm_QingPu_WQP-PJ398SM_Vertical_CircularHoles"
# 2x7 comb to R2b (R139), same numbering as hardware/r2b-jacks/gen/design.py COMB
R2B_COMB = {"1": "MO1_4", "2": "MO1_5", "3": "MO2_4", "4": "MO2_5", "5": "MO3_4", "6": "MO3_5", "7": "MO4_4", "8": "MO4_5",
            "9": "MI1_4", "10": "MI1_5", "11": "MI2_4", "12": "MI2_5", "13": "GND", "14": "GND"}
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"

# GPIO map of the RP2350A (30 GPIO, all used)
GPIO = {0: "MIDI_TX1", 1: "MIDI_TX2", 2: "MIDI_TX3", 3: "MIDI_TX4", 4: "MIDI_RX1", 5: "MIDI_RX2",
        6: "TRS1_T", 7: "TRS1_R", 8: "TRS2_T", 9: "TRS2_R", 10: "TRSIN_A", 11: "TRSIN_B",
        12: "MUTE", 13: "R2_OK", 14: "DAC_SCK", 15: "DAC_SDI", 16: "DAC_CS1", 17: "DAC_CS2",
        18: "CLK_OUT1", 19: "CLK_OUT2", 20: "RST_OUT", 21: "CLK_IN", 22: "RST_IN",
        23: "PH48_1", 24: "PH48_2", 25: "PHONO", 26: "CVIN1", 27: "CVIN2", 28: "CVIN3", 29: "CVIN4"}
GPIO_PIN = {0: "2", 1: "3", 2: "4", 3: "5", 4: "7", 5: "8", 6: "9", 7: "10", 8: "12", 9: "13", 10: "14", 11: "15",
            12: "16", 13: "17", 14: "18", 15: "19", 16: "27", 17: "28", 18: "29", 19: "31", 20: "32", 21: "33",
            22: "34", 23: "35", 24: "36", 25: "37", 26: "40", 27: "41", 28: "42", 29: "43"}


def parts():
    P = []
    n = {"R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Q": 0, "L": 0, "Y": 0, "SW": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def R(value, a, b, **f):
        K.rc(add, ref("R"), value, a, b, **f)

    def C(value, a, b="GND", fp=None, **f):
        K.rc(add, ref("C"), value, a, b, fp, **f)

    def jack(note, tip, ring=None):
        add(ref("J"), "Connector_Audio:AudioJack3", "PJ398SM", JACK35, {"T": tip, "R": ring, "S": "GND"},
            LCSC="C9900009788", Note=note)

    # ---------------------------------------------------------------- power in, 3.3 V
    add(ref("J"), "Connector_Generic:Conn_01x05", "Power from PW", PH.format(n=5),
        {"1": "+12V", "2": "GND", "3": "-12V", "4": "GND", "5": "+5V"}, Note="from PW: +-12 V for CV, +5 V for 3.3 V and DACs")
    u = ref("U")
    add(u, "Regulator_Linear:AP2112K-3.3", "AP2112K-3.3", "Package_TO_SOT_SMD:SOT-23-5",
        {"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": "+3V3"}, LCSC="C51118")
    C("1u", "+5V")
    C("1u", "+3V3")
    for _ in range(2):
        C("100n", "+12V")
        C("100n", "-12V")

    # ---------------------------------------------------------------- RP2350A
    u = ref("U")
    mcu = {"1": "+3V3", "11": "+3V3", "20": "+3V3", "30": "+3V3", "38": "+3V3", "45": "+3V3",
           "6": "DVDD", "23": "DVDD", "39": "DVDD", "44": "ADC_AVDD", "46": "VREG_AVDD", "47": "GND", "48": "VREG_LX",
           "49": "+3V3", "50": "DVDD", "51": "MCU_DM_R", "52": "MCU_DP_R", "53": "+3V3", "54": "+3V3",
           "55": "QSPI_SD3", "56": "QSPI_SCLK", "57": "QSPI_SD0", "58": "QSPI_SD2", "59": "QSPI_SD1", "60": "QSPI_SS",
           "21": "XIN", "22": "XOUT", "24": "SWCLK", "25": "SWDIO", "26": "RUN", "61": "GND"}
    mcu.update({GPIO_PIN[g]: net for g, net in GPIO.items()})
    add(u, "MCU_RaspberryPi:RP2350A", "RP2350A", "Package_DFN_QFN:QFN-60-1EP_7x7mm_P0.4mm_EP3.4x3.4mm", mcu,
        LCSC="C42411118", Note="R85; RP2350A, LCSC C42411118 (Extended, 5380 in stock 14.11.2026)")
    add(ref("L"), "Device:L", "3.3uH", "Inductor_SMD:L_Abracon_AOTA-B201610S", {"1": "VREG_LX", "2": "DVDD"},
        LCSC="C42411119", Note="AOTA-B201610S3R3-101-T 2.1 A as in Raspberry Pi's minimal design; polarised: dot as on the "
        "reference layout (Hardware design with RP2350); only 10 in stock at LCSC on 14.11.2026")
    R("33", "+3V3", "VREG_AVDD", Note="VREG_AVDD filter 33 R + 4.7 uF (minimal design)")
    C("4.7u", "VREG_AVDD", fp=C0805)
    R("33", "+3V3", "ADC_AVDD", Note="ADC supply filter (own choice; the minimal design has 100 nF only)")
    C("1u", "ADC_AVDD")
    C("4.7u", "DVDD", fp=C0805)
    C("4.7u", "+3V3", fp=C0805, Note="VREG_VIN")
    for _ in range(7):                    # 6 x IOVDD + one shared by USB_OTP_VDD and QSPI_IOVDD (pins 53, 54)
        C("100n", "+3V3")
    for _ in range(3):
        C("100n", "DVDD")
    R("10k", "RUN", "+3V3")
    C("100n", "RUN")
    add(ref("Y"), "Device:Crystal_GND24", "12MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
        {"1": "XIN", "3": "XTAL_O", "2": "GND", "4": "GND"}, LCSC="C20625731",
        Note="ABM8-272-T3, 10 pF load: 2 x 15 pF + ~3 pF stray (minimal design)")
    R("1k", "XOUT", "XTAL_O")
    C("15p", "XIN")
    C("15p", "XTAL_O")
    add(ref("U"), "Memory_Flash:W25Q16JVSS", "W25Q128JVSIQ", "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
        {"1": "QSPI_SS", "2": "QSPI_SD1", "3": "QSPI_SD2", "4": "GND", "5": "QSPI_SD0", "6": "QSPI_SCLK", "7": "QSPI_SD3",
         "8": "+3V3"}, LCSC="C97521", Note="16 MB QSPI flash (same pinout as the W25Q16JVSS symbol)")
    C("100n", "+3V3")
    R("10k", "QSPI_SS", "+3V3", Note="DNF on the reference design; harmless with W25Q128JV")
    R("1k", "QSPI_SS", "BOOTSEL", Note="BOOTSEL: button pulls QSPI_SS low (minimal design)")
    add(ref("SW"), "Switch:SW_Push", "BOOTSEL", "Button_Switch_SMD:SW_Push_1P1T_XKB_TS-1187A", {"1": "BOOTSEL", "2": "GND"},
        LCSC="C318884", Note="BOOTSEL (USB boot); picotool can also reboot into it over USB")
    R("27", "MCU_DM_R", "MCU_DM", Note="USB series")
    R("27", "MCU_DP_R", "MCU_DP", Note="USB series")
    add(ref("J"), "Connector_Generic:Conn_01x03", "SWD", PH.format(n=3), {"1": "SWCLK", "2": "SWDIO", "3": "GND"})
    R("1k", "R2_OK", "LED_K", Note="status LED; R2_OK is also the 'alive' line to the audio boards")
    add(ref("D"), "Device:LED", "green", "LED_SMD:LED_0603_1608Metric", {"2": "LED_K", "1": "GND"})

    # ---------------------------------------------------------------- USB hub USB2514B
    u = ref("U")
    add(u, "Interface_USB:USB2514B_Bi", "USB2514B", "Package_DFN_QFN:QFN-36-1EP_6x6mm_P0.5mm_EP3.7x3.7mm",
        {"1": "MCU_DM", "2": "MCU_DP", "3": "P2_DM", "4": "P2_DP", "6": "A1_DM", "7": "A1_DP", "8": "SP_DM", "9": "SP_DP",
         "5": "+3V3", "10": "+3V3", "29": "+3V3", "36": "+3V3", "15": "+3V3", "23": "+3V3", "37": "GND", "11": "GND",
         "12": None, "16": None, "18": None, "20": None, "13": "HUB_OCS", "17": "HUB_OCS", "19": "HUB_OCS", "21": "HUB_OCS",
         "14": "HUB_CRFILT", "34": "HUB_PLLFILT", "35": "HUB_RBIAS", "32": "HUB_XO", "33": "HUB_XI",
         "26": "HUB_RESET", "27": "HUB_VBUSDET", "30": "UP_DM", "31": "UP_DP",
         "22": None, "24": None, "25": None, "28": None},
        LCSC="C220679", Note="straps CFG_SEL[1:0], NON_REM[1:0] low through the internal pull-downs = default "
        "configuration (datasheet: strap low needs no part; HS_IND, SUSP_IND are LED outputs and must not be tied together)")
    R("10k", "HUB_OCS", "+3V3", Note="no over-current inputs: ports always powered (OCS_N also has internal pull-ups)")
    C("100n", "HUB_CRFILT", Note="datasheet: up to 0.1 uF low ESR")
    C("100n", "HUB_PLLFILT", Note="datasheet: up to 0.1 uF low ESR")
    R("12k", "HUB_RBIAS", "GND", Note="1 %")
    add(ref("Y"), "Device:Crystal_GND24", "24MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
        {"1": "HUB_XI", "3": "HUB_XO", "2": "GND", "4": "GND"}, LCSC="C70590",
        Note="X322524MOB4SI, 12 pF load (datasheet: load caps typically 18 pF)")
    C("18p", "HUB_XI")
    C("18p", "HUB_XO")
    R("10k", "HUB_RESET", "+3V3")
    C("1u", "HUB_RESET")
    R("100k", "UP_VBUS", "HUB_VBUSDET", Note="VBUS_DET from the Mini-ITX port: 2:1 divider, 2 x 100k (datasheet)")
    R("100k", "HUB_VBUSDET", "GND")
    for _ in range(6):                    # VDDA33 x 4, VDD33 x 2
        C("100n", "+3V3")
    C("4.7u", "+3V3", fp=C0805)
    for note, pins in (("USB up: from the Mini-ITX USB header", {"1": "UP_VBUS", "2": "UP_DM", "3": "UP_DP", "4": "GND"}),
                       ("USB down: panel P2 (R86)", {"1": "+5V", "2": "P2_DM", "3": "P2_DP", "4": "GND"}),
                       ("USB down: A1 port A (R82)", {"1": "+5V", "2": "A1_DM", "3": "A1_DP", "4": "GND"}),
                       ("USB down: spare", {"1": "+5V", "2": "SP_DM", "3": "SP_DP", "4": "GND"})):
        add(ref("J"), "Connector_Generic:Conn_01x04", note.split(":")[0], PH.format(n=4), pins, Note=note)

    # ---------------------------------------------------------------- comb to R2b (R139): the DIN jacks sit on the shelf
    add(ref("J"), "Connector_Generic:Conn_02x07_Odd_Even", "to R2b", "Connector_PinSocket_2.54mm:PinSocket_2x07_P2.54mm_Horizontal",
        R2B_COMB, Note="R139: right-angle socket down to the R2b header; MIDI DIN lines only (USB and power jacks go from R2b "
        "straight to A1, the Mini-ITX and PW)")

    # ---------------------------------------------------------------- control lines to the audio boards (R118, R137)
    add(ref("J"), "Connector_Generic:Conn_02x05_Odd_Even", "to A1/R1", "Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical",
        {"1": "PH48_1", "2": "GND", "3": "PH48_2", "4": "GND", "5": "PHONO", "6": "GND", "7": "MUTE", "8": "GND",
         "9": "R2_OK", "10": "GND"},
        Note="phantom 48 V per channel, phono/line, output mute relays (all outputs), alive; relays open when R2 stops (R66, R137)")
    for net in ("PH48_1", "PH48_2", "PHONO", "MUTE"):
        R("100k", net, "GND", Note="off while the RP2350 boots")

    # ---------------------------------------------------------------- MIDI (CA-033, 3.3 V)
    for k in range(4):                                     # DIN out 1-4 (jacks on R2b): pin 4 <- 33 R <- 3.3 V, pin 5 <- 10 R <- TX
        K.rc(add, ref("R"), "33", "+3V3", f"MO{k + 1}_4", "Resistor_SMD:R_1206_3216Metric", Note="CA-033 3.3 V: 33 R 0.5 W")
        R("10", f"MIDI_TX{k + 1}", f"MO{k + 1}_5", Note="CA-033 3.3 V: 10 R")
    for k in range(2):                                     # DIN in 1-2 (jacks on R2b): opto TLP2361 (3.3 V)
        R("220", f"MI{k + 1}_4", f"MI{k + 1}_A")
        add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": f"MI{k + 1}_A", "2": f"MI{k + 1}_5"}, Note="reverse protection")
        add(ref("U"), "Isolator:TLP2361", "TLP2361", "Package_SO:SO-5-6_4.55x3.7mm_P1.27mm",
            {"1": f"MI{k + 1}_A", "3": f"MI{k + 1}_5", "4": "GND", "5": f"MIDI_RX{k + 1}", "6": "+3V3"}, LCSC="C107626")
        C("100n", "+3V3")
    for k in range(2):                                     # TRS out 1-2: type A/B swapped in firmware (two GPIO)
        jack(f"MIDI TRS OUT {k + 1} (type A/B in firmware, R32)", f"TO{k + 1}_T", f"TO{k + 1}_R")
        R("22", f"TRS{k + 1}_T", f"TO{k + 1}_T")
        R("22", f"TRS{k + 1}_R", f"TO{k + 1}_R")
    jack("MIDI TRS IN (type A and B: two optos back to back)", "TI_T", "TI_R")
    for side, a, kk in (("A", "TI_T", "TI_R"), ("B", "TI_R", "TI_T")):
        R("220", a, f"TI{side}_A")
        add(ref("U"), "Isolator:TLP2361", "TLP2361", "Package_SO:SO-5-6_4.55x3.7mm_P1.27mm",
            {"1": f"TI{side}_A", "3": kk, "4": "GND", "5": f"TRSIN_{side}", "6": "+3V3"}, LCSC="C107626")
        C("100n", "+3V3")

    # ---------------------------------------------------------------- CV/Gate out 1-8: DAC80504 x 2 + OPA4197 difference amps
    for d in range(2):
        u = ref("U")
        add(u, "Analog_DAC:DAC80504", "DAC80504", "Package_DFN_QFN:Texas_RTE0016D_WQFN-16-1EP_3x3mm_P0.5mm_EP0.8x0.8mm_ThermalVias",
            {"1": f"DAC_REF{d + 1}", "2": f"DAC{4 * d + 1}", "3": f"DAC{4 * d + 2}", "4": f"DAC{4 * d + 3}", "5": f"DAC{4 * d + 4}",
             "6": "GND", "7": "+5V", "8": "+3V3", "9": "+3V3", "10": "+3V3", "11": "GND", "12": f"DAC_CS{d + 1}",
             "13": "DAC_SCK", "14": "DAC_SDI", "15": None, "16": "+3V3", "17": "GND"},
            LCSC="C2862796", Note="DAC80504RTET; internal 2.5 V ref divided by 2 (REFDIV high) and gain 2 = 0-2.5 V "
            "(undivided needs VDD >= 5.0 V); RSTSEL high = mid-scale = 0 V out; LDAC low = update on CS")
        C("100n", "+5V")
        C("100n", "+3V3")
        C("100n", f"DAC_REF{d + 1}")
    opa = []
    for _ in range(3):
        u = ref("U")
        opa.append(u)
        C("100n", "+12V")
        C("100n", "-12V")
    sections = [(opa[i // 4], i % 4) for i in range(12)]     # (U, section 0-3)
    SEC = [("3", "2", "1"), ("5", "6", "7"), ("10", "9", "8"), ("12", "13", "14")]   # (+, -, out) per section
    pins = {u: {"4": "+12V", "11": "-12V"} for u in opa}

    def sec(i, plus, minus, out):
        u, s = sections[i]
        p, m, o = SEC[s]
        pins[u].update({p: plus, m: minus, o: out})

    R("10k", "DAC_REF1", "REFHALF", Note="0.1 %: REF / 2 = 1.25 V = DAC mid-scale")
    R("10k", "REFHALF", "GND", Note="0.1 %")
    C("100n", "REFHALF")
    sec(0, "REFHALF", "REFBUF", "REFBUF")                       # 1.25 V buffer for the 8 difference amps
    for c in range(8):                                          # Vout = 8.06 (Vdac - 1.25 V): -10.1 ... +10.1 V
        sec(1 + c, f"CVP{c + 1}", f"CVN{c + 1}", f"CVO{c + 1}")
        R("10k", f"DAC{c + 1}", f"CVP{c + 1}", Note="0.1 %")
        R("80.6k", f"CVP{c + 1}", "GND", Note="0.1 %")
        R("10k", "REFBUF", f"CVN{c + 1}", Note="0.1 %")
        R("80.6k", f"CVN{c + 1}", f"CVO{c + 1}", Note="0.1 %")
        R("1k", f"CVO{c + 1}", f"CV{c + 1}_J", Note="output protection")
        jack(f"CV/GATE OUT {c + 1}", f"CV{c + 1}_J")
    for i, (g, name) in enumerate((("CLK_OUT1", "CLOCK OUT 1"), ("CLK_OUT2", "CLOCK OUT 2"), ("RST_OUT", "RESET/RUN OUT"))):
        o = f"SO{i + 1}"                                        # 3.3 V GPIO -> 0 / +5 V: gain 1.51
        sec(9 + i, g, f"{o}_N", f"{o}_O")
        R("5.1k", f"{o}_O", f"{o}_N")
        R("10k", f"{o}_N", "GND")
        R("1k", f"{o}_O", f"{o}_J")
        jack(name, f"{o}_J")
    for u in opa:
        add(u, "Amplifier_Operational:OPA4197xD", "OPA4197", "Package_SO:TSSOP-14_4.4x5mm_P0.65mm", pins[u], LCSC="C2057327")

    # ---------------------------------------------------------------- CV in 1-4: -10...+10 V -> 0...3.03 V (ADC0-3)
    for c in range(4):
        jack(f"CV IN {c + 1}", f"CVI{c + 1}_J")
        R("100k", f"CVI{c + 1}_J", f"CVIN{c + 1}")
        R("33k", "+3V3", f"CVIN{c + 1}")
        R("39k", f"CVIN{c + 1}", "GND")
        C("10n", f"CVIN{c + 1}")
        add(ref("D"), "Diode:BAT54S", "BAT54S", SOT23, {"1": "GND", "2": "+3V3", "3": f"CVIN{c + 1}"}, Note="clamp to the ADC rails")

    # ---------------------------------------------------------------- sync in (Clock, Reset/Run): NPN, inverted
    for g, name in (("CLK_IN", "CLOCK IN"), ("RST_IN", "RESET/RUN IN")):
        j = f"{g}_J"
        jack(name, j)
        R("22k", j, f"{g}_B")
        R("100k", f"{g}_B", "GND")
        add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": f"{g}_B", "2": "GND"}, Note="negative input clamp")
        add(ref("Q"), "Transistor_BJT:MMBT3904", "MMBT3904", SOT23, {"1": f"{g}_B", "2": "GND", "3": g})
        R("10k", g, "+3V3")
    return P


def placement():
    """Rev 0.1 is the schematic only: the board waits for the rear panel layout."""
    return {}


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
