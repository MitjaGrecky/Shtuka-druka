> Часть документа 12 ([индекс](../12_compute_research.md)): 1. Сколько дорожек у других и почему

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
