#!/bin/bash
cd /c/Users/karpa/Documents/Shtuka-druka
P="/c/Program Files/KiCad/10.0/bin/python.exe"; id=$1; d=$2; name=${id}_${3:-v3}
out=$(timeout 280 "$P" tools/eda/eda_import.py hardware/for-routing/$id/${id}_kicad7.zip $name 2>&1 | tail -1)
uuid=$(echo "$out" | grep -o "'uuid': '[0-9a-f]*'" | head -1 | cut -d"'" -f4)
echo "import $name uuid=$uuid"; [ -z "$uuid" ] && { echo "$out"; exit 1; }
for t in 1 2 3; do
  w=$("$P" -c "import sys;sys.path.insert(0,'tools/eda');import eda_check as E;b=E.find_bridge();print(sum(x['connected'] for x in E.http(b+'/eda-windows')['windows']))"); [ "$w" -gt 0 ] && break; sleep 10; done
timeout 280 "$P" ""$(dirname "$0")"/eda_open2.py" $name $uuid 2>&1 | tail -1
bash ""$(dirname "$0")"/eda_board.sh" $id $name $d 2>&1 | tail -10
timeout 300 "$P" ""$(dirname "$0")"/eda_save.py" $name 2>&1 | tail -1
