"""Rough automatic placement for boards whose mechanics are not fixed yet (PW, R1, A1, P2): connectors in a row along the
bottom edge (top side), every IC / transistor / relay / crystal / inductor an anchor on a grid, passives and diodes packed
(packer.py) around the anchor they share most signal nets with. For routing in EasyEDA Pro / Quilter: placement is a starting
point and is expected to be changed by hand. License: AGPL-3.0-or-later.
"""
import math
import sys
from collections import Counter, defaultdict

import packer

ANCHOR = ("U", "Q", "K", "Y", "L", "F", "ENC")

GAPS = (1.4, 1.2, 1.0, 0.8, 0.6, 0.4, 0.25)   # rule template 20.11.2026: the largest courtyard gap that fits the outline


def fit(D, place, gaps=GAPS):
    """place(gap, ic_gap) -> placement. Tries the gaps from the largest; the first that fits wins. ic_gap (fine-pitch ICs) = gap + 0.6,
    at most 2.0. Env PLACE_GAP (and PLACE_ICGAP) force one value. Sets D.PLACED_GAP / D.PLACED_ICGAP (README records them)."""
    import os
    if os.environ.get("PLACE_GAP"):
        gaps = (float(os.environ["PLACE_GAP"]),)
    err = None
    for g in gaps:
        ic = float(os.environ["PLACE_ICGAP"]) if os.environ.get("PLACE_ICGAP") else min(2.0, round(g + 0.6, 2))
        try:
            r = place(g, ic)
        except RuntimeError as e:
            err = e
            continue
        D.PLACED_GAP, D.PLACED_ICGAP = g, ic
        print(f"placement: gap {g} ic_gap {ic}", file=sys.stderr)
        return r
    raise err


def place(D, fixed=None, margin=6.0, conn_y=None, skip_anchor=(), conn_side="top", follow=(), gap=0.25, ic_gap=None):
    """follow: fixed parts (e.g. ICs placed by hand) whose small parts gather around them, on their side (16.11.2026, PW LDOs)."""
    P = D.parts()
    fixed = dict(fixed or {})
    byref = {p["ref"]: p for p in P}
    W, H = D.W, D.H
    # signal nets: not on every part (power, ground)
    cnt = Counter(n for p in P for n in set(p["pins"].values()) if n)
    sig = {n for n, c in cnt.items() if c <= 8}
    # connectors along the bottom edge, top side
    conns = [p["ref"] for p in P if p["ref"].startswith("J") and p["ref"] not in fixed]
    x, y, rowh = margin, (conn_y if conn_y else H - margin), 0
    for r in conns:
        box, _ = packer._bbox(D, byref[r], 0, conn_side)
        w, h = box[2] - box[0], box[3] - box[1]
        if x + w > W - margin:
            x, y = margin, y - rowh - 2
            rowh = 0
        fixed[r] = (round(x - box[0], 1), round(y - box[3], 1), 0, conn_side)
        x += w + 2
        rowh = max(rowh, h)
    for p in P:                                            # holes keep the corners
        if p["ref"].startswith("H") and p["ref"] not in fixed:
            i = int(p["ref"][1:]) - 1
            fixed[p["ref"]] = [(3, 3), (W - 3, 3), (3, H - 3), (W - 3, H - 3)][i % 4] + (0, "top")
    anchors = [p["ref"] for p in P if p["ref"] not in fixed and p["ref"].startswith(ANCHOR) and p["ref"] not in skip_anchor]
    area = max(1.0, (W - 2 * margin) * (H - 2 * margin - (H - conns_top(fixed, H))))
    n = max(1, len(anchors))
    cols = max(1, round(math.sqrt(n * (W - 2 * margin) / max(1.0, (conns_top(fixed, H) - 2 * margin)))))
    rows = math.ceil(n / cols)
    top = conns_top(fixed, H)
    cw, ch = (W - 2 * margin) / cols, (top - 2 * margin) / rows
    # order anchors by connectivity: neighbours get adjacent cells (greedy chain)
    nets_of = {r: {nn for nn in byref[r]["pins"].values() if nn in sig} for r in anchors}
    order, left = [], list(anchors)
    if left:
        cur = max(left, key=lambda r: len(nets_of[r]))
        while left:
            left.remove(cur)
            order.append(cur)
            if left:
                cur = max(left, key=lambda r: len(nets_of[r] & nets_of[order[-1]]) * 1000 + len(nets_of[r]))
    pos = {}
    for k, r in enumerate(order):
        rr, cc = divmod(k, cols)
        if rr % 2:
            cc = cols - 1 - cc
        pos[r] = (margin + cw * (cc + 0.5), margin + ch * (rr + 0.5))
    groups = defaultdict(list)
    for p in P:
        r = p["ref"]
        if r in fixed:
            continue
        if r in pos:
            groups[r].append(r)
            continue
        mine = {nn for nn in p["pins"].values() if nn in sig}
        best, bs = None, 0
        for a in list(follow) + list(pos) + [c for c in conns if c in fixed]:
            s = len(mine & {nn for nn in byref[a]["pins"].values() if nn in sig})
            if s > bs:
                best, bs = a, s
        if best is None:                                   # only power nets: next to the nearest-numbered anchor
            best = order[len(groups) % len(order)] if order else conns[0]
        groups[best].append(r)
    G = []
    for a, refs in groups.items():
        ax, ay = (pos[a] if a in pos else fixed[a][:2])
        G.append((ax, ay, fixed[a][3] if a in follow else "bottom", refs, 0))
    return packer.pack(sys.modules[D.__name__], P, fixed, G, [(0, 0, W, H)], rmax=max(W, H), gap=gap, ic_gap=ic_gap)


def conns_top(fixed, H):
    ys = [v[1] for k, v in fixed.items() if k.startswith("J") and v[1] > H / 2 and v[3] == "bottom" or k.startswith("J") and v[1] > H - 20]
    return (min(ys) - 8) if ys else H
