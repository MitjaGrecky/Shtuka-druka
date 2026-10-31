import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('F', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('FB', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

W, D, H0, WZ0, WZ1, ANG = 515.0, 500.0, 68.0, 340.0, 470.0, math.radians(30)
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

def part_deck(c):
    w, h = W, WZ0
    grid(c, w, h); outline_rect(c, w, h)
    for j in range(8):
        for i in range(8):
            x, y = 137.5 + 25 * i, 102.5 + 25 * j
            stroke(c, 0.3); c.rect(x - 10.5, y - 10.5, 21, 21, stroke=1, fill=0)
    zone(c, 122, 328, 88, 293, GREY, 'Pads 8x8')
    for i in range(8): btn(c, 137.5 + 25 * i, 75, 19, 10)
    txt(c, 'Scenes 1-8', 225, 66, 2.6)
    for j in range(8):
        y = 102.5 + 25 * j
        btn(c, 342, y, 14, 14); knob(c, 370, y, 8)
    btn(c, 342, 75, 14, 10, 'Mute', 66); btn(c, 370, 75, 14, 10, 'Solo', 66)
    zone(c, 331, 388, 62, 293, PURP, 'Tracks')
    names = ['Cutoff', 'Reso', 'Drive', 'Slot 1', 'Slot 2', 'Send A', 'Send B', 'Level']
    for k in range(8): knob(c, 150 + 30 * k, 318, 9.5); txt(c, names[k], 150 + 30 * k, 301.5, 2.2)
    zone(c, 135, 375, 296, 340, PURP, 'Params')
    for i, n in enumerate(['Grab', 'Shape', 'Perform', 'Arrange']): btn(c, 30 + 22 * i, 322, 18, 12, n, 310)
    zone(c, 15, 125, 300, 340, TEAL, 'Pages')
    for n, x, y in [('Undo', 45, 262), ('Copy', 85, 262), ('Delete', 45, 228), ('Save', 85, 228)]: btn(c, x, y, 22, 14, n)
    zone(c, 15, 115, 208, 286, TEAL, 'Edit')
    btn(c, 42, 165, 28, 28, 'Capture', 146); btn(c, 88, 165, 28, 28, 'Freeze', 146)
    zone(c, 15, 115, 137, 203, TEAL, 'Capture')
    for i, n in enumerate(['Rec', 'Play', 'Stop', 'Tap']): btn(c, 30 + 22 * i, 98, 18, 14, n, 85)
    zone(c, 15, 115, 78, 116, TEAL, 'Transport')
    for n, x in [('Monitor', 35), ('Phones', 65), ('Cue/Mix', 95)]:
        stroke(c, 0.3); c.circle(x, 42, 13, stroke=1, fill=0); knob(c, x, 42, 9.5, None, False); txt(c, n, x, 24.5, 2.2)
    zone(c, 15, 115, 18, 66, GREY, 'Volume')
    stroke(c, 0.3, GREY, (2, 1.5)); c.roundRect(125, 15, 263, 43, 2.5, stroke=1, fill=0)
    txt(c, 'Reserved: touch strip (phase 2). Wrist rest sits in front of this area.', 256.5, 36, 2.6, False, 'c', GREY)
    stroke(c, 0.3); c.circle(447, 292, 22.5, stroke=1, fill=0); knob(c, 447, 292, 19, None, False)
    txt(c, 'Main wheel 45', 447, 264, 2.2)
    for x, y in [(455, 238), (455, 206), (439, 222), (471, 222)]: btn(c, x, y, 12, 12)
    btn(c, 410, 222, 18, 12, 'Back', 211)
    zone(c, 395, 500, 195, 330, PURP, 'Navigation')
    for x, y in [(415, 160), (447, 160), (479, 160), (415, 128), (447, 128), (479, 128)]: knob(c, x, y, 9.5)
    zone(c, 395, 500, 105, 185, PURP, 'Macro')
    stroke(c, 0.3); c.rect(447 - 42, 40, 84, 4, stroke=1, fill=0); btn(c, 447, 42, 10, 16)
    btn(c, 415, 78, 18, 12, 'A', 67); btn(c, 479, 78, 18, 12, 'B', 67)
    zone(c, 395, 500, 18, 98, PURP, 'Crossfader')
    txt(c, 'FRONT EDGE', w / 2, 5, 3, True)
    txt(c, 'JOINT WITH SCREEN PANEL (fold up 30 deg)', w / 2, h - 4, 3, True)

def part_screen(c):
    w, h = W, L
    grid(c, w, h); outline_rect(c, w, h)
    sy = lambda z: S(z)
    stroke(c, 0.3, GREY, (2, 1.5)); c.rect(255 - 120, sy(405) - 73, 240, 146, stroke=1, fill=0)
    stroke(c, 0.6); c.rect(255 - 108.5, sy(405) - 68, 217, 136, stroke=1, fill=0)
    txt(c, 'CUT OUT: screen 10.1" active area 217 x 136', 255, sy(405) + 6, 3, True)
    txt(c, 'dashed = bezel 240 x 146', 255, sy(405) - 2, 2.6)
    knob(c, 45, sy(440), 9, 'Gain 1'); knob(c, 100, sy(440), 9, 'Gain 2')
    btn(c, 45, sy(395), 16, 10, 'P48'); btn(c, 100, sy(395), 16, 10, 'P48')
    btn(c, 72, sy(365), 26, 10, 'Input', sy(365) - 7.5)
    for x in (30, 115): stroke(c, 0.3); c.circle(x, sy(455), 2, stroke=1, fill=0)
    zone(c, 15, 130, sy(350), sy(465), GREY, 'Inputs')
    for i in range(12):
        stroke(c, 0.25); c.rect(392, sy(357 + i * 8.5) - 2.5, 6, 5, stroke=1, fill=0)
    txt(c, 'Main', 395, sy(350) + 1.5, 2.2)
    btn(c, 440, sy(435), 22, 10, 'Browser'); btn(c, 476, sy(435), 22, 10, 'Menu')
    stroke(c, 0.3); c.circle(458, sy(378), 8, stroke=1, fill=0); c.circle(458, sy(378), 5.5, stroke=1, fill=0)
    txt(c, 'Power (hold 2 s)', 458, sy(378) - 12, 2.2)
    zone(c, 380, 500, sy(350), sy(465), GREY, 'System')
    txt(c, 'JOINT WITH TOP PANEL', w / 2, 4, 3, True)
    txt(c, 'JOINT WITH REAR SHELF', w / 2, h - 4, 3, True)

def part_side(c):
    pts = [(0, 0), (0, H0), (WZ0, H0), (WZ1, TOP), (D, TOP), (D, 0)]
    grid(c, D, TOP)
    stroke(c, 0.6); p = c.beginPath(); p.moveTo(*pts[0])
    for q in pts[1:]: p.lineTo(*q)
    p.close(); c.drawPath(p, stroke=1, fill=0)
    stroke(c, 0.25, GREY, (2, 1.5))
    c.rect(80, 3, 170, 45, stroke=1, fill=0); txt(c, 'Mini-ITX board, ~45 high', 165, 25, 2.6, False, 'c', GREY)
    c.line(5, 50, WZ0, 50); txt(c, 'panel PCB layer', 60, 47, 2.4, False, 'c', GREY)
    c.line(455, 8, 455, 112); txt(c, 'rear jack board', 452, 60, 2.4, False, 'r', GREY)
    txt(c, 'FRONT  68', 3, H0 + 4, 3, True, 'l')
    txt(c, 'REAR  143', D - 3, TOP + 4, 3, True, 'r')
    txt(c, '30 deg', 395, H0 + 18, 3, True)
    txt(c, 'SIDE PROFILE - cut 2 (flip the second one)', 200, 20, 3.4, True)

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
    for x, t in [(35, 'Phones 1'), (95, 'Phones 2')]:
        stroke(c, 0.4); c.circle(x, 30, 4.75, stroke=1, fill=0); txt(c, t, x, 20, 2.6, True)
    stroke(c, 0.4); c.rect(430 - 13, 34 - 1.25, 26, 2.5, stroke=1, fill=0); txt(c, 'SD', 430, 27, 2.6, True)
    c.rect(472 - 6.5, 34 - 2.75, 13, 5.5, stroke=1, fill=0); txt(c, 'USB', 472, 27, 2.6, True)
    stroke(c, 0.3, GREY, (2, 1.5)); c.rect(122, 0, 265, 58, stroke=1, fill=0)
    txt(c, 'wrist rest goes here (x 122-387)', 254.5, 30, 2.8, False, 'c', GREY)
    txt(c, 'FRONT PANEL - VIEW FROM FRONT', w / 2, h - 5, 3, True)

def part_small(c):
    ox, oy = 10, 40
    stroke(c, 0.6); p = c.beginPath(); p.moveTo(ox, oy); p.lineTo(ox, oy + 58); p.lineTo(ox + 70, oy + 24); p.lineTo(ox + 70, oy); p.close(); c.drawPath(p, stroke=1, fill=0)
    txt(c, 'WRIST REST PROFILE - cut 2', ox + 35, oy - 6, 2.8, True)
    txt(c, '58', ox + 3, oy + 50, 2.6, False, 'l'); txt(c, '24', ox + 67, oy + 20, 2.6, False, 'r'); txt(c, '70', ox + 35, oy + 3, 2.6)
    txt(c, 'device side', ox + 1, oy + 62, 2.4, False, 'l')
    lines = ['CUT BY RULER (no template needed):', 'Base of the device  515 x 500', 'Rear shelf  515 x 30',
             'Wrist rest top  265 x 78 (sloped)', 'Wrist rest back  265 x 58', 'Wrist rest front  265 x 24', 'Wrist rest base  265 x 70']
    for i, t in enumerate(lines): txt(c, t, 100, oy + 90 - i * 7, 3.2, i == 0, 'l')

PARTS = [
    ('Top panel', W, WZ0, part_deck, '1 pc'),
    ('Screen panel (30 deg slope)', W, L, part_screen, '1 pc'),
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
    txt(c, 'Cardboard mockup 1:1  -  layout v4  -  body 515 x 500 mm, 68 mm front, 143 mm rear', 15, y, 3.6, False, 'l'); y -= 12
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
    rows = [('Top panel', '515 x 340', '1', 'printed'), ('Screen panel', '515 x 150', '1', 'printed, cut out screen'),
            ('Side profile', '500 x 143', '2', 'printed'), ('Rear panel', '515 x 143', '1', 'printed'),
            ('Front panel', '515 x 68', '1', 'printed'), ('Rear shelf', '515 x 30', '1', 'cut by ruler'),
            ('Base', '515 x 500', '1', 'cut by ruler'), ('Wrist rest', '265 x 70, h 58/24', '1 set', 'profile printed')]
    for k, (a, b2, n, note) in enumerate(rows):
        txt(c, a, 18, y, 3.1, False, 'l'); txt(c, b2, 70, y, 3.1, False, 'l'); txt(c, n, 115, y, 3.1, False, 'l'); txt(c, note, 130, y, 3.1, False, 'l'); y -= 5.5
    y -= 4
    steps = [('ASSEMBLY', True),
             ('1. Glue the printed sheets onto cardboard (3-5 mm), then cut along the thick outer lines.', False),
             ('2. Base 515 x 500. Glue both side profiles on its left and right edges, standing up.', False),
             ('3. Glue the front panel (68 high) and rear panel (143 high) between the sides.', False),
             ('   With board thickness t, shorten front, rear, top and screen panels by 2t in width.', False),
             ('4. Glue the top panel flat at 68 mm, the screen panel on the 30 deg slope, the rear shelf on top.', False),
             ('5. Glue the wrist rest in front of the device, between x = 122 and 387 mm.', False),
             ('6. Knobs: bottle caps or coins on the circles. Main wheel: 45 mm lid. Pads: 21 mm squares.', False),
             ('', False),
             ('WHAT TO CHECK', True),
             ('Sit as you normally work. Reach the main wheel, Capture and the param knobs without stretching.', False),
             ('Can you read the screen labels? Do cables at the back clear the screen slope?', False),
             ('Do your wrists rest comfortably while playing the pads? Note anything awkward.', False)]
    for s, b in steps: txt(c, s, 15, y, 3.4 if b else 3.1, b, 'l'); y -= 6 if s else 3
    txt(c, 'Sizes from project docs 13 (section 3.6) and 17. Internals are estimates.', 15, 14, 2.8, False, 'l', GREY)

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
