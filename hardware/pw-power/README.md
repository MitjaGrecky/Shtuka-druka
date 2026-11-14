# PW - Power board (under the slope, right, next to the battery bay)

All the power of the instrument: three inputs joined by ideal diodes, the rear On/Off switch, and every rail the boards need.
Research: `docs/ru/34_rear_boards_research.md` (section 5). Decisions: R36 (Mini-ITX, 19 V), R40/R59/R109 (battery),
R72 (DC 12-24 V with protection, USB-C PD), R110 (screen 5 V / 4 W), R118 (phantom), R145 (USB-C Power separate from the PC port).

**Status: rev 0.1 - schematic only** (177 parts, 95 nets, 14.11.2026). Values follow the TI datasheet examples scaled to these
rails; the notes marked "check" are to be verified against the datasheets before the board (cloud task #23).

## Power tree

| Block | Part | From -> to | Notes |
|---|---|---|---|
| DC input | fuse 7 A, SMBJ28CA, LM74700 + CSD18540Q5B | DC jack 12-24 V -> BUS_IN | reverse polarity and ORing |
| USB-C Power | TPS25730D (C22438973), SMBJ22CA, LM74700 + FET | PD 15-20 V, 3 A operating / 5 A max -> BUS_IN | no I2C: ADCIN1 = 15 V min, ADCIN2 = 20 V max, ADCIN3/4 = 3 A / 5 A (datasheet tables 8-3..8-6) |
| Battery | fuse 10 A, SMBJ20CA, LM74700 + FET | 4S 12.8-16.8 V -> BUS_IN | pack with its own BMS (R109); charger later (R40) |
| On/Off | rocker on the rear wall, >= 10 A DC | BUS_IN -> BUS | mechanical master switch |
| 19 V Mini-ITX | LM5176 four-switch buck-boost, 4 x CSD18540Q5B | BUS 12-24 V -> 19 V 5 A (95 W), 300 kHz | ASRock N100DC-ITX officially wants 19 V (doc 34); upgrades limited to 35-45 W (R36) |
| +5V_PANEL | TPS54560B (C1850354) | BUS -> 5 V 5 A | panel boards and LEDs; LED budget up to ~5.6 A white on full (doc 10): firmware limits brightness |
| +5V | TPS54560B | BUS -> 5 V 5 A | screen 4 W, R2, USB devices, logic of the audio boards |
| +-14 V | 2 x LMR33640 (buck, inverting buck-boost) | 19 V -> +14 V / -14 V | pre-regulators 1-2 V above the LDOs (doc 34) |
| +-12 V quiet | TPS7A4701 / TPS7A3301 | +-14 V -> +-12 V | TIDA-01458 scheme; TPS7A47: 4 uV rms, ANY-OUT 12.0 V |
| +48 V phantom | LM5156H boost + TPS7A4101 | 19 V -> 49.7 V -> 47.8 V, ~40 mA | two P48 channels (doc 34, 2.3); switched per channel on R1 (R118) |

## Connectors

| J | To | Pins |
|---|---|---|
| DC in | DC jack on the wall (Micro-Fit 1x2) | DC_RAW, GND |
| USB-C Power in | USB-C receptacle on the wall (Micro-Fit 2x3) | VBUS x 2, GND x 2, CC1, CC2 |
| Battery | pack (Micro-Fit 2x2) | BAT x 2, GND x 2 |
| On/Off switch | rocker (Micro-Fit 1x2) | BUS_IN, BUS |
| 19 V to Mini-ITX | Micro-Fit 2x2 -> 5.5 x 2.5 plug | V19 x 2, GND x 2 |
| +5V panel | P2 hub (Micro-Fit 2x3) | +5V_PANEL x 3, GND x 3 |
| to R2 | JST PH 5 | +12V, GND, -12V, GND, +5V (as R2 J1) |
| to A1/R1 | Micro-Fit 2x5 | +12V, -12V, +5V x 2, +48V, GND x 5 |
| to F1 | JST PH 3 | +12V, GND, -12V |
| +5V screen | JST PH 2 | +5V, GND |

Budget (estimate): Mini-ITX 25-45 W, panel 5-28 W (LEDs), screen 4 W, audio +-12 V ~ 10 W, phantom < 2 W. Typical 45-60 W,
peak above the 100 W of a PD source: the firmware caps LED brightness when running from PD or the battery.

ERC notes: PWR_FLAG on the rails that only connectors and converter outputs drive (`PWR_FLAG_NETS`); in the KiCad-7 symbol
copies (`hardware/common/gen/sym7.py`, `PIN_TYPE`) the second OUT pin of the TPS7A4701 is passive and VOSNS of the LM5176 is
an input, so ERC does not see two power outputs or an output against the PWR_FLAG.

Checks: `tools/sch_netcheck.py hardware/pw-power` - 177 symbol units, 541 pins, 0 mismatches; every symbol pin listed in
`design.py`. ERC by CI.

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
