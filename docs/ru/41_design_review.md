# 41. Дизайнерский разбор корпуса: почему «принтер» и три силуэта (17.11.2026)

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `41_design_review.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «41, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [00_nachalo](41_design_review/00_nachalo.md) | 41. Дизайнерский разбор корпуса: почему «принтер» и три силуэта (17.11.2026) | 4.8 |
| [01_1-korotko](41_design_review/01_1-korotko.md) | 1. Коротко | 1.9 |
| [02_2-chto-imenno-delaet-formu-printerom](41_design_review/02_2-chto-imenno-delaet-formu-printerom.md) | 2. Что именно делает форму «принтером» (с числами) | 3.9 |
| [03_3-tri-silueta](41_design_review/03_3-tri-silueta.md) | 3. Три силуэта | 5.1 |
| [04_4-ergonomika-proverka-po-siluetam](41_design_review/04_4-ergonomika-proverka-po-siluetam.md) | 4. Эргономика: проверка по силуэтам | 4.0 |
| [05_5-chto-kazhdyy-siluet-lomaet-i](41_design_review/05_5-chto-kazhdyy-siluet-lomaet-i.md) | 5. Что каждый силуэт ломает и что дороже | 2.9 |
| [06_6-cvet-material-detali-goditsya-dlya](41_design_review/06_6-cvet-material-detali-goditsya-dlya.md) | 6. Цвет, материал, детали (годится для любого силуэта) | 1.7 |
| [07_7-voprosy-polzovatelyu](41_design_review/07_7-voprosy-polzovatelyu.md) | 7. Вопросы пользователю | 2.2 |
| [08_10-analogi-razmery-i-forma-poisk](41_design_review/08_10-analogi-razmery-i-forma-poisk.md) | 10. Аналоги: размеры и форма (поиск 17.11.2026) | 4.9 |
| [09_11-ergonomika-chto-nashlos-i-chto](41_design_review/09_11-ergonomika-chto-nashlos-i-chto.md) | 11. Эргономика: что нашлось и что из этого следует | 3.6 |
| [10_12-otkuda-beretsya-vysota-budki-i](41_design_review/10_12-otkuda-beretsya-vysota-budki-i.md) | 12. Откуда берётся высота «будки» и что с этим делать | 3.9 |
| [11_15-vashi-dve-linii-progon-v](41_design_review/11_15-vashi-dve-linii-progon-v.md) | 15. Ваши две линии: прогон в модели посадки (17.11.2026, ночь) | 1.7 |
| [12_15-1-glavnoe-pochemu-sgib-byl](41_design_review/12_15-1-glavnoe-pochemu-sgib-byl.md) | 15.1 Главное: почему сгиб был 56 и почему он больше не нужен | 0.7 |
| [13_15-2-rezultat-progona](41_design_review/13_15-2-rezultat-progona.md) | 15.2 Результат прогона | 3.0 |
| [14_15-3-ergonomika-dvuh-variantov](41_design_review/14_15-3-ergonomika-dvuh-variantov.md) | 15.3 Эргономика двух вариантов | 1.5 |
| [15_15-4-chto-lomaetsya-i-chto](41_design_review/15_15-4-chto-lomaetsya-i-chto.md) | 15.4 Что ломается и что переделывать | 1.8 |
| [16_15-5-chto-ne-provereno](41_design_review/16_15-5-chto-ne-provereno.md) | 15.5 Что не проверено | 2.0 |
| [17_16-predlozheniya-glavnogo-dizaynera-i-zadanie](41_design_review/17_16-predlozheniya-glavnogo-dizaynera-i-zadanie.md) | 16. Предложения главного дизайнера и задание инженерам (17.11.2026) | 8.3 |
| [18_17-otvet-glavnomu-inzheneru-17-11](41_design_review/18_17-otvet-glavnomu-inzheneru-17-11.md) | 17. Ответ главному инженеру (17.11.2026) | 5.2 |
| [19_18-itogovaya-forma-bez-guby-eskizy](41_design_review/19_18-itogovaya-forma-bez-guby-eskizy.md) | 18. Итоговая форма без губы: эскизы и выводы дизайнера (17.11.2026) | 5.7 |
| [20_19-zelenaya-liniya-deka-30-bez](41_design_review/20_19-zelenaya-liniya-deka-30-bez.md) | 19. «Зелёная» линия: дека 30, без ступеньки, глубина 500 (17.11.2026) | 5.6 |
| [21_20-tri-koncepta-zad-120-sovmestno](41_design_review/21_20-tri-koncepta-zad-120-sovmestno.md) | 20. Три концепта «зад ≤ 120» (совместно с главным инженером, 17.11.2026) | 5.6 |
| [22_21-artefakt-v8-pravki-vida-i](41_design_review/22_21-artefakt-v8-pravki-vida-i.md) | 21. Артефакт v8: правки вида и концепты К1–К3 параметрами генератора (17.11.2026) | 7.6 |
| [23_22-ventilyator-na-pravoy-stenke-h5](41_design_review/23_22-ventilyator-na-pravoy-stenke-h5.md) | 22. Вентилятор на правой стенке, H5 вплотную к задней (идея пользователя, проверено главной сессией, 17.11.2026) | 2.3 |
| [24_23-nabrosok-polzovatelya-na-v8-makushku](41_design_review/24_23-nabrosok-polzovatelya-na-v8-makushku.md) | 23. Набросок пользователя на v8: макушку ниже, зад назад, экран краем к коробке задних гнёзд (17.11.2026) | 4.5 |
| [25_24-zadnyaya-stenka-v5-i-scheli](41_design_review/25_24-zadnyaya-stenka-v5-i-scheli.md) | 24. Задняя стенка v5 и щели в люке (18.11.2026) | 1.0 |
| [26_24-1-raskladka-v5-v4-otklonena](41_design_review/26_24-1-raskladka-v5-v4-otklonena.md) | 24.1 Раскладка v5 (v4 отклонена пользователем) | 3.5 |
| [27_24-2-v5-2-edinaya-setka](41_design_review/27_24-2-v5-2-edinaya-setka.md) | 24.2 v5.2: единая сетка (пользователь: «криво, косо, некрасиво») | 2.0 |
| [28_24-4-v6-po-karte-svobodnyh](41_design_review/28_24-4-v6-po-karte-svobodnyh.md) | 24.4 v6: по карте свободных зон главного инженера (18.11.2026) | 3.2 |
| [29_24-5-ventilyator-reshen-inzhener-18](41_design_review/29_24-5-ventilyator-reshen-inzhener-18.md) | 24.5 Вентилятор решён (инженер, 18.11.2026): один 80 × 80 × 25, прорезь, ножки | 2.1 |
| [30_24-3-ventilyaciya-tolko-scheli-v](41_design_review/30_24-3-ventilyaciya-tolko-scheli-v.md) | 24.3 Вентиляция: только щели в люке под аккумуляторами (R185) | 0.7 |
| [31_25-istochniki](41_design_review/31_25-istochniki.md) | 25. Источники | 0.7 |
| [32_26-chto-ne-sdelano](41_design_review/32_26-chto-ne-sdelano.md) | 26. Что не сделано | 0.9 |

Проверка полноты: `python tools/split_docs.py --verify docs/ru/41_design_review.md`.
