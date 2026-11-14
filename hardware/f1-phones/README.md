# F1 - Headphone board (front edge, horizontal)

Two 6.35 mm stereo jacks (Neutrik NMJ6HCD2, C368502, right angle, P94: the board lies horizontally, the jacks face the front) and one TI
OPA1622 (C2876559) per jack. Research: `docs/ru/21_audio_board.md`, `docs/ru/34_rear_boards_research.md` (3). Decisions: R8, R66, R67, R87, R137, P94.

**Status: rev 0.1 - schematic only** (52 parts, 14.11.2026).

## Signal path

- A1 sends Phones 1 and 2 as differential pairs from the CS4308P I-V stages (outputs 5-8), 2 Vrms differential full scale. **The volume is
  the DAC's digital attenuator (R87)**: F1 has no potentiometer; Phones 1/2 knobs are read by the panel.
- Each channel is an OPA1622 difference amplifier: 10k in, 20k feedback, 20k to ground (0.1 %), gain 2: 2 Vrms -> **4 Vrms** = R67 (>= 4 V
  on 600 Ohm, peak 5.7 V from +-12 V; 32 Ohm at 30 mA is 0.96 V, the OPA1622 gives +145 / -130 mA). 22 pF across the feedback resistor.
  The DAC mid-rail (DAC_VMID) cancels in the difference; check the residual DC offset on the prototype (no coupling capacitors).
- Output: 10 R build-out (feedback taken before it) -> G6K-2 relay contact -> jack tip / ring; sleeve to GND.
- **Mute (R66, R137):** one DPDT G6K-2 per jack, normally open, closes only when MUTE and R2_OK are both high (the same 2 x 2N7002 logic as the
  output relays on R1). The OPA1622 enable pin follows MUTE through 1k / 100k: held low while R2 boots (thresholds 0.78 / 0.82 V against the
  device ground, datasheet 7.3.3 and 7.4.2); it is not a high-impedance output, so the relay is the real mute.

## Connectors (contract with the other boards)

| J | From | Pins |
|---|---|---|
| from A1, 2x6 2.54 mm | A1 (to design) | 1 HP1 L+, 2 HP1 L-, 3 GND, 4 HP1 R+, 5 HP1 R-, 6 GND, 7 HP2 L+, 8 HP2 L-, 9 GND, 10 HP2 R+, 11 HP2 R-, 12 GND (twisted pairs) |
| from PW, JST PH 4 | PW rev 0.5 "to F1" | +12V, GND, -12V, +5V (relay coils) |
| from R1 (mute), JST PH 3 | R1 rev 0.4 "to F1 (mute)" | MUTE, R2_OK, GND |

## To check

- OPA1622 stability on a long headphone cable with the 22 pF / 10 R and relay; EN pin timing against the relay (the relay needs ~3 ms).
- Difference amplifier CMRR (0.1 % resistors) and the common-mode voltage of the A1 pair; DC offset at the jack.
- Board geometry: NMJ6HCD2 is 18.2 x 15.67 mm (doc 32); jack positions from the 3D model (x 32 and 80 on the slope front).

Checks: `tools/sch_netcheck.py hardware/f1-phones` - 56 symbol units, 157 pins, 0 mismatches; every symbol pin listed. ERC by CI.
Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).
