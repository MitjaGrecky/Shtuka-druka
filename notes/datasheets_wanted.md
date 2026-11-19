# Нужные даташиты (19.11.2026)

Список для пользователя: скачать PDF и прислать в чат; читаем через markitdown. ADuM4165/4166 получен.

| № | Часть | Производитель | Что проверить | Где нужна |
|---|---|---|---|---|
| 1 | XU316 (XU316-1024-FB265 или фактический номер) | XMOS | питание, пины, boot, JTAG/xTAG, USB | A1 (xcore A/B) |
| 2 | CY8CMBR3108 | Infineon/Cypress | питание, I2C, ёмкостные входы | M-платы |
| 3 | AS5600 (вывод PGO, режимы) | ams OSRAM | PGO (вывод 5), режимы I2C/PWM | P4, колесо |
| 4 | OT2EL4C4JI (24.576 МГц) | YXC | состояние выхода при OE=0, джиттер | A1 (заменён на SCTF, для сравнения) |
| 5 | SX3M24.576B10F20TNN | SCTF | джиттер, tri-state, питание | A1 |
| 6 | PCM-L04S15-E95 | Ayaa | порог перезаряда, ток 7 или 12 А, NTC | запасная BMS |
| 7 | LP8042102 (5 А·ч, 103×42×8) | LiPol | макс. напряжение, ток заряда, выводы | запасной вариант ячейки |

## Добавлено 19.11.2026 (технолог, док. 48, гнёзда задней стенки)
Скачать PDF и прислать в чат (с neutrik.com): размеры выреза, глубина за стенкой, ток и выводы, посадка на плату.

| № | Часть | Что проверить | Где нужна |
|---|---|---|---|
| 8 | Neutrik NE8FDP (RJ45 D) | вырез, глубина, шаг винтов | LAN H5 |
| 9 | Neutrik NAUSB-W (USB A-B) | вырез, глубина, шаг винтов | USB-A стенки |
| 10 | Neutrik NCJ6FI-S / -V / -H (комбо D) | вырез, глубина, посадка | R1 Mic/Line |
| 11 | Neutrik NJ3FD-V (6,35 мм, на плату) | вырез, глубина, посадка | R1, 14 шт. |
| 12 | Neutrik NF2D (RCA D) | вырез, глубина | R1 RCA |
| 13 | Cliff CL1115 (6,35 мм) | чертёж, карта выводов | F1 |
| 14 | Molex 43045-0612 | чертёж платы (Ø отверстия) | PW |
| 15 | Würth 865250349007 | чертёж площадки (текст PDF перемешан) | A1 |

Добавлено 19.11.2026 (док. 48, повторный обход Thomann): TAD 114BPC, Adam Hall 7217 PCB02 TP, Neutrik NRJ6HF и NMJ3HF-S (посадка на плату, отверстие, выводы); Neutrik NCJ6FA-V (посадка, вырез A против D); Hicon HI-J35SEFD (D-фланец, размеры); Seetronic SCCMCDF-01 (26,5×23 мм: ориентация), SAUSB-W; Neutrik NJ3FD-V (размер фланца при шаге 22).

Добавлено 19.11.2026 (док. 49, D-формат задней стенки): Rane Note 151 «Grounding and Shielding Audio Devices» и Note 110 «Sound System Interconnection» (ranecommercial.com/legacy/pdf/ranenotes/, прочитаны только в выдержках поиска); AES48-2005 (платный стандарт, не скачан); Neutrik: размеры D-вырезов и экранирование NC3FD/NJ3FD, Hicon HI-J35SEFD (габарит D, наличие не проверено); JST PH/XH (номинальный ток и напряжение из даташита, цифры в док. 49 по памяти).

## Закрыто 19.11.2026 (Neutrik, см. notes/datasheets_text/neutrik_*.md и док. 48 разд. 6)
Получены и разобраны: NE8FDP, NE8FDV, NAUSB-W, NCJ6FI-S/-V/-H, NCJ6FA-V, NJ3FD-V, NJ3FP6C, NF2D-0, NMJ3HF-S. Вычеркнуто из списка выше: Neutrik NE8FDP, NAUSB-W, NCJ6FI-S/-V/-H, NCJ6FA-V, NJ3FD-V, NF2D, NJ3FP6C.
Ещё нужны (не Neutrik или нет чертежа): NRJ6HF и NMJ2HC-S (только DXF), NC3FD (чертёж не прочитан), TAD 114BPC, Adam Hall 7217 PCB02, Hicon HI-J35SEFD, Seetronic SCCMCDF-01, Thomann MIDI Socket, Cliff CL1115, Molex 43045-0612, Würth 865250349007.
