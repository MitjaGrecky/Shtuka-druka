"""R2b - Jack shelf under R2 (R139): the right-angle rear jacks that cannot face outwards from the vertical R2 -
MIDI DIN 2 in / 4 out, rear USB-C to the PC (passed to A1's port B), rear USB-A (passed to the Mini-ITX), power jacks
(USB-C PD 5 A, DC 12-24 V, passed to PW). A horizontal board at the bottom of the rear wall, jacks in one row, joined to
R2 by a 2x7 comb that carries only the MIDI DIN lines. The MIDI parts (CA-033 resistors, optos) stay on R2;
USB and power go from here straight to A1, the Mini-ITX and PW, not through R2.
Single source of truth for the schematic. Decisions: R139, R140; research docs/ru/34_rear_boards_research.md, handoff #20.

Rev 0.1 (14.11.2026) = schematic. Outline and jack positions follow the rear panel v2 (tools/rear_panel.py).
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "r2b-jacks"
ID = "R2b"
TITLE = "R2b - Jack shelf under R2: MIDI DIN, USB-C PC, USB-A, USB-C PD, DC"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("R139: right-angle jacks in one row on a horizontal shelf; 2x7 comb to R2 = MIDI DIN lines only; "
            "USB-C PC -> A1 port B, USB-A -> Mini-ITX, USB-C PD and DC -> PW")
PWR_FLAG_NETS = ("UA_VBUS",)           # ERC: USB-A VBUS comes from the Mini-ITX header
NO_PWR_FLAG = ("+5V", "+3V3")          # no logic supply on this board
W, H = 240.0, 30.0                     # rough: x 5-245 of the rear view (panel v2), depth to the wall; refined with the board
LAYERS = 2

DIN5 = ""   # footprint for CUI SDS-50J is drawn with the board (EasyEDA has CONN-TH_SDS-50J); empty keeps ERC clean
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"

# 2x7 comb R2b <-> R2: DIN out k pins 4/5, DIN in k pins 4/5, GND (same numbering on R2)
COMB = {"1": "MO1_4", "2": "MO1_5", "3": "MO2_4", "4": "MO2_5", "5": "MO3_4", "6": "MO3_5", "7": "MO4_4", "8": "MO4_5",
        "9": "MI1_4", "10": "MI1_5", "11": "MI2_4", "12": "MI2_5", "13": "GND", "14": "GND"}


def parts():
    P = []
    n = {"R": 0, "U": 0, "J": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def R(value, a, b, **f):
        K.rc(add, ref("R"), value, a, b, **f)

    # ---------------------------------------------------------------- comb to R2
    add(ref("J"), "Connector_Generic:Conn_02x07_Odd_Even", "to R2", "Connector_PinHeader_2.54mm:PinHeader_2x07_P2.54mm_Vertical",
        COMB, Note="R139: comb to the vertical R2 (socket on R2); MIDI DIN lines only")

    # ---------------------------------------------------------------- MIDI DIN (CUI SDS-50J, right angle)
    for k in range(4):
        add(ref("J"), "Connector:DIN-5", f"MIDI OUT {k + 1}", DIN5,
            {"1": None, "2": "GND", "3": None, "4": f"MO{k + 1}_4", "5": f"MO{k + 1}_5"}, LCSC="C6216157",
            Note="CUI SDS-50J right angle; 33 R / 10 R (CA-033) on R2")
    for k in range(2):
        add(ref("J"), "Connector:DIN-5", f"MIDI IN {k + 1}", DIN5,
            {"1": None, "2": None, "3": None, "4": f"MI{k + 1}_4", "5": f"MI{k + 1}_5"}, LCSC="C6216157",
            Note="CUI SDS-50J right angle; pin 2 not connected on a receiver (CA-033); opto on R2")

    # ---------------------------------------------------------------- rear USB-C (PC) -> A1 port B
    add(ref("J"), "Connector:USB_C_Receptacle_USB2.0_14P", "USB-C PC", "Connector_USB:USB_C_Receptacle_HRO_TYPE-C-31-M-12",
        {"A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "A4": "PC_VBUS", "A9": "PC_VBUS", "B4": "PC_VBUS", "B9": "PC_VBUS",
         "A5": "PC_CC1", "B5": "PC_CC2", "A6": "PC_DP", "B6": "PC_DP", "A7": "PC_DM", "B7": "PC_DM", "SH": "GND"},
        LCSC="C165948", Note="R80/R82: USB audio to an external computer; isolated on A1 (ADuM4166); data only, no power drawn")
    R("5.1k", "PC_CC1", "GND", Note="device (Rd)")
    R("5.1k", "PC_CC2", "GND", Note="device (Rd)")
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", "Package_TO_SOT_SMD:SOT-23-6",
        {"1": "PC_DP", "6": "PC_DP", "3": "PC_DM", "4": "PC_DM", "2": "GND", "5": "PC_VBUS"}, LCSC="C323793")
    add(ref("J"), "Connector_Generic:Conn_01x04", "to A1 port B", PH.format(n=4),
        {"1": "PC_VBUS", "2": "PC_DM", "3": "PC_DP", "4": "GND"}, Note="cable to A1: ADuM4166 side of the PC")

    # ---------------------------------------------------------------- rear USB-A <- Mini-ITX
    add(ref("J"), "Connector:USB_A", "USB-A rear", "Connector_USB:USB_A_Molex_67643_Horizontal",
        {"1": "UA_VBUS", "2": "UA_DM", "3": "UA_DP", "4": "GND", "SH": "GND"}, Note="R80: storage and firmware, straight to the Mini-ITX")
    add(ref("U"), "Power_Protection:USBLC6-2SC6", "USBLC6-2SC6", "Package_TO_SOT_SMD:SOT-23-6",
        {"1": "UA_DP", "6": "UA_DP", "3": "UA_DM", "4": "UA_DM", "2": "GND", "5": "UA_VBUS"}, LCSC="C323793")
    add(ref("J"), "Connector_Generic:Conn_01x04", "USB-A to Mini-ITX", PH.format(n=4),
        {"1": "UA_VBUS", "2": "UA_DM", "3": "UA_DP", "4": "GND"}, Note="cable to a Mini-ITX USB header")

    # ---------------------------------------------------------------- power jacks -> PW
    add(ref("J"), "Connector:USB_C_Receptacle_USB2.0_16P", "USB-C PD 5 A", "Connector_USB:USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal",
        {"A1": "GND", "A12": "GND", "B1": "GND", "B12": "GND", "A4": "VBUS_PD", "A9": "VBUS_PD", "B4": "VBUS_PD", "B9": "VBUS_PD",
         "A5": "PD_CC1", "B5": "PD_CC2", "A6": None, "B6": None, "A7": None, "B7": None, "A8": None, "B8": None, "SH": "GND"},
        LCSC="C3025063", Note="R59/R72: GCT USB4105-GF-A-060, 5 A 20 V (task #20); the PD sink TPS25730 sits on PW")
    add(ref("J"), "Connector:Barrel_Jack_Switch", "DC 12-24 V", "Connector_BarrelJack:BarrelJack_CUI_PJ-063AH_Horizontal",
        {"1": "DC_IN", "2": "GND", "3": None},
        Note="R72: locking right-angle DC jack 12-24 V 5 A - part to choose with the board (PJ-063AH footprint is a placeholder)")
    add(ref("J"), "Connector_Generic:Conn_02x05_Odd_Even", "to PW", "Connector_PinHeader_2.54mm:PinHeader_2x05_P2.54mm_Vertical",
        {"1": "VBUS_PD", "2": "VBUS_PD", "3": "DC_IN", "4": "DC_IN", "5": "GND", "6": "GND", "7": "GND", "8": "GND",
         "9": "PD_CC1", "10": "PD_CC2"}, Note="power inputs to PW (protection, PD, source selection there); 5 A: 2 pins per rail")
    return P


def placement():
    """Rev 0.1 is the schematic only: the board follows the rear panel v2."""
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
