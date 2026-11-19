# План закупки: чем закрыть всё, чего нет на JLC (технолог, 19.11.2026)

Количество — на 2 комплекта плат. Остатки и цены с карточек Digikey, Mouser, LCSC, Thonk (19.11.2026) и из поисковой выдачи; где остаток из выдачи, помечено «≈». «JLC» — собственные детали JLC в наличии (API). Ничего не заказывалось. QFN/SOIC — consigned на JLC (условия: док. 46 разд. 2), выводные — вручную.

| # | Плата, поз. | Нужно | Источник | SKU | Цена | Остаток | Ссылка | Примечание |
|---|---|---|---|---|---|---|---|---|
| 1 | A1 U6, U7 | 4 | Digikey | CS5308P-DNR (лента CT) | 22,76 $ | 3065 | [Digikey](https://www.digikey.com/en/products/detail/cirrus-logic-inc/CS5308P-DNR/26753133) | consigned; -DN (трей) без запаса, срок 16 нед. |
| 2 | A1 U8 | 2 | JLC C49192888 + Digikey | CS5304P-DN | 14,53 $ (JLC 27,2 $) | JLC 3; Digikey 409 | [Digikey](https://www.digikey.com/en/products/detail/cirrus-logic-inc/CS5304P-DN/26753132) | 2 шт. с JLC хватит; Digikey запас |
| 3 | A1 U29 | 2 | Digikey | CS4308P-DN | 16,59 $ | 298 | [Digikey](https://www.digikey.com/en/products/detail/cirrus-logic-inc/CS4308P-DN/26828149) | consigned; номер в BOM не нужен |
| 4 | A1 U44 | 2 | Digikey / Mouser | ADUM4166BRIZ | 19,74 $ | Digikey ≈569; Mouser ≈767 в пути | [Digikey](https://www.digikey.com/en/products/detail/analog-devices-inc/ADUM4166BRIZ/16285972) | consigned (SOIC-20W); ADuM4160 не годится (12 Мбит/с) |
| 5 | A1 C60… ×40 | 80 | Digikey / Mouser | 865250349007 (Digikey 732-8307-6-ND; Mouser 710-865250349007) | ≈0,61–0,67 $ | ≈586 (Digikey), 239 по README | [EasyBOM](https://www.easybom.com/p/865250349007-wurth-elektronik-2960845) | вручную; на JLC 0 |
| 6 | R2 U4 | 2 | Mouser EU / Digikey | USB2514B-I/M2 | 2,73 € (Mouser), 3,17 $ (Digikey) | ≈6280 / ≈11 645 | [Mouser](https://eu.mouser.com/ProductDetail/Microchip-Technology/USB2514B-I-M2?qs=uus7iwvxYD%2BYUekNs2mWlw%3D%3D) | consigned (QFN-36); на JLC 0 |
| 7 | PW J2, J3, J4, J8 | 8 | Newark / Sager / Arrow | Molex 43045-0612 (0430450612) | ≈0,47–0,72 $ | ≈15 900–20 900 | [Newark 97C5002](https://www.newark.com/molex/43045-0612/connector-header-6pos-2row-3mm/dp/97C5002), [Sager](https://www.sager.com/product/0430450612-molex/80491) | вручную; LCSC C234188 = 0 |
| 8 | R2 J14–J16 | 6 | **JLC C707258** | PJ-3920-3A (тот же MPN, другой LCSC) | 0,47 $ | JLC 416 | [LCSC](https://www.lcsc.com/product-detail/C707258.html) | **замена номера**: C707259 → C707258, схема и посадка те же |
| 9 | R2 J17–J32 | 34 | Thonk | WQP518MA (= PJ398SM, взаимозаменяемы по Thonk) | £0,31 (от 50), £0,38 (до) без НДС | в наличии | [Thonk](https://www.thonk.co.uk/shop/thonkiconn/) | вручную; Befaco 25 шт. 13,31 € как резерв |
| 10 | R1 J6, J7 | 4 | Mouser UK / Diginet | NCJ6FI-V | £2,41 (Mouser), 2,37 € (Diginet, 9 шт.) | Mouser есть, Diginet 9 | [Mouser](https://www.mouser.co.uk/ProductDetail/Neutrik/NCJ6FI-V?qs=2AuUxvzm3x%2FEtGDxOLS%2Bsw%3D%3D) | вручную; JLC 0 |
| 11 | R1 J8, J9, J12–J23 | 28 | Mouser UK | NJ3FD-V | £1,06 (1), £0,79 (1000) | ≈9077 | [Mouser](https://www.mouser.co.uk/ProductDetail/Neutrik/NJ3FD-V?qs=JfNPhaIww3IZW5co/IYJ8A%3D%3D) | вручную; Ø12 круглый вырез, подходит в сетку 18/22 (док. 48 разд. 6) |
| 12 | F1 J4, J5 | 4 | Digikey | CL1115 (4654-CL1115-ND) | 2,41 $ (1), 2,05 $ (10) | 131 | [Digikey](https://www.digikey.com/en/products/detail/cliff-electronic-components-ltd/CL1115/20532447) | вручную; карту выводов проверить на живом разъёме до заказа F1 |
| 13 | R1 R101, R114 | 4 | **JLC C25918** | 0402WGF7501TCE, 7,5 кОм 1 % | ≈0,001 $ | JLC 873 457 | LCSC C25918 | **замена: 7,5 кОм вместо 7,42 кОм** (E192 нет в наличии; отклонение +1,1 %) |
| 14 | A1 C289 | 2 | **JLC C190223** | KL1E470M-CRE77, 47 мкФ 25 В, Ø6,3×7,7 | 0,069 $ | JLC 980 | LCSC C190223 | **замена: 25 В вместо 10 В**, тот же корпус, та же ёмкость |
| 15 | PW L4, L5 | 4 | Digikey (оригинал) или JLC | Bourns SRP1038CC-8R2M (Digikey 118-SRP1038CC-8R2MTR-ND) / **замена FXL1040-8R2-M JLC C167232** | ≈0,81 $ / JLC | Digikey ≈295 (выдача); JLC 10 957 | [Digikey](https://www.digikey.com/en/products/detail/bourns-inc/SRP1038C-8R2M/10249095) | FXL1040: 8,2 мкГн, 8 А насыщ./9 А, 27 мОм, **11,5×10 мм** вместо 10×10: нужна новая посадка, 1,5 мм больше |
| 16 | PW L3 | 2 | JLC C3221079 | SRP1245A-4R7M | 2,64 $ | JLC 4 | [LCSC](https://www.lcsc.com/product-detail/C3221079.html) | хватает на 2 комплекта; Digikey/Mouser без остатка до янв. 2027 |
| 17 | PW Q1–Q4, Q7, Q10–Q13 | 18 | **JLC C882766** | CSD18532Q5B | 2,36 $ | JLC 2799 | LCSC C882766 | **замена: CSD18532Q5B вместо CSD18540Q5B** (2,5 против 1,8 мОм, Qg 44 против 41 нКл), корпус тот же |
| 18 | PW D4, D6 | 4 | **JLC C224008** | Littelfuse SMBJ13CA | 0,16 $ | JLC 7663 | LCSC C224008 | **замена номера** C132568 → C224008, MPN тот же |
| 19 | P4 U8 | 2 | **JLC C499458** | AS5600-ASOT | 1,23 $ | JLC 10 (LCSC 0) | LCSC C499458 | **замена: ASOT вместо ASOM** (SOIC-8, тот же кристалл); запас Digikey AS5600-ASOM ≈3,39 $ без бэкордера |
| 20 | W1 RV1–RV4 | 8 | **JLC C209779** | RK09K1130A5R | 0,85 $ | JLC 3273 | LCSC C209779 | **замена: A5R вместо A6S**; вал сверить с ручкой |
| 21 | LP5864 (10 плат) | 50 + запас | JLC C5220564 + Digikey | LP5864RSMR | 1,62 $ (JLC), ≈2,58 $ (Digikey) | JLC 50; Digikey ≈5681 (таблица замен) | [Digikey](https://www.digikey.com/en/products/search?keywords=LP5864RSMR) | без запаса на JLC: взять ≈10 шт. consigned |
| 22 | P2 D1, PW D5, D7, D11, R2 D1 (зелёные 0603) | 10 | JLC C84267 | NCD0603G1 | ≈0,02 $ | JLC 806 624 | LCSC C84267 | точный «green» с остатком 0: замена на NCD0603G1 (520 нм) |

## Что меняется в схемах (для схемотехника)
- **R1:** R101, R114 7,42 кОм → 7,5 кОм (+1,1 %), проверить петлю; посадки NJ3FD-V и NCJ6FI-V не меняются.
- **A1:** C289 47 мкФ 10 В → 25 В (C190223); остальное без изменений (кодеки, ADuM4166, WCAP — те же MPN).
- **PW:** FET C86513 → C882766 (CSD18532Q5B, R_DS 2,5 мОм вместо 1,8): проверить тепло LM5176 и ORing; TVS D4, D6 → C224008; если L4, L5 брать FXL1040-8R2-M, поменять посадку (11,5×10), плата ещё не разведена.
- **P4:** U8 AS5600-ASOM → ASOT (только BOM). **W1:** RK09K A6S → A5R (BOM, вал).
- **R2:** J14–J16 номер C707259 → C707258 (BOM); зелёные светодиоды NCD0603G1 (BOM).
- Остальное (Cirrus, ADuM, USB2514B, Micro-Fit, Thonkiconn, Cliff) — те же MPN, только другой поставщик.

## Не подтверждено живыми карточками
CS5308P-DNR, CS5304P-DN, CS4308P-DN, CL1115, Thonk — карточки открыты; ADuM4166, USB2514B, WCAP, Micro-Fit, SRP1038CC, LP5864 на Digikey/Mouser — из выдачи, остатки «≈».
