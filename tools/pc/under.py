import sys,pcbnew,collections
for b in sys.argv[1:]:
    pcb=pcbnew.LoadBoard(f"{b}/{b}.kicad_pcb")
    bb=pcb.GetBoardEdgesBoundingBox()
    print("==",b,round(bb.GetWidth()/1e6,1),"x",round(bb.GetHeight()/1e6,1))
    c=collections.Counter()
    for f in pcb.GetFootprints():
        side="B" if f.GetLayer()==pcbnew.B_Cu else "T"
        th=f.GetAttributes()&pcbnew.FP_THROUGH_HOLE
        name=str(f.GetFPID().GetLibItemName())
        c[(side,"TH" if th else "SMD",name)]+=1
    for k,v in sorted(c.items()): print(v,*k)
