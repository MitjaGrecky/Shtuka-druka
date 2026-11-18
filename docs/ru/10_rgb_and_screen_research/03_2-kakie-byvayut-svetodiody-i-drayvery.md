> Часть документа 10 ([индекс](../10_rgb_and_screen_research.md)): 2. Какие бывают светодиоды и драйверы

## 2. Какие бывают светодиоды и драйверы

| Вариант | Частота ШИМ | Интерфейс и скорость | Ток | Особенности |
|---|---|---|---|---|
| WS2812B | ≈400 Гц, типичное измерение ([Enttec](https://support.enttec.com/pixel/pixel-general-knowledge/why-do-leds-flicker-on-camera)) | Один провод, ≈30 мкс на светодиод; 300 штук ≈9 мс ([applied-ee](https://applied-ee.github.io/embedded/docs/led-systems/addressable-led-architectures/apa102-and-sk9822/)) | 10–20 мА на цвет, до ≈60 мА на светодиод; в покое ≈0,5 мА ([EEVblog](https://www.eevblog.com/forum/projects/ws2812b-leds-power-consumption/)) | Дёшево, но ШИМ попадает в звуковой диапазон и мерцает на камере |
| SK6812 | ≈1,2 кГц ([Enttec](https://support.enttec.com/pixel/pixel-general-knowledge/why-do-leds-flicker-on-camera)) | Как у WS2812 | Сопоставимо | Лучше, но всё ещё в звуковом диапазоне |
| APA102 | Часто называют ≈19 кГц, данные расходятся ([Enttec](https://support.enttec.com/pixel/pixel-general-knowledge/why-do-leds-flicker-on-camera)) | SPI с тактом, 1–8 МГц; 300 штук ≈1,5 мс при 8 МГц ([applied-ee](https://applied-ee.github.io/embedded/docs/led-systems/addressable-led-architectures/apa102-and-sk9822/)) | Не указан | 5-битная глобальная яркость, всего около 13 бит на канал; в 1,5–2 раза дороже WS2812 |
| SK9822 | Глобальная яркость сделана отдельным ШИМ | Как у APA102 | — | На камере даёт биения и полосы; для съёмки советуют настоящий APA102 ([applied-ee](https://applied-ee.github.io/embedded/docs/led-systems/addressable-led-architectures/apa102-and-sk9822/)) |
| Матричный драйвер IS31FL3741 + обычные RGB-светодиоды | 29 кГц ([даташит](https://www.mouser.com/datasheet/2/198/IS31FL3741-1275466.pdf)) | I²C до 1 МГц; до 117 RGB (351 светодиод) на микросхему | Максимум 38 мА на линию; в среднем до ≈3,75 мА на светодиод | Есть подавление «призраков», питание 2,7–5,5 В, 256 ступеней тока и ШИМ |

**Вывод.** WS2812/SK6812 для звукового прибора не подходят: их ШИМ лежит в звуковом диапазоне, на видео они мерцают, и даже погашенные потребляют ток. Выбираем матричные драйверы (класса IS31FL3741) с дискретными RGB-светодиодами: 29 кГц, низкий ток, управление по I²C от платы контроллера. APA102 — запасной вариант для отдельных мест вроде длинной ленты.
