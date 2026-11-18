#!/usr/bin/env python3
"""Artifact "Штука Дрюка 3D v8": the three case variants from ONE source (model3d/fit/fit_model.py).
was    - the final model of 16.11.2026 (deck 22, 28 mm front overhang, step 56, depth 548);
orange - no overhang, deck 22, 3.5 mm jacks under P1, H5 in the rear right corner on 8 mm standoffs, slope 33 deg, depth 515;
green  - deck 30, 6.35 mm jacks under P1, battery under the pads, A1 on the floor, no step, depth 500.
Run: KiCad python (the model is only read; never kicad-cli).  Writes v8.html (template.html with the data inserted)."""
import importlib.util, json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "model3d", "fit"))
import low_case_final as F  # noqa: E402
import lower_case_study as L  # noqa: E402
spec = importlib.util.spec_from_file_location("ws", os.path.join(REPO, "docs", "ru", "img", "41_wedge_study.py"))
ws = importlib.util.module_from_spec(spec); spec.loader.exec_module(ws)


def rework_right(m, P0, h5c, y1):
    """Fan on the RIGHT wall (as R163), H5 against the rear wall and off the fan by 1 mm. Fan size/thickness from FAN_SPEC."""
    fs, ft = FAN_SPEC["s"], FAN_SPEC["T"]
    h5x1 = 512 - ft - 1.0
    h5x0 = h5x1 - 120.0
    keep = [p for p in P0 if p.name not in ("R2 control rear board, low arm", "Rear jacks", "Rear jacks (right)")]
    y0 = 413.4 + m.RS
    jt = m.REAR_JACK_TOP
    h0 = h5c - 60
    # R2 rev 0.7 (R178): no low arm, the tall part ends at R2_TALL_X1 (359)
    keep.append(m.box("Rear jacks (left)", "rear", 5, 359, y0 + 1.6, y1, 8, jt, color="metal", est=True))
    keep.append(m.box("Rear panel-mount jacks over the H5", "rear", h5x0, 510, y1 - 25, y1, 70, min(jt, 112), color="metal", est=True))
    keep.append(m.box("H5 harness room", "rear", h5x0, h5x1, h0 - 45, h0 - 25, 3.5, 26, color="plastic", est=True))
    keep.append(m.box(f"Fan {fs:g} x {fs:g} x {ft:g} (right wall)", "rear", 512 - ft, 512, h5c + FAN_SPEC["dy"] - fs / 2, h5c + FAN_SPEC["dy"] + fs / 2, FAN_SPEC["z0"], FAN_SPEC["z0"] + fs, color="plastic"))
    return keep


def rw_factory(jacks, fan="rear"):
    def rw(m, P0):
        if fan == "right":
            P = rework_right(m, P0, FAN_H5C["c"], m.D - m.SKIN)
        else:
            P = ws.corner_rework2(harness=HARNESS(m))(m, P0)
        S = m.SKIN
        P = [p for p in P if p.name not in ("Phones 1 jack", "Phones 2 jack", "F1 headphone board", "F1 headphone board parts below")]
        for p in list(P):
            if p.name == "P1 Left parts below":      # the real P1 has no bottom parts in the front 43 mm (checked on p1-left.kicad_pcb)
                lo = [c - h for c, h in zip(p.c, p.h)]; hi = [c + h for c, h in zip(p.c, p.h)]
                P.remove(p); P.append(m.box("P1 Left parts below (from y 43)", "panel", lo[0], hi[0], 43, hi[1], lo[2], hi[2], color="parts", est=True))
        if jacks == "3.5":
            for x in (32, 80):
                P.append(m.box(f"Phones jack 3.5 at x {x}", "front", x - 4.5, x + 4.5, 3.0, 16.0, S + 2.0, S + 7.5, color="metal", est=True))
            P.append(m.box("F1 small board", "front", 12, 102, 3.0, 38, S + 0.4, S + 2.0, color="pcb"))
            P.append(m.box("F1 relays 5.4", "front", 45, 70, 18, 36, S + 2.0, S + 7.4, color="parts", est=True))
            P.append(m.box("F1 low parts 2.5", "front", 72, 100, 18, 36, S + 2.0, S + 4.5, color="parts", est=True))
        else:
            for x in (32, 80):
                P.append(m.box(f"Phones jack 6.35 at x {x}", "front", x - 7.95, x + 7.95, 3.0, 30.0, S + 2.0, S + 14.7, color="metal", est=True))
            P.append(m.box("F1 small board", "front", 12, 102, 3.0, 40, S + 0.4, S + 2.0, color="pcb"))
            P.append(m.box("F1 relays 5.4", "front", 45, 70, 31, 40, S + 2.0, S + 7.4, color="parts", est=True))
        return P
    return rw


_H = {}
FAN_H5C = {}
FAN_SPEC = {"s": 60.0, "T": 15.0, "dy": 0.0, "z0": 6.0}      # fan on the right wall: size (square, mm) and thickness; the H5 stands 1 mm off the fan
def HARNESS(m):
    return _H["h"]


def profile(m):
    """Side profile (y, z) of the outer shell: front wall, deck, step, slope, roof / ridge, rear wall (for the solid view)."""
    y0 = -m.FL
    pts = [(y0, 0), (y0, m.TOP_Z), (m.FOLD_Y, m.TOP_Z)]
    if m.FOLD_Z > m.TOP_Z + 0.5:
        pts.append((m.FOLD_Y, m.FOLD_Z))
    if getattr(m, "RIDGE", None):
        pass
    pts += [(m.SHELF_Y, m.BACK_Z)]
    pts += [(m.D, m.BACK_Z), (m.D, 0)]
    return [[round(a, 1), round(b, 1)] for a, b in pts]


def variant_data(m, P, name, note, extra):
    res = m.check(P)
    tight = [dict(gap=round(g, 1), a=a, b=b) for g, a, b, e in res if g < 1.0 and "harness room" not in a + b]
    col = [t for t in tight if t["gap"] < -0.05]
    parts = []
    for p in P:
        g = "clear" if "harness room" in p.name else p.group
        parts.append(dict(n=p.name, g=g, c=[round(x, 2) for x in p.c], s=[round(2 * h, 2) for h in p.h], rx=round(p.rx, 3), col=p.color, sh=p.shape, est=bool(p.est)))
    dims = [["Дека с пэдами", f"{m.TOP_Z:g}"], ["Свес спереди", f"{m.FL:g}"], ["Скат экрана", f"{math.degrees(m.SLOPE):.1f}°"],
            ["Зад (высота)", f"{m.BACK_Z:g}"], ["Глубина", f"{m.D + m.FL:g}"], ["Ширина", "515"], ["Столкновений (> 0,05 мм)", str(len(col))]] + extra
    prof = profile(m)
    return dict(name=name, note=note, profile=prof, parts=parts, tight=[dict(gap=t["gap"], a=t["a"], b=t["b"]) for t in tight if t["gap"] >= -0.05], dims=dims)


def load_was():
    env = F.config(40, fs=20); env["FRONT_Z"] = 56.0
    for k in L.KEYS: os.environ.pop(k, None)
    os.environ.update({k: str(v) for k, v in env.items()})
    sp = importlib.util.spec_from_file_location("fm_was", os.path.join(REPO, "model3d", "fit", "fit_model.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m, m.parts()


def build_wedge(deck, ang, jacks, h5st=8, roof=41, fs=0, fan="rear"):
    rl, D = 453.4 + fs, 500 + fs
    h5y = D - 3 - 15 - 60 - 0.5 if fan == "rear" else D - 3 - 60 - 0.5
    FAN_H5C["c"] = h5y
    if deck >= 28:
        e = ws.env(deck, deck, fs, rl - 101, 6, "130,300,60,160,3", h5y, h5_st=h5st)
    else:
        e = ws.env(22, 31, fs, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5y, h5_st=h5st)
    e.update(FRONT_LIP=0)
    if fan == "right":
        e.update(H5_REAR_X=436)
    run_len = D - 3 - roof - (300 + fs)
    back = round((deck if deck >= 28 else 31) + run_len * math.tan(math.radians(ang)), 1)
    m = ws.load(e, D - 3 - roof, back, 30)
    _H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    return m, rw_factory(jacks, fan)(m, m.parts())


def main():
    V = {}
    m, P = load_was()
    V["was"] = variant_data(m, P, "Было (548)", "Итоговая модель на 16.11.2026: дека 22, передний свес 28 мм под плату наушников, ступенька со стенкой 34 мм, сгиб 56, скат 30°, аккумулятор на подносе под A1.",
                            [["Гнёзда наушников", "6,35 мм в свесе"], ["Аккумулятор", "на полу под A1"], ["H5", "справа, порты вправо"]])
    m, P = build_wedge(22, 33, "3.5", fan="right")
    V["orange"] = variant_data(m, P, "Оранжевая (515)", "Без свеса: гнёзда 3,5 мм в передней стенке, плата F1 ≈ 90 × 35 на полу под передним краем P1. Ступенька 9 мм, скат 33°. Вентилятор перенесён на ПРАВУЮ стенку (как R163), поэтому H5 стоит вплотную к задней стенке, на 15 мм левее правой (x 376–496); плечо R2 до x 373. Столкновений нет.",
                            [["Гнёзда наушников", "3,5 мм угловые"], ["Аккумулятор", "на полу под A1 (поднос)"], ["H5", "у задней стенки, порты вперёд"], ["Вентилятор", "на правой стенке"]])
    m, P = build_wedge(30, 33, "6.35", fan="right")
    V["green"] = variant_data(m, P, "Зелёная (500)", "Дека 30: гнёзда 6,35 мм под передним краем P1 (без свеса), аккумулятор под пэдами (1–2 пакета), A1 на полу, скат 33° от деки без ступеньки. Вентилятор на правой стенке, H5 вплотную к задней стенке (x 376–496), плечо R2 до x 373. Столкновений нет. Колесо пока на y 277: 4 мм до начала ската, дизайнер просит 268 (решение за вами).",
                            [["Гнёзда наушников", "6,35 мм под P1"], ["Аккумулятор", "под пэдами"], ["H5", "у задней стенки, порты вперёд"], ["Вентилятор", "на правой стенке"]])
    spec_c = importlib.util.spec_from_file_location("cs", os.path.join(REPO, "docs", "ru", "img", "41_crest_study.py"))
    cs = importlib.util.module_from_spec(spec_c); spec_c.loader.exec_module(cs)
    m, P, _, _ = cs.build_pw(30, 10, 120, 20, 245, "6.35")
    P = cs.angled(P, m)
    V["g2"] = variant_data(m, P, "Зелёная-2 (510)", "Набросок пользователя: макушка ниже (120), весь задник (гнёзда, H5, вентилятор справа) сдвинут назад на 10 мм, конец ската на передней кромке коробки задних гнёзд (y 463), скат 28,8°, экран на 20 мм выше по скату. Столкновений и касаний < 1 мм нет, но только с УГЛОВЫМИ (90°) штекерами HDMI и USB-C у экрана (изгибы кабелей убраны, допущение, нужны покупные штекеры ≤ 12 мм за платой драйвера: наличие не проверено). Без них остаются петли кабелей экрана о PW (12,1 и 5,3 мм).",
                           [["Гнёзда наушников", "6,35 мм под P1"], ["Аккумулятор", "под пэдами"], ["H5", "у задней стенки, порты вперёд"], ["Вентилятор", "на правой стенке"], ["Штекеры экрана", "угловые 90° (допущение)"]])
    import g3
    m, P, _c, _t = g3.build(30, 0, 117.0, 20, 0)
    V["g3"] = variant_data(m, P, "Зелёная-2 сжатая (500)", "Пересборка по вашему наброску: дека 30; два аккумулятора под P2 (отсеки по 106 × 220 × 11 мм, зазор 1,4 мм до деталей P2, 1 мм по краям); макушка 117 мм вплотную к плате R2 (её верх 113 + обшивка 3 + зазор 1); скат 33,1° кончается на 20 мм раньше передней кромки коробки гнёзд; задник не сдвигается (глубина 500); вентилятор 80 × 80 × 25 мм на правой стенке (R182), H5 у задней стенки; щели в полу под обоими аккумуляторами (24 щели 4 × 40 мм) и ножки 5 мм; угловые штекеры у экрана (принято). Перебор 1 600 вариантов: ниже 117 мм не проходит, глубже 500 не нужно. Все зазоры не меньше 1 мм.",
                           [["Гнёзда наушников", "6,35 мм под P1"], ["Аккумуляторы", "2 отсека 106 × 220 × 11, ≈ 148 Вт·ч (оценка)"], ["H5", "у задней стенки, порты вперёд"], ["Вентилятор", "80 × 80 × 25 на правой стенке"], ["Вентиляция", "24 щели 4 × 40 мм в полу + ножки 5 мм"], ["Штекеры экрана", "угловые 90° (принято)"], ["Зазоры", "все ≥ 1 мм"]])
    V = {"g3": V["g3"]}   # 17.11.2026 (user): only the main line stays; "was" is the hidden reference of the red contour
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    # data for the solid ("glukhoy") mode, the same sources as the v7 page: layout_v7.json elements and the element descriptions (INFO)
    import runpy, tempfile
    lay = json.load(open(os.path.join(REPO, "mockup", "layout", "layout_v7.json"), encoding="utf-8"))
    cwd = os.getcwd(); tmp = tempfile.mkdtemp(); os.chdir(tmp)
    try:
        g7 = runpy.run_path(os.path.join(REPO, "model3d", "build_model3d_v7.py"))
    finally:
        os.chdir(cwd)
    info7 = g7["info"]
    tpl = tpl_pre = None
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    tpl = tpl.replace("/*LAYOUT*/", json.dumps({k: lay[k] for k in ("W", "D", "F0", "F1")} | {"E": lay["elements"]}, ensure_ascii=False, separators=(",", ":")))
    tpl = tpl.replace("/*INFO*/", json.dumps(info7, ensure_ascii=False, separators=(",", ":")))
    out = tpl.replace("__VARIANTS__", json.dumps(V, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(HERE, "v8.html"), "w", encoding="utf-8").write(out)
    for k, v in V.items():
        print(k, len(v["parts"]), "parts", len(v["tight"]), "tight", [d for d in v["dims"] if d[0].startswith("Столк")])
    print("v8.html", len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
