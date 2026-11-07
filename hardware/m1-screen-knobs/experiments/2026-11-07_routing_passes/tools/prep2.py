"""prep2.py in out dsn angle : drivers U1,U6 on top at ANGLE, their nearby small parts flipped to top too (same x,y)"""
import sys, math, pcbnew
mm=lambda v:v/1e6
inp,outp,dsn,angle=sys.argv[1:5]; angle=float(angle)
b=pcbnew.LoadBoard(inp)
d=getattr(pcbnew,"FLIP_DIRECTION_LEFT_RIGHT",None)
if d is None: d=pcbnew.FLIP_DIRECTION.LEFT_RIGHT
for ref in sys.argv[5].split(","):
    f=b.FindFootprintByReference(ref); c=f.GetPosition()
    moved=[]
    for g in list(b.GetFootprints()):
        r=g.GetReference()
        if r.startswith(("U","ENC","D","J","H")) or g.GetLayer()!=pcbnew.B_Cu: continue
        p=g.GetPosition(); dist=math.hypot(mm(p.x-c.x),mm(p.y-c.y))
        if dist<9.0:
            g.Flip(g.GetPosition(),d); moved.append(r)
    if f.GetLayer()==pcbnew.B_Cu: f.Flip(f.GetPosition(),d)
    f.SetOrientationDegrees(angle)
    print(ref,f.GetLayerName(),"parts flipped to top:",moved)
b.Save(outp)
print("export",pcbnew.ExportSpecctraDSN(b,dsn))
