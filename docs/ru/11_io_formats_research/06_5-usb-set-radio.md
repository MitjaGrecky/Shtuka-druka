> Часть документа 11 ([индекс](../11_io_formats_research.md)): 5. USB, сеть, радио

## 5. USB, сеть, радио

### 5.1 USB-аудио к компьютеру

*Обновление 31.10.2026: после перехода на x86 Mini-ITX (R36) режим USB-гаджета недоступен — варианты в документе 19, раздел 9.*

У MPC — 24 канала в каждую сторону через USB-C, у Push 3 — 10 × 12 ([Gearnews](https://www.gearnews.com/akai-mpc-live-iii-review/), [Thomann](https://www.thomann.de/be/ableton_push_3_standalone_live_std.htm)).

На Linux устройство-гаджет UAC2 долго было ограничено 27 каналами. Патч июля 2026 года добавляет явное число каналов, проверено до 96 каналов на Pi Zero 2 W ([LKML](https://lkml.iu.edu/2607.3/09667.html)).

**Пропускная способность** (32 канала × 48 кГц × 32 бита):
- 32 · 48 000 · 32 = 49,2 Мбит/с в одну сторону, туда и обратно ≈98 Мбит/с.
- USB 2.0 High-Speed (480 Мбит/с) хватает.

У CM5 есть порт USB 2.0 ([CM5 brief](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008181-DS-10-cm5-product-brief.pdf)); работу в режиме устройства нужно проверить.

### 5.2 Хост, сеть и радио (вывод)

- 2–3 порта USB-A под контроллеры и флешки.
- Ethernet для Link и переноса файлов.
- Wi-Fi и Bluetooth через готовый сертифицированный модуль (документ 13). Bluetooth MIDI на Linux пока нестабилен по таймингу, обзор 2026 года называет джиттер 8–20 мс ([обзор](https://linuxdj-project.pages.dev/notes/midi-2-0-on-linux-2026-pipewire-ump-kernel-support-and-safe-fallbacks/)).

---
