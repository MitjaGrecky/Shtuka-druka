n=$1; S=$2; PY="/c/Program Files/KiCad/10.0/bin/python.exe"; K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"; cd $S
"$PY" -I imp2.py $n 2>&1 | grep -v "duplicate image\|memory leak"; mkdir -p ${n}_drc; cp $n/routed.kicad_pcb ${n}_drc/m1-screen-knobs.kicad_pcb; cp $n/m1-screen-knobs.kicad_pro $n/m1-screen-knobs.kicad_sch ${n}_drc/
"$K" pcb drc --severity-all --schematic-parity --format json -o $S/drc_$n.json ${n}_drc/m1-screen-knobs.kicad_pcb 2>&1 | grep -c Found >/dev/null
node -e "const d=require('$S/drc_$n.json');const gnd=d.unconnected_items.filter(u=>/\[GND\]/.test(u.items[0].description)).length;const c={};for(const v of d.violations.filter(v=>v.severity=='error'))c[v.type]=(c[v.type]||0)+1;console.log('$n unconnected',d.unconnected_items.length,'GND',gnd,'signal',d.unconnected_items.length-gnd,'errors',JSON.stringify(c))"
"$PY" -I st.py ${n}_drc/m1-screen-knobs.kicad_pcb 2>&1 | grep -v "duplicate image\|memory leak"
