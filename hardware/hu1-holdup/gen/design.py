"""HU1 - hold-up module for the +-14 V audio rails (P129, P130, R202): 4 x 470 uF 25 V aluminium electrolytics next to the PW board on a short harness.
On a loss of all power the +-14 V rails (before the TPS7A47 / TPS7A33 LDOs of the +-12 V) must keep the audio boards alive for >= 6 ms, until the output relays have opened
(G6K <= 3 ms + PM_ALERT about 1 ms): tasks/12 of the team folder: 0.29-0.43 A per rail, dV 2.5 V (14 V -> 11.5 V) -> 0.7-1.0 mF per rail.
Each rail: 2 x 470 uF behind 10 ohm (charge, inrush 1.4 A instead of 3.5 A: the LMR33640 has a 4 ms soft start, a 3.9-5 A low-side limit and takes at most about 1000 uF at its
output, datasheet 9.2.2) with a Schottky SS34 across it in the discharge direction (the storage feeds the rail when it sags; drop 0.3-0.4 V -> 4.8 ms at 0.43 A, 7.1 ms at 0.29 A).
P14: R 10 ohm P14 -> P14_ST, D anode P14_ST, cathode P14; N14: mirrored (the capacitors are GND(+) / N14_ST(-)).
Connector J1 Micro-Fit 3.0 1x3 (latching, 5 A per contact; the inrush peak 1.4 A, the load up to 0.43 A per rail): 1 P14, 2 GND, 3 N14, harness <= 80 mm to PW.
Rev 0.1 (21.11.2026): schematic and placed board, 2 layers, about 35 x 45 mm. License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "hu1-holdup"
ID = "HU1"
TITLE = "HU1 - hold-up module +-14 V: 4 x 470 uF 25 V, 2 x 10 ohm, 2 x SS34"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("Harness to PW (P14, GND, N14) J1; two electrolytics per rail behind 10 ohm with a Schottky in the discharge direction; "
            "hold-up of the +-14 V rails of the audio boards for >= 6 ms (tasks/12, P129, P130)")
PWR_FLAG_NETS = ("P14", "N14")   # ERC: nets that only a connector drives
NO_PWR_FLAG = ("+5V", "+3V3")
W, H = 35.0, 45.0
HOLES = [(3.5, 3.5), (W - 3.5, H - 3.5)]
LAYERS = 2

R1206 = "Resistor_SMD:R_1206_3216Metric"
CP10 = "Capacitor_SMD:CP_Elec_10x10.5"
SMA = "Diode_SMD:D_SMA"
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Vertical"


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "D": 0, "J": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    add(ref("J"), "Connector_Generic:Conn_01x03", "to PW (P14, GND, N14)", MF.format("43650-0315_1x03"), {"1": "P14", "2": "GND", "3": "N14"},
        Note="Micro-Fit 3.0 1x3 vertical, latching (housing 43645-0300): P14, GND, N14 from the PW 'to HU1' connector, harness <= 80 mm, AWG 20")
    for rail, plus, minus, rs, anode, cathode in (("P14", "P14_ST", "GND", ("P14", "P14_ST"), "P14_ST", "P14"), ("N14", "GND", "N14_ST", ("N14", "N14_ST"), "N14", "N14_ST")):
        for _ in range(2):
            add(ref("C"), "Device:C_Polarized", "470u 25V", CP10, {"1": plus, "2": minus},
                Note=f"hold-up storage {rail}: aluminium electrolytic 105 C, 10 x 10.5 mm, 25 V (technologist: part; ESR is no concern here)")
        add(ref("R"), "Device:R", "10", R1206, {"1": rs[0], "2": rs[1]},
            Note=f"{rail} storage charge resistor: inrush 1.4 A instead of 3.5 A at 14 V (LMR33640: soft start 4 ms, low-side limit 3.9-5 A); pulse only")
        add(ref("D"), "Device:D_Schottky", "SS34", SMA, {"1": cathode, "2": anode}, LCSC="C8678",
            Note=f"{rail} storage discharge diode: the storage feeds the rail when it sags (drop 0.3-0.4 V); 40 V 3 A; check the part number and stock")
    K.mount_holes(add, ref, HOLES, "M3 standoff; the final positions come with the enclosure model")
    return P


def placement():
    """Connector at the top edge; capacitors, resistors and diodes are packed around the board centre (packer.py, no autoplace: there is no IC to anchor)."""
    import packer
    P = parts()
    fixed = K.hole_fixed(P, HOLES)
    fixed["J1"] = (W / 2, 9.0, 0, "top")
    rest = [p["ref"] for p in P if p["ref"] not in fixed]
    big = [r for r in rest if r.startswith("C")]
    anchors = [(9.2, 21.3), (25.8, 21.3), (9.2, 34.9), (25.8, 34.9)]       # capacitors turned 90 deg: 11 mm wide, 13.4 mm high, a 2 x 2 block under the connector
    G = [(ax, ay, "top", [c], 90) for (ax, ay), c in zip(anchors, big)] + [(W / 2, 43.0, "top", [r for r in rest if r not in big], 0)]
    return packer.pack(sys.modules[__name__], P, fixed, G, [(0, 0, W, H)], gap=float(os.environ.get("PLACE_GAP", "0.6")))


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    print(len(P), "parts,", len(nets), "nets")
