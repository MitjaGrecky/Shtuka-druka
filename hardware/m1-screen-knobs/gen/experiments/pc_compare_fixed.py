import sys, pcbnew, collections, math
mm=lambda v: v/1e6
def load(p): return pcbnew.LoadBoard(p)
A=load(sys.argv[1]); B=load(sys.argv[2])   # A=source, B=result
def fps(b): return {f.GetReference():f for f in b.GetFootprints()}
fa,fb=fps(A),fps(B)
print("footprints src %d res %d"%(len(fa),len(fb)))
print("missing in res:",sorted(set(fa)-set(fb)),"added in res:",sorted(set(fb)-set(fa)))
def cls(r):
    for p in ("ENC","D","J","H","U","RN","R","C"):
        if r.startswith(p) and r[len(p):].isdigit(): return p
    return "?"
moved=collections.defaultdict(list); locked=collections.Counter()
for r in sorted(set(fa)&set(fb)):
    a,b=fa[r],fb[r]
    dx=mm(b.GetPosition().x-a.GetPosition().x); dy=mm(b.GetPosition().y-a.GetPosition().y)
    dr=(b.GetOrientationDegrees()-a.GetOrientationDegrees())%360
    ds=a.GetLayer()!=b.GetLayer()
    if abs(dx)>0.001 or abs(dy)>0.001 or min(dr,360-dr)>0.01 or ds:
        moved[cls(r)].append((r,round(dx,3),round(dy,3),round(dr,2),"side!" if ds else ""))
    if a.IsLocked(): locked[("src",cls(r))]+=1
    if b.IsLocked(): locked[("res",cls(r))]+=1
print("locked flags:",dict(locked))
for c in ("ENC","D","J","H"):
    print("MOVED fixed class",c,len(moved[c]),moved[c][:10])
for c in ("U","RN","R","C"):
    m=moved[c]; print("moved movable",c,len(m), "of", sum(1 for r in fa if cls(r)==c))
print("U moves:",moved["U"])
# pad nets of fixed parts
chg=0
for r in sorted(set(fa)&set(fb)):
    for pa in fa[r].Pads():
        pb=[p for p in fb[r].Pads() if p.GetNumber()==pa.GetNumber() and abs(p.GetPosition().x-pa.GetPosition().x)<10 ]
        if pb and pb[0].GetNetname()!=pa.GetNetname(): chg+=1; print("  pad net change",r,pa.GetNumber(),pa.GetNetname(),"->",pb[0].GetNetname())
print("pad net changes",chg)
# mounting holes / NPTH
for nm,b in (("src",A),("res",B)):
    h=[(f.GetReference(),round(mm(f.GetPosition().x),2),round(mm(f.GetPosition().y),2)) for f in b.GetFootprints() if cls(f.GetReference())=="H"]
    print(nm,"holes",len(h),h)
# edge cuts
def edge(b):
    out=[]
    for d in b.GetDrawings():
        if d.GetLayer()==pcbnew.Edge_Cuts: out.append((d.GetClass(),round(mm(d.GetStart().x),2),round(mm(d.GetStart().y),2),round(mm(d.GetEnd().x),2),round(mm(d.GetEnd().y),2)))
    return sorted(out)
ea,eb=edge(A),edge(B); print("edge cuts src %d res %d same=%s"%(len(ea),len(eb),ea==eb))
if ea!=eb: print(" src",ea[:6]," res",eb[:6])
# tracks
def key(t):
    if t.Type()==pcbnew.PCB_VIA_T: return ("via",round(mm(t.GetPosition().x),3),round(mm(t.GetPosition().y),3),t.GetNetname())
    return (t.GetClass(),t.GetLayerName(),)+tuple(sorted([(round(mm(t.GetStart().x),3),round(mm(t.GetStart().y),3)),(round(mm(t.GetEnd().x),3),round(mm(t.GetEnd().y),3))]))
ta=collections.Counter(); tb=collections.Counter()
for t in A.GetTracks(): ta[(key(t),t.GetNetname())]+=1
for t in B.GetTracks(): tb[(key(t),t.GetNetname())]+=1
print("tracks+vias src %d res %d"%(sum(ta.values()),sum(tb.values())))
print("classes src",collections.Counter(t.GetClass() for t in A.GetTracks()),"res",collections.Counter(t.GetClass() for t in B.GetTracks()))
lost=ta-tb; added=tb-ta
print("src items not present identical in res:",sum(lost.values()),"; new in res:",sum(added.values()))
# ring items: nets named *_CS*/A_SW etc. in src that were pre-routed in src (those that exist in src at all)
byn=collections.Counter(k[1] for k in lost.elements()); print("lost by net (top):",byn.most_common(12))
# which src items were pre-routed (all src tracks)
print("src pre-routed nets count", len(set(t.GetNetname() for t in A.GetTracks())))
