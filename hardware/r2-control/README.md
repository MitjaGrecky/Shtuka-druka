# R2 - Control board (rear wall, right part)

The RP2350 of the control board (R85) with everything that is not audio at the rear wall: MIDI, CV/Gate, sync, the internal
USB hub, the rear USB-C (to a computer) and USB-A, the power jacks and the control lines to the audio boards.
Research and decisions: `docs/ru/34_rear_boards_research.md`, R118, R135-R138. Map of boards: `docs/ru/29_board_map.md`.

**Status: rev 0.2 - schematic only** (232 parts, 169 nets; rev 0.2 = checked against the datasheets, 14.11.2026, see below). The board outline and the jack positions follow the rear panel
layout (doc 13, section 3.5), which is not drawn yet; the 5-pin DIN footprint (CUI SDS-50J, LCSC C6216157), the locking
DC jack and a 5 A USB-C receptacle for PD are chosen together with it.

| Block | Parts | Notes |
|---|---|---|
| MCU | RP2350A (C42411118), W25Q128JVSIQ (C97521, 16 MB QSPI), 12 MHz ABM8-272-T3 (C20625731), core regulator with 3.3 uH AOTA-B201610S3R3 (C42411119), BOOTSEL button | As Raspberry Pi's minimal design (Hardware design with RP2350) |
| USB hub | USB2514B (C220679), 24 MHz X322524MOB4SI (C70590) | Up: Mini-ITX USB header. Down: 1 RP2350, 2 panel P2 (R86), 3 A1 port A (R82), 4 spare. Straps low by the internal pull-downs = default configuration |
| Rear USB-C (PC) | HRO TYPE-C-31-M-12, 5.1k Rd, USBLC6-2SC6 | Passed to A1 port B (isolated there by ADuM4166) |
| Rear USB-A | Molex 67643, USBLC6-2SC6 | Passed to a Mini-ITX USB header (R80) |
| Power jacks | USB-C PD, DC 12-24 V | Passed to PW on a 2x5 header; PD sink (TPS25730), protection and source selection are on PW |
| MIDI DIN | 2 in (TLP2361 at 3.3 V), 4 out | CA-033 3.3 V: 33 R 0.5 W + 10 R per output; every output has its own port (R34) |
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

Checks: `tools/sch_netcheck.py hardware/r2-control` - rev 0.2 (14.11.2026, cloud): 244 symbol units, 763 pins, 0 mismatches against
`design.py`; ERC by CI.


## Rear panel jacks (proposal v1, 14.11.2026 - not decided)

Sketch: `docs/ru/img/rear_panel_v1.png` / `.svg` (generator `tools/rear_panel.py`). Rear view: x from the left edge as seen from
behind (R2 zone x 5-263 = panel x 252-510), z from the bottom of the 143 mm rear wall (R44); jack tops below ~116 mm (doc 13, 3.6).
Inputs framed, outputs filled (R26); labels in English (R45), CLK = clock. Board coordinates follow once the layout is decided
(open questions V12, V13 in `notes/handoff.md`): the DIN-5 SDS-50J, both USB-C, the USB-A Molex 67643 and the DC jack in rev 0.2
are right-angle parts and do not face out of a vertical board.

| Jack | Zone | Kind | x (rear view) | z | Panel x | Direction |
|---|---|---|---|---|---|---|
| DC 12-24V | POWER / USB | dc | 18 | 35 | 497 | in |
| USB-C PD | POWER / USB | usbc | 46 | 35 | 469 | in |
| USB-C PC | POWER / USB | usbc | 18 | 70 | 497 | io |
| USB-A | POWER / USB | usba | 46 | 70 | 469 | io |
| MIDI IN 1 | MIDI | din | 84 | 70 | 431 | in |
| MIDI IN 2 | MIDI | din | 84 | 35 | 431 | in |
| MIDI OUT 1 | MIDI | din | 108 | 70 | 407 | out |
| MIDI OUT 2 | MIDI | din | 132 | 70 | 383 | out |
| MIDI OUT 3 | MIDI | din | 108 | 35 | 407 | out |
| MIDI OUT 4 | MIDI | din | 132 | 35 | 383 | out |
| TRS IN | MIDI | mini | 158 | 80 | 357 | in |
| TRS OUT 1 | MIDI | mini | 158 | 55 | 357 | out |
| TRS OUT 2 | MIDI | mini | 158 | 30 | 357 | out |
| CV IN 1 | CV / SYNC | mini | 184 | 80 | 331 | in |
| CV IN 2 | CV / SYNC | mini | 198.5 | 80 | 316.5 | in |
| CV IN 3 | CV / SYNC | mini | 213 | 80 | 302 | in |
| CV IN 4 | CV / SYNC | mini | 227.5 | 80 | 287.5 | in |
| CLK IN | CV / SYNC | mini | 242 | 80 | 273 | in |
| RESET IN | CV / SYNC | mini | 256.5 | 80 | 258.5 | in |
| CV OUT 1 | CV / SYNC | mini | 184 | 55 | 331 | out |
| CV OUT 2 | CV / SYNC | mini | 198.5 | 55 | 316.5 | out |
| CV OUT 3 | CV / SYNC | mini | 213 | 55 | 302 | out |
| CV OUT 4 | CV / SYNC | mini | 227.5 | 55 | 287.5 | out |
| CV OUT 5 | CV / SYNC | mini | 242 | 55 | 273 | out |
| CV OUT 6 | CV / SYNC | mini | 256.5 | 55 | 258.5 | out |
| CV OUT 7 | CV / SYNC | mini | 184 | 30 | 331 | out |
| CV OUT 8 | CV / SYNC | mini | 198.5 | 30 | 316.5 | out |
| CLK OUT 1 | CV / SYNC | mini | 213 | 30 | 302 | out |
| CLK OUT 2 | CV / SYNC | mini | 227.5 | 30 | 287.5 | out |
| RESET OUT | CV / SYNC | mini | 242 | 30 | 273 | out |

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`, multi-unit symbols placed unit by unit).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
