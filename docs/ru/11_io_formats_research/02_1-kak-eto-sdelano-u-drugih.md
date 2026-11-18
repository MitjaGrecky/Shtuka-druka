> Часть документа 11 ([индекс](../11_io_formats_research.md)): 1. Как это сделано у других

## 1. Как это сделано у других

| Устройство | Входы | Выходы | MIDI | CV/Gate | USB, сеть |
|---|---|---|---|---|---|
| MPC XL | 6: 2 комбо с предусилителями и фантомом, 2 инструментальных, фоно | 8 линейных | 2 вх / 4 вых | 16 (8 стерео-гнёзд 3,5 мм) | 3×USB-A, USB-C (24 канала аудио) ([Perfect Circuit](https://www.perfectcircuit.com/m2e/akai-mpc-xl.html)) |
| MPC Live III | 2 комбо XLR/TRS с фантомом; стерео-фоно (по MusicTech; Gearnews называет их RCA-входами); встроенный микрофон | 3 стереопары | 2 комплекта вх/вых | 4 гнезда TRS = 8 сигналов | USB-C (24 канала), 2×USB-A, Wi-Fi, BT, без Ethernet ([Gearnews](https://www.gearnews.com/akai-mpc-live-iii-review/), [MusicTech](https://musictech.com/reviews/studio-recording-gear/akai-mpc-live-iii-review/), [Thomann](https://www.thomannmusic.com/akai_professional_mpc_live_iii_case_bundle.htm)) |
| Akai Force | 2 комбо с фантомом и режимом инструмента | 4 | Мини-джеки 3,5 мм с переходниками | 4 | 3×USB, Ethernet, Wi-Fi, BT; SD и наушники спереди ([Bonedo](https://www.bonedo.de/artikel/akai-force-test/)) |
| Push 3 | 2 линейных/инструментальных; ADAT | 2 + наушники; ADAT | Мини-джеки | 4 + 2 гибких (педаль или CV) | USB-C (10 × 12 каналов, до 96 кГц) ([Thomann](https://www.thomann.de/be/ableton_push_3_standalone_live_std.htm)) |
| Elektron Tonverk | 2 | 4 + наушники | Вх/вых/thru | — | 2×USB-C, SD ([MusicRadar](https://www.musicradar.com/music-tech/samplers/elektron-tonverk-review)) |
| Behringer Kick | Стерео | Стерео + наушники спереди | DIN вх/вых | 4 | USB-C, USB-A, LINK (RJ45), SD, 12 В ([GitHub](https://github.com/MusicTribeOpenSource/0700-AAM/blob/main/README.md)) |
| Torso S-4 | Стерео 6,3 мм + встроенный микрофон | Стерео + наушники | Мини-джеки + аналоговый клок | — | USB-C, 4 ГБ внутри, без SD ([SoS](https://www.soundonsound.com/reviews/torso-electronics-s-4)) |
| MPC Sample | 2 TRS, USB-аудио, встроенный микрофон | 2 TRS + наушники 3,5 мм | Вх/вых + Sync Out | — | USB-C, microSD; постоянный буфер 25 с ([MusicRadar](https://www.musicradar.com/music-tech/samplers/the-closest-thing-akai-has-released-to-a-vintage-mpc-in-decades-akai-mpc-sample-review)) |

**Что из этого следует:**
- Фоно-вход есть у двух старших MPC (XL и Live III). Наше решение про фоно совпадает с тем, куда идёт рынок.
- Встроенный микрофон стал нормой у устройств «захвата» (S-4, MPC Sample, Live III).
- Постоянный буфер записи тоже стал нормой (MPC Sample — 25 с, SP-404 MK2 — Skip Back).
- Отличаться будем широтой источников и тем, что буфер есть у каждой дорожки, а также заморозкой (Freeze) выхода (документ 08).

---
