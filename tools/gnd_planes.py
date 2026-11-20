#!/usr/bin/env python3
# License: AGPL-3.0-or-later. Run with KiCad's python: gnd_planes.py IN.kicad_pcb OUT.kicad_pcb ...
# Pour stage with inner GND planes: routing.py pour_stage + In1/In2 solid GND (4-layer boards routed on F/B only).
import sys,pcbnew
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','hardware','common','gen'))
import routing as R
src,out=sys.argv[1],sys.argv[2]; inner=sys.argv[3].split(',') if len(sys.argv)>3 else ['In1.Cu','In2.Cu']
b=pcbnew.LoadBoard(src); net=R.gnd_net_name(b)
R.gnd_pours(b,net)
outline=pcbnew.SHAPE_POLY_SET(); b.GetBoardPolygonOutlines(outline,False)
outline.Deflate(R.mm(0.5),pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,R.mm(0.05))
g=b.FindNet(net)
for ln in inner:
    z=pcbnew.ZONE(b); z.SetLayer(b.GetLayerID(ln)); z.SetNet(g); z.SetAssignedPriority(2)
    z.SetMinThickness(R.mm(0.25)); z.SetLocalClearance(R.mm(0.3))
    z.SetPadConnection(pcbnew.ZONE_CONNECTION_THERMAL); z.SetThermalReliefGap(R.mm(0.3)); z.SetThermalReliefSpokeWidth(R.mm(0.3))
    z.SetIslandRemovalMode(pcbnew.ISLAND_REMOVAL_MODE_ALWAYS)
    p=pcbnew.SHAPE_POLY_SET(outline); p.thisown=False; z.SetOutline(p); b.Add(z)
R.fill(b); n1=R.stitch(b,net); R.fill(b)
n2=R.stitch_islands(b,net); R.fill(b); n2+=R.connect_islands(b,net)
s,t=R.fix_gnd_pads(b,net); R.fill(b); n2+=R.connect_islands(b,net)
b.Save(out); print(f"planes {inner}: {n1} stitch, {n2} island vias, {s} solid, {t} stubs")
