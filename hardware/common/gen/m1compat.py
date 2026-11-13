"""Load M1's generator modules (hardware/m1-screen-knobs/gen) on Python 3.11 (KiCad 10's Python on the PC).

M1's make_sch.py uses an f-string with nested quotes of the same kind (valid from Python 3.12 only).
This loader rewrites that construct in memory - the file itself stays as the cloud side wrote it.
Usage: import m1compat; M = m1compat.load("make_sch")      License: AGPL-3.0-or-later.
"""
import importlib.util
import os
import re
import sys

M1_GEN = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "m1-screen-knobs", "gen"))


def _fix(src):
    # {'a' if c else 'b'} inside an f'...' string -> {"a" if c else "b"}
    return re.sub(r"\{'([^'{}]*)' if ([^{}']+) else '([^'{}]*)'\}", r'{"\1" if \2 else "\3"}', src)


def load(name):
    if name in sys.modules:
        return sys.modules[name]
    path = os.path.join(M1_GEN, name + ".py")
    src = open(path, encoding="utf-8").read()
    if sys.version_info < (3, 12):
        src = _fix(src)
    if M1_GEN not in sys.path:
        sys.path.append(M1_GEN)          # M1's own imports (its design.py) resolve after the board's folder
    spec = importlib.util.spec_from_loader(name, loader=None, origin=path)
    mod = importlib.util.module_from_spec(spec)
    mod.__file__ = path
    sys.modules[name] = mod
    exec(compile(src, path, "exec"), mod.__dict__)
    if name == "make_sch":                       # "Common:<symbol>" comes from hardware/common/lib/Common.kicad_sym
        orig = mod.lib_block

        def lib_block(lib_id):
            if not lib_id.startswith("Common:"):
                return orig(lib_id)
            old, mod.KSYM = mod.KSYM, COMMON_LIB
            try:
                return orig(lib_id)
            finally:
                mod.KSYM = old
        mod.lib_block = lib_block
    return mod


COMMON_LIB = os.path.abspath(os.path.join(M1_GEN, "..", "..", "common", "lib"))
