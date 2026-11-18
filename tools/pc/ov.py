import sys,pcbnew
for b in sys.argv[1:]:
    pcb=pcbnew.LoadBoard(f"{b}/{b}.kicad_pcb"); fs=list(pcb.GetFootprints())
    def box(f):
        lay=pcbnew.B_CrtYd if f.GetLayer()==pcbnew.B_Cu else pcbnew.F_CrtYd
        return f.GetCourtyard(lay).BBox()
    n=0
    for i,a in enumerate(fs):
        for c in fs[i+1:]:
            if a.GetLayer()!=c.GetLayer(): continue
            A,C=box(a),box(c)
            if A.GetWidth() and C.GetWidth() and A.Intersects(C): print(b,"overlap",a.GetReference(),c.GetReference()); n+=1
    print(b,"overlaps",n)
