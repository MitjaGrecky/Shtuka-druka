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


_PADS = {}


def _padpos(D, part, rot, side):
    """{pad number: (x, y)} relative to the placement point (same conventions as _bbox)."""
    key = (part["fp"], rot, side, part["ref"].startswith(("J", "RV")))
    if key not in _PADS:
        if not _BOARD:
            _BOARD.append(pcbnew.BOARD())
        fp = MP.load_fp(D, part["fp"])
        _BOARD[0].Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(0, 0))
        fp.SetOrientationDegrees(rot)
        if side == "bottom":
            B.flip_bottom(fp)
        dx = dy = 0
        if part["ref"].startswith(("J", "RV")):
            xs = [q.GetPosition().x for q in fp.Pads()]
            ys = [q.GetPosition().y for q in fp.Pads()]
            dx, dy = -(min(xs) + max(xs)) // 2, -(min(ys) + max(ys)) // 2
        d = {}
        for q in fp.Pads():
            d.setdefault(q.GetNumber(), (mm(q.GetPosition().x + dx), mm(q.GetPosition().y + dy)))
        _PADS[key] = d
    return _PADS[key]


def _hit(a, b, gap):
    return a[0] < b[2] + gap and b[0] < a[2] + gap and a[1] < b[3] + gap and b[1] < a[3] + gap


def _shift(b, x, y):
    return (b[0] + x, b[1] + y, b[2] + x, b[3] + y)


FINE_FP = ("QFN", "DFN", "VSON", "SSOP", "TSSOP", "MSOP", "VSSOP", "LQFP", "TQFP", "SOT-363")   # footprints with a 0.4-0.65 mm pitch (fan-out needs a free ring)


def _fine(p):
    return p["ref"].startswith(("U", "Q")) and any(k in p["fp"] for k in FINE_FP)


def _grow(b, d):
    return (b[0] - d, b[1] - d, b[2] + d, b[3] + d)


GND_NAMES = ("GND", "AGND", "DGND", "PGND", "GNDA", "GNDD", "BAT_N")


def _is_gnd(n):
    u = (n or "").strip("/").upper()
    return u.startswith("GND") or u in GND_NAMES or u.endswith("_GND")


def _is_power(n):
    """Supply net by name: +3V3, -12V, VDD/VCC/VBUS/VREG/VSYS/VIN/AVDD/DVDD..., not an RC filter on a signal input (CVIN3, RUN)."""
    import re
    u = (n or "").strip("/").upper()
    return bool(re.match(r"^[+-]\d", u) or re.search(r"(^|_)(VDD|VCC|VBUS|VREG|VSYS|VIN|VOUT|VBAT|PVIN|AVDD|DVDD|IOVDD|LDO|BUS|SYS|PMID|REGN|V\d)", u)
                or re.search(r"(VDD|VCC|VBUS)", u))


def _is_ic(ref):
    return ref.startswith(("U", "Q"))


def _capval(v):
    """'100n', '4.7uF', '10u 25V' -> farads (unknown -> 1, i.e. placed last)."""
    import re
    m = re.match(r"\s*([0-9.]+)\s*([pnuµm]?)", str(v))
    if not m:
        return 1.0
    try:
        return float(m.group(1)) * {"p": 1e-12, "n": 1e-9, "u": 1e-6, "µ": 1e-6, "m": 1e-3, "": 1.0}[m.group(2)]
    except ValueError:
        return 1.0


def pin_targets(parts, movable, group_of):
    """Rule A-037 (20.11.2026): which passive belongs at which IC pin. {ref: (ic_ref, pad, net, kind)}.
    kind 'decap': a C between a power net and GND whose power net reaches a U/Q pin; the IC is the least loaded per pin, then the
    nearest in the parts list (the schematic generators define the capacitors next to their IC); among its pins on that net the least
    loaded one (ICs balanced by capacitors per pin), smallest capacitors first (100 nF closest, bulk next).
    kind 'pin': a C/R/L/D/FB on a net of at most 4 pads with exactly one U/Q pad (compensation, feedback, bootstrap, switch-node
    inductor, catch diode, series resistor): next to that pin."""
    from collections import Counter, defaultdict
    netpads = defaultdict(list)
    for p in parts:
        for pad, n in p["pins"].items():
            if n:
                netpads[n].append((p["ref"], pad))
    order = {p["ref"]: k for k, p in enumerate(parts)}
    load, out, decs = Counter(), {}, []
    for p in parts:
        r = p["ref"]
        if r not in movable or not r.startswith("C") or len(p["pins"]) != 2:
            continue
        nets = list(p["pins"].values())
        g = [n for n in nets if _is_gnd(n)]
        pw = [n for n in nets if n and not _is_gnd(n)]
        if len(g) == 1 and len(pw) == 1:
            ics = [(rr, pad) for rr, pad in netpads[pw[0]] if _is_ic(rr)]
            if ics:
                decs.append((_capval(p["value"]), order[r], r, pw[0], ics))
    for _, _, r, net, ics in sorted(decs):
        cand = ics      # no same-group preference: autoplace puts power-only parts into an arbitrary group (A1: 9 caps on one pin)
        npins = Counter(x[0] for x in cand)
        icload = Counter()
        for (q, _), v in load.items():
            if (q, _) in cand:
                icload[q] += v
        ic = min(npins, key=lambda q: (icload[q] / npins[q], abs(order[q] - order[r]), q))   # spread over the ICs per pin, then nearest
        best = min((x for x in cand if x[0] == ic), key=lambda x: (load[x], x[1]))
        load[best] += 1
        out[r] = (ic, best[1], net, "decap")
    for p in parts:
        r = p["ref"]
        if r in out or r not in movable or _is_ic(r) or not r.startswith(("C", "R", "L", "D", "FB")):
            continue
        best = None
        for pad, n in p["pins"].items():
            if not n or _is_gnd(n):
                continue
            ic = [x for x in netpads[n] if _is_ic(x[0])]
            if len(netpads[n]) <= 4 and len(ic) == 1 and (best is None or len(netpads[n]) < best[0]):
                best = (len(netpads[n]), ic[0], n)
        if best:
            out[r] = (best[1][0], best[1][1], best[2], "pin")
    return out


def pack(D, parts, fixed, groups, areas, edge=0.6, gap=0.25, step=0.5, rmax=120.0, ic_gap=None, pin_rule=None, tight_gap=0.0, pin_gap=0.5):
    """ic_gap (rev 20.11.2026, routing analysis tools/placement_analysis.py): extra courtyard gap around the fine-pitch ICs (QFN, TSSOP, ...), so that
    the 0.4-0.65 mm pins can fan out; default = gap (old behaviour).
    pin_rule (rev 20.11.2026, audit A-037; default on, env PLACE_PINRULE=0 turns it off): the ICs of every group are placed first; then each
    decoupling capacitor goes to its power pin and each own-pin passive (pin_targets) to its pin, searched from the pin itself, courtyard gap
    tight_gap (decap) / min(gap, pin_gap) (own-pin), ic_gap NOT applied to them; then the rest as before (gap, ic_gap). Order: HF decoupling (<= 1 uF), own-pin parts, bulk capacitors. P118: HF supply decoupling of a 0.4 mm pitch QFN goes under its pin on the
    other side (via <= 0.3 mm within 1.5 mm of the pin is the router's job). A part that finds no
    spot within 15 mm of its pin falls back to its group.

    fixed: {ref: (x, y, rot, side)}; groups: [(anchor_x, anchor_y, side, [refs], rot)]; areas: [(x0, y0, x1, y1)].
    Returns the full placement; raises if a part finds no spot."""
    import os
    if pin_rule is None:
        pin_rule = os.environ.get("PLACE_PINRULE", "1") != "0"
    tight_gap = float(os.environ.get("PLACE_TIGHT", tight_gap))
    under = os.environ.get("PLACE_UNDER", "1") != "0"   # P118 (20.11.2026); PLACE_UNDER=0: same side
    P = {p["ref"]: p for p in parts}
    grow = max(0.0, (ic_gap - gap)) if ic_gap else 0.0
    pl = dict(fixed)
    occ = {"top": [], "bottom": []}       # (raw courtyard box, box the other parts keep `gap` from)
    tht = []

    def occupy(ref, box, pads, x, y, side, tight=False):
        raw = _shift(box, x, y)
        occ[side].append((raw, _shift(_grow(box, grow), x, y) if (_fine(P[ref]) and not tight) else raw))
        tht.extend(_shift(b, x, y) for b in pads)

    for ref, (x, y, r, side) in fixed.items():
        box, pads = _bbox(D, P[ref], r, side)
        occupy(ref, box, pads, x, y, side)
    inner = [(a[0] + edge, a[1] + edge, a[2] - edge, a[3] - edge) for a in areas]

    def inside(b):
        # every corner inside some area rectangle (areas may touch: a tab under the main board)
        corners = ((b[0], b[1]), (b[2], b[1]), (b[0], b[3]), (b[2], b[3]))
        return all(any(a[0] <= cx <= a[2] and a[1] <= cy <= a[3] for a in inner) for cx, cy in corners)

    def free(b, pads, side, g, raw):
        if not inside(b):
            return False
        k = 0 if raw else 1
        if any(_hit(b, o[k], g) for o in occ[side]) or any(_hit(b, t, g) for t in tht):
            return False
        other = "top" if side == "bottom" else "bottom"
        return not (pads and any(_hit(t, o[0], g) for t in pads for o in occ[other]))

    def place_near(ref, ax, ay, side, rot):
        box, pads = _bbox(D, P[ref], rot, side)
        r = 0.0
        while r <= rmax:
            n = max(1, int(2 * math.pi * r / step)) if r else 1
            for k in range(n):
                a = 2 * math.pi * k / n
                x, y = round((ax + r * math.cos(a)) / 0.1) * 0.1, round((ay + r * math.sin(a)) / 0.1) * 0.1
                if free(_shift(box, x, y), [_shift(t, x, y) for t in pads], side, gap, False):
                    pl[ref] = (x, y, rot, side)
                    occupy(ref, box, pads, x, y, side)
                    return
            r += step
        raise RuntimeError(f"no room for {ref} near ({ax}, {ay}) on {side}")

    def place_at_pin(ref, ic, pad, net, kind):
        ix, iy, irot, side = pl[ic]
        pp = _padpos(D, P[ic], irot, side).get(pad)
        if (kind == "decap" and under and "P0.4mm" in P[ic]["fp"] and _capval(P[ref]["value"]) <= 1.1e-6
                and _is_power(net)):
            side = "top" if side == "bottom" else "bottom"   # P118: HF decoupling of a 0.4 mm pitch QFN under its pin on the other side
        if pp is None:
            return False
        tx, ty = ix + pp[0], iy + pp[1]
        mine = [q for q, nn in P[ref]["pins"].items() if nn == net][:1]
        g = tight_gap if kind == "decap" else min(gap, pin_gap)
        found, r, stop, st = [], 0.0, None, 0.25
        while r <= 15.0 and (stop is None or r <= stop):
            n = max(1, int(2 * math.pi * r / st)) if r else 1
            for rot in (0, 90, 180, 270):
                box, pads = _bbox(D, P[ref], rot, side)
                mp = _padpos(D, P[ref], rot, side).get(mine[0]) if mine else (0.0, 0.0)
                for k in range(n):
                    a = 2 * math.pi * k / n
                    x, y = round((tx + r * math.cos(a)) / 0.05) * 0.05, round((ty + r * math.sin(a)) / 0.05) * 0.05
                    if free(_shift(box, x, y), [_shift(t, x, y) for t in pads], side, g, True):
                        found.append((math.hypot(x + mp[0] - tx, y + mp[1] - ty), x, y, rot, box, pads))
            if found and stop is None:
                stop = r + 0.75
            r += st
        if not found:
            return False
        _, x, y, rot, box, pads = min(found, key=lambda t: t[0])
        pl[ref] = (x, y, rot, side)
        occupy(ref, box, pads, x, y, side, tight=True)
        return True

    group_of = {ref: k for k, (_, _, _, refs, _) in enumerate(groups) for ref in refs}
    targets = pin_targets(parts, set(group_of), group_of) if pin_rule else {}
    rest = []
    for k, (ax, ay, side, refs, rot) in enumerate(groups):
        sized = [(((lambda b: (b[2] - b[0]) * (b[3] - b[1]))(_bbox(D, P[ref], rot, side)[0])), ref) for ref in refs]
        sized = sorted(sized, key=lambda t: -t[0])
        for _, ref in sized:
            if pin_rule and _is_ic(ref):
                place_near(ref, ax, ay, side, rot)        # phase 1: the ICs of the group
            elif ref not in targets:
                rest.append((k, ref))
    if pin_rule:
        first = {}                                        # P116: the first (smallest) bulk capacitor of each bank (net + pin) goes before the rest
        for ref, (ic, pad, net, kind) in sorted(targets.items(), key=lambda t: (_capval(P[t[0]]["value"]), t[0])):
            if kind == "decap" and _capval(P[ref]["value"]) > 1.1e-6:
                first.setdefault((net, ic, pad), ref)
        firsts = set(first.values())

        def prio(t):                                      # HF decoupling (<= 1 uF), first of each bulk bank, own-pin parts (switch node L/D, FB, COMP), rest of the banks
            ref, (_, _, _, kind) = t
            if kind == "decap":
                v = _capval(P[ref]["value"])
                if v <= 1.1e-6:
                    return (0, 0 if _is_power(t[1][2]) else 1, v, ref)   # supply decoupling before RC filters on signal inputs
                return (1 if ref in firsts else 3, 0, v, ref)
            return (2, 0, 0, ref)
        tl = sorted(targets.items(), key=prio)
        for ref, (ic, pad, net, kind) in tl:              # phase 2: decoupling and own-pin passives at their pins
            if ic not in pl or not place_at_pin(ref, ic, pad, net, kind):
                rest.append((group_of[ref], ref))
                if os.environ.get("PLACE_DEBUG"):
                    import sys
                    print(f"pin rule: {ref} ({kind}, {net}) no spot within 15 mm of {ic}.{pad}" + ("" if ic in pl else " (IC not placed yet)"), file=sys.stderr)
    for k, ref in rest:                                   # phase 3: everything else around the group anchor
        ax, ay, side, _, rot = groups[k]
        place_near(ref, ax, ay, side, rot)
    return pl
