"""PT - test board of the pads, 4 x 4 (R194, P120): one source of truth for the schematic and the placed board.

16 pads on the 28 x 25 mm grid of the panel, each a 21 x 17 mm comb with four zones and a light slot in the middle:
full factorial of comb 7 / 10 mil, zones quadrants / triangles, slot 3.1 / 4.0 mm - eight combinations, once in the left
two columns (silicone foot V1) and once in the right two (foot V3). 64 zones are read like the 64 pads of P2 (common
electrode to +3V3A, 10 k pull-down per zone, 8 x 74HC4051 + ADC128S102), 16 reverse-mount RGB LEDs on one LP5864.
Controller: a Raspberry Pi Pico 2 module on headers, GPIO map as on P2. Footprints of the pads and LEDs: footprints.py.
License: AGPL-3.0-or-later (code), CERN-OHL-S-2.0 (the generated board).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402
import footprints as F  # noqa: E402

NAME = "pt-padtest"
ID = "PT"
TITLE = "PT - Pad test board 4 x 4: comb 7/10 mil, quadrant/triangle zones, light slot 3/4 mm, Pico 2 readout"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("Pico 2 module (USB) -> 8 x 74HC4051 + ADC128S102 (64 zones, SPI0) and LP5864 (16 RGB, I2C0); GPIO map as on P2. "
            "LP5864 firmware: Max_Line_Num 3, data refresh mode 1, 125 kHz, PWM_Phase_Shift on (notes/closing/led_noise.md)")
PWR_FLAG_NETS = ("+3V3A", "VAP")
LAYERS = 2
W, H = 132.0, 164.0
HOLES = [(4.0, 4.0), (128.0, 4.0), (4.0, 160.0), (128.0, 160.0), (4.0, 105.5), (128.0, 105.5)]

TSSOP16 = "Package_SO:TSSOP-16_4.4x5mm_P0.65mm"
X0, Y0, DX, DY = 24.0, 18.0, 28.0, 25.0                      # pad centres: panel pitch 28 x 25 (doc 27)
ROWS = (("quad", "31"), ("quad", "40"), ("tri", "31"), ("tri", "40"))
MILS = ("7", "10", "7", "10")                                 # by column; columns 1-2 foot V1, 3-4 foot V3
HC4051_Y = ("13", "14", "15", "12", "1", "5", "2", "4")


def pads():
    """(number 1..16, row, column, zones kind, comb mil, slot)."""
    return [(4 * r + c + 1, r, c, ROWS[r][0], MILS[c], ROWS[r][1]) for r in range(4) for c in range(4)]


def parts():
    P = []
    n = {"H": 0, "R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "FB": 0, "FSR": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=K.conn_lcsc(fp, f)))

    def R(value, a, b, fp=None, **f):
        K.rc(add, ref("R"), value, a, b, fp, **f)

    def C(value, a, b="GND", fp=None, **f):
        K.rc(add, ref("C"), value, a, b, fp, **f)

    # ---------------------------------------------------------------- pads: electrodes and their LEDs
    for i, r, c, kind, mil, slot in pads():
        zn = "quadrants TL TR BL BR" if kind == "quad" else "triangles top right bottom left"
        add(ref("FSR"), "Connector_Generic:Conn_01x05", f"PAD {i} {kind} {mil}mil S{slot}", "ShtukaDruka:" + F.PAD_NAME.format(kind, mil, slot),
            {"1": "+3V3A", **{str(k + 2): f"Z{i}_{k + 1}" for k in range(4)}},
            Note=f"pad {i} (row {r + 1}, column {c + 1}, foot {'V1' if c < 2 else 'V3'}): comb {mil} mil, zones {zn}; pin 1 common, pins 2-5 zones 1-4; copper only, ENIG")
    for i, r, c, kind, mil, slot in pads():
        line, k = divmod(i - 1, 6)
        add(ref("D"), "ShtukaDruka:RGB_6028_CA", "GL6028RGB01-B", "ShtukaDruka:" + F.LED_NAME.format(slot),
            {"3": f"A_SW{line}", "1": f"A_CS{3 * k}", "2": f"A_CS{3 * k + 1}", "4": f"A_CS{3 * k + 2}"}, LCSC="C51933363",
            Note=f"under pad {i}, bottom side, shines up through the slot; colour of cathodes 1/2/4 to be found on the bench (no datasheet yet)")

    # ---------------------------------------------------------------- readout: 8 x 74HC4051 + ADC128S102 (as P2)
    for m in range(8):
        r, half = divmod(m, 2)
        pa, pb = 4 * r + 2 * half + 1, 4 * r + 2 * half + 2
        nets = [f"Z{pa}_{k}" for k in range(1, 5)] + [f"Z{pb}_{k}" for k in range(1, 5)]
        pins = {"16": "+3V3A", "8": "GND", "7": "GND", "6": "GND", "9": "MUX_S2", "10": "MUX_S1", "11": "MUX_S0", "3": f"ROW{m + 1}_C"}
        pins.update({pin: net for pin, net in zip(HC4051_Y, nets)})
        add(ref("U"), "74xx:74HC4051", "74HC4051", TSSOP16, pins, LCSC="C5645",
            Note=f"pads {pa} (Y0-Y3) and {pb} (Y4-Y7), COM -> ADC channel {m + 1}; Nexperia 74HC4051PW,118")
        C("100n", "+3V3A")
        for net in nets:
            R("10k", net, "GND", Note="divider pull-down, as on P2")
        R("1k", f"ROW{m + 1}_C", f"ROW{m + 1}", Note="series + 1n: anti-alias, as on P2")
        C("1n", f"ROW{m + 1}")
    add(ref("U"), "ShtukaDruka:ADC128S102", "ADC128S102", TSSOP16,
        {"1": "ADC_CS", "16": "ADC_SCK", "14": "ADC_DIN", "15": "ADC_DOUT", "2": "VAP", "13": "VAP", "3": "GND", "12": "GND",
         **{str(4 + k): f"ROW{k + 1}" for k in range(8)}}, LCSC="C206503", Note="12-bit, 8 channels; VA = reference = 3.3 V analog")
    add(ref("FB"), "Device:FerriteBead_Small", "600R", "Resistor_SMD:R_0603_1608Metric", {"1": "+3V3", "2": "+3V3A"}, LCSC="C14709",
        Note="analog 3.3 V for the dividers, the muxes and the ADC")
    C("10u", "+3V3A", fp=K.C0805)
    C("100n", "+3V3A")
    add(ref("FB"), "Device:FerriteBead_Small", "600R", "Resistor_SMD:R_0603_1608Metric", {"1": "+3V3A", "2": "VAP"}, LCSC="C14709",
        Note="reference / ADC supply filter")
    C("10u", "VAP", fp=K.C0805)
    C("1u", "VAP", Note="ADC128S102 datasheet: VA bypass 1 uF + 0.1 uF at the pins")
    C("100n", "VAP")

    # ---------------------------------------------------------------- LEDs: one LP5864, 3 scan lines x 6 pixels
    u = ref("U")
    K.lp5864(add, u, "A", (ref("C"), ref("C"), ref("C"), ref("C")), addr=(0, 0))
    next(p for p in P if p["ref"] == u)["pins"]["14"] = None   # SW3 not used: left open (datasheet)
    R("4.7k", "SDA", "+3V3")
    R("4.7k", "SCL", "+3V3")
    C("100u 16V", "+5V", fp="Capacitor_SMD:CP_Elec_6.3x5.4", LCSC="C7469977", Note="bulk on the USB 5 V next to the LED driver")
    C("10u", "+5V", fp=K.C0805)
    C("10u", "+3V3", fp=K.C0805)

    # ---------------------------------------------------------------- controller: Raspberry Pi Pico 2 module
    pico = {1: "SDA", 2: "SCL", 21: "ADC_DOUT", 22: "ADC_CS", 24: "ADC_SCK", 25: "ADC_DIN", 26: "MUX_S0", 27: "MUX_S1", 29: "MUX_S2",
            36: "+3V3", 40: "+5V", **{g: "GND" for g in (3, 8, 13, 18, 23, 28, 33, 38)}}
    add(ref("J"), "Connector_Generic:Conn_02x20_Odd_Even", "Raspberry Pi Pico 2 (module)", "Module:RaspberryPi_Pico_Common_THT",
        {str(k): pico.get(k) for k in range(1, 41)},
        Note="Pico 2 on two 1x20 headers, symbol pin number = module pin: USB power and data; 3V3(OUT) pin 36, VBUS pin 40; GP0/1 I2C, GP16-19 SPI0, GP20-22 mux address (as P2)")
    K.mount_holes(add, ref, HOLES, "M3 standoff, board stands on the bench")
    return P


def placement():
    """Pads on the panel grid (top), their LEDs under them (bottom), the electronics in the strip below the pads."""
    import packer
    P = parts()
    me = sys.modules[__name__]
    fixed = {}
    fsr = [p["ref"] for p in P if p["ref"].startswith("FSR")]
    led = [p["ref"] for p in P if p["ref"].startswith("D")]
    for (i, r, c, *_), fr, d in zip(pads(), fsr, led):
        xy = (X0 + DX * c, Y0 + DY * r)
        fixed[fr] = xy + (0, "top")
        fixed[d] = xy + (0, "bottom")
    fixed.update(K.hole_fixed(P, HOLES))
    byref = {p["ref"]: p for p in P}

    def at(ref, x, y, rot=0):                                  # place by the top-left corner of the courtyard box
        box, _ = packer._bbox(me, byref[ref], rot, "top")
        fixed[ref] = (round(x - box[0], 2), round(y - box[1], 2), rot, "top")

    pico = next(p["ref"] for p in P if p["ref"].startswith("J"))
    at(pico, 9.0, 138.5, 90)                                  # lying along the lower edge, USB towards the left edge
    ics = [p["ref"] for p in P if p["ref"].startswith("U")]
    muxes, adc, drv = ics[:8], ics[8], ics[9]
    for k, u in enumerate(muxes):
        fixed[u] = (14.0 + 14.9 * k, 111.0, 0, "top")
    fixed[adc] = (72.0, 129.0, 0, "top")
    fixed[drv] = (100.0, 129.0, 0, "top")
    owner = {}
    for k, u in enumerate(muxes):
        nets = {v for v in byref[u]["pins"].values() if v and v.startswith(("Z", "ROW"))} | {f"ROW{k + 1}"}
        owner.update({net: k for net in nets})
    groups = [[] for _ in range(10)]
    for p in P:
        r = p["ref"]
        if r in fixed:
            continue
        hit = [owner[v] for v in p["pins"].values() if v in owner]
        nets = set(p["pins"].values())
        if hit:
            groups[hit[0]].append(r)
        elif nets & {"VAP", "+3V3A"} or r.startswith("FB"):
            groups[8].append(r)
        else:
            groups[9].append(r)
    caps = [r for r in groups[8] if r.startswith("C") and byref[r]["value"] == "100n" and byref[r]["pins"]["1"] == "+3V3A"]
    for k, r in enumerate(caps[:8]):                           # one 100 nF next to each multiplexer
        groups[k].insert(0, r)
        groups[8].remove(r)
    G = [(fixed[u][0], 118.0, "top", groups[k], 0) for k, u in enumerate(muxes)]
    G += [(72.0, 129.0, "top", groups[8], 0), (100.0, 129.0, "top", groups[9], 0)]
    return packer.pack(me, P, fixed, G, [(0.5, 103.5, W - 0.5, H - 0.5)], gap=0.8, ic_gap=1.4)


if __name__ == "__main__":
    P = parts()
    nets = sorted({v for p in P for v in p["pins"].values() if v})
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
    count = {x: sum(1 for p in P for v in p["pins"].values() if v == x) for x in nets}
    print("single-pin nets:", [x for x in nets if count[x] < 2])
