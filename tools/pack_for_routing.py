#!/usr/bin/env python3
"""Pack one generated board project into hardware/for-routing/<ID>/ for hand routing in EasyEDA Pro.

  python3 tools/pack_for_routing.py ID PROJECT_DIR [--out hardware/for-routing]

PROJECT_DIR holds <name>.kicad_pcb/_sch/_pro, lib tables and gen/design.py (generated beforehand, see
hardware/for-routing/README.md). Writes: ID_kicad7.zip (what EasyEDA Pro imports), BOM.csv (JLCPCB format),
BOM_notes.csv, netlist.net, outline.dxf, schematic.pdf, preview_top.png, preview_bottom.png, README.md.
Needs kicad-cli (7+), pcbnew module, playwright (Chromium) for the PNG previews.
License: AGPL-3.0-or-later.
"""
import csv
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import zipfile
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, "..")
# Generic passives: LCSC numbers used by the generators in earlier sessions; NOT re-checked against LCSC stock
# (the session cannot open arbitrary LCSC pages). Status "verified" only for parts whose page was read (docs 30, 31, job L).
STATUS = json.load(open(os.path.join(REPO, "hardware", "for-routing", "lcsc_status.json")))
DEFAULT_LCSC = {  # (value, footprint) -> LCSC, only where a number is known
    ("100n", "C0402"): "C1525", ("1u", "C0402"): "C52923", ("10u", "C0805"): "C15850", ("10k", "R0402"): "C25744",
    ("4.7k", "R0402"): "C25900", ("1k", "R0402"): "C11702",
}


def load_design(proj):
    gen = os.path.abspath(os.path.join(proj, "gen"))
    sys.path.insert(0, gen)
    spec = importlib.util.spec_from_file_location("design", os.path.join(gen, "design.py"))
    d = importlib.util.module_from_spec(spec)
    sys.modules["design"] = d
    spec.loader.exec_module(d)
    return d


def short_fp(fp):
    return fp.split(":")[-1]


VALUE_LCSC = {"74HC165PW": "C80696", "4x10k": "C25725"}


def lcsc_of(p):
    v = p["fields"].get("LCSC")
    if v:
        return v
    if p["value"] in VALUE_LCSC:
        return VALUE_LCSC[p["value"]]
    if "PinHeader_2x07_P1.27" in p["fp"]:
        return "C3975190"
    key = (p["value"], "R0402" if "R_0402" in p["fp"] else "C0402" if "C_0402" in p["fp"] else "C0805" if "C_0805" in p["fp"] else "")
    return DEFAULT_LCSC.get(key, "")


def write_bom(d, out):
    groups = OrderedDict()
    for p in d.parts():
        ref = p["ref"]
        if ref.startswith("H"):
            continue
        if p["fields"].get("DNP") == "yes":
            key = ("DNP", p["value"], p["fp"], "")
        else:
            key = ("", p["value"], p["fp"], lcsc_of(p))
        groups.setdefault(key, []).append(ref)
    rows, notes = [], []
    for (dnp, val, fp, lc), refs in groups.items():
        refs.sort(key=lambda r: (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0)))
        st = STATUS.get(lc, {}).get("status", "проверить в EasyEDA" if lc else "номера нет: выбрать деталь")
        if dnp:
            notes.append([",".join(refs), val, short_fp(fp), "не ставить (DNP)", ""])
            continue
        rows.append([val, ",".join(refs), short_fp(fp), lc])
        notes.append([",".join(refs), val, short_fp(fp), lc, st])
    with open(os.path.join(out, "BOM.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Comment", "Designator", "Footprint", "LCSC Part #"])
        w.writerows(rows)
    with open(os.path.join(out, "BOM_notes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Designator", "Value", "Footprint", "LCSC", "Status of the LCSC number"])
        w.writerows(notes)
    return rows, notes


def render(pcb, out, w, h):
    from playwright.sync_api import sync_playwright
    tmp = tempfile.mkdtemp()
    shots = {}
    for side, layers in (("top", "F.Cu,F.Silkscreen,F.Fab,Edge.Cuts"), ("bottom", "B.Cu,B.Silkscreen,B.Fab,Edge.Cuts")):
        svg = os.path.join(tmp, side + ".svg")
        cmd = ["kicad-cli", "pcb", "export", "svg", "--layers", layers.replace("Silkscreen", "SilkS"), "--page-size-mode", "2",
               "--exclude-drawing-sheet", "-o", svg, pcb]
        if side == "bottom":
            cmd.insert(-3, "--mirror")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            print("svg failed", side, r.stderr[:300])
            continue
        shots[side] = svg
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for side, svg in shots.items():
            vw = 1800 if w >= h else max(700, int(1500 * w / h))
            vh = int(vw * h / w) if w >= h else 1500
            pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=1)
            html = svg[:-4] + ".html"
            open(html, "w").write(f'<body style="margin:0;background:#fff"><img src="{os.path.basename(svg)}" style="width:{vw}px;height:{vh}px;object-fit:contain"></body>')
            pg.goto("file://" + html)
            pg.wait_for_timeout(400)
            pg.screenshot(path=os.path.join(out, f"preview_{side}.png"))
        b.close()


def main():
    ident, proj = sys.argv[1], os.path.abspath(sys.argv[2])
    root = os.path.abspath(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv else os.path.join(REPO, "hardware", "for-routing")
    out = os.path.join(root, ident)
    os.makedirs(out, exist_ok=True)
    d = load_design(proj)
    pcb, sch, pro = (os.path.join(proj, d.NAME + e) for e in (".kicad_pcb", ".kicad_sch", ".kicad_pro"))
    rows, notes = write_bom(d, out)
    pl = d.placement()
    parts = d.parts()
    holes = sorted((round(pl[p["ref"]][0], 2), round(pl[p["ref"]][1], 2)) for p in parts if p["ref"].startswith("H"))
    conns = [(p["ref"], p["value"]) for p in parts if p["ref"].startswith("J")]
    # package for EasyEDA Pro: KiCad 7 file format (EasyEDA Pro reads KiCad below 10)
    zp = os.path.join(out, f"{ident}_kicad7.zip")
    with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
        for f in (pcb, sch, pro, os.path.join(proj, "fp-lib-table"), os.path.join(proj, "sym-lib-table")):
            if os.path.exists(f):
                z.write(f, os.path.basename(f))
        lib = os.path.join(proj, "lib")
        if not os.path.isdir(lib):
            lib = os.path.join(proj, "..", "m1-screen-knobs", "lib")        # W1 uses the M1 project library
        for dp, _, fs in os.walk(lib):
            for f in fs:
                z.write(os.path.join(dp, f), os.path.join("lib", os.path.relpath(os.path.join(dp, f), lib)))
    subprocess.run(["kicad-cli", "sch", "export", "netlist", "--format", "kicadsexpr", "-o", os.path.join(out, "netlist.net"), sch], capture_output=True)
    subprocess.run(["kicad-cli", "sch", "export", "pdf", "-o", os.path.join(out, "schematic.pdf"), sch], capture_output=True)
    subprocess.run(["kicad-cli", "pcb", "export", "dxf", "--layers", "Edge.Cuts", "--output-units", "mm", "-o", os.path.join(out, "outline.dxf"), pcb], capture_output=True)
    render(pcb, out, d.W, d.H)
    meta = dict(id=ident, name=d.NAME, title=d.TITLE, rev=d.REV, w=d.W, h=d.H, layers=d.LAYERS, parts=len(parts),
                holes=holes, connectors=conns, bom_lines=len(rows))
    json.dump(meta, open(os.path.join(out, "board.json"), "w"), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False))


if __name__ == "__main__":
    main()
