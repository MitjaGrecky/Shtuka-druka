#!/usr/bin/env python3
"""Nightly PC check: update the repo if it is safe, run tools/pc_check.py on boards changed since
the last run, write logs/night/<date>.md. Nothing is committed or pushed.

Usage: night_check.py [--all] [--since-hours N] [--extra DIR ...]
Boards looked at: every *.kicad_pcb under hardware/ (project boards and Quilter results) and
under each --extra folder (default: the local Quilter inputs folder next to the repo, if any),
newer than the previous run (logs/night/last_run) or than N hours; --all checks every board.
Parity: a board is checked against the schematic in its own folder; a Quilter result folder
<JOB>_cand<a>_<b> against the job's inputs <extra>/<JOB>/ (same revision); otherwise against the
current project hardware/<board>/ (then parity may only show the revision difference).
Pull: only `git pull --ff-only`, and only when tracked files have no local changes.
License: AGPL-3.0-or-later.
"""
import argparse
import datetime as dt
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "night"
DEFAULT_EXTRA = [ROOT.parent / "ShtukaDruka" / "quilter_inputs"]


def sh(*cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (p.stdout + p.stderr).strip()


def project_for(board, extra):
    """Folder with the matching schematic. Own folder first; for a Quilter result <JOB>_cand<a>_<b>
    the job's inputs folder <extra>/<JOB>/ (same revision); last resort hardware/<name>/
    (the current revision, so parity may show the revision difference)."""
    if (board.parent / f"{board.stem}.kicad_sch").exists():
        return None, "board folder"                   # pc_check finds it itself
    m = re.match(r"(.+)_cand\d+_\d+$", board.parent.name)
    if m:
        for r in extra:
            inp = Path(r) / m.group(1)
            if any(inp.glob("*.kicad_sch")):
                return inp, f"Quilter inputs `{inp}`"
    parts = board.relative_to(ROOT).parts if board.is_relative_to(ROOT) else ()
    if len(parts) > 2 and parts[0] == "hardware":
        proj = ROOT / "hardware" / parts[1]
        if any(proj.glob("*.kicad_sch")):
            return proj, f"current project `hardware/{parts[1]}` (may be a newer revision)"
    return None, "none found"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--since-hours", type=float)
    ap.add_argument("--extra", nargs="*", default=None)
    a = ap.parse_args()
    LOG.mkdir(parents=True, exist_ok=True)
    stamp = LOG / "last_run"
    start = time.time()
    out = [f"# Night check {dt.datetime.now():%Y-%m-%d %H:%M}", ""]

    rc, dirty = sh("git", "status", "--porcelain", "--untracked-files=no")
    if dirty:
        out.append("- git: local changes in tracked files, pull skipped")
    else:
        rc, msg = sh("git", "pull", "--ff-only")
        out.append(f"- git pull: {msg.splitlines()[-1] if msg else rc}")
    _, head = sh("git", "log", "-1", "--format=%h %s")
    out.append(f"- HEAD: {head}")

    if a.all:
        since = 0.0
    elif a.since_hours is not None:
        since = start - a.since_hours * 3600
    else:
        since = stamp.stat().st_mtime if stamp.exists() else start - 24 * 3600
    roots = [ROOT / "hardware"] + [Path(p) for p in (a.extra if a.extra is not None else DEFAULT_EXTRA)]
    boards = sorted({p.resolve() for r in roots if r.is_dir() for p in r.rglob("*.kicad_pcb")
                     if "backups" not in p.parts and ".history" not in p.parts and p.stat().st_mtime > since})
    out.append(f"- boards changed since {dt.datetime.fromtimestamp(since):%Y-%m-%d %H:%M}: {len(boards)}")
    out.append("")

    extra = [Path(p) for p in (a.extra if a.extra is not None else DEFAULT_EXTRA)]
    by_proj = {}
    for b in boards:
        by_proj.setdefault(project_for(b, extra), []).append(b)
    for (proj, label), group in by_proj.items():
        cmd = [sys.executable, str(ROOT / "tools" / "pc_check.py"), *map(str, group)]
        if proj:
            cmd += ["--sch-from", str(proj)]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
        table = [l for l in p.stdout.splitlines() if l.startswith("|")]
        out.append(f"Schematic from: {label}")
        out += table or [f"pc_check failed: {p.stderr.strip()[-400:]}"]
        out.append("")
    if not boards:
        out.append("Nothing new to check.")
    out.append(f"\nTime: {time.time() - start:.0f} s")
    report = LOG / f"{dt.date.today():%Y-%m-%d}.md"
    report.write_text("\n".join(out) + "\n", encoding="utf-8")
    stamp.write_text(dt.datetime.now().isoformat(), encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
