import sys,pcbnew
for b in sys.argv[1:]:
    pcb=pcbnew.LoadBoard(f"{b}/{b}.kicad_pcb"); e=pcb.GetBoardEdgesBoundingBox()
    print("==",b,"edges x",e.GetX()/1e6,(e.GetX()+e.GetWidth())/1e6,"y",e.GetY()/1e6,(e.GetY()+e.GetHeight())/1e6)
    for f in pcb.GetFootprints():
        r=f.GetReference()
        if not r.startswith("J"): continue
        pads=[p.GetPosition() for p in f.Pads()]
        cx=sum(p.x for p in pads)/len(pads)/1e6; cy=sum(p.y for p in pads)/len(pads)/1e6
        c=f.GetCourtyard(pcbnew.B_CrtYd if f.GetLayer()==pcbnew.B_Cu else pcbnew.F_CrtYd).BBox()
        print(f"{r} {f.GetFPID().GetLibItemName()} rot {f.GetOrientationDegrees()} pads({cx:.1f},{cy:.1f}) court x {c.GetX()/1e6:.1f}..{(c.GetX()+c.GetWidth())/1e6:.1f} y {c.GetY()/1e6:.1f}..{(c.GetY()+c.GetHeight())/1e6:.1f}")
