#!/bin/bash
n=$1; f=$2; title=$3; S="C:/Users/karpa/AppData/Local/Temp/claude/f078bbe906961183/b4e53a53-8857-4bd0-ba5f-77737f7bc4cd/scratchpad/F"
K="/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"; E="/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
cd $S/shots; rm -rf svg_$n; mkdir -p svg_$n/raw
"$K" pcb export svg --layers "F.Cu,In2.Cu,B.Cu" --common-layers "Edge.Cuts" --mode-multi --page-size-mode 2 --exclude-drawing-sheet -o svg_$n/raw $S/$f >/dev/null 2>&1
for x in svg_$n/raw/*.svg; do case "$x" in *F_Cu*|*Top*) cp "$x" svg_$n/f.svg;; *B_Cu*|*Bottom*) cp "$x" svg_$n/b.svg;; *) cp "$x" svg_$n/i.svg;; esac; done
cat > svg_$n/sheet.html <<HTML
<html><body style="margin:0;background:#fff;font-family:Arial"><div style="font-size:44px;padding:10px 20px">$title</div>
<div style="padding:0 20px;font-size:28px">Top copper (F.Cu)</div><img src="f.svg" style="width:3960px;margin-left:20px">
<div style="padding:0 20px;font-size:28px">Inner signal layer (In2.Cu)</div><img src="i.svg" style="width:3960px;margin-left:20px">
<div style="padding:0 20px;font-size:28px">Bottom copper (B.Cu)</div><img src="b.svg" style="width:3960px;margin-left:20px">
</body></html>
HTML
"$E" --headless=old --disable-gpu --hide-scrollbars --screenshot="$(cygpath -w "$S/shots/$n.png")" --window-size=4000,2200 "file:///$S/shots/svg_$n/sheet.html" >/dev/null 2>&1
echo "$n: $(ls svg_$n/raw | wc -l) svgs, $(stat -c %s $n.png) bytes"
