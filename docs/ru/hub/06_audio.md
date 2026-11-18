<!-- сгенерировано tools/build_hubs.py; не править руками (правки в docs/ru/README.md и в самих документах) -->
# Хаб: Звук: преобразователи, входы, выходы, аудиоплата

Решения темы: [`decisions/06_audio.md`](../decisions/06_audio.md) (4.5 КБ, читать, если задача касается решений темы).

## 11. Входы, выходы, форматы
Входы (2), MIDI/CV/синхро (4), USB (5), хранилище (6), форматы (7), питание и земля (8). Раздел 3 заменён документом 15
- [Штука Дрюка: входы, выходы, форматы, синхронизация, хранилище, питание](../11_io_formats_research/00_nachalo.md) · 0.5 КБ
- [0. Что уже решено](../11_io_formats_research/01_0-chto-uzhe-resheno.md) · 0.8 КБ
- [1. Как это сделано у других](../11_io_formats_research/02_1-kak-eto-sdelano-u-drugih.md) · 3.3 КБ
- [2. Входы](../11_io_formats_research/03_2-vhody.md) · 8.1 КБ
- [3. Выходы](../11_io_formats_research/04_3-vyhody.md) · 1.8 КБ
- [4. MIDI, CV и синхронизация](../11_io_formats_research/05_4-midi-cv-i-sinhronizaciya.md) · 3.8 КБ
- [5. USB, сеть, радио](../11_io_formats_research/06_5-usb-set-radio.md) · 1.9 КБ
- [6. Хранилище](../11_io_formats_research/07_6-hranilische.md) · 1.3 КБ
- [7. Форматы](../11_io_formats_research/08_7-formaty.md) · 2.5 КБ
- [8. Питание и земля](../11_io_formats_research/09_8-pitanie-i-zemlya.md) · 4.0 КБ
- [Открытые вопросы](../11_io_formats_research/10_otkrytye-voprosy.md) · 0.5 КБ

## 15. Аудиовыходы
Набор выходов, уровни, педальная петля
- [Аудиовыходы](../15_outputs_research.md) · 17.2 КБ

## 20. Звуковая карта для компьютера
Два порта xcore.ai, каналы, тактирование, 48/96 кГц
- [Звуковая карта для компьютера](../20_usb_audio_interface.md) · 14.6 КБ

## 21. Аудиоплата
Частично:  блок-схема, тактирование, управление — действуют; микросхемы (раздел 2) заменены документом 28
- [Штука Дрюка: аудиоплата — блок-схема и выбор микросхем](../21_audio_board/00_nachalo.md) · 0.9 КБ
- [0. Коротко](../21_audio_board/01_0-korotko.md) · 1.1 КБ
- [1. Требования (из журнала)](../21_audio_board/02_1-trebovaniya-iz-zhurnala.md) · 1.0 КБ
- [2. Микросхемы](../21_audio_board/03_2-mikroshemy.md) · 4.3 КБ
- [3. Раскладка каналов](../21_audio_board/04_3-raskladka-kanalov.md) · 0.8 КБ
- [4. Тактирование и шина](../21_audio_board/05_4-taktirovanie-i-shina.md) · 1.3 КБ
- [5. Управление и безопасность](../21_audio_board/06_5-upravlenie-i-bezopasnost.md) · 1.9 КБ
- [6. Расчёты](../21_audio_board/07_6-raschety.md) · 1.1 КБ
- [7. Питание (концепция)](../21_audio_board/08_7-pitanie-koncepciya.md) · 1.0 КБ
- [8. План проверки](../21_audio_board/09_8-plan-proverki.md) · 0.6 КБ
- [9. Перепроверка 01.11.2026 (P49, P51)](../21_audio_board/10_9-pereproverka-01-11-2026-p49.md) · 3.8 КБ
- [Открытые вопросы](../21_audio_board/11_otkrytye-voprosy.md) · 0.5 КБ

## 28. Входы и преобразователи
Входы с двумя путями, Cirrus Logic Pro (R116–R118)
- [Входы и преобразователи](../28_mic_inputs_and_converters.md) · 13.2 КБ

## 34. Платы задней стенки
R1, A1, R2, F1, PW: что на какой плате, живые микросхемы вместо снятых THAT, фантом, MIDI 3,3 В, CV, питание 19 В для Mini-ITX, номера LCSC
- [Штука Дрюка: платы задней стенки — входы, предусилители, выходы, управление, питание](../34_rear_boards_research/00_nachalo.md) · 1.2 КБ
- [0. Коротко](../34_rear_boards_research/01_0-korotko.md) · 3.3 КБ
- [1. Что на какой плате (вывод, по R120 и документу 29)](../34_rear_boards_research/02_1-chto-na-kakoy-plate-vyvod.md) · 2.4 КБ
- [2. Входы (R1 → A1)](../34_rear_boards_research/03_2-vhody-r1-a1.md) · 6.6 КБ
- [3. Выходы (A1 → R1, F1)](../34_rear_boards_research/04_3-vyhody-a1-r1-f1.md) · 1.9 КБ
- [4. Управление (R2)](../34_rear_boards_research/05_4-upravlenie-r2.md) · 2.6 КБ
- [5. Питание (PW)](../34_rear_boards_research/06_5-pitanie-pw.md) · 2.3 КБ
- [6. Гнёзда задней стенки (из библиотеки EasyEDA)](../34_rear_boards_research/07_6-gnezda-zadney-stenki-iz-biblioteki.md) · 0.8 КБ
- [7. Что проверить на макете (вывод)](../34_rear_boards_research/08_7-chto-proverit-na-makete-vyvod.md) · 0.5 КБ
- [Открытые вопросы](../34_rear_boards_research/09_otkrytye-voprosy.md) · 3.1 КБ
