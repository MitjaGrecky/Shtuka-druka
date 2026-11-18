# Штука Дрюка: платы задней стенки — входы, предусилители, выходы, управление, питание

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `34_rear_boards_research.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «34, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [00_nachalo](34_rear_boards_research/00_nachalo.md) | Штука Дрюка: платы задней стенки — входы, предусилители, выходы, управление, питание | 1.2 |
| [01_0-korotko](34_rear_boards_research/01_0-korotko.md) | 0. Коротко | 3.3 |
| [02_1-chto-na-kakoy-plate-vyvod](34_rear_boards_research/02_1-chto-na-kakoy-plate-vyvod.md) | 1. Что на какой плате (вывод, по R120 и документу 29) | 2.4 |
| [03_2-vhody-r1-a1](34_rear_boards_research/03_2-vhody-r1-a1.md) | 2. Входы (R1 → A1) | 6.6 |
| [04_3-vyhody-a1-r1-f1](34_rear_boards_research/04_3-vyhody-a1-r1-f1.md) | 3. Выходы (A1 → R1, F1) | 1.9 |
| [05_4-upravlenie-r2](34_rear_boards_research/05_4-upravlenie-r2.md) | 4. Управление (R2) | 2.6 |
| [06_5-pitanie-pw](34_rear_boards_research/06_5-pitanie-pw.md) | 5. Питание (PW) | 2.3 |
| [07_6-gnezda-zadney-stenki-iz-biblioteki](34_rear_boards_research/07_6-gnezda-zadney-stenki-iz-biblioteki.md) | 6. Гнёзда задней стенки (из библиотеки EasyEDA) | 0.8 |
| [08_7-chto-proverit-na-makete-vyvod](34_rear_boards_research/08_7-chto-proverit-na-makete-vyvod.md) | 7. Что проверить на макете (вывод) | 0.5 |

Проверка полноты: `python tools/split_docs.py --verify docs/ru/34_rear_boards_research.md`.
