@echo off
rem Shtuka Druka: CPU benchmark on Windows (same runs as run_bench.sh). About 15-20 minutes.
rem Put shtuka_bench.exe next to this file. Results: shtuka_bench_results_windows.txt in this folder.
rem License: AGPL-3.0-or-later.
setlocal
cd /d "%~dp0"
set OUT=%~dp0shtuka_bench_results_windows.txt
> "%OUT%" (
  echo === Shtuka Druka benchmark, Windows, %DATE% %TIME% ===
  powershell -NoProfile -Command "$c=Get-CimInstance Win32_Processor; 'CPU: '+$c.Name; 'Cores/threads: '+$c.NumberOfCores+'/'+$c.NumberOfLogicalProcessors; 'Max clock MHz: '+$c.MaxClockSpeed; 'RAM GB: '+[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory/1GB,1); 'Model: '+(Get-CimInstance Win32_ComputerSystem).Model; 'OS: '+(Get-CimInstance Win32_OperatingSystem).Caption; $b=Get-CimInstance Win32_Battery -ErrorAction SilentlyContinue; if($b){'Power: battery status '+$b.BatteryStatus+' (2 = on AC), charge '+$b.EstimatedChargeRemaining+'%%'}else{'Power: no battery'}"
  powercfg /getactivescheme
  echo.
  echo --- 1. Sweep, 8 voices per track ---
  shtuka_bench.exe --seconds 5
  echo.
  echo --- 2. Target 16 tracks ^(R11^), all threads, 60 s realtime ---
  shtuka_bench.exe --tracks 16 --seconds 60 --realtime
  echo.
  echo --- 3. Heavy synths: 16 voices per track, sweep ---
  shtuka_bench.exe --seconds 3 --voices 16
  echo.
  echo --- 4. 96 kHz, block 256 ^(same 2.67 ms^), sweep ---
  shtuka_bench.exe --seconds 3 --rate 96000 --block 256
  echo.
  echo === done ===
)
type "%OUT%"
echo.
echo Done: %OUT%
