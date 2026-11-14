"""A1 - Digital audio board (under the slope, left; mates R1 at a right angle): 20 differential ADC channels (CS5308P x 2 + CS5304P),
8 DAC channels (CS4308P) with current-to-voltage stages, two XMOS xcore.ai (XU316-1024-QF60B): A = bus master, internal USB audio port to
the Mini-ITX (port A, through the R2 hub) and the converters' SPI; B = USB device to the external computer through an ADuM4166 isolator
(port B). Two oscillators (24.576 and 22.5792 MHz, R114), quiet 3.3 V, 1.8 V, two 0.9 V cores.
Single source of truth for the schematic. Plan, pinouts and sources: hardware/a1-digital/PLAN.md; decisions R82-R84, R87, R88, R114, R116,
R117, R136; levels: R1 README ("ADC buffer FS 8 Vrms").

Input stage (CS5308P fig. 2-1 / AN0635): R1 delivers 8 Vrms differential at 0 dBFS; each leg goes through 68 uF and 1.2k into an inverting
stage of an OPA1656 (Rf 300 R || 680 pF, non-inverting input at the converter's ADC_VMID) = gain 1/4 -> 2 Vrms at the ADC pins; 10 R in series
with every pin, 15 nF across the pair. The stage inverts, so the source P leg drives the converter's N pin: the polarity is kept.
Output stage (AN0679 fig. 1): inverting I-V per leg, Rf 1.2k || 620 pF, non-inverting input at DAC_VMID, 2 Vrms differential full scale;
47 R build-out, 1 nF across the pair. Outputs 1-4 = Main L/R, Aux L/R (to R1), 5-8 = Phones 1 L/R, 2 L/R (to F1).

Rev 0.1 (14.11.2026, PC) = schematic only. Capacitor values around the converters follow the datasheet typical-connection drawings as far as
they were readable ("check" notes); XU316 PLL_AVDD at 0.9 V (check), ADuM4166 supply pins (check), oscillator part numbers (to choose).
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "a1-digital"
ID = "A1"
TITLE = "A1 - Digital audio: 3 ADC, 1 DAC, 2 xcore.ai, USB isolator, clocks, quiet supplies"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("R1 -> A1: 18 ADC pairs (8 Vrms FS), A1 -> R1: Main/Aux DAC pairs, A1 -> F1: Phones pairs; xcore A: TDM master, SPI to the "
            "converters, USB port A (hub on R2), xcore B: USB port B through the ADuM4166 (isolated ground GNDPC)")
PWR_FLAG_NETS = ("+12V", "-12V", "GNDPC", "PC_VBUS", "ISO_V1", "+0V9A", "+0V9B", "PLLA", "PLLB")   # ERC: R1 rails, computer side, buck outputs, filtered PLL supplies
NO_PWR_FLAG = ("+3V3",)          # no plain +3V3 rail here (+3V3A and +3V3D): no standard power symbol for it
W, H = 220.0, 100.0          # rough: under the slope on the left, about 220 x 100 mm (doc 29)
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603, R1206 = "Resistor_SMD:R_0603_1608Metric", "Resistor_SMD:R_1206_3216Metric"
C1210 = "Capacitor_SMD:C_1210_3225Metric"
SOIC8 = "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SOT235, SOT236 = "Package_TO_SOT_SMD:SOT-23-5", "Package_TO_SOT_SMD:SOT-23-6"
QFN48 = "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm"
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"
SOCKET = "Connector_PinSocket_2.54mm:PinSocket_2x{n:02d}_P2.54mm_Horizontal"
HEADER = "Connector_PinHeader_2.54mm:PinHeader_{rows}x{n:02d}_P2.54mm_Vertical"
OSC = "Oscillator:Oscillator_SMD_Abracon_ASE-4Pin_3.2x2.5mm"
VSSOP10 = None


def _fill(pins, count):
    for k in range(1, count + 1):
        pins.setdefault(str(k), None)
    return pins


def parts():
    P = []
    n = {"R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Y": 0, "L": 0, "FB": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def R(value, a, b, fp=R0402, **f):
        add(ref("R"), "Device:R", value, fp, {"1": a, "2": b}, **f)

    def C(value, a, b="GND", fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, **f)

    def FB(a, b, **f):
        add(ref("FB"), "Device:FerriteBead_Small", "600R", R0603, {"1": a, "2": b}, LCSC="C14709", **f)

    # ================================================================ connectors to R1, F1, R2 hub, PC jack
    adc = [f"ADC{k}" for k in range(1, 19)]
    a_pins = {}
    for k in range(10):
        a_pins[str(4 * k + 1)], a_pins[str(4 * k + 2)] = f"{adc[k]}_P", f"{adc[k]}_N"
        a_pins[str(4 * k + 3)], a_pins[str(4 * k + 4)] = "GND", "GND"
    add(ref("J"), "Connector_Generic:Conn_02x20_Odd_Even", "from R1 (ADC 1-10)", SOCKET.format(n=20), a_pins,
        Note="mates R1 'to A1 (ADC 1-10)' at a right angle; same pinout: pairs on adjacent pins, GND pair between pairs")
    pairs_b = adc[10:] + ["DAC_ML", "DAC_MR", "DAC_AL", "DAC_AR"]
    b_pins = {}
    for k, pr in enumerate(pairs_b):
        b_pins[str(4 * k + 1)], b_pins[str(4 * k + 2)] = f"{pr}_P", f"{pr}_N"
        if k < 11:
            b_pins[str(4 * k + 3)], b_pins[str(4 * k + 4)] = "GND", "GND"
    b_pins.update({"47": "+12V", "48": "-12V", "49": "+5V", "50": "+5V"})
    add(ref("J"), "Connector_Generic:Conn_02x25_Odd_Even", "R1 (ADC 11-18, DAC 1-4, power)", SOCKET.format(n=25), b_pins,
        Note="mates R1 'to A1 (ADC 11-18, DAC 1-4, power)'; +-12 V and +5 V come in here (PW -> R1 -> A1)")
    hp = ["HP1L_P", "HP1L_N", "GND", "HP1R_P", "HP1R_N", "GND", "HP2L_P", "HP2L_N", "GND", "HP2R_P", "HP2R_N", "GND"]
    add(ref("J"), "Connector_Generic:Conn_02x06_Odd_Even", "to F1", HEADER.format(rows=2, n=6), {str(i + 1): x for i, x in enumerate(hp)},
        Note="same pinout as F1 'from A1': Phones 1 and 2, L+ L- GND R+ R- GND, twisted pairs")
    add(ref("J"), "Connector_Generic:Conn_01x04", "USB port A (hub)", PH.format(n=4), {"1": "HUB_VBUS", "2": "HUB_DM", "3": "HUB_DP", "4": "GND"},
        Note="cable from the R2 hub 'USB down: A1 port A' (R82): VBUS sense only, +5 V comes from PW")
    add(ref("J"), "Connector_Generic:Conn_01x06", "USB-C PC", PH.format(n=6),
        {"1": "PC_VBUS", "2": "PC_DM", "3": "PC_DP", "4": "PC_CC1", "5": "PC_CC2", "6": "GNDPC"},
        Note="cable from the rear USB-C (PC) receptacle on the wall (R145): data only, isolated by the ADuM4166; Rd 5.1k on A1")
    add(ref("J"), "Connector_Generic:Conn_01x06", "spare ADC 19-20", PH.format(n=6),
        {"1": "ADC19_P", "2": "ADC19_N", "3": "GND", "4": "ADC20_P", "5": "ADC20_N", "6": "GND"},
        Note="R88: two spare channels, assignable (an internal source or an extra input board)")
    add(ref("J"), "Connector_Generic:Conn_01x04", "PDM mic", PH.format(n=4), {"1": "PDM_CLK", "2": "PDM_DATA", "3": "+3V3D", "4": "GND"},
        Note="built-in microphone (MEMS PDM) read by xcore B")

    # ================================================================ supplies
    def ldo33(net, note, lib="Regulator_Linear:AP2112K-3.3", lc="C51118"):
        add(ref("U"), lib, "AP2112K-3.3", SOT235, {"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": net}, LCSC=lc, Note=note)
        C("1u", "+5V", fp=C0603)
        C("2.2u", net, fp=C0603)

    ldo33("+3V3D", "digital 3.3 V: xcore I/O, flash, converter digital I/O, oscillators, USB (600 mA)")
    add(ref("U"), "Regulator_Linear:AP2112K-1.8", "AP2112K-1.8", SOT235, {"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": "+1V8"},
        LCSC="C176944", Note="1.8 V: xcore bottom I/O domain (JTAG, crystal) and USB_VDD18")
    C("1u", "+5V", fp=C0603)
    C("2.2u", "+1V8", fp=C0603)
    u = ref("U")
    add(u, "Regulator_Linear:TPS7A4701xRGW", "TPS7A4701", "Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias",
        {"1": "+3V3A", "3": "+3V3A", "4": None, "5": None, "6": None, "7": "GND", "8": "GND", "9": None, "10": None, "11": "GND",
         "12": "GND", "13": "+5V", "14": "REG_NR", "15": "+5V", "16": "+5V", "20": "+3V3A", "21": "GND"},
        LCSC="C90084", Note="quiet analog 3.3 V for the converters: ANY-OUT 1.4 + 1.6 + 0.2 + 0.1 = 3.3 V (pins 8, 11, 12 to GND), 4 uV rms")
    C("1u", "REG_NR", fp=C0603, Note="NR - check value")
    C("10u", "+5V", fp=C0805)
    C("22u", "+3V3A", fp=C0805)
    C("100n", "+3V3A")
    for k, core in (("A", "+0V9A"), ("B", "+0V9B")):
        u = ref("U")
        add(u, "Regulator_Switching:TLV62568DBV", "TLV62568", SOT235,
            {"1": "+5V", "2": "GND", "3": f"SW{k}", "4": "+5V", "5": f"FB{k}"}, LCSC="C163219",
            Note=f"core 0.9 V for xcore {k}: 0.6 V x (1 + 100k / 200k) = 0.9 V, 1 A")
        R("100k", core, f"FB{k}")
        R("200k", f"FB{k}", "GND")
        add(ref("L"), "Device:L", "2.2uH", "Inductor_SMD:L_Bourns-SRN4018", {"1": f"SW{k}", "2": core}, Note="2.2 uH, Isat >= 2 A - choose")
        C("10u", "+5V", fp=C0805)
        C("22u", core, fp=C0805)
        C("22u", core, fp=C0805)

    # ================================================================ clocks
    for nm, freq, en_pull in (("OSC48", "24.576MHz", "+3V3D"), ("OSC44", "22.5792MHz", "GND")):
        add(ref("Y"), "Oscillator:ASE-xxxMHz", freq, OSC, {"1": f"{nm}_EN", "2": "GND", "3": f"{nm}_OUT", "4": "+3V3D"},
            Note=f"{freq} 3.3 V oscillator, enable pin: part to choose with JLC stock (R114); low phase noise")
        R("10k", f"{nm}_EN", en_pull, Note="default state; xcore A can switch (one oscillator on at a time)")
        C("100n", "+3V3D")
        R("33", f"{nm}_OUT", "MCLK", Note="series, outputs tied: only one is enabled")

    def mclk_load(name):
        R("22", "MCLK", name, Note="star series resistor")

    # ================================================================ converters: shared digital nets
    # MCLK_<chip>, BCLK, FSYNC, SPI_SCK/MOSI/MISO, CS_<chip>, CONV_RESET
    def adc_chip(name, lib, value, lcsc, vmid_nets, n_in, cs, sdo):
        pins = {"5": "+3V3A", "9": "+3V3A", "31": "+3V3D", "33": f"{name}_LDOD", "6": "GND", "8": "GND", "30": "GND", "49": "GND",
                "7": f"{name}_LDOA", "32": f"{name}_LDOD", "34": f"MCLK_{name}", "23": f"RST_{name}", "36": "SPI_SCK", "35": "SPI_MISO",
                "37": "SPI_MOSI", "38": cs, "29": "BCLK", "24": "FSYNC", "25": sdo, "26": None, "27": None, "28": None,
                "2": f"{name}_CFG1", "3": f"{name}_CFG2", "4": f"{name}_CFG3", "10": f"{name}_CFG4", "11": f"{name}_CFG5"}
        if value == "CS5308P":
            pins.update({"43": f"{name}_F1P", "44": f"{name}_F1N", "18": f"{name}_F2P", "17": f"{name}_F2N", "1": vmid_nets[0], "12": vmid_nets[1]})
        else:
            pins.update({"43": f"{name}_F1P", "44": f"{name}_F1N", "1": vmid_nets[0]})
        return pins

    chips = [("ADCA", "CS5308P", "C42457798", 8, "CS_ADCA", "ADCA_SDO"),
             ("ADCB", "CS5308P", "C42457798", 8, "CS_ADCB", "ADCB_SDO"),
             ("ADCC", "CS5304P", "C49192888", 4, "CS_ADCC", "ADCC_SDO")]
    # channel -> (chip, input index): chip A = ADC 1-8 (mic, Hi-Z), B = ADC 9-16 (phono, line 1-6), C = ADC 17-20 (line 7-8, spare 1-2)
    in_pin = {1: ("40", "39"), 2: ("42", "41"), 3: ("46", "45"), 4: ("48", "47"), 5: ("14", "13"), 6: ("16", "15"), 7: ("20", "19"), 8: ("22", "21")}
    chan_net = {}
    for ci, (name, value, lcsc, nin, cs, sdo) in enumerate(chips):
        vm = (f"{name}_VMID1", f"{name}_VMID2") if value == "CS5308P" else (f"{name}_VMID", None)
        pins = adc_chip(name, "", value, lcsc, vm, nin, cs, sdo)
        for j in range(1, nin + 1):
            chn = 8 * ci + j
            pp, pn = in_pin[j]
            pins[pp], pins[pn] = f"ADC{chn}_BP", f"ADC{chn}_BN"
            chan_net[chn] = (name, j, vm[0] if j <= 4 or value == "CS5304P" else vm[1])
        if value == "CS5304P":
            for k in range(12, 23):
                pins[str(k)] = None
            for k in ("26", "27", "28"):
                pins[k] = None
        add(ref("U"), f"ShtukaDruka:{value}", value, QFN48, _fill(pins, 49), LCSC=lcsc,
            Note=f"{value} {nin} channels, software control by SPI (CONFIG1 to VDD_A), ASP secondary: BCLK and FSYNC from xcore A")
        mclk_load(f"MCLK_{name}")
        R("100k", f"RST_{name}", "GND", Note="held in reset until xcore A releases it")
        R("33", "CONV_RESET", f"RST_{name}")
        R("0", f"{name}_CFG1", "+3V3A", Note="CONFIG1 to VDD_A = software control mode (datasheet table 4-1)")
        for k in (2, 3, 4):
            R("10k", f"{name}_CFG{k}", "GND", Note="unused in SPI mode: to ground - check")
        R("10k", f"{name}_CFG5", "GND", Note="I2C address select, unused (SPI)")
        C("1u", "+3V3A", fp=C0603)
        C("10n", "+3V3A")
        C("1u", "+3V3A", fp=C0603)
        C("10n", "+3V3A")
        C("100n", "+3V3D")
        C("10u", f"{name}_LDOD", fp=C0805, Note="LDO_D_FILT / VDD_D - check value")
        C("4.7u", f"{name}_LDOA", fp=C0805, Note="LDO_A_FILT - check value")
        R("1", "+3V3A", f"{name}_F1P", Note="ADC_FILTP to VDD_A via 1 R (datasheet)")
        C("4.7u", f"{name}_F1P", f"{name}_F1N", fp=C0805, Note="FILT cap - check value")
        C("10n", f"{name}_F1P", f"{name}_F1N")
        if value == "CS5308P":
            R("1", "+3V3A", f"{name}_F2P")
            C("4.7u", f"{name}_F2P", f"{name}_F2N", fp=C0805)
            C("10n", f"{name}_F2P", f"{name}_F2N")
        for v in [x for x in vm if x]:
            C("2.2u", v, fp=C0603, Note="ADC_VMID: 2.2 uF + 0.22 uF (typical connection) - check")
            C("220n", v)

    # ---------------------------------------------------------------- ADC input buffers (20 channels)
    for ch in range(1, 21):
        chip, j, vmid = chan_net[ch]
        u = ref("U")
        add(u, "Amplifier_Operational:OPA1656ID", "OPA1656", SOIC8,
            {"1": f"B{ch}_OA", "2": f"B{ch}_IA", "3": vmid, "4": "-12V", "5": vmid, "6": f"B{ch}_IB", "7": f"B{ch}_OB", "8": "+12V"},
            LCSC="C1849431", Note=f"ADC{ch} input buffer: inverting x 1/4 (300 R / 1.2k), non-inverting inputs at {vmid}; 8 Vrms diff FS -> 2 Vrms")
        C("100n 25V", "+12V", fp=C0603)
        C("100n 25V", "-12V", fp=C0603)
        for leg, src, out_net, adc_net in (("A", f"ADC{ch}_P", f"B{ch}_OA", f"ADC{ch}_BN"), ("B", f"ADC{ch}_N", f"B{ch}_OB", f"ADC{ch}_BP")):
            C("68u 25V", src, f"B{ch}_C{leg}", fp=C1210, Note="series coupling 68 uF (Cirrus) - check type (low leakage)")
            R("1.2k", f"B{ch}_C{leg}", f"B{ch}_I{leg}", Note="0.1 %")
            R("300", out_net, f"B{ch}_I{leg}", Note="0.1 %: gain 1/4")
            C("680p C0G", out_net, f"B{ch}_I{leg}", fp=C0603)
            R("10", out_net, adc_net, Note="series to the ADC pin")
        C("15n C0G", f"ADC{ch}_BP", f"ADC{ch}_BN", fp=C0603, Note="across the pair at the ADC pins")
        R("100k", f"B{ch}_CA", "GND", Note="DC reference for the coupling cap when the source is open")
        R("100k", f"B{ch}_CB", "GND")

    # ================================================================ DAC
    dpins = {"2": "+3V3A", "38": "+3V3A", "11": "+3V3D", "7": "DAC_LDOD", "3": "GND", "37": "GND", "12": "GND", "49": "GND",
             "39": "DAC_FP", "40": "DAC_FN", "32": "DAC_VMID", "4": "DAC_LDOA", "6": "DAC_LDOD", "41": None, "42": None, "47": None,
             "8": "MCLK_DAC", "5": "RST_DAC", "9": "BCLK", "10": "FSYNC", "16": "DAC_DIN", "15": "GND", "14": "GND", "13": "GND",
             "17": "SPI_SCK", "18": "SPI_MISO", "19": "SPI_MOSI", "20": "CS_DAC",
             "48": "DAC_CFG1", "1": "DAC_CFG5", "22": "DAC_CFG2", "21": "DAC_CFG3", "23": "DAC_CFG4"}
    out_pins = {1: ("46", "45"), 2: ("44", "43"), 3: ("36", "35"), 4: ("34", "33"), 5: ("31", "30"), 6: ("29", "28"), 7: ("27", "26"), 8: ("25", "24")}
    for c, (pp, pn) in out_pins.items():
        dpins[pp], dpins[pn] = f"DO{c}_P", f"DO{c}_N"
    add(ref("U"), "ShtukaDruka:CS4308P", "CS4308P", QFN48, _fill(dpins, 49),
        Note="CS4308P: 8 channels, current outputs (I-V on this board), TDM data in on DIN1, software control by SPI; not in the EasyEDA library "
        "(R136): LCSC number to find or hand-place; QFN-48 6x6 P0.4, pad 4.6 - check the drawing")
    mclk_load("MCLK_DAC")
    R("100k", "RST_DAC", "GND")
    R("33", "CONV_RESET", "RST_DAC")
    R("0", "DAC_CFG1", "+3V3A", Note="CONFIG1 to VDD_A = software control mode - check")
    for k in (2, 3, 4):
        R("10k", f"DAC_CFG{k}", "GND")
    R("10k", "DAC_CFG5", "GND")
    C("1u", "+3V3A", fp=C0603)
    C("22u", "+3V3A", fp=C0805)
    C("4.7u", "+3V3A", fp=C0805)
    C("10n", "+3V3A")
    C("100n", "+3V3D")
    C("10u", "DAC_LDOD", fp=C0805)
    C("1u", "DAC_LDOA", fp=C0603)
    C("4.7u", "DAC_FP", "DAC_FN", fp=C0805, Note="DAC_FILTP/N - check value; FILTP to VDD_A2 per datasheet")
    C("10n", "DAC_FP", "DAC_FN")
    C("1u", "DAC_VMID", fp=C0603, Note="DAC_VMID 1 uF (typical connection)")
    dac_names = {1: "DAC_ML", 2: "DAC_MR", 3: "DAC_AL", 4: "DAC_AR", 5: "HP1L", 6: "HP1R", 7: "HP2L", 8: "HP2R"}
    for c in range(1, 9):
        u = ref("U")
        nm = dac_names[c]
        add(u, "Amplifier_Operational:OPA1656ID", "OPA1656", SOIC8,
            {"1": f"DO{c}_VP", "2": f"DO{c}_P", "3": "DAC_VMID", "4": "-12V", "5": "DAC_VMID", "6": f"DO{c}_N", "7": f"DO{c}_VN",
             "8": "+12V"}, LCSC="C1849431", Note=f"DAC{c} ({nm}): current-to-voltage, Rf 1.2k || 620 pF per leg (AN0679 fig. 1), 2 Vrms diff FS")
        C("100n 25V", "+12V", fp=C0603)
        C("100n 25V", "-12V", fp=C0603)
        for leg, o in (("P", f"DO{c}_VP"), ("N", f"DO{c}_VN")):
            R("1.2k", o, f"DO{c}_{leg}", Note="Rf 0.1 %")
            C("620p C0G", o, f"DO{c}_{leg}", fp=C0603)
            out_net = f"{nm}_{'P' if leg == 'P' else 'N'}"
            R("47", o, out_net, fp=R0603, Note="build-out to the cable")
        C("1n C0G", f"{nm}_P", f"{nm}_N", fp=C0603, Note="across the pair")

    # ================================================================ xcore.ai A and B
    def xcore(tag, xl_a, notes):
        u = ref("U")
        v = "+0V9" + tag
        xs = {}
        for pin in (4, 12, 19, 27, 34, 42, 49, 57, 61, 62, 63, 64):
            xs[str(pin)] = v
        xs.update({"8": "+3V3D", "38": "+3V3D", "52": "+3V3D", "17": "+1V8", "26": "+1V8", "22": f"PLL{tag}", "30": "+3V3D", "31": "+1V8",
                   "65": "GND", "25": None, "16": f"XIN{tag}", "15": f"XOUT{tag}", "21": f"RST{tag}", "23": f"TMS{tag}", "24": f"TCK{tag}",
                   "18": f"TDI{tag}", "20": f"TDO{tag}"})
        # QSPI boot flash: SS X0D01 (3), SCLK X0D10 (5), DQ0-3 X0D04 (59), X0D05 (1), X0D06 (60), X0D07 (2)
        xs.update({"3": f"QCS{tag}", "5": f"QCLK{tag}", "59": f"QD0{tag}", "1": f"QD1{tag}", "60": f"QD2{tag}", "2": f"QD3{tag}"})
        xs.update(xl_a)
        xs.update(notes)
        return u, xs

    xlA = {"36": "XLA_O0", "37": "XLA_O1", "35": "XLA_I0", "33": "XLA_I1"}    # A out0/out1 -> B in0/in1; B out0/out1 -> A in0/in1
    xlB = {"36": "XLA_I0", "37": "XLA_I1", "35": "XLA_O0", "33": "XLA_O1"}
    # A: MCLK X0D11 (7), BCLK X0D00 (6), FSYNC X0D35 (41), DAC DIN X0D36 (43), ADC SDO X0D37 (44) X0D38 (45) X0D39 (47),
    #    SPI tile 1: SCK X1D00 (9), MOSI X1D01 (10), MISO X1D10 (13), CS X1D11 (14), X1D22 (39), X1D13 (32), X1D34 (53),
    #    reset X0D29 (40), oscillator enables X0D30 (54), X0D31 (55), VBUS sense X0D40 (46), USB 28/29
    pa = {"7": "MCLK_XA", "6": "BCLK_X", "41": "FSYNC_X", "43": "DAC_DIN", "44": "ADCA_SDO", "45": "ADCB_SDO", "47": "ADCC_SDO",
          "9": "SPI_SCK", "10": "SPI_MOSI", "13": "SPI_MISO", "14": "CS_ADCA", "39": "CS_ADCB", "32": "CS_ADCC", "53": "CS_DAC",
          "40": "CONV_RESET", "54": "OSC48_EN", "55": "OSC44_EN", "46": "HUB_VBUS_S", "28": "HUB_DM", "29": "HUB_DP"}
    uA, xa = xcore("A", xlA, pa)
    # B: MCLK X0D11 (7), PDM X1D00 (9) clock, X1D01 (10) data, USB 28/29 to the isolator
    pb = {"7": "MCLK_XB", "9": "PDM_CLK", "10": "PDM_DATA", "28": "UDM", "29": "UDP"}
    uB, xb = xcore("B", xlB, pb)
    for u, xs, tag, what in ((uA, xa, "A", "bus master, USB port A (hub), TDM, SPI to the converters"),
                             (uB, xb, "B", "USB port B (external computer) through the ADuM4166, PDM microphone")):
        add(u, "ShtukaDruka:XU316-1024-QF60B", "XU316-1024-QF60B", "ShtukaDruka:XU316-1024-QF60B_QFN-60_7x7_P0.4", _fill(xs, 65), LCSC="C7397517",
            Note=f"xcore {tag}: {what}; core 0.9 V, I/O 3.3 V (left/right/top), 1.8 V (bottom: JTAG, crystal) - port plan in PLAN.md")
        mclk_load(f"MCLK_X{tag}")
        # power decoupling
        for _ in range(4):
            C("100n", f"+0V9{tag}")
        C("4.7u", f"+0V9{tag}", fp=C0603)
        for net in ("+3V3D", "+3V3D", "+3V3D", "+1V8", "+1V8"):
            C("100n", net)
        FB(f"+0V9{tag}", f"PLL{tag}", Note="PLL_AVDD filter (0.9 V - check against the datasheet)")
        C("4.7u", f"PLL{tag}", fp=C0603)
        C("100n", f"PLL{tag}")
        # crystal 24 MHz on XIN/XOUT (1.8 V domain)
        add(ref("Y"), "Device:Crystal_GND24", "24MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
            {"1": f"XIN{tag}", "3": f"XOUT{tag}", "2": "GND", "4": "GND"}, LCSC="C70590", Note="X322524MOB4SI, 12 pF load - check against XMOS")
        C("18p", f"XIN{tag}")
        C("18p", f"XOUT{tag}")
        # reset, JTAG
        R("10k", f"RST{tag}", "+1V8", Note="RST_N pull-up (1.8 V domain)")
        C("100n", f"RST{tag}")
        add(ref("J"), "Connector_Generic:Conn_01x06", f"JTAG {tag}", PH.format(n=6),
            {"1": f"TCK{tag}", "2": f"TMS{tag}", "3": f"TDI{tag}", "4": f"TDO{tag}", "5": f"RST{tag}", "6": "GND"},
            Note=f"xcore {tag} debug: 1.8 V logic, xTAG adapter - check the pinout")
        # boot flash
        add(ref("U"), "Memory_Flash:W25Q16JVSS", "W25Q16JVSIQ", "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
            {"1": f"QCS{tag}", "2": f"QD1{tag}", "3": f"QD2{tag}", "4": "GND", "5": f"QD0{tag}", "6": f"QCLK{tag}", "7": f"QD3{tag}",
             "8": "+3V3D"}, LCSC="C131025", Note=f"xcore {tag} boot flash (QSPI), 16 Mbit - firmware + UAC2 descriptors; check size")
        C("100n", "+3V3D")
        R("10k", f"QCS{tag}", "+3V3D")

    # USB port A (hub cable): ESD and VBUS sense divider
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", SOT236,
        {"1": "HUB_DP", "6": "HUB_DP", "3": "HUB_DM", "4": "HUB_DM", "2": "GND", "5": "HUB_VBUS"}, LCSC="C323793")
    R("10k", "HUB_VBUS", "HUB_VBUS_S")
    R("20k", "HUB_VBUS_S", "GND", Note="5 V -> 3.33 V sense for xcore A (port A VBUS present)")

    # ================================================================ USB port B: PC jack side (GNDPC), ADuM4166, xcore B
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", SOT236,
        {"1": "PC_DP", "6": "PC_DP", "3": "PC_DM", "4": "PC_DM", "2": "GNDPC", "5": "PC_VBUS"}, LCSC="C323793", Note="ESD on the computer side")
    R("5.1k", "PC_CC1", "GNDPC", Note="device (Rd)")
    R("5.1k", "PC_CC2", "GNDPC", Note="device (Rd)")
    add(ref("U"), "ShtukaDruka:ADuM4166", "ADuM4166", "Package_SO:SOIC-20W_7.5x15.4mm_P1.27mm",
        {"1": "PC_VBUS", "3": "ISO_V1", "8": "PC_DP", "9": "PC_DM", "2": "GNDPC", "4": "GNDPC", "5": "GNDPC", "6": "GNDPC", "7": "GNDPC", "10": "GNDPC",
         "20": "+5V", "18": "+3V3D", "12": "UDP", "13": "UDM", "14": None, "15": "ISO_XO", "16": "ISO_XI", "11": "GND", "17": "GND", "19": "GND"},
        LCSC="C5367256", Note="USB 2.0 HS isolator: side 1 = computer (VBUS1 = PC VBUS, GNDPC), side 2 = xcore B (VBUS2 +5 V, VDD2 3.3 V); "
        "supply pins and crystal: check the datasheet; footprint SOIC-20W 15.4 mm per the LCSC part - check")
    C("1u", "PC_VBUS", "GNDPC", fp=C0603)
    C("1u", "ISO_V1", "GNDPC", fp=C0603, Note="VDD1: check whether it is an output (LDO) or an input")
    C("100n", "+3V3D")
    C("1u", "+5V", fp=C0603)
    add(ref("Y"), "Device:Crystal_GND24", "24MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
        {"1": "ISO_XI", "3": "ISO_XO", "2": "GND", "4": "GND"}, LCSC="C70590", Note="ADuM4166 crystal (XI2/XO2): frequency - check")
    C("18p", "ISO_XI")
    C("18p", "ISO_XO")

    # ================================================================ shared TDM clocks: source series resistors
    R("22", "BCLK_X", "BCLK", Note="BCLK from xcore A to the four converters")
    R("22", "FSYNC_X", "FSYNC")
    R("100k", "DAC_DIN", "GND")
    R("100k", "CONV_RESET", "GND", Note="converters stay in reset until xcore A drives the line")
    for net in ("SPI_SCK", "CS_ADCA", "CS_ADCB", "CS_ADCC", "CS_DAC"):
        R("100k", net, "+3V3D" if net.startswith("CS_") else "GND", Note="idle state while xcore A boots")
    # decoupling on the board-to-board rails
    for _ in range(2):
        C("47u 25V", "+12V", fp="Capacitor_SMD:CP_Elec_6.3x7.7")
        C("47u 25V", "GND", "-12V", fp="Capacitor_SMD:CP_Elec_6.3x7.7")
    C("47u 10V", "+5V", fp="Capacitor_SMD:CP_Elec_6.3x7.7")
    return P


def placement():
    """Rev 0.1 is the schematic only."""
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
