SHTUKA DRUKA - CPU BENCHMARK

1. Copy this "bench" folder to your home folder on the M93 (Ubuntu Studio).
2. Open a terminal and run:
     cd ~/bench
     ./run_bench.sh
3. Enter your password when asked. Wait 15-20 minutes, do not run anything else.
4. Send the file ~/shtuka_bench_results.txt to Claude.

What it measures: how many reference tracks (8 voices, filter, drive,
chorus, compressor, 4 sends; 2 reverbs + 2 delays on buses) the CPU can
process at 48 kHz with 128-sample blocks (2.67 ms), keeping p99 load under 70%.

License: AGPL-3.0-or-later.
