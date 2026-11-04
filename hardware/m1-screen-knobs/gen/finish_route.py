"""Finish the last unrouted connections that Freerouting leaves behind (around the QFN-60 LED driver).

A small grid maze router (Lee/BFS with via cost) on F.Cu, In2.Cu and B.Cu, 0.05 mm grid, one connection
at a time, obstacles inflated by the board rules. Used by make_pcb.py after the autorouter; every track
it adds is checked by KiCad's DRC in CI like any other.
License: AGPL-3.0-or-later.
"""
import heapq
import math

import pcbnew

G = 0.05                                   # grid, mm
MARGIN = 4.0                               # search window around the gap, mm
LAYERS = None                              # filled in run(): routing layers


def _mm(v):
    return pcbnew.ToMM(v)


class Grid:
    def __init__(self, b, net, box, track, clear, via):
        self.b, self.net, self.track, self.clear, self.via = b, net, track, clear, via
        self.x0, self.y0, self.x1, self.y1 = box
        self.nx, self.ny = int((self.x1 - self.x0) / G) + 1, int((self.y1 - self.y0) / G) + 1
        self.block = {L: bytearray(self.nx * self.ny) for L in LAYERS}
        self.noVia = bytearray(self.nx * self.ny)

    def idx(self, i, j):
        return j * self.nx + i

    def cell(self, x, y):
        return int(round((x - self.x0) / G)), int(round((y - self.y0) / G))

    def xy(self, i, j):
        return self.x0 + i * G, self.y0 + j * G

    def _mark(self, arr, x0, y0, x1, y1, test):
        i0, j0 = self.cell(x0, y0)
        i1, j1 = self.cell(x1, y1)
        for j in range(max(0, j0), min(self.ny - 1, j1) + 1):
            for i in range(max(0, i0), min(self.nx - 1, i1) + 1):
                x, y = self.xy(i, j)
                if test(x, y):
                    arr[self.idx(i, j)] = 1

    def seg(self, arr, ax, ay, bx, by, r):
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy

        def t(x, y):
            u = 0 if L == 0 else max(0, min(1, ((x - ax) * dx + (y - ay) * dy) / L))
            return (x - ax - u * dx) ** 2 + (y - ay - u * dy) ** 2 < r * r
        self._mark(arr, min(ax, bx) - r, min(ay, by) - r, max(ax, bx) + r, max(ay, by) + r, t)

    def rect(self, arr, l, t_, r_, b_, m):
        self._mark(arr, l - m, t_ - m, r_ + m, b_ + m, lambda x, y: True)

    def build(self):
        b, nc = self.b, self.net.GetNetCode()
        kt = self.clear + self.track / 2           # keep a track centre this far from other copper
        kv = self.clear + self.via[0] / 2           # keep a via centre this far
        for t in b.GetTracks():
            if t.GetNetCode() == nc:
                continue
            if t.Type() == pcbnew.PCB_VIA_T:
                p, w = t.GetPosition(), _mm(t.GetWidth()) / 2
                for L in LAYERS:
                    self.seg(self.block[L], _mm(p.x), _mm(p.y), _mm(p.x), _mm(p.y), w + kt)
                self.seg(self.noVia, _mm(p.x), _mm(p.y), _mm(p.x), _mm(p.y), w + kv + 0.05)
            elif t.GetLayer() in LAYERS:
                s, e, w = t.GetStart(), t.GetEnd(), _mm(t.GetWidth()) / 2
                self.seg(self.block[t.GetLayer()], _mm(s.x), _mm(s.y), _mm(e.x), _mm(e.y), w + kt)
                self.seg(self.noVia, _mm(s.x), _mm(s.y), _mm(e.x), _mm(e.y), w + kv)
        for fp in b.GetFootprints():
            for pad in fp.Pads():
                bb = pad.GetBoundingBox()
                l, t_, r_, b_ = _mm(bb.GetLeft()), _mm(bb.GetTop()), _mm(bb.GetRight()), _mm(bb.GetBottom())
                if r_ < self.x0 - 2 or l > self.x1 + 2 or b_ < self.y0 - 2 or t_ > self.y1 + 2:
                    continue
                same = pad.GetNetCode() == nc and nc != 0
                hole = pad.HasHole()
                for L in LAYERS:
                    if pad.IsOnLayer(L) and not same:
                        self.rect(self.block[L], l, t_, r_, b_, kt)
                if not same or hole:
                    self.rect(self.noVia, l, t_, r_, b_, kv + (0.15 if hole else 0))
        for z in b.Zones():
            if z.GetIsRuleArea() and z.GetDoNotAllowTracks():
                bb = z.GetBoundingBox()
                ol = z.Outline()
                l, t_, r_, b_ = _mm(bb.GetLeft()), _mm(bb.GetTop()), _mm(bb.GetRight()), _mm(bb.GetBottom())

                def inside(x, y, ol=ol):
                    return ol.Contains(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                for L in LAYERS:
                    if z.IsOnLayer(L):
                        self._mark(self.block[L], l - kt, t_ - kt, r_ + kt, b_ + kt,
                                   lambda x, y, f=inside: f(x, y))
                self._mark(self.noVia, l - kv, t_ - kv, r_ + kv, b_ + kv, lambda x, y, f=inside: f(x, y))

    def route(self, src, dst, via_cost=40):
        """src/dst: lists of (layer, i, j). Returns list of (layer, i, j) or None."""
        D = [(1, 0, 1), (-1, 0, 1), (0, 1, 1), (0, -1, 1), (1, 1, 1.41), (1, -1, 1.41), (-1, 1, 1.41), (-1, -1, 1.41)]
        goal = set(dst)
        dist, prev, pq = {}, {}, []
        for s in src:
            dist[s] = 0
            heapq.heappush(pq, (0, s))
        while pq:
            d, (L, i, j) = heapq.heappop(pq)
            if (L, i, j) in goal:
                path, n = [], (L, i, j)
                while n in prev:
                    path.append(n)
                    n = prev[n]
                path.append(n)
                return path[::-1]
            if d > dist.get((L, i, j), 1e18):
                continue
            for di, dj, c in D:
                ni, nj = i + di, j + dj
                if not (0 <= ni < self.nx and 0 <= nj < self.ny):
                    continue
                k = self.idx(ni, nj)
                n = (L, ni, nj)
                if self.block[L][k] and n not in goal:
                    continue
                if di and dj and (self.block[L][self.idx(ni, j)] or self.block[L][self.idx(i, nj)]):
                    continue
                nd = d + c
                if nd < dist.get(n, 1e18):
                    dist[n], prev[n] = nd, (L, i, j)
                    heapq.heappush(pq, (nd, n))
            if not self.noVia[self.idx(i, j)]:
                for L2 in LAYERS:
                    if L2 == L or self.block[L2][self.idx(i, j)]:
                        continue
                    n = (L2, i, j)
                    nd = d + via_cost
                    if nd < dist.get(n, 1e18):
                        dist[n], prev[n] = nd, (L, i, j)
                        heapq.heappush(pq, (nd, n))
        return None


def _cells_of_item(g, item):
    """Grid cells (layer, i, j) covered by a same-net pad or track end, for the search start/goal."""
    out = []
    if isinstance(item, pcbnew.PAD):
        bb = item.GetBoundingBox()
        c = item.GetPosition()
        for L in LAYERS:
            if item.IsOnLayer(L):
                i, j = g.cell(_mm(c.x), _mm(c.y))
                out += [(L, i + a, j + bb_) for a in (-1, 0, 1) for bb_ in (-1, 0, 1)]
    return out


def run(b, track, clear, via, max_conn=40, log=print):
    """Route every remaining ratsnest edge that a short local search can solve. Returns count added."""
    global LAYERS
    LAYERS = [pcbnew.F_Cu, pcbnew.In2_Cu, pcbnew.B_Cu]
    import os
    import re
    import tempfile
    rpt = os.path.join(tempfile.gettempdir(), "finish_route_drc.rpt")
    pcbnew.WriteDRCReport(b, rpt, pcbnew.EDA_UNITS_MILLIMETRES, False)
    txt = open(rpt).read()
    pairs = []
    for blk in txt.split("[unconnected_items]")[1:]:
        hits = re.findall(r"@\(([-\d.]+) mm, ([-\d.]+) mm\): .*?\[([^\]]+)\]", blk.split("\n[")[0])
        if len(hits) >= 2 and hits[0][2] == hits[1][2] and hits[0][2] != "GND":
            pairs.append((hits[0][2], float(hits[0][0]), float(hits[0][1]), float(hits[1][0]), float(hits[1][1])))
    added, failed = 0, []
    for name, sx, sy, tx, ty in pairs[:max_conn]:
        net = b.FindNet(name)
        code = net.GetNetCode()
        if True:
            m = MARGIN
            box = (min(sx, tx) - m, min(sy, ty) - m, max(sx, tx) + m, max(sy, ty) + m)
            g = Grid(b, net, box, track, clear, via)
            g.build()

            def ends(x, y):
                pts = []
                i, j = g.cell(x, y)
                for L in LAYERS:
                    for item in list(b.GetTracks()) + [p for f in b.GetFootprints() for p in f.Pads()]:
                        if item.GetNetCode() != code:
                            continue
                        if isinstance(item, pcbnew.PAD):
                            if item.IsOnLayer(L) and item.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))):
                                pts.append((L, i, j))
                        elif item.Type() == pcbnew.PCB_VIA_T or item.GetLayer() == L:
                            if item.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)), pcbnew.FromMM(0.05)):
                                pts.append((L, i, j))
                return list(set(pts))
            src = ends(sx, sy)
            # goal: every bit of this net's copper in the window except the item we start from
            si = g.cell(sx, sy)
            goalarr = {L: bytearray(g.nx * g.ny) for L in LAYERS}
            for item in b.GetTracks():
                if item.GetNetCode() != code:
                    continue
                if item.Type() == pcbnew.PCB_VIA_T:
                    q = item.GetPosition()
                    for L in LAYERS:
                        g.seg(goalarr[L], _mm(q.x), _mm(q.y), _mm(q.x), _mm(q.y), _mm(item.GetWidth()) / 2)
                elif item.GetLayer() in LAYERS:
                    a_, c_ = item.GetStart(), item.GetEnd()
                    g.seg(goalarr[item.GetLayer()], _mm(a_.x), _mm(a_.y), _mm(c_.x), _mm(c_.y), _mm(item.GetWidth()) / 2)
            for f in b.GetFootprints():
                for pd in f.Pads():
                    if pd.GetNetCode() != code or pd.HitTest(pcbnew.VECTOR2I(pcbnew.FromMM(sx), pcbnew.FromMM(sy))):
                        continue
                    bb = pd.GetBoundingBox()
                    for L in LAYERS:
                        if pd.IsOnLayer(L):
                            g.rect(goalarr[L], _mm(bb.GetLeft()), _mm(bb.GetTop()), _mm(bb.GetRight()), _mm(bb.GetBottom()), -0.05)
            dst = [(L, k % g.nx, k // g.nx) for L in LAYERS for k in range(g.nx * g.ny) if goalarr[L][k]]
            dst = [d for d in dst if abs(d[1] - si[0]) + abs(d[2] - si[1]) > 4 or d[0] not in [s_[0] for s_ in src]]
            if not src or not dst:
                log(f"  {net.GetNetname()}: no start/end layer found")
                failed.append((name, sx, sy))
                continue
            path = g.route(src, dst)
            if not path:
                log(f"  {net.GetNetname()}: no path in the local window")
                failed.append((name, sx, sy))
                continue
            # path -> tracks and vias (merge straight runs)
            pts = [(L, *g.xy(i, j)) for L, i, j in path]
            run_start = pts[0]
            for k in range(1, len(pts)):
                L0, x0, y0 = pts[k - 1]
                L1, x1, y1 = pts[k]
                if L1 != L0:
                    if (run_start[1], run_start[2]) != (x0, y0):
                        _track(b, net, run_start, (L0, x0, y0), track)
                    v = pcbnew.PCB_VIA(b)
                    v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x0), pcbnew.FromMM(y0)))
                    v.SetWidth(pcbnew.FromMM(via[0]))
                    v.SetDrill(pcbnew.FromMM(via[1]))
                    v.SetNet(net)
                    b.Add(v)
                    run_start = (L1, x1, y1)
                    continue
                nxt = pts[k + 1] if k + 1 < len(pts) else None
                d0 = (round((x1 - x0) / G), round((y1 - y0) / G))
                if nxt is None or nxt[0] != L1 or (round((nxt[1] - x1) / G), round((nxt[2] - y1) / G)) != d0:
                    _track(b, net, run_start, (L1, x1, y1), track)
                    run_start = (L1, x1, y1)
            added += 1
            log(f"  {net.GetNetname()}: routed ({len(path)} cells)")
    return added, failed


def rip_and_finish(b, track, clear, via, rounds=6, radius=1.0, log=print):
    """Local rip-up and reroute: when a connection finds no path, take out the other nets' copper
    right around its stuck end and route again; the nets taken out are routed in the next round."""
    total = 0
    for r in range(rounds):
        n, failed = run(b, track, clear, via, log=log)
        total += n
        if not failed:
            break
        rad = radius * (1 + 0.5 * r)
        for name, x, y in failed:
            p = pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y))
            gone = []
            for t in list(b.GetTracks()):
                if t.GetNetname() in (name, "GND"):
                    continue
                if t.HitTest(p, pcbnew.FromMM(rad)):
                    gone.append(t.GetNetname())
                    b.Remove(t)
            log(f"  round {r + 1}: ripped {len(gone)} pieces of {sorted(set(gone))} around {name}")
    return total


def _track(b, net, a, c, w):
    if (a[1], a[2]) == (c[1], c[2]):
        return
    t = pcbnew.PCB_TRACK(b)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(a[1]), pcbnew.FromMM(a[2])))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(c[1]), pcbnew.FromMM(c[2])))
    t.SetWidth(pcbnew.FromMM(w))
    t.SetLayer(a[0])
    t.SetNet(net)
    b.Add(t)
