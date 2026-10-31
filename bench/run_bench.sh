#!/usr/bin/env bash
# Shtuka Druka: CPU benchmark. Usage: ./run_bench.sh   (takes about 10-15 minutes)
set -e
cd "$(dirname "$0")"
OUT="$HOME/shtuka_bench_results.txt"
if ! command -v g++ >/dev/null; then
  echo "Installing compiler (needs password)..."; sudo apt-get update && sudo apt-get install -y build-essential
fi
g++ -O2 -march=native -std=c++20 -pthread shtuka_bench.cpp -o shtuka_bench
echo "Realtime priority needs sudo:"; sudo -v
{
  echo "=== Shtuka Druka benchmark, $(date -Iseconds) ==="
  echo "CPU: $(grep -m1 'model name' /proc/cpuinfo | cut -d: -f2)"
  echo "Cores/threads: $(nproc)"
  echo "RAM: $(free -h | awk '/Mem:/{print $2}')"
  echo "Kernel: $(uname -r)   preempt: $(cat /sys/kernel/realtime 2>/dev/null || uname -v | grep -o 'PREEMPT[_A-Z]*' | head -1)"
  echo "Governor: $(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo unknown)"
  echo
  echo "--- 1. Sweep, 8 voices per track ---"
  sudo ./shtuka_bench --seconds 5
  echo
  echo "--- 2. Target 16 tracks (R11), all threads, 60 s realtime ---"
  sudo ./shtuka_bench --tracks 16 --seconds 60 --realtime
  echo
  echo "--- 3. Heavy synths: 16 voices per track, sweep ---"
  sudo ./shtuka_bench --seconds 3 --voices 16
} 2>&1 | tee "$OUT"
echo
echo "Done. Send this file to Claude: $OUT"
