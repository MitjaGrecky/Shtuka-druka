#!/usr/bin/env python3
"""Compare a KiCad netlist (.net, export version E) with a pin -> net dump, by pin sets (net names may differ).

Usage: netcompare.py NETLIST.net DUMP.json
DUMP.json: {"comps": {"U1": [["1", "GND"], ["2", ""]], ...}}  ("" = pin not connected),
or the bridge reply {"result": {"comps": ...}}. Used by eda_check.py.
License: AGPL-3.0-or-later.
"""
import json
import re
import sys
from collections import defaultdict


def read_kicad_net(path):
    txt = open(path, encoding="utf-8").read()
    refs = set(re.findall(r'\(comp\s+\(ref\s+"([^"]+)"\)', txt))
    nets = {}
    # KiCad 7 writes one line per node, KiCad 10 one token per line: whitespace-tolerant patterns
    for m in re.finditer(r'\(net\s+\(code\s+"?\d+"?\)\s+\(name\s+"((?:[^"\\]|\\.)*)"\)(.*?)(?=\(net\s+\(code|\Z)', txt, re.S):
        nets[m.group(1)] = {f"{r}.{p}" for r, p in re.findall(r'\(node\s+\(ref\s+"([^"]+)"\)\s+\(pin\s+"([^"]+)"\)', m.group(2))}
    return refs, nets


def compare(netlist, comps):
    """Return a dict with counts and lists of problems."""
    refs, kic = read_kicad_net(netlist)
    pin2eda, eda = {}, defaultdict(set)
    for ref, pads in comps.items():
        for pin, net in pads:
            pin2eda[f"{ref}.{pin}"] = net
            if net:
                eda[net].add(f"{ref}.{pin}")
    multi = {n: p for n, p in kic.items() if len(p) >= 2}
    bad = []
    for n, pins in sorted(multi.items()):
        got = defaultdict(int)
        for p in pins:
            got[pin2eda.get(p, "<no pin>")] += 1
        if len(got) == 1:
            e = next(iter(got))
            if e and e != "<no pin>" and eda[e] == pins:
                continue
            got = {e: len(eda.get(e, ()))}
        bad.append((n, len(pins), dict(got)))
    pin2kic = {p: n for n, ps in kic.items() for p in ps}
    merges = []
    for e, ps in sorted(eda.items()):
        ks = defaultdict(int)
        for p in ps:
            ks[pin2kic.get(p, "<not in netlist>")] += 1
        if len(ks) > 1:
            merges.append((e, len(ps), dict(ks)))
    return {
        "parts_netlist": len(refs), "parts_eda": len(comps),
        "missing": sorted(refs - set(comps)), "extra": sorted(set(comps) - refs),
        "nets": len(multi), "matched": len(multi) - len(bad), "mismatched": bad, "merges": merges,
    }


def report(title, r):
    out = [f"**{title}:** parts {r['parts_eda']} / {r['parts_netlist']}, "
           f"nets (2+ pins) {r['matched']} / {r['nets']} matched"]
    if r["missing"]:
        out.append(f"- missing parts: {', '.join(r['missing'])}")
    if r["extra"]:
        out.append(f"- extra parts: {', '.join(r['extra'])}")
    for n, k, d in r["mismatched"]:
        out.append(f"- net `{n}` ({k} pins) -> {d}")
    for e, k, d in r["merges"]:
        out.append(f"- MERGE: EasyEDA net `{e}` ({k} pins) joins {d}")
    return "\n".join(out)


if __name__ == "__main__":
    d = json.load(open(sys.argv[2], encoding="utf-8"))
    d = d.get("result", d)
    print(report(sys.argv[2], compare(sys.argv[1], d["comps"])))
