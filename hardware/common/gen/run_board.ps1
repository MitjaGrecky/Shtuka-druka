# PC (Windows, KiCad 10): regenerate one kit-based board and check it.
#   powershell -File hardware/common/gen/run_board.ps1 <project-dir-name> <ID>
# Steps: KiCad-7 symbols, design summary, schematic, netlist check, ERC, board, DRC + parity, EasyEDA package.
# License: AGPL-3.0-or-later.
param([Parameter(Mandatory)][string]$Proj, [Parameter(Mandatory)][string]$Id)
$ErrorActionPreference = 'Stop'
$repo = (Resolve-Path "$PSScriptRoot\..\..\..").Path
$kbin = 'C:\Program Files\KiCad\10.0\bin'
$py = "$kbin\python.exe"; $cli = "$kbin\kicad-cli.exe"
$env:KICAD_SYMBOL_DIR = "$repo\hardware\common\sym7"
$env:KICAD_FOOTPRINT_DIR = 'C:\Program Files\KiCad\10.0\share\kicad\footprints'
$gen = "$repo\hardware\$Proj\gen"
& $py "$repo\hardware\common\gen\sym7.py" | Out-Null
Push-Location $gen
try {
    & $py design.py
    & $py make_sch.py
    & $py check_netlist.py | Select-Object -Last 3
    New-Item -ItemType Directory -Force "$repo\logs\$Id" | Out-Null
    & $cli sch erc --severity-all -o "$repo\logs\$Id\erc.rpt" "$repo\hardware\$Proj\$Proj.kicad_sch" | Out-Null
    Select-String -Path "$repo\logs\$Id\erc.rpt" -Pattern 'ERC messages'
    & $py make_pcb.py
} finally { Pop-Location }
& $py -I "$repo\tools\pc_check.py" "$repo\hardware\$Proj\$Proj.kicad_pcb" | Select-String '^\| `'
& $py "$repo\tools\pack_easyeda.py" $Id "$repo\hardware\$Proj" | Select-Object -Last 1
