#!/usr/bin/env python3
"""Quick geometric checks of a placed, unrouted board without kicad-cli (the PC must not run kicad-cli):
courtyard overlaps per side, footprints whose courtyard leaves the outline (except the jack faces on an edge, listed
with --edge-ok), pads closer than 0.3 mm to the outline, pads of different footprints closer than the clearance.

Usage: pcb_geomcheck.py BOARD.kicad_pcb [--edge-ok J1,J2,...] [--clear 0.2]      License: AGPL-3.0-or-later.
"""
import argparse
import itertools
import sys

import pcbnew


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("board")
    ap.add_argument("--edge-ok", default="", help="refs allowed to reach over the outline (jacks on a panel edge)")
    ap.add_argument("--clear", type=float, default=0.2)
    a = ap.parse_args()
    b = pcbnew.LoadBoard(a.board)
    mm = pcbnew.FromMM
    edge_ok = set(filter(None, a.edge_ok.split(",")))
    outline = pcbnew.SHAPE_POLY_SET()
    try:
        b.GetBoardPolygonOutlines(outline, True)
    except TypeError:
        b.GetBoardPolygonOutlines(outline)
    fps = list(b.GetFootprints())
    errors = 0
    for side, layer in (("top", pcbnew.F_CrtYd), ("bottom", pcbnew.B_CrtYd)):
        cy = [(f.GetReference(), f.GetCourtyard(layer)) for f in fps if f.GetCourtyard(layer).OutlineCount()]
        for (ra, pa), (rb, pb) in itertools.combinations(cy, 2):
            x = pcbnew.SHAPE_POLY_SET(pa)
            x.BooleanIntersection(pb)
            if x.Area() > mm(0.01) ** 2 * 1:
                print(f"courtyard overlap {side}: {ra} / {rb} ({x.Area() / mm(1) ** 2:.2f} mm2)")
                errors += 1
        for r, p in cy:
            out = pcbnew.SHAPE_POLY_SET(p)
            out.BooleanSubtract(outline)
            if out.Area() > mm(0.05) ** 2 and r not in edge_ok:
                print(f"courtyard outside the outline: {r} ({out.Area() / mm(1) ** 2:.2f} mm2)")
                errors += 1
    edges = [s for s in b.GetDrawings() if s.GetLayer() == pcbnew.Edge_Cuts]

    def lay(p):
        return pcbnew.F_Cu if p.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu
    pads = [(f.GetReference(), p) for f in fps for p in f.Pads()]
    for r, p in pads:
        sh = p.GetEffectiveShape(lay(p))
        for e in edges:
            d = sh.Collide(e.GetEffectiveShape(), mm(0.3))
            if d:
                print(f"pad near the edge (< 0.3 mm): {r}.{p.GetNumber() or '-'}")
                errors += 1
                break
    for (ra, pa), (rb, pb) in itertools.combinations(pads, 2):
        if ra == rb:
            continue
        if pa.GetBoundingBox().Distance(pb.GetPosition()) > mm(15):
            continue
        common = [ly for ly in (pcbnew.F_Cu, pcbnew.B_Cu) if pa.IsOnLayer(ly) and pb.IsOnLayer(ly)]
        if not common:
            continue
        ly = common[0]
        if pa.GetEffectiveShape(ly).Collide(pb.GetEffectiveShape(ly), mm(a.clear)) and \
                (pa.GetNetCode() != pb.GetNetCode() or pa.GetNetCode() == 0):
            print(f"pads closer than {a.clear} mm: {ra}.{pa.GetNumber() or '-'} / {rb}.{pb.GetNumber() or '-'}")
            errors += 1
    print(f"{len(fps)} footprints, {len(pads)} pads: {errors} problems")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
