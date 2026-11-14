#!/usr/bin/env python3
"""Cross-board connector check: for each cable between two boards, print the nets of the two connectors pin by pin and flag pins
where the names differ (ribbon cables connect pin n to pin n). Usage: xboard_check.py   (run from the repo root; KiCad python)
License: AGPL-3.0-or-later."""
import importlib.util
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
HW = os.path.join(REPO, "hardware")
sys.path.insert(0, os.path.join(HW, "common", "gen"))
os.environ.setdefault("KICAD_SYMBOL_DIR", os.path.join(HW, "common", "sym7"))


def load(board):
    path = os.path.join(HW, board, "gen", "design.py")
    sys.path.insert(0, os.path.dirname(path))
    spec = importlib.util.spec_from_file_location("design_" + board.replace("-", "_"), path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["design"] = mod
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    d = {}
    for p in mod.parts():
        if p["ref"].startswith("J"):
            d.setdefault(p["value"], p)
            d[p["ref"]] = p                     # also by reference (values repeat, e.g. R2 "USB down")
    return d


PAIRS = [("r1-audio", "to A1 (ADC 1-10)", "a1-digital", "from R1 (ADC 1-10)"),
         ("r1-audio", "to A1 (ADC 11-18, DAC 1-4, power)", "a1-digital", "R1 (ADC 11-18, DAC 1-4, power)"),
         ("a1-digital", "to F1", "f1-phones", "from A1"),
         ("r2-control", "to A1/R1", "r1-audio", "from R2"),
         ("pw-power", "to F1", "f1-phones", "from PW"),
         ("r1-audio", "to F1 (mute)", "f1-phones", "from R1 (mute)"),
         ("pw-power", "to R2", "r2-control", "Power from PW"),
         ("pw-power", "to A1/R1", "r1-audio", "Power from PW"),
         ("pw-power", "I2C power monitor", "p2-grid", "I2C power monitor (PW)"),
         ("pw-power", "+5V panel", "p2-grid", "+5V from PW"),
         ("r2-control", "J4", "p2-grid", "USB to R2 hub"),
         ("r2-control", "J5", "a1-digital", "USB port A (hub)"),
         ("p2-grid", "J5", "p1-left", "Deck bus to P2 2x8 1.27"),
         ("p2-grid", "J6", "p3-tracks", "Deck bus to P2 2x8 1.27"),
         ("p2-grid", "J7", "p4-right", "Deck bus to P2 2x8 1.27")]
if __name__ == "__main__":
    cache = {}
    for b1, c1, b2, c2 in PAIRS:
        for b in (b1, b2):
            if b not in cache:
                cache[b] = load(b)
        if c1 not in cache[b1] or c2 not in cache[b2]:
            print(f"?? {b1}:{c1} / {b2}:{c2}: connector not found")
            continue
        p1, p2 = cache[b1][c1]["pins"], cache[b2][c2]["pins"]
        pins = sorted(set(p1) | set(p2), key=lambda s: int(s) if s.isdigit() else 0)
        diff = [(n, p1.get(n), p2.get(n)) for n in pins if (p1.get(n) or "").lstrip("/") != (p2.get(n) or "").lstrip("/")]
        print(f"== {b1}:{c1} <-> {b2}:{c2}: {len(pins)} pins, {len(diff)} with different names")
        for n, a, b in diff:
            print(f"   pin {n}: {a} | {b}")
