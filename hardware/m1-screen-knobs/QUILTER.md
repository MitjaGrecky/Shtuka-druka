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

Inputs: run `gen/make_quilter.py OUT` - three jobs: `A_route_only` (our placement, routing only), `B_place_and_route` (only panel-fixed parts inside the outline) and `C_small_parts_free` (our placement, ICs and passives may move: anywhere on the bottom, on the top only inside two free strips). Upload the three files of one job: `.kicad_pcb`, `.kicad_sch`, `.kicad_pro` (no zip).
Output wanted: the routed `.kicad_pcb` (same nets), which CI then checks with KiCad 10 (DRC with schematic parity).

Each job folder also gets `bypass_capacitors.csv`, `high_current_nets.csv` and `ground_nets.csv` for the
Circuit Comprehension step ("Upload CSV"); column names follow Quilter's own CSV export.

## Fixed and movable (map: `mech/m1_fixed_vs_movable.png`)

| Group | Parts | Rule |
|---|---|---|
| Locked (the panel decides) | ENC1-8, D1-D104, J1, H1-H4 (117 parts) | never move |
| Movable (job C) | R1-R18, RN1-RN6, C1-C13 (37 parts), start below the board | Quilter places them next to their ICs |
| Anchors (job C) | U1-U5 | locked inside the outline; parts inside the outline are pre-placed for Quilter |
| Top (job C) | strips "Top strip rear" 211 x 5.1 mm (y 0.8-5.9) and "Top strip front" 211 x 2.4 mm (y 30.8-33.2) | small SMD only (0402, 0805, RN) |
| Top, everything else | rule area "Top: locked parts only" (footprints disallowed) | nothing new |

Why the top is free in the strips: the light guide is 6.4 mm thick and every movable part is at most 1.2 mm high
(0402, 0805, TSSOP-16). The guide gets a groove from below over the strips (like the J1 pocket), made from the final
placement. The strips follow from a free-space map: ring LED + 2 mm wall, encoder cut-out + 0.8 mm, screw head r 3.5 mm
and 0.8 mm board edge are blocked. U1 (7 x 7 mm QFN) and the 74HC165 (legs 6.4 mm) do not fit the 5.1 mm strip: ICs stay on the back.
Top and bottom regions are a union for the parts assigned to both (Quilter: two-sided region).

Job A result (Nov 6, 1h 28m): 1 candidate, 12 incomplete nets, 8 of 13 bypass capacitors flagged.

## What we learned on app.quilter.ai (November 2026)

- No public API, SDK, CLI or MCP: the web app is the only way in.
- Settings of a step are saved only by its **Continue** button; jumping to another step by URL drops them.
- "Replace Files" makes a new draft and offers to copy settings from the old one. Copying **Floorplan**
  overwrote the placement regions parsed from the new file; stack-up and fab limits were not copied at all.
- KiCad placement region: a rule area on B.Cu with every keep-out item allowed. It shows up in Floorplan,
  parts are added to it by reference.
- A rule area on F.Cu with only footprints disallowed is read as a top-side component keep-out.
- "Prefer single-sided layouts" means **top side only**.
- Job B (parts to be placed on the back only) failed after 8 minutes: "one of your components is too large
  for Quilter to place within this board area". Quilter did not try the back side, so for M1 use job A.
