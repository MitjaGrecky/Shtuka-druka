import sys, pcbnew
inp, outp, dsn, side = sys.argv[1:5]
b = pcbnew.LoadBoard(inp)
print("tracks", len(list(b.GetTracks())))
if side == "top":
    d = getattr(pcbnew, "FLIP_DIRECTION_LEFT_RIGHT", None)
    if d is None: d = pcbnew.FLIP_DIRECTION.LEFT_RIGHT
    for ref in ("U1", "U6"):
        f = b.FindFootprintByReference(ref)
        if f.GetLayer() == pcbnew.B_Cu: f.Flip(f.GetPosition(), d)
        print(ref, f.GetLayerName())
b.Save(outp)
print("export", pcbnew.ExportSpecctraDSN(b, dsn))
