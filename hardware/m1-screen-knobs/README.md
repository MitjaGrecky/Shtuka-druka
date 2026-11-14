# M1 - screen knobs module

**Current source (R148, 14.11.2026): rev 0.5** - four TI LP5864 (one per pair of rings), 12 RGB LEDs per ring, 4 corner holes + 3 in the gaps (x 56, 112, 168 mm, P97), 163 parts. `gen/design.py` builds rev 0.5 by default; `M1_LP=0` builds the old rev 0.3 (two IS31FL3741A, 13 LEDs, 8 holes), kept for history. The KiCad files here and `hardware/for-routing/M1` agree. The text below still describes rev 0.1-0.3.

Eight smooth encoders with push and touch (Param 1-8 under the screen), each with a ring of 13 RGB LEDs.
Spec and reasoning: `docs/ru/30_m1_screen_knobs.md`. Status: rev 0.1 - schematic done, board routed except 4 connections around U1 (see UNROUTED), light guide ready to print.

| | |
|---|---|
| Board | 224 x 34 mm, 4 layers; panel position x 108.75-332.75, y 263-297 (knob row y 277, panel fold y 300) |
| Top side | 8 x Alps EC11E (smooth, switch), 104 x XINGLIGHT XL-1615RGBC-RF (LCSC C965840) |
| Bottom side | IS31FL3741A LED driver (C2940604), CY8CMBR3108 touch (C462528), 3 x 74HC165, passives, J1 |
| Bus J1 | 2 x 7, 1.27 mm: +5V x2, +3V3, GND x4, SDA, SCL, INT, SR_LOAD, SR_CLK, SR_OUT, SR_IN |
| I2C | LED driver 0x30 (ADDR=GND, R3; 0x31-0x33 via R4-R6), touch 0x37 |
| LED matrix | LED n = 13 (ring-1) + (dot-1): SW = n mod 9 + 1, CS = 3 (n div 9) + 1..3 (R, G, B); CS37-39 unused |
| Shift chain | host reads U3 D7..D0, U4, U5: E1 A, E1 B, E1 push, E2 A, ... E8 push |

## Files

- `m1-screen-knobs.kicad_pro/.kicad_sch/.kicad_pcb` - open in KiCad 10 (written in the KiCad 7 format; KiCad 10 upgrades on save).
- `mech/m1_light_guide.stl` - the light guide (R126), black PETG/PLA, 0.2 mm layers.
- `lib/` - project symbols (IS31FL3741A, XL-1615RGBC-RF, encoder with touch pin) and footprints (LED 1615, QFN-60).
- `gen/` - the generators. Edit `design.py`, then run:

```
python3 gen/make_lib.py     # symbols and footprints
python3 gen/make_sch.py     # schematic
python3 gen/make_pcb.py     # board: placement, nets, GND planes (needs KiCad's pcbnew module)
python3 gen/make_pcb.py --route freerouting-1.9.0.jar --passes 16 --finish   # + autorouting (xvfb-run, Java)
python3 gen/make_pcb.py --ses gen/last_route.ses --finish                     # rebuild from the last routing
python3 gen/make_light_guide.py mech             # light guide STL (needs bpy)
```

`UNROUTED` marks the board as not routed yet: CI keeps the DRC report but does not fail.
`QUILTER.md` - rules for handing the board to an external layout service; the parts fixed by the panel are locked.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
