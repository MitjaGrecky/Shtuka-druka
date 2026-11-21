#!/usr/bin/env python3
# License: AGPL-3.0-or-later. Run with KiCad's python:
#   power_pour_in2.py IN.kicad_pcb OUT.kicad_pcb "/+12V,/-12V,+5V" [In2.Cu]
# P119 (20.11.2026): supply nets that were left out of the routing (like GND) are poured on an inner signal layer in the
# free areas after the signals are routed. Each net gets a zone over the hull of its pads (+4 mm), smaller hull = higher
# priority; then every pad of the net that does not reach its pour gets a via (0.6/0.3) next to it with a short stub on the
# pad's layer, placed clear of other-net copper on every layer and inside the net's pour. Run after the GND stage.
import math
import os
import sys

import pcbnew

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "hardware", "common", "gen"))
import routing as R  # noqa: E402

src, out, nets = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
layer_name = sys.argv[4] if len(sys.argv) > 4 else "In2.Cu"
b = pcbnew.LoadBoard(src)
L = b.GetLayerID(layer_name)
mm = R.mm
VIA, DRILL, CL, ME, STUB_W = 0.6, 0.3, mm(0.2), mm(0.02), mm(0.4)
outline = pcbnew.SHAPE_POLY_SET()
b.GetBoardPolygonOutlines(outline, False)
outline.Deflate(mm(0.5), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, ME)

hulls = []
for n in nets:
    net = b.FindNet(n)
    if net is None:
        print("no net", n)
        continue
    pts = [p.GetPosition() for f in b.GetFootprints() for p in f.Pads() if p.GetNetname() == n]
    if len(pts) < 2:
        continue
    ch = pcbnew.SHAPE_LINE_CHAIN()
    for p in pts:                      # 4 mm squares around the pads, hull of all
        for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            ch.Append(int(p.x + dx * mm(4)), int(p.y + dy * mm(4)))
    hp = pcbnew.SHAPE_POLY_SET()
    hp.NewOutline()
    for p in pts:
        hp.Append(int(p.x - mm(4)), int(p.y - mm(4)))
    # bounding hull: convex hull via the pad cloud
    xs = sorted((p.x, p.y) for p in pts)

    def cross(o, a, c):
        return (a[0] - o[0]) * (c[1] - o[1]) - (a[1] - o[1]) * (c[0] - o[0])
    lo, up = [], []
    for q in xs:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], q) <= 0:
            lo.pop()
        lo.append(q)
    for q in reversed(xs):
        while len(up) >= 2 and cross(up[-2], up[-1], q) <= 0:
            up.pop()
        up.append(q)
    hull = lo[:-1] + up[:-1]
    poly = pcbnew.SHAPE_POLY_SET()
    poly.NewOutline()
    for x, y in hull:
        poly.Append(int(x), int(y))
    if poly.Outline(0).PointCount() < 3:
        poly = pcbnew.SHAPE_POLY_SET()
        poly.NewOutline()
        x0, y0 = min(p.x for p in pts), min(p.y for p in pts)
        x1, y1 = max(p.x for p in pts), max(p.y for p in pts)
        for x, y in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            poly.Append(int(x), int(y))
    poly.Inflate(mm(4), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, ME)
    poly.BooleanIntersection(outline)
    hulls.append((poly.Area(), n, net, poly))

for prio, (_, n, net, poly) in enumerate(sorted(hulls, key=lambda t: -t[0])):    # smallest area = highest priority
    z = pcbnew.ZONE(b)
    z.SetLayer(L)
    z.SetNet(net)
    z.SetAssignedPriority(10 + prio)
    z.SetMinThickness(mm(0.3))
    z.SetLocalClearance(mm(0.3))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_FULL)
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    p = pcbnew.SHAPE_POLY_SET(poly)
    p.thisown = False
    z.SetOutline(p)
    b.Add(z)
R.fill(b)


def fill_of(n):
    s = pcbnew.SHAPE_POLY_SET()
    for z in b.Zones():
        if z.GetNetname() == n and z.IsOnLayer(L) and not z.GetIsRuleArea():
            s.BooleanAdd(z.GetFilledPolysList(L))
    return s


def obstacles(nc, lay):
    """Other-net copper: everything for the via (all layers), and the pad layer for the stub."""
    via_ob, stub_ob = pcbnew.SHAPE_POLY_SET(), pcbnew.SHAPE_POLY_SET()
    r = mm(VIA / 2) + CL
    for t in b.GetTracks():
        if t.GetNetCode() == nc:
            continue
        tl = pcbnew.F_Cu if t.Type() == pcbnew.PCB_VIA_T else t.GetLayer()
        t.TransformShapeToPolygon(via_ob, tl, r, ME, pcbnew.ERROR_OUTSIDE)
        if t.Type() == pcbnew.PCB_VIA_T or t.GetLayer() == lay:
            t.TransformShapeToPolygon(stub_ob, lay, STUB_W // 2 + CL, ME, pcbnew.ERROR_OUTSIDE)
    for f in b.GetFootprints():
        for p in f.Pads():
            for pl in (pcbnew.F_Cu, pcbnew.B_Cu):
                if p.IsOnLayer(pl):
                    p.TransformShapeToPolygon(via_ob, pl, r if p.GetNetCode() != nc else r, ME, pcbnew.ERROR_OUTSIDE)
                    if p.GetNetCode() != nc and pl == lay:
                        p.TransformShapeToPolygon(stub_ob, lay, STUB_W // 2 + CL, ME, pcbnew.ERROR_OUTSIDE)
            if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
                p.TransformHoleToPolygon(via_ob, r, ME, pcbnew.ERROR_OUTSIDE)
    via_ob.Simplify()
    stub_ob.Simplify()
    return via_ob, stub_ob


added, lost = 0, []
for n in nets:
    net = b.FindNet(n)
    if net is None:
        continue
    nc = net.GetNetCode()
    fl = fill_of(n)
    fl.Deflate(mm(VIA / 2) + ME, pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, ME)
    for f in b.GetFootprints():
        for pad in f.Pads():
            if pad.GetNetCode() != nc:
                continue
            c = pad.GetPosition()
            if pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH and fl.Contains(c):
                continue                                         # THT pad sits in its pour
            lay = pcbnew.F_Cu if pad.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu
            via_ob, stub_ob = obstacles(nc, lay)
            half = max(pad.GetSize().x, pad.GetSize().y) / 2
            best = None
            for k in range(0, 16):
                rad = half + mm(0.5 + 0.25 * k)
                for j in range(24):
                    a = 2 * math.pi * j / 24
                    v = pcbnew.VECTOR2I(int(c.x + rad * math.cos(a)), int(c.y + rad * math.sin(a)))
                    if not fl.Contains(v) or via_ob.Contains(v):
                        continue
                    seg = pcbnew.SHAPE_POLY_SET()
                    tr = pcbnew.PCB_TRACK(b)
                    tr.SetStart(c)
                    tr.SetEnd(v)
                    tr.SetWidth(STUB_W)
                    tr.SetLayer(lay)
                    tr.TransformShapeToPolygon(seg, lay, 0, ME, pcbnew.ERROR_OUTSIDE)
                    seg.BooleanIntersection(stub_ob)
                    if seg.OutlineCount():
                        continue
                    best = (v, tr)
                    break
                if best:
                    break
            if not best:
                lost.append(f"{f.GetReference()}.{pad.GetNumber()}")
                continue
            v, tr = best
            via = pcbnew.PCB_VIA(b)
            via.SetPosition(v)
            via.SetWidth(mm(VIA))
            via.SetDrill(mm(DRILL))
            via.SetNet(net)
            b.Add(via)
            tr.SetNet(net)
            b.Add(tr)
            added += 1
R.fill(b)
b.Save(out)
print(f"power pours {[h[1] for h in hulls]} on {layer_name}: {added} pad vias, no room: {len(lost)} {lost[:20]}")
