> Часть документа 09 ([индекс](../09_controls_research.md)): 5. Сетка пэдов

## 5. Сетка пэдов

### 5.1 Датчики

- **Velocity обязательно:** у Polyend Play и Deluge его нет, и обозреватели это ругают ([SoS](https://www.soundonsound.com/reviews/polyend-play), [Waveform](https://waveformmagazine.com/waveform-reviews/synthstrom-audible-deluge/)).
- **Что умеют лучшие:**
  - MPCe: сила удара, полифоническое послекасание и положение пальца X/Y; пэд делится на 4 квадранта ([Gearnews](https://www.gearnews.com/akai-mpc-live-iii-review/)).
  - Push 3: скорость, полифоническое давление и X/Y ([MusicRadar](https://www.musicradar.com/reviews/ableton-push-3)).
  - Launchpad Pro MK3: velocity и давление ([Kirstein](https://www.kirstein.de/en/Live-Studio/Studio/Controllers/DAW-Controllers/Novation-Launchpad-PRO-MK3.html)).
- **Опыт самодельных пэдов на FSR из Velostat:**
  - бывают ложные срабатывания при движении пальца;
  - чувствительность теряется, если основание гнётся;
  - нужна калибровка;
  - вывод автора: жёсткая опора и плотная печатная матрица важнее самой идеи датчика ([Hackaday.io](https://hackaday.io/project/1601-diy-usb-midi-controller-mpc-style)).
- Пьезодатчики дают перекрёстные срабатывания между соседними пэдами. Для чувствительности советуют переплетённые дорожки с покрытием ENIG и хороший внешний АЦП ([MIDIbox](https://forum.midibox.org/t/integrating-akai-mpc-mpd-like-pads-in-midibox/19561)).

**Вывод:** 8×8 RGB, velocity и полифоническое давление на FSR. Положение X/Y — не в первой версии. На прототипе сетку берём внешнюю: Push или Launchpad.

### 5.2 Размер

- Launchpad Pro MK3 — 268 × 268 мм на поле 10 × 10 позиций, то есть около 27 мм на ячейку с рамкой (оценка, [Kirstein](https://www.kirstein.de/en/Live-Studio/Studio/Controllers/DAW-Controllers/Novation-Launchpad-PRO-MK3.html)).
- У Push пэды меньше, чем у Maschine, но их вчетверо больше. Maschine удобнее для пальцевого барабанинга, Push — для мелодий и шагов ([MusicRadar](https://musicradar.com/news/head-to-head-ableton-push-vs-native-instruments-maschine-mk3)).
- **Вывод:** шаг 25 мм, сетка 8 · 25 = 200 мм в квадрате. Тогда энкодеры уровня справа от сетки стоят ровно по строкам и не теснее практического минимума 25 мм.

---
