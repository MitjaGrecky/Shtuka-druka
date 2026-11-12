# Проверка проекта EasyEDA Pro против нетлиста KiCad

`eda_check.py ID [--project ИМЯ]` сверяет открытый в EasyEDA Pro проект с `hardware/for-routing/<ID>/netlist.net`:
цепи платы (по площадкам) и цепи схемы (собираются по геометрии: выводы, провода, флаги). Сравнение по наборам выводов,
имена цепей не важны. Ловит пропавшие детали, разорванные и склеенные цепи, флаги `PWR_FLAG`. В проекте ничего не меняет.

```
python tools/eda/eda_check.py M1 --project M1_v2 --md logs/m1_v2.md
```

## Что нужно один раз
1. Мост: `git clone https://github.com/easyeda/easyeda-api-skill ~/easyeda-api-skill`, затем `npm install` в этой папке.
   Другое место: переменная `EASYEDA_BRIDGE`. Если мост не запущен, скрипт запускает его сам (лог в `logs/eda_bridge.log`).
2. В EasyEDA: Advanced → Extensions Manager → Import → `run-api-gateway` 1.0.5 (jlcext.com), во вкладке Config
   включить «Allow interactive with external» и «Show at header menu».

## Как пользоваться
1. Открыть проект в EasyEDA.
2. Запустить скрипт. Если он пишет «no extension connection sees them yet», нажать в EasyEDA меню
   API Gateway → Reconnect и запустить ещё раз. Причина: экземпляр расширения не видит документы,
   открытые после его запуска; после смены проекта или открытия вкладок нужен Reconnect.
3. Результат: таблица в консоли и, с `--md`, файл. `--keep DIR` сохраняет сырые выгрузки (JSON).

## Известное
- `sch_Netlist.getNetlist()` зависает (запрос моста обрывается через 30 с), поэтому схема собирается по геометрии.
  Сборщик проверен на M1: дал те же 143/146 цепей и ту же склейку питания, что выгрузка `.tel` из GUI.
- В мосте `POST /eda-windows/select` роняет сервер (необъявленная `activeWindowId`); скрипт его не использует.
- macOS: мост слушает 127.0.0.1, а расширение идёт на `localhost` (IPv6); в `scripts/bridge-server.mjs` поставить `LISTEN_HOST = '::'`.
- `netcompare.py NETLIST.net DUMP.json` сравнивает отдельно сохранённую выгрузку.
