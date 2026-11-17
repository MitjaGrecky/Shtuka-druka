#!/usr/bin/env python3
"""Doc 41 section 19: the user's "green" line (17.11.2026) as sketches, by the main engineer's run
(model3d/fit/chain_study.py): deck 30, no lip, no step (slope from y 300 = 4 mm behind the wheel), slope 33 deg, rear 131,
depth 500; 6.35 mm Cliff jacks under the front of P1, battery under P2, A1 on the floor (z 6-28), H5 in the rear right corner.
Reuses the scene code of 41_final_render.py with other numbers. Run: python 41_green_render.py"""
import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("fr", os.path.join(HERE, "41_final_render.py"))
fr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fr)

DECK, FOLD_Y, BACK, ANG, D = 30.0, 300.0, 131.0, 33.0, 500.0
SHELF = FOLD_Y + (BACK - DECK) / math.tan(math.radians(ANG))
fr.D, fr.DECK, fr.STEP_Y, fr.STEP_Z, fr.CH = D, DECK, FOLD_Y, DECK, 0.0
fr.SHELF_Y, fr.BACK = SHELF, BACK
fr.SLOPE = math.atan2(BACK - DECK, SHELF - FOLD_Y)
fr.PROFILE = [(0, 0), (0, DECK - 3), (3, DECK), (FOLD_Y, DECK), (SHELF, BACK), (D - 3, BACK), (D, BACK - 3), (D, 0)]
h5y0 = D - 3 - 120
fr.interior = lambda: [("H5", (376, 496, h5y0, h5y0 + 120, 11, 55), "#d64545"), ("вент.", (497, 512, h5y0 + 30, h5y0 + 90, 6, 66), "#8a96a3"),
                       ("A1", (20, 240, 352, 452, 6, 28), "#3f9b5b"), ("АКБ", (130, 300, 60, 160, 3, 17), "#e8b84a"),
                       ("PW", (245, 345, 360, 440, 6, 25), "#3f9b5b"), ("F1 + 6,35", (15, 105, 3, 40, 3, 17), "#3f9b5b"),
                       ("R1 / R2", (4, 373, 453, 455, 8, 113), "#3f9b5b")]

if __name__ == "__main__":
    fr.FACES.clear()
    fr.shell()
    fr.controls()
    fr.FACES[:] = [f for f in fr.FACES if f[1] != (15, 15, 15)]          # drop the 3.5 mm jacks of the orange sketch
    for x in (32.0, 80.0):                                                # 6.35 mm Cliff jacks: nut ring and hole
        for r, col in ((7.5, (150, 155, 160)), (4.8, (12, 12, 12))):
            fr.FACES.append(([(x + r * math.cos(a), -0.05 * (r < 5), 12 + r * math.sin(a)) for a in [2 * math.pi * i / 20 for i in range(20)]],
                             col, (0, -1, 0), 1, None))
    notes = ("Условности: как в разделе 18 (скругления светом, ручки — призмы, картинка экрана условная).",
             "Числа — прогон главного инженера (chain_study.py): дека 30, скат 33°, зад 131, глубина 500; гнёзда 6,35 мм под P1.")
    fr.render(fr.cam_34(), "41_green_34.svg", "«Зелёная»: дека 30, без ступеньки, 500 × 515 × 131 — вид 3/4 (эскиз)", 1.45, notes)
    fr.render(fr.cam_side(), "41_green_side.svg", "«Зелёная», вид слева, узлы внутри пунктиром", 1.35,
              ("АКБ под пэдами (P2), A1 на полу, H5 вплотную к задней стенке, вентилятор на правой стенке, гнёзда 6,35 мм на передней стенке под P1.",),
              dims=[("h", (0, 0, -12), (0, D, -12), "500"), ("v", (0, D + 8, 0), (0, D + 8, BACK), "131"),
                    ("v", (0, -10, 0), (0, -10, DECK), "30"), ("h", (0, SHELF, BACK + 10), (0, D, BACK + 10), f"{D - SHELF:.0f}"),
                    ("h", (0, FOLD_Y + 40, DECK + 50), (0, FOLD_Y + 40, DECK + 50), f"{ANG:.0f}°")], inside=True)
    # was -> orange -> green, one scale
    S = 1.35
    profs = [("было: 548 × 515, губа + дека 22, стенка 34, зад 131", "#8a96a3", "7 4",
              [(0, 0), (0, 22), (345, 22), (345, 56), (348, 56), (478, 131), (548, 131), (548, 0)]),
             ("«оранжевая»: 515, дека 22, ступенька 9, скат 33°, зад 131", "#e8731a", None,
              [(0, 0), (0, 22), (315, 22), (315, 27), (319, 31), (471, 131), (515, 131), (515, 0)]),
             ("«зелёная»: 500, дека 30, без ступеньки, скат 33°, зад 131", "#2f9e5b", None,
              [(0, 0), (0, 30), (300, 30), (SHELF, 131), (500, 131), (500, 0)])]
    Wd, Hd = 60 + 600 * S, 90 + 150 * S + 70
    P = lambda y, z: (30 + y * S, 40 + (140 - z) * S)
    el = ['<rect width="100%" height="100%" fill="#fff"/>',
          '<text x="30" y="26" font-size="16" font-weight="700" fill="#1f2933">Было → «оранжевая» → «зелёная», один масштаб (вид сбоку)</text>']
    for k, (lab, col, dash, pts) in enumerate(profs):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        el.append('<polyline points="' + " ".join(f"{P(y, z)[0]:.1f},{P(y, z)[1]:.1f}" for y, z in pts) + f'" fill="none" stroke="{col}" stroke-width="2.5"{da}/>')
        el.append(f'<text x="30" y="{40 + 150 * S + 24 + 16 * k:.0f}" font-size="12" fill="{col}">— {lab}</text>')
    X, Y = P(286, 30 + 8.5)
    el.append(f'<rect x="{X:.0f}" y="{Y:.0f}" width="{38 * S:.0f}" height="{8.5 * S:.0f}" fill="#6b46c1" fill-opacity="0.5"/>')
    X, Y = P(305, 52)
    el.append(f'<text x="{X:.0f}" y="{Y:.0f}" font-size="11" fill="#6b46c1" text-anchor="middle">колесо</text>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd:.0f} {Hd:.0f}" width="{Wd:.0f}" height="{Hd:.0f}" '
           f'font-family="Segoe UI, Arial, sans-serif"><title>Было, оранжевая, зелёная</title>' + "".join(el) + "</svg>")
    open(os.path.join(HERE, "41_green_compare.svg"), "w", encoding="utf-8").write(svg)
    print("shelf", round(SHELF, 1), "roof", round(D - SHELF, 1))
