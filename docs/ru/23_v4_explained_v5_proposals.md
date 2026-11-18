# Штука Дрюка: что я сделал в макете v4, почему, и что поменять (наброски v5)

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `23_v4_explained_v5_proposals.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «23, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [00_nachalo](23_v4_explained_v5_proposals/00_nachalo.md) | Штука Дрюка: что я сделал в макете v4, почему, и что поменять (наброски v5) | 0.4 |
| [01_0-principy-polzovatelya-resheno-r89](23_v4_explained_v5_proposals/01_0-principy-polzovatelya-resheno-r89.md) | 0. Принципы пользователя (решено, R89) | 0.8 |
| [02_1-ustroystva-polzovatelya-i-chemu-oni](23_v4_explained_v5_proposals/02_1-ustroystva-polzovatelya-i-chemu-oni.md) | 1. Устройства пользователя и чему они учат | 2.2 |
| [03_2-razbor-v4-chto-pochemu-chto](23_v4_explained_v5_proposals/03_2-razbor-v4-chto-pochemu-chto.md) | 2. Разбор v4: что, почему, что предлагаю | 4.2 |
| [04_3-koleso-i-strelki-pochemu-tak](23_v4_explained_v5_proposals/04_3-koleso-i-strelki-pochemu-tak.md) | 3. Колесо и стрелки: почему так и как развести | 1.3 |
| [05_4-blok-urovni-za-i-protiv](23_v4_explained_v5_proposals/05_4-blok-urovni-za-i-protiv.md) | 4. Блок «Уровни»: за и против | 1.7 |
| [06_5-nabrosok-v5-predlozheniya-p53-p55](23_v4_explained_v5_proposals/06_5-nabrosok-v5-predlozheniya-p53-p55.md) | 5. Набросок v5 (предложения P53–P55 в журнале) | 1.0 |
| [07_6-chastota-ispolzovaniya-r90-p56](23_v4_explained_v5_proposals/07_6-chastota-ispolzovaniya-r90-p56.md) | 6. Частота использования (R90, P56) | 3.2 |
| [08_7-filtr-vysoty-r91-p57](23_v4_explained_v5_proposals/08_7-filtr-vysoty-r91-p57.md) | 7. Фильтр высоты (R91, P57) | 3.3 |
| [09_8-push-1-ne-etalon-chto](23_v4_explained_v5_proposals/09_8-push-1-ne-etalon-chto.md) | 8. Push 1 — не эталон: что поменяли в Push 2 и Push 3 (R92) | 3.1 |
| [10_9-orientaciya-setki-dorozhki-strokami-ili](23_v4_explained_v5_proposals/10_9-orientaciya-setki-dorozhki-strokami-ili.md) | 9. Ориентация сетки: дорожки строками или столбцами | 4.7 |
| [11_otkrytye-voprosy](23_v4_explained_v5_proposals/11_otkrytye-voprosy.md) | Открытые вопросы | 0.7 |

Проверка полноты: `python tools/split_docs.py --verify docs/ru/23_v4_explained_v5_proposals.md`.
