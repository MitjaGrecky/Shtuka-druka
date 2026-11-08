#!/bin/bash
W="C:/Users/karpa/AppData/Local/Temp/claude/da5cb96d4386b7ca/b4e53a53-8857-4bd0-ba5f-77737f7bc4cd/scratchpad/I2"; R=/c/Users/karpa/Documents/Shtuka-druka/hardware/m1-screen-knobs
PY="/c/Program Files/KiCad/10.0/bin/python.exe"; K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"; cd $W
REF=s2/m1-screen-knobs.kicad_pcb
mk(){ rm -rf $1; mkdir -p $1; cp $R/m1-screen-knobs.kicad_sch $1/; cp -r $R/lib $R/fp-lib-table $R/sym-lib-table $1/; }
drcrun(){ cp $R/m1-screen-knobs.kicad_pro $1/; "$K" pcb drc --severity-all --schematic-parity --format json -o $W/drc_$1.json $1/m1-screen-knobs.kicad_pcb 2>&1 | grep Found | tr '\n' ' '; echo "<- $1"; }
nets(){ node -e "const d=require('$W/drc_$1.json');const s=new Set();d.unconnected_items.forEach(u=>{const n=u.items[0].description.match(/\[(.*?)\]/)[1];if($2)s.add(n)});console.log([...s].join(','))"; }
route(){ src=$1; dst=$2; drc=$3; only=$4; tiers=$5; g=${6:-0.05}; mk $dst; MSYS_NO_PATHCONV=1 G=$g TLIM=70 TIERS="$tiers" ONLY="$only" "$PY" -I -u route.py $src/m1-screen-knobs.kicad_pcb $dst/r.kicad_pcb $drc 2>&1 | grep "^(" | cut -c1-150
  "$PY" -I -u tjunc.py $dst/r.kicad_pcb $dst/m1-screen-knobs.kicad_pcb $REF 2>&1 | grep split; rm -f $dst/r.*; drcrun $dst; }
route s2 q1 drc_s2.json "$(nets s2 "n!='+5V'")" "((0.12,0.14),(0.12,0.13))"
route q1 q2 drc_q1.json "+5V" "((0.3,0.14),(0.25,0.13),(0.2,0.13))"
mk q3; "$PY" -I -u gndstub.py q2/m1-screen-knobs.kicad_pcb q3/m1-screen-knobs.kicad_pcb 2>&1 | grep stub; drcrun q3
route q3 q4 drc_q3.json "$(nets q3 "n!='GND'")" "((0.12,0.13),(0.1,0.13))"
bash clean.sh q4
