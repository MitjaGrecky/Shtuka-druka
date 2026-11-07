import sys, pcbnew
d=sys.argv[1]
b=pcbnew.LoadBoard(d+"/m1-screen-knobs.kicad_pcb")
print("import",pcbnew.ImportSpecctraSES(b,d+"/out.ses"))
pcbnew.ZONE_FILLER(b).Fill(b.Zones())
b.Save(d+"/routed.kicad_pcb")
