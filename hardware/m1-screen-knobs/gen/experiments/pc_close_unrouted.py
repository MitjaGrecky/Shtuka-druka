"""Close the unconnected nets of a Quilter result on a COPY of the board with a small grid router.
usage: route.py in.kicad_pcb out.kicad_pcb drc.json   (pcbnew from KiCad 10)"""
import sys, os, json, math, heapq, re, traceback
import numpy as np, pcbnew
mm = lambda v: v / 1e6
IU = lambda v: int(round(v * 1e6))
SRC, OUT, DRC = sys.argv[1:4]
b = pcbnew.LoadBoard(SRC)
b.BuildConnectivity()
con = b.GetConnectivity()
LAY = [0, 6, 2]                  # F.Cu, In2.Cu, B.Cu (In1 is the GND plane)
LNAME = {0: "F.Cu", 6: "In2.Cu", 2: "B.Cu"}
G = float(os.environ.get("G", "0.05"))
X0, Y0, X1, Y1 = 40.3, 40.3, 263.7, 73.7
VIA_D, VIA_DR = 0.45, 0.2


def prims():
    seg = []; via = []; pad = []
    for t in b.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T:
            via.append((mm(t.GetPosition().x), mm(t.GetPosition().y), mm(t.GetWidth(0)) / 2, t.GetNetname()))
        else:
            seg.append((t.GetLayer(), mm(t.GetStart().x), mm(t.GetStart().y), mm(t.GetEnd().x), mm(t.GetEnd().y), mm(t.GetWidth()) / 2, t.GetNetname()))
    for f in b.GetFootprints():
        for p in f.Pads():
            bb = p.GetBoundingBox()
            ls = [l for l in LAY if p.IsOnLayer(l)]
            if not ls:
                continue
            extra = 0.35 if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH else 0.0
            pad.append((ls, mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom()), p.GetNetname(), extra))
    return seg, via, pad


KEEP = []
for z in b.Zones():
    if z.GetIsRuleArea():
        bb = z.GetBoundingBox()
        KEEP.append((mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom()), z.GetDoNotAllowTracks(), z.GetDoNotAllowVias()))


def raster(win, net, w, clr, seg, via, pad):
    wx0, wy0, W, H = win
    blk = {l: np.zeros((H, W), bool) for l in LAY}
    vb = {l: np.zeros((H, W), bool) for l in LAY}
    xs = wx0 + (np.arange(W) + 0.5) * G
    ys = wy0 + (np.arange(H) + 0.5) * G

    def rng(lo, hi, o, n):
        return max(0, int((lo - o) / G)), min(n, int((hi - o) / G) + 2)

    def mark_seg(arr, x1, y1, x2, y2, r):
        a0, a1 = rng(min(x1, x2) - r, max(x1, x2) + r, wx0, W)
        c0, c1 = rng(min(y1, y2) - r, max(y1, y2) + r, wy0, H)
        if a0 >= a1 or c0 >= c1:
            return
        X, Y = np.meshgrid(xs[a0:a1], ys[c0:c1])
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        t = np.zeros_like(X) if L == 0 else np.clip(((X - x1) * dx + (Y - y1) * dy) / L, 0, 1)
        arr[c0:c1, a0:a1] |= np.hypot(X - (x1 + t * dx), Y - (y1 + t * dy)) < r

    def mark_rect(arr, l, t, rr, bt, r):
        a0, a1 = rng(l - r, rr + r, wx0, W)
        c0, c1 = rng(t - r, bt + r, wy0, H)
        if a0 >= a1 or c0 >= c1:
            return
        X, Y = np.meshgrid(xs[a0:a1], ys[c0:c1])
        arr[c0:c1, a0:a1] |= (X > l - r) & (X < rr + r) & (Y > t - r) & (Y < bt + r)

    m = float(os.environ.get("M", "0.04"))
    vr = VIA_D / 2
    for (l, x1, y1, x2, y2, hw, n) in seg:
        if n == net or l not in blk:
            continue
        mark_seg(blk[l], x1, y1, x2, y2, hw + clr + w / 2 + m)
        mark_seg(vb[l], x1, y1, x2, y2, hw + clr + vr + m)
    for (x, y, r, n) in via:
        if n == net:
            continue
        for l in LAY:
            mark_seg(blk[l], x, y, x, y, r + clr + w / 2 + m)
            mark_seg(vb[l], x, y, x, y, r + clr + vr + m)
    for (ls, l, t, rr, bt, n, ex) in pad:
        if n == net:
            continue
        for lay in ls:
            mark_rect(blk[lay], l, t, rr, bt, clr + w / 2 + m + ex)
            mark_rect(vb[lay], l, t, rr, bt, clr + vr + m + ex)
    for (l, t, rr, bt, tr, vi) in KEEP:
        for lay in LAY:
            if tr:
                mark_rect(blk[lay], l, t, rr, bt, w / 2)
            if vi:
                mark_rect(vb[lay], l, t, rr, bt, vr)
    for arr in list(blk.values()) + list(vb.values()):
        arr[:, xs < X0 + 0.3 + w / 2] = True
        arr[:, xs > X1 - 0.3 - w / 2] = True
        arr[ys < Y0 + 0.3 + w / 2, :] = True
        arr[ys > Y1 - 0.3 - w / 2, :] = True
    vblk = np.zeros((H, W), bool)
    for l in LAY:
        vblk |= vb[l]
    return blk, vblk


def astar(win, blk, vblk, start, tmask, viacost=60, fcost=1.4):
    wx0, wy0, W, H = win
    N = len(LAY) * H * W
    g = np.full(N, np.inf, np.float32)
    par = np.full(N, -1, np.int64)
    sl, sx, sy = start
    s = LAY.index(sl) * H * W + sy * W + sx
    stack = np.stack([tmask[l] for l in LAY])
    ts = np.argwhere(stack)
    if len(ts) == 0:
        return None
    tb = (ts[:, 2].min(), ts[:, 2].max(), ts[:, 1].min(), ts[:, 1].max())
    tmflat = stack.reshape(-1)
    bflat = np.stack([blk[l] for l in LAY]).reshape(-1)
    vflat = vblk.reshape(-1)

    def h(x, y):
        dx = max(tb[0] - x, 0, x - tb[1])
        dy = max(tb[2] - y, 0, y - tb[3])
        return max(dx, dy) + 0.414 * min(dx, dy)

    g[s] = 0
    pq = [(h(sx, sy), s)]
    nd = 0
    mul = [fcost if l == 0 else 1.0 for l in LAY]
    nbr = [(1, 0, 1.0), (-1, 0, 1.0), (0, 1, 1.0), (0, -1, 1.0), (1, 1, 1.414), (1, -1, 1.414), (-1, 1, 1.414), (-1, -1, 1.414)]
    while pq:
        f, i = heapq.heappop(pq)
        nd += 1
        if tmflat[i] and not bflat[i]:
            path = []
            while i != -1:
                path.append(i)
                i = par[i]
            return path[::-1], nd
        L = i // (H * W)
        r = i % (H * W)
        y = r // W
        x = r % W
        base = L * H * W
        gi = g[i]
        for dx, dy, c in nbr:
            nx, ny = x + dx, y + dy
            if nx < 0 or ny < 0 or nx >= W or ny >= H:
                continue
            j = base + ny * W + nx
            if bflat[j]:
                continue
            if dx and dy and (bflat[base + y * W + nx] or bflat[base + ny * W + x]):
                continue
            ng = gi + c * mul[L]
            if ng < g[j]:
                g[j] = ng
                par[j] = i
                heapq.heappush(pq, (ng + h(nx, ny), j))
        if not vflat[r]:
            for L2 in range(len(LAY)):
                if L2 == L:
                    continue
                j = L2 * H * W + r
                if bflat[j]:
                    continue
                ng = gi + viacost
                if ng < g[j]:
                    g[j] = ng
                    par[j] = i
                    heapq.heappush(pq, (ng + h(x, y), j))
        if nd > 2500000:
            return None
    return None


def cluster(item):
    out = [item]
    for it in con.GetConnectedItems(item):
        if it.GetClass() in ("PCB_TRACK", "PCB_VIA", "PAD"):
            out.append(it)
    return out


def tmask_of(items, win):
    wx0, wy0, W, H = win
    tm = {l: np.zeros((H, W), bool) for l in LAY}
    xs = wx0 + (np.arange(W) + 0.5) * G
    ys = wy0 + (np.arange(H) + 0.5) * G

    def mk(arr, x1, y1, x2, y2, r):
        a0 = max(0, int((min(x1, x2) - r - wx0) / G)); a1 = min(W, int((max(x1, x2) + r - wx0) / G) + 2)
        c0 = max(0, int((min(y1, y2) - r - wy0) / G)); c1 = min(H, int((max(y1, y2) + r - wy0) / G) + 2)
        if a0 >= a1 or c0 >= c1:
            return
        X, Y = np.meshgrid(xs[a0:a1], ys[c0:c1])
        dx, dy = x2 - x1, y2 - y1
        Ls = dx * dx + dy * dy
        t = np.zeros_like(X) if Ls == 0 else np.clip(((X - x1) * dx + (Y - y1) * dy) / Ls, 0, 1)
        arr[c0:c1, a0:a1] |= np.hypot(X - (x1 + t * dx), Y - (y1 + t * dy)) < r

    for it in items:
        cl = it.GetClass()
        if cl == "PCB_TRACK" and it.GetLayer() in tm:
            mk(tm[it.GetLayer()], mm(it.GetStart().x), mm(it.GetStart().y), mm(it.GetEnd().x), mm(it.GetEnd().y), 0.03)
        elif cl == "PCB_VIA":
            p = it.GetPosition()
            for l in LAY:
                mk(tm[l], mm(p.x), mm(p.y), mm(p.x), mm(p.y), 0.12)
        elif cl == "PAD":
            bb = it.GetBoundingBox()
            for l in LAY:
                if it.IsOnLayer(l):
                    a0 = max(0, int((mm(bb.GetLeft()) + 0.05 - wx0) / G)); a1 = min(W, int((mm(bb.GetRight()) - 0.05 - wx0) / G) + 1)
                    c0 = max(0, int((mm(bb.GetTop()) + 0.05 - wy0) / G)); c1 = min(H, int((mm(bb.GetBottom()) - 0.05 - wy0) / G) + 1)
                    if a0 < a1 and c0 < c1:
                        tm[l][c0:c1, a0:a1] = True
    return tm


def find_track(net, pos, layername):
    best = None
    for t in b.GetTracks():
        if t.Type() == pcbnew.PCB_VIA_T or t.GetNetname() != net or t.GetLayerName() != layername:
            continue
        s, e = t.GetStart(), t.GetEnd()
        x1, y1, x2, y2 = mm(s.x), mm(s.y), mm(e.x), mm(e.y)
        dx, dy = x2 - x1, y2 - y1
        L = dx * dx + dy * dy
        tt = 0 if L == 0 else max(0, min(1, ((pos[0] - x1) * dx + (pos[1] - y1) * dy) / L))
        d = math.hypot(pos[0] - (x1 + tt * dx), pos[1] - (y1 + tt * dy))
        if best is None or d < best[0]:
            best = (d, t)
    return best[1] if best and best[0] < 0.2 else None


def find_pad(desc):
    m = re.match(r"Pad (\S+) \[(.*?)\] of (\S+) on", desc)
    f = b.FindFootprintByReference(m.group(3))
    return f.FindPadByNumber(m.group(1)), m.group(2)


drc = json.load(open(DRC))
pairs = [u["items"] for u in drc["unconnected_items"]]
report = []
for k, its in enumerate(pairs, 1):
    try:
        pads = [i for i in its if i["description"].startswith("Pad")]
        trs = [i for i in its if i["description"].startswith("Track")]
        padobj, net = find_pad(pads[0]["description"])
        if os.environ.get("ONLY") and net not in os.environ["ONLY"].split(","):
            continue
        if trs:
            lname = re.search(r" on (.*?)(?:,|$)", trs[0]["description"]).group(1)
            tgt = find_track(net, (trs[0]["pos"]["x"], trs[0]["pos"]["y"]), lname)
            if tgt is None:
                report.append((k, net, "FAIL", "target track not found")); print(report[-1], flush=True); continue
            titems = cluster(tgt)
        else:
            p2, _ = find_pad(pads[1]["description"])
            titems = cluster(p2)
        sp = padobj.GetPosition()
        sx_, sy_ = mm(sp.x), mm(sp.y)
        sl = [l for l in LAY if padobj.IsOnLayer(l)][0]

        def pos_of(i):
            if i.GetClass() == "PCB_TRACK":
                return [(mm(i.GetStart().x), mm(i.GetStart().y)), (mm(i.GetEnd().x), mm(i.GetEnd().y))]
            return [(mm(i.GetPosition().x), mm(i.GetPosition().y))]

        tit = [i for i in titems if min(abs(p[0] - sx_) for p in pos_of(i)) < 45]
        pts_all = [p for i in tit for p in pos_of(i)]
        wx0 = max(X0, min([sx_] + [p[0] for p in pts_all]) - 6); wx1 = min(X1, max([sx_] + [p[0] for p in pts_all]) + 6)
        wy0 = max(Y0, min([sy_] + [p[1] for p in pts_all]) - 6); wy1 = min(Y1, max([sy_] + [p[1] for p in pts_all]) + 6)
        win = (wx0, wy0, int((wx1 - wx0) / G), int((wy1 - wy0) / G))
        W, H = win[2], win[3]
        done = False
        for (w, clr) in eval(os.environ.get("TIERS", "((0.12, 0.14), (0.102, 0.11))")):
            seg, via, pad = prims()
            blk, vblk = raster(win, net, w, clr, seg, via, pad)
            tm = tmask_of(tit, win)
            sx = int((sx_ - wx0) / G)
            sy = int((sy_ - wy0) / G)
            for l in LAY:
                blk[l][max(0, sy - 1):sy + 2, max(0, sx - 1):sx + 2] = False
            res = astar(win, blk, vblk, (sl, sx, sy), tm)
            if res is None:
                continue
            path, nd = res
            pts = []
            for i in path:
                L = i // (H * W)
                r = i % (H * W)
                pts.append((LAY[L], r % W, r // W))

            def clear(l, a, c):
                n = int(max(abs(c[0] - a[0]), abs(c[1] - a[1])) * 2) + 1
                for q in range(n + 1):
                    x = a[0] + (c[0] - a[0]) * q / n
                    y = a[1] + (c[1] - a[1]) * q / n
                    if blk[l][int(round(y)), int(round(x))]:
                        return False
                return True

            out = []
            i = 0
            while i < len(pts):
                l = pts[i][0]
                j = i
                while j + 1 < len(pts) and pts[j + 1][0] == l:
                    j += 1
                run = [(p[1], p[2]) for p in pts[i:j + 1]]
                simp = [run[0]]
                a = 0
                while a < len(run) - 1:
                    c = len(run) - 1
                    while c > a + 1 and not clear(l, run[a], run[c]):
                        c -= 1
                    simp.append(run[c])
                    a = c
                out.append((l, simp))
                i = j + 1
            netinfo = b.FindNet(net)
            nv = 0; ntr = 0; tl = 0.0
            for q, (l, simp) in enumerate(out):
                P = [(wx0 + (x + 0.5) * G, wy0 + (y + 0.5) * G) for x, y in simp]
                if q == 0:
                    P[0] = (sx_, sy_)
                for a, c in zip(P[:-1], P[1:]):
                    if a == c:
                        continue
                    t = pcbnew.PCB_TRACK(b)
                    t.SetStart(pcbnew.VECTOR2I(IU(a[0]), IU(a[1])))
                    t.SetEnd(pcbnew.VECTOR2I(IU(c[0]), IU(c[1])))
                    t.SetWidth(IU(w)); t.SetLayer(l); t.SetNet(netinfo)
                    b.Add(t); ntr += 1; tl += math.hypot(c[0] - a[0], c[1] - a[1])
                if q < len(out) - 1:
                    v = pcbnew.PCB_VIA(b)
                    v.SetPosition(pcbnew.VECTOR2I(IU(P[-1][0]), IU(P[-1][1])))
                    v.SetViaType(pcbnew.VIATYPE_THROUGH)
                    v.SetWidth(IU(VIA_D)); v.SetDrill(IU(VIA_DR))
                    v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu); v.SetNet(netinfo)
                    b.Add(v); nv += 1
            b.BuildConnectivity()
            con = b.GetConnectivity()
            report.append((k, net, "OK", "w=%.3f clr=%.2f tracks=%d vias=%d len=%.1f mm layers=%s" % (w, clr, ntr, nv, tl, ",".join(LNAME[l] for l, _ in out))))
            done = True
            break
        if not done:
            report.append((k, net, "FAIL", "no path"))
    except Exception as e:
        report.append((k, "?", "ERR", repr(e) + traceback.format_exc()[-300:]))
    print(report[-1], flush=True)
b.Save(OUT)
print("saved", OUT)
