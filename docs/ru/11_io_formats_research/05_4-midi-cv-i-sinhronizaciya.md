> Часть документа 11 ([индекс](../11_io_formats_research.md)): 4. MIDI, CV и синхронизация

## 4. MIDI, CV и синхронизация

### 4.1 MIDI

- **DIN 5-pin:** Force с мини-джеками и переходниками критикуют, переходники легко потерять ([Bonedo](https://www.bonedo.de/artikel/akai-force-test/)).
- **TRS-MIDI:** тип A входит в стандарт MIDI Association с 2018 года (Korg, Akai, Teenage Engineering). Тип B используют Arturia, Novation, Polyend. Выглядят одинаково, но несовместимы ([Bonedo](https://www.bonedo.de/artikel/midi-wirrwarr-entschlusselt-ueber-midi-klinke-trs-a-und-trs-b)).
- **MIDI 2.0 на Linux:** UMP в ядре с 6.5, зрелая база к 6.12; PipeWire 1.2+; выигрыш в разрешении, не в задержке. Советуют считать поддержку бонусом ([kernel.org](https://www.kernel.org/doc/html/v6.5/sound/designs/midi-2.0.html), [обзор 2026](https://linuxdj-project.pages.dev/notes/midi-2-0-on-linux-2026-pipewire-ump-kernel-support-and-safe-fallbacks/)).

**Вывод:**
- DIN: 2 входа и 2–4 выхода (у MPC XL 2/4), один выход переключается в Thru.
- USB-MIDI в обе стороны: как устройство для компьютера и как хост для MPD218, Push, Launchpad.
- MIDI 2.0 включаем, когда стек стабилен, железо этого не требует.

### 4.2 CV/Gate

| Стандарт | Что значит | Кто |
|---|---|---|
| 1 В/окт | 1 В = октава | Roland, Moog, Sequential, Oberheim, ARP, Eurorack ([Wikipedia](https://en.wikipedia.org/wiki/CV/gate)) |
| Гц/В | Удвоение напряжения = октава | Большинство Korg и Yamaha |
| V-trig | Положительный импульс 2–10 В | Roland, Sequential |
| S-trig | Замыкание на землю | Ранние Moog |
| Уровни Eurorack | Аудио ±5 В; CV 0…10 В или ±5 В; триггер 10 В, 1 мс; порог входа около 0,1–2 В | [VCV Rack](https://vcvrack.com/manual/VoltageStandards) |

**Сколько у других:** Kick — 4, Force — 4, Push 3 — 4 + 2, Live III — 8 сигналов, APC64 — 8, MPC XL — 16, BCR32 — 4 и Sync.

**Расчёт точности ЦАП для 1 В/окт** (диапазон 10 В, 1 В = 1200 центов):
- 16 бит: 10 В / 65 536 ≈ 0,153 мВ ≈ 0,18 цента — с запасом.
- 12 бит: 10 В / 4096 ≈ 2,44 мВ ≈ 2,9 цента — на грани слышимой расстройки в аккордах.

**Вывод:**
- 8 CV/Gate-выходов на 3,5 мм (как у Live III), ЦАП 16 бит, калибровка в софте, защита выходов.
- Переключаемые режимы: 1 В/окт или Гц/В, V-trig или S-trig.
- 2–4 CV-входа для модуляции наших параметров. У конкурентов это редкость.

### 4.3 Синхронизация

| Способ | Детали |
|---|---|
| MIDI-клок | 24 импульса на четверть |
| Аналоговый клок | KeyStep поддерживает: 1 импульс на шаг, 4 PPQ, ≈2 PPQ (Korg Volca), 24 PPQ (Roland TR-808), 48 PPQ (Linn LM-2) ([Arturia](https://support.arturia.com/hc/en-us/articles/4405741335954)) |
| Ableton Link | Темп, фаза, старт/стоп по локальной сети. Двойная лицензия: GPLv2+ или проприетарная ([GitHub](https://www.Github.com/Ableton/link)) |

**Вывод:**
- Clock In/Out 3,5 мм с выбором PPQ из списка выше.
- Link по Ethernet и Wi-Fi. Для открытого проекта подходит GPLv2+, для закрытого коммерческого понадобится лицензия Ableton.

---
