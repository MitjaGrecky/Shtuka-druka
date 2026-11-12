# Скрипты `tools/`

Python 3, только стандартная библиотека. На ПК обычного Python нет: запускать `C:\Program Files\KiCad\10.0\bin\python.exe`.

| Скрипт | Что делает |
|---|---|
| `pc_start.py` | Начало сессии на ПК: pull, последние коммиты, открытые задачи ПК из `notes/handoff.md`, итог ночной проверки, состояние инструментов |
| `pc_check.py BOARD... [--sch-from DIR] [--details]` | DRC KiCad 10 + сверка со схемой + медь и via одной таблицей; плата не меняется |
| `quilter_intake.py JOB --match TEXT [--sch-from DIR]` | Архивы Quilter из «Загрузок» → `hardware/<board>/quilter/results/<JOB>_cand*`, дубли по md5 отсеиваются, затем `pc_check` |
| `night_check.py [--all] [--since-hours N]` | Ночная проверка: pull (только fast-forward и без локальных правок), `pc_check` по платам, изменённым с прошлого раза; отчёт `logs/night/<дата>.md`, ничего не коммитит |
| `eda/eda_check.py ID [--project ИМЯ]` | Сверка проекта EasyEDA Pro (схема и плата) с `hardware/for-routing/<ID>/netlist.net`; см. `eda/README.md` |
| `board_stats.py BOARD [--nets]` | Длина меди, via, обходы по семействам цепей |
| `pack_for_routing.py`, `build_for_routing.py` | Пакеты `hardware/for-routing/` (архивы KiCad 7 для EasyEDA, без PWR_FLAG) |
| `sdp.py`, `split_decisions.py` | Служебные для документов и журнала решений |

Отчёты скриптов складываются в `logs/` (в git не идёт).

## Ночная проверка на ПК
Задача Планировщика Windows «ShtukaDruka night check» (создана 12.11.2026 по слову пользователя): каждый день в 03:30,
при пропуске (ПК спал) запускается при первой возможности; `pythonw.exe -I tools\night_check.py`, без окна, лимит 1 ч.
Проверить: `Get-ScheduledTaskInfo -TaskName 'ShtukaDruka night check'`. Удалить: `Unregister-ScheduledTask -TaskName 'ShtukaDruka night check'`.
