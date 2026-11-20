#!/usr/bin/env python3
# License: AGPL-3.0-or-later. Run with KiCad's python: gnd_island_vias.py IN.kicad_pcb OUT.kicad_pcb ...
# Drop a GND via into every outer-layer GND fill island without a via/PTH (inner GND planes must exist).
# Via spot: inside the island (inset by via radius + 0.3 mm) and clear of other-net copper on the opposite outer layer
# and of all pads on both outer layers (no via-in-pad).
import sys,pcbnew
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','hardware','common','gen'))
import routing as R
src,out=sys.argv[1],sys.argv[2]
b=pcbnew.LoadBoard(src); net=b.FindNet(R.gnd_net_name(b)); nc=net.GetNetCode()
VIA=0.6; CL=R.mm(float(__import__("os").environ.get("IV_CL","0.3"))); r=R.mm(VIA/2); M=r+CL; ME=R.mm(0.02)
def fills(layer):
    s=pcbnew.SHAPE_POLY_SET()
    for z in b.Zones():
        if z.GetNetCode()==nc and z.IsOnLayer(layer) and not z.GetIsRuleArea(): s.BooleanAdd(z.GetFilledPolysList(layer))
    return s
def obstacles(L,O):
    s=pcbnew.SHAPE_POLY_SET()
    for t in b.GetTracks():
        if t.GetNetCode()==nc: continue
        if t.Type()==pcbnew.PCB_VIA_T or t.IsOnLayer(O):
            t.TransformShapeToPolygon(s,O,M,ME,pcbnew.ERROR_OUTSIDE)
    for f in b.GetFootprints():
        for p in f.Pads():
            for lay in (L,O):
                if p.IsOnLayer(lay): p.TransformShapeToPolygon(s,lay,M,ME,pcbnew.ERROR_OUTSIDE)
            if p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH or p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH:
                p.TransformHoleToPolygon(s,M,ME,pcbnew.ERROR_OUTSIDE)
    for t in b.GetTracks():   # same-net vias: keep 0.3 mm apart
        if t.Type()==pcbnew.PCB_VIA_T and t.GetNetCode()==nc: t.TransformShapeToPolygon(s,L,M,ME,pcbnew.ERROR_OUTSIDE)
    for z in keepouts():       # keepouts that forbid vias
        if z.GetIsRuleArea() and z.GetDoNotAllowVias():
            k=pcbnew.SHAPE_POLY_SET(z.Outline()); k.Inflate(r,pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,ME); s.BooleanAdd(k)
    s.Simplify(); return s
def keepouts():
    return list(b.Zones())+[z for f in b.GetFootprints() for z in f.Zones()]
total=0
for it in range(3):
    R.fill(b); added=0; skipped=[]
    pts=[v.GetPosition() for v in b.GetTracks() if v.Type()==pcbnew.PCB_VIA_T and v.GetNetCode()==nc]
    pts+=[p.GetPosition() for f in b.GetFootprints() for p in f.Pads() if p.GetNetCode()==nc and p.GetAttribute()==pcbnew.PAD_ATTRIB_PTH]
    for L,O in ((pcbnew.F_Cu,pcbnew.B_Cu),(pcbnew.B_Cu,pcbnew.F_Cu)):
        fl=fills(L); ob=obstacles(L,O)
        for i in range(fl.OutlineCount()):
            isl=fl.UnitSet(i)
            if any(isl.Contains(pcbnew.VECTOR2I(p.x,p.y)) for p in pts): continue
            d=pcbnew.SHAPE_POLY_SET(isl); d.Deflate(r+R.mm(0.05),pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,ME)
            d.BooleanSubtract(ob)
            if d.OutlineCount()==0:
                skipped.append((b.GetLayerName(L),round(isl.Area()/1e12,1))); continue
            ol=d.Outline(0); c=ol.BBox().Centre(); p=c if d.Contains(c) else ol.CPoint(0)
            v=pcbnew.PCB_VIA(b); v.SetPosition(p); v.SetWidth(R.mm(VIA)); v.SetDrill(R.mm(0.3)); v.SetNet(net); b.Add(v)
            pts.append(p); added+=1
            vv=pcbnew.SHAPE_POLY_SET(); v.TransformShapeToPolygon(vv,L,M,ME,pcbnew.ERROR_OUTSIDE); ob.BooleanAdd(vv)
    total+=added; print('pass',it,'vias',added,'skipped',len(skipped),sorted(skipped,key=lambda x:-x[1])[:6])
    if not added: break
rm=0                          # drop any GND via (also from routing.py stitching) inside a no-via keepout
for z in keepouts():
    if z.GetIsRuleArea() and z.GetDoNotAllowVias():
        k=pcbnew.SHAPE_POLY_SET(z.Outline()); k.Inflate(r,pcbnew.CORNER_STRATEGY_ROUND_ALL_CORNERS,ME)
        for v in [t for t in b.GetTracks() if t.Type()==pcbnew.PCB_VIA_T and t.GetNetCode()==nc]:
            if k.Contains(v.GetPosition()): b.Remove(v); rm+=1
R.fill(b); b.Save(out); print('island vias total',total,'keepout vias removed',rm)
