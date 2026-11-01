# M1 - screen knobs module

Eight smooth encoders with push and touch (Param 1-8 under the screen), each with a ring of 13 RGB LEDs.
Spec and reasoning: `docs/ru/30_m1_screen_knobs.md`. Status: rev 0.1 - schematic done, parts placed, routing in progress.

| | |
|---|---|
| Board | 224 x 28 mm, 4 layers; panel position x 108.75-332.75, y 263-291 (knob row y 277) |
| Top side | 8 x Alps EC11E (smooth, switch), 104 x XINGLIGHT XL-1615RGBC-RF (LCSC C965840) |
| Bottom side | IS31FL3741A LED driver (C2940604), CY8CMBR3108 touch (C462528), 3 x 74HC165, passives, J1 |
| Bus J1 | 2 x 7, 1.27 mm: +5V x2, +3V3, GND x4, SDA, SCL, INT, SR_LOAD, SR_CLK, SR_OUT, SR_IN |
| I2C | LED driver 0x30 (ADDR=GND, R3; 0x31-0x33 via R4-R6), touch 0x37 |
| Shift chain | host reads U3 D7..D0, U4, U5: E1 A, E1 B, E1 push, E2 A, ... E8 push |

## Files

- `m1-screen-knobs.kicad_pro/.kicad_sch/.kicad_pcb` - open in KiCad 10 (written in the KiCad 7 format; KiCad 10 upgrades on save).
- `lib/` - project symbols (IS31FL3741A, XL-1615RGBC-RF, encoder with touch pin) and footprints (LED 1615, QFN-60).
- `gen/` - the generators. Edit `design.py`, then run:

```
python3 gen/make_lib.py     # symbols and footprints
python3 gen/make_sch.py     # schematic
python3 gen/make_pcb.py     # board: placement, nets, GND planes (needs KiCad's pcbnew module)
```

`UNROUTED` marks the board as not routed yet: CI keeps the DRC report but does not fail.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
