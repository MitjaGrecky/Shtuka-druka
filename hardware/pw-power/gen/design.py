"""PW - Power board under the slope (right, next to the battery bay, R109): input (DC removed, R205) was DC 12-24 V (locking jack on the rear
wall), USB-C Power (PD 20 V / 5 A, R145) and the 3S batteries (R40, R59; rev 1.0), joined by ideal diodes; the rear On/Off switch;
rails: 15 V for the ODROID-H5 (R149, P106; H5 window 11-20 V) from the internal 19 V rail, +5V_PANEL (panel boards and their LEDs), +5V (screen,
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
Rev 0.9 (18.11.2026, engineer's audit): charge enable only with the switch on and P2 alive (CE pulled up, two series 2N7002: gate 1 = CHG_EN from P2,
gate 2 = +3V3 behind the switch); hardware 45 C cut-off by the BQ25798 itself (TS divider RT1 only, T5 = 45 C). Doc 43.
Rev 0.8 (18.11.2026, R183): two 4S battery inputs, each with its own BQ25798 charger (charger-only, system stays on the
ideal-diode bus), NTC per pack, I2C mux, 12 V fan stage + PWM/tach to P2. Doc 43.
Rev 1.0 (18.11.2026, engineer, R186, P111, doc 43 5c): packs 3S (3 x Jauch LP906090JH, Digikey in stock) instead of 4S: PROG 10.5k = 3S / 1.5 MHz
(POR VREG 12.6 V, ICHG 1 A, VSYSMIN 9 V), pack TVS SMBJ13CA (SMBJ20CA clamped above the 20 V BAT limit), bus 9-12.6 V from the packs, LM5176
UVLO start 10.1 V / stop 9.3 V (was 9.45 / 8.7 V; boost mode from 9.3 V in); 15 V / 12 V fan / 5 V stages unchanged (fed from the 19 V rail or from a BUS >= 8.7 V).
The pack BMS is a separate small board in each pack (BQ7791500, doc 43 5c); the PW 45 C hardware charge stop and the charge-only-with-switch-on gate stay.
Rev 1.1 (18.11.2026, schematic audit notes/reviews/schematics_2026-11-18.md): EXT and PD TVS SMBJ24CA / SMBJ22CA -> SMBJ20CA (BQ25798 VBUS 30 V abs. max / 24 V
recommended, TPS25730 VBUS 28 V abs. max); DC adapter is 12-20 V. Values and nets unchanged otherwise (same placement).
Rev 1.2 (19.11.2026, purchase_plan.md): all 60 V FETs CSD18540Q5B (C86513) -> CSD18532Q5B (C882766): R_DS 2.5 mOhm at 10 V instead of 1.8; LM5176 at 9.3 V in / 95 W: about +0.25 W in the four FETs (about 1.3 W total, DFN pads), ORing LM74700: drop 27 mV at 11 A (the chip regulates 20 mV, then the FET is fully on). Pack TVS SMBJ13CA C132568 -> C224008 (stock). L4, L5 stay Bourns SRP1038CC-8R2M. Rev 1.2 also (rear wall harness check): DC fuse 7 A -> 5 A (jack 721A 5 A); On/Off switch connector 1x2 -> Micro-Fit 2x2 (10.2 A peak split over two contacts per side). Rev 1.2 also (audit A-025): DC input eFuse TPS26631 (OVP 22.9 V) between DC_F and the ideal diode IDC; EXT stays below the 24 V recommended / 30 V absolute maximum of the chargers.
Rev 2.7 (26.11.2026, decision P): board 100 x 80 (was 100 x 100: it hit R2 in the case), parts on both sides (placement()).
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "pw-power"
ID = "PW"
TITLE = "PW - Power: DC / USB-C PD / battery, 15 V ODROID-H5, 19 V internal, +5 V x 2, +-12 V quiet, +48 V phantom"
REV = "2.7"
M1_LIB = K.M1_LIB
BUS_NOTE = ("Input USB-C PD 15-20 V (TPS25730D, also a MacBook charger; the DC input is removed, R205) -> EXT; EXT and two 3S packs (each with its own BQ25798 charger from EXT) -> ideal diodes (LM74700) -> rear On/Off "
            "switch -> BUS 9-24 V (packs 9-12.6 V) -> 19 V internal rail (LM5176) -> 15 V H5 (LMR33640), +5V_PANEL and +5V (TPS54560B), +-14 V (LMR33640) -> "
            "+-12 V (TPS7A47 / TPS7A33), +48 V (LM5156H + TPS7A4101)")
PWR_FLAG_NETS = ("B19_VCC", "B19_VIN", "BAT1_F", "BAT2_F", "BUS", "EXT", "HV_RAW", "N14", "P14", "PD_OUT", "PD_VBUS", "PD_VBUSF", "V12F", "V19")         # ERC: nets with power inputs and no power output pin (connectors, switch, converters)
NO_PWR_FLAG = ("+3V3",)     # no 3.3 V rail on this board
W, H = 100.0, float(os.environ.get("PW_H", "80.0"))         # rough: under the slope on the right next to the battery bay (R109); with the board
HOLES = [(4.0, 4.0), (96.0, 4.0), (4.0, H - 4.0), (96.0, H - 4.0)]   # M3, board coordinates (KiCad, y down); 15.11.2026
LAYERS = 4

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603 = "Resistor_SMD:R_0603_1608Metric"
R0805 = "Resistor_SMD:R_0805_2012Metric"
C1206, C1210 = "Capacitor_SMD:C_1206_3216Metric", "Capacitor_SMD:C_1210_3225Metric"
CP8, CP10 = "Capacitor_SMD:CP_Elec_8x10.5", "Capacitor_SMD:CP_Elec_10x10.5"
R2512, R1206 = "Resistor_SMD:R_2512_6332Metric", "Resistor_SMD:R_1206_3216Metric"
WIRE1 = "Connector_Wire:SolderWire-1sqmm_1x02_P5.4mm_D1.4mm_OD2.7mm"   # P151: wire loop for the pack current (measurement point)
SMA, SMB, SMC, SOD123F, SOD123 = ("Diode_SMD:D_SMA", "Diode_SMD:D_SMB", "Diode_SMD:D_SMC", "Diode_SMD:D_SOD-123F",
                                  "Diode_SMD:D_SOD-123")
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"
FET = ("Transistor_FET:CSD18540Q5B", "Package_TO_SOT_SMD:TDSON-8-1")   # CSD18532Q5B since rev 1.2 (2.5 mOhm at 10 V), pins 1-3 S, 4 G, 5 D


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Q": 0, "L": 0, "F": 0, "TP": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    def R(value, a, b, fp=R0402, **f):
        add(ref("R"), "Device:R", value, fp, {"1": a, "2": b}, **f)

    def C(value, a, b="GND", fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, **f)

    def CP(value, plus, minus="GND", fp=CP8, **f):
        add(ref("C"), "Device:C_Polarized", value, fp, {"1": plus, "2": minus}, **f)

    def fet(g, s, d, **f):
        add(ref("Q"), FET[0], "CSD18532Q5B", FET[1], {"1": s, "2": s, "3": s, "4": g, "5": d}, LCSC="C882766", **f)

    def ideal_diode(name, anode, cathode):
        u = ref("U")
        add(u, "Power_Management:LM74700", "LM74700-Q1", "Package_TO_SOT_SMD:SOT-23-6",
            {"1": f"{name}_VCAP", "2": "GND", "3": anode, "4": cathode, "5": f"{name}_GATE", "6": anode},
            LCSC="C2941042", Note=f"ideal diode {name}: reverse polarity and ORing (EN tied to ANODE = always on)")
        C("100n 25V", f"{name}_VCAP", anode, fp=C0603, Note="VCAP to ANODE (charge pump)")
        fet(f"{name}_GATE", anode, cathode, Note="ideal-diode FET: source = input, drain = output node")

    def charger(k, bat):
        """BQ25798 (TI SLUSDV2C fig. 8-1: single input, no ship FET), 3S, 1.5 MHz / 1 uH: the pack on BAT, the system pin SYS only
        has its capacitors (charger-only use; the instrument is fed by the ideal diodes). Host: I2C through the mux, INT wired-AND."""
        c = f"CH{k}"
        u = ref("U")
        add(u, "Battery_Management:BQ25798", "BQ25798", "Package_DFN_QFN:Texas_RQM0029A_VQFN-29_4x4mm_P0.4mm",
            {"1": f"{c}_STAT", "2": "EXT", "3": "EXT", "4": f"{c}_BTST1", "5": f"{c}_REGN", "6": None, "7": None, "8": "EXT", "9": "EXT",
             "10": "GND", "11": "GND", "12": None, "13": f"{c}_CE", "14": f"{c}_SCL", "15": f"{c}_SDA", "16": f"{c}_TS",
             "17": f"{c}_ILIM", "18": f"{c}_BATP", "19": f"{c}_BTST2", "20": f"{c}_PROG", "21": "CHG_INT", "22": bat, "23": bat,
             "24": f"{c}_SDRV", "25": f"{c}_SYS", "26": f"{c}_SW2", "27": "GND", "28": f"{c}_SW1", "29": f"{c}_PMID"},
            LCSC="C2876593", Note=f"charger {k}: 1-4 cell buck-boost, I2C 0x6B behind the mux; PROG 10.5k = 3S / 1.5 MHz (POR VREG 12.6 V, "
            "ICHG 1 A, VSYSMIN 9 V; the host sets VREG 12.45 V = 4.15 V per cell under the BMS OV 4.20 V, doc 43 5c); no ACFET/RBFET (ACDRV1/2 to GND, VAC1/2 to VBUS); QON open; D+/D- open")
        add(ref("L"), "Device:L", "1uH", "Inductor_SMD:L_Bourns_SRP7028A_7.3x6.6mm", {"1": f"{c}_SW1", "2": f"{c}_SW2"}, LCSC="C87572",
            Note="TDK SPM6530T-1R0M120, Isat 14.1 A (datasheet example fig. 8-4); 1.5 MHz only works with 1 uH; footprint is an approximation of 7.1 x 6.5 x 3")
        C("47n 25V", f"{c}_BTST1", f"{c}_SW1", fp=C0603)
        C("47n 25V", f"{c}_BTST2", f"{c}_SW2", fp=C0603)
        C("4.7u 10V", f"{c}_REGN", fp=C0603, Note="REGN 4.7 uF, 10 V")
        C("100n 50V", "EXT", fp=C0603, Note="VBUS 0.1 uF next to the IC")
        for _ in range(2):
            C("10u 35V", "EXT", fp=C1206, Note="VBUS 2 x 10 uF")
        R("2", "EXT", f"{c}_SNUB", fp=R0805, Note="hot-plug snubber 2 ohm + 2.2 uF (fig. 8-1 note 1: adapters above 15 V)")
        C("2.2u 35V", f"{c}_SNUB", fp=C0805)
        C("100n 50V", f"{c}_PMID", fp=C0603, Note="PMID 0.1 uF next to the IC")
        for _ in range(3):
            C("10u 35V", f"{c}_PMID", fp=C1206, Note="PMID 3 x 10 uF (up to 3.3 A input)")
        C("100n 25V", f"{c}_SYS", fp=C0603, Note="SYS 0.1 uF next to the IC")
        for _ in range(5):
            C("10u 25V", f"{c}_SYS", fp=C1206, Note="SYS 5 x 10 uF (up to 5 A charge); no system load on SYS")
        for _ in range(2):
            C("10u 25V", bat, fp=C1206, Note="BAT 2 x 10 uF")
        R("100", bat, f"{c}_BATP", Note="BATP sense: 100 ohm to the pack positive")
        C("1n 50V", f"{c}_SDRV", Note="SDRV 1 nF to GND: no ship FET")
        R("10.5k", f"{c}_PROG", "GND", Note="PROG: 3S, 1.5 MHz (table 7-1; 13.7k would be 3S at 750 kHz with a 2.2 uH inductor)")
        R("47k", f"{c}_REGN", f"{c}_ILIM", Note="ILIM_HIZ = 1 V + 0.8 ohm x I: REGN 5 V x 100/147 = 3.4 V = 3.0 A ceiling (lower of pin and IINDPM)")
        R("100k", f"{c}_ILIM", "GND")
        R("9.31k", f"{c}_REGN", f"{c}_TS", Note="TS: RT1 only (no RT2), 103AT pack NTC to GND: T5 comparator (34.2 % of REGN, charge suspended below it) trips at 45 C "
          "(44.4-45.7 C by the tolerance 33.7-34.7 %, B-model of the NTC), resumes at 43 C (35.5 %); cold cut-off T1 (73.3 %) about 2.5 C; no host needed; doc 43")
        R("100k", f"{c}_REGN", f"{c}_CE", Note="CE high = charging off by default (the charger's own REGN)")
        add(ref("Q"), "Transistor_FET:2N7002", "2N7002", "Package_TO_SOT_SMD:SOT-23", {"1": "CHG_EN", "2": f"{c}_CEM", "3": f"{c}_CE"}, LCSC="C8545",
            Note="CE pull-down 1/2: opens only while P2 holds CHG_EN high")
        add(ref("Q"), "Transistor_FET:2N7002", "2N7002", "Package_TO_SOT_SMD:SOT-23", {"1": "+3V3", "2": "GND", "3": f"{c}_CEM"}, LCSC="C8545",
            Note="CE pull-down 2/2: opens only while +3V3 exists = the On/Off switch is on (the +3V3 comes from +5V from BUS behind the switch)")
        R("2.2k", f"{c}_REGN", f"{c}_LEDA", Note="STAT LED: on = charging, blink = fault")
        add(ref("D"), "Device:LED", "green", "LED_SMD:LED_0603_1608Metric", {"2": f"{c}_LEDA", "1": f"{c}_STAT"}, LCSC="C84267")
        R("10k", f"{c}_SCL", "+3V3", Note="I2C pull-up (downstream of the mux channel)")
        R("10k", f"{c}_SDA", "+3V3")

    # ---------------------------------------------------------------- inputs
    # rev 2.3 (R205): the DC input (jack, fuse, TVS, eFuse, ideal diode IDC) is removed; the only external input is USB-C PD, then the two packs

    add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", "USB-C Power in", MF.format("43045-0612_2x03"),
        {"1": "PD_VBUS", "2": "PD_VBUS", "3": "GND", "4": "GND", "5": "PD_CC1", "6": "PD_CC2"},
        Note="cable from the USB-C Power receptacle on the rear wall (R145): VBUS x 2, GND x 2, CC1, CC2; 5 A rated USB-C")
    add(ref("D"), "Device:D_TVS", "SMBJ20CA", SMB, {"1": "PD_VBUS", "2": "GND"}, LCSC="C151258",
        Note="VBUS surge (audit 18.11.2026, rev 1.1): 20 V standoff, breakdown 22.2-24.5 V = between the TPS25730 recommended 22 V and absolute 28 V "
        "(SLVSGP9 6.1 note 4), clamp about 32 V at 18 A (SMBJ22CA clamped 35 V). TI's TVS2200 (C523793) has 2 pcs at JLC: not used; Littelfuse C151258, 9636 pcs 18.11.2026")
    u = ref("U")
    add(u, "Interface_USB:TPS25730D", "TPS25730D", "Package_DFN_QFN:Texas_REF0038A_WQFN-38-2EP_6x4mm_P0.4",
        {"1": "PD_LDO3V3", "2": "PD_ADCIN1", "3": "PD_LDO3V3", "4": "PD_LDO1V5", "5": "PD_ADCIN34", "6": None,
         "7": "PD_ADCIN34", "8": "GND", "9": "GND", "10": None, "11": "GND", "12": "GND", "13": None, "14": "GND",
         "15": "PD_DRAIN", "16": "GND", "17": "GND", "18": "PD_FAULT", "19": None, "20": "PD_OUT", "23": "PD_VBUSF",
         "26": "PD_RSV26", "27": "PD_RSV27", "28": "PD_CC1", "29": "PD_CC2", "30": "PD_DRAIN", "31": "GND", "32": "PD_VBUSF",
         "34": "GND", "36": "PD_RSV36", "37": None, "38": "GND", "39": "GND", "40": "PD_DRAIN"},
        LCSC="C22438973", PadClearance="20,23:0.12",   # TI land pattern (REF0038A): PP_HV pads 20/23 are 0.125 mm apart, < 0.15 rule
        Note="USB PD sink without I2C (I2Ct_SDA/SCL grounded: allowed if unused): ADCIN1 = 3 (min 15 V), "
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
    C("10u 50V", "PD_VBUSF", fp=C1206, Note="C_VBUS 1-10 uF; rev 1.4 (P123, R201): was 4.7u 25V, which keeps about 1.9 uF at 20 V; 50 V X7R keeps most of 10 uF, so a hot-plugged 20 V cable rings up less (about 37 V unclamped before, limit 28 V)")
    C("10n 50V", "PD_VBUSF", fp=C0603)
    for _ in range(2):
        CP("47u 35V", "PD_VBUS", fp="Capacitor_SMD:CP_Elec_6.3x5.9", LCSC="C178565",
           Note="rev 2.1 (P134): TWO Panasonic EEEFK1V470P in parallel (47 uF 35 V, series FK, ESR about 0.36 ohm at 100 kHz by the datasheet, 6.3 x 6.1 mm, 105 C, C178565, 9238 pcs): 94 uF, ESR about 0.18 ohm; "
           "VBUS hot-plug peak about 21-24 V against the TPS25730 28 V limit (tasks/11, P134); no series resistor; land pattern CP_Elec_6.3x5.9 (the 6.3 mm F case)")
    C("330p", "PD_CC1", Note="C_CC 200-480 pF")
    C("330p", "PD_CC2")
    for _ in range(2):
        C("22u 25V", "PD_OUT", fp=C1210, Note="C_PPHV 47-100 uF in total")
    C("10u 25V", "PD_OUT", fp=C1210)
    CP("47u 35V", "PD_OUT", fp=CP8, Note="C_PPHV 47-100 uF: the 25 V ceramics lose most of their value at 20 V")
    ideal_diode("IPD", "PD_OUT", "EXT")

    # ---- EXT = DC or PD (whichever is higher); it feeds the two chargers and, through its own ideal diode, the bus. The batteries
    # never feed EXT (so a pack cannot charge the other pack through the chargers).
    add(ref("D"), "Device:D_TVS", "SMBJ20CA", SMB, {"1": "EXT", "2": "GND"}, LCSC="C151258",
        Note="EXT clamp (audit 18.11.2026, rev 1.1): the chargers' VBUS/VAC pins are 30 V absolute maximum and 24 V recommended (BQ25798 6.1, 6.3); "
        "SMBJ24CA clamped 38.9 V at 15 A. SMBJ20CA: 20 V standoff, breakdown 22.2-24.5 V, clamp about 32 V at 18 A and about 28 V at 3 A. "
        "Rule: the DC adapter is 12-20 V (19 V standard, R36), not 24 V. Littelfuse C151258, 9636 pcs at JLC 18.11.2026")
    ideal_diode("IEXT", "EXT", "BUS_IN")

    # ---- two battery inputs, each: pack harness (power + NTC), fuse, TVS, ideal diode to the bus, BQ25798 charger from EXT
    for k in (1, 2):
        b, bf, cs = f"BAT{k}_RAW", f"BAT{k}_F", f"CH{k}"
        add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", f"Battery {k}", MF.format("43045-0612_2x03"),
            {"1": b, "2": b, "3": "GND", "4": "GND", "5": f"{cs}_TS", "6": "GND"},
            Note=f"3S pack {k} (3 x Jauch LP906090JH, doc 43 5c) with its own BMS board (BQ7791500, R183): BAT+ x 2, GND x 2, NTC 10k (103AT, B 3435) between pin 5 and pin 6; harness 150-250 mm")
        add(ref("F"), "Device:Fuse", "10A", "Fuse:Fuse_2920_7451Metric", {"1": f"BAT{k}_J", "2": bf}, Note="resettable, 10 A hold: the pack is 6 A (1C of the cell, Jauch datasheet), the BMS trips at 9.6-14.4 A")
        R("0 wire 1mm2", b, f"BAT{k}_J", fp=WIRE1, Note=f"P151 (was 0 ohm 1206, 2-3 A, P147): wire loop in the pack {k} line, 1 mm2 copper (17 mOhm/m), 30 mm: 0.5 mOhm, 33 mW at 8 A, 52 mW at 10 A; clamp meter on the loop or cut it for an ammeter. Thick-film 0 ohm 2512 x 2 would be up to 25 mOhm = 1.6 W at 8 A")
        add(ref("D"), "Device:D_TVS", "SMBJ13CA", SMB, {"1": bf, "2": "GND"}, LCSC="C224008",
            Note="hot-plug TVS at BAT (BQ25798 fig. 8-1, note 2): 13 V standoff above the 12.6 V pack, clamp 21.5 V at 28 A and about 16-17 V at a few A; BAT/BATP absolute maximum is 20 V (SMBJ20CA clamped at 32 V)")
        ideal_diode(f"IBAT{k}", bf, "BUS_IN")
        charger(k, bf)

    # ---------------------------------------------------------------- On/Off switch and BUS
    add(ref("J"), "Connector_Generic:Conn_02x02_Odd_Even", "On/Off switch", MF.format("43045-0412_2x02"), {"1": "BUS_IN", "2": "BUS_IN", "3": "BUS_SW", "4": "BUS_SW"},
        Note="mechanical On/Off on the rear wall: Carling 2GK51-73, both poles in parallel (>= 10 A DC); rev 1.2: Micro-Fit 2x2 (43045-0412, housing 43025-0400): two contacts per side, 5 A per contact at the "
        "10.2 A peak (95 W from a 9.3 V pack); was a 1x2 with 10 A on one contact, over the contact rating (harness H3: 4 wires, one pole = 2 wires)")
    # input power monitor (R146): everything the instrument draws passes the shunt; P2 reads it and caps the LEDs
    # INA226 ALERT (P130): bus under-voltage limit set by the firmware (register 0x1EA0 = 9.8 V at 1.25 mV/LSB, "pack is running down"): the LM5176 stops by itself at 9.3 V (8.4-10.4 V),
    # the BMS cuts at 3 x 2.9 V = 8.7 V; the alert mutes the outputs smoothly, the hold-up module HU1 covers the rest (tasks/13)
    R("5m", "BUS_SW", "BUS", fp=R2512, Note="shunt 5 mOhm 1 % 3 W: 8 A -> 40 mV (INA226 range 81.9 mV)")
    u = ref("U")
    add(u, "Sensor_Energy:INA226", "INA226", "Package_SO:MSOP-10_3x3mm_P0.5mm",
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
    add(ref("J"), "Connector_Generic:Conn_01x08", "Power telemetry to P2", PH.format(n=8),
        {"1": "PM_SDA", "2": "PM_SCL", "3": "PM_ALERT", "4": "CHG_INT", "5": "FAN_PWM_IN", "6": "FAN_TACH_OUT", "7": "GND", "8": "CHG_EN"},
        LCSC="C157974", Note="to the panel hub P2 (R146, R183): I2C (INA226 0x40, mux 0x70 -> chargers 0x6B x 2), ALERT = over-limit, CHG_INT = "
        "charger interrupt (wired-AND), fan PWM in (3.3 V, 25 kHz), tach out and CHG_EN (3.3 V from P2: charging allowed; low or open = no charge); pull-ups of SDA/SCL to 3.3 V on P2")
    # two BQ25798 have the same I2C address 0x6B: TCA9546A mux (0x70), channel 0 = charger 1, channel 1 = charger 2
    add(ref("U"), "Interface_Expansion:TCA9546APW", "TCA9546APW", "Package_SO:TSSOP-16_4.4x5mm_P0.65mm",
        {"1": "GND", "2": "GND", "3": "MUX_RST", "4": "CH1_SDA", "5": "CH1_SCL", "6": "CH2_SDA", "7": "CH2_SCL", "8": "GND",
         "9": None, "10": None, "11": None, "12": None, "13": "GND", "14": "PM_SCL", "15": "PM_SDA", "16": "+3V3"},
        LCSC="C201653", Note="I2C switch 0x70 (A0-A2 GND): channels 0 and 1 = the two chargers; INA226 stays on the main bus")
    R("10k", "MUX_RST", "+3V3")
    C("100n", "+3V3", fp=C0603, Note="mux VCC")
    R("10k", "CHG_INT", "+3V3", Note="pull-up of the wired-AND charger INT")
    R("100k", "CHG_EN", "GND", Note="open or dead P2 = charging disabled")
    CP("100u 35V", "BUS", fp=CP10, Note="bulk")
    for _ in range(2):
        CP("150u 35V", "BUS", fp=CP8, MPN="EEH-ZA1V151P", Note="rev 1.4 (P123, R201): hold-up on loss of external power: BUS 125 uF effective = 105 us at 95 W, +300 uF = about 350 us (tasks/09); P153: Panasonic EEH-ZA1V151P hybrid polymer 150 uF 35 V, 8 x 10.2 (datasheet to confirm)")
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
        LCSC="C442493", Note="9-24 V (rev 1.0: 3S packs 9-12.6 V) -> 19 V 5 A (95 W), 300 kHz; values after fig. 8-1 (6-50 V -> 12 V 6 A); ISNS+/- "
        "shorted = average current loop off; DITH to AGND = no dithering; BIAS from VOUT (8-36 V)")
    R("10", "BUS", "B19_VIN", fp=R0603, Note="VIN filter")
    C("1u 50V", "B19_VIN", fp=C0805)
    R("249k", "BUS", "B19_UVLO", Note="UVLO rev 1.0 (datasheet eq. 1-2): start 1.22 V x (1 + 249k / 32.4k) - 249k x 2 uA = 10.1 V, stop 10.1 V - 3.15 uA x 249k = 9.3 V (was 9.45 / 8.7 V): the converter stops before the cell PCMs cut at about 9.0 V and restarts only above 10.1 V (no restart loop on a flat 3S pack)")
    R("32.4k", "B19_UVLO", "GND")
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
      "= 12.5-17.5 A > 9.9 A peak at 12 V in; ~0.6 W at 12 V; rev 1.0 at 9.3 V in: ripple 3.4 A, average limit >= 10.3 A = 96 W in, "
      "about 86 W out against 45-50 W on the 19 V rail (H5 25 W, audio, phantom, fan)")
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
    add(ref("J"), "Connector_Generic:Conn_02x02_Odd_Even", "15 V to H5", MF.format("43045-0412_2x02"),
        {"1": "V15", "2": "V15", "3": "GND", "4": "GND"},
        Note="cable to the DC jack of the ODROID-H5 (5.5 x 2.1 mm plug, centre positive; H5 input 11-20 V, Hardkernel recommends 15 V / 4 A, R149)")

    # ---------------------------------------------------------------- +5 V x 2: LM70660, 6 A each (rev 1.5, P125: was TPS54560B with Eco-mode only)
    # LM70660 (SNVSCD4): PFM/SYNCIN to AGND = forced PWM (no pulse skipping, no audible burst hum at dark LEDs); CONFIG 41.2k = standalone + DRSS (spread spectrum +-8 %);
    # fixed 5 V: RFB = 24.9k from FB to VDDA, BIAS at VOUT (VCC 5 V); RT 54.9k = 400 kHz (design example 7.2.1.2.7); EXTCOMP 100k to VDDA = internal compensation;
    # CBOOT 47 nF, VCC 4.7 uF, VDDA 0.1 uF; shunt current limit: Rs = 56 mV / (Ipk), Ipk = 5.6 A + dIL/2 -> 8.2 A with 6.8 mOhm; L 4.7 uH (dIL = 5 V x (1 - 5/24) / (4.7 uH x 400 kHz)
    # = 2.1 A at 24 V in, 30 % of 6 A), Isat >= 9 A; Cin 4 x 2.2 uF 50 V + 10 nF, Cout 4 x 47 uF 10 V (about 100 uF at 5 V; the datasheet example has 82 uF effective for 8 A).
    def buck5(net, note):
        u5 = ref("U")
        p = net.replace("+", "P").replace("_", "")
        add(u5, "ShtukaDruka:LM70660", "LM70660", "ShtukaDruka:VQFN-29_RRX0029B_6x6_P0.5mm",
            {"1": "BUS", "2": "BUS", "3": "BUS", "4": f"{p}_BOOT", "5": f"{p}_SW", "6": net, "7": None, "8": "GND", "9": f"{p}_EN", "10": None,
             "11": f"{p}_LS", "12": net, "13": f"{p}_CFG", "14": f"{p}_RT", "15": f"{p}_XC", "16": f"{p}_FB", "17": "GND", "18": f"{p}_VDDA", "19": f"{p}_VCC",
             "20": f"{p}_SW", "21": f"{p}_SW", "22": f"{p}_SW", "23": "GND", "24": "GND", "25": "GND", "26": "GND", "27": "BUS", "28": "BUS", "29": "BUS", "30": "GND"},
            LCSC="C42328952", Note=f"{note}; BUS -> 5 V 6 A, 400 kHz forced PWM + DRSS (P125); footprint checked against the TI RRX0029B drawing with TI vias (doc 52)")
        R("392k", "BUS", f"{p}_EN", Note="UVLO divider (datasheet 6.3.2, eq. 2): EN rising 1.0 V (0.95-1.05) x (1 + 392k / 49.9k) = start 8.86 V (8.4-9.3 V), stop at 90 % = 7.97 V; the pack runs 9-12.6 V (BMS cut-off 8.7 V); EN pin 65 V tolerant, 2.7 V at 24 V in")
        R("49.9k", f"{p}_EN", "GND")
        R("54.9k", f"{p}_RT", "GND", Note="RT: 400 kHz (datasheet 7.2.1.2.7, E96)")
        R("41.2k", f"{p}_CFG", "GND", Note="CONFIG: standalone, DRSS enabled (table 6-2)")
        R("24.9k", f"{p}_FB", f"{p}_VDDA", Note="fixed 5 V output (RFB = 24.9k to VDDA)")
        R("100k", f"{p}_XC", f"{p}_VDDA", Note="EXTCOMP to VDDA: internal compensation")
        C("100n", f"{p}_VDDA", Note="VDDA decoupling to AGND")
        C("4.7u", f"{p}_VCC", fp=C0805, Note="VCC to PGND")
        C("47n", f"{p}_BOOT", f"{p}_SW", fp=C0603, Note="CBOOT")
        add(ref("L"), "Device:L", "4.7uH", "Inductor_SMD:L_Bourns_SRP1038C_10.0x10.0mm", {"1": f"{p}_SW", "2": f"{p}_LS"},
            MPN="SRP1038CC-4R7M", Note="P153: Bourns SRP1038CC-4R7M (datasheet notes/datasheets_text/srp1038cc.md): 4.7 uH, Isat 20 A, Irms 13 A, DCR 14.5 / 15.5 mOhm typ / max: 6 A -> 0.56 W; same footprint as the 8.2 uH")
        R("6.8m", f"{p}_LS", net, fp=R2512, Note="current-sense shunt 1 %, Kelvin to ISNS+ / VOUT: Rs = 56 mV / 8.2 A")
        for _ in range(4):
            C("2.2u 50V", "BUS", fp=C1206, Note="input")
        C("10n 50V", "BUS", fp=C0603, Note="input, high di/dt, next to VIN and PGND")
        for _ in range(4):
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
    add(ref("J"), "Connector_Generic:Conn_01x04", "to F1", PH.format(n=4), {"1": "+12V", "2": "GND", "3": "-12V", "4": "+5V"},
        Note="headphone amplifiers +-12 V and the mute relay coils +5 V (F1 'from PW')")
    add(ref("J"), "Connector_Generic:Conn_01x02", "+5V screen", PH.format(n=2), {"1": "+5V", "2": "GND"},
        Note="Waveshare 10.1DP-CAPLCD, 5 V / 4 W (R110)")
    R("2.2k", "+5V", "LED_K", Note="power LED")
    add(ref("D"), "Device:LED", "green", "LED_SMD:LED_0603_1608Metric", {"2": "LED_K", "1": "GND"}, LCSC="C84267")

    # ---------------------------------------------------------------- 15 V for the ODROID-H5 (R149, P106): LMR33640 buck from V19
    u = ref("U")
    add(u, "Regulator_Switching:LMR33640ADDA", "LMR33640", "Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias",
        {"1": "GND", "2": "V19", "3": "V19", "4": None, "5": "V15_FB", "6": "V15_VCC", "7": "V15_BOOT", "8": "V15_SW", "9": "GND"},
        LCSC="C2836966", Note="19 V -> 15 V for the H5 (25 W peak = 1.7 A; the part gives 4 A), 400 kHz like the 14 V stage; "
        "the H5 never sees more than 15 V + tolerance: the 19 V rail stays inside PW (+-14 V, phantom need it)")
    R("100k", "V15", "V15_FB", Note="1.0 V x (1 + 100k / 7.15k) = 15.0 V")
    R("7.15k", "V15_FB", "GND")
    C("100n 25V", "V15_BOOT", "V15_SW", fp=C0603)
    C("1u", "V15_VCC", fp=C0603)
    C("10u 50V", "V19", fp=C1210)
    C("220n 50V", "V19", fp=C0603)
    add(ref("L"), "Device:L", "10uH", "Inductor_SMD:L_Bourns_SRN6045TA", {"1": "V15_SW", "2": "V15"}, Note="10 uH, Isat >= 3.2 A - check")
    for _ in range(3):
        C("22u 25V", "V15", fp=C1210)

    # ---------------------------------------------------------------- 12 V for the case fan (80 x 80 x 25, PWM, 4-pin): LMR33640 buck from V19
    u = ref("U")
    add(u, "Regulator_Switching:LMR33640ADDA", "LMR33640", "Package_SO:Texas_HSOP-8-1EP_3.9x4.9mm_P1.27mm_ThermalVias",
        {"1": "GND", "2": "V19", "3": "V19", "4": None, "5": "V12F_FB", "6": "V12F_VCC", "7": "V12F_BOOT", "8": "V12F_SW", "9": "GND"},
        LCSC="C2836966", Note="19 V -> 12 V for the fan (an 80 x 25 mm fan takes 0.2-0.5 A; the part gives 4 A): same stage as the 15 V one, 400 kHz")
    R("100k", "V12F", "V12F_FB", Note="1.0 V x (1 + 100k / 9.09k) = 12.0 V")
    R("9.09k", "V12F_FB", "GND")
    C("100n 25V", "V12F_BOOT", "V12F_SW", fp=C0603)
    C("1u", "V12F_VCC", fp=C0603)
    C("10u 50V", "V19", fp=C1210)
    C("220n 50V", "V19", fp=C0603)
    add(ref("L"), "Device:L", "10uH", "Inductor_SMD:L_Bourns_SRN6045TA", {"1": "V12F_SW", "2": "V12F"}, Note="10 uH, Isat >= 1 A - check")
    for _ in range(3):
        C("22u 25V", "V12F", fp=C1210)
    add(ref("J"), "Connector_Generic:Conn_01x04", "Fan 12 V PWM", "Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical",
        {"1": "GND", "2": "V12F", "3": "FAN_TACH", "4": "FAN_PWM"}, LCSC="C2691448",
        Note="4-pin PC fan (Intel pinout: 1 GND, 2 +12 V, 3 tach, 4 PWM): one 80 x 80 x 25 fan; speed = max of the H5 and the pack NTC temperatures, set by P2")
    R("100", "FAN_PWM_IN", "FAN_PWM", Note="PWM from P2 (3.3 V, 25 kHz); no signal = the fan runs full speed (Intel spec)")
    R("10k", "FAN_TACH", "+3V3", Note="tach is open collector: pull-up to 3.3 V")
    R("100", "FAN_TACH", "FAN_TACH_OUT")

    # ---------------------------------------------------------------- rev 1.5 (P127): eFuse TPS26631 at the INPUT of the TPS25730 (was after it, rev 1.4)
    # connector -> TVS D2 (PD_VBUS) -> damper 47 uF electrolytic -> eFuse -> PD_VBUSF -> TPS25730 VBUS (pins 23/32) + 10 uF ceramic. The eFuse (IN 67 V absolute) takes the hot-plug
    # spike; its OVP cuts at 22.55 V, so the TPS25730 (28 V absolute) never sees more. UV 4.16 V: the TPS25730 is powered from VBUS alone (no VIN_3V3), so the 5 V attach must pass.
    # Divider (eq. 9, 10, 1.2 V): R1 357k, R2 118k, R3 26.7k -> OV = 1.2 x 501.7k / 26.7k = 22.55 V, UV = 1.2 x 501.7k / 144.7k = 4.16 V (+-4 % reference: UV 4.0-4.3 V, OV 21.6-23.5 V,
    # a 20 V source +5 % = 21 V clears it by 0.6 V). dVdT 10 nF = 4 ms at 19 V; ILIM 5.4 A (PD maximum 5 A). PD_OUT -> IPD directly; the charge of PP_HV 101 uF and of EXT/BUS/V19
    # behind it is no longer slewed by the eFuse (open: TPS25730 gate datasheet or bench).
    u = ref("U")
    add(u, "ShtukaDruka:TPS26631", "TPS26631RGER", "Package_DFN_QFN:QFN-24-1EP_4x4mm_P0.5mm_EP2.65x2.65mm",
        {"1": "PD_VBUS", "2": "PD_VBUS", "3": None, "4": None, "5": "PD_VBUS", "6": "PDF_UV", "7": "PDF_OV", "8": "GND", "9": "PDF_DVDT", "10": "PDF_ILIM", "11": "GND",
         "12": "PDF_SHDN", "13": None, "14": None, "15": "GND", "16": None, "17": "PD_VBUSF", "18": "PD_VBUSF", "19": None, "20": None, "21": None, "22": None, "23": None,
         "24": None, "25": "GND"}, LCSC="C1850273",
        Note="USB-C PD input eFuse in front of the TPS25730 VBUS (rev 1.5, P127): OVP 22.55 V, UV 4.16 V, 5.4 A limit; no blocking FET; JLC 314 pcs 19.11.2026")
    R("357k", "PD_VBUS", "PDF_UV", Note="R1 of the UVLO/OVP divider (OV 22.55 V, UV 4.16 V)")
    R("118k", "PDF_UV", "PDF_OV", Note="R2")
    R("26.7k", "PDF_OV", "GND", Note="R3")
    R("3.32k", "PDF_ILIM", "GND", Note="RILIM: 18 kOhm x A / 3.32k = 5.4 A")
    C("10n 50V", "PDF_DVDT", fp=C0603, Note="dVdT slew: about 4 ms at 19 V")
    R("220k", "PD_VBUS", "PDF_SHDN", Note="SHDN pull-up (needs 2 V, abs max 5.5 V; 5 V attach is above 2 V)")
    add(ref("D"), "ShtukaDruka:BZT52C3V3", "BZT52C3V3", SOD123, {"1": "GND", "2": "PDF_SHDN"}, LCSC="C173413", Note="clamps SHDN to 3.3 V")
    # ---------------------------------------------------------------- rev 1.8 (P129/P131): hold-up storage on the +-14 V rails, before the LDOs, on PW itself (HU1 cancelled)
    # 2 x 470 uF 25 V per rail = 0.94 mF: 4.8 ms at 0.43 A, 7.1 ms at 0.29 A (tasks/12, dV 2.2 V with the Schottky drop). Behind 10 ohm: the LMR33640 (soft start 4 ms,
    # low-side limit 3.9-5 A, total output capacitance at most about 1000 uF) would charge 1 mF at 3.5 A, through 10 ohm the peak is 1.4 A; Schottky in the discharge direction.
    for rail, plus, minus, rs, anode, cathode in (("P14", "P14_ST", "GND", ("P14", "P14_ST"), "P14_ST", "P14"), ("N14", "GND", "N14_ST", ("N14", "N14_ST"), "N14", "N14_ST")):
        for _ in range(2):
            CP("470u 25V", plus.replace("_ST", "_C"), minus.replace("_ST", "_C"), fp=CP10, MPN="EEE-FK1E471P", Note=f"hold-up storage {rail}: Panasonic EEE-FK1E471P 470 uF 25 V, 105 C, case G 10 x 10.2, ripple 850 mA, ESR 0.08 ohm (datasheet, notes/datasheets_text/panasonic_eee_fk.md), bottom side")
        R("0", rs[1], rs[1].replace("_ST", "_C"), fp=R1206, Note=f"P147: 0 ohm jumper between the {rail} storage node and its capacitors: charge and discharge current of the storage")
        R("10", rs[0], rs[1], fp=R2512, Note=f"P153: 2512 (1 W, pulse 0.09 J) instead of 1206; {rail} storage charge resistor: LMR33640 datasheet 9.2.2: total output capacitance at most about 1000 uF (10 x design value), soft start 4 ms, low-side limit 3.9-5 A; 0.94 mF + 45 uF straight on the output would be 3.5 A; behind 10 ohm the peak is 1.4 A (tau 9.4 ms)")
        add(ref("D"), "Device:D_Schottky", "SS34", SMA, {"1": cathode, "2": anode}, LCSC="C8678",
            Note=f"{rail} storage discharge diode (the storage feeds the rail when it sags), 40 V 3 A; check the part number and the stock")
    # rev 2.2 (P135): idle load of about 30 mA on each LMR33640 output, so that the converters stay out of PFM (burst hum in the audio): R = Uout / 0.03 A, two 1206 resistors in parallel per rail (<= 0.25 W each)
    for net, ohm in (("P14", "1k"), ("N14", "1k"), ("V15", "1k"), ("V12F", "820")):
        for _ in range(2):
            R(ohm, net, "GND", fp=R2512, Note=f"PFM idle load P135: {net}, 2 x {ohm} = about 30 mA; P153: 2512 1 W, 0.23 W at 15 V = 23 % (was 1206, 90 %)")
    # rev 2.4 (P147): test points (D2.0 mm pads): VBUS after the damper, BUS, +-14 V, 5 V rails, 3V3, three GND
    for net in ("PD_VBUS", "BUS", "P14", "N14", "+5V", "+5V_PANEL", "+3V3", "GND", "GND", "GND"):
        add(ref("TP"), "Connector:TestPoint", net.replace("PD_VBUS", "VBUS"), "TestPoint:TestPoint_Pad_D2.0mm", {"1": net}, Note="P147 test point")
    K.mount_holes(add, ref, HOLES, "M3 standoff (Codex review 15.11.2026): corners first; the final positions come with the enclosure")
    return P


def placement():
    """Rev 2.7 (26.11.2026, user via the main chief engineer, decision P: "rebuild at 100 x 80 ... spread the parts over both sides"):
    100 x 80, two-sided. Top: every IC, FET, inductor, fuse, connector, electrolytic, 1206 / 1210 / 2512 part and the hot-loop
    capacitors (input ceramics of the LM5176 / LM70660 / LMR33640 / LM5156H, bootstrap caps), the phantom boost diode, power shunts; bottom: the other
    passives (resistors, output and decoupling caps, under the pins of their IC), TVS, SS34, 2N7002, LEDs, test points, INA226 / AP2112 / TCA9546 and the electrolytics (10.5 mm, as before). Connectors on the edges: inputs (USB-C PD, packs, On/Off) left, outputs
    bottom, telemetry and fan right. Quiet LDO corner (TPS7A4701 / TPS7A3301 / TPS7A4101) bottom-right above the output row, no switcher
    in it; the +-14 V hold-up electrolytics in a row under the board above the output connectors. The rest: autoplace grid (connectivity chain),
    gap / ic_gap from autoplace.fit (template 20.11.2026, >= 1.4 mm wanted)."""
    import autoplace
    import packer
    P = parts()
    byref = {p["ref"]: p for p in P}
    fixed = K.hole_fixed(P, HOLES)
    me = sys.modules[__name__]

    def edge_column(refs, x_edge, y0, rot, right=False):
        y = y0
        for r in refs:
            box, _ = packer._bbox(me, byref[r], rot, "top")
            x = (x_edge - box[2]) if right else (x_edge - box[0])
            fixed[r] = (round(x, 2), round(y - box[1], 2), rot, "top")
            y += box[3] - box[1] + 2.0

    def edge_row(refs, x0, y_edge):
        x = x0
        for r in refs:
            box, _ = packer._bbox(me, byref[r], 0, "top")
            fixed[r] = (round(x - box[0], 2), round(y_edge - box[3], 2), 0, "top")
            x += box[2] - box[0] + 2.0

    edge_column(["J1", "J2", "J3", "J4"], 0.8, 8.5, 90)             # inputs: USB-C PD, packs 1 and 2, On/Off
    edge_column(["J5", "J12", "J11"], W - 0.8, 8.5, 90, right=True)  # telemetry to P2, fan, screen 5 V
    edge_row(["J7", "J9", "J6", "J8", "J10"], 9.0, H - 0.8)  # outputs: +5V panel, A1/R1, 15 V H5, R2, F1
    for v, xy in QUIET_XY.items():
        r = next(p["ref"] for p in P if p["value"] == v)
        fixed[r] = xy + (0, "top")
    st = sorted(p["ref"] for p in P if p["ref"].startswith("C") and p["value"] == "470u 25V")
    for r, x in zip(st, (21.0, 32.5, 44.0, 55.5)):
        fixed[r] = (x, H - 18.0, 90, "bottom")                       # hold-up storage row under the board, above the output connectors
    follow = [r for r, v in fixed.items() if r.startswith("U")]

    def side_of(ref, side):
        p = byref[ref]
        fp = p["fp"]
        nets = {n for n in p["pins"].values() if n}
        if ref.startswith("U") and p["value"] in ("INA226", "AP2112K-3.3", "TCA9546APW"):
            return "bottom"                        # small logic: monitor, its LDO, the I2C mux
        if ref.startswith(("U", "L", "F", "J", "H")) or ref.startswith("Q") and p["value"] != "2N7002":
            return "top"
        if ref.startswith("D"):
            return "top" if p["value"] == "SS1H10" else "bottom"   # the phantom boost diode is in the hot loop; TVS / SS34 / LEDs below
        if ref.startswith("R"):
            return "top" if p["value"] in ("5m", "8m", "6.8m") or fp == WIRE1 else "bottom"   # shunts in the power path, the wire loop
        if ref.startswith("C") and "CP_Elec" not in fp:
            hot = (any(k in n for n in nets for k in ("BOOT", "BTST")) or "high di/dt" in p["fields"].get("Note", "")
                   or p["value"] in ("220n 50V", "4.7u 50V", "2.2u 50V", "4.7u 100V") and nets & {"BUS", "V19", "HV_RAW"})
            return "top" if hot else "bottom"      # switcher input banks and bootstraps (hot loops) with their IC
        if "CP_Elec" in fp:
            return "top"                           # bulk electrolytics with their rails (the 470 uF hold-up row is fixed under the board)
        return "bottom"                            # 2N7002, test points

    return autoplace.fit(me, lambda g, ic: autoplace.place(me, fixed=fixed, follow=follow, gap=g, ic_gap=ic, anchor_side="top",
                                                          grid=(14.0, 7.0, W - 12.0, H - 16.0), keepout=KEEPOUT, side_of=side_of),
                         ic_add=0.2)   # gap 1.4 / ic_gap 1.6 fits 100 x 80 (1.4 / 2.0 does not)


QUIET_XY = {"TPS7A4701": (76.0, 49.0), "TPS7A3301": (76.0, 60.0), "TPS7A4101": (87.0, 49.0)}   # rev 2.7: quiet corner bottom-right
KEEPOUT = [(66.0, 42.0, 100.0, 80.0)]   # grid cells: not in the quiet corner


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
