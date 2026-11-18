# 41. Дизайнерский разбор корпуса: почему «принтер» и три силуэта (17.11.2026)

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `41_design_review.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «41, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [08_10-analogi-razmery-i-forma-poisk](41_design_review/08_10-analogi-razmery-i-forma-poisk.md) | 10. Аналоги: размеры и форма (поиск 17.11.2026) | 4.9 |
| [09_11-ergonomika-chto-nashlos-i-chto](41_design_review/09_11-ergonomika-chto-nashlos-i-chto.md) | 11. Эргономика: что нашлось и что из этого следует | 3.6 |
| [20_19-zelenaya-liniya-deka-30-bez](41_design_review/20_19-zelenaya-liniya-deka-30-bez.md) | 19. «Зелёная» линия: дека 30, без ступеньки, глубина 500 (17.11.2026) | 5.6 |
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
