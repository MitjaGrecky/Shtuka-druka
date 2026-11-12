#!/usr/bin/env python3
"""Routing statistics of a KiCad board file (any version, no pcbnew needed).

Per net: copper length, via count, ideal length (minimum spanning tree over pad centres) and
detour = copper / ideal. Grouped by net family. Usage: board_stats.py BOARD.kicad_pcb [--nets]
"""
import math
import re
import sys
from collections import defaultdict


def parse(text):
    """Tiny S-expression parser: returns nested lists of str."""
    tok = re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', text)
    stack, cur = [], []
    for t in tok:
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t[1:-1] if t.startswith('"') else t)
    return cur[0]


def find(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def first(node, key):
    f = find(node, key)
    return f[0] if f else None


def net_name(node, nets):
    n = first(node, "net")
    if not n or len(n) < 2:
        return None
    v = n[-1] if len(n) > 2 else n[1]
    return nets.get(v, v)


def family(net):
    n = net.lstrip("/")
    if re.match(r"[A-D]_CS\d+", n):
        return "LED CS"
    if re.match(r"[A-D]_SW\d+", n):
        return "LED SW"
    if re.match(r"E\d_(A|B|SW)$", n):
        return "encoder"
    if n.startswith(("SR_", "~{SR")) or n.startswith("SR"):
        return "shift reg"
    if n.startswith(("TR", "TOUCH")):
        return "touch"
    if n in ("+5V", "GND", "+3V3"):
        return "power"
    return "other"


def mst(points):
    if len(points) < 2:
        return 0.0
    left, tot = set(range(1, len(points))), 0.0
    best = {i: math.dist(points[0], points[i]) for i in left}
    while left:
        i = min(left, key=best.get)
        tot += best[i]
        left.remove(i)
        for j in left:
            best[j] = min(best[j], math.dist(points[i], points[j]))
    return tot


def stats(path):
    root = parse(open(path, encoding="utf-8").read())
    nets = {c[1]: c[2] for c in find(root, "net") if len(c) > 2}   # old format: (net 3 "name")
    length, vias, pads = defaultdict(float), defaultdict(int), defaultdict(list)
    layer_len = defaultdict(float)
    for s in find(root, "segment") + find(root, "arc"):
        n = net_name(s, nets)
        a, b = first(s, "start"), first(s, "end")
        d = math.dist((float(a[1]), float(a[2])), (float(b[1]), float(b[2])))
        length[n] += d
        layer_len[first(s, "layer")[1]] += d
    for v in find(root, "via"):
        vias[net_name(v, nets)] += 1
    for fp in find(root, "footprint"):
        at = first(fp, "at")
        fx, fy = float(at[1]), float(at[2])
        r = math.radians(float(at[3])) if len(at) > 3 else 0.0
        for p in find(fp, "pad"):
            n = net_name(p, nets)
            if not n:
                continue
            pa = first(p, "at")
            dx, dy = float(pa[1]), float(pa[2])
            pads[n].append((fx + dx * math.cos(r) + dy * math.sin(r), fy - dx * math.sin(r) + dy * math.cos(r)))
    rows = []
    for n, pts in pads.items():
        if len(pts) < 2:
            continue
        rows.append((n, family(n), len(pts), length[n], vias[n], mst(pts)))
    return rows, layer_len


def main():
    path = sys.argv[1]
    rows, layer_len = stats(path)
    fam = defaultdict(lambda: [0, 0, 0.0, 0, 0.0])
    for n, f, npads, L, v, ideal in rows:
        a = fam[f]
        a[0] += 1; a[1] += npads; a[2] += L; a[3] += v; a[4] += ideal
    print(f"{'family':10} {'nets':>5} {'pads':>5} {'copper mm':>10} {'ideal mm':>9} {'detour':>7} {'vias':>5}")
    for f, (nn, np_, L, v, ideal) in sorted(fam.items(), key=lambda x: -x[1][2]):
        print(f"{f:10} {nn:5} {np_:5} {L:10.0f} {ideal:9.0f} {L / ideal if ideal else 0:7.2f} {v:5}")
    print("layers:", {k: round(v) for k, v in layer_len.items()})
    if "--nets" in sys.argv:
        print("\nworst detours (signal nets):")
        sig = [r for r in rows if r[1] != "power" and r[5] > 0]
        for n, f, npads, L, v, ideal in sorted(sig, key=lambda r: -(r[3] - r[5]))[:25]:
            print(f"  {n:14} {f:9} pads {npads:3} copper {L:6.1f} ideal {ideal:6.1f} x{L / ideal:4.1f} vias {v}")


if __name__ == "__main__":
    main()
