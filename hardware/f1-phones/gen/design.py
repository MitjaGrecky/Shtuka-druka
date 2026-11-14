"""F1 - Headphone board (front edge, horizontal, P94): two 6.35 mm stereo jacks (Neutrik NMJ6HCD2, right angle) and one TI OPA1622
per jack. Each channel is a difference amplifier that takes the CS4308P I-V stage pair from A1 (2 Vrms differential full scale, DAC
outputs 5-8 = Phones 1 / Phones 2, R87: the volume is the DAC's digital attenuator) and gives 4 Vrms single-ended: gain 20k / 10k = 2 =
R67 (>= 4 V on 600 Ohm, >= 30 mA on 32 Ohm; the OPA1622 gives +145 / -130 mA).
Single source of truth for the schematic. Research: docs/ru/21_audio_board.md, docs/ru/34_rear_boards_research.md (3); decisions R8, R66,
R67, R87, R137, P94.

Mute (R66, R137): a G6K-2 DPDT per jack, normally open, closes only when MUTE and R2_OK are both high (same logic as the output relays
on R1); the OPA1622 enable pin follows MUTE (held low while R2 boots, thresholds 0.78 / 0.82 V against the device ground, datasheet 7.3.3 and
7.4.2). The enable pin is not a high-impedance output: the relay is the real mute.

Connectors (contract with the other boards): from A1 2x6 audio header (pairs with a ground between them), from PW JST PH 4 (+12 V, GND, -12 V,
+5 V for the relays), from R1 JST PH 3 (MUTE, R2_OK, GND).
Rev 0.1 (14.11.2026, PC) = schematic only.
License: CERN-OHL-S-2.0 (hardware data), AGPL-3.0-or-later (code).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "common", "gen"))
import kit as K  # noqa: E402

NAME = "f1-phones"
ID = "F1"
TITLE = "F1 - Headphones: 2 x NMJ6HCD2, 2 x OPA1622 difference amplifiers x2, mute relays"
REV = "0.1"
M1_LIB = K.M1_LIB
BUS_NOTE = ("From A1: Phones 1 and 2 as differential pairs (2 Vrms FS) -> OPA1622 difference amp x2 -> 10 R -> relay -> NMJ6HCD2; "
            "volume is the DAC's digital attenuator (R87); mute relays need MUTE and R2_OK (R66, R137)")
PWR_FLAG_NETS = ("+12V", "-12V")      # ERC: rails from the connector (+5V already gets the standard flag)
NO_PWR_FLAG = ("+3V3",)
W, H = 100.0, 40.0          # rough: front edge under the headphone columns (model: x 32 and 80 on the slope front); with the board
LAYERS = 2

R0402, C0402, C0603, C0805 = K.R0402, K.C0402, "Capacitor_SMD:C_0603_1608Metric", K.C0805
R0603 = "Resistor_SMD:R_0603_1608Metric"
C1210 = "Capacitor_SMD:C_1210_3225Metric"
SOT23, SOD123 = "Package_TO_SOT_SMD:SOT-23", "Diode_SMD:D_SOD-123"
JACK = "Connector_Audio:Jack_6.35mm_Neutrik_NMJ6HCD2_Horizontal"
VSON10 = "Package_SON:Texas_S-PVSON-N10"
RELAY = ("Relay:Omron_G6K-2", "Relay_SMD:Relay_DPDT_Omron_G6K-2F-Y")
PH = "Connector_JST:JST_PH_B{n}B-PH-K_1x0{n}_P2.00mm_Vertical"


def parts():
    P = []
    n = {"R": 0, "C": 0, "U": 0, "J": 0, "D": 0, "Q": 0, "K": 0}

    def ref(k):
        n[k] += 1
        return f"{k}{n[k]}"

    def add(r, lib, value, fp, pins, **f):
        P.append(dict(ref=r, lib=lib, value=value, fp=fp, pins=pins, fields=f))

    def R(value, a, b, fp=R0402, **f):
        add(ref("R"), "Device:R", value, fp, {"1": a, "2": b}, **f)

    def C(value, a, b="GND", fp=C0402, **f):
        add(ref("C"), "Device:C", value, fp, {"1": a, "2": b}, **f)

    # ---------------------------------------------------------------- connectors
    pairs = ["HP1L_P", "HP1L_N", "GND", "HP1R_P", "HP1R_N", "GND", "HP2L_P", "HP2L_N", "GND", "HP2R_P", "HP2R_N", "GND"]
    add(ref("J"), "Connector_Generic:Conn_02x06_Odd_Even", "from A1", "Connector_PinHeader_2.54mm:PinHeader_2x06_P2.54mm_Vertical",
        {str(i + 1): net for i, net in enumerate(pairs)},
        Note="Phones 1/2 from the CS4308P I-V stages on A1 (outputs 5-8): L+ L- GND R+ R- GND per jack, pins 1-12; twisted pairs, "
        "2 Vrms differential full scale")
    add(ref("J"), "Connector_Generic:Conn_01x04", "from PW", PH.format(n=4), {"1": "+12V", "2": "GND", "3": "-12V", "4": "+5V"},
        Note="+-12 V for the amplifiers, +5 V for the relay coils (PW 'to F1', 4 pins from PW rev 0.5)")
    add(ref("J"), "Connector_Generic:Conn_01x03", "from R1 (mute)", PH.format(n=3), {"1": "MUTE", "2": "R2_OK", "3": "GND"},
        Note="MUTE and R2_OK from R2 via R1 ('to F1' header on R1 rev 0.4); low while R2 boots (R66, R137)")
    for _ in range(2):
        C("10u 25V", "+12V", fp=C1210)
        C("10u 25V", "GND", "-12V", fp=C1210)

    # ---------------------------------------------------------------- mute logic: coils close only with MUTE and R2_OK
    R("1k", "MUTE", "MUTE_G")
    R("100k", "MUTE_G", "GND")
    R("1k", "R2_OK", "R2OK_G")
    R("100k", "R2OK_G", "GND")
    add(ref("Q"), "Transistor_FET:2N7002", "2N7002", SOT23, {"1": "MUTE_G", "2": "COIL_KS", "3": "COIL_K"},
        Note="MUTE and R2_OK in series: the relays close only when both are high")
    add(ref("Q"), "Transistor_FET:2N7002", "2N7002", SOT23, {"1": "R2OK_G", "2": "GND", "3": "COIL_KS"})
    add(ref("D"), "Diode:1N4148W", "1N4148W", SOD123, {"1": "+5V", "2": "COIL_K"}, Note="flyback")

    # ---------------------------------------------------------------- per jack: OPA1622 difference amps, relay, jack
    for k in (1, 2):
        h = f"HP{k}"
        u = ref("U")
        add(u, "Amplifier_Audio:OPA1622", "OPA1622", VSON10,
            {"1": f"{h}L_IP", "2": "+12V", "3": "GND", "4": "-12V", "5": f"{h}R_IP", "6": f"{h}R_IM", "7": f"{h}R_O", "8": f"{h}_EN",
             "9": f"{h}L_O", "10": f"{h}L_IM", "11": "-12V"},
            LCSC="C2876559", Note=f"Phones {k}: two difference amplifiers, gain 2; thermal pad to V-; EN follows MUTE (0.82 V / 0.78 V vs GND pin)")
        R("1k", "MUTE", f"{h}_EN", Note="enable: low while MUTE is low (supply ramp, boot); never left floating")
        R("100k", f"{h}_EN", "GND")
        C("100n 25V", "+12V", fp=C0603)
        C("100n 25V", "-12V", fp=C0603)
        for ch in ("L", "R"):
            c = f"{h}{ch}"
            R("10k", f"{c}_P", f"{c}_IP", fp=R0603, Note="0.1 %: Rin")
            R("10k", f"{c}_N", f"{c}_IM", fp=R0603, Note="0.1 %: Rin")
            R("20k", f"{c}_O", f"{c}_IM", fp=R0603, Note="0.1 %: Rf, gain 2")
            R("20k", f"{c}_IP", "GND", fp=R0603, Note="0.1 %: Rg")
            C("22p C0G", f"{c}_O", f"{c}_IM", fp=C0603, Note="Cf, stability with the cable - check")
            R("10", f"{c}_O", f"{c}_OR", fp=R0603, Note="output build-out; feedback is taken before it")
        # relay: first contact set tip (left), second ring (right); common 11 / 21, normally open 14 / 24
        add(ref("K"), RELAY[0], "G6K-2F-Y 5V", RELAY[1],
            {"A1": "+5V", "A2": "COIL_K", "11": f"{h}L_OR", "12": None, "14": f"{h}_TIP", "21": f"{h}R_OR", "22": None, "24": f"{h}_RING"},
            LCSC="C37516489", Note=f"Phones {k} mute relay: normally open, opens without power (R66, R137)")
        add(ref("J"), "Connector_Audio:AudioJack3_Switch", f"PHONES {k}", JACK,
            {"T": f"{h}_TIP", "TN": None, "R": f"{h}_RING", "RN": None, "S": "GND", "SN": None},
            LCSC="C368502", Note=f"Phones {k}: Neutrik NMJ6HCD2, 6.35 mm stereo, right angle, switched (unused)")
    return P


def placement():
    """Rev 0.1 is the schematic only."""
    return {}


if __name__ == "__main__":
    P = parts()
    nets = sorted({n for p in P for n in p["pins"].values() if n})
    refs = [p["ref"] for p in P]
    print(len(P), "parts,", len(nets), "nets; duplicate refs:", sorted({r for r in refs if refs.count(r) > 1}))
    single = {}
    for p in P:
        for pin, nn in p["pins"].items():
            if nn:
                single.setdefault(nn, []).append(f"{p['ref']}.{pin}")
    print("single-pin nets:", sorted(k for k, v in single.items() if len(v) == 1))
