#!/bin/bash
# bisect.sh DIR : remove dangling items in groups; a group that raises unconnected is split in halves (down to single items)
W="C:/Users/karpa/AppData/Local/Temp/claude/da5cb96d4386b7ca/b4e53a53-8857-4bd0-ba5f-77737f7bc4cd/scratchpad/I2"; R=/c/Users/karpa/Documents/Shtuka-druka/hardware/m1-screen-knobs
PY="/c/Program Files/KiCad/10.0/bin/python.exe"; K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"; cd $W; d=$1
dr(){ cp $R/m1-screen-knobs.kicad_pro $d/; "$K" pcb drc --severity-all --schematic-parity --format json -o $W/drc_$d.json $d/m1-screen-knobs.kicad_pcb >/dev/null 2>&1; node -e "const j=require('$W/drc_$d.json');console.log(j.unconnected_items.length+j.violations.filter(v=>v.severity=='error').length)"; }
base=$(dr); echo "start (unconnected+errors) $base"
try(){ # $1 = file with uuids
  cp $d/m1-screen-knobs.kicad_pcb $d/bk.kicad_pcb; node rm.js $d/m1-screen-knobs.kicad_pcb $d/x.kicad_pcb $1 >/dev/null; mv $d/x.kicad_pcb $d/m1-screen-knobs.kicad_pcb
  u=$(dr); if [ "$u" -le "$base" ]; then base=$u; echo "  removed $(wc -l < $1 | tr -d ' ')+ ok ($u)"; return 0; fi
  cp $d/bk.kicad_pcb $d/m1-screen-knobs.kicad_pcb; echo "  group of $(($(wc -l < $1)+1)) breaks"; return 1; }
for round in 1 2 3; do
  dr >/dev/null
  node -e "const d=require('$W/drc_$d.json');const ids=new Set();for(const v of d.violations){if(/track_dangling|via_dangling/.test(v.type))ids.add(v.items[0].uuid);if(v.type=='holes_co_located')ids.add(v.items[1].uuid)}require('fs').writeFileSync('$W/all.txt',[...ids].join('\n'));console.log('round $round dangling',ids.size)"
  [ -s all.txt ] || break
  # queue of groups: start with groups of 8
  split -l 8 -d all.txt grp_; progress=0
  for g in grp_*; do
    if try $g; then progress=1; else
      split -l 2 -d $g sub_; for s in sub_*; do if try $s; then progress=1; else split -l 1 -d $s one_; for o in one_*; do try $o && progress=1; done; rm -f one_*; fi; done; rm -f sub_*
    fi
  done; rm -f grp_*
  [ $progress = 1 ] || break
done
rm -f $d/bk.kicad_pcb; "$PY" -I -u refill.py $d/m1-screen-knobs.kicad_pcb $d/m1-screen-knobs.kicad_pcb 2>&1 | grep refilled
cp $R/m1-screen-knobs.kicad_pro $d/; "$K" pcb drc --severity-all --schematic-parity --format json -o $W/drc_$d.json $d/m1-screen-knobs.kicad_pcb 2>&1 | grep Found | tr '\n' ' '; echo "<- $d final"
