#!/usr/bin/env python3
"""PNG previews of a board without kicad-cli and without a browser (written under the kicad-cli ban, lifted 19.11.2026): the layers are plotted
to one SVG per side with pcbnew's PLOT_CONTROLLER, then rasterised with PyMuPDF (fitz, ships with KiCad 10 on the PC).

  python tools/render_pcbnew.py BOARD.kicad_pcb OUT_DIR       -> OUT_DIR/preview_top.png, preview_bottom.png

Same file names as tools/pack_for_routing.py; tools/pack_easyeda.py uses render() when playwright is missing.
License: AGPL-3.0-or-later.
"""
import os
import sys
import tempfile

import pcbnew

SIDES = (("top", ("F.Cu", "F.SilkS", "F.Fab", "Edge.Cuts"), False),
         ("bottom", ("B.Cu", "B.SilkS", "B.Fab", "Edge.Cuts"), True))


def _layer(board, name):
    lid = board.GetLayerID(name)
    if lid < 0:                                   # KiCad 8+ canonical names
        lid = board.GetLayerID(name.replace("SilkS", "Silkscreen"))
    return lid


def render(pcb, out, w=None, h=None, width_px=1800):
    import fitz
    board = pcbnew.LoadBoard(pcb)
    tmp = tempfile.mkdtemp()
    done = []
    for side, layers, mirror in SIDES:
        pc = pcbnew.PLOT_CONTROLLER(board)
        po = pc.GetPlotOptions()
        po.SetOutputDirectory(tmp)
        po.SetPlotFrameRef(False)
        po.SetMirror(mirror)
        po.SetUseAuxOrigin(False)
        po.SetAutoScale(False)
        po.SetScale(1)
        if hasattr(po, "SetBlackAndWhite"):
            po.SetBlackAndWhite(False)
        seq = pcbnew.LSEQ()
        for name in layers:
            seq.push_back(_layer(board, name))
        pc.OpenPlotfile(side, pcbnew.PLOT_FORMAT_SVG, side)
        if hasattr(pc, "PlotLayers"):
            pc.PlotLayers(seq)
        else:                                     # older pcbnew: one layer per file, keep the copper only
            pc.SetLayer(seq[0])
            pc.PlotLayer()
        svg = pc.GetPlotFileName()
        pc.ClosePlot()
        # crop to the board: rasterise the whole page, then clip to the board outline's bounding box
        bb = board.GetBoardEdgesBoundingBox()
        doc = fitz.open(svg)
        page = doc[0]
        pw = page.rect.width
        # SVG user units are mm in KiCad plots (viewBox in mm); scale so the board is width_px wide
        bx0, by0, bw, bh = bb.GetX() / 1e6, bb.GetY() / 1e6, bb.GetWidth() / 1e6, bb.GetHeight() / 1e6
        import re
        head = open(svg, encoding="utf-8", errors="ignore").read(2000)
        wmm = float(re.search(r'width="([\d.]+)(?:mm|cm|in)?"', head).group(1))
        unit = re.search(r'width="[\d.]+(mm|cm|in)?"', head).group(1) or "mm"
        wmm *= {"mm": 1.0, "cm": 10.0, "in": 25.4}[unit]
        sx = page.rect.width / wmm                    # page points per board mm
        if mirror:
            bx0 = page.rect.width / sx - bx0 - bw
        clip = fitz.Rect(bx0 * sx - 2, by0 * sx - 2, (bx0 + bw) * sx + 2, (by0 + bh) * sx + 2) & page.rect
        zoom = width_px / max(1.0, clip.width)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
        path = os.path.join(out, f"preview_{side}.png")
        pix.save(path)
        done.append(path)
    return done


if __name__ == "__main__":
    print(render(sys.argv[1], sys.argv[2]))
