"""BB1 - battery board (P143, R208): one long board (398 x 28 mm, P144) along the ends of the three cell blocks under the pads. It joins all 6 Ampul cells (8 Ah, solder pads for the wires, P146),
makes two 3S packs (pack A = cell 1 of blocks 1, 2, 3 in series, pack B the same) with one BQ7791500 protection each (the circuit of bm_circuit.py, from the former hardware/bm-bms3s, reused, nets suffixed _A / _B),
and gives two Micro-Fit 2x3 outputs to PW (BAT+ x 2, GND x 2, NTC, GND, the harness of PW Battery 1 / 2) and four NTC sockets (JST GH-class 1.25 mm latching, 103AT 10k: one per BQ chip, one per charger of PW).
BM boards 38 x 38 mm are cancelled (P143). 2 layers, 2 oz copper (8 A: tracks >= 3 mm on 2 oz by IPC-2152, set at routing), 3 mm standoffs.
Board coordinates: x = model x - 104 (0-398), y = model y - 156 (0-28); the cells are on the y < 0 side (model y <= 153), the wires of the cells come to the connectors at y 3-11.
Source of the positions: model3d/batt_bays/under_pads.csv (P144; blocks x 104-234, 238-368, 372-502). Rev 0.3 (21.11.2026, P146): wire pads instead of XT60PW, GH-class NTC sockets. Rev 0.4 (25.11.2026, P150): the protection circuit lives in gen/bm_circuit.py (archive removed); cell tracks for 8 A. License: CERN-OHL-S-2.0, AGPL-3.0-or-later.
"""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "bb1-battery"
ID = "BB1"
TITLE = "BB1 - battery board: 6 cell wire pads, 2 x BQ7791500 protection, 2 outputs to PW"
REV = "0.4"
M1_LIB = K.M1_LIB
BUS_NOTE = ("6 cells (solder pads): pack A = cells 1, 3, 5, pack B = cells 2, 4, 6, 3S each; two BQ7791500 protections (bm-bms3s circuit); outputs J7 (A) and J8 (B) = PW Battery 1 / 2 "
            "(BAT+ x 2, GND x 2, NTC, GND); NTC sockets J9-J12 (chip A, chip B, PW A, PW B)")
PWR_FLAG_NETS = ("BAT_P_A", "BAT_N_A", "BAT_P_B", "BAT_N_B", "VDD_A", "VDD_B")
NO_PWR_FLAG = ("+5V", "+3V3", "GND")
W, H = 398.0, 28.0
HOLES = [(4.0, 3.5), (4.0, 24.5), (132.0, 3.5), (132.0, 24.5), (266.0, 3.5), (266.0, 24.5), (394.0, 3.5), (394.0, 24.5)]   # M3, ends and the ribs between the blocks (model x 235-237, 369-371 minus 104); assumed: the csv has no holes
LAYERS = 2

# cell connectors (model x centres of bb1_outline.csv minus 15): block 1 (x 42.5, 67.5), block 2 (217.5, 242.5), block 3 (417.5, 442.5); A = first, B = second of every block
CELL_X = ((52.5, "A"), (77.5, "B"), (186.5, "A"), (211.5, "B"), (320.5, "A"), (345.5, "B"))   # block centres 65, 199, 333 (model 169, 303, 437 minus 104) +- 12.5
WIRE = "ShtukaDruka:WirePads_2x_THT_P8.0mm_TieHoles"   # P146: solder pads for the cell wires, no power connectors
MF = "Connector_Molex:Molex_Micro-Fit_3.0_{}_P3.00mm_Horizontal"
GH = "Connector_JST:JST_GH_BM0{n}B-GHS-TBT_1x0{n}-1MP_P1.25mm_Vertical"   # P146: small latching 1.25 mm connector (JST GH class), series by the technologist
PW_X = {"A": 150.0, "B": 250.0}          # Micro-Fit 2x3 centres, between the blocks
BM_X = {"A": 112.0, "B": 266.0}          # the protection circuits between the cell connectors (gaps 85-175 and 219-309)


def _bm():
    spec = importlib.util.spec_from_file_location("bm_design", os.path.join(HERE, "bm_circuit.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def parts():
    bm = _bm()
    P = []
    n = {"J": 0, "H": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    # ---- cells: XT60PW-M, pin 1 = +, pin 2 = -; per pack the chain BAT_N - cell1 - B1 - cell2 - B2 - cell3 - BAT_P
    chain = {"A": [("BAT_N_A", "B1_A"), ("B1_A", "B2_A"), ("B2_A", "BAT_P_A")], "B": [("BAT_N_B", "B1_B"), ("B1_B", "B2_B"), ("B2_B", "BAT_P_B")]}
    seen = {"A": 0, "B": 0}
    for i, (x, s) in enumerate(CELL_X):
        lo, hi = chain[s][seen[s]]
        seen[s] += 1
        add(ref("J"), "Connector_Generic:Conn_01x02", f"Cell {i + 1} (pack {s})", WIRE, {"1": hi, "2": lo},
            Note=f"solder pads for the two wires of the Ampul cell (>= 1.0 mm2; 8 A = 1C of the pack: tracks >= 3 mm at 2 oz or pours, P155), wires fixed with a cable tie through the two 3 mm holes; cell {seen[s]} of pack {s}: + (pad 1) to {hi}, - (pad 2) to {lo}")
    # ---- two protection circuits from bm-bms3s (without its connectors and holes), nets and references suffixed
    for s in ("A", "B"):
        off = 0 if s == "A" else 100
        for p in bm.parts():
            r = p["ref"]
            if r.startswith(("J", "H")):
                continue
            q = dict(p)
            q["ref"] = r[0] + str(int(r[1:]) + off)
            q["pins"] = {k: (f"{v}_{s}" if v else v) for k, v in p["pins"].items()}
            P.append(q)
        add(ref("J"), "Connector_Generic:Conn_02x03_Odd_Even", f"to PW (Battery {1 if s == 'A' else 2})", MF.format("43045-0600_2x03"),
            {"1": f"BAT_P_{s}", "2": f"BAT_P_{s}", "3": f"PACK_N_{s}", "4": f"PACK_N_{s}", "5": f"NTC_PW_{s}", "6": f"PACK_N_{s}"},
            LCSC="C127367", Note=f"right-angle Micro-Fit 43045-0600 (C127367), PW Battery {1 if s == 'A' else 2} harness: BAT+ x 2, GND x 2, NTC, GND; 8 A: 2 contacts per pole")
    for s in ("A", "B"):
        add(ref("J"), "Connector_Generic:Conn_01x02", f"NTC chip {s}", GH.format(n=2), {"1": f"TS_{s}", "2": f"BAT_N_{s}"},
            Note=f"103AT 10k (B 3435) NTC of the BQ7791500 of pack {s} (on the cell of block 2): TS input, 45 C stops charging in the chip")
    for s in ("A", "B"):
        add(ref("J"), "Connector_Generic:Conn_01x02", f"NTC PW {s}", GH.format(n=2), {"1": f"NTC_PW_{s}", "2": f"PACK_N_{s}"},
            Note=f"103AT 10k NTC of pack {s} for the BQ25798 TS of PW (a separate thermistor: the charger biases it itself)")
    K.mount_holes(add, ref, HOLES, "M3 on the 3 mm standoffs; positions assumed (the outline csv has none), check with the designer")
    return P


def placement():
    """Cell connectors along the cell side (y 7), PW outputs and NTC sockets on the back side, the protections packed around their anchors between the blocks."""
    import packer
    P = parts()
    fixed = K.hole_fixed(P, HOLES)
    j = {p["value"]: p["ref"] for p in P if p["ref"].startswith("J")}
    for i, (x, s) in enumerate(CELL_X):
        fixed[j[f"Cell {i + 1} (pack {s})"]] = (x, 7.0, 0, "top")
    for s in ("A", "B"):
        fixed[j[f"to PW (Battery {1 if s == 'A' else 2})"]] = (PW_X[s], 20.0, 180, "top")
    ntc = {"NTC chip A": 25.0, "NTC chip B": 373.0, "NTC PW A": 35.0, "NTC PW B": 363.0}
    for name, x in ntc.items():
        fixed[j[name]] = (x, 23.0, 180, "top")
    G = []
    for s in ("A", "B"):
        refs = [p["ref"] for p in P if p["ref"] not in fixed and any(str(v).endswith(f"_{s}") for v in p["pins"].values())]
        G.append((BM_X[s], 14.0, "top", refs, 0))
    return packer.pack(sys.modules[__name__], P, fixed, G, [(0, 0, W, H)], gap=float(os.environ.get("PLACE_GAP", "0.4")), rmax=60.0)


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
