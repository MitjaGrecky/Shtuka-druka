#!/usr/bin/env python3
"""Input files for Quilter (quilter.ai), three jobs:

  A_route_only       - our placement; Quilter only routes (every part sits inside the outline,
                       and Quilter keeps parts inside the outline where they are)
  B_place_and_route  - only what the panel fixes is inside the outline (encoders, ring LEDs, J1,
                       mounting holes); ICs and passives wait below the board for Quilter to place
  C_small_parts_free - ICs (U1-U5) stay where we put them, inside the outline: Quilter treats parts
                       inside the outline as pre-placed and they anchor their passives. Resistors,
                       capacitors and arrays (37 parts) wait below the board and Quilter places them
                       next to their ICs: on the bottom, or on the top inside two free strips only
                       (see TOP_STRIPS). Encoders, ring LEDs, J1, holes and ICs stay fixed.

Rev 0.2 (job D, route only): the cathode arcs and vias of the LED rings are drawn by make_pcb and locked,
Quilter routes the rest. No other tracks, no bottom pour. The In1 plane is renamed "GND" so Quilter recognises it.
Keep-outs under the encoder bodies (touch electrodes) are rule areas Quilter respects.
Run with KiCad's Python: python3 make_quilter.py OUT_DIR
License: AGPL-3.0-or-later.
"""
import math
import os
import shutil
import sys

import pcbnew

import design as D
import make_pcb as M

FIXED = ("ENC", "D", "J", "H")


def placement_region(b, top_keepout=True):
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
    if not top_keepout:
        return
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


# Top-side strips where small SMD parts may sit (job C). Found from the free-space map: rings (LED +
# 2 mm guide wall), encoder cut-outs (+0.8 mm) and screw heads (r 3.5 mm) are blocked, the rest of the
# top is free. The light guide gets a groove from below over these strips; every part there is <= 1.2 mm
# (0402, 0805, TSSOP-16) and the guide is 6.4 mm thick. 7 x 7 mm U1 and TSSOP legs (6.4 mm) do not fit
# the 5.1 mm rear strip, so ICs stay on the back.
TOP_STRIPS = {"Top strip rear": (6.3, 0.8, D.W - 6.3, 5.9), "Top strip front": (6.3, 30.8, D.W - 6.3, D.H - 0.8)}


def top_filter(b):
    """F.Cu: footprints are forbidden everywhere except the two strips (board rectangle minus strips),
    and the strips themselves are placement regions."""
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetLayer(pcbnew.F_Cu)
    for allow in (z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowCopperPour,
                  z.SetDoNotAllowPads):
        allow(False)
    z.SetDoNotAllowFootprints(True)
    z.SetZoneName("Top: locked parts only")
    rect(z)
    o = z.Outline()
    cut = pcbnew.SHAPE_POLY_SET()
    for x0, y0, x1, y1 in TOP_STRIPS.values():
        cut.NewOutline()
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            q = M.P(x, y)
            cut.Append(q.x, q.y)
    o.BooleanSubtract(cut, pcbnew.SHAPE_POLY_SET.PM_FAST)
    b.Add(z)
    for name, (x0, y0, x1, y1) in TOP_STRIPS.items():
        r = pcbnew.ZONE(b)
        r.SetIsRuleArea(True)
        r.SetLayer(pcbnew.F_Cu)
        for allow in (r.SetDoNotAllowTracks, r.SetDoNotAllowVias, r.SetDoNotAllowCopperPour,
                      r.SetDoNotAllowPads, r.SetDoNotAllowFootprints):
            allow(False)
        r.SetZoneName(name)
        o = r.Outline()
        o.NewOutline()
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            q = M.P(x, y)
            o.Append(q.x, q.y)
        b.Add(r)


def offboard_region(b, y0, y1):
    """Quilter placement region OFF the board (job H): parts assigned to it form a group that Quilter
    places anywhere, on the top OR the bottom (an off-board region has no side). Shape is ignored."""
    z = pcbnew.ZONE(b)
    z.SetIsRuleArea(True)
    z.SetLayer(pcbnew.B_Cu)
    for allow in (z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowCopperPour,
                  z.SetDoNotAllowPads, z.SetDoNotAllowFootprints):
        allow(False)
    z.SetZoneName("Free parts any side")
    o = z.Outline()
    o.NewOutline()
    for x, y in ((0, y0), (D.W, y0), (D.W, y1), (0, y1)):
        q = M.P(x, y)
        o.Append(q.x, q.y)
    b.Add(z)


def encoder_part_keepouts(b, m=0.5):
    """B.Cu rule areas that forbid footprints under each encoder (job I). Job H put U2 and its passives
    under ENC4 on the back: inside the track keep-out (touch electrode), so its pads could not be reached.
    Quilter respects keep-outs on F.Cu/B.Cu. Area = encoder courtyard (the body and its THT pins) + m."""
    for fp in b.GetFootprints():
        if not fp.GetReference().startswith("ENC"):
            continue
        bb = fp.GetCourtyard(pcbnew.F_CrtYd).BBox()
        z = pcbnew.ZONE(b)
        z.SetIsRuleArea(True)
        ls = pcbnew.LSET()
        ls.AddLayer(pcbnew.B_Cu)
        z.SetLayerSet(ls)
        for allow in (z.SetDoNotAllowTracks, z.SetDoNotAllowVias, z.SetDoNotAllowCopperPour, z.SetDoNotAllowPads):
            allow(False)
        z.SetDoNotAllowFootprints(True)
        z.SetZoneName(f"no_parts_under_{fp.GetReference()}")
        o = z.Outline()
        o.NewOutline()
        d = pcbnew.FromMM(m)
        for x, y in ((bb.GetLeft() - d, bb.GetTop() - d), (bb.GetRight() + d, bb.GetTop() - d),
                     (bb.GetRight() + d, bb.GetBottom() + d), (bb.GetLeft() - d, bb.GetBottom() + d)):
            o.Append(int(x), int(y))
        b.Add(z)


def inner_track_keepouts(b):
    """Job F routed 61 tracks on In2 under the encoders although the all-layer rule areas forbid it (F and B
    were respected). Job I adds a copy of each area on In2 alone, in case Quilter reads only one layer of a rule area."""
    for z0 in list(b.Zones()):
        if not z0.GetZoneName().startswith("under_encoder_"):
            continue
        z = pcbnew.ZONE(b)
        z.SetIsRuleArea(True)
        ls = pcbnew.LSET()
        ls.AddLayer(pcbnew.In2_Cu)
        z.SetLayerSet(ls)
        z.SetDoNotAllowTracks(True)
        z.SetDoNotAllowVias(True)
        z.SetDoNotAllowCopperPour(True)
        z.SetDoNotAllowPads(False)
        z.SetDoNotAllowFootprints(False)
        z.SetZoneName(z0.GetZoneName() + "_In2")
        z.Outline().Append(z0.Outline())
        b.Add(z)


def rect(z, m=0.5):
    o = z.Outline()
    o.NewOutline()
    for x, y in ((m, m), (D.W - m, m), (D.W - m, D.H - m), (m, D.H - m)):
        q = M.P(x, y)
        o.Append(q.x, q.y)


# Circuit Comprehension tables for Quilter (upload with "Upload CSV" instead of editing its grid).
# Column names follow Quilter's own CSV export; capacitance in nF, current in mA.
BYPASS = [  # capacitor, bypassed component, pin, nF (rev 0.2: two LED drivers U1, U6)
    ("C1", "U1", 15, 4700), ("C2", "U1", 15, 1000), ("C3", "U1", 14, 100), ("C4", "U1", 25, 100),
    ("C14", "U6", 15, 4700), ("C15", "U6", 15, 1000), ("C16", "U6", 14, 100), ("C17", "U6", 25, 100),
    ("C18", "U7", 15, 4700), ("C19", "U7", 15, 1000), ("C20", "U7", 14, 100), ("C21", "U7", 25, 100),
    ("C22", "U8", 15, 4700), ("C23", "U8", 15, 1000), ("C24", "U8", 14, 100), ("C25", "U8", 25, 100),
    ("C5", "U2", 3, 2.2), ("C6", "U2", 4, 100), ("C7", "U2", 5, 1000), ("C8", "U2", 6, 100),
    ("C9", "U3", 16, 100), ("C10", "U4", 16, 100), ("C11", "U5", 16, 100),
    ("C12", "J1", 1, 10000), ("C13", "J1", 5, 1000)]
if D.LP:     # LP5864 cell: VCC pin 1 (1u), VLED pin 15 (4.7u), VCAP pin 25 (1u), VIO_EN pin 32 (1n)
    BYPASS = [(c, D.DRIVER[cell], pin, nf) for cell in D.CELLS
              for c, pin, nf in zip(D.CELL_REFS[cell]["caps"], (1, 15, 25, 32), (1000, 4700, 1000, 1))] + \
             [r for r in BYPASS if r[1] in ("U2", "U3", "U4", "U5", "J1")]
POWER = [("+5V", 800), ("GND", 800), ("+3V3", 100), ("/VREG", 50)] + \
        ([(f"/{c}_SW{k}", 300) for c in D.CELLS for k in range(4)] if D.LP else   # LP5864 SW: 6 LEDs x 3 CS x 15 mA = 270 mA
         [(f"/{c}_SW{k}", 700 if D.ONE_CHIP else 250 if D.FOUR else 350) for c in D.CELLS for k in range(1, 8 if D.FOUR else 10)])   # anode rows: CS x 19 mA (18 per cell, 36 for one chip)


def bypass():
    have = {p["ref"] for p in D.parts()}
    return [r for r in BYPASS if r[0] in have and r[1] in have]


def write_csv(d):
    rows = {
        "bypass_capacitors.csv": ["capacitor,bypassed_component,bypassed_pin,capacitance"] +
                                 [f"{c},{u},{p},{nf:g}" for c, u, p, nf in bypass()],
        "high_current_nets.csv": ["net_name,max_current,use_power_pour"] +
                                 [f"{n},{ma},false" for n, ma in POWER],
        "ground_nets.csv": ["net_name,is_primary,use_region_pour", "GND,true,false"],
    }
    for name, lines in rows.items():
        with open(os.path.join(d, name), "w", newline="\n") as f:
            f.write("\n".join(lines) + "\n")



def arcs_to_chords(b, n=8):
    """Quilter failed on PCB_ARC objects (jobs D, 06.11); replace each locked arc by n straight chords."""
    for t in list(b.GetTracks()):
        if t.Type() != pcbnew.PCB_ARC_T:
            continue
        c, r = t.GetCenter(), t.GetRadius()
        a0 = t.GetArcAngleStart().AsRadians()
        da = t.GetAngle().AsRadians()
        net, layer, w = t.GetNet(), t.GetLayer(), t.GetWidth()
        pts = [pcbnew.VECTOR2I(int(c.x + r * math.cos(a0 + da * i / n)), int(c.y + r * math.sin(a0 + da * i / n))) for i in range(n + 1)]
        pts[0], pts[-1] = t.GetStart(), t.GetEnd()
        b.Remove(t)
        for p1, p2 in zip(pts, pts[1:]):
            s = pcbnew.PCB_TRACK(b)
            s.SetStart(p1); s.SetEnd(p2); s.SetLayer(layer); s.SetNet(net); s.SetWidth(w); s.SetLocked(True)
            b.Add(s)

JOBS = ("L_rev05_lp5864",) if D.LP else ("K_rev04_four_drivers",) if D.FOUR else ("J2_rev031_one_chip",) if D.ONE_CHIP else ("I2_rev031_two_chips",)   # rev 0.3.1 (07.11 evening); before: I_rev03_fanout_free, J_rev03_one_chip_diamond  # rev 0.3; earlier H_free_any_side (U2 landed under ENC4), D/F/G  # earlier: D_rev02_route_only, F_chords_route_only, G_chords_place_and_route            # rev 0.2 (P98): our placement, ring arcs pre-drawn and locked; A-C were rev 0.1


def main(out):
    for job in JOBS:
        d = os.path.join(out, job)
        os.makedirs(d, exist_ok=True)
        b = M.build()
        b.SetLayerName(pcbnew.In1_Cu, "GND")
        b.SetLayerName(pcbnew.In2_Cu, "Signal")
        if job[0] in "BG":
            free = [fp for fp in b.GetFootprints() if not fp.GetReference().startswith(FIXED)]
            for n, fp in enumerate(sorted(free, key=lambda f: f.GetReference())):
                fp.SetLocked(False)
                x, y = 4 + 8 * (n % 26), D.H + 8 + 8 * (n // 26)   # rows under the board
                fp.SetPosition(M.P(x, y))
            placement_region(b)
        if job.startswith("C"):
            # ICs stay where we put them (anchors, inside the outline); only resistors, capacitors and
            # arrays wait below the board and are placed by Quilter next to their ICs (schematic clustering)
            passives = [fp for fp in b.GetFootprints() if fp.GetReference().rstrip("0123456789") in ("R", "C", "RN")]
            for n, fp in enumerate(sorted(passives, key=lambda f: f.GetReference())):
                fp.SetLocked(False)
                fp.SetPosition(M.P(4 + 8 * (n % 26), D.H + 8 + 8 * (n // 26)))
            for fp in b.GetFootprints():
                if fp.GetReference().startswith("U"):
                    fp.SetLocked(True)
            top_filter(b)                            # top side: only the two free strips
        if job[0] in "HIJKL":
            # 07.11, user: everything except the panel parts may move, on either side; Quilter decides
            keep = FIXED + (tuple(D.DRIVER.values()) if job[0] in "IJKL" else ())   # rev 0.3: drivers stay with their fan-out
            free = [fp for fp in b.GetFootprints() if not fp.GetReference().startswith(keep)
                    or (fp.GetReference().startswith("U") and fp.GetReference() not in keep)]
            for n, fp in enumerate(sorted(free, key=lambda f: f.GetReference())):
                fp.SetLocked(False)
                fp.SetPosition(M.P(4 + 8 * (n % 26), D.H + 8 + 8 * (n // 26)))
            offboard_region(b, D.H + 4, D.H + 8 + 8 * (len(free) // 26 + 1))
        if job[0] in "IJKL":
            encoder_part_keepouts(b)
            inner_track_keepouts(b)
        if job[0] in "FGHIJKL":
            arcs_to_chords(b)
        path = os.path.join(d, D.NAME + ".kicad_pcb")
        M.save(b, path)
        for ext in (".kicad_sch", ".kicad_pro"):
            shutil.copy(os.path.join(M.PROJ, D.NAME + ext), os.path.join(d, D.NAME + ext))
        if D.ONE_CHIP or D.FOUR:                         # (FOUR includes LP) its own schematic (one driver), not the repo's
            import make_sch
            make_sch.OUT = os.path.join(d, D.NAME + ".kicad_sch")
            make_sch.main()
        write_csv(d)
        print("ok", path)


if __name__ == "__main__":
    main(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "quilter"))
