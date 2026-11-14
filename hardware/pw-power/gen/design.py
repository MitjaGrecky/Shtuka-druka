"""PW - Power board under the slope (right, next to the battery bay, R109): inputs DC 12-24 V (locking jack on the rear
wall), USB-C Power (PD 20 V / 5 A, R145) and the 4S battery (R40, R59), joined by ideal diodes; the rear On/Off switch;
rails: 19 V for the Mini-ITX (R36: ASRock N100DC-ITX needs 19 V), +5V_PANEL (panel boards and their LEDs), +5V (screen,
R2, USB, logic), +-14 V pre-regulators and quiet +-12 V for the audio boards (TIDA-01458 scheme), +48 V phantom (R118).
Single source of truth for the schematic. Research: docs/ru/34_rear_boards_research.md (section 5), decisions R36, R40,
R59, R72, R109, R118, R145.

Rev 0.1 (14.11.2026, PC) = schematic only. Component values follow the TI datasheet examples (TPS25730 fig. 9-3,
LM5176 fig. 8-1, TPS54560B 8.2, LMR33640 table 9-2, LM5156H table 10-3, TPS7A47 ANY-OUT, PMP40871 for the phantom)
scaled to these rails; every "check" note is to be verified against the datasheet before the board.
Rev 0.2 (14.11.2026, cloud, task #23): checked against the datasheets - TPS25730 VIN_3V3 to GND (VBUS-powered only),
+47 uF on PPHV; LM5176 RMODE to AGND (was to VCC = no hiccup); TPS7A33 thermal pad to GND (was IN) and 10 nF FB-OUT;
LM5156H DITHOFF to VCC (dithering off) and a 100 V FET; boost 48.5 V and phantom 46.1 V (TPS7A4101 input max 50 V).
Rev 0.3 (14.11.2026, PC, R146): INA226 input power monitor on a 5 mOhm shunt after the On/Off switch, I2C cable to P2.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "pw-power"
ID = "PW"
TITLE = "PW - Power: DC / USB-C PD / battery, 19 V Mini-ITX, +5 V x 2, +-12 V quiet, +48 V phantom"
REV = "0.4"
M1_LIB = K.M1_LIB
BUS_NOTE = ("Inputs DC 12-24 V, USB-C PD 15-20 V (TPS25730D), battery 4S 12.8-16.8 V -> ideal diodes (LM74700) -> rear On/Off "
            "switch -> BUS 12-24 V -> 19 V Mini-ITX (LM5176), +5V_PANEL and +5V (TPS54560B), +-14 V (LMR33640) -> "
            "+-12 V (TPS7A47 / TPS7A33), +48 V (LM5156H + TPS7A4101)")
PWR_FLAG_NETS = ("B19_VCC", "B19_VIN", "BAT_F", "BUS", "DC_F", "HV_RAW", "N14", "P14", "PD_OUT", "PD_VBUS", "V19")         # ERC: nets with power inputs and no power output pin (connectors, switch, converters)
NO_PWR_FLAG = ("+3V3",)     # no 3.3 V rail on this board
W, H = 100.0, 80.0          # rough: under the slope on the right next to the battery bay (R109); with the board
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603 = "Resistor_SMD:R_0603_1608Metric"
C1206, C1210 = "Capacitor_SMD:C_1206_3216Metric", "Capacitor_SMD:C_1210_3225Metric"
CP8, CP10 = "Capacitor_SMD:CP_Elec_8x10.5", "Capacitor_SMD:CP_Elec_10x10.5"
R2512, R1206 = "Resistor_SMD:R_2512_6332Metric", "Resistor_SMD:R_1206_3216Metric"
SMA, SMB, SMC, SOD123F, SOD123 = ("Diode_SMD:D_SMA", "Diode_SMD:D_SMB", "Diode_SMD:D_SMC", "Diode_SMD:D_SOD-123F",
                                  "Diode_SMD:D_SOD-123")
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"
FET = ("Transistor_FET:CSD18540Q5B", "Package_TO_SOT_SMD:TDSON-8-1")   # 60 V 1.8 mOhm, pins 1-3 S, 4 G, 5 D


def parts():
    P = []
    n = {"R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Q": 0, "L": 0, "F": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def R(value, a, b, fp=R0402, **f):
        add(ref("R"), "Device:R", value, fp, {"1": a, "2": b}, **f)

    def C(value, a, b="GND", fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, **f)

    def CP(value, plus, minus="GND", fp=CP8, **f):
        add(ref("C"), "Device:C_Polarized", value, fp, {"1": plus, "2": minus}, **f)

    def fet(g, s, d, **f):
        add(ref("Q"), FET[0], "CSD18540Q5B", FET[1], {"1": s, "2": s, "3": s, "4": g, "5": d}, LCSC="C86513", **f)

    def ideal_diode(name, anode, cathode):
        u = ref("U")
        add(u, "Power_Management:LM74700", "LM74700-Q1", "Package_TO_SOT_SMD:SOT-23-6",
            {"1": f"{name}_VCAP", "2": "GND", "3": anode, "4": cathode, "5": f"{name}_GATE", "6": anode},
            LCSC="C2941042", Note=f"ideal diode {name}: reverse polarity and ORing (EN tied to ANODE = always on)")
        C("100n 25V", f"{name}_VCAP", anode, fp=C0603, Note="VCAP to ANODE (charge pump)")
        fet(f"{name}_GATE", anode, cathode, Note="ideal-diode FET: source = input, drain = BUS_IN")

    # ---------------------------------------------------------------- inputs
    add(ref("J"), "Connector_Generic:Conn_01x02", "DC in", MF.format("43650-0215_1x02"), {"1": "DC_RAW", "2": "GND"},
        Note="cable from the locking DC jack on the rear wall (R141; Kycon KLDHCX-0202-BC-1, 5 A 24 V)")
    add(ref("F"), "Device:Fuse", "7A", "Fuse:Fuse_2920_7451Metric", {"1": "DC_RAW", "2": "DC_F"}, Note="resettable fuse, 7 A hold - check")
    add(ref("D"), "Device:D_TVS", "SMBJ28CA", SMB, {"1": "DC_F", "2": "GND"}, LCSC="C132572", Note="DC input surge, 28 V standoff (R72)")
    ideal_diode("IDC", "DC_F", "BUS_IN")

    add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", "USB-C Power in", MF.format("43045-0612_2x03"),
        {"1": "PD_VBUS", "2": "PD_VBUS", "3": "GND", "4": "GND", "5": "PD_CC1", "6": "PD_CC2"},
        Note="cable from the USB-C Power receptacle on the rear wall (R145): VBUS x 2, GND x 2, CC1, CC2; 5 A rated USB-C")
    add(ref("D"), "Device:D_TVS", "SMBJ22CA", SMB, {"1": "PD_VBUS", "2": "GND"}, LCSC="C127561", Note="VBUS surge, 22 V standoff")
    u = ref("U")
    add(u, "Interface_USB:TPS25730D", "TPS25730D", "Package_DFN_QFN:Texas_REF0038A_WQFN-38-2EP_6x4mm_P0.4",
        {"1": "PD_LDO3V3", "2": "PD_ADCIN1", "3": "PD_LDO3V3", "4": "PD_LDO1V5", "5": "PD_ADCIN34", "6": None,
         "7": "PD_ADCIN34", "8": "GND", "9": "GND", "10": None, "11": "GND", "12": "GND", "13": None, "14": "GND",
         "15": "PD_DRAIN", "16": "GND", "17": "GND", "18": "PD_FAULT", "19": None, "20": "PD_OUT", "23": "PD_VBUS",
         "26": "PD_RSV26", "27": "PD_RSV27", "28": "PD_CC1", "29": "PD_CC2", "30": "PD_DRAIN", "31": "GND", "32": "PD_VBUS",
         "34": "GND", "36": "PD_RSV36", "37": None, "38": "GND", "39": "GND", "40": "PD_DRAIN"},
        LCSC="C22438973", Note="USB PD sink without I2C (I2Ct_SDA/SCL grounded: allowed if unused): ADCIN1 = 3 (min 15 V), "
        "ADCIN2 = 7 (max 20 V), ADCIN3 = 3 (operating 3 A), ADCIN4 = 3 (max 5 A); VIN_3V3 to GND = powered from VBUS only")
    R("42.2k", "PD_LDO3V3", "PD_ADCIN1", Note="ADCIN1 divider 0.19 -> decoded 3 = 15 V minimum")
    R("10k", "PD_ADCIN1", "GND")
    R("42.2k", "PD_LDO3V3", "PD_ADCIN34", Note="ADCIN3 = ADCIN4 = 3: 3 A operating, 5 A maximum")
    R("10k", "PD_ADCIN34", "GND")
    R("10k", "PD_FAULT", "PD_LDO3V3", Note="FAULT_IN high = keep the connection")
    for rsv in ("PD_RSV26", "PD_RSV27", "PD_RSV36"):
        R("10k", rsv, "GND", Note="RESERVED: tie to GND or LDO_3V3")
    C("10u", "PD_LDO3V3", fp=C0805, Note="C_LDO_3V3 5-25 uF")
    C("4.7u", "PD_LDO1V5", fp=C0603, Note="C_LDO_1V5 4.5-12 uF")
    C("4.7u 25V", "PD_VBUS", fp=C0805, Note="C_VBUS 1-10 uF")
    C("10n 50V", "PD_VBUS", fp=C0603)
    C("330p", "PD_CC1", Note="C_CC 200-480 pF")
    C("330p", "PD_CC2")
    for _ in range(2):
        C("22u 25V", "PD_OUT", fp=C1210, Note="C_PPHV 47-100 uF in total")
    C("10u 25V", "PD_OUT", fp=C1210)
    CP("47u 35V", "PD_OUT", fp=CP8, Note="C_PPHV 47-100 uF: the 25 V ceramics lose most of their value at 20 V")
    ideal_diode("IPD", "PD_OUT", "BUS_IN")

    add(ref("J"), "Connector_Generic:Conn_02x02_Odd_Even", "Battery", MF.format("43045-0412_2x02"),
        {"1": "BAT_RAW", "2": "BAT_RAW", "3": "GND", "4": "GND"},
        Note="removable 4S2P pack with its own BMS (R109), 12.8-16.8 V; charger later (R40)")
    add(ref("F"), "Device:Fuse", "10A", "Fuse:Fuse_2920_7451Metric", {"1": "BAT_RAW", "2": "BAT_F"}, Note="check rating")
    add(ref("D"), "Device:D_TVS", "SMBJ20CA", SMB, {"1": "BAT_F", "2": "GND"}, LCSC="C127559")
    ideal_diode("IBAT", "BAT_F", "BUS_IN")

    # ---------------------------------------------------------------- On/Off switch and BUS
    add(ref("J"), "Connector_Generic:Conn_01x02", "On/Off switch", MF.format("43650-0215_1x02"), {"1": "BUS_IN", "2": "BUS_SW"},
        Note="mechanical On/Off on the rear wall (model): rocker rated 10 A DC or more in series with the bus")
    # input power monitor (R146): everything the instrument draws passes the shunt; P2 reads it and caps the LEDs
    R("5m", "BUS_SW", "BUS", fp=R2512, Note="shunt 5 mOhm 1 % 3 W: 8 A -> 40 mV (INA226 range 81.9 mV)")
    u = ref("U")
    add(u, "Sensor_Energy:INA226", "INA226", "Package_SO:VSSOP-10_3x3mm_P0.5mm",
        {"1": "GND", "2": "GND", "3": "PM_ALERT", "4": "PM_SDA", "5": "PM_SCL", "6": "+3V3", "7": "GND", "8": "BUS",
         "9": "PM_INN", "10": "PM_INP"}, LCSC="C49851",
        Note="R146: input power monitor, I2C address 0x40 (A0 = A1 = GND), powered from +3V3; BUS voltage up to 36 V")
    R("10", "BUS_SW", "PM_INP", fp=R0603, Note="shunt sense filter")
    R("10", "BUS", "PM_INN", fp=R0603)
    C("100n 50V", "PM_INP", "PM_INN", fp=C0603)
    C("100n", "+3V3", fp=C0603)
    # INA226 VIH = 0.7 x VS (3.5 V at 5 V) is above a 3.3 V pull-up level: the monitor runs from its own 3.3 V (review 14.11.2026)
    add(ref("U"), "Regulator_Linear:AP2112K-3.3", "AP2112K-3.3", "Package_TO_SOT_SMD:SOT-23-5",
        {"1": "+5V", "2": "GND", "3": "+5V", "4": None, "5": "+3V3"}, LCSC="C51118",
        Note="3.3 V for the INA226 only (VIH = 0.7 x VS); the same level as the pull-ups on P2")
    C("1u", "+5V", fp=C0603)
    C("1u", "+3V3", fp=C0603)
    add(ref("J"), "Connector_Generic:Conn_01x04", "I2C power monitor", PH.format(n=4),
        {"1": "PM_SDA", "2": "PM_SCL", "3": "PM_ALERT", "4": "GND"},
        Note="to the panel hub P2, which drives the LEDs (R146): pull-ups to 3.3 V on P2; ALERT open drain = over-limit")
    CP("100u 35V", "BUS", fp=CP10, Note="bulk")
    for _ in range(2):
        C("10u 50V", "BUS", fp=C1210)

    # ---------------------------------------------------------------- 19 V for the Mini-ITX: LM5176 four-switch buck-boost
    u = ref("U")
    add(u, "Regulator_Switching:LM5176PWP", "LM5176", "Package_SO:HTSSOP-28-1EP_4.4x9.7mm_P0.65mm_EP3.4x9.5mm_ThermalVias",
        {"1": "B19_UVLO", "2": "B19_VIN", "3": "B19_VIN", "4": "B19_MODE", "5": "GND", "6": "B19_RT", "7": "B19_SLOPE",
         "8": "B19_SS", "9": "B19_COMP", "10": "GND", "11": "B19_FB", "12": "V19", "13": "V19", "14": "V19",
         "15": "GND", "16": "B19_CS", "17": "B19_PG", "18": "B19_SW2", "19": "B19_HDRV2", "20": "B19_BOOT2",
         "21": "B19_LDRV2", "22": "GND", "23": "B19_VCC", "24": "V19", "25": "B19_LDRV1", "26": "B19_BOOT1",
         "27": "B19_HDRV1", "28": "B19_SW1", "29": "GND"},
        LCSC="C442493", Note="12-24 V -> 19 V 5 A (95 W), 300 kHz; values after fig. 8-1 (6-50 V -> 12 V 6 A); ISNS+/- "
        "shorted = average current loop off; DITH to AGND = no dithering; BIAS from VOUT (8-36 V)")
    R("10", "BUS", "B19_VIN", fp=R0603, Note="VIN filter")
    C("1u 50V", "B19_VIN", fp=C0805)
    R("249k", "BUS", "B19_UVLO", Note="UVLO: start ~ 10 V")
    R("34.8k", "B19_UVLO", "GND")
    R("93.1k", "B19_MODE", "GND", Note="RMODE to AGND: 1.38-2.22 V = CCM, hiccup enabled (datasheet; to VCC = no hiccup)")
    R("27.4k", "B19_RT", "GND", Note="300 kHz")
    C("220p", "B19_SLOPE", Note="CSLOPE = L gm / (Rs Acs) = 4.7u x 2u / (8m x 5) = 235 pF")
    C("100n", "B19_SS")
    R("10k", "B19_COMP", "B19_CMP_RC", Note="Rc1 as fig. 8-1 (12 V 6 A); loop to be measured on the board")
    C("33n", "B19_CMP_RC", Note="Cc1 as fig. 8-1")
    C("560p", "B19_COMP", Note="Cc2 as fig. 8-1")
    R("453k", "V19", "B19_FB", Note="FB: 0.8 V x (1 + 453k / 20k) = 18.9 V")
    R("20k", "B19_FB", "GND")
    C("1u 25V", "B19_VCC", fp=C0603, Note="1-4.7 uF, 16 V or more")
    C("100n 50V", "B19_BOOT1", "B19_SW1", fp=C0603)
    C("100n 50V", "B19_BOOT2", "B19_SW2", fp=C0603)
    R("10k", "B19_PG", "B19_VCC")
    fet("B19_HDRV1", "B19_SW1", "BUS", Note="QH1")
    fet("B19_LDRV1", "B19_CSN", "B19_SW1", Note="QL1")
    fet("B19_HDRV2", "B19_SW2", "V19", Note="QH2")
    fet("B19_LDRV2", "B19_CSN", "B19_SW2", Note="QL2")
    R("8m", "B19_CSN", "GND", fp=R2512, Note="Rsense 8 mOhm: buck <= 80 mV / 5 A = 16 mOhm; boost limit 100-140 mV / 8 mOhm "
      "= 12.5-17.5 A > 9.9 A peak at 12 V in; ~0.6 W at 12 V")
    R("100", "B19_CSN", "B19_CS", fp=R0603, Note="CS filter")
    C("47p", "B19_CS", Note="CS filter")
    add(ref("L"), "Device:L", "4.7uH", "Inductor_SMD:L_Bourns_SRP1245A", {"1": "B19_SW1", "2": "B19_SW2"},
        Note="4.7 uH, Isat >= 18 A (above the highest current limit 140 mV / 8 mOhm = 17.5 A); part to choose")
    for _ in range(4):
        C("4.7u 50V", "BUS", fp=C1210, Note="input ceramic")
    for _ in range(4):
        C("10u 35V", "V19", fp=C1210, Note="output ceramic")
    for _ in range(2):
        CP("100u 35V", "V19", fp=CP8, Note="output polymer")
    add(ref("J"), "Connector_Generic:Conn_02x02_Odd_Even", "19 V to Mini-ITX", MF.format("43045-0412_2x02"),
        {"1": "V19", "2": "V19", "3": "GND", "4": "GND"}, Note="cable to the DC jack of the ASRock N100DC-ITX (5.5 x 2.5 plug)")

    # ---------------------------------------------------------------- +5 V x 2: TPS54560B, 5 A each
    def buck5(net, note):
        u5 = ref("U")
        p = net.replace("+", "P").replace("_", "")
        add(u5, "Regulator_Switching:TPS54560BDDA", "TPS54560B", "Package_SO:Texas_R-PDSO-G8_EP2.95x4.9mm_Mask2.4x3.1mm_ThermalVias",
            {"1": f"{p}_BOOT", "2": "BUS", "3": f"{p}_EN", "4": f"{p}_RT", "5": f"{p}_FB", "6": f"{p}_COMP", "7": "GND",
             "8": f"{p}_SW", "9": "GND"},
            LCSC="C1850354", Note=f"{note}; BUS -> 5 V 5 A, 400 kHz; values = datasheet example 8.2 (RT, EN, compensation, B560C)")
        R("442k", "BUS", f"{p}_EN", Note="UVLO start 6.5 V (datasheet example)")
        R("90.9k", f"{p}_EN", "GND")
        R("243k", f"{p}_RT", "GND", Note="RT = 101756 x 400^-1.008 = 242k: 400 kHz")
        R("53.6k", net, f"{p}_FB", Note="0.8 V x (1 + 53.6k / 10.2k) = 5.0 V")
        R("10.2k", f"{p}_FB", "GND")
        R("16.9k", f"{p}_COMP", f"{p}_CRC")
        C("4.7n", f"{p}_CRC")
        C("47p", f"{p}_COMP")
        C("100n 25V", f"{p}_BOOT", f"{p}_SW", fp=C0603)
        add(ref("D"), "Device:D_Schottky", "B560C", SMC, {"1": f"{p}_SW", "2": "GND"}, LCSC="C85100", Note="catch diode 60 V 5 A (example)")
        add(ref("L"), "Device:L", "8.2uH", "Inductor_SMD:L_Bourns_SRP1038C_10.0x10.0mm", {"1": f"{p}_SW", "2": net},
            Note="8.2 uH, Isat >= 8 A (example: 7.2 uH WE 7447798720, Isat 7.9 A)")
        for _ in range(4):
            C("2.2u 50V", "BUS", fp=C1206, Note="input")
        for _ in range(3):
            C("47u 10V", net, fp=C1210, Note="output")

    buck5("+5V_PANEL", "panel boards: logic and LEDs (LED budget doc 10: up to ~5.6 A white on full - firmware limits brightness)")
    buck5("+5V", "screen (5 V / 4 W, R110), R2, USB devices, logic")

    # ---------------------------------------------------------------- +-14 V from 19 V: LMR33640 buck and inverting buck-boost
    u = ref("U")
    add(u, "Regulator_Switching:LMR33640ADDA", "LMR33640", "Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias",
        {"1": "GND", "2": "V19", "3": "V19", "4": None, "5": "P14_FB", "6": "P14_VCC", "7": "P14_BOOT", "8": "P14_SW", "9": "GND"},
        LCSC="C2836966", Note="19 V -> +14 V, 400 kHz (table 9-2 scaled)")
    R("100k", "P14", "P14_FB", Note="1.0 V x (1 + 100k / 7.68k) = 14.0 V")
    R("7.68k", "P14_FB", "GND")
    C("100n 25V", "P14_BOOT", "P14_SW", fp=C0603)
    C("1u", "P14_VCC", fp=C0603)
    C("10u 50V", "V19", fp=C1210)
    C("220n 50V", "V19", fp=C0603)
    add(ref("L"), "Device:L", "10uH", "Inductor_SMD:L_Bourns_SRN6045TA", {"1": "P14_SW", "2": "P14"}, Note="10 uH, Isat >= 2 A - check")
    for _ in range(3):
        C("22u 25V", "P14", fp=C1210)

    u = ref("U")
    add(u, "Regulator_Switching:LMR33640ADDA", "LMR33640", "Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias",
        {"1": "N14", "2": "V19", "3": "V19", "4": None, "5": "N14_FB", "6": "N14_VCC", "7": "N14_BOOT", "8": "N14_SW", "9": "N14"},
        LCSC="C2836966", Note="inverting buck-boost 19 V -> -14 V: IC ground = -14 V, inductor to system GND; VIN to IC ground "
        "= 33 V of 36 V (8 % margin: see report #23); EN on VIN (EN may go up to VIN)")
    R("100k", "GND", "N14_FB", Note="FB is referred to the IC ground (-14 V): 1.0 V x (1 + 100k / 7.68k) = 14 V")
    R("7.68k", "N14_FB", "N14")
    C("100n 25V", "N14_BOOT", "N14_SW", fp=C0603)
    C("1u", "N14_VCC", "N14", fp=C0603)
    C("10u 50V", "V19", "N14", fp=C1210, Note="input cap VIN to IC ground")
    C("10u 50V", "V19", fp=C1210)
    add(ref("L"), "Device:L", "10uH", "Inductor_SMD:L_Bourns_SRN6045TA", {"1": "N14_SW", "2": "GND"}, Note="10 uH, Isat >= 3 A - check")
    for _ in range(3):
        C("22u 25V", "GND", "N14", fp=C1210, Note="output: GND to -14 V")

    # ---------------------------------------------------------------- quiet +-12 V: TPS7A4701 / TPS7A3301 (TIDA-01458)
    u = ref("U")
    add(u, "Regulator_Linear:TPS7A4701xRGW", "TPS7A4701", "Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias",
        {"1": "+12V", "3": "+12V", "4": "GND", "5": None, "6": "GND", "7": "GND", "8": None, "9": "GND", "10": None,
         "11": "GND", "12": None, "13": "P14", "14": "P12_NR", "15": "P14", "16": "P14", "20": "+12V", "21": "GND"},
        LCSC="C90084", Note="ANY-OUT: 1.4 V + 6.4 + 3.2 + 0.8 + 0.2 (pins 4, 6, 9, 11 to GND) = 12.0 V; 4 uV rms")
    C("1u", "P12_NR", fp=C0603, Note="NR - check value")
    C("10u 25V", "P14", fp=C1210)
    C("10u 25V", "+12V", fp=C1210)
    u = ref("U")
    add(u, "Regulator_Linear:TPS7A3301RGW", "TPS7A3301", "Package_DFN_QFN:Texas_RGW0020A_VQFN-20-1EP_5x5mm_P0.65mm_EP3.15x3.15mm_ThermalVias",
        {"1": "-12V", "3": "N12_FB", "7": "GND", "13": "N14", "14": "N12_NR", "15": "N14", "16": "N14", "20": "-12V", "21": "GND"},
        LCSC="C90082", Note="-12 V = -1.176 V x (1 + 102k / 11k) = -12.1 V; EN tied to IN (allowed: |EN| <= |IN|); "
        "thermal pad to GND (datasheet: large ground plane)")
    R("102k", "-12V", "N12_FB")
    R("11k", "N12_FB", "GND")
    C("1u", "N12_NR", fp=C0603, Note="NR/SS 1 uF (datasheet)")
    C("10n", "-12V", "N12_FB", Note="10 nF FB to OUT (datasheet)")
    C("10u 25V", "GND", "N14", fp=C1210)
    C("47u 25V", "GND", "-12V", fp=C1210, Note="OUT >= 10 uF required, 47 uF recommended")

    # ---------------------------------------------------------------- +48 V phantom: LM5156H boost + TPS7A4101 (R118)
    u = ref("U")
    add(u, "Regulator_Switching:LM5156HPWP", "LM5156H", "Package_SO:Texas_HTSSOP-14-1EP_4.4x5mm_P0.65mm_EP3.4x5mm_Mask3.155x3.255mm_ThermalVias",
        {"1": "V19", "2": None, "3": "HV_VCC", "4": "HV_GATE", "5": "GND", "6": "GND", "7": "HV_CS", "8": "HV_COMP",
         "9": "HV_VCC", "10": "HV_FB", "11": "HV_SS", "12": "HV_RT", "13": None, "14": "HV_UVLO", "15": "GND"},
        LCSC="C2867852", Note="19 V -> 48.5 V, ~40 mA for two P48 channels (doc 34, 2.3); DITHOFF to VCC = spread spectrum off "
        "(to AGND it is on); fsw = 2.21e10 / (RT + 955) = 435 kHz; VREF 1.0 V; current limit 93-107 mV")
    R("100k", "V19", "HV_UVLO")
    R("27k", "HV_UVLO", "GND")
    C("1u 25V", "HV_VCC", fp=C0603, Note="VCC 1-4.7 uF")
    R("49.9k", "HV_RT", "GND", Note="435 kHz (as table 10-3)")
    C("47n", "HV_SS")
    R("10k", "HV_COMP", "HV_CRC", Note="compensation near table 10-3 (11.3k / 22n / 220p); light load, DCM: measure on the board")
    C("22n", "HV_CRC")
    C("470p", "HV_COMP")
    R("475k", "HV_RAW", "HV_FB", Note="1.0 V x (1 + 475k / 10k) = 48.5 V: margin to the TPS7A4101 input limit of 50 V")
    R("10k", "HV_FB", "GND")
    add(ref("L"), "Device:L", "22uH", "Inductor_SMD:L_Bourns_SRN6045TA", {"1": "V19", "2": "HV_SW"}, Note="22 uH 1 A")
    add(ref("Q"), "Transistor_FET:IRLML2060", "IRLML0100", "Package_TO_SOT_SMD:SOT-23", {"1": "HV_GATE", "2": "HV_CSN", "3": "HV_SW"},
        LCSC="C53658", Note="IRLML0100TRPBF 100 V 1.6 A 220 mOhm (switch node ~49 V: a 60 V part had too little margin); IRLML2060 symbol = same SOT-23 G/S/D")
    R("0.1", "HV_CSN", "GND", fp=R0603, Note="current limit 93-107 mV / 0.1 = 0.93-1.07 A; peak ~0.7 A at 40 mA out (DCM)")
    R("100", "HV_CSN", "HV_CS", Note="CS filter")
    add(ref("D"), "Device:D_Schottky", "SS1H10", SMA, {"1": "HV_RAW", "2": "HV_SW"}, LCSC="C3151624", Note="100 V 1 A")
    for _ in range(2):
        C("4.7u 100V", "HV_RAW", fp=C1210)
    u = ref("U")
    add(u, "Regulator_Linear:TPS7A4101DGN", "TPS7A4101", "Package_SO:Texas_DGN0008B_VSSOP-8-1EP_3x3mm_P0.65mm_EP2x3mm_Mask1.88x1.98mm_ThermalVias",
        {"1": "+48V", "2": "P48_FB", "3": None, "4": "GND", "5": "HV_RAW", "6": None, "7": None, "8": "HV_RAW", "9": "GND"},
        LCSC="C111739", Note="48.5 V -> 46.1 V (P48 44-52 V); input 7-50 V, dropout <= 1.3 V at 50 mA; current limit "
        "51-200 mA for shorted mic lines (doc 34, 2.3)")
    R("383k", "+48V", "P48_FB", Note="1.173 V x (1 + 383k / 10k) = 46.1 V")
    R("10k", "P48_FB", "GND")
    C("1u 100V", "HV_RAW", fp=C1206)
    C("4.7u 100V", "+48V", fp=C1210)

    # ---------------------------------------------------------------- outputs to the boards
    add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", "+5V panel", MF.format("43045-0612_2x03"),
        {"1": "+5V_PANEL", "2": "+5V_PANEL", "3": "+5V_PANEL", "4": "GND", "5": "GND", "6": "GND"},
        Note="to the panel hub P2 (panel boards and LEDs)")
    add(ref("J"), "Connector_Generic:Conn_01x05", "to R2", PH.format(n=5),
        {"1": "+12V", "2": "GND", "3": "-12V", "4": "GND", "5": "+5V"}, Note="same pinout as R2 J1")
    add(ref("J"), "Connector_Generic:Conn_02x05_Odd_Even", "to A1/R1", MF.format("43045-1012_2x05"),
        {"1": "+12V", "2": "GND", "3": "-12V", "4": "GND", "5": "+5V", "6": "GND", "7": "+48V", "8": "GND", "9": "+5V", "10": "GND"},
        Note="audio boards: +-12 V quiet, +5 V digital (their own 3.3 V LDOs), +48 V phantom")
    add(ref("J"), "Connector_Generic:Conn_01x03", "to F1", PH.format(n=3), {"1": "+12V", "2": "GND", "3": "-12V"},
        Note="headphone amplifiers")
    add(ref("J"), "Connector_Generic:Conn_01x02", "+5V screen", PH.format(n=2), {"1": "+5V", "2": "GND"},
        Note="Waveshare 10.1DP-CAPLCD, 5 V / 4 W (R110)")
    R("2.2k", "+5V", "LED_K", Note="power LED")
    add(ref("D"), "Device:LED", "green", "LED_SMD:LED_0603_1608Metric", {"2": "LED_K", "1": "GND"})
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
