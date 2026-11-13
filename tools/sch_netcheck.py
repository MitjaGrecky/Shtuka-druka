#!/usr/bin/env python3
"""Check a generated parts-sheet schematic (module_sch.write_grid / make_sch writers) against its design.py without
kicad-cli (it crashes the PC): for every placed symbol unit, the end of every pin is computed from the lib_symbols in the
file; the label, power symbol or no-connect sitting on that point gives the pin's net. Compared pin by pin with design.py.

  python tools/sch_netcheck.py hardware/r2-control

Works for sheets where nets are made by labels and power symbols on pin ends (no wires) - the way our writers draw.
License: AGPL-3.0-or-later.
"""
import importlib.util
import math
import os
import re
import sys


def sexpr(txt):
    stack, cur = [], []
    for t in re.findall(r'\(|\)|"(?:[^"\\]|\\.)*"|[^\s()]+', txt):
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t.strip('"') if t.startswith('"') else t)
    return cur[0]


def kids(n, key):
    return [c for c in n if isinstance(c, list) and c and c[0] == key]


def lib_pins(sym):
    """{unit: [(number, x, y)]} of a lib symbol; unit 0 = all units."""
    name = sym[1].split(":")[-1]
    out = {}
    for sub in kids(sym, "symbol"):
        m = re.match(re.escape(name) + r"_(\d+)_(\d+)$", sub[1])
        if not m or m.group(2) not in ("0", "1"):
            continue
        for p in kids(sub, "pin"):
            at = kids(p, "at")[0]
            num = kids(p, "number")[0][1]
            out.setdefault(int(m.group(1)), []).append((num, float(at[1]), float(at[2])))
    return out


def rot(x, y, r):
    a = math.radians(r)
    return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def key(x, y):
    return (round(x, 2), round(y, 2))


def main(proj):
    spec = importlib.util.spec_from_file_location("d", os.path.join(proj, "gen", "design.py"))
    D = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(D)
    root = sexpr(open(os.path.join(proj, D.NAME + ".kicad_sch"), encoding="utf-8").read())
    libs = {s[1]: lib_pins(s) for s in kids(kids(root, "lib_symbols")[0], "symbol")}
    at_point = {}
    for lb in kids(root, "label") + kids(root, "global_label"):
        at = kids(lb, "at")[0]
        at_point.setdefault(key(float(at[1]), float(at[2])), set()).add(lb[1])
    for nc in kids(root, "no_connect"):
        at = kids(nc, "at")[0]
        at_point.setdefault(key(float(at[1]), float(at[2])), set()).add(None)
    placed = []
    for s in kids(root, "symbol"):
        lib = kids(s, "lib_id")[0][1]
        at = kids(s, "at")[0]
        x, y, r = float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0
        unit = int(kids(s, "unit")[0][1])
        ref = [p[2] for p in kids(s, "property") if p[1] == "Reference"][0]
        if lib.startswith("power:"):
            if "PWR_FLAG" not in lib:
                at_point.setdefault(key(x, y), set()).add(lib.split(":")[1])
            continue
        placed.append((ref, lib, x, y, r, unit))
    got = {}
    for ref, lib, x, y, r, unit in placed:
        units = libs[lib]
        for num, px, py in units.get(unit, []) + (units.get(0, []) if unit else []):
            dx, dy = rot(px, py, r)
            names = at_point.get(key(x + dx, y - dy), set())
            got.setdefault(ref, {})[num] = names
    bad, n = [], 0
    for p in D.parts():
        for num, want in p["pins"].items():
            n += 1
            names = got.get(p["ref"], {}).get(num)
            if names is None:
                bad.append((p["ref"], num, want, "pin not placed"))
            elif want is None:
                if names - {None}:
                    bad.append((p["ref"], num, want, names))
            elif names != {want}:
                bad.append((p["ref"], num, want, names))
    print(f"{len(placed)} symbol units, {n} design pins checked, {len(bad)} mismatches")
    for b in bad[:20]:
        print("  ", b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
