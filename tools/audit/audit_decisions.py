#!/usr/bin/env python3
"""Механический аудит журнала решений «Штуки Дрюка» (только чтение).

Проверяет то, что можно проверить без суждения: нумерацию, дубли, ссылки, соответствие индексу, записи без цитаты пользователя
и запрещённые термины в документах и скриптах (список правил — tools/audit/forbidden_terms.json).

  python tools/audit/audit_decisions.py                 # отчёт в консоль
  python tools/audit/audit_decisions.py --md OUT.md     # и в файл Markdown
  python tools/audit/audit_decisions.py --no-terms      # только журнал

Коды выхода: 0 — замечаний уровня ERROR нет; 1 — есть. Уровни: ERROR (нарушено правило ведения журнала), WARN (проверить глазами),
INFO (справка). Скрипт ничего не правит. Лицензия: AGPL-3.0-or-later.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEC = os.path.join(REPO, "docs", "ru", "decisions")
ROW = re.compile(r"^\|\s*([RP])(\d+)\s*\|(.*)\|\s*$")
REF = re.compile(r"(?<![A-Za-zА-Яа-я0-9])R(\d{1,3})(?![0-9A-Za-z])")
RANGE = re.compile(r"R(\d+)\s*[–-]\s*R?(\d+)")
QUOTE = re.compile(r"[«\"“].{3,}[»\"”]")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse_blocks():
    """Возвращает список записей: dict(id, kind, num, file, line, section, text)."""
    rows = []
    for name in sorted(os.listdir(DEC)):
        if not name.endswith(".md") or name in ("README.md",):
            continue
        section = ""
        for i, line in enumerate(read(os.path.join(DEC, name)).split("\n"), 1):
            if line.startswith("## "):
                section = line[3:].strip()
            m = ROW.match(line)
            if m:
                rows.append(dict(id=m.group(1) + m.group(2), kind=m.group(1), num=int(m.group(2)), file=name, line=i,
                                 section=section, text=m.group(3)))
    return rows


def section_kind(sec):
    s = sec.lower()
    if "заменено" in s:
        return "replaced"
    if "ждёт" in s or "ждет" in s:
        return "pending"
    if "действует" in s:
        return "active"
    return "other"


def expand_index_ranges(text):
    """Номера R, названные в ячейке индекса: 'R44, R152–R173' -> {44, 152..173}."""
    nums = set()
    for a, b in RANGE.findall(text):
        nums.update(range(int(a), int(b) + 1))
    for n in re.findall(r"R(\d+)(?!\s*[–-])", RANGE.sub(" ", text)):
        nums.add(int(n))
    return nums


def run(findings, rows):
    F = findings.append
    by_id = defaultdict(list)
    for r in rows:
        by_id[r["id"]].append(r)

    # 1. Дубли: один номер в двух живых строках
    for rid, lst in by_id.items():
        live = [r for r in lst if section_kind(r["section"]) in ("active", "pending")]
        if len(live) > 1:
            F(("ERROR", "J1 дубль номера", f"{rid} в нескольких живых строках: " + ", ".join(f"{r['file']}:{r['line']}" for r in live)))

    # 2. Следующий свободный номер в индексе против фактического максимума
    idx = read(os.path.join(DEC, "README.md"))
    m = re.search(r"следующее решение\s*\*\*R(\d+)\*\*,\s*следующее предложение\s*\*\*P(\d+)\*\*", idx)
    maxr = max((r["num"] for r in rows if r["kind"] == "R"), default=0)
    maxp = max((r["num"] for r in rows if r["kind"] == "P"), default=0)
    if m:
        nr, np_ = int(m.group(1)), int(m.group(2))
        if nr <= maxr:
            F(("ERROR", "J2 индекс: следующий R", f"индекс обещает R{nr}, а R{maxr} уже занят (должно быть ≥ R{maxr + 1})"))
        if np_ <= maxp:
            F(("WARN", "J2 индекс: следующий P", f"индекс обещает P{np_}, максимум в блоках P{maxp} (проверьте архив: номера P не переиспользуются)"))
    else:
        F(("WARN", "J2 индекс", "не найдена строка «следующее решение **Rnn**, следующее предложение **Pnn**»"))

    # 3. Ссылки на несуществующие R
    exist = {r["num"] for r in rows if r["kind"] == "R"}
    arch = read(os.path.join(DEC, "99_archive.md"))
    for n in REF.findall(arch):
        exist.add(int(n))              # в архиве R упоминаются как судьба старых P: считаем «существующими»
    for r in rows:
        for n in REF.findall(r["text"]):
            if int(n) not in exist and int(n) != r["num"]:
                F(("WARN", "J3 ссылка на несуществующий R", f"{r['id']} ({r['file']}:{r['line']}) ссылается на R{n}"))

    # 4. Живое R без цитаты пользователя (свежие R >= 150 — WARN, старые — одной строкой INFO)
    old_no_quote = []
    for r in rows:
        if r["kind"] == "R" and section_kind(r["section"]) == "active" and not QUOTE.search(r["text"]):
            if "предварительно" in r["text"].lower() or "пока" in r["text"].lower():
                continue
            if r["num"] >= 150:
                F(("WARN", "J4 R без цитаты", f"{r['id']} ({r['file']}:{r['line']}): нет «цитаты» пользователя (правило ведения: в R только то, что сказал пользователь)"))
            else:
                old_no_quote.append(r["id"])
    if old_no_quote:
        F(("INFO", "J4 старые R без цитаты", f"{len(old_no_quote)} шт. до R150 (до введения правила цитат?): " + ", ".join(sorted(old_no_quote, key=lambda x: int(x[1:]))[:60])))

    # 5. Заменённое без стрелки «→ Rm», живое с пометкой «заменено»
    for r in rows:
        k = section_kind(r["section"])
        if r["kind"] == "R" and k == "replaced" and "→" not in r["text"] and "заменено" not in r["text"].lower():
            F(("WARN", "J5 «Заменено» без стрелки", f"{r['id']} ({r['file']}:{r['line']}) стоит в «Заменено», но нет «→ Rm»"))
        if r["kind"] == "R" and k == "active" and re.search(r"заменен[оа]\s+R\d+", r["text"], re.I):
            F(("WARN", "J5 живое с пометкой «заменено»", f"{r['id']} ({r['file']}:{r['line']}) помечено заменённым, но лежит в «Действует»"))

    # 6. Строки индекса против реальных номеров блока
    for line in idx.split("\n"):
        mm = re.match(r"\|\s*\[(\d\d_\w+)\]\(([^)]+)\)\s*\|[^|]*\|([^|]*)\|", line)
        if not mm:
            continue
        stem = mm.group(1)
        listed = expand_index_ranges(mm.group(3))
        real = {r["num"] for r in rows if r["kind"] == "R" and r["file"].startswith(stem[:2])}
        missing = sorted(real - listed)
        gone = sorted(listed - real - exist)
        if missing:
            F(("WARN", "J6 индекс неполон", f"блок {stem}: R{', R'.join(map(str, missing[:12]))}{' …' if len(missing) > 12 else ''} есть в блоке, но не назван в таблице индекса"))
        if gone:
            F(("WARN", "J6 индекс врёт", f"блок {stem}: индекс называет R{', R'.join(map(str, gone[:12]))}, которых нет нигде"))

    # 7. Сводка
    F(("INFO", "сводка", f"записей R: {sum(1 for r in rows if r['kind'] == 'R')}, P: {sum(1 for r in rows if r['kind'] == 'P')}; максимум R{maxr}, P{maxp}"))


def scan_terms(findings):
    path = os.path.join(HERE, "forbidden_terms.json")
    if not os.path.exists(path):
        findings.append(("WARN", "T0 термины", "нет tools/audit/forbidden_terms.json"))
        return
    rules = json.load(open(path, encoding="utf-8"))
    roots = [os.path.join(REPO, p) for p in rules.get("scan", ["docs/ru", "hardware", "mockup", "model3d", "firmware"])]
    skip = tuple(rules.get("skip_dirs", [".git", "archive", "for-routing", "__pycache__", "UNROUTED", "logs"]))
    exts = tuple(rules.get("exts", [".md", ".py", ".json", ".txt"]))
    pats = [(re.compile(t["pattern"], 0 if t.get("case") else re.I), t) for t in rules["terms"]]
    for root in roots:
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in skip]
            for f in fn:
                if not f.endswith(exts):
                    continue
                p = os.path.join(dp, f)
                rel = os.path.relpath(p, REPO).replace("\\", "/")
                if rel.startswith("docs/ru/decisions/") or rel.startswith("docs/ru/3") and False:
                    continue
                try:
                    lines = read(p).split("\n")
                except Exception:
                    continue
                for i, line in enumerate(lines, 1):
                    for rx, t in pats:
                        if rx.search(line):
                            ok = t.get("allow_if")
                            if ok and re.search(ok, line, re.I):
                                continue
                            findings.append((t.get("level", "WARN"), "T " + t["id"], f"{rel}:{i}: {t['rule']} :: {line.strip()[:110]}"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md")
    ap.add_argument("--no-terms", action="store_true")
    a = ap.parse_args()
    rows = parse_blocks()
    findings = []
    run(findings, rows)
    if not a.no_terms:
        scan_terms(findings)
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda x: (order[x[0]], x[1], x[2]))
    out = []
    for lvl, code, msg in findings:
        out.append(f"{lvl:5} {code}: {msg}")
    cnt = {k: sum(1 for f in findings if f[0] == k) for k in order}
    out.append(f"\nИтого: ERROR {cnt['ERROR']}, WARN {cnt['WARN']}, INFO {cnt['INFO']}")
    print("\n".join(out))
    if a.md:
        md = ["# Механический аудит журнала решений", "", f"ERROR {cnt['ERROR']}, WARN {cnt['WARN']}, INFO {cnt['INFO']}", ""]
        for lvl in ("ERROR", "WARN", "INFO"):
            sub = [f for f in findings if f[0] == lvl]
            if sub:
                md += [f"## {lvl}", ""] + [f"- **{c}** — {m}" for _, c, m in sub] + [""]
        open(a.md, "w", encoding="utf-8").write("\n".join(md))
    sys.exit(1 if cnt["ERROR"] else 0)


if __name__ == "__main__":
    main()
