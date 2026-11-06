import pcbnew, math, sys
b = pcbnew.LoadBoard('m1-screen-knobs.kicad_pcb')
mm = pcbnew.FromMM; tm = pcbnew.ToMM
leds = [b.FindFootprintByReference(f'D{i}') for i in range(1, 14)]
# ring centre: average of LED positions is biased (270 deg arc) -> use encoder ENC1
cx, cy = 54.0, 60.0   # ring 1 centre (circle fit through D1-D13, R = 12.000)
def polar(p): x, y = tm(p.x) - cx, tm(p.y) - cy; return math.hypot(x, y), math.atan2(y, x)
def pt(r, a): return pcbnew.VECTOR2I(mm(cx + r * math.cos(a)), mm(cy + r * math.sin(a)))
ringnets = set()
for fp in leds:
    for p in fp.Pads(): ringnets.add(p.GetNetCode())
# remove old copper of these nets inside the ring area
rm = []
def segdist(t):
    ax, ay = tm(t.GetStart().x) - cx, tm(t.GetStart().y) - cy; bx, by = tm(t.GetEnd().x) - cx, tm(t.GetEnd().y) - cy
    dx, dy = bx - ax, by - ay; L = dx * dx + dy * dy
    u = 0 if L == 0 else max(0, min(1, -(ax * dx + ay * dy) / L))
    return math.hypot(ax + u * dx, ay + u * dy)
for t in b.GetTracks():
    if segdist(t) < 15.0: rm.append(t)          # clean slate around ring 1, every net
for t in rm: b.Remove(t)
print('removed', len(rm))
W = mm(0.12); VD, VH = mm(0.45), mm(0.2)
def track(p1, p2, layer, net):
    t = pcbnew.PCB_TRACK(b); t.SetStart(p1); t.SetEnd(p2); t.SetWidth(W); t.SetLayer(layer); t.SetNetCode(net); b.Add(t)
def arc(r, a1, a2, layer, net):
    dd = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    t = pcbnew.PCB_ARC(b); t.SetStart(pt(r, a1)); t.SetMid(pt(r, a1 + dd / 2)); t.SetEnd(pt(r, a1 + dd))
    t.SetWidth(W); t.SetLayer(layer); t.SetNetCode(net); b.Add(t)
def via(p, net):
    v = pcbnew.PCB_VIA(b); v.SetPosition(p); v.SetWidth(VD); v.SetDrill(VH); v.SetNetCode(net); b.Add(v); return v
RG, RB, RR = 13.10, 10.90, None
info = []   # per LED: angle, pads by number -> (r, a, pos, net)
for fp in leds:
    d = {p.GetNumber(): (*polar(p.GetPosition()), p.GetPosition(), p.GetNetCode()) for p in fp.Pads()}
    info.append((polar(fp.GetPosition())[1], d))
vias = 0
for k, (ac, d) in enumerate(info):
    for num, (r, a, pos, net) in d.items():
        if num == '3':            # G outer row -> radial stub out to arc RG
            track(pos, pt(RG, a), pcbnew.F_Cu, net)
        elif num == '4':          # B inner row -> stub in to arc RB
            track(pos, pt(RB, a), pcbnew.F_Cu, net)
        elif num in ('1', '2'):   # R (outer) and A (inner): via beside the pad, away from the LED centre
            side = math.copysign(1, (a - ac + math.pi) % (2 * math.pi) - math.pi)
            av = a + side * 1.30 / r
            vp = pt(r, av); track(pos, vp, pcbnew.F_Cu, net); via(vp, net); vias += 1
            d[num] = (r, a, pos, net, av)
# arcs between consecutive LEDs sharing a net (G, B on F.Cu; R on In2 between its vias)
for k in range(len(info) - 1):
    d1, d2 = info[k][1], info[k + 1][1]
    for num, rr, layer in (('3', RG, pcbnew.F_Cu), ('4', RB, pcbnew.F_Cu), ('1', None, pcbnew.In2_Cu)):
        if d1[num][3] != d2[num][3]: continue
        if num == '1':
            r = (d1['1'][0] + d2['1'][0]) / 2
            arc(r, d1['1'][4], d2['1'][4], layer, d1['1'][3])
        else:
            arc(rr, d1[num][1], d2[num][1], layer, d1[num][3])
print('vias in ring 1:', vias, 'per LED', vias / 13)
b.Save('ring_test.kicad_pcb')
open('centre.txt', 'w').write(f'{cx} {cy}')
