# W1 - Levels (slope, left column)

Four volume pots with end stops (Main, Cue Mix, Phones 1, Phones 2), two P48 phantom-power buttons
with RGB lights, and a window for the encoder module M5 (Gain 1 + 2). No microcontroller: the board
speaks the 2 x 7 module bus (R123) and passes it on to M5.
Spec and reasoning: `docs/ru/31_w1_levels.md`. Status: rev 0.2 - schematic and routed board (rev 0.2, 13.11.2026: M5 window to x 89.5 for M5 rev 0.2, decision R132; rerouted with Freerouting 1.9, 100 passes).

| | |
|---|---|
| Board | 92 x 126 mm along the slope, 2 layers; panel x 10-102, slope s 12-138 mm from the fold; window 85 x 35 mm for M5 (rims 4.5 mm left, 2.5 mm right) |
| Top side | 4 x Alps RK09K 10k pots (LCSC C209770), 2 x TS-1187A tact switches (C318884), 4 x XL-1615RGBC-RF (C965840) |
| Bottom side | ADS1115 16-bit ADC (C37593), IS31FL3218 LED driver (C2940546), 74HC165 (C80696), passives, J1 and J2 |
| Bus | J1 to P1 over the fold, J2 to M5: 2 x 7, 1.27 mm, same pinout as every encoder module |
| I2C | ADS1115 0x48 (AIN0 Main, AIN1 Cue Mix, AIN2 Phones 1, AIN3 Phones 2), IS31FL3218 0x54 (write only) |
| Shift chain | P1 reads W1 first: D7 P48 1, D6 P48 2, D5-D0 = 1, then the M5 registers (M5 SR_OUT -> W1 U2 DS) |
| LEDs | IS31FL3218 OUT1-3 P48 1 left (R, G, B), OUT4-6 P48 1 right, OUT7-9 P48 2 left, OUT10-12 P48 2 right; 16 mA max |

## Files

- `w1-levels.kicad_pro/.kicad_sch/.kicad_pcb` - open in KiCad 10 (written in the KiCad 7 format).
- Symbols and footprints of the 1615 LED come from `../m1-screen-knobs/lib` (shared project library).
- `gen/` - the generators; they reuse M1's schematic writer and board helpers. Edit `design.py`, then:

```
python3 gen/make_sch.py          # schematic
python3 gen/check_netlist.py     # schematic netlist == design.py, pin by pin
python3 gen/make_pcb.py --route freerouting-1.9.0.jar --passes 100   # board + autorouting (xvfb-run, Java)
python3 gen/make_pcb.py --ses gen/last_route.ses                     # rebuild from the last routing
python3 gen/drc.py               # local DRC (KiCad 7 pcbnew); CI runs ERC and DRC on KiCad 10
```

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
