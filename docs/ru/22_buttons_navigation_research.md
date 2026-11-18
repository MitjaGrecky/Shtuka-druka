# 22. Кнопки и навигация: как у других устройств (исследование, 31.10.2026)

Статус: **исследование для версии v4, решения приняты позже** (R89, R90, R94, R95, R96 — [decisions/02_controls.md](decisions/02_controls.md)). Факт — из источника, вывод — аудитора или проектировщика.

## 1. Что сказал пользователь (v4)

- Большая часть кнопок v4 не объясняла действие; не видно Старт, Стоп, Rec.
- В блоке System могли бы быть громкости и гейны.
- Один индикатор уровня, а работаем в стерео: нужны два (L/R мастера).
- Часть идей — «гибриды», не все знакомы; «потерялся в навигации».

## 2. Как устроено у других

| Устройство | Кнопки и группы | Навигация | Источник |
|---|---|---|---|
| NI Maschine MK3 | Блок Control 2 × 6 (Channel, Plug-In, Arranger, Mixer, Browser, Sampling, Page, File, Settings…); транспорт внизу слева; режимы пэдов справа | Кнопки названы по тому, что откроется (Mixer, Browser, Sampling) | [NI](https://docs.native-instruments.com/online-guides/maschine-accessibility/en/maschine-hardware-layout) |
| Akai MPC One | Транспорт: Rec, Overdub, Stop, Play; режимы: Track Mute, Step Seq, Sampler; второе действие через Shift | Main (главный экран), Menu (все режимы), колесо | [Akai](https://www.manualslib.com/manual/1855574/Akai-Mpc-One.html?page=5) |
| MPC Live III | Выделенные кнопки режимов; 16 шаговых кнопок | Matrix неудобна, «новичок может растеряться» | [SoS](https://www.soundonsound.com/reviews/akai-mpc-live-iii) |
| Ableton Push 3 | Режимы Session/Note, Clip, Device, Mix; транспорт Play, Record, Fixed Length, Metronome, Tap, Capture; D-pad; Learn на устройстве | Две оси: что делают пэды (Session/Note) и что на экране (Device/Mix/Clip); «Back» нет | [Ableton](https://www.ableton.com/en/push/manual/) |
| Novation Launchpad Pro MK3 | Режимы сверху; ряд «что делают кнопки дорожек» снизу; запуск сцен справа | Стрелки двигают окно сетки | [Novation](https://userguides.novationmusic.com/hc/en-gb/articles/25494530115346-Launchpad-Pro-MK3-interface) |
| Novation Circuit Tracks | Транспорт Play ▶, Record ●; 8 кнопок дорожек с именами; кнопки видов | Кнопка вида = что увидишь на сетке | [Novation](https://userguides.novationmusic.com/hc/en-gb/articles/25494476280850-Circuit-Tracks-hardware-overview) |
| Elektron Digitakt II | 16 trig-кнопок, FUNC (второе действие оранжевым) | Комбинации FUNC + кнопка | [Sweetwater](https://www.sweetwater.com/sweetcare/articles/elektron-digitakt-ii-quickstart-guide/) |
| Akai Force | Экран сверху, сетка клипов 8 × 9 снизу | «Вижу, где я и легко запускаю клипы» | [SoS](https://www.soundonsound.com/reviews/akai-force) |

Значки: ▶ и ■ стандартизированы ISO и IEC; у значка должна быть текстовая подпись ([NN/g](https://www.nngroup.com/articles/icon-usability/)).

## 3. Правила (вывод)

| Правило | У кого | Что было в v4 |
|---|---|---|
| Транспорт — отдельная группа с ▶ ■ ● и цветом | Maschine, MPC, Circuit, Push | Кнопки того же размера и цвета |
| Режим называется существительным — тем, что откроется | Maschine, Push, Circuit | Глаголы Grab, Shape, Perform, Arrange: придуманы, не говорят, что будет |
| Две оси: пэды и экран | Push, Launchpad | Одна ось «страница меняет всё» |
| Кнопка «домой» | MPC Main | Только Back |
| Shift-функция подписана на кнопке | Maschine, Elektron, Circuit | Скрытые комбинации, поэтому кнопок больше |
| Громкость под рукой | Circuit, Push, Maschine | Громкости спереди — понятно |
| Mute и Solo как ряд дорожек | Launchpad | Есть, но спрятаны |
| Сцены справа от сетки | Launchpad, Push | Ряд под сеткой — непривычно |
| Обучение на устройстве | Push 3 Learn | Нет |

**Непонятные в v4:** Grab, Shape, Perform, Arrange, Capture, Freeze, Input, 6 Macro, сцены под сеткой. Понятные: Play, Stop, Undo, Browser, Mute, Monitor, Phones.

## 4. Варианты навигации (как предлагалось)

- **A. Как Push:** две оси. Режимы сетки: Clips, Notes, Steps, FX. Экраны: Sound, Mixer, Sampler, Song, Browser. Кнопка Home.
- **B. Как MPC:** Home и Menu со списком режимов на экране, колесо выбирает.
- **C. Одна ось, понятные имена:** Grab → Sampler, Shape → Sound, Perform → Live, Arrange → Song; Home; подпись на экране «что делает сетка».

Решение: вариант A с правками — **принят в R94** (две оси: сетка и экран). Остальное — в [decisions/02_controls.md](decisions/02_controls.md).

## 5. Что приняли из частных пожеланий

- Транспорт крупный, с ▶ ■ ● и цветом (R94).
- Два столбика L/R мастера; остальные уровни на экране (R94, блок «Уровни»).
- Громкости и гейны в одном блоке «Уровни» (R94).
- Scenes — колонка справа от сетки (R94, R101).
- Learn-подсказка при удержании кнопки — в решениях не записана (не решено).

Подписи захвата решены в R48 и R94 (Capture и Resample).
