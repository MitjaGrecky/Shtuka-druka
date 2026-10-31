# Shtuka Druka

An open, standalone desktop music instrument: synthesizer, sampler and DAW in one box.
The idea is improvising with sound from everywhere: capture audio from any source,
then shape it with filters and effects.

Status: design phase. Panel layout v4, enclosure, I/O and compute platform are decided;
a CPU benchmark is running on the first test machine.

## What is here

| Folder | Contents |
|---|---|
| `docs/ru/` | Research and design documents (Russian). Start with `14_decisions_log.md` — the single source of truth for every decision |
| `bench/` | CPU benchmark: how many reference tracks a processor can run at 48 kHz / 128 samples |
| `mockup/` | 1:1 cardboard mockup templates (A4, PDF) and the script that generates them |
| `model3d/` | Interactive 3D model of panel v7, built from `mockup/layout/layout_v7.json` (open `index.html` in a browser; rebuild with `build_model3d_v7.py`) |
| `firmware/protocol/` | Board <-> computer protocol (SDP v0): C header for firmware and host |
| `tools/` | `sdp.py`: reference codec, self-test and frame monitor |
| `hardware/` | Hardware design files (to come) |

## Key facts

- 8x8 RGB pad grid, 16+ tracks (target 32-64), endless encoders with LED rings, 10.1" screen at 30 deg
- Body 515 x 500 mm, 68 mm high at the front, 143 mm at the rear, detachable wrist rest
- Inputs: 2 combo XLR/TRS, 2 Hi-Z, phono with RIAA, 8 line inputs, USB audio, 4 CV
- Outputs: Main and Aux (balanced TRS), RCA copy of Main, 2 headphones
- MIDI: 2 in / 4 out DIN, 1 in / 2 out TRS (type A/B switchable); 8 CV/Gate, sync block, Ableton Link
- Compute: x86 on a Mini-ITX board (Intel N100 to start, 8-core upgrade on the same mounts)
- Panel MCU over USB; audio board over USB Audio Class 2

## Licenses

- Software: GNU AGPL-3.0-or-later (`LICENSE`)
- Hardware: CERN-OHL-S-2.0 (`hardware/LICENSE`)

---

Штука Дрюка — открытый настольный инструмент: синтезатор, сэмплер и DAW в одном корпусе.
Документы проекта на русском лежат в `docs/ru/`, все решения — в `docs/ru/14_decisions_log.md`.
