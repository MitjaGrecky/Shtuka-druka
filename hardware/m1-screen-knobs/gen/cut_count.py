"""Congestion check for M1: signal nets crossing each gap between encoders, LED distance to U1,
decoupling distance. Usage: python3 cut_count.py [board.kicad_pcb]"""
import re,math,collections,sys
t=open(sys.argv[1] if len(sys.argv)>1 else "m1-screen-knobs.kicad_pcb").read()
parts=re.split(r'\n  \(footprint ',t)[1:]
fps=[]
for p in parts:
    m=re.search(r'\n    \(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)',p)
    ref=re.search(r'\(fp_text reference "([^"]+)"',p)
    if not m or not ref: continue
    x,y=float(m.group(1)),float(m.group(2)); rot=float(m.group(3) or 0)
    a=math.radians(-rot)
    pads=[]
    for pm in re.finditer(r'\(pad "([^"]*)" [^\n]*?\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)[^\n]*?(?:\n[^\n]*?)*?\(net (\d+) "([^"]*)"\)',p):
        px,py=float(pm.group(2)),float(pm.group(3))
        pads.append((pm.group(1),x+px*math.cos(a)-py*math.sin(a),y+px*math.sin(a)+py*math.cos(a),pm.group(6)))
    fps.append((ref.group(1),x,y,pads))
print(len(fps),'footprints')
d={r:(x,y) for r,x,y,_ in fps}
for r in ['U1','U2','U3','U4','U5','J1','ENC1','ENC8','H1','H2','H3','H4','D1','D104']: print(r,d.get(r))
nets=collections.defaultdict(list)
for r,x,y,pads in fps:
    for n,gx,gy,net in pads:
        if net: nets[net].append((r,gx,gy))
print(len(nets),'nets')
enc=sorted(x for r,x,y,_ in fps if r.startswith('ENC'))
print('enc x',[round(e,1) for e in enc])
sig=lambda n: n not in('GND','+5V','+3V3')
for i in range(len(enc)-1):
    cx=(enc[i]+enc[i+1])/2
    c=[n for n,v in nets.items() if sig(n) and min(p[1] for p in v)<cx<max(p[1] for p in v)]
    print(f'cut x={cx:.1f}: {len(c)} signal nets cross')
# distances of LED pads to U1
u1=d['U1']
dist=[math.hypot(x-u1[0],y-u1[1]) for r,x,y,_ in fps if r.startswith('D')]
print('LED dist to U1 mm: min %.0f max %.0f mean %.0f'%(min(dist),max(dist),sum(dist)/len(dist)))
# bypass caps distance to nearest U pin they share a net with
for r,x,y,pads in fps:
    if r.startswith('C'):
        best=None
        for n,gx,gy,net in pads:
            if net in('GND',): continue
            for rr,px,py in nets[net]:
                if rr.startswith('U') :
                    dd=math.hypot(gx-px,gy-py); best=min(best,dd) if best else dd
        print(r,round(x,1),round(y,1),'to U pin %.1f'%best if best else '-')
