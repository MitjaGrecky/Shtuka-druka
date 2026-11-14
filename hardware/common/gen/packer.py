"""Group placement for boards with many small parts (R2): fixed parts (jacks, ICs, connectors) are given; the rest go in
groups, each packed around its anchor point on one side - spiral search for the nearest free spot. Free = inside the
allowed rectangles (minus an edge margin), not over another courtyard on the same side, not over a through-hole pad
(either side). Uses the same footprint conventions as module_pcb (connectors J* are centred on their pad field).
Result: a placement dict {ref: (x, y, rot, side)} for design.placement(). Not a router and not an optimiser: the user
moves parts by hand later; groups only keep parts next to the jack or IC they belong to.
License: AGPL-3.0-or-later.
"""
import math

import pcbnew

import boardkit as B
import module_pcb as MP

mm = pcbnew.ToMM


_BOARD = []     # footprints need a parent board to be flipped (KiCad 10 crashes otherwise)
_CACHE = {}


def _bbox(D, part, rot, side):
    """Courtyard bbox and through-hole pad boxes, relative to the placement point (module_pcb conventions)."""
    key = (part["fp"], rot, side, part["ref"].startswith(("J", "RV")))
    if key not in _CACHE:
        _CACHE[key] = _bbox_raw(D, part, rot, side)
    return _CACHE[key]


def _bbox_raw(D, part, rot, side):
    if not _BOARD:
        _BOARD.append(pcbnew.BOARD())
    fp = MP.load_fp(D, part["fp"])
    _BOARD[0].Add(fp)
    fp.SetPosition(pcbnew.VECTOR2I(0, 0))
    fp.SetOrientationDegrees(rot)
    if side == "bottom":
        B.flip_bottom(fp)                                   # as module_pcb does
    dx = dy = 0
    if part["ref"].startswith(("J", "RV")):
        xs = [p.GetPosition().x for p in fp.Pads()]
        ys = [p.GetPosition().y for p in fp.Pads()]
        dx, dy = -(min(xs) + max(xs)) // 2, -(min(ys) + max(ys)) // 2
    lay = pcbnew.B_CrtYd if side == "bottom" else pcbnew.F_CrtYd
    c = fp.GetCourtyard(lay)
    bb = c.BBox() if c.OutlineCount() else fp.GetBoundingBox(False)
    box = (mm(bb.GetLeft() + dx), mm(bb.GetTop() + dy), mm(bb.GetRight() + dx), mm(bb.GetBottom() + dy))
    tht = []
    for p in fp.Pads():
        if p.GetAttribute() in (pcbnew.PAD_ATTRIB_PTH, pcbnew.PAD_ATTRIB_NPTH):
            b = p.GetBoundingBox()
            tht.append((mm(b.GetLeft() + dx), mm(b.GetTop() + dy), mm(b.GetRight() + dx), mm(b.GetBottom() + dy)))
    return box, tht


def _hit(a, b, gap):
    return a[0] < b[2] + gap and b[0] < a[2] + gap and a[1] < b[3] + gap and b[1] < a[3] + gap


def _shift(b, x, y):
    return (b[0] + x, b[1] + y, b[2] + x, b[3] + y)


def pack(D, parts, fixed, groups, areas, edge=0.6, gap=0.25, step=0.5, rmax=120.0):
    """fixed: {ref: (x, y, rot, side)}; groups: [(anchor_x, anchor_y, side, [refs], rot)]; areas: [(x0, y0, x1, y1)].
    Returns the full placement; raises if a part finds no spot."""
    P = {p["ref"]: p for p in parts}
    pl = dict(fixed)
    occ = {"top": [], "bottom": []}
    tht = []
    for ref, (x, y, r, side) in fixed.items():
        box, pads = _bbox(D, P[ref], r, side)
        occ[side].append(_shift(box, x, y))
        tht += [_shift(b, x, y) for b in pads]
    inner = [(a[0] + edge, a[1] + edge, a[2] - edge, a[3] - edge) for a in areas]

    def inside(b):
        # every corner inside some area rectangle (areas may touch: a tab under the main board)
        corners = ((b[0], b[1]), (b[2], b[1]), (b[0], b[3]), (b[2], b[3]))
        return all(any(a[0] <= cx <= a[2] and a[1] <= cy <= a[3] for a in inner) for cx, cy in corners)

    for ax, ay, side, refs, rot in groups:
        sized = []
        for ref in refs:
            box, pads = _bbox(D, P[ref], rot, side)
            sized.append(((box[2] - box[0]) * (box[3] - box[1]), ref, box, pads))
        for _, ref, box, pads in sorted(sized, key=lambda t: -t[0]):
            spot = None
            r = 0.0
            while spot is None and r <= rmax:
                n = max(1, int(2 * math.pi * r / step)) if r else 1
                for k in range(n):
                    a = 2 * math.pi * k / n
                    x, y = round((ax + r * math.cos(a)) / 0.1) * 0.1, round((ay + r * math.sin(a)) / 0.1) * 0.1
                    b = _shift(box, x, y)
                    if not inside(b):
                        continue
                    if any(_hit(b, o, gap) for o in occ[side]) or any(_hit(b, t, gap) for t in tht):
                        continue
                    pb = [_shift(t, x, y) for t in pads]
                    if pb and any(_hit(t, o, gap) for t in pb for o in occ["top" if side == "bottom" else "bottom"]):
                        continue
                    spot = (x, y)
                    break
                r += step
            if spot is None:
                raise RuntimeError(f"no room for {ref} near ({ax}, {ay}) on {side}")
            x, y = spot
            pl[ref] = (x, y, rot, side)
            occ[side].append(_shift(box, x, y))
            tht += [_shift(t, x, y) for t in pads]
    return pl
