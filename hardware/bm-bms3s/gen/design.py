"""BM - Battery protection board for one 3S pack (BQ7791500, TI SLUSCU0L): sits at the end of the pack, 2 pcs per set (docs/ru/43_battery_power.md 5c).
Low-side protection: cell 1 negative = BAT_N = VSS, the series path goes BAT_N -> 5 mOhm -> CSD18540Q5B (DSG) -> CSD18540Q5B (CHG) -> PACK_N.
Pack plus (cell 3 positive) is not switched: BAT_P goes straight to the output. Single source of truth for the schematic.

Values: TI SLUSCU0L fig. 9-11 (3-series, balancing on, HIBERNATE off) and table 10-1 / 10-2 (design example, 3S, 4.2 V):
VDD 1k + 1 uF; cell inputs RIN + CIN 0.1 uF (RIN 75 R, not the 1k of the table: the same resistor sets the internal balancing current, 4.2 V / (2 x 75 R + internal) = 25 mA
= 8 % of the 0.05 C end-of-charge current of a 6 Ah cell, doc 43); VC5 = VC4 = VC3 on the top cell (section 11: unused VCx pins short to the highest used one);
CCFG and CBI to VSS (3 cells, balancing on); PRES to the top of the pack through 10k (NORMAL mode); OCDP 100k to VSS (OCD delay 180 ms);
TS: 103AT NTC to VSS + 10k 1 % from VTB (OTC 45 C stops charging; OTD 65 C, UTC 0 C, UTD -10 C); CTRC, CTRD, LPWR, CBO open (single device, fig. 9-11);
SRP/SRN 100 R + 0.1 uF; DSG 4.53k (table: 4.5k), CHG 1k; gate-source 1M (DSG) and 3.3M (CHG, load removal for UV recovery); LD 470k (table 10-1; doc 43 had 453k).
Thresholds (BQ7791500): OV 4.200 V, UV 2.9 V, OCD 60 mV / 5 mOhm = 12 A nominal (9.6-14.4 A), SCD 120 mV, OTC 45 C.
Rev 0.1 (19.11.2026, PC): schematic and placed board. License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "bm-bms3s"
ID = "BM"
TITLE = "BM - Battery protection 3S: BQ7791500, 2 x CSD18540Q5B, 5 mOhm, balancing, NTC"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("Pack: cell taps J1 (B-, B1, B2, B+), power in J2 (cell 1 negative, cell 3 positive), NTC of the chip J3 and NTC for PW J4; "
            "output J5 = PW 'Battery' harness (BAT+ x 2, GND x 2, NTC, GND)")
PWR_FLAG_NETS = ("BAT_P", "BAT_N", "B1", "B2", "PACK_N", "NTC_PW", "TS_NTC")   # ERC: nets that only connectors drive
NO_PWR_FLAG = ("+3V3",)
W, H = 38.0, 38.0           # the pack end has 38.5 mm along the pack (doc 43 5a) and about 12 mm spare across; 2 x M3 mid-edge
HOLES = [(3.5, H / 2), (W - 3.5, H / 2)]
LAYERS = 2

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R2512 = "Resistor_SMD:R_2512_6332Metric"
TSSOP24 = "Package_SO:TSSOP-24_4.4x7.8mm_P0.65mm"
FET = ("Transistor_FET:CSD18540Q5B", "Package_TO_SOT_SMD:TDSON-8-1")   # 60 V 1.8 mOhm, pins 1-3 S, 4 G, 5 D
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"
# LCSC numbers, all in stock at JLC on 19.11.2026 (jlcpcb.com parts search): 0402 resistors by value
LCSC_R = {"75": "C114757", "100": "C25076", "1k": "C11702", "4.53k": "C79537", "10k": "C25744", "100k": "C25741", "470k": "C25790",
          "1M": "C26083", "3.3M": "C270613"}
LCSC_C = {"100n": "C1525", "1u": "C52923"}


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "Q": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    def R(value, a, b, **f):
        add(ref("R"), "Device:R", value, R0402, {"1": a, "2": b}, LCSC=LCSC_R[value], **f)

    def C(value, a, b, fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, LCSC=LCSC_C[value], **f)

    # ---------------------------------------------------------------- connectors
    add(ref("J"), "Connector_Generic:Conn_01x04", "Cell taps", PH.format(n=4), {"1": "BAT_N", "2": "B1", "3": "B2", "4": "BAT_P"},
        Note="thin sense wires to the cell junctions: B- (cell 1 negative), B1 (cell 1 / 2), B2 (cell 2 / 3), B+ (cell 3 positive); no load current here")
    add(ref("J"), "Connector_Generic:Conn_01x02", "Cell power", MF.format("43650-0215_1x02"), {"1": "BAT_N", "2": "BAT_P"},
        Note="cell 1 negative and cell 3 positive (AWG18 pack wires, joined wire to wire, doc 43); the pack current flows through this connector, 6 A")
    add(ref("J"), "Connector_Generic:Conn_01x02", "NTC chip", PH.format(n=2), {"1": "TS", "2": "BAT_N"},
        Note="103AT 10k (B 3435) NTC on the middle cell: the BQ7791500 TS input (45 C stops charging in the chip)")
    add(ref("J"), "Connector_Generic:Conn_01x02", "NTC PW", PH.format(n=2), {"1": "NTC_PW", "2": "PACK_N"},
        Note="second 103AT NTC on the middle cell for the BQ25798 TS of PW (not in parallel with the chip's): wired to the PW harness pins 5 and 6")
    add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", "to PW (Battery)", MF.format("43045-0612_2x03"),
        {"1": "BAT_P", "2": "BAT_P", "3": "PACK_N", "4": "PACK_N", "5": "NTC_PW", "6": "PACK_N"},
        Note="same pinout as PW 'Battery 1/2': BAT+ x 2, GND x 2, NTC, GND (harness 150-250 mm). Vertical plug height about 9 mm: check the 11 mm of the pack bay")

    # ---------------------------------------------------------------- BQ7791500
    u = ref("U")
    add(u, "ShtukaDruka:BQ77915", "BQ7791500PWR", TSSOP24,
        {"1": "VDD", "2": "AVDD", "3": "VC3F", "4": "VC3F", "5": "VC3F", "6": "VC2F", "7": "VC1F", "8": "VC0F", "9": "BAT_N", "10": "SRPF", "11": "SRNF",
         "12": "DSG", "13": "CHG", "14": "LD", "15": None, "16": "BAT_N", "17": "OCDP", "18": "TS", "19": "VTB", "20": "BAT_N", "21": None,
         "22": "PRES", "23": None, "24": None},
        LCSC="C2876946", Note="3S, 4.2 V (variant 00): OV 4.200 V, UV 2.9 V, OCD 60 mV / 5 mOhm, SCD 120 mV, OTC 45 C, balancing from 3.8 V; "
        "Digikey 296-50995-1-ND, 2095 pcs 18.11.2026")
    R("1k", "BAT_P", "VDD", Note="RVDD (table 10-1)")
    C("1u", "VDD", "BAT_N", fp=C0603, Note="CVDD; 25 V")
    C("1u", "AVDD", "BAT_N", fp=C0603, Note="AVDD: capacitor only (pin 2)")
    cells = (("BAT_N", "VC0F", "VC0"), ("B1", "VC1F", "VC1"), ("B2", "VC2F", "VC2"), ("BAT_P", "VC3F", "VC3, VC4, VC5"))
    for src, node, pins in cells:
        R("75", src, node, Note=f"RIN of {pins}: also sets the balancing current (about 25 mA, doc 43)")
    for lo, hi in (("VC0F", "VC1F"), ("VC1F", "VC2F"), ("VC2F", "VC3F")):
        C("100n", hi, lo, Note="CIN across one cell")
    R("100k", "OCDP", "BAT_N", Note="ROCD: OCD1/2 delay (table 10-1)")
    R("10k", "VTB", "TS", Note="RTS_PU 1 % (103AT)")
    R("10k", "PRES", "BAT_P", Note="RHIB: pull-up = NORMAL mode, HIBERNATE off")
    R("470k", "LD", "PACK_N", Note="RLD: load removal detection (table 10-1; datasheet 470k)")

    # ---------------------------------------------------------------- current path and FETs
    add(ref("R"), "Device:R", "5m", R2512, {"1": "BAT_N", "2": "SRN_NODE"}, LCSC="C2903482",
        Note="RSNS 5 mOhm 1 % 3 W (2512): OCD 60 mV = 12 A, SCD 120 mV = 24 A; 0.18 W at 6 A")
    R("100", "BAT_N", "SRPF", Note="RS (SRP)")
    R("100", "SRN_NODE", "SRNF", Note="RS (SRN)")
    C("100n", "SRPF", "SRNF", Note="CS across SRP-SRN")
    add(ref("Q"), FET[0], "CSD18540Q5B", FET[1], {"1": "SRN_NODE", "2": "SRN_NODE", "3": "SRN_NODE", "4": "DSG_G", "5": "MID"}, LCSC="C86513",
        Note="discharge FET: source on the sense resistor, drain to the charge FET (back to back)")
    add(ref("Q"), FET[0], "CSD18540Q5B", FET[1], {"1": "PACK_N", "2": "PACK_N", "3": "PACK_N", "4": "CHG_G", "5": "MID"}, LCSC="C86513",
        Note="charge FET: source on PACK-")
    R("4.53k", "DSG", "DSG_G", Note="RDSG (table 10-1: 4.5k)")
    R("1M", "DSG_G", "SRN_NODE", Note="RGS_DSG")
    R("1k", "CHG", "CHG_G", Note="RCHG")
    R("3.3M", "CHG_G", "PACK_N", Note="RGS_CHG: load removal enabled for UV recovery (table 10-1)")
    K.mount_holes(add, ref, HOLES, "M3 standoff, pack end plate; the final positions come with the pack bay model")
    return P


def placement():
    """Connectors along the bottom edge, the IC and the FETs by autoplace (rough, a starting point for routing)."""
    import autoplace
    fixed = K.hole_fixed(parts(), HOLES)
    # connector bodies (packer._bbox): J1 cell taps 11 x 5.6, J3/J4 NTC 7 x 5.6 in a row along the top edge; J2 cell power 10.8 x 6.9 and the
    # Micro-Fit 2x3 output J5 14.2 x 9.9 along the bottom edge; the chip, the FETs and the sense resistor sit between.
    fixed.update({"J1": (8.0, 3.0, 0, "top"), "J3": (18.5, 3.0, 0, "top"), "J4": (27.0, 3.0, 0, "top"),
                  "J2": (11.0, H - 5.0, 0, "top"), "J5": (W - 8.3, H - 5.5, 0, "top")})
    return autoplace.place(sys.modules[__name__], fixed=fixed, conn_y=H - 6.0)


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
