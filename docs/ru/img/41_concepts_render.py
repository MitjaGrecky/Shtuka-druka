#!/usr/bin/env python3
"""Doc 41 section 20: three concepts "rear <= 120" for the main engineer (17.11.2026). Designer's numbers, to be checked
in the fit model by the main session. Reuses the scene of 41_final_render.py. Run: python 41_concepts_render.py"""
import importlib.util
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def fresh():
    spec = importlib.util.spec_from_file_location("fr", os.path.join(HERE, "41_final_render.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def build(m, deck, prof, fold_y, slope_end, screen=None, skip=(), center_s=None):
    m.DECK, m.STEP_Y, m.STEP_Z, m.CH = deck, fold_y, deck, 0.0
    m.SHELF_Y, m.BACK = slope_end
    m.SLOPE = math.atan2(slope_end[1] - deck, slope_end[0] - fold_y)
    m.PROFILE = prof
    m.D = prof[-2][0] if prof[-1][1] == 0 else prof[-1][0]
    if screen:
        m.SCREEN_X, m.SCREEN_G, m.SCREEN_A = screen
    m.SKIP_KINDS = skip
    if center_s is not None:
        m.SCREEN_SHIFT = center_s - m.s_of(365)
    m.FACES.clear()
    m.shell()
    m.controls()
    m.FACES[:] = [f for f in m.FACES if f[1] != (15, 15, 15)]
    for x in (32.0, 80.0):
        for r, col in ((7.5, (150, 155, 160)), (4.8, (12, 12, 12))):
            m.FACES.append(([(x + r * math.cos(a), -0.05 * (r < 5), 12 + r * math.sin(a)) for a in [2 * math.pi * i / 20 for i in range(20)]],
                            col, (0, -1, 0), 1, None))
    return m


if __name__ == "__main__":
    out = []
    # K1 low wedge: 28 deg, flat rear 113, rear jacks lying (strip z 3-50), H5 in the corner with its own rear I/O, USB/SD on the right side wall
    a = math.radians(28)
    z1 = 30 + 155.5 * math.tan(a)
    p1 = [(0, 0), (0, 27), (3, 30), (300, 30), (455.5, z1), (497, z1), (500, z1 - 3), (500, 0)]
    m = build(fresh(), 30, p1, 300, (455.5, z1), center_s=95)
    m.render(m.cam_34(), "41_concept_k1.svg", f"К1 «Низкий клин»: 28°, зад {z1:.0f}, глубина 500", 1.3,
             ("Красиво: один ровный клин от пэдов до кромки, зад ниже на 18 мм, порты — на боку, как у ноутбука, а не в кармане сверху.",
              "Ломает: R1 / R2 лёжа (полоса гнёзд z 3–50), W3 без деталей снизу над H5, карман USB / SD → правый бок (R81), угловые штекеры экрана."),
             inset=(p1, [("H5", (376, 496, 11, 55), "#d64545"), ("гнёзда", (455, 497, 3, 50), "#9fd3ad"), ("A1", (352, 452, 6, 28), "#3f9b5b")],
                    "К1 сбоку: дека 30 → 28° → зад 113"))
    # K2 bar screen: 12.3" 1920x720 (glass ~301 x 123, active 293 x 110, Waveshare wiki), 30 deg, rear ~96
    zt = 30 + 115 * math.tan(math.radians(30))
    p2 = [(0, 0), (0, 27), (3, 30), (300, 30), (415, zt), (497, zt), (500, zt - 3), (500, 0)]
    m = build(fresh(), 30, p2, 300, (415, zt), screen=(257.5, (301.2, 123.35), (293.1, 110.2)), skip=("meter",), center_s=66)
    m.render(m.cam_34(), "41_concept_k2.svg", f"К2 «Полоса»: экран 12,3″ 1920 × 720, 30°, зад {zt:.0f}", 1.3,
             ("Красиво: широкий экран-полоса во всю сетку и дорожки, как приборная панель; зад ниже на 35 мм; индикаторы уровня — на экране.",
              "Ломает: R150 (экран EP 10,1″), W2 Meters (огни → экран), R107 (8 столбцов на 293 мм, пересчёт), задние платы ≤ 85 или лёжа."),
             inset=(p2, [("H5", (376, 496, 11, 55), "#d64545"), ("A1", (352, 452, 6, 28), "#3f9b5b")], f"К2 сбоку: 30°, крыша {zt:.0f}"))
    # K3 ridge: front slope 32 deg to the crest y 440 z 117.5, back slope down to a low rear 55; H5 under the ridge
    zc = 30 + 140 * math.tan(math.radians(32))
    p3 = [(0, 0), (0, 27), (3, 30), (300, 30), (440, zc), (492, 55), (500, 55), (500, 0)]
    m = build(fresh(), 30, p3, 300, (440, zc), center_s=85)
    m.render(m.cam_34(), "41_concept_k3.svg", f"К3 «Конёк»: гребень {zc:.0f}, зад 55, глубина 500", 1.3,
             ("Красиво: сбоку треугольник, как пюпитр или крыло; ящика сзади нет совсем, сзади низкая полоса гнёзд, вентилятор на заднем скате.",
              "Ломает: R1 / R2 лёжа (полоса z 3–50), H5 впритык под гребнем (~0,6 мм над W3 — проверить), меньше объёма для тепла, сложнее оболочка."),
             inset=(p3, [("H5", (365, 485, 11, 55), "#d64545"), ("гнёзда", (455, 497, 3, 50), "#9fd3ad"), ("A1", (352, 452, 6, 28), "#3f9b5b")],
                    f"К3 сбоку: 32° вверх, 49° вниз к заду 55"))
    print("K1 rear", round(z1, 1), "K2 rear", round(zt, 1), "K3 crest", round(zc, 1))
