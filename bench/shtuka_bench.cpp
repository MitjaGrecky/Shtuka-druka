// Shtuka Druka DSP benchmark: how many reference tracks a CPU can run.
// License: AGPL-3.0-or-later (project decision R20/P27).
// Build: g++ -O2 -march=native -std=c++20 -pthread shtuka_bench.cpp -o shtuka_bench
// Windows (cross): x86_64-w64-mingw32-g++-posix -O2 -march=haswell -std=c++20 -static shtuka_bench.cpp -o shtuka_bench.exe -lwinmm
#include <algorithm>
#include <atomic>
#include <barrier>
#include <chrono>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <memory>
#include <random>
#include <string>
#include <thread>
#include <vector>
#ifdef _WIN32
#include <windows.h>
#else
#include <pthread.h>
#include <sched.h>
#include <sys/mman.h>
#endif

static int SR = 48000;
static int BLOCK = 128;
static int VOICES = 8;
static constexpr float PI = 3.14159265358979f;

struct Rng { uint32_t s; explicit Rng(uint32_t x) : s(x) {} float next() { s ^= s << 13; s ^= s >> 17; s ^= s << 5; return (s & 0xFFFFFF) / 16777216.0f; } };

struct SVF {  // Cytomic/Simper state-variable filter, low-pass
  float ic1 = 0, ic2 = 0, g = 0, k = 1, a1 = 0, a2 = 0, a3 = 0;
  void set(float fc, float q) { g = std::tan(PI * std::min(fc, 20000.f) / SR); k = 1.f / q; a1 = 1.f / (1.f + g * (g + k)); a2 = g * a1; a3 = g * a2; }
  inline float run(float v0) { float v3 = v0 - ic2; float v1 = a1 * ic1 + a2 * v3; float v2 = ic2 + a2 * ic1 + a3 * v3; ic1 = 2 * v1 - ic1; ic2 = 2 * v2 - ic2; return v2; }
};

struct ADSR { float v = 0, a, d, s, r; int stage = 0; ADSR() : a(1.f / (0.01f * SR)), d(1.f / (0.2f * SR)), s(0.6f), r(1.f / (0.3f * SR)) {}
  inline float run() { switch (stage) { case 0: v += a; if (v >= 1) { v = 1; stage = 1; } break; case 1: v -= d; if (v <= s) { v = s; stage = 2; } break; case 2: break; default: v -= r; if (v < 0) v = 0; } return v; } };

static std::vector<float> g_sample;              // 2 s mono sample
static std::vector<float> g_wavetable;            // 64 frames x 2048
static constexpr int WT_FRAMES = 64, WT_LEN = 2048;

static void make_tables() {
  g_sample.resize(2 * SR);
  Rng r(7);
  for (int i = 0; i < 2 * SR; i++) { float t = i / float(SR); g_sample[i] = 0.5f * std::sin(2 * PI * 110 * t) * std::exp(-2 * t) + 0.2f * (r.next() * 2 - 1) * std::exp(-8 * t); }
  g_wavetable.resize(WT_FRAMES * WT_LEN);
  for (int f = 0; f < WT_FRAMES; f++)
    for (int i = 0; i < WT_LEN; i++) {
      float ph = 2 * PI * i / WT_LEN, v = 0;
      int harm = 1 + f / 2;
      for (int h = 1; h <= harm; h++) v += std::sin(ph * h) / h;
      g_wavetable[f * WT_LEN + i] = v * 0.4f;
    }
}

static inline float cubic(const float* d, int n, double pos) {
  int i = int(pos); float t = float(pos - i);
  float y0 = d[std::max(i - 1, 0)], y1 = d[i], y2 = d[std::min(i + 1, n - 1)], y3 = d[std::min(i + 2, n - 1)];
  float c1 = 0.5f * (y2 - y0), c2 = y0 - 2.5f * y1 + 2 * y2 - 0.5f * y3, c3 = 0.5f * (y3 - y0) + 1.5f * (y1 - y2);
  return ((c3 * t + c2) * t + c1) * t + y1;
}

struct Track {
  bool synth; int voices = VOICES; Rng rng;
  double pos[32]{}; double rate[32]{}; float phase[32]{}, inc[32]{}, morph[32]{};
  SVF vf[32]; ADSR env[32];
  SVF fL, fR; float lfo = 0;
  std::vector<float> outL, outR;
  float sendA = 0.3f, sendB = 0.2f; std::vector<float> cb = std::vector<float>(2048, 0.f); int ci = 0; float envf = 0;
  Track(bool s, uint32_t seed) : synth(s), rng(seed) {
    for (int v = 0; v < voices; v++) {
      rate[v] = 0.5 + rng.next(); pos[v] = rng.next() * SR;
      float f = 55.f * std::pow(2.f, rng.next() * 4);
      inc[v] = f / SR; morph[v] = rng.next() * (WT_FRAMES - 2);
      vf[v].set(800 + 4000 * rng.next(), 0.9f);
    }
    outL.assign(1024, 0); outR.assign(1024, 0);
  }
  void process(int n) {
    lfo += 0.002f * n; float cutoff = 1200 + 900 * std::sin(lfo);
    fL.set(cutoff, 1.2f); fR.set(cutoff * 1.01f, 1.2f);
    for (int i = 0; i < n; i++) {
      float mix = 0;
      if (!synth) {
        for (int v = 0; v < voices; v++) {
          pos[v] += rate[v]; if (pos[v] >= g_sample.size() - 4) pos[v] = 0;
          mix += vf[v].run(cubic(g_sample.data(), int(g_sample.size()), pos[v])) * env[v].run();
        }
      } else {
        for (int v = 0; v < voices; v++) {
          phase[v] += inc[v]; if (phase[v] >= 1) phase[v] -= 1;
          morph[v] += 0.00002f; if (morph[v] > WT_FRAMES - 2) morph[v] = 0;
          int f0 = int(morph[v]); float mf = morph[v] - f0;
          double p = phase[v] * WT_LEN;
          float a = cubic(&g_wavetable[f0 * WT_LEN], WT_LEN, p), b = cubic(&g_wavetable[(f0 + 1) * WT_LEN], WT_LEN, p);
          double p2 = std::fmod(phase[v] * 1.0071 + 0.31, 1.0) * WT_LEN;
          float c = cubic(&g_wavetable[f0 * WT_LEN], WT_LEN, p2), d = cubic(&g_wavetable[(f0 + 1) * WT_LEN], WT_LEN, p2);
          float s = (a + (b - a) * mf) + (c + (d - c) * mf);
          mix += vf[v].run(s) * env[v].run();
        }
      }
      mix *= 0.15f;
      float l = std::tanh(1.8f * fL.run(mix)), r = std::tanh(1.8f * fR.run(mix * 0.97f));
      cb[ci] = 0.5f * (l + r); float md = 240 + 80 * std::sin(lfo * 7 + i * 0.0003f); float rp = ci - md; if (rp < 0) rp += 2048;
      float ch = cubic(cb.data(), 2048, rp); if (++ci >= 2048) ci = 0;
      l += 0.3f * ch; r -= 0.3f * ch;
      float lv = std::fabs(l) + std::fabs(r); envf += (lv > envf ? 0.01f : 0.0005f) * (lv - envf);
      float gr = envf > 0.5f ? 0.5f / envf : 1.f; l *= gr; r *= gr;
      outL[i] = l; outR[i] = r;
    }
  }
};

struct Comb { std::vector<float> b; int i = 0; float fs = 0, fb = 0.84f, damp = 0.2f;
  explicit Comb(int n) : b(n, 0) {} inline float run(float x) { float y = b[i]; fs = y * (1 - damp) + fs * damp; b[i] = x + fs * fb; if (++i >= (int)b.size()) i = 0; return y; } };
struct Allp { std::vector<float> b; int i = 0; explicit Allp(int n) : b(n, 0) {}
  inline float run(float x) { float y = b[i]; float o = -x + y; b[i] = x + y * 0.5f; if (++i >= (int)b.size()) i = 0; return o; } };
struct Reverb {  // Freeverb-like: 8 combs + 4 allpasses per channel
  std::vector<Comb> cl, cr; std::vector<Allp> al, ar;
  Reverb() { int c[8] = {1116, 1188, 1277, 1356, 1422, 1491, 1557, 1617}, a[4] = {556, 441, 341, 225};
    for (int k : c) { cl.emplace_back(k); cr.emplace_back(k + 23); } for (int k : a) { al.emplace_back(k); ar.emplace_back(k + 23); } }
  void process(const float* in, float* L, float* R, int n) {
    for (int i = 0; i < n; i++) { float x = in[i] * 0.015f, l = 0, r = 0;
      for (auto& c : cl) l += c.run(x); for (auto& c : cr) r += c.run(x);
      for (auto& a : al) l = a.run(l); for (auto& a : ar) r = a.run(r);
      L[i] += l; R[i] += r; } }
};
struct Delay { std::vector<float> bl, br; int i = 0, d; SVF tone;
  Delay() : bl(SR, 0), br(SR, 0), d(SR * 3 / 8) { tone.set(3000, 0.7f); }
  void process(const float* in, float* L, float* R, int n) {
    for (int k = 0; k < n; k++) { int j = (i - d + SR) % SR; float yl = bl[j], yr = br[j];
      bl[i] = in[k] + tone.run(yr) * 0.45f; br[i] = yl * 0.45f; L[k] += yl; R[k] += yr; if (++i >= SR) i = 0; } }
};

struct Engine {
  int ntracks, nthreads; std::vector<std::unique_ptr<Track>> tracks;
  Reverb rv[2]; Delay dl[2];
  std::vector<float> busA, busB, busC, busD, mL, mR;
  std::unique_ptr<std::barrier<>> start, done; std::vector<std::thread> workers; std::atomic<bool> stop{false};
  Engine(int n, int t) : ntracks(n), nthreads(t) {
    for (int i = 0; i < n; i++) tracks.emplace_back(std::make_unique<Track>(i % 2 == 1, 1234 + i));
    busA.assign(1024, 0); busB = busA; busC = busA; busD = busA; mL = busA; mR = busA;
    start = std::make_unique<std::barrier<>>(t); done = std::make_unique<std::barrier<>>(t);
    for (int w = 1; w < t; w++) workers.emplace_back([this, w] { while (true) { start->arrive_and_wait(); if (stop) break; work(w); done->arrive_and_wait(); } });
  }
  ~Engine() { stop = true; if (nthreads > 1) start->arrive_and_wait(); for (auto& w : workers) w.join(); }
  void work(int w) { for (int i = w; i < ntracks; i += nthreads) tracks[i]->process(BLOCK); }
  void block() {
    if (nthreads > 1) start->arrive_and_wait();
    work(0);
    if (nthreads > 1) done->arrive_and_wait();
    int n = BLOCK;
    std::fill(busA.begin(), busA.begin() + n, 0.f); std::fill(busB.begin(), busB.begin() + n, 0.f);
    std::fill(busC.begin(), busC.begin() + n, 0.f); std::fill(busD.begin(), busD.begin() + n, 0.f);
    std::fill(mL.begin(), mL.begin() + n, 0.f); std::fill(mR.begin(), mR.begin() + n, 0.f);
    for (auto& t : tracks) for (int i = 0; i < n; i++) {
      float m = 0.5f * (t->outL[i] + t->outR[i]);
      busA[i] += m * t->sendA; busB[i] += m * t->sendB; busC[i] += m * 0.1f; busD[i] += m * 0.1f;
      mL[i] += t->outL[i] * 0.2f; mR[i] += t->outR[i] * 0.2f; }
    rv[0].process(busA.data(), mL.data(), mR.data(), n); rv[1].process(busC.data(), mL.data(), mR.data(), n);
    dl[0].process(busB.data(), mL.data(), mR.data(), n); dl[1].process(busD.data(), mL.data(), mR.data(), n);
    for (int i = 0; i < n; i++) { mL[i] = std::tanh(mL[i]); mR[i] = std::tanh(mR[i]); }
  }
};

struct Result { double avg, p99, mx; long overruns, blocks; };

static Result run(int ntr, int nthr, double seconds, bool realtime) {
  Engine e(ntr, nthr);
  const double period = double(BLOCK) / SR;
  long nb = long(seconds / period);
  std::vector<double> t(nb);
  for (int i = 0; i < 200; i++) e.block();  // warm-up
  auto next = std::chrono::steady_clock::now();
  long over = 0;
  for (long b = 0; b < nb; b++) {
    if (realtime) { next += std::chrono::nanoseconds(long(period * 1e9)); }
    auto a = std::chrono::steady_clock::now();
    e.block();
    auto z = std::chrono::steady_clock::now();
    t[b] = std::chrono::duration<double>(z - a).count() / period;
    if (realtime) { if (z > next) { over++; next = z; } else std::this_thread::sleep_until(next); }
  }
  std::vector<double> s = t; std::sort(s.begin(), s.end());
  double avg = 0; for (double v : t) avg += v; avg /= nb;
  if (!realtime) for (double v : t) if (v > 1.0) over++;
  return {avg * 100, s[size_t(nb * 0.99)] * 100, s.back() * 100, over, nb};
}

static void try_realtime_priority() {
#ifdef _WIN32
  // Windows: highest priority class a normal user may set, plus 1 ms timer resolution
  timeBeginPeriod(1);
  if (SetPriorityClass(GetCurrentProcess(), HIGH_PRIORITY_CLASS) &&
      SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_TIME_CRITICAL))
    std::printf("# realtime priority: on (Windows HIGH_PRIORITY_CLASS, TIME_CRITICAL)\n");
  else std::printf("# realtime priority: off\n");
  std::printf("# memory locked: no (Windows)\n");
#else
  sched_param sp{}; sp.sched_priority = 80;
  if (pthread_setschedparam(pthread_self(), SCHED_FIFO, &sp) == 0) std::printf("# realtime priority: on (SCHED_FIFO 80)\n");
  else std::printf("# realtime priority: off (run with sudo or audio group limits for SCHED_FIFO)\n");
  if (mlockall(MCL_CURRENT | MCL_FUTURE) == 0) std::printf("# memory locked: yes\n"); else std::printf("# memory locked: no\n");
#endif
}

int main(int argc, char** argv) {
  int tracks = 0, threads = 0; double secs = 0; bool rt = false;
  for (int i = 1; i < argc; i++) {
    std::string a = argv[i];
    if (a == "--tracks" && i + 1 < argc) tracks = std::atoi(argv[++i]);
    else if (a == "--threads" && i + 1 < argc) threads = std::atoi(argv[++i]);
    else if (a == "--seconds" && i + 1 < argc) secs = std::atof(argv[++i]);
    else if (a == "--block" && i + 1 < argc) BLOCK = std::atoi(argv[++i]);
    else if (a == "--voices" && i + 1 < argc) VOICES = std::max(1, std::min(32, std::atoi(argv[++i])));
    else if (a == "--rate" && i + 1 < argc) SR = std::atoi(argv[++i]);
    else if (a == "--realtime") rt = true;
    else { std::printf("usage: shtuka_bench [--tracks N --threads T --seconds S --block 128 --rate 48000 --voices 8 --realtime]\n"); return 1; }
  }
  make_tables();
  int cores = int(std::thread::hardware_concurrency());
  std::printf("# Shtuka Druka DSP benchmark. %d Hz, block %d (%.2f ms). Reference track: %d voices with filter+envelope (odd = wavetable synth, 2 osc/voice; even = sampler), track filter, drive, chorus, compressor, 4 sends; buses: 2 reverbs, 2 delays.\n", SR, BLOCK, 1000.0 * BLOCK / SR, VOICES);
  std::printf("# Load = processing time / block time. Capacity: p99 < 70%% (offline sweep). Stability: overruns in the 30 s realtime check (depends on kernel and system noise).\n");
  try_realtime_priority();
  if (tracks > 0) {
    int th = threads > 0 ? threads : cores;
    Result r = run(tracks, th, secs > 0 ? secs : 60, rt);
    std::printf("tracks=%d threads=%d mode=%s avg=%.1f%% p99=%.1f%% max=%.1f%% overruns=%ld/%ld\n", tracks, th, rt ? "realtime" : "offline", r.avg, r.p99, r.mx, r.overruns, r.blocks);
    return 0;
  }
  std::vector<int> ths = {1}; if (cores > 1) ths.push_back(cores);
  std::printf("%-8s %-7s %-8s %-8s %-8s %-9s %s\n", "threads", "tracks", "avg%", "p99%", "max%", "overruns", "verdict");
  for (int th : ths) {
    int best = 0;
    for (int n = 4; n <= 256; n += (n < 32 ? 4 : n < 64 ? 8 : 16)) {
      Result r = run(n, th, secs > 0 ? secs : 5, false);
      bool pass = r.p99 < 70;
      std::printf("%-8d %-7d %-8.1f %-8.1f %-8.1f %-9ld %s\n", th, n, r.avg, r.p99, r.mx, r.overruns, pass ? "pass" : "FAIL");
      std::fflush(stdout);
      if (pass) best = n; else break;
    }
    std::printf("# threads=%d: max reference tracks that pass = %d\n", th, best);
    if (best > 0) {
      Result r = run(best, th, 30, true);
      std::printf("# realtime check 30 s, %d tracks, %d threads: avg=%.1f%% p99=%.1f%% max=%.1f%% overruns=%ld/%ld\n", best, th, r.avg, r.p99, r.mx, r.overruns, r.blocks);
    }
  }
  return 0;
}
