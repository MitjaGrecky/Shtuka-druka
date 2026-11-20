"""Autorouting of a placed board with Freerouting 1.9 through KiCad's pcbnew Python module (no kicad-cli), then
optionally (--gnd-pour) a GND pour stage: B.Cu pour, F.Cu pour in free places, stitching vias; --pour-only does that stage on a routed board.

  python routing.py BOARD.kicad_pcb --jar freerouting-1.9.0.jar [--passes 100] [--out ROUTED.kicad_pcb] [--no-pour | --gnd-pour [--gnd-net N]] [--pour-only]

The board's .kicad_pro (next to it) carries the net classes (Default, Power, LED_SW of boardkit.write_project);
pcbnew exports them into the DSN, so Freerouting uses the same widths and clearances.
On Windows Freerouting opens its own window while it works and is stopped once the session file is written.
License: AGPL-3.0-or-later.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import pcbnew

mm = pcbnew.FromMM


def _sexpr(txt):
    """Minimal s-expression reader: nested lists of strings."""
    stack, cur = [], []
    for t in re.findall(r'\(|\)|"[^"]*"|[^\s()]+', txt):
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t.strip('"'))
    return cur[0]


def _kids(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def run_freerouting(b, jar, passes, work, two_layers=False):
    if two_layers:                               # inner layers stay planes: route on F.Cu/B.Cu only
        b.SetCopperLayerCount(2)
    dsn, ses = os.path.join(work, "board.dsn"), os.path.join(work, "board.ses")
    assert pcbnew.ExportSpecctraDSN(b, dsn), "DSN export failed"
    java = shutil.which("java") or "java"
    cmd = [java, "-jar", jar, "-de", dsn, "-do", ses, "-mp", str(passes)]
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        cmd = ["xvfb-run", "-a"] + cmd
    print(" ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd)
    t0 = time.time()
    while proc.poll() is None:                   # 1.9 sometimes keeps running after it saved the session
        if os.path.exists(ses) and time.time() - os.path.getmtime(ses) > 20:
            proc.terminate()
            break
        time.sleep(5)
    assert os.path.exists(ses), "no SES from Freerouting"
    print(f"routed in {time.time() - t0:.0f} s", flush=True)
    return ses


def import_ses(b, path, via_drill):
    """Add the wires and vias of a Specctra session file (pcbnew's own importer needs the GUI)."""
    routes = _kids(_sexpr(open(path).read()), "routes")[0]
    res = _kids(routes, "resolution")[0]
    unit = {"um": 1e-3, "mm": 1.0, "mil": 0.0254, "inch": 25.4}[res[1]] / int(res[2])
    to = lambda v: pcbnew.FromMM(float(v) * unit)  # noqa: E731
    layers = {b.GetLayerName(l): l for l in range(pcbnew.PCB_LAYER_ID_COUNT) if pcbnew.IsCopperLayer(l)}
    vdia = {ps[1]: c[2] for lib in _kids(routes, "library_out") for ps in _kids(lib, "padstack")
            for sh in _kids(ps, "shape") for c in _kids(sh, "circle")}
    n = 0
    for no in _kids(routes, "network_out"):
        for nt in _kids(no, "net"):
            net = b.FindNet(nt[1])
            for w in _kids(nt, "wire"):
                for pth in _kids(w, "path"):
                    v = [int(x) for x in pth[3:] if not isinstance(x, list)]
                    xy = [(to(v[i]), -to(v[i + 1])) for i in range(0, len(v) - 1, 2)]
                    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
                        t = pcbnew.PCB_TRACK(b)
                        t.SetStart(pcbnew.VECTOR2I(x0, y0))
                        t.SetEnd(pcbnew.VECTOR2I(x1, y1))
                        t.SetWidth(to(pth[2]))
                        t.SetLayer(layers[pth[1]])
                        t.SetNet(net)
                        b.Add(t)
                        n += 1
            for v in _kids(nt, "via"):
                via = pcbnew.PCB_VIA(b)
                via.SetPosition(pcbnew.VECTOR2I(to(v[2]), -to(v[3])))
                via.SetWidth(to(vdia.get(v[1], 6000)))
                via.SetDrill(mm(via_drill))
                via.SetNet(net)
                b.Add(via)
                n += 1
    return n


def gnd_net_name(b):
    """GND net of the board: 'GND', else '/BAT_N' (BM's ground)."""
    names = [str(n) for n in b.GetNetsByName().keys()]
    for cand in ("GND", "/GND", "/BAT_N"):
        if cand in names:
            return cand
    raise SystemExit("no GND net found")


def gnd_pours(b, net=None, clearance=0.3, edge=0.5):
    """Pours of the ground net: B.Cu over the whole board outline (inset by `edge`), F.Cu in the free places.
    Clearance to other nets `clearance` (or the net class if larger), thermal reliefs on pads, islands removed.
    Existing zones are dropped first, keepout (rule area) zones are kept."""
    for z in list(b.Zones()):
        if not z.GetIsRuleArea():
            b.Remove(z)
    outline = pcbnew.SHAPE_POLY_SET()
    b.GetBoardPolygonOutlines(outline, False)
    outline.Deflate(mm(edge), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, mm(0.05))
    gnd = b.FindNet(net or gnd_net_name(b))
    for fp in b.GetFootprints():                 # through-hole ground pads: solid connection (no starved thermals)
        for pad in fp.Pads():
            if pad.GetNetname() == gnd.GetNetname() and pad.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
                pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
    for prio, layer in ((0, pcbnew.F_Cu), (1, pcbnew.B_Cu)):
        z = pcbnew.ZONE(b)
        z.SetLayer(layer)
        z.SetNet(gnd)
        z.SetAssignedPriority(prio)
        z.SetMinThickness(mm(0.25))
        z.SetLocalClearance(mm(clearance))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.3))
        z.SetThermalReliefSpokeWidth(mm(0.3))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        p = pcbnew.SHAPE_POLY_SET(outline)
        p.thisown = False
        z.SetOutline(p)
        b.Add(z)


def fill(b):
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())


def _fills(b, net):
    z = {x.GetLayer(): x for x in b.Zones() if not x.GetIsRuleArea() and x.GetNetname() == net}
    return z[pcbnew.F_Cu].GetFilledPolysList(pcbnew.F_Cu), z[pcbnew.B_Cu].GetFilledPolysList(pcbnew.B_Cu)


def _drills(b):
    """(x, y, keep-out radius) of every pad hole: a via must stay hole_to_hole + margin from it."""
    out = []
    for fp in b.GetFootprints():
        for pad in fp.Pads():
            d = pad.GetDrillSize()
            if max(d.x, d.y) > 0:
                out.append((pad.GetPosition().x, pad.GetPosition().y, max(d.x, d.y) / 2 + mm(0.15 + 0.6)))
    return out


def _mains(f, frac=0.25):
    """Outlines of the pour islands with at least `frac` of the biggest island's area (the pour proper; the small
    leftovers between tracks are not worth a via and would only make orphan copper clusters)."""
    ar = [f.Outline(i).Area() for i in range(f.OutlineCount())]
    return [f.Outline(i) for i, a in enumerate(ar) if a >= frac * max(ar)] if ar else []


def _ring(x, y, r):
    return [pcbnew.VECTOR2I(int(x + r * c), int(y + r * s)) for c, s in
            ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7))]


def stitch(b, net=None, via=(0.6, 0.3), pitch=5.0, margin=0.6, edge_pitch=4.0, near_pad=3.0, hole_keep=2.0):
    """GND stitching vias, every one fully inside both pours (so >= `margin` mm of pour around the via edge, which
    keeps it at least pour clearance + `margin` from foreign pads, tracks and vias on both layers):
    (1) along the board edge every `edge_pitch`, (2) on a `pitch` grid, (3) next to every SMD ground pad that has
    no ground via within `near_pad` mm, (4) in every pour island that still has none (smaller margins)."""
    net = net or gnd_net_name(b)
    gnd = b.FindNet(net)
    top, bot = _fills(b, net)
    r = mm(via[0] / 2 + margin)
    holes = [fp.GetPosition() for fp in b.GetFootprints() if fp.GetReference().startswith("H")]
    vias = [t.GetPosition() for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
    drills = _drills(b)
    mt, mb = _mains(top), _mains(bot)
    d2 = lambda a, x, y: (a.x - x) ** 2 + (a.y - y) ** 2  # noqa: E731
    bb = b.GetBoardEdgesBoundingBox()
    cnt = [0]

    def ok(x, y, rr, sep):
        if any((x - hx) ** 2 + (y - hy) ** 2 < hr ** 2 for hx, hy, hr in drills):
            return False
        if any(d2(v, x, y) < mm(sep) ** 2 for v in vias) or any(d2(h, x, y) < mm(hole_keep + 2) ** 2 for h in holes):
            return False
        c = pcbnew.VECTOR2I(int(x), int(y))
        return (any(ch.PointInside(c) for ch in mt) and any(ch.PointInside(c) for ch in mb)
                and all(top.Contains(q) and bot.Contains(q) for q in _ring(x, y, rr)))

    def put(x, y):
        v = pcbnew.PCB_VIA(b)
        v.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
        v.SetWidth(mm(via[0]))
        v.SetDrill(mm(via[1]))
        v.SetNet(gnd)
        b.Add(v)
        vias.append(v.GetPosition())
        cnt[0] += 1

    # (1) edge: grid cells within 1.5 mm of the inset outline, step 0.5 mm along the bounding box edges
    outl = pcbnew.SHAPE_POLY_SET()
    b.GetBoardPolygonOutlines(outl, False)
    ch = outl.Outline(0)
    pts = [ch.CPoint(i) for i in range(ch.PointCount())]
    for p0, p1 in zip(pts, pts[1:] + pts[:1]):
        L = ((p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2) ** 0.5
        if L < 1:
            continue
        ux, uy = (p1.x - p0.x) / L, (p1.y - p0.y) / L
        nx, ny = -uy, ux                      # normal, try both sides (inside is where the pour is)
        t = mm(edge_pitch) / 2
        while t < L:
            for dist in (0.9, 1.2, 1.6):
                done = False
                for sgn in (1, -1):
                    x, y = p0.x + ux * t + sgn * nx * mm(dist), p0.y + uy * t + sgn * ny * mm(dist)
                    if ok(x, y, r, edge_pitch * 0.7):
                        put(x, y)
                        done = True
                        break
                if done:
                    break
            t += mm(edge_pitch)
    # (2) grid
    step = mm(pitch)
    y = bb.GetTop() + step // 2
    while y < bb.GetBottom():
        x = bb.GetLeft() + step // 2
        while x < bb.GetRight():
            if ok(x, y, r, pitch * 0.5):
                put(x, y)
            x += step
        y += step
    # (3) next to SMD ground pads
    for fp in b.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() != net or pad.GetAttribute() != pcbnew.PAD_ATTRIB_SMD:
                continue
            c = pad.GetPosition()
            if any(d2(v, c.x, c.y) < mm(near_pad) ** 2 for v in vias):
                continue
            best = None
            for k in range(1, 25):            # radius 0.5 .. 3 mm, 16 directions
                rad = mm(0.5 * k)
                for j in range(16):
                    import math
                    x, y = c.x + rad * math.cos(j * math.pi / 8), c.y + rad * math.sin(j * math.pi / 8)
                    if ok(x, y, r, 1.0):
                        best = (x, y)
                        break
                if best:
                    break
            if best:
                put(*best)
    return cnt[0]


def stitch_islands(b, net=None, via=(0.6, 0.3)):
    """Main pour islands (top or bottom) that carry no via: add one wherever a via fits (margins 0.45, 0.3 mm)."""
    net = net or gnd_net_name(b)
    gnd = b.FindNet(net)
    n = 0
    drills = _drills(b)
    for _ in range(2):
        top, bot = _fills(b, net)
        vias = [t.GetPosition() for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == net]
        for fills, other in ((top, bot), (bot, top)):
            om = _mains(other)
            for ch in _mains(fills):
                if any(ch.PointInside(v) for v in vias):
                    continue
                bb = ch.BBox()
                placed = False
                for margin in (0.45, 0.3):
                    r = mm(via[0] / 2 + margin)
                    step = mm(0.4)
                    y = bb.GetTop() + r
                    while y < bb.GetBottom() - r and not placed:
                        x = bb.GetLeft() + r
                        while x < bb.GetRight() - r:
                            if not any((x - hx) ** 2 + (y - hy) ** 2 < hr ** 2 for hx, hy, hr in drills) and (
                                    all(ch.PointInside(q) and fills.Contains(q) and other.Contains(q) for q in _ring(x, y, r))
                                    and any(o.PointInside(pcbnew.VECTOR2I(int(x), int(y))) for o in om)):
                                v = pcbnew.PCB_VIA(b)
                                v.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
                                v.SetWidth(mm(via[0]))
                                v.SetDrill(mm(via[1]))
                                v.SetNet(gnd)
                                b.Add(v)
                                vias.append(v.GetPosition())
                                n += 1
                                placed = True
                                break
                            x += step
                        y += step
                    if placed:
                        break
        if n:
            fill(b)
    return n


class _GndGraph:
    """Connectivity of the ground net as copper sees it: pour islands (per layer) joined by vias, ground pads and
    tracks (union-find). Used to find pour fragments that are not tied to the main ground."""

    def __init__(self, b, net, gap=0.3):
        import math
        self.b, self.net = b, net
        self.f = dict(zip((pcbnew.F_Cu, pcbnew.B_Cu), _fills(b, net)))
        self.par = {}
        self.cell = mm(5)
        self.idx = {}
        for lay, f in self.f.items():
            g = {}
            for i in range(f.OutlineCount()):
                bb = f.Outline(i).BBox()
                for cx in range(bb.GetLeft() // self.cell, bb.GetRight() // self.cell + 1):
                    for cy in range(bb.GetTop() // self.cell, bb.GetBottom() // self.cell + 1):
                        g.setdefault((cx, cy), []).append(i)
            self.idx[lay] = g
        at = {}
        for t in b.GetTracks():
            if t.GetNetname() != net:
                continue
            if t.Type() == pcbnew.PCB_VIA_T:
                k = ("v", t.m_Uuid.AsString() if hasattr(t, "m_Uuid") else id(t))
                self.par.setdefault(k, k)
                p = t.GetPosition()
                for lay in self.f:
                    for q in _ring(p.x, p.y, mm(0.35))[:5]:
                        i = self.island_at(lay, q.x, q.y)
                        if i is not None:
                            self.union(k, ("i", lay, i))
                at.setdefault((p.x, p.y), []).append(k)
            else:
                k = ("t", t.m_Uuid.AsString() if hasattr(t, "m_Uuid") else id(t))
                self.par.setdefault(k, k)
                for p in (t.GetStart(), t.GetEnd()):
                    at.setdefault((p.x, p.y), []).append(k)
        for fp in b.GetFootprints():
            for pad in fp.Pads():
                if pad.GetNetname() != net:
                    continue
                k = ("p", fp.GetReference(), pad.GetNumber())
                self.par.setdefault(k, k)
                c, sz = pad.GetPosition(), pad.GetSize()
                rr = max(sz.x, sz.y) / 2 + mm(gap + 0.2)
                lays = [l for l in self.f if pad.IsOnLayer(l)]
                for lay in lays:
                    for j in range(8):
                        i = self.island_at(lay, c.x + rr * math.cos(j * math.pi / 4), c.y + rr * math.sin(j * math.pi / 4))
                        if i is not None:
                            self.union(k, ("i", lay, i))
                at.setdefault((c.x, c.y), []).append(k)
        for ks in at.values():
            for k in ks[1:]:
                self.union(ks[0], k)

    def find(self, k):
        self.par.setdefault(k, k)
        while self.par[k] != k:
            self.par[k] = self.par[self.par[k]]
            k = self.par[k]
        return k

    def union(self, a, b):
        self.par[self.find(a)] = self.find(b)

    def island_at(self, lay, x, y):
        v = pcbnew.VECTOR2I(int(x), int(y))
        f = self.f[lay]
        for i in self.idx[lay].get((int(x) // self.cell, int(y) // self.cell), ()):
            if f.Outline(i).PointInside(v):
                return i
        return None

    def comp(self, lay, x, y):
        i = self.island_at(lay, x, y)
        return None if i is None else self.find(("i", lay, i))

    def main(self):
        area = {}
        for lay, f in self.f.items():
            for i in range(f.OutlineCount()):
                r = self.find(("i", lay, i))
                area[r] = area.get(r, 0) + f.Outline(i).Area()
        return max(area, key=area.get), area


def connect_islands(b, net=None, via=(0.6, 0.3)):
    """Tie every pour fragment that is not part of the main ground to it with a via placed where the fragment (one
    layer) and the main ground (the other layer) overlap. Returns the number of vias added."""
    net = net or gnd_net_name(b)
    gnd = b.FindNet(net)
    drills = _drills(b)
    n = 0
    for _ in range(6):
        g = _GndGraph(b, net)
        main, area = g.main()
        vias = [t.GetPosition() for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
        added = 0
        for lay, f in g.f.items():
            oth = pcbnew.B_Cu if lay == pcbnew.F_Cu else pcbnew.F_Cu
            for i in range(f.OutlineCount()):
                if g.find(("i", lay, i)) == main:
                    continue
                ch = f.Outline(i)
                bb = ch.BBox()
                done = False
                for margin in (0.6, 0.45, 0.3, 0.15):
                    r = mm(via[0] / 2 + margin)
                    x0 = bb.GetLeft() + r
                    y = bb.GetTop() + r
                    while y < bb.GetBottom() - r and not done:
                        x = x0
                        while x < bb.GetRight() - r:
                            if (ch.PointInside(pcbnew.VECTOR2I(int(x), int(y))) and g.comp(oth, x, y) == main
                                    and all(f.Contains(q) and g.f[oth].Contains(q) for q in _ring(x, y, r))
                                    and not any((x - hx) ** 2 + (y - hy) ** 2 < hr ** 2 for hx, hy, hr in drills)
                                    and not any((v.x - x) ** 2 + (v.y - y) ** 2 < mm(0.8) ** 2 for v in vias)):
                                v = pcbnew.PCB_VIA(b)
                                v.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
                                v.SetWidth(mm(via[0]))
                                v.SetDrill(mm(via[1]))
                                v.SetNet(gnd)
                                b.Add(v)
                                vias.append(v.GetPosition())
                                added += 1
                                done = True
                                break
                            x += mm(0.4)
                        y += mm(0.4)
                    if done:
                        break
        n += added
        if not added:
            break
        fill(b)
    return n


def fix_gnd_pads(b, net=None, via=(0.6, 0.3), width=0.25, gap=0.3):
    """SMD ground pads the pour reaches badly: fewer than 3 of 8 directions at thermal-gap distance lie in the main
    pour of the pad's layer -> solid connection (no starved thermal); none -> also a short track to a new via
    that sits in both main pours (the pad is cut off by foreign copper on its own layer)."""
    import math
    net = net or gnd_net_name(b)
    gnd = b.FindNet(net)
    top, bot = _fills(b, net)

    def mains(f):
        ar = [f.Outline(i).Area() for i in range(f.OutlineCount())]
        return [f.Outline(i) for i, a in enumerate(ar) if a >= 0.25 * max(ar)] if ar else []

    main = {pcbnew.F_Cu: mains(top), pcbnew.B_Cu: mains(bot)}
    full = {pcbnew.F_Cu: top, pcbnew.B_Cu: bot}
    drills = _drills(b)
    inmain = lambda lay, x, y: any(ch.PointInside(pcbnew.VECTOR2I(int(x), int(y))) for ch in main[lay])  # noqa: E731
    vias = [t.GetPosition() for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
    solid = tracked = 0
    g = _GndGraph(b, net)
    gmain = g.main()[0]
    for fp in b.GetFootprints():
        for pad in fp.Pads():
            if pad.GetNetname() != net or pad.GetAttribute() not in (pcbnew.PAD_ATTRIB_SMD, pcbnew.PAD_ATTRIB_PTH):
                continue
            lost = g.find(("p", fp.GetReference(), pad.GetNumber())) != gmain
            lay = pcbnew.F_Cu if pad.IsOnLayer(pcbnew.F_Cu) else pcbnew.B_Cu
            oth = pcbnew.B_Cu if lay == pcbnew.F_Cu else pcbnew.F_Cu
            c, sz = pad.GetPosition(), pad.GetSize()
            half = max(sz.x, sz.y) / 2
            rr = half + mm(gap + 0.2)
            hits = sum(inmain(lay, c.x + rr * math.cos(k * math.pi / 4), c.y + rr * math.sin(k * math.pi / 4))
                       for k in range(8))
            if hits >= 3 and not lost:
                continue
            pad.SetLocalZoneConnection(pcbnew.ZONE_CONNECTION_FULL)
            solid += 1
            if hits and not lost:
                continue
            best = None
            for k in range(1, 15):
                rad = half + mm(0.6 + 0.2 * k)
                for j in range(16):
                    x, y = c.x + rad * math.cos(j * math.pi / 8), c.y + rad * math.sin(j * math.pi / 8)
                    if any((x - hx) ** 2 + (y - hy) ** 2 < hr ** 2 for hx, hy, hr in drills) or                             any((v.x - x) ** 2 + (v.y - y) ** 2 < mm(0.8) ** 2 for v in vias):
                        continue
                    ring = _ring(x, y, mm(via[0] / 2 + 0.3))
                    d = math.hypot(x - c.x, y - c.y)
                    seg = [pcbnew.VECTOR2I(int(c.x + (x - c.x) * t / d), int(c.y + (y - c.y) * t / d))
                           for t in range(int(half + mm(gap + 0.15)), int(d), mm(0.15))]
                    if (g.comp(oth, x, y) == gmain and g.comp(lay, x, y) == gmain
                            and all(full[oth].Contains(q) for q in ring)
                            and all(full[lay].Contains(q) for q in ring + seg)):
                        best = (x, y)
                        break
                if best:
                    break
            if best:
                v = pcbnew.PCB_VIA(b)
                v.SetPosition(pcbnew.VECTOR2I(int(best[0]), int(best[1])))
                v.SetWidth(mm(via[0]))
                v.SetDrill(mm(via[1]))
                v.SetNet(gnd)
                b.Add(v)
                t = pcbnew.PCB_TRACK(b)
                t.SetStart(c)
                t.SetEnd(v.GetPosition())
                t.SetWidth(mm(width))
                t.SetLayer(lay)
                t.SetNet(gnd)
                b.Add(t)
                vias.append(v.GetPosition())
                tracked += 1
    return solid, tracked


def pour_stage(b, net=None):
    """GND pours + stitching vias: the stage after routing (--gnd-pour)."""
    net = net or gnd_net_name(b)
    gnd_pours(b, net)
    fill(b)
    n1 = stitch(b, net)
    fill(b)
    n2 = stitch_islands(b, net)
    fill(b)
    n2 += connect_islands(b, net)
    solid, tracked = fix_gnd_pads(b, net)
    fill(b)
    n2 += connect_islands(b, net)
    print(f"GND pour on {net}: {n1} stitching vias, {n2} island vias, {solid} solid pads, {tracked} pad stubs")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board")
    ap.add_argument("--jar", required=True)
    ap.add_argument("--passes", type=int, default=100)
    ap.add_argument("--out", help="routed board (default: overwrite BOARD)")
    ap.add_argument("--ses", help="use this session file instead of running Freerouting")
    ap.add_argument("--no-pour", action="store_true")
    ap.add_argument("--gnd-pour", action="store_true", help="GND pours and stitching vias after routing (replaces the old pour)")
    ap.add_argument("--pour-only", action="store_true", help="board is already routed: only the GND pour stage")
    ap.add_argument("--gnd-net", help="ground net name (default GND, else /BAT_N)")
    ap.add_argument("--two-layers", action="store_true", help="4-layer board: route signals on F.Cu/B.Cu only")
    ap.add_argument("--via-drill", type=float, default=0.3)
    a = ap.parse_args()
    if a.pour_only:
        b = pcbnew.LoadBoard(a.board)
        pour_stage(b, a.gnd_net)
        b.Save(a.out or a.board)
        return
    b = pcbnew.LoadBoard(a.board)
    work = tempfile.mkdtemp(prefix="route_")
    ses = a.ses or run_freerouting(b, os.path.abspath(a.jar), a.passes, work, a.two_layers)
    if not a.ses:
        keep = os.path.splitext(a.out or a.board)[0] + ".ses"
        shutil.copy(ses, keep)
        print("session kept:", keep)
    b = pcbnew.LoadBoard(a.board)                # fresh board: the DSN export may leave state behind
    print("imported", import_ses(b, ses, a.via_drill), "tracks and vias")
    if a.gnd_pour and not a.no_pour:
        pour_stage(b, a.gnd_net)
    out = a.out or a.board
    b.Save(out)
    print("ok", out, len(b.GetTracks()), "tracks/vias,", len(b.Zones()), "zones")


if __name__ == "__main__":
    sys.exit(main())
