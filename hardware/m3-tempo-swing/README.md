# M3 - Tempo + Swing (encoder module)

Two smooth encoders with push (Tempo, Swing) and a 12-LED RGB ring around each. Spec: `hardware/for-routing/SPEC_boards.md`, section M3.
Status: rev 0.2 (rings r 15 from the layout, V2) - schematic and placed board with mounts, not routed (`UNROUTED`). Package for EasyEDA Pro: `hardware/for-routing/M3/`.

| | |
|---|---|
| Board | 92 x 34 mm, 2 layers; panel x 10-102, y 263-297 (the M1 strip, left column) |
| Top side | 2 x Alps EC11E smooth with switch (shafts at panel x 32 and 80, y 277; knob 22 mm), 24 x XL-1615RGBC-RF (C965840) on rings r 15 mm (layout ring 30; V2, user 13.11: the layout wins over the spec formula), 270 degrees |
| Bottom side | LP5864 LED driver (C5220564), 74HC165 (C80696), 2 x 4x10k packs (C25725), passives, J1 |
| Bus | J1 2 x 7, 1.27 mm (R123) at the front edge, to P1 (I2C channel 1 of P1's TCA9546A, P99) |
| I2C | LP5864 0x40 (ADDR1 ADDR0 = 0 0); SDA/SCL pull-ups R1, R2 not fitted (on the host); ~INT not used |
| Shift chain | host reads D7..D0: Tempo A, Tempo B, Tempo push, Swing A, Swing B, Swing push, 1, 1; DS <- SR_IN (R3 10k pull-up) |
| LEDs | left ring (Tempo) CS9-17, right ring (Swing) CS0-8; runs of 4 dots share a CS triple, SW0-3 serpentine (as M1 rev 0.5) |
| Touch | none (P102, proposal): encoder frames MP on GND; `design.TOUCH` marks the switch point |
| Holes | M2 in the corners and one between the knobs at the rear edge |

Checks (12.11.2026, KiCad 10.0.8): ERC 0 errors (4 warnings: ~INT on one pin, two library symbol versions);
`check_netlist.py` 202 pins, 0 mismatches; DRC 0 errors, schematic parity 0, 163 unrouted (by design);
EasyEDA Pro 3.2.209 import (project M3_v4, rev 0.2): PCB 38/38 and schematic 38/38 nets, 46/46 parts.

## Files and generators

Shared blocks: `hardware/common/gen/kit.py` (bus, LP5864, 74HC165, encoder, rings, holes), `boardkit.py`, `check_netlist.py`.
The schematic writer is M1's (`m1-screen-knobs/gen/make_sch.py`), loaded through `common/gen/m1compat.py` (Python 3.11).

```
python gen/design.py            # parts, nets, placement summary
python gen/make_sch.py          # schematic (KiCad 7 format)
python gen/check_netlist.py     # schematic netlist == design.py, pin by pin
python gen/make_pcb.py          # placed board, nets, mounts; no routing
python ../../tools/pack_easyeda.py M3 .     # package for EasyEDA (PC, KiCad 9/10)
```

On a PC with KiCad 10 set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7` (built by `python ../common/gen/sym7.py`)
and `KICAD_FOOTPRINT_DIR=<KiCad>/share/kicad/footprints`; run with KiCad's Python. The board written by KiCad 10's pcbnew
is in the KiCad 10 format; the cloud (KiCad 7) regenerates it with `make_pcb.py`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
