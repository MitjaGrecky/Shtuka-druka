"""Shtuka Druka Panel protocol (SDP) v0.0 - host-side reference codec and self-test.
Spec: docs/ru/19_panel_protocol.md.  SPDX-License-Identifier: AGPL-3.0-or-later

Usage:
  python3 tools/sdp.py --selftest          run codec tests
  python3 tools/sdp.py --listen /dev/ttyACM0   print decoded frames from a board (needs pyserial)
"""
import struct
import sys

VERSION = 0x00
MAX_PAYLOAD = 1536
TYPES = {0x01: 'HELLO', 0x02: 'PING', 0x03: 'PONG', 0x04: 'ACK', 0x05: 'NACK', 0x06: 'LOG', 0x0F: 'HEARTBEAT',
         0x7F: 'BOOTLOADER', 0x10: 'PAD', 0x11: 'PAD_PRESSURE', 0x12: 'BUTTON', 0x13: 'ENCODER', 0x14: 'ENC_PUSH',
         0x15: 'ENC_TOUCH', 0x16: 'ANALOG', 0x20: 'LED_SET', 0x21: 'LED_FRAME', 0x22: 'LED_ANIM',
         0x23: 'LED_BRIGHTNESS', 0x24: 'TEMPO', 0x28: 'CONFIG_PADS', 0x29: 'CONFIG_ENC', 0x30: 'CV_SET',
         0x31: 'GATE', 0x32: 'CV_MODE', 0x33: 'CV_IN', 0x34: 'CLOCK_CFG', 0x35: 'TRANSPORT', 0x36: 'CLOCK_IN',
         0x37: 'MIDI_TRS_TYPE', 0x38: 'MUTE', 0x39: 'MIDI_OUT_TS'}
NAME = {v: k for k, v in TYPES.items()}


def crc16(data: bytes) -> int:
    c = 0xFFFF
    for b in data:
        c ^= b << 8
        for _ in range(8):
            c = ((c << 1) ^ 0x1021) & 0xFFFF if c & 0x8000 else (c << 1) & 0xFFFF
    return c


def cobs_encode(data: bytes) -> bytes:
    out, block = bytearray(), bytearray()
    for b in data:
        if b == 0:
            out += bytes([len(block) + 1]) + block
            block = bytearray()
        else:
            block.append(b)
            if len(block) == 254:
                out += bytes([255]) + block
                block = bytearray()
    out += bytes([len(block) + 1]) + block
    return bytes(out)


def cobs_decode(data: bytes) -> bytes:
    out, i = bytearray(), 0
    while i < len(data):
        code = data[i]
        if code == 0 or i + code > len(data):
            raise ValueError('bad COBS')
        out += data[i + 1:i + code]
        i += code
        if code != 0xFF and i < len(data):
            out.append(0)
    return bytes(out)


def frame(type_name: str, seq: int, payload: bytes = b'') -> bytes:
    if len(payload) > MAX_PAYLOAD:
        raise ValueError('payload too long')
    raw = bytes([VERSION, NAME[type_name], seq & 0xFF]) + payload
    raw += struct.pack('<H', crc16(raw))
    return cobs_encode(raw) + b'\x00'


def parse(encoded: bytes):
    raw = cobs_decode(encoded)
    if len(raw) < 5:
        raise ValueError('short frame')
    if struct.unpack('<H', raw[-2:])[0] != crc16(raw[:-2]):
        raise ValueError('CRC mismatch')
    if raw[0] >> 4 != VERSION >> 4:
        raise ValueError('protocol major version mismatch')
    return TYPES.get(raw[1], hex(raw[1])), raw[2], raw[3:-2]


class Stream:
    """Splits a byte stream into frames on 0x00 and decodes them; bad frames are counted and skipped."""
    def __init__(self):
        self.buf, self.errors = bytearray(), 0

    def feed(self, data: bytes):
        for b in data:
            if b == 0:
                if self.buf:
                    try:
                        yield parse(bytes(self.buf))
                    except ValueError:
                        self.errors += 1
                self.buf.clear()
            else:
                self.buf.append(b)


def pad(pad_id, event, velocity, t_us):
    return struct.pack('<BBHI', pad_id, event, velocity, t_us)


def encoder(enc_id, delta, t_us):
    return struct.pack('<BhI', enc_id, delta, t_us)


def selftest():
    assert crc16(b'123456789') == 0x29B1, 'CRC-16/CCITT-FALSE check value'
    for case in [b'', b'\x00', b'\x00\x00', b'\x11\x22\x00\x33', bytes(range(1, 255)), bytes(range(256)) * 5]:
        assert cobs_decode(cobs_encode(case)) == case, case[:8]
        assert 0 not in cobs_encode(case)
    s = Stream()
    wire = frame('PAD', 7, pad(12, 1, 51234, 123456)) + b'\x13\x37garbage\x00' + frame('ENCODER', 8, encoder(3, -5, 99))
    leds = bytes((i * 7) & 0xFF for i in range(430 * 3))
    wire += frame('LED_FRAME', 9, leds)
    got = list(s.feed(wire))
    assert got[0][0] == 'PAD' and struct.unpack('<BBHI', got[0][2]) == (12, 1, 51234, 123456)
    assert got[1][0] == 'ENCODER' and struct.unpack('<BhI', got[1][2]) == (3, -5, 99)
    assert got[2][0] == 'LED_FRAME' and got[2][2] == leds
    assert s.errors == 1
    print('SDP selftest: OK (crc, cobs, stream resync, 1290-byte LED frame = %d bytes on the wire)' % len(frame('LED_FRAME', 0, leds)))


if __name__ == '__main__':
    if '--selftest' in sys.argv:
        selftest()
    elif '--listen' in sys.argv:
        import serial  # pip install pyserial
        port = serial.Serial(sys.argv[sys.argv.index('--listen') + 1], timeout=0.1)
        st = Stream()
        while True:
            for t, seq, p in st.feed(port.read(4096)):
                print(t, seq, p.hex())
    else:
        print(__doc__)
