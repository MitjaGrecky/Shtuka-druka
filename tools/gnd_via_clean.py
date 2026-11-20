#!/usr/bin/env python3
# License: AGPL-3.0-or-later. Run with KiCad's python: gnd_via_clean.py IN.kicad_pcb OUT.kicad_pcb
# Remove GND vias that hit other-net copper on ANY layer (routing.py stitching checks only F/B; on a 4-layer board with
# In2 as a signal layer its vias short In2 tracks). Run before gnd_island_vias.py. Env IV_CL = clearance (default 0.2 mm).
import os,sys,pcbnew
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','hardware','common','gen'))
import routing as R
src,out=sys.argv[1],sys.argv[2]
b=pcbnew.LoadBoard(src); nc=b.FindNet(R.gnd_net_name(b)).GetNetCode()
CL=R.mm(float(os.environ.get("IV_CL","0.2"))); ME=R.mm(0.02)
OTH=[t for t in b.GetTracks() if t.GetNetCode()!=nc]
def clash(v):
    """GND via hitting other-net copper on any layer (routing.py stitching knows only F/B)."""
    p=v.GetPosition(); rr=v.GetWidth(pcbnew.F_Cu)//2+CL
    vp=None
    for t in OTH:
        bb=t.GetBoundingBox()
        if p.x+rr<bb.GetLeft() or p.x-rr>bb.GetRight() or p.y+rr<bb.GetTop() or p.y-rr>bb.GetBottom(): continue
        if vp is None:
            vp=pcbnew.SHAPE_POLY_SET(); v.TransformShapeToPolygon(vp,pcbnew.F_Cu,CL,ME,pcbnew.ERROR_OUTSIDE)
        q=pcbnew.SHAPE_POLY_SET(); t.TransformShapeToPolygon(q,pcbnew.F_Cu if t.Type()==pcbnew.PCB_VIA_T else t.GetLayer(),0,ME,pcbnew.ERROR_OUTSIDE)
        q.BooleanIntersection(vp)
        if q.OutlineCount(): return True
    return False
vias=[t for t in b.GetTracks() if t.Type()==pcbnew.PCB_VIA_T and t.GetNetCode()==nc]
bad=[v for v in vias if clash(v)]
for v in bad: b.Remove(v)
R.fill(b); b.Save(out); print('clashing GND vias removed',len(bad))
