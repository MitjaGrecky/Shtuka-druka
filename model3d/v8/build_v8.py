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


def rw_factory(jacks):
    def rw(m, P0):
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
def HARNESS(m):
    return _H["h"]


def variant_data(m, P, name, note, extra):
    res = m.check(P)
    tight = [dict(gap=round(g, 1), a=a, b=b) for g, a, b, e in res if g < 1.0]
    col = [t for t in tight if t["gap"] < -0.05]
    parts = []
    for p in P:
        g = "clear" if "harness room" in p.name else p.group
        parts.append(dict(n=p.name, g=g, c=[round(x, 2) for x in p.c], s=[round(2 * h, 2) for h in p.h], rx=round(p.rx, 3), col=p.color, sh=p.shape, est=bool(p.est)))
    dims = [["Дека с пэдами", f"{m.TOP_Z:g}"], ["Свес спереди", f"{m.FL:g}"], ["Скат экрана", f"{math.degrees(m.SLOPE):.1f}°"],
            ["Зад (высота)", f"{m.BACK_Z:g}"], ["Глубина", f"{m.D + m.FL:g}"], ["Ширина", "515"], ["Столкновений (> 0,05 мм)", str(len(col))]] + extra
    return dict(name=name, note=note, parts=parts, tight=[dict(gap=t["gap"], a=t["a"], b=t["b"]) for t in tight if t["gap"] >= -0.05], dims=dims)


def load_was():
    env = F.config(40, fs=20); env["FRONT_Z"] = 56.0
    for k in L.KEYS: os.environ.pop(k, None)
    os.environ.update({k: str(v) for k, v in env.items()})
    sp = importlib.util.spec_from_file_location("fm_was", os.path.join(REPO, "model3d", "fit", "fit_model.py"))
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m, m.parts()


def build_wedge(deck, ang, jacks, h5st=8, roof=41, fs=0):
    rl, D = 453.4 + fs, 500 + fs
    h5y = D - 3 - 15 - 60 - 0.5
    if deck >= 28:
        e = ws.env(deck, deck, fs, rl - 101, 6, "130,300,60,160,3", h5y, h5_st=h5st)
    else:
        e = ws.env(22, 31, fs, rl - 101, 20, f"40,210,{rl - 101},{rl - 1},3", h5y, h5_st=h5st)
    e.update(FRONT_LIP=0)
    run_len = D - 3 - roof - (300 + fs)
    back = round((deck if deck >= 28 else 31) + run_len * math.tan(math.radians(ang)), 1)
    m = ws.load(e, D - 3 - roof, back, 30)
    _H["h"] = (391, 511, h5y - 60 - 45, h5y - 60 - 25, 3.5, 26)
    return m, rw_factory(jacks)(m, m.parts())


def main():
    V = {}
    m, P = load_was()
    V["was"] = variant_data(m, P, "Было (548)", "Итоговая модель на 16.11.2026: дека 22, передний свес 28 мм под плату наушников, ступенька со стенкой 34 мм, сгиб 56, скат 30°, аккумулятор на подносе под A1.",
                            [["Гнёзда наушников", "6,35 мм в свесе"], ["Аккумулятор", "на полу под A1"], ["H5", "справа, порты вправо"]])
    m, P = build_wedge(22, 33, "3.5")
    V["orange"] = variant_data(m, P, "Оранжевая (515)", "Без свеса: гнёзда 3,5 мм в передней стенке, плата F1 ≈ 90 × 35 на полу под передним краем P1. Ступенька 9 мм, скат 33°, H5 в заднем правом углу на стойках 8 мм, вентилятор на задней стенке. Остаются 4 известных столкновения: карман USB/SD и платы W3 о H5 (до 2,8 мм); лечится сдвигом кармана по скату вперёд.",
                            [["Гнёзда наушников", "3,5 мм угловые"], ["Аккумулятор", "на полу под A1 (поднос)"], ["H5", "в заднем углу, порты вперёд"]])
    m, P = build_wedge(30, 33, "6.35")
    V["green"] = variant_data(m, P, "Зелёная (500)", "Дека 30: гнёзда 6,35 мм под передним краем P1 (без свеса), аккумулятор под пэдами (1–2 пакета), A1 на полу, скат 33° от деки без ступеньки, H5 в заднем углу. Колесо пока на y 277: 4 мм до начала ската, дизайнер просит 268 (решение за вами). Остаются известные столкновения: карман USB/SD и платы W3 о H5 (до 3,8 мм), 1 мм детали W3 о зону жгутов.",
                            [["Гнёзда наушников", "6,35 мм под P1"], ["Аккумулятор", "под пэдами"], ["H5", "в заднем углу, порты вперёд"]])
    tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
    out = tpl.replace("__VARIANTS__", json.dumps(V, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(HERE, "v8.html"), "w", encoding="utf-8").write(out)
    for k, v in V.items():
        print(k, len(v["parts"]), "parts", len(v["tight"]), "tight", [d for d in v["dims"] if d[0].startswith("Столк")])
    print("v8.html", len(out) // 1024, "KB")


if __name__ == "__main__":
    main()
