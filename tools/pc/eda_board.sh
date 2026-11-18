#!/bin/bash
# usage: eda_board.sh ID NAME DIR
cd /c/Users/karpa/Documents/Shtuka-druka
P="/c/Program Files/KiCad/10.0/bin/python.exe"; id=$1; name=$2; d=$3
for t in 1 2 3; do o=$(timeout 400 "$P" tools/eda/eda_check.py $id --project $name 2>&1 | grep -E "^\*\*PCB|^\*\*Schematic|no EasyEDA"); echo "$o"; [ $(echo "$o" | grep -c "matched") -eq 2 ] && break; sleep 15; done
for t in 1 2 3 4; do r=$(timeout 900 "$P" tools/eda/eda_set_lcsc.py $id --project $name 2>&1 | grep -E "^sch|^pcb|no EasyEDA"); echo "$r"; [ $(echo "$r" | grep -c "missing 0, error None") -eq 2 ] && [ $(echo "$r" | grep -c "written 0,") -eq 2 ] && break; sleep 10; done
timeout 200 "$P" ""$(dirname "$0")"/cmp.py" $name hardware/$d/$d.kicad_pcb 2>&1 | tail -1
