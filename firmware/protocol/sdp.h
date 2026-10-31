/* Shtuka Druka Panel protocol (SDP) v0.0 - shared by panel firmware, control-board firmware and host.
 * Spec: docs/ru/19_panel_protocol.md
 * Frame: [version][type][seq][payload...][crc16 lo][crc16 hi], COBS-encoded, terminated by 0x00.
 * CRC-16/CCITT-FALSE (poly 0x1021, init 0xFFFF) over version..payload. All multi-byte fields little-endian.
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
#ifndef SDP_H
#define SDP_H
#include <stddef.h>
#include <stdint.h>

#define SDP_VERSION_MAJOR 0
#define SDP_VERSION_MINOR 0
#define SDP_VERSION ((SDP_VERSION_MAJOR << 4) | SDP_VERSION_MINOR)
#define SDP_MAX_PAYLOAD 1536
#define SDP_HEADER 3
#define SDP_CRC 2
#define SDP_MAX_RAW (SDP_HEADER + SDP_MAX_PAYLOAD + SDP_CRC)
#define SDP_MAX_ENCODED (SDP_MAX_RAW + SDP_MAX_RAW / 254 + 2)
#define SDP_BOOT_MAGIC 0x53445042u /* "SDPB" */

enum sdp_board { SDP_BOARD_PANEL = 1, SDP_BOARD_CONTROL = 2 };

enum sdp_type {
  /* common */
  SDP_HELLO = 0x01, SDP_PING = 0x02, SDP_PONG = 0x03, SDP_ACK = 0x04, SDP_NACK = 0x05,
  SDP_LOG = 0x06, SDP_HEARTBEAT = 0x0F, SDP_BOOTLOADER = 0x7F,
  /* panel -> host */
  SDP_PAD = 0x10, SDP_PAD_PRESSURE = 0x11, SDP_BUTTON = 0x12, SDP_ENCODER = 0x13,
  SDP_ENC_PUSH = 0x14, SDP_ENC_TOUCH = 0x15, SDP_ANALOG = 0x16,
  /* host -> panel */
  SDP_LED_SET = 0x20, SDP_LED_FRAME = 0x21, SDP_LED_ANIM = 0x22, SDP_LED_BRIGHTNESS = 0x23,
  SDP_TEMPO = 0x24, SDP_CONFIG_PADS = 0x28, SDP_CONFIG_ENC = 0x29,
  /* control board */
  SDP_CV_SET = 0x30, SDP_GATE = 0x31, SDP_CV_MODE = 0x32, SDP_CV_IN = 0x33, SDP_CLOCK_CFG = 0x34,
  SDP_TRANSPORT = 0x35, SDP_CLOCK_IN = 0x36, SDP_MIDI_TRS_TYPE = 0x37, SDP_MUTE = 0x38, SDP_MIDI_OUT_TS = 0x39,
  /* control board -> audio board front end (doc 21) */
  SDP_PREAMP_GAIN = 0x3A, SDP_PHANTOM = 0x3B, SDP_INPUT_MODE = 0x3C, SDP_CLIP = 0x3D
};

#define SDP_HEARTBEAT_PERIOD_MS 100
#define SDP_HEARTBEAT_TIMEOUT_MS 500

/* Payload layouts (packed, little-endian). */
#pragma pack(push, 1)
typedef struct { uint8_t board, fw_major, fw_minor, fw_patch, hw_rev; uint8_t serial[8]; uint32_t caps; } sdp_hello_t;
typedef struct { uint64_t t_host_us; } sdp_ping_t;
typedef struct { uint64_t t_host_us; uint32_t t_board_us; } sdp_pong_t;
typedef struct { uint8_t pad, event; uint16_t velocity; uint32_t t_us; } sdp_pad_t;
typedef struct { uint8_t id, state; uint32_t t_us; } sdp_button_t;          /* also ENC_PUSH, ENC_TOUCH */
typedef struct { uint8_t id; int16_t delta; uint32_t t_us; } sdp_encoder_t;
typedef struct { uint8_t id; uint16_t value; uint32_t t_us; } sdp_analog_t;
typedef struct { uint16_t first, count; /* followed by count * 3 bytes RGB */ } sdp_led_set_t;
typedef struct { uint16_t led; uint8_t mode, r2, g2, b2; uint16_t period; } sdp_led_anim_t;
typedef struct { uint32_t bpm_milli, phase; uint32_t t_board_us; } sdp_tempo_t;
typedef struct { uint8_t ch; uint16_t value; uint32_t t_board_us; } sdp_cv_set_t;
typedef struct { uint8_t ch, state; uint32_t t_board_us; } sdp_gate_t;
typedef struct { uint32_t bpm_milli, phase; uint8_t running; uint32_t t_board_us; } sdp_transport_t;
typedef struct { uint8_t mask, state; } sdp_mute_t;
typedef struct { uint8_t ch; uint8_t gain_db; } sdp_preamp_gain_t;   /* 0 = unity, 10..65 dB (PGA2500) */
typedef struct { uint8_t ch, on; uint16_t ramp_ms; } sdp_phantom_t;
typedef struct { uint8_t input, mode; } sdp_input_mode_t;            /* phono: 0 = line, 1 = phono */
typedef struct { uint8_t ch; uint16_t peak; uint32_t t_us; } sdp_clip_t;
#pragma pack(pop)

static inline uint16_t sdp_crc16(const uint8_t *d, size_t n) {
  uint16_t c = 0xFFFF;
  for (size_t i = 0; i < n; i++) {
    c ^= (uint16_t)d[i] << 8;
    for (int b = 0; b < 8; b++) c = (c & 0x8000) ? (uint16_t)((c << 1) ^ 0x1021) : (uint16_t)(c << 1);
  }
  return c;
}

/* COBS encode n bytes from in to out (no trailing 0x00). Returns encoded length. */
static inline size_t sdp_cobs_encode(const uint8_t *in, size_t n, uint8_t *out) {
  size_t r = 0, w = 1, code_pos = 0; uint8_t code = 1;
  while (r < n) {
    if (in[r] == 0) { out[code_pos] = code; code_pos = w++; code = 1; }
    else { out[w++] = in[r]; if (++code == 0xFF) { out[code_pos] = code; code_pos = w++; code = 1; } }
    r++;
  }
  out[code_pos] = code;
  return w;
}

/* COBS decode n bytes (without trailing 0x00). Returns decoded length or 0 on error. */
static inline size_t sdp_cobs_decode(const uint8_t *in, size_t n, uint8_t *out) {
  size_t r = 0, w = 0;
  while (r < n) {
    uint8_t code = in[r++];
    if (code == 0) return 0;
    for (uint8_t i = 1; i < code; i++) { if (r >= n) return 0; out[w++] = in[r++]; }
    if (code != 0xFF && r < n) out[w++] = 0;
  }
  return w;
}

/* Build a complete wire frame (COBS + 0x00). Returns bytes written to out (>= SDP_MAX_ENCODED + 1). */
static inline size_t sdp_frame(uint8_t type, uint8_t seq, const void *payload, size_t len, uint8_t *out) {
  uint8_t raw[SDP_MAX_RAW];
  if (len > SDP_MAX_PAYLOAD) return 0;
  raw[0] = SDP_VERSION; raw[1] = type; raw[2] = seq;
  for (size_t i = 0; i < len; i++) raw[SDP_HEADER + i] = ((const uint8_t *)payload)[i];
  uint16_t c = sdp_crc16(raw, SDP_HEADER + len);
  raw[SDP_HEADER + len] = (uint8_t)(c & 0xFF); raw[SDP_HEADER + len + 1] = (uint8_t)(c >> 8);
  size_t m = sdp_cobs_encode(raw, SDP_HEADER + len + SDP_CRC, out);
  out[m] = 0;
  return m + 1;
}

/* Parse one wire frame without its trailing 0x00. Returns payload length, or -1 on error.
 * raw must hold SDP_MAX_RAW bytes; payload starts at raw + SDP_HEADER. */
static inline int sdp_parse(const uint8_t *enc, size_t n, uint8_t *raw, uint8_t *type, uint8_t *seq) {
  size_t m = sdp_cobs_decode(enc, n, raw);
  if (m < SDP_HEADER + SDP_CRC) return -1;
  uint16_t c = (uint16_t)(raw[m - 2] | (raw[m - 1] << 8));
  if (sdp_crc16(raw, m - 2) != c) return -1;
  if ((raw[0] >> 4) != SDP_VERSION_MAJOR) return -1;
  *type = raw[1]; *seq = raw[2];
  return (int)(m - SDP_HEADER - SDP_CRC);
}
#endif
