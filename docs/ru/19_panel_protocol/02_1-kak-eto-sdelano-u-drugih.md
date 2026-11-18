> Часть документа 19 ([индекс](../19_panel_protocol.md)): 1. Как это сделано у других

## 1. Как это сделано у других

| Устройство | Как панель говорит с компьютером | Источник |
|---|---|---|
| Ableton Push 2 | USB 2.0: два MIDI-порта и отдельный интерфейс для экрана (кадры 960 × 160, 16 бит, 60 кадр/с, массовая передача) | [Push 2 Interface Manual](https://github.com/Ableton/push-interface) |
| Push 2: энкодеры | Относительное значение 7 бит в дополнительном коде, ≈ 210 шагов на оборот | там же |
| Push 2: светодиоды | Note On / CC с номером цвета из палитры; канал MIDI задаёт анимацию (мигание, пульс), чтобы компьютер не слал сообщения непрерывно; ШИМ по умолчанию 100 Гц, максимум 116 Гц | там же |
| Behringer Kick | Свой пакетный протокол по USB: 2 стартовых байта, тип, направление, номер, длина, данные, CRC-8 (полином 0x31, начальное 0xFF). Типы пакетов: система, кнопка, светодиод, пэд, ручки, MIDI, CV, слайдер | [GitHub, ComProtocol](https://github.com/MusicTribeOpenSource/0700-AAM) (AGPL-3.0) |
| Linux | С ядра 6.5 есть драйвер USB MIDI 2.0 (UMP); при необходимости откат на MIDI 1.0 параметром `midi2_enable=0` | [kernel.org](https://docs.kernel.org/6.5/sound/designs/midi-2.0.html) |

**Нормы и физика:**
- Кадр USB Full-Speed — 1 мс, High-Speed — 125 мкс ([Microchip](https://developerhelp.microchip.com/xwiki/bin/view/applications/usb/how-it-works/frame/)).
- Допустимая задержка реакции на жест — до 10 мс, разброс — не больше 1 мс ([Wessel & Wright, NIME](https://arxiv.org/pdf/2010.01570)).
- RP2350: 2 ядра до 150 МГц, 520 КБ ОЗУ, USB 1.1 (устройство и хост), 2 UART, 12 машин состояний PIO ([Tom's Hardware](https://www.tomshardware.com/raspberry-pi/raspberry-pi-pico/whats-inside-the-raspberry-pi-pico-2s-rp2350)).

**Вывод.** Берём лучшее от обоих: от Push — стандартный MIDI как запасной путь и анимации светодиодов на стороне платы; от Kick — компактный пакет с типом и контрольной суммой. Экран по USB, как у Push, нам не нужен: он подключён к вычислителю напрямую (eDP/HDMI).
