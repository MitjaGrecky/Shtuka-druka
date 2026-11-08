"""GND stub on the driver's layer from pad 12 (GND) along the pad's own axis into the exposed pad (GND) of U1/U6;
removes an earlier 0.2 mm stub that starts at pad 12"""
import sys, math, pcbnew
b=pcbnew.LoadBoard(sys.argv[1])
for ref in ("U1","U6"):
    f=b.FindFootprintByReference(ref); p=f.FindPadByNumber("12"); q=p.GetPosition(); c=f.GetPosition()
    for t in list(b.GetTracks()):
        if t.Type()!=pcbnew.PCB_VIA_T and t.GetNetname()=="GND" and t.GetWidth()==200000 and (t.GetStart()==q):
            b.Remove(t); print(ref,"old stub removed")
    a=math.radians(p.GetOrientationDegrees()); ax=(math.cos(a),-math.sin(a))
    if ax[0]*(c.x-q.x)+ax[1]*(c.y-q.y)<0: ax=(-ax[0],-ax[1])
    e=pcbnew.VECTOR2I(int(q.x+ax[0]*1.0e6),int(q.y+ax[1]*1.0e6))
    t=pcbnew.PCB_TRACK(b); t.SetStart(q); t.SetEnd(e); t.SetWidth(200000); t.SetLayer(f.GetLayer()); t.SetNet(p.GetNet()); b.Add(t)
    print(ref,"stub end inside EP:",any(pp.GetNumber()=="61" and pp.HitTest(e) for pp in f.Pads()))
b.Save(sys.argv[2])
