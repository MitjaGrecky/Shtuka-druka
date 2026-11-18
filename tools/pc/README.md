# tools/pc: PC helper scripts for board work (no kicad-cli)

All run with KiCad's Python (`C:\Program Files\KiCad\10.0\bin\python.exe`; there is no system Python for pcbnew) from the repo root.
Env for the generators: `KICAD_SYMBOL_DIR=C:/Users/karpa/Documents/Shtuka-druka/hardware/common/sym7`, `KICAD_FOOTPRINT_DIR="C:/Program Files/KiCad/10.0/share/kicad/footprints"` (set them in every bash call: shell state does not persist).

| Script | What it does |
|---|---|
| `ov.py BOARD...` | courtyard overlaps per side, run from `hardware/` (`python ov.py p1-left`) |
| `opn.py BOARD...` | for every J*: pad centre vs courtyard = which way a lying connector opens, board edges |
| `under.py BOARD...` | count of parts per side and type (heights under the board) |
| `eda_one.sh ID DIR vN` | import the packed board into EasyEDA Pro (`ID_vN`), compare parts/nets, write LCSC numbers, save. Needs EasyEDA running with the API bridge. Large boards (A1, P2, M1, R2) may need a manual double click on the project in "All Projects" |
| `eda_board.sh ID NAME DIR` | the check/LCSC part of the above for an already open project |
| `eda_open2.py NAME UUID`, `eda_save.py NAME`, `eda_wait.py` | open tabs, save, wait for the bridge |
| `cmp.py NAME PCB` | positions in EasyEDA against the KiCad file (needs the env vars; otherwise "NoneType ... GetFootprints") |
