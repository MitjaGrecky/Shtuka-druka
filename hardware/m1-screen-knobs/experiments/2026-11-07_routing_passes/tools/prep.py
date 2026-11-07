"""prep.py in.kicad_pcb out.kicad_pcb out.dsn side angle refs   (tracks are stripped beforehand as text)"""
import sys, math, pcbnew
mm=lambda v:v/1e6
inp,outp,dsn,side,angle,refs=sys.argv[1:7]; angle=float(angle)
b=pcbnew.LoadBoard(inp)
d=getattr(pcbnew,"FLIP_DIRECTION_LEFT_RIGHT",None)
if d is None: d=pcbnew.FLIP_DIRECTION.LEFT_RIGHT
for ref in refs.split(","):
    f=b.FindFootprintByReference(ref)
    if side=="top" and f.GetLayer()==pcbnew.B_Cu: f.Flip(f.GetPosition(),d)
    f.SetOrientationDegrees(angle)
    c=f.GetPosition(); lay=f.GetLayer()
    if angle%90:
        for g in b.GetFootprints():
            r=g.GetReference()
            if r.startswith(("U","ENC","D","J","H")) or g.GetLayer()!=lay: continue
            p=g.GetPosition(); dx,dy=mm(p.x-c.x),mm(p.y-c.y); dist=math.hypot(dx,dy)
            if dist<6.4 and dist>0:
                k=(dist+1.8)/dist
                g.SetPosition(pcbnew.VECTOR2I(int(c.x+dx*k*1e6),int(c.y+dy*k*1e6)))
                print("pushed",r)
    print(ref,f.GetLayerName(),f.GetOrientationDegrees())
b.Save(outp)
print("export",pcbnew.ExportSpecctraDSN(b,dsn))
