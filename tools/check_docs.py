#!/usr/bin/env python3
"""Проверка документации: локальные markdown-ссылки (файлы и якоря заголовков), достижимость
рабочих документов из индексов, части разбитых документов, пустые/битые указатели.
  python tools/check_docs.py          # печатает ошибки, код 1 при ошибках
"""
import re, sys, pathlib, subprocess

ROOT = pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
SCAN = ["CLAUDE.md", "README.md", "docs", "notes"]
LINK = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)\)|!\[[^\]]*\]\(([^)\s]+)\)")


def slug_anchor(h):
    h = re.sub(r"[`*_]", "", h.strip().lower())
    h = re.sub(r"[^\w\- ]", "", h, flags=re.U)
    return h.replace(" ", "-")


def files():
    for s in SCAN:
        p = ROOT / s
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from (f for f in p.rglob("*.md") if "archive" not in f.parts[:-1] or True)


def main():
    errs, linked = [], set()
    for f in files():
        text = f.read_text(encoding="utf-8", errors="replace")
        in_code = False
        for n, line in enumerate(text.split("\n"), 1):
            if line.startswith("```"):
                in_code = not in_code
            if in_code:
                continue
            for m in LINK.finditer(re.sub(r"`[^`]*`", "", line)):
                t = m.group(1) or m.group(2)
                if re.match(r"(https?:|mailto:)", t):
                    continue
                path, _, anchor = t.partition("#")
                tgt = (f.parent / path).resolve() if path else f
                if not tgt.exists():
                    errs.append(f"{f.relative_to(ROOT)}:{n}: нет файла {t}")
                    continue
                linked.add(tgt)
                if anchor and tgt.suffix == ".md":
                    heads = {slug_anchor(re.sub(r"^#+\s*", "", l)) for l in tgt.read_text(encoding="utf-8", errors="replace").split("\n") if l.startswith("#")}
                    if anchor.lower() not in heads and slug_anchor(anchor) not in heads:
                        errs.append(f"{f.relative_to(ROOT)}:{n}: нет якоря #{anchor} в {tgt.name}")
    # достижимость: части разбитых документов и рабочие документы docs/ru/*.md должны быть слинкованы
    for d in (ROOT / "docs/ru").iterdir():
        if d.is_dir() and (d.parent / (d.name + ".md")).exists():
            for part in d.glob("*.md"):
                if part.resolve() not in linked:
                    errs.append(f"не в индексе: {part.relative_to(ROOT)}")
    for md in (ROOT / "docs/ru").glob("[0-9][0-9]_*.md"):
        if md.resolve() not in linked:
            errs.append(f"не в карте docs/ru/README.md: {md.name}")
    for f in (ROOT / "notes/handoff_archive").glob("[0-9]*.md"):
        if f.resolve() not in linked:
            errs.append(f"не в индексе архива: {f.relative_to(ROOT)}")
    print("\n".join(errs) if errs else "OK: ссылки, якоря и достижимость в порядке")
    print(f"ошибок: {len(errs)}")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
