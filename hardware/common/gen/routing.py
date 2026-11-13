"""Autorouting of a placed board with Freerouting 1.9 through KiCad's pcbnew Python module (no kicad-cli), then
GND pours on both outer layers and stitching vias - the same steps as M1's and W1's make_pcb.py, as a library.

  python routing.py BOARD.kicad_pcb --jar freerouting-1.9.0.jar [--passes 100] [--out ROUTED.kicad_pcb] [--no-pour]

The board's .kicad_pro (next to it) carries the net classes (Default, Power, LED_SW of boardkit.write_project);
pcbnew exports them into the DSN, so Freerouting uses the same widths and clearances.
On Windows Freerouting opens its own window while it works and is stopped once the session file is written.
License: AGPL-3.0-or-later.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

import pcbnew

mm = pcbnew.FromMM


def _sexpr(txt):
    """Minimal s-expression reader: nested lists of strings."""
    stack, cur = [], []
    for t in re.findall(r'\(|\)|"[^"]*"|[^\s()]+', txt):
        if t == "(":
            stack.append(cur)
            cur = []
        elif t == ")":
            done, cur = cur, stack.pop()
            cur.append(done)
        else:
            cur.append(t.strip('"'))
    return cur[0]


def _kids(node, key):
    return [c for c in node if isinstance(c, list) and c and c[0] == key]


def run_freerouting(b, jar, passes, work):
    dsn, ses = os.path.join(work, "board.dsn"), os.path.join(work, "board.ses")
    assert pcbnew.ExportSpecctraDSN(b, dsn), "DSN export failed"
    java = shutil.which("java") or "java"
    cmd = [java, "-jar", jar, "-de", dsn, "-do", ses, "-mp", str(passes)]
    if os.name != "nt" and not os.environ.get("DISPLAY"):
        cmd = ["xvfb-run", "-a"] + cmd
    print(" ".join(cmd), flush=True)
    proc = subprocess.Popen(cmd)
    t0 = time.time()
    while proc.poll() is None:                   # 1.9 sometimes keeps running after it saved the session
        if os.path.exists(ses) and time.time() - os.path.getmtime(ses) > 20:
            proc.terminate()
            break
        time.sleep(5)
    assert os.path.exists(ses), "no SES from Freerouting"
    print(f"routed in {time.time() - t0:.0f} s", flush=True)
    return ses


def import_ses(b, path, via_drill):
    """Add the wires and vias of a Specctra session file (pcbnew's own importer needs the GUI)."""
    routes = _kids(_sexpr(open(path).read()), "routes")[0]
    res = _kids(routes, "resolution")[0]
    unit = {"um": 1e-3, "mm": 1.0, "mil": 0.0254, "inch": 25.4}[res[1]] / int(res[2])
    to = lambda v: pcbnew.FromMM(float(v) * unit)  # noqa: E731
    layers = {b.GetLayerName(l): l for l in range(pcbnew.PCB_LAYER_ID_COUNT) if pcbnew.IsCopperLayer(l)}
    vdia = {ps[1]: c[2] for lib in _kids(routes, "library_out") for ps in _kids(lib, "padstack")
            for sh in _kids(ps, "shape") for c in _kids(sh, "circle")}
    n = 0
    for no in _kids(routes, "network_out"):
        for nt in _kids(no, "net"):
            net = b.FindNet(nt[1])
            for w in _kids(nt, "wire"):
                for pth in _kids(w, "path"):
                    v = [int(x) for x in pth[3:] if not isinstance(x, list)]
                    xy = [(to(v[i]), -to(v[i + 1])) for i in range(0, len(v) - 1, 2)]
                    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
                        t = pcbnew.PCB_TRACK(b)
                        t.SetStart(pcbnew.VECTOR2I(x0, y0))
                        t.SetEnd(pcbnew.VECTOR2I(x1, y1))
                        t.SetWidth(to(pth[2]))
                        t.SetLayer(layers[pth[1]])
                        t.SetNet(net)
                        b.Add(t)
                        n += 1
            for v in _kids(nt, "via"):
                via = pcbnew.PCB_VIA(b)
                via.SetPosition(pcbnew.VECTOR2I(to(v[2]), -to(v[3])))
                via.SetWidth(to(vdia.get(v[1], 6000)))
                via.SetDrill(mm(via_drill))
                via.SetNet(net)
                b.Add(via)
                n += 1
    return n


def gnd_pours(b, clearance=0.3, edge=0.5):
    """GND zones on F.Cu and B.Cu over the whole board outline (inset by `edge`), islands removed."""
    outline = pcbnew.SHAPE_POLY_SET()
    b.GetBoardPolygonOutlines(outline)
    outline.Deflate(mm(edge), pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS, mm(0.05)) if hasattr(pcbnew, "CORNER_STRATEGY_ROUND_ALL_CORNERS") \
        else outline.Deflate(mm(edge), 16)
    gnd = b.FindNet("GND")
    for prio, layer in ((0, pcbnew.F_Cu), (1, pcbnew.B_Cu)):
        z = pcbnew.ZONE(b)
        z.SetLayer(layer)
        z.SetNet(gnd)
        z.SetAssignedPriority(prio) if hasattr(z, "SetAssignedPriority") else z.SetPriority(prio)
        z.SetMinThickness(mm(0.25))
        z.SetLocalClearance(mm(clearance))
        z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL)
        z.SetThermalReliefGap(mm(0.3))
        z.SetThermalReliefSpokeWidth(mm(0.3))
        z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
        p = pcbnew.SHAPE_POLY_SET(outline)
        p.thisown = False
        z.SetOutline(p)
        b.Add(z)


def fill(b):
    pcbnew.ZONE_FILLER(b).Fill(b.Zones())


def stitch(b, via=(0.6, 0.3), pitch=3.0, margin=0.75, keepout_refs=("H",)):
    """GND vias on a grid wherever both the top and the bottom GND pour cover a disc of radius `margin`
    (so the via keeps the pour clearance from every other net on both layers) and not under a mounting hole.
    Ties the two pours (and the SMD ground pads in them) together."""
    zones = {z.GetLayer(): z for z in b.Zones() if not z.GetIsRuleArea() and z.GetNetname() == "GND"}
    top, bot = zones[pcbnew.F_Cu].GetFilledPolysList(pcbnew.F_Cu), zones[pcbnew.B_Cu].GetFilledPolysList(pcbnew.B_Cu)
    holes = [fp.GetPosition() for fp in b.GetFootprints() if fp.GetReference().startswith(keepout_refs)]
    gnd = b.FindNet("GND")
    vias = [t.GetPosition() for t in b.GetTracks() if t.Type() == pcbnew.PCB_VIA_T]
    bb = b.GetBoardEdgesBoundingBox()
    step, m, n = mm(pitch), mm(margin), 0
    y = bb.GetTop() + step // 2
    while y < bb.GetBottom():
        x = bb.GetLeft() + step // 2
        while x < bb.GetRight():
            ring = [pcbnew.VECTOR2I(int(x + m * c), int(y + m * s)) for c, s in
                    ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (0.7, 0.7), (-0.7, 0.7), (0.7, -0.7), (-0.7, -0.7))]
            if (all(top.Contains(q) and bot.Contains(q) for q in ring)
                    and all((x - h.x) ** 2 + (y - h.y) ** 2 > mm(4.0) ** 2 for h in holes)
                    and all((x - v.x) ** 2 + (y - v.y) ** 2 > mm(1.0) ** 2 for v in vias)):
                v = pcbnew.PCB_VIA(b)
                v.SetPosition(pcbnew.VECTOR2I(int(x), int(y)))
                v.SetWidth(mm(via[0]))
                v.SetDrill(mm(via[1]))
                v.SetNet(gnd)
                b.Add(v)
                vias.append(v.GetPosition())
                n += 1
            x += step
        y += step
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("board")
    ap.add_argument("--jar", required=True)
    ap.add_argument("--passes", type=int, default=100)
    ap.add_argument("--out", help="routed board (default: overwrite BOARD)")
    ap.add_argument("--ses", help="use this session file instead of running Freerouting")
    ap.add_argument("--no-pour", action="store_true")
    ap.add_argument("--via-drill", type=float, default=0.3)
    a = ap.parse_args()
    b = pcbnew.LoadBoard(a.board)
    work = tempfile.mkdtemp(prefix="route_")
    ses = a.ses or run_freerouting(b, os.path.abspath(a.jar), a.passes, work)
    if not a.ses:
        keep = os.path.splitext(a.out or a.board)[0] + ".ses"
        shutil.copy(ses, keep)
        print("session kept:", keep)
    b = pcbnew.LoadBoard(a.board)                # fresh board: the DSN export may leave state behind
    print("imported", import_ses(b, ses, a.via_drill), "tracks and vias")
    if not a.no_pour:
        gnd_pours(b)
        fill(b)
        print("stitching vias", stitch(b))
        fill(b)
    out = a.out or a.board
    b.Save(out)
    print("ok", out, len(b.GetTracks()), "tracks/vias,", len(b.Zones()), "zones")


if __name__ == "__main__":
    sys.exit(main())
