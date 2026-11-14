# R2 - Control board (rear wall, right part)

The RP2350 of the control board (R85) with everything that is not audio at the rear wall: MIDI, CV/Gate, sync, the internal
USB hub and the control lines to the audio boards. The DIN, USB and power jacks are on the shelf R2b below (R139).
Research and decisions: `docs/ru/34_rear_boards_research.md`, R118, R135-R140. Map of boards: `docs/ru/29_board_map.md`.

**Status: rev 0.3 - schematic only** (216 parts, 157 nets). Rev 0.2 = checked against the datasheets (14.11.2026, cloud, see below);
rev 0.3 = the right-angle jacks (MIDI DIN x 6, USB-C PC, USB-A, USB-C PD, DC) moved to the jack shelf **R2b**
(`hardware/r2b-jacks`, R139) with their ESD and cables; R2 keeps the MIDI parts and gets a 2x7 comb socket to R2b.

| Block | Parts | Notes |
|---|---|---|
| MCU | RP2350A (C42411118), W25Q128JVSIQ (C97521, 16 MB QSPI), 12 MHz ABM8-272-T3 (C20625731), core regulator with 3.3 uH AOTA-B201610S3R3 (C42411119), BOOTSEL button | As Raspberry Pi's minimal design (Hardware design with RP2350) |
| USB hub | USB2514B (C220679), 24 MHz X322524MOB4SI (C70590) | Up: Mini-ITX USB header. Down: 1 RP2350, 2 panel P2 (R86), 3 A1 port A (R82), 4 spare. Straps low by the internal pull-downs = default configuration |
| Comb to R2b (2x7) | MIDI DIN out 1-4 pins 4/5, in 1-2 pins 4/5, GND x 2 | R139: the DIN, USB and power jacks sit on R2b; USB and power go from R2b straight to A1, the Mini-ITX and PW |
| MIDI DIN | 2 in (TLP2361 at 3.3 V), 4 out; jacks on R2b | CA-033 3.3 V: 33 R 0.5 W + 10 R per output; every output has its own port (R34) |
| MIDI TRS | 1 in, 2 out | Out: tip and ring each from a GPIO through 22 R - type A/B is swapped in firmware (R32). In: two optos back to back, type A and B both work |
| CV/Gate out 1-8 | 2 x DAC80504RTET (C2862796; internal 2.5 V ref divided by 2, gain 2 = 0-2.5 V), 3 x OPA4197 (C2057327) on +-12 V | Vout = 8.06 (Vdac - 1.25 V) = -10.1 ... +10.1 V around a buffered REF/2; reset to mid-scale = 0 V; 1k output resistors. Step 0.31 mV = 0.37 cent at 1 V/oct |
| CV in 1-4 | RP2350 ADC0-3 | -10 ... +10 V -> 0 ... 3.03 V (100k / 33k to 3.3 V / 39k to GND), BAT54S clamp |
| Sync | 3 out, 2 in | Out: GPIO -> op-amp x1.51 -> 0 / +5 V. In: NPN inverter, 22k / 100k, negative clamp |
| To A1/R1 (2x5) | PH48_1, PH48_2, PHONO, MUTE, R2_OK | Pulled low while booting; the output relays (R137) open when R2 stops |

GPIO map (all 30 used): 0-3 MIDI TX 1-4, 4-5 MIDI RX 1-2, 6-9 TRS out 1-2 tip/ring, 10-11 TRS in A/B, 12 MUTE,
13 R2_OK (+ status LED), 14-17 DAC SCK, SDI, CS1, CS2, 18-20 clock out 1, 2, reset/run out, 21-22 clock in, reset/run in,
23-24 phantom 1-2, 25 phono/line, 26-29 CV in 1-4.

Datasheet check (rev 0.2, 14.11.2026; table in `notes/handoff.md`, report #20): RP2350 per the minimal design; DAC80504 GAIN high = x2,
RSTSEL high = mid-scale, **REFDIV high** (with the internal 2.5 V reference undivided the DAC needs VDD >= 5.0 V and raises a
reference alarm, all outputs 0 V, below that); USB2514B straps by the internal pull-downs, CRFILT/PLLFILT 100 nF, VBUS_DET 100k/100k.
Still without an LCSC number: the 0.1 % resistors (10k, 80.6k), the 1206 33 R 0.5 W, the passives in general (chosen at the BOM).

Checks: `tools/sch_netcheck.py hardware/r2-control` - rev 0.3 (14.11.2026, PC): 228 symbol units, 675 pins, 0 mismatches against
`design.py`; ERC by CI.


## Rear panel jacks (v2, 14.11.2026: R140 base v1 + R139 shelf)

Sketch: `docs/ru/img/rear_panel_v2.png` / `.svg` (generator `tools/rear_panel.py`; v1 kept). Rear view: x from the left edge as seen
from behind (R2 zone x 5-263 = panel x 252-510), z from the bottom of the 143 mm rear wall (R44); jack tops below ~116 mm (doc 13, 3.6).
Inputs framed, outputs filled (R26); labels in English (R45), CLK = clock. R2b = horizontal shelf at the bottom (z 1-36, right-angle
jacks in one row); R2 = vertical board above it (z 38-113, PJ398SM). Positions are estimates until the parts and the board are drawn.

| Jack | Board | Zone | Kind | x (rear view) | z | Panel x | Direction |
|---|---|---|---|---|---|---|---|
| DC 12-24V | R2b | POWER / USB | dc | 12 | 18 | 503 | in |
| USB-C PD | R2b | POWER / USB | usbc | 30 | 18 | 485 | in |
| USB-C PC | R2b | POWER / USB | usbc | 48 | 18 | 467 | io |
| USB-A | R2b | POWER / USB | usba | 67 | 18 | 448 | io |
| MIDI IN 1 | R2b | MIDI DIN | din | 92 | 18 | 423 | in |
| MIDI IN 2 | R2b | MIDI DIN | din | 115 | 18 | 400 | in |
| MIDI OUT 1 | R2b | MIDI DIN | din | 140 | 18 | 375 | out |
| MIDI OUT 2 | R2b | MIDI DIN | din | 163 | 18 | 352 | out |
| MIDI OUT 3 | R2b | MIDI DIN | din | 186 | 18 | 329 | out |
| MIDI OUT 4 | R2b | MIDI DIN | din | 209 | 18 | 306 | out |
| TRS IN | R2 | MIDI TRS | mini | 92 | 98 | 423 | in |
| TRS OUT 1 | R2 | MIDI TRS | mini | 92 | 76 | 423 | out |
| TRS OUT 2 | R2 | MIDI TRS | mini | 92 | 54 | 423 | out |
| CV IN 1 | R2 | CV / SYNC | mini | 140 | 98 | 375 | in |
| CV IN 2 | R2 | CV / SYNC | mini | 160 | 98 | 355 | in |
| CV IN 3 | R2 | CV / SYNC | mini | 180 | 98 | 335 | in |
| CV IN 4 | R2 | CV / SYNC | mini | 200 | 98 | 315 | in |
| CLK IN | R2 | CV / SYNC | mini | 220 | 98 | 295 | in |
| RESET IN | R2 | CV / SYNC | mini | 240 | 98 | 275 | in |
| CV OUT 1 | R2 | CV / SYNC | mini | 140 | 76 | 375 | out |
| CV OUT 2 | R2 | CV / SYNC | mini | 160 | 76 | 355 | out |
| CV OUT 3 | R2 | CV / SYNC | mini | 180 | 76 | 335 | out |
| CV OUT 4 | R2 | CV / SYNC | mini | 200 | 76 | 315 | out |
| CV OUT 5 | R2 | CV / SYNC | mini | 220 | 76 | 295 | out |
| CV OUT 6 | R2 | CV / SYNC | mini | 240 | 76 | 275 | out |
| CV OUT 7 | R2 | CV / SYNC | mini | 140 | 54 | 375 | out |
| CV OUT 8 | R2 | CV / SYNC | mini | 160 | 54 | 355 | out |
| CLK OUT 1 | R2 | CV / SYNC | mini | 180 | 54 | 335 | out |
| CLK OUT 2 | R2 | CV / SYNC | mini | 200 | 54 | 315 | out |
| RESET OUT | R2 | CV / SYNC | mini | 220 | 54 | 295 | out |

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`, multi-unit symbols placed unit by unit).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
