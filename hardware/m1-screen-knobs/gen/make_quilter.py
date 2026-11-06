#!/usr/bin/env python3
"""Input files for Quilter (quilter.ai), three jobs:

  A_route_only       - our placement; Quilter only routes (every part sits inside the outline,
                       and Quilter keeps parts inside the outline where they are)
  B_place_and_route  - only what the panel fixes is inside the outline (encoders, ring LEDs, J1,
                       mounting holes); ICs and passives wait below the board for Quilter to place
  C_small_parts_free - A plus the placement filter: ICs and passives start where our layout put them
                       (inside the outline, bottom side) and may move, but only on the bottom side
                       (F.Cu footprint keep-out + B.Cu placement region). Encoders, ring LEDs, J1 and
                       mounting holes stay locked. Use this when A is too hard to route.

No tracks, no bottom pour. The In1 plane is renamed "GND" so Quilter recognises it.
Keep-outs under the encoder bodies (touch electrodes) are rule areas Quilter respects.
Run with KiCad's Python: python3 make_quilter.py OUT_DIR
License: AGPL-3.0-or-later.
"""
import os
import shutil
import sys

import pcbnew

import design as D
import make_pcb as M

FIXED = ("ENC", "D", "J", "H")


def placement_region(b):
    """Quilter placement region: a KiCad rule area with every keep-out item off,
    linked to the bottom copper. ICs and passives are assigned to it in Quilter by
    reference, so they stay on the back (the top belongs to encoders and LEDs)."""
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetLayer(pcbnew.B_Cu)
    for allow in (z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowCopperPour,
                  z.SetDoNotAllowPads, z.SetDoNotAllowFootprints):
        allow(False)
    z.SetZoneName("Bottom parts")
    rect(z)
    b.Add(z)
    # Quilter did not pick the region up from our KiCad 7 file, so the top side also gets a
    # footprint keep-out: nothing new may be placed there (the locked encoders and LEDs stay)
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetLayer(pcbnew.F_Cu)
    for allow in (z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowCopperPour,
                  z.SetDoNotAllowPads):
        allow(False)
    z.SetDoNotAllowFootprints(True)
    z.SetZoneName("Top no new parts")
    rect(z)
    b.Add(z)


def rect(z, m=0.5):
    o = z.Outline()
    o.NewOutline()
    for x, y in ((m, m), (D.W - m, m), (D.W - m, D.H - m), (m, D.H - m)):
        q = M.P(x, y)
        o.Append(q.x, q.y)


# Circuit Comprehension tables for Quilter (upload with "Upload CSV" instead of editing its grid).
# Column names follow Quilter's own CSV export; capacitance in nF, current in mA.
BYPASS = [  # capacitor, bypassed component, pin, nF
    ("C1", "U1", 15, 4700), ("C2", "U1", 15, 1000), ("C3", "U1", 14, 100), ("C4", "U1", 25, 100),
    ("C5", "U2", 3, 2.2), ("C6", "U2", 4, 100), ("C7", "U2", 5, 1000), ("C8", "U2", 6, 100),
    ("C9", "U3", 16, 100), ("C10", "U4", 16, 100), ("C11", "U5", 16, 100),
    ("C12", "J1", 1, 10000), ("C13", "J1", 5, 1000)]
POWER = [("+5V", 800), ("GND", 800), ("+3V3", 100), ("VREG", 50)]   # LED driver peak ~0.7 A


def write_csv(d):
    rows = {
        "bypass_capacitors.csv": ["capacitor,bypassed_component,bypassed_pin,capacitance"] +
                                 [f"{c},{u},{p},{nf:g}" for c, u, p, nf in BYPASS],
        "high_current_nets.csv": ["net_name,max_current,use_power_pour"] +
                                 [f"{n},{ma},false" for n, ma in POWER],
        "ground_nets.csv": ["net_name,is_primary,use_region_pour", "GND,true,false"],
    }
    for name, lines in rows.items():
        with open(os.path.join(d, name), "w", newline="\n") as f:
            f.write("\n".join(lines) + "\n")


def main(out):
    for job in ("A_route_only", "B_place_and_route", "C_small_parts_free"):
        d = os.path.join(out, job)
        os.makedirs(d, exist_ok=True)
        b = M.build()
        b.SetLayerName(pcbnew.In1_Cu, "GND")
        b.SetLayerName(pcbnew.In2_Cu, "Signal")
        if job.startswith("B"):
            free = [fp for fp in b.GetFootprints() if not fp.GetReference().startswith(FIXED)]
            for n, fp in enumerate(sorted(free, key=lambda f: f.GetReference())):
                fp.SetLocked(False)
                x, y = 4 + 8 * (n % 26), D.H + 8 + 8 * (n // 26)   # rows under the board
                fp.SetPosition(M.P(x, y))
            placement_region(b)
        if job.startswith("C"):
            placement_region(b)      # parts keep our positions; the filter only keeps them on the back
        path = os.path.join(d, D.NAME + ".kicad_pcb")
        b.Save(path)
        for ext in (".kicad_sch", ".kicad_pro"):
            shutil.copy(os.path.join(M.PROJ, D.NAME + ext), os.path.join(d, D.NAME + ext))
        write_csv(d)
        print("ok", path)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "quilter"))
