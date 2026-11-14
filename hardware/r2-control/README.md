# R2 - Control board (rear wall, right part)

The RP2350 of the control board (R85) with everything that is not audio at the rear wall: MIDI, CV/Gate, sync, the internal
USB hub and the control lines to the audio boards. DIN, USB, LAN and DC are panel parts on nuts with cables (R141).
Research and decisions: `docs/ru/34_rear_boards_research.md`, R118, R135-R143. Map of boards: `docs/ru/29_board_map.md`.

**Status: rev 0.4 - schematic and placed board, not routed** (221 parts, 4 layers; 14.11.2026). Rear wall = the 3D model
of panel v7 (R142). MIDI DIN, USB, LAN and DC are panel parts on nuts with short cables (R141, the shelf R2b of rev 0.3 is
dropped): R2 carries the twenty 3.5 mm jacks and six JST PH headers for the DIN cables. Outline: the Control block, rear
x 88-263, z 10-113, without the window behind the DIN sockets (rear x 88-156, z 38-113) - an L, 175 x 103 mm.

| Block | Parts | Notes |
|---|---|---|
| MCU | RP2350A (C42411118), W25Q128JVSIQ (C97521, 16 MB QSPI), 12 MHz ABM8-272-T3 (C20625731), core regulator with 3.3 uH AOTA-B201610S3R3 (C42411119), BOOTSEL button | As Raspberry Pi's minimal design (Hardware design with RP2350) |
| USB hub | USB2514B (C220679), 24 MHz X322524MOB4SI (C70590) | Up: Mini-ITX USB header. Down: 1 RP2350, 2 panel P2 (R86), 3 A1 port A (R82), 4 spare. Straps low by the internal pull-downs = default configuration |
| MIDI DIN | 2 in (TLP2361 at 3.3 V), 4 out; sockets on the wall, one cable each to a JST PH header (out: 3 pins 4, 5, shield; in: 2 pins 4, 5) | CA-033 3.3 V: 33 R 0.5 W + 10 R per output; every output has its own port (R34). Out 3, Out 4 = **Out/Thru** on the panel: Thru from In 1 or In 2 is set in the menu, the RP2350 PIO copies the input bit by bit (microseconds, no CPU), R144 |
| MIDI TRS | 1 in, 2 out: stereo Hroparts PJ-3920-3A (C707259, R143) | Out: tip and ring each from a GPIO through 22 R - type A/B is swapped in firmware (R32). In: two optos back to back, type A and B both work |
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

Board (`gen/make_pcb.py`): F side (jacks only) faces the rear wall; seen from behind, board x = rear x - 88, y = 113 - z.
Jacks at the model positions (axis 0.78 mm below the pad-field centre for the PJ398SM, 1.29 mm for the PJ-3920-3A). On the B side
(inside): the DIN cable headers along the window edge, power/USB/A1/SWD headers along the right edge, the ICs and the parts of
each channel packed next to their IC or jack (`hardware/common/gen/packer.py`). BOOTSEL is on the B side.
MIDI TRS: stereo **PJ-3920-3A** from JLC stock (R143) - pin 1 sleeve, 2 tip, 3 ring per the Flux library: **check the sleeve on a
sample** (tip and ring are swapped in firmware anyway, R32). Mono jacks: PJ398SM on the AudioJack2_SwitchT symbol (S, T, TN).
Panel DIN sockets at a 22 mm pitch (model): pick a panel DIN whose flange fits (e.g. round-flange types), with the enclosure.
Geometry without kicad-cli: `tools/pcb_geomcheck.py hardware/r2-control/r2-control.kicad_pcb` - 0 problems; pins = pads.

Checks: `tools/sch_netcheck.py hardware/r2-control` - rev 0.4 (14.11.2026, PC): 233 symbol units, 677 pins, 0 mismatches against
`design.py`; ERC by CI.


## Rear panel jacks (v3 = 3D model of panel v7, R142)

Sketch: `docs/ru/img/rear_panel_v3.png` / `.svg` (generator `tools/rear_panel.py`; v1, v2 kept). Rear view: x from the left edge as
seen from behind, z from the bottom of the 143 mm rear wall (R44). Inputs framed, outputs filled (R26); labels in English (R45).
Board "panel" = parts on nuts with a cable (R141); "R2" = on this board.

| Jack | Board | Zone | Kind | x (rear view) | z | Panel x | Direction |
|---|---|---|---|---|---|---|---|
| LAN | panel | POWER / USB | lan | 20 | 78 | 495 | io |
| USB-A | panel | POWER / USB | usba | 40 | 80 | 475 | io |
| USB-C (PC) | panel | POWER / USB | usbc | 62 | 80 | 453 | io |
| DC 12-24V | panel | POWER / USB | dc | 22 | 40 | 493 | in |
| ON/OFF | panel | POWER / USB | onoff | 52 | 40 | 463 | in |
| MIDI IN 1 | panel | CONTROL | din | 100 | 82 | 415 | in |
| MIDI OUT 1 | panel | CONTROL | din | 122 | 82 | 393 | out |
| MIDI OUT/THRU 3 | panel | CONTROL | din | 144 | 82 | 371 | out |
| MIDI IN 2 | panel | CONTROL | din | 100 | 52 | 415 | in |
| MIDI OUT 2 | panel | CONTROL | din | 122 | 52 | 393 | out |
| MIDI OUT/THRU 4 | panel | CONTROL | din | 144 | 52 | 371 | out |
| TRS IN | R2 | CONTROL | mini3 | 100 | 22 | 415 | in |
| TRS OUT 1 | R2 | CONTROL | mini3 | 122 | 22 | 393 | out |
| TRS OUT 2 | R2 | CONTROL | mini3 | 144 | 22 | 371 | out |
| CLK OUT 1 | R2 | CONTROL | mini | 172 | 90 | 343 | out |
| CLK OUT 2 | R2 | CONTROL | mini | 189 | 90 | 326 | out |
| RESET OUT | R2 | CONTROL | mini | 206 | 90 | 309 | out |
| CLK IN | R2 | CONTROL | mini | 223 | 90 | 292 | in |
| RESET IN | R2 | CONTROL | mini | 240 | 90 | 275 | in |
| CV IN 1 | R2 | CONTROL | mini | 172 | 68 | 343 | in |
| CV IN 2 | R2 | CONTROL | mini | 189 | 68 | 326 | in |
| CV IN 3 | R2 | CONTROL | mini | 206 | 68 | 309 | in |
| CV IN 4 | R2 | CONTROL | mini | 223 | 68 | 292 | in |
| CV OUT 1 | R2 | CONTROL | mini | 172 | 46 | 343 | out |
| CV OUT 2 | R2 | CONTROL | mini | 189 | 46 | 326 | out |
| CV OUT 3 | R2 | CONTROL | mini | 206 | 46 | 309 | out |
| CV OUT 4 | R2 | CONTROL | mini | 223 | 46 | 292 | out |
| CV OUT 5 | R2 | CONTROL | mini | 172 | 24 | 343 | out |
| CV OUT 6 | R2 | CONTROL | mini | 189 | 24 | 326 | out |
| CV OUT 7 | R2 | CONTROL | mini | 206 | 24 | 309 | out |
| CV OUT 8 | R2 | CONTROL | mini | 223 | 24 | 292 | out |

Generators: `gen/design.py`, `gen/make_sch.py` (shared writer `hardware/common/gen/module_sch.py`, multi-unit symbols placed unit by unit).

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
