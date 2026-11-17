"""Main engineer, 17.11.2026: the user chain (deck up, 6.35 jacks under P1, battery under the pads, A1 on the floor, lower slope angle); reuses docs/ru/img/41_wedge_study.py. KiCad python; the model is only read."""
import importlib.util, math, sys
spec=importlib.util.spec_from_file_location("ws","docs/ru/img/41_wedge_study.py"); ws=importlib.util.module_from_spec(spec); spec.loader.exec_module(ws)
def go(deck, ang, fs=0, roof=41, jacks="6.35", shift=30, h5st=8, d_h5=0.0):
    rl,D=453.4+fs,500+fs
    h5y=D-3-15-60-0.5+d_h5
    if deck>=28: e=ws.env(deck,deck,fs,rl-101,6,"130,300,60,160,3",h5y,h5_st=h5st)
    else: e=ws.env(22,31,fs,rl-101,20,f"40,210,{rl-101},{rl-1},3",h5y,h5_st=h5st)
    e.update(FRONT_LIP=0)
    run_len=D-3-roof-(300+fs); back=round((deck if deck>=28 else 31)+run_len*math.tan(math.radians(ang)),1)
    m=ws.load(e,D-3-roof,back,shift)
    rw0=ws.corner_rework2(harness=(391,511,h5y-60-45,h5y-60-25,3.5,26))
    def rw(m,P):
        P=rw0(m,P); S=m.SKIN
        P=[p for p in P if p.name not in ("Phones 1 jack","Phones 2 jack","F1 headphone board","F1 headphone board parts below")]
        for p in list(P):
            if p.name=="P1 Left parts below":
                lo=[c-h for c,h in zip(p.c,p.h)]; hi=[c+h for c,h in zip(p.c,p.h)]
                P.remove(p); P.append(m.box("P1 Left parts below (from y 43)","panel",lo[0],hi[0],43,hi[1],lo[2],hi[2],color="parts",est=True))
        if jacks=="6.35":
            for x in (32,80): P.append(m.box(f"Phones jack 6.35 at x {x}","front",x-7.95,x+7.95,3.0,30.0,S+0.4+1.6,S+0.4+1.6+12.7,color="metal",est=True))
            P.append(m.box("F1 small board","front",12,102,3.0,40,S+0.4,S+0.4+1.6,color="pcb"))
            P.append(m.box("F1 relays 5.4","front",45,70,31,40,S+0.4+1.6,S+0.4+1.6+5.4,color="parts",est=True))
        return P
    col=ws.collisions(m,rw)
    base=[c for c in col if not (('Pocket' in c[1] or 'Pocket' in c[2] or 'W3 System parts' in c[1] or 'W3 System parts' in c[2]) and ('Mini-ITX' in c[1] or 'Mini-ITX' in c[2]))]
    print(f"deck {deck} angle {ang} rear {m.BACK_Z:g} depth {m.D+m.FL:g} (A1 z {'6 floor' if deck>=28 else '20 tray'}): collisions {len(col)} (without the known H5/pocket ones {len(base)})", sorted(base,reverse=True)[:5], flush=True)
for deck in (28,30):
    go(deck,33)
