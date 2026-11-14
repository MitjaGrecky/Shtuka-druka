# R1 - Audio board (rear wall, left: Audio Out and Audio In blocks)

The audio jacks and the analog front end. Every input leaves R1 as a differential pair scaled to the converters' full scale;
the Cirrus buffers around ADC_VMID / DAC_VMID (AN0635 for the CS5304P/8P inputs, AN0679 for the CS4308P outputs) sit next to the
converters on A1. Research: `docs/ru/34_rear_boards_research.md` (sections 2, 3), doc 28. Decisions: R64-R66, R72, R88,
R116-R118, R135-R137, R142 (jack positions = 3D model).

**Status: rev 0.1 - schematic only** (424 parts, 248 nets, 14.11.2026). Values are a level plan, to be checked (cloud task #24).

## Channels

| Input | Jack | Path | ADC (A1) |
|---|---|---|---|
| Mic/Line 1-2 | Neutrik NCJ6FI-V combo, vertical (C368503) | phantom 6.81k + 47 uF on XLR only (R72); TRS joins after the caps; clamps to +-12 V; OPA1612 two-op-amp front end x 4; OPA1637 loud x 0.137 and quiet x 13.7 (+40 dB) | 1-4 (two per input, R117) |
| Hi-Z 1-2 | Neutrik NJ3FD-V, vertical | 1 MOhm, clamps, OPA1642 buffer; OPA1637 loud x 0.649, quiet x 64.9 | 5-8 |
| Phono L/R | RCA with nut (part to choose) | relay per channel (R118; off = line): line -> OPA1637 x 1; phono -> RIAA on OPA1612 (+40 dB at 1 kHz, approximate network) -> OPA1637 x 1 | 9-10 |
| Line 1-8 | NJ3FD-V | RF filter, OPA1637 diff x 0.162: +24 dBu -> 2 Vrms (R135) | 11-18 |
| Spare (R88) | - | on A1 | 19-20 |

| Output | Path |
|---|---|
| Main L/R, Aux L/R (NJ3FD-V) | DAC pair (2 Vrms diff from the A1 I-V stage) -> OPA1612 difference amp x 3.09 -> +18.2 dBu (R64); hot through 47 R, cold 47 R to GND (impedance-balanced) |
| RCA L/R | copy of Main through 100 R (R23) |
| Relays | Omron G6K-2F-Y 5 V, one DPDT per pair (Main, Aux, RCA): normally open, close only when MUTE and R2_OK are high (R66, R137, R118) |

Phantom per channel (R118): MMBTA92 (300 V PNP) high-side switch from +48 V, base RC for a slow ramp, driven from R2 through an
MMBT3904; 47k bleeder.

Connectors: power from PW (Micro-Fit 2x5, same pinout as PW "to A1/R1"), control from R2 (2x5, same pinout as R2 "to A1/R1"),
to A1: 2x20 (ADC 1-10) and 2x25 (ADC 11-18, DAC 1-4, +-12 V, +5 V) - pairs on adjacent pins with GND pairs between.

## To check (cloud #24, before the board)

- ADC full scale of the CS5308P/CS5304P and the AN0635 buffer gain (assumed 2.0 Vrms differential); the 49.9 R + 1 nF filter.
- Mic front end gain (+12 dB) vs noise and the TRS line level on the combo (a pad may be needed); loud/quiet split +40 dB.
- RIAA network values (approximate 3180/318/75 us) - replace with a computed network.
- Phantom ramp (base RC) and turn-off; MMBTA92 drop.
- Jack mechanics: vertical-mount NCJ6FI-V and NJ3FD-V on a vertical board; RCA part; positions from the 3D model.
- Model vs R118: the model shows a Phono/Line switch on the wall, R118 says R2 switches phono/line (relays here).

Checks: `tools/sch_netcheck.py hardware/r1-audio` - 438 symbol units, 1155 pins, 0 mismatches; every symbol pin listed.
ERC by CI. OPA1637 symbol: project library (`hardware/m1-screen-knobs/gen/make_lib.py`, `opa1637()`).

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
