#!/usr/bin/env python3
"""Разбивает большой документ docs/ru/NN_name.md на небольшие части + индекс.

Без потерь: части = исходный текст, нарезанный по заголовкам `## ` (а крупные куски, > LIMIT байт,
ещё и по `### `); относительные ссылки получают префикс `../`; к каждой части добавлена одна строка-шапка.
Исходный путь остаётся индексом (на него ссылаются решения и документы).

  python tools/split_docs.py docs/ru/41_design_review.md          # разбить
  python tools/split_docs.py --verify docs/ru/41_design_review.md  # склеить части и сравнить с git HEAD
Для проверки исходник берётся из `git show HEAD:<путь>`, пока индекс не закоммичен;
после коммита используйте `--verify --orig <файл>`.
"""
import re, sys, subprocess, pathlib, argparse

LIMIT = 9000  # байт; крупнее — режем дальше по ###
TR = dict(zip("абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
              ["a","b","v","g","d","e","e","zh","z","i","y","k","l","m","n","o","p","r","s","t","u","f","h","c","ch","sh","sch","","y","","e","yu","ya"]))


def slug(title):
    t = re.sub(r"^#+\s*", "", title).lower()
    t = "".join(TR.get(c, c) for c in t)
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return "-".join(t.split("-")[:6]) or "part"


def cut(lines, prefix):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    if not idx:
        return [lines]
    out = []
    if idx[0] > 0:
        out.append(lines[:idx[0]])
    for a, b in zip(idx, idx[1:] + [len(lines)]):
        out.append(lines[a:b])
    return out


def fix_links(text):
    def rep(m):
        t = m.group(2)
        if re.match(r"(https?:|#|/|\.\./|mailto:)", t):
            return m.group(0)
        return f"{m.group(1)}../{t})"
    return re.sub(r"(\]\()([^)\s]+)\)", rep, text)


def parts_of(text):
    lines = text.split("\n")
    first = cut(lines, "## ")
    parts = []
    for chunk in first:
        size = len("\n".join(chunk).encode())
        if size > LIMIT and chunk[0].startswith("## "):
            sub = cut(chunk, "### ")
            parts.extend(sub)
        else:
            parts.append(chunk)
    return ["\n".join(p) for p in parts]


def title_of(part, n):
    for l in part.split("\n"):
        if l.startswith("#"):
            return re.sub(r"^#+\s*", "", l).strip()
    return "Начало документа" if n == 0 else "Часть"


def split(path):
    path = pathlib.Path(path)
    text = path.read_text(encoding="utf-8")
    assert "](../" not in text, "в исходнике уже есть ../"
    stem = path.stem
    outdir = path.parent / stem
    outdir.mkdir(exist_ok=True)
    num = stem.split("_")[0]
    parts = parts_of(text)
    rows = []
    for n, p in enumerate(parts):
        t = title_of(p, n)
        name = "00_nachalo.md" if n == 0 else f"{n:02d}_{slug(t)}.md"
        head = f"> Часть документа {num} ([индекс](../{path.name})): {t}\n\n"
        (outdir / name).write_text(head + fix_links(p), encoding="utf-8", newline="\n")
        rows.append((name, t, len(p.encode())))
    first_title = title_of(parts[0], 0)
    idx = [f"# {first_title}", "",
           f"**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `{path.name}` теперь индекс).",
           f"Читай только нужную часть. Номера разделов и решений прежние: «{num}, раздел N» = часть с этим номером в названии. "
           f"Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).", "",
           "| Часть | Раздел | КБ |", "|---|---|---|"]
    for name, t, sz in rows:
        idx.append(f"| [{name[:-3]}]({stem}/{name}) | {t} | {sz/1024:.1f} |")
    idx += ["", f"Проверка полноты: `python tools/split_docs.py --verify docs/ru/{path.name}`.", ""]
    path.write_text("\n".join(idx), encoding="utf-8", newline="\n")
    return len(parts)


def verify(path, orig=None):
    path = pathlib.Path(path)
    stem = path.stem
    if orig:
        text = pathlib.Path(orig).read_text(encoding="utf-8")
    else:
        rel = path.resolve().relative_to(pathlib.Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()).resolve()).as_posix()
        text = subprocess.check_output(["git", "show", f"HEAD:{rel}"]).decode("utf-8")
    got = []
    for f in sorted((path.parent / stem).glob("*.md")):
        t = f.read_text(encoding="utf-8")
        t = t.split("\n", 2)[2]  # убрать шапку
        got.append(t.replace("](../", "]("))
    joined = "\n".join(got)
    ok = joined == text
    print("OK: части склеиваются в исходник" if ok else "ОТЛИЧИЯ: проверь вручную")
    return ok


# ---- режим архивации хвоста файла: python tools/split_docs.py --archive-tail FILE LINE OUTDIR ----
def archive_tail(path, line, outdir, pack=14000):
    path = pathlib.Path(path)
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    lines = path.read_text(encoding="utf-8").split("\n")
    head, tail = lines[:line - 1], lines[line - 1:]
    idx = [i for i, l in enumerate(tail) if l.startswith("## ") or l.startswith("### ")]
    chunks = []
    if idx and idx[0] > 0:
        chunks.append(tail[:idx[0]])
    for a, b in zip(idx, idx[1:] + [len(tail)]):
        chunks.append(tail[a:b])
    files, cur = [], []
    for c in chunks:
        if cur and len("\n".join(sum(cur, []) + c).encode()) > pack:
            files.append(cur); cur = []
        cur.append(c)
    if cur:
        files.append(cur)
    rows = []
    for n, f in enumerate(files, 1):
        name = f"{n:02d}.md"
        body = "\n".join("\n".join(c) for c in f)
        (outdir / name).write_text(body, encoding="utf-8", newline="\n")
        for c in f:
            t = next((l for l in c if l.startswith("#")), c[0] if c else "")
            rows.append((name, re.sub(r"^#+\s*", "", t).strip()))
    # точная склейка: куски соединяются через "\n" так же, как строки хвоста
    joined = "\n".join("\n".join(sum(f, [])) if False else "\n".join("\n".join(c) for c in f) for f in files)
    assert joined == "\n".join(tail), "архив не совпадает с хвостом"
    index = ["# Архив передачи хода (отчёты и закрытые записи)", "",
             f"Перенесено из `{path.as_posix()}` без изменений ради экономии контекста. Читать нужную запись по таблице; новые записи пишутся в `notes/handoff.md`.", "",
             "| Файл | Запись |", "|---|---|"]
    index += [f"| [{n}]({n}) | {t} |" for n, t in rows]
    (outdir / "README.md").write_text("\n".join(index) + "\n", encoding="utf-8", newline="\n")
    note = (f"(Старые отчёты и закрытые записи перенесены в [`notes/handoff_archive/`]({outdir.name}/README.md): индекс записей по заголовкам, текст без изменений.)\n")
    path.write_text("\n".join(head) + "\n" + note, encoding="utf-8", newline="\n")
    return len(files), len(rows)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--orig")
    if len(sys.argv) > 1 and sys.argv[1] == "--archive-tail":
        print(archive_tail(sys.argv[2], int(sys.argv[3]), sys.argv[4]))
        sys.exit(0)
    a = ap.parse_args()
    if a.verify:
        sys.exit(0 if verify(a.path, a.orig) else 1)
    print(split(a.path), "частей")


