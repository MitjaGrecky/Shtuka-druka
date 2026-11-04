# Handing M1 to an external layout service (Quilter or similar)

Everything that the panel fixes is **locked** in the board file. A service may move only the
unlocked parts (U1-U5, resistors, capacitors) and must keep these rules:

| What | Rule |
|---|---|
| Locked parts | ENC1-8 (knob row, 28 mm pitch), D1-D104 (ring LEDs), J1 (bus connector), H1-H4 |
| Top side (F.Cu) | only encoders and ring LEDs; no other parts (the light guide sits on it) |
| Under encoder bodies | no tracks, no vias on any layer (rule areas `under_encoder_*`): the encoder frame is the touch electrode |
| In1.Cu | GND plane, cut out under each encoder frame (x +-6 mm, y +-8 mm around the shaft) |
| Stack-up | 4 layers, 1.6 mm, JLCPCB standard |
| Net classes | Default: track 0.12, clearance 0.13, via 0.45/0.2 mm. Power (+5V, GND): track 0.3 mm |
| Fab limits (JLCPCB 4-layer) | track/space >= 0.09 mm, via drill >= 0.2 mm, via hole to track >= 0.254 mm, copper to edge >= 0.3 mm |
| Touch lines | TOUCH0-7 from R7-R14 to each encoder MP pin: short, away from SW/CS lines where possible |
| LED driver U1 | IS31FL3741A, QFN-60 0.4 mm; thermal vias in the exposed pad; keep its decoupling (C1-C4) close |

Inputs: `m1-screen-knobs.kicad_sch`, `m1-screen-knobs.kicad_pcb`, `m1-screen-knobs.kicad_pro`, `lib/`.
Output wanted: the routed `.kicad_pcb` (same nets), which CI then checks with KiCad 10 (DRC with schematic parity).
