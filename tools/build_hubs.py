#!/usr/bin/env python3
"""Строит тематические хабы документации docs/ru/hub/*.md из карты docs/ru/README.md и индексов разбитых документов.

Хаб = короткий список «тема → файл» (одна строка на часть документа). Агент читает хаб своей темы (1–3 КБ) и открывает только нужную часть.
Не правит документы. Запуск: python tools/build_hubs.py   (результат docs/ru/hub/, в начале каждого файла пометка «сгенерировано»).
Источники: строки таблицы карты `| NN | [Название](файл.md) | блок1, блок2 | описание |` и таблицы частей `| [имя](папка/файл.md) | заголовок | КБ |`.
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs" / "ru"
HUB = DOCS / "hub"
DOMAINS = {
    "01_project": "Проект: цели, лицензии, этапы, рынок",
    "02_controls": "Управление: кнопки, режимы, навигация, запись",
    "03_panel": "Панель и экран: раскладка v7, ручки, пэды, подсветка",
    "04_enclosure": "Корпус, форма, размеры, посадка деталей, внешний вид",
    "05_io": "Разъёмы и задняя стенка: аудио, MIDI, CV, USB",
    "06_audio": "Звук: преобразователи, входы, выходы, аудиоплата",
    "07_compute_power": "Вычислитель, питание, аккумуляторы, тепло",
    "08_boards": "Платы: карта, M1, W1–W3, P1–P4, R1, R2, A1, PW, F1",
    "09_software": "Софт: система, SDK, протокол, эффекты",
}
ROW = re.compile(r"^\|\s*(\d{2})\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]*)\|\s*(.*?)\s*\|\s*$")
PART = re.compile(r"^\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|\s*([\d.]+)\s*\|")


def kb(path):
    try:
        return round(path.stat().st_size / 1024, 1)
    except OSError:
        return 0.0


def doc_parts(doc_rel):
    """Строки хаба для документа: части (если он разбит) или сам документ."""
    p = DOCS / doc_rel
    out = []
    if p.exists():
        for line in p.read_text(encoding="utf-8").split("\n"):
            m = PART.match(line)
            if m and "/" in m.group(2):
                out.append((m.group(3).strip(), (Path(doc_rel).parent / m.group(2)).as_posix(), float(m.group(4))))
    return out


def main():
    text = (DOCS / "README.md").read_text(encoding="utf-8")
    docs = []
    archive = False
    for line in text.split("\n"):
        if line.startswith("## ") and ("Архив" in line or "архив" in line or "Устарел" in line):
            archive = True
        m = ROW.match(line)
        if m and not archive:
            docs.append(dict(num=m.group(1), title=m.group(2), path=m.group(3), blocks=[b.strip() for b in m.group(4).split(",") if b.strip()],
                             note=re.sub(r"\*\*|\s+", " ", m.group(5)).strip()))
    by_dom = defaultdict(list)
    for d in docs:
        for b in d["blocks"] or ["01_project"]:
            by_dom[b].append(d)
    HUB.mkdir(exist_ok=True)
    idx = ["<!-- сгенерировано tools/build_hubs.py из docs/ru/README.md; не править руками -->",
           "# Хабы документации: читай хаб своей темы, потом нужную часть", "",
           "Правило: **не открывать документ целиком.** Хаб темы (1–3 КБ) → нужная часть (1–5 КБ). Решения темы — в файле блока `decisions/NN_*.md` (прав всегда он).", "",
           "| Хаб | Тема | Документов | Решения |", "|---|---|---|---|"]
    for dom, title in DOMAINS.items():
        lines = ["<!-- сгенерировано tools/build_hubs.py; не править руками (правки в docs/ru/README.md и в самих документах) -->",
                 f"# Хаб: {title}", "",
                 f"Решения темы: [`decisions/{dom}.md`](../decisions/{dom}.md) ({kb(DOCS / 'decisions' / (dom + '.md'))} КБ, читать, если задача касается решений темы).", ""]
        n = 0
        for d in sorted(by_dom.get(dom, []), key=lambda x: x["num"]):
            n += 1
            lines.append(f"## {d['num']}. {d['title']}")
            lines.append(f"{d['note'][:160]}")
            parts = doc_parts(d["path"])
            if parts:
                for t, rel, size in parts:
                    lines.append(f"- [{t[:90]}](../{rel}) · {size} КБ")
            else:
                lines.append(f"- [{d['title']}](../{d['path']}) · {kb(DOCS / d['path'])} КБ")
            lines.append("")
        (HUB / f"{dom}.md").write_text("\n".join(lines), encoding="utf-8")
        idx.append(f"| [{dom}]({dom}.md) | {title} | {n} | [decisions/{dom}.md](../decisions/{dom}.md) |")
    (HUB / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    for f in sorted(HUB.glob("*.md")):
        print(f"{f.name:22} {kb(f):5} КБ  {len(f.read_text(encoding='utf-8').splitlines())} строк")


if __name__ == "__main__":
    sys.exit(main())
