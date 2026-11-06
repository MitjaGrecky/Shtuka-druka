"""One-off: split docs/ru/14_decisions_log.md into docs/ru/decisions/*.md.

Rows are copied verbatim; every R and P id lands in exactly one block file.
Run: python3 tools/split_decisions.py --verify  (re-running without the flag regenerates block files from the old log and would overwrite later edits)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs/ru/14_decisions_log.md"
OUT = ROOT / "docs/ru/decisions"

R = lambda *a: [f"R{i}" for i in a]
rng = lambda a, b: list(range(a, b + 1))

# file -> title, scope, R ids, P ids
BLOCKS = {
    "01_project.md": ("Проект и процесс",
        "Зачем Штука, этапы, открытость, лицензии, язык надписей, как ведём работу.",
        R(1, 2, 4, 5, 6, 9, 20, 25, 27, 28, 45, 69, 77), []),
    "02_controls.md": ("Логика управления",
        "Как человек работает с устройством: сетка, дорожки, режимы, навигация, запись, принципы кнопок.",
        R(7, 11, 12, 14, 15, 17, 46, 48, 49, 52, 53, *rng(89, 97), 99, 111, 112), []),
    "03_panel.md": ("Панель: раскладка и органы",
        "Где что стоит на верхней панели, какие органы, экран, полоса, ручки.",
        R(10, 13, 18, 41, 42, 50, 62, 63, 74, 75, 98, *rng(100, 108), 110, 113), []),
    "04_enclosure.md": ("Корпус и механика",
        "Габариты корпуса, отсек аккумулятора, макет, посадка реальных деталей.",
        R(43, 44, 109), [f"P{i}" for i in rng(90, 96)]),
    "05_io.md": ("Входы, выходы, разъёмы",
        "Какие гнёзда есть, сколько и где: аудио, MIDI, CV, синхро, USB, задняя панель.",
        R(3, 8, *rng(22, 24), 26, *rng(32, 35), 37, 39, 55, 56, 60, 68, *rng(71, 73), *rng(78, 81)), []),
    "06_audio.md": ("Аудиотракт и звуковая карта",
        "Электрика звука: преобразователи, предусилители, выходные каскады, генераторы, USB-аудио.",
        R(16, *rng(64, 67), *rng(82, 84), 87, 88, 114, *rng(116, 118)), []),
    "07_compute_power.md": ("Вычислитель, питание, стенд",
        "Mini-ITX, стенд разработки, аккумулятор и питание.",
        R(19, 36, 40, 58, 59, 76), []),
    "08_boards.md": ("Платы и электроника",
        "Карта плат, микроконтроллеры, протокол, светодиоды, модули ручек M1–M5, W1, сборка и разводка.",
        R(51, 54, 85, 86, 115, *rng(119, 127)), ["P75", "P82", "P83", "P84", "P85", "P97"]),
    "09_software.md": ("Софт и звуковой движок",
        "Система, обновления, SDK, дорожка и эффекты, хранение и экспорт.",
        R(21, *rng(29, 31), 38, 47, 57, 61, 70), []),
}

# Rows fully replaced by newer decisions: go to the "Заменено" part of their block.
REPLACED = {
    "R41": "раскладка v4 заменена направлением v5 и панелью v7 (R94, R107); принцип частоты — R90",
    "R46": "страницы-глаголы отменены, вместо них две оси режимов (R94)",
    "R62": "ряд сцен — над сеткой (R101)",
    "R75": "полоса под пэдами, уже в первой версии (R105, R113)",
    "R79": "уточнено R80 и R81 (два USB-A, место второго — в System)",
}
# Rows still valid but partly refined: stay in the main table with a note.
REFINED = {
    "R15": "колесо больше не двигает сетку, только экран (R94); ориентация сетки подтверждена R93",
    "R44": "глубина и сгиб — R107",
    "R45": "страницы Grab/Shape/Perform/Arrange отменены R94; правило про английские надписи действует",
    "R52": "работа колеса по сетке отменена R94; колесо + Back — только экран",
    "R55": "Bluetooth-аудио в первой версии нет (R39); линейные входы — R37; схема входов — R117",
    "R56": "MIDI, синхро и CV уточнены R32–R35",
    "R58": "вычислитель уточнён R36 (Mini-ITX)",
    "R59": "отсек — R109",
    "R60": "громкости — в блоке «Уровни» (R94, R100); SD и второй USB-A — в System (R81); гнёзда наушников спереди остаются",
    "R87": "чип ЦАП теперь CS4308P (R116), аттенюатор — в нём",
    "R125": "размер платы уточнён R127: 224 × 34 мм",
}

NEW_P = {
    "P97": "| P97 | Крепление M1: латунные вставки M2 (запрессовка нагревом) в световоде, винт снизу через плату. "
           "К угловым H1–H4 добавить 3 отверстия в задней полосе, в зазорах между энкодерами 2–3, 4–5, 6–7 "
           "(x ≈ 56, 112, 168 мм), шаг креплений ≈ 56 мм. Отверстия ставятся до финальной разводки | "
           "Пользователь: «каждый второй энкодер надо ставить крепление», крепление — «второе после расположения "
           "исполнительных элементов». Световод 6,4 мм уже стоит между платой и обшивкой, отдельные стойки не нужны; "
           "прижим рядом с огнями держит юстировку; головки снизу не мешают верхним полосам SMD; вставки есть в рознице "
           "(R28). Координаты проверить по генератору | 30, `hardware/m1-screen-knobs` |",
}


def parse():
    # the old single-file log lives on in git history (last version: commit 29d30af)
    import subprocess
    text = subprocess.run(["git", "-C", str(ROOT), "show", f"29d30af:{SRC.relative_to(ROOT)}"],
                          capture_output=True, text=True, check=True).stdout
    rows = {}
    for line in text.splitlines():
        m = re.match(r"\| ([RP]\d+) \|", line)
        if m:
            rows[m.group(1)] = line
    rows.update(NEW_P)
    return text, rows


def block_file(fname, title, scope, rids, pids, rows):
    out = [f"# Решения: {title}", "", f"*{scope}*", "",
           "Общие правила ведения и приоритеты — в [README](README.md).", ""]
    if pids:
        out += ["## Ждёт «да» или «нет»", "", "| № | Предложение | Почему | Где |", "|---|---|---|---|"]
        out += [rows[p] for p in pids]
        out.append("")
    live = [r for r in rids if r not in REPLACED]
    out += ["## Действует", "", "| № | Дата | Решение | Где подробно |", "|---|---|---|---|"]
    for r in live:
        row = rows[r]
        if r in REFINED:
            row = row.rstrip()[:-1].rstrip() + f" *(уточнено: {REFINED[r]})* |"
        out.append(row)
    old = [r for r in rids if r in REPLACED]
    if old:
        out += ["", "## Заменено (история, читать не обязательно)", "",
                "| № | Дата | Решение | Где подробно |", "|---|---|---|---|"]
        for r in old:
            out.append(rows[r].rstrip()[:-1].rstrip() + f" **→ {REPLACED[r]}** |")
    return "\n".join(out) + "\n"


def main():
    text, rows = parse()
    OUT.mkdir(parents=True, exist_ok=True)
    for fname, (title, scope, rids, pids) in BLOCKS.items():
        (OUT / fname).write_text(block_file(fname, title, scope, rids, pids, rows), encoding="utf-8")
    # archive: everything below the tables of the old log (P notes, questions, outdated docs)
    note = re.search(r"\n\(P5, P7.*?\)\n", text, re.S).group(0).strip()
    q = text[text.index("## 3. Открытые вопросы"):text.index("## 4. Что устарело")]
    old_docs = text[text.index("## 4. Что устарело"):]
    arch = ["# Решения: архив", "",
            "*История журнала: какие предложения во что превратились, закрытые вопросы, устаревшие документы. "
            "Читать, только если нужна история.*", "",
            "## Судьба старых предложений", "", note, "",
            q.replace("## 3. Открытые вопросы (по важности)", "## Вопросы из старого журнала (как были на 06.11.2026)"),
            old_docs.replace("## 4. Что устарело", "## Что устарело")]
    (OUT / "99_archive.md").write_text("\n".join(arch).rstrip() + "\n", encoding="utf-8")


def verify():
    text, rows = parse()
    ids = set(re.findall(r"^\| ([RP]\d+) \|", text, re.M))
    seen = {}
    for f in OUT.glob("0*.md"):
        for i in re.findall(r"^\| ([RP]\d+) \|", f.read_text(encoding="utf-8"), re.M):
            seen.setdefault(i, []).append(f.name)
    missing = sorted(ids - set(seen), key=lambda s: (s[0], int(s[1:])))
    dup = {k: v for k, v in seen.items() if len(v) > 1}
    print(f"old ids {len(ids)}, placed {len(seen)}, missing {missing}, duplicated {dup}, new {sorted(set(seen) - ids)}")
    return not missing and not dup


if __name__ == "__main__":
    if "--verify" in sys.argv:
        sys.exit(0 if verify() else 1)
    main()
    verify()
