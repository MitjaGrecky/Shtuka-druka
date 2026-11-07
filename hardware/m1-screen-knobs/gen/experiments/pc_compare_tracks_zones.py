import sys, pcbnew, collections, math
mm=lambda v: v/1e6
A=pcbnew.LoadBoard(sys.argv[1]); B=pcbnew.LoadBoard(sys.argv[2])
def dist_pt_seg(px,py,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1; L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,((px-x1)*dx+(py-y1)*dy)/L))
    return math.hypot(px-(x1+t*dx),py-(y1+t*dy))
idx=collections.defaultdict(list)
for t in B.GetTracks():
    if t.Type()==pcbnew.PCB_VIA_T: continue
    idx[(t.GetLayer(),t.GetNetname())].append((mm(t.GetStart().x),mm(t.GetStart().y),mm(t.GetEnd().x),mm(t.GetEnd().y),mm(t.GetWidth())))
miss=collections.Counter(); tot=collections.Counter(); changed_w=0; missing_items=[]
for t in A.GetTracks():
    if t.Type()==pcbnew.PCB_VIA_T: continue
    k=(t.GetLayer(),t.GetNetname()); sx,sy,ex,ey=mm(t.GetStart().x),mm(t.GetStart().y),mm(t.GetEnd().x),mm(t.GetEnd().y)
    L=math.hypot(ex-sx,ey-sy); n=max(2,int(L/0.05)+1); ok=True
    for i in range(n):
        px,py=sx+(ex-sx)*i/(n-1),sy+(ey-sy)*i/(n-1)
        if not any(dist_pt_seg(px,py,*s[:4])<=0.02 for s in idx[k]): ok=False;break
    tot[t.GetNetname()[:6]]+=1
    if not ok: miss[t.GetNetname()]+=1; missing_items.append((t.GetNetname(),t.GetLayer(),round(sx,2),round(sy,2),round(ex,2),round(ey,2)))
print("src tracks",sum(tot.values()),"not covered by res copper (same net+layer):",sum(miss.values()))
print(miss.most_common(20)); print(missing_items[:10])
# widths of src tracks vs res covering
wsrc=collections.Counter(round(mm(t.GetWidth()),3) for t in A.GetTracks() if t.Type()!=pcbnew.PCB_VIA_T)
wres=collections.Counter(round(mm(t.GetWidth()),3) for t in B.GetTracks() if t.Type()!=pcbnew.PCB_VIA_T)
print("widths src",dict(wsrc),"res",dict(wres))
# vias: src vias identical?
va={(round(mm(v.GetPosition().x),3),round(mm(v.GetPosition().y),3),v.GetNetname()) for v in A.GetTracks() if v.Type()==pcbnew.PCB_VIA_T}
vb={(round(mm(v.GetPosition().x),3),round(mm(v.GetPosition().y),3),v.GetNetname()) for v in B.GetTracks() if v.Type()==pcbnew.PCB_VIA_T}
print("src vias %d, present in res %d, new vias %d"%(len(va),len(va&vb),len(vb-va)))
vd=[(v.GetDrillValue()/1e6,mm(v.GetWidth(pcbnew.F_Cu))) for v in B.GetTracks() if v.Type()==pcbnew.PCB_VIA_T]
print("res via (drill,dia) counts",collections.Counter((round(a,2),round(b,2)) for a,b in vd))
# zones
for nm,b in (("SRC",A),("RES",B)):
    print(nm,"zones:")
    for z in b.Zones():
        bb=z.GetBoundingBox(); ls=[b.GetLayerName(l) for l in z.GetLayerSet().Seq()]
        print("  %-18s net=%-5s rule=%s layers=%s prio=%d filled=%s bbox=(%.1f,%.1f)-(%.1f,%.1f) pads=%s clr=%.2f minw=%.2f island=%d"%(z.GetZoneName() or "-", z.GetNetname() or "-", z.GetIsRuleArea(), ls, z.GetAssignedPriority(), z.IsFilled(), mm(bb.GetLeft()),mm(bb.GetTop()),mm(bb.GetRight()),mm(bb.GetBottom()), z.GetPadConnection(), mm(z.GetLocalClearance()), mm(z.GetMinThickness()), z.GetIslandRemovalMode()) if not z.GetIsRuleArea() else "  rule %-14s tracks_off=%s vias_off=%s pour_off=%s fp_off=%s layers=%s bbox=(%.1f,%.1f)-(%.1f,%.1f)"%(z.GetZoneName(),z.GetDoNotAllowTracks(),z.GetDoNotAllowVias(),z.GetDoNotAllowZoneFills(),z.GetDoNotAllowFootprints(),ls,mm(bb.GetLeft()),mm(bb.GetTop()),mm(bb.GetRight()),mm(bb.GetBottom())))
