"""T-junctions: where a track end lies inside another same-net, same-layer track (not at its ends), move that end onto the
other track's centre line and split the other track there (no shift of the existing track). Then refill zones.
usage: tjunc.py in.kicad_pcb out.kicad_pcb [reference.kicad_pcb: its tracks are never moved]"""
import sys, math, pcbnew
mm = lambda v: v / 1e6
b = pcbnew.LoadBoard(sys.argv[1])
keep = set()
if len(sys.argv) > 3:
    import re
    keep = set(re.findall(r'\(uuid "([0-9a-f-]+)"\)', open(sys.argv[3], encoding="utf8").read()))
    print("tracks kept fixed:", len(keep))
n = 0
for _ in range(3):
    changed = False
    tracks = [t for t in b.GetTracks() if t.Type() != pcbnew.PCB_VIA_T]
    bykey = {}
    for t in tracks:
        bykey.setdefault((t.GetNetCode(), t.GetLayer()), []).append(t)
    for a in tracks:
        if a.m_Uuid.AsString() in keep:
            continue
        for end in (0, 1):
            p = a.GetStart() if end == 0 else a.GetEnd()
            for t in bykey[(a.GetNetCode(), a.GetLayer())]:
                if t is a:
                    continue
                s, e = t.GetStart(), t.GetEnd()
                if (s.x == p.x and s.y == p.y) or (e.x == p.x and e.y == p.y):
                    break
                dx, dy = e.x - s.x, e.y - s.y
                L = dx * dx + dy * dy
                if L == 0:
                    continue
                u = ((p.x - s.x) * dx + (p.y - s.y) * dy) / L
                if u <= 0.001 or u >= 0.999:
                    continue
                q = pcbnew.VECTOR2I(int(round(s.x + u * dx)), int(round(s.y + u * dy)))
                if math.hypot(mm(q.x - p.x), mm(q.y - p.y)) > mm(t.GetWidth()) / 2:
                    continue
                if end == 0:
                    a.SetStart(q)
                else:
                    a.SetEnd(q)
                t2 = pcbnew.PCB_TRACK(b)
                t2.SetStart(q); t2.SetEnd(e); t2.SetWidth(t.GetWidth()); t2.SetLayer(t.GetLayer()); t2.SetNet(t.GetNet())
                b.Add(t2)
                t.SetEnd(q)
                bykey[(a.GetNetCode(), a.GetLayer())].append(t2)
                n += 1; changed = True
                break
    if not changed:
        break
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.Save(sys.argv[2])
print("split", n)
