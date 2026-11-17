#!/usr/bin/env python3
"""Study for docs/ru/41_design_review.md (section 15): the user's two lines on the side view (17.11.2026) -
a long slope from right behind the knob row to the rear top, with no step (red) or a small one (orange).
Loads model3d/fit/fit_model.py with env settings, then lengthens the slope (SHELF_Y) and keeps the rear height,
and reports what collides. Nothing in the model is changed; this file only reads it.
Run: python 41_wedge_study.py   (any python 3; never kicad-cli)."""
import importlib.util
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FM = os.path.join(HERE, "..", "..", "..", "model3d", "fit", "fit_model.py")
KEYS = ("FRONT_Z", "DECK", "COMPUTER", "H5_STANDOFF", "H5_H", "H5_Z0", "PANEL_GAP", "P2_GAP", "P2_PARTS", "PANEL_PARTS", "WHEEL_TRACK",
        "F1_MODE", "FRONT_LIP", "REAR_SHIFT", "FOLD_SHIFT", "JACK_H", "JACK_W", "F1_STAND", "M1_J1_H", "A1_X0", "A1_Y0", "A1_Z0",
        "PW_X0", "PW_TOP", "H5_PORT", "H5_PORT_LEN", "H5_REAR_X", "H5_REAR_Y", "BATT_BOXES", "LIPO_H", "FAN", "BACK_H",
        "REAR_JACK_TOP", "REAR_JACK_TOP_R", "R2_TALL_X1", "R1_TOP", "R2_TOP", "BATT_LIPO", "SCREEN", "SCREEN_ROT")


def load(env, shelf_y, back_z, screen_shift=None):
    for k in KEYS:
        os.environ.pop(k, None)
    os.environ.update({k: str(v) for k, v in env.items()})
    spec = importlib.util.spec_from_file_location("fm_wedge", FM)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(FM))
    spec.loader.exec_module(m)
    # the longer slope: same fold, shelf (end of the slope) further back, rear height kept
    m.SHELF_Y, m.BACK_Z = shelf_y, back_z
    m.SLOPE = math.atan2(m.BACK_Z - m.FOLD_Z, m.SHELF_Y - m.FOLD_Y)
    m.SLOPE_LEN = math.hypot(m.BACK_Z - m.FOLD_Z, m.SHELF_Y - m.FOLD_Y)
    m.POCKET = (413.0, 505.0, m.s_of(365) - 12 / math.cos(m.SLOPE), m.s_of(365) + 12 / math.cos(m.SLOPE))
    if screen_shift is not None:
        m.SCREEN_SHIFT = screen_shift
    return m


def collisions(m, rework=None):
    P = m.parts()
    if rework:
        P = rework(m, P)
    res = m.check(P)
    return [(round(abs(g), 1), a, b) for g, a, b, e in res if g < -0.05]


def corner_rework(h5x0=391.0, fan=True):
    """Proposed rework of the rear wall for the H5 in the rear right corner (assumption, not a design):
    R2 low arm ends at x 388; rear jacks right of x 388 are panel-mount (on nuts, R141) and sit above the H5 (z 60-112)
    and right of the fan; a 60 mm fan blows out through the rear wall above the H5."""
    def f(m, P):
        keep = [p for p in P if p.name not in ("R2 control rear board, low arm", "Rear jacks", "Rear jacks (right)")]
        y0 = 413.4 + m.RS
        keep.append(m.box("R2 low arm (shortened)", "rear", m.R2_TALL_X1, h5x0 - 3, y0, y0 + 1.6, 10, 38, color="pcb"))
        keep.append(m.box("Rear jacks (left)", "rear", 5, h5x0 - 3, y0 + 1.6, m.D - m.SKIN, 8, m.REAR_JACK_TOP, color="metal", est=True))
        fx1 = h5x0 + 60 if fan else h5x0
        keep.append(m.box("Rear panel-mount jacks over the H5", "rear", fx1, 510, y0 + 1.6, m.D - m.SKIN, 60, m.REAR_JACK_TOP,
                          color="metal", est=True))
        if fan:
            keep.append(m.box("Fan 60 x 60 x 15 (rear wall)", "rear", h5x0, h5x0 + 60, m.D - m.SKIN - 15, m.D - m.SKIN, 58, 118,
                              color="plastic"))
        return keep
    return f


def env(deck, fold_z, fs, a1y, a1z, batt, h5y, h5_st=8, port="S"):
    rs = 40                      # REAR_SHIFT: depth 460 + 28 lip + 40 + FS
    return dict(WHEEL_TRACK=1, COMPUTER="H5REAR", P2_PARTS=1.5, PANEL_PARTS=3, PW_X0=245, A1_X0=20, A1_Y0=a1y, A1_Z0=a1z,
                H5_PORT=port, F1_MODE="LIP", FRONT_LIP=28, REAR_SHIFT=rs, FOLD_SHIFT=fs, DECK=deck, FRONT_Z=fold_z,
                H5_REAR_X=451, H5_REAR_Y=h5y, H5_STANDOFF=h5_st, JACK_H=12.7, JACK_W=15.9, F1_STAND=1, M1_J1_H=5, PW_TOP=25,
                BATT_BOXES=batt)


def run(name, e, shelf_off, back, shift=None, rework=None, show=30):
    m = load(e, 0, back)                                  # first load to get FOLD_Y
    m = load(e, m.FOLD_Y + shelf_off, back, shift)
    col = collisions(m, rework)
    print(f"\n== {name}: slope {math.degrees(m.SLOPE):.1f} deg over {m.SHELF_Y - m.FOLD_Y:g} mm, fold y {m.FOLD_Y:g} z {m.FOLD_Z:g}, "
          f"deck {m.TOP_Z:g}, rear {m.BACK_Z:g}, depth {m.D + m.FL:g}, screen shift {m.SCREEN_SHIFT:g}; collisions {len(col)}", flush=True)
    for g, a, b in sorted(col, reverse=True)[:show]:
        print(f"   {g:6.1f}  {a}  /  {b}")
    return m, col


if __name__ == "__main__":
    import itertools
    bA1 = lambda y: f"40,210,{y},{y + 100},3"         # pack on the floor under A1 (final model)
    bP2 = "130,300,60,160,3"                          # pack under the pads (P2), user's idea
    # R1 / R2 line at y 413.4 + 40 + FS; A1 docks to it; H5 against the rear wall (inner y = D - 3), ports to the front (S)
    for fs in (0, 15):
        rl = 453.4 + fs
        D = 500 + fs
        h5y = D - 3 - 60 - 0.5
        for deck, back, shift in ((22, 131, 0), (22, 131, 30), (32, 131, 0), (32, 131, 30), (32, 116, 30)):
            if deck == 22:
                e = env(22, 22 if fs == 0 else 31, fs, rl - 101, 20, bA1(rl - 101), h5y)
            else:
                e = env(32, 32, fs, rl - 101, 6, bP2, h5y)
            run(f"fold +{fs}, deck {deck}, rear {back}", e, D - 3 - 41 - (300 + fs) if True else 0, back, shift, corner_rework())


# ------------------------------------------------------------------ drawings straight from the model boxes
COL = {"pcb": "#3f9b5b", "parts": "#9fd3ad", "metal": "#9aa5b1", "shell": "#d9dee3", "battery": "#e8b84a", "plastic": "#c5cbd3",
       "glass": "#8ec5e8", "lcd": "#5d7f99", "knob": "#2b2f33", "chip": "#333", "led": "#f0c", "standoff": "#b0b8c0"}
GRP_HI = {"itx": "#d64545", "battery": "#e8b84a"}


def corners(b):
    out = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            for sz in (-1, 1):
                v = [b.c[i] + sx * b.h[0] * b.ax[0][i] + sy * b.h[1] * b.ax[1][i] + sz * b.h[2] * b.ax[2][i] for i in range(3)]
                out.append(v)
    return out


def hull2(pts):
    pts = sorted(set((round(a, 2), round(b, 2)) for a, b in pts))
    if len(pts) < 3:
        return pts
    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def draw(m, P, fname, title, view="side", user_lines=None):
    """view side: y (front at left) vs z; view top: x vs y (front at bottom)."""
    S = 1.3
    if view == "side":
        X0, X1, Z0, Z1 = -40, m.D + 20, -15, 150
        px = lambda y, z: (30 + (y - X0) * S, 30 + (Z1 - z) * S)
        order = sorted(P, key=lambda b: -b.c[0])          # far side first
        proj = lambda b: [px(v[1], v[2]) for v in corners(b)]
    else:
        X0, X1, Z0, Z1 = -10, 525, -40, m.D + 10
        px = lambda x, y: (30 + (x - X0) * S, 30 + (Z1 - y) * S)
        order = sorted(P, key=lambda b: b.c[2])           # low parts first
        proj = lambda b: [px(v[0], v[1]) for v in corners(b)]
    W = 60 + (X1 - X0) * S
    H = 90 + (Z1 - Z0) * S
    el = [f'<rect width="100%" height="100%" fill="#fff"/>',
          f'<text x="30" y="20" font-size="14" font-weight="700" fill="#1f2933">{title}</text>']
    for b in order:
        if b.group == "m1led":
            continue
        if b.group == "shell" and view == "top" and b.name not in ("Floor",):
            continue
        col = GRP_HI.get(b.group, COL.get(b.color, "#bbb"))
        if b.name.startswith("Battery pack"):
            col = "#e8b84a"
        if b.group == "shell":
            op, st = (0.35, "#6b7785")
        else:
            op, st = (0.75, "#1f2933")
        hp = hull2(proj(b))
        el.append('<polygon points="' + " ".join(f"{a:.1f},{c:.1f}" for a, c in hp) + f'" fill="{col}" fill-opacity="{op}" stroke="{st}" stroke-width="0.4"/>')
    if user_lines and view == "side":
        for pts, c in user_lines:
            el.append('<polyline points="' + " ".join(f"{px(a, b)[0]:.1f},{px(a, b)[1]:.1f}" for a, b in pts) + f'" fill="none" stroke="{c}" stroke-width="2.5"/>')
    # labels
    if view == "top":
        for b in P:
            if b.name in ("A1 audio board", "PW power", "Mini-ITX parts H5", "Battery pack 1", "R1 audio rear board", "R2 control rear board",
                          "Fan 60 x 60 x 15 (rear wall)", "P2 Grid", "Screen glass"):
                lab = {"Mini-ITX parts H5": "H5", "Battery pack 1": "АКБ", "A1 audio board": "A1", "PW power": "PW", "R1 audio rear board": "R1",
                       "R2 control rear board": "R2", "Fan 60 x 60 x 15 (rear wall)": "вент.", "P2 Grid": "P2 (пэды)", "Screen glass": "экран"}[b.name]
                X, Y = px(b.c[0], b.c[1])
                el.append(f'<text x="{X:.0f}" y="{Y:.0f}" font-size="12" font-weight="700" fill="#111" text-anchor="middle">{lab}</text>')
        X, Y = px(257, -32)
        el.append(f'<text x="{X:.0f}" y="{Y:.0f}" font-size="11" fill="#52606d" text-anchor="middle">перед (к музыканту)</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>{title}</title>' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, fname), "w", encoding="utf-8") as f:
        f.write(svg)


def eye(m):
    """Screen centre and viewing numbers; eye 300 mm in front of the lip edge, 430 mm above the table (doc 41, section 4)."""
    gs = m.s_of(365) + m.SCREEN_SHIFT
    cy = m.FOLD_Y + gs * math.cos(m.SLOPE) - 3 * math.sin(m.SLOPE)
    cz = m.FOLD_Z + gs * math.sin(m.SLOPE)
    ey, ez = -m.FL - 300, 430
    dy, dz = ey - cy, ez - cz
    el = math.degrees(math.atan2(dz, -dy))
    nel = 90 - math.degrees(m.SLOPE)
    return dict(screen_y_from_edge=round(cy + m.FL), screen_z=round(cz), dist=round(math.hypot(dy, dz)), eye_elev=round(el, 1),
                off_axis=round(nel - el, 1), glare_elev=round(90 - 2 * math.degrees(m.SLOPE), 1))


def profiles():
    """Outlines in one picture, x = mm from the front edge of the lip."""
    S = 1.4
    prof = [("сейчас: 22 / стенка 34 / 131, глубина 548", "#8a96a3", "6 4", [(0, 22), (345, 22), (345, 56), (348, 56), (478, 131), (548, 131)], 548),
            ("«оранжевая»: 22 / ступенька 9 / 131, глубина 543", "#e8731a", None, [(0, 22), (343, 22), (343, 31), (499, 131), (543, 131)], 543),
            ("«красная»: 32 без ступеньки / 131, глубина 528", "#d64545", None, [(0, 32), (328, 32), (484, 131), (528, 131)], 528)]
    W, H = 60 + 600 * S, 60 + 150 * S + 70
    P = lambda x, z: (30 + x * S, 40 + (140 - z) * S)
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="30" y="22" font-size="14" font-weight="700" fill="#1f2933">Профили сбоку: сейчас и по вашим линиям (из прогона модели)</text>']
    x0, y0 = P(-10, 0)
    x1, _ = P(570, 0)
    el.append(f'<line x1="{x0:.0f}" y1="{y0:.0f}" x2="{x1:.0f}" y2="{y0:.0f}" stroke="#1f2933" stroke-width="2"/>')
    for k, (lab, c, dash, pts, d) in enumerate(prof):
        pts = [(0, 0)] + pts + [(d, 0)]
        da = f' stroke-dasharray="{dash}"' if dash else ""
        el.append('<polyline points="' + " ".join(f"{P(a, b)[0]:.1f},{P(a, b)[1]:.1f}" for a, b in pts) + f'" fill="none" stroke="{c}" stroke-width="2.5"{da}/>')
        lx, ly = P(0, -14 - 12 * k)
        el.append(f'<text x="{lx:.0f}" y="{ly:.0f}" font-size="12" fill="{c}">— {lab}</text>')
    X, Y = P(286, 22 + 8.5)
    el.append(f'<rect x="{X:.0f}" y="{Y:.0f}" width="{38 * S:.0f}" height="{8.5 * S:.0f}" fill="#6b46c1" fill-opacity="0.6"/>')
    X, Y = P(305, 48)
    el.append(f'<text x="{X:.0f}" y="{Y:.0f}" font-size="11" fill="#6b46c1" text-anchor="middle">колесо (на деке 22)</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>Профили сбоку</title>' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_wedge_profiles.svg"), "w", encoding="utf-8") as f:
        f.write(svg)


def final_pack():
    import itertools  # noqa
    out = {}
    fsv = {"red": 0, "orange": 15}
    for nm, fs in fsv.items():
        rl, D = 453.4 + fs, 500 + fs
        h5y = D - 3 - 60 - 0.5
        if nm == "red":
            e = env(32, 32, fs, rl - 101, 6, "130,300,60,160,3", h5y)
        else:
            e = env(22, 31, fs, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5y)
        m0 = load(e, 0, 131)
        m = load(e, D - 3 - 41, 131, 30)
        P = corner_rework()(m, m.parts())
        out[nm] = (m, P)
    return out


if __name__ == "__main__" and os.environ.get("DRAW", "1") == "1":
    print("\n--- extra: lower rear with shorter rear boards (rows of jacks squeezed), red deck 32")
    for back, top in ((121, 100), (116, 95), (110, 90)):
        e = env(32, 32, 0, 352.4, 6, "130,300,60,160,3", 500 - 3 - 60.5)
        e.update(R1_TOP=top, R2_TOP=top, REAR_JACK_TOP=top + 4, REAR_JACK_TOP_R=top + 4)
        run(f"rear {back}, R1 / R2 top {top}", e, 500 - 3 - 41 - 300, back, 30, corner_rework(), show=8)
    pk = final_pack()
    # current final model for comparison
    mf = load(env(22, 56, 20, 365, 20, "40,210,365,465,3", 409.4, port="E") | dict(FAN="420,4,60", H5_REAR_X=410), 450.0, 131.0)
    lines = None
    for nm, (m, P) in pk.items():
        print(nm, "collisions:", len([1 for g, a, b, e in m.check(P) if g < -0.05]), eye(m))
        ttl = {"red": "«Красная»: дека 32, АКБ под пэдами, H5 в заднем углу",
               "orange": "«Оранжевая»: дека 22, ступенька 9, H5 в заднем углу"}[nm]
        draw(m, P, f"41_wedge_{nm}_side.svg", ttl + " (вид слева)", "side")
        draw(m, P, f"41_wedge_{nm}_top.svg", ttl + " (сверху)", "top")
    profiles()
    print("final", eye(mf))
    draw(mf, mf.parts(), "41_wedge_final_side.svg", "Сейчас: дека 22, стенка 34, сгиб 56, зад 131 (вид слева)", "side")
