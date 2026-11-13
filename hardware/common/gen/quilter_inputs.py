#!/usr/bin/env python3
"""Input files for a Quilter (quilter.ai) route-only job of any generated board (pcbnew Python, no kicad-cli):
the placed board, the schematic and the project file (uploaded separately), and the Circuit Comprehension
tables as CSV (columns as Quilter exports them; capacitance in nF, current in mA).

  python quilter_inputs.py hardware/m3-tempo-swing OUT_DIR

Bypass capacitors: each capacitor whose other side is GND is assigned to the nearest IC (U*) or connector (J*)
that has a pin on the capacitor's supply net, at that pin. High-current nets: +5V and GND 800 mA, +3V3 100 mA,
LED anode rows *_SW* 300 mA (LP5864: 6 LEDs x 3 CS x 15 mA). Ground: GND, primary.
Mounting holes, encoders, LEDs and connectors stay locked as make_pcb left them (Quilter keeps parts inside the
outline where they are). License: AGPL-3.0-or-later.
"""
import importlib.util
import math
import os
import re
import shutil
import sys

import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import boardkit as B  # noqa: E402


def load_design(proj):
    spec = importlib.util.spec_from_file_location("design_q", os.path.join(proj, "gen", "design.py"))
    d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d)
    return d


def nf(value):
    v = value.lower().replace("f", "")
    for suf, k in (("p", 1e-3), ("n", 1.0), ("u", 1e3), ("m", 1e6)):
        if v.endswith(suf):
            return float(v[:-1]) * k
    return float(v) * 1e9


def bypass(D):
    parts = {p["ref"]: p for p in D.parts()}
    pl = D.placement()
    rows = []
    for ref, p in parts.items():
        if not ref.startswith("C") or p["fields"].get("DNP") == "yes":
            continue
        nets = [n for n in p["pins"].values() if n]
        if "GND" not in nets or len(set(nets)) != 2:
            continue
        sup = [n for n in nets if n != "GND"][0]
        best = None
        for r2, q in parts.items():
            if not r2.startswith(("U", "J")):
                continue
            pins = [pn for pn, n in q["pins"].items() if n == sup]
            if not pins or r2 not in pl or ref not in pl:
                continue
            d = math.hypot(pl[r2][0] - pl[ref][0], pl[r2][1] - pl[ref][1])
            if best is None or d < best[0]:
                best = (d, r2, sorted(pins, key=lambda s: (len(s), s))[0])
        if best:
            u, pin = best[1], best[2]
            m = re.search(r"\(pin (\d+)\)", p["fields"].get("Note", ""))       # kit.lp5864 notes: "VLED (pin 15)"
            pins = [pn for pn, n in parts[u]["pins"].items() if n == sup]
            if m and m.group(1) in pins:
                pin = m.group(1)
            else:                                                             # a supply pin by name, not a tied-up input
                named = [pn for pn in pins if re.search(r"V(CC|DD|IO|LED|IN)|^V\+|PWR", B.pin_name(parts[u]["lib"], pn) or "", re.I)]
                if named:
                    pin = sorted(named, key=lambda s: (len(s), s))[0]
            rows.append((ref, u, pin, nf(p["value"])))
    return rows


def power(D):
    nets = {n for p in D.parts() for n in p["pins"].values() if n}
    out = [(n, ma) for n, ma in (("+5V", 800), ("GND", 800), ("+3V3", 100)) if n in nets]
    out += [("/" + n, 300) for n in sorted(nets) if "_SW" in n and n[0] in "ABCDLR" and n.split("_SW")[1].isdigit()]
    return out


def main(proj, out):
    proj, out = os.path.abspath(proj), os.path.abspath(out)
    D = load_design(proj)
    os.makedirs(out, exist_ok=True)
    for ext in (".kicad_pcb", ".kicad_sch", ".kicad_pro"):
        shutil.copy(os.path.join(proj, D.NAME + ext), os.path.join(out, D.NAME + ext))
    b = pcbnew.LoadBoard(os.path.join(out, D.NAME + ".kicad_pcb"))
    assert not [t for t in b.GetTracks()], "the board must have no tracks or vias (Quilter treats them as fixed)"
    rows = {
        "bypass_capacitors.csv": ["capacitor,bypassed_component,bypassed_pin,capacitance"] +
                                 [f"{c},{u},{p},{v:g}" for c, u, p, v in bypass(D)],
        "high_current_nets.csv": ["net_name,max_current,use_power_pour"] + [f"{n},{ma},false" for n, ma in power(D)],
        "ground_nets.csv": ["net_name,is_primary,use_region_pour", "GND,true,false"],
    }
    for name, lines in rows.items():
        with open(os.path.join(out, name), "w", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
    print("ok", out, "; bypass", len(rows["bypass_capacitors.csv"]) - 1, "; high-current", len(rows["high_current_nets.csv"]) - 1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
