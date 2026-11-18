# Штука Дрюка: органы управления — энкодеры, навигация, кнопки, сетка, 16 дорожек

**Документ разбит на части ради экономии контекста** (исходный текст перенесён без потерь, файл `09_controls_research.md` теперь индекс).
Читай только нужную часть. Номера разделов и решений прежние: «09, раздел N» = часть с этим номером в названии. Номера строк в старых отчётах относятся к версии до разбиения (см. историю git).

| Часть | Раздел | КБ |
|---|---|---|
| [00_nachalo](09_controls_research/00_nachalo.md) | Штука Дрюка: органы управления — энкодеры, навигация, кнопки, сетка, 16 дорожек | 0.6 |
| [01_resheniya-polzovatelya-ot-kotoryh-zdes-ottalkivaemsya](09_controls_research/01_resheniya-polzovatelya-ot-kotoryh-zdes-ottalkivaemsya.md) | Решения пользователя, от которых здесь отталкиваемся | 1.3 |
| [02_1-enkodery](09_controls_research/02_1-enkodery.md) | 1. Энкодеры | 0.0 |
| [03_1-1-pochemu-beskonechnye-pravilno-vyvod](09_controls_research/03_1-1-pochemu-beskonechnye-pravilno-vyvod.md) | 1.1 Почему бесконечные — правильно (вывод, с опорой на источники) | 1.0 |
| [04_1-2-tipy-enkoderov](09_controls_research/04_1-2-tipy-enkoderov.md) | 1.2 Типы энкодеров | 5.2 |
| [05_1-6-ceny-i-vybor-posle](09_controls_research/05_1-6-ceny-i-vybor-posle.md) | 1.6 Цены и выбор после R28 (31.10.2026) | 1.2 |
| [06_1-3-schelchki-fiksaciya-po-rolyam](09_controls_research/06_1-3-schelchki-fiksaciya-po-rolyam.md) | 1.3 Щелчки (фиксация): по ролям | 1.9 |
| [07_1-4-razreshenie-i-uskorenie](09_controls_research/07_1-4-razreshenie-i-uskorenie.md) | 1.4 Разрешение и ускорение | 1.6 |
| [08_1-5-kasanie-sensornye-enkodery](09_controls_research/08_1-5-kasanie-sensornye-enkodery.md) | 1.5 Касание (сенсорные энкодеры) | 1.5 |
| [09_1-6-razmer-kolpachkov-i-shag](09_controls_research/09_1-6-razmer-kolpachkov-i-shag.md) | 1.6 Размер колпачков и шаг между энкодерами | 2.3 |
| [10_1-7-skolko-poluchaetsya-enkoderov](09_controls_research/10_1-7-skolko-poluchaetsya-enkoderov.md) | 1.7 Сколько получается энкодеров | 1.0 |
| [11_2-ruchka-navigacii](09_controls_research/11_2-ruchka-navigacii.md) | 2. Ручка навигации | 4.0 |
| [12_3-knopki](09_controls_research/12_3-knopki.md) | 3. Кнопки | 4.3 |
| [13_4-krossfeyder-sensornye-polosy-feydery](09_controls_research/13_4-krossfeyder-sensornye-polosy-feydery.md) | 4. Кроссфейдер, сенсорные полосы, фейдеры | 2.2 |
| [14_5-setka-pedov](09_controls_research/14_5-setka-pedov.md) | 5. Сетка пэдов | 2.9 |
| [15_6-kak-zhit-s-16-dorozhkami](09_controls_research/15_6-kak-zhit-s-16-dorozhkami.md) | 6. Как жить с 16+ дорожками | 8.7 |
| [16_7-gde-stavit-8-enkoderov-otnositelno](09_controls_research/16_7-gde-stavit-8-enkoderov-otnositelno.md) | 7. Где ставить 8 энкодеров относительно экрана | 1.3 |
| [17_otkrytye-voprosy-etogo-dokumenta](09_controls_research/17_otkrytye-voprosy-etogo-dokumenta.md) | Открытые вопросы этого документа | 0.5 |

Проверка полноты: `python tools/split_docs.py --verify docs/ru/09_controls_research.md`.
