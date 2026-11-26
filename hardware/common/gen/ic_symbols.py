"""Library symbols for the A1 digital board that KiCad does not ship: Cirrus CS5308P / CS5304P (ADC), CS4308P (DAC), XMOS XU316-1024-QF60B,
ADI ADuM4166. Pin numbers and names from the datasheets (CS5308P DS1314F1, CS5304P DS1313F1, CS4308P DS1317F1, XMOS XM-015129-PC QF60B list,
LCSC/EasyEDA symbols for the XU316 and ADuM4166); see hardware/a1-digital/PLAN.md. Written into ShtukaDruka.kicad_sym by
hardware/m1-screen-knobs/gen/make_lib.py (write_symbols). License: AGPL-3.0-or-later.
"""

F = "(effects (font (size 1.27 1.27)))"
FH = "(effects (font (size 1.27 1.27)) hide)"


def _prop(name, value, x, y, hide=False, justify=None):
    j = f" (justify {justify})" if justify else ""
    return f'    (property "{name}" "{value}" (at {x:g} {y:g} 0)\n      (effects (font (size 1.27 1.27)){j}{" hide" if hide else ""})\n    )\n'


def _pin(kind, x, y, angle, name, number, length=2.54):
    return (f'      (pin {kind} line (at {x:g} {y:g} {angle}) (length {length:g})\n        (name "{name}" {F})\n'
            f'        (number "{number}" {F})\n      )\n')


def ic(name, value, ref, fp, datasheet, lcsc, descr, left, right, top, bottom):
    """Single-unit rectangle symbol. Each side is a list of (number, name, type) or None (gap)."""
    n_l, n_r = len(left), len(right)
    h = max(n_l, n_r) * 2.54 + 5.08
    w = max(len(top), len(bottom), 1) * 2.54 + 7.62
    w = max(w, 20.32)
    hw, hh = round(w / 2 / 2.54) * 2.54, round(h / 2 / 2.54) * 2.54
    s = f'  (symbol "{name}" (pin_names (offset 1.016)) (in_bom yes) (on_board yes)\n'
    s += _prop("Reference", ref, -hw, hh + 1.27, justify="left")
    s += _prop("Value", value, -hw, -hh - 1.27, justify="left")
    s += _prop("Footprint", fp, 0, 0, hide=True)
    s += _prop("Datasheet", datasheet, 0, 0, hide=True)
    s += _prop("ki_description", descr, 0, 0, hide=True)
    s += _prop("LCSC", lcsc, 0, 0, hide=True)
    s += f'    (symbol "{name}_0_1"\n      (rectangle (start {-hw:g} {hh:g}) (end {hw:g} {-hh:g}) (stroke (width 0.254) (type default)) (fill (type background)))\n    )\n'
    s += f'    (symbol "{name}_1_1"\n'
    for side, items in (("L", left), ("R", right)):
        y = hh - 2.54
        for it in items:
            if it:
                x, a = (-hw - 2.54, 0) if side == "L" else (hw + 2.54, 180)
                s += _pin(it[2], x, round(y, 2), a, it[1], it[0])
            y -= 2.54
    for side, items in (("T", top), ("B", bottom)):
        x = -hw + 2.54
        for it in items:
            if it:
                y, a = (hh + 2.54, 270) if side == "T" else (-hh - 2.54, 90)
                s += _pin(it[2], round(x, 2), y, a, it[1], it[0])
            x += 2.54
    s += '    )\n  )\n'
    return s


I, O, B, P, PA, NC = "input", "output", "bidirectional", "power_in", "passive", "no_connect"


def cs5308p():
    ins = []
    for k, (p, n) in enumerate(((40, 39), (42, 41), (46, 45), (48, 47), (14, 13), (16, 15), (20, 19), (22, 21))):
        ins += [(str(p), f"IN{k + 1}P", I), (str(n), f"IN{k + 1}N", I)]
    left = ins
    right = [("29", "ASP_BCLK", B), ("24", "ASP_FSYNC", B), ("25", "ASP_DOUT1", O), ("26", "ASP_DOUT2", O), ("27", "ASP_DOUT3", O),
             ("28", "ASP_DOUT4", O), None, ("34", "MCLK", I), ("23", "RESET", I), None, ("36", "SPI_SCK", I), ("35", "SPI_SDO/I2C_SCL", B),
             ("37", "SPI_SDI/I2C_SDA", B), ("38", "SPI_CS", I), None, ("2", "CONFIG1", B), ("3", "CONFIG2/HGC_SCK", B),
             ("4", "CONFIG3/HGC_SDO", B), ("10", "CONFIG4/HGC_CS", B), ("11", "CONFIG5", B)]
    top = [("5", "VDD_A1", P), ("9", "VDD_A2", P), ("31", "VDD_IO", P), ("33", "VDD_D", PA)]
    bottom = [("6", "GND_A", P), ("8", "GND_A", P), ("30", "GND_D", P), ("49", "EP", P), None, ("43", "ADC_FILT1P", PA), ("44", "ADC_FILT1N", PA),
              ("18", "ADC_FILT2P", PA), ("17", "ADC_FILT2N", PA), None, ("1", "ADC_VMID1", PA), ("12", "ADC_VMID2", PA), ("7", "LDO_A_FILT", PA),
              ("32", "LDO_D_FILT", PA)]
    return ic("CS5308P", "CS5308P", "U", "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm",
              "https://statics.cirrus.com/pubs/proDatasheet/CS5308P_DS1314F1.pdf", "C42457798",
              "Cirrus 8-channel 32-bit differential audio ADC, 123 dBA, QFN-48", left, right, top, bottom)


def cs5304p():
    left = []
    for k, (p, n) in enumerate(((40, 39), (42, 41), (46, 45), (48, 47))):
        left += [(str(p), f"IN{k + 1}P", I), (str(n), f"IN{k + 1}N", I)]
    right = [("29", "ASP_BCLK", B), ("24", "ASP_FSYNC", B), ("25", "ASP_DOUT1", O), ("26", "ASP_DOUT2", O), ("27", "ASP_DOUT3", O),
             ("28", "ASP_DOUT4", O), None, ("34", "MCLK", I), ("23", "RESET", I), None, ("36", "SPI_SCK", I), ("35", "SPI_SDO/I2C_SCL", B),
             ("37", "SPI_SDI/I2C_SDA", B), ("38", "SPI_CS", I), None, ("2", "CONFIG1", B), ("3", "CONFIG2/HGC_SCK", B),
             ("4", "CONFIG3/HGC_SDO", B), ("10", "CONFIG4/HGC_CS", B), ("11", "CONFIG5", B)]
    top = [("5", "VDD_A1", P), ("9", "VDD_A2", P), ("31", "VDD_IO", P), ("33", "VDD_D", PA)]
    bottom = [("6", "GND_A", P), ("8", "GND_A", P), ("30", "GND_D", P), ("49", "EP", P), None, ("43", "ADC_FILTP", PA), ("44", "ADC_FILTN", PA),
              ("1", "ADC_VMID", PA), ("7", "LDO_A_FILT", PA), ("32", "LDO_D_FILT", PA), None] + \
             [(str(k), "DNC", NC) for k in (12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22)]
    return ic("CS5304P", "CS5304P", "U", "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm",
              "https://statics.cirrus.com/pubs/proDatasheet/CS5304P_DS1313F1.pdf", "C49192888",
              "Cirrus 4-channel 32-bit differential audio ADC, QFN-48 (pins 12-22 do not connect)", left, right, top, bottom)


def cs4308p():
    left = [("1", "CONFIG5", B), ("48", "CONFIG1", B), ("22", "CONFIG2/DSD_DIN5", B), ("21", "CONFIG3/DSD_DIN6", B), ("23", "CONFIG4", B), None,
            ("9", "ASP_BCLK/DSD_CLK", B), ("10", "ASP_FSYNC", B), ("16", "ASP_DIN1/DSD_DIN1", I), ("15", "ASP_DIN2/DSD_DIN2", I),
            ("14", "ASP_DIN3/DSD_DIN3", I), ("13", "ASP_DIN4/DSD_DIN4", I), None, ("8", "MCLK", I), ("5", "RESET", I), None,
            ("17", "SPI_SCK", I), ("18", "SPI_SDO/I2C_SCL", B), ("19", "SPI_SDI/I2C_SDA", B), ("20", "SPI_CS", I)]
    right = []
    for k, (p, n) in enumerate(((46, 45), (44, 43), (36, 35), (34, 33), (31, 30), (29, 28), (27, 26), (25, 24))):
        right += [(str(p), f"OUT{k + 1}P", O), (str(n), f"OUT{k + 1}N", O)]
    top = [("2", "VDD_A1", P), ("38", "VDD_A2", P), ("11", "VDD_IO", P), ("7", "VDD_D", PA)]
    bottom = [("3", "GND_A", P), ("37", "GND_A", P), ("12", "GND_D", P), ("49", "EP", P), None, ("39", "DAC_FILTP", PA), ("40", "DAC_FILTN", PA),
              ("32", "DAC_VMID", PA), ("4", "LDO_A_FILT", PA), ("6", "LDO_D_FILT", PA), None, ("41", "NC", NC), ("42", "NC", NC), ("47", "NC", NC)]
    return ic("CS4308P", "CS4308P", "U", "Package_DFN_QFN:QFN-48-1EP_6x6mm_P0.4mm_EP4.6x4.6mm",
              "https://statics.cirrus.com/pubs/proDatasheet/CS4308P_DS1317F1.pdf", "none",
              "Cirrus 8-channel 32-bit audio DAC, 123 dBA, current outputs (AN0679 I-V stage), QFN-48", left, right, top, bottom)


XU = {1: "X0D05", 2: "X0D07", 3: "X0D01", 5: "X0D10", 6: "X0D00", 7: "X0D11", 9: "X1D00", 10: "X1D01", 11: "X1D09", 13: "X1D10",
      14: "X1D11", 32: "X1D13", 33: "X1D16", 35: "X1D17", 36: "X1D18", 37: "X1D19", 39: "X1D22", 40: "X0D29", 41: "X0D35", 43: "X0D36",
      44: "X0D37", 45: "X0D38", 46: "X0D40", 47: "X0D39", 48: "X0D42", 50: "X0D41", 51: "X0D43", 53: "X1D34", 54: "X0D30", 55: "X0D31",
      56: "X0D32", 58: "X0D33", 59: "X0D04", 60: "X0D06"}


def xu316():
    ports = [(str(p), n, B) for p, n in sorted(XU.items(), key=lambda t: t[1])]
    half = len(ports) // 2 + 1
    left, right = ports[:half], ports[half:]
    left = left + [None]
    top = [("8", "VDDIOL", P), ("38", "VDDIOR", P), ("52", "VDDIOT", P), ("17", "VDDIOB18", P), ("26", "VDDIOB18", P), ("22", "PLL_AVDD", P),
           ("30", "USB_VDD33", P), ("31", "USB_VDD18", P)]
    bottom = [(str(k), "VDD", P) for k in (4, 12, 19, 27, 34, 42, 49, 57, 61, 62, 63, 64)] + [None, ("65", "VSS", P)]
    right = right + [None, ("28", "USB_DM", B), ("29", "USB_DP", B), None, ("16", "XIN", I), ("15", "XOUT", O), None, ("21", "RST_N", I),
                     ("23", "TMS", I), ("24", "TCK", I), ("18", "TDI", I), ("20", "TDO", O), ("25", "NC", NC)]
    return ic("XU316-1024-QF60B", "XU316-1024-QF60B", "U", "ShtukaDruka:XU316-1024-QF60B_QFN-60_7x7_P0.4",
              "https://www.xmos.com/documentation/XM-015129-PC/html/rst/XU316-1024.html", "C7397517",
              "XMOS xcore.ai XU316, 16 cores, QFN-60 7x7; core 0.9 V, I/O 3.3 V (L/R/T), 1.8 V (bottom: JTAG, crystal), USB 2.0 HS", left, right, top, bottom)


def adum4166():
    left = [("1", "VBUS1", P), ("3", "VDD1", P), ("8", "UD+", B), ("9", "UD-", B), None, ("2", "GND1", P), ("4", "GND1", P), ("5", "GND1", P),
            ("6", "GND1", P), ("7", "GND1", P), ("10", "GND1", P)]
    right = [("20", "VBUS2", P), ("18", "VDD2", P), ("12", "DD+", B), ("13", "DD-", B), None, ("14", "PGOOD", O), ("15", "XO2", O), ("16", "XI2", I),
             None, ("11", "GND2", P), ("17", "GND2", P), ("19", "GND2", P)]
    return ic("ADuM4166", "ADuM4166", "U", "Package_SO:SOIC-20W_7.5x12.8mm_P1.27mm",
              "https://www.analog.com/en/products/adum4166.html", "C5367256",
              "Analog Devices USB 2.0 high-speed isolator (side 1 = computer, side 2 = device), SOIC-20", left, right, [], [])


def adc128s102():
    left = [("1", "CS#", I), ("16", "SCLK", I), ("14", "DIN", I), ("15", "DOUT", O)]
    right = [(str(4 + k), f"IN{k}", I) for k in range(8)]
    top = [("2", "VA", P), ("13", "VD", P)]
    bottom = [("3", "AGND", P), ("12", "DGND", P)]
    return ic("ADC128S102", "ADC128S102", "U", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm",
              "https://www.ti.com/lit/ds/symlink/adc128s102.pdf", "C206503",
              "TI 12-bit 8-channel SPI ADC, 500 ksps to 1 MSPS, 2.7-5.25 V, TSSOP-16", left, right, top, bottom)


def tps2051b():
    left = [("5", "IN", P), ("4", "EN", I)]
    right = [("1", "OUT", O), ("3", "OC", O)]
    return ic("TPS2051B", "TPS2051B", "U", "Package_TO_SOT_SMD:SOT-23-5",
              "https://www.ti.com/lit/ds/symlink/tps2051b.pdf", "C24593",
              "TI current-limited USB power switch, 0.5 A, 2.7-5.5 V, EN active high, OC open drain (DBV pins: 1 OUT, 2 GND, 3 OC, 4 EN, 5 IN)", left, right, [], [("2", "GND", P)])


def bq77915():
    left = [("1", "VDD", P), ("2", "AVDD", PA), ("3", "VC5", I), ("4", "VC4", I), ("5", "VC3", I), ("6", "VC2", I), ("7", "VC1", I), ("8", "VC0", I),
            ("9", "VSS", P), ("10", "SRP", I), ("11", "SRN", I), ("12", "DSG", O)]
    right = [("13", "CHG", O), ("14", "LD", I), ("15", "LPWR", O), ("16", "CBI", I), ("17", "OCDP", I), ("18", "TS", I), ("19", "VTB", O),
             ("20", "CCFG", I), ("21", "CBO", O), ("22", "PRES", I), ("23", "CTRC", I), ("24", "CTRD", I)]
    return ic("BQ77915", "BQ7791500PWR", "U", "Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm",
              "https://www.ti.com/lit/ds/symlink/bq77915.pdf", "C2876946",
              "TI BQ77915 3- to 5-series low-power primary protector (variant 00: 3S, OV 4.2 V), TSSOP-24 (SLUSCU0L table 7-1)", left, right, [], [])


def tps26631():
    left = [("1", "IN", P), ("2", "IN", P), ("5", "IN_SYS", P), ("6", "UVLO", I), ("7", "OVP", I), ("3", "B_GATE", O), ("4", "DRV", O)]
    right = [("17", "OUT", P), ("18", "OUT", P), ("14", "FLT", O), ("16", "PGOOD", O), ("15", "PGTH", I), ("13", "IMON", O),
             ("12", "SHDN", I), ("11", "MODE", I), ("10", "ILIM", PA), ("9", "dVdT", PA)]
    bottom = [("8", "GND", P), ("25", "EP", P)]
    top = [(str(n), "NC", NC) for n in (19, 20, 21, 22, 23, 24)]
    return ic("TPS26631", "TPS26631RGER", "U", "Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.65x2.65mm",
              "https://www.ti.com/lit/ds/symlink/tps2663.pdf", "C1850273",
              "TI TPS26631 4.5-60 V 6 A eFuse, adjustable UVLO/OVP/current limit/slew (SLVSE94G, RGE VQFN-24: IN 1-2, OUT 17-18)", left, right, top, bottom)


def bzt52c3v3():
    left = [("1", "A", PA)]
    right = [("2", "K", PA)]
    return ic("BZT52C3V3", "BZT52C3V3", "D", "Diode_SMD:D_SOD-123", "https://www.diodes.com/assets/Datasheets/ds18010.pdf", "C173413",
              "Zener diode 3.3 V 0.5 W, SOD-123 (pin 1 anode, pin 2 cathode)", left, right, [], [])


def isousb211():
    left = [("1", "VBUS1", P), ("2", "V3P3V1", PA), ("5", "VCC1", P), ("4", "V1P8V1", PA), ("11", "V1P8V1", PA), ("7", "UD-", B), ("8", "UD+", B),
            ("9", "EQ10", I), ("10", "EQ11", I), ("13", "CDPENZ1", I), ("6", "V2OK", O), ("14", "NC", NC)]
    right = [("28", "VBUS2", P), ("27", "V3P3V2", P), ("24", "VCC2", P), ("25", "V1P8V2", P), ("18", "V1P8V2", P), ("22", "DD-", B), ("21", "DD+", B),
             ("19", "EQ21", I), ("20", "EQ20", I), ("16", "CDPENZ2", I), ("23", "V1OK", O), ("15", "NC", NC)]
    bottom = [("3", "GND1", P), ("12", "GND1", P), ("17", "GND2", P), ("26", "GND2", P)]
    return ic("ISOUSB211", "ISOUSB211DPR", "U", "ShtukaDruka:SSOP-28_DP0028A_7.5x10.3mm_P0.65mm",
              "https://www.ti.com/lit/ds/symlink/isousb211.pdf", "C5772877",
              "TI ISOUSB211 isolated USB 2.0 repeater, low/full/high speed, no crystal, 5.7 kVrms, SSOP-28 DP0028A (SLLSFC5D)", left, right, [], bottom)


def lm70660():
    left = [("27", "VIN", P), ("28", "VIN", P), ("29", "VIN", P), ("1", "VIN", P), ("2", "VIN", P), ("3", "VIN", P), ("9", "EN/UVLO", I),
            ("8", "PFM/SYNCIN", I), ("6", "BIAS", PA), ("14", "RT", PA), ("13", "CONFIG", PA)]
    right = [("20", "SW", PA), ("21", "SW", PA), ("22", "SW", PA), ("5", "SW4", PA), ("4", "CBOOT", PA), ("11", "ISNS+", I), ("12", "VOUT", I),
             ("16", "FB", I), ("15", "EXTCOMP", O), ("7", "PG/SYNCOUT", O)]
    bottom = [("17", "AGND", P), ("18", "VDDA", PA), ("19", "VCC", PA), ("23", "PGND", P), ("24", "PGND", P), ("25", "PGND", P), ("26", "PGND", P), ("30", "EP", P)]
    top = [("10", "NC", NC)]
    return ic("LM70660", "LM70660RRXR", "U", "ShtukaDruka:VQFN-29_RRX0029B_6x6_P0.5mm",
              "https://www.ti.com/lit/ds/symlink/lm70660.pdf", "C42328952",
              "TI LM70660 65 V 6 A synchronous buck, PFM/FPWM pin, DRSS, shunt current limit (SNVSCD4, RRX VQFN-29 6x6: pins 1-3 VIN4-6, 4 CBOOT, 5 SW4, 20-22 SW, 23-26 PGND, 27-29 VIN, 30 PGND pad)",
              left, right, top, bottom)


def rgb6028():
    left = [("3", "A", PA)]
    right = [("1", "K1", PA), ("2", "K2", PA), ("4", "K4", PA)]
    return ic("RGB_6028_CA", "GL6028RGB01-B", "D", "ShtukaDruka:LED_RGB_6028_ReverseMount_C51933363_slot31",
              "https://jlcpcb.com/partdetail/C51933363", "C51933363",
              "Reverse-mount RGB 6028, common anode pin 3 (LCSC library symbol of C51933363; colour of K1/K2/K4 not confirmed by a datasheet)", left, right, [], [])


def all_symbols():
    return cs5308p() + cs5304p() + cs4308p() + xu316() + adum4166() + adc128s102() + tps2051b() + bq77915() + tps26631() + bzt52c3v3() + isousb211() + lm70660() + rgb6028()
