# Каталог навыков (ред. 20.11.2026)

Владелец каталога: **главный инженер** (может поручить редактору базы знаний). Установлено на ПК: `C:\Users\karpa\.claude\skills\` (глобально) и `.claude/skills/` проекта. **Наличие в облачном чате не проверено**: установка на ПК не доказывает его.

- Выбирать минимальный набор по задаче из этого каталога; читать `SKILL.md` перед применением, числа (DRC, ток, тепло, производство) сверять с первоисточником; `kicad-cli` из навыков не запускать (запрет ПК).
- Статусы: кандидат / проверен в области / ограниченно / отложен / исключён. Статус относится к версии, среде и области проверки; «ещё не проверен» = контрольный пример не оформлен. Все навыки ниже сейчас «ещё не проверен» (кроме отмеченных).
- Обновления: назначенный исполнитель, примерно раз в неделю между задачами (`npx skills update -g -y`; `npx skills ls -g`), перед обновлением записать версии, после повторить контрольные примеры. **Обязательного обновления на каждом старте и после сжатия контекста больше нет** (заменяет прежнее правило 17.11).
- Следующая проверка обновлений: 2026-11-25 (напоминание в каталоге, расписание не создаётся автоматически).
- **Установка новых навыков (`npx skills add`) только с разрешения пользователя**: 20.11.2026 запрос без разрешения отклонён системой (скачивание по `CLAUDE.md`). Кандидаты для технолога, не установлены, ждут разрешения: `digikey`, `mouser`, `bom` (aklofas/kicad-happy). Плагины PartsPlan и BoardRepo предложены пользователю, решения нет.
- **Инструмент (не навык): markitdown 0.1.9**, установлен 20.11.2026: `uv tool install "markitdown[all]" --python 3.12`, путь `C:\Users\karpa\.local\bin\markitdown`. Правило: PDF и DOCX (даташиты, документы) читать через него (`markitdown FILE -o OUT.md`), в чат только суть.
- Не установлены намеренно: `kicad` (kicad-happy; построен на kicad-cli), digikey/mouser/element14/bom/pcbway (по необходимости закупки), ee-analog/general-pcb/high-speed/hv-safety/low-power/rf (по теме).

| Навык | Для кого | Источник | КБ | Файл от | Статус | Назначение (из описания) |
|---|---|---|---|---|---|---|
| datasheets | инженер, аудитор | aklofas/kicad-happy | 11 | 2026-11-17 | ещё не проверен | Extract structured specifications from electronic component datasheet PDFs — pinouts, electrical characteristi |
| design-and-review-circuit | инженер | keitark/pcba-design-skills | 3 | 2026-11-17 | ещё не проверен | Design, audit, or correct an electronic circuit from a product brief, native schematic, netlist, block diagram |
| design-everyday-things | дизайнер | wondelai/skills | 16 | 2026-11-17 | ещё не проверен | 'Apply foundational design principles: affordances, signifiers, constraints, feedback, and conceptual models.  |
| ee-audio | инженер | fxp/ee-skills | 5 | 2026-11-17 | ещё не проверен | Sourced best-practice rules for audio circuits: codec/ADC/DAC signal chains, AC-coupling capacitor dielectric  |
| ee-design-review | инженер, аудитор | fxp/ee-skills | 7 | 2026-11-17 | ещё не проверен | Review a schematic, PCB layout, netlist or design spec against a sourced catalog of 500+ circuit-design best-p |
| ee-dfm | инженер, технолог | fxp/ee-skills | 10 | 2026-11-17 | ещё не проверен | Sourced best-practice rules for DFM/DFA/DFT: fab limits (trace/space, drill, annular ring, mask, silkscreen),  |
| ee-emc-esd | инженер | fxp/ee-skills | 7 | 2026-11-17 | ещё не проверен | Sourced best-practice rules for EMC/ESD/surge: loop-area and return-path control, edge-rate and clock handling |
| ee-pcb-verify | инженер, аудитор | fxp/ee-skills | 7 | 2026-11-17 | ещё не проверен | Verify a KiCad design headlessly and automatically - ERC, DRC with custom .kicad_dru rules, schematic-vs-PCB n |
| ee-power | инженер | fxp/ee-skills | 9 | 2026-11-17 | ещё не проверен | Sourced best-practice rules for power circuits: buck/boost/flyback layout (hot loop, switch node, feedback rou |
| ee-thermal | инженер | fxp/ee-skills | 6 | 2026-11-17 | ещё не проверен | Sourced best-practice rules for PCB thermal design: theta-JA/JC/psi-JT and junction-temperature budgets, coppe |
| emc | инженер | aklofas/kicad-happy | 13 | 2026-11-17 | ещё не проверен | >- |
| find-skills | ответственный за навыки | vercel-labs/skills | 5 | 2026-11-17 | ещё не проверен | Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for  |
| frontend-design | дизайнер (артефакты) | anthropics/skills | 9 | 2026-11-17 | ещё не проверен | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps w |
| hmi-design-full | дизайнер (с оговоркой, см. ниже) | timhok/hmi-design | 12 | 2026-11-17 | ещё не проверен | Comprehensive ISA-101 design rules for Human Machine Interfaces in process automation, with detailed reference |
| impeccable | дизайнер | pbakaus | 13 | 2026-11-17 | ещё не проверен | Use when the user wants to design, redesign, shape, critique, audit, polish, simplify, harden, animate, or oth |
| jlcpcb | технолог | aklofas/kicad-happy | 11 | 2026-11-17 | ещё не проверен | JLCPCB PCB fabrication and assembly — BOM/CPL generation, basic vs extended parts, assembly constraints, desig |
| lcsc | технолог | aklofas/kicad-happy | 12 | 2026-11-17 | ещё не проверен | Search LCSC Electronics for electronic components — find parts by LCSC number (Cxxxxx) or MPN, check stock/pri |
| librarian | инженер | diodeinc/pcb | 6 | 2026-11-17 | ещё не проверен | Create or repair reusable component and module packages in a PCB registry. |
| pcb-layout-review | инженер | keitark/pcba-design-skills | 7 | 2026-11-17 | ещё не проверен | Audit, finish, or port PCB placement and routing using circuit intent, mechanical constraints, sourcing eviden |
| product-designer | дизайнер | borghei/claude-skills | 14 | 2026-11-17 | ещё не проверен | > |
| registry-search | инженер | diodeinc/pcb | 1 | 2026-11-17 | ещё не проверен | Find reusable registry modules and component packages for a board or specification. |
| release-pcba-fabrication | технолог | keitark/pcba-design-skills | 3 | 2026-11-17 | ещё не проверен | Build and verify a vendor-neutral PCB/PCBA manufacturing release from one frozen design revision. Use when gen |
| spice-sim | инженер | diodeinc/pcb | 3 | 2026-11-17 | ещё не проверен | Add or run an ngspice-backed Zener testbench with `pcb sim`. |
| spice | инженер | aklofas/kicad-happy | 25 | 2026-11-17 | ещё не проверен | >- |
| ui-ux-pro-max | дизайнер | nextlevelbuilder | 18 | 2026-11-17 | ещё не проверен | UI/UX design intelligence for web, mobile, and desktop. This skill should be used when designing, building, re |
| vibe-industrial-design | дизайнер | luckiday/vibe-hardware | 17 | 2026-11-17 | ещё не проверен | >- |

## Наблюдения по локальным файлам (18.11.2026, не полный аудит)
- `ee-dfm`: поиск по индексу правил, чтение нужного блока, сверка чисел по оригиналу: способ сохраняется.
- `hmi-design-full`: процессная автоматизация и ISA-101; для музыкального инструмента сценарии другие, применимость каждого требования обосновывать.
- `product-designer`: разбор сценариев и испытаний удобства; расчёт крепежа и жёсткости корпуса другой методикой.
- `ee-pcb-verify`, `pcb-layout-review`, `release-pcba-fabrication` пересекаются: ведущий выбирается по пробам, не по именам.
- Происхождение и ранний разбор: `docs/ru/40_external_skills_review.md`.

## Новый навык: поиск и приёмка
Искать, когда есть конкретный пробел (операция, вход, результат) и каталог его не закрывает. Порядок: проектные навыки, официальные инструкции поставщика, каталоги (`npx skills find <запрос>`), 2–3 кандидата; звёзды и объём не доказательство. Проверить: предмет, основания, среду (ОС, CAD, MCP), что запускается и какие сетевые обращения, полномочия (нет требований менять правила проекта), контрольный пример, поддержку (автор, версия/коммит, лицензия). Приёмка: контрольная задача с известным ответом на копии входов, сравнение с первоисточником, запись найденного, пропущенного, расхода. Установка только с разрешения пользователя (см. начало каталога).

Карточка навыка: шаблон в [../templates.md](../templates.md). Карточки заводить при первом рабочем применении (контрольный пример, версия/коммит, способ восстановления).
