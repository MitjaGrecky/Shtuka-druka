# Командная памятка (для всех агентов проекта «Штука Дрюка»)

Прочитать целиком перед первой правкой. Пользователь пишет по-русски; **отвечай и документируй по-русски**, надписи на устройстве по-английски (R45).

## Что за проект и где что лежит
Репозиторий `C:\Users\karpa\Documents\Shtuka-druka` (ветка `m1-two-cells`). Платы: `hardware/<имя>/` с генераторами `gen/design.py`, `make_sch.py`, `make_pcb.py`; общая часть `hardware/common/gen/` (`kit.py`, `packer.py`, `autoplace.py`). Пакеты для EasyEDA и трассировки: `hardware/for-routing/<ID>/`. Решения: `docs/ru/decisions/` (журнал R/P). Очередь и история: `notes/handoff.md`. Модель посадки: `model3d/fit/fit_model.py`, артефакт: `model3d/v8/` (генератор `build_v8.py`). Главная линия корпуса — **R174 «Зелёная-2 сжатая»**: дека 30, глубина 500, макушка 117, два аккумуляторных отсека под P2 (106 × 220 × 11 мм), A1 на полу, гнёзда 6,35 мм под передним краем P1 без свеса, H5 в заднем правом углу (x 376–496), вентилятор на правой стенке, угловые штекеры экрана. Память проекта: `C:\Users\karpa\.claude\projects\C--Users-karpa-Documents-ShtukaDruka\memory\MEMORY.md` (читается автоматически).

## Жёсткие правила
1. **Никакого `kicad-cli`**: он вешает этот ПК (синий экран). Проверки DRC и паритета делает CI. Все скрипты запускать KiCad-овским Python: `C:\Program Files\KiCad\10.0\bin\python.exe` (системный Python без `pcbnew`). В каждом вызове bash заново ставить `KICAD_SYMBOL_DIR=C:/Users/karpa/Documents/Shtuka-druka/hardware/common/sym7` и `KICAD_FOOTPRINT_DIR="C:/Program Files/KiCad/10.0/share/kicad/footprints"` (состояние оболочки не сохраняется).
2. **Только детали в наличии**. Номер LCSC брать из библиотеки EasyEDA (`tools/eda/eda_parts.py`), наличие проверять на странице `https://jlcpcb.com/partdetail/Cxxxx` во встроенном браузере (подождать ≈ 4 с, прочитать «In Stock»). Детали, которых нет на JLCPCB, можно купить на Digikey/Mouser и паять вручную (пользователь согласен), тогда пометить в BOM.
3. **Даташиты читать по тексту** (`markitdown`: `C:\Users\karpa\.venvs\markitdown\Scripts\markitdown.exe FILE -o OUT.md`; PDF-картинки через `pymupdf`). Не спорить с EasyEDA: «проверь easyeda и сравни».
4. **Делаем как рекомендует производитель** (типовые схемы из даташита и application note), «сжечь на старте не хочу ничего».
5. **Журнал решений R — только слова пользователя** (правило аудитора, `audit/AUDITOR_CHARTER.md`). Свой выбор оформляй предложением P с пометкой «выбрал инженер, не подтверждено», расчёты и выводы клади в документы, не в R. Свои оценки помечай «оценка / не проверено».
6. **GitHub держим тихим**: эксперименты локально, пуш пакетами, CI зелёный. Коммитить так: `git -c user.name=MitjaGrecky -c user.email=MitjaGrecky@users.noreply.github.com commit` (личную почту пользователя не вписывать), в конце сообщения `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. CI смотреть публичным API: `curl -s "https://api.github.com/repos/MitjaGrecky/Shtuka-druka/actions/runs?head_sha=<sha>"`.
7. Пароли и коды не вводить, CAPTCHA не обходить, платных стандартов не покупать, внешние сайты не залогинивать.
8. Работать самостоятельно, не спрашивать «продолжать?»; в конце короткий отчёт: что сделано, что проверено, что нет, что нужно от пользователя (один чёткий вопрос).

## Как делается плата (шаблон)
1. `gen/design.py`: детали и цепи (`parts()`), размеры (`W, H`), `placement()`; `make_sch.py` и `make_pcb.py` пишут `.kicad_sch` / `.kicad_pcb` (разводки нет, она потом).
2. Проверки: `tools/sch_netcheck.py hardware/<имя>` (схема против генератора, 0 расхождений), `tools/pc/ov.py` (перекрытия), `tools/pc/opn.py` (куда открыты лежачие разъёмы), `tools/pc/under.py` (детали по сторонам).
3. Пакет: `tools/pack_easyeda.py ID hardware/<имя> --no-cli` (пересобирает BOM, zip, netlist, превью без kicad-cli).
4. EasyEDA: `bash tools/pc/eda_one.sh ID <имя_каталога> vN` (импорт, сверка деталей и цепей, номера LCSC, позиции, сохранение). Большие платы открываются только после двойного щелчка по проекту в списке «All Projects» (computer-use, доступ к «EasyEDA Pro» уже даёт пользователь). Подробности: `tools/pc/README.md`, `tools/eda/README.md`.
5. README платы: ревизия, что изменено и почему, чего не проверено. Запись в `notes/handoff.md`.

## Навыки (установлены глобально, `~\.claude\skills`)
ee-power, ee-thermal, ee-emc-esd, ee-dfm, ee-audio, ee-design-review, ee-pcb-verify, pcb-layout-review, release-pcba-fabrication, design-and-review-circuit, jlcpcb, lcsc, datasheets, spice, spice-sim, librarian, registry-search, find-skills. Перед использованием просмотри `SKILL.md`. Если нужен новый навык — `npx skills find <запрос>` и `npx skills add <url> --skill <имя> -g -a claude-code -y`, затем запиши в память (`external-skills.md`).
