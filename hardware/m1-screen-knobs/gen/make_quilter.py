#!/usr/bin/env python3
"""Input files for Quilter (quilter.ai), two jobs:

  A_route_only       - our placement; Quilter only routes (every part sits inside the outline,
                       and Quilter keeps parts inside the outline where they are)
  B_place_and_route  - only what the panel fixes is inside the outline (encoders, ring LEDs, J1,
                       mounting holes); ICs and passives wait below the board for Quilter to place

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


def main(out):
    for job in ("A_route_only", "B_place_and_route"):
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
        path = os.path.join(d, D.NAME + ".kicad_pcb")
        b.Save(path)
        for ext in (".kicad_sch", ".kicad_pro"):
            shutil.copy(os.path.join(M.PROJ, D.NAME + ext), os.path.join(d, D.NAME + ext))
        print("ok", path)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "quilter"))
