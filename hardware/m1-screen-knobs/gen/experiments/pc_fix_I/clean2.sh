#!/bin/bash
# clean2.sh DIR : remove dangling tracks/vias pass by pass; a pass that increases unconnected is rolled back and stops
W="C:/Users/karpa/AppData/Local/Temp/claude/da5cb96d4386b7ca/b4e53a53-8857-4bd0-ba5f-77737f7bc4cd/scratchpad/I2"; R=/c/Users/karpa/Documents/Shtuka-druka/hardware/m1-screen-knobs
PY="/c/Program Files/KiCad/10.0/bin/python.exe"; K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"; cd $W; d=$1
dr(){ cp $R/m1-screen-knobs.kicad_pro $d/; "$K" pcb drc --severity-all --schematic-parity --format json -o $W/drc_$d.json $d/m1-screen-knobs.kicad_pcb >/dev/null 2>&1; node -e "console.log(require('$W/drc_$d.json').unconnected_items.length)"; }
u0=$(dr); echo "start unconnected $u0"
for i in 1 2 3 4 5 6 7 8; do
  node -e "const d=require('$W/drc_$d.json');const ids=new Set();for(const v of d.violations){if(/track_dangling|via_dangling/.test(v.type))ids.add(v.items[0].uuid);if(v.type=='holes_co_located')ids.add(v.items[1].uuid)}require('fs').writeFileSync('$W/rmd.txt',[...ids].join('\n'));console.log('pass $i remove',ids.size)"
  [ -s rmd.txt ] || break
  cp $d/m1-screen-knobs.kicad_pcb $d/backup.kicad_pcb; node rm.js $d/m1-screen-knobs.kicad_pcb $d/x.kicad_pcb rmd.txt >/dev/null; mv $d/x.kicad_pcb $d/m1-screen-knobs.kicad_pcb
  u=$(dr); echo "  unconnected $u"
  if [ "$u" -gt "$u0" ]; then cp $d/backup.kicad_pcb $d/m1-screen-knobs.kicad_pcb; dr >/dev/null; echo "  rolled back"; break; fi; u0=$u
done
rm -f $d/backup.kicad_pcb; "$PY" -I -u refill.py $d/m1-screen-knobs.kicad_pcb $d/m1-screen-knobs.kicad_pcb 2>&1 | grep refilled
cp $R/m1-screen-knobs.kicad_pro $d/; "$K" pcb drc --severity-all --schematic-parity --format json -o $W/drc_$d.json $d/m1-screen-knobs.kicad_pcb 2>&1 | grep Found | tr '\n' ' '; echo "<- $d final"
