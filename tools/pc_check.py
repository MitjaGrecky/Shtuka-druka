#!/usr/bin/env python3
"""DRC + schematic parity summary for one or more KiCad boards (KiCad 10 kicad-cli).

Usage:
  pc_check.py BOARD.kicad_pcb [BOARD2 ...] [--sch-from DIR] [--no-refill] [--md OUT.md]

For each board: runs `kicad-cli pcb drc --format json --severity-all --schematic-parity --refill-zones`
in a temporary folder (the board file itself is never changed) and prints one table row:
errors, warnings, unconnected items, parity issues, copper length and via count.

--sch-from DIR  take <name>.kicad_sch and <name>.kicad_pro from DIR (the project the board
                belongs to). Needed for Quilter results, which come without a schematic.
                Without it the schematic/project next to the board are used, if present.
The full JSON report is kept in logs/pc_check/ (git-ignored).
License: AGPL-3.0-or-later.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import board_stats  # noqa: E402


def kicad_cli():
    for c in (os.environ.get("KICAD_CLI"), shutil.which("kicad-cli"),
              r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
              "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"):
        if c and Path(c).exists():
            return c
    sys.exit("kicad-cli not found: set KICAD_CLI")


def run_drc(cli, board, sch_from, refill):
    board = Path(board).resolve()
    src = Path(sch_from).resolve() if sch_from else board.parent
    # the board must carry the project's name for kicad-cli to find the schematic (e.g. fixed.kicad_pcb)
    schs = sorted(src.glob("*.kicad_sch"))
    name = board.stem if (src / f"{board.stem}.kicad_sch").exists() or len(schs) != 1 else schs[0].stem
    with tempfile.TemporaryDirectory(prefix="pc_check_") as tmp:
        t = Path(tmp)
        shutil.copy2(board, t / f"{name}.kicad_pcb")
        have_sch = False
        for ext in (".kicad_sch", ".kicad_pro"):
            # project from --sch-from wins; else whatever sits next to the board
            for d in ([src, board.parent] if ext == ".kicad_pro" else [src]):
                f = d / f"{name}{ext}"
                if f.exists():
                    shutil.copy2(f, t / f.name)
                    have_sch |= ext == ".kicad_sch"
                    break
        out = t / "drc.json"
        cmd = [cli, "pcb", "drc", "--format", "json", "--severity-all", "--units", "mm", "-o", str(out)]
        if have_sch:
            cmd.append("--schematic-parity")
        if refill:
            cmd.append("--refill-zones")
        cmd.append(str(t / f"{name}.kicad_pcb"))
        p = subprocess.run(cmd, capture_output=True, text=True)
        if not out.exists():
            raise RuntimeError(f"kicad-cli failed ({p.returncode}): {p.stderr.strip() or p.stdout.strip()}")
        rep = json.loads(out.read_text(encoding="utf-8"))
        keep_dir = Path(__file__).resolve().parent.parent / "logs" / "pc_check"   # logs/ is git-ignored
        keep_dir.mkdir(parents=True, exist_ok=True)
        keep = keep_dir / f"{board.parent.name}__{board.stem}.drc.json"
        shutil.copy2(out, keep)
    return rep, have_sch, keep


def summarize(rep):
    sev = Counter(v.get("severity", "?") for v in rep.get("violations", []))
    types = Counter(v.get("type", "?") for v in rep.get("violations", []) if v.get("severity") == "error")
    return {
        "errors": sev.get("error", 0),
        "warnings": sev.get("warning", 0),
        "unconnected": len(rep.get("unconnected_items", [])),
        "parity": len(rep.get("schematic_parity", [])),
        "error_types": types,
        "unconnected_nets": sorted({i.get("description", "") for u in rep.get("unconnected_items", [])
                                    for i in u.get("items", [])[:1]}),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("boards", nargs="+")
    ap.add_argument("--sch-from")
    ap.add_argument("--no-refill", action="store_true")
    ap.add_argument("--md", help="also write the summary to this Markdown file")
    ap.add_argument("--details", action="store_true", help="list error types and unconnected items")
    a = ap.parse_args()
    cli = kicad_cli()
    lines = ["| Board | Errors | Warnings | Unconnected | Parity | Copper, mm | Vias |",
             "|---|---|---|---|---|---|---|"]
    details = []
    for b in a.boards:
        try:
            rep, have_sch, keep = run_drc(cli, b, a.sch_from, not a.no_refill)
        except Exception as e:  # noqa: BLE001 - report and go on with the next board
            lines.append(f"| `{b}` | failed: {e} | | | | | |")
            continue
        s = summarize(rep)
        rows, _ = board_stats.stats(b)
        copper = sum(r[3] for r in rows)
        vias = sum(r[4] for r in rows)
        parity = s["parity"] if have_sch else "n/a (no schematic)"
        lines.append(f"| `{b}` | {s['errors']} | {s['warnings']} | {s['unconnected']} | {parity} | {copper:.0f} | {vias} |")
        if a.details:
            details.append(f"\n`{b}` (full report: `{keep}`)")
            for t, n in s["error_types"].most_common():
                details.append(f"- error {t}: {n}")
            for u in s["unconnected_nets"][:30]:
                details.append(f"- unconnected: {u}")
    ver = subprocess.run([cli, "version"], capture_output=True, text=True).stdout.strip()
    text = "\n".join([f"kicad-cli {ver}, refill zones: {not a.no_refill}", "", *lines, *details]) + "\n"
    print(text)
    if a.md:
        Path(a.md).write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
