"""Step 1 on a COPY of the Quilter I result: layer names/types and GND zones as in the generator board, parity nets for
unconnected pins, and lists of items to remove (GND stubs at free pads 52-54, In2 tracks under encoders).
usage: fix1.py result.kicad_pcb gen.kicad_pcb drc.json out.kicad_pcb out_lists.json"""
import sys, json, re, math, pcbnew
mm = lambda v: v / 1e6
res, genp, drcp, outp, listp = sys.argv[1:6]
b = pcbnew.LoadBoard(res)
g = pcbnew.LoadBoard(genp)

# 1. layer names and types
for lid in (pcbnew.F_Cu, pcbnew.In1_Cu, pcbnew.In2_Cu, pcbnew.B_Cu):
    b.SetLayerName(lid, g.GetLayerName(lid))
    b.SetLayerType(lid, g.GetLayerType(lid))
print("layers", [(b.GetLayerName(l), b.GetLayerType(l)) for l in (0, 4, 6, 2)])

# 2. GND zones: parameters of In1 as in the generator; B.Cu GND zone re-created from the generator
gz = {z.GetLayer(): z for z in g.Zones() if not z.GetIsRuleArea()}
for z in b.Zones():
    if z.GetIsRuleArea() or z.GetNetname() != "GND":
        continue
    s = gz[z.GetLayer()]
    z.SetLocalClearance(s.GetLocalClearance()); z.SetMinThickness(s.GetMinThickness())
    z.SetPadConnection(s.GetPadConnection()); z.SetThermalReliefGap(s.GetThermalReliefGap())
    z.SetThermalReliefSpokeWidth(s.GetThermalReliefSpokeWidth()); z.SetAssignedPriority(s.GetAssignedPriority())
    z.SetIslandRemovalMode(s.GetIslandRemovalMode()); z.SetZoneName(s.GetZoneName())
    print("In1 zone restored")
have = {z.GetLayer() for z in b.Zones() if not z.GetIsRuleArea() and z.GetNetname() == "GND"}
for lay, s in gz.items():
    if lay in have:
        continue
    z = pcbnew.ZONE(b)
    z.SetLayer(lay); z.SetNet(b.FindNet("GND"))
    poly = pcbnew.SHAPE_POLY_SET(s.Outline()); poly.thisown = 0
    z.SetOutline(poly)
    z.SetLocalClearance(s.GetLocalClearance()); z.SetMinThickness(s.GetMinThickness())
    z.SetPadConnection(s.GetPadConnection()); z.SetThermalReliefGap(s.GetThermalReliefGap())
    z.SetThermalReliefSpokeWidth(s.GetThermalReliefSpokeWidth()); z.SetAssignedPriority(s.GetAssignedPriority())
    z.SetIslandRemovalMode(s.GetIslandRemovalMode())
    b.Add(z)
    print("zone re-created on", b.GetLayerName(lay), "outlines", s.Outline().OutlineCount(), "holes", sum(s.Outline().HoleCount(i) for i in range(s.Outline().OutlineCount())))

# 3. parity: nets of unconnected pins as the schematic names them
drc = json.load(open(drcp))
want = {}
for v in drc["schematic_parity"]:
    m = re.match(r"Pad missing net given by schematic \((.*)\)", v["description"])
    p = re.match(r"Pad (\S+) \[.*?\] of (\S+) on", v["items"][0]["description"])
    if m and p:
        want[(p.group(2), p.group(1))] = m.group(1)
for (ref, num), name in want.items():
    ni = pcbnew.NETINFO_ITEM(b, name); b.Add(ni); ni.thisown = 0
    b.FindFootprintByReference(ref).FindPadByNumber(num).SetNet(ni)
print("parity nets added", len(want))

# 4. lists: GND tracks near free pads 52-54 of U1/U6; In2 tracks crossing the encoder keep-outs
def dseg(px, py, t):
    x1, y1, x2, y2 = mm(t.GetStart().x), mm(t.GetStart().y), mm(t.GetEnd().x), mm(t.GetEnd().y)
    dx, dy = x2 - x1, y2 - y1; L = dx * dx + dy * dy
    u = 0 if L == 0 else max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / L))
    return math.hypot(px - (x1 + u * dx), py - (y1 + u * dy))
gnd_rm = []
for ref in ("U1", "U6"):
    f = b.FindFootprintByReference(ref)
    for num in ("52", "53", "54"):
        p = f.FindPadByNumber(num); pp = p.GetPosition()
        for t in b.GetTracks():
            if t.Type() == pcbnew.PCB_VIA_T or t.GetNetname() != "GND" or not p.IsOnLayer(t.GetLayer()):
                continue
            if dseg(mm(pp.x), mm(pp.y), t) - mm(t.GetWidth()) / 2 < 0.13 + 0.45:
                gnd_rm.append(t.m_Uuid.AsString())
gnd_rm = sorted(set(gnd_rm))
keep = []
for z in g.Zones():
    if z.GetIsRuleArea() and z.GetZoneName().startswith("under_encoder"):
        bb = z.GetBoundingBox(); keep.append((z.GetZoneName(), mm(bb.GetLeft()), mm(bb.GetTop()), mm(bb.GetRight()), mm(bb.GetBottom())))
def inside(t, r):
    _, l, tp, rr, bt = r
    n = max(2, int(mm(t.GetLength()) / 0.05) + 1)
    for i in range(n + 1):
        x = mm(t.GetStart().x) + (mm(t.GetEnd().x) - mm(t.GetStart().x)) * i / n
        y = mm(t.GetStart().y) + (mm(t.GetEnd().y) - mm(t.GetStart().y)) * i / n
        hw = mm(t.GetWidth()) / 2
        if l - hw < x < rr + hw and tp - hw < y < bt + hw:
            return True
    return False
in2 = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T or t.GetLayer() != pcbnew.In2_Cu:
        continue
    for r in keep:
        if inside(t, r):
            in2.append({"uuid": t.m_Uuid.AsString(), "net": t.GetNetname(), "zone": r[0], "len": round(mm(t.GetLength()), 2)})
            break
print("GND tracks at pads 52-54:", len(gnd_rm), "| In2 tracks under encoders:", len(in2))
b.Save(outp)
json.dump({"gnd": gnd_rm, "in2": in2}, open(listp, "w"), indent=1)
