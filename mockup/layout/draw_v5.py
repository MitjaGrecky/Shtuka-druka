#!/usr/bin/env python3
"""Draw panel layout v5 (top view, to scale) from layout_v5.json -> SVG. AGPL-3.0-or-later."""
import json, math, html

E = json.load(open("layout_v5.json"))
W, D, F0, F1 = 515, 500, 340, 470
S = 2.0                      # px per mm
MX, MY = 70, 70              # margins (px)
PW, PH = int(MX * 2 + W * S), int(MY + D * S + 110)
X = lambda x: MX + x * S
Y = lambda y: MY + (D - y) * S
FONT = "DejaVu Sans, Arial, sans-serif"
COL = {"grey": "#3b4045", "red": "#c9473d", "green": "#3f9f5a", "white": "#d9dddb", "teal": "#2d8c73",
       "purple": "#6b63c9", "amber": "#b5852c", "blue": "#3d86c6", "coral": "#c0613f", "alu": "#b9bec2"}
o = []
a = o.append


def t(x, y, s, size=3.0, color="#e8ecea", anchor="middle", weight=400):
    a(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size*S:.1f}" fill="{color}" '
      f'text-anchor="{anchor}" dominant-baseline="central" font-weight="{weight}">{html.escape(s)}</text>')


def frame(x0, y0, x1, y1, title, color="#8a918d"):
    a(f'<rect x="{X(x0):.1f}" y="{Y(y1):.1f}" width="{(x1-x0)*S:.1f}" height="{(y1-y0)*S:.1f}" rx="{2.5*S}" '
      f'fill="none" stroke="{color}" stroke-width="0.9" opacity="0.7"/>')
    if title:
        tw = len(title) * 2.0 + 3
        a(f'<rect x="{X(x0+2.5):.1f}" y="{Y(y1)-3.4*S/2-1:.1f}" width="{tw*S:.1f}" height="{3.4*S+2:.1f}" fill="{BG}"/>')
        t(X(x0 + 4), Y(y1), title, 2.8, color, "start", 500)


a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{PW}" height="{PH}" viewBox="0 0 {PW} {PH}">')
a(f'<rect width="{PW}" height="{PH}" fill="#f4f3ef"/>')
# body
a(f'<rect x="{X(0)}" y="{Y(D)}" width="{W*S}" height="{D*S}" rx="{8*S}" fill="#1a1d20"/>')
a(f'<rect x="{X(0)}" y="{Y(F0)}" width="{W*S}" height="{F0*S}" rx="{8*S}" fill="#1d2023"/>')
a(f'<rect x="{X(0)}" y="{Y(F1)}" width="{W*S}" height="{(F1-F0)*S}" fill="#24282c"/>')
for yy in (F0, F1):
    a(f'<line x1="{X(0)}" y1="{Y(yy)}" x2="{X(W)}" y2="{Y(yy)}" stroke="#555b60" stroke-width="1" stroke-dasharray="6 5"/>')
BG = "#1d2023"

# group frames (deck)
BG = "#1d2023"
frame(8, 10, 108, 70, "TRANSPORT")
frame(8, 84, 108, 116, "CAPTURE")
frame(8, 132, 108, 210, "EDIT")
frame(8, 219, 108, 247, "")
frame(8, 268, 108, 318, "TEMPO")
frame(92, 250, 366, 267, "SCENES")
frame(318, 18, 390, 248, "")
for hx, ht in ((330, "MUTE"), (352, "SELECT"), (378, "LEVEL")): t(X(hx), Y(244), ht, 2.1, "#8a918d", weight=500)
frame(395, 12, 505, 34, "")
frame(395, 48, 505, 98, "PAD MODE")
frame(397, 230, 454, 324, "SCREEN")
frame(395, 132, 505, 190, "SCREEN NAV")
frame(455, 230, 505, 324, "LIVE")
BG = "#24282c"
frame(8, 348, 132, 462, "LEVELS")
frame(380, 356, 507, 456, "SYSTEM")

for e in E:
    k, x, y, w, h = e["kind"], e["x"], e["y"], e["w"], e["h"]
    if k == "strip":
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{3*S}" fill="#0d0f11" stroke="#3a3f44" stroke-width="1.2"/>')
        for i in range(25):
            lx = x - w / 2 + 6 + i * (w - 12) / 24
            a(f'<circle cx="{X(lx):.1f}" cy="{Y(y+h/2+3.2):.1f}" r="{0.8*S:.1f}" fill="#9b93f0" fill-opacity="{0.9 if 6 <= i <= 11 else 0.18}"/>')
        t(X(x), Y(y + 1), "TOUCH STRIP", 2.6, "#4d5358", weight=500)
    elif k == "zone":
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{3*S}" '
          f'fill="#202326" stroke="#2c3034" stroke-dasharray="3 4"/>')
        t(X(x), Y(y), "PALM REST", 3, "#4d5358")
    elif k == "pad":
        lit = (hash(e["name"]) % 5) > 1
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{2*S}" '
          f'fill="{e["color"]}" fill-opacity="{0.75 if lit else 0.16}" stroke="#0e1012" stroke-width="1"/>')
    elif k == "button":
        c = e["color"]
        fill = COL.get(c, c)
        txt = "#16191b" if c in ("white", "amber", "alu") or c.startswith("#e7") or c.startswith("#f0") or c.startswith("#55") or c.startswith("#3f") else "#f2f5f3"
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{1.8*S}" '
          f'fill="{fill}" stroke="#0e1012" stroke-width="1"/>')
        lab = e["label"]
        size = min(3.3, (w - 2.5) / max(len(lab), 1) * 1.65, h * 0.42)
        if w >= 26 and h >= 20: size = min(4.2, (w - 3) / max(len(lab), 1) * 1.7)
        t(X(x), Y(y), lab, size, txt, weight=500 if h >= 20 else 400)
    elif k in ("encoder", "pot"):
        r = w / 2
        cx, cy = X(x), Y(y)
        if k == "encoder":
            # endless: no mark on the cap, value only on the LED ring (15 dots over 270 deg)
            ring = e.get("ring", w + 7) / 2
            rc = COL.get(e["color"], e["color"])
            n_on = 4 + (hash(e["name"]) % 9)
            for i in range(15):
                ang = math.radians(225 - 270 * i / 14)
                px, py = cx + ring * S * math.cos(ang), cy - ring * S * math.sin(ang)
                a(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{0.9*S:.1f}" fill="{rc}" fill-opacity="{0.95 if i < n_on else 0.18}"/>')
            if "утоплен" in e.get("note", ""):
                a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{(r+1.8)*S:.1f}" fill="#0b0c0d"/>')
            a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*S:.1f}" fill="#141618" stroke="#4a5055" stroke-width="1.2"/>')
            a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{(r-2)*S:.1f}" fill="none" stroke="#24282c" stroke-width="1.5"/>')
            off = ring + 2.6
        else:
            # finite pot with end stops: printed scale + mark on the cap
            for i in range(11):
                ang = math.radians(225 - 27 * i)
                r0, r1 = (r + 2.2) * S, (r + (3.6 if i in (0, 10) else 3.0)) * S
                a(f'<line x1="{cx + r0*math.cos(ang):.1f}" y1="{cy - r0*math.sin(ang):.1f}" x2="{cx + r1*math.cos(ang):.1f}" '
                  f'y2="{cy - r1*math.sin(ang):.1f}" stroke="#d9dddb" stroke-width="{1.4 if i in (0, 10) else 0.9}"/>')
            a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r*S:.1f}" fill="#c3c8cb" stroke="#7d8387" stroke-width="1.2"/>')
            ang = math.radians(225 - 270 * (0.35 + (hash(e["name"]) % 5) * 0.1))
            a(f'<line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + r*0.85*S*math.cos(ang):.1f}" y2="{cy - r*0.85*S*math.sin(ang):.1f}" '
              f'stroke="#111" stroke-width="{1.0*S}" stroke-linecap="round"/>')
            off = r + 4.2
        if e["label"]:
            t(X(x), Y(y - off), e["label"], 2.4, "#c9cfcc")
    elif k == "wheel":
        # endless: no dimple or mark - grip ring only
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{w/2*S:.1f}" fill="#30353a" stroke="#6c7276" stroke-width="2"/>')
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{(w/2-2.5)*S:.1f}" fill="none" stroke="#454b50" stroke-width="{1.2*S}" stroke-dasharray="2 3"/>')
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{(w/2-6)*S:.1f}" fill="#1f2326"/>')
        t(X(x), Y(y - w / 2 - 3), "PUSH = OK", 2.4, "#c9cfcc")
    elif k == "fader":
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+1):.1f}" width="{w*S:.1f}" height="{2*S}" rx="2" fill="#050607"/>')
        a(f'<rect x="{X(x-5):.1f}" y="{Y(y+8):.1f}" width="{10*S}" height="{16*S}" rx="3" fill="#2b2f33" stroke="#555b60"/>')
        a(f'<line x1="{X(x)}" y1="{Y(y+8)}" x2="{X(x)}" y2="{Y(y-8)}" stroke="#e8ecea" stroke-width="2"/>')
        t(X(x), Y(y - 11), e["label"], 2.6, "#c9cfcc")
    elif k == "meter":
        n = 14
        for i in range(n):
            yy = y - h / 2 + 4 + i * (h - 8) / n
            col = "#55c26b" if i < 9 else ("#e7d24a" if i < 12 else "#e8564a")
            a(f'<rect x="{X(x-w/2):.1f}" y="{Y(yy+3):.1f}" width="{w*S:.1f}" height="{5*S:.1f}" rx="1" fill="{col}" fill-opacity="{0.85 if i < 7 else 0.18}"/>')
        t(X(x), Y(y - h / 2 - 1), e["label"], 2.4, "#c9cfcc")
    elif k == "led":
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{w/2*S:.1f}" fill="{COL.get(e["color"], e["color"])}" opacity="0.6"/>')
    elif k == "pocket":
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{3*S}" fill="#0b0c0d"/>')
        a(f'<rect x="{X(x-28):.1f}" y="{Y(y+3):.1f}" width="{13*S}" height="{6*S}" fill="#2b6cb0"/>')
        a(f'<rect x="{X(x+2):.1f}" y="{Y(y+1.5):.1f}" width="{26*S}" height="{3*S}" fill="#3a3f44"/>')
        t(X(x - 21.5), Y(y - 7), "USB", 2.4, "#c9cfcc"); t(X(x + 15), Y(y - 7), "SD", 2.4, "#c9cfcc")
    elif k == "power":
        a(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="{w/2*S:.1f}" fill="#0b0c0d" stroke="#e8ecea" stroke-width="1.5"/>')
        a(f'<path d="M{X(x-3.5):.1f},{Y(y+2.5):.1f} A{4.5*S},{4.5*S} 0 1 0 {X(x+3.5):.1f},{Y(y+2.5):.1f}" fill="none" stroke="#e8ecea" stroke-width="1.6"/>')
        a(f'<line x1="{X(x)}" y1="{Y(y+5)}" x2="{X(x)}" y2="{Y(y)}" stroke="#e8ecea" stroke-width="1.6"/>')
        t(X(x), Y(y - w / 2 - 3), "POWER (HOLD)", 2.2, "#c9cfcc")
    elif k == "screen":
        a(f'<rect x="{X(x-w/2):.1f}" y="{Y(y+h/2):.1f}" width="{w*S:.1f}" height="{h*S:.1f}" rx="{3*S}" fill="#0f1113" stroke="#2a2e32"/>')
        ax0, ax1, ay0, ay1 = x - 108.5, x + 108.5, y - 58, y + 56
        a(f'<rect x="{X(ax0):.1f}" y="{Y(ay1):.1f}" width="{(ax1-ax0)*S:.1f}" height="{(ay1-ay0)*S:.1f}" fill="#0b0d0f" stroke="#33393e"/>')
        t(X(ax0 + 3), Y(ay1 - 5), "SOUND · Track 1 · Drums", 3, "#e6ebea", "start", 500)
        for c in range(8):
            cx = 150 + 30 * c
            a(f'<rect x="{X(cx-13):.1f}" y="{Y(ay0+42):.1f}" width="{26*S}" height="{38*S}" fill="#161a1d"/>')
            a(f'<circle cx="{X(cx):.1f}" cy="{Y(ay0+20):.1f}" r="{8*S}" fill="none" stroke="#9b93f0" stroke-width="{1.6*S}" '
              f'stroke-dasharray="{8*S*2*math.pi*(0.3+0.08*c):.1f} 999" transform="rotate(135 {X(cx):.1f} {Y(ay0+20):.1f})"/>')
            t(X(cx), Y(ay0 + 35), ['Cutoff', 'Reso', 'Drive', 'Slot 1', 'Slot 2', 'Send A', 'Send B', 'Level'][c], 2.6, "#e6ebea")
        t(X(x), Y(ay1 - 26), "screen columns line up with the 8 knobs below", 2.8, "#5f676c")

t(X(W/2), Y(485), "REAR JACK LABELS (R73): AUDIO IN · AUDIO OUT · MIDI · SYNC · CV · USB · POWER", 2.6, "#5f676c")
# annotations (outside the body)
a(f'<line x1="{X(0)}" y1="{Y(0)+22}" x2="{X(W)}" y2="{Y(0)+22}" stroke="#555" stroke-width="1"/>')
t(X(W / 2), Y(0) + 34, "515 мм", 3.4, "#333")
a(f'<line x1="{X(W)+18}" y1="{Y(0)}" x2="{X(W)+18}" y2="{Y(D)}" stroke="#555" stroke-width="1"/>')
t(X(W) + 32, Y(D / 2), "500", 3.4, "#333")
a(f'<line x1="{X(-6)}" y1="{Y(330)}" x2="{X(0)}" y2="{Y(330)}" stroke="#d0453a" stroke-width="2"/>')
t(X(-7), Y(330), "330", 2.8, "#d0453a", "end")
t(X(-7), Y(170), "плоская", 2.8, "#555", "end"); t(X(-7), Y(162), "часть", 2.8, "#555", "end")
t(X(-7), Y(410), "наклон", 2.8, "#555", "end"); t(X(-7), Y(402), "30°", 2.8, "#555", "end")
t(X(-7), Y(485), "полка", 2.8, "#555", "end")
t(X(-7), Y(14), "край", 2.8, "#555", "end")
t(X(212), Y(0) + 12, "Notes, Chords: модуляция · Clips, Steps: прокрутка ◄ ► · Touch FX: глубина эффекта", 2.6, "#555")
# legend: endless vs finite
lx, ly = X(130), Y(0) + 52
for i in range(15):
    ang = math.radians(225 - 270 * i / 14)
    a(f'<circle cx="{lx + 11*math.cos(ang):.1f}" cy="{ly - 11*math.sin(ang):.1f}" r="1.6" fill="#6b63c9" fill-opacity="{0.95 if i < 8 else 0.2}"/>')
a(f'<circle cx="{lx}" cy="{ly}" r="8" fill="#141618" stroke="#4a5055"/>')
t(lx + 18, ly, "энкодер без упоров: значение — на кольце огней, риски на колпачке нет", 2.9, "#333", "start")
lx2 = X(360)
for i in range(11):
    ang = math.radians(225 - 27 * i)
    a(f'<line x1="{lx2 + 10*math.cos(ang):.1f}" y1="{ly - 10*math.sin(ang):.1f}" x2="{lx2 + 12.5*math.cos(ang):.1f}" y2="{ly - 12.5*math.sin(ang):.1f}" stroke="#333" stroke-width="1"/>')
a(f'<circle cx="{lx2}" cy="{ly}" r="8" fill="#c3c8cb" stroke="#7d8387"/>')
a(f'<line x1="{lx2}" y1="{ly}" x2="{lx2 - 5}" y2="{ly - 5}" stroke="#111" stroke-width="2" stroke-linecap="round"/>')
t(lx2 + 18, ly, "потенциометр с упорами: риска и шкала", 2.9, "#333", "start")
# scale bar
a(f'<rect x="{X(0)}" y="{Y(0)+76}" width="{100*S}" height="6" fill="#333"/>')
t(X(50), Y(0) + 90, "100 мм", 3, "#333")
t(X(W), Y(0) + 90, "Штука Дрюка · панель v5 · вид сверху, наклон в проекции · масштаб 1:1 = 2 px/мм", 3, "#333", "end")
a('</svg>')
open("panel_v5.svg", "w").write("\n".join(o))
print("ok", PW, PH)
