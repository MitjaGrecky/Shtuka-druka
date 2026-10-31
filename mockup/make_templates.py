"""1:1 cardboard mockup templates for panel v7, positions from layout_v7.json. AGPL-3.0-or-later.
Usage: make_templates.py out.pdf"""
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('F', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf'))
pdfmetrics.registerFont(TTFont('FB', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf'))

W, D, H0, WZ0, WZ1, ANG = 515.0, 460.0, 68.0, 300.0, 430.0, math.radians(30)
T30 = math.tan(ANG)
TOP = H0 + (WZ1 - WZ0) * T30
L = (WZ1 - WZ0) / math.cos(ANG)
S = lambda z: (z - WZ0) / math.cos(ANG)
YS = 1.2
MARGIN, HEAD, FOOT, OV = 8.0, 15.0, 13.0, 10.0
TEAL, PURP, GREY = (0.06, 0.48, 0.39), (0.35, 0.31, 0.75), (0.42, 0.44, 0.43)

def txt(c, s, x, y, size=3.0, bold=False, align='c', color=(0, 0, 0)):
    c.setFillColorRGB(*color)
    c.setFont('FB' if bold else 'F', size)
    if align == 'c': c.drawCentredString(x, y - size * 0.35, s)
    elif align == 'l': c.drawString(x, y - size * 0.35, s)
    else: c.drawRightString(x, y - size * 0.35, s)

def stroke(c, w=0.25, col=(0, 0, 0), dash=None):
    c.setLineWidth(w); c.setStrokeColorRGB(*col)
    c.setDash(*dash) if dash else c.setDash()

def zone(c, x0, x1, y0, y1, col, title):
    stroke(c, 0.3, col); c.roundRect(x0, y0, x1 - x0, y1 - y0, 2.5, stroke=1, fill=0)
    if title: txt(c, title, x0 + 2, y1 - 2.6, 2.6, True, 'l', col)

def btn(c, x, y, w, h, label=None, ly=None):
    stroke(c, 0.3); c.rect(x - w / 2, y - h / 2, w, h, stroke=1, fill=0)
    if label: txt(c, label, x, ly if ly is not None else y - h / 2 - 2.6, 2.2)

def knob(c, x, y, r, label=None, ring=True):
    stroke(c, 0.3); c.circle(x, y, r, stroke=1, fill=0)
    if ring:
        stroke(c, 0.2, (0.4, 0.4, 0.4), (1, 1)); c.circle(x, y, r + 3.6, stroke=1, fill=0)
    stroke(c, 0.2); c.line(x - 1.5, y, x + 1.5, y); c.line(x, y - 1.5, x, y + 1.5)
    if label: txt(c, label, x, y - r - (6 if ring else 3), 2.2)

def grid(c, w, h):
    stroke(c, 0.12, (0.82, 0.84, 0.83))
    for x in range(50, int(w), 50): c.line(x, 0, x, h)
    for y in range(50, int(h), 50): c.line(0, y, w, y)

def outline_rect(c, w, h):
    stroke(c, 0.6); c.rect(0, 0, w, h, stroke=1, fill=0)

import json
import os
_here = os.path.dirname(os.path.abspath(__file__))
_lay = next(p for p in (os.path.join(_here, 'layout_v7.json'), os.path.join(_here, 'layout', 'layout_v7.json')) if os.path.exists(p))
LAY = json.load(open(_lay))
E = LAY['elements']
C30 = math.cos(ANG)


def onw(e):
    return e['y'] > WZ0


def draw_el(c, e, X, Y, k):
    """X, Y: centre on the sheet (mm); k: factor for the depth dimension (1 on the deck, 1/cos30 on the slope)."""
    kind, w, h = e['kind'], e['w'], e['h'] * k
    if kind == 'button':
        stroke(c, 0.3); c.rect(X - w / 2, Y - h / 2, w, h, stroke=1, fill=0)
        lab = e['label']; size = min(2.6, (w - 2) / max(len(lab), 1) * 1.55, h * 0.4)
        txt(c, lab, X, Y, size, e['h'] >= 20)
    elif kind == 'pad':
        stroke(c, 0.3); c.rect(X - w / 2, Y - h / 2, w, h, stroke=1, fill=0)
    elif kind in ('encoder', 'pot'):
        r = w / 2
        stroke(c, 0.35); c.circle(X, Y, r, stroke=1, fill=0)
        stroke(c, 0.2); c.line(X - 1.5, Y, X + 1.5, Y); c.line(X, Y - 1.5, X, Y + 1.5)
        if kind == 'encoder':
            stroke(c, 0.2, (0.4, 0.4, 0.4), (1, 1)); c.circle(X, Y, e.get('ring', w + 7) / 2, stroke=1, fill=0)
            off = e.get('ring', w + 7) / 2 + 2.6
        else:
            for i in range(11):
                a = math.radians(225 - 27 * i); r0, r1 = r + 2.2, r + (3.6 if i in (0, 10) else 3)
                stroke(c, 0.25); c.line(X + r0 * math.cos(a), Y + r0 * math.sin(a), X + r1 * math.cos(a), Y + r1 * math.sin(a))
            off = r + 4.4
        if e['label']:
            if onw(e): txt(c, e['label'], X, Y - off, 2.3)
            else: txt(c, e['label'], X, Y + off + 0.6, 2.3)
    elif kind == 'wheel':
        stroke(c, 0.4); c.circle(X, Y, w / 2, stroke=1, fill=0); stroke(c, 0.2, (0.4, 0.4, 0.4), (1, 1)); c.circle(X, Y, w / 2 - 2.2, stroke=1, fill=0)
        stroke(c, 0.2); c.line(X - 1.5, Y, X + 1.5, Y); c.line(X, Y - 1.5, X, Y + 1.5)
        txt(c, 'Wheel 38 (push = OK)', X, Y - w / 2 - 3.2, 2.3)
    elif kind == 'strip':
        stroke(c, 0.4); c.roundRect(X - w / 2, Y - h / 2, w, h, 2, stroke=1, fill=0)
        txt(c, 'touch strip %g mm' % w, X, Y, 2.6, False, 'c', GREY)
    elif kind == 'fader':
        stroke(c, 0.3); c.rect(X - w / 2, Y - 2, w, 4, stroke=1, fill=0); c.rect(X - 5, Y - 8, 10, 16, stroke=1, fill=0)
    elif kind == 'meter':
        for i in range(14):
            yy = Y - h / 2 + 5 + i * (h - 10) / 13
            stroke(c, 0.25); c.rect(X - w / 2, yy - 2.8, w, 5.6, stroke=1, fill=0)
        txt(c, e['label'], X, Y - h / 2 - 2.6, 2.6, True)
    elif kind == 'led':
        stroke(c, 0.3); c.circle(X, Y, w / 2, stroke=1, fill=0)
    elif kind == 'pocket':
        stroke(c, 0.3, GREY, (1.5, 1)); c.roundRect(X - w / 2, Y - h / 2, w, h, 2, stroke=1, fill=0)
        stroke(c, 0.5); c.rect(X - 23.5 - 6.5, Y - 1, 13, 6, stroke=1, fill=0); c.rect(X + 23 - 13, Y, 26, 3, stroke=1, fill=0)
        stroke(c, 0.3); c.circle(X, Y + 2, 1.6, stroke=1, fill=0)
        txt(c, 'USB', X - 23.5, Y - 6.5, 2.2); txt(c, 'busy', X, Y - 6.5, 2.0); txt(c, 'SD', X + 23, Y - 6.5, 2.2)
    elif kind == 'power':
        stroke(c, 0.3); c.circle(X, Y, w / 2, stroke=1, fill=0); c.circle(X, Y, w / 2 - 2, stroke=1, fill=0)
        txt(c, 'Power (hold 2 s)', X, Y - w / 2 - 3.6, 2.2)
    elif kind == 'screen':
        stroke(c, 0.6); c.rect(X - w / 2, Y - h / 2, w, h, stroke=1, fill=0)
        stroke(c, 0.3, GREY, (2, 1.5)); c.rect(X - 217.5 / 2, Y - 135.6 / 2, 217.5, 135.6, stroke=1, fill=0)
        txt(c, 'CUT OUT: screen window %g x %.0f' % (w, h), X, Y + 8, 3, True)
        txt(c, 'dashed = active area 217.5 x 135.6 (10.1", 1280 x 800)', X, Y + 1, 2.6)
        for col in range(8):
            xx = X - 98 + 28 * col
            stroke(c, 0.2, GREY, (1, 1.5)); c.line(xx, Y - h / 2, xx, Y - h / 2 + 12)
        txt(c, 'ticks = screen columns, same x as the knobs and pad columns', X, Y - h / 2 + 15, 2.3, False, 'c', GREY)


def part_deck(c):
    w, h = W, WZ0
    grid(c, w, h); outline_rect(c, w, h)
    for e in E:
        if not onw(e): draw_el(c, e, e['x'], e['y'], 1)
    txt(c, 'FRONT EDGE', w / 2, 4, 3, True)
    txt(c, 'JOINT WITH SCREEN PANEL (fold up 30 deg)', w / 2, h - 4, 3, True)


def part_screen(c):
    w, h = W, L
    grid(c, w, h); outline_rect(c, w, h)
    for e in E:
        if onw(e): draw_el(c, e, e['x'], S(e['y']), 1 / C30)
    txt(c, 'JOINT WITH TOP PANEL', 459, 3, 3, True)
    txt(c, 'JOINT WITH REAR SHELF', 459, h - 3, 3, True)


def part_shelf(c):
    w, h = W, D - WZ1
    grid(c, w, h); outline_rect(c, w, h)
    for t, x0, x1, lines in [('Audio In', 4.5, 162.5, ['Mic/Line 1-2, Hi-Z 1-2', 'Line 1-8, Phono L R, GND']),
                             ('Audio Out', 172.5, 242.5, ['Main L R, Aux L R', 'RCA L R']),
                             ('Control', 252.5, 426.5, ['MIDI In 1-2, Out 1-4, TRS In, O1, O2', 'Clock, Reset, CV In 1-4, CV 1-8']),
                             ('Power / USB', 436.5, 510.5, ['LAN, USB-A, USB-C (PC)', 'DC 12-24V, On/Off'])]:
        cx = (x0 + x1) / 2
        txt(c, t, cx, h - 8, 3, True); [txt(c, l, cx, h - 15.5 - i * 6.5, 2.3) for i, l in enumerate(lines)]
    txt(c, 'JOINT WITH SCREEN PANEL', w / 2, 2.2, 2.2, False, 'c', GREY)


def part_side(c):
    pts = [(0, 0), (0, H0), (WZ0, H0), (WZ1, TOP), (D, TOP), (D, 0)]
    grid(c, D, TOP)
    stroke(c, 0.6); p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=1, fill=0)
    stroke(c, 0.25, GREY, (2, 1.5))
    c.rect(45, 3, 170, 45, stroke=1, fill=0); txt(c, 'Mini-ITX, ~45 high', 130, 25, 2.6, False, 'c', GREY)
    c.line(5, 50, WZ0 - 8, 50); txt(c, 'panel PCB layer', 250, 47, 2.4, False, 'c', GREY)
    c.rect(315, 6, 90, 22, stroke=1, fill=0); txt(c, 'audio board', 360, 17, 2.4, False, 'c', GREY)
    c.rect(312, 3, 86, 45, stroke=1, fill=0); txt(c, 'battery bay (right side)', 355, 42, 2.2, False, 'c', GREY)
    c.line(D - 45, 8, D - 45, 112); txt(c, 'rear jack board', D - 48, 60, 2.4, False, 'r', GREY)
    txt(c, 'FRONT  68', 3, H0 + 4, 3, True, 'l')
    txt(c, 'REAR  143', D - 3, TOP + 4, 3, True, 'r')
    txt(c, '30 deg', (WZ0 + WZ1) / 2 - 10, H0 + 22, 3, True)
    txt(c, 'SIDE PROFILE - cut 2 (flip the second one)', 160, 60, 3.4, True)


def part_rear(c):
    w, h = W, TOP
    grid(c, w, h); outline_rect(c, w, h)
    def tag(t, r, y, out):
        c.setFont('FB', 2.2); tw = c.stringWidth(t, 'FB', 2.2) + 2
        stroke(c, 0.25)
        if out:
            c.setFillColorRGB(0, 0, 0); c.roundRect(r - tw / 2, y - 1.8, tw, 3.6, 0.6, stroke=1, fill=1)
            txt(c, t, r, y, 2.2, True, 'c', (1, 1, 1))
        else:
            c.roundRect(r - tw / 2, y - 1.8, tw, 3.6, 0.6, stroke=1, fill=0); txt(c, t, r, y, 2.2, True)
    HOLE = {'xlr': 24, 'trs': 9.5, 'din': 16, 'rca': 9, 'mini': 6, 'dc': 8}
    OFF = {'xlr': 15.5, 'din': 12, 'trs': 9, 'rca': 7.5, 'mini': 7.5, 'dc': 8}
    def J(kind, r, y, t, out):
        yy = y * YS; stroke(c, 0.4); c.circle(r, yy, HOLE[kind] / 2, stroke=1, fill=0)
        stroke(c, 0.2); c.line(r - 1.5, yy, r + 1.5, yy); c.line(r, yy - 1.5, r, yy + 1.5)
        if t: tag(t, r, (y - OFF[kind]) * YS, out)
    def B(wd, ht, r, y, t):
        yy = y * YS; stroke(c, 0.4); c.rect(r - wd / 2, yy - ht / 2, wd, ht, stroke=1, fill=0)
        if t: tag(t, r, yy - ht / 2 - 4, False)
    def Z(r0, r1, t):
        stroke(c, 0.3); c.roundRect(r0, 4, r1 - r0, h - 10, 2.5, stroke=1, fill=0); txt(c, t, r0 + 2, h - 8.6, 2.8, True, 'l')
    Z(4.5, 78.5, 'Power / USB')
    B(16, 13, 20, 78, 'LAN'); B(13, 5.5, 40, 80, 'USB-A'); B(9, 3.5, 62, 80, 'USB-C (PC)')
    J('dc', 22, 40, None, False); tag('DC 12-24V', 22, 30 * YS, False); B(12, 8, 52, 40, 'On/Off')
    Z(88.5, 262.5, 'Control')
    for t, r, y, o in [('In 1', 100, 82, 0), ('Out 1', 122, 82, 1), ('Out 3', 144, 82, 1), ('In 2', 100, 52, 0), ('Out 2', 122, 52, 1), ('Out 4', 144, 52, 1)]: J('din', r, y, t, o)
    for t, r, o in [('TRS In', 100, 0), ('TRS O1', 122, 1), ('TRS O2', 144, 1)]: J('mini', r, 22, t, o)
    for i, (t, o) in enumerate([('Clk O1', 1), ('Clk O2', 1), ('Rst O', 1), ('Clk In', 0), ('Rst In', 0)]): J('mini', 172 + i * 17, 90, t, o)
    for i in range(4): J('mini', 172 + i * 17, 68, 'CV In %d' % (i + 1), 0)
    for i in range(8): J('mini', 172 + (i % 4) * 17, 46 if i < 4 else 24, 'CV %d' % (i + 1), 1)
    Z(272.5, 342.5, 'Audio Out')
    for t, r, y in [('Main L', 292, 80), ('Main R', 322, 80), ('Aux L', 292, 52), ('Aux R', 322, 52)]: J('trs', r, y, t, 1)
    for t, r in [('RCA L', 292), ('RCA R', 322)]: J('rca', r, 24, t, 1)
    Z(352.5, 510.5, 'Audio In')
    for t, r in [('Mic/Line 1', 370), ('Mic/Line 2', 400)]: J('xlr', r, 80, t, 0)
    for t, r in [('Hi-Z 1', 370), ('Hi-Z 2', 400)]: J('trs', r, 32, t, 0)
    for t, r in [('Phono L', 428), ('Phono R', 446)]: J('rca', r, 86, t, 0)
    J('dc', 468, 86, None, 0); tag('GND', 468, 78.5 * YS, False); B(5, 9, 490, 86, None); tag('Phono/Line', 490, 78.5 * YS, False)
    for i in range(8): J('trs', 428 + (i % 4) * 22, 56 if i < 4 else 28, 'Line %d' % (i + 1), 0)
    txt(c, 'REAR PANEL - VIEW FROM BEHIND.  Filled tag = output, outlined tag = input.  Circles = hole diameters.', w / 2, 1.8, 2.4)

def part_front(c):
    w, h = W, H0
    grid(c, w, h); outline_rect(c, w, h)
    for x, t in [(32, 'Phones 1'), (80, 'Phones 2')]:
        stroke(c, 0.4); c.circle(x, 30, 4.75, stroke=1, fill=0); txt(c, t, x, 20, 2.6, True)
    stroke(c, 0.3, GREY, (2, 1.5)); c.rect(110, 0, 221.5, 58, stroke=1, fill=0)
    txt(c, 'wrist rest goes here (x 110-331.5, as wide as the pad grid)', 220.75, 30, 2.8, False, 'c', GREY)
    txt(c, 'FRONT PANEL - VIEW FROM FRONT', w / 2, h - 5, 3, True)


def part_small(c):
    ox, oy = 10, 40
    stroke(c, 0.6); p = c.beginPath(); p.moveTo(ox, oy); p.lineTo(ox, oy + 58); p.lineTo(ox + 70, oy + 24); p.lineTo(ox + 70, oy); p.close(); c.drawPath(p, stroke=1, fill=0)
    txt(c, 'WRIST REST PROFILE - cut 2', ox + 35, oy - 6, 2.8, True)
    txt(c, '58', ox + 3, oy + 50, 2.6, False, 'l'); txt(c, '24', ox + 67, oy + 20, 2.6, False, 'r'); txt(c, '70', ox + 35, oy + 3, 2.6)
    txt(c, 'device side', ox + 1, oy + 62, 2.4, False, 'l')
    lines = ['CUT BY RULER (no template needed):', 'Base of the device  515 x 460',
             'Wrist rest top  221.5 x 78 (sloped)', 'Wrist rest back  221.5 x 58', 'Wrist rest front  221.5 x 24', 'Wrist rest base  221.5 x 70']
    for i, t in enumerate(lines): txt(c, t, 100, oy + 90 - i * 7, 3.2, i == 0, 'l')

PARTS = [
    ('Top panel', W, WZ0, part_deck, '1 pc'),
    ('Screen panel (30 deg slope)', W, L, part_screen, '1 pc'),
    ('Rear shelf (rear jack labels, R73)', W, D - WZ1, part_shelf, '1 pc'),
    ('Side profile', D, TOP, part_side, '2 pcs'),
    ('Rear panel', W, TOP, part_rear, '1 pc'),
    ('Front panel', W, H0, part_front, '1 pc'),
    ('Wrist rest + parts cut by ruler', 250, 140, part_small, 'profile: 2 pcs'),
]

def layout(pw, ph):
    uw, uh = pw - 2 * MARGIN, ph - 2 * MARGIN - HEAD - FOOT
    return uw, uh

def tiles(w, h, pagesize):
    pw, ph = pagesize[0] / mm, pagesize[1] / mm
    uw, uh = layout(pw, ph)
    nx = max(1, math.ceil((w - OV) / (uw - OV))) if w > uw else 1
    ny = max(1, math.ceil((h - OV) / (uh - OV))) if h > uh else 1
    return nx, ny, uw, uh

def scale_bar(c, x, y):
    stroke(c, 0.4); c.line(x, y, x + 100, y)
    for k in range(0, 101, 10): c.line(x + k, y, x + k, y + (3 if k % 50 == 0 else 1.5))
    txt(c, 'CHECK: this bar must measure exactly 100 mm. If not, reprint at 100% / Actual size.', x + 104, y + 1, 2.8, False, 'l')

def page_frame(c, pw, ph, title, info, nx, ny, i, j):
    txt(c, 'SHTUKA DRUKA - cardboard mockup 1:1', MARGIN, ph - MARGIN - 3, 3.4, True, 'l')
    txt(c, title + '  -  ' + info, MARGIN, ph - MARGIN - 9, 3, False, 'l')
    if nx * ny > 1:
        cs = 5; mx = pw - MARGIN - nx * cs; my = ph - MARGIN - 12
        for a in range(nx):
            for b in range(ny):
                stroke(c, 0.25)
                c.setFillColorRGB(*(TEAL if (a, b) == (i, j) else (1, 1, 1)))
                c.rect(mx + a * cs, my + b * cs * 0.7, cs, cs * 0.7, stroke=1, fill=1)
    scale_bar(c, MARGIN, MARGIN + 4)

def draw_cover(c):
    pw, ph = A4[0] / mm, A4[1] / mm
    c.scale(mm, mm)
    y = ph - 22
    txt(c, 'SHTUKA DRUKA', 15, y, 9, True, 'l'); y -= 9
    txt(c, 'Cardboard mockup 1:1  -  panel v7  -  body 515 x 460 mm, 68 mm front, 143 mm rear', 15, y, 3.6, False, 'l'); y -= 12
    lines = [
        ('PRINTING', True),
        ('Print at 100% / Actual size. Do NOT use "Fit to page". A4 paper.', False),
        ('Every sheet has a 100 mm bar at the bottom. Measure it before cutting.', False),
        ('', False),
        ('JOINING SHEETS', True),
        ('Sheets overlap by 10 mm. On a sheet with a neighbour to the right or above,', False),
        ('the shaded GLUE band shows where the next sheet goes.', False),
        ('Trim the next sheet along its CUT edge, lay it on the band, align the drawing', False),
        ('and the 50 mm grid lines, glue. The mini map (top right) shows the sheet position.', False),
        ('', False),
        ('PARTS', True),
    ]
    for s, b in lines: txt(c, s, 15, y, 3.4 if b else 3.1, b, 'l'); y -= 6 if s else 3
    rows = [('Top panel', '515 x 300', '1', 'printed'), ('Screen panel', '515 x 150', '1', 'printed, cut out screen'),
            ('Rear shelf', '515 x 30', '1', 'printed (rear jack labels)'), ('Side profile', '460 x 143', '2', 'printed'),
            ('Rear panel', '515 x 143', '1', 'printed'), ('Front panel', '515 x 68', '1', 'printed'),
            ('Base', '515 x 460', '1', 'cut by ruler'), ('Wrist rest', '221.5 x 70, h 58/24', '1 set', 'profile printed')]
    for k, (a, b2, n, note) in enumerate(rows):
        txt(c, a, 18, y, 3.1, False, 'l'); txt(c, b2, 70, y, 3.1, False, 'l'); txt(c, n, 115, y, 3.1, False, 'l'); txt(c, note, 130, y, 3.1, False, 'l'); y -= 5.5
    y -= 4
    steps = [('ASSEMBLY', True),
             ('1. Glue the printed sheets onto cardboard (3-5 mm), then cut along the thick outer lines.', False),
             ('2. Base 515 x 460. Glue both side profiles on its left and right edges, standing up.', False),
             ('3. Glue the front panel (68 high) and rear panel (143 high) between the sides.', False),
             ('   With board thickness t, shorten front, rear, top and screen panels by 2t in width.', False),
             ('4. Glue the top panel flat at 68 mm, the screen panel on the 30 deg slope, the rear shelf on top.', False),
             ('5. Glue the wrist rest in front of the device, between x = 110 and 331.5 mm (under the pads).', False),
             ('6. Knobs: bottle caps or coins on the circles. Wheel: 38 mm lid. Pads: 25.5 x 21 mm pieces.', False),
             ('', False),
             ('WHAT TO CHECK', True),
             ('Sit as you normally work. Reach Capture, the 8 screen knobs, the wheel and Filter without stretching.', False),
             ('Two fingers on one pad: is 25.5 mm wide enough? Do palms on the touch strip get in the way?', False),
             ('Wheel next to the slope: is there room for your knuckles? Is the screen readable?', False),
             ('Do your wrists rest comfortably while playing the pads? Note anything awkward.', False)]
    for s, b in steps: txt(c, s, 15, y, 3.4 if b else 3.1, b, 'l'); y -= 6 if s else 3
    txt(c, 'Positions from layout_v7.json (doc 27, decision R107). Internals are estimates.', 15, 14, 2.8, False, 'l', GREY)

def build(path):
    c = canvas.Canvas(path, pagesize=A4)
    c.setTitle('Shtuka Druka - cardboard mockup 1:1'); c.setAuthor('Shtuka Druka project')
    draw_cover(c); c.showPage()
    total = 0
    for title, w, h, fn, qty in PARTS:
        best = None
        for ps in (landscape(A4), A4):
            nx, ny, uw, uh = tiles(w, h, ps)
            if best is None or nx * ny < best[0]: best = (nx * ny, ps, nx, ny, uw, uh)
        _, ps, nx, ny, uw, uh = best
        pw, ph = ps[0] / mm, ps[1] / mm
        for j in range(ny):
            for i in range(nx):
                c.setPageSize(ps); c.saveState(); c.scale(mm, mm)
                x0 = i * (uw - OV); y0 = j * (uh - OV)
                ox, oy = MARGIN, MARGIN + FOOT
                k = j * nx + i + 1
                info = '%s - sheet %d of %d (column %d, row %d from bottom)' % (qty, k, nx * ny, i + 1, j + 1)
                page_frame(c, pw, ph, title, info, nx, ny, i, j)
                c.saveState()
                pth = c.beginPath(); pth.rect(ox, oy, uw, uh); c.clipPath(pth, stroke=0, fill=0)
                c.translate(ox - x0, oy - y0)
                fn(c)
                c.restoreState()
                c.setFillAlpha(0.13); c.setFillColorRGB(0, 0.4, 0.3)
                if i < nx - 1:
                    c.rect(ox + uw - OV, oy, OV, uh, stroke=0, fill=1)
                if j < ny - 1:
                    c.rect(ox, oy + uh - OV, uw, OV, stroke=0, fill=1)
                c.setFillAlpha(1)
                if i < nx - 1:
                    stroke(c, 0.3, (0, 0.4, 0.3), (2, 1)); c.line(ox + uw - OV, oy, ox + uw - OV, oy + uh)
                    c.saveState(); c.translate(ox + uw - OV / 2, oy + uh / 2); c.rotate(90)
                    txt(c, 'GLUE - next sheet (column %d) goes here' % (i + 2), 0, 0, 2.6, True, 'c', (0, 0.4, 0.3)); c.restoreState()
                if j < ny - 1:
                    stroke(c, 0.3, (0, 0.4, 0.3), (2, 1)); c.line(ox, oy + uh - OV, ox + uw, oy + uh - OV)
                    txt(c, 'GLUE - next sheet (row %d) goes here' % (j + 2), ox + uw / 2, oy + uh - OV / 2, 2.6, True, 'c', (0, 0.4, 0.3))
                stroke(c, 0.35, (0.7, 0.1, 0.1), (3, 1.5))
                if i > 0:
                    c.line(ox, oy, ox, oy + uh)
                    c.saveState(); c.translate(ox + 2.5, oy + 20); c.rotate(90); txt(c, 'CUT this edge', 0, 0, 2.4, True, 'c', (0.7, 0.1, 0.1)); c.restoreState()
                if j > 0:
                    c.line(ox, oy, ox + uw, oy); txt(c, 'CUT this edge', ox + 30, oy + 2.5, 2.4, True, 'c', (0.7, 0.1, 0.1))
                c.restoreState(); c.showPage(); total += 1
    c.save()
    return total + 1

if __name__ == '__main__':
    import sys
    print(build(sys.argv[1]))
