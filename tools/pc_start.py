#!/usr/bin/env python3
"""Start-of-session summary for the PC side: sync, open tasks, tools.

Usage: pc_start.py [--no-pull]
(1) git pull --rebase; branch, last commits, uncommitted files.
(2) Open tasks for the PC from notes/handoff.md: unchecked items addressed to it ("- [ ] #N ПК: ...").
(3) Tools: kicad-cli version, EasyEDA bridge (and whether EasyEDA is connected), markitdown.
Read-only apart from the pull. License: AGPL-3.0-or-later.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def sh(*cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (p.stdout + p.stderr).strip()


def bridge():
    for port in range(49620, 49630):
        try:
            with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1) as r:
                h = json.loads(r.read())
            if h.get("service") == "easyeda-bridge":
                return f"port {port}, EasyEDA connections: {h.get('edaWindowCount', 0)}"
        except OSError:
            pass
    return "not running (tools/eda/eda_check.py starts it)"


def main():
    if "--no-pull" not in sys.argv:
        print("git pull:", sh("git", "pull", "--rebase").splitlines()[-1:] or "")
    print("branch:", sh("git", "branch", "--show-current"))
    print("last commits:\n" + sh("git", "log", "-5", "--format=  %h %ad %an: %s", "--date=format:%d.%m %H:%M"))
    dirty = sh("git", "status", "--short")
    print("uncommitted:", "none" if not dirty else "\n" + dirty)

    print("\nOpen PC tasks (notes/handoff.md):")
    text = (ROOT / "notes" / "handoff.md").read_text(encoding="utf-8").splitlines()
    section, found = "", 0
    for i, line in enumerate(text, 1):
        if line.startswith("#"):
            section = line.lstrip("# ").strip()
        if re.match(r"\s*- \[ \] (#\d+ )?ПК\b", line):   # addressed to the PC, not merely mentioning it
            found += 1
            print(f"  line {i} [{section[:60]}]\n    {line.strip()[:220]}")
    if not found:
        print("  none")

    print("\nTools:")
    cli = next((c for c in (os.environ.get("KICAD_CLI"), shutil.which("kicad-cli"),
                            r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
                            "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli") if c and Path(c).exists()), None)
    print("  kicad-cli:", sh(cli, "version") if cli else "not found")
    print("  EasyEDA bridge:", bridge())
    md = next((c for c in (shutil.which("markitdown"), str(Path.home() / ".venvs/markitdown/Scripts/markitdown.exe"),
                           str(Path.home() / ".venvs/markitdown/bin/markitdown")) if c and Path(c).exists()), None)
    print("  markitdown:", md or "not installed")


if __name__ == "__main__":
    main()
