#!/usr/bin/env python3
"""Build the PT board (placed, nets, no routing) with the shared board writer.
Run: python3 make_pcb.py   (KiCad 10 PC: KICAD_FOOTPRINT_DIR=<KiCad>/share/kicad/footprints)   License: AGPL-3.0-or-later.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import design as D  # noqa: E402
import module_pcb  # noqa: E402

if __name__ == "__main__":
    module_pcb.main(D, [(f"PT pad test rev {D.REV}", (30.0, 102.5)), ("Shtuka Druka CERN-OHL-S-2.0", (95.0, 102.5))], HERE)
    # the light slots under the pads are routed inside the board: copper keeps 0.2 mm from them (LED pads, JLCPCB minimum for routed edges)
    pro = os.path.join(HERE, "..", D.NAME + ".kicad_pro")
    with open(pro, encoding="utf-8") as f:
        j = json.load(f)
    j["board"]["design_settings"]["rules"]["min_copper_edge_clearance"] = 0.2
    with open(pro, "w", encoding="utf-8") as f:
        json.dump(j, f, indent=2)
