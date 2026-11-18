# Штука Дрюка: протокол между платами и вычислителем (SDP v0)

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `19_panel_protocol.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «19, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [00_nachalo](19_panel_protocol/00_nachalo.md) | Штука Дрюка: протокол между платами и вычислителем (SDP v0) | 0.6 |
| [01_0-korotko](19_panel_protocol/01_0-korotko.md) | 0. Коротко | 1.6 |
| [02_1-kak-eto-sdelano-u-drugih](19_panel_protocol/02_1-kak-eto-sdelano-u-drugih.md) | 1. Как это сделано у других | 2.7 |
| [03_2-arhitektura](19_panel_protocol/03_2-arhitektura.md) | 2. Архитектура | 2.3 |
| [04_3-transport](19_panel_protocol/04_3-transport.md) | 3. Транспорт | 1.2 |
| [05_4-kadr-sdp](19_panel_protocol/05_4-kadr-sdp.md) | 4. Кадр SDP | 1.0 |
| [06_5-soobscheniya](19_panel_protocol/06_5-soobscheniya.md) | 5. Сообщения | 5.4 |
| [07_6-vremya-i-zaderzhka-raschet](19_panel_protocol/07_6-vremya-i-zaderzhka-raschet.md) | 6. Время и задержка (расчёт) | 1.4 |
| [08_7-propusknaya-sposobnost-raschet](19_panel_protocol/08_7-propusknaya-sposobnost-raschet.md) | 7. Пропускная способность (расчёт) | 1.1 |
| [09_8-bezopasnost](19_panel_protocol/09_8-bezopasnost.md) | 8. Безопасность | 0.9 |
| [10_9-naydennaya-problema-usb-c-k](19_panel_protocol/10_9-naydennaya-problema-usb-c-k.md) | 9. Найденная проблема: «USB-C к компьютеру» | 1.2 |
| [11_10-proverka-zagotovki-koda](19_panel_protocol/11_10-proverka-zagotovki-koda.md) | 10. Проверка заготовки кода | 1.0 |
| [12_11-simulyator-r31](19_panel_protocol/12_11-simulyator-r31.md) | 11. Симулятор (R31) | 0.5 |
| [13_resheno](19_panel_protocol/13_resheno.md) | Решено | 0.2 |
| [14_otkrytye-voprosy](19_panel_protocol/14_otkrytye-voprosy.md) | Открытые вопросы | 0.1 |

Проверка полноты: `python tools/split_docs.py --verify docs/ru/19_panel_protocol.md`.
