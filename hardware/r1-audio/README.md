# R1 - Audio board (rear wall, left: Audio Out and Audio In blocks)

The audio jacks and the analog front end. Every input leaves R1 as a differential pair scaled to the converters' full scale;
the Cirrus buffers around ADC_VMID / DAC_VMID (AN0635 for the CS5304P/8P inputs, AN0679 for the CS4308P outputs) sit next to the
converters on A1. Research: `docs/ru/34_rear_boards_research.md` (sections 2, 3), doc 28. Decisions: R64-R66, R72, R88,
R116-R118, R135-R137, R142 (jack positions = 3D model).

**Status: rev 0.8 (18.11.2026) - schematic and placed board, not routed** (452 parts, 264 nets; Mic/Line attenuator relays since rev 0.3, user decision on В16). Levels and values checked against the datasheets (cloud task #24).

## Channels

| Input | Jack | Path | ADC (A1) |
|---|---|---|---|
| Mic/Line 1-2 | Neutrik NCJ6FI-V combo, vertical (C368503) | phantom 6.81k + 47 uF on XLR only (R72); TRS joins after the caps; clamps to +-12 V; relay attenuator -12 dB (rev 0.3); OPA1612 two-op-amp front end x 4.01; OPA1637 loud x 0.681 (FS +11.9 dBu) and quiet x 68.1 (+40 dB, FS -28.1 dBu) | 1-4 (two per input, R117) |
| Hi-Z 1-2 | Neutrik NJ3FD-V, vertical | 1 MOhm, clamps, OPA1642 buffer; OPA1637 loud x 1.37 (FS +17.9 dBu), quiet x 137 (+40 dB, FS -22.1 dBu) | 5-8 |
| Phono L/R | RCA with nut (part to choose) | relay per channel (R118; off = line): line -> OPA1637 x 4.12 (FS +8.3 dBu); phono -> computed RIAA on OPA1612 (+35 dB at 1 kHz) -> OPA1637 x 4.12 | 9-10 |
| Line 1-8 | NJ3FD-V | RF filter, OPA1637 diff x 0.674: FS +24.1 dBu (R135) | 11-18 |
| Spare (R88) | - | on A1 | 19-20 |

| Output | Path |
|---|---|
| Main L/R, Aux L/R (NJ3FD-V) | DAC pair (2 Vrms diff from the A1 I-V stage) -> OPA1612 difference amp x 3.09 -> 6.19 Vrms = +18.0 dBu (R64); hot through 47 R, cold 47 R to GND (impedance-balanced) |
| RCA L/R | copy of Main through 100 R (R23) |
| Relays | Omron G6K-2F-Y 5 V, one DPDT per pair (Main, Aux, RCA): normally open, close only when MUTE and R2_OK are high (R66, R137, R118) |

Phantom per channel (R118): MMBTA92 (300 V PNP) high-side switch from +48 V, slow ramp by a Miller capacitor (2.2 uF base-collector), driven from R2 through an
MMBTA42 (300 V NPN, the collector sees 48 V); 47k bleeder.

Connectors: power from PW (Micro-Fit 2x5, same pinout as PW "to A1/R1"), control from R2 (2x7: the 2x5 pinout of R2 "to A1/R1" plus ATT1 at pin 11 and ATT2 at pin 13, GND between; R2 must be widened - PC task #25),
to A1: 2x20 (ADC 1-10) and 2x25 (ADC 11-18, DAC 1-4, +-12 V, +5 V) - pairs on adjacent pins with GND pairs between.

## Level plan (checked, rev 0.2)

Sources: CS53A04P datasheet DS1397 (same family as CS5304P/8P), CS4308P DS1317, Cirrus AN0635 and AN0679.

- **ADC:** 0 dBFS = 2.0 Vrms differential at the ADC pins (scales with VDD_A). The recommended AN0635 input buffer (inverting, 1.2k in /
  300 R feedback, 68 uF per leg, OPA1612) has gain 1/4: 0 dBFS = **8 Vrms differential** at the buffer. Rev 0.1 assumed 2 Vrms - every
  gain is now x 4.17 higher. With the 49.9 R build-out the R1 driver must deliver 8.33 Vrms differential at full scale.
  The 49.9 R + 1 nF filter: 1.6 MHz differential, fine ahead of the buffer's own 640 kHz filter; C0G.
- **Line 1-8:** gain 6.81k / (10k + 100 R) = 0.674, FS at +24.1 dBu (R135). Input 100 R + 1 nF (RF, 1.6 MHz). No clamps (a clamp to +-12 V
  would clip +24 dBu = 17 Vpk); the OPA1637 inputs see only the Rg current.
- **Mic/Line:** front end 1 + 2 x 499 / 332 = 4.01 (+12 dB) - the 332 R gives thermal noise 2.3 nV/rtHz instead of 3.3 with 665 R. The front end clips at
  about +13.6 dBu (+-10.5 V on each output), so FS of the loud path is set to +11.9 dBu: **no pad is needed**, the loud path has 1.7 dB headroom
  over line level; a line signal above +13.6 dBu on the combo clips (question to the user). Quiet path +40 dB higher, FS -28.1 dBu; the 1k Rg
  keeps the fault current into the OPA1637 below 10 mA.
- **Attenuator (rev 0.3, В16 b):** one G6K-2F-Y per combo after the phantom caps and the 10 R, in front of the clamps and the front end: 15k series + 4.99k shunt per leg
  (ratio 0.250 = -12.0 dB, 0.1 %). De-energised = direct (mic), energised = attenuated: FS of the loud path +23.9 dBu; the clamps see
  only the attenuated signal. Control: ATT1/ATT2 from R2 (3.3 V) through a 2N7002, flyback diode per coil. In the direct position the divider loads each leg with 20k
  (parallel to the 10k bias: 6.7k per leg, 13 k differential) - fine for microphones; the divider adds 7.8 nV/rtHz only while attenuated.
- **Hi-Z:** OPA1642 buffer, then x 1.37 / x 137 (FS +17.9 / -22.1 dBu). The JFET buffer keeps the 1 MOhm input.
- **Phono:** FS of the line path +8.3 dBu (2.02 Vrms, CD level). RIAA computed (script in the cloud task, `docs/ru/` note): active stage 3180 / 318 us
  (68.1k || 47n in series with 7.42k, over 130 R + 470 uF), 75 us as a passive section 787 R + 100 nF ahead of the FDA (input 16.7 k).
  Gain +35.0 dB at 1 kHz, **error below 0.05 dB from 20 Hz to 20 kHz** (nominal values), FS 36 mV at 1 kHz (7 x the 5 mV of a normal MM
  cartridge); corner of the 130 R + 470 uF leg 2.6 Hz (the subsonic rolloff is left to the DSP). 0.1 % resistors and 1 % C0G capacitors give
  about +-0.1 dB.
- **Outputs:** CS4308P current-mode output 1.67 mA rms (1.63-1.71) per channel; AN0679 I-V stage 1.2 kOhm gives 2.0 Vrms differential
  (the A1 stage, not R1). R1: x 3.09 -> 6.19 Vrms = +18.0 dBu per channel, impedance-balanced (cold 47 R).
- **Phantom:** MMBTA92 + Miller capacitor 2.2 uF between base and collector: base current 0.45 mA from the 100k, ramp about 0.1-0.2 s
  (X7R loses capacity at 48 V, 1-2 uF effective); Vce(sat) < 0.5 V at 14 mA (both legs shorted); turn-off through the 100k pull-up
  and the 47k bleeder. Estimated, not simulated. The level shifter is the MMBTA42 (300 V): the old MMBT3904 (40 V) sees 48 V on its
  collector when off.

## Still open

- Mic EIN: front end 2.3 nV/rtHz plus the 6.81k phantom resistors (about 3.3 nV/rtHz each in parallel to the capsule) - about -125 dBu EIN estimated,
  to measure on the first board; the quiet path reaches ADC FS at -28.1 dBu, so the ADC noise floor (123 dBA) is -95 dBu referred to the input.
- Jack mechanics: vertical-mount NCJ6FI-V and NJ3FD-V on a vertical board; RCA part; positions from the 3D model.
- Model vs R118: the model shows a Phono/Line switch on the wall, R118 says R2 switches phono/line (relays here).
- The A1 buffers (AN0635, AN0679) are on A1: R1 only assumes them.

Rev 0.4 (14.11.2026, PC): JST PH 3 "to F1 (mute)" with MUTE, R2_OK, GND for the headphone board.

Checks: `tools/sch_netcheck.py hardware/r1-audio` - 440 symbol units, 1159 pins, 0 mismatches; every symbol pin listed.
ERC by CI. OPA1637 symbol: project library (`hardware/m1-screen-knobs/gen/make_lib.py`, `opa1637()`).

Generators: `gen/design.py`, `gen/make_sch.py`. On the PC set `KICAD_SYMBOL_DIR=<repo>/hardware/common/sym7`.

License: CERN-OHL-S-2.0 (hardware), AGPL-3.0-or-later (scripts).

## Rev 0.5: placed board for routing (14.11.2026, PC)
Placed board (no routing) generated by `gen/make_pcb.py`; `UNROUTED` marker for CI; package `hardware/for-routing/R1`. Placement is a starting point: jacks at the 3D-model positions, the rest by `hardware/common/gen/autoplace.py` (ICs on a grid, small parts around the IC they share signals with, cable headers along the bottom edge). Outline and mounting holes are rough until the enclosure is fixed. `pcb_geomcheck`: 0 problems.

Rev 0.6 (17.11.2026, R171): A1 headers J4 / J5 raised by 19 mm for A1 on a tray above the battery (R162); superseded by rev 0.7. Mounting hole H5 at (34, 86), back at (34, 79) in rev 0.7.

Rev 0.7 (17.11.2026, R179): A1 now stands on the floor on about 10.7 mm standoffs (R174, green-2 line), so the A1 headers J4 / J5 are raised by `A1_RISE` = 5.1 mm instead of 19 mm (A1 socket rows about 16.6 / 19.1 mm above the floor; estimate +-1 mm, check against the socket drawing). Mounting hole H5 back at (34, 79). EasyEDA R1_v6: 452/452 parts, 264/264 nets.

Rev 0.8 (18.11.2026, rear wall v6 (audio as in v5.2), doc 41 sections 24.2 / 24.4): jack axes on the grid rows z 99 / 73 / 47 (rear x = r): Main L / R r 292 / 314 (z 99), Aux (73), RCA (47); Mic/Line 1 / 2 r 362 / 394 (z 99), Hi-Z 1 / 2 (73); Phono L / R r 434 / 456 (z 99); Line 1-4 r 434 / 456 / 478 / 500 (73), Line 5-8 (47). The XLR row z 99 stands above the old board top (104), so the top edge is raised to z 117 (`Z0` = 117, `H` = 109; the W1 U3 limit is about 117.4, the XLR courtyard sticks out 0.2 mm above the edge) and the bottom edge stays at z 8; the A1 headers and the bottom mounting holes moved down by 13 mm in board coordinates (same height above the floor), the RCA / Phono standoff holes follow the new jack positions. Phono GND post and Ph/Line switch (r 478 / 500, z 99) are not on R1 (panel parts, as before). Fit model (`model3d/fit/fit_model.py`, `R1_TOP` = 117; 1 tight spot to W1 under 1 mm): 0 collisions with A1 and the batteries (R1 is a vertical board at the wall, depth unchanged). EasyEDA not verified for rev 0.8.

## Rev 0.9: phantom hot-plug (audit 18.11.2026)
Unbalanced XLR (pin 3 to shield) plugged with phantom on moved the far side of the charged 47 uF cap to about -46 V; the 10 R + 1N4148W clamps took about 3.5 A / 0.5 ms and pulled the -12 V rail. Now each Mic/Line leg has an **SMBJ18CA** (Littelfuse C83327) from the cap's far side to GND (18 V standoff, above the +24 dBu TS peak 17.4 V) and the series resistor is **47 R 0805** (was 10 R): tail 0.2 A / 1.5 ms, 7.6 mJ. Test on the bench with a pin-3-to-shield cable and phantom on. Noise: +1 dB at 150 R.
Same rev 0.9: the MUTE / R2_OK series FETs of the output relays 2N7002 -> **AO3400A** (C20917): three G6K-2F-Y coils (21 mA, must operate 4.0 V) through two 2N7002 at Vgs 3.3 V left 3.8-4.0 V at +5 V -5 %. The single-FET ATT and PHONO coil drivers stay 2N7002 (one coil, 0.1 V drop).

EasyEDA (18.11.2026, PC, rev 0.9): project `R1_v7`: parts 456 / 456, nets 264 / 264 (PCB and schematic), LCSC written (120 sch / 106 pcb) and re-checked, positions 456 / 456, saved. DRC and parity left to CI.

Rev 1.0 (19.11.2026, rear wall v6.1, `docs/ru/img/41_rear_v6_1_jacks.csv`, doc 41 section 24): the rows shift by -4 to z 95 / 69 / 43 (x unchanged: Main/Aux/RCA r 292 / 314, Mic/Line and Hi-Z r 362 / 394, Phono / Line r 434-500). The top edge goes down from 117 to 113 so R1 clears the shelf / cover that starts at z 114 (`Z0` = 113, `H` = 105, bottom edge stays z 8); the bottom mounting holes moved up by 4 mm in board coordinates. Fit model (`R1_TOP` = 113): 0 collisions, 0 tight spots. EasyEDA not verified for rev 1.0.
