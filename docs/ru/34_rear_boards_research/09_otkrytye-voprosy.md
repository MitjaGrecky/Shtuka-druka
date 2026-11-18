> Часть документа 34 ([индекс](../34_rear_boards_research.md)): Открытые вопросы

## Открытые вопросы

> **Ответы 13.11.2026:** 1 — +24 dBu (R135); 2 — CS4308P со своей посадкой (R136; ES9039PRO и AK4499EX — токовый выход, отказались); 3 — реле (R137); 4 — начинаем с R2 (R138).

1. **Запас линейных входов:** +18 dBu или +24 dBu? От этого и от полной шкалы CS5308P (даташит DS1314F2, заметка AN0556 — взять) зависит ослабление в драйвере АЦП.
2. **ЦАП CS4308P нет в библиотеке EasyEDA:** рисуем символ и посадочное место сами (корпус QFN, по даташиту) или берём запасной AKM AK4458 — он в библиотеке есть (AK4458VN, C1520729), но хуже по цифрам (115 против 123 дБА, документ 28)? Предлагаю CS4308P со своей посадкой.
3. **Ключи выходов:** реле (размыкаются сами без питания, R66) — или полевые ключи (тише, но без питания не гарантированно разомкнуты)? Предлагаю реле.
4. **Порядок работы:** начинаю схемы с R2 (цифровая, без риска для звука) или с макета входного узла R1 (самое рискованное — склейка путей)?

Sources:
- [TI OPA1612](https://www.ti.com/product/OPA1612), [TI OPA1642](https://www.ti.com/product/OPA1642), [TI OPA1637](https://www.ti.com/product/OPA1637), [TI INA1620](https://www.ti.com/product/INA1620), [TI INA1650](https://ti.com/document-viewer/INA1650/datasheet), [TI DRV134](https://www.ti.com/product/DRV134)
- [Cirrus CS5308P](https://www.cirrus.com/products/cs5308p/)
- [TI PMP40871 (фантом 48 В)](https://ti.com/tool/PMP40871), [TI TIDT235](https://ti.com/lit/pdf/tidt235), [ADI фантом на LT8362](https://www.radiolocman.com/shem/schematics.html?di=618795)
- [TI TIDA-01458 (±12 В)](https://www.ti.com/tool/TIDA-01458), [TI TPS7A47](https://ti.com/product/TPS7A47), [TI E2E: TPS65131 5 → ±14 → ±12 В](https://e2e.ti.com/support/power-management-group/power-management/f/power-management-forum/1419211/tps65131-request-for-schematic-review)
- [TI TPS25730](https://www.ti.com/document-viewer/TPS25730/datasheet)
- [ASRock N100DC-ITX](https://www.asrock.com/MB/Intel/N100DC-ITX/index.asp), [mini-ITX.com N100DC-ITX](https://www.mini-ITX.com/~N100DC-ITX)
- [MIDI CA-033 (2014)](https://midi.org/wp-content/uploads/wpforo/default_attachments/1709416667-ca33-MIDI-10-Electrical-Specification-Update.pdf), [mt32-pi: GPIO MIDI](https://github.com/dwhinham/mt32-pi/wiki/GPIO-MIDI-interface), [MIDI.org: оптрон для 3,3 В](https://midi.org/community/midi-hardware/best-optoisolator-for-3-3v)
- [ADI AD5676R](https://www.analog.com/en/products/ad5676r.html), [TI DAC8568](https://www.ti.com/lit/gpn/dac8568)
- [Microchip USB2514B](https://www.microchip.com/en-us/product/USB2514B)
- Номера LCSC — библиотека EasyEDA Pro через `tools/eda/eda_parts.py`, 13.11.2026.
