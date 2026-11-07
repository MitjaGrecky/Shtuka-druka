"""split same-net, same-layer tracks where another track's end lands in their middle (T-junction), then refill zones"""
import sys, math, pcbnew
mm=lambda v:v/1e6
b=pcbnew.LoadBoard(sys.argv[1])
tr=[t for t in b.GetTracks() if t.Type()!=pcbnew.PCB_VIA_T]
ends=[(t.GetNetname(),t.GetLayer(),p) for t in tr for p in (t.GetStart(),t.GetEnd())]
n=0
for net,lay,p in ends:
    for t in [x for x in b.GetTracks() if x.Type()!=pcbnew.PCB_VIA_T and x.GetNetname()==net and x.GetLayer()==lay]:
        a,c=t.GetStart(),t.GetEnd()
        if (a.x==p.x and a.y==p.y) or (c.x==p.x and c.y==p.y): continue
        dx,dy=c.x-a.x,c.y-a.y; L=dx*dx+dy*dy
        if L==0: continue
        u=((p.x-a.x)*dx+(p.y-a.y)*dy)/L
        if u<=0.001 or u>=0.999: continue
        qx,qy=a.x+u*dx,a.y+u*dy
        if math.hypot(mm(qx-p.x),mm(qy-p.y))>mm(t.GetWidth())/2: continue
        t2=pcbnew.PCB_TRACK(b); t2.SetStart(pcbnew.VECTOR2I(p.x,p.y)); t2.SetEnd(c); t2.SetWidth(t.GetWidth()); t2.SetLayer(lay); t2.SetNet(t.GetNet()); b.Add(t2)
        t.SetEnd(pcbnew.VECTOR2I(p.x,p.y)); n+=1
        break
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.Save(sys.argv[2]); print("split",n)
