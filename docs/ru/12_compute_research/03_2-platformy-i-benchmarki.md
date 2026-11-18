> Часть документа 12 ([индекс](../12_compute_research.md)): 2. Платформы и бенчмарки

## 2. Платформы и бенчмарки

| Платформа | Geekbench 6 (одно ядро / все ядра) | Потребление | Плюсы | Минусы |
|---|---|---|---|---|
| Raspberry Pi 5 / CM5 (4 × A76, 2,4 ГГц) | 789 / 1523 ([CNX](https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison-features-benchmarks-price/)); 796 / 1584 ([AndroidPIMP](https://www.androidpimp.com/embedded/orange-pi-6-review/11/)) | Простой 3,0–3,6 Вт, нагрузка 8,8 Вт | I²S, 2 × DSI, GPIO; CM5 выпускается минимум до января 2036 года ([CM5 brief](https://pip-assets.raspberrypi.com/categories/944-raspberry-pi-compute-module-5/documents/RP-008181-DS-10-cm5-product-brief.pdf)) | Мало запаса для тяжёлых синтов |
| RK3588 (4 × A76 + 4 × A55) | 826 / 2913 ([Geekbench](https://browser.geekbench.com/v6/cpu/baseline/2105580)) | Нет данных в найденном | Почти вдвое больше многопоточной мощности, чем у Pi 5 | Программная поддержка сложнее, чем у Pi |
| Intel N100 (мини-ПК) | 1213 / 3272 ([CNX](https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison-features-benchmarks-price/)) | Простой 7,5–10 Вт, нагрузка 17–20 Вт | x86, зрелые плагины, быстрый NVMe | Нет I²S и DSI: звук по USB, экран по HDMI |
| Intel N150 (LattePanda IOTA, ограничен по мощности) | 885 / 1861 ([AndroidPIMP](https://www.androidpimp.com/embedded/lattepanda-iota-review/14)) | — | Компактная плата | Результат сильно зависит от лимита мощности |
| 12-ядерный ARM (Orange Pi 6) | 1167 / 6798 ([AndroidPIMP](https://www.androidpimp.com/embedded/orange-pi-6-review/11/)) | — | Запас под 64 дорожки | Новая платформа, зрелость софта неизвестна |
| Intel Core i3-1115G4 (как в Push 3) | Не измерял | — | Проверено в серийном standalone-устройстве | Дороже и горячее |

**Задержка.**
- На Pi 5 с официальной звуковой платой Zynthian V5 достигли ≈5,2 мс при 48 кГц; меньше — щелчки. 96 кГц сильно грузит процессор ([Zynthian](https://discourse.zynthian.org/t/expected-latency-with-raspberry-pi-5-raspberry-pi-dac-pro-pianoteq-for-live-playing/13397)).
- Формула буфера: t = N / fs. При 48 кГц: 64 отсчёта → 1,33 мс; 128 → 2,67 мс; 256 → 5,33 мс.
- Ядро реального времени (PREEMPT_RT) вошло в основной Linux в версии 6.12 ([Phoronix](https://phoronix.com/review/linux-612-features)).

**Тяжесть синтов.**
- На Pi в Zynthian Surge и Vitalium из-за нагрузки дают шумы и вылеты. Нагрузка сильно зависит от пресета ([Zynthian](https://discourse.zynthian.org/t/lv2-synth-how-to-limit-cpu-usage/9116)).
- Pi 5 почти вдвое мощнее Pi 4. На Pi 4 Pianoteq работал почти на пределе ([Zynthian](https://discourse.zynthian.org/t/pi5-pianoteq-at-full-rate/12700)).
