# Передача хода: облако ⇄ ПК

Формат записи: `- [ ] #N кому: задача. Контекст/файлы.` Закрытие: `- [x] #N результат (коммит/файл)`.
Закрытые записи и старые отчёты переносить в `notes/handoff_archive/` (индекс там же; здесь только активное). Решения здесь не принимаются, только предлагаются. Очередь ведёт главный инженер по `ShtukaDruka\claude\chief\PRIORITIES.md`; рабочее место только `C:\Users\karpa\Documents\Shtuka-druka`, ветка `claude-team` (пользователь 25.11.2026; копия `claude\repo` закрыта); push и gh делает только главный инженер (CLAUDE.md). Сводка состояния: [`STATUS.md`](STATUS.md).

## Очередь (21.11.2026, по PRIORITIES и журналу решений R191–R197, P112–P119)
| # | Задача | Владелец | Состояние |
|---|---|---|---|
| 1 | **А-037 развязка у выводов** (P116, P118): правило выводов в `packer`/`autoplace`; F1, BM, PW, R2, R1, A1, P2 перегенерированы (`38d30ec`, `6f063e5`, `86829a7`). PW: ВЧ 86 %, объёмные банки не прошли, силовые каскады U6/U8/U12/U13 без места на нижней стороне; R2 после правила 28 не-GND (22 у RP2350) против 11 до | схемотехник; решение по сторонам PW и объёмным банкам — главный инженер | в работе, А-037 по PW открыта |
| 2 | **Слои** (R197: 2–4 слоя, 6 — только отдельным вопросом пользователю; P119: R1 4 слоя, ±12V заливками на In2); PW — по расчёту спроса | схемотехник | P114 (6 слоёв) заменено R197 |
| 3 | **Трассировка заново**, по одной плате после п. 1–2; данные Freerouting 1.9 на новой расстановке — не окончательные (PW 61/13, R2 78/28, F1 3/0, BM 1/1) | схемотехник, запуски субагентом | после п. 1–2 |
| 4 | **Вентиляция:** вход R195, выход — сквозная часть боковины R196, P115 (22,7 см², док. 50); осталось: паспортная кривая вентилятора (в 50 «по памяти»), замер | главный инженер | расчёт есть, не подтверждён паспортом |
| 5 | **Тестовая плата пэдов 4 × 4** (R194): RP2350 + мультиплексоры + ADC128S102; полную P2 не менять | схемотехник после п. 1–3 | не начата |
| 6 | **Проверка XU316 32 × 40 до разводки A1** (А-040), образец пэда до P2 | ПО и испытания (роль не открыта) | не начата |
| 7 | **BOM плат** чистый, без закупки (R192): `hardware/for-routing/<ID>/BOM_clean.csv`; пробелы: M1 R15–R17 (dnp), A1 C290–C293 (деталь не выбрана), MPN пуст у 52 строк, генератор SiT8208 или SX3M, провод 20–24 AWG у 43030-0007 против токов PW | технолог; решения — главный инженер | BOM есть, вопросы открыты |
| 8 | **Журнал и сводки:** А-041 (R/P) выполнен: R191, P112; STATUS и README плат по `REV`; P1: README Rev 0.2 против `REV` 0.1 в генераторе — см. отчёт | редактор | см. «Отчёты» |
| 9 | **Нет в наличии → замена:** ISOUSB211 вместо ADuM4166 сделано (A1 0.9); CS5308P/CS4308P, Micro-Fit, JST PH — вне JLC по R191, закупки нет (R192) | технолог | без заказа |

## Вопросы пользователю (решает он; задаёт только главный инженер)
- **К-2** — экран XLR/гнёзд и корпус на R1; **К-3** — земля A1 (`docs/ru/40_external_skills_review.md`).
- **В19** (14.11) — генераторы: 24,576 МГц SiTime SiT8208 (джиттер 0,5 пс, на LCSC нет), 22,5792 МГц SCTF SX3M22.5792M20F30TNN (есть, джиттер не указан); пока JLC-деталь в схеме, SiTime — запасной вариант. Вопрос: брать SiTime у Digikey/Mouser, а JLC-деталь оставить запасной?
- **6 слоёв** (R197) — только если 2–4 слоя не сработают; не спрашивать заранее.
- Закрыто 20.11 и перенесено в архив: В17 (P112), В20–В22 (R191).
- P98, P97, P75, P82–P85, P90–P96: список по приоритету в `docs/ru/decisions/README.md`; открытые инженерные P закрывает главный инженер (R186).

## Прочее открытое
- A1 (rev 1.0): конденсаторы связи WCAP-ASNP (P108), THD+N на 20–100 Гц измерить на первой плате; EasyEDA проверен для 0.9, ревизии 20.11 не загружены.
- Внешние навыки: `docs/ru/40_external_skills_review.md`; установка новых — только с разрешения пользователя.
- Хвосты архива 18 (щели R184, W3 карман USB/SD, опоры P2, угловые штекеры HDMI/USB-C): предложение редактора `claude\editor\runs\archive18_review.md`, решение главного инженера.

## Отчёты
(новые записи сверху: дата, кто, что сделано, где результат)
- 21.11.2026, редактор: очередь переписана по PRIORITIES и журналу решений (R191–R197, P112–P119); В17, В20–В22 закрыты и перенесены в `handoff_archive/closed_items.md`; STATUS обновлён; документ `claude\editor\tasks\06_handoff_status_p1.md`.
- 20.11.2026, редактор (аудит №4 А-042/А-043): из очереди сняты как устаревшие #30–#49 и «Колесо R173» → `handoff_archive/closed_items.md`; строки статуса README плат по `REV` генераторов.

(Закрытые и старые записи 18–19.11.2026 перенесены в [`notes/handoff_archive/18.md`](handoff_archive/18.md) без изменений; сводка состояния: [`notes/STATUS.md`](STATUS.md).)
(Старые отчёты и закрытые записи перенесены в [`notes/handoff_archive/`](handoff_archive/README.md): индекс записей по заголовкам, текст без изменений.)

## Quilter jobs 26.11.2026 (rev 0205bcb, Riga time)
Mode for all three: route only (all parts pre-placed in the PCB, Quilter keeps them; freeing non-mechanical parts would need moving them off-board in the generator). JLCPCB 2-Layer 6/6 mil, via 0.45/0.2, Full Layout. CSV in hardware/<board>/quilter/.
| job id | board | mode / notes | start |
|---|---|---|---|
| 6b07bf702434cbecec7e1b8b | BB1 | route only; 16 power nets 8 A, ground BAT_N_A/B; stack 1 oz (README wants 2 oz: widen after import) | 07:14 |
| 6b07c0632434cbecec7e1b8d | U1 | route only; PD_VBUS and GND 5 A, power pour | 07:18 |
| 6b07c136d811c3754ddac8d1 | F1 | route only; auto power nets 500 mA; 4 auto 100-ohm diff pairs (balanced audio in) deleted | 07:21 |
Links: https://app.quilter.ai/jobs/<id>. Result check: later, import + DRC in CI.

## Quilter jobs 26.11.2026, second batch (rev b74e5cc, Riga time)
Route only (all parts pre-placed), via 0.45/0.2, clearance 0.152 (project 0.15), Full Layout. CSV in hardware/<board>/quilter/.
| job id | board | mode / notes | start |
|---|---|---|---|
| 6b07edcb9f9b114eee405f75 | PW | 4L JLCPCB with power plane 6/6 (In1 Ground, In2 Power, 1 oz: no 2 oz in README); power nets from CSV (BUS 10 A, packs 8 A, 19 V/5 V 5-8 A), 13 duplicate rows deleted; auto diff pair PM_INP/N (INA226 sense) deleted; warning: pin count mismatch U16/U17/U19 (EP via pads) | 09:36 |
| 6b07efc29f9b114eee405f7e | P1 | 2L JLCPCB 6/6; auto +3V3/+5V/GND 500 mA kept (CSV not loaded, same content) | 09:40 |
| 6b07f09a9f9b114eee405f81 | P4 | 2L JLCPCB 6/6; job moved into project "P1 left" (Quilter offer, saves 503 pins); same auto nets; warning: RV1 pin count (board 4, schematic 3) | 09:43 |

## Quilter jobs 26.11.2026, third batch (rev 7024900, Riga time)
Route only, JLC 2L 6/6, via 0.45/0.2, clearance 0.152. Power nets: auto rows deleted, `hardware/<board>/quilter/high_current_nets.csv` uploaded (ground: auto GND kept). No diff pairs detected on the 2L boards.
| Job id | Board | Project / notes | Start |
|---|---|---|---|
| 6b08139c9f9b114eee405fa7 | M3 | new project "M3-M5 modules" | 12:10 |
| 6b0814a39f9b114eee405fa8 | M4 | same project (pins of M3 reused) | 12:14 |
| 6b081563d811c3754ddac926 | M5 | same project | 12:17 |
| 6b0816472434cbecec7e1bfe | W2 | project "W1-W3 modules" | 12:24 |
| 6b0817612434cbecec7e1c05 | W3 | DRAFT, fully set up, not started (limit); own project "W3 system" (Quilter: not the same design as W2) | - |
| 6b0818169f9b114eee405fb4 | M1 | DRAFT, fully set up, not started (limit). 4L JLC 6/6, In1 Ground, In2 Signal (ring chords on In2), 216 PCB_ARC -> chords (8/quarter) in the upload copy only | - |
Free plan limit hit: 10 jobs per 24 h (next start ~06:05 27.11 Riga). Not created yet: R1, R2, A1, P2, P3 (CSV ready in hardware/<board>/quilter/). Plan for 4L: "JLCPCB 4-Layer (with power plane) 6/6" (In1 Ground, In2 Power); A1 keep USB pair 90 Ohm. W1 skipped: its board is already routed (908 tracks), Quilter would only analyze it.
quilter_inputs.py fails on the PC (no KiCad footprint plugin / symbol path in the PC Python); CSV made by a scratch script from the board nets.
