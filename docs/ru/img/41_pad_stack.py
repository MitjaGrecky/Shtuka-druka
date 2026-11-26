#!/usr/bin/env python3
"""Doc 41 section 24.15: pad stack for the 4x4 test board (R194): layers, heights, three pad forms. Designer's concept.

Sources: z of the board and deck from the production model g3.build(30, 0, 117, 20, 0) (designer/runs/pad_stack_model.txt:
P2 board z 18.9-20.5, top skin z 27-30, standoffs 20.5-27, pad cap in the model z 30.2-33.2); pad 25.5 x 21, pitch 28 x 25
(doc 27 section 4); light hole 3-4 mm (R194); tape 0.05-0.1 and XactFSR ~0.13 mm (user's research via the chief engineer,
NOT checked against the Interlink datasheet); Sorta-Clear 40, Shore 40A (Smooth-On SORTA-Clear Series TB, datasheets/smoothon_sorta_clear.pdf).
ASSUMPTION (designer): comb field of one pad 21 x 17 mm (the test board layout does not exist yet; electrodes are placeholders).
Views: section A-A through the pad centre along x (across the row), seen from the FRONT (musician), z up from the outer floor,
mm; and each foot seen from BELOW (from the board), x to the right as seen from the front, i.e. mirrored left-right against a
top view. Status: concept. Run: python 41_pad_stack.py -> 41_pad_stack.svg / .csv (and prints the table)."""
import math, os
HERE = os.path.dirname(os.path.abspath(__file__))

PCB0, PCB1 = 18.9, 20.5            # P2 board (model)
DECK0, DECK1 = 27.0, 30.0          # top skin (model)
TAPE = (0.05, 0.10)                # spacer tape frame
FILM = 0.13                        # XactFSR (research, unverified)
TOP = 33.0                         # pad top: 3.0 above the deck (model cap 30.2-33.2)
PAD_X, PAD_Y, PITCH = 25.5, 21.0, (28.0, 25.0)
GAP = 0.4                          # pad-to-deck-opening clearance per side
WEB = 1.2                          # silicone mat web under the deck, its top against the deck underside
PRELOAD = 0.15                     # foot interference on the film (no dead zone)
COMB = (21.0, 17.0)                # ASSUMPTION
FOOT = (COMB[0] - 2, COMB[1] - 2)  # 1 mm inside the comb field on each side
RELIEF = 6.0                       # light relief around the 3-4 mm hole (film hole 5)
SHORE = 40.0


def gent_E(s):                     # Gent (1958): Young's modulus from Shore A, MPa (estimate)
    return 0.0981 * (56 + 7.62336 * s) / (0.137505 * (254 - 2.54 * s))


def foot_area(kind, step=0.02):
    fx, fy = FOOT
    n = 0
    for i in range(int(fx / step)):
        x = -fx / 2 + (i + .5) * step
        for j in range(int(fy / step)):
            y = -fy / 2 + (j + .5) * step
            if math.hypot(x, y) < RELIEF / 2: continue
            if kind == "V2" and abs(x) < fx / 2 - 2 and abs(y) < fy / 2 - 2: continue      # ring 2 mm wide
            if kind == "V3" and (abs(x) < 1 or abs(y) < 1): continue                      # cross slot 2 mm
            n += 1
    return n * step * step


def main():
    E = gent_E(SHORE)
    film_top = [PCB1 + t + FILM for t in TAPE]
    web0 = DECK0 - WEB
    rows = []
    for kind, name in (("V1", "Монолит"), ("V2", "Колпак"), ("V3", "Четыре зоны")):
        A = foot_area(kind)
        foot_len = web0 - film_top[1] + PRELOAD
        d10 = 10.0 / (E * A) * foot_len            # N/(MPa*mm2)*mm = mm, foot column only
        rows.append((kind, name, round(A, 1), round(1 / A * 1000, 2), round(10 / A * 1000, 1), round(d10, 3)))
    total = TOP - film_top[1]
    open_x, open_y = PAD_X + 2 * GAP, PAD_Y + 2 * GAP
    print(f"E(40A) ~ {E:.2f} MPa; film top z {film_top[0]:.2f}-{film_top[1]:.2f}; pad height {total:.2f} (+{PRELOAD} preload); "
          f"foot length {web0 - film_top[1]:.2f}; deck opening {open_x:.1f} x {open_y:.1f}, webs {PITCH[0] - open_x:.1f} / {PITCH[1] - open_y:.1f}")
    for r in rows: print(r)

    # ---------- drawing ----------
    K = 13.0
    CW = 28 * K + 40
    W, H = int(3 * CW + 40 + 230), 800
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="20" y="30" font-size="18" font-weight="700" fill="#1f2933">Стек пэда для тестовой платы 4 × 4 (R194): разрез и три формы (концепт дизайнера, 21.11.2026)</text>',
          '<text x="20" y="52" font-size="12" fill="#52606d">Разрез A-A через центр пэда поперёк ряда, вид спереди (от музыканта), z от низа корпуса, мм, 1 мм = 13 px. z платы и деки — боевая модель g3.</text>',
          '<text x="20" y="70" font-size="12" fill="#52606d">Снизу — ножка пэда, вид СНИЗУ (со стороны платы): зеркально к виду сверху. Пунктир — поле гребёнок 21 × 17 (допущение), кружок — отверстие света 3–4 мм.</text>']
    Z0, Z1 = 18.0, 34.0
    for v, (kind, name, A, p1, p10, d10) in enumerate(rows):
        ox = 20 + v * CW
        oy = 95
        T = lambda x, z: (ox + 20 + (x + 14) * K, oy + 30 + (Z1 - z) * K)
        el.append(f'<text x="{ox + 20}" y="{oy + 14}" font-size="15" font-weight="700" fill="#1f2933">{kind}. {name}</text>')
        def rect(x0, z0, x1, z1, fill, stroke="none", sw=0.8, op=1):
            a, b = T(x0, z1), T(x1, z0)
            el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{max(b[1] - a[1], 1.2):.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{op}"/>')
        def poly(pts, fill, stroke="#1d6b58", sw=1.0):
            el.append('<polygon points="' + " ".join("%.1f,%.1f" % T(x, z) for x, z in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        # board, combs, tape, film
        rect(-14, PCB0, 14, PCB1, "#2f6f4f")
        rect(-COMB[0] / 2, PCB1 - 0.05, COMB[0] / 2, PCB1, "#d4af37")
        rect(-COMB[0] / 2 - 1.5, PCB1, -COMB[0] / 2, PCB1 + TAPE[1], "#c9b27c"); rect(COMB[0] / 2, PCB1, COMB[0] / 2 + 1.5, PCB1 + TAPE[1], "#c9b27c")
        rect(-COMB[0] / 2 - 1.5, PCB1 + TAPE[1], COMB[0] / 2 + 1.5, film_top[1], "#7a6a52")
        rect(-2.0, PCB0, 2.0, film_top[1], "#fff7cc")                     # light hole through board and film (Ø 4)
        # deck skin with the opening
        ox_half = PAD_X / 2 + GAP
        rect(-14, DECK0, -ox_half, DECK1, "#3a3f45"); rect(ox_half, DECK0, 14, DECK1, "#3a3f45")
        # pad silhouette (section): top chamfer 0.8, body through the deck, web under the deck, foot
        fx = FOOT[0] / 2
        c = 0.8
        body = [(-PAD_X / 2, DECK0), (-PAD_X / 2, TOP - c), (-PAD_X / 2 + c, TOP), (PAD_X / 2 - c, TOP), (PAD_X / 2, TOP - c), (PAD_X / 2, DECK0)]
        sil = "#cfe8e1"
        web = [(-14, web0), (-14, DECK0), (14, DECK0), (14, web0)]
        poly(web, sil)
        poly(body, sil)
        if kind == "V1":
            poly([(-fx, film_top[1]), (-fx, web0), (fx, web0), (fx, film_top[1]), (RELIEF / 2, film_top[1]), (RELIEF / 2, film_top[1] + 0.8),
                  (-RELIEF / 2, film_top[1] + 0.8), (-RELIEF / 2, film_top[1])], sil)
        elif kind == "V2":
            poly([(-fx, film_top[1]), (-fx, web0), (fx, web0), (fx, film_top[1]), (fx - 2, film_top[1]), (fx - 2, TOP - 2.0), (-fx + 2, TOP - 2.0), (-fx + 2, film_top[1])], sil)
            rect(-PAD_X / 2 + 1.5, DECK0, -fx, TOP - 2.0, "#ffffff", op=0)   # (outline only)
            # hollow inside the body above the web
            poly([(-fx + 2, web0), (-fx + 2, TOP - 2.0), (fx - 2, TOP - 2.0), (fx - 2, web0)], "#ffffff", stroke="#1d6b58", sw=0.6)
        else:
            poly([(-fx, film_top[1]), (-fx, web0), (fx, web0), (fx, film_top[1]), (1, film_top[1]), (1, film_top[1] + 0.8), (-1, film_top[1] + 0.8), (-1, film_top[1])], sil)
        # light cone
        a, b = T(0, PCB0 - 0.3), T(0, TOP)
        el.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#f2b705" stroke-width="1.4" stroke-dasharray="4 3"/>')
        # z labels on the first panel
        if v == 2:
            for z, lab in ((TOP, "33,0 верх пэда (+3 над декой)"), (DECK1, "30,0 дека"), (DECK0, "27,0 низ обшивки"), (web0, f"{web0:.1f} перемычка коврика".replace(".", ",")),
                           (film_top[1], f"{film_top[1]:.2f} плёнка XactFSR".replace(".", ",")), (PCB1, "20,5 верх платы, гребёнки"), (PCB0, "18,9 низ платы")):
                p = T(14, z)
                el.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{p[0] + 30:.1f}" y2="{p[1]:.1f}" stroke="#9aa5b1"/>')
                el.append(f'<text x="{p[0] + 34:.1f}" y="{p[1] + 4 - (9 if 'плёнка' in lab else 0) + (5 if 'верх платы' in lab else 0):.1f}" font-size="11" fill="#1f2933">{lab}</text>')
        # bottom view of the foot
        by = oy + 30 + (Z1 - Z0) * K + 40
        B = lambda x, y: (ox + 20 + (x + 14) * K, by + (12.5 - y) * K)
        a, b = B(-PAD_X / 2, PAD_Y / 2), B(PAD_X / 2, -PAD_Y / 2)
        el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="#eef6f3" stroke="#9aa5b1" stroke-dasharray="2 2"/>')
        a, b = B(-COMB[0] / 2, COMB[1] / 2), B(COMB[0] / 2, -COMB[1] / 2)
        el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="none" stroke="#b8860b" stroke-width="1.2" stroke-dasharray="5 3"/>')
        fx, fy = FOOT[0] / 2, FOOT[1] / 2
        def frect(x0, y0, x1, y1, fill="#5fa894"):
            a, b = B(x0, y1), B(x1, y0)
            el.append(f'<rect x="{a[0]:.1f}" y="{a[1]:.1f}" width="{b[0] - a[0]:.1f}" height="{b[1] - a[1]:.1f}" fill="{fill}"/>')
        if kind == "V1":
            frect(-fx, -fy, fx, fy)
        elif kind == "V2":
            frect(-fx, -fy, fx, fy); frect(-fx + 2, -fy + 2, fx - 2, fy - 2, "#eef6f3")
        else:
            for sx in (-1, 1):
                for sy in (-1, 1):
                    frect(min(sx, sx * fx), min(sy, sy * fy), max(sx, sx * fx), max(sy, sy * fy))
        c = B(0, 0)
        el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{RELIEF / 2 * K:.1f}" fill="#eef6f3" stroke="#5fa894"/>')
        el.append(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{2.0 * K:.1f}" fill="#fff7cc" stroke="#f2b705"/>')
        ty = by + 25 * K + 22
        for i, t in enumerate((f"ножка {FOOT[0]:g} × {FOOT[1]:g}, площадь {str(A).replace('.', ',')} мм²",
                               f"давление: 1 Н → {str(p1).replace('.', ',')} кПа, 10 Н → {str(p10).replace('.', ',')} кПа",
                               f"сжатие ножки при 10 Н ≈ {str(d10).replace('.', ',')} мм (40A, E ≈ {E:.1f} МПа, оценка)".replace(".", ",", 1))):
            el.append(f'<text x="{ox + 20}" y="{ty + i * 17}" font-size="11.5" fill="#1f2933">{t}</text>')
    el.append(f'<text x="20" y="{H - 14}" font-size="11" fill="#52606d">Слои снизу вверх: плата 1,6 (z 18,9–20,5) · рамка-скотч 0,05–0,1 · XactFSR ≈ 0,13 · силикон Sorta-Clear (коврик: перемычка ' + f'{WEB:g}'.replace('.', ',') + ' под декой, ножка, тело, +3 над декой). Отверстие в деке ' + f'{open_x:.1f} × {open_y:.1f}'.replace('.', ',') + '.</text>')
    open(os.path.join(HERE, "41_pad_stack.svg"), "w", encoding="utf-8").write(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Segoe UI, Arial, sans-serif">' + "".join(el) + "</svg>")
    with open(os.path.join(HERE, "41_pad_stack.csv"), "w", encoding="utf-8") as f:
        f.write("variant,name,foot_area_mm2,p_1N_kPa,p_10N_kPa,foot_compression_10N_mm\n")
        for r in rows: f.write(",".join(str(x) for x in r) + "\n")
    print(W, H)


if __name__ == "__main__":
    main()
