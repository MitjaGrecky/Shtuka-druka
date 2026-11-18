> Часть документа 11 ([индекс](../11_io_formats_research.md)): 7. Форматы

## 7. Форматы

| Что | Формат | Комментарий |
|---|---|---|
| Внутренняя обработка | 48 кГц, 32 бит float | Zynthian оптимизирован под 48 кГц; на 96 кГц у Pi 5 резко растёт нагрузка ([Zynthian](https://discourse.zynthian.org/t/expected-latency-with-raspberry-pi-5-raspberry-pi-dac-pro-pianoteq-for-live-playing/13397)) |
| Импорт аудио | WAV, AIFF, FLAC, MP3, OGG | Типично |
| Экспорт аудио | WAV, FLAC; стемы по дорожкам | Отсутствие стемов и переноса в DAW ругают у MPC Sample ([MusicRadar](https://www.musicradar.com/music-tech/samplers/the-closest-thing-akai-has-released-to-a-vintage-mpc-in-decades-akai-mpc-sample-review)) |
| Перенос проекта в DAW | **DAWproject** — открытый формат; поддерживают Bitwig, PreSonus, Cubase 14; Pro Tools нет ([Production Expert](https://www.production-expert.com/production-expert-1/steinberg-joins-dawproject-support-can-avid-ignore-it)) | Сильный довод «DAW в железе». Формат Ableton Live закрытый; Move работает с проектами Live ([MusicTech](https://musictech.com/reviews/controllers/ableton-move-review/)), Force экспорт в Live обещал ещё на анонсе ([CDM](https://cdm.link/akai-force-hands-on-preview/)) |
| MIDI | Standard MIDI File | Типично |
| Вейвтейблы | WAV с кадрами по 2048 отсчётов (де-факто у Serum и Vital) | По общим знаниям; уточнить по документации синтов. 2048 при 48 кГц — это кадр 42,7 мс (основной тон ≈23,4 Гц) |
| Плагины | LV2 (как у Zynthian), CLAP (есть сборки под aarch64, например LSP), VST3 под Linux | LV2 и CLAP открытые и без лицензионных сложностей ([Alpine](https://pkgs.alpinelinux.org/package/v3.23/community/aarch64/lsp-plugins-clap)) |

**Вывод про вейвтейблы.** Чтобы сделать таблицу из захваченного звука, нужны:
1. определение высоты тона;
2. вырезание периодов;
3. пересэмплирование каждого периода в 2048 отсчётов.

Это ещё один аргумент за 48 кГц внутри и float без потерь.

---
