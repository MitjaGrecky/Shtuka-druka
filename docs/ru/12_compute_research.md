# 12. Вычислитель: мощность под 16 → 32 → 64 дорожки (28.10.2026)

Статус: решения — R11 (16 дорожек, мощность на 32, цель 64), R36 (x86 Mini-ITX, ASRock N100DC-ITX), R85 (панель и вычислитель разделены). Замер — [18](18_benchmark_m93.md). Факт — источник (ссылка), вывод — логика проекта.

## 1. Сколько дорожек у других

| Устройство | Дорожек | Ограничение |
|---|---|---|
| Ableton Move | 4 | CPU; Ableton отказалась добавлять ([MusicRadar](https://musicradar.com/music-tech/no-we-do-not-intend-to-add-four-more-instrument-tracks-to-move-ableton-responds-to-critics-of-moves-limited-track-count)) |
| Torso S-4 | 4 стерео | концепция ([SoS](https://www.soundonsound.com/reviews/torso-electronics-s-4)) |
| Akai Force | 8 стерео, до 128 всего | 2 ГБ ОЗУ, аудио грузится в память целиком ([Synth.market](https://synth.market/catalogue/akai/force)) |
| OP-XY | 8 + 8 служебных | ([SoS](https://www.soundonsound.com/reviews/teenage-engineering-op-xy?amp)) |
| Polyend Play+ | 8 сэмплов + 8 синтов/MIDI | ([Polyend](https://backstage.polyend.com/t/more-midi-tracks-16-perhaps/8397)) |
| Elektron Tonverk | 8 аудио + 4 шины + 3 посыла + микс | ([MusicRadar](https://www.musicradar.com/music-tech/samplers/elektron-tonverk-review)) |
| MPC Live III | до 16 стерео + 32 плагина | 8-ядерный ARM, 8 ГБ ([MusicTech](https://musictech.com/reviews/studio-recording-gear/akai-mpc-live-iii-review/)) |
| MPC XL | многодорожечный | 8-ядерный ARM, 16 ГБ ([Perfect Circuit](https://www.perfectcircuit.com/m2e/akai-mpc-xl.html)) |
| Push 3 standalone | CPU | Intel Core i3-1115G4 в модуле NUC Compute Element, 8 ГБ ([Ableton](https://help.ableton.com/hc/en-us/articles/9204692908188-Push-3-Upgradability-with-Third-Party-Parts)) |
| Deluge | RAM | Cortex-A9 400 МГц + отдельный PIC24 для панели ([Matrixsynth](https://www.matrixsynth.com/2018/07/whats-inside-synthstrom-deluge.html)) |

**Behringer Kick:** образ Linux собран под i.MX8M Mini ([03](03_doc_open_source_analysis.md)); в Discord-обсуждении говорят о RK3588 для финальной версии. Официально не объявлено.

**Вывод:** число дорожек упирается в процессор и память, не в интерфейс. 16 дорожек — уровень Tonverk и MPC Live III.

## 2. Платформы и бенчмарки

| Платформа | Geekbench 6 (1 ядро / все) | Потребление | Плюсы | Минусы |
|---|---|---|---|---|
| Raspberry Pi 5 / CM5 (4 × A76, 2,4 ГГц) | 789 / 1523 ([CNX](https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison-features-benchmarks-price/)) | простой 3–3,6 Вт, нагрузка 8,8 Вт | I²S, 2 × DSI, GPIO; CM5 — минимум до января 2036 | мало запаса под тяжёлые синты |
| RK3588 (4 × A76 + 4 × A55) | 826 / 2913 ([Geekbench](https://browser.geekbench.com/v6/cpu/baseline/2105580)) | нет данных | почти вдвое больше многопоточности Pi 5 | софт сложнее |
| Intel N100 | 1213 / 3272 ([CNX](https://www.cnx-software.com/2024/04/29/raspberry-pi-5-intel-n100-mini-pc-comparison-features-benchmarks-price/)) | простой 7,5–10 Вт, нагрузка 17–20 Вт | x86, зрелые плагины, быстрый NVMe | нет I²S и DSI: звук по USB, экран по HDMI |
| Intel N150 (LattePanda IOTA) | 885 / 1861 ([AndroidPIMP](https://www.androidpimp.com/embedded/lattepanda-iota-review/14)) | — | компактная плата | сильно зависит от лимита мощности |
| 12-ядерный ARM (Orange Pi 6) | 1167 / 6798 ([AndroidPIMP](https://www.androidpimp.com/embedded/orange-pi-6-review/11/)) | — | запас под 64 дорожки | новая платформа |
| Intel Core i3-1115G4 (Push 3) | не измерял | — | проверен в серийном standalone | дороже и горячее |

**Задержка:**
- Pi 5 с Zynthian V5: ≈ 5,2 мс при 48 кГц; меньше — щелчки. 96 кГц сильно грузит CPU ([Zynthian](https://discourse.zynthian.org/t/expected-latency-with-raspberry-pi-5-raspberry-pi-dac-pro-pianoteq-for-live-playing/13397)).
- Буфер: t = N / fs. При 48 кГц: 64 отсчёта = 1,33 мс; 128 = 2,67 мс; 256 = 5,33 мс.
- PREEMPT_RT вошёл в основной Linux в версии 6.12 ([Phoronix](https://phoronix.com/review/linux-612-features)).

**Тяжесть синтов:** на Pi в Zynthian Surge и Vitalium дают шумы и вылеты; нагрузка сильно зависит от пресета ([Zynthian](https://discourse.zynthian.org/t/lv2-synth-how-to-limit-cpu-usage/9116)). Pi 5 почти вдвое мощнее Pi 4.

## 3. Что занимает процессор (вывод)

| Блок | Цена |
|---|---|
| Сэмпл-голос (интерполяция) | низкая |
| Фильтр, драйв на дорожку | низкая — средняя |
| Вейвтейбл и FM-голос | средняя × полифония |
| Аналоговое и физическое моделирование | высокая (Pianoteq, Surge с тяжёлыми пресетами) |
| Реверберация | средняя — высокая; лучше посылом на общие шины |
| Гранулярный процессор | средняя — высокая |
| Буфер «пишет всегда» | почти бесплатно (копирование) |

**Вывод.** Стоимость дорожки отличается в десятки раз. «32 дорожки» без уточнения ничего не значат. Нужны: бюджет дорожки (лимиты полифонии, качество движка); общие шины эффектов (2–4 реверба и дилея; у Tonverk — 4 шины и 3 посыла); многоядерный граф (дорожки параллельно, цепочка внутри дорожки последовательно).

## 4. План замера (вывод)

1. Две эталонные дорожки: сэмпл (8 голосов, фильтр, драйв, посылы) и синт (вейвтейбл 8 голосов, та же цепочка).
2. Шины: 2 реверба и 2 дилея общие.
3. Критерий: загрузка DSP не выше 70 % при буфере 128 и 48 кГц, без щелчков в течение часа.
4. Где мерить: M93 → Pi 5 → x86 и RK3588.
5. Результат: сколько эталонных дорожек тянет каждая платформа.

**M93 Tiny (по наклейке, 28.10.2026):** тип 10A5, модель S01900, выпуск 12.2014, блок 20 В 3,25 А (65 Вт). Процессор на наклейке не указан; в таких машинах — 35-ваттные T-процессоры 4-го поколения (например, i3-4150T; [Lapstore](https://www.lapstore.de/a.php/shop/lapstore/lang/en/a/15982/kw/Lenovo-ThinkCentre-M93-Tiny-10A50006GE)). Узнать: BIOS (F1), `lscpu` с флешки, «Система» в Windows. Ориентир i3-4150T — Geekbench 6 ≈ 890 / 1767 ([Geekbench](https://browser.geekbench.com/processors/intel-core-i3-4150t)) — уровень Pi 5 (789 / 1523).

**Вывод:** M93 Tiny — заменитель класса Pi 5 для замера. Если на нём 16 дорожек проходят с запасом, Pi 5 вероятно справится (с поправкой на x86 и ARM). Класс N100 и выше M93 не изображает — для запаса на 32 дорожки мерить на другой машине. Звуковую карту внутрь не ставим: AudioFuse и CI2 по USB.

## 5. Архитектура: вычислительный модуль сменный

- Push 3 построен на сменном модуле NUC Compute Element; Ableton допускает более мощные модули. Deluge разделяет CPU и панель. Kick разделяет приложение и железо протоколом по USB.

**Вывод:**
1. Панель (энкодеры, кнопки, пэды, огни) — своя плата на микроконтроллере, говорит по USB-MIDI и своему протоколу ([05](11_io_formats_research.md)).
2. Аудиотракт (предусилители, АЦП/ЦАП, CV) — своя плата по USB Audio Class 2, не зависит от I²S конкретного процессора.
3. Вычислитель — сменный модуль: CM5 сейчас, мощнее потом.

Путь «16 → 32 → 64 дорожки» тогда — замена модуля. Цена: USB вместо I²S добавляет буферизацию и немного задержки; замер покажет, насколько заметно.

## 6. Открыто

1. Точный процессор M93 Tiny (BIOS или `lscpu`).
2. Приемлема ли задержка около 5 мс или нужна меньше?
3. Согласие на сменный вычислительный модуль (решено по R36 и R85; подтверждение пользователя — в журнале).
