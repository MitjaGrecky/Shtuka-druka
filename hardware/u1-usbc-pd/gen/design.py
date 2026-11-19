"""U1 - USB-C PD input board (rear wall, harness H1): the panel USB-C receptacle GCT USB4105-GF-A (5 A, LCSC C3020560) on a small board, six solder pads for the
wires to PW J2 (Micro-Fit 2x3, 12 cm): VBUS x 2 and GND x 2 (20 AWG, 2.5 A per wire at 5 A), CC1 and CC2 (24 AWG). The PD sink controller TPS25730D stays on PW
(R145); D+ / D- / SBU are not used (power only) and stay open. The shield goes to GND through 1 MOhm || 1 nF (floating shield, ESD path to the chassis comes
through the panel contact of the board's mounting holes).
Pad numbers of the symbol Connector:USB_C_Receptacle_USB2.0_16P = pads of the KiCad footprint USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal (SH = shield).
Rev 0.1 (19.11.2026, PC): schematic and placed board. License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "u1-usbc-pd"
ID = "U1"
TITLE = "U1 - USB-C PD input board: GCT USB4105-GF-A, wires to PW J2"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = "Rear-wall USB-C PD receptacle on a small board; 6 wires to PW J2: VBUS x 2, GND x 2, CC1, CC2 (harness H1, notes/harness_bom.md)"
PWR_FLAG_NETS = ("PD_VBUS",)
NO_PWR_FLAG = ("+5V", "+3V3")
W, H = 32.0, 20.0
HOLES = [(3.5, H - 3.5), (W - 3.5, H - 3.5)]
LAYERS = 2
HOLE_CLEARANCE = 0.15       # the GCT USB4105 footprint (KiCad library, from the GCT drawing) has its NPTH pegs 0.19 mm from the GND pads (JLC: NPTH to copper 0.15 mm is fine)
R0402, C0402 = K.R0402, K.C0402
HDR = "Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical"


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "J": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    pins = {"A1": "GND", "B1": "GND", "A12": "GND", "B12": "GND", "A4": "PD_VBUS", "B4": "PD_VBUS", "A9": "PD_VBUS", "B9": "PD_VBUS",
            "A5": "PD_CC1", "B5": "PD_CC2", "A6": None, "B6": None, "A7": None, "B7": None, "A8": None, "B8": None, "SH": "SHIELD"}
    add(ref("J"), "Connector:USB_C_Receptacle_USB2.0_16P", "USB4105-GF-A", "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal", pins,
        LCSC="C3020560", Note="GCT USB4105-GF-A, 16P top-mounted horizontal, 5 A, 13495 pcs at JLC 19.11.2026; D+, D-, SBU unused")
    add(ref("J"), "Connector_Generic:Conn_01x06", "to PW J2", HDR, {"1": "PD_VBUS", "2": "PD_VBUS", "3": "GND", "4": "GND", "5": "PD_CC1", "6": "PD_CC2"},
        Note="solder pads for the harness H1: same order as PW 'USB-C Power in' (Micro-Fit 2x3): VBUS x 2, GND x 2, CC1, CC2; VBUS and GND 20 AWG, CC 24 AWG, 12 cm")
    add(ref("R"), "Device:R", "1M", R0402, {"1": "SHIELD", "2": "GND"}, LCSC="C26083", Note="shield bleed")
    add(ref("C"), "Device:C", "1n", C0402, {"1": "SHIELD", "2": "GND"}, LCSC="C1523", Note="shield HF return")
    K.mount_holes(add, ref, HOLES, "M3 to the rear wall stand-offs")
    return P


def placement():
    fixed = K.hole_fixed(parts(), HOLES)
    import packer
    P = parts()
    byref = {q["ref"]: q for q in P}
    box, _ = packer._bbox(sys.modules[__name__], byref["J2"], 90, "top")
    fixed["J1"] = (W / 2, H - 5.5, 0, "top")                        # receptacle at the bottom edge, courtyard bottom on the edge
    fixed["J2"] = (round(W / 2 - (box[2] - box[0]) / 2 - box[0], 2), round(4.0 - box[1], 2), 90, "top")   # solder pads in a row along the top
    fixed["R1"] = (6.5, 11.0, 90, "top")
    fixed["C1"] = (25.5, 11.0, 90, "top")
    return fixed


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    print(len(P), "parts,", len(nets), "nets")
