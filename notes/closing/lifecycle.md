# Жизненный цикл деталей по платам (R200), технолог, 26.11.2026

Источники: **TI** — приложение «PACKAGE OPTION ADDENDUM» в даташите производителя (первичный). Остальное: страницы производителя там, где указано; иначе дистрибьюторы из поисковой выдачи (вторичный). «не найден» = явного статуса не увидел; LCSC «normal» статусом производителя не считается. «проверить» = источники противоречат. EOL без замены не обнаружен. Пассивные R/C, сборки и дроссели не проверялись. Закупкой не занимался.

## Вердикты

| Плата | Можно разводить? | active | проверить | не найден |
|---|---|---|---|---|
| M3 | да (EC11E: см. оговорку) | 2 | 1 | 2 |
| M4 | да (EC11E: оговорка) | 2 | 1 | 2 |
| M5 | да (EC11E: оговорка) | 2 | 1 | 2 |
| P1 | да | 3 | 0 | 4 |
| P3 | да (EC11E: оговорка) | 4 | 1 | 4 |
| P4 | да с оговоркой: AS5600 не подтверждён, посадка SOIC-8 общая с AS5600L; кроссфейдер PTA4543 не выбран — его посадку до разводки подтвердить | 5 | 1 | 5 |
| W1 | да | 4 | 0 | 3 |
| W2 | да | 1 | 0 | 2 |
| W3 | да | 2 | 0 | 3 |
| M1 | да (EC11E: оговорка) | 3 | 1 | 2 |
| P2 | да | 6 | 0 | 13 |
| A1 | да с оговоркой: W25Q32 (запас в той же посадке); суффикс XU316 выбрать | 9 | 1 | 8 |
| F1 | да с оговоркой: CL1115 статус не найден и карта выводов не проверена на живом разъёме | 2 | 0 | 5 |
| R1 | да с оговоркой: NCJ6FI-V возможно снимается, замены в той же посадке нет — подтвердить у Neutrik до разводки | 4 | 1 | 11 |
| R2 | да | 6 | 0 | 16 |
| PW | да по статусам (все микросхемы TI Active); прежний запрет README PW (проверка пакета) остаётся | 16 | 0 | 16 |
| U1 | да | 0 | 0 | 1 |
| BB1 | да по статусам (TI Active); запрет на заказ до проверки пакета остаётся | 2 | 0 | 1 |

## По платам (деталь: позиция ×кол-во — статус)

**M3**: XL-1615RGBC-RF (D1×24) — не найден; EC11E1834403 (ENC1×2) — проверить; HCTL PZ127-2-07-Z (J1×1) — не найден; LP5864RSMR (U1×1) — active; 74HC165PW (U2×1) — active.

**M4**: XL-1615RGBC-RF (D1×24) — не найден; EC11E1834403 (ENC1×2) — проверить; HCTL PZ127-2-07-Z (J1×1) — не найден; LP5864RSMR (U1×1) — active; 74HC165PW (U2×1) — active.

**M5**: XL-1615RGBC-RF (D1×24) — не найден; EC11E1834403 (ENC1×2) — проверить; HCTL PZ127-2-07-Z (J1×1) — не найден; LP5864RSMR (U1×1) — active; 74HC165PW (U2×1) — active.

**P1**: XL-1615RGBC-RF (D1×38) — не найден; HCTL PZ127-2-08-Z (J1×1) — не найден; HCTL PZ127-2-07-Z (J2×2) — не найден; TS-1187A-B-A-B (SW1×19) — не найден; LP5864RSMR (U1×2) — active; 74HC165PW (U3×3) — active; TCA9546APWR (U6×1) — active.

**P3**: XL-1615RGBC-RF (D1×138) — не найден; EC11E1834403 (ENC1×8) — проверить; HCTL PZ127-2-08-Z (J1×1) — не найден; HCTL PZ127-2-07-Z (J3×2) — не найден; TS-1187A-B-A-B (SW1×21) — не найден; LP5864RSMR (U1×6) — active; 74HC165PW (U3×6) — active; TCA9546APWR (U6×1) — active; CY8CMBR3108-LQXIT (U11×1) — active.

**P4**: XL-1615RGBC-RF (D1×40) — не найден; HCTL PZ127-2-08-Z (J1×1) — не найден; HCTL PZ127-2-07-Z (J3×1) — не найден; S2B-PH-K-S(LF)(SN) (J4×1) — не найден; PTA4543-2015DPB103 (RV1×1) — active; TS-1187A-B-A-B (SW1×20) — не найден; LP5864RSMR (U1×2) — active; 74HC165PW (U3×3) — active; TCA9546APWR (U6×1) — active; ADS1115IDGSR (U7×1) — active; AS5600-ASOT (U8×1) — проверить.

**W1**: XL-1615RGBC-RF (D1×4) — не найден; HCTL PZ127-2-07-Z (J1×2) — не найден; RK09K1130A5R (RV1×4) — active; TS-1187A-B-A-B (SW1×2) — не найден; ADS1115IDGSR (U1×1) — active; 74HC165PW (U2×1) — active; IS31FL3218-QFLS2-TR (U3×1) — active.

**W2**: XL-1615RGBC-RF (D1×28) — не найден; HCTL PZ127-2-07-Z (J1×1) — не найден; LP5864RSMR (U1×2) — active.

**W3**: XL-1615RGBC-RF (D1×5) — не найден; HCTL PZ127-2-07-Z (J1×1) — не найден; TS-1187A-B-A-B (SW1×2) — не найден; LP5864RSMR (U1×1) — active; 74HC165PW (U2×1) — active.

**M1**: XL-1615RGBC-RF (D1×96) — не найден; EC11E1834403 (ENC1×8) — проверить; HCTL PZ127-2-07-Z (J1×1) — не найден; LP5864RSMR (U1×4) — active; CY8CMBR3108-LQXIT (U2×1) — active; 74HC165PW (U3×3) — active.

**P2**: NCD0603G1 (D1×1) — не найден; XL-1615RGBC-RF (D2×109) — не найден; Molex 43650-0600 (J1×1) — не найден; S3B-PH-K-S(LF)(SN) (J2×1) — не найден; S4B-PH-K-S(LF)(SN) (J3×3) — не найден; HCTL PZ127-2-07-Z (J4×1) — не найден; HCTL PZ127-2-08-Z (J5×3) — не найден; S8B-PH-K-S(LF)(SN) (J10×1) — не найден; TS-1187A-B-A-B (SW1×11) — не найден; AP2112K-3.3 (U1×1) — active; RP2350A (U2×1) — active; W25Q128JVSIQ (U3×1) — не найден; USBLC6-2SC6 (U4×1) — не найден; ADC128S102 (U5×1) — active; 74HC4051 (U6×8) — не найден; TCA9546APWR (U14×1) — active; LP5864RSMR (U15×5) — active; 74HC165PW (U20×2) — active; ABM8-272-T3 (Y1×1) — не найден.

**A1**: BAT54S (D1×40) — не найден; B4B-PH-K-S(LF)(SN) (J4×2) — не найден; B6B-PH-K-S(LF)(SN) (J5×4) — не найден; AP2112K-3.3 (U1×1) — active; AP2112K-1.8 (U2×1) — не найден; TPS7A4701 (U3×1) — active; TLV62568 (U4×2) — active; CS5308P (U6×2) — active; CS5304P (U8×1) — active; OPA1656 (U9×28) — active; CS4308P (U29×1) — active; XU316-1024-QF60B (U38×2) — active; W25Q32JVSSIQ (U40×2) — проверить; USBLC6-2SC6 (U42×2) — не найден; ISOUSB211DPR (U44×1) — active; SX3M24.576B10F20TNN (Y1×1) — не найден; SX3M22.5792B10F20TNN (Y2×1) — не найден; X322524MOB4SI (Y3×2) — не найден.

**F1**: 1N4148W (D1×1) — не найден; S4B-PH-K-S(LF)(SN) (J2×1) — не найден; S3B-PH-K-S(LF)(SN) (J3×1) — не найден; CL1115 (J4×2) — не найден; G6K-2F-Y 5V (K1×2) — active; AO3400A (Q1×2) — не найден; OPA1622 (U1×2) — active.

**R1**: SMBJ18CA (D1×4) — не найден; 1N4148W (D2×18) — не найден; Molex 43045-1012 (J1×1) — не найден; B3B-PH-K-S(LF)(SN) (J3×2) — не найден; NCJ6FI-V (J6×2) — проверить; NJ3FD-V (J8×14) — не найден; RCJ-025 (J10×4) — не найден; B2B-PH-K-S(LF)(SN) (J26×1) — не найден; G6K-2F-Y 5V (K1×7) — active; MMBTA92 (Q1×2) — не найден; MMBTA42 (Q2×2) — не найден; 2N7002 (Q5×3) — не найден; AO3400A (Q8×2) — не найден; OPA1612 (U1×5) — active; OPA1637 (U2×18) — active; OPA1642 (U7×1) — active.

**R2**: NCD0603G1 (D1×1) — не найден; 1N4148W (D2×4) — не найден; BAT54S (D4×4) — не найден; B5B-PH-K-S(LF)(SN) (J1×1) — не найден; B3B-PH-K-S(LF)(SN) (J2×5) — не найден; B4B-PH-K-S(LF)(SN) (J3×4) — не найден; B2B-PH-K-S(LF)(SN) (J11×2) — не найден; PJ-3920-3A (J14×3) — не найден; PJ398SM (J17×17) — не найден; MMBT3904 (Q1×2) — не найден; TS-1187A-B-A-B (SW1×1) — не найден; AP2112K-3.3 (U1×1) — active; RP2350A (U2×1) — active; W25Q128JVSIQ (U3×1) — не найден; USB2514B (U4×1) — active; TPS2051B (U5×3) — active; 74HC595 (U8×1) — не найден; TLP2361 (U9×4) — не найден; DAC80504 (U13×2) — active; OPA4197 (U15×3) — active; ABM8-272-T3 (Y1×1) — не найден; X322524MOB4SI (Y2×1) — не найден.

**PW**: SMBJ28CA (D1×1) — не найден; SMBJ20CA (D2×2) — не найден; SMBJ13CA (D4×2) — не найден; NCD0603G1 (D5×3) — не найден; B560C (D8×2) — не найден; SS1H10 (D10×1) — не найден; BZT52C3V3 (D12×1) — не найден; Molex 43650-0215 (J1×1) — не найден; Molex 43045-0612 (J2×4) — не найден; Molex 43045-0412 (J5×2) — не найден; B8B-PH-K-S(LF)(SN) (J6×1) — не найден; B5B-PH-K-S(LF)(SN) (J9×1) — не найден; Molex 43045-1012 (J10×1) — не найден; B4B-PH-K-S(LF)(SN) (J11×1) — не найден; B2B-PH-K-S(LF)(SN) (J12×1) — не найден; CSD18532Q5B (Q1×9) — active; 2N7002 (Q5×4) — не найден; IRLML0100 (Q14×1) — active; LM74700-Q1 (U1×5) — active; TPS25730D (U2×1) — active; BQ25798 (U6×2) — active; INA226 (U9×1) — active; AP2112K-3.3 (U10×1) — active; TCA9546APW (U11×1) — active; LM5176 (U12×1) — active; TPS54560B (U13×2) — active; LMR33640 (U15×4) — active; TPS7A4701 (U17×1) — active; TPS7A3301 (U18×1) — active; LM5156H (U19×1) — active; TPS7A4101 (U20×1) — active; TPS26631RGER (U23×1) — active.

**U1**: USB4105-GF-A (J1×1) — не найден.

**BB1**: BQ7791500 (U×2) — active; CSD18532Q5B (Q×2) — active; Molex 43045-0600 (J×1) — не найден. Без статуса/MPN: NTC 103AT, шунт и прочие разъёмы BB1: BOM_clean для BB1 нет, список из gen/ неполный.

## Детали: статус, источник, замена

| Деталь | Статус | Источник | Замена / замечание |
|---|---|---|---|
| EC11E1834403 | проверить | Alps PCN: снят 09.08.2021 (farnell.com/datasheets/3565107.pdf) и 28.02.2023 (media.futureelectronics.com/PCN/96258_SPCN.PDF), 17.03.2023 восстановлен «Remain Active, system error» (…/96683_SPCN.PDF). RS/Octopart: снят/NRND | последний документ производителя: Active. Запас: любой EC11 20 мм гладкий с кнопкой в той же посадке |
| AS5600-ASOT | проверить | противоречие: SnapMagic Obsolete, Digipart Active; страница ams без явного статуса https://ams-osram.com/de/products/sensor-solutions/position-sensors/ams-as5600-position-sensor | запас в той же посадке SOIC-8: AS5600L-ASOM (I²C 0x40 вместо 0x36) |
| W25Q32JVSSIQ | проверить | Digi-Key Active; Octopart EOL (противоречие) https://octopart.com/part/winbond/W25Q32JVSSIQ | запас SOIC-8 208 mil: W25Q64JV или W25Q128JVSIQ |
| NCJ6FI-V | проверить | страница и чертёж на neutrik.com есть (19.11), но Adam Hall «archive», Markertek «no longer available» | запас в BOM нет; NCJ6FA-V — другая посадка |
| LP5864RSMR | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/lp5864.pdf | — |
| 74HC165PW | active | Nexperia https://www.nexperia.com/pip/74HC165PW (через поиск: Active) | — |
| TCA9546APWR | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tca9546a.pdf | — |
| CY8CMBR3108-LQXIT | active | Digi-Key/Future/Arrow Active (не производитель) https://www.digikey.ie/en/products/detail/infineon-technologies/CY8CMBR3108-LQXIT/5825530 | — |
| PTA4543-2015DPB103 | active | Digi-Key Active (не производитель) https://www.digikey.com.br/en/products/detail/bourns-inc/PTA4543-2015DPB103/3534245 | деталь в проекте «заглушка» (не выбрана) |
| ADS1115IDGSR | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/ads1115.pdf | — |
| RK09K1130A5R | active | Digi-Key Active, Octopart Production (поиск; не производитель) https://octopart.com/part/alps/RK09K1130A5R | — |
| IS31FL3218-QFLS2-TR | active | Digi-Key Active (не производитель) https://www.digikey.at/en/products/detail/lumissil-microsystems/IS31FL3218-QFLS2-TR/5319749 | — |
| AP2112K-3.3 | active | Digi-Key Active (Diodes AP2112K-3.3TRG1) | — |
| RP2350A | active | Raspberry Pi: производство до января 2045 https://datasheets.raspberrypi.com/rp2350/rp2350-product-brief.pdf | — |
| ADC128S102 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/adc128s102.pdf | — |
| TPS7A4701 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps7a47.pdf | — |
| TLV62568 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tlv62568.pdf | — |
| CS5308P, CS5304P | active | Cirrus EOL-лист: указаны как замена снятых CS5364/66/68 https://cirrus.com/products/eol | — |
| OPA1656 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa1656.pdf | — |
| CS4308P | active | Digi-Key CS4308P-DNR Active; в EOL-листе Cirrus как снятый не значится | — |
| XU316-1024-QF60B | active | Digi-Key Active для -C24 https://www.digikey.at/en/products/detail/xmos/XU316-1024-QF60B-C24/16839845 | в BOM без суффикса: заказной код выбрать (-C32 / -C24) |
| ISOUSB211DPR | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/isousb211.pdf | — |
| G6K-2F-Y 5V | active | Octopart Production (не производитель) https://octopart.com/part/omron/G6K-2F-Y%20DC5 | — |
| OPA1622 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa1622.pdf | — |
| OPA1612 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa1612.pdf | — |
| OPA1637 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa1637.pdf | — |
| OPA1642 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa1642.pdf | — |
| USB2514B | active | Octopart Production/REL, Microchip USB2514B In Production (NRND только у USB2514 без B) | — |
| TPS2051B | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps2051b.pdf | брать TPS2051BDBVR; TPS2051BDBVT — Obsolete |
| DAC80504 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/dac80504.pdf | — |
| OPA4197 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/opa4197.pdf | — |
| CSD18532Q5B | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/csd18532q5b.pdf | — |
| IRLML0100 | active | Digi-Key Active IRLML0100TRPBF (не производитель) | — |
| LM74700-Q1 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/lm74700-q1.pdf | — |
| TPS25730D | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps25730.pdf | — |
| BQ25798 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/bq25798.pdf | — |
| INA226 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/ina226.pdf | — |
| TCA9546APW | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tca9546a.pdf | в BOM PW записано TCA9546APW: заказной код TCA9546APWR |
| LM5176 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/lm5176.pdf | — |
| TPS54560B | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps54560b.pdf | — |
| LMR33640 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/lmr33640.pdf | — |
| TPS7A3301 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps7a33.pdf | — |
| LM5156H | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/lm5156h.pdf | — |
| TPS7A4101 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps7a4101.pdf | — |
| TPS26631RGER | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/tps2663.pdf | — |
| BQ7791500 | active | TI, PACKAGE OPTION ADDENDUM: https://www.ti.com/lit/ds/symlink/bq77915.pdf | — |
| XL-1615RGBC-RF, TS-1187A-B-A-B, S2B-PH-K-S(LF)(SN), NCD0603G1, Molex 43650-0600, S3B-PH-K-S(LF)(SN), S4B-PH-K-S(LF)(SN), S8B-PH-K-S(LF)(SN), USBLC6-2SC6, 74HC4051, ABM8-272-T3, BAT54S, B4B-PH-K-S(LF)(SN), B6B-PH-K-S(LF)(SN), AP2112K-1.8, SX3M24.576B10F20TNN, SX3M22.5792B10F20TNN, X322524MOB4SI, 1N4148W, AO3400A, SMBJ18CA, Molex 43045-1012, B3B-PH-K-S(LF)(SN), RCJ-025, B2B-PH-K-S(LF)(SN), MMBTA92, MMBTA42, 2N7002, B5B-PH-K-S(LF)(SN), PJ-3920-3A, MMBT3904, 74HC595, SMBJ28CA, SMBJ13CA, B560C, SS1H10, BZT52C3V3, Molex 43650-0215, Molex 43045-0612, Molex 43045-0412, B8B-PH-K-S(LF)(SN), USB4105-GF-A, Molex 43045-0600 | не найден | только LCSC productCycle=normal (не статус производителя) | — |
| HCTL PZ127-2-07-Z | не найден | только LCSC productCycle=normal (не статус производителя) | разъём 2×7 1,27 мм стандартный, замена по посадке |
| HCTL PZ127-2-08-Z | не найден | только LCSC productCycle=normal (не статус производителя) | разъём 2×8 1,27 мм стандартный |
| W25Q128JVSIQ | не найден | статус производителя не найден; EmbeddedRelated Active | — |
| CL1115 | не найден | LCSC без статуса; Digi-Key 4654-CL1115-ND был в наличии 19.11 | — |
| NJ3FD-V | не найден | страница neutrik.com/en/product/nj3fd-v есть (19.11), статуса не указано | — |
| PJ398SM | не найден | производитель WQP статуса не публикует | взаимозаменяем с WQP518MA/PJ301M-12 (Thonk) |
| TLP2361 | не найден | явного статуса нет; страница Toshiba https://toshiba.semicon-storage.com/us/product/opto/photocoupler/detail.TLP2361.html | — |
| SMBJ20CA | не найден | только LCSC productCycle=normal (не статус производителя) | любой SMBJ20CA |

## Даташиты и подтверждения, которые нужны от пользователя

1. Alps EC11E1834403: актуальный статус (страница tech.alpsalpine.com не открылась) — PDF спецификации или ответ Alps.
2. ams OSRAM AS5600-ASOT: статус/PCN и таблица заказных кодов.
3. Neutrik NCJ6FI-V: подтверждение выпуска (PCN или ответ Neutrik).
4. Winbond W25Q32JVSSIQ: PCN/EOL (расхождение Octopart и Digi-Key).
5. XINGLIGHT XL-1615RGBC-RF, XKB TS-1187A, HCTL PZ127-2-07-Z и -08-Z: статус производителей не публикуется (даташит XL-1615 уже есть).
6. Toshiba TLP2361, Winbond W25Q128JVSIQ, Cliff CL1115: страница/паспорт с пометкой статуса.
