> Часть документа 34 ([индекс](../34_rear_boards_research.md)): 4. Управление (R2)

## 4. Управление (R2)

| Узел | Деталь | Факт | LCSC |
|---|---|---|---|
| Микроконтроллер | RP2350A (R85) | — | в библиотеке есть (C9900136995 — номер библиотеки EasyEDA, не склада LCSC; проверить складской) |
| USB-хаб | Microchip USB2514B, 4 порта High-Speed | «In Production» ([Microchip](https://www.microchip.com/en-us/product/USB2514B)) | C633338 |
| MIDI выход 3,3 В | 2 резистора на гнездо | CA-033 (2014): при 3,3 В ± 5 % — 33 Ом / 0,5 Вт и 10 Ом; при 5 В — 220 / 220 Ом; петля 5 мА, фронты < 2 мкс; ферритовые бусины 1 кОм на 100 МГц — по желанию ([MIDI.org, CA-033](https://midi.org/wp-content/uploads/wpforo/default_attachments/1709416667-ca33-MIDI-10-Electrical-Specification-Update.pdf)) | — |
| MIDI вход | Оптрон на 3,3 В: TLP2361 (SMD) или H11L1 / PC900V | 6N138 от 3,3 В — вне даташита; на 3,3 В советуют H11L1 или 3,3-вольтовые TLP2361, HCPL-260L ([mt32-pi wiki](https://github.com/dwhinham/mt32-pi/wiki/GPIO-MIDI-interface), [MIDI.org форум](https://midi.org/community/midi-hardware/best-optoisolator-for-3-3v)) | TLP2361 C107626, H11L1 C255760 |
| CV/Gate 8 выходов | ADI AD5676R + масштабирующие ОУ на ±12 В | 8 × 16 бит, опора 2 ppm/°C, INL ±3 LSB, выход 0…Vref или 0…2Vref ([ADI](https://www.analog.com/en/products/ad5676r.html)); запасной TI DAC8568 (INL 4 LSB) | AD5676RBRUZ C488149, DAC8568ICPW C2868758 |
| CV-входы 4 | Делитель и сдвиг ±10 В → 0…3,3 В, АЦП RP2350 | вывод | — |
| Гнёзда 3,5 мм (MIDI TRS, CV, синхро) | Тип PJ398SM («Thonkiconn») | в библиотеке — WQP-PJ398SM | C9900009788 (номер библиотеки, проверить склад) |

**Расчёт CV (вывод).** Диапазон −10…+10 В = 20 В; шаг 16 бит: 20 В / 65 536 ≈ 0,305 мВ. При 1 В/окт полутон = 1000 / 12 ≈ 83,3 мВ, цент ≈ 0,833 мВ → шаг ЦАП ≈ 0,37 цента. Ошибка ±3 LSB ≈ ±0,9 мВ ≈ ±1,1 цента — убирается калибровкой (R35).

**Вывод — порты хаба:** вверх — Mini-ITX; вниз — панель P2 (R86), A1 порт A (R82), RP2350 на R2; четвёртый свободен. Экран (тач) идёт прямо в Mini-ITX (R110). Четырёх портов хватает.
