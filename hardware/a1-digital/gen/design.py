"""A1 - Digital audio board (under the slope, left; mates R1 at a right angle): 20 differential ADC channels (CS5308P x 2 + CS5304P),
8 DAC channels (CS4308P) with current-to-voltage stages, two XMOS xcore.ai (XU316-1024-QF60B): A = bus master, internal USB audio port to
the Mini-ITX (port A, through the R2 hub) and the converters' SPI; B = USB device to the external computer through an ISOUSB211 isolator
(port B). Two oscillators (24.576 and 22.5792 MHz, R114), quiet 3.3 V, 1.8 V, two 0.9 V cores.
Single source of truth for the schematic. Plan, pinouts and sources: hardware/a1-digital/PLAN.md; decisions R82-R84, R87, R88, R114, R116,
R117, R136; levels: R1 README ("ADC buffer FS 8 Vrms").

Input stage (CS5308P fig. 2-1 / AN0635): R1 delivers 8 Vrms differential at 0 dBFS; each leg goes through 68 uF and 1.2k into an inverting
stage of an OPA1656 (Rf 300 R || 680 pF, non-inverting input at the converter's ADC_VMID) = gain 1/4 -> 2 Vrms at the ADC pins; 10 R in series
with every pin, 15 nF across the pair. The stage inverts, so the source P leg drives the converter's N pin: the polarity is kept.
Output stage (AN0679 fig. 1): inverting I-V per leg, Rf 1.2k || 620 pF, non-inverting input at DAC_VMID, 2 Vrms differential full scale;
47 R build-out, 1 nF across the pair. Outputs 1-4 = Main L/R, Aux L/R (to R1), 5-8 = Phones 1 L/R, 2 L/R (to F1).

Rev 0.1 (14.11.2026, PC) = schematic only. Rev 0.2 (14.11.2026, cloud #26) = checked against the datasheets CS4308P DS1317, CS53A04P DS1397,
XU316-1024-QF60B, ADuM4165/4166: converter capacitors, 47 uF X5R coupling capacitors, PLL_AVDD filter, ADuM4166 supplies (VBUS2 = VDD2),
oscillator parts. The CS5308P / CS5304P datasheets were not reachable: their pins are compared with the CS53A04P (same family).
Rev 0.5 (18.11.2026, schematic audit notes/reviews/schematics_2026-11-18.md, B1): BAT54S overload clamp (3V3A / GND) on every ADC input pin (40 pins), CS5308P DS1314F2
table 3-3: -0.3 ... VDD_A + 0.3 V and 10 mA.
Rev 0.6 (18.11.2026, audit): 24.576 MHz oscillator YXC OT2EL4C4JI (OE-low state unknown) -> SCTF SX3M24.576B10F20TNN (tri-state, same family as the 22.5792 one).
Rev 0.7 (19.11.2026, ADuM4166 datasheet read): isolator crystal 12 pF -> 10 pF (S322524M10PF10PPM, C7568725); rest of the isolator node checked, no other change.
Rev 0.8 (19.11.2026): +5V bulk capacitor 47 uF 10 V -> 25 V (C190223), same 6.3 x 7.7 footprint.
Rev 0.9 (20.11.2026): USB isolator ADuM4166 (unavailable) -> TI ISOUSB211DPR (SSOP-28 DP0028A, no crystal): the isolator crystal and its 15 pF capacitors are gone; supplies per the datasheet (side 2 from +3V3D and +1V8).
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
REV = "1.0"
M1_LIB = K.M1_LIB
BUS_NOTE = ("R1 -> A1: 18 ADC pairs (8 Vrms FS), A1 -> R1: Main/Aux DAC pairs, A1 -> F1: Phones pairs; xcore A: TDM master, SPI to the "
            "converters, USB port A (hub on R2), xcore B: USB port B through the ISOUSB211 (isolated ground GNDPC)")
PWR_FLAG_NETS = ("+12V", "-12V", "GNDPC", "PC_VBUS", "ISO_V1", "ISO_V18", "+0V9A", "+0V9B", "PLLA", "PLLB")   # ERC: R1 rails, computer side, buck outputs, filtered PLL supplies
NO_PWR_FLAG = ("+3V3",)          # no plain +3V3 rail here (+3V3A and +3V3D): no standard power symbol for it
W, H = 220.0, 100.0          # rough: under the slope on the left, about 220 x 100 mm (doc 29)
HOLES = [(4.0, 4.0), (216.0, 4.0), (4.0, 96.0), (216.0, 96.0), (110.0, 4.0), (110.0, 96.0)]   # M3, board coordinates (KiCad, y down); 15.11.2026
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603, R1206 = "Resistor_SMD:R_0603_1608Metric", "Resistor_SMD:R_1206_3216Metric"
C1210 = "Capacitor_SMD:C_1210_3225Metric"
SOIC8 = "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
SOT235, SOT236 = "Package_TO_SOT_SMD:SOT-23-5", "Package_TO_SOT_SMD:SOT-23-6"
SOT23 = "Package_TO_SOT_SMD:SOT-23"
QFN48 = "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm"   # CS5308P DS1314F2 / CS5304P: EP 4.6 nom (4.5-4.7)
QFN48_DAC = "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.3x4.3mm"   # CS4308P DS1317F1 fig. 10-1: EP 4.3 nom (4.2-4.4), L 0.4
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
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Y": 0, "L": 0, "FB": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

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
        Note="cable from the rear USB-C (PC) receptacle on the wall (R145): data only, isolated by the ISOUSB211; Rd 5.1k on A1")
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

    ldo33("+3V3D", "digital 3.3 V: xcore I/O + USB_VDD33, flash, converter digital I/O, oscillators, ISOUSB211 side 2 (600 mA max; about 150 mA typical = 0.26 W in the SOT-23-5, +65 K: watch the temperature)")
    add(ref("U"), "Regulator_Linear:AP2112K-1.8", "AP2112K-1.8", SOT235, {"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": "+1V8"},
        LCSC="C176944", Note="1.8 V: xcore bottom I/O domain (JTAG, crystal) and USB_VDD18")
    C("1u", "+5V", fp=C0603)
    C("2.2u", "+1V8", fp=C0603)
    u = ref("U")
    add(u, "Regulator_Linear:TPS7A4701xRGW", "TPS7A4701", "Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias",
        {"1": "+3V3A", "3": "+3V3A", "4": None, "5": None, "6": None, "7": "GND", "8": "GND", "9": None, "10": None, "11": "GND",
         "12": "GND", "13": "+5V", "14": "REG_NR", "15": "+5V", "16": "+5V", "20": "+3V3A", "21": "GND"},
        LCSC="C90084", Note="quiet analog 3.3 V for the converters: ANY-OUT 1.4 + 1.6 + 0.2 + 0.1 = 3.3 V (pins 8, 11, 12 to GND), 4 uV rms")
    C("1u", "REG_NR", fp=C0603, Note="NR/SS 1 uF: not verified (the TI datasheet text was not retrievable)")
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
        add(ref("L"), "Device:L", "2.2uH", "Inductor_SMD:L_Bourns-SRN4018", {"1": f"SW{k}", "2": core}, Note="2.2 uH, Isat >= 2 A (TLV62568: 1 A)")
        C("10u", "+5V", fp=C0805)
        C("22u", core, fp=C0805)
        C("22u", core, fp=C0805)

    # ================================================================ clocks
    osc_lcsc = {"OSC48": "C7431342", "OSC44": "C7431341"}
    osc_note = {"OSC48": "SCTF SX3M24.576B10F20TNN (LCSC C7431342), same series as the 22.5792 one: 3.3 V CMOS, +-10 ppm, pin 1 tri-state (high or open = on), 922 in stock on "
                         "18.11.2026; rev 0.6 (audit): replaces the YXC OT2EL4C4JI-111OLP (C5203547, jitter 0.7 ps) whose datasheet could not be downloaded, so the output state "
                         "at OE low (Hi-Z or low) is unknown: with outputs tied a low-driving disabled oscillator would halve the other one. Jitter of the SCTF is NOT in its datasheet: measure (B19)",
                "OSC44": "SCTF SX3M22.5792B10F20TNN (LCSC C7431341), 3.3 V CMOS, +-10 ppm, pin 1 tri-state (high or open = on), 641 in stock on "
                         "14.11.2026; jitter is NOT in the datasheet: measure on the first board (B19)"}
    for nm, freq, en_pull in (("OSC48", "24.576MHz", "+3V3D"), ("OSC44", "22.5792MHz", "GND")):
        add(ref("Y"), "Oscillator:ASE-xxxMHz", freq, OSC, {"1": f"{nm}_EN", "2": "GND", "3": f"{nm}_OUT", "4": "+3V3D"},
            LCSC=osc_lcsc[nm], Note=f"{freq} 3.3 V oscillator, 3.2 x 2.5, pin 1 = output enable (high = on): {osc_note[nm]} (R114)")
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
            R("1k", f"{name}_CFG{k}", "GND", Note="CONFIG2-4 are the HGC SPI outputs in software mode (unused: HGC off); 1k to ground is safe either way")
        R("10k", f"{name}_CFG5", "GND", Note="SPI: CONFIG5 to GND (datasheet)")
        for _ in range(2):
            C("4.7u", "+3V3A", fp=C0805, Note="VDD_A1 / VDD_A2: 4.7 uF + 10 nF each (typical connection)")
            C("10n", "+3V3A")
        C("100n", "+3V3D")
        C("1u", f"{name}_LDOD", fp=C0603, Note="LDO_D_FILT / VDD_D: 1 uF (typical connection)")
        C("1u", f"{name}_LDOA", fp=C0603, Note="LDO_A_FILT: 1 uF (typical connection)")
        R("1", "+3V3A", f"{name}_F1P", Note="ADC_FILTP to VDD_A via 1 R (datasheet)")
        C("4.7u", f"{name}_F1P", f"{name}_F1N", fp=C0805, Note="FILT 4.7 uF + 0.47 uF (typical connection, pair assignment read from the figure)")
        C("470n", f"{name}_F1P", f"{name}_F1N")
        if value == "CS5308P":
            R("1", "+3V3A", f"{name}_F2P")
            C("4.7u", f"{name}_F2P", f"{name}_F2N", fp=C0805)
            C("470n", f"{name}_F2P", f"{name}_F2N")
        for v in [x for x in vm if x]:
            C("2.2u", v, fp=C0603, Note="ADC_VMID: 2.2 uF + 0.22 uF (typical connection; pairing with FILT read from the figure)")
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
            # P108 (18.11.2026, chief engineer): Cirrus AN0556 4.1 asks for C0G or electrolytic coupling capacitors. A truly NON-POLARISED SMD
            # electrolytic exists: Wuerth WCAP-ASNP 865250349007, 47 uF 16 V, 8.0 x 6.5 mm (datasheet rev 002.000: non-polarized, no reverse voltage),
            # 239 pcs at Digikey 18.11.2026, LCSC C5530373 (0 in stock at JLCPCB: hand-soldered, 40 pcs). Same corner as rev 0.4 (2.8 Hz with 1.2k);
            # THD+N at 20-50 Hz is not in the datasheet: measure on the first board. Footprint: KiCad CP_Elec_8x6.5 (8 x 6.5 mm) as an approximation of the
            # datasheet land pattern (check before ordering boards). One lot per board (tolerance +-20 %).
            add(ref("C"), "Device:C", "47u 16V NP", "Capacitor_SMD:CP_Elec_8x6.5", {"1": src, "2": f"B{ch}_C{leg}"}, LCSC="C5530373",
                Note="coupling capacitor, non-polarised (Wuerth WCAP-ASNP 865250349007); Cirrus AN0556 4.1: electrolytic or C0G; hand-soldered (not in stock at JLCPCB)")
            R("1.2k", f"B{ch}_C{leg}", f"B{ch}_I{leg}", Note="0.1 %")
            R("300", out_net, f"B{ch}_I{leg}", Note="0.1 %: gain 1/4")
            C("680p C0G", out_net, f"B{ch}_I{leg}", fp=C0603)
            R("10", out_net, adc_net, Note="series to the ADC pin")
            # rev 0.5 (audit 18.11.2026, B1): CS5308P DS1314F2 table 3-3: analog inputs -0.3 ... VDD_A + 0.3 V, +-10 mA. A clipped R1 stage (about +-11 V) leaves
            # this buffer at 1.65 V +- 2.75 V = -1.1 ... +4.4 V: about 70 mA through 10 R into the ADC's own diodes. A BAT54S Schottky pair per pin (3V3A / GND) takes it.
            add(ref("D"), "Diode:BAT54S", "BAT54S", SOT23, {"1": "GND", "2": "+3V3A", "3": adc_net}, LCSC="C19726",
                Note="overload clamp at the ADC pin (CS5308P abs. max -0.3 ... VDD_A+0.3 V, 10 mA): Schottky conducts before the ADC's internal diodes; onsemi C19726")
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
    add(ref("U"), "ShtukaDruka:CS4308P", "CS4308P", QFN48_DAC, _fill(dpins, 49),
        Note="CS4308P: 8 channels, current outputs (I-V on this board), TDM data in on DIN1, software control by SPI; not in the EasyEDA library "
        "(R136): no LCSC number, order CS4308P-DN from Digikey (598-CS4308P-DN-ND), hand-soldered; 48-QFN 6x6 P0.4, exposed pad 4.3 x 4.3 "
        "(DS1317F1 fig. 10-1), smaller than the 4.6 pad of the ADCs")
    mclk_load("MCLK_DAC")
    R("100k", "RST_DAC", "GND")
    R("33", "CONV_RESET", "RST_DAC")
    R("0", "DAC_CFG1", "+3V3A", Note="CONFIG1 to VDD_A = software control mode - check")
    for k in (2, 3, 4):
        R("10k", f"DAC_CFG{k}", "GND")
    R("10k", "DAC_CFG5", "GND")
    for _ in range(2):
        C("4.7u", "+3V3A", fp=C0805, Note="VDD_A1 / VDD_A2: 4.7 uF + 10 nF each (typical connection)")
        C("10n", "+3V3A")
    C("100n", "+3V3D")
    C("1u", "DAC_LDOD", fp=C0603, Note="LDO_D_FILT / VDD_D: 1 uF (typical connection)")
    C("1u", "DAC_LDOA", fp=C0603, Note="LDO_A_FILT: 1 uF (typical connection)")
    C("22u", "DAC_FP", "+3V3A", fp=C0805, Note="DAC_FILTP: 22 uF to VDD_A2 (typical connection, Table 1-1)")
    C("22u", "DAC_FN", fp=C0805, Note="DAC_FILTN: 22 uF to ground (typical connection)")
    C("10u", "DAC_VMID", fp=C0805, Note="DAC_VMID 10 uF (typical connection; AN0679: 2 x 10 uF lowers THD+N, slows start-up)")
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
                             (uB, xb, "B", "USB port B (external computer) through the ISOUSB211, PDM microphone")):
        add(u, "ShtukaDruka:XU316-1024-QF60B", "XU316-1024-QF60B", "ShtukaDruka:XU316-1024-QF60B_QFN-60_7x7_P0.4", _fill(xs, 65), LCSC="C7397517",
            Note=f"xcore {tag}: {what}; core 0.9 V, I/O 3.3 V (left/right/top), 1.8 V (bottom: JTAG, crystal) - port plan in PLAN.md")
        mclk_load(f"MCLK_X{tag}")
        # power decoupling
        for _ in range(4):
            C("100n", f"+0V9{tag}")
        C("4.7u", f"+0V9{tag}", fp=C0603)
        for net in ("+3V3D", "+3V3D", "+3V3D", "+1V8", "+1V8"):
            C("100n", net)
        FB(f"+0V9{tag}", f"PLL{tag}", Note="PLL_AVDD filter: 600 R at 100 MHz, DCR < 1 R, + 1 uF MLCC (XMOS datasheet, 0.9 V nominal)")
        C("1u", f"PLL{tag}", fp=C0603, Note="PLL_AVDD 1 uF MLCC, close to pin 22")
        C("100n", f"PLL{tag}")
        # crystal 24 MHz on XIN/XOUT (1.8 V domain)
        add(ref("Y"), "Device:Crystal_GND24", "24MHz", "Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
            {"1": f"XIN{tag}", "3": f"XOUT{tag}", "2": "GND", "4": "GND"}, LCSC="C70590", Note="X322524MOB4SI: 24 MHz, 12 pF load, ESR <= 60 R as XMOS requires (18 pF caps)")
        C("18p", f"XIN{tag}")
        C("18p", f"XOUT{tag}")
        # reset, JTAG
        R("10k", f"RST{tag}", "+1V8", Note="RST_N pull-up (1.8 V domain)")
        C("100n", f"RST{tag}")
        add(ref("J"), "Connector_Generic:Conn_01x06", f"JTAG {tag}", PH.format(n=6),
            {"1": f"TCK{tag}", "2": f"TMS{tag}", "3": f"TDI{tag}", "4": f"TDO{tag}", "5": f"RST{tag}", "6": "GND"},
            Note=f"xcore {tag} debug: 1.8 V logic (TCK, TMS, TDI, TDO, RST_N), xTAG adapter - check the cable pinout")
        # boot flash
        add(ref("U"), "Memory_Flash:W25Q16JVSS", "W25Q32JVSSIQ", "Package_SO:SOIC-8_5.3x5.3mm_P1.27mm",
            {"1": f"QCS{tag}", "2": f"QD1{tag}", "3": f"QD2{tag}", "4": "GND", "5": f"QD0{tag}", "6": f"QCLK{tag}", "7": f"QD3{tag}",
             "8": "+3V3D"}, LCSC="C179173", Note=f"xcore {tag} boot flash (QSPI) 32 Mbit (4 MB, B18; pinout of the W25Q16 symbol): ready within 300 us of power-up, Quad I/O read (0xEB): set QE once from xflash; boot pins X0D04-06 have weak pull-downs = QSPI")
        C("100n", "+3V3D")
        R("10k", f"QCS{tag}", "+3V3D")

    # USB port A (hub cable): ESD and VBUS sense divider
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", SOT236,
        {"1": "HUB_DP", "6": "HUB_DP", "3": "HUB_DM", "4": "HUB_DM", "2": "GND", "5": "HUB_VBUS"}, LCSC="C7519")
    R("10k", "HUB_VBUS", "HUB_VBUS_S")
    R("20k", "HUB_VBUS_S", "GND", Note="5 V -> 3.33 V sense for xcore A (port A VBUS present)")

    # ================================================================ USB port B: PC jack side (GNDPC), ISOUSB211, xcore B
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", SOT236,
        {"1": "PC_DP", "6": "PC_DP", "3": "PC_DM", "4": "PC_DM", "2": "GNDPC", "5": "PC_VBUS"}, LCSC="C7519", Note="ESD on the computer side")
    R("5.1k", "PC_CC1", "GNDPC", Note="device (Rd)")
    R("5.1k", "PC_CC2", "GNDPC", Note="device (Rd)")
    # rev 0.9 (20.11.2026): ADuM4166 (no stock anywhere, 51 weeks at Digikey) -> TI ISOUSB211 (SLLSFC5D): USB 2.0 repeater LS/FS/HS 480 Mbit/s, reinforced 5.7 kVrms, no crystal.
    # Side 1 (PC cable, GNDPC): VBUS1 and VCC1 from PC VBUS 5 V, internal LDOs make V3P3V1 (ISO_V1) and V1P8V1 (ISO_V18) - USB cable power, about 50-60 mA, 0.3-0.5 W in the chip (RthJA 44 K/W).
    # Side 2 (A1 ground): VBUS2 = V3P3V2 = +3V3D (external 3.3 V, allowed), VCC2 = V1P8V2 = +1V8 (external 1.8 V from the AP2112K-1.8, internal LDO bypassed, less heat);
    # no isolated DC-DC is needed: both sides have their own supply from their own side (the PC ground is isolated by the barrier, the PC only gives VBUS).
    add(ref("U"), "ShtukaDruka:ISOUSB211", "ISOUSB211DPR", "ShtukaDruka:SSOP-28_DP0028A_7.5x10.3mm_P0.65mm",
        {"1": "PC_VBUS", "2": "ISO_V1", "3": "GNDPC", "4": "ISO_V18", "5": "PC_VBUS", "6": None, "7": "PC_DM", "8": "PC_DP", "9": "GNDPC", "10": "GNDPC",
         "11": "ISO_V18", "12": "GNDPC", "13": "ISO_V1", "14": None, "15": None, "16": "+3V3D", "17": "GND", "18": "+1V8", "19": "GND", "20": "GND",
         "21": "UDP", "22": "UDM", "23": None, "24": "+1V8", "25": "+1V8", "26": "GND", "27": "+3V3D", "28": "+3V3D"},
        LCSC="C5772877", Note="USB 2.0 HS isolator (SLLSFC5D): UD+/UD- (7, 8) to the PC jack, DD+/DD- (21, 22) = xcore B; EQ pins 00 (GND); CDPENZ high = no CDP advertising; "
        "V1OK/V2OK open; NC 14, 15 open. Capacitors per 8.3: 1 uF at VBUSx, 0.1 uF at V3P3Vx, 2 uF + 0.1 uF + 10 nF at V1P8Vx. Footprint DP0028A (SSOP-28, body 7.5 x 10.3, creepage 8.15 mm: "
        "no copper of any layer between the sides under the chip). JLC 15 pcs, LCSC about 1420, Digikey 3553 (20.11.2026)")
    C("1u", "PC_VBUS", "GNDPC", fp=C0402, Note="VBUS1 / VCC1: 1 uF close to pins 1 and 5")
    C("100n", "ISO_V1", "GNDPC", fp=C0402, Note="V3P3V1 (internal LDO output): 0.1 uF close to pin 2")
    C("2.2u", "ISO_V18", "GNDPC", fp=C0402, Note="V1P8V1: 2 uF (the datasheet: 2 uF + 0.1 uF + 10 nF), close to pin 4")
    C("100n", "ISO_V18", "GNDPC", fp=C0402)
    C("10n", "ISO_V18", "GNDPC", fp=C0402)
    C("1u", "+3V3D", fp=C0402, Note="VBUS2: 1 uF close to pin 28")
    C("100n", "+3V3D", fp=C0402, Note="V3P3V2: 0.1 uF close to pin 27")
    C("2.2u", "+1V8", fp=C0402, Note="V1P8V2 / VCC2: 2 uF close to pin 25")
    C("100n", "+1V8", fp=C0402)
    C("10n", "+1V8", fp=C0402)

    # ================================================================ shared TDM clocks: source series resistors
    R("22", "BCLK_X", "BCLK", Note="BCLK from xcore A to the four converters")
    R("22", "FSYNC_X", "FSYNC")
    R("100k", "DAC_DIN", "GND")
    R("100k", "CONV_RESET", "GND", Note="converters stay in reset until xcore A drives the line")
    for net in ("SPI_SCK", "CS_ADCA", "CS_ADCB", "CS_ADCC", "CS_DAC"):
        R("100k", net, "+3V3D" if net.startswith("CS_") else "GND", Note="idle state while xcore A boots")
    # decoupling on the board-to-board rails
    for _ in range(2):
        C("47u 25V", "+12V", fp="Capacitor_SMD:CP_Elec_6.3x7.7", LCSC="C190223", Note="21.11.2026: the same part as C294 (KL1E470M-CRE77, C190223); stock: see C294, technologist re-checks")
        C("47u 25V", "GND", "-12V", fp="Capacitor_SMD:CP_Elec_6.3x7.7", LCSC="C190223", Note="21.11.2026: the same part as C294 (KL1E470M-CRE77, C190223); stock: see C294, technologist re-checks")
    C("47u 25V", "+5V", fp="Capacitor_SMD:CP_Elec_6.3x7.7", LCSC="C190223",
      Note="rev 0.8 (parts_missing.md): 47 uF 10 V 6.3x7.7 not in stock -> KL1E470M-CRE77 47 uF 25 V, D6.3 x L7.7 (C190223, 980 pcs), the same case as the +-12 V bulk capacitors; on 5 V it is derated, ESR is no concern for bulk")
    K.mount_holes(add, ref, HOLES, "M3 standoff (Codex review 15.11.2026): corners first; the final positions come with the enclosure")
    return P


def placement():
    """Rev 0.3: rough automatic placement (hardware/common/gen/autoplace.py): cable headers in a row along the bottom edge
    (top side), ICs on a grid, small parts around the IC they share signals with. Starting point for the routing."""
    import autoplace
    # the two TLV62568 buck converters (U4, U5) and their inductors (L1, L2) go to the empty top-right corner: in rev 0.3 they sat
    # 16-32 mm from the 24.576 / 22.5792 MHz audio master clocks (Y1, Y2) and 63 mm from the CS5304P; now 38-55 mm from the clocks (measured 15.11.2026 after adding the holes; was 16-32)
    fixed = {"U4": (210.0, 10.0, 0, "top"), "L1": (196.0, 10.0, 0, "top"), "U5": (210.0, 24.0, 0, "top"), "L2": (196.0, 24.0, 0, "top")}   # inside W = 220
    fixed.update(K.hole_fixed(parts(), HOLES))
    return autoplace.fit(sys.modules[__name__], lambda g, ic: autoplace.place(sys.modules[__name__], fixed=fixed, conn_y=H - 8.5, gap=g, ic_gap=ic), gaps=(1.0, 0.8, 0.6, 0.4, 0.25))   # 1.0 fits (800 s per try: 1.2/1.4 not tried, each try ~13 min)   # header row clear of the bottom holes


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
