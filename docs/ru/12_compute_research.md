# Штука Дрюка: вычислительная мощность под 16 → 32 → 64 дорожки

*28.10.2026. **Факт** — из источника, **вывод** — моя инженерная логика, **решено** — решение пользователя.*

## Решение

- **Решено:** не меньше 16 дорожек; мощность закладываем на 32, цель 64.

## 1. Сколько дорожек у других и почему

| Устройство | Дорожек | Ограничение |
|---|---|---|
| Ableton Move | 4 | CPU: Ableton прямо отказалась добавлять ещё 4 ради стабильности и цены ([MusicRadar](https://musicradar.com/music-tech/no-we-do-not-intend-to-add-four-more-instrument-tracks-to-move-ableton-responds-to-critics-of-moves-limited-track-count)) |
| Torso S-4 | 4 стерео | Концепция ([SoS](https://www.soundonsound.com/reviews/torso-electronics-s-4)) |
| Akai Force | 8 стерео-аудио, до 128 всего | 2 ГБ ОЗУ, аудио грузится в память целиком ([Synth.market](https://synth.market/catalogue/akai/force)) |
| OP-XY | 8 + 8 служебных | ([SoS](https://www.soundonsound.com/reviews/teenage-engineering-op-xy?amp)) |
| Polyend Play+ | 8 сэмплов + 8 синтов/MIDI | ([Polyend](https://backstage.polyend.com/t/more-midi-tracks-16-perhaps/8397)) |
| Elektron Tonverk | 16 = 8 аудио (по 8 голосов) + 4 шины + 3 посыла + микс | ([MusicRadar](https://www.musicradar.com/music-tech/samplers/elektron-tonverk-review)) |
| MPC Live III | до 16 стерео-аудио + 32 плагина (у Live II было по 8) | 8-ядерный ARM, 8 ГБ ([MusicTech](https://musictech.com/reviews/studio-recording-gear/akai-mpc-live-iii-review/)) |
| MPC XL | Старший MPC | 8-ядерный ARM, 16 ГБ ([Perfect Circuit](https://www.perfectcircuit.com/m2e/akai-mpc-xl.html)) |
| Push 3 standalone | Ограничено CPU | Intel Core i3-1115G4 в модуле NUC Compute Element, 8 ГБ ([Ableton](https://help.ableton.com/hc/en-us/articles/9204692908188-Push-3-Upgradability-with-Third-Party-Parts)) |
| Deluge | Ограничено объёмом RAM | Cortex-A9 400 МГц + отдельный микроконтроллер панели PIC24 ([Matrixsynth](https://www.matrixsynth.com/2018/07/whats-inside-synthstrom-deluge.html), [Waveform](https://waveformmagazine.com/waveform-reviews/synthstrom-audible-deluge/)) |

**Behringer Kick.** В репозитории образ Linux, который мы читали, собран под i.MX8M Mini (документ 03). На форуме Zynthian со ссылкой на Discord пишут, что финальная версия получит RK3588 ([Zynthian](https://discourse.zynthian.org/t/behringer-kick-open-source-groovebox/13799)). Официально процессор не объявлен.

**Что из этого следует:**
- Число дорожек почти всегда упирается в процессор и память, а не в интерфейс.
- 16 дорожек — это уровень Tonverk и MPC Live III, то есть устройств текущего поколения.

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

## 3. Что занимает процессор (вывод)

| Блок | Цена | Комментарий |
|---|---|---|
| Сэмпл-голос (воспроизведение, интерполяция) | Низкая | Дешевле всего |
| Фильтр, драйв на дорожку | Низкая — средняя | Зависит от модели |
| Вейвтейбл- и FM-голос | Средняя | × полифония |
| Аналоговое моделирование, физическое моделирование | Высокая | Pianoteq, Surge с тяжёлыми пресетами |
| Реверберация | Средняя — высокая | Лучше делать посылом на общие шины, а не на каждую дорожку |
| Гранулярный процессор | Средняя — высокая | Зависит от числа зёрен |
| Буфер «пишет всегда» | Почти бесплатно | Копирование в память |

**Вывод.** Стоимость дорожки отличается в десятки раз в зависимости от источника. Поэтому «32 дорожки» без уточнения ничего не значат. Нужны:
1. **Бюджет дорожки:** лимиты полифонии и выбор качества движка.
2. **Общие шины эффектов:** 2–4 шины реверба и дилея вместо эффекта на каждой дорожке. Так сделано у Tonverk: 4 шины, 3 посыла.
3. **Многоядерный граф:** дорожки обрабатываются параллельно на разных ядрах, а цепочка внутри дорожки — последовательно.

## 4. План замера (вывод)

Сравнивать платформы на словах бессмысленно, нужно измерение.

1. **Две эталонные дорожки:**
   - сэмпл-дорожка: 8 голосов, фильтр, драйв, посылы на шины;
   - синт-дорожка: вейвтейбл на 8 голосов, та же цепочка.
2. **Шины:** 2 реверба и 2 дилея общие.
3. **Критерий:** загрузка DSP не выше 70% при буфере 128 отсчётов и 48 кГц, без щелчков в течение часа.
4. **Где мерить:** M93 (сейчас) → Pi 5 → кандидаты x86 и RK3588.
5. **Результат:** сколько эталонных дорожек тянет каждая платформа. По этому выбираем железо под 32 дорожки.

### Что за M93 у тебя (по фото наклейки, 28.10.2026)

- Тип 10A5, модель S01900, выпуск 12.2014, питание 20 В 3,25 А (65 Вт).
- Внешний блок на 65 Вт и тип 10A5 указывают на **M93 Tiny**: маленький корпус с внешним блоком. У M93 Tiny блок на 65 Вт ([Data System Works](https://www.datasystemworks.com/thinkcentre-m93-tiny.asp)), тип 10A5 продаётся как M93 Tiny ([Lapstore](https://www.lapstore.de/a.php/shop/lapstore/lang/en/a/15982/kw/Lenovo-ThinkCentre-M93-Tiny-10A50006GE)).
- В таких машинах стоят 35-ваттные процессоры 4-го поколения с буквой T: например, i3-4150T в 10A50006GE ([Lapstore](https://www.lapstore.de/a.php/shop/lapstore/lang/en/a/15982/kw/Lenovo-ThinkCentre-M93-Tiny-10A50006GE)), i5-4570T или i7-4765T в M93p Tiny ([Data System Works](https://www.datasystemworks.com/thinkcentre-m93-tiny.asp)).
- Процессор на наклейке не указан. Точно узнать:
  - в BIOS (F1 при включении);
  - в Linux с флешки: `lscpu`;
  - в Windows: «Параметры» → «Система» → «О системе».
- Ориентир мощности: i3-4150T — Geekbench 6 ≈ 890 / 1767 ([Geekbench](https://browser.geekbench.com/processors/intel-core-i3-4150t)). Это уровень Pi 5 (789 / 1523). Четырёхъядерный i5-T, вероятно, немного выше.

**Вывод:** M93 Tiny — хороший заменитель класса Pi 5 для замера. Если на нём эталонные 16 дорожек проходят с запасом, Pi 5 скорее всего тоже справится (с поправкой на разницу x86 и ARM). Класс N100 и выше M93 не изображает: если понадобится запас на 32 дорожки, мерить придётся на другой машине.

Внутрь Tiny звуковую карту не поставить, но для прототипа это не нужно: AudioFuse и CI2 подключаются по USB.

## 5. Архитектурный вывод: вычислительный модуль должен быть сменным

**Факты.**
- Push 3 построен на сменном модуле Intel NUC Compute Element. Ableton допускает в будущем более мощные процессоры как отдельные компоненты ([Ableton](https://help.ableton.com/hc/en-us/articles/9204692908188-Push-3-Upgradability-with-Third-Party-Parts)).
- Deluge разделяет главный процессор и микроконтроллер панели.
- Kick разделяет приложение и контроллер железа протоколом по USB (документ 03).

**Вывод.** Делаем так же:
1. **Панель** (энкодеры, кнопки, пэды, светодиоды) — своя плата на микроконтроллере, говорит по USB-MIDI или своему USB-протоколу (уже решено ранее, документ 05).
2. **Аудиотракт** (предусилители, АЦП/ЦАП, CV) — своя плата, подключается по USB Audio Class 2, чтобы не зависеть от I²S конкретного процессора.
3. **Вычислитель** — сменный модуль: CM5 сейчас, x86 или ARM помощнее потом.

Тогда путь «16 → 32 → 64 дорожки» — это замена модуля, а не переделка устройства.

Компромисс: связь аудиоплаты по USB вместо I²S добавляет буферизацию и немного задержки (на Zynthian I²S предпочитают USB, [Zynthian](https://discourse.zynthian.org/t/expected-latency-with-raspberry-pi-5-raspberry-pi-dac-pro-pianoteq-for-live-playing/13397)). Замер покажет, насколько это заметно.

## Открытые вопросы

1. Какой точно процессор в M93 Tiny (BIOS или `lscpu`)? Модель машины определена по наклейке, процессор на ней не указан.
2. Приемлема ли задержка около 5 мс или нужна меньше?
3. Согласен ли ты с идеей сменного вычислительного модуля?

## 6. Сменные процессорные модули: варианты (29.10.2026)

**Почему вопрос встал.** Пользователь хочет сводить трек прямо в устройстве, хотя бы легко. Вместе с 20–24 дорожками входов, синтами и шинами это выходит за пределы Pi 5 (P36).

**Урок Push 3.** Push 3 построен на модуле Intel NUC Compute Element. В июле 2023 года Intel вышла из бизнеса NUC, и пользователи Ableton на форуме обсуждают, будут ли дальше модули для апгрейда; официального ответа Ableton в теме нет ([Ableton Forum](https://forum.ableton.com/viewtopic.php?p=1814113)). **Вывод:** закрытый модуль одного производителя может умереть, поэтому лучше открытый стандарт с несколькими производителями.

| Вариант | Что это | Процессор | Плюсы | Минусы |
|---|---|---|---|---|
| Raspberry Pi CM5 | Модуль Raspberry Pi | 4 × A76 | Дёшево, мало ест, производство до 2036 | Мало запаса; один производитель |
| LattePanda Mu | x86-модуль размером с планку памяти + несущая плата (есть готовая Lite Carrier) ([CNX](https://cnx-software.com/?p=128258), [DFRobot](https://www.dfrobot.com/product-2820.html)) | Intel N100, 4 ядра, до 16 ГБ | Недорогой x86, формат как у CM5 | Один производитель, свой разъём; только 4 ядра |
| COM Express Type 6 Compact | Открытый промышленный стандарт PICMG, модуль 95 × 95 мм на несущей плате | До 8 ядер Ryzen Embedded 8840U, до 128 ГБ DDR5, eDP, 4 × DP, много USB ([CNX: SolidRun](https://www.cnx-software.com/2025/12/10/amd-ryzen-embedded-8840u-com-express-type-6-compact-module-takes-up-to-128gb-ddr5/)); есть и Intel Core Ultra ([CNX: AAEON](https://www.cnx-software.com/2025/11/28/aaeon-com-arhc6-com-express-type-6-module-targets-edge-ai-applications-with-an-up-99-tops-intel-core-ultra-9-arrow-lake-cpu/)) | Много производителей (Congatec, Kontron, AAEON, SolidRun, iBase); одна несущая плата на поколения процессоров | Промышленная цена; несущую плату проектировать сложнее |
| Плата Framework | Материнская плата ноутбука Framework, продаётся отдельно; работает как одноплатник от USB-C ([Framework](https://frame.work/blog/mainboard-availability-and-open-source-release)) | Intel или AMD, разные поколения в одном формате | Потребительская цена; чертежи открыты (Creative Commons); новые поколения в том же размере | Один производитель; форма ноутбучной платы; порты в основном USB-C |
| Mini-ITX | Самый распространённый настольный стандарт, 170 × 170 мм | Любой настольный процессор | Самый дешёвый апгрейд, огромный выбор | Крупно, горячо, много потребляет |

**Вывод.**
1. Архитектура уже позволяет менять процессор: аудиоплата и панель подключаются по USB. Процессору нужны только USB, экран (eDP или HDMI), NVMe и питание. Это и есть наш «сокет».
2. Для прототипа — M93, затем LattePanda Mu или плата Framework (дёшево).
3. Для финальной версии — COM Express Type 6 Compact: открытый стандарт, 8 ядер, апгрейд без переделки несущей платы.
4. Цену модулей COM Express нужно уточнить у поставщиков до решения.

### 6.1 Уточнение после решения R28 (30.10.2026)

Пользователь: проект некоммерческий, нужны общедоступные комплектующие. Промышленный COM Express отпадает (продаётся через дистрибьюторов, цена по запросу), остаётся вариантом только для Kickstarter.

**Выбор — Mini-ITX как «сокет».**
- Стандарт с 2001 года, 170 × 170 мм, крепёж одинаковый у всех производителей; платы продаются в обычных магазинах, в том числе в Прибалтике.
- Старт: ASRock N100DC-ITX — Intel N100, пассивное охлаждение, питание от DC-разъёма, одна планка DDR4, M.2, HDMI ([CNX](https://www.cnx-software.com/2023/08/29/asrock-unveils-intel-processor-n100-motherboards-with-24-pin-atx-connector-or-dc-in-jack/), [Guru3D](https://guru3d.com/story/asrock-introduces-n100dc-itx-a-fanless-mini-itx-motherboard-with-intel-n100), в продаже в Эстонии: [ox.ee](https://www.ox.ee/est/product/2669413)).
- Апгрейд: любая Mini-ITX с 8-ядерным Ryzen; мощность ограничить в BIOS (35–45 Вт), охлаждение тихое или пассивное через корпус.
- Компактная альтернатива: LattePanda Mu с готовой Lite Carrier.
- Плата Framework: продаётся в ЕС ([TechPowerUp](https://techpowerup.com/314396/framework-marketplace-readied-for-eu-uk-shipping)), но это один производитель и ноутбучная форма; держим как запасной путь.
- Экран 10,1″ подключается через плату-контроллер HDMI → панель (обычное решение для DIY-экранов).

### 6.2 Процессор M93 уточнён (31.10.2026)

*Обновление: Windows на M93 нет (скриншот был с другой установки), стоял Home Assistant; Linux ставим начисто (R76). Набор для замера — документ 18.*

По скриншоту «О системе» в Windows: **Intel Core i3-4150T @ 3,00 ГГц** (2 ядра / 4 потока, 35 Вт), 8 ГБ DDR3, SSD 238 ГБ (занято 49), Windows 11 Pro 25H2. Geekbench 6 ≈ 890 / 1767 — уровень Pi 5 (789 / 1523), см. раздел 4.

**Вывод для замера.** M93 — нижняя планка. Мерить в Linux (цель — Linux с PREEMPT_RT), а не в Windows: Linux поставить второй системой на свободное место SSD или грузиться с внешнего USB-SSD. Если 16 эталонных дорожек на M93 не проходят, это подтверждает переход на x86 класса N100 и выше (P36).
